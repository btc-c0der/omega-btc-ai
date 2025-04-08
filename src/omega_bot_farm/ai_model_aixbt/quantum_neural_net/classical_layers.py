#!/usr/bin/env python3
"""
Classical Layers for Quantum Neural Networks
===========================================

This module provides classical neural network layers that can be used in 
conjunction with quantum layers, allowing for hybrid classical-quantum networks.
"""

import numpy as np
from typing import Dict, List, Optional, Union, Tuple, Callable, Any
import logging

from .base import QuantumLayer

# Set up logging
logger = logging.getLogger("quantum-neural-net")
LOG_PREFIX = "🧠 vQuB1T-NN"

class DenseLayer(QuantumLayer):
    """
    Classical dense (fully connected) layer.
    
    This is a traditional neural network layer that can be integrated
    with quantum layers to create hybrid classical-quantum architectures.
    """
    
    def __init__(self, 
                input_dim: int, 
                output_dim: int, 
                activation: str = None,
                use_bias: bool = True,
                weight_initializer: str = 'glorot_uniform',
                use_complex: bool = False,
                name: str = "dense"):
        """
        Initialize the dense layer.
        
        Args:
            input_dim: Input dimension
            output_dim: Output dimension
            activation: Activation function to use
            use_bias: Whether to include bias terms
            weight_initializer: Weight initialization method
            use_complex: Whether to use complex-valued weights
            name: Name of the layer
        """
        super().__init__(
            input_dim=input_dim,
            output_dim=output_dim,
            activation=activation,
            use_complex=use_complex,
            name=name
        )
        
        self.use_bias = use_bias
        self.weight_initializer = weight_initializer
        
        # Initialize weights and biases
        self.initialize_weights()
    
    def initialize_weights(self):
        """Initialize weights using the specified initializer."""
        # Determine initialization scaling
        if self.weight_initializer == 'glorot_uniform':
            # Glorot/Xavier initialization
            limit = np.sqrt(6.0 / (self.input_dim + self.output_dim))
            
            if self.use_complex:
                self.weights = (
                    np.random.uniform(-limit, limit, (self.input_dim, self.output_dim)) +
                    1j * np.random.uniform(-limit, limit, (self.input_dim, self.output_dim))
                )
                
                if self.use_bias:
                    self.bias = (
                        np.random.uniform(-limit, limit, (self.output_dim,)) +
                        1j * np.random.uniform(-limit, limit, (self.output_dim,))
                    )
            else:
                self.weights = np.random.uniform(-limit, limit, (self.input_dim, self.output_dim))
                
                if self.use_bias:
                    self.bias = np.random.uniform(-limit, limit, (self.output_dim,))
        
        elif self.weight_initializer == 'he_normal':
            # He initialization (for ReLU-like activations)
            stddev = np.sqrt(2.0 / self.input_dim)
            
            if self.use_complex:
                self.weights = (
                    np.random.normal(0, stddev, (self.input_dim, self.output_dim)) +
                    1j * np.random.normal(0, stddev, (self.input_dim, self.output_dim))
                )
                
                if self.use_bias:
                    self.bias = (
                        np.random.normal(0, stddev, (self.output_dim,)) +
                        1j * np.random.normal(0, stddev, (self.output_dim,))
                    )
            else:
                self.weights = np.random.normal(0, stddev, (self.input_dim, self.output_dim))
                
                if self.use_bias:
                    self.bias = np.random.normal(0, stddev, (self.output_dim,))
        
        else:
            # Default to small random values
            stddev = 0.1
            
            if self.use_complex:
                self.weights = (
                    np.random.normal(0, stddev, (self.input_dim, self.output_dim)) +
                    1j * np.random.normal(0, stddev, (self.input_dim, self.output_dim))
                )
                
                if self.use_bias:
                    self.bias = (
                        np.random.normal(0, stddev, (self.output_dim,)) +
                        1j * np.random.normal(0, stddev, (self.output_dim,))
                    )
            else:
                self.weights = np.random.normal(0, stddev, (self.input_dim, self.output_dim))
                
                if self.use_bias:
                    self.bias = np.random.normal(0, stddev, (self.output_dim,))
                
        if not self.use_bias:
            # Set bias to zero if not using bias
            self.bias = np.zeros(self.output_dim, dtype=complex if self.use_complex else float)
    
    def get_weights(self) -> List[np.ndarray]:
        """
        Get all trainable weights.
        
        Returns:
            List of weight arrays
        """
        return [self.weights, self.bias] if self.use_bias else [self.weights]
    
    def set_weights(self, weights: List[np.ndarray]) -> None:
        """
        Set all trainable weights.
        
        Args:
            weights: List of weight arrays
        """
        if self.use_bias and len(weights) != 2:
            raise ValueError(f"Expected 2 weight arrays with bias, got {len(weights)}")
        elif not self.use_bias and len(weights) != 1:
            raise ValueError(f"Expected 1 weight array without bias, got {len(weights)}")
        
        self.weights = weights[0]
        
        if self.use_bias:
            self.bias = weights[1]
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        Forward pass through the dense layer.
        
        Args:
            x: Input data (batch_size, input_dim)
            
        Returns:
            Output data (batch_size, output_dim)
        """
        # Cache input for backward pass
        self._cached_input = x
        
        # Linear transformation: y = x @ W + b
        output = x @ self.weights
        
        if self.use_bias:
            output = output + self.bias
        
        # Apply activation function if specified
        if self.activation_fn is not None:
            output = self.activation_fn(output)
        
        return output
    
    def backward(self, 
                grad_output: np.ndarray, 
                learning_rate: float = 0.01) -> np.ndarray:
        """
        Backward pass to compute gradients and update weights.
        
        Args:
            grad_output: Gradient of loss with respect to output
            learning_rate: Learning rate for weight updates
            
        Returns:
            Gradient of loss with respect to input
        """
        # If activation function was applied, compute gradient through it
        if self.activation_fn is not None and hasattr(self.activation_fn, 'gradient'):
            grad_output = self.activation_fn.gradient(self._cached_output, grad_output)
        
        # Gradient of loss with respect to weights: dL/dW = x^T @ dL/dy
        grad_weights = self._cached_input.T @ grad_output
        
        # Gradient of loss with respect to bias: dL/db = sum(dL/dy)
        if self.use_bias:
            grad_bias = np.sum(grad_output, axis=0)
        
        # Gradient of loss with respect to input: dL/dx = dL/dy @ W^T
        grad_input = grad_output @ self.weights.T
        
        # Update weights and biases
        self.weights -= learning_rate * grad_weights
        
        if self.use_bias:
            self.bias -= learning_rate * grad_bias
        
        return grad_input
    
    def get_config(self) -> Dict:
        """
        Get layer configuration.
        
        Returns:
            Layer configuration dictionary
        """
        config = super().get_config()
        config.update({
            'use_bias': self.use_bias,
            'weight_initializer': self.weight_initializer
        })
        return config


class BatchNormalizationLayer(QuantumLayer):
    """
    Batch normalization layer.
    
    Normalizes inputs across a batch, allowing for more stable training.
    Can handle both real and complex-valued inputs.
    """
    
    def __init__(self, 
                input_dim: int,
                momentum: float = 0.99,
                epsilon: float = 1e-5,
                use_complex: bool = False,
                name: str = "batch_norm"):
        """
        Initialize the batch normalization layer.
        
        Args:
            input_dim: Input dimension
            momentum: Momentum for moving average
            epsilon: Small constant for numerical stability
            use_complex: Whether to use complex-valued weights
            name: Name of the layer
        """
        super().__init__(
            input_dim=input_dim,
            output_dim=input_dim,  # Output dimension is same as input
            activation=None,
            use_complex=use_complex,
            name=name
        )
        
        self.momentum = momentum
        self.epsilon = epsilon
        
        # Initialize parameters
        self.initialize_parameters()
    
    def initialize_parameters(self):
        """Initialize batch normalization parameters."""
        # Learnable parameters - scale and shift
        if self.use_complex:
            self.gamma = np.ones(self.input_dim, dtype=complex)
            self.beta = np.zeros(self.input_dim, dtype=complex)
        else:
            self.gamma = np.ones(self.input_dim, dtype=float)
            self.beta = np.zeros(self.input_dim, dtype=float)
        
        # Running statistics for inference
        self.running_mean = np.zeros(self.input_dim, dtype=complex if self.use_complex else float)
        self.running_var = np.ones(self.input_dim, dtype=float)  # Variance is always real
        
        # For tracking batch count
        self.batch_count = 0
    
    def get_weights(self) -> List[np.ndarray]:
        """
        Get all trainable weights.
        
        Returns:
            List of weight arrays
        """
        return [self.gamma, self.beta]
    
    def set_weights(self, weights: List[np.ndarray]) -> None:
        """
        Set all trainable weights.
        
        Args:
            weights: List of weight arrays
        """
        if len(weights) != 2:
            raise ValueError(f"Expected 2 weight arrays, got {len(weights)}")
        
        self.gamma = weights[0]
        self.beta = weights[1]
    
    def forward(self, x: np.ndarray, training: bool = True) -> np.ndarray:
        """
        Forward pass through the batch normalization layer.
        
        Args:
            x: Input data (batch_size, input_dim)
            training: Whether in training mode
            
        Returns:
            Normalized output data (batch_size, output_dim)
        """
        # Cache input for backward pass
        self._cached_input = x
        
        if training:
            # Calculate statistics on current batch
            if self.use_complex or np.iscomplexobj(x):
                # For complex inputs, handle real and imaginary parts separately
                batch_mean = np.mean(x, axis=0)
                # Variance is calculated on magnitude for complex values
                batch_var = np.var(np.abs(x), axis=0)
            else:
                batch_mean = np.mean(x, axis=0)
                batch_var = np.var(x, axis=0)
            
            # Update running statistics
            self.running_mean = self.momentum * self.running_mean + (1 - self.momentum) * batch_mean
            self.running_var = self.momentum * self.running_var + (1 - self.momentum) * batch_var
            
            # Cache batch statistics for backward pass
            self._cached_mean = batch_mean
            self._cached_var = batch_var
            self._cached_std = np.sqrt(batch_var + self.epsilon)
            
            # Normalize using batch statistics
            if self.use_complex or np.iscomplexobj(x):
                # For complex inputs, normalize maintaining phase
                normalized = (x - batch_mean) / (np.sqrt(batch_var + self.epsilon))
            else:
                normalized = (x - batch_mean) / (np.sqrt(batch_var + self.epsilon))
            
        else:
            # Use running statistics for inference
            if self.use_complex or np.iscomplexobj(x):
                normalized = (x - self.running_mean) / (np.sqrt(self.running_var + self.epsilon))
            else:
                normalized = (x - self.running_mean) / (np.sqrt(self.running_var + self.epsilon))
        
        # Apply scale and shift
        output = self.gamma * normalized + self.beta
        
        # Cache normalized output for backward pass
        self._cached_normalized = normalized
        
        return output
    
    def backward(self, 
                grad_output: np.ndarray, 
                learning_rate: float = 0.01) -> np.ndarray:
        """
        Backward pass to compute gradients and update weights.
        
        Args:
            grad_output: Gradient of loss with respect to output
            learning_rate: Learning rate for weight updates
            
        Returns:
            Gradient of loss with respect to input
        """
        batch_size = self._cached_input.shape[0]
        
        # Gradient with respect to gamma and beta
        grad_gamma = np.sum(grad_output * self._cached_normalized, axis=0)
        grad_beta = np.sum(grad_output, axis=0)
        
        # Gradient with respect to normalized input
        grad_normalized = grad_output * self.gamma
        
        # Gradient with respect to input
        if self.use_complex or np.iscomplexobj(self._cached_input):
            # For complex inputs
            grad_var = -0.5 * np.sum(grad_normalized * (self._cached_input - self._cached_mean) / 
                                    (self._cached_var + self.epsilon)**1.5, axis=0)
            
            grad_mean = -np.sum(grad_normalized / np.sqrt(self._cached_var + self.epsilon), axis=0) - \
                       2 * grad_var * np.mean(self._cached_input - self._cached_mean, axis=0)
            
            grad_input = grad_normalized / np.sqrt(self._cached_var + self.epsilon) + \
                        2 * grad_var * (self._cached_input - self._cached_mean) / batch_size + \
                        grad_mean / batch_size
        else:
            # For real inputs
            grad_var = -0.5 * np.sum(grad_normalized * (self._cached_input - self._cached_mean) / 
                                    (self._cached_var + self.epsilon)**1.5, axis=0)
            
            grad_mean = -np.sum(grad_normalized / np.sqrt(self._cached_var + self.epsilon), axis=0) - \
                       2 * grad_var * np.mean(self._cached_input - self._cached_mean, axis=0)
            
            grad_input = grad_normalized / np.sqrt(self._cached_var + self.epsilon) + \
                        2 * grad_var * (self._cached_input - self._cached_mean) / batch_size + \
                        grad_mean / batch_size
        
        # Update parameters
        self.gamma -= learning_rate * grad_gamma
        self.beta -= learning_rate * grad_beta
        
        return grad_input
    
    def get_config(self) -> Dict:
        """
        Get layer configuration.
        
        Returns:
            Layer configuration dictionary
        """
        config = super().get_config()
        config.update({
            'momentum': self.momentum,
            'epsilon': self.epsilon
        })
        return config


class DropoutLayer(QuantumLayer):
    """
    Dropout layer for regularization.
    
    Randomly sets a fraction of input units to 0 during training, which helps
    prevent overfitting. Can handle both real and complex-valued inputs.
    """
    
    def __init__(self, 
                input_dim: int,
                dropout_rate: float = 0.5,
                use_complex: bool = False,
                name: str = "dropout"):
        """
        Initialize the dropout layer.
        
        Args:
            input_dim: Input dimension
            dropout_rate: Fraction of the input units to drop
            use_complex: Whether to use complex-valued weights
            name: Name of the layer
        """
        super().__init__(
            input_dim=input_dim,
            output_dim=input_dim,  # Output dimension is same as input
            activation=None,
            use_complex=use_complex,
            name=name
        )
        
        self.dropout_rate = dropout_rate
        self.mask = None
    
    def forward(self, x: np.ndarray, training: bool = True) -> np.ndarray:
        """
        Forward pass through the dropout layer.
        
        Args:
            x: Input data (batch_size, input_dim)
            training: Whether in training mode
            
        Returns:
            Output data with dropout applied (batch_size, output_dim)
        """
        # Cache input for backward pass
        self._cached_input = x
        
        if not training or self.dropout_rate == 0:
            return x
        
        # Generate dropout mask
        self.mask = np.random.binomial(1, 1 - self.dropout_rate, size=x.shape) / (1 - self.dropout_rate)
        
        # Apply dropout mask
        output = x * self.mask
        
        return output
    
    def backward(self, 
                grad_output: np.ndarray, 
                learning_rate: float = 0.01) -> np.ndarray:
        """
        Backward pass to compute gradients.
        
        Args:
            grad_output: Gradient of loss with respect to output
            learning_rate: Learning rate (not used)
            
        Returns:
            Gradient of loss with respect to input
        """
        # If not in training mode or no dropout applied, gradient passes through unchanged
        if self.mask is None:
            return grad_output
        
        # Apply same mask to gradients
        grad_input = grad_output * self.mask
        
        return grad_input
    
    def get_config(self) -> Dict:
        """
        Get layer configuration.
        
        Returns:
            Layer configuration dictionary
        """
        config = super().get_config()
        config.update({
            'dropout_rate': self.dropout_rate
        })
        return config 