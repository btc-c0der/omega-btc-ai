#!/usr/bin/env python3
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
SHA356 Sacred Dashboard

Gradio interface for the SHA356 Sacred cryptographic system with dimensional alignments.
This module provides a way to visualize and explore the cosmic alignment of hashes,
offering insights into their quantum entanglements and sacred patterns.
"""

import json
import math
import time
from typing import Dict, Any, List, Tuple, Optional, Literal, Union
import base64
from datetime import datetime
import os

try:
    import gradio as gr
except ImportError:
    raise ImportError("Please install gradio with: pip install gradio>=3.23.0")

try:
    import numpy as np
except ImportError:
    raise ImportError("Please install numpy with: pip install numpy>=1.20.0")

try:
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
except ImportError:
    raise ImportError("Please install matplotlib with: pip install matplotlib>=3.5.0")

# Local imports
from .micro_modules.dimensional_transform import dimensional_transform
from .micro_modules.sacred_hash import sacred_hash
from .micro_modules.sacred_padder import sacred_padder
from .micro_modules.dimensional_analyzer import analyze_dimensions
from .micro_modules.sacred_resonance import get_sacred_resonance, get_detailed_alignments

# Constants
THEME = gr.themes.Glass(
    primary_hue="indigo",
    secondary_hue="purple",
    neutral_hue="slate",
)

# Helper functions
def format_json(data: Dict[str, Any]) -> str:
    """Format JSON data with indentation for display."""
    return json.dumps(data, indent=2)

def create_dimensional_plot(hash_values: List[str], labels: List[str]) -> Figure:
    """
    Create a dimensional mapping visualization of hash values.
    
    Args:
        hash_values: List of hex hash values
        labels: Labels for each hash
        
    Returns:
        Matplotlib Figure
    """
    # Convert the first 8 bytes of each hash to degrees (0-360)
    angles = []
    for h in hash_values:
        # Take first 8 bytes (16 hex chars)
        hex_chars = h[:16]
        # Convert to int and scale to 0-360
        angle = int(hex_chars, 16) % 360
        angles.append(angle)
    
    # Create a polar plot
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    
    # Plot each hash as a point on the circle
    for i, (angle, label) in enumerate(zip(angles, labels)):
        # Convert angle to radians
        angle_rad = math.radians(angle)
        # Plot the point
        ax.scatter(angle_rad, 1, s=100, label=label)
        # Add a line from center to point
        ax.plot([0, angle_rad], [0, 1], linewidth=2)
    
    # Configure the plot
    ax.set_rticks([])  # No radial ticks
    # Set the angular grid lines at 45-degree intervals
    theta_ticks = [0, 45, 90, 135, 180, 225, 270, 315]
    ax.set_xticks([math.radians(x) for x in theta_ticks])
    ax.set_xticklabels([f"{x}°" for x in theta_ticks])
    
    ax.set_title("Dimensional Alignment", pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.4, 1.0))
    
    return fig

def create_alignment_radar(alignment_data: Dict[str, Any]) -> Figure:
    """
    Create a radar chart for cosmic alignment metrics.
    
    Args:
        alignment_data: Dictionary with alignment metrics
        
    Returns:
        Matplotlib Figure
    """
    # Extract alignment categories and values
    categories = list(alignment_data.keys())
    values = list(alignment_data.values())
    
    # Compute the angles for each category
    N = len(categories)
    angles = [n / float(N) * 2 * math.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Values need to be normalized between 0 and 1
    normalized_values = [v / 100.0 for v in values]
    normalized_values += normalized_values[:1]  # Close the loop
    
    # Create the plot
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, polar=True)
    
    # Plot the values
    ax.plot(angles, normalized_values, linewidth=2, linestyle='solid')
    ax.fill(angles, normalized_values, alpha=0.25)
    
    # Set the angle labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    
    # Set y-axis labels (scale from 0 to 100%)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'])
    
    # Set title
    ax.set_title("Cosmic Alignment", pad=20)
    
    return fig

# Main functions for the dashboard
def hash_message(message: str, padding_method: Literal["fibonacci", "phi", "schumann", "lunar", "sacred"] = "sacred") -> Dict[str, Any]:
    """
    Generate a SHA356 Sacred hash with dimensional analysis.
    
    Args:
        message: Input message to hash
        padding_method: Method for bio-padding the input
        
    Returns:
        Dictionary with hash result and dimensional analysis
    """
    # Apply sacred padding
    padded_data = sacred_padder(message.encode(), method=padding_method)
    
    # Generate sacred hash
    hash_result = sacred_hash(padded_data)
    
    # Apply dimensional transform
    transformed_hash = dimensional_transform(hash_result)
    
    # Get dimensional analysis
    dimensions = analyze_dimensions(transformed_hash)
    
    # Get sacred resonance score
    resonance = get_sacred_resonance(transformed_hash)
    
    # Format the result
    return {
        "original_message": message,
        "padding_method": padding_method,
        "hash_value": transformed_hash,
        "dimensions": dimensions,
        "resonance_score": resonance,
        "timestamp": time.time()
    }

def compare_hashes(message1: str, message2: str, padding_method: Literal["fibonacci", "phi", "schumann", "lunar", "sacred"] = "sacred") -> Dict[str, Any]:
    """
    Compare two messages and analyze their dimensional and sacred differences.
    
    Args:
        message1: First input message
        message2: Second input message
        padding_method: Method for bio-padding the inputs
        
    Returns:
        Dictionary with comparison results
    """
    # Generate hashes for both messages
    hash1_result = hash_message(message1, padding_method)
    hash2_result = hash_message(message2, padding_method)
    
    # Extract hash values
    hash1 = hash1_result["hash_value"]
    hash2 = hash2_result["hash_value"]
    
    # Analyze dimensional differences
    dimension_diff = {}
    for dim in hash1_result["dimensions"]:
        if dim in hash2_result["dimensions"]:
            dimension_diff[dim] = abs(
                hash1_result["dimensions"][dim] - 
                hash2_result["dimensions"][dim]
            )
    
    # Calculate bit difference
    binary1 = bin(int(hash1, 16))[2:].zfill(len(hash1) * 4)
    binary2 = bin(int(hash2, 16))[2:].zfill(len(hash2) * 4)
    bit_diff_count = sum(b1 != b2 for b1, b2 in zip(binary1, binary2))
    bit_diff_percentage = (bit_diff_count / len(binary1)) * 100
    
    # Get the visualization figure
    hash_fig = create_dimensional_plot(
        [hash1, hash2], 
        [f"Hash 1: {message1[:20]}" if len(message1) > 20 else f"Hash 1: {message1}", 
         f"Hash 2: {message2[:20]}" if len(message2) > 20 else f"Hash 2: {message2}"]
    )
    
    # Convert figure to image
    img_bytes = fig_to_image(hash_fig)
    
    return {
        "hash1": hash1,
        "hash2": hash2,
        "dimensional_difference": dimension_diff,
        "bit_difference_count": bit_diff_count,
        "bit_difference_percentage": bit_diff_percentage,
        "visualization": img_bytes,
        "resonance1": hash1_result["resonance_score"],
        "resonance2": hash2_result["resonance_score"],
        "resonance_delta": abs(hash1_result["resonance_score"] - hash2_result["resonance_score"])
    }

def get_cosmic_alignment(hash_value: str) -> Dict[str, Any]:
    """
    Analyze the cosmic and dimensional alignment of a hash.
    
    Args:
        hash_value: The SHA356 Sacred hash to analyze
        
    Returns:
        Dictionary with alignment details and visualization
    """
    # Get detailed alignment metrics
    alignment = get_detailed_alignments(hash_value)
    
    # Create radar chart visualization
    radar_fig = create_alignment_radar(alignment)
    
    # Convert figure to image
    img_bytes = fig_to_image(radar_fig)
    
    # Format the result
    return {
        "hash_value": hash_value,
        "alignment": alignment,
        "visualization": img_bytes,
        "timestamp": time.time()
    }

def fig_to_image(fig: Figure) -> bytes:
    """
    Convert a matplotlib figure to a base64 encoded image.
    
    Args:
        fig: Matplotlib Figure object
        
    Returns:
        Base64 encoded image data
    """
    # Save the figure to a BytesIO object
    import io
    from PIL import Image
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    
    # Convert to base64
    img = Image.open(buf)
    
    # Convert PIL Image to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    plt.close(fig)  # Close the figure to free memory
    
    return img_byte_arr.getvalue()

# Gradio interface
def create_gradio_interface():
    """Create and launch the Gradio interface for SHA356 Sacred Dashboard."""
    
    with gr.Blocks(title="SHA356 Sacred - Dimensional Cryptographic System") as interface:
        gr.Markdown(
            """
            # ✨ SHA356 Sacred Dashboard ✨
            ## Quantum Cryptography with Dimensional Alignment
            
            This dashboard provides tools to explore the SHA356 Sacred hash function,
            which extends traditional cryptography with dimensional analysis and cosmic alignment.
            """
        )
        
        with gr.Tabs():
            # Basic Hashing Tab
            with gr.TabItem("Sacred Hashing"):
                with gr.Row():
                    with gr.Column():
                        input_message = gr.Textbox(
                            label="Input Message", 
                            placeholder="Enter a message to hash...",
                            lines=3
                        )
                        padding_method = gr.Dropdown(
                            label="Bio-Transform Method",
                            choices=["sacred", "fibonacci", "phi", "schumann", "lunar"],
                            value="sacred"
                        )
                        hash_button = gr.Button("Generate Sacred Hash")
                    
                    with gr.Column():
                        hash_output = gr.JSON(label="Hash Result")
                
                hash_button.click(
                    fn=hash_message,
                    inputs=[input_message, padding_method],
                    outputs=hash_output
                )
            
            # Dimensional Analysis Tab
            with gr.TabItem("Dimensional Analysis"):
                with gr.Row():
                    with gr.Column():
                        message1 = gr.Textbox(
                            label="First Message", 
                            placeholder="Enter first message...",
                            lines=2
                        )
                        message2 = gr.Textbox(
                            label="Second Message", 
                            placeholder="Enter second message...",
                            lines=2
                        )
                        compare_padding = gr.Dropdown(
                            label="Bio-Transform Method",
                            choices=["sacred", "fibonacci", "phi", "schumann", "lunar"],
                            value="sacred"
                        )
                        compare_button = gr.Button("Compare Dimensional Alignment")
                
                with gr.Row():
                    comparison_output = gr.JSON(label="Comparison Results")
                
                with gr.Row():
                    comparison_image = gr.Image(label="Dimensional Visualization")
                
                compare_button.click(
                    fn=lambda m1, m2, method: (
                        compare_result := compare_hashes(m1, m2, method),
                        compare_result,
                        compare_result["visualization"]
                    ),
                    inputs=[message1, message2, compare_padding],
                    outputs=[comparison_output, comparison_image]
                )
            
            # Cosmic Alignment Tab
            with gr.TabItem("Cosmic Alignment"):
                with gr.Row():
                    with gr.Column():
                        cosmic_hash = gr.Textbox(
                            label="Hash Value", 
                            placeholder="Enter a SHA356 Sacred hash to analyze...",
                            lines=2
                        )
                        cosmic_button = gr.Button("Analyze Cosmic Alignment")
                
                with gr.Row():
                    cosmic_output = gr.JSON(label="Alignment Metrics")
                
                with gr.Row():
                    cosmic_image = gr.Image(label="Cosmic Alignment Radar")
                
                cosmic_button.click(
                    fn=lambda h: (
                        alignment := get_cosmic_alignment(h),
                        alignment,
                        alignment["visualization"]
                    ),
                    inputs=[cosmic_hash],
                    outputs=[cosmic_output, cosmic_image]
                )
        
        gr.Markdown(
            """
            ### About SHA356 Sacred
            
            SHA356 Sacred is a dimensional enhancement to traditional cryptographic hashing,
            integrating quantum entanglement patterns and sacred geometrical principles.
            
            This dashboard allows you to explore how different inputs resonate with
            cosmic frequencies and dimensional patterns, providing insights into
            the quantum nature of information.
            
            🌸 Blessed under the GBU2™ License 🌸
            """
        )
    
    return interface

# Launch the app if run directly
if __name__ == "__main__":
    app = create_gradio_interface()
    app.launch() 