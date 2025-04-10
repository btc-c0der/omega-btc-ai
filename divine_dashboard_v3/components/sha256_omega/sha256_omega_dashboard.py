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

import gradio as gr
import json
import time
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any, Tuple, List, Optional
import random

# Import Omega SHA256 micro modules
from micro_modules.bio_padder import bio_padder
from micro_modules.fibonacci_transform import fibonacci_transform
from micro_modules.sha256_omega import sha256_omega
from micro_modules.avalanche_analyzer import avalanche_score, detailed_avalanche_analysis
from micro_modules.resonance_score import get_resonance_score, get_detailed_resonance

# Constants
THEME = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="blue",
)

# Helper functions
def format_json(data: Dict[str, Any]) -> str:
    """Format dictionary as pretty JSON string."""
    return json.dumps(data, indent=2)

def create_avalanche_visualization(hash1: str, hash2: str) -> np.ndarray:
    """Create visualization of avalanche effect between two hashes."""
    # Get binary representations
    import re
    from micro_modules.avalanche_analyzer import hex_to_binary
    
    bin1 = hex_to_binary(hash1)
    bin2 = hex_to_binary(hash2)
    
    # Create a 16x16 grid (256 bits total)
    grid = np.zeros((16, 16), dtype=int)
    
    # Fill grid with 1s where bits differ
    for i in range(256):
        row, col = divmod(i, 16)
        grid[row, col] = 1 if bin1[i] != bin2[i] else 0
    
    # Create visualization
    plt.figure(figsize=(10, 8))
    plt.imshow(grid, cmap='viridis', interpolation='none')
    plt.title('Avalanche Effect Visualization')
    plt.colorbar(ticks=[0, 1], label='Bit Difference')
    plt.xlabel('Bit Position')
    plt.ylabel('Bit Position')
    plt.grid(False)
    
    # Save to numpy array
    fig = plt.gcf()
    fig.canvas.draw()
    img = np.array(fig.canvas.renderer.buffer_rgba())
    plt.close()
    
    return img

def create_cosmic_chart(resonance_data: Dict[str, Any]) -> np.ndarray:
    """Create a visualization of cosmic alignment."""
    # Extract data
    score = resonance_data["resonance_score"]
    lunar = resonance_data["lunar_phase"]
    schumann = resonance_data["schumann_resonance"]
    solar = resonance_data["solar_activity"]
    
    # Create radar chart data
    categories = ['Resonance', 'Lunar', 'Schumann', 'Solar']
    values = [score, lunar, schumann/10, solar]  # Normalize Schumann to 0-1 range
    
    # Make it a closed polygon by repeating first point
    categories = categories + [categories[0]]
    values = values + [values[0]]
    
    # Convert to radians and create coordinates
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # Close the polygon
    
    # Create chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Plot data
    ax.plot(angles, values, 'o-', linewidth=2, color='blue')
    ax.fill(angles, values, alpha=0.25, color='blue')
    
    # Set category labels
    ax.set_thetagrids(np.degrees(angles[:-1]), categories[:-1])
    
    # Set chart properties
    ax.set_ylim(0, 1)
    ax.set_title("Cosmic Alignment", size=20, y=1.05)
    ax.grid(True)
    
    # Add a fancy background gradient
    background = np.linspace(0, 1, 100).reshape(-1, 1) * np.ones((100, 100))
    ax.patches = []
    
    # Save to numpy array
    fig.canvas.draw()
    img = np.array(fig.canvas.renderer.buffer_rgba())
    plt.close()
    
    return img

# Main functions for Gradio interface
def hash_input(message: str, use_bio: bool, padding_method: str, fibonacci_seed: str) -> Dict[str, Any]:
    """Hash input message using SHA256 Omega."""
    try:
        # Convert fibonacci seed to int if provided
        seed = int(fibonacci_seed) if fibonacci_seed else None
        
        # Hash the message
        result = sha256_omega(
            data=message, 
            bio=use_bio, 
            padding_method=padding_method,
            fibonacci_seed=seed
        )
        
        # Add cosmic resonance data
        resonance = get_detailed_resonance(result["hash"])
        result["cosmic_resonance"] = resonance
        
        return result
    except Exception as e:
        return {"error": str(e)}

def compare_hashes(message1: str, message2: str, use_bio: bool, padding_method: str, fibonacci_seed: str) -> Tuple[Dict[str, Any], np.ndarray]:
    """Compare two messages and analyze their hash differences."""
    try:
        # Convert fibonacci seed to int if provided
        seed = int(fibonacci_seed) if fibonacci_seed else None
        
        # Hash both messages
        result1 = sha256_omega(
            data=message1, 
            bio=use_bio, 
            padding_method=padding_method,
            fibonacci_seed=seed
        )
        
        result2 = sha256_omega(
            data=message2, 
            bio=use_bio, 
            padding_method=padding_method,
            fibonacci_seed=seed
        )
        
        # Analyze avalanche effect
        hash1 = result1["hash"]
        hash2 = result2["hash"]
        analysis = detailed_avalanche_analysis(hash1, hash2)
        
        # Create visualization
        viz = create_avalanche_visualization(hash1, hash2)
        
        # Combine results
        result = {
            "message1": message1,
            "message2": message2,
            "hash1": hash1,
            "hash2": hash2,
            "avalanche_analysis": analysis
        }
        
        return result, viz
    except Exception as e:
        return {"error": str(e)}, np.zeros((100, 100, 4))

