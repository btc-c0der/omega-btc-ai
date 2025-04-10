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
Hash Trace Module

Provides functions for tracing and visualizing the hash computation process.
This module helps understand the entropy flow and avalanche effect in SHA356.
"""

import random
import binascii
import hashlib
from typing import List, Dict, Any, Tuple, Optional

def create_entropy_lineage(input_data: bytes, output_hash: bytes) -> Dict[str, Any]:
    """
    Create an entropy lineage visualization of how input becomes output.
    
    Args:
        input_data: Original input bytes
        output_hash: Final hash bytes
        
    Returns:
        Dictionary with entropy lineage visualization data
    """
    # Visualize entropy distribution in input
    input_entropy = analyze_entropy_distribution(input_data)
    
    # Visualize entropy in output hash
    output_entropy = analyze_entropy_distribution(output_hash)
    
    # Visualize entropy transfer
    stages = [
        {"name": "Input", "entropy": input_entropy},
        {"name": "Internal State", "entropy": simulate_internal_state(input_data, output_hash)},
        {"name": "Output", "entropy": output_entropy}
    ]
    
    return {
        "stages": stages,
        "lineage_summary": {
            "entropy_amplification": output_entropy["normalized"] / max(0.001, input_entropy["normalized"]),
            "distribution_quality": output_entropy["evenness"],
            "bit_influence": calculate_bit_influence(input_data, output_hash)
        }
    }

def generate_entropy_visualization(hash_bytes: bytes) -> Dict[str, Any]:
    """
    Generate a visual representation of entropy in a hash.
    
    Args:
        hash_bytes: Hash bytes to visualize
        
    Returns:
        Dictionary with entropy visualization data
    """
    # Bit pattern analysis
    bit_patterns = []
    for i in range(len(hash_bytes)):
        byte = hash_bytes[i]
        bit_pattern = [(byte >> j) & 1 for j in range(7, -1, -1)]
        bit_patterns.append({
            "byte_index": i,
            "binary": "".join(["1" if b else "0" for b in bit_pattern]),
            "hex": f"{byte:02x}",
            "value": byte
        })
    
    # Create visual representation
    visual = []
    for i, byte in enumerate(hash_bytes):
        # Convert byte to grayscale value (0-255)
        visual.append({
            "position": i,
            "value": byte,
            "intensity": byte / 255.0
        })
    
    # Calculate entropy statistics
    stats = analyze_entropy_distribution(hash_bytes)
    
    return {
        "bit_patterns": bit_patterns,
        "visual_representation": visual,
        "entropy_stats": stats
    }

def get_avalanche_data(hash1: str, hash2: str) -> Dict[str, Any]:
    """
    Analyze the avalanche effect between two hashes.
    
    Args:
        hash1: First hash (hex string)
        hash2: Second hash (hex string)
        
    Returns:
        Dictionary with avalanche effect analysis
    """
    # Convert hex strings to binary
    bin1 = bin(int(hash1, 16))[2:].zfill(len(hash1) * 4)
    bin2 = bin(int(hash2, 16))[2:].zfill(len(hash2) * 4)
    
    # Collect differing bit positions
    diff_positions = []
    for i in range(min(len(bin1), len(bin2))):
        if bin1[i] != bin2[i]:
            diff_positions.append(i)
    
    # Calculate statistics
    total_bits = min(len(bin1), len(bin2))
    diff_count = len(diff_positions)
    diff_percentage = diff_count / total_bits if total_bits > 0 else 0
    
    # Create bit change visualization
    visual = []
    block_size = 8  # Group bits into 8-bit blocks for visualization
    for i in range(0, total_bits, block_size):
        block_end = min(i + block_size, total_bits)
        block_diff_count = sum(1 for pos in diff_positions if i <= pos < block_end)
        block_diff_percent = block_diff_count / (block_end - i)
        
        visual.append({
            "block_index": i // block_size,
            "bit_range": [i, block_end-1],
            "diff_count": block_diff_count,
            "diff_percent": block_diff_percent
        })
    
    # Calculate avalanche quality (how close to 50% difference)
    ideal_diff = 0.5
    avalanche_quality = 1.0 - abs(diff_percentage - ideal_diff) / ideal_diff
    
    return {
        "total_bits": total_bits,
        "different_bits": diff_count,
        "difference_percentage": diff_percentage * 100,
        "difference_positions": diff_positions[:100],  # Limit to first 100 positions
        "visualization": visual,
        "avalanche_quality": avalanche_quality
    }

def analyze_entropy_distribution(data: bytes) -> Dict[str, float]:
    """
    Analyze the entropy distribution in a byte sequence.
    
    Args:
        data: Bytes to analyze
        
    Returns:
        Dictionary with entropy statistics
    """
    if not data:
        return {
            "shannon_entropy": 0.0,
            "normalized": 0.0,
            "evenness": 0.0,
            "bit_balance": 0.0
        }
    
    # Count byte frequencies
    freq = {}
    for byte in data:
        freq[byte] = freq.get(byte, 0) + 1
    
    # Calculate Shannon entropy
    shannon = 0.0
    for count in freq.values():
        p = count / len(data)
        shannon -= p * (256 / 255) * (p * 8)  # 8 bits per byte
    
    # Calculate bit balance (0s vs 1s across all bits)
    ones = 0
    total_bits = len(data) * 8
    for byte in data:
        for i in range(8):
            if (byte >> i) & 1:
                ones += 1
    
    bit_balance = ones / total_bits if total_bits > 0 else 0.5
    bit_balance_quality = 1.0 - abs(bit_balance - 0.5) / 0.5
    
    # Calculate value distribution evenness
    max_evenness = 8.0 if len(data) >= 256 else min(8.0, 256 / len(data))
    normalized_entropy = shannon / max_evenness
    
    # Calculate evenness of distribution
    max_count = max(freq.values())
    min_count = min(freq.values()) if freq else 0
    range_quality = 1.0 - (max_count - min_count) / len(data) if len(data) > 0 else 0.0
    
    return {
        "shannon_entropy": shannon,
        "normalized": normalized_entropy,
        "evenness": range_quality,
        "bit_balance": bit_balance_quality
    }

def simulate_internal_state(input_data: bytes, output_hash: bytes) -> Dict[str, float]:
    """
    Simulate internal state entropy (for visualization purposes).
    
    Args:
        input_data: Input bytes
        output_hash: Output hash bytes
        
    Returns:
        Dictionary with internal state entropy statistics
    """
    # Create a plausible internal state representation by combining input and output
    # This is for visualization only - not actual internal state
    blend_factor = 0.7  # Weight towards output hash
    
    # Create a blend of input and output
    internal_bytes = bytearray()
    max_len = max(len(input_data), len(output_hash))
    
    for i in range(max_len):
        input_byte = input_data[i % len(input_data)] if input_data else 0
        output_byte = output_hash[i % len(output_hash)] if output_hash else 0
        
        # Blend input and output bytes
        blended = int(input_byte * (1 - blend_factor) + output_byte * blend_factor)
        internal_bytes.append(blended & 0xFF)
    
    # Add some entropy from internal operations
    for i in range(len(internal_bytes)):
        if random.random() < 0.2:  # Randomly modify 20% of bytes
            internal_bytes[i] = (internal_bytes[i] + hash(bytes(internal_bytes[:i+1])) % 256) & 0xFF
    
    # Analyze entropy of simulated internal state
    return analyze_entropy_distribution(bytes(internal_bytes))

def calculate_bit_influence(input_data: bytes, output_hash: bytes) -> float:
    """
    Calculate how much each input bit influences output bits.
    
    Args:
        input_data: Input bytes
        output_hash: Output hash bytes
        
    Returns:
        Bit influence score between 0.0 and 1.0
    """
    # For estimation only - full calculation would be very complex
    # Higher score means input bits have more balanced influence on output
    
    # Calculate a simple input-output correlation
    h = hashlib.sha256(input_data).digest()
    
    # Compare to actual output to estimate influence balance
    differences = sum(1 for a, b in zip(h, output_hash) if a != b)
    difference_ratio = differences / max(1, min(len(h), len(output_hash)))
    
    # More differences = better influence distribution
    return min(1.0, difference_ratio * 2) 