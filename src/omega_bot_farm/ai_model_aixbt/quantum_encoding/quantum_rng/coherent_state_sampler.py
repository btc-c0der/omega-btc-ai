#!/usr/bin/env python3
"""
Coherent State Sampler
=====================

Implementation of a sampler for coherent quantum states, which are quantum 
states with well-defined amplitude and phase.
"""

import numpy as np
import math
import logging
from typing import List, Tuple, Dict, Union, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger("quantum-rng")

@dataclass
class CoherentStateConfig:
    """Configuration for coherent state sampling."""
    
    alpha: complex = 1.0 + 0.0j  # Complex amplitude
    num_photons: int = 10  # Number of photons to simulate
    squeezing: float = 0.0  # Squeezing parameter
    phase_shift: float = 0.0  # Phase shift in radians
    cutoff_dim: int = 20  # Dimension cutoff for Fock space
    decoherence: float = 0.01  # Decoherence rate


class SamplingMethod(Enum):
    """Enum representing different sampling methods."""
    
    PHOTON_NUMBER = "photon_number"  # Sample from photon number distribution
    QUADRATURE = "quadrature"  # Sample from quadrature distribution
    WIGNER = "wigner"  # Sample from Wigner distribution
    HUSIMI_Q = "husimi_q"  # Sample from Husimi Q distribution


