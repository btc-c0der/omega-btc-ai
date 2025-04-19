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
Compression Function Module for SHA-356

Implements the core compression function for SHA-356 hash algorithm.
This is where the main transformation happens, extending SHA-256's
8 working variables to 12 (H0-H11) for the enhanced 356-bit output.
"""

from typing import List, Dict, Any, Tuple, Optional
import struct

# Helper functions
def rightrotate(n: int, rotations: int, bit_length: int = 32) -> int:
    """Right rotate a 32-bit integer by specified number of bits."""
    return ((n >> rotations) | (n << (bit_length - rotations))) & ((1 << bit_length) - 1)

def sha356_compress(block: bytes, state: List[int], round_constants: List[int], 
                   trace: bool = False) -> Tuple[List[int], Optional[Dict[str, Any]]]:
    """
    Perform the main compression function for SHA-356.
    
    Args:
        block: 64-byte block of data
        state: Current state (H0-H11)
        round_constants: List of 89 constants for each round
        trace: Whether to generate detailed trace info
        
    Returns:
        Tuple of (new state, optional trace information)
    """
    # Ensure we have 12 state variables (instead of 8 in SHA-256)
    assert len(state) == 12, "SHA-356 requires 12 state variables"
    
    # Ensure we have 89 round constants (instead of 64 in SHA-256)
    assert len(round_constants) == 89, "SHA-356 requires 89 round constants"
    
    # Break the block into 16 32-bit words
    words = list(struct.unpack('>16I', block))
    
    # Expand the message schedule to 89 words
    for i in range(16, 89):
        # Standard SHA-256 message expansion, modified for SHA-356
        w_2 = words[i-2]
        w_7 = words[i-7]  
        w_15 = words[i-15]
        w_16 = words[i-16]
        
        # Additional terms for SHA-356
        w_13 = words[i-13] if i >= 13 else words[i % 13]  # Fibonacci number
        w_21 = words[i-21] if i >= 21 else words[i % 16]  # Fibonacci number
        
        # Standard sigma functions, but with adjusted rotations
        s0 = rightrotate(w_15, 7) ^ rightrotate(w_15, 18) ^ (w_15 >> 3)
        s1 = rightrotate(w_2, 17) ^ rightrotate(w_2, 19) ^ (w_2 >> 10)
        
        # Additional sigma function for SHA-356
        s2 = rightrotate(w_21, 13) ^ rightrotate(w_21, 21) ^ (w_21 >> 8)
        
        # Combine all terms for SHA-356's enhanced diffusion
        word = (s0 + s1 + s2 + w_7 + w_13) & 0xFFFFFFFF
        words.append(word)
    
    # Initialize working variables to current state
    a, b, c, d, e, f, g, h, i, j, k, l = state
    
    # Create trace log if requested
    trace_log = {
        "rounds": [],
        "initial_state": [f"0x{x:08x}" for x in state],
        "final_state": None
    } if trace else None
    
    # Compression function main loop (89 rounds instead of 64)
    for round_idx in range(89):
        # SHA-256 compression function with extensions for SHA-356
        # Additional variables i, j, k, l complement a, b, c, d, e, f, g, h
        
        # SHA-356 introduces enhanced Ch and Maj functions that use more variables
        ch = (e & f) ^ (~e & g) ^ (h & i)  # Extended Ch function
        maj = (a & b) ^ (a & c) ^ (b & c) ^ (c & d)  # Extended Maj function
        
        # SHA-356 sigmoid functions with additional rotations
        s0 = rightrotate(a, 2) ^ rightrotate(a, 13) ^ rightrotate(a, 22)
        s1 = rightrotate(e, 6) ^ rightrotate(e, 11) ^ rightrotate(e, 25)
        
        # Additional sigmoid functions for SHA-356 (using new variables)
        s2 = rightrotate(i, 7) ^ rightrotate(i, 18) ^ rightrotate(i, 24)
        s3 = rightrotate(j, 17) ^ rightrotate(j, 19) ^ rightrotate(j, 28)
        
        # Calculate temporary values
        temp1 = (h + s1 + ch + round_constants[round_idx] + words[round_idx]) & 0xFFFFFFFF
        temp2 = (s0 + maj) & 0xFFFFFFFF
        temp3 = (s2 + s3) & 0xFFFFFFFF  # Additional temp value for SHA-356
        
        # Update working variables with SHA-356 enhancements
        # This rotation pattern creates a more complex diffusion
        l = k
        k = j
        j = i
        i = h + temp1
        h = g
        g = f
        f = e
        e = (d + temp1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (temp1 + temp2 + temp3) & 0xFFFFFFFF
        
        # Add round to trace if enabled
        if trace and trace_log is not None:
            trace_log["rounds"].append({
                "round": round_idx,
                "word": f"0x{words[round_idx]:08x}",
                "constant": f"0x{round_constants[round_idx]:08x}",
                "ch": f"0x{ch:08x}",
                "maj": f"0x{maj:08x}",
                "s0": f"0x{s0:08x}",
                "s1": f"0x{s1:08x}",
                "temp1": f"0x{temp1:08x}",
                "temp2": f"0x{temp2:08x}",
                "a-l": [f"0x{x:08x}" for x in [a, b, c, d, e, f, g, h, i, j, k, l]]
            })
    
    # Add to current state (same approach as SHA-256 but with 12 variables)
    state[0] = (state[0] + a) & 0xFFFFFFFF
    state[1] = (state[1] + b) & 0xFFFFFFFF
    state[2] = (state[2] + c) & 0xFFFFFFFF
    state[3] = (state[3] + d) & 0xFFFFFFFF
    state[4] = (state[4] + e) & 0xFFFFFFFF
    state[5] = (state[5] + f) & 0xFFFFFFFF
    state[6] = (state[6] + g) & 0xFFFFFFFF
    state[7] = (state[7] + h) & 0xFFFFFFFF
    state[8] = (state[8] + i) & 0xFFFFFFFF
    state[9] = (state[9] + j) & 0xFFFFFFFF
    state[10] = (state[10] + k) & 0xFFFFFFFF
    state[11] = (state[11] + l) & 0xFFFFFFFF
    
    # Add final state to trace
    if trace and trace_log is not None:
        trace_log["final_state"] = [f"0x{x:08x}" for x in state]
    
    return state, trace_log 