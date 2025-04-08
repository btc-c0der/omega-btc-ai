#!/usr/bin/env python3
"""
Quantum Neural Network Model
============================

Implementation of a full Quantum Neural Network model with composable
layers for financial time series prediction and trading signal generation.
"""

import numpy as np
from typing import Dict, List, Optional, Union, Tuple, Any, Callable
import logging
import json
import os

# Import quantum layers and utilities
from .qcnn import QCNN
try:
    from .variational import VariationalQuantumLayer
    from .classical_layers import DenseLayer, BatchNormalizationLayer, DropoutLayer
except ImportError:
    # Fallback stubs for required classes if modules are not yet implemented
    class VariationalQuantumLayer:
        pass
    class DenseLayer:
        pass
    class BatchNormalizationLayer:
        pass
    class DropoutLayer:
        pass

# Import metrics for model evaluation
try:
    from .metrics import quantum_fidelity, entanglement_entropy, prediction_accuracy
except ImportError:
    # Fallback metrics
    def quantum_fidelity(y_true, y_pred):
        return np.mean(np.abs(np.sum(np.conj(y_true) * y_pred, axis=1)))
    
    def entanglement_entropy(y_true, y_pred):
        err = y_true - y_pred
        return -np.sum(np.abs(err)**2 * np.log(np.abs(err)**2 + 1e-10))
    
    def prediction_accuracy(y_true, y_pred, task="regression"):
        if task == "classification":
            return np.mean(np.argmax(y_true, axis=1) == np.argmax(y_pred, axis=1))
        else:
            return np.mean(np.abs(y_true - y_pred) < 0.1)

# Import loss functions and optimizers
try:
    from .utils import quantum_mse, quantum_crossentropy, QuantumAdam, QuantumSGD
