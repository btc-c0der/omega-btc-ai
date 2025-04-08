#!/usr/bin/env python3
"""
Quantum Neural Network Utilities
==============================

Utility functions and optimizers for quantum neural network implementation.
"""

import os
import json
import pickle
import logging
import numpy as np
from typing import Dict, List, Any, Optional, Union, Callable, Type, Tuple, cast
import time
from datetime import datetime

# Set up logging
logger = logging.getLogger("quantum-neural-net")

# Constants
LOG_PREFIX = "🧠 vQuB1T-NN"

# Define simple passthrough layer for fallbacks
class SimpleLayer:
    """Simple passthrough layer for fallback cases."""
    def __init__(self, input_dim=None, output_dim=None, **kwargs):
        self.input_dim = input_dim
        self.output_dim = output_dim or input_dim
        self.name = kwargs.get('name', 'simple_layer')
        self.error = kwargs.get('error', None)
    
    def forward(self, inputs):
        if self.error:
            logger.warning(f"{LOG_PREFIX} - Using fallback layer! Original error: {self.error}")
        return inputs
    
    def backward(self, grad_output, learning_rate=0.01):
        return grad_output
    
    def get_config(self):
        return {
            'input_dim': self.input_dim,
            'output_dim': self.output_dim,
            'name': self.name
        }

# Simple model implementation for fallbacks
class SimpleModel:
    """Simple model for fallback cases."""
    def __init__(self, name="simple_model"):
        self.layers = []
        self.name = name
        
    def add(self, layer):
        self.layers.append(layer)
        
    def predict(self, x):
        # Simple forward pass through all layers
        for layer in self.layers:
            if hasattr(layer, 'forward'):
                x = layer.forward(x)
        return x
        
    def get_config(self):
        return {'layers': [getattr(layer, 'name', str(layer)) for layer in self.layers]}

# ===== Loss Functions =====

