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
Fractal Mermaid Compiler
=======================

Transforms Mermaid diagrams into fractal patterns during compilation.
When compiled with -03 flag, the diagram becomes a fractal structure.
"""

import re
import sys
import random
from typing import List, Dict, Tuple
import math

class FractalMermaidCompiler:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.fractal_depth = 3
        self.fractal_angle = 60
        self.colors = {
            'start': '#4CAF50',  # Green
            'end': '#F44336',    # Red
            'state': '#2196F3',  # Blue
            'edge': '#9C27B0',   # Purple
            'text': '#212121',   # Dark Gray
            'background': '#FFFFFF'  # White
        }
        
    def parse_mermaid(self, mermaid_text: str) -> None:
        """Parse Mermaid diagram text into nodes and edges."""
        # Remove comments and empty lines
        lines = [line.strip() for line in mermaid_text.split('\n') 
                if line.strip() and not line.strip().startswith('%')]
        
        # Skip the stateDiagram-v2 line if present
        if lines and lines[0].startswith('stateDiagram'):
            lines = lines[1:]
        
        # Extract nodes and edges
        for line in lines:
            if '-->' in line:
                # Parse edge
                parts = line.split('-->')
                source = parts[0].strip()
                target = parts[1].strip()
                
                # Handle labels
                if ':' in target:
                    target, label = target.split(':', 1)
                    target = target.strip()
                    label = label.strip()
                else:
                    label = None
                
                self.edges.append((source, target, label))
                
                # Add nodes if they don't exist
                if source not in self.nodes:
                    self.nodes[source] = {'type': 'state', 'x': 0, 'y': 0}
                if target not in self.nodes:
                    self.nodes[target] = {'type': 'state', 'x': 0, 'y': 0}
            
            elif line.startswith('[*]'):
                # Handle start/end states
                if '-->' in lines[lines.index(line) + 1]:
                    self.nodes['[*]'] = {'type': 'start', 'x': 0, 'y': 0}
                else:
                    self.nodes['[*]'] = {'type': 'end', 'x': 0, 'y': 0}
    
    def generate_fractal(self, node: str, depth: int, angle: float, 
                        x: float, y: float, length: float) -> List[Tuple[float, float, str]]:
        """Generate fractal pattern for a node."""
        points = []
        
        if depth <= 0:
            return points
            
        # Calculate new points
        new_length = length * 0.7
        angle_rad = math.radians(angle)
        
        # Forward point
        x1 = x + length * math.cos(angle_rad)
        y1 = y + length * math.sin(angle_rad)
        points.append((x1, y1, node))
        
        # Find connected nodes
        connected_nodes = [(s, t) for s, t, _ in self.edges if s == node]
        
        if connected_nodes:
            # Calculate angles for branches
            angle_step = self.fractal_angle / len(connected_nodes)
            current_angle = angle - (self.fractal_angle / 2)
            
            for source, target in connected_nodes:
                # Generate fractal for connected node
                branch_points = self.generate_fractal(
                    target, depth - 1, current_angle, x1, y1, new_length
                )
                points.extend(branch_points)
                current_angle += angle_step
        else:
            # If no connected nodes, create decorative branches
            left_angle = angle - self.fractal_angle
            right_angle = angle + self.fractal_angle
            
            left_points = self.generate_fractal(node, depth - 1, left_angle, x1, y1, new_length)
            right_points = self.generate_fractal(node, depth - 1, right_angle, x1, y1, new_length)
            
            points.extend(left_points)
            points.extend(right_points)
        
        return points
    
    def compile_to_fractal(self) -> str:
        """Compile the diagram into a fractal pattern."""
        output = []
        
        # Start SVG with background
        output.append('<?xml version="1.0" encoding="UTF-8"?>')
        output.append(f'<svg width="1200" height="800" xmlns="http://www.w3.org/2000/svg">')
        output.append(f'<rect width="100%" height="100%" fill="{self.colors["background"]}"/>')
        
        # Add definitions for gradients and filters
        output.append('<defs>')
        # Gradient for paths
        output.append('''
            <linearGradient id="fractalGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#2196F3;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#9C27B0;stop-opacity:1" />
            </linearGradient>
        ''')
        # Glow filter
        output.append('''
            <filter id="glow">
                <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                <feMerge>
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        ''')
        output.append('</defs>')
        
        # Generate fractal patterns for each start node
        start_x, start_y = 600, 400  # Center of SVG
        
        # Find start nodes
        start_nodes = [node for node, props in self.nodes.items() if props['type'] == 'start']
        
        for start_node in start_nodes:
            # Generate main fractal pattern
            points = self.generate_fractal(start_node, self.fractal_depth, 90, start_x, start_y, 100)
            
            # Draw the fractal pattern
            if points:
                # Create the main path
                path_data = f"M {start_x} {start_y}"
                prev_x, prev_y = start_x, start_y
                
                for x, y, node in points:
                    path_data += f" L {x} {y}"
                    
                    # Store node position for labels
                    self.nodes[node]['x'] = x
                    self.nodes[node]['y'] = y
                    
                    # Add decorative elements
                    output.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{self.colors["state"]}" filter="url(#glow)"/>')
                    
                    # Add connecting line with gradient
                    output.append(f'''
                        <path d="M {prev_x} {prev_y} L {x} {y}"
                              stroke="url(#fractalGradient)"
                              stroke-width="2"
                              stroke-opacity="0.6"
                              fill="none"
                              filter="url(#glow)"/>
                    ''')
                    
                    prev_x, prev_y = x, y
                
                # Draw the main fractal path
                output.append(f'''
                    <path d="{path_data}"
                          stroke="{self.colors['edge']}"
                          stroke-width="1.5"
                          fill="none"
                          opacity="0.4"
                          filter="url(#glow)"/>
                ''')
        
        # Add node labels with better positioning
        for node, props in self.nodes.items():
            if 'x' in props and 'y' in props:
                # Add background for text
                output.append(f'''
                    <rect x="{props['x'] - 40}" y="{props['y'] - 15}"
                          width="80" height="20"
                          fill="white"
                          fill-opacity="0.8"
                          rx="5" ry="5"/>
                ''')
                
                # Add text
                output.append(f'''
                    <text x="{props['x']}" y="{props['y']}"
                          text-anchor="middle"
                          dominant-baseline="middle"
                          fill="{self.colors['text']}"
                          font-family="Arial"
                          font-size="10px">{node}</text>
                ''')
        
        # Close SVG
        output.append('</svg>')
        
        return '\n'.join(output)

def main():
    """Main function to compile Mermaid to fractal."""
    # Read input from stdin
    mermaid_text = sys.stdin.read()
    
    # Create compiler
    compiler = FractalMermaidCompiler()
    
    # Parse Mermaid diagram
    compiler.parse_mermaid(mermaid_text)
    
    # Compile to fractal
    fractal_svg = compiler.compile_to_fractal()
    
    # Output SVG
    print(fractal_svg)

if __name__ == "__main__":
    main() 