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
Avalanche Analyzer Module

Compares two hashes and analyzes the bit-level avalanche effect.
"""

from typing import Dict, Any, List, Tuple

def hex_to_binary(hex_str: str) -> str:
    """
    Convert a hexadecimal string to its binary representation.
    
    Args:
        hex_str: Hexadecimal string
        
    Returns:
        Binary string representation
    """
    # Convert to integer then to binary, removing '0b' prefix and zero-padding to 256 bits
    return bin(int(hex_str, 16))[2:].zfill(256)

def avalanche_score(hash1: str, hash2: str) -> float:
    """
    Calculate the avalanche effect score between two hash values.
    
    The avalanche score represents the percentage of bits that differ between
    the two hashes, with an ideal score of ~0.5 (50%) for cryptographic functions.
    
    Args:
        hash1: First SHA256 hash (hexadecimal)
        hash2: Second SHA256 hash (hexadecimal)
        
    Returns:
        Avalanche score between 0.0 and 1.0
    """
    # Convert hashes to binary
    b1 = hex_to_binary(hash1)
    b2 = hex_to_binary(hash2)
    
    # Count differing bits
    diff_count = sum(x != y for x, y in zip(b1, b2))
    
    # Calculate percentage (0.0 to 1.0)
    return diff_count / 256.0

def detailed_avalanche_analysis(hash1: str, hash2: str) -> Dict[str, Any]:
    """
    Perform detailed analysis of the avalanche effect between two hashes.
    
    Args:
        hash1: First SHA256 hash (hexadecimal)
        hash2: Second SHA256 hash (hexadecimal)
        
    Returns:
        Dictionary containing detailed analysis results
    """
    # Convert hashes to binary
    b1 = hex_to_binary(hash1)
    b2 = hex_to_binary(hash2)
    
    # Calculate overall avalanche score
    score = avalanche_score(hash1, hash2)
    
    # Calculate differences by byte (8-bit chunks)
    byte_diffs = []
    for i in range(0, 256, 8):
        chunk1 = b1[i:i+8]
        chunk2 = b2[i:i+8]
        byte_diff = sum(x != y for x, y in zip(chunk1, chunk2))
        byte_diffs.append(byte_diff / 8.0)
    
    # Find sections with highest and lowest avalanche effect
    max_diff_byte = byte_diffs.index(max(byte_diffs))
    min_diff_byte = byte_diffs.index(min(byte_diffs))
    
    # Calculate whether the avalanche effect is properly distributed
    # (std dev of byte differences should be relatively small)
    import statistics
    byte_diff_std = statistics.stdev(byte_diffs) if len(byte_diffs) > 1 else 0
    
    # Return comprehensive analysis
    return {
        "avalanche_score": score,
        "byte_level_scores": byte_diffs,
        "max_diff_byte": max_diff_byte,
        "min_diff_byte": min_diff_byte,
        "byte_diff_std": byte_diff_std,
        "quality_score": 1.0 - abs(0.5 - score) * 2,  # 1.0 = perfect (50% diff), 0.0 = worst (0% or 100% diff)
        "ideal_threshold": 0.45 <= score <= 0.55,
        "summary": f"Avalanche effect: {score:.2%}" + (
            " (IDEAL)" if 0.45 <= score <= 0.55 else 
            " (TOO LOW)" if score < 0.45 else 
            " (TOO HIGH)"
        )
    }

# Alias for dashboard compatibility
analyze_avalanche = detailed_avalanche_analysis 