def quantum_mse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Quantum-inspired mean squared error.
    
    For complex values, considers both magnitude and phase differences.
    
    Args:
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        Loss value
    """
    if np.iscomplexobj(y_true) or np.iscomplexobj(y_pred):
        # For complex values, handle both magnitude and phase
        y_true_comp = np.asarray(y_true, dtype=complex)
        y_pred_comp = np.asarray(y_pred, dtype=complex)
        
        # Magnitude error
        mag_error = np.abs(np.abs(y_true_comp) - np.abs(y_pred_comp))
        
        # Phase error (normalized to [0, 1])
        phase_true = np.angle(y_true_comp)
        phase_pred = np.angle(y_pred_comp)
        phase_error = np.abs(np.exp(1j * phase_true) - np.exp(1j * phase_pred)) / 2
        
        # Combined error
        error = mag_error + phase_error
        
        return float(np.mean(error**2))
    else:
        # Regular MSE for real values
        return float(np.mean((y_true - y_pred)**2))

# Add gradient method for MSE
def mse_gradient(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """Gradient of MSE loss."""
    return 2 * (y_pred - y_true) / len(y_true)

# Attach the gradient function
setattr(quantum_mse, 'gradient', mse_gradient)

def quantum_crossentropy(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-10) -> float:
    """
    Quantum-inspired cross-entropy loss.
    
    Treats input as probability amplitudes for quantum states.
    
    Args:
        y_true: True values
        y_pred: Predicted values
        eps: Small value to avoid log(0)
        
    Returns:
        Loss value
    """
    # Ensure proper normalization (quantum probability-like)
    if np.iscomplexobj(y_true) or np.iscomplexobj(y_pred):
        # For complex values, use probability-like normalization
        y_true_prob = np.abs(y_true)**2
        y_pred_prob = np.abs(y_pred)**2
    else:
        # Softmax-like normalization for real values
        y_true_exp = np.exp(y_true - np.max(y_true, axis=-1, keepdims=True))
        y_pred_exp = np.exp(y_pred - np.max(y_pred, axis=-1, keepdims=True))
        
        y_true_prob = y_true_exp / (np.sum(y_true_exp, axis=-1, keepdims=True) + eps)
        y_pred_prob = y_pred_exp / (np.sum(y_pred_exp, axis=-1, keepdims=True) + eps)
    
    # Classical cross-entropy formula
    return float(-np.mean(np.sum(y_true_prob * np.log(y_pred_prob + eps), axis=-1)))

# Add gradient method for cross-entropy
def crossentropy_gradient(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-10) -> np.ndarray:
    """Gradient of quantum cross-entropy loss."""
    if np.iscomplexobj(y_true) or np.iscomplexobj(y_pred):
        # For complex values
        y_pred_prob = np.abs(y_pred)**2
        y_true_prob = np.abs(y_true)**2
        
        # Gradient includes chain rule for squared magnitude
        grad = -2 * y_true_prob / (y_pred_prob + eps) * np.conjugate(y_pred)
        return grad / len(y_true)
    else:
        # Softmax-like normalization
        y_pred_exp = np.exp(y_pred - np.max(y_pred, axis=-1, keepdims=True))
        y_pred_prob = y_pred_exp / (np.sum(y_pred_exp, axis=-1, keepdims=True) + eps)
        
        return (y_pred_prob - y_true) / len(y_true)

# Attach the gradient function
setattr(quantum_crossentropy, 'gradient', crossentropy_gradient)

def quantum_fidelity_loss(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-10) -> float:
    """
    Quantum fidelity loss based on how close two quantum states are.
    
    Args:
        y_true: True values
        y_pred: Predicted values
        eps: Small value for numerical stability
        
    Returns:
        Loss value (lower is better)
    """
    # Import here to avoid circular import
    from .metrics import quantum_fidelity
    # Fidelity is from 0 to 1, where 1 is perfect match
    # Convert to loss where 0 is perfect match
    return float(1.0 - quantum_fidelity(y_true, y_pred))

# Add gradient method for fidelity loss
def fidelity_loss_gradient(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-10) -> np.ndarray:
    """Approximate gradient of quantum fidelity loss."""
    # Normalize inputs to quantum state-like representations
    if np.iscomplexobj(y_true) or np.iscomplexobj(y_pred):
        # For complex values
        y_true_norm = y_true / (np.sqrt(np.sum(np.abs(y_true)**2)) + eps)
        y_pred_norm = y_pred / (np.sqrt(np.sum(np.abs(y_pred)**2)) + eps)
        
        # Approximate gradient (negative direction of maximum fidelity)
        grad = -y_true_norm + np.sum(y_true_norm * np.conjugate(y_pred_norm)) * y_pred_norm
        return grad / len(y_true)
    else:
        # For real values
        y_true_norm = y_true / (np.linalg.norm(y_true) + eps)
        y_pred_norm = y_pred / (np.linalg.norm(y_pred) + eps)
        
        # Gradient of cosine similarity
        similarity = np.dot(y_true_norm, y_pred_norm)
        grad = -y_true_norm + similarity * y_pred_norm
        return grad / len(y_true)

# Attach the gradient function
setattr(quantum_fidelity_loss, 'gradient', fidelity_loss_gradient)

# ===== Optimizers =====

class QuantumOptimizer:
    """Base class for quantum-inspired optimizers."""
    
    def __init__(self, learning_rate: float = 0.01, **kwargs):
        """
        Initialize the optimizer.
        
        Args:
            learning_rate: Learning rate
            **kwargs: Additional optimizer parameters
        """
        self.learning_rate = learning_rate
        self.params = kwargs
    
    def update(self, params: np.ndarray, gradients: np.ndarray) -> np.ndarray:
        """
        Update parameters with gradients.
        
        Args:
            params: Current parameters
            gradients: Gradients of loss with respect to parameters
            
        Returns:
            Updated parameters
        """
        raise NotImplementedError("Subclasses must implement update method")

class QuantumSGD(QuantumOptimizer):
    """
    Quantum-inspired Stochastic Gradient Descent.
    
    Includes phase-aware updates for complex parameters.
    """
    
    def __init__(self, learning_rate: float = 0.01, momentum: float = 0.0, **kwargs):
        """
        Initialize the SGD optimizer.
        
        Args:
            learning_rate: Learning rate
            momentum: Momentum factor
            **kwargs: Additional optimizer parameters
        """
        super().__init__(learning_rate, **kwargs)
        self.momentum = momentum
        self.velocity = 0
    
    def update(self, params: np.ndarray, gradients: np.ndarray) -> np.ndarray:
        """
        Update parameters with SGD.
        
        Args:
            params: Current parameters
            gradients: Gradients of loss with respect to parameters
            
        Returns:
            Updated parameters
        """
        # Apply momentum
        self.velocity = self.momentum * self.velocity + self.learning_rate * gradients
        
        if np.iscomplexobj(params):
            # For complex parameters, preserve phase relationships
            # Update both real and imaginary parts separately
            updated_params = params - self.velocity
        else:
            # Regular update for real parameters
            updated_params = params - self.velocity
        
        return updated_params

class QuantumAdam(QuantumOptimizer):
    """
    Quantum-inspired Adam optimizer.
    
    Enhanced for complex-valued parameters with phase-aware updates.
    """
    
    def __init__(self, learning_rate: float = 0.001, beta1: float = 0.9, 
                beta2: float = 0.999, epsilon: float = 1e-8, **kwargs):
        """
        Initialize the Adam optimizer.
        
        Args:
            learning_rate: Learning rate
            beta1: Exponential decay rate for first moment
            beta2: Exponential decay rate for second moment
            epsilon: Small constant for numerical stability
            **kwargs: Additional optimizer parameters
        """
        super().__init__(learning_rate, **kwargs)
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = 0  # First moment
        self.v = 0  # Second moment
        self.t = 0  # Timestep
    
    def update(self, params: np.ndarray, gradients: np.ndarray) -> np.ndarray:
        """
        Update parameters with Adam.
        
        Args:
            params: Current parameters
            gradients: Gradients of loss with respect to parameters
            
        Returns:
            Updated parameters
        """
        self.t += 1
        
        # Update moments
        self.m = self.beta1 * self.m + (1 - self.beta1) * gradients
        
        if np.iscomplexobj(gradients):
            # For complex gradients, compute second moment on squared magnitude
            self.v = self.beta2 * self.v + (1 - self.beta2) * np.abs(gradients)**2
        else:
            self.v = self.beta2 * self.v + (1 - self.beta2) * gradients**2
        
        # Bias correction
        m_hat = self.m / (1 - self.beta1**self.t)
        v_hat = self.v / (1 - self.beta2**self.t)
        
        # Update parameters
        if np.iscomplexobj(params):
            # For complex parameters, preserve phase relationships
            update = self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)
            updated_params = params - update
        else:
            # Regular update for real parameters
            updated_params = params - self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)
        
        return updated_params

class QuantumRMSProp(QuantumOptimizer):
    """
    Quantum-inspired RMSProp optimizer.
    
    Adapted for complex parameters with phase-aware updates.
    """
    
    def __init__(self, learning_rate: float = 0.001, decay: float = 0.9, 
                epsilon: float = 1e-8, **kwargs):
        """
        Initialize the RMSProp optimizer.
        
        Args:
            learning_rate: Learning rate
            decay: Decay rate for squared gradient
            epsilon: Small constant for numerical stability
            **kwargs: Additional optimizer parameters
        """
        super().__init__(learning_rate, **kwargs)
        self.decay = decay
        self.epsilon = epsilon
        self.squared_grad = 0
    
    def update(self, params: np.ndarray, gradients: np.ndarray) -> np.ndarray:
        """
        Update parameters with RMSProp.
        
        Args:
            params: Current parameters
            gradients: Gradients of loss with respect to parameters
            
        Returns:
            Updated parameters
        """
        if np.iscomplexobj(gradients):
            # For complex gradients, compute squared gradient on magnitude
            self.squared_grad = self.decay * self.squared_grad + \
                               (1 - self.decay) * np.abs(gradients)**2
        else:
            self.squared_grad = self.decay * self.squared_grad + \
                               (1 - self.decay) * gradients**2
        
        # Update parameters
        if np.iscomplexobj(params):
            # For complex parameters, preserve phase relationships
            updated_params = params - self.learning_rate * gradients / \
                           (np.sqrt(self.squared_grad) + self.epsilon)
        else:
            updated_params = params - self.learning_rate * gradients / \
                           (np.sqrt(self.squared_grad) + self.epsilon)
        
        return updated_params

# ===== Utility Functions =====

def get_optimizer(optimizer_name: str, **kwargs) -> QuantumOptimizer:
    """
    Get optimizer by name.
    
    Args:
        optimizer_name: Name of the optimizer
        **kwargs: Additional optimizer parameters
        
    Returns:
        Optimizer instance
    """
    optimizers = {
        'quantum_sgd': QuantumSGD,
        'quantum_adam': QuantumAdam,
        'quantum_rmsprop': QuantumRMSProp
    }
    
    # Default to Adam
    optimizer_class = optimizers.get(optimizer_name.lower(), QuantumAdam)
    return optimizer_class(**kwargs)

def get_loss_function(loss_name: str) -> Callable:
    """
    Get loss function by name.
    
    Args:
        loss_name: Name of the loss function
        
    Returns:
        Loss function
    """
    loss_functions = {
        'quantum_mse': quantum_mse,
        'quantum_crossentropy': quantum_crossentropy,
        'quantum_fidelity_loss': quantum_fidelity_loss
    }
    
    # Default to MSE
    return loss_functions.get(loss_name.lower(), quantum_mse)

def get_metrics(metrics_names: List[str]) -> List[Callable]:
    """
    Get metrics functions by name.
    
    Args:
        metrics_names: List of metric names
        
    Returns:
        List of metric functions
    """
    # Import here to avoid circular import
    from .metrics import (
        quantum_fidelity, 
        entanglement_entropy,
        prediction_accuracy, 
        quantum_advantage_factor
    )
    
    metrics_functions = {
        'quantum_fidelity': quantum_fidelity,
        'entanglement_entropy': entanglement_entropy,
        'prediction_accuracy': prediction_accuracy,
        'quantum_advantage_factor': quantum_advantage_factor
    }
    
    metrics = []
    for name in metrics_names:
        metric_fn = metrics_functions.get(name.lower())
        if metric_fn is not None:
            metrics.append(metric_fn)
    
    return metrics

def create_layer_from_name(layer_name: str, **kwargs) -> Any:
    """
    Create a layer instance from name.
    
    Args:
        layer_name: Layer name or type
        **kwargs: Additional layer parameters
        
    Returns:
        Layer instance
    """
    # Import modules lazily to avoid circular imports and linter errors
    from importlib import import_module
    
    # Map of layer types to their module paths
    layer_modules = {
        'qcnn': '.qcnn.QCNN',
        'qlstm': '.qlstm.QLSTM',
        'entanglement_layer': '.entanglement.EntanglementLayer',
        'variational_circuit': '.variational.VariationalQuantumLayer',
        'classical_dense': '.classical_layers.DenseLayer',
    }
    
    try:
        # Look up module path for the requested layer
        if layer_name.lower() in layer_modules:
            module_path, class_name = layer_modules[layer_name.lower()].rsplit('.', 1)
            module = import_module(module_path, package='omega_bot_farm.ai_model_aixbt.quantum_neural_net')
            layer_class = getattr(module, class_name)
            # Return an instance of the layer
            return layer_class(**kwargs)
        else:
            # Default fallback if layer type not recognized
            logger.warning(f"{LOG_PREFIX} - Unknown layer type: {layer_name}. Using simple passthrough layer.")
            # Return a copy of SimpleLayer (already defined at module level)
            return SimpleLayer(input_dim=kwargs.get('input_dim'), 
                              output_dim=kwargs.get('output_dim'),
                              name=kwargs.get('name', 'simple_layer'))
            
    except Exception as e:
        logger.error(f"{LOG_PREFIX} - Error creating layer {layer_name}: {e}")
        # Return a simple fallback layer in case of errors
        return SimpleLayer(input_dim=kwargs.get('input_dim'), 
                          output_dim=kwargs.get('output_dim'),
                          name=kwargs.get('name', 'fallback_layer'),
                          error=str(e))

def quantum_loss(loss_fn: Callable, y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Compute quantum loss with protection against bad inputs.
    
    Args:
        loss_fn: Loss function
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        Loss value
    """
    try:
        # Ensure arrays have compatible shapes
        if y_true.shape != y_pred.shape:
            # Try to match shapes
            if len(y_true.shape) < len(y_pred.shape):
                # Broadcast y_true to match y_pred
                y_true = np.broadcast_to(y_true, y_pred.shape)
            elif len(y_pred.shape) < len(y_true.shape):
                # Broadcast y_pred to match y_true
                y_pred = np.broadcast_to(y_pred, y_true.shape)
        
        return float(loss_fn(y_true, y_pred))
    except Exception as e:
        logger.error(f"{LOG_PREFIX} - Error computing loss: {e}")
        # Return a high loss value to indicate failure
        return 1e6

