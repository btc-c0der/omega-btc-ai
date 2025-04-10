#!/usr/bin/env python3

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

"""
Quantum Circuit Simulator
=======================

Basic quantum circuit simulator for educational purposes.
Provides classical simulation of quantum registers and simple gates.
"""

import numpy as np
import logging
from typing import Dict, List, Union, Any, Optional, Tuple

# Configure logging
logger = logging.getLogger("quantum-encoding")

class QuantumRegister:
    """Simulates a quantum register (collection of qubits)."""
    
    def __init__(self, n_qubits: int = 1, name: str = "q"):
        """
        Initialize a quantum register with n qubits.
        
        Args:
            n_qubits: Number of qubits in the register
            name: Name identifier for the register
        """
        self.n_qubits = n_qubits
        self.name = name
        self.dimension = 2 ** n_qubits
        
        # Initialize to |0...0⟩ state
        self.state = np.zeros(self.dimension, dtype=complex)
        self.state[0] = 1.0
        
        logger.info(f"Initialized {n_qubits}-qubit register '{name}'")
    
    def reset(self) -> None:
        """Reset register to |0...0⟩ state."""
        self.state = np.zeros(self.dimension, dtype=complex)
        self.state[0] = 1.0
    
    def get_statevector(self) -> np.ndarray:
        """Get the current statevector."""
        return self.state
    
    def set_statevector(self, statevector: np.ndarray) -> None:
        """
        Set the statevector of the register.
        
        Args:
            statevector: New state vector (must be normalized)
        """
        if len(statevector) != self.dimension:
            raise ValueError(f"Statevector dimension {len(statevector)} doesn't match register dimension {self.dimension}")
        
        # Normalize if needed
        norm = np.linalg.norm(statevector)
        if abs(norm - 1.0) > 1e-8:
            statevector = statevector / norm
            logger.warning(f"Input statevector was not normalized, applied normalization")
        
        self.state = statevector
    
    def get_probabilities(self) -> np.ndarray:
        """Get measurement probabilities for each basis state."""
        return np.abs(self.state) ** 2
    
    def measure(self, collapse: bool = True) -> int:
        """
        Perform a measurement on the register.
        
        Args:
            collapse: Whether to collapse the state after measurement
            
        Returns:
            Measured basis state as an integer
        """
        probabilities = self.get_probabilities()
        outcomes = np.arange(self.dimension)
        result = np.random.choice(outcomes, p=probabilities)
        
        if collapse:
            # Collapse to the measured state
            new_state = np.zeros(self.dimension, dtype=complex)
            new_state[result] = 1.0
            self.state = new_state
            
        return result
    
    def __str__(self) -> str:
        """String representation showing probabilities of each basis state."""
        probs = self.get_probabilities()
        result = [f"Quantum register '{self.name}' ({self.n_qubits} qubits):"]
        
        # Only show states with non-negligible probability
        for i, prob in enumerate(probs):
            if prob > 1e-6:
                # Convert to binary representation with leading zeros
                binary = format(i, f'0{self.n_qubits}b')
                result.append(f"|{binary}⟩: {prob:.6f}")
        
        return "\n".join(result)