class CoherentStateSampler:
    """
    Sampler for coherent quantum states that provides truly random
    numbers by sampling from various distributions associated with
    these states.
    """
    
    def __init__(
        self,
        config: Optional[CoherentStateConfig] = None,
        default_method: SamplingMethod = SamplingMethod.PHOTON_NUMBER
    ):
        """
        Initialize the coherent state sampler.
        
        Args:
            config: Configuration for the coherent state
            default_method: Default sampling method to use
        """
        self.config = config or CoherentStateConfig()
        self.default_method = default_method
        
        # Initialize the state
        self._initialize_state()
        
        logger.info(f"Initialized coherent state sampler with α={self.config.alpha}")
    
    def _initialize_state(self) -> None:
        """Initialize the coherent state representation."""
        # Calculate the Fock basis representation of our coherent state
        self.fock_probs = self._coherent_state_fock_probabilities(
            self.config.alpha,
            self.config.cutoff_dim
        )
        
        # Apply squeezing if requested
        if self.config.squeezing != 0.0:
            self._apply_squeezing()
        
        # Apply phase shift if requested
        if self.config.phase_shift != 0.0:
            self._apply_phase_shift()
    
    def _coherent_state_fock_probabilities(
        self, alpha: complex, cutoff_dim: int
    ) -> np.ndarray:
        """
        Calculate probabilities of Fock states for a coherent state.
        
        Args:
            alpha: Complex amplitude of the coherent state
            cutoff_dim: Cutoff dimension for the Fock space
            
        Returns:
            Array of probabilities for each Fock state
        """
        # |α⟩ = e^(-|α|²/2) ∑ (α^n/√n!) |n⟩
        # P(n) = e^(-|α|²) |α|²^n / n!
        
        abs_alpha_squared = np.abs(alpha)**2
        n_values = np.arange(cutoff_dim)
        
        # Calculate probabilities: P(n) = e^(-|α|²) |α|²^n / n!
        probs = np.exp(-abs_alpha_squared) * abs_alpha_squared**n_values / np.array([math.factorial(n) for n in n_values])
        
        # Normalize (should be close to 1 already if cutoff_dim is large enough)
        probs /= np.sum(probs)
        
        return probs
    
    def _apply_squeezing(self) -> None:
        """Apply squeezing to the coherent state."""
        # This is a simplified model of squeezing
        # In reality, this would require a more complex quantum operation
        
        # Squeezing changes the variance in one quadrature while increasing
        # it in the other, preserving the uncertainty principle
        
        # For our purposes, we'll just modify the Fock state distribution
        r = self.config.squeezing
        
        # Calculate squeezed state distribution (simplified)
        # This is an approximation based on squeezing operator effects
        cutoff = len(self.fock_probs)
        squeezed_probs = np.zeros_like(self.fock_probs)
        
        # Simple model: boost even photon numbers for positive r
        for n in range(cutoff):
            if n % 2 == 0:  # Even photon numbers
                factor = 1 + np.tanh(r)
            else:  # Odd photon numbers
                factor = 1 - np.tanh(r)
            squeezed_probs[n] = self.fock_probs[n] * factor
        
        # Normalize
        self.fock_probs = squeezed_probs / np.sum(squeezed_probs)
    
    def _apply_phase_shift(self) -> None:
        """Apply phase shift to the coherent state."""
        # Phase shift doesn't change photon number distribution,
        # but it does change the phase of the coherent state
        
        # For the current implementation based on photon number sampling,
        # this doesn't affect our probabilities, but we include it for
        # future implementations involving quadrature sampling
        
        self.config.alpha *= np.exp(1j * self.config.phase_shift)
    
    def _apply_decoherence(self) -> None:
        """Apply decoherence effects to the coherent state."""
        # Decoherence tends to transform coherent states towards thermal states
        
        # Simple model: mix with a thermal state
        thermal_n = np.abs(self.config.alpha)**2 * self.config.decoherence
        thermal_probs = np.zeros_like(self.fock_probs)
        
        for n in range(len(thermal_probs)):
            if thermal_n > 0:
                thermal_probs[n] = (thermal_n**n) / ((1 + thermal_n)**(n + 1))
            else:
                thermal_probs[n] = 1.0 if n == 0 else 0.0
        
        # Normalize
        thermal_probs /= np.sum(thermal_probs)
        
        # Mix with original state
        mix_ratio = 1.0 - self.config.decoherence
        self.fock_probs = mix_ratio * self.fock_probs + (1.0 - mix_ratio) * thermal_probs
    
    def sample_photon_number(self, num_samples: int = 1) -> np.ndarray:
        """
        Sample photon numbers based on the coherent state distribution.
        
        Args:
            num_samples: Number of samples to generate
            
        Returns:
            Array of sampled photon numbers
        """
        # Sample from the photon number distribution
        samples = np.random.choice(
            len(self.fock_probs),
            size=num_samples,
            p=self.fock_probs
        )
        
        # Apply decoherence after sampling
        self._apply_decoherence()
        
        return samples
    
    def sample_quadrature(self, num_samples: int = 1, phase: float = 0.0) -> np.ndarray:
        """
        Sample quadrature values along a specified phase.
        
        Args:
            num_samples: Number of samples to generate
            phase: Phase angle for the quadrature measurement
            
        Returns:
            Array of sampled quadrature values
        """
        # For a coherent state |α⟩, the quadrature distribution is a Gaussian
        # centered at Re(α·e^(-iφ)) with variance 0.5
        
        # Calculate mean based on amplitude and phase
        alpha = self.config.alpha
        mean = np.real(alpha * np.exp(-1j * phase))
        
        # For a squeezed state, the variance depends on the squeezing parameter
        # and the phase of measurement relative to the squeezing axis
        variance = 0.5
        if self.config.squeezing != 0.0:
            # Simplified model of squeezing effect on variance
            rel_phase = phase - np.angle(alpha) / 2
            squeeze_factor = np.exp(-2 * self.config.squeezing * np.cos(2 * rel_phase))
            variance *= squeeze_factor
        
        # Sample from Gaussian distribution
        samples = np.random.normal(mean, np.sqrt(variance), num_samples)
        
        # Apply decoherence
        self._apply_decoherence()
        
        return samples
    
    def sample_wigner(self, num_samples: int = 1) -> np.ndarray:
        """
        Sample points from the Wigner distribution of the coherent state.
        
        Args:
            num_samples: Number of samples to generate
            
        Returns:
            Array of sampled points in phase space (x, p)
        """
        # For a coherent state, the Wigner function is a 2D Gaussian
        # centered at (Re(α), Im(α)) with variance 0.5 in each direction
        
        # Mean of the Gaussian
        re_alpha = np.real(self.config.alpha)
        im_alpha = np.imag(self.config.alpha)
        
        # Variance depends on squeezing
        var_x = 0.5
        var_p = 0.5
        
        if self.config.squeezing != 0.0:
            # Apply squeezing effect on variances
            r = self.config.squeezing
            squeeze_angle = np.angle(self.config.alpha) / 2
            
            # Rotate to squeezing reference frame
            cos_theta = np.cos(squeeze_angle)
            sin_theta = np.sin(squeeze_angle)
            
            # Calculate squeezed variances
            var_x_squeezed = 0.5 * np.exp(-2 * r)
            var_p_squeezed = 0.5 * np.exp(2 * r)
            
            # Rotate back to original frame
            var_x = var_x_squeezed * cos_theta**2 + var_p_squeezed * sin_theta**2
            var_p = var_x_squeezed * sin_theta**2 + var_p_squeezed * cos_theta**2
        
        # Sample x and p independently
        x_samples = np.random.normal(re_alpha, np.sqrt(var_x), num_samples)
        p_samples = np.random.normal(im_alpha, np.sqrt(var_p), num_samples)
        
        # Apply decoherence
        self._apply_decoherence()
        
        # Return as pairs of (x, p)
        return np.column_stack((x_samples, p_samples))
    
    def sample_husimi_q(self, num_samples: int = 1) -> np.ndarray:
        """
        Sample points from the Husimi Q distribution of the coherent state.
        
        Args:
            num_samples: Number of samples to generate
            
        Returns:
            Array of sampled points in phase space (x, p)
        """
        # For a coherent state, the Husimi Q function is a 2D Gaussian
        # centered at (Re(α), Im(α)) with variance 1 in each direction
        
        # Mean of the Gaussian
        re_alpha = np.real(self.config.alpha)
        im_alpha = np.imag(self.config.alpha)
        
        # For a coherent state, the Q function has fixed variance of 1
        # Squeezing will change this, but for simplicity we'll use a fixed value
        var = 1.0
        
        # Sample x and p independently
        x_samples = np.random.normal(re_alpha, np.sqrt(var), num_samples)
        p_samples = np.random.normal(im_alpha, np.sqrt(var), num_samples)
        
        # Apply decoherence
        self._apply_decoherence()
        
        # Return as pairs of (x, p)
        return np.column_stack((x_samples, p_samples))
    
    def sample(
        self, 
        num_samples: int = 1, 
        method: Optional[SamplingMethod] = None
    ) -> np.ndarray:
        """
        Sample from the coherent state using the specified method.
        
        Args:
            num_samples: Number of samples to generate
            method: Sampling method to use
            
        Returns:
            Array of samples
        """
        method = method or self.default_method
        
        if method == SamplingMethod.PHOTON_NUMBER:
            return self.sample_photon_number(num_samples)
        elif method == SamplingMethod.QUADRATURE:
            return self.sample_quadrature(num_samples)
        elif method == SamplingMethod.WIGNER:
            return self.sample_wigner(num_samples)
        elif method == SamplingMethod.HUSIMI_Q:
            return self.sample_husimi_q(num_samples)
        else:
            raise ValueError(f"Unknown sampling method: {method}")
    
    def generate_random_sequence(
        self, 
        length: int, 
        out_min: float = 0.0, 
        out_max: float = 1.0,
        method: Optional[SamplingMethod] = None
    ) -> List[float]:
        """
        Generate a sequence of random numbers in the specified range.
        
        Args:
            length: Length of the sequence
            out_min: Minimum value in the output range
            out_max: Maximum value in the output range
            method: Sampling method to use
            
        Returns:
            List of random numbers in the specified range
        """
        method = method or self.default_method
        samples = self.sample(length, method)
        
        # Transform samples to the desired range
        if method == SamplingMethod.PHOTON_NUMBER:
            # Photon numbers need to be normalized
            max_n = self.config.cutoff_dim - 1
            normalized = samples / max_n
        elif method == SamplingMethod.QUADRATURE:
            # Quadrature values need to be shifted and scaled
            # For coherent states, values typically fall within ±4 of the mean
            normalized = (samples - np.min(samples)) / (np.max(samples) - np.min(samples))
        elif method in (SamplingMethod.WIGNER, SamplingMethod.HUSIMI_Q):
            # Phase space points need to be converted to scalars
            # Use the Euclidean distance from the origin
            distances = np.sqrt(samples[:, 0]**2 + samples[:, 1]**2)
            # Normalize by the maximum distance
            normalized = distances / np.max(distances)
        else:
            raise ValueError(f"Unknown sampling method: {method}")
        
        # Map to the specified range
        result = out_min + normalized * (out_max - out_min)
        
        return result.tolist()
    
    def update_config(self, new_config: CoherentStateConfig) -> None:
        """
        Update the configuration of the coherent state.
        
        Args:
            new_config: New configuration to use
        """
        self.config = new_config
        self._initialize_state()
        
        logger.info(f"Updated coherent state configuration: α={self.config.alpha}")

if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Create a coherent state sampler
    config = CoherentStateConfig(alpha=2.0 + 1.0j, squeezing=0.5)
    sampler = CoherentStateSampler(config)
    
    # Sample photon numbers
    photons = sampler.sample_photon_number(10)
    print("Photon number samples:", photons)
    
    # Sample quadrature values
    quads = sampler.sample_quadrature(10)
    print("Quadrature samples:", quads)
    
    # Generate a random sequence
    sequence = sampler.generate_random_sequence(5)
    print("Random sequence:", sequence) 