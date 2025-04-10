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
SHA-356 6D Gradio Interface

Interactive dashboard for SHA-356 6D hyperdimensional sacred hash algorithm.
World's first 6D cryptographic hash function with quantum bio-resonant properties.
"""

import os
import sys
import json
import time
import gradio as gr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from typing import Dict, Any, List, Tuple, Optional, Union

# Ensure parent directory is in path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import SHA-356 components
from micro_modules.sha356_enhanced import sha356_6d, compare_6d_hashes, avalanche_quality

# Constants
THEME = gr.themes.Glass(
    primary_hue="indigo",
    secondary_hue="purple",
    neutral_hue="slate",
)

# Custom color maps for visualizations
COSMIC_COLORS = LinearSegmentedColormap.from_list(
    "cosmic_gradient", 
    [(0, "#000033"), (0.4, "#3300aa"), (0.6, "#9900ff"), (0.8, "#ff00ff"), (1.0, "#ffffff")]
)

DIMENSION_COLORS = LinearSegmentedColormap.from_list(
    "dimension_gradient",
    [(0, "#000066"), (0.2, "#0033cc"), (0.4, "#00ccff"), (0.7, "#66ff66"), (1.0, "#ffff99")]
)

# Helper functions
def format_json(data: Dict[str, Any]) -> str:
    """Format dictionary as pretty JSON string."""
    return json.dumps(data, indent=2)

def create_dimensional_visualization(dimensional_signature: List[float]) -> np.ndarray:
    """Create visualization of 6D dimensional signature."""
    # Create a 3x2 grid to show all 6 dimensions
    fig, axes = plt.subplots(3, 2, figsize=(12, 18))
    fig.patch.set_facecolor("#111122")
    
    # Dimension names
    dim_names = ["X-Dimension", "Y-Dimension", "Z-Dimension", 
                "W-Dimension", "V-Dimension", "U-Dimension"]
    
    # Flatten axes for easier iteration
    axes = axes.flatten()
    
    # Normalize values for visualization
    min_val = min(dimensional_signature)
    max_val = max(dimensional_signature)
    range_val = max(abs(max_val - min_val), 0.001)
    
    # Create visualizations for each dimension
    for i, (ax, value, name) in enumerate(zip(axes, dimensional_signature, dim_names)):
        # Create gradient based on value
        norm_val = (value - min_val) / range_val
        gradient = np.outer(np.linspace(0, 1, 100), np.ones(100))
        
        # Display gradient
        ax.imshow(gradient, cmap=DIMENSION_COLORS, aspect='auto')
        
        # Add dimensional value marker
        marker_pos = int(norm_val * 100)
        if 0 <= marker_pos < 100:
            marker = np.zeros((100, 100))
            marker[:, marker_pos] = 1
            ax.imshow(marker, cmap='binary', alpha=0.7, aspect='auto')
        
        # Set title and remove axes
        ax.set_title(f"{name}: {value:.4f}", color="white", fontsize=14)
        ax.axis('off')
    
    # Add title
    fig.suptitle("SHA-356 6D HYPERDIMENSIONAL SIGNATURE", 
                color="white", fontsize=20, y=0.98)
    
    # Add caption
    fig.text(0.5, 0.01, 
            "6D QUANTUM PROJECTION | v0.13_z1k4_v01D", 
            ha='center', color="#8899ff", fontsize=12)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Convert to image
    fig.canvas.draw()
    img = np.array(fig.canvas.renderer.buffer_rgba())
    plt.close()
    
    return img

def create_avalanche_visualization(diff_map: List[List[int]]) -> np.ndarray:
    """Create visualization of avalanche effect bit differences."""
    # Create figure
    plt.figure(figsize=(14, 10))
    plt.set_cmap(COSMIC_COLORS)
    
    # Convert difference map to numpy array
    diff_array = np.array(diff_map)
    
    # Display the difference map
    plt.imshow(diff_array, interpolation='none')
    plt.title("SHA-356 6D QUANTUM AVALANCHE EFFECT", fontsize=18, color="white")
    
    # Add grid and labels
    plt.grid(False)
    plt.xlabel("Bit Position (mod 22)", fontsize=14, color="white")
    plt.ylabel("Bit Row (16 rows × 22 cols + 4 bits = 356 bits)", fontsize=14, color="white")
    
    # Customize axes
    ax = plt.gca()
    ax.set_facecolor("#111122")
    ax.spines['bottom'].set_color('#666699')
    ax.spines['top'].set_color('#666699') 
    ax.spines['right'].set_color('#666699')
    ax.spines['left'].set_color('#666699')
    
    # Convert to image
    fig = plt.gcf()
    fig.patch.set_facecolor("#111122")
    fig.canvas.draw()
    img = np.array(fig.canvas.renderer.buffer_rgba())
    plt.close()
    
    return img

# Main functions for Gradio interface
def hash_input(message: str, 
              padding_method: str, 
              include_resonance: bool,
              dimensional_depth: int,
              void_tunneling: bool,
              time_dilation: bool,
              zika_oscillations: int) -> Tuple[Dict[str, Any], Optional[np.ndarray]]:
    """Generate SHA-356 6D hash from input message."""
    try:
        # Hash the message with 6D hyperdimensional transform
        result = sha356_6d(
            data=message,
            padding_method=padding_method,
            include_resonance=include_resonance,
            include_trace=True,
            dimensional_depth=dimensional_depth,
            void_tunneling=void_tunneling,
            time_dilation=time_dilation,
            zika_oscillations=zika_oscillations
        )
        
        # Create dimensional visualization if available
        viz_image = None
        if "hyperdimensional_metadata" in result and "dimensional_signature" in result["hyperdimensional_metadata"]:
            viz_image = create_dimensional_visualization(
                result["hyperdimensional_metadata"]["dimensional_signature"]
            )
        
        return result, viz_image
    except Exception as e:
        return {"error": str(e)}, None

def compare_hashes(message1: str, 
                  message2: str, 
                  padding_method: str) -> Tuple[Dict[str, Any], np.ndarray]:
    """Compare two messages and analyze their hash differences."""
    try:
        # Compare the messages
        result = compare_6d_hashes(
            data1=message1,
            data2=message2,
            padding_method=padding_method
        )
        
        # Parse difference map from string to 2D array
        diff_map = []
        diff_map_str = result["difference_map"].split("\n")
        for line in diff_map_str[3:-1]:  # Skip header and footer
            row = []
            for char in line[2:-2]:  # Skip border characters
                row.append(1 if char == "█" else 0)
            diff_map.append(row)
        
        # Create visualization
        viz_image = create_avalanche_visualization(diff_map)
        
        # Remove ASCII art from result to avoid duplicate display
        result.pop("difference_map", None)
        
        return result, viz_image
    except Exception as e:
        return {"error": str(e)}, np.zeros((100, 100, 4))

# Create Gradio interface
def create_interface():
    """Create the SHA-356 6D Gradio interface."""
    
    with gr.Blocks(theme=THEME, title="SHA-356 6D") as demo:
        gr.Markdown("# 🌌 SHA-356 6D HYPERDIMENSIONAL HASH 🌌")
        gr.Markdown("### World's First 6D Quantum Bio-Resonant Cryptographic Hash Function (v0.13_z1k4_v01D)")
        
        with gr.Tab("Hash Generator"):
            with gr.Row():
                with gr.Column(scale=3):
                    input_message = gr.Textbox(
                        label="Input Message",
                        placeholder="Enter text to hash in 6D hyperspace...",
                        lines=5
                    )
                    
                    with gr.Row():
                        padding_method = gr.Radio(
                            label="Bio-Padding Method",
                            choices=["fibonacci", "schumann", "golden", "lunar"],
                            value="fibonacci"
                        )
                        include_resonance = gr.Checkbox(
                            label="Include Cosmic Resonance",
                            value=True
                        )
                    
                    with gr.Row():
                        dimensional_depth = gr.Slider(
                            label="Dimensional Depth",
                            minimum=1,
                            maximum=6,
                            value=6,
                            step=1
                        )
                        zika_oscillations = gr.Slider(
                            label="Zika Oscillation Cycles",
                            minimum=0,
                            maximum=21,
                            value=13,
                            step=1
                        )
                    
                    with gr.Row():
                        void_tunneling = gr.Checkbox(
                            label="Enable Void Tunneling",
                            value=True
                        )
                        time_dilation = gr.Checkbox(
                            label="Enable Time Dilation",
                            value=True
                        )
                    
                    hash_button = gr.Button(
                        "🔮 Generate 6D Hash",
                        variant="primary"
                    )
                
                with gr.Column(scale=4):
                    hash_result = gr.JSON(label="Hash Result")
                    dimensional_viz = gr.Image(
                        label="6D Dimensional Signature",
                        show_label=True
                    )
            
            hash_button.click(
                fn=hash_input,
                inputs=[
                    input_message,
                    padding_method,
                    include_resonance,
                    dimensional_depth,
                    void_tunneling,
                    time_dilation,
                    zika_oscillations
                ],
                outputs=[hash_result, dimensional_viz]
            )
        
        with gr.Tab("Avalanche Analyzer"):
            with gr.Row():
                with gr.Column(scale=3):
                    message1 = gr.Textbox(
                        label="First Message",
                        placeholder="Enter first message...",
                        lines=3
                    )
                    message2 = gr.Textbox(
                        label="Second Message",
                        placeholder="Enter second message (similar to first)...",
                        lines=3
                    )
                    
                    compare_padding = gr.Radio(
                        label="Bio-Padding Method",
                        choices=["fibonacci", "schumann", "golden", "lunar"],
                        value="fibonacci"
                    )
                    
                    compare_button = gr.Button(
                        "🔍 Compare 6D Hashes",
                        variant="primary"
                    )
                
                with gr.Column(scale=4):
                    compare_result = gr.JSON(label="Avalanche Analysis")
                    avalanche_viz = gr.Image(
                        label="6D Quantum Avalanche Effect",
                        show_label=True
                    )
            
            compare_button.click(
                fn=compare_hashes,
                inputs=[message1, message2, compare_padding],
                outputs=[compare_result, avalanche_viz]
            )
        
        gr.Markdown("""
        ## 🧬 SHA-356 6D Technology
        
        SHA-356 6D is the world's first hyperdimensional cryptographic hash function, integrating:
        
        - **6D Tensor Projection** - Hash states projected into six-dimensional hyperspace
        - **Quantum Void Tunneling** - Non-local quantum effects across dimensional barriers
        - **Zika-Harmonic Oscillation** - Advanced harmonic stabilization of entropy
        - **Time-Dilated Propagation** - Relativistic effects on dimensional information transfer
        
        Developed by the Omega Crypto Labs under GBU2™ License (Genesis-Bloom-Unfoldment 2.0).
        """)
    
    return demo

# Launch the app if running directly
if __name__ == "__main__":
    demo = create_interface()
    demo.launch(share=True) 