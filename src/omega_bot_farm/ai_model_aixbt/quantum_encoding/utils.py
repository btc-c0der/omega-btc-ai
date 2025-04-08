#!/usr/bin/env python3
"""
Quantum Encoding Utilities
========================

Utility functions for quantum data encoding.
Provides helper functions for normalization, fidelity calculation,
visualization, and other common operations.
"""

import numpy as np
import logging
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Dict, List, Union, Any, Optional, Tuple, cast

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def normalize_vector(vector: np.ndarray) -> np.ndarray:
    """
    Normalize a vector to unit length.
    
    Args:
        vector (np.ndarray): Input vector to normalize
    
    Returns:
        np.ndarray: Normalized vector
    """
    norm = np.linalg.norm(vector)
    if norm == 0:
        logger.warning("Attempted to normalize a zero vector, returning zeros")
        return vector
    return vector / norm

def min_max_normalize(data: np.ndarray, feature_range: Tuple[float, float] = (0, 1)) -> np.ndarray:
    """
    Scale features to a given range using min-max normalization.
    
    Args:
        data (np.ndarray): Input data to normalize
        feature_range (tuple): Desired range of transformed data
    
    Returns:
        np.ndarray: Normalized data in the specified range
    """
    if len(data.shape) == 1:
        data = data.reshape(-1, 1)
    
    min_val = np.min(data, axis=0)
    max_val = np.max(data, axis=0)
    
    # Handle the case where min and max are the same
    range_val = max_val - min_val
    range_val[range_val == 0] = 1  # Avoid division by zero
    
    scaled_data = (data - min_val) / range_val
    
    # Scale to feature range
    min_dest, max_dest = feature_range
    scaled_data = scaled_data * (max_dest - min_dest) + min_dest
    
    if data.shape[1] == 1:
        return scaled_data.ravel()
    return scaled_data

def compute_encoding_fidelity(original: np.ndarray, decoded: np.ndarray) -> float:
    """
    Compute fidelity between original and decoded data.
    
    Args:
        original (np.ndarray): Original data vector
        decoded (np.ndarray): Decoded data vector
    
    Returns:
        float: Fidelity measure between 0 and 1
    """
    if len(original) != len(decoded):
        raise ValueError(f"Vectors must have same length: {len(original)} vs {len(decoded)}")
    
    # Normalize both vectors
    orig_norm = normalize_vector(original)
    dec_norm = normalize_vector(decoded)
    
    # Compute cosine similarity
    fidelity = np.abs(np.dot(orig_norm, dec_norm))
    return float(fidelity)  # Explicitly cast to float

def visualize_encoding(original: np.ndarray, encoded: np.ndarray, decoded: Optional[np.ndarray] = None, 
                      title: str = "Quantum Encoding Visualization") -> Figure:
    """
    Visualize original data, encoded quantum state, and optionally decoded data.
    
    Args:
        original (np.ndarray): Original data vector
        encoded (np.ndarray): Encoded quantum state
        decoded (np.ndarray, optional): Decoded data vector
        title (str): Plot title
    
    Returns:
        matplotlib.figure.Figure: Matplotlib figure object
    """
    has_decoded = decoded is not None
    n_plots = 3 if has_decoded else 2
    
    fig, axes = plt.subplots(1, n_plots, figsize=(n_plots*5, 4))
    
    # Plot original data
    x = np.arange(len(original))
    axes[0].bar(x, original, color='blue', alpha=0.7)
    axes[0].set_title("Original Data")
    axes[0].set_xlabel("Feature Index")
    axes[0].set_ylabel("Value")
    
    # Plot encoded state (probabilities)
    if len(encoded.shape) > 1:
        encoded = encoded.ravel()
    
    probs = np.abs(encoded)**2
    x = np.arange(len(probs))
    
    # Limit to first 16 states if there are many
    if len(probs) > 16:
        x = x[:16]
        probs = probs[:16]
        axes[1].set_title("Encoded State (First 16 Amplitudes)")
    else:
        axes[1].set_title("Encoded State")
        
    axes[1].bar(x, probs, color='purple', alpha=0.7)
    axes[1].set_xlabel("Quantum State Index")
    axes[1].set_ylabel("Probability")
    
    # Plot decoded data if provided
    if has_decoded and decoded is not None:  # Extra check for type safety
        x = np.arange(len(decoded))
        axes[2].bar(x, decoded, color='green', alpha=0.7)
        axes[2].set_title("Decoded Data")
        axes[2].set_xlabel("Feature Index")
        axes[2].set_ylabel("Value")
    
    # Add overall title
    fig.suptitle(title, fontsize=16)
    fig.tight_layout()
    
    return fig

