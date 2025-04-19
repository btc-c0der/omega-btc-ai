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
Quantum Convolutional Neural Network
===================================

Implementation of a Quantum Convolutional Neural Network (QCNN) 
inspired by quantum computing principles.
"""

import numpy as np
from typing import Dict, List, Optional, Union, Tuple, Any, Callable, cast
import logging

# Set up logging
logger = logging.getLogger("quantum-neural-net")
LOG_PREFIX = "🧠 vQuB1T-NN"

class QCNN:
    """
    Quantum Convolutional Neural Network.
    
    Implements a convolutional layer inspired by quantum computing principles.
    Uses complex-valued kernels and quantum-like operations for feature extraction.
    """
    
    def __init__(self, 
                input_dim: Union[int, Tuple[int, ...]],
                filters: int = 4,
                kernel_size: Union[int, Tuple[int, ...]] = 3,
                stride: Union[int, Tuple[int, ...]] = 1,
                padding: str = 'valid',
                activation: Optional[str] = None,
                use_complex: bool = True,
                name: str = "qcnn"):
        """
        Initialize the QCNN layer.
        
        Args:
            input_dim: Input dimensions (width, height, channels) or (length, channels)
            filters: Number of filters/kernels
            kernel_size: Size of the convolution kernel
            stride: Stride of the convolution
            padding: 'valid' or 'same'
            activation: Activation function to use
            use_complex: Whether to use complex-valued weights
            name: Name of the layer
        """
        self.name = name
        self.use_complex = use_complex
        
        # Convert input dimensions to tuple if single int
        if isinstance(input_dim, int):
            self.input_dim = (input_dim, 1)  # 1D input with single channel
        else:
            self.input_dim = input_dim
        
        # Get number of dimensions (1D, 2D, or 3D)
        if len(self.input_dim) == 2:  # (length, channels)
            self.n_dims = 1
            self.input_length, self.in_channels = self.input_dim
            self.input_height = 1
            self.input_width = self.input_length
        elif len(self.input_dim) == 3:  # (height, width, channels)
            self.n_dims = 2
            self.input_height, self.input_width, self.in_channels = self.input_dim
            self.input_length = self.input_height * self.input_width
        else:
            raise ValueError(f"Input dimension should be 2 or 3, got {len(self.input_dim)}")
        
        # Convert kernel size to tuple if single int
        if isinstance(kernel_size, int):
            if self.n_dims == 1:
                self.kernel_size: Tuple[int, ...] = (kernel_size,)
            else:  # 2D
                self.kernel_size = (kernel_size, kernel_size)
        else:
            self.kernel_size = kernel_size
            
        # Convert stride to tuple if single int
        if isinstance(stride, int):
            if self.n_dims == 1:
                self.stride: Tuple[int, ...] = (stride,)
            else:  # 2D
                self.stride = (stride, stride)
        else:
            self.stride = stride
            
        self.filters = filters
        self.padding = padding
        
        # Calculate output dimensions
        if self.padding == 'valid':
            if self.n_dims == 1:
                # Ensure kernel_size is not empty
                if len(self.kernel_size) < 1:
                    raise ValueError("Kernel size must have at least 1 element for 1D convolution")
                if len(self.stride) < 1:
                    raise ValueError("Stride must have at least 1 element for 1D convolution")
                    
                self.output_width = (self.input_width - self.kernel_size[0]) // self.stride[0] + 1
                self.output_height = 1
            else:  # 2D
                # Ensure kernel_size has at least 2 elements for 2D
                if len(self.kernel_size) < 2:
                    raise ValueError("Kernel size must have at least 2 elements for 2D convolution")
                if len(self.stride) < 1:
                    raise ValueError("Stride must have at least 1 element for 2D convolution")
                    
                self.output_height = (self.input_height - self.kernel_size[0]) // self.stride[0] + 1
                self.output_width = (self.input_width - self.kernel_size[1]) // self.stride[0] + 1
        else:  # 'same'
            self.output_height = self.input_height
            self.output_width = self.input_width
            
        self.output_dim = (self.output_height, self.output_width, self.filters)
        
        # Set up activation function
        self.activation_fn: Optional[Callable[[np.ndarray], np.ndarray]] = None
        if activation is not None:
            if activation.lower() == 'relu':
                self.activation_fn = lambda x: np.maximum(0, x)
            elif activation.lower() == 'sigmoid':
                self.activation_fn = lambda x: 1 / (1 + np.exp(-x))
            elif activation.lower() == 'tanh':
                self.activation_fn = lambda x: np.tanh(x)
            else:
                logger.warning(f"{LOG_PREFIX} - Unknown activation function: {activation}. Using None.")
            
        # Initialize weights (kernels)
        self.initialize_weights()
        
        # For storing cached computations for backprop
        self._cached_input: Optional[np.ndarray] = None
        self._cached_output_pre_activation: Optional[np.ndarray] = None
        
    def initialize_weights(self):
        """Initialize convolutional kernels."""
        # Initialize convolutional kernels
        if self.n_dims == 1:
            # Ensure kernel_size is not empty
            if len(self.kernel_size) < 1:
                raise ValueError("Kernel size must have at least 1 element for 1D convolution")
                
            kernel_shape = (self.kernel_size[0], self.in_channels, self.filters)
        else:  # 2D
            if len(self.kernel_size) < 2:
                raise ValueError("Kernel size must have at least 2 elements for 2D convolution")
                
            kernel_shape = (self.kernel_size[0], self.kernel_size[1], self.in_channels, self.filters)
        
        # Standard deviation for initialization
        stddev = np.sqrt(2.0 / (np.prod(self.kernel_size) * self.in_channels))
        
        if self.use_complex:
            # Complex-valued kernels
            real_part = np.random.normal(0, stddev, kernel_shape)
            imag_part = np.random.normal(0, stddev, kernel_shape)
            self.kernels = real_part + 1j * imag_part
            
            # Phase term (quantum-inspired)
            self.phase = np.random.uniform(0, 2*np.pi, (self.filters,))
            
            # Bias term
            self.bias = np.random.normal(0, 0.01, (self.filters,)) + 1j * np.random.normal(0, 0.01, (self.filters,))
        else:
            # Real-valued kernels
            self.kernels = np.random.normal(0, stddev, kernel_shape)
            
            # Bias term
            self.bias = np.random.normal(0, 0.01, (self.filters,))
            
    def get_weights(self) -> List[np.ndarray]:
        """
        Get all trainable weights.
        
        Returns:
            List of weight arrays
        """
        if self.use_complex:
            return [self.kernels, self.phase, self.bias]
        else:
            return [self.kernels, self.bias]
    
    def set_weights(self, weights: List[np.ndarray]) -> None:
        """
        Set all trainable weights.
        
        Args:
            weights: List of weight arrays
        """
        if self.use_complex and len(weights) != 3:
            raise ValueError(f"Expected 3 weight arrays for complex mode, got {len(weights)}")
        elif not self.use_complex and len(weights) != 2:
            raise ValueError(f"Expected 2 weight arrays for real mode, got {len(weights)}")
        
        self.kernels = weights[0]
        
        if self.use_complex:
            self.phase = weights[1]
            self.bias = weights[2]
        else:
            self.bias = weights[1]
    
    def _im2col(self, inputs: np.ndarray) -> np.ndarray:
        """
        Convert the input image to column vectors for efficient convolution.
        
        Args:
            inputs: Input data (batch_size, height, width, channels)
            
        Returns:
            Columns for convolution
        """
        batch_size = inputs.shape[0]
        
        if self.n_dims == 1:
            # 1D convolution
            # Ensure kernel_size is not empty
            if len(self.kernel_size) < 1 or len(self.stride) < 1:
                raise ValueError("Kernel size and stride must have at least 1 element for 1D convolution")
                
            length, channels = inputs.shape[1], inputs.shape[2]
            col_length = self.kernel_size[0]
            col_width = channels
            
            # Calculate output length
            output_length = (length - col_length) // self.stride[0] + 1
            
            # Create output array
            cols = np.zeros((batch_size, output_length, col_length * col_width), 
                           dtype=complex if self.use_complex else float)
            
            # Extract sliding windows
            for b in range(batch_size):
                for i in range(output_length):
                    start_idx = i * self.stride[0]
                    end_idx = start_idx + col_length
                    window = inputs[b, start_idx:end_idx, :]
                    cols[b, i, :] = window.reshape(-1)
            
            return cols
        else:
            # 2D convolution
            height, width, channels = inputs.shape[1], inputs.shape[2], inputs.shape[3]
            
            # Ensure kernel_size has at least 2 elements for 2D
            if len(self.kernel_size) < 2:
                raise ValueError("Kernel size must have at least 2 elements for 2D convolution")
            if len(self.stride) < 1:
                raise ValueError("Stride must have at least 1 element for 2D convolution")
                
            col_height, col_width = self.kernel_size[0], self.kernel_size[1]
            
            # Calculate output dimensions
            output_height = (height - col_height) // self.stride[0] + 1
            
            # Ensure stride has at least 2 elements for 2D
            if len(self.stride) < 2:
                stride_width = self.stride[0]  # Use the same stride for width if not specified
            else:
                stride_width = self.stride[1]
                
            output_width = (width - col_width) // stride_width + 1
            
            # Create output array
            cols = np.zeros((batch_size, output_height * output_width, col_height * col_width * channels), 
                           dtype=complex if self.use_complex else float)
            
            # Extract sliding windows
            for b in range(batch_size):
                idx = 0
                for i in range(0, height - col_height + 1, self.stride[0]):
                    stride_w = stride_width  # Use the computed stride_width
                    for j in range(0, width - col_width + 1, stride_w):
                        window = inputs[b, i:i+col_height, j:j+col_width, :]
                        cols[b, idx, :] = window.reshape(-1)
                        idx += 1
            
            return cols
    
    def _quantum_interference(self, x: np.ndarray) -> np.ndarray:
        """
        Apply quantum interference effects to the input.
        
        Args:
            x: Input data
            
        Returns:
            Output with quantum interference applied
        """
        if not self.use_complex:
            return x
        
        # Apply phase shifts
        phase_factors = np.exp(1j * self.phase)
        
        # Apply quantum-like interference
        # This is a simplified simulation of quantum effects
        # In a real quantum circuit, this would be more sophisticated
        
        # Simple interference: allow channels to interfere with each other
        # based on their phase relationship
        if x.ndim == 4:  # (batch, height, width, channels)
            # For each filter, apply phase shift
            result = np.zeros_like(x)
            for f in range(self.filters):
                # Apply phase to each position
                result[:, :, :, f] = x[:, :, :, f] * phase_factors[f]
            
            # Sum of probability amplitudes (quantum interference)
            # This allows constructive and destructive interference
            amplitude = np.abs(result)
            phase = np.angle(result)
            
            # Constructive interference increases amplitude
            # Destructive interference decreases amplitude
            interference = np.sum(amplitude * np.cos(phase), axis=-1, keepdims=True)
            
            # Apply interference effect
            result = result * (1 + 0.1 * interference)
            
            return result
        else:
            # Apply phase to each filter output
            return x * phase_factors
    
    def forward(self, inputs: np.ndarray) -> np.ndarray:
        """
        Forward pass through the QCNN layer.
        
        Args:
            inputs: Input data (batch_size, height, width, channels) or (batch_size, length, channels)
            
        Returns:
            Output after convolution and activation
        """
        # Cache inputs for backward pass
        self._cached_input = inputs
        
        batch_size = inputs.shape[0]
        
        # Handle padding if 'same'
        if self.padding == 'same':
            if self.n_dims == 1:
                # Ensure kernel_size is not empty
                if len(self.kernel_size) < 1:
                    raise ValueError("Kernel size must have at least 1 element for 1D convolution")
                    
                pad_width = self.kernel_size[0] - 1
                padded_inputs = np.pad(
                    inputs, 
                    ((0, 0), (pad_width//2, pad_width - pad_width//2), (0, 0)), 
                    'constant'
                )
            else:  # 2D
                if len(self.kernel_size) < 2:
                    raise ValueError("Kernel size must have at least 2 elements for 2D convolution")
                    
                pad_height = self.kernel_size[0] - 1
                pad_width = self.kernel_size[1] - 1
                padded_inputs = np.pad(
                    inputs, 
                    ((0, 0), 
                     (pad_height//2, pad_height - pad_height//2), 
                     (pad_width//2, pad_width - pad_width//2), 
                     (0, 0)), 
                    'constant'
                )
        else:
            padded_inputs = inputs
        
        # Convert input patches to columns for efficient convolution
        if self.n_dims == 1:
            # Ensure kernel_size is not empty
            if len(self.kernel_size) < 1:
                raise ValueError("Kernel size must have at least 1 element for 1D convolution")
                
            # Reshape kernels for matrix multiplication
            kernels_col = self.kernels.reshape(self.kernel_size[0] * self.in_channels, self.filters)
        else:  # 2D
            # Ensure kernel_size has at least 2 elements for 2D
            if len(self.kernel_size) < 2:
                raise ValueError("Kernel size must have at least 2 elements for 2D convolution")
                
            # Reshape kernels for matrix multiplication
            kernels_col = self.kernels.reshape(self.kernel_size[0] * self.kernel_size[1] * self.in_channels, self.filters)
        
        # Perform convolution via im2col and matrix multiplication
        x_col = self._im2col(padded_inputs)
        
        # Reshape for batch matrix multiplication
        output = np.matmul(x_col, kernels_col)
        
        # Apply bias
        output = output + self.bias
        
        # Apply quantum interference effects
        if self.use_complex:
            output = self._quantum_interference(output)
        
        # Reshape output to proper dimensions
        if self.n_dims == 1:
            output = output.reshape(batch_size, self.output_width, self.filters)
        else:  # 2D
            output = output.reshape(batch_size, self.output_height, self.output_width, self.filters)
        
        # Cache output before activation
        self._cached_output_pre_activation = output
        
        # Apply activation function
        if self.activation_fn is not None:
            if self.use_complex:
                # For complex values, apply activation to magnitude and preserve phase
                magnitude = np.abs(output)
                phase = np.angle(output)
                
                activated_magnitude = self.activation_fn(magnitude)
                output = activated_magnitude * np.exp(1j * phase)
            else:
                output = self.activation_fn(output)
        
        return output
    
    def backward(self, grad_output: np.ndarray) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
        """
        Backward pass to compute gradients.
        
        Args:
            grad_output: Gradient of loss with respect to output
            
        Returns:
            Gradient of loss with respect to input and gradients for parameters
        """
        if self._cached_output_pre_activation is None or self._cached_input is None:
            raise ValueError("Cannot perform backward pass before forward pass")
            
        # Get dimensions
        batch_size = grad_output.shape[0]
        
        # Compute gradient through activation function
        if self.activation_fn is not None:
            if self.use_complex:
                # For complex activation, handle magnitude and phase separately
                magnitude = np.abs(self._cached_output_pre_activation)
                phase = np.angle(self._cached_output_pre_activation)
                
                # Compute gradient of activation with respect to magnitude
                # For now, we'll use a simple approximation
                epsilon = 0.01
                grad_magnitude = (self.activation_fn(magnitude + epsilon) - self.activation_fn(magnitude)) / epsilon
                
                # Apply chain rule
                grad_output = grad_output * (grad_magnitude * np.exp(1j * phase))
            else:
                # For real activation, compute gradient directly
                # For common activations:
                activation_name = getattr(self.activation_fn, '__name__', '')
                
                if activation_name == 'relu' or '<lambda>' in activation_name and 'maximum' in str(self.activation_fn):
                    grad_activation = np.where(self._cached_output_pre_activation > 0, 1, 0)
                elif activation_name == 'sigmoid' or '<lambda>' in activation_name and 'exp' in str(self.activation_fn):
                    activated = 1 / (1 + np.exp(-self._cached_output_pre_activation))
                    grad_activation = activated * (1 - activated)
                elif activation_name == 'tanh' or '<lambda>' in activation_name and 'tanh' in str(self.activation_fn):
                    grad_activation = 1 - np.tanh(self._cached_output_pre_activation)**2
                else:
                    # Fallback: numerical approximation
                    epsilon = 0.01
                    grad_activation = (self.activation_fn(self._cached_output_pre_activation + epsilon) - 
                                      self.activation_fn(self._cached_output_pre_activation)) / epsilon
                
                grad_output = grad_output * grad_activation
        
        # Prepare gradients for parameters
        if self.n_dims == 1:
            # Ensure kernel_size is not empty
            if len(self.kernel_size) < 1:
                raise ValueError("Kernel size must have at least 1 element for 1D convolution")
                
            kernels_col = self.kernels.reshape(self.kernel_size[0] * self.in_channels, self.filters)
        else:  # 2D
            # Ensure kernel_size has at least 2 elements for 2D
            if len(self.kernel_size) < 2:
                raise ValueError("Kernel size must have at least 2 elements for 2D convolution")
                
            kernels_col = self.kernels.reshape(self.kernel_size[0] * self.kernel_size[1] * self.in_channels, self.filters)
        
        # Gradient with respect to bias
        grad_bias = np.sum(grad_output, axis=tuple(range(grad_output.ndim-1)))
        
        # Flatten spatial dimensions of grad_output for matrix multiplication
        if self.n_dims == 1:
            grad_output_reshaped = grad_output.reshape(batch_size, -1, self.filters)
        else:  # 2D
            grad_output_reshaped = grad_output.reshape(batch_size, -1, self.filters)
        
        # Get im2col representation of input
        x_col = self._im2col(self._cached_input)
        
        # Gradient with respect to kernels
        grad_kernels_col = np.zeros_like(kernels_col)
        for b in range(batch_size):
            grad_kernels_col += np.matmul(x_col[b].T, grad_output_reshaped[b])
        
        # Reshape grad_kernels back to original kernel shape
        if self.n_dims == 1:
            # Ensure kernel_size is not empty
            if len(self.kernel_size) < 1:
                raise ValueError("Kernel size must have at least 1 element for 1D convolution")
                
            grad_kernels = grad_kernels_col.reshape(self.kernel_size[0], self.in_channels, self.filters)
        else:  # 2D
            # Ensure kernel_size has at least 2 elements for 2D
            if len(self.kernel_size) < 2:
                raise ValueError("Kernel size must have at least 2 elements for 2D convolution")
                
            grad_kernels = grad_kernels_col.reshape(self.kernel_size[0], self.kernel_size[1], 
                                                  self.in_channels, self.filters)
        
        # Gradient with respect to phase (for complex case)
        grad_phase = None
        if self.use_complex:
            # Compute gradient for phase parameters
            # This is a simplified approximation
            grad_phase = np.zeros_like(self.phase)
            
            # Gradient is related to change in output when phase changes
            for f in range(self.filters):
                # Derivative of e^(i*phi) with respect to phi is i*e^(i*phi)
                grad_phase[f] = np.sum(1j * np.exp(1j * self.phase[f]) * grad_output[..., f])
                # Keep only the imaginary part which affects the real output
                grad_phase[f] = np.imag(grad_phase[f])
        
        # Compute gradient with respect to input
        # This is the most complex part and would require full im2col implementation
        # For simplicity, we'll use a basic approximation
        grad_input = np.zeros_like(self._cached_input)
        
        # Simple approximation: distribute gradient back through the convolution
        if self.n_dims == 1:
            # Ensure kernel_size and stride are not empty
            if len(self.kernel_size) < 1 or len(self.stride) < 1:
                raise ValueError("Kernel size and stride must have at least 1 element for 1D convolution")
                
            for b in range(batch_size):
                for i in range(self.output_width):
                    start_idx = i * self.stride[0]
                    for k in range(self.kernel_size[0]):
                        for c in range(self.in_channels):
                            for f in range(self.filters):
                                if start_idx + k < self.input_width:
                                    grad_input[b, start_idx + k, c] += self.kernels[k, c, f] * grad_output[b, i, f]
        else:  # 2D
            # Ensure kernel_size has at least 2 elements for 2D
            if len(self.kernel_size) < 2 or len(self.stride) < 1:
                raise ValueError("Kernel size must have at least 2 elements and stride at least 1 element for 2D convolution")
                
            for b in range(batch_size):
                for i in range(self.output_height):
                    for j in range(self.output_width):
                        start_i = i * self.stride[0]
                        # Use stride[0] for the second dimension if stride[1] is not available
                        start_j = j * (self.stride[1] if len(self.stride) >= 2 else self.stride[0])
                        for k_i in range(self.kernel_size[0]):
                            for k_j in range(self.kernel_size[1]):
                                for c in range(self.in_channels):
                                    for f in range(self.filters):
                                        if (start_i + k_i < self.input_height and 
                                            start_j + k_j < self.input_width):
                                            grad_input[b, start_i + k_i, start_j + k_j, c] += (
                                                self.kernels[k_i, k_j, c, f] * grad_output[b, i, j, f]
                                            )
        
        # Collect gradients
        if self.use_complex:
            gradients = {
                'kernels': grad_kernels,
                'phase': grad_phase,
                'bias': grad_bias
            }
        else:
            gradients = {
                'kernels': grad_kernels,
                'bias': grad_bias
            }
        
        return grad_input, gradients
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get layer configuration.
        
        Returns:
            Layer configuration dictionary
        """
        return {
            'name': self.name,
            'input_dim': self.input_dim,
            'filters': self.filters,
            'kernel_size': self.kernel_size,
            'stride': self.stride,
            'padding': self.padding,
            'activation': getattr(self.activation_fn, '__name__', None),
            'use_complex': self.use_complex
        } 