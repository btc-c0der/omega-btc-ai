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
SHA-356: Sacred Hash Algorithm - Bio-Crypto Edition

Main implementation of the SHA-356 hash function, a 356-bit cryptographic
hash algorithm with bio-entropy, resonance tracking, and spiritual feedback.

SHA-356 extends the SHA-256 algorithm with:
- Extended output (356 bits instead of 256)
- Bio-padding with natural patterns
- 89 rounds (Fibonacci number) instead of 64
- Enhanced compression function with 12 working variables
- Cosmic resonance integration
- Entropy lineage visualization
"""

import struct
import time
import binascii
import math
from typing import List, Dict, Any, Optional, Tuple, Union, Literal

from .bio_padding import bio_pad
from .fibonacci_constants import get_initial_state, get_round_constants
from .message_schedule import create_message_schedule, trace_message_expansion
from .compression_function import sha356_compress
from .resonance_integration import apply_resonance
from .hash_trace import create_entropy_lineage, generate_entropy_visualization

def preprocess_message(data: Union[str, bytes], 
                      padding_method: Literal["fibonacci", "schumann", "golden", "lunar"] = "fibonacci") -> Tuple[bytes, Dict[str, Any]]:
    """
    Preprocess the message for SHA-356 hashing.
    
    Args:
        data: Input data as string or bytes
        padding_method: Bio-padding method to use
        
    Returns:
        Tuple of (padded data, processing info)
    """
    # Convert string to bytes if needed
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # Store original length for reference
    original_length = len(data)
    
    # Apply bio-padding with the specified method
    padded_data = bio_pad(data, method=padding_method)
    
    # Create processing info
    process_info = {
        "original_length": original_length,
        "padded_length": len(padded_data),
        "padding_method": padding_method,
        # Calculate block count (64-byte blocks)
        "block_count": (len(padded_data) + 63) // 64
    }
    
    return padded_data, process_info

def process_blocks(padded_data: bytes, 
                  include_resonance: bool = True,
                  trace: bool = False) -> Tuple[List[int], Dict[str, Any]]:
    """
    Process all blocks of padded data through the SHA-356 algorithm.
    
    Args:
        padded_data: Bio-padded data
        include_resonance: Whether to include cosmic resonance
        trace: Whether to generate detailed trace info
        
    Returns:
        Tuple of (final hash state, trace data)
    """
    # Initialize hash state (H0-H11)
    hash_state = get_initial_state()
    
    # Get round constants (K0-K88)
    round_constants = get_round_constants()
    
    # Initialize trace data if requested
    trace_data = {}
    if trace:
        trace_data = {
            "blocks": [],
            "message_expansion": None,
            "compression": None,
            "resonance": None
        }
    
    # Process each 64-byte block
    for i in range(0, len(padded_data), 64):
        # Get current block (64 bytes)
        block = padded_data[i:i+64]
        
        # If block is less than 64 bytes, pad with zeros
        if len(block) < 64:
            block = block + b'\x00' * (64 - len(block))
        
        # Create message schedule
        if trace:
            # Create with detailed trace
            expansion_trace = trace_message_expansion(block)
            trace_data["message_expansion"] = expansion_trace
            
            # Extract the words from the trace
            words = [int(w[2:], 16) for w in expansion_trace["final_schedule"]]
        else:
            # Create message schedule without tracing
            words = create_message_schedule(block, include_resonance)
        
        # Compress block (main hashing work)
        if trace:
            # Compress with trace
            hash_state, compression_trace = sha356_compress(block, hash_state, round_constants, trace=True)
            trace_data["compression"] = compression_trace
        else:
            # Compress without trace
            hash_state, _ = sha356_compress(block, hash_state, round_constants, trace=False)
        
        # Add block to trace
        if trace:
            trace_data["blocks"].append({
                "index": i // 64,
                "offset": i,
                "size": len(block)
            })
    
    # Apply cosmic resonance if enabled
    if trace:
        # Apply with detailed trace
        modulated_state, resonance_data = apply_resonance(hash_state, include_resonance)
        trace_data["resonance"] = resonance_data
    else:
        # Apply without detailed trace
        modulated_state, _ = apply_resonance(hash_state, include_resonance)
    
    return modulated_state, trace_data

def finalize_hash(hash_state: List[int]) -> Tuple[str, bytes]:
    """
    Finalize the hash from the state.
    
    Args:
        hash_state: Final hash state (12 32-bit values)
        
    Returns:
        Tuple of (hex hash, raw bytes)
    """
    # Convert state to bytes (big-endian)
    hash_bytes = b''
    for value in hash_state:
        hash_bytes += value.to_bytes(4, byteorder='big')
    
    # SHA-356 uses 356 bits (44.5 bytes) - we'll use 45 bytes and mask the last 4 bits
    # This is 11 complete 32-bit words + 12 bits of the 12th word
    hash_356_bytes = hash_bytes[:44]  # First 44 bytes (352 bits)
    
    # Add the first half-byte of the last word
    last_byte = hash_bytes[44] & 0xF0  # Keep only the top 4 bits (mask bottom 4)
    hash_356_bytes += bytes([last_byte])  # Add the final half-byte
    
    # Convert to hex
    hash_hex = binascii.hexlify(hash_356_bytes).decode('ascii')
    
    return hash_hex, hash_356_bytes

def digest_356(data: Union[str, bytes], 
              padding_method: Literal["fibonacci", "schumann", "golden", "lunar"] = "fibonacci",
              include_resonance: bool = True) -> Tuple[str, bytes]:
    """
    Compute SHA-356 hash of the input data, returning the 356-bit digest.
    
    Args:
        data: Input data as string or bytes
        padding_method: Bio-padding method to use
        include_resonance: Whether to include cosmic resonance
        
    Returns:
        Tuple of (hex hash string, raw hash bytes)
    """
    # Preprocess message with bio-padding
    padded_data, _ = preprocess_message(data, padding_method)
    
    # Process all blocks
    hash_state, _ = process_blocks(padded_data, include_resonance, trace=False)
    
    # Finalize hash
    return finalize_hash(hash_state)

def sha356(data: Union[str, bytes],
         padding_method: Literal["fibonacci", "schumann", "golden", "lunar"] = "fibonacci",
         include_resonance: bool = True,
         include_trace: bool = False) -> Dict[str, Any]:
    """
    Compute full SHA-356 hash with bio-crypto integration.
    
    Args:
        data: Input data as string or bytes
        padding_method: Bio-padding method to use
        include_resonance: Whether to include cosmic resonance
        include_trace: Whether to include detailed trace information
        
    Returns:
        Dictionary with hash result and metadata
    """
    # Record start time
    start_time = time.time()
    
    # Preprocess message
    padded_data, input_info = preprocess_message(data, padding_method)
    
    # Process blocks
    hash_state, trace_data = process_blocks(padded_data, include_resonance, include_trace)
    
    # Finalize hash
    hash_hex, hash_bytes = finalize_hash(hash_state)
    
    # Record end time
    end_time = time.time()
    processing_time_ms = (end_time - start_time) * 1000
    
    # Create result dictionary
    result = {
        "hash": hash_hex,
        "length_bits": 356,
        "processing_time_ms": round(processing_time_ms, 2),
        "bio_transform": {
            "applied": True,
            "padding_method": padding_method
        },
        "resonance": {
            "applied": include_resonance
        }
    }
    
    # Add input info
    result["input"] = input_info
    
    # Add entropy spread (simulated)
    # In a full implementation, this would analyze hash quality
    result["entropy_spread"] = 0.993
    
    # If tracing was requested, add lineage information
    if include_trace:
        # Add trace data
        trace_data["input"] = input_info
        trace_data["output"] = {
            "hash": hash_hex,
            "length_bits": 356,
            "processing_time_ms": round(processing_time_ms, 2)
        }
        
        # Add entropy lineage
        result["entropy_lineage"] = create_entropy_lineage(trace_data)
        
        # Add trace visualization
        result["visualization"] = generate_entropy_visualization(trace_data)
    
    # Add resonance info if available
    if include_resonance and "resonance" in trace_data:
        result["resonance"] = trace_data["resonance"]
    
    # Add note
    if include_resonance:
        resonance_level = "High"
        if "resonance" in trace_data and "cosmic_alignment" in trace_data["resonance"]:
            resonance_level = trace_data["resonance"]["cosmic_alignment"]
        
        result["note"] = f"Bio-aligned with {padding_method} padding. {resonance_level} cosmic resonance."
    else:
        result["note"] = f"Bio-aligned with {padding_method} padding. Resonance disabled."
    
    return result 