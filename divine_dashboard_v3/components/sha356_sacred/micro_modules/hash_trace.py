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
Hash Trace Module for SHA-356

Provides detailed tracing of the SHA-356 hashing process with entropy 
lineage mapping for enhanced understanding and visualization.
"""

from typing import Dict, List, Any, Optional, Tuple, Union
import time
import math
import json
import base64

def create_entropy_lineage(trace_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create an entropy lineage map from trace data.
    
    This visualizes how entropy flows through the SHA-356 algorithm,
    showing the cosmic patterns that emerge during the hashing process.
    
    Args:
        trace_data: Full trace data from the hashing process
        
    Returns:
        Entropy lineage mapping data
    """
    # Initialize lineage map
    lineage = {
        "name": "SHA-356 Entropy Map",
        "timestamp": time.time(),
        "metadata": {
            "algorithm": "SHA-356",
            "description": "Sacred Hash Algorithm with Bio-Crypto integration"
        },
        "input_entropy": {},
        "message_expansion": {},
        "compression_flow": {},
        "resonance_points": {},
        "output_signature": {}
    }
    
    # Extract input entropy information if available
    if "input" in trace_data:
        input_data = trace_data["input"]
        lineage["input_entropy"] = {
            "original_length": input_data.get("original_length", 0),
            "padded_length": input_data.get("padded_length", 0),
            "padding_method": input_data.get("padding_method", "unknown"),
            "blocks": input_data.get("block_count", 0)
        }
    
    # Extract message expansion flow if available
    if "message_expansion" in trace_data:
        expansion = trace_data["message_expansion"]
        # Map how words evolve through the schedule
        words_flow = []
        
        for step in expansion.get("expansion_steps", []):
            flow_point = {
                "index": step.get("index", 0),
                "dependencies": [
                    step.get("index", 0) - 16,
                    step.get("index", 0) - 2,
                    step.get("index", 0) - 21 if step.get("index", 0) >= 21 else None,
                    step.get("index", 0) - 7,
                    step.get("index", 0) - 13
                ],
                "sigma_entropy": step.get("s0", "0x0") + step.get("s1", "0x0") + step.get("s2", "0x0"),
                "resonance_applied": step.get("resonance_applied", False)
            }
            words_flow.append(flow_point)
            
        lineage["message_expansion"] = {
            "word_count": expansion.get("schedule_length", 89),
            "flow": words_flow,
            "resonance_points": expansion.get("resonance_points", [])
        }
    
    # Extract compression flow if available
    if "compression" in trace_data:
        compression = trace_data["compression"]
        
        # Track how variables evolve through rounds
        var_evolution = []
        for round_data in compression.get("rounds", []):
            var_evolution.append({
                "round": round_data.get("round", 0),
                "ch_entropy": round_data.get("ch", "0x0"),
                "maj_entropy": round_data.get("maj", "0x0"),
                "sigma_entropy": round_data.get("s0", "0x0") + round_data.get("s1", "0x0"),
                "variable_state": round_data.get("a-l", [])
            })
            
        lineage["compression_flow"] = {
            "round_count": len(compression.get("rounds", [])),
            "variable_evolution": var_evolution,
            "initial_state": compression.get("initial_state", []),
            "final_state": compression.get("final_state", [])
        }
    
    # Extract resonance information if available
    if "resonance" in trace_data:
        resonance = trace_data["resonance"]
        
        lineage["resonance_points"] = {
            "lunar_phase": resonance.get("lunar_phase", 0),
            "schumann_resonance": resonance.get("schumann_resonance", 0),
            "solar_activity": resonance.get("solar_activity", 0),
            "resonance_score": resonance.get("resonance_score", 0),
            "cosmic_alignment": resonance.get("cosmic_alignment", "Unknown"),
            "modulation_points": resonance.get("modulation_values", {})
        }
    
    # Extract output signature if available
    if "output" in trace_data:
        output = trace_data["output"]
        
        lineage["output_signature"] = {
            "hash": output.get("hash", ""),
            "length_bits": output.get("length_bits", 356),
            "entropy_density": output.get("entropy_density", 0),
            "processing_time": output.get("processing_time_ms", 0)
        }
    
    return lineage

