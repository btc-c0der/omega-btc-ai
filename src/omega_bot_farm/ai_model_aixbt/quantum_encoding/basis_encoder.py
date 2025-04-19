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
Basis Encoder
===========

Implements basis encoding for market data, mapping categorical
or discretized values to quantum basis states.
"""

import numpy as np
import logging
from typing import Dict, List, Union, Any, Optional, Tuple

from .base_encoder import BaseQuantumEncoder

# Configure logging
logger = logging.getLogger("quantum-encoding")

class BasisEncoder(BaseQuantumEncoder):
    """
    Encodes data into computational basis states.
    Maps discrete values to distinct basis states.
    """
    
    def __init__(self, n_qubits: int = 4, mapping: Optional[Dict[Any, int]] = None, 
                name: str = "basis_encoder"):
        """
        Initialize the basis encoder.
        
        Args:
            n_qubits: Number of qubits to use for encoding
            mapping: Optional dictionary mapping values to basis states
            name: Name identifier for the encoder
        """
        super().__init__(n_qubits=n_qubits, name=name)
        self.mapping = mapping or {}
        logger.info(f"{self.log_prefix} - Basis encoder initialized")
    
    def encode(self, data: Union[Any, List[Any], np.ndarray]) -> np.ndarray:
        """
        Encode classical data into basis states.
        
        Args:
            data: Input data to encode (categorical value or array)
            
        Returns:
            One-hot encoded representation (basis states)
        """
        # Handle different input types
        if isinstance(data, (list, np.ndarray)) and len(data) > 1:
            # Handle list or array of values
            return np.array([self._encode_value(val) for val in data])
        else:
            # Handle single value
            return self._encode_value(data)
    
    def _encode_value(self, value: Any) -> np.ndarray:
        """
        Encode a single value to a basis state.
        
        Args:
            value: Input value to encode
            
        Returns:
            One-hot encoded vector
        """
        # Get the index for this value
        if value in self.mapping:
            index = self.mapping[value]
        else:
            # Auto-assign a new index
            if len(self.mapping) < self.dimension:
                index = len(self.mapping)
                self.mapping[value] = index
                logger.info(f"{self.log_prefix} - Assigned basis state {index} to value '{value}'")
            else:
                # If we've exceeded capacity, use modulo
                index = hash(value) % self.dimension
                logger.warning(f"{self.log_prefix} - Encoder capacity exceeded, using hash-based mapping for '{value}'")
        
        # Create one-hot encoding
        encoding = np.zeros(self.dimension)
        encoding[index] = 1.0
        
        return encoding
    
    def decode(self, quantum_data: np.ndarray) -> Union[Any, List[Any]]:
        """
        Decode from basis encoding back to classical values.
        
        Args:
            quantum_data: Basis state encoding(s)
            
        Returns:
            Original categorical value(s)
        """
        # Handle different input shapes
        if len(quantum_data.shape) > 1 and quantum_data.shape[0] > 1:
            # If we have multiple encodings, decode each separately
            return [self._decode_basis_state(state) for state in quantum_data]
        
        # Otherwise decode single encoding
        return self._decode_basis_state(quantum_data)
    
    def _decode_basis_state(self, state: np.ndarray) -> Any:
        """
        Decode a single basis state back to its categorical value.
        
        Args:
            state: Basis state encoding
            
        Returns:
            Original categorical value
        """
        # Find index of the basis state (maximum value)
        if np.max(state) < 0.5:
            logger.warning(f"{self.log_prefix} - No clear basis state found, using argmax")
        
        index = np.argmax(state)
        
        # Look up the original value in the mapping
        reverse_mapping = {idx: val for val, idx in self.mapping.items()}
        
        if index in reverse_mapping:
            return reverse_mapping[index]
        else:
            # If index not found in mapping, return the index itself
            logger.warning(f"{self.log_prefix} - No value found for basis state {index}, returning index")
            return index
    
    def encode_multiple_features(self, data_dict: Dict[str, Any]) -> np.ndarray:
        """
        Encode multiple categorical features into separate qubit subspaces.
        
        Args:
            data_dict: Dictionary mapping feature names to values
            
        Returns:
            Encoded representation with one qubit per feature
        """
        if len(data_dict) > self.n_qubits:
            raise ValueError(f"Too many features ({len(data_dict)}) for available qubits ({self.n_qubits})")
        
        # Initialize state to |0...0⟩
        state = np.zeros(self.dimension)
        state[0] = 1.0
        
        # Assign features to individual qubits
        for i, (feature_name, value) in enumerate(data_dict.items()):
            if i >= self.n_qubits:
                break
                
            # Map value to 0 or 1
            if isinstance(value, bool):
                bit_value = 1 if value else 0
            elif isinstance(value, (int, float)):
                bit_value = 1 if value > 0 else 0
            elif isinstance(value, str):
                # Map string values like "high"/"low", "up"/"down", etc.
                positive_values = ["high", "up", "true", "on", "yes", "bullish", "increasing"]
                negative_values = ["low", "down", "false", "off", "no", "bearish", "decreasing"]
                
                if value.lower() in positive_values:
                    bit_value = 1
                elif value.lower() in negative_values:
                    bit_value = 0
                else:
                    # Hash other string values
                    bit_value = hash(value) % 2
            else:
                # Hash other types
                bit_value = hash(value) % 2
            
            # If bit should be 1, flip the corresponding qubit
            if bit_value == 1:
                # Create X gate for the specific qubit
                mask = 1 << i
                for j in range(self.dimension):
                    if (j & mask) != (j ^ mask) & mask:  # Check if ith bit differs
                        # Swap amplitudes for states that differ only in the ith bit
                        j2 = j ^ mask  # Flip the ith bit
                        state[j], state[j2] = state[j2], state[j]
        
        return state
    
    def get_basis_mapping(self) -> Dict[Any, int]:
        """
        Get the current mapping of values to basis states.
        
        Returns:
            Dictionary mapping values to basis state indices
        """
        return self.mapping.copy() 