class QuantumCircuitSimulator:
    """Simple quantum circuit simulator."""
    
    def __init__(self, n_qubits: int = 1):
        """
        Initialize a quantum circuit simulator.
        
        Args:
            n_qubits: Number of qubits in the circuit
        """
        self.n_qubits = n_qubits
        self.register = QuantumRegister(n_qubits)
        
        # Define common gates
        self._init_gates()
        
        logger.info(f"Initialized quantum circuit simulator with {n_qubits} qubits")
    
    def _init_gates(self) -> None:
        """Initialize common quantum gates."""
        # Single-qubit gates
        self.I = np.array([[1, 0], [0, 1]], dtype=complex)
        self.X = np.array([[0, 1], [1, 0]], dtype=complex)  # Pauli-X (NOT)
        self.Y = np.array([[0, -1j], [1j, 0]], dtype=complex)  # Pauli-Y
        self.Z = np.array([[1, 0], [0, -1]], dtype=complex)  # Pauli-Z
        self.H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)  # Hadamard
        
        # Two-qubit gates
        self.CNOT = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ], dtype=complex)
    
    def _get_gate_matrix(self, gate_name: str, params: Optional[List[float]] = None) -> np.ndarray:
        """Get the matrix for a quantum gate."""
        if gate_name == 'I':
            return self.I
        elif gate_name == 'X':
            return self.X
        elif gate_name == 'Y':
            return self.Y
        elif gate_name == 'Z':
            return self.Z
        elif gate_name == 'H':
            return self.H
        elif gate_name == 'CNOT':
            return self.CNOT
        elif gate_name in ['RX', 'RY', 'RZ']:
            # Rotation gates need parameters
            if not params or len(params) != 1:
                raise ValueError(f"{gate_name} gate requires an angle parameter")
            
            angle = params[0]
            cos_half = np.cos(angle / 2)
            sin_half = np.sin(angle / 2)
            
            if gate_name == 'RX':
                return np.array([
                    [cos_half, -1j * sin_half],
                    [-1j * sin_half, cos_half]
                ], dtype=complex)
            elif gate_name == 'RY':
                return np.array([
                    [cos_half, -sin_half],
                    [sin_half, cos_half]
                ], dtype=complex)
            elif gate_name == 'RZ':
                return np.array([
                    [np.exp(-1j * angle / 2), 0],
                    [0, np.exp(1j * angle / 2)]
                ], dtype=complex)
        else:
            raise ValueError(f"Unknown gate: {gate_name}")
    
    def apply_gate(self, gate_name: str, target_qubit: int, 
                  control_qubit: Optional[int] = None,
                  params: Optional[List[float]] = None) -> None:
        """
        Apply a quantum gate to the register.
        
        Args:
            gate_name: Name of the gate ('X', 'H', 'CNOT', etc.)
            target_qubit: Target qubit index
            control_qubit: Control qubit index (for controlled gates)
            params: Gate parameters (e.g., rotation angles)
        """
        if target_qubit >= self.n_qubits or (control_qubit is not None and control_qubit >= self.n_qubits):
            raise ValueError(f"Qubit index out of range: register has {self.n_qubits} qubits")
        
        # Get the gate matrix
        gate_matrix = self._get_gate_matrix(gate_name, params)
        
        # Apply the gate
        if control_qubit is None:
            # Single-qubit gate
            if gate_matrix.shape == (2, 2):
                self._apply_single_qubit_gate(gate_matrix, target_qubit)
            else:
                raise ValueError(f"Invalid matrix dimensions for single-qubit gate: {gate_matrix.shape}")
        else:
            # Controlled gate
            if gate_name == 'CNOT':
                self._apply_cnot(control_qubit, target_qubit)
            else:
                raise ValueError(f"Controlled version of {gate_name} not implemented")
    
    def _apply_single_qubit_gate(self, gate_matrix: np.ndarray, target_qubit: int) -> None:
        """Apply a single-qubit gate to a specific qubit."""
        # Create the full operator using tensor products
        op = None
        
        for i in range(self.n_qubits):
            if i == target_qubit:
                term = gate_matrix
            else:
                term = self.I
            
            if op is None:
                op = term
            else:
                op = np.kron(term, op)  # Note: order of tensor product
        
        # Apply the operator
        self.register.state = op @ self.register.state
    
    def _apply_cnot(self, control_qubit: int, target_qubit: int) -> None:
        """Apply a CNOT gate between control and target qubits."""
        # For simplicity, we'll just handle the 2-qubit case for demonstration
        if self.n_qubits == 2 and {control_qubit, target_qubit} == {0, 1}:
            # Adjust for ordering if needed
            if control_qubit == 0 and target_qubit == 1:
                op = self.CNOT
            else:  # control=1, target=0
                # Swap the qubits before and after
                swap = np.array([
                    [1, 0, 0, 0],
                    [0, 0, 1, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 1]
                ], dtype=complex)
                op = swap @ self.CNOT @ swap
            
            self.register.state = op @ self.register.state
        else:
            raise ValueError("CNOT implementation for arbitrary qubits not included in this demo")
    
    def get_statevector(self) -> np.ndarray:
        """Get the current statevector."""
        return self.register.get_statevector()
    
    def set_statevector(self, statevector: np.ndarray) -> None:
        """Set the statevector of the circuit."""
        self.register.set_statevector(statevector)
    
    def measure_all(self, collapse: bool = True) -> str:
        """
        Measure all qubits in the register.
        
        Args:
            collapse: Whether to collapse the state after measurement
            
        Returns:
            Measured bit string
        """
        result = self.register.measure(collapse)
        return format(result, f'0{self.n_qubits}b')
    
    def get_probabilities(self) -> Dict[str, float]:
        """
        Get measurement probabilities for each basis state.
        
        Returns:
            Dictionary mapping bit strings to probabilities
        """
        probs = self.register.get_probabilities()
        return {format(i, f'0{self.n_qubits}b'): p for i, p in enumerate(probs) if p > 1e-8}
    
    def __str__(self) -> str:
        """String representation of the circuit state."""
        return str(self.register) 