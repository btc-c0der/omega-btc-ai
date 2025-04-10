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
Sacred Hash Module

Implements the SHA356 Sacred hash function with bio-dimensional transformations.
This provides enhanced cryptographic properties aligned with natural patterns.
"""

import hashlib
import json
from typing import Dict, Any, Optional, Union, Tuple
from .sacred_padder import apply_sacred_padding
from .dimensional_transform import dimensional_transform

def sacred_hash(
    message: Union[str, bytes],
    padding_method: str = "phi",
    transform_type: str = "fibonacci",
    transform_strength: float = 0.5,
    include_diagnostics: bool = False
) -> Union[str, Tuple[str, Dict[str, Any]]]:
    """
    Generate a SHA356 Sacred hash with bio-dimensional transformations.
    
    Args:
        message: Input message to hash (string or bytes)
        padding_method: Method for sacred padding ('phi', 'cosmic', 'harmonic')
        transform_type: Type of dimensional transform ('fibonacci', 'phi', 'hyperdimensional')
        transform_strength: Strength of the dimensional transform (0.0-1.0)
        include_diagnostics: Whether to include diagnostic information
        
    Returns:
        Hexadecimal hash string if include_diagnostics is False,
        or a tuple of (hash_string, diagnostics_dict) if include_diagnostics is True
    """
    # Convert string to bytes if needed
    if isinstance(message, str):
        message_bytes = message.encode('utf-8')
    else:
        message_bytes = message
    
    # Apply sacred padding
    padded_bytes = apply_sacred_padding(message_bytes, method=padding_method)
    
    # Apply dimensional transform
    transformed_bytes = dimensional_transform(
        padded_bytes, 
        transform_type=transform_type,
        strength=transform_strength
    )
    
    # Apply two rounds of SHA-256 (inspired by SHA-512 structure but with 356-bit output)
    first_hash = hashlib.sha256(transformed_bytes).digest()
    second_hash = hashlib.sha256(first_hash).digest()
    
    # Truncate to 356 bits (44.5 bytes, rounded to 45)
    final_hash = second_hash[:45]
    
    # Convert to hex string
    hash_hex = final_hash.hex()
    
    if include_diagnostics:
        diagnostics = {
            "original_length": len(message_bytes),
            "padded_length": len(padded_bytes),
            "padding_method": padding_method,
            "transform_type": transform_type,
            "transform_strength": transform_strength,
            "hash_bit_length": len(hash_hex) * 4,  # Each hex character is 4 bits
        }
        return hash_hex, diagnostics
    
    return hash_hex

def compare_sacred_hashes(hash1: str, hash2: str) -> float:
    """
    Compare two SHA356 Sacred hashes and return similarity score.
    
    Args:
        hash1: First hash string
        hash2: Second hash string
        
    Returns:
        Similarity score between 0.0 (completely different) and 1.0 (identical)
    """
    # Convert hex strings to binary
    binary1 = bin(int(hash1, 16))[2:].zfill(len(hash1) * 4)
    binary2 = bin(int(hash2, 16))[2:].zfill(len(hash2) * 4)
    
    # Count matching bits
    min_len = min(len(binary1), len(binary2))
    matches = sum(b1 == b2 for b1, b2 in zip(binary1[:min_len], binary2[:min_len]))
    
    # Calculate similarity as percentage of matching bits
    similarity = matches / min_len
    
    return similarity 