def trace_to_json(trace_data: Dict[str, Any], pretty: bool = True) -> str:
    """
    Convert trace data to JSON string.
    
    Args:
        trace_data: Trace data dictionary
        pretty: Whether to format with indentation
        
    Returns:
        JSON string representation
    """
    if pretty:
        return json.dumps(trace_data, indent=2)
    return json.dumps(trace_data)

def generate_entropy_visualization(trace_data: Dict[str, Any]) -> str:
    """
    Generate an ASCII visualization of the entropy flow.
    
    Args:
        trace_data: Trace data from the hashing process
        
    Returns:
        ASCII art visualization
    """
    # This is a simple representation - in a full implementation
    # this would generate a more complex visualization
    
    # Create header
    viz = ["╔═══════════════════════════════════════════════╗"]
    viz.append("║  SHA-356 ENTROPY LINEAGE VISUALIZATION     ║")
    viz.append("╠═══════════════════════════════════════════════╣")
    
    # Add input representation
    if "input" in trace_data:
        input_data = trace_data["input"]
        viz.append("║  Input:                                    ║")
        viz.append(f"║  - Length: {input_data.get('original_length', 0)} bytes{' ' * 26}║")
        viz.append(f"║  - Padding: {input_data.get('padding_method', 'unknown')}{' ' * (32 - len(input_data.get('padding_method', 'unknown')))}║")
    
    # Add resonance info
    if "resonance" in trace_data:
        resonance = trace_data["resonance"]
        viz.append("║                                           ║")
        viz.append("║  Cosmic Alignment:                        ║")
        viz.append(f"║  - Score: {resonance.get('resonance_score', 0):.3f}{' ' * 26}║")
        viz.append(f"║  - Level: {resonance.get('cosmic_alignment', 'Unknown')}{' ' * (32 - len(resonance.get('cosmic_alignment', 'Unknown')))}║")
    
    # Add processing visualization
    viz.append("║                                           ║")
    viz.append("║  Entropy Flow:                            ║")
    viz.append("║  Input → Bio-Pad → Message Schedule →     ║")
    viz.append("║  → Compression (89 rounds) → Resonance →  ║") 
    viz.append("║  → Final Hash (356 bits)                  ║")
    
    # Add output
    if "output" in trace_data:
        output = trace_data["output"]
        viz.append("║                                           ║")
        viz.append("║  Output Signature:                        ║")
        viz.append(f"║  - Processing: {output.get('processing_time_ms', 0)} ms{' ' * 21}║")
    
    # Close box
    viz.append("╚═══════════════════════════════════════════════╝")
    
    return "\n".join(viz)

def get_avalanche_data(hash1: str, hash2: str) -> Dict[str, Any]:
    """
    Analyze the avalanche effect between two hashes.
    
    Args:
        hash1: First hash
        hash2: Second hash
        
    Returns:
        Avalanche analysis data
    """
    # Helper function to convert hex to binary
    def hex_to_binary(hex_str):
        return bin(int(hex_str, 16))[2:].zfill(len(hex_str) * 4)
    
    # Convert hashes to binary
    bin1 = hex_to_binary(hash1)
    bin2 = hex_to_binary(hash2)
    
    # Count differing bits
    diff_bits = sum(b1 != b2 for b1, b2 in zip(bin1, bin2))
    total_bits = len(bin1)
    
    # Calculate avalanche score (percentage of bits that differ)
    avalanche_score = diff_bits / total_bits
    
    # Create full analysis
    analysis = {
        "hash1": hash1,
        "hash2": hash2,
        "total_bits": total_bits,
        "differing_bits": diff_bits,
        "avalanche_score": avalanche_score,
        "avalanche_percentage": f"{avalanche_score * 100:.2f}%",
        "ideal_score": 0.45 <= avalanche_score <= 0.55,
        "bit_pattern": [int(b1 != b2) for b1, b2 in zip(bin1, bin2)]
    }
    
    # Determine quality assessment
    if 0.45 <= avalanche_score <= 0.55:
        analysis["quality"] = "Ideal"
    elif 0.4 <= avalanche_score <= 0.6:
        analysis["quality"] = "Good"
    elif 0.3 <= avalanche_score <= 0.7:
        analysis["quality"] = "Acceptable"
    else:
        analysis["quality"] = "Poor"
    
    return analysis 