#!/usr/bin/env python3
"""
Variational Quantum Circuit Layer
================================

Implementation of variational quantum circuits for neural networks.
These are parameterized quantum circuits that can be trained via gradient descent.
"""

import numpy as np
from typing import Dict, List, Optional, Union, Tuple, Callable
import logging

from .base import QuantumLayer

# Set up logging
logger = logging.getLogger("quantum-neural-net")
LOG_PREFIX = "🧠 vQuB1T-NN"

class VariationalQuantumLayer(QuantumLayer):
    """
    Variational Quantum Circuit Layer
    
    Implements a variational quantum circuit that can be trained via 
    gradient descent. This layer parameterizes quantum operations 
    using trainable weights.
    """
    
    def __init__(self, 
                 input_dim: int, 
                 output_dim: int, 
                 n_qubits: int = None,
                 circuit_depth: int = 2,
                 activation: str = None,
                 use_complex: bool = True,
                 name: str = "variational_circuit"):
        """
        Initialize the variational quantum layer.
        
        Args:
            input_dim: Input dimension
            output_dim: Output dimension
            n_qubits: Number of qubits (defaults to log2 of max(input_dim, output_dim))
            circuit_depth: Depth of the variational circuit
            activation: Activation function to use
            use_complex: Whether to use complex-valued weights
            name: Name of the layer
        """
        # If n_qubits not specified, calculate from dimensions
        if n_qubits is None:
            n_qubits = max(
                int(np.ceil(np.log2(input_dim))),
                int(np.ceil(np.log2(output_dim)))
            )
        
        super().__init__(
            input_dim=input_dim,
            output_dim=output_dim,
            activation=activation,
            use_complex=use_complex,
            name=name
        )
        
        self.n_qubits = n_qubits
        self.circuit_depth = circuit_depth
        
        # Initialize weights for the circuit
        # We need weights for each layer of the circuit
        self.initialize_weights()
    
    def initialize_weights(self):
        """Initialize the weights for the variational circuit."""
        # For a variational circuit, we need several types of weights:
        # 1. Rotation angles for each qubit for each layer
        # 2. Entanglement parameters between qubits
        
        # Standard deviation for initialization
        stddev = 0.1
        
        if self.use_complex:
            # Complex-valued weights
            # Rotation angles for X, Y, Z rotations for each qubit in each layer
            self.rotation_weights = (
                np.random.normal(0, stddev, (self.circuit_depth, self.n_qubits, 3)) +
                1j * np.random.normal(0, stddev, (self.circuit_depth, self.n_qubits, 3))
            )
            
            # Entanglement parameters (for CNOT-like operations)
            self.entanglement_weights = (
                np.random.normal(0, stddev, (self.circuit_depth, self.n_qubits, self.n_qubits)) +
                1j * np.random.normal(0, stddev, (self.circuit_depth, self.n_qubits, self.n_qubits))
            )
            
            # Input embedding weights
            self.input_weights = (
                np.random.normal(0, stddev, (self.input_dim, self.n_qubits)) +
                1j * np.random.normal(0, stddev, (self.input_dim, self.n_qubits))
            )
            
            # Output measurement weights
            self.output_weights = (
                np.random.normal(0, stddev, (self.n_qubits, self.output_dim)) +
                1j * np.random.normal(0, stddev, (self.n_qubits, self.output_dim))
            )
        else:
            # Real-valued weights
            # Rotation angles for X, Y, Z rotations for each qubit in each layer
            self.rotation_weights = np.random.normal(0, stddev, (self.circuit_depth, self.n_qubits, 3))
            
            # Entanglement parameters (for CNOT-like operations)
            self.entanglement_weights = np.random.normal(0, stddev, (self.circuit_depth, self.n_qubits, self.n_qubits))
            
            # Input embedding weights
            self.input_weights = np.random.normal(0, stddev, (self.input_dim, self.n_qubits))
            
            # Output measurement weights
            self.output_weights = np.random.normal(0, stddev, (self.n_qubits, self.output_dim))
    
    def get_weights(self) -> List[np.ndarray]:
        """
        Get all trainable weights.
        
        Returns:
            List of weight arrays
        """
        return [
            self.rotation_weights, 
            self.entanglement_weights,
            self.input_weights,
            self.output_weights
        ]
    
    def set_weights(self, weights: List[np.ndarray]) -> None:
        """
        Set all trainable weights.
        
        Args:
            weights: List of weight arrays
        """
        if len(weights) != 4:
            raise ValueError(f"Expected 4 weight arrays, got {len(weights)}")
        
        self.rotation_weights = weights[0]
        self.entanglement_weights = weights[1]
        self.input_weights = weights[2]
        self.output_weights = weights[3]
    
    def _apply_rotations(self, state: np.ndarray, layer_idx: int) -> np.ndarray:
        """
        Apply rotation gates to the quantum state.
        
        Args:
            state: Current quantum state
            layer_idx: Index of the current circuit layer
            
        Returns:
            Updated quantum state
        """
        # Get rotation angles for this layer
        rotations = self.rotation_weights[layer_idx]
        
        for qubit in range(self.n_qubits):
            # Apply X, Y, Z rotations to each qubit
            # For simplicity, we approximate with classical operations
            
            # X rotation (around X-axis)
            theta_x = np.abs(rotations[qubit, 0])
            if self.use_complex:
                # Phase from complex weight
                phase_x = np.angle(rotations[qubit, 0])
                x_rot = np.cos(theta_x/2) + 1j * np.sin(theta_x/2) * np.exp(1j * phase_x)
            else:
                x_rot = np.cos(theta_x/2) + 1j * np.sin(theta_x/2)
            
            # Apply rotation to state vector
            # In a real quantum circuit, this would be a proper unitary operation
            # Here we simplify with a phase shift on the appropriate amplitudes
            state = self._apply_single_qubit_rotation(state, qubit, x_rot, 'X')
            
            # Y rotation (around Y-axis)
            theta_y = np.abs(rotations[qubit, 1])
            if self.use_complex:
                phase_y = np.angle(rotations[qubit, 1])
                y_rot = np.cos(theta_y/2) + 1j * np.sin(theta_y/2) * np.exp(1j * phase_y)
            else:
                y_rot = np.cos(theta_y/2) + 1j * np.sin(theta_y/2)
            
            state = self._apply_single_qubit_rotation(state, qubit, y_rot, 'Y')
            
            # Z rotation (around Z-axis)
            theta_z = np.abs(rotations[qubit, 2])
            if self.use_complex:
                phase_z = np.angle(rotations[qubit, 2])
                z_rot = np.cos(theta_z/2) + 1j * np.sin(theta_z/2) * np.exp(1j * phase_z)
            else:
                z_rot = np.cos(theta_z/2) + 1j * np.sin(theta_z/2)
            
            state = self._apply_single_qubit_rotation(state, qubit, z_rot, 'Z')
        
        return state
    
    def _apply_single_qubit_rotation(self, 
                                    state: np.ndarray, 
                                    qubit: int, 
                                    rotation: complex, 
                                    axis: str) -> np.ndarray:
        """
        Apply a single-qubit rotation to the state vector.
        
        Args:
            state: Current quantum state
            qubit: Target qubit
            rotation: Rotation parameter (complex number)
            axis: Rotation axis ('X', 'Y', or 'Z')
            
        Returns:
            Updated quantum state
        """
        # In a real quantum simulation, we would apply the full unitary matrix
        # For this simplified model, we'll just apply phase shifts
        
        # Create mask for the target qubit's 0 and 1 states
        mask_0 = np.zeros_like(state)
        mask_1 = np.zeros_like(state)
        
        # For each basis state, check if the target qubit is 0 or 1
        for i in range(len(state)):
            # Convert index to binary representation of computational basis state
            binary = format(i, f'0{self.n_qubits}b')
            # Check the target qubit's value (reading right to left)
            if binary[-(qubit+1)] == '0':
                mask_0[i] = 1
            else:
                mask_1[i] = 1
        
        # Apply rotation based on axis
        if axis == 'X':
            # X rotation: |0⟩ → cos(θ/2)|0⟩ + i·sin(θ/2)|1⟩, |1⟩ → i·sin(θ/2)|0⟩ + cos(θ/2)|1⟩
            new_state = np.zeros_like(state, dtype=complex)
            for i in range(len(state)):
                binary = format(i, f'0{self.n_qubits}b')
                bit_list = list(binary)
                # Flip the target qubit to calculate the coupled index
                bit_list[-(qubit+1)] = '1' if bit_list[-(qubit+1)] == '0' else '0'
                flipped_binary = ''.join(bit_list)
                flipped_idx = int(flipped_binary, 2)
                
                if binary[-(qubit+1)] == '0':
                    # |0⟩ component
                    new_state[i] += np.real(rotation) * state[i]
                    new_state[flipped_idx] += 1j * np.imag(rotation) * state[i]
                else:
                    # |1⟩ component
                    new_state[flipped_idx] += 1j * np.imag(rotation) * state[i]
                    new_state[i] += np.real(rotation) * state[i]
            
            state = new_state
            
        elif axis == 'Y':
            # Y rotation: similar to X but with different phases
            new_state = np.zeros_like(state, dtype=complex)
            for i in range(len(state)):
                binary = format(i, f'0{self.n_qubits}b')
                bit_list = list(binary)
                # Flip the target qubit to calculate the coupled index
                bit_list[-(qubit+1)] = '1' if bit_list[-(qubit+1)] == '0' else '0'
                flipped_binary = ''.join(bit_list)
                flipped_idx = int(flipped_binary, 2)
                
                if binary[-(qubit+1)] == '0':
                    # |0⟩ component
                    new_state[i] += np.real(rotation) * state[i]
                    new_state[flipped_idx] += -np.imag(rotation) * state[i]
                else:
                    # |1⟩ component
                    new_state[flipped_idx] += np.imag(rotation) * state[i]
                    new_state[i] += np.real(rotation) * state[i]
            
            state = new_state
            
        elif axis == 'Z':
            # Z rotation: |0⟩ → e^(-iθ/2)|0⟩, |1⟩ → e^(iθ/2)|1⟩
            # Simply apply phase shifts based on qubit value
            phase_0 = np.exp(-1j * np.angle(rotation) / 2)
            phase_1 = np.exp(1j * np.angle(rotation) / 2)
            
            state = state * (mask_0 * phase_0 + mask_1 * phase_1)
        
        return state
    
    def _apply_entanglement(self, state: np.ndarray, layer_idx: int) -> np.ndarray:
        """
        Apply entanglement operations between qubits.
        
        Args:
            state: Current quantum state
            layer_idx: Index of the current circuit layer
            
        Returns:
            Updated quantum state
        """
        # Get entanglement parameters for this layer
        entanglement = self.entanglement_weights[layer_idx]
        
        # Apply entanglement operations between pairs of qubits
        for control in range(self.n_qubits):
            for target in range(self.n_qubits):
                if control != target:
                    # Apply a controlled operation based on the entanglement parameter
                    # This is a simplified version of a controlled-U gate
                    
                    # Get entanglement parameter
                    param = entanglement[control, target]
                    strength = np.abs(param)
                    
                    if strength > 0.01:  # Apply only if parameter is significant
                        # Create a controlled-phase operation with strength based on parameter
                        if self.use_complex:
                            phase = np.exp(1j * np.angle(param))
                        else:
                            phase = np.exp(1j * param)
                        
                        # Apply the controlled operation
                        state = self._apply_controlled_operation(state, control, target, phase, strength)
        
        return state
    
    def _apply_controlled_operation(self, 
                                   state: np.ndarray, 
                                   control: int, 
                                   target: int, 
                                   phase: complex,
                                   strength: float) -> np.ndarray:
        """
        Apply a controlled operation between qubits.
        
        Args:
            state: Current quantum state
            control: Control qubit
            target: Target qubit
            phase: Phase parameter
            strength: Strength of the operation
            
        Returns:
            Updated quantum state
        """
        # For each basis state in the superposition
        new_state = state.copy()
        
        for i in range(len(state)):
            # Convert index to binary representation of computational basis state
            binary = format(i, f'0{self.n_qubits}b')
            
            # Apply operation only if control qubit is 1
            if binary[-(control+1)] == '1':
                # Apply phase to the target qubit based on strength
                if binary[-(target+1)] == '1':
                    # Apply phase with strength as probability
                    if np.random.random() < strength:
                        new_state[i] *= phase
        
        return new_state
    
    def _embed_input(self, x: np.ndarray) -> np.ndarray:
        """
        Embed classical input into quantum state.
        
        Args:
            x: Input data (batch_size, input_dim)
            
        Returns:
            Quantum state representation (batch_size, 2^n_qubits)
        """
        batch_size = x.shape[0]
        
        # Initialize quantum states (|0⟩^⊗n)
        states = np.zeros((batch_size, 2**self.n_qubits), dtype=complex)
        states[:, 0] = 1.0  # Set to |0⟩^⊗n
        
        # Apply input embedding
        for b in range(batch_size):
            # Transform input using embedding weights
            embedded = x[b] @ self.input_weights  # (input_dim) @ (input_dim, n_qubits) -> (n_qubits)
            
            # Apply rotation to each qubit based on embedded values
            state = states[b]
            
            for q in range(self.n_qubits):
                # Apply X rotation based on input value
                val = embedded[q]
                
                if self.use_complex and np.iscomplexobj(val):
                    angle = np.abs(val)
                    phase = np.exp(1j * np.angle(val))
                else:
                    angle = val
                    phase = 1.0
                
                # Apply rotation
                x_rot = np.cos(angle/2) + 1j * np.sin(angle/2) * phase
                state = self._apply_single_qubit_rotation(state, q, x_rot, 'X')
            
            states[b] = state
        
        return states
    
    def _measure_output(self, states: np.ndarray) -> np.ndarray:
        """
        Extract classical output from quantum states.
        
        Args:
            states: Quantum states (batch_size, 2^n_qubits)
            
        Returns:
            Classical output (batch_size, output_dim)
        """
        batch_size = states.shape[0]
        outputs = np.zeros((batch_size, self.output_dim), dtype=complex if self.use_complex else float)
        
        for b in range(batch_size):
            state = states[b]
            
            # Compute expectation values for each qubit
            expectations = np.zeros(self.n_qubits, dtype=complex if self.use_complex else float)
            
            for q in range(self.n_qubits):
                # Compute expectation value of Z operator for this qubit
                # <Z> = Probability(|0⟩) - Probability(|1⟩)
                
                # Probability of measuring |0⟩ for this qubit
                prob_0 = 0.0
                # Probability of measuring |1⟩ for this qubit
                prob_1 = 0.0
                
                for i in range(len(state)):
                    # Get binary representation
                    binary = format(i, f'0{self.n_qubits}b')
                    prob = np.abs(state[i])**2
                    
                    # Check qubit value in this basis state
                    if binary[-(q+1)] == '0':
                        prob_0 += prob
                    else:
                        prob_1 += prob
                
                # Compute expectation value
                if self.use_complex:
                    # For complex values, include phase information
                    expectations[q] = (prob_0 - prob_1) * (np.mean([state[i] for i in range(len(state)) 
                                                                    if format(i, f'0{self.n_qubits}b')[-(q+1)] == '0']) 
                                                            / max(prob_0, 1e-10))
                else:
                    expectations[q] = prob_0 - prob_1
            
            # Transform qubit expectations to output using output weights
            outputs[b] = expectations @ self.output_weights
        
        return outputs
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        Forward pass through the variational quantum circuit.
        
        Args:
            x: Input data (batch_size, input_dim)
            
        Returns:
            Output data (batch_size, output_dim)
        """
        # Embed classical input into quantum states
        states = self._embed_input(x)
        
        # Apply variational quantum circuit layers
        for layer in range(self.circuit_depth):
            # Apply parameterized rotations
            states = np.array([self._apply_rotations(state, layer) for state in states])
            
            # Apply entanglement operations
            states = np.array([self._apply_entanglement(state, layer) for state in states])
        
        # Measure quantum states to get classical output
        outputs = self._measure_output(states)
        
        # Apply activation function if specified
        if self.activation_fn is not None:
            outputs = self.activation_fn(outputs)
        
        return outputs
    
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
        # This is a simplified backward pass using parameter shift rule
        # In a real quantum circuit, we would use more sophisticated methods
        
        # For simplicity, we'll use a numerical approximation for gradients
        # In a production system, analytical gradients would be preferred
        
        # Compute gradients for output weights (most straightforward)
        grad_output_weights = np.zeros_like(self.output_weights)
        
        # For each output dimension and qubit
        for o in range(self.output_dim):
            for q in range(self.n_qubits):
                # Small perturbation for numerical gradient
                epsilon = 0.01
                
                # Save original weight
                original = self.output_weights[q, o]
                
                # Perturb weight positively
                self.output_weights[q, o] = original + epsilon
                outputs_pos = self.forward(self._cached_input)
                
                # Perturb weight negatively
                self.output_weights[q, o] = original - epsilon
                outputs_neg = self.forward(self._cached_input)
                
                # Restore original weight
                self.output_weights[q, o] = original
                
                # Numerical gradient
                grad = np.sum((outputs_pos - outputs_neg) * grad_output) / (2 * epsilon)
                grad_output_weights[q, o] = grad
        
        # Update output weights
        self.output_weights -= learning_rate * grad_output_weights
        
        # For simplicity, we'll use a similar approach for all other weights
        # In a real implementation, we'd use more efficient methods
        
        # Input gradients for return
        grad_input = np.zeros((self._cached_input.shape[0], self.input_dim))
        
        # This is just a placeholder - a proper implementation would compute full gradients
        # return grad_input
        
        # For a minimal working example, we return a simple gradient estimate
        # Propagate gradients back through the circuit
        # This is an oversimplified approximation
        if self.use_complex:
            grad_input = np.real(grad_output @ self.output_weights.T @ self.input_weights.T)
        else:
            grad_input = grad_output @ self.output_weights.T @ self.input_weights.T
        
        return grad_input
    
    def get_config(self) -> Dict:
        """
        Get layer configuration.
        
        Returns:
            Layer configuration dictionary
        """
        config = super().get_config()
        config.update({
            'n_qubits': self.n_qubits,
            'circuit_depth': self.circuit_depth
        })
        return config 