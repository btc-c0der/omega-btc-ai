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
Amplitude Encoder
===============

Implements amplitude encoding for market data, mapping normalized
vectors directly into quantum amplitudes (statevector).
"""

import numpy as np
import logging
from typing import Dict, List, Union, Any, Optional, Tuple

from .base_encoder import BaseQuantumEncoder

# Configure logging
logger = logging.getLogger("quantum-encoding")

class AmplitudeEncoder(BaseQuantumEncoder):
    """
    Encodes data into amplitude encoding (statevector representation).
    Maps input vectors directly to quantum amplitudes of a statevector.
    """
    
    def __init__(self, n_qubits: int = 4, padding_value: float = 0.0, 
                name: str = "amplitude_encoder"):
        """
        Initialize the amplitude encoder.
        
        Args:
            n_qubits: Number of qubits to use for encoding
            padding_value: Value to use for padding if input dimension < 2^n_qubits
            name: Name identifier for the encoder
        """
        super().__init__(n_qubits=n_qubits, name=name)
        self.padding_value = padding_value
        logger.info(f"{self.log_prefix} - Amplitude encoder initialized")
    
    def encode(self, data: np.ndarray) -> np.ndarray:
        """
        Encode classical data into quantum amplitudes.
        
        Args:
            data: Input data to encode (vector or matrix)
            
        Returns:
            Quantum amplitude representation (statevector)
        """
        # Validate and normalize input data
        data = self._validate_input(data)
        
        # Handle different input shapes
        original_shape = data.shape
        
        # If input is a matrix, we encode each row separately and stack
        if len(original_shape) > 1 and original_shape[0] > 1:
            encoded_data = np.array([self._encode_vector(row) for row in data])
            logger.info(f"{self.log_prefix} - Encoded matrix of shape {original_shape} to {encoded_data.shape}")
            return encoded_data
        
        # Otherwise encode as a single vector
        encoded_vector = self._encode_vector(data.flatten())
        logger.info(f"{self.log_prefix} - Encoded vector of length {len(data.flatten())} to statevector of size {len(encoded_vector)}")
        return encoded_vector
    
    def _encode_vector(self, vector: np.ndarray) -> np.ndarray:
        """
        Encode a single vector into quantum amplitudes.
        
        Args:
            vector: Input vector to encode
            
        Returns:
            Quantum amplitude representation (statevector)
        """
        # Normalize input to a valid quantum state (unit vector)
        normalized = self._normalize_to_unit(vector)
        
        # Pad or truncate to match quantum state dimension
        quantum_state = self._pad_to_dimension(normalized, self.dimension)
        
        # Store original vector length for potential decoding
        self.encoding_params['original_length'] = len(vector)
        
        return quantum_state
    
    def _normalize_to_unit(self, vector: np.ndarray) -> np.ndarray:
        """
        Normalize a vector to unit length (L2 norm = 1).
        
        Args:
            vector: Vector to normalize
            
        Returns:
            Unit vector
        """
        norm = np.linalg.norm(vector)
        
        # Handle zero-norm case
        if norm < 1e-10:
            logger.warning(f"{self.log_prefix} - Input vector has near-zero norm, using uniform state")
            unit_vector = np.ones(len(vector)) / np.sqrt(len(vector))
            return unit_vector
        
        return vector / norm
    
    def _pad_to_dimension(self, vector: np.ndarray, target_dim: int) -> np.ndarray:
        """
        Pad or truncate vector to match target dimension.
        
        Args:
            vector: Vector to pad/truncate
            target_dim: Target dimension (2^n_qubits)
            
        Returns:
            Padded/truncated vector
        """
        current_dim = len(vector)
        
        # If dimensions match, return as is
        if current_dim == target_dim:
            return vector
        
        # If input is too large, truncate and renormalize
        if current_dim > target_dim:
            logger.warning(f"{self.log_prefix} - Input dimension {current_dim} exceeds quantum state dimension {target_dim}, truncating")
            truncated = vector[:target_dim]
            return self._normalize_to_unit(truncated)
        
        # If input is too small, pad with zeros (or specified value)
        padding = np.full(target_dim - current_dim, self.padding_value)
        padded = np.concatenate([vector, padding])
        
        # Renormalize after padding
        return self._normalize_to_unit(padded)
    
    def decode(self, quantum_data: np.ndarray) -> np.ndarray:
        """
        Decode quantum amplitudes back to classical data.
        
        Args:
            quantum_data: Quantum amplitude representation (statevector)
            
        Returns:
            Decoded classical data
        """
        # Handle different input shapes
        if len(quantum_data.shape) > 1 and quantum_data.shape[0] > 1:
            # If we have multiple statevectors, decode each separately
            decoded_data = np.array([self._decode_statevector(qstate) for qstate in quantum_data])
            return decoded_data
        
        # Otherwise decode single statevector
        return self._decode_statevector(quantum_data)
    
    def _decode_statevector(self, statevector: np.ndarray) -> np.ndarray:
        """
        Decode a single statevector back to classical data.
        
        Args:
            statevector: Quantum state to decode
            
        Returns:
            Decoded classical vector
        """
        # Extract original length if available, otherwise use full vector
        original_length = self.encoding_params.get('original_length', len(statevector))
        
        # Truncate to original length
        classical_vector = statevector[:original_length].real
        
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
    
    def get_quantum_probabilities(self, statevector: np.ndarray) -> np.ndarray:
        """
        Calculate measurement probabilities from statevector.
        
        Args:
            statevector: Quantum state vector
            
        Returns:
            Probability distribution
        """
        return np.abs(statevector) ** 2 