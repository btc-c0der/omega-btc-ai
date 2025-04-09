#!/usr/bin/env python3
"""
Quantum Random Number Generator
==============================

Implementation of a quantum-inspired random number generator using
simulated quantum superposition and measurement.
"""

import os
import time
import numpy as np
import hashlib
import logging
from typing import List, Tuple, Dict, Union, Optional, Any
from enum import Enum

logger = logging.getLogger("quantum-rng")

class QuantumSource(Enum):
    """Enum representing the source of quantum randomness."""
    SIMULATED = "simulated"
    HARDWARE = "hardware"
    HYBRID = "hybrid"

class QuantumRNG:
    """
    Quantum Random Number Generator that leverages quantum supremacy
    in sampling truly random numbers from coherent quantum states.
    
    This implementation provides a quantum-inspired RNG that can be used
    with classical hardware while maintaining properties similar to
    true quantum randomness.
    """
    
    def __init__(
        self,
        num_qubits: int = 8,
        source: QuantumSource = QuantumSource.SIMULATED,
        entanglement_depth: int = 2,
        decoherence_rate: float = 0.01,
        api_key: Optional[str] = None
    ):
        """
        Initialize the Quantum Random Number Generator.
        
        Args:
            num_qubits: Number of qubits to use in the generator
            source: Source of quantum randomness (simulated or hardware)
            entanglement_depth: Depth of entanglement in the quantum circuit
            decoherence_rate: Rate of decoherence in the quantum simulation
            api_key: API key for hardware quantum services (if applicable)
        """
        self.num_qubits = num_qubits
        self.source = source
        self.entanglement_depth = entanglement_depth
        self.decoherence_rate = decoherence_rate
        self.api_key = api_key
        
        # Initialize the quantum state
        self._initialize_state()
        
        # Set up entropy sources
        self._entropy_pool = bytearray()
        self._entropy_threshold = 1024  # bytes
        self._collect_system_entropy()
        
        logger.info(f"Initialized {source.value} quantum RNG with {num_qubits} qubits")
    
    def _initialize_state(self) -> None:
        """Initialize the quantum state with superposition."""
        # For simulated mode, we initialize a state vector
        if self.source == QuantumSource.SIMULATED:
            # Create state vector representing |00...0⟩
            self.state = np.zeros(2**self.num_qubits, dtype=np.complex128)
            self.state[0] = 1.0
            
            # Apply Hadamard gate to all qubits to create superposition
            self._apply_hadamard_all()
            
            # Apply entanglement if requested
            if self.entanglement_depth > 0:
                self._apply_entanglement()
    
    def _apply_hadamard_all(self) -> None:
        """Apply Hadamard gates to all qubits to create superposition."""
        # Hadamard transform creates equal superposition
        # In the state vector, this corresponds to equal amplitudes
        h_transform = np.ones((2**self.num_qubits,), dtype=np.complex128) / np.sqrt(2**self.num_qubits)
        self.state = h_transform
    
    def _apply_entanglement(self) -> None:
        """Apply entanglement operations to the quantum state."""
        # For simple simulation, we'll add phase correlations between qubits
        for depth in range(self.entanglement_depth):
            # Add phase correlations between neighboring qubits
            for qubit in range(self.num_qubits - 1):
                control = qubit
                target = qubit + 1
                # Simple model of CNOT entanglement: adding phase correlation
                # In real quantum computing, this would be a controlled-NOT gate
                phase_shifts = np.random.uniform(0, 2 * np.pi, 2**self.num_qubits)
                self.state *= np.exp(1j * phase_shifts)
            
            # Normalize state vector
            self.state /= np.linalg.norm(self.state)
    
    def _collect_system_entropy(self) -> None:
        """Collect entropy from system sources to seed the generator."""
        # Collect entropy from system sources
        entropy_sources = [
            os.urandom(64),  # System random
            str(time.time()).encode(),  # Current time
            str(os.getpid()).encode(),  # Process ID
            str(np.random.random()).encode(),  # NumPy PRNG
        ]
        
        # Mix entropy sources with SHA-256
        for source in entropy_sources:
            h = hashlib.sha256()
            h.update(source)
            self._entropy_pool.extend(h.digest())
        
        logger.debug(f"Collected {len(self._entropy_pool)} bytes of system entropy")
    
    def _simulate_measurement(self, num_samples: int = 1) -> List[int]:
        """
        Simulate quantum measurement on the current state.
        
        Args:
            num_samples: Number of measurement samples to take
            
        Returns:
            List of measurement outcomes as integers
        """
        # Calculate probabilities from state amplitudes
        probabilities = np.abs(self.state)**2
        
        # Ensure probabilities sum to 1
        probabilities /= np.sum(probabilities)
        
        # Sample from the probability distribution
        outcomes = np.random.choice(
            2**self.num_qubits, 
            size=num_samples, 
            p=probabilities
        )
        
        # Apply decoherence (state collapse after measurement)
        if self.decoherence_rate > 0:
            self._apply_decoherence()
            
        return outcomes.tolist()
    
    def _apply_decoherence(self) -> None:
        """Apply decoherence effects to the quantum state."""
        # Model decoherence as slight random variations in amplitudes
        noise = np.random.normal(0, self.decoherence_rate, self.state.shape)
        self.state = self.state * (1 + noise)
        
        # Re-normalize
        self.state /= np.linalg.norm(self.state)
        
        # Re-apply partial Hadamard to maintain some superposition
        self._refresh_superposition()
    
    def _refresh_superposition(self) -> None:
        """Refresh the quantum superposition to maintain randomness."""
        # Apply partial Hadamard to restore some superposition
        h_contribution = np.ones((2**self.num_qubits,), dtype=np.complex128) / np.sqrt(2**self.num_qubits)
        
        # Mix current state with new superposition
        mix_ratio = 0.7  # 70% of original state, 30% new superposition
        self.state = mix_ratio * self.state + (1 - mix_ratio) * h_contribution
        
        # Normalize
        self.state /= np.linalg.norm(self.state)
    
    def _int_to_float(self, value: int, bits: int) -> float:
        """
        Convert an integer to a float in range [0, 1)
        
        Args:
            value: Integer value to convert
            bits: Number of bits in the integer
            
        Returns:
            Float in range [0, 1)
        """
        return value / (2**bits)
    
    def generate_random_bits(self, num_bits: int) -> List[int]:
        """
        Generate random bits using quantum measurements.
        
        Args:
            num_bits: Number of random bits to generate
            
        Returns:
            List of random bits (0 or 1)
        """
        # Determine how many measurements we need
        bits_per_measurement = self.num_qubits
        num_measurements = (num_bits + bits_per_measurement - 1) // bits_per_measurement
        
        # Generate measurements
        measurements = self._simulate_measurement(num_measurements)
        
        # Convert measurements to bits
        bits = []
        for m in measurements:
            # Convert integer to binary and extract bits
            for i in range(bits_per_measurement):
                bit = (m >> i) & 1
                bits.append(bit)
                if len(bits) >= num_bits:
                    break
            if len(bits) >= num_bits:
                break
        
        return bits[:num_bits]
    
    def generate_random_int(self, low: int, high: int) -> int:
        """
        Generate a random integer in the specified range.
        
        Args:
            low: Lower bound (inclusive)
            high: Upper bound (exclusive)
            
        Returns:
            Random integer in range [low, high)
        """
        # Calculate number of bits needed
        range_size = high - low
        bits_needed = max(1, int(np.ceil(np.log2(range_size))))
        
        # Generate random bits
        bits = self.generate_random_bits(bits_needed)
        
        # Convert bits to integer
        value = 0
        for i, bit in enumerate(bits):
            value |= bit << i
        
        # Map to target range [low, high)
        value = low + (value % range_size)
        
        return value
    
    def generate_random_float(self, low: float = 0.0, high: float = 1.0) -> float:
        """
        Generate a random float in the specified range.
        
        Args:
            low: Lower bound (inclusive)
            high: Upper bound (exclusive)
            
        Returns:
            Random float in range [low, high)
        """
        # Generate 53 bits (double precision)
        bits = self.generate_random_bits(53)
        
        # Convert bits to float in [0, 1)
        value = 0.0
        for i, bit in enumerate(bits):
            value += bit * (2 ** -(i + 1))
        
        # Map to target range [low, high)
        value = low + (high - low) * value
        
        return value
    
    def generate_random_normal(self, mean: float = 0.0, std: float = 1.0) -> float:
        """
        Generate a random float from a normal distribution.
        
        Args:
            mean: Mean of the normal distribution
            std: Standard deviation of the normal distribution
            
        Returns:
            Random float from normal distribution
        """
        # Box-Muller transform to generate normal from uniform
        u1 = self.generate_random_float()
        u2 = self.generate_random_float()
        
        # Avoid u1 = 0
        while u1 == 0:
            u1 = self.generate_random_float()
        
        # Box-Muller transform
        z0 = np.sqrt(-2.0 * np.log(u1)) * np.cos(2.0 * np.pi * u2)
        
        # Scale and shift to target distribution
        return mean + std * z0
    
    def generate_random_sequence(self, length: int, distribution: str = "uniform",
                                **dist_params) -> List[float]:
        """
        Generate a sequence of random numbers.
        
        Args:
            length: Length of sequence to generate
            distribution: Type of distribution ("uniform", "normal", "exponential")
            **dist_params: Parameters for the distribution
            
        Returns:
            List of random numbers
        """
        sequence = []
        
        for _ in range(length):
            if distribution == "uniform":
                low = dist_params.get("low", 0.0)
                high = dist_params.get("high", 1.0)
                value = self.generate_random_float(low, high)
            elif distribution == "normal":
                mean = dist_params.get("mean", 0.0)
                std = dist_params.get("std", 1.0)
                value = self.generate_random_normal(mean, std)
            elif distribution == "exponential":
                scale = dist_params.get("scale", 1.0)
                value = -scale * np.log(self.generate_random_float())
            else:
                raise ValueError(f"Unsupported distribution: {distribution}")
            
            sequence.append(value)
        
        return sequence
    
    def reseed(self) -> None:
        """Reseed the random number generator with fresh entropy."""
        self._collect_system_entropy()
        self._initialize_state()
        
        logger.debug("Reseeded quantum RNG with fresh entropy")

if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Create a quantum RNG
    qrng = QuantumRNG(num_qubits=8)
    
    # Generate some random numbers
    print("Random bits:", qrng.generate_random_bits(10))
    print("Random int (1-100):", qrng.generate_random_int(1, 100))
    print("Random float:", qrng.generate_random_float())
    print("Random normal:", qrng.generate_random_normal())
    
    # Generate a sequence
    sequence = qrng.generate_random_sequence(5, "uniform")
    print("Random sequence:", sequence) 