def bitstring_to_int(bitstring: str) -> int:
    """
    Convert a binary string to an integer.
    
    Args:
        bitstring (str): Binary string (e.g., '101')
    
    Returns:
        int: Integer representation
    """
    return int(bitstring, 2)

def int_to_bitstring(integer: int, n_bits: int) -> str:
    """
    Convert an integer to a binary string with specified length.
    
    Args:
        integer (int): Integer to convert
        n_bits (int): Number of bits in the output
    
    Returns:
        str: Binary string representation
    """
    return format(integer, f'0{n_bits}b')

def hamming_distance(a: Union[str, int], b: Union[str, int]) -> int:
    """
    Calculate Hamming distance between two bit strings or integers.
    
    Args:
        a (Union[str, int]): First bit string or integer
        b (Union[str, int]): Second bit string or integer
    
    Returns:
        int: Hamming distance
    """
    # Convert integers to strings if needed
    a_str = str(a) if isinstance(a, int) else a
    b_str = str(b) if isinstance(b, int) else b
    
    # If they're integers converted to strings, convert to binary representation
    if all(c in '0123456789' for c in a_str) and all(c in '0123456789' for c in b_str):
        a_int = int(a_str)
        b_int = int(b_str)
        max_val = max(a_int, b_int)
        n_bits = max(1, max_val.bit_length())
        a_str = int_to_bitstring(a_int, n_bits)
        b_str = int_to_bitstring(b_int, n_bits)
    
    # Ensure strings are same length by padding
    if len(a_str) != len(b_str):
        max_len = max(len(a_str), len(b_str))
        a_str = a_str.zfill(max_len)
        b_str = b_str.zfill(max_len)
    
    # Calculate Hamming distance
    return sum(bit_a != bit_b for bit_a, bit_b in zip(a_str, b_str))

def binary_array_to_int(arr: np.ndarray) -> int:
    """
    Convert a binary array [0, 1, 0, 1] to an integer.
    
    Args:
        arr (np.ndarray): Binary array
    
    Returns:
        int: Integer representation
    """
    # Convert to string and then to int
    binary_str = ''.join(map(str, arr.astype(int)))
    return bitstring_to_int(binary_str)

def int_to_binary_array(num: int, length: int) -> np.ndarray:
    """
    Convert an integer to a binary array of specified length.
    
    Args:
        num (int): Integer to convert
        length (int): Length of binary array
    
    Returns:
        np.ndarray: Binary array
    """
    binary_str = int_to_bitstring(num, length)
    return np.array([int(bit) for bit in binary_str])

def calculate_reconstruction_error(original: np.ndarray, reconstructed: np.ndarray, 
                                 method: str = 'mse') -> float:
    """
    Calculate error between original and reconstructed data.
    
    Args:
        original: Original data
        reconstructed: Reconstructed data after encode-decode cycle
        method: Error metric ('mse', 'rmse', 'mae', 'mape')
        
    Returns:
        Error value
    """
    if not isinstance(original, np.ndarray):
        original = np.array(original)
    
    if not isinstance(reconstructed, np.ndarray):
        reconstructed = np.array(reconstructed)
    
    # Ensure same shape
    if original.shape != reconstructed.shape:
        logger.warning(f"Shape mismatch: {original.shape} vs {reconstructed.shape}")
        # Try to reshape if possible
        if original.size == reconstructed.size:
            reconstructed = reconstructed.reshape(original.shape)
        else:
            logger.error("Cannot compute error for different sized arrays")
            return float('inf')
    
    if method == 'mse':
        # Mean squared error
        return np.mean((original - reconstructed) ** 2)
        
    elif method == 'rmse':
        # Root mean squared error
        return np.sqrt(np.mean((original - reconstructed) ** 2))
        
    elif method == 'mae':
        # Mean absolute error
        return np.mean(np.abs(original - reconstructed))
        
    elif method == 'mape':
        # Mean absolute percentage error
        # Avoid division by zero
        mask = original != 0
        if not np.any(mask):
            return float('inf')
        return np.mean(np.abs((original[mask] - reconstructed[mask]) / original[mask])) * 100
        
    else:
        logger.warning(f"Unknown error method: {method}, using mse")
        return calculate_reconstruction_error(original, reconstructed, 'mse')

def visualize_encoding_fidelity(original: np.ndarray, reconstructed: np.ndarray, 
                               title: str = "Encoding Fidelity Analysis") -> plt.Figure:
    """
    Visualize encoding fidelity between original and reconstructed data.
    
    Args:
        original: Original data
        reconstructed: Reconstructed data
        title: Plot title
        
    Returns:
        Matplotlib figure
    """
    fig = plt.figure(figsize=(14, 8))
    
    # Scatter plot comparing original vs reconstructed
    ax1 = fig.add_subplot(121)
    
    # Flatten data for comparison
    orig_flat = original.flatten()
    recon_flat = reconstructed.flatten()
    
    # Scatter plot with identity line
    ax1.scatter(orig_flat, recon_flat, alpha=0.5, color='blue')
    
    # Add identity line
    min_val = min(np.min(orig_flat), np.min(recon_flat))
    max_val = max(np.max(orig_flat), np.max(recon_flat))
    padding = (max_val - min_val) * 0.1
    ax1.plot([min_val - padding, max_val + padding], [min_val - padding, max_val + padding], 
             'r--', label='Identity')
    
    ax1.set_title("Original vs Reconstructed")
    ax1.set_xlabel("Original Values")
    ax1.set_ylabel("Reconstructed Values")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Compute and display error metrics
    ax2 = fig.add_subplot(122)
    
    metrics = {
        'MSE': calculate_reconstruction_error(original, reconstructed, 'mse'),
        'RMSE': calculate_reconstruction_error(original, reconstructed, 'rmse'),
        'MAE': calculate_reconstruction_error(original, reconstructed, 'mae'),
        'Fidelity': compute_encoding_fidelity(original, reconstructed)
    }
    
    # Try to calculate MAPE if no zeros in original
    if not np.any(original == 0):
        metrics['MAPE'] = calculate_reconstruction_error(original, reconstructed, 'mape')
    
    # Bar chart of metrics
    metric_names = list(metrics.keys())
    metric_values = list(metrics.values())
    
    # Use different colors for fidelity (higher is better) vs errors (lower is better)
    colors = ['red'] * (len(metrics) - 1) + ['green']
    
    bars = ax2.bar(metric_names, metric_values, color=colors)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.annotate(f'{height:.4f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    ax2.set_title("Reconstruction Metrics")
    ax2.set_ylabel("Value")
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    
    return fig

def compare_encoders(encoders: List[Any], data: np.ndarray, 
                   title: str = "Encoder Comparison") -> plt.Figure:
    """
    Compare multiple encoders on the same data.
    
    Args:
        encoders: List of encoder instances
        data: Data to encode and decode
        title: Plot title
        
    Returns:
        Matplotlib figure
    """
    n_encoders = len(encoders)
    
    fig = plt.figure(figsize=(14, 4 * n_encoders))
    
    # Create a flattened copy of data for consistent comparison
    flat_data = data.flatten() if len(data.shape) > 1 else data
    
    # Metrics to track
    metrics = []
    
    for i, encoder in enumerate(encoders):
        # Encode and decode
        encoded = encoder.encode(flat_data)
        decoded = encoder.decode(encoded)
        
        # Calculate metrics
        fidelity = compute_encoding_fidelity(flat_data, decoded)
        mse = calculate_reconstruction_error(flat_data, decoded, 'mse')
        
        metrics.append({
            'name': encoder.name,
            'fidelity': fidelity,
            'mse': mse,
            'n_qubits': encoder.n_qubits,
            'dimension': encoder.dimension
        })
        
        # Create plot for this encoder
        ax = fig.add_subplot(n_encoders, 1, i+1)
        
        # Plot original and reconstructed
        ax.plot(flat_data, marker='o', linestyle='-', color='blue', label='Original')
        ax.plot(decoded, marker='x', linestyle='--', color='red', label='Reconstructed')
        
        ax.set_title(f"{encoder.name} (n_qubits={encoder.n_qubits}, fidelity={fidelity:.4f})")
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout()
    
    return fig, metrics 