#!/usr/bin/env python3
"""
Quantum Activation Functions
===========================

Implementation of quantum-inspired activation functions that mimic
quantum gates and operations for neural networks.
"""

import numpy as np
import logging
from typing import Dict, Any, Optional
from .base import QuantumActivation

# Set up logging
logger = logging.getLogger("quantum-neural-net")

# Constants
LOG_PREFIX = "🧠 vQuB1T-NN"
SQRT2_INV = 1.0 / np.sqrt(2.0)
PI = np.pi

class HadamardActivation(QuantumActivation):
    """
    Quantum activation function inspired by the Hadamard gate.
    
    The Hadamard gate creates superpositions in quantum computing by
    transforming basis states into equal superpositions.
    """
    
    def __init__(self, scale: float = 1.0, **kwargs):
        """
        Initialize the Hadamard activation function.
        
        Args:
            scale: Scaling factor for the activation
            **kwargs: Additional parameters
        """
        super().__init__(**kwargs)
        self.scale = scale
        
    def apply(self, inputs: np.ndarray) -> np.ndarray:
        """
        Apply the Hadamard-inspired activation function.
        
        Args:
            inputs: Input tensor
            
        Returns:
            Transformed tensor
        """
        if np.iscomplexobj(inputs):
            # For complex inputs, apply quantum-inspired transformation
            # that preserves phases but changes amplitudes
            
            # Normalize first to preserve quantum-like properties
            norm = np.sqrt(np.sum(np.abs(inputs)**2, axis=-1, keepdims=True)) + 1e-10
            x_norm = inputs / norm
            
            # Apply Hadamard-inspired transformation (combines inputs with its phase shift)
            return SQRT2_INV * self.scale * (x_norm + 1j * x_norm)
        else:
            # For real inputs, approximate with a scaled non-linearity
            # that has similar properties to the quantum version
            return SQRT2_INV * self.scale * (inputs + np.tanh(inputs))
    
    def gradient(self, inputs: np.ndarray) -> np.ndarray:
        """
        Compute the gradient of the Hadamard activation function.
        
        Args:
            inputs: Input tensor (or pre-activation gradients)
            
        Returns:
            Gradient tensor
        """
        if np.iscomplexobj(inputs):
            # For complex gradients, we need to compute the complex derivative
            # which involves both real and imaginary parts
            
            # Simplified approximation of the gradient
            # In reality, this would be more complex for a true quantum gate
            return SQRT2_INV * self.scale * (1.0 + 1j)
        else:
            # For real inputs, compute the gradient of our approximation
            return SQRT2_INV * self.scale * (1.0 + (1.0 - np.tanh(inputs)**2))

class PhaseActivation(QuantumActivation):
    """
    Quantum activation function inspired by the phase gate.
    
    The phase gate introduces a phase shift in quantum states,
    which can be used as a non-linearity in neural networks.
    """
    
    def __init__(self, phase: float = PI/4, **kwargs):
        """
        Initialize the phase activation function.
        
        Args:
            phase: Phase angle (default: π/4 or 45 degrees)
            **kwargs: Additional parameters
        """
        super().__init__(**kwargs)
        self.phase = phase
        
    def apply(self, inputs: np.ndarray) -> np.ndarray:
        """
        Apply the phase-inspired activation function.
        
        Args:
            inputs: Input tensor
            
        Returns:
            Transformed tensor with phase shifts
        """
        if np.iscomplexobj(inputs):
            # For complex inputs, apply a phase shift based on the magnitude
            magnitude = np.abs(inputs)
            current_phase = np.angle(inputs)
            
            # Phase shift is proportional to the magnitude (non-linear effect)
            phase_shift = self.phase * magnitude
            
            # Apply phase shift
            return magnitude * np.exp(1j * (current_phase + phase_shift))
        else:
            # For real inputs, convert to complex and apply phase
            return inputs * np.exp(1j * self.phase * inputs)
    
    def gradient(self, inputs: np.ndarray) -> np.ndarray:
        """
        Compute the gradient of the phase activation function.
        
        Args:
            inputs: Input tensor (or pre-activation gradients)
            
        Returns:
            Gradient tensor
        """
        if np.iscomplexobj(inputs):
            # Compute complex derivative of the phase activation
            magnitude = np.abs(inputs)
            
            # The derivative involves both the phase shift and its derivative
            # This is a simplified approximation
            return np.exp(1j * self.phase * magnitude) * (1.0 + 1j * self.phase * np.sign(inputs))
        else:
            # For real inputs, derivative of the complex transformation
            return np.exp(1j * self.phase * inputs) * (1.0 + 1j * self.phase * inputs)

