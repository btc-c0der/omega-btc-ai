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
SHA256 Omega Module

Enhanced SHA256 function with bio-inspired transformations and partial avalanche control.
"""

import hashlib
import time
from typing import Dict, Any, Optional, Union, Literal

from .bio_padder import bio_padder
from .fibonacci_transform import fibonacci_transform

def sha256_omega(
    data: Union[bytes, str], 
    bio: bool = True, 
    padding_method: Literal["fibonacci", "schumann", "generic"] = "fibonacci",
    fibonacci_seed: Optional[int] = None,
    rounds: Optional[int] = None
) -> Dict[str, Any]:
    """
    Enhanced SHA256 function with bio-inspired transformations.
    
    Args:
        data: Input data as bytes or string
        bio: Whether to apply bio transformations
        padding_method: Method for bio-padding
        fibonacci_seed: Optional seed for fibonacci transform
        rounds: Optional override for hash rounds
        
    Returns:
        Dictionary with hash results and metadata
    """
    # Convert string to bytes if needed
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # Store original data for reference
    original_data = data
    
    # Record start time for metrics
    start_time = time.time()
    
    # Apply bio transformations if requested
    if bio:
        data = bio_padder(data, method=padding_method)
        data = fibonacci_transform(data, seed=fibonacci_seed)
    
    # Compute standard SHA256 hash
    full_hash = hashlib.sha256(data).hexdigest()
    
    # Record end time
    end_time = time.time()
    
    # Create result dictionary with rich metadata
    result = {
        "input_length": len(original_data),
        "transformed_length": len(data),
        "hash": full_hash,
        "processing_time_ms": round((end_time - start_time) * 1000, 2),
        "bio_transform": {
            "applied": bio,
            "padding_method": padding_method if bio else None,
            "fibonacci_seed": fibonacci_seed if bio else None
        },
        "note": "Bio + Fibonacci aligned" if bio else "Raw SHA-256"
    }
    
    # Add optional diagnostic info
    if bio:
        # Show first and last 8 bytes of transformed data as hex
        result["transformed_data_snippet"] = {
            "prefix": data[:8].hex(),
            "suffix": data[-8:].hex()
        }
    
    return result 