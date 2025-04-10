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
Angle Encoder
============

Implements angle encoding for market data, mapping normalized
vectors into rotation angles in a quantum circuit.
"""

import numpy as np
import logging
from typing import Dict, List, Union, Any, Optional, Tuple

from .base_encoder import BaseQuantumEncoder

# Configure logging
logger = logging.getLogger("quantum-encoding")

class AngleEncoder(BaseQuantumEncoder):
    """
    Encodes data into rotation angles for quantum gates.
    Maps input features to angles that would be applied to quantum gates.
    """
    
    def __init__(self, n_qubits: int = 4, rotation_axis: str = "y", 
                repetitions: int = 1, name: str = "angle_encoder"):
        """
        Initialize the angle encoder.
        
        Args:
            n_qubits: Number of qubits to use for encoding
            rotation_axis: Rotation axis (x, y, z, or all)
            repetitions: Number of repetition layers
            name: Name identifier for the encoder
        """
        super().__init__(n_qubits=n_qubits, name=name)
        
        # Validate rotation axis
        valid_axes = ['x', 'y', 'z', 'all']
        if rotation_axis not in valid_axes:
            logger.warning(f"{self.log_prefix} - Invalid rotation axis '{rotation_axis}', using 'y'")
            rotation_axis = 'y'
        
        self.rotation_axis = rotation_axis
        self.repetitions = max(1, repetitions)  # Ensure at least 1 repetition
        
        # Calculate feature capacity based on number of qubits and repetitions
        if rotation_axis == 'all':
            self.feature_capacity = 3 * n_qubits * repetitions
        else:
            self.feature_capacity = n_qubits * repetitions
            
        logger.info(f"{self.log_prefix} - Angle encoder initialized with {rotation_axis} rotation(s), "
                   f"{repetitions} repetition(s), feature capacity: {self.feature_capacity}")
    
    def encode(self, data: np.ndarray) -> np.ndarray:
        """
        Encode classical data into rotation angles.
        
        Args:
            data: Input data to encode (vector or matrix)
            
        Returns:
            Rotation angles for quantum gates
        """
        # Validate and normalize input data
        data = self._validate_input(data)
        normalized_data = self._normalize_data(data)
        
        # Handle different input shapes
        original_shape = normalized_data.shape
        
        # If input is a matrix, we encode each row separately and stack
        if len(original_shape) > 1 and original_shape[0] > 1:
            encoded_data = np.array([self._encode_vector(row) for row in normalized_data])
            logger.info(f"{self.log_prefix} - Encoded matrix of shape {original_shape} to {encoded_data.shape}")
            return encoded_data
        
        # Otherwise encode as a single vector
        encoded_vector = self._encode_vector(normalized_data.flatten())
        logger.info(f"{self.log_prefix} - Encoded vector of length {len(normalized_data.flatten())} "
                   f"to angles array of shape {encoded_vector.shape}")
        return encoded_vector
    
    def _encode_vector(self, vector: np.ndarray) -> np.ndarray:
        """
        Encode a single vector into rotation angles.
        
        Args:
            vector: Input vector to encode
            
        Returns:
            Rotation angles for quantum gates
        """
        # Ensure vector is normalized to [0,1] range
        if np.min(vector) < 0 or np.max(vector) > 1:
            vector = (vector - np.min(vector)) / (np.max(vector) - np.min(vector) or 1)
        
        # Scale to [0, 2π] range for angles
        scaled_vector = vector * 2 * np.pi
        
        # Store original vector length for potential decoding
        self.encoding_params['original_length'] = len(vector)
        
        # If vector is too long, truncate to match feature capacity
        if len(scaled_vector) > self.feature_capacity:
            logger.warning(f"{self.log_prefix} - Input dimension {len(scaled_vector)} exceeds feature capacity "
                          f"{self.feature_capacity}, truncating")
            return scaled_vector[:self.feature_capacity]
            
        # If vector is too short, pad with zeros
        if len(scaled_vector) < self.feature_capacity:
            padding = np.zeros(self.feature_capacity - len(scaled_vector))
            return np.concatenate([scaled_vector, padding])
            
        return scaled_vector
    
    def _structure_angles(self, angles: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Structure angles by rotation axis and qubit index.
        
        Args:
            angles: Flat array of rotation angles
            
        Returns:
            Dictionary with structured angles by axis and qubit
        """
        structured_angles = {}
        
        if self.rotation_axis == 'all':
            # Split angles into x, y, z rotations
            features_per_rep = 3 * self.n_qubits
            
            # For each repetition
            for rep in range(self.repetitions):
                start_idx = rep * features_per_rep
                
                # Extract angles for each axis
                x_angles = angles[start_idx:start_idx + self.n_qubits]
                y_angles = angles[start_idx + self.n_qubits:start_idx + 2*self.n_qubits]
                z_angles = angles[start_idx + 2*self.n_qubits:start_idx + 3*self.n_qubits]
                
                structured_angles[f'rep{rep}_x'] = x_angles
                structured_angles[f'rep{rep}_y'] = y_angles
                structured_angles[f'rep{rep}_z'] = z_angles
        else:
            # Single axis rotation
            features_per_rep = self.n_qubits
            
            # For each repetition
            for rep in range(self.repetitions):
                start_idx = rep * features_per_rep
                axis_angles = angles[start_idx:start_idx + self.n_qubits]
                structured_angles[f'rep{rep}_{self.rotation_axis}'] = axis_angles
        
        return structured_angles
    
    def decode(self, quantum_data: np.ndarray) -> np.ndarray:
        """
        Decode rotation angles back to classical data.
        
        Args:
            quantum_data: Rotation angles
            
        Returns:
            Decoded classical data
        """
        # Handle different input shapes
        if len(quantum_data.shape) > 1 and quantum_data.shape[0] > 1:
            # If we have multiple angle sets, decode each separately
            decoded_data = np.array([self._decode_angles(angles) for angles in quantum_data])
            return decoded_data
        
        # Otherwise decode single set of angles
        return self._decode_angles(quantum_data)
    
    def _decode_angles(self, angles: np.ndarray) -> np.ndarray:
        """
        Decode a single set of angles back to classical data.
        
        Args:
            angles: Rotation angles to decode
            
        Returns:
            Decoded classical vector
        """
        # Extract original length if available, otherwise use all angles
        original_length = self.encoding_params.get('original_length', len(angles))
        
        # Normalize from [0, 2π] back to [0,1]
        normalized = angles / (2 * np.pi)
        
        # Truncate to original length
        classical_vector = normalized[:original_length]
        
        # If we stored normalization parameters, denormalize
        if 'data_min' in self.encoding_params and 'data_max' in self.encoding_params:
            # Extract relevant normalization parameters
            data_min = self.encoding_params['data_min']
            data_max = self.encoding_params['data_max']
            
            # Ensure correct shape for normalization parameters
            if isinstance(data_min, np.ndarray) and len(data_min) > original_length:
                data_min = data_min[:original_length]
                data_max = data_max[:original_length] if len(data_max) > original_length else data_max
            
            # Denormalize
            range_values = data_max - data_min
            denormalized = (classical_vector * range_values) + data_min
            return denormalized
        
        return classical_vector
    
    def get_circuit_representation(self, angles: np.ndarray) -> str:
        """
        Generate a text representation of the quantum circuit.
        
        Args:
            angles: Rotation angles
            
        Returns:
            Text representation of quantum circuit
        """
        structured = self._structure_angles(angles)
        
        circuit_str = [f"Quantum Circuit - {self.n_qubits} qubits:"]
        circuit_str.append("-" * 50)
        
        for i in range(self.n_qubits):
            qubit_line = [f"q{i}: |0⟩"]
            
            for rep in range(self.repetitions):
                if self.rotation_axis == 'all':
                    x_angle = structured.get(f'rep{rep}_x', [0] * self.n_qubits)[i]
                    y_angle = structured.get(f'rep{rep}_y', [0] * self.n_qubits)[i]
                    z_angle = structured.get(f'rep{rep}_z', [0] * self.n_qubits)[i]
                    
                    qubit_line.append(f"─Rx({x_angle:.2f})─Ry({y_angle:.2f})─Rz({z_angle:.2f})─")
                else:
                    angle = structured.get(f'rep{rep}_{self.rotation_axis}', [0] * self.n_qubits)[i]
                    qubit_line.append(f"─R{self.rotation_axis}({angle:.2f})─")
            
            circuit_str.append("".join(qubit_line))
        
        return "\n".join(circuit_str) 