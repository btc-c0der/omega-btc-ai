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
Base Classes for Quantum Neural Networks
=======================================

Core abstract classes and interfaces for quantum-inspired neural network layers
and models for financial time series prediction.
"""

import os
import json
import logging
import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
from abc import ABC, abstractmethod

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("quantum-neural-net")

# Constants
LOG_PREFIX = "🧠 vQuB1T-NN"

class QuantumActivation(ABC):
    """
    Base class for quantum activation functions.
    
    Quantum activation functions are inspired by quantum gates and operations.
    They provide non-linearities in quantum neural networks similar to how
    classical activation functions work in classical neural networks.
    """
    
    def __init__(self, **kwargs):
        """Initialize the quantum activation function."""
        self.params = kwargs
        self.name = self.__class__.__name__
    
    @abstractmethod
    def apply(self, inputs: np.ndarray) -> np.ndarray:
        """Apply the quantum activation function to inputs."""
        pass
    
    @abstractmethod
    def gradient(self, inputs: np.ndarray) -> np.ndarray:
        """Compute the gradient of the quantum activation function."""
        pass
    
    def __call__(self, inputs: np.ndarray) -> np.ndarray:
        """Make the activation function callable."""
        return self.apply(inputs)

class QuantumLayer(ABC):
    """
    Base class for quantum neural network layers.
    
    Quantum layers are the building blocks of quantum neural networks.
    They implement quantum-inspired transformations on input data.
    """
    
    def __init__(self, name: Optional[str] = None, **kwargs):
        """
        Initialize the quantum layer.
        
        Args:
            name: Name of the layer (optional)
            **kwargs: Additional layer parameters
        """
        self.name = name or self.__class__.__name__
        self.params = kwargs
        self.weights = {}
        self.initialized = False
        self.input_shape = None
        self.output_shape = None
    
    @abstractmethod
    def initialize(self, input_shape: Tuple) -> Tuple:
        """
        Initialize the layer weights based on input shape.
        
        Args:
            input_shape: Shape of input tensor
            
        Returns:
            Shape of output tensor
        """
        self.input_shape = input_shape
        self.initialized = True
        return input_shape  # Default to same shape
    
    @abstractmethod
    def forward(self, inputs: np.ndarray) -> np.ndarray:
        """
        Perform forward pass computation.
        
        Args:
            inputs: Input tensor
            
        Returns:
            Output tensor
        """
        pass
    
    @abstractmethod
    def backward(self, grad_output: np.ndarray) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
        """
        Perform backward pass (gradient computation).
        
        Args:
            grad_output: Gradient from next layer
            
        Returns:
            Tuple of (gradient with respect to inputs, gradients with respect to weights)
        """
        pass
    
    def __call__(self, inputs: np.ndarray) -> np.ndarray:
        """Make the layer callable for easier sequential model building."""
        if not self.initialized:
            self.initialize(inputs.shape)
        return self.forward(inputs)
    
    def get_config(self) -> Dict[str, Any]:
        """Get layer configuration for serialization."""
        return {
            "name": self.name,
            "class": self.__class__.__name__,
            "params": self.params
        }
    
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> 'QuantumLayer':
        """Create a layer from config dictionary."""
        return cls(name=config["name"], **config["params"])

class QuantumModel:
    """
    Quantum Neural Network Model.
    
    A sequential model built from quantum layers for prediction tasks.
    """
    
    def __init__(self, layers: Optional[List[Union[QuantumLayer, str]]] = None):
        """
        Initialize the quantum model.
        
        Args:
            layers: List of layers or layer type strings
        """
        self.layers = layers or []
        self.compiled = False
        self.optimizer = None
        self.loss_fn = None
        self.metrics = []
        self.history = {
            "loss": [],
            "val_loss": []
        }
        
        logger.info(f"{LOG_PREFIX} - Quantum model initialized with {len(self.layers)} layers")
    
    def add(self, layer: Union[QuantumLayer, str]) -> None:
        """
        Add a layer to the model.
        
        Args:
            layer: Quantum layer or layer type string
        """
        self.layers.append(layer)
        logger.info(f"{LOG_PREFIX} - Added layer: {layer if isinstance(layer, str) else layer.name}")
    
    def compile(self, optimizer: str = 'quantum_adam', loss: str = 'quantum_mse',
               metrics: List[str] = None) -> None:
        """
        Compile the model for training.
        
        Args:
            optimizer: Optimizer name or function
            loss: Loss function name or function
            metrics: List of metrics to track
        """
        from .utils import get_optimizer, get_loss_function, get_metrics
        
        self.optimizer = get_optimizer(optimizer)
        self.loss_fn = get_loss_function(loss)
        self.metrics = get_metrics(metrics or ['quantum_fidelity'])
        self.compiled = True
        
        logger.info(f"{LOG_PREFIX} - Model compiled with {optimizer} optimizer and {loss} loss")
    
    def _build(self, input_shape: Tuple) -> None:
        """
        Build the model by initializing all layers.
        
        Args:
            input_shape: Input shape for the first layer
        """
        shape = input_shape
        for i, layer in enumerate(self.layers):
            if isinstance(layer, str):
                # Replace string layer with actual layer instance
                from .utils import create_layer_from_name
                self.layers[i] = layer = create_layer_from_name(layer)
            
            shape = layer.initialize(shape)
            logger.debug(f"{LOG_PREFIX} - Layer {i} ({layer.name}) input: {layer.input_shape}, output: {shape}")
    
    def train(self, x: np.ndarray, y: np.ndarray, epochs: int = 10, batch_size: int = 32,
              validation_data: Optional[Tuple[np.ndarray, np.ndarray]] = None) -> Dict[str, List[float]]:
        """
        Train the model on data.
        
        Args:
            x: Training inputs
            y: Target outputs
            epochs: Number of training epochs
            batch_size: Batch size for training
            validation_data: Optional validation data tuple (x_val, y_val)
            
        Returns:
            Training history dictionary
        """
        if not self.compiled:
            logger.warning(f"{LOG_PREFIX} - Model not compiled. Using default settings.")
            self.compile()
        
        # Build the model if not already built
        if not self.layers or not hasattr(self.layers[0], 'initialized') or not self.layers[0].initialized:
            self._build(x.shape[1:])
        
        # Training loop
        n_samples = x.shape[0]
        n_batches = (n_samples + batch_size - 1) // batch_size
        
        for epoch in range(epochs):
            epoch_loss = 0.0
            
            # Shuffle data
            indices = np.random.permutation(n_samples)
            x_shuffled = x[indices]
            y_shuffled = y[indices]
            
            for batch in range(n_batches):
                start_idx = batch * batch_size
                end_idx = min(start_idx + batch_size, n_samples)
                
                x_batch = x_shuffled[start_idx:end_idx]
                y_batch = y_shuffled[start_idx:end_idx]
                
                # Forward pass
                y_pred = self.predict(x_batch)
                
                # Compute loss
                batch_loss = self.loss_fn(y_batch, y_pred)
                epoch_loss += batch_loss * (end_idx - start_idx) / n_samples
                
                # Backward pass (gradient computation)
                self._backward(y_batch, y_pred)
                
                # Update weights using optimizer
                self._update_weights()
            
            # Record metrics
            self.history["loss"].append(epoch_loss)
            
            # Validation
            if validation_data is not None:
                x_val, y_val = validation_data
                y_val_pred = self.predict(x_val)
                val_loss = self.loss_fn(y_val, y_val_pred)
                self.history["val_loss"].append(val_loss)
                
                logger.info(f"{LOG_PREFIX} - Epoch {epoch+1}/{epochs}: loss={epoch_loss:.4f}, val_loss={val_loss:.4f}")
            else:
                logger.info(f"{LOG_PREFIX} - Epoch {epoch+1}/{epochs}: loss={epoch_loss:.4f}")
        
        logger.info(f"{LOG_PREFIX} - Training completed. Final loss: {self.history['loss'][-1]:.4f}")
        return self.history
    
    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Generate predictions for input samples.
        
        Args:
            x: Input data
            
        Returns:
            Model predictions
        """
        # Build the model if not already built
        if not self.layers or not hasattr(self.layers[0], 'initialized') or not self.layers[0].initialized:
            self._build(x.shape[1:])
        
        # Forward pass through all layers
        outputs = x
        for layer in self.layers:
            outputs = layer(outputs)
        
        return outputs
    
    def _backward(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        """
        Perform backward pass through the network.
        
        Args:
            y_true: True values
            y_pred: Predicted values
        """
        # Initial gradient from loss function
        grad = self.loss_fn.gradient(y_true, y_pred)
        
        # Backward pass through layers in reverse order
        for layer in reversed(self.layers):
            grad, weight_gradients = layer.backward(grad)
            
            # Store gradients for optimizer
            for param_name, param_grad in weight_gradients.items():
                layer.weights[param_name + "_grad"] = param_grad
    
    def _update_weights(self) -> None:
        """Update weights using the optimizer."""
        for layer in self.layers:
            # Get trainable weights
            trainable_weights = {k: v for k, v in layer.weights.items() if not k.endswith("_grad")}
            
            # Get corresponding gradients
            weight_gradients = {k: layer.weights[k + "_grad"] for k in trainable_weights.keys()}
            
            # Update each weight using optimizer
            for weight_name, weight in trainable_weights.items():
                gradient = weight_gradients[weight_name]
                layer.weights[weight_name] = self.optimizer.update(weight, gradient)
    
    def evaluate(self, x: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """
        Evaluate the model on test data.
        
        Args:
            x: Test inputs
            y: True outputs
            
        Returns:
            Dictionary of metrics
        """
        y_pred = self.predict(x)
        loss = self.loss_fn(y, y_pred)
        
        metrics = {"loss": loss}
        for metric_fn in self.metrics:
            metrics[metric_fn.__name__] = metric_fn(y, y_pred)
        
        return metrics
    
    def save(self, filepath: str) -> None:
        """
        Save the model to disk.
        
        Args:
            filepath: Path to save model
        """
        from .utils import save_model
        save_model(self, filepath)
        logger.info(f"{LOG_PREFIX} - Model saved to {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> 'QuantumModel':
        """
        Load a model from disk.
        
        Args:
            filepath: Path to saved model
            
        Returns:
            Loaded model
        """
        from .utils import load_model
        model = load_model(filepath)
        logger.info(f"{LOG_PREFIX} - Model loaded from {filepath}")
        return model
    
    def get_config(self) -> Dict[str, Any]:
        """Get model configuration for serialization."""
        return {
            "layers": [layer.get_config() if hasattr(layer, 'get_config') else str(layer) 
                      for layer in self.layers],
            "optimizer": self.optimizer.__class__.__name__ if self.optimizer else None,
            "loss": self.loss_fn.__name__ if self.loss_fn else None,
            "metrics": [metric.__name__ for metric in self.metrics]
        } 