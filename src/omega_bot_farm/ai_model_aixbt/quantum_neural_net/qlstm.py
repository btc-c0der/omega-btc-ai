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
Quantum Long Short-Term Memory (QLSTM)
=====================================

Implementation of quantum-inspired LSTM networks for capturing
temporal dependencies in financial time series data with
quantum-enhanced memory cells.
"""

import numpy as np
import logging
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
from .base import QuantumLayer

# Set up logging
logger = logging.getLogger("quantum-neural-net")

# Constants
LOG_PREFIX = "🧠 vQuB1T-NN"
SQRT2_INV = 1.0 / np.sqrt(2.0)

class QuantumLSTMCell(QuantumLayer):
    """
    Quantum-inspired LSTM memory cell.
    
    Implements a single Long Short-Term Memory cell with quantum-inspired
    gates and operations for processing time series data.
    """
    
    def __init__(self, units: int = 32, 
                 use_complex: bool = True,
                 recurrent_activation: str = "hadamard",
                 name: Optional[str] = None):
        """
        Initialize the Quantum LSTM cell.
        
        Args:
            units: Number of hidden units (memory dimensionality)
            use_complex: Whether to use complex numbers for quantum simulation
            recurrent_activation: Activation function for recurrent connections
            name: Name of the layer (optional)
        """
        super().__init__(name=name or "QuantumLSTMCell")
        self.params = {
            "units": units,
            "use_complex": use_complex,
            "recurrent_activation": recurrent_activation
        }
        
        self.units = units
        self.use_complex = use_complex
        self.recurrent_activation = recurrent_activation
        
        # State variables
        self.hidden_state = None
        self.cell_state = None
        
        # Cache for backward pass
        self.cache = {}
        
        logger.debug(f"{LOG_PREFIX} - Created {self.name} with {units} units, complex: {use_complex}")
    
    def initialize(self, input_shape: Tuple) -> Tuple:
        """
        Initialize the layer weights based on input shape.
        
        Args:
            input_shape: Shape of input tensor (batch_size, input_dim)
            
        Returns:
            Shape of output tensor
        """
        self.input_shape = input_shape
        
        # Get input dimension
        if len(input_shape) == 2:
            _, input_dim = input_shape
        else:
            input_dim = input_shape[0]
        
        # Set up weight data type based on configuration
        dtype = complex if self.use_complex else float
        
        # Initialize gate weights
        # Input gate (i): controls new memory cell input
        # Forget gate (f): controls how much of the old cell state to keep
        # Cell gate (c): creates candidate cell state values
        # Output gate (o): controls how much of the cell state to expose
        
        # Weight matrices for input connections to gates (4 gates × input_dim × units)
        w_init_scale = 0.1
        
        if self.use_complex:
            # For complex weights, initialize real and imaginary parts separately
            # and normalize to preserve quantum-like unitary properties
            w_real = np.random.normal(0, w_init_scale, (4, input_dim, self.units))
            w_imag = np.random.normal(0, w_init_scale, (4, input_dim, self.units))
            self.weights["kernel"] = w_real + 1j * w_imag
            
            # Normalize each gate's weights to have unit norm (quantum-inspired)
            for g in range(4):
                for j in range(self.units):
                    norm = np.sqrt(np.sum(np.abs(self.weights["kernel"][g, :, j])**2))
                    if norm > 0:
                        self.weights["kernel"][g, :, j] /= norm
        else:
            # Classical initialization for non-complex mode
            self.weights["kernel"] = np.random.normal(0, w_init_scale, (4, input_dim, self.units))
        
        # Recurrent weight matrices (4 gates × units × units)
        if self.use_complex:
            u_real = np.random.normal(0, w_init_scale, (4, self.units, self.units))
            u_imag = np.random.normal(0, w_init_scale, (4, self.units, self.units))
            self.weights["recurrent_kernel"] = u_real + 1j * u_imag
            
            # Apply constraints to make recurrent matrices closer to unitary
            for g in range(4):
                # A rough approximation of orthogonalization
                u, _, vh = np.linalg.svd(self.weights["recurrent_kernel"][g], full_matrices=False)
                self.weights["recurrent_kernel"][g] = u @ vh
        else:
            self.weights["recurrent_kernel"] = np.random.normal(0, w_init_scale, (4, self.units, self.units))
        
        # Bias terms for each gate
        self.weights["bias"] = np.zeros((4, self.units), dtype=dtype)
        
        # Forget gate bias initialized to 1.0 to encourage memory retention
        self.weights["bias"][1] = np.ones(self.units, dtype=dtype)
        
        # Initialize states to zero
        self.hidden_state = np.zeros((1, self.units), dtype=dtype)
        self.cell_state = np.zeros((1, self.units), dtype=dtype)
        
        # Set output shape
        self.output_shape = (self.units,)
        
        self.initialized = True
        logger.debug(f"{LOG_PREFIX} - {self.name} initialized: input {input_shape} → output {self.output_shape}")
        
        return self.output_shape
    
    def reset_states(self, batch_size: int = 1) -> None:
        """
        Reset the cell and hidden states.
        
        Args:
            batch_size: Batch size for state initialization
        """
        dtype = complex if self.use_complex else float
        self.hidden_state = np.zeros((batch_size, self.units), dtype=dtype)
        self.cell_state = np.zeros((batch_size, self.units), dtype=dtype)
    
    def _quantum_sigmoid(self, x: np.ndarray) -> np.ndarray:
        """
        Quantum-inspired sigmoid function.
        
        For complex input, computes a quantum-inspired gate
        that approximately maps to [0, 1] range.
        
        Args:
            x: Input tensor
            
        Returns:
            Quantum sigmoid activation
        """
        if np.iscomplexobj(x):
            # Quantum-inspired activation that preserves phase
            # Apply sigmoid to magnitude, preserve phase
            magnitude = np.abs(x)
            phase = np.angle(x)
            sigmoid_mag = 1.0 / (1.0 + np.exp(-magnitude))
            return sigmoid_mag * np.exp(1j * phase)
        else:
            # Classical sigmoid for real numbers
            return 1.0 / (1.0 + np.exp(-x))
    
    def _quantum_tanh(self, x: np.ndarray) -> np.ndarray:
        """
        Quantum-inspired tanh function.
        
        For complex input, computes a quantum-inspired gate
        that approximately maps to [-1, 1] range.
        
        Args:
            x: Input tensor
            
        Returns:
            Quantum tanh activation
        """
        if np.iscomplexobj(x):
            # Quantum-inspired activation that preserves phase
            # Apply tanh to magnitude, preserve phase
            magnitude = np.abs(x)
            phase = np.angle(x)
            tanh_mag = np.tanh(magnitude)
            return tanh_mag * np.exp(1j * phase)
        else:
            # Classical tanh for real numbers
            return np.tanh(x)
    
    def _quantum_hadamard(self, x: np.ndarray) -> np.ndarray:
        """
        Quantum-inspired Hadamard activation.
        
        A non-linear activation inspired by the Hadamard gate,
        which creates superpositions in quantum computing.
        
        Args:
            x: Input tensor
            
        Returns:
            Transformed tensor
        """
        if np.iscomplexobj(x):
            # Normalize first to preserve quantum-like properties
            norm = np.sqrt(np.sum(np.abs(x)**2, axis=-1, keepdims=True)) + 1e-10
            x_norm = x / norm
            
            # Apply Hadamard-inspired transformation
            return SQRT2_INV * (x_norm + 1j * x_norm)
        else:
            # For real inputs, approximate with a scaled ELU
            return SQRT2_INV * (x + np.where(x < 0, 0.1 * (np.exp(x) - 1), 0))
    
    def forward(self, inputs: np.ndarray, states: Optional[List[np.ndarray]] = None) -> Tuple[np.ndarray, List[np.ndarray]]:
        """
        Perform forward pass computation of the LSTM cell.
        
        Args:
            inputs: Input tensor of shape (batch_size, input_dim)
            states: Optional list of [hidden_state, cell_state]
            
        Returns:
            Tuple of (output, [hidden_state, cell_state])
        """
        # Get input dimensions
        if len(inputs.shape) == 1:
            # Single sample case
            batch_size = 1
            inputs = inputs.reshape(1, -1)
        else:
            batch_size, _ = inputs.shape
        
        # Use provided states or initialize if None
        if states is not None:
            h_prev, c_prev = states
        else:
            if self.hidden_state.shape[0] != batch_size:
                self.reset_states(batch_size)
            h_prev, c_prev = self.hidden_state, self.cell_state
        
        # Cache inputs and previous states for backward pass
        self.cache["inputs"] = inputs
        self.cache["h_prev"] = h_prev
        self.cache["c_prev"] = c_prev
        
        # Compute gate preactivations
        # Extract gate weights
        W_i, W_f, W_c, W_o = self.weights["kernel"]
        U_i, U_f, U_c, U_o = self.weights["recurrent_kernel"] 
        b_i, b_f, b_c, b_o = self.weights["bias"]
        
        # Gate preactivations
        i_preact = np.dot(inputs, W_i) + np.dot(h_prev, U_i) + b_i
        f_preact = np.dot(inputs, W_f) + np.dot(h_prev, U_f) + b_f
        c_preact = np.dot(inputs, W_c) + np.dot(h_prev, U_c) + b_c
        o_preact = np.dot(inputs, W_o) + np.dot(h_prev, U_o) + b_o
        
        # Apply gate activations
        i_gate = self._quantum_sigmoid(i_preact)
        f_gate = self._quantum_sigmoid(f_preact)
        c_tilde = self._quantum_tanh(c_preact)
        o_gate = self._quantum_sigmoid(o_preact)
        
        # Cache gate activations
        self.cache["i_gate"] = i_gate
        self.cache["f_gate"] = f_gate
        self.cache["c_tilde"] = c_tilde
        self.cache["o_gate"] = o_gate
        
        # Update cell state with quantum-inspired operations
        # New cell state combines forget gate * old cell + input gate * candidate
        c_new = f_gate * c_prev + i_gate * c_tilde
        
        # Compute output (hidden state)
        # Hidden state is output gate * activated cell state
        h_new = o_gate * self._quantum_tanh(c_new)
        
        # Cache new states
        self.cache["c_new"] = c_new
        self.cache["h_new"] = h_new
        
        # Update states
        self.hidden_state = h_new
        self.cell_state = c_new
        
        return h_new, [h_new, c_new]
    
    def backward(self, grad_output: np.ndarray, grad_states: Optional[List[np.ndarray]] = None) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
        """
        Perform backward pass (gradient computation).
        
        Args:
            grad_output: Gradient from next layer
            grad_states: Gradients for [hidden_state, cell_state] if provided
            
        Returns:
            Tuple of (gradient with respect to inputs, gradients with respect to weights)
        """
        # Retrieve cached values
        inputs = self.cache["inputs"]
        h_prev = self.cache["h_prev"]
        c_prev = self.cache["c_prev"]
        i_gate = self.cache["i_gate"]
        f_gate = self.cache["f_gate"]
        c_tilde = self.cache["c_tilde"]
        o_gate = self.cache["o_gate"]
        c_new = self.cache["c_new"]
        
        # Extract shapes
        batch_size = inputs.shape[0]
        
        # Handle gradient from next timestep if provided
        if grad_states is not None:
            dh_next, dc_next = grad_states
        else:
            dh_next = np.zeros_like(self.hidden_state)
            dc_next = np.zeros_like(self.cell_state)
        
        # Add gradient from output
        dh = grad_output + dh_next
        
        # Gradient for output gate
        do = dh * self._quantum_tanh(c_new)
        # Gradient for cell state
        dc = dc_next + dh * o_gate * (1 - self._quantum_tanh(c_new)**2)
        
        # Gradient for input and forget gates
        di = dc * c_tilde
        df = dc * c_prev
        # Gradient for cell candidate
        dc_tilde = dc * i_gate
        
        # Gradient for gate preactivations
        di_preact = di * i_gate * (1 - i_gate)
        df_preact = df * f_gate * (1 - f_gate)
        dc_tilde_preact = dc_tilde * (1 - c_tilde**2)
        do_preact = do * o_gate * (1 - o_gate)
        
        # Gradient for weights
        # Extract gate weights
        W_i, W_f, W_c, W_o = self.weights["kernel"]
        U_i, U_f, U_c, U_o = self.weights["recurrent_kernel"]
        
        # Initialize weight gradients
        dW = np.zeros_like(self.weights["kernel"])
        dU = np.zeros_like(self.weights["recurrent_kernel"])
        db = np.zeros_like(self.weights["bias"])
        
        # Gradients for kernels
        for b in range(batch_size):
            # Input weights
            dW[0] += np.outer(inputs[b], di_preact[b])
            dW[1] += np.outer(inputs[b], df_preact[b])
            dW[2] += np.outer(inputs[b], dc_tilde_preact[b])
            dW[3] += np.outer(inputs[b], do_preact[b])
            
            # Recurrent weights
            dU[0] += np.outer(h_prev[b], di_preact[b])
            dU[1] += np.outer(h_prev[b], df_preact[b])
            dU[2] += np.outer(h_prev[b], dc_tilde_preact[b])
            dU[3] += np.outer(h_prev[b], do_preact[b])
        
        # Gradient for biases (summed over batch)
        db[0] = np.sum(di_preact, axis=0)
        db[1] = np.sum(df_preact, axis=0)
        db[2] = np.sum(dc_tilde_preact, axis=0)
        db[3] = np.sum(do_preact, axis=0)
        
        # Gradient for inputs
        dx = np.zeros_like(inputs)
        for b in range(batch_size):
            dx[b] = (di_preact[b] @ W_i.T +
                     df_preact[b] @ W_f.T +
                     dc_tilde_preact[b] @ W_c.T +
                     do_preact[b] @ W_o.T)
        
        # Gradient for previous hidden state
        dh_prev = np.zeros_like(h_prev)
        for b in range(batch_size):
            dh_prev[b] = (di_preact[b] @ U_i.T +
                          df_preact[b] @ U_f.T +
                          dc_tilde_preact[b] @ U_c.T +
                          do_preact[b] @ U_o.T)
        
        # Gradient for previous cell state
        dc_prev = dc * f_gate
        
        # Return gradients
        return dx, {"kernel": dW, "recurrent_kernel": dU, "bias": db}

class QLSTM(QuantumLayer):
    """
    Quantum Long Short-Term Memory layer.
    
    This layer implements a quantum-inspired LSTM for processing
    sequence data with enhanced memory capabilities.
    """
    
    def __init__(self, units: int = 32, return_sequences: bool = False,
                 use_complex: bool = True, recurrent_activation: str = "hadamard",
                 name: Optional[str] = None):
        """
        Initialize the QLSTM layer.
        
        Args:
            units: Number of hidden units
            return_sequences: Whether to return the full sequence or just the final output
            use_complex: Whether to use complex numbers for quantum simulation
            recurrent_activation: Activation function for recurrent connections
            name: Name of the layer (optional)
        """
        super().__init__(name=name or "QLSTM")
        self.params = {
            "units": units,
            "return_sequences": return_sequences,
            "use_complex": use_complex,
            "recurrent_activation": recurrent_activation
        }
        
        self.units = units
        self.return_sequences = return_sequences
        self.use_complex = use_complex
        self.recurrent_activation = recurrent_activation
        
        # Create cell
        self.cell = QuantumLSTMCell(
            units=units,
            use_complex=use_complex,
            recurrent_activation=recurrent_activation,
            name=f"{self.name}_cell"
        )
        
        # Sequence cache for backward pass
        self.sequence_cache = {
            "inputs": None,
            "outputs": None,
            "states": None
        }
        
        logger.debug(f"{LOG_PREFIX} - Created {self.name} with {units} units, return_sequences={return_sequences}")
    
    def initialize(self, input_shape: Tuple) -> Tuple:
        """
        Initialize the layer weights based on input shape.
        
        Args:
            input_shape: Shape of input tensor (batch_size, sequence_length, features)
            
        Returns:
            Shape of output tensor
        """
        self.input_shape = input_shape
        
        # Extract sequence dimensions
        if len(input_shape) == 3:
            batch_size, seq_length, feature_dim = input_shape
        else:
            # Assume (sequence_length, features) for single sample
            seq_length, feature_dim = input_shape
            batch_size = 1
        
        # Initialize the cell with feature dimension
        self.cell.initialize((batch_size, feature_dim))
        
        # Set output shape based on return_sequences flag
        if self.return_sequences:
            if len(input_shape) == 3:
                self.output_shape = (batch_size, seq_length, self.units)
            else:
                self.output_shape = (seq_length, self.units)
        else:
            if len(input_shape) == 3:
                self.output_shape = (batch_size, self.units)
            else:
                self.output_shape = (self.units,)
        
        self.initialized = True
        logger.debug(f"{LOG_PREFIX} - {self.name} initialized: input {input_shape} → output {self.output_shape}")
        
        return self.output_shape
    
    def forward(self, inputs: np.ndarray) -> np.ndarray:
        """
        Perform forward pass computation of the QLSTM layer.
        
        Args:
            inputs: Input tensor of shape (batch_size, seq_length, features)
            
        Returns:
            Output tensor
        """
        # Cache inputs for backward pass
        self.sequence_cache["inputs"] = inputs
        
        # Get input dimensions
        if len(inputs.shape) == 3:
            batch_size, seq_length, _ = inputs.shape
        else:
            # Handle single sample case
            seq_length, _ = inputs.shape
            batch_size = 1
            inputs = inputs.reshape(1, seq_length, -1)
        
        # Reset cell states
        self.cell.reset_states(batch_size)
        
        # Initialize output containers
        if self.return_sequences:
            outputs = np.zeros((batch_size, seq_length, self.units), 
                              dtype=complex if self.use_complex else float)
        else:
            outputs = np.zeros((batch_size, self.units), 
                              dtype=complex if self.use_complex else float)
        
        # Initialize states and state history
        h = np.zeros((batch_size, self.units), dtype=complex if self.use_complex else float)
        c = np.zeros((batch_size, self.units), dtype=complex if self.use_complex else float)
        states_history = []
        
        # Process sequence
        for t in range(seq_length):
            x_t = inputs[:, t, :]
            h, [h, c] = self.cell.forward(x_t, [h, c])
            
            # Store output for each timestep if returning sequences
            if self.return_sequences:
                outputs[:, t, :] = h
            
            # Store states for backward pass
            states_history.append((h.copy(), c.copy()))
        
        # If not returning sequences, only keep the final output
        if not self.return_sequences:
            outputs = h
        
        # Cache outputs and states for backward pass
        self.sequence_cache["outputs"] = outputs
        self.sequence_cache["states"] = states_history
        
        # Remove batch dimension for single sample case if not returning sequences
        if batch_size == 1 and len(self.input_shape) == 2:
            if self.return_sequences:
                outputs = outputs.reshape(seq_length, self.units)
            else:
                outputs = outputs.reshape(self.units)
        
        return outputs
    
    def backward(self, grad_output: np.ndarray) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
        """
        Perform backward pass (gradient computation).
        
        Args:
            grad_output: Gradient from next layer
            
        Returns:
            Tuple of (gradient with respect to inputs, gradients with respect to weights)
        """
        # Retrieve cached values
        inputs = self.sequence_cache["inputs"]
        states_history = self.sequence_cache["states"]
        
        # Get input dimensions
        if len(inputs.shape) == 3:
            batch_size, seq_length, feature_dim = inputs.shape
        else:
            # Handle single sample case
            seq_length, feature_dim = inputs.shape
            batch_size = 1
            inputs = inputs.reshape(1, seq_length, feature_dim)
        
        # Reshape gradient if needed
        if not self.return_sequences:
            # For non-sequence output, the gradient is for the final output only
            if len(grad_output.shape) == 1:
                grad_output = grad_output.reshape(1, -1)
        else:
            # For sequence output, ensure gradient has batch dimension
            if len(grad_output.shape) == 2:
                grad_output = grad_output.reshape(1, seq_length, -1)
        
        # Initialize gradients
        grad_inputs = np.zeros_like(inputs)
        grad_kernel = np.zeros_like(self.cell.weights["kernel"])
        grad_recurrent = np.zeros_like(self.cell.weights["recurrent_kernel"])
        grad_bias = np.zeros_like(self.cell.weights["bias"])
        
        # Initialize backward pass
        dh_next = np.zeros((batch_size, self.units), dtype=inputs.dtype)
        dc_next = np.zeros((batch_size, self.units), dtype=inputs.dtype)
        
        # Backpropagate through time
        for t in reversed(range(seq_length)):
            # Get current timestep input
            x_t = inputs[:, t, :]
            
            # For sequence output, add gradient from output at this timestep
            if self.return_sequences:
                dh_t = grad_output[:, t, :] + dh_next
            else:
                # For single output, gradient only flows from the end
                dh_t = dh_next if t < seq_length - 1 else grad_output
            
            # Set up cell state for this timestep
            self.cell.hidden_state, self.cell.cell_state = states_history[t]
            
            # Backpropagate through cell
            dx_t, grad_weights = self.cell.backward(dh_t, [dh_next, dc_next])
            
            # Accumulate weight gradients
            grad_kernel += grad_weights["kernel"]
            grad_recurrent += grad_weights["recurrent_kernel"]
            grad_bias += grad_weights["bias"]
            
            # Store input gradient for this timestep
            grad_inputs[:, t, :] = dx_t
            
            # Get previous states for next iteration
            if t > 0:
                h_prev, c_prev = states_history[t-1]
            else:
                h_prev = np.zeros((batch_size, self.units), dtype=inputs.dtype)
                c_prev = np.zeros((batch_size, self.units), dtype=inputs.dtype)
            
            # Prepare for next timestep (going backward)
            # This requires recomputing the gate values for t-1
            if t > 0:
                self.cell.forward(inputs[:, t-1, :], [h_prev, c_prev])
                
                # Get gradient for previous timestep's hidden and cell states
                _, [dh_next, dc_next] = self.cell.backward(np.zeros_like(h_prev))
            
        # Prepare weight gradients dictionary
        weight_gradients = {
            "kernel": grad_kernel,
            "recurrent_kernel": grad_recurrent,
            "bias": grad_bias
        }
        
        # Remove batch dimension for single sample case
        if batch_size == 1 and len(self.input_shape) == 2:
            grad_inputs = grad_inputs.reshape(seq_length, feature_dim)
        
        return grad_inputs, weight_gradients 