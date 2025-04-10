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
Avalanche Effect Analyzer Module

Provides functions to analyze the avalanche effect in cryptographic hash functions.
The avalanche effect is the property where a small change in the input causes
a significant change in the output hash, which is essential for cryptographic security.
"""

import math
import re
from typing import List, Dict, Any, Tuple, Optional

def avalanche_score(hash1: str, hash2: str) -> float:
    """
    Calculate the avalanche effect score between two hash values.
    
    This returns a score between 0.0 and 1.0 that indicates how well the
    hash function exhibits the avalanche effect between these two inputs.
    A score of 0.5 is ideal (50% of bits changed).
    
    Args:
        hash1: First hash value (hex string)
        hash2: Second hash value (hex string)
        
    Returns:
        Avalanche score between 0.0 and 1.0
    """
    # Convert hex strings to binary
    bin1 = bin(int(hash1, 16))[2:].zfill(len(hash1) * 4)
    bin2 = bin(int(hash2, 16))[2:].zfill(len(hash2) * 4)
    
    # Calculate bit differences
    min_len = min(len(bin1), len(bin2))
    diff_bits = sum(1 for i in range(min_len) if bin1[i] != bin2[i])
    diff_percentage = diff_bits / min_len
    
    # Calculate score (1.0 = perfect 50% difference)
    # The closer the diff_percentage is to 0.5, the better the avalanche effect
    avalanche_quality = 1.0 - abs(0.5 - diff_percentage) * 2.0
    
    return avalanche_quality

def detailed_avalanche_analysis(hash1: str, hash2: str) -> Dict[str, Any]:
    """
    Perform detailed analysis of avalanche effect between two hashes.
    
    Args:
        hash1: First hash value (hex string)
        hash2: Second hash value (hex string)
        
    Returns:
        Dictionary with detailed analysis results
    """
    # Convert hex strings to binary
    bin1 = bin(int(hash1, 16))[2:].zfill(len(hash1) * 4)
    bin2 = bin(int(hash2, 16))[2:].zfill(len(hash2) * 4)
    
    # Calculate bit differences
    min_len = min(len(bin1), len(bin2))
    
    # Track position of each bit difference
    diff_positions = []
    for i in range(min_len):
        if bin1[i] != bin2[i]:
            diff_positions.append(i)
    
    # Calculate diff stats
    diff_bits = len(diff_positions)
    diff_percentage = diff_bits / min_len
    
    # Analyze bit distribution (check if changes are evenly distributed)
    byte_changes = [0] * (min_len // 8 + 1)
    for pos in diff_positions:
        byte_idx = pos // 8
        if byte_idx < len(byte_changes):
            byte_changes[byte_idx] += 1
    
    # Calculate byte-level entropy of changes
    byte_entropy = 0
    for changes in byte_changes:
        if changes > 0:
            p = changes / 8  # Probability of bit change within byte
            byte_entropy -= p * math.log2(p) + (1-p) * math.log2(1-p) if p < 1 else 0
    byte_entropy = byte_entropy / len(byte_changes) if byte_changes else 0
    
    # Calculate avalanche completeness - how well spread the changes are
    completeness = 1.0 - (max(byte_changes) - min(byte_changes)) / 8 if byte_changes else 0
    
    # Calculate burst resistance - resistance to concentrated changes
    consecutive_changes = 0
    max_consecutive = 0
    for i in range(1, len(diff_positions)):
        if diff_positions[i] == diff_positions[i-1] + 1:
            consecutive_changes += 1
            max_consecutive = max(max_consecutive, consecutive_changes)
        else:
            consecutive_changes = 0
    
    # Create visualization of bit differences
    diff_visual = []
    for i in range(min_len):
        if i % 32 == 0:
            diff_visual.append("|")
        if i in diff_positions:
            diff_visual.append("X")
        else:
            diff_visual.append("_")
    
    diff_visual = "".join(diff_visual)
    
    return {
        "bit_differences": diff_bits,
        "percentage_changed": diff_percentage * 100,
        "avalanche_quality": 1.0 - abs(0.5 - diff_percentage) * 2.0,
        "diff_positions": diff_positions,
        "byte_entropy": byte_entropy,
        "completeness": completeness,
        "max_consecutive_changes": max_consecutive,
        "visualization": diff_visual
    }

def calculate_avalanche_spectrum(hash_values: List[str]) -> Dict[str, Any]:
    """
    Calculate avalanche effect spectrum across multiple hash values.
    
    This analyzes how changes propagate across a set of related hashes,
    useful for visualizing how small input changes affect the entire hash.
    
    Args:
        hash_values: List of hex hash strings to compare
        
    Returns:
        Dictionary with spectrum analysis results
    """
    if len(hash_values) < 2:
        return {"error": "Need at least 2 hash values for spectrum analysis"}
    
    # Calculate pairwise avalanche scores
    pairs = []
    for i in range(len(hash_values) - 1):
        score = avalanche_score(hash_values[i], hash_values[i+1])
        pairs.append({
            "hash1": hash_values[i],
            "hash2": hash_values[i+1],
            "score": score
        })
    
    # Calculate overall avalanche consistency
    scores = [p["score"] for p in pairs]
    avg_score = sum(scores) / len(scores)
    variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
    
    return {
        "pairs": pairs,
        "average_avalanche": avg_score,
        "variance": variance,
        "consistency": 1.0 - math.sqrt(variance)
    } 