def get_cosmic_alignment(hash_value: str) -> Tuple[Dict[str, Any], np.ndarray]:
    """Get cosmic alignment details for a hash."""
    try:
        # Get resonance data
        resonance = get_detailed_resonance(hash_value)
        
        # Create visualization
        viz = create_cosmic_chart(resonance)
        
        return resonance, viz
    except Exception as e:
        return {"error": str(e)}, np.zeros((100, 100, 4))

# Create Gradio interface
def create_interface():
    """Create Gradio interface for SHA256 Omega Dashboard."""
    
    # Tab 1: Basic Hashing
    with gr.Blocks(theme=THEME, title="SHA256 Omega") as hash_tab:
        gr.Markdown("# 🔱 SHA256 OMEGA 🔱")
        gr.Markdown("### Biologically-Aligned Cryptographic Hash Function")
        
        with gr.Row():
            with gr.Column(scale=3):
                input_message = gr.Textbox(
                    label="Input Message",
                    placeholder="Enter text to hash...",
                    lines=5
                )
                
                with gr.Row():
                    use_bio = gr.Checkbox(label="Use Bio Transform", value=True)
                    padding_method = gr.Radio(
                        label="Padding Method",
                        choices=["fibonacci", "schumann", "generic"],
                        value="fibonacci"
                    )
                    fibonacci_seed = gr.Textbox(
                        label="Fibonacci Seed (Optional)",
                        placeholder="Enter a number"
                    )
                
                hash_button = gr.Button("🧬 Generate Omega Hash", variant="primary")
            
            with gr.Column(scale=4):
                hash_result = gr.JSON(label="Hash Result")
                
        hash_button.click(
            fn=hash_input,
            inputs=[input_message, use_bio, padding_method, fibonacci_seed],
            outputs=hash_result
        )
    
    # Tab 2: Avalanche Analysis
    with gr.Blocks(theme=THEME) as avalanche_tab:
        gr.Markdown("# 🌊 Avalanche Analysis")
        gr.Markdown("### Compare hash outputs for similar inputs")
        
        with gr.Row():
            with gr.Column(scale=1):
                message1 = gr.Textbox(
                    label="Message 1",
                    placeholder="First message...",
                    lines=3
                )
                message2 = gr.Textbox(
                    label="Message 2",
                    placeholder="Second message (similar to first)...",
                    lines=3
                )
                
                with gr.Row():
                    av_use_bio = gr.Checkbox(label="Use Bio Transform", value=True)
                    av_padding_method = gr.Radio(
                        label="Padding Method",
                        choices=["fibonacci", "schumann", "generic"],
                        value="fibonacci"
                    )
                    av_fibonacci_seed = gr.Textbox(
                        label="Fibonacci Seed (Optional)",
                        placeholder="Enter a number"
                    )
                
                compare_button = gr.Button("🔍 Compare Hashes", variant="primary")
            
            with gr.Column(scale=1):
                av_result = gr.JSON(label="Avalanche Analysis")
        
        with gr.Row():
            av_viz = gr.Image(label="Avalanche Visualization", show_label=True)
        
        compare_button.click(
            fn=compare_hashes,
            inputs=[message1, message2, av_use_bio, av_padding_method, av_fibonacci_seed],
            outputs=[av_result, av_viz]
        )
    
    # Tab 3: Cosmic Alignment
    with gr.Blocks(theme=THEME) as cosmic_tab:
        gr.Markdown("# ✨ Cosmic Alignment")
        gr.Markdown("### Analyze hash alignment with natural resonances")
        
        with gr.Row():
            with gr.Column(scale=1):
                hash_input = gr.Textbox(
                    label="Hash Value",
                    placeholder="Enter a SHA256 hash (64 hex characters)...",
                    lines=2
                )
                
                cosmic_button = gr.Button("🌌 Analyze Cosmic Alignment", variant="primary")
            
            with gr.Column(scale=1):
                cosmic_result = gr.JSON(label="Cosmic Alignment Analysis")
        
        with gr.Row():
            cosmic_viz = gr.Image(label="Cosmic Alignment Visualization")
            
        cosmic_button.click(
            fn=get_cosmic_alignment,
            inputs=[hash_input],
            outputs=[cosmic_result, cosmic_viz]
        )
    
    # Create final tabbed interface
    demo = gr.TabbedInterface(
        [hash_tab, avalanche_tab, cosmic_tab],
        ["SHA256 Omega", "Avalanche Analysis", "Cosmic Alignment"]
    )
    
    return demo

# Launch the app
if __name__ == "__main__":
    demo = create_interface()
    demo.launch(share=True) 