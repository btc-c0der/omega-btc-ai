#!/usr/bin/env python3
"""
Base Quantum Encoder
===================

Abstract base class for all quantum encoding strategies.
Defines the interface and common functionality for encoding market data.
"""

import numpy as np
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Union, Any, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("quantum-encoding")

class BaseQuantumEncoder(ABC):
    """Abstract base class for quantum data encoders."""
    
    def __init__(self, n_qubits: int = 4, name: str = "base_encoder"):
        """
        Initialize the quantum encoder.
        
        Args:
            n_qubits: Number of qubits to use for encoding
            name: Name identifier for the encoder
        """
        self.n_qubits = n_qubits
        self.name = name
        self.dimension = 2 ** n_qubits
        self.is_trained = False
        self.encoding_params = {}
        self.log_prefix = f"🔮 QUANTUM ENCODING [{self.name}]"
        
        logger.info(f"{self.log_prefix} - Initialized with {n_qubits} qubits (dimension: {self.dimension})")
    
    @abstractmethod
    def encode(self, data: np.ndarray) -> np.ndarray:
        """
        Encode classical data into quantum-inspired representation.
        
        Args:
            data: Input data to encode (array or matrix)
            
        Returns:
            Quantum-encoded representation of data
        """
        pass
    
    @abstractmethod
    def decode(self, quantum_data: np.ndarray) -> np.ndarray:
        """
        Decode quantum-inspired representation back to classical data.
        
        Args:
            quantum_data: Quantum-encoded data
            
        Returns:
            Classical representation of data
        """
        pass
    
    def fit(self, training_data: np.ndarray) -> None:
        """
        Optimize encoding parameters based on training data.
        
        Args:
            training_data: Data to use for optimizing encoding parameters
        """
        # Default implementation does nothing
        # Subclasses can override to implement parameter optimization
        self.is_trained = True
        logger.info(f"{self.log_prefix} - Fitted encoder to data of shape {training_data.shape}")
    
    def transform(self, data: np.ndarray) -> np.ndarray:
        """
        Transform data using the encoder (alias for encode).
        
        Args:
            data: Input data to encode
            
        Returns:
            Encoded data
        """
        return self.encode(data)
    
    def fit_transform(self, data: np.ndarray) -> np.ndarray:
        """
        Fit encoder to data and then transform it.
        
        Args:
            data: Input data to fit and encode
            
        Returns:
            Encoded data
        """
        self.fit(data)
        return self.transform(data)
    
    def _validate_input(self, data: np.ndarray) -> np.ndarray:
        """
        Validate and preprocess input data.
        
        Args:
            data: Input data to validate
            
        Returns:
            Validated and preprocessed data
        
        Raises:
            ValueError: If data is not valid for encoding
        """
        # Check if data is a numpy array
        if not isinstance(data, np.ndarray):
            try:
                data = np.array(data, dtype=np.float32)
            except:
                raise ValueError(f"Input data must be convertible to numpy array, got {type(data)}")
        
        # Check for NaN or inf values
        if np.isnan(data).any() or np.isinf(data).any():
            raise ValueError("Input data contains NaN or infinite values")
        
        return data
    
    def _normalize_data(self, data: np.ndarray) -> np.ndarray:
        """
        Normalize data to prepare for quantum encoding.
        
        Args:
            data: Input data to normalize
            
        Returns:
            Normalized data
        """
        # Apply min-max normalization to [0,1] range
        data_min = np.min(data, axis=0)
        data_max = np.max(data, axis=0)
        
        # Handle constant features (where min == max)
        range_values = data_max - data_min
        range_values = np.where(range_values == 0, 1.0, range_values)
        
        normalized_data = (data - data_min) / range_values
        
        # Store normalization parameters for potential decoding
        self.encoding_params['data_min'] = data_min
        self.encoding_params['data_max'] = data_max
        
        return normalized_data
    
    def get_encoding_info(self) -> Dict[str, Any]:
        """
        Get information about the encoder.
        
        Returns:
            Dictionary with encoder information
        """
        return {
            'name': self.name,
            'n_qubits': self.n_qubits,
            'dimension': self.dimension,
            'is_trained': self.is_trained,
            'encoding_params': self.encoding_params
        }
    
    def compute_state_fidelity(self, original_data: np.ndarray, 
                              reconstructed_data: np.ndarray) -> float:
        """
        Compute fidelity between original and reconstructed data.
        
        Args:
            original_data: Original input data
            reconstructed_data: Data after encode-decode cycle
            
        Returns:
            Fidelity score (0-1)
        """
        # Ensure data is properly shaped and normalized
        original = self._validate_input(original_data)
        reconstructed = self._validate_input(reconstructed_data)
        
        # Reshape if needed to compute fidelity
        original = original.flatten()
        reconstructed = reconstructed.flatten()
        
        # Normalize to unit vectors
        norm_orig = np.linalg.norm(original)
        norm_recon = np.linalg.norm(reconstructed)
        
        if norm_orig == 0 or norm_recon == 0:
            return 0.0
        
        orig_unit = original / norm_orig
        recon_unit = reconstructed / norm_recon
        
        # Compute fidelity as squared inner product
        fidelity = np.abs(np.dot(orig_unit, recon_unit.conj())) ** 2
        
        return float(fidelity) 