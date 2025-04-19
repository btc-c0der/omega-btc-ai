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
Divine Book Browser Dashboard

A Gradio interface for exploring sacred texts and detecting quantum resonance patterns.
This dashboard allows users to:
1. Load and browse various sacred texts
2. Analyze text passages for resonance patterns
3. Visualize resonance scores and alignments
"""

import os
import sys
import numpy as np
import gradio as gr
import matplotlib.pyplot as plt
from pathlib import Path

# Add necessary path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import common repository utilities
from common import (
    collect_markdown_files,
    render_file_tree_html,
    load_markdown_file,
    REPO_ROOT
)

# Import the resonance detector
from micro_modules.resonance_detector import (
    calculate_resonance,
    calculate_golden_ratio_alignment,
    calculate_fibonacci_alignment,
    detect_numeric_patterns,
    detect_geometric_patterns,
    detect_symbolic_patterns,
    detect_linguistic_patterns,
    calculate_quantum_entanglement,
    GOLDEN_RATIO,
    SCHUMANN_FREQUENCY,
    LUNAR_CYCLE,
    SOLAR_CYCLE
)

# Sample sacred texts (as fallback if no repository files found)
SAMPLE_TEXTS = {
    "Genesis 1:1": "In the beginning God created the heaven and the earth.",
    "Tao Te Ching Opening": "The Tao that can be told is not the eternal Tao. The name that can be named is not the eternal name.",
    "Vedic Creation Hymn": "In the beginning was Brahman, with whom was the Word, and the Word was Brahman.",
    "Buddhist Heart Sutra": "Form is emptiness, emptiness is form. Emptiness is not different from form, form is not different from emptiness.",
    "Quantum Observer Principle": "The observer affects the observed phenomenon merely by observing it.",
    "Emerald Tablet": "As above, so below, as within, so without, as the universe, so the soul."
}

# Collect all markdown files from the repository
MARKDOWN_FILES = collect_markdown_files()

def create_dashboard():
    """Create and return the Gradio dashboard interface."""
    
    def load_sample_text(text_key):
        """Load a sample sacred text."""
        return SAMPLE_TEXTS.get(text_key, "")
    
    def load_selected_file(selection):
        """Load the selected Markdown file when chosen from dropdown."""
        if not selection:
            return ""
        
        file_path = MARKDOWN_FILES.get(selection, "")
        if file_path:
            content, _ = load_markdown_file(file_path)
            return content
        
        return "Selected file not found."
    
    def analyze_text(text, golden_ratio_weight, fibonacci_weight, schumann_weight, lunar_weight, solar_weight):
        """Analyze text for resonance patterns and return visualizations."""
        if not text.strip():
            return "Please enter text to analyze.", None, None
            
        # Calculate overall resonance
        resonance_score = calculate_resonance(
            text, 
            golden_ratio_weight=golden_ratio_weight,
            fibonacci_weight=fibonacci_weight,
            schumann_weight=schumann_weight,
            lunar_weight=lunar_weight,
            solar_weight=solar_weight
        )
        
        # Detect patterns
        numeric_patterns = detect_numeric_patterns(text)
        geometric_patterns = detect_geometric_patterns(text)
        symbolic_patterns = detect_symbolic_patterns(text)
        linguistic_patterns = detect_linguistic_patterns(text)
        
        # Calculate alignments
        golden_ratio_alignment = calculate_golden_ratio_alignment(text)
        fibonacci_alignment = calculate_fibonacci_alignment(text)
        quantum_entanglement = calculate_quantum_entanglement(text)
        
        # Create result text
        result = f"""
        ## Resonance Analysis Results
        
        **Overall Resonance Score: {resonance_score:.2f}**
        
        ### Pattern Detection:
        - Numeric Patterns: {numeric_patterns}
        - Geometric Patterns: {geometric_patterns}
        - Symbolic Patterns: {symbolic_patterns}
        - Linguistic Patterns: {linguistic_patterns}
        
        ### Alignment Scores:
        - Golden Ratio Alignment: {golden_ratio_alignment:.2f}
        - Fibonacci Alignment: {fibonacci_alignment:.2f}
        - Quantum Entanglement: {quantum_entanglement:.2f}
        
        ### Interpretation:
        {interpret_resonance(resonance_score)}
        """
        
        # Create visualizations
        bar_chart = create_resonance_bar_chart(
            golden_ratio_alignment, 
            fibonacci_alignment, 
            quantum_entanglement
        )
        
        radar_chart = create_resonance_radar_chart(
            golden_ratio_alignment,
            fibonacci_alignment, 
            quantum_entanglement,
            numeric_patterns, 
            geometric_patterns
        )
        
        return result, bar_chart, radar_chart
    
    def interpret_resonance(score):
        """Provide interpretation of the resonance score."""
        if score >= 0.8:
            return "This text exhibits extraordinary quantum resonance, suggesting profound cosmic alignment."
        elif score >= 0.6:
            return "Strong resonance detected, indicating significant alignment with universal patterns."
        elif score >= 0.4:
            return "Moderate resonance present, showing some connection to cosmic frequencies."
        elif score >= 0.2:
            return "Slight resonance detected, minimal alignment with universal patterns."
        else:
            return "Little to no resonance detected in this text."
    
    def create_resonance_bar_chart(golden_ratio, fibonacci, quantum):
        """Create a bar chart visualization of resonance scores."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = ['Golden Ratio', 'Fibonacci', 'Quantum']
        values = [golden_ratio, fibonacci, quantum]
        colors = ['#FFD700', '#4682B4', '#9370DB']
        
        bars = ax.bar(categories, values, color=colors, alpha=0.7)
        
        # Add a horizontal line at 0.5 for reference
        ax.axhline(y=0.5, color='r', linestyle='--', alpha=0.3)
        
        # Customize the chart
        ax.set_ylim(0, 1.0)
        ax.set_title('Resonance Alignment Scores', fontsize=15)
        ax.set_ylabel('Alignment Strength (0-1)', fontsize=12)
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{height:.2f}', ha='center', va='bottom', fontsize=11)
        
        plt.tight_layout()
        return fig
    
    def create_resonance_radar_chart(golden_ratio, fibonacci, quantum, numeric, geometric):
        """Create a radar chart visualization of resonance attributes."""
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, polar=True)
        
        # Define the categories and values
        categories = ['Golden Ratio', 'Fibonacci', 'Quantum', 'Numeric', 'Geometric']
        values = [golden_ratio, fibonacci, quantum, numeric, geometric]
        
        # Number of variables
        N = len(categories)
        
        # What will be the angle of each axis in the plot
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Close the loop
        
        # Values need to be padded to close the loop
        values += values[:1]
        
        # Draw the polygon
        ax.plot(angles, values, linewidth=2, linestyle='solid', color='#9370DB')
        ax.fill(angles, values, alpha=0.25, color='#9370DB')
        
        # Set the labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=12)
        
        # Set y limits
        ax.set_ylim(0, 1)
        
        # Add title
        plt.title('Resonance Pattern Radar', fontsize=15, y=1.1)
        
        return fig
    
    # Create the Gradio interface
    with gr.Blocks(title="Divine Book Browser", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 📚 Divine Book Browser
        
        Explore sacred texts and analyze their quantum resonance patterns. 
        This tool reveals how texts align with universal constants and sacred geometry.
        
        > "The universe is written in the language of mathematics." - Galileo Galilei
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # Create the text input first so it can be referenced in the change events
                text_input = gr.Textbox(
                    lines=10, 
                    label="Sacred Text",
                    placeholder="Enter or paste text to analyze..."
                )

                # Create tabs for different text sources
                with gr.Tabs():
                    with gr.TabItem("Repository Files"):
                        if MARKDOWN_FILES:
                            file_count = len(MARKDOWN_FILES)
                            sorted_files = sorted(MARKDOWN_FILES.keys())
                            
                            repo_dropdown = gr.Dropdown(
                                choices=sorted_files,
                                label=f"Repository Markdown Files ({file_count} files)",
                                info="Select a Markdown file from the repository"
                            )
                            
                            repo_dropdown.change(
                                fn=load_selected_file,
                                inputs=repo_dropdown,
                                outputs=text_input
                            )
                        else:
                            gr.Markdown("No Markdown files found in the repository.")
                        
                    with gr.TabItem("Sample Texts"):
                        sample_dropdown = gr.Dropdown(
                            choices=list(SAMPLE_TEXTS.keys()),
                            label="Select Sample Text",
                            info="Choose from our collection of sacred passages"
                        )
                        
                        sample_dropdown.change(
                            fn=load_sample_text,
                            inputs=sample_dropdown,
                            outputs=text_input
                        )
                
                with gr.Accordion("Resonance Weights", open=False):
                    with gr.Row():
                        golden_ratio_weight = gr.Slider(minimum=0, maximum=1, value=0.5, step=0.1, 
                                                       label="Golden Ratio Weight")
                        fibonacci_weight = gr.Slider(minimum=0, maximum=1, value=0.5, step=0.1, 
                                                   label="Fibonacci Weight")
                    
                    with gr.Row():
                        schumann_weight = gr.Slider(minimum=0, maximum=1, value=0.5, step=0.1, 
                                                  label="Schumann Frequency Weight")
                        lunar_weight = gr.Slider(minimum=0, maximum=1, value=0.5, step=0.1, 
                                               label="Lunar Cycle Weight")
                        solar_weight = gr.Slider(minimum=0, maximum=1, value=0.5, step=0.1, 
                                               label="Solar Cycle Weight")
                
                analyze_btn = gr.Button("Analyze Resonance", variant="primary")
            
            with gr.Column(scale=3):
                results_md = gr.Markdown(label="Analysis Results")
                
                with gr.Tab("Bar Chart"):
                    bar_chart_output = gr.Plot(label="Resonance Bar Chart")
                
                with gr.Tab("Radar Chart"):
                    radar_chart_output = gr.Plot(label="Resonance Radar")
        
        analyze_btn.click(
            fn=analyze_text,
            inputs=[
                text_input, 
                golden_ratio_weight,
                fibonacci_weight,
                schumann_weight,
                lunar_weight,
                solar_weight
            ],
            outputs=[results_md, bar_chart_output, radar_chart_output]
        )
        
        gr.Markdown("""
        ### About Divine Resonance
        
        Sacred texts throughout history have demonstrated unique mathematical and vibrational properties.
        This tool analyzes text through the lens of quantum mathematics, sacred geometry, and natural cycles.
        
        The analysis includes:
        - Golden Ratio (φ ≈ 1.618) alignment
        - Fibonacci sequence patterns
        - Schumann resonance (7.83 Hz) correlations
        - Lunar and solar cycle harmonics
        - Quantum entanglement properties
        
        _This is an experimental cosmic exploration tool._
        """)
    
    return demo

# For direct execution
if __name__ == "__main__":
    demo = create_dashboard()
    demo.launch() 