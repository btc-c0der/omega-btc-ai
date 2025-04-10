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
SHA256 Omega Dashboard

Gradio interface for the SHA256 Omega cryptographic system with cosmic alignment.
"""

import json
import time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Dict, Any, Tuple, List, Optional, Literal
import random
from datetime import datetime

# Check for required packages and give helpful error if missing
try:
    import gradio as gr
except ImportError:
    print("Error: gradio package is required.")
    print("Please install it with: pip install gradio>=3.23.0")
    raise

try:
    import numpy as np
except ImportError:
    print("Error: numpy package is required.")
    print("Please install it with: pip install numpy>=1.20.0")
    raise

from .micro_modules.sha256_omega import sha256_omega
from .micro_modules.avalanche_analyzer import avalanche_score, detailed_avalanche_analysis as analyze_avalanche
from .micro_modules.resonance_score import get_resonance_score

# Constants
THEME = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="blue",
)

# Helper function to format JSON nicely
def format_json(data: Dict[str, Any]) -> str:
    """Format a dictionary as a nice JSON string."""
    return json.dumps(data, indent=2)

# Helper function to create visualization of avalanche effect
def create_avalanche_visualization(bits_different: List[int], positions: List[int]) -> Figure:
    """Create a visualization of the avalanche effect."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(positions, bits_different)
    ax.set_xlabel('Byte Position in Hash')
    ax.set_ylabel('Bits Different')
    ax.set_title('Avalanche Effect Visualization')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig

# Helper function to create cosmic alignment visualization
def create_cosmic_alignment_radar(alignment_data: Dict[str, float]) -> Figure:
    """Create a radar chart of cosmic alignment metrics."""
    # Extract categories and values
    categories = list(alignment_data.keys())
    values = list(alignment_data.values())
    
    # Number of variables
    N = len(categories)
    
    # What will be the angle of each axis in the plot
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Values need to be repeated to close the loop
    values += values[:1]
    
    # Initialize the figure
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Draw one axis per variable + add labels
    plt.xticks(angles[:-1], categories, color='grey', size=10)
    
    # Draw ylabels
    ax.set_yticks([0.25, 0.5, 0.75])
    ax.set_yticklabels(["0.25", "0.5", "0.75"], color="grey", size=8)
    plt.ylim(0, 1)
    
    # Plot data
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    
    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)
    
    plt.title("Cosmic Alignment Metrics", size=15, y=1.1)
    return fig

# Function to hash input message
def hash_input(message: str, bio_transform: bool, 
               padding_method: Literal["fibonacci", "phi", "schumann", "generic"], 
               fibonacci_seed: int, include_diagnostics: bool = False) -> Dict[str, Any]:
    """Hash input message using SHA256 Omega."""
    
    # Call SHA256 Omega function
    result = sha256_omega(
        message=message,
        bio_method=padding_method,
        fibonacci_alignment=bio_transform,
        include_diagnostics=include_diagnostics
    )
    
    return result

# Function for comparing hashes (avalanche analysis)
def compare_hashes(message1: str, message2: str, bio_transform: bool,
                  padding_method: Literal["fibonacci", "phi", "schumann", "generic"],
                  fibonacci_seed: int = 3) -> Dict[str, Any]:
    """Compare hashes to analyze avalanche effect."""
    
    # Get hashes for both messages
    hash1 = sha256_omega(
        message=message1,
        bio_method=padding_method,
        fibonacci_alignment=bio_transform,
    )
    
    hash2 = sha256_omega(
        message=message2,
        bio_method=padding_method,
        fibonacci_alignment=bio_transform,
    )
    
    # Calculate avalanche score
    score = avalanche_score(hash1['hash'], hash2['hash'])
    
    # Get detailed analysis
    detailed = analyze_avalanche(hash1['hash'], hash2['hash'])
    
    # Create visualization
    fig = create_avalanche_visualization(
        detailed['byte_level_scores'], 
        list(range(len(detailed['byte_level_scores'])))
    )
    
    return {'score': score, 'detailed': detailed, 'visualization': fig, 'hash1': hash1, 'hash2': hash2}