class ParametricRXActivation(QuantumActivation):
    """
    Quantum activation function inspired by the RX (rotation-X) gate.
    
    The RX gate rotates a qubit around the X-axis of the Bloch sphere.
    This activation function parameterizes this rotation based on the input.
    """
    
    def __init__(self, scaling: float = 1.0, **kwargs):
        """
        Initialize the parametric RX activation function.
        
        Args:
            scaling: Scaling factor for the rotation angle
            **kwargs: Additional parameters
        """
        super().__init__(**kwargs)
        self.scaling = scaling
        
    def apply(self, inputs: np.ndarray) -> np.ndarray:
        """
        Apply the RX-inspired activation function.
        
        Args:
            inputs: Input tensor
            
        Returns:
            Transformed tensor with X-rotations
        """
        if np.iscomplexobj(inputs):
            # For complex inputs, simulate a rotation around X-axis
            # Extract magnitude and phase
            magnitude = np.abs(inputs)
            phase = np.angle(inputs)
            
            # Calculate rotation angle based on input
            theta = self.scaling * magnitude
            
            # Apply RX-like transformation (mixing real and imaginary parts)
            cos_half_theta = np.cos(theta/2)
            sin_half_theta = np.sin(theta/2)
            
            # Compute new complex value after rotation
            real_part = cos_half_theta * np.cos(phase) - sin_half_theta * np.sin(phase)
            imag_part = cos_half_theta * np.sin(phase) + sin_half_theta * np.cos(phase)
            
            return magnitude * (real_part + 1j * imag_part)
        else:
            # For real inputs, approximate with a sinusoidal transformation
            theta = self.scaling * inputs
            return inputs * np.cos(theta) + inputs * np.sin(theta)
    
    def gradient(self, inputs: np.ndarray) -> np.ndarray:
        """
        Compute the gradient of the parametric RX activation function.
        
        Args:
            inputs: Input tensor (or pre-activation gradients)
            
        Returns:
            Gradient tensor
        """
        if np.iscomplexobj(inputs):
            # Complex derivative of the RX transformation
            # This is a simplified approximation
            magnitude = np.abs(inputs)
            theta = self.scaling * magnitude
            
            # Derivative includes both the rotation and its derivative
            d_theta = self.scaling * np.sign(inputs)
            
            cos_half_theta = np.cos(theta/2)
            sin_half_theta = np.sin(theta/2)
            
            # Approximate the complex derivative
            return (cos_half_theta - 0.5 * sin_half_theta * d_theta) + 1j * (sin_half_theta + 0.5 * cos_half_theta * d_theta)
        else:
            # Derivative of the real approximation
            theta = self.scaling * inputs
            d_theta = self.scaling
            
            return np.cos(theta) + np.sin(theta) + inputs * (-d_theta * np.sin(theta) + d_theta * np.cos(theta))

class ToffoliActivation(QuantumActivation):
    """
    Quantum activation function inspired by the Toffoli (CCNOT) gate.
    
    The Toffoli gate is a controlled-controlled-NOT gate that flips a target
    bit if both control bits are 1. This activation simulates a multi-valued 
    version for neural network use.
    """
    
    def __init__(self, threshold: float = 0.5, sharpness: float = 10.0, **kwargs):
        """
        Initialize the Toffoli activation function.
        
        Args:
            threshold: Activation threshold (similar to control bit threshold)
            sharpness: How sharply the activation transitions at the threshold
            **kwargs: Additional parameters
        """
        super().__init__(**kwargs)
        self.threshold = threshold
        self.sharpness = sharpness
        
    def apply(self, inputs: np.ndarray) -> np.ndarray:
        """
        Apply the Toffoli-inspired activation function.
        
        Args:
            inputs: Input tensor
            
        Returns:
            Transformed tensor with conditional activation
        """
        if np.iscomplexobj(inputs):
            # For complex inputs, we need to consider both magnitude and phase
            magnitude = np.abs(inputs)
            phase = np.angle(inputs)
            
            # Apply conditional transformation based on magnitude
            # If magnitude > threshold, "flip" the phase (add PI)
            # Use sigmoid for smooth transition
            flip_factor = 1.0 / (1.0 + np.exp(-self.sharpness * (magnitude - self.threshold)))
            
            # Modified phase: original + conditional phase flip
            new_phase = phase + flip_factor * PI
            
            # Return with original magnitude but modified phase
            return magnitude * np.exp(1j * new_phase)
        else:
            # For real inputs, use a sigmoid-based conditional negation
            flip_factor = 1.0 / (1.0 + np.exp(-self.sharpness * (np.abs(inputs) - self.threshold)))
            
            # Conditional sign flip (smooth approximation of sign change)
            return inputs * (1.0 - 2.0 * flip_factor)
    
    def gradient(self, inputs: np.ndarray) -> np.ndarray:
        """
        Compute the gradient of the Toffoli activation function.
        
        Args:
            inputs: Input tensor (or pre-activation gradients)
            
        Returns:
            Gradient tensor
        """
        if np.iscomplexobj(inputs):
            # Complex derivative of the conditional phase transformation
            magnitude = np.abs(inputs)
            
            # Derivative of sigmoid flip factor
            sigmoid = 1.0 / (1.0 + np.exp(-self.sharpness * (magnitude - self.threshold)))
            d_sigmoid = self.sharpness * sigmoid * (1.0 - sigmoid) * np.sign(inputs)
            
            # Derivative includes both maintaining the original and the phase change
            return np.exp(1j * sigmoid * PI) + 1j * PI * d_sigmoid * np.exp(1j * sigmoid * PI)
        else:
            # Derivative of conditional sign flip
            abs_inputs = np.abs(inputs)
            sigmoid = 1.0 / (1.0 + np.exp(-self.sharpness * (abs_inputs - self.threshold)))
            d_sigmoid = self.sharpness * sigmoid * (1.0 - sigmoid) * np.sign(inputs)
            
            # Return derivative
            return (1.0 - 2.0 * sigmoid) - 2.0 * inputs * d_sigmoid 