def quantum_gradient(loss_fn: Callable, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Compute gradient of quantum loss.
    
    Args:
        loss_fn: Loss function with gradient method
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        Gradient of loss with respect to y_pred
    """
    if hasattr(loss_fn, 'gradient'):
        # Use analytical gradient if available
        gradient_fn = getattr(loss_fn, 'gradient')
        return gradient_fn(y_true, y_pred)
    else:
        # Compute numerical gradient (central difference)
        epsilon = 1e-7
        grads = np.zeros_like(y_pred)
        
        # Iterate over all elements - handle as nested loops for type safety
        for idx in np.ndindex(y_pred.shape):
            # Save original value
            old_value = y_pred[idx]
            
            # Forward difference
            y_pred[idx] = old_value + epsilon
            f_plus = loss_fn(y_true, y_pred)
            
            # Backward difference
            y_pred[idx] = old_value - epsilon
            f_minus = loss_fn(y_true, y_pred)
            
            # Central difference gradient
            grads[idx] = (f_plus - f_minus) / (2 * epsilon)
            
            # Restore original value
            y_pred[idx] = old_value
        
        return grads

def save_model(model: Any, filepath: str) -> None:
    """
    Save quantum model to disk.
    
    Args:
        model: Quantum model to save
        filepath: Path to save file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    
    # Add timestamp to filename if not specified
    if not filepath.endswith('.pkl') and not filepath.endswith('.json'):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"{filepath}_{timestamp}.pkl"
    
    try:
        # Save model using pickle
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
        
        # Also save a JSON config for reference
        config_path = os.path.splitext(filepath)[0] + '_config.json'
        if hasattr(model, 'get_config'):
            config = model.get_config()
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
        
        logger.info(f"{LOG_PREFIX} - Model saved to {filepath}")
    except Exception as e:
        logger.error(f"{LOG_PREFIX} - Error saving model: {e}")

def load_model(filepath: str) -> Any:
    """
    Load quantum model from disk.
    
    Args:
        filepath: Path to model file
        
    Returns:
        Loaded quantum model
    """
    try:
        # Load model using pickle
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        
        logger.info(f"{LOG_PREFIX} - Model loaded from {filepath}")
        return model
    except Exception as e:
        logger.error(f"{LOG_PREFIX} - Error loading model: {e}")
        
        # Try to construct a new model from config
        config_path = os.path.splitext(filepath)[0] + '_config.json'
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Dynamically import the model class
            try:
                from .base import QuantumModel
                model = QuantumModel()
                
                # Add layers from config
                for layer_config in config.get('layers', []):
                    if isinstance(layer_config, dict) and 'class' in layer_config:
                        layer_class_name = layer_config.get('class')
                        layer_params = layer_config.get('params', {})
                        if layer_class_name:
                            layer = create_layer_from_name(layer_class_name, **layer_params)
                            if layer:
                                model.add(layer)
                    elif isinstance(layer_config, str):
                        layer = create_layer_from_name(layer_config)
                        if layer:
                            model.add(layer)
                
                logger.warning(f"{LOG_PREFIX} - Reconstructed model from config: {config_path}")
                return model
            except ImportError:
                # Fallback to a simple model implementation
                model = SimpleModel(name="reconstructed_model")
                
                # Add layers from config
                for layer_config in config.get('layers', []):
                    if isinstance(layer_config, dict) and 'class' in layer_config:
                        layer_class_name = layer_config.get('class')
                        layer_params = layer_config.get('params', {})
                        if layer_class_name:
                            layer = create_layer_from_name(layer_class_name, **layer_params)
                            if layer:
                                model.add(layer)
                    elif isinstance(layer_config, str):
                        layer = create_layer_from_name(layer_config)
                        if layer:
                            model.add(layer)
                
                logger.warning(f"{LOG_PREFIX} - Created simple fallback model with config")
                return model
                
        except Exception as e2:
            logger.error(f"{LOG_PREFIX} - Error loading model from config: {e2}")
            # Last resort, return a simple model
            return SimpleModel(name="empty_fallback_model")

def quantum_random(shape: Union[int, Tuple[int, ...]], complex_values: bool = False) -> np.ndarray:
    """
    Generate quantum-inspired random numbers.
    
    Args:
        shape: Shape of output array
        complex_values: Whether to generate complex values
        
    Returns:
        Array of random values
    """
    if complex_values:
        # Generate complex random values with phase
        real_part = np.random.normal(0, 1, shape)
        imag_part = np.random.normal(0, 1, shape)
        
        # Normalize to unit circles (quantum state-like)
        magnitude = np.sqrt(real_part**2 + imag_part**2)
        magnitude = np.where(magnitude == 0, 1.0, magnitude)
        
        return (real_part + 1j * imag_part) / magnitude
    else:
        # Generate real-valued random numbers
        return np.random.uniform(0, 1, shape)

def quantum_timer(func: Callable) -> Callable:
    """
    Decorator to time quantum functions.
    
    Args:
        func: Function to time
        
    Returns:
        Wrapped function
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logger.debug(f"{LOG_PREFIX} - {func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    
    return wrapper 