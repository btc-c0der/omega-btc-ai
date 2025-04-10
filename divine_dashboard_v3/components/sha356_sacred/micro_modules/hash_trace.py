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

# Flag to check if visualization libraries are available
VISUALIZATION_AVAILABLE = False

try:
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    from io import BytesIO
    VISUALIZATION_AVAILABLE = True
except ImportError:
    # Will use fallback implementations
    pass

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
        Bit influence score (0.0-1.0)
    """
    # This is a simplified model - a real analysis would involve differential cryptanalysis
    
    if not input_data or not output_hash:
        return 0.0
    
    # Create variations of the input by flipping single bits
    base_hash = output_hash
    influence_scores = []
    
    # Test a subset of bit flips (for efficiency)
    max_tests = min(len(input_data) * 8, 64)  # Limit to 64 tests
    test_positions = random.sample(range(len(input_data) * 8), max_tests)
    
    for bit_pos in test_positions:
        # Create copy of input data
        modified = bytearray(input_data)
        
        # Flip a single bit
        byte_pos = bit_pos // 8
        bit_offset = bit_pos % 8
        modified[byte_pos] ^= (1 << bit_offset)
        
        # Compute new hash
        modified_hash = hashlib.sha256(modified).digest()
        
        # Count differing bits
        diff_count = 0
        for i in range(min(len(base_hash), len(modified_hash))):
            xor_byte = base_hash[i] ^ modified_hash[i]
            # Count the set bits in xor_byte
            for j in range(8):
                if (xor_byte >> j) & 1:
                    diff_count += 1
        
        # Calculate influence as normalized difference
        total_bits = min(len(base_hash), len(modified_hash)) * 8
        influence = diff_count / total_bits if total_bits > 0 else 0
        influence_scores.append(influence)
    
    # Average influence score
    avg_influence = sum(influence_scores) / len(influence_scores) if influence_scores else 0
    
    # Normalize to 0-1 scale (optimal avalanche would be 0.5)
    normalized_influence = 1.0 - abs(avg_influence - 0.5) / 0.5
    
    return normalized_influence

def visualize_avalanche_effect(hash1: str, hash2: str) -> bytes:
    """
    Create a visualization of the avalanche effect between two hashes.
    
    Args:
        hash1: First hash (hex string)
        hash2: Second hash (hex string)
        
    Returns:
        PNG image data as bytes
    """
    # Get avalanche data
    avalanche_data = get_avalanche_data(hash1, hash2)
    
    if VISUALIZATION_AVAILABLE:
        # Create figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Convert to binary for bit-level comparison
        bin1 = bin(int(hash1, 16))[2:].zfill(len(hash1) * 4)
        bin2 = bin(int(hash2, 16))[2:].zfill(len(hash2) * 4)
        
        # Get differing bit positions
        diff_bits = avalanche_data["difference_positions"]
        
        # Create heat map data for 2D visualization (16x16 grid for 256 bits)
        heatmap_size = 16  # 16x16 = 256 bits
        heatmap = np.zeros((heatmap_size, heatmap_size))
        
        for bit in diff_bits:
            row, col = divmod(bit, heatmap_size)
            if row < heatmap_size and col < heatmap_size:
                heatmap[row, col] = 1
        
        # Plot heatmap
        im = ax.imshow(heatmap, cmap='viridis', interpolation='nearest')
        
        # Add title and labels
        ax.set_title(f'Bit Differences: {avalanche_data["different_bits"]} bits '
                     f'({avalanche_data["difference_percentage"]:.1f}%)')
        ax.set_xlabel('Bit Position % 16')
        ax.set_ylabel('Bit Position / 16')
        
        # Add colorbar
        plt.colorbar(im, ax=ax)
        
        # Export figure to PNG
        buf = BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format='png', dpi=100)
        plt.close(fig)
        
        buf.seek(0)
        return buf.getvalue()
    else:
        # Return an empty PNG if visualization libraries aren't available
        return b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII='

def generate_bit_flip_report(input_text: str) -> Dict[str, Any]:
    """
    Generate a report showing the avalanche effect by flipping individual bits.
    
    Args:
        input_text: Input text to analyze
        
    Returns:
        Dictionary with bit flip analysis results
    """
    # Convert text to bytes
    input_bytes = input_text.encode('utf-8')
    
    # Calculate original hash
    original_hash = hashlib.sha256(input_bytes).hexdigest()
    
    # Analyze bit flips
    bit_flip_results = []
    
    # Limit analysis to first 8 bytes (64 bits) to keep it manageable
    max_bytes = min(len(input_bytes), 8)
    
    for byte_pos in range(max_bytes):
        for bit_pos in range(8):
            # Create modified input with one bit flipped
            modified_bytes = bytearray(input_bytes)
            modified_bytes[byte_pos] ^= (1 << bit_pos)
            
            # Calculate modified hash
            modified_hash = hashlib.sha256(modified_bytes).hexdigest()
            
            # Get avalanche data
            avalanche_data = get_avalanche_data(original_hash, modified_hash)
            
            # Store result
            flipped_char = input_bytes[byte_pos]
            original_char = chr(flipped_char) if 32 <= flipped_char <= 126 else f"0x{flipped_char:02x}"
            modified_char = chr(modified_bytes[byte_pos]) if 32 <= modified_bytes[byte_pos] <= 126 else f"0x{modified_bytes[byte_pos]:02x}"
            
            bit_flip_results.append({
                "byte_position": byte_pos,
                "bit_position": bit_pos,
                "original_character": original_char,
                "modified_character": modified_char,
                "different_bits": avalanche_data["different_bits"],
                "difference_percentage": avalanche_data["difference_percentage"],
                "avalanche_quality": avalanche_data["avalanche_quality"]
            })
    
    # Calculate average avalanche quality
    avg_quality = sum(r["avalanche_quality"] for r in bit_flip_results) / len(bit_flip_results) if bit_flip_results else 0
    avg_diff_percent = sum(r["difference_percentage"] for r in bit_flip_results) / len(bit_flip_results) if bit_flip_results else 0
    
    return {
        "input_text": input_text,
        "original_hash": original_hash,
        "bit_flip_results": bit_flip_results,
        "average_avalanche_quality": avg_quality,
        "average_difference_percentage": avg_diff_percent,
        "ideal_difference_percentage": 50.0,
        "theoretical_max_avalanche_quality": 1.0
    } 