except ImportError:
    # Fallback loss functions and optimizer
    def quantum_mse(y_true, y_pred):
        return np.mean(np.abs(y_true - y_pred)**2)
    
    def quantum_crossentropy(y_true, y_pred):
        return -np.mean(y_true * np.log(y_pred + 1e-10))
    
    class QuantumAdam:
        def __init__(self, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
            self.learning_rate = learning_rate
            self.beta1 = beta1
            self.beta2 = beta2
            self.epsilon = epsilon
            self.m = {}
            self.v = {}
            self.t = 0
            
        def update(self, params, grads):
            self.t += 1
            for k, param in params.items():
                if k not in self.m:
                    self.m[k] = np.zeros_like(param)
                    self.v[k] = np.zeros_like(param)
                
                self.m[k] = self.beta1 * self.m[k] + (1 - self.beta1) * grads[k]
                self.v[k] = self.beta2 * self.v[k] + (1 - self.beta2) * (grads[k]**2)
                
                m_hat = self.m[k] / (1 - self.beta1**self.t)
                v_hat = self.v[k] / (1 - self.beta2**self.t)
                
                params[k] -= self.learning_rate * m_hat / (np.sqrt(v_hat) + self.epsilon)
            
            return params
    
    class QuantumSGD:
        def __init__(self, learning_rate=0.01):
            self.learning_rate = learning_rate
            
        def update(self, params, grads):
            for k, param in params.items():
                params[k] -= self.learning_rate * grads[k]
            
            return params

# Set up logging
logger = logging.getLogger("quantum-neural-net")
LOG_PREFIX = "🧠 vQuB1T-NN"

class QuantumNeuralNetwork:
    """
    Quantum Neural Network Model
    
    A neural network model incorporating quantum-inspired layers
    for financial time series prediction and trading signal generation.
    """
    
    def __init__(self, name: str = "QuantumModel"):
        """
        Initialize a quantum neural network model.
        
        Args:
            name: Name of the model
        """
        self.name = name
        self.layers = []
        self.is_compiled = False
        self.optimizer = None
        self.loss_fn = None
        self.metrics = {}
        self.training_history = {
            "loss": [],
            "val_loss": [],
            "metrics": {}
        }
        
        logger.info(f"{LOG_PREFIX} - Created Quantum Neural Network: {name}")
    
    def add(self, layer: Any) -> None:
        """
        Add a layer to the model.
        
        Args:
            layer: Layer to add (QCNN, VariationalQuantumLayer, DenseLayer, etc.)
        """
        self.layers.append(layer)
        logger.debug(f"{LOG_PREFIX} - Added layer: {layer.__class__.__name__}")
    
    def compile(self, 
                optimizer: Union[str, Any] = "quantum_adam", 
                loss: Union[str, Callable] = "quantum_mse",
                metrics: List[Union[str, Callable]] = None) -> None:
        """
        Compile the model.
        
        Args:
            optimizer: Optimizer to use ('quantum_adam', 'quantum_sgd', or custom optimizer instance)
            loss: Loss function to use ('quantum_mse', 'quantum_crossentropy', or custom function)
            metrics: List of metrics to compute during training and evaluation
        """
        # Set optimizer
        if isinstance(optimizer, str):
            if optimizer.lower() == "quantum_adam":
                self.optimizer = QuantumAdam()
            elif optimizer.lower() == "quantum_sgd":
                self.optimizer = QuantumSGD()
            else:
                raise ValueError(f"Unknown optimizer: {optimizer}")
        else:
            self.optimizer = optimizer
        
        # Set loss function
        if isinstance(loss, str):
            if loss.lower() == "quantum_mse":
                self.loss_fn = quantum_mse
            elif loss.lower() in ["quantum_crossentropy", "quantum_cross_entropy"]:
                self.loss_fn = quantum_crossentropy
            else:
                raise ValueError(f"Unknown loss function: {loss}")
        else:
            self.loss_fn = loss
        
        # Set metrics
        self.metrics = {}
        if metrics:
            for metric in metrics:
                if isinstance(metric, str):
                    if metric.lower() == "quantum_fidelity":
                        self.metrics["quantum_fidelity"] = quantum_fidelity
                    elif metric.lower() == "entanglement_entropy":
                        self.metrics["entanglement_entropy"] = entanglement_entropy
                    elif metric.lower() == "accuracy":
                        self.metrics["accuracy"] = lambda y_true, y_pred: prediction_accuracy(y_true, y_pred, "classification")
                    elif metric.lower() == "regression_accuracy":
                        self.metrics["regression_accuracy"] = lambda y_true, y_pred: prediction_accuracy(y_true, y_pred, "regression")
                    else:
                        logger.warning(f"{LOG_PREFIX} - Unknown metric: {metric}")
                else:
                    # Custom metric function
                    self.metrics[metric.__name__] = metric
                    
        self.is_compiled = True
        logger.info(f"{LOG_PREFIX} - Compiled model with optimizer: {self.optimizer.__class__.__name__}, "
                  f"loss: {self.loss_fn.__name__}, metrics: {list(self.metrics.keys())}")
    
    def _forward(self, inputs: np.ndarray, training: bool = False) -> np.ndarray:
        """
        Forward pass through the model.
        
        Args:
            inputs: Input data
            training: Whether in training mode or not
            
        Returns:
            Model output
        """
        x = inputs
        
        for layer in self.layers:
            try:
                x = layer.forward(x)
            except AttributeError:
                # Try __call__ instead
                x = layer(x)
            
        return x
    
    def _backward(self, grad_output: np.ndarray) -> Dict[str, Dict[str, np.ndarray]]:
        """
        Backward pass through the model.
        
        Args:
            grad_output: Gradient of loss with respect to output
            
        Returns:
            Dictionary of gradients for each layer
        """
        gradients = {}
        
        for i in range(len(self.layers) - 1, -1, -1):
            layer = self.layers[i]
            
            try:
                # Propagate gradients backward
                if i > 0:
                    grad_output, layer_grads = layer.backward(grad_output)
                else:
                    # For the first layer, we don't need the gradient with respect to input
                    _, layer_grads = layer.backward(grad_output)
                
                gradients[f"layer_{i}"] = layer_grads
            except (AttributeError, TypeError) as e:
                logger.warning(f"{LOG_PREFIX} - Layer {i} does not support backward pass: {e}")
        
        return gradients
    
    def _update_parameters(self, gradients: Dict[str, Dict[str, np.ndarray]]) -> None:
        """
        Update model parameters using the optimizer.
        
        Args:
            gradients: Dictionary of gradients for each layer
        """
        for i, layer in enumerate(self.layers):
            layer_key = f"layer_{i}"
            
            if layer_key in gradients:
                try:
                    # Get current weights
                    params = {}
                    for key, value in gradients[layer_key].items():
                        if hasattr(layer, key):
                            params[key] = getattr(layer, key)
                    
                    # Update parameters
                    updated_params = self.optimizer.update(params, gradients[layer_key])
                    
                    # Set updated weights
                    for key, value in updated_params.items():
                        if hasattr(layer, key):
                            setattr(layer, key, value)
                
                except (AttributeError, TypeError) as e:
                    logger.warning(f"{LOG_PREFIX} - Cannot update parameters for layer {i}: {e}")
    
    def fit(self, 
            x_train: np.ndarray, 
            y_train: np.ndarray, 
            epochs: int = 10, 
            batch_size: int = 32,
            validation_data: Optional[Tuple[np.ndarray, np.ndarray]] = None,
            verbose: int = 1,
            callbacks: List[Any] = None) -> Dict[str, List[float]]:
        """
        Train the model.
        
        Args:
            x_train: Training inputs
            y_train: Training targets
            epochs: Number of epochs to train
            batch_size: Batch size
            validation_data: Tuple of (x_val, y_val) for validation
            verbose: Verbosity level (0=silent, 1=progress bar, 2=one line per epoch)
            callbacks: List of callbacks to apply during training
            
        Returns:
            Training history
        """
        if not self.is_compiled:
            raise ValueError("Model must be compiled before training")
        
        # Initialize history for metrics
        for metric_name in self.metrics:
            if metric_name not in self.training_history["metrics"]:
                self.training_history["metrics"][metric_name] = []
            
            if validation_data is not None:
                val_metric_name = f"val_{metric_name}"
                if val_metric_name not in self.training_history["metrics"]:
                    self.training_history["metrics"][val_metric_name] = []
        
        # Training loop
        num_samples = x_train.shape[0]
        num_batches = int(np.ceil(num_samples / batch_size))
        
        for epoch in range(epochs):
            epoch_loss = 0.0
            metrics_values = {metric: 0.0 for metric in self.metrics}
            
            # Shuffle data
            indices = np.random.permutation(num_samples)
            x_shuffled = x_train[indices]
            y_shuffled = y_train[indices]
            
            # Batch training
            for batch_idx in range(num_batches):
                start_idx = batch_idx * batch_size
                end_idx = min(start_idx + batch_size, num_samples)
                
                x_batch = x_shuffled[start_idx:end_idx]
                y_batch = y_shuffled[start_idx:end_idx]
                
                # Forward pass
                y_pred = self._forward(x_batch, training=True)
                
                # Compute loss
                batch_loss = self.loss_fn(y_batch, y_pred)
                epoch_loss += batch_loss * (end_idx - start_idx) / num_samples
                
                # Compute metrics
                for metric_name, metric_fn in self.metrics.items():
                    metric_value = metric_fn(y_batch, y_pred)
                    metrics_values[metric_name] += metric_value * (end_idx - start_idx) / num_samples
                
                # Compute gradient of loss with respect to predictions
                if hasattr(self.loss_fn, "gradient"):
                    # Use custom gradient if available
                    grad_output = self.loss_fn.gradient(y_batch, y_pred)
                else:
                    # Numerical approximation of gradient
                    epsilon = 1e-7
                    grad_output = np.zeros_like(y_pred)
                    
                    for i in range(y_pred.shape[0]):
                        for j in range(y_pred.size // y_pred.shape[0]):
                            # Compute partial derivative for each output element
                            idx = np.unravel_index(j, y_pred.shape[1:])
                            y_pred_plus = y_pred.copy()
                            y_pred_plus[(i,) + idx] += epsilon
                            
                            loss_plus = self.loss_fn(y_batch, y_pred_plus)
                            grad_output[(i,) + idx] = (loss_plus - batch_loss) / epsilon
                
                # Backward pass
                gradients = self._backward(grad_output)
                
                # Update parameters
                self._update_parameters(gradients)
            
            # Validation
            val_loss = None
            val_metrics = {}
            
            if validation_data is not None:
                x_val, y_val = validation_data
                y_val_pred = self._forward(x_val, training=False)
                
                val_loss = self.loss_fn(y_val, y_val_pred)
                
                for metric_name, metric_fn in self.metrics.items():
                    val_metric_value = metric_fn(y_val, y_val_pred)
                    val_metrics[f"val_{metric_name}"] = val_metric_value
            
            # Log progress
            if verbose > 0:
                progress_msg = f"Epoch {epoch+1}/{epochs} - loss: {epoch_loss:.4f}"
                
                for metric_name, metric_value in metrics_values.items():
                    progress_msg += f" - {metric_name}: {metric_value:.4f}"
                
                if val_loss is not None:
                    progress_msg += f" - val_loss: {val_loss:.4f}"
                    
                    for metric_name, metric_value in val_metrics.items():
                        progress_msg += f" - {metric_name}: {metric_value:.4f}"
                
                logger.info(f"{LOG_PREFIX} - {progress_msg}")
            
            # Update history
            self.training_history["loss"].append(float(epoch_loss))
            
            if val_loss is not None:
                self.training_history["val_loss"].append(float(val_loss))
            
            for metric_name, metric_value in metrics_values.items():
                self.training_history["metrics"][metric_name].append(float(metric_value))
            
            for metric_name, metric_value in val_metrics.items():
                self.training_history["metrics"][metric_name].append(float(metric_value))
            
            # Execute callbacks
            if callbacks:
                for callback in callbacks:
                    if hasattr(callback, "on_epoch_end"):
                        callback.on_epoch_end(epoch, {
                            "loss": epoch_loss,
                            "val_loss": val_loss,
                            **metrics_values,
                            **val_metrics
                        })
        
        return self.training_history
    
    def predict(self, x: np.ndarray, batch_size: int = 32) -> np.ndarray:
        """
        Make predictions with the model.
        
        Args:
            x: Input data
            batch_size: Batch size for predictions
            
        Returns:
            Model predictions
        """
        num_samples = x.shape[0]
        num_batches = int(np.ceil(num_samples / batch_size))
        
        # Initialize output array
        sample_output = self._forward(x[:1], training=False)
        output_shape = list(sample_output.shape)[1:]
        predictions = np.zeros([num_samples] + output_shape, dtype=sample_output.dtype)
        
        # Batch predictions
        for batch_idx in range(num_batches):
            start_idx = batch_idx * batch_size
            end_idx = min(start_idx + batch_size, num_samples)
            
            x_batch = x[start_idx:end_idx]
            predictions[start_idx:end_idx] = self._forward(x_batch, training=False)
        
        return predictions
    
    def evaluate(self, 
                x: np.ndarray, 
                y: np.ndarray, 
                batch_size: int = 32,
                verbose: int = 1) -> Dict[str, float]:
        """
        Evaluate the model.
        
        Args:
            x: Input data
            y: Target data
            batch_size: Batch size for evaluation
            verbose: Verbosity level
            
        Returns:
            Dictionary of metrics
        """
        predictions = self.predict(x, batch_size=batch_size)
        
        # Compute loss
        loss = self.loss_fn(y, predictions)
        
        # Compute metrics
        metrics_values = {}
        for metric_name, metric_fn in self.metrics.items():
            metrics_values[metric_name] = metric_fn(y, predictions)
        
        # Log results
        if verbose > 0:
            result_msg = f"Evaluation - loss: {loss:.4f}"
            
            for metric_name, metric_value in metrics_values.items():
                result_msg += f" - {metric_name}: {metric_value:.4f}"
            
            logger.info(f"{LOG_PREFIX} - {result_msg}")
        
        return {"loss": float(loss), **{k: float(v) for k, v in metrics_values.items()}}
    
    def summary(self) -> None:
        """Print a summary of the model architecture."""
        print(f"\n{LOG_PREFIX} - Model: {self.name}")
        print("_" * 80)
        print("Layer (type)                 Output Shape              Param #")
        print("=" * 80)
        
        total_params = 0
        
        for i, layer in enumerate(self.layers):
            # Get layer type
            layer_type = layer.__class__.__name__
            
            # Get output shape (approximate)
            if hasattr(layer, "output_dim"):
                output_shape = str(layer.output_dim)
            elif hasattr(layer, "output_shape"):
                output_shape = str(layer.output_shape)
            else:
                output_shape = "Unknown"
            
            # Count parameters
            params = 0
            if hasattr(layer, "get_weights"):
                for w in layer.get_weights():
                    params += np.size(w)
            
            # Format the line
            line = f"{i+1:<3} {layer_type:<25} {output_shape:<25} {params:,}"
            print(line)
            
            total_params += params
        
        print("=" * 80)
        print(f"Total params: {total_params:,}")
        print(f"Trainable params: {total_params:,}")
        print(f"Non-trainable params: 0")
        print("_" * 80)
    
    def save(self, filepath: str) -> None:
        """
        Save the model to disk.
        
        Args:
            filepath: Path to save the model
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        
        # Save model architecture and weights
        model_data = {
            "name": self.name,
            "layers": [],
            "training_history": self.training_history
        }
        
        # Save layer configurations and weights
        for i, layer in enumerate(self.layers):
            layer_data = {
                "type": layer.__class__.__name__,
                "index": i
            }
            
            # Save configuration if available
            if hasattr(layer, "get_config"):
                layer_data["config"] = layer.get_config()
            
            # Save weights if available
            if hasattr(layer, "get_weights"):
                weights_path = f"{filepath}_layer_{i}_weights.npy"
                np.save(weights_path, layer.get_weights())
                layer_data["weights_path"] = weights_path
            
            model_data["layers"].append(layer_data)
        
        # Save model architecture to JSON
        with open(filepath, "w") as f:
            json.dump(model_data, f, indent=2)
        
        logger.info(f"{LOG_PREFIX} - Model saved to {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> 'QuantumNeuralNetwork':
        """
        Load a model from disk.
        
        Args:
            filepath: Path to load the model from
            
        Returns:
            Loaded model
        """
        # Load model architecture from JSON
        with open(filepath, "r") as f:
            model_data = json.load(f)
        
        # Create model
        model = cls(name=model_data["name"])
        
        # Load layer configurations and weights
        for layer_data in sorted(model_data["layers"], key=lambda x: x["index"]):
            layer_type = layer_data["type"]
            
            # Create layer based on type
            if layer_type == "QCNN":
                layer = QCNN(**layer_data.get("config", {}))
            elif layer_type == "VariationalQuantumLayer":
                layer = VariationalQuantumLayer(**layer_data.get("config", {}))
            elif layer_type == "DenseLayer":
                layer = DenseLayer(**layer_data.get("config", {}))
            elif layer_type == "BatchNormalizationLayer":
                layer = BatchNormalizationLayer(**layer_data.get("config", {}))
            elif layer_type == "DropoutLayer":
                layer = DropoutLayer(**layer_data.get("config", {}))
            else:
                logger.warning(f"{LOG_PREFIX} - Unknown layer type: {layer_type}")
                continue
            
            # Load weights if available
            if "weights_path" in layer_data and hasattr(layer, "set_weights"):
                weights = np.load(layer_data["weights_path"], allow_pickle=True)
                layer.set_weights(weights)
            
            # Add layer to model
            model.add(layer)
        
        # Load training history
        if "training_history" in model_data:
            model.training_history = model_data["training_history"]
        
        logger.info(f"{LOG_PREFIX} - Model loaded from {filepath}")
        return model

# Example model builder function
def create_quantum_cnn(
    input_shape: Union[int, Tuple[int, ...]], 
    output_dim: int,
    n_filters: int = 4,
    kernel_size: int = 3,
    use_complex: bool = True,
    activation: str = "relu",
    final_activation: Optional[str] = None
) -> QuantumNeuralNetwork:
    """
    Create a Quantum CNN model for financial time series prediction.
    
    Args:
        input_shape: Input shape (e.g., (sequence_length, features))
        output_dim: Output dimension
        n_filters: Number of filters in QCNN layer
        kernel_size: Kernel size for convolution
        use_complex: Whether to use complex-valued weights
        activation: Activation function
        final_activation: Final activation function
        
    Returns:
        QuantumNeuralNetwork model
    """
    model = QuantumNeuralNetwork(name="QuantumCNN")
    
    # Add QCNN layer
    model.add(QCNN(
        input_dim=input_shape,
        filters=n_filters,
        kernel_size=kernel_size,
        padding="same",
        activation=activation,
        use_complex=use_complex
    ))
    
    # Add Dense output layer
    try:
        model.add(DenseLayer(
            input_dim=n_filters,
            output_dim=output_dim,
            activation=final_activation,
            use_complex=use_complex
        ))
    except NameError:
        # Fallback if DenseLayer is not implemented
        logger.warning(f"{LOG_PREFIX} - DenseLayer not available, model may not be functional")
    
    return model 