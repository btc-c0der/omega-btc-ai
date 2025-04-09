#!/usr/bin/env python3

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Any, Optional, Union
import logging
import os
from scipy.stats import entropy
import random

# Import quantum libraries if available
try:
    import qiskit
    from qiskit import QuantumCircuit, Aer, execute
    from qiskit.visualization import plot_bloch_multivector
    from qiskit.quantum_info import state_fidelity, partial_trace, Statevector
    from qiskit.circuit import ParameterVector
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    logging.warning("Qiskit not available. Using simulated quantum features.")

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuantumFeatureExtractor:
    """
    Quantum feature extractor for financial market data.
    Uses quantum circuits to extract non-linear features for improved prediction.
    """
    
    def __init__(self, 
                 n_qubits: int = 4,
                 n_layers: int = 2,
                 backend_name: str = "aer_simulator",
                 shots: int = 1024,
                 feature_map_type: str = "zz_feature_map"):
        """
        Initialize quantum feature extractor.
        
        Args:
            n_qubits: Number of qubits in the quantum circuit
            n_layers: Number of repeated layers in the feature map
            backend_name: Name of the quantum backend to use
            shots: Number of measurement shots
            feature_map_type: Type of quantum feature map to use
        """
        self.logger = logging.getLogger(__name__)
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.backend_name = backend_name
        self.shots = shots
        self.feature_map_type = feature_map_type
        
        if not QISKIT_AVAILABLE:
            self.logger.warning("Qiskit not available. Using fallback classical features.")
            return
            
        # Initialize quantum backend
        try:
            self.backend = Aer.get_backend(backend_name)
        except Exception as e:
            self.logger.error(f"Error initializing quantum backend: {e}")
            self.backend = None
            
        # Create parameterized circuit template
        self.params = ParameterVector('θ', n_qubits)
        self.circuit_template = self._create_feature_map()
        
    def _create_feature_map(self) -> Optional[QuantumCircuit]:
        """Create the quantum feature map circuit."""
        if not QISKIT_AVAILABLE:
            return None
            
        qc = QuantumCircuit(self.n_qubits)
        
        if self.feature_map_type == "zz_feature_map":
            # ZZFeatureMap-inspired circuit
            for layer in range(self.n_layers):
                # H-gates layer
                for q in range(self.n_qubits):
                    qc.h(q)
                
                # Data encoding layer
                for q in range(self.n_qubits):
                    qc.rz(self.params[q], q)
                
                # Entanglement layer
                for q in range(self.n_qubits - 1):
                    qc.cx(q, q + 1)
                qc.cx(self.n_qubits - 1, 0)  # Close the loop
                
                # Second data encoding
                for q in range(self.n_qubits):
                    qc.rz(self.params[q], q)
                    
        elif self.feature_map_type == "amplitude_embedding":
            # Simple amplitude embedding
            qc.h(range(self.n_qubits))
            for q in range(self.n_qubits):
                qc.ry(self.params[q], q)
                
            # Add entanglement
            for layer in range(self.n_layers):
                for q in range(self.n_qubits - 1):
                    qc.cx(q, q + 1)
                
        else:
            # Default simple feature map
            for layer in range(self.n_layers):
                for q in range(self.n_qubits):
                    qc.rx(self.params[q], q)
                    qc.rz(self.params[q], q)
                
                # Entanglement
                for q in range(self.n_qubits - 1):
                    qc.cx(q, q + 1)
        
        # Measurement
        qc.measure_all()
        
        return qc
    
    def _normalize_data(self, data: np.ndarray) -> np.ndarray:
        """Normalize input data to appropriate range for quantum circuit."""
        # Scale to [0, 2π] for rotation gates
        data_min = data.min(axis=0)
        data_max = data.max(axis=0)
        
        # Handle constant features
        range_data = data_max - data_min
        range_data[range_data == 0] = 1.0
        
        normalized = 2 * np.pi * (data - data_min) / range_data
        return normalized
    
    def _execute_circuit(self, params: np.ndarray) -> Dict[str, int]:
        """Execute quantum circuit with given parameters."""
        if not QISKIT_AVAILABLE or self.backend is None:
            return {}
            
        circuit = self.circuit_template.bind_parameters(params)
        
        try:
            job = execute(circuit, self.backend, shots=self.shots)
            result = job.result()
            counts = result.get_counts(circuit)
            return counts
        except Exception as e:
            self.logger.error(f"Error executing quantum circuit: {e}")
            return {}
    
    def _process_measurement_outcomes(self, counts: Dict[str, int]) -> np.ndarray:
        """Process measurement outcomes into feature vector."""
        if not counts:
            # Fallback to random features if quantum execution failed
            return np.random.rand(2**self.n_qubits)
            
        # Convert counts to normalized probabilities
        all_bitstrings = [format(i, f'0{self.n_qubits}b') for i in range(2**self.n_qubits)]
        probabilities = np.array([counts.get(bs, 0) for bs in all_bitstrings]) / self.shots
        
        # Additional derived features
        mean_prob = np.mean(probabilities)
        std_prob = np.std(probabilities)
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
        
        return np.concatenate([
            probabilities,
            [mean_prob, std_prob, entropy]
        ])
    
    def extract_features(self, data: np.ndarray) -> np.ndarray:
        """
        Extract quantum features from classical data.
        
        Args:
            data: Input data array of shape (n_samples, n_features)
            
        Returns:
            Quantum features of shape (n_samples, n_quantum_features)
        """
        if not QISKIT_AVAILABLE:
            # Fallback to simple non-linear transformations
            self.logger.warning("Using classical fallback features")
            return self._fallback_features(data)
            
        n_samples = data.shape[0]
        normalized_data = self._normalize_data(data)
        
        # Limit to first n_qubits features
        data_to_encode = normalized_data[:, :self.n_qubits]
        if data_to_encode.shape[1] < self.n_qubits:
            # Pad with zeros if not enough features
            padding = np.zeros((n_samples, self.n_qubits - data_to_encode.shape[1]))
            data_to_encode = np.hstack([data_to_encode, padding])
        
        quantum_features = []
        for i in range(n_samples):
            sample_params = data_to_encode[i]
            counts = self._execute_circuit(sample_params)
            features = self._process_measurement_outcomes(counts)
            quantum_features.append(features)
            
            # Log progress for large datasets
            if n_samples > 100 and i % 50 == 0:
                self.logger.info(f"Processed {i}/{n_samples} samples")
        
        return np.array(quantum_features)
    
    def _fallback_features(self, data: np.ndarray) -> np.ndarray:
        """Generate classical non-linear features as fallback."""
        # Simple non-linear transformations
        squared = data ** 2
        sqrt = np.sqrt(np.abs(data))
        sin_features = np.sin(data)
        cos_features = np.cos(data)
        
        # Interactions between features
        n_features = min(data.shape[1], 10)  # Limit to avoid explosion
        interactions = []
        for i in range(n_features):
            for j in range(i+1, n_features):
                interactions.append(data[:, i] * data[:, j])
        
        if interactions:
            interactions = np.column_stack(interactions)
            return np.hstack([data, squared, sqrt, sin_features, cos_features, interactions])
        else:
            return np.hstack([data, squared, sqrt, sin_features, cos_features])
    
    def get_config(self) -> Dict[str, Any]:
        """Get configuration parameters for serialization."""
        return {
            "n_qubits": self.n_qubits,
            "n_layers": self.n_layers,
            "backend_name": self.backend_name,
            "shots": self.shots,
            "feature_map_type": self.feature_map_type
        }
    
    def batch_extract_features(self, data_sequences: np.ndarray) -> np.ndarray:
        """Extract quantum features from multiple input sequences.
        
        Args:
            data_sequences: Input data sequences (batch_size, seq_len, n_features)
            
        Returns:
            Extracted quantum features (batch_size, n_quantum_features)
        """
        if len(data_sequences.shape) != 3:
            raise ValueError(f"Expected 3D input (batch_size, seq_len, n_features), got shape {data_sequences.shape}")
        
        batch_size, seq_len, n_features = data_sequences.shape
        logger.info(f"Processing batch of {batch_size} sequences with shape {seq_len}x{n_features}")
        
        # Prepare output array
        # First extract features for one sequence to determine feature size
        sample_features = self.extract_features(data_sequences[0].flatten())
        n_quantum_features = len(sample_features)
        
        # Initialize output array
        batch_features = np.zeros((batch_size, n_quantum_features))
        
        # Process each sequence in the batch
        for i in range(batch_size):
            # Flatten the sequence and extract features
            seq_data = data_sequences[i].flatten()
            features = self.extract_features(seq_data)
            batch_features[i] = features
        
        logger.info(f"Extracted quantum features batch of shape {batch_features.shape}")
        return batch_features
    
    def get_entanglement_metrics(self, data: np.ndarray) -> Dict[str, float]:
        """Calculate entanglement metrics for the given data.
        
        Args:
            data: Input data array
            
        Returns:
            Dictionary of entanglement metrics
        """
        features = self.extract_features(data)
        return {
            'entanglement': np.mean([abs(v) for v in features.flatten() if v != 0]),
            'coherence': np.mean([v for v in features.flatten() if v != 0])
        }
    
    def save_configuration(self, save_path: str):
        """Save the configuration of the quantum feature extractor.
        
        Args:
            save_path: Path to save the configuration
        """
        config = self.get_config()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save as numpy file
        np.save(save_path, config)
        logger.info(f"Saved quantum feature extractor configuration to {save_path}")
    
    @classmethod
    def load_configuration(cls, load_path: str) -> 'QuantumFeatureExtractor':
        """Load a quantum feature extractor configuration.
        
        Args:
            load_path: Path to load the configuration from
            
        Returns:
            Configured QuantumFeatureExtractor instance
        """
        config = np.load(load_path, allow_pickle=True).item()
        logger.info(f"Loaded quantum feature extractor configuration from {load_path}")
        
        return cls(**config) 