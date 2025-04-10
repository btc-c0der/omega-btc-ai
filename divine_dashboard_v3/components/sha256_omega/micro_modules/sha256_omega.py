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
from .avalanche_analyzer import analyze_avalanche
from .resonance_score import get_detailed_cosmic_alignments, get_resonance_score

def sha256_omega(
    message: Union[str, bytes], 
    bio_method: Literal["fibonacci", "phi", "schumann", "generic"] = "fibonacci",
    fibonacci_alignment: bool = True,
    include_diagnostics: bool = False,
    lunar_phase_alignment: Optional[float] = None,
    reference_message: Optional[Union[str, bytes]] = None
) -> Dict[str, Any]:
    """
    Enhanced SHA256 with bio-inspired transformations and optional diagnostics.
    
    Args:
        message: Input message to hash
        bio_method: Bio-padding method to use (fibonacci, phi, schumann, generic)
        fibonacci_alignment: Whether to apply Fibonacci transformation
        include_diagnostics: Include detailed diagnostics in result
        lunar_phase_alignment: Optional lunar phase (0-1) for cosmic alignment
        reference_message: Optional reference message for avalanche comparison
        
    Returns:
        Dictionary containing the hash and optional diagnostics
    """
    # Convert string to bytes if needed
    if isinstance(message, str):
        message_bytes = message.encode('utf-8')
    else:
        message_bytes = message
        
    # Apply bio-padding with specified method
    padded_bytes = bio_padder(message_bytes, method=bio_method)
    
    # Apply Fibonacci transformation if requested
    if fibonacci_alignment:
        transformed_bytes = fibonacci_transform(padded_bytes)
    else:
        transformed_bytes = padded_bytes
    
    # Calculate SHA256 hash
    hash_obj = hashlib.sha256(transformed_bytes)
    hash_hex = hash_obj.hexdigest()
    
    # Prepare result dictionary
    result = {
        "hash": hash_hex,
        "input_type": "string" if isinstance(message, str) else "bytes",
        "bio_method": bio_method,
        "fibonacci_alignment": fibonacci_alignment
    }
    
    # Include diagnostics if requested
    if include_diagnostics:
        # Add timing info
        result["timestamp"] = time.time()
        
        # Add avalanche effect analysis if reference provided
        if reference_message is not None:
            if isinstance(reference_message, str):
                ref_bytes = reference_message.encode('utf-8')
            else:
                ref_bytes = reference_message
                
            # Apply same transformations to reference message
            ref_padded = bio_padder(ref_bytes, method=bio_method)
            
            if fibonacci_alignment:
                ref_transformed = fibonacci_transform(ref_padded)
            else:
                ref_transformed = ref_padded
                
            # Calculate reference hash
            ref_hash = hashlib.sha256(ref_transformed).hexdigest()
            
            # Analyze avalanche effect
            avalanche_analysis = analyze_avalanche(hash_hex, ref_hash)
            result["avalanche_analysis"] = avalanche_analysis
        
        # Add cosmic alignment metrics - get_detailed_cosmic_alignments doesn't accept lunar_phase_alignment parameter
        cosmic_alignments = get_detailed_cosmic_alignments(hash_hex)
        result["cosmic_alignments"] = cosmic_alignments
        
        # Add overall resonance score
        result["resonance_score"] = get_resonance_score(hash_hex)
    
    return result 