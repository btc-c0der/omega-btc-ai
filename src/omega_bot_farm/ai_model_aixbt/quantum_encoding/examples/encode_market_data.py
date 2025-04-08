#!/usr/bin/env python3
"""
Market Data Encoding Example
=========================

Example script demonstrating how to encode market data using
different quantum encoding methods.

This script shows how to:
1. Load market data using MarketDataLoader
2. Apply different quantum encoding methods
3. Visualize the encoded data
4. Compare encoding results
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any
import pandas as pd
import logging

# Add parent directory to path to allow imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # quantum_encoding
grandparent_dir = os.path.dirname(parent_dir)  # ai_model_aixbt
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
if grandparent_dir not in sys.path:
    sys.path.append(grandparent_dir)

# Import quantum encoding components
from quantum_encoding import (
    create_encoder,
    get_available_encoders,
    MarketDataLoader,
    visualize_encoding,
    compute_encoding_fidelity
)

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("quantum-encoding-example")


def load_market_data() -> Tuple[np.ndarray, List[str]]:
    """
    Load market data for encoding.
    
    Returns:
        Tuple[np.ndarray, List[str]]: Market data and feature names
    """
    # Initialize data loader with fallback to synthetic data
    loader = MarketDataLoader(
        data_dir="data/aixbt_training_data",
        fallback_to_synthetic=True
    )
    
    # Load data
    feature_names = ['price', 'volume', 'volatility', 'return']
    
    try:
        # Try to load actual market data
        data = loader.load_data()
        # Select only the features we want to encode
        features = loader.get_feature_matrix(feature_names)
    except Exception as e:
        logger.warning(f"Failed to load real market data: {e}")
        logger.info("Falling back to synthetic data")
        
        # Generate synthetic market dataset
        synthetic_generator = loader.synthetic_generator
        syn_data = synthetic_generator.generate_market_dataset(
            num_samples=100,
            include_price=True,
            include_volume=True,
            include_volatility=True
        )
        
        # Extract features
        features = syn_data[feature_names].values
    
    logger.info(f"Loaded market data with {len(features)} samples and {len(feature_names)} features")
    
    return features, feature_names


def encode_with_different_methods(features: np.ndarray, feature_names: List[str]) -> Dict[str, Any]:
    """
    Encode market data using different quantum encoding methods.
    
    Args:
        features (np.ndarray): Market data features
        feature_names (List[str]): Names of features
    
    Returns:
        Dict[str, Any]: Dictionary of encoding results
    """
    results = {}
    
    # Normalize features for better encoding
    features_norm = np.zeros_like(features)
    for i in range(features.shape[1]):
        column = features[:, i]
        min_val = np.min(column)
        max_val = np.max(column)
        features_norm[:, i] = (column - min_val) / (max_val - min_val)
    
    # We'll use the first sample for demonstration
    sample = features_norm[0]
    logger.info(f"Normalized sample for encoding: {sample}")
    
    # 1. Amplitude Encoding
    amplitude_encoder = create_encoder("amplitude", n_qubits=4, name="market_amplitude")
    amplitude_encoded = amplitude_encoder.encode(sample)
    amplitude_decoded = amplitude_encoder.decode(amplitude_encoded)
    amplitude_fidelity = compute_encoding_fidelity(sample, amplitude_decoded)
    
    logger.info(f"Amplitude encoding: {len(amplitude_encoded)} amplitudes, fidelity: {amplitude_fidelity:.4f}")
    
    results["amplitude"] = {
        "encoder": amplitude_encoder,
        "encoded": amplitude_encoded,
        "decoded": amplitude_decoded,
        "fidelity": amplitude_fidelity
    }
    
    # 2. Angle Encoding
    angle_encoder = create_encoder("angle", n_qubits=3, rotation_axis='all', name="market_angle")
    angle_encoded = angle_encoder.encode(sample)
    angle_decoded = angle_encoder.decode(angle_encoded)
    angle_fidelity = compute_encoding_fidelity(sample, angle_decoded)
    
    logger.info(f"Angle encoding: {len(angle_encoded)} angles, fidelity: {angle_fidelity:.4f}")
    
    results["angle"] = {
        "encoder": angle_encoder,
        "encoded": angle_encoded,
        "decoded": angle_decoded,
        "fidelity": angle_fidelity,
        "circuit": angle_encoder.get_circuit_representation(angle_encoded)
    }
    
    # 3. Basis Encoding (for categorical data)
    # We'll discretize the volatility to categories for this example
    volatility_idx = feature_names.index('volatility')
    volatility_value = features[0, volatility_idx]
    
    # Create categories based on volatility value
    if volatility_value < 0.1:
        category = "low"
    elif volatility_value < 0.3:
        category = "medium"
    else:
        category = "high"
    
    logger.info(f"Volatility: {volatility_value}, categorized as: {category}")
    
    basis_encoder = create_encoder("basis", n_qubits=2, name="market_basis")
    basis_encoded = basis_encoder.encode(category)
    basis_decoded = basis_encoder.decode(basis_encoded)
    
    logger.info(f"Basis encoding: category '{category}' -> {basis_encoded} -> '{basis_decoded}'")
    
    results["basis"] = {
        "encoder": basis_encoder,
        "encoded": basis_encoded,
        "decoded": basis_decoded,
        "category": category
    }
    
    # 4. Entanglement Encoding
    # Select 4 samples to demonstrate correlation analysis
    samples = features_norm[:4]
    
    entanglement_encoder = create_encoder("entanglement", n_qubits=4, 
                                      correlation_threshold=0.3,
                                      name="market_entanglement")
    
    # Analyze correlations between features
    corr_matrix, entanglement_graph = entanglement_encoder.analyze_correlations(samples)
    
    # Encode one sample
    ent_encoded = entanglement_encoder.encode(sample)
    ent_decoded = entanglement_encoder.decode(ent_encoded)
    ent_fidelity = compute_encoding_fidelity(sample, ent_decoded)
    
    logger.info(f"Entanglement encoding: {len(ent_encoded)} amplitudes, fidelity: {ent_fidelity:.4f}")
    
    results["entanglement"] = {
        "encoder": entanglement_encoder,
        "encoded": ent_encoded,
        "decoded": ent_decoded,
        "fidelity": ent_fidelity,
        "correlation_matrix": corr_matrix,
        "entanglement_graph": entanglement_graph
    }
    
    return results


def visualize_results(results: Dict[str, Any], feature_names: List[str], sample: np.ndarray) -> None:
    """
    Visualize encoding results.
    
    Args:
        results (Dict[str, Any]): Encoding results
        feature_names (List[str]): Names of features
        sample (np.ndarray): Original data sample
    """
    # Set up figure
    plt.figure(figsize=(16, 12))
    
    # 1. Original data
    plt.subplot(321)
    plt.bar(feature_names, sample, color='blue')
    plt.title("Original Market Data")
    plt.xticks(rotation=45)
    
    # 2. Amplitude Encoding
    plt.subplot(322)
    amp_encoded = results["amplitude"]["encoded"]
    probs = np.abs(amp_encoded)**2
    plt.bar(range(min(16, len(probs))), probs[:16], color='purple')
    plt.title(f"Amplitude Encoding (Fidelity: {results['amplitude']['fidelity']:.4f})")
    plt.xlabel("Quantum State Index")
    plt.ylabel("Probability")
    
    # 3. Angle Encoding
    plt.subplot(323)
    angle_encoded = results["angle"]["encoded"]
    plt.bar(range(len(angle_encoded)), angle_encoded, color='green')
    plt.title(f"Angle Encoding (Fidelity: {results['angle']['fidelity']:.4f})")
    plt.xlabel("Angle Parameter Index")
    plt.ylabel("Angle Value")
    
    # 4. Angle Encoding Circuit
    plt.subplot(324)
    plt.text(0.1, 0.5, results["angle"]["circuit"], fontsize=9, family='monospace')
    plt.title("Quantum Circuit Representation")
    plt.axis('off')
    
    # 5. Basis Encoding
    plt.subplot(325)
    basis_encoded = results["basis"]["encoded"]
    plt.bar(range(len(basis_encoded)), basis_encoded, color='orange')
    plt.title(f"Basis Encoding (Category: {results['basis']['category']})")
    plt.xlabel("Basis State Index")
    plt.ylabel("Probability")
    
    # 6. Correlation Matrix for Entanglement Encoding
    plt.subplot(326)
    corr_matrix = results["entanglement"]["correlation_matrix"]
    plt.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
    plt.colorbar(label='Correlation')
    plt.title("Feature Correlation for Entanglement Encoding")
    tick_positions = np.arange(len(feature_names))
    plt.xticks(tick_positions, feature_names, rotation=45)
    plt.yticks(tick_positions, feature_names)
    
    plt.tight_layout()
    
    # Save figure
    output_dir = os.path.join(current_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "market_data_encoding.png"))
    logger.info(f"Saved visualization to {output_dir}/market_data_encoding.png")
    
    # Show individual plots for each encoding
    for encoding_type in ["amplitude", "angle", "entanglement"]:
        result = results[encoding_type]
        fig = visualize_encoding(
            sample, 
            result["encoded"], 
            result["decoded"],
            title=f"{encoding_type.capitalize()} Encoding (Fidelity: {result.get('fidelity', 0):.4f})"
        )
        fig.savefig(os.path.join(output_dir, f"{encoding_type}_encoding.png"))
        logger.info(f"Saved {encoding_type} encoding visualization")


def main() -> None:
    """Main function to run the example."""
    logger.info("Starting Market Data Encoding Example")
    
    # Get available encoding methods
    logger.info(f"Available encoders: {get_available_encoders()}")
    
    # Load market data
    features, feature_names = load_market_data()
    
    # Take first sample for demonstration
    sample = features[0]
    
    # Normalize sample
    sample_norm = np.zeros_like(sample)
    for i in range(len(sample)):
        min_val = np.min(features[:, i])
        max_val = np.max(features[:, i])
        sample_norm[i] = (sample[i] - min_val) / (max_val - min_val)
    
    # Encode with different methods
    results = encode_with_different_methods(features, feature_names)
    
    # Visualize results
    visualize_results(results, feature_names, sample_norm)
    
    logger.info("Market Data Encoding Example completed")


if __name__ == "__main__":
    main() 