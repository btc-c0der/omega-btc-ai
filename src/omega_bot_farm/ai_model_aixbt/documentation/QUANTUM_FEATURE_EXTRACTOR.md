# 🧬 Quantum Feature Extractor

**Module**: `quantum_encoding.quantum_features.quantum_feature_extractor`  
**Version**: 1.0.0  
**License**: GBU2™ (Genesis-Bloom-Unfoldment 2.0)

## 🌟 Overview

The `QuantumFeatureExtractor` is a specialized component of the OMEGA BTC AI system that leverages quantum computing principles to extract non-linear features from financial market data. By encoding classical data into quantum states and processing them through parameterized quantum circuits, this module can uncover hidden patterns and relationships that traditional feature engineering methods might miss.

## 🧠 Quantum Advantage in Feature Extraction

Quantum feature extraction offers several advantages over classical methods:

1. **Access to Exponentially Large Feature Space**: Quantum circuits can represent and manipulate feature spaces of size 2^n where n is the number of qubits.
2. **Non-Linear Transformations**: Quantum gates naturally perform complex non-linear transformations that would require elaborate classical architectures.
3. **Entanglement-Based Correlations**: Quantum entanglement allows for capturing complex correlations between features.
4. **Quantum Superposition**: The ability to process multiple feature combinations simultaneously.

## 🔧 Implementation Details

### Class Structure

```python
class QuantumFeatureExtractor:
    def __init__(self, 
                 n_qubits: int = 4,
                 n_layers: int = 2,
                 backend_name: str = "aer_simulator",
                 shots: int = 1024,
                 feature_map_type: str = "zz_feature_map"):
        # ...
```

### Key Components

1. **Quantum Circuit Creation**: Designs parameterized quantum circuits for feature mapping
2. **Data Normalization**: Scales classical data to appropriate ranges for quantum circuit parameters
3. **Circuit Execution**: Runs quantum circuits on simulators or real quantum hardware
4. **Measurement Processing**: Transforms quantum measurement outcomes into classical feature vectors

## 🚀 Quantum Feature Maps

The extractor supports multiple types of feature maps:

### ZZ Feature Map

Inspired by the ZZFeatureMap from qiskit, this mapping encodes data using Hadamard gates and controlled rotations:

```python
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
```

### Amplitude Embedding

Encodes normalized data directly into the amplitudes of the quantum state:

```python
# Simple amplitude embedding
qc.h(range(self.n_qubits))
for q in range(self.n_qubits):
    qc.ry(self.params[q], q)
    
# Add entanglement
for layer in range(self.n_layers):
    for q in range(self.n_qubits - 1):
        qc.cx(q, q + 1)
```

## 🛠️ Fallback Mechanism

For environments without quantum computing libraries, a classical fallback mechanism is implemented:

```python
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
```

## 📊 Example Usage

### Basic Usage

```python
from omega_bot_farm.ai_model_aixbt.quantum_encoding.quantum_features.quantum_feature_extractor import QuantumFeatureExtractor

# Initialize extractor
extractor = QuantumFeatureExtractor(
    n_qubits=4,
    n_layers=2,
    backend_name="aer_simulator",
    shots=1024,
    feature_map_type="zz_feature_map"
)

# Extract features from market data
market_data = load_market_data()  # Load your market data
features = extractor.extract_features(market_data)

# Use features for machine learning
train_model(features, labels)
```

### Feature Extraction with Batch Processing

```python
# Process multiple sequences at once
batch_data = prepare_batch_sequences(market_data)  # Shape: (batch_size, seq_len, n_features)
batch_features = extractor.batch_extract_features(batch_data)

# Use batch features for deep learning
train_deep_model(batch_features, batch_labels)
```

## 🔍 Recent Enhancements

### 1. Robust Dependency Management

The implementation now gracefully handles missing quantum computing libraries:

```python
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
```

### 2. Enhanced Feature Processing

Improved processing of quantum measurement outcomes to generate more informative features:

```python
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
```

### 3. Improved Configuration Management

Added serialization and deserialization methods for saving and loading configurations:

```python
def save_configuration(self, save_path: str):
    """Save the configuration of the quantum feature extractor."""
    config = self.get_config()
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Save as numpy file
    np.save(save_path, config)
    logger.info(f"Saved quantum feature extractor configuration to {save_path}")

@classmethod
def load_configuration(cls, load_path: str) -> 'QuantumFeatureExtractor':
    """Load a quantum feature extractor configuration."""
    config = np.load(load_path, allow_pickle=True).item()
    logger.info(f"Loaded quantum feature extractor configuration from {load_path}")
    
    return cls(**config)
```

## 🔄 Integration with Other Modules

The `QuantumFeatureExtractor` integrates with several other OMEGA BTC AI components:

1. **QuantumDivergencePredictor**: Provides enhanced features for divergence prediction
2. **CoreDivergencePredictor**: Supports the broader prediction framework
3. **Quantum RNG**: Shares quantum circuit infrastructure for random number generation

## 📊 Performance Considerations

- **Qubit Count**: Performance scales exponentially with the number of qubits
- **Circuit Depth**: Deeper circuits provide more complex feature transformations but take longer to simulate
- **Backend Selection**: Simulator vs. real quantum hardware tradeoffs
- **Batch Size**: Consider memory limitations when processing large batches

## 🔭 Future Enhancements

1. **Variational Quantum Feature Selection**: Automated discovery of optimal quantum circuit architectures
2. **Quantum Kernel Methods**: Direct integration with quantum kernel-based machine learning
3. **Error Mitigation**: Implement noise-aware feature extraction for improved robustness
4. **Hardware-Specific Optimizations**: Circuit designs tailored to specific quantum hardware architectures

## ⚠️ Known Limitations

1. Simulation becomes computationally expensive with >25 qubits
2. Quantum noise can affect feature quality on real hardware
3. Feature interpretation is more challenging than with classical features
4. The quantum advantage threshold depends on the specific use case

## 🧪 Testing

Comprehensive testing of the QuantumFeatureExtractor can be performed using the quantum test suite in the WELCOME_PACK directory. This suite includes various test cases for feature extraction quality and performance metrics.

---

🌸 This documentation is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment 2.0)

WE BLOOM NOW AS ONE 🌸