# Function to get cosmic alignment details
def get_cosmic_alignment() -> Tuple[Dict[str, float], Figure]:
    """Get cosmic alignment details and visualization."""
    
    # In a real implementation, this would connect to external data sources
    # For now, we generate sample data
    base_score = get_resonance_score("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    
    # Create sample alignment data
    alignment_data = {
        "Schumann Resonance": base_score,
        "Lunar Phase Alignment": round(0.6 + random.uniform(-0.1, 0.1), 3),
        "Solar Activity": round(0.7 + random.uniform(-0.1, 0.1), 3),
        "Quantum Fluctuation": round(0.85 + random.uniform(-0.08, 0.08), 3),
        "Planetary Alignment": round(0.75 + random.uniform(-0.1, 0.1), 3),
    }
    
    # Create visualization
    fig = create_cosmic_alignment_radar(alignment_data)
    
    return alignment_data, fig

# Create the Gradio interface

# Tab 1: Basic Hashing
with gr.Blocks(theme=THEME, title="SHA256 Omega") as hash_tab:
    gr.Markdown("# 🔱 SHA256 OMEGA 🔱")
    gr.Markdown("### Biologically-Aligned Cryptographic Hash Function")
    
    with gr.Row():
        with gr.Column(scale=1):
            input_message = gr.Textbox(
                label="Input Message",
                placeholder="Enter message to hash...",
                lines=5
            )
            use_bio = gr.Checkbox(
                label="Enable Bio-Transformation",
                value=True
            )
            padding_method = gr.Dropdown(
                label="Padding Method",
                choices=["fibonacci", "phi", "schumann", "generic"],
                value="fibonacci"
            )
            fibonacci_seed = gr.Number(
                label="Fibonacci Seed (optional)",
                value=3
            )
            hash_button = gr.Button("Generate Hash", variant="primary")
        
        with gr.Column(scale=2):
            hash_result = gr.JSON(label="Hash Result")
    
    hash_button.click(
        fn=hash_input,
        inputs=[input_message, use_bio, padding_method, fibonacci_seed],
        outputs=hash_result
    )

# Tab 2: Avalanche Analysis
with gr.Blocks(theme=THEME) as avalanche_tab:
    gr.Markdown("# 🔀 Avalanche Analysis")
    gr.Markdown("### Compare how small changes cascade through the entire hash")
    
    with gr.Row():
        with gr.Column(scale=1):
            message1 = gr.Textbox(
                label="First Message",
                placeholder="First message to compare...",
                lines=3
            )
            message2 = gr.Textbox(
                label="Second Message",
                placeholder="Second message to compare...",
                lines=3
            )
            compare_use_bio = gr.Checkbox(
                label="Enable Bio-Transformation",
                value=True
            )
            compare_padding = gr.Dropdown(
                label="Padding Method",
                choices=["fibonacci", "schumann", "generic"],
                value="fibonacci"
            )
            compare_seed = gr.Number(
                label="Fibonacci Seed",
                value=3
            )
            compare_button = gr.Button("Compare Hashes", variant="primary")
        
        with gr.Column(scale=2):
            avalanche_score_display = gr.Number(label="Avalanche Score (% of bits changed)")
            avalanche_details = gr.JSON(label="Analysis Details")
            avalanche_viz = gr.Plot(label="Avalanche Visualization")
    
    compare_button.click(
        fn=compare_hashes,
        inputs=[message1, message2, compare_use_bio, compare_padding, compare_seed],
        outputs=[avalanche_score_display, avalanche_details, avalanche_viz]
    )

# Tab 3: Cosmic Alignment
with gr.Blocks(theme=THEME) as cosmic_tab:
    gr.Markdown("# ☯️ Cosmic Alignment")
    gr.Markdown("### Explore how your hash resonates with universal frequencies")
    
    with gr.Row():
        with gr.Column():
            cosmic_button = gr.Button("Generate Cosmic Alignment", variant="primary")
            cosmic_result = gr.JSON(label="Cosmic Resonance Details")
        
        with gr.Column():
            cosmic_viz = gr.Plot(label="Cosmic Alignment Visualization")
    
    cosmic_button.click(
        fn=get_cosmic_alignment,
        outputs=[cosmic_result, cosmic_viz]
    )

# Create final tabbed interface
demo = gr.TabbedInterface(
    [hash_tab, avalanche_tab, cosmic_tab],
    ["SHA256 Omega", "Avalanche Analysis", "Cosmic Alignment"]
)

# Launch the app
if __name__ == "__main__":
    demo.launch(share=True) 