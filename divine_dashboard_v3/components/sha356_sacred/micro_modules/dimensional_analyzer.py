# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
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
Dimensional Analyzer Module for SHA-356 Sacred

Analyzes the dimensional properties of a SHA-356 Sacred hash, extracting
information about its projection into 6D hyperspace and cosmic alignment.
"""

import math
import matplotlib.pyplot as plt
from typing import Dict, Any, List, Tuple, Optional, Union
import io
from matplotlib.figure import Figure
from PIL import Image

# Create a stub for numpy to handle linter errors
class NumpyStub:
    """Minimal numpy-like stub for linting purposes."""
    
    def __init__(self):
        self.pi = math.pi
        
    def linspace(self, start, stop, num, endpoint=True):
        step = (stop - start) / (num - 1 if endpoint else num)
        result = [start + step * i for i in range(num)]
        result.tolist = lambda: result
        return result
            
    def degrees(self, radians):
        result = [r * 180 / math.pi for r in radians]
        result.tolist = lambda: result
        return result
            
    def array(self, obj):
        return obj

# Use try/except to import numpy
try:
    import numpy as np
except ImportError:
    np = NumpyStub()

# Constants for dimensional analysis
PHI = (1 + math.sqrt(5)) / 2  # Golden ratio (1.618...)
DIMENSION_NAMES = ["Physical", "Temporal", "Ethereal", "Astral", "Causal", "Void"]
DIMENSION_COLORS = ["#3498db", "#e74c3c", "#2ecc71", "#9b59b6", "#f39c12", "#1abc9c"]

def extract_dimensional_signature(hash_hex: str) -> List[float]:
    """
    Extract 6D dimensional signature from a SHA-356 Sacred hash.
    
    Args:
        hash_hex: A SHA-356 Sacred hash (89 hex characters)
        
    Returns:
        A list of 6 dimensional values ranging from -2.0 to 2.0
    """
    if len(hash_hex) != 89:
        raise ValueError("SHA-356 Sacred hash must be 89 hexadecimal characters")
    
    # Convert hash to list of integers
    hash_ints = []
    for i in range(0, len(hash_hex), 2):
        if i+1 < len(hash_hex):
            hash_ints.append(int(hash_hex[i:i+2], 16))
        else:
            hash_ints.append(int(hash_hex[i], 16))
    
    # Group integers for dimensional extraction (using pairs)
    dim_values = []
    for i in range(6):
        # Use specific regions of the hash for each dimension
        start_idx = i * 14
        region_sum = sum(hash_ints[start_idx:start_idx+14])
        
        # Normalize to range -2.0 to 2.0
        normalized = (region_sum / (255 * 14) * 4) - 2
        dim_values.append(normalized)
    
    return dim_values

def analyze_dimensions(hash_hex: str) -> Dict[str, Any]:
    """
    Perform dimensional analysis on a SHA-356 Sacred hash.
    
    Args:
        hash_hex: A SHA-356 Sacred hash (89 hex characters)
        
    Returns:
        Dictionary with dimensional analysis data
    """
    # Extract dimensional signature
    dim_signature = extract_dimensional_signature(hash_hex)
    
    # Calculate dimensional metrics
    dim_magnitude = math.sqrt(sum(v**2 for v in dim_signature))
    dim_harmony = calculate_dimensional_harmony(dim_signature)
    dim_balance = calculate_dimensional_balance(dim_signature)
    void_presence = calculate_void_presence(dim_signature)
    
    # Create dimensional report
    dim_report = {}
    for i, name in enumerate(DIMENSION_NAMES):
        dim_report[name] = {
            "value": dim_signature[i],
            "normalized": (dim_signature[i] + 2) / 4,  # 0 to 1 scale
            "polarity": "Positive" if dim_signature[i] >= 0 else "Negative",
            "intensity": abs(dim_signature[i]) / 2 * 100  # Percentage intensity
        }
    
    # Compile results
    return {
        "dimensional_signature": dim_signature,
        "magnitude": dim_magnitude,
        "harmony": dim_harmony,
        "balance": dim_balance,
        "void_presence": void_presence,
        "dimensions": dim_report
    }

def calculate_dimensional_harmony(dim_signature: List[float]) -> float:
    """
    Calculate the dimensional harmony - how well dimensions complement each other.
    Higher values indicate more harmonic relationships between dimensions.
    
    Args:
        dim_signature: 6D dimensional signature
        
    Returns:
        Harmony score between 0.0 and 1.0
    """
    harmony = 0.0
    
    # Check golden ratio relationships between dimensions
    for i in range(6):
        for j in range(i+1, 6):
            # Calculate ratio between dimension values (absolute to avoid division by zero)
            a, b = abs(dim_signature[i] + 2.001), abs(dim_signature[j] + 2.001)
            ratio = max(a, b) / min(a, b)
            
            # How close is this to PHI?
            phi_proximity = 1 - min(abs(ratio - PHI), abs(ratio - 1/PHI)) / PHI
            harmony += phi_proximity
    
    # Normalize to 0-1 range (15 is max number of pairs with 6 dimensions)
    return harmony / 15

def calculate_dimensional_balance(dim_signature: List[float]) -> float:
    """
    Calculate dimensional balance - how evenly the dimensions are distributed.
    1.0 means perfectly balanced, 0.0 means completely unbalanced.
    
    Args:
        dim_signature: 6D dimensional signature
        
    Returns:
        Balance score between 0.0 and 1.0
    """
    # Normalize to positive values for calculation
    normalized = [v + 2 for v in dim_signature]
    
    # Calculate variance
    mean = sum(normalized) / len(normalized)
    variance = sum((v - mean)**2 for v in normalized) / len(normalized)
    
    # Convert variance to balance score (inverse relationship)
    max_possible_variance = 4  # Maximum possible in our range
    balance = 1 - (variance / max_possible_variance)
    
    return max(0.0, min(1.0, balance))

def calculate_void_presence(dim_signature: List[float]) -> float:
    """
    Calculate void presence - the influence of the Void dimension.
    
    Args:
        dim_signature: 6D dimensional signature
        
    Returns:
        Void presence score between 0.0 and 1.0
    """
    # Void is the 6th dimension
    void_value = dim_signature[5]
    
    # Normalize to 0-1 range
    void_presence = (void_value + 2) / 4
    
    # The Void influences other dimensions when strong
    if void_presence > 0.7:
        # Calculate how much void pulls on other dimensions
        void_influence = sum(abs(dim_signature[i] - void_value) for i in range(5)) / 20
        void_presence = 0.7 + (void_presence - 0.7) * (1 - void_influence)
    
    return void_presence

def create_dimension_radar_chart(dim_analysis: Dict[str, Any]) -> Any:
    """
    Create a radar chart visualization of dimensional signature.
    
    Args:
        dim_analysis: Dimensional analysis dictionary
        
    Returns:
        Image data (format depends on numpy availability)
    """
    # Extract dimension values
    dim_values = [dim_analysis["dimensions"][name]["normalized"] for name in DIMENSION_NAMES]
    
    # Set up radar chart
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    
    # Set the angles for each dimension (equally spaced)
    angles = np.linspace(0, 2*np.pi, len(DIMENSION_NAMES), endpoint=False)
    angles_list = angles.tolist() if hasattr(angles, 'tolist') else angles
    angles_list += angles_list[:1]  # Close the loop
    
    # Add values and close the loop
    values = dim_values + [dim_values[0]]
    
    # Plot radar
    ax.plot(angles_list, values, linewidth=2, linestyle='solid', color='#2980b9')
    ax.fill(angles_list, values, alpha=0.25, color='#3498db')
    
    # Add dimension labels - using set_xticks and set_xticklabels instead of set_thetagrids
    ax.set_xticks(angles)
    ax.set_xticklabels(DIMENSION_NAMES)
    
    # Set y limits
    ax.set_ylim(0, 1)
    
    # Add harmony and balance annotations
    harmony = dim_analysis["harmony"]
    balance = dim_analysis["balance"]
    plt.annotate(f"Harmony: {harmony:.2f}", xy=(0.5, 0.02), xycoords='figure fraction', 
                ha='center', fontsize=10, color='#333333')
    plt.annotate(f"Balance: {balance:.2f}", xy=(0.5, 0.06), xycoords='figure fraction', 
                ha='center', fontsize=10, color='#333333')
    
    # Convert to image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    # Convert to image data
    img = Image.open(buf)
    
    # Convert to numpy array if available
    if 'numpy' in globals() or 'np' in globals() and hasattr(np, 'array'):
        return np.array(img)
    return img

def create_dimension_bar_chart(dim_analysis: Dict[str, Any]) -> Any:
    """
    Create a bar chart visualization of dimensional values.
    
    Args:
        dim_analysis: Dimensional analysis dictionary
        
    Returns:
        Image data (format depends on numpy availability)
    """
    # Extract raw dimension values
    dim_values = [dim_analysis["dimensions"][name]["value"] for name in DIMENSION_NAMES]
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(DIMENSION_NAMES, dim_values, color=DIMENSION_COLORS)
    
    # Add zero line
    ax.axhline(y=0, color='#7f8c8d', linestyle='-', linewidth=0.5)
    
    # Add labels and title
    ax.set_ylabel('Dimensional Value')
    ax.set_title('SHA-356 Sacred Dimensional Analysis')
    
    # Add values on bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                   xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 3 if height >= 0 else -12),
                   textcoords="offset points",
                   ha='center', va='bottom')
    
    # Set y-axis limits to ensure consistent scale
    ax.set_ylim(-2.5, 2.5)
    
    # Convert to image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    # Convert to image data
    img = Image.open(buf)
    
    # Convert to numpy array if available
    if 'numpy' in globals() or 'np' in globals() and hasattr(np, 'array'):
        return np.array(img)
    return img

def compare_dimensional_signatures(sig1: List[float], sig2: List[float]) -> Dict[str, Any]:
    """
    Compare two dimensional signatures and analyze their differences.
    
    Args:
        sig1: First 6D dimensional signature
        sig2: Second 6D dimensional signature
        
    Returns:
        Dictionary with comparison results
    """
    # Calculate differences
    differences = [abs(a - b) for a, b in zip(sig1, sig2)]
    
    # Calculate overall difference
    total_diff = sum(differences)
    max_possible_diff = 4 * 6  # Maximum possible difference (±2 in each dimension)
    diff_percentage = total_diff / max_possible_diff * 100
    
    # Find most different dimension
    most_diff_idx = differences.index(max(differences))
    most_diff_name = DIMENSION_NAMES[most_diff_idx]
    
    # Calculate dimensional shift vector
    shift_vector = [b - a for a, b in zip(sig1, sig2)]
    
    # Calculate if signature shifted toward or away from void
    void_shift = shift_vector[5]  # 6th dimension is Void
    void_relationship = "toward" if void_shift > 0 else "away from"
    
    return {
        "dimensional_differences": differences,
        "total_difference": total_diff,
        "difference_percentage": diff_percentage,
        "most_different_dimension": most_diff_name,
        "most_different_value": differences[most_diff_idx],
        "shift_vector": shift_vector,
        "void_shift": void_shift,
        "void_relationship": void_relationship
    }

def create_comparison_visualization(sig1: List[float], sig2: List[float]) -> Any:
    """
    Create a visualization comparing two dimensional signatures.
    
    Args:
        sig1: First 6D dimensional signature
        sig2: Second 6D dimensional signature
        
    Returns:
        Image data (format depends on numpy availability)
    """
    # Set up radar chart
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, polar=True)
    
    # Set the angles for each dimension (equally spaced)
    angles = np.linspace(0, 2*np.pi, len(DIMENSION_NAMES), endpoint=False)
    angles_list = angles.tolist() if hasattr(angles, 'tolist') else angles
    angles_list += angles_list[:1]  # Close the loop
    
    # Add values and close the loop
    values1 = [(v + 2) / 4 for v in sig1]  # Normalize to 0-1
    values2 = [(v + 2) / 4 for v in sig2]  # Normalize to 0-1
    values1 += values1[:1]  # Close the loop
    values2 += values2[:1]  # Close the loop
    
    # Plot both signatures
    ax.plot(angles_list, values1, linewidth=2, linestyle='solid', color='#2980b9', label='Hash 1')
    ax.fill(angles_list, values1, alpha=0.1, color='#3498db')
    
    ax.plot(angles_list, values2, linewidth=2, linestyle='solid', color='#c0392b', label='Hash 2')
    ax.fill(angles_list, values2, alpha=0.1, color='#e74c3c')
    
    # Add dimension labels - using set_xticks and set_xticklabels instead of set_thetagrids
    ax.set_xticks(angles)
    ax.set_xticklabels(DIMENSION_NAMES)
    
    # Set y limits
    ax.set_ylim(0, 1)
    
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # Convert to image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    
    # Convert to image data
    img = Image.open(buf)
    
    # Convert to numpy array if available
    if 'numpy' in globals() or 'np' in globals() and hasattr(np, 'array'):
        return np.array(img)
    return img 