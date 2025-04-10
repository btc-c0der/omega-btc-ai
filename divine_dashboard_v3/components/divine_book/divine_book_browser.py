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

A dashboard for exploring and analyzing sacred texts for resonance patterns.
Integrates with the resonance detector module to identify alignment with
universal constants and sacred patterns.
"""

import os
import math
import sys
import numpy as np
import matplotlib.pyplot as plt
import gradio as gr
from typing import Dict, List, Tuple, Optional, Any
import json
from pathlib import Path
import re
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from rich.tree import Tree
from rich.console import Console
from rich import print as rprint
import io
from collections import defaultdict

# Add the current directory to the path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Find the repository root directory
repo_root = None
current_path = Path(current_dir)
while current_path != current_path.parent:
    if (current_path / ".git").exists():
        repo_root = current_path
        break
    current_path = current_path.parent

if repo_root is None:
    # Fallback to current directory if .git not found
    repo_root = Path(current_dir).parent.parent.parent

# Import the resonance detector module
from micro_modules.resonance_detector import (
    calculate_resonance,
    find_sacred_patterns,
    detect_numeric_patterns,
    detect_geometric_patterns,
    detect_symbolic_patterns,
    detect_linguistic_patterns,
    calculate_quantum_entanglement
)

# Custom Markdown renderer with syntax highlighting
class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, lang=None):
        if lang:
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
                formatter = html.HtmlFormatter(
                    style='monokai',
                    linenos=True,
                    cssclass="source"
                )
                return highlight(code, lexer, formatter)
            except:
                pass
        return f'<pre><code>{mistune.escape(code)}</code></pre>'

# Create Markdown parser
markdown_parser = mistune.create_markdown(
    renderer=HighlightRenderer(),
    plugins=['table', 'url', 'strikethrough', 'footnotes', 'task_lists']
)

def build_file_tree() -> Dict[str, Any]:
    """
    Build a hierarchical tree structure of all Markdown files in the repository.
    
    Returns:
        Dictionary representing the file tree
    """
    tree = defaultdict(dict)
    
    # Collect all markdown files
    md_files = collect_markdown_files()
    
    # Build the tree structure
    for path in md_files.keys():
        parts = path.split('/')
        current = tree
        
        # Navigate through directories
        for i, part in enumerate(parts):
            if i == len(parts) - 1:  # File
                current[part] = md_files[path]
            else:  # Directory
                if part not in current:
                    current[part] = defaultdict(dict)
                current = current[part]
    
    return tree

def render_file_tree() -> str:
    """
    Render the file tree structure as HTML for display in the UI.
    
    Returns:
        HTML string representation of the file tree
    """
    # Build the file tree
    file_tree = build_file_tree()
    
    # Use rich to create a pretty tree
    console = Console(file=io.StringIO(), highlight=False)
    tree = Tree(f"📚 Repository Markdown Files ({len(MARKDOWN_FILES)} files)")
    
    # Recursively add branches to the tree
    def add_to_tree(node, data):
        for key, value in sorted(data.items()):
            if isinstance(value, (dict, defaultdict)):
                # This is a directory
                branch = node.add(f"📁 {key}")
                add_to_tree(branch, value)
            else:
                # This is a file
                file_path = value
                rel_path = Path(file_path).relative_to(repo_root)
                node.add(f"📄 {key} [dim]({rel_path})[/dim]")
    
    add_to_tree(tree, file_tree)
    
    # Print the tree to the string buffer
    console.print(tree)
    
    # Get the output and convert to HTML
    tree_output = console.file.getvalue()
    
    # Convert to HTML with <pre> and styling
    html_output = f"""
    <style>
        .file-tree {{
            background-color: #1e1e2e;
            color: #cdd6f4;
            padding: 1rem;
            border-radius: 0.5rem;
            font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
            overflow-y: auto;
            max-height: 500px;
        }}
    </style>
    <div class="file-tree">
        <pre>{tree_output}</pre>
    </div>
    """
    
    return html_output

def collect_markdown_files() -> Dict[str, str]:
    """
    Collect all Markdown files from the repository.
    
    Returns:
        Dictionary mapping display names to file paths
    """
    md_files = {}
    ignored_dirs = ["node_modules", ".git", "__pycache__", "venv", "divine_venv"]
    
    # Walk through the repository directory
    for root, dirs, files in os.walk(repo_root):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                
                # Create a display name from the path
                rel_path = os.path.relpath(file_path, repo_root)
                display_name = f"{os.path.dirname(rel_path)}/{os.path.basename(rel_path)}"
                
                # Store the file path with its display name
                md_files[display_name] = file_path
    
    return md_files

# Collect all Markdown files from the repository
MARKDOWN_FILES = collect_markdown_files()

def create_dashboard():
    """
    Create the Divine Book Browser Dashboard.
    
    Returns:
        Gradio interface
    """
    def load_markdown_file(file_path: str) -> Tuple[str, str]:
        """
        Load the content of a Markdown file and render it to HTML.
        
        Returns:
            Tuple of (raw_markdown, rendered_html)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Render markdown to HTML
                html_content = markdown_parser(content)
                
                return content, html_content
        except Exception as e:
            error_msg = f"Error loading file: {str(e)}"
            return error_msg, f"<div class='error'>{error_msg}</div>"
    
    def load_selected_file(selection: str) -> Tuple[str, str]:
        """
        Load the selected Markdown file when chosen from dropdown.
        
        Returns:
            Tuple of (raw_markdown, rendered_html)
        """
        if not selection:
            return "", ""
        
        file_path = MARKDOWN_FILES.get(selection, "")
        if file_path:
            return load_markdown_file(file_path)
        
        error_msg = "Selected file not found."
        return error_msg, f"<div class='error'>{error_msg}</div>"
    
    def analyze_text(
        text: str,
        golden_ratio_weight: float,
        fibonacci_weight: float,
        schumann_weight: float,
        lunar_weight: float,
        solar_weight: float
    ) -> Tuple[float, Dict, str, np.ndarray, np.ndarray]:
        """
        Analyze text for resonance patterns
        
        Args:
            text: The text to analyze
            golden_ratio_weight: Weight for golden ratio alignment (0-1)
            fibonacci_weight: Weight for fibonacci alignment (0-1)
            schumann_weight: Weight for Schumann resonance alignment (0-1)
            lunar_weight: Weight for lunar cycle alignment (0-1)
            solar_weight: Weight for solar cycle alignment (0-1)
            
        Returns:
            Tuple containing:
            - Overall resonance score
            - Sacred patterns dictionary
            - Interpretation text
            - Bar chart figure
            - Radar chart figure
        """
        if not text or not text.strip():
            return 0.0, {}, "Please enter text to analyze", None, None
        
        # Calculate overall resonance
        resonance_score = calculate_resonance(
            text,
            golden_ratio_weight=golden_ratio_weight,
            fibonacci_weight=fibonacci_weight,
            schumann_weight=schumann_weight,
            lunar_weight=lunar_weight,
            solar_weight=solar_weight
        )
        
        # Find sacred patterns
        patterns = find_sacred_patterns(text)
        
        # Generate interpretation
        interpretation = interpret_resonance(resonance_score, patterns)
        
        # Create visualizations
        bar_chart = create_resonance_bar_chart(patterns)
        radar_chart = create_resonance_radar_chart(patterns)
        
        return resonance_score, patterns, interpretation, bar_chart, radar_chart
    
    def interpret_resonance(resonance_score: float, patterns: Dict) -> str:
        """Generate an interpretation of the resonance results"""
        interpretation = f"## Divine Resonance Analysis\n\n"
        interpretation += f"### Overall Resonance Score: {resonance_score:.2f}\n\n"
        
        # Interpret the overall score
        if resonance_score > 0.8:
            interpretation += "🌟 **Exceptional Resonance**: This text exhibits extraordinary alignment with universal patterns and sacred geometry.\n\n"
        elif resonance_score > 0.6:
            interpretation += "✨ **Strong Resonance**: This text shows significant alignment with cosmic patterns and sacred principles.\n\n"
        elif resonance_score > 0.4:
            interpretation += "🔆 **Moderate Resonance**: This text contains notable sacred patterns and philosophical resonance.\n\n"
        elif resonance_score > 0.2:
            interpretation += "✓ **Mild Resonance**: This text exhibits some alignment with universal patterns.\n\n"
        else:
            interpretation += "○ **Minimal Resonance**: This text shows limited alignment with sacred patterns.\n\n"
        
        # Add pattern interpretations
        interpretation += "### Key Findings:\n\n"
        
        # Numeric patterns
        numeric_score = patterns["numeric_patterns"]
        if numeric_score > 0.5:
            interpretation += "- **Sacred Numbers**: Strong presence of sacred numerical patterns\n"
        elif numeric_score > 0.2:
            interpretation += "- **Sacred Numbers**: Some sacred numerical patterns detected\n"
        
        # Geometric patterns
        geometric_score = patterns["geometric_patterns"]
        if geometric_score > 0.5:
            interpretation += "- **Sacred Geometry**: Strong references to geometric principles\n"
        elif geometric_score > 0.2:
            interpretation += "- **Sacred Geometry**: Some geometric principles referenced\n"
        
        # Symbolic patterns
        symbolic_score = patterns["symbolic_patterns"]
        if symbolic_score > 0.5:
            interpretation += "- **Symbolic Elements**: Rich with symbolic language and metaphors\n"
        elif symbolic_score > 0.2:
            interpretation += "- **Symbolic Elements**: Contains symbolic references\n"
        
        # Linguistic patterns
        linguistic_score = patterns["linguistic_patterns"]
        if linguistic_score > 0.5:
            interpretation += "- **Linguistic Harmony**: Exceptional rhythmic and poetic structure\n"
        elif linguistic_score > 0.2:
            interpretation += "- **Linguistic Harmony**: Contains rhythmic or poetic elements\n"
        
        # Golden ratio alignment
        golden_ratio = patterns["golden_ratio_alignment"]
        if golden_ratio > 0.7:
            interpretation += "- **Golden Ratio**: Text structure shows remarkable alignment with the divine proportion\n"
        elif golden_ratio > 0.4:
            interpretation += "- **Golden Ratio**: Text structure exhibits some alignment with the divine proportion\n"
        
        # Quantum entanglement
        entanglement = patterns["quantum_entanglement"]
        if entanglement > 0.7:
            interpretation += "- **Quantum Properties**: Text exhibits exceptional information density and balance\n"
        elif entanglement > 0.4:
            interpretation += "- **Quantum Properties**: Text shows good information balance characteristics\n"
        
        return interpretation
    
    def create_resonance_bar_chart(patterns: Dict) -> np.ndarray:
        """Create a bar chart of resonance patterns"""
        plt.figure(figsize=(10, 6))
        
        # Extract pattern values
        pattern_names = [
            "Numeric\nPatterns",
            "Geometric\nPatterns",
            "Symbolic\nElements",
            "Linguistic\nPatterns",
            "Golden Ratio\nAlignment",
            "Fibonacci\nAlignment",
            "Quantum\nEntanglement"
        ]
        
        values = [
            patterns["numeric_patterns"],
            patterns["geometric_patterns"],
            patterns["symbolic_patterns"],
            patterns["linguistic_patterns"],
            patterns["golden_ratio_alignment"],
            patterns["fibonacci_alignment"],
            patterns["quantum_entanglement"]
        ]
        
        # Create bar chart
        bars = plt.bar(pattern_names, values, color='purple', alpha=0.7)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{height:.2f}', ha='center', va='bottom', fontsize=9)
        
        plt.title('Sacred Pattern Distribution', fontsize=16)
        plt.ylabel('Resonance Score', fontsize=12)
        plt.ylim(0, 1.1)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # Convert to image array
        fig = plt.gcf()
        fig.canvas.draw()
        img = np.array(fig.canvas.renderer.buffer_rgba())
        plt.close()
        
        return img
    
    def create_resonance_radar_chart(patterns: Dict) -> np.ndarray:
        """Create a radar chart of resonance patterns"""
        # Extract pattern values
        categories = [
            'Numeric\nPatterns',
            'Geometric\nPatterns',
            'Symbolic\nElements',
            'Linguistic\nPatterns',
            'Golden Ratio\nAlignment',
            'Fibonacci\nAlignment',
            'Quantum\nEntanglement'
        ]
        
        values = [
            patterns["numeric_patterns"],
            patterns["geometric_patterns"],
            patterns["symbolic_patterns"],
            patterns["linguistic_patterns"],
            patterns["golden_ratio_alignment"],
            patterns["fibonacci_alignment"],
            patterns["quantum_entanglement"]
        ]
        
        # Number of variables
        N = len(categories)
        
        # Compute angle for each axis
        angles = [n / float(N) * 2 * math.pi for n in range(N)]
        angles += angles[:1]  # Close the loop
        
        # Add the values for the plot (also closes the loop)
        values_plot = values + values[:1]
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        
        # Draw the outline of the data
        ax.plot(angles, values_plot, linewidth=1, linestyle='solid', color='purple')
        
        # Fill area
        ax.fill(angles, values_plot, color='purple', alpha=0.25)
        
        # Set category labels
        plt.xticks(angles[:-1], categories, size=9)
        
        # Draw y-axis circles
        ax.set_rlabel_position(0)
        plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=8)
        plt.ylim(0, 1)
        
        plt.title('Sacred Pattern Radar', size=16, y=1.1)
        
        # Convert to image array
        fig.canvas.draw()
        img = np.array(fig.canvas.renderer.buffer_rgba())
        plt.close()
        
        return img
    
    # Custom CSS for the interface
    custom_css = """
    .md-preview {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1.5rem;
        background-color: #f7f9fc;
        overflow-y: auto;
        height: 700px;  /* Set fixed height */
        max-height: 700px;
        font-family: 'Source Sans Pro', 'Open Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        line-height: 1.6;
        font-size: 16px;
    }
    
    .md-preview h1 {
        color: #5E35B1;
        margin-top: 1.5em;
        margin-bottom: 0.8em;
        font-size: 2.2em;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0.3em;
    }
    
    .md-preview h2 {
        color: #7E57C2;
        margin-top: 1.4em;
        margin-bottom: 0.7em;
        font-size: 1.8em;
        border-bottom: 1px solid #e0e0e0;
        padding-bottom: 0.2em;
    }
    
    .md-preview h3 {
        color: #9575CD;
        margin-top: 1.3em;
        margin-bottom: 0.6em;
        font-size: 1.5em;
    }
    
    .md-preview pre {
        background-color: #282a36;
        border-radius: 8px;
        padding: 1.2em;
        overflow-x: auto;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1.5em 0;
    }
    
    .md-preview code {
        font-family: 'Fira Code', 'Menlo', 'Monaco', 'Courier New', monospace;
        font-size: 0.9em;
    }
    
    .md-preview .source {
        background-color: #282a36;
        color: #f8f8f2;
    }
    
    .md-preview .source .linenos {
        color: #6272a4;
        border-right: 1px solid #4e5579;
        padding-right: 0.8em;
        margin-right: 0.8em;
    }
    
    .md-preview table {
        border-collapse: collapse;
        width: 100%;
        margin: 1.5em 0;
        box-shadow: 0 2px 3px rgba(0,0,0,0.1);
    }
    
    .md-preview th {
        background-color: #e6e8f0;
        font-weight: bold;
        padding: 12px;
        border: 1px solid #cfd8dc;
    }
    
    .md-preview td {
        padding: 10px;
        border: 1px solid #ddd;
    }
    
    .md-preview tr:nth-child(even) {
        background-color: #f5f7fa;
    }
    
    .md-preview blockquote {
        border-left: 4px solid #9575cd;
        padding: 0.8em 1.2em;
        margin: 1.5em 0;
        background-color: #f3f0ff;
        border-radius: 0 4px 4px 0;
        font-style: italic;
        color: #555;
    }
    
    .md-preview ul, .md-preview ol {
        padding-left: 1.8em;
        margin: 1em 0;
    }
    
    .md-preview li {
        margin-bottom: 0.5em;
    }
    
    .md-preview a {
        color: #7c4dff;
        text-decoration: none;
        border-bottom: 1px dotted #7c4dff;
        transition: all 0.2s ease;
    }
    
    .md-preview a:hover {
        color: #651fff;
        border-bottom: 1px solid #651fff;
    }
    
    .file-tree {
        background-color: #1e1e2e;
        color: #cdd6f4;
        padding: 1.2rem;
        border-radius: 8px;
        font-family: 'JetBrains Mono', 'Fira Code', 'Menlo', 'Monaco', 'Courier New', monospace;
        overflow-y: auto;
        max-height: 600px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        font-size: 14px;
        line-height: 1.4;
    }
    
    .error {
        color: #d32f2f;
        padding: 1em;
        background-color: #ffebee;
        border-radius: 8px;
        border-left: 4px solid #d32f2f;
        margin: 1em 0;
        font-family: 'Source Sans Pro', sans-serif;
        line-height: 1.6;
    }
    
    /* Gradio component styling improvements */
    .gradio-container {
        max-width: 1400px !important;
    }
    
    .tabs {
        border-radius: 8px;
        overflow: hidden;
    }
    """
    
    # Create Gradio interface
    with gr.Blocks(title="Divine Book Browser", css=custom_css) as interface:
        gr.Markdown(
            """# 📚 Divine Book Browser
            
            Explore sacred texts from the repository and analyze them for resonance patterns and universal alignments.
            
            Browse the repository structure, select a document, then adjust the resonance weights and analyze!
            """
        )
        
        with gr.Tabs() as tabs:
            with gr.TabItem("Document Explorer"):
                with gr.Row(equal_height=False):
                    with gr.Column(scale=1):
                        # File browser and text input
                        file_count = len(MARKDOWN_FILES)
                        sorted_files = sorted(MARKDOWN_FILES.keys())
                        
                        # Make the file tree taller and more visually prominent
                        file_tree_html = gr.HTML(
                            render_file_tree(), 
                            label="Repository Structure"
                        )
                        
                        # Improve the dropdown styling with height and width
                        sample_dropdown = gr.Dropdown(
                            choices=sorted_files,
                            label=f"Repository Markdown Files ({file_count} files)",
                            info="Select a Markdown file from the repository",
                            value=None,
                            container=True
                        )
                        
                    with gr.Column(scale=2):
                        # Markdown preview and raw text - make this section larger
                        with gr.Tabs() as preview_tabs:
                            with gr.TabItem("Rendered Preview"):
                                # Increase height to give more space to preview
                                html_preview = gr.HTML(
                                    value="<div class='md-preview'>Select a document to preview it here...</div>",
                                    label="Preview"
                                )
                            
                            with gr.TabItem("Raw Markdown"):
                                # Make the text box larger as well
                                text_input = gr.Textbox(
                                    label="Markdown Text",
                                    placeholder="Select a document or enter text here...",
                                    lines=25,  # Increase number of visible lines
                                    max_lines=40  # Allow more expansion
                                )
                
                # Set up event handler for file selection
                sample_dropdown.change(
                    load_selected_file,
                    inputs=sample_dropdown,
                    outputs=[text_input, html_preview]
                )
            
            with gr.TabItem("Resonance Analysis"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### Resonance Weights")
                        with gr.Row():
                            with gr.Column(scale=1):
                                golden_ratio_weight = gr.Slider(
                                    minimum=0, maximum=1, value=0.5, step=0.05,
                                    label="Golden Ratio Weight"
                                )
                                fibonacci_weight = gr.Slider(
                                    minimum=0, maximum=1, value=0.5, step=0.05,
                                    label="Fibonacci Weight"
                                )
                                schumann_weight = gr.Slider(
                                    minimum=0, maximum=1, value=0.5, step=0.05,
                                    label="Schumann Resonance Weight"
                                )
                            
                            with gr.Column(scale=1):
                                lunar_weight = gr.Slider(
                                    minimum=0, maximum=1, value=0.5, step=0.05,
                                    label="Lunar Cycle Weight"
                                )
                                solar_weight = gr.Slider(
                                    minimum=0, maximum=1, value=0.5, step=0.05,
                                    label="Solar Cycle Weight"
                                )
                        
                        analyze_btn = gr.Button("✨ Analyze Divine Resonance", variant="primary")
                
                with gr.Row():
                    with gr.Column():
                        resonance_score = gr.Number(label="Overall Resonance Score", precision=2)
                
                with gr.Tabs():
                    with gr.TabItem("Interpretation"):
                        interpretation = gr.Markdown()
                    
                    with gr.TabItem("Pattern Visualizations"):
                        with gr.Row():
                            bar_chart = gr.Image(label="Pattern Distribution")
                            radar_chart = gr.Image(label="Pattern Radar")
        
        # Set up analyze button event handler
        analyze_btn.click(
            analyze_text,
            inputs=[
                text_input,
                golden_ratio_weight,
                fibonacci_weight,
                schumann_weight,
                lunar_weight,
                solar_weight
            ],
            outputs=[
                resonance_score,
                interpretation,
                interpretation,
                bar_chart,
                radar_chart
            ]
        )
        
        # Add information about the tool
        gr.Markdown(
            """
            ### About Divine Resonance
            
            Sacred texts throughout history have demonstrated unique mathematical properties and vibrational resonance with cosmic patterns.
            This tool analyzes text for alignment with universal constants and sacred geometry, including:
            
            - Golden Ratio (φ ≈ 1.618) alignment
            - Fibonacci sequence patterns
            - Schumann resonance (7.83 Hz)
            - Lunar and solar cycles
            - Sacred numerical patterns
            
            The visualization tools help identify how your selected texts resonate with these universal patterns.
            """
        )
    
    return interface

def main():
    # Get share parameter from environment if available
    share_app = os.environ.get("GRADIO_SHARE", "false").lower() == "true"
    
    # Create and launch the dashboard
    dashboard = create_dashboard()
    
    print(f"Starting Divine Book Browser Dashboard (Sharing: {'Enabled' if share_app else 'Disabled'})")
    print(f"Loaded {len(MARKDOWN_FILES)} Markdown files from repository")
    dashboard.launch(share=share_app)

if __name__ == "__main__":
    main() 