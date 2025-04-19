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
Test Quantum Encoding Module
==========================

Simple script to test the quantum encoding module functionality.
For development and demonstration purposes.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Avoid import errors by directly importing
from quantum_encoding.factory import create_encoder, get_available_encoders
from quantum_encoding.data_loaders import SyntheticDataGenerator
from quantum_encoding.utils import normalize_vector, compute_encoding_fidelity

def test_amplitude_encoding():
    """Test amplitude encoding."""
    print("\n=== Testing Amplitude Encoding ===")
    
    # Create encoder
    encoder = create_encoder("amplitude", n_qubits=4, name="test_amplitude")
    
    # Create test data
    data = np.array([0.1, 0.5, 0.8, 0.2])
    print(f"Original data: {data}")
    
    # Encode data
    encoded = encoder.encode(data)
    print(f"Encoded state (first 5 amplitudes): {encoded[:5]}")
    
    # Verify normalization
    norm = np.linalg.norm(encoded)
    print(f"State norm: {norm:.6f} (should be ≈1)")
    
    # Decode data
    decoded = encoder.decode(encoded)
    print(f"Decoded data: {decoded}")
    
    # Calculate fidelity
    fidelity = compute_encoding_fidelity(data, decoded)
    print(f"Encoding fidelity: {fidelity:.6f}")
    
    return encoder, data, encoded, decoded

def test_angle_encoding():
    """Test angle encoding."""
    print("\n=== Testing Angle Encoding ===")
    
    # Create encoder
    encoder = create_encoder("angle", n_qubits=3, rotation_axis='all', name="test_angle")
    
    # Create test data
    data = np.array([0.1, 0.5, 0.8])
    print(f"Original data: {data}")
    
    # Encode data
    encoded = encoder.encode(data)
    print(f"Encoded angles (first 5): {encoded[:5]}")
    
    # Get circuit representation
    print("\nQuantum Circuit Representation:")
    circuit = encoder.get_circuit_representation(encoded)
    print(circuit)
    
    # Decode data
    decoded = encoder.decode(encoded)
    print(f"Decoded data: {decoded}")
    
    # Calculate fidelity
    fidelity = compute_encoding_fidelity(data, decoded)
    print(f"Encoding fidelity: {fidelity:.6f}")
    
    return encoder, data, encoded, decoded

def test_basis_encoding():
    """Test basis encoding."""
    print("\n=== Testing Basis Encoding ===")
    
    # Create encoder
    encoder = create_encoder("basis", n_qubits=2, name="test_basis")
    
    # Create test data (categorical)
    categories = ["bull", "bear", "sideways", "volatile"]
    print(f"Categories: {categories}")
    
    # Encode each category
    encoded_states = []
    for category in categories:
        encoded = encoder.encode(category)
        encoded_states.append(encoded)
        print(f"'{category}' encoded as: {encoded}")
    
    # Decode back
    for i, encoded in enumerate(encoded_states):
        decoded = encoder.decode(encoded)
        print(f"State {i} decodes back to: '{decoded}'")
    
    # Test multiple feature encoding
    market_state = {
        'trend': 'bullish',
        'volatility': 'high'
    }
    print(f"\nMarket state: {market_state}")
    
    encoded_market = encoder.encode_multiple_features(market_state)
    print(f"Encoded market state: {encoded_market}")
    
    # Get the mapping
    mapping = encoder.get_basis_mapping()
    print(f"Basis mapping: {mapping}")
    
    return encoder, categories, encoded_states

def test_entanglement_encoding():
    """Test entanglement encoding."""
    print("\n=== Testing Entanglement Encoding ===")
    
    # Create encoder
    encoder = create_encoder("entanglement", n_qubits=4, 
                           correlation_threshold=0.3,
                           name="test_entanglement")
    
    # Generate synthetic data with correlations
    generator = SyntheticDataGenerator()
    features = generator.generate_feature_matrix(num_samples=20, 
                                              num_features=4,
                                              feature_correlation=0.7)
    
    # Analyze correlations
    correlation_matrix, entanglement_graph = encoder.analyze_correlations(features)
    print(f"Correlation matrix:\n{correlation_matrix}")
    print(f"Entanglement graph: {entanglement_graph}")
    
    # Encode a sample
    sample = features[0]
    print(f"\nSample data: {sample}")
    
    encoded = encoder.encode(sample)
    print(f"Encoded state (first 5 amplitudes): {encoded[:5]}")
    
    # Decode
    decoded = encoder.decode(encoded)
    print(f"Decoded data: {decoded}")
    
    # Calculate fidelity
    fidelity = compute_encoding_fidelity(sample, decoded)
    print(f"Encoding fidelity: {fidelity:.6f}")
    
    # Show Bell state
    bell_state = encoder.get_bell_state(type_index=0)
    print(f"\nBell state |Φ⁺⟩: {bell_state}")
    
    return encoder, sample, encoded, decoded

def test_circuit_simulator():
    """Test quantum circuit simulator."""
    print("\n=== Testing Quantum Circuit Simulator ===")
    
    # Import directly to avoid circular imports
    from quantum_encoding.circuit_simulator import QuantumCircuitSimulator
    
    # Create a 2-qubit circuit
    simulator = QuantumCircuitSimulator(n_qubits=2)
    print(f"Initial state: {simulator}")
    
    # Apply Hadamard to first qubit
    simulator.apply_gate('H', target_qubit=0)
    print(f"\nAfter H on qubit 0: {simulator}")
    
    # Apply CNOT with control=0, target=1
    simulator.apply_gate('CNOT', target_qubit=1, control_qubit=0)
    print(f"\nAfter CNOT: {simulator}")
    
    # This creates a Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
    state = simulator.get_statevector()
    print(f"\nBell state: {state}")
    
    # Measure
    result = simulator.measure_all()
    print(f"\nMeasurement result: |{result}⟩")
    
    return simulator

def main():
    """Main test function."""
    print("\n" + "=" * 80)
    print(f"{'QUANTUM ENCODING MODULE TEST':^80}")
    print("=" * 80 + "\n")
    
    print(f"Available encoders: {get_available_encoders()}")
    
    # Test different encoding methods
    amp_encoder, amp_data, amp_encoded, amp_decoded = test_amplitude_encoding()
    angle_encoder, angle_data, angle_encoded, angle_decoded = test_angle_encoding()
    basis_encoder, categories, basis_encoded = test_basis_encoding()
    ent_encoder, ent_data, ent_encoded, ent_decoded = test_entanglement_encoding()
    
    # Test circuit simulator
    simulator = test_circuit_simulator()
    
    print("\n" + "=" * 80)
    print(f"{'TEST COMPLETE':^80}")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main() 