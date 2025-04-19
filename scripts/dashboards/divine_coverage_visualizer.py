#!/usr/bin/env python3

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
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
OMEGA CUSTOM PYTEST COVERAGE 3D REPORT
--------------------------------------
Divine Visualization System for Test Coverage Analysis
Implementing Agile Quantum Testing Principles

This module creates a 3D cosmic visualization of test coverage,
respecting the divine balance of the code universe.
"""

import os
import json
import sys
import subprocess
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.colors as mcolors
import webbrowser

# ANSI colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Quantum constants
PLANCK_CONSTANT = 6.62607015e-34
GOLDEN_RATIO = (1 + np.sqrt(5)) / 2
FIBONACCI_SEQUENCE = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

def print_cosmic_banner():
    """Display a cosmic banner for the visualization process."""
    print(f"{MAGENTA}{BOLD}╔══════════════════════════════════════════════════════════╗{RESET}")
    print(f"{MAGENTA}{BOLD}║        OMEGA CUSTOM PYTEST COVERAGE 3D REPORT           ║{RESET}")
    print(f"{MAGENTA}{BOLD}║     🧠 DIVINE QUANTUM VISUALIZATION SYSTEM 🧠           ║{RESET}")
    print(f"{MAGENTA}{BOLD}╚══════════════════════════════════════════════════════════╝{RESET}")
    print(f"{YELLOW}Manifesting the sacred patterns of code coverage...{RESET}")
    print()

def generate_coverage_data():
    """Generate coverage data using pytest and coverage modules."""
    print(f"{CYAN}Initializing quantum observation of code coverage...{RESET}")
    
    # Run pytest with coverage on target modules
    subprocess.run(
        ["python", "-m", "pytest", 
         "omega_ai/tests/monitor/", 
         "--cov=omega_ai/monitor", 
         "--cov-config=.coveragerc",
         "--no-header",
         "-v"],
        capture_output=True
    )
    
    # Export coverage data to JSON for visualization
    subprocess.run(
        ["coverage", "json", "-o", ".coverage_data.json"],
        capture_output=True
    )
    
    print(f"{GREEN}Coverage data quantum state observed and recorded.{RESET}")
    
    # Load the coverage data from JSON
    try:
        with open(".coverage_data.json", "r") as f:
            coverage_data = json.load(f)
        return coverage_data
    except FileNotFoundError:
        print(f"{RED}Error: Coverage data file not found. Ensure pytest and coverage are installed.{RESET}")
        print(f"{YELLOW}Install with: pip install pytest pytest-cov coverage plotly pandas numpy matplotlib{RESET}")
        sys.exit(1)

def process_coverage_data(coverage_data):
    """Process coverage data into a format suitable for visualization."""
    print(f"{CYAN}Processing quantum coverage patterns...{RESET}")
    
    modules = []
    
    for filename, file_data in coverage_data.get("files", {}).items():
        if "omega_ai/monitor" in filename:
            module_name = os.path.basename(filename)
            
            # Extract coverage metrics
            total_lines = file_data.get("summary", {}).get("num_statements", 0)
            covered_lines = total_lines - file_data.get("summary", {}).get("missing_lines", 0)
            coverage_pct = file_data.get("summary", {}).get("percent_covered", 0)
            
            # Extract line-level details
            lines_covered = file_data.get("executed_lines", [])
            lines_missing = file_data.get("missing_lines", [])
            
            # Calculate code complexity (simple metric: lines per function)
            # Fix: Count number of functions by estimating from line ranges
            executed_lines = file_data.get("executed_lines", [])
            missing_lines = file_data.get("missing_lines", [])
            all_lines = sorted(executed_lines + missing_lines)
            
            # Estimate number of functions by looking at groups of consecutive lines
            if all_lines:
                # Identify gaps in line numbers to estimate function boundaries
                gaps = []
                for i in range(1, len(all_lines)):
                    if all_lines[i] - all_lines[i-1] > 5:  # If gap is more than 5 lines, likely new function
                        gaps.append(i)
                num_functions = len(gaps) + 1  # Number of functions is number of gaps + 1
                num_functions = max(1, num_functions)  # Ensure at least 1 function
            else:
                num_functions = 1
                
            complexity = total_lines / max(1, num_functions) / 5  # Normalized
            
            # Calculate quantum entropy (measure of code organization)
            # Higher entropy = less organized code
            if total_lines > 0:
                missing_ratio = len(lines_missing) / total_lines
                entropy = -missing_ratio * np.log2(missing_ratio + 0.00001) if missing_ratio > 0 else 0
            else:
                entropy = 0
                
            # Fibonacci alignment score (how well the coverage aligns with Fibonacci sequence)
            closest_fib = min(FIBONACCI_SEQUENCE, key=lambda x: abs(x - total_lines))
            fib_alignment = 1 - (abs(total_lines - closest_fib) / max(total_lines, 1))
            
            modules.append({
                'module': module_name,
                'coverage': coverage_pct,
                'lines': total_lines,
                'complexity': complexity,
                'entropy': entropy * 10,  # Scale for visualization
                'covered_lines': len(lines_covered),
                'fib_alignment': fib_alignment * 10,  # Scale for visualization
                'missing_lines': len(lines_missing)
            })
    
    df = pd.DataFrame(modules)
    print(f"{GREEN}Quantum state processing complete: {len(modules)} modules analyzed.{RESET}")
    return df

def create_3d_coverage_visualization(df):
    """Create the 3D visualization of coverage data."""
    print(f"{CYAN}Manifesting the Divine Coverage Matrix...{RESET}")
    
    # Calculate optimal marker sizing
    max_lines = df['lines'].max()
    df['marker_size'] = df['lines'] / max(1, max_lines) * 30 + 10
    
    # Create color map based on coverage
    df['color'] = df['coverage'] / 100
    
    # Create main 3D scatter plot
    fig = go.Figure()
    
    # Add main data points
    fig.add_trace(go.Scatter3d(
        x=df['coverage'],
        y=df['complexity'],
        z=df['entropy'],
        mode='markers',
        marker=dict(
            size=df['marker_size'],
            color=df['color'],
            colorscale='Viridis',
            opacity=0.8,
            colorbar=dict(
                title="Coverage %",
                tickvals=[0, 0.25, 0.5, 0.75, 1],
                ticktext=["0%", "25%", "50%", "75%", "100%"]
            ),
        ),
        text=df['module'],
        hovertemplate=
        "<b>%{text}</b><br>" +
        "Coverage: %{x:.2f}%<br>" +
        "Complexity: %{y:.2f}<br>" +
        "Entropy: %{z:.2f}<br>" +
        "Lines: %{marker.size:.0f}<br>" +
        "Missing Lines: %{customdata[0]}<br>" +
        "Fibonacci Alignment: %{customdata[1]:.2f}<br>",
        customdata=np.vstack((df['missing_lines'], df['fib_alignment'])).T,
        name="Modules"
    ))
    
    # Add sacred Fibonacci spiral
    theta = np.linspace(0, 6*np.pi, 200)
    r = GOLDEN_RATIO ** (theta/(2*np.pi))
    
    # Scale to reasonable values for the plot
    x_fib = r * np.cos(theta) * 25 + 50  # Center at 50% coverage
    y_fib = r * np.sin(theta) * 2 + 5    # Center in complexity range
    z_fib = np.sin(theta * GOLDEN_RATIO) * 5 + 5  # Undulate through entropy space
    
    fig.add_trace(go.Scatter3d(
        x=x_fib, y=y_fib, z=z_fib,
        mode='lines',
        line=dict(
            color='gold',
            width=5
        ),
        opacity=0.7,
        name="Divine Fibonacci Path"
    ))
    
    # Add quantum field indicators (radial waves emanating from high coverage points)
    if not df.empty and len(df) > 0:
        # Find high coverage module
        high_coverage = df.loc[df['coverage'].idxmax()]
        
        # Create quantum field
        u = np.linspace(0, 2*np.pi, 30)
        v = np.linspace(0, np.pi, 30)
        radius = min(high_coverage['coverage'] / 200 + 0.1, 0.3)  # Scaled radius
        
        x_sphere = high_coverage['coverage'] + radius * np.outer(np.cos(u), np.sin(v))
        y_sphere = high_coverage['complexity'] + radius * np.outer(np.sin(u), np.sin(v))
        z_sphere = high_coverage['entropy'] + radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Add quantum field sphere
        fig.add_trace(go.Surface(
            x=x_sphere,
            y=y_sphere,
            z=z_sphere,
            colorscale=[[0, 'rgba(255, 215, 0, 0.1)'], [1, 'rgba(255, 215, 0, 0.3)']],
            showscale=False,
            name="Quantum Field"
        ))
    
    # Update layout with cosmic theme
    fig.update_layout(
        title={
            'text': "OMEGA DIVINE COVERAGE MATRIX",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24, 'color': '#7F3FBF'}
        },
        scene=dict(
            xaxis_title='Coverage (%)',
            yaxis_title='Code Complexity',
            zaxis_title='Quantum Entropy',
            xaxis=dict(range=[0, 100], backgroundcolor="#f0f0f0"),
            yaxis=dict(backgroundcolor="#f0f0f0"),
            zaxis=dict(backgroundcolor="#f0f0f0"),
            camera=dict(
                eye=dict(x=1.8, y=1.8, z=1.8)
            )
        ),
        legend=dict(
            x=0.01,
            y=0.99,
            bgcolor='rgba(255, 255, 255, 0.5)'
        ),
        width=1200,
        height=900,
        margin=dict(l=0, r=0, b=0, t=30),
        paper_bgcolor='#FFFFFF',
        template="plotly_dark"
    )
    
    # Add timestamp and project info
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fig.add_annotation(
        x=0.01,
        y=0.01,
        xref="paper",
        yref="paper",
        text=f"Generated: {timestamp} | OMEGA BTC AI",
        showarrow=False,
        font=dict(size=10, color="#888888"),
        align="left"
    )
    
    # Add helper text
    fig.add_annotation(
        x=0.99,
        y=0.01,
        xref="paper",
        yref="paper",
        text="Use mouse to rotate, scroll to zoom",
        showarrow=False,
        font=dict(size=10, color="#888888"),
        align="right"
    )
    
    # Create additional summary plots
    return fig, df

def create_2d_supplementary_plots(df):
    """Create additional 2D plots to supplement the 3D visualization."""
    plots = []
    
    # Coverage Distribution Sunburst
    fig1 = px.sunburst(
        df,
        path=['module'],
        values='lines',
        color='coverage',
        color_continuous_scale='RdYlGn',
        range_color=[0, 100],
        hover_data=['coverage', 'lines', 'missing_lines'],
        title="Coverage Distribution by Module"
    )
    fig1.update_layout(width=600, height=600)
    plots.append(fig1)
    
    # Cosmic Balance Chart (radar chart)
    if not df.empty:
        categories = ['Coverage', 'Complexity', 'Entropy', 'Fibonacci Alignment']
        
        fig2 = go.Figure()
        
        for i, row in df.iterrows():
            # Normalize values to 0-1 range for radar chart
            coverage_norm = row['coverage'] / 100
            complexity_norm = row['complexity'] / df['complexity'].max()
            entropy_norm = row['entropy'] / df['entropy'].max() if df['entropy'].max() > 0 else 0
            fib_norm = row['fib_alignment'] / 10
            
            fig2.add_trace(go.Scatterpolar(
                r=[coverage_norm, complexity_norm, entropy_norm, fib_norm],
                theta=categories,
                fill='toself',
                name=row['module'],
                opacity=0.7
            ))
        
        fig2.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Cosmic Balance of Modules",
            width=600,
            height=600
        )
        plots.append(fig2)
    
    return plots

def save_visualization(main_fig, supplementary_figs, df):
    """Save the visualization to an HTML file with all plots."""
    print(f"{CYAN}Creating sacred HTML document...{RESET}")
    
    # Create a custom HTML file with all visualizations
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"omega_divine_coverage_{timestamp}.html"
    
    # Create a dedicated directory for this visualization
    viz_dir = f"omega_viz_{timestamp}"
    os.makedirs(viz_dir, exist_ok=True)
    
    # Save main figure to visualization directory
    main_html_file = f"{viz_dir}/main_figure.html"
    main_fig.write_html(main_html_file, include_plotlyjs="cdn")
    
    # Save supplementary figures to visualization directory
    supp_html_files = []
    for i, fig in enumerate(supplementary_figs):
        html_file = f"{viz_dir}/supp_figure_{i}.html"
        fig.write_html(html_file, include_plotlyjs="cdn")
        supp_html_files.append(html_file)
    
    # Create a summary table
    table_html = """
    <div class="summary-table">
        <h2>DIVINE COVERAGE SUMMARY</h2>
        <table>
            <tr>
                <th>Module</th>
                <th>Coverage (%)</th>
                <th>Lines</th>
                <th>Missing</th>
                <th>Quantum State</th>
            </tr>
    """
    
    # Add rows for each module
    for i, row in df.iterrows():
        coverage = row['coverage']
        if coverage >= 80:
            quantum_state = "🟢 Divine Harmony"
            color = "#00AA00"
        elif coverage >= 50:
            quantum_state = "🟡 Cosmic Balance"
            color = "#AAAA00"
        elif coverage >= 20:
            quantum_state = "🟠 Quantum Flux"
            color = "#AA5500"
        else:
            quantum_state = "🔴 Void State"
            color = "#AA0000"
            
        table_html += f"""
        <tr>
            <td>{row['module']}</td>
            <td style="color: {color}; font-weight: bold;">{row['coverage']:.2f}%</td>
            <td>{int(row['lines'])}</td>
            <td>{int(row['missing_lines'])}</td>
            <td>{quantum_state}</td>
        </tr>
        """
    
    # Close table
    table_html += """
        </table>
    </div>
    """
    
    # These are the paths that will be used in iframes - they must be relative to the HTML file
    main_iframe_src = os.path.basename(viz_dir) + "/main_figure.html"
    supp_iframe_srcs = [os.path.basename(viz_dir) + f"/supp_figure_{i}.html" for i in range(len(supplementary_figs))]
    
    # Create the full HTML document
    with open(output_file, "w") as f:
        f.write(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>OMEGA DIVINE COVERAGE VISUALIZATION</title>
            <style>
                body {{
                    font-family: 'Helvetica Neue', Arial, sans-serif;
                    background-color: #121212;
                    color: #E0E0E0;
                    margin: 0;
                    padding: 0;
                }}
                
                .header {{
                    background: linear-gradient(135deg, #4A148C, #311B92);
                    color: white;
                    text-align: center;
                    padding: 20px;
                    margin-bottom: 20px;
                    border-bottom: 4px solid #7B1FA2;
                }}
                
                .main-container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                
                .visualization-container {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                
                .main-visualization {{
                    width: 100%;
                    margin-bottom: 20px;
                    background-color: #1E1E1E;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                }}
                
                .supplementary-visualization {{
                    flex: 1;
                    min-width: 400px;
                    background-color: #1E1E1E;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                }}
                
                .summary-table {{
                    background-color: #1E1E1E;
                    border-radius: 8px;
                    padding: 20px;
                    margin-bottom: 30px;
                    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                }}
                
                .summary-table h2 {{
                    text-align: center;
                    color: #7B1FA2;
                    margin-top: 0;
                }}
                
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                
                th, td {{
                    border: 1px solid #333;
                    padding: 12px;
                    text-align: left;
                }}
                
                th {{
                    background-color: #2A2A2A;
                    color: #BB86FC;
                }}
                
                tr:nth-child(even) {{
                    background-color: #252525;
                }}
                
                footer {{
                    text-align: center;
                    padding: 20px;
                    font-size: 12px;
                    color: #888;
                    border-top: 1px solid #333;
                }}
                
                .cosmic-quote {{
                    font-style: italic;
                    text-align: center;
                    padding: 20px;
                    color: #BB86FC;
                    font-size: 18px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>OMEGA DIVINE COVERAGE VISUALIZATION</h1>
                <p>Agile Quantum Testing Analysis | Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
            
            <div class="main-container">
                <div class="cosmic-quote">
                    "JAH BLESS the processing path. This assembly is not mechanical—it's rhythmic."
                </div>
                
                {table_html}
                
                <div class="main-visualization">
                    <iframe src="{main_iframe_src}" width="100%" height="800px" frameborder="0"></iframe>
                </div>
                
                <div class="visualization-container">
        """)
        
        # Add supplementary visualizations
        for i, iframe_src in enumerate(supp_iframe_srcs):
            f.write(f"""
                    <div class="supplementary-visualization">
                        <iframe src="{iframe_src}" width="100%" height="600px" frameborder="0"></iframe>
                    </div>
            """)
        
        f.write(f"""
                </div>
                
                <div class="cosmic-quote">
                    "In the quantum realm of code, coverage is but one dimension of the divine matrix."
                </div>
            </div>
            
            <footer>
                OMEGA BTC AI | Divine Coverage Visualization | TDD • QA • Agile Quantum Testing
            </footer>
        </body>
        </html>
        """)
    
    # Create a README file in the visualization directory
    with open(f"{viz_dir}/README.txt", "w") as f:
        f.write(f"OMEGA BTC AI - Divine Coverage Visualization\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Main Visualization: {output_file}\n")
        f.write(f"Components:\n")
        f.write(f"- Main figure: {main_html_file}\n")
        for i, html_file in enumerate(supp_html_files):
            f.write(f"- Supplementary figure {i+1}: {html_file}\n")
    
    # Open the visualization in the browser
    webbrowser.open(os.path.abspath(output_file))
    
    print(f"{GREEN}{BOLD}Divine Visualization Manifested: {output_file}{RESET}")
    print(f"{CYAN}A browser window should open automatically to display the visualization.{RESET}")
    print(f"{YELLOW}All visualization files are stored in: {viz_dir}/{RESET}")
    
    return output_file

def main():
    """Main function to generate the 3D coverage visualization."""
    print_cosmic_banner()
    
    # Generate coverage data
    coverage_data = generate_coverage_data()
    
    # Process the data
    df = process_coverage_data(coverage_data)
    
    # Create 3D visualization
    main_fig, df = create_3d_coverage_visualization(df)
    
    # Create supplementary 2D plots
    supplementary_figs = create_2d_supplementary_plots(df)
    
    # Save the visualization
    output_file = save_visualization(main_fig, supplementary_figs, df)
    
    # Coverage data file can be removed
    try:
        os.remove(".coverage_data.json")
    except:
        pass
    
    print(f"{MAGENTA}{BOLD}DIVINE VISUALIZATION COMPLETE{RESET}")
    print(f"{YELLOW}May your tests be cosmic and your coverage divine.{RESET}")

if __name__ == "__main__":
    main() 