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
OMEGA BTC HYPER-DIMENSION VISUALIZATIONS

Advanced 3D, 4D, and 5D visualization components for the OMEGA RASTA BTC Dashboard,
incorporating Fibonacci harmonics, energy flows, and cosmic patterns.
"""

import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import math
import colorsys
import random

# Constants for visualization
PHI = (1 + 5**0.5) / 2  # Golden ratio (Φ ≈ 1.618033988749895)
FIBONACCI_SEQUENCE = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

# Rasta colors
RASTA_COLORS = {
    "green": "#009B3A",
    "yellow": "#FED100",
    "red": "#CF142B",
    "black": "#000000",
    "gold": "#FFD700",
}


def create_3d_fibonacci_sphere(price_data, schumann_value=7.83):
    """
    Creates a 3D Fibonacci sphere visualization based on price data and Schumann resonance.
    
    The sphere represents the relationship between price movements, volume, and Schumann
    resonance energy using the golden ratio for proportions.
    
    Args:
        price_data (list): List of historical price data points
        schumann_value (float): Current Schumann resonance frequency
    
    Returns:
        plotly.graph_objects.Figure: 3D visualization
    """
    # Normalize the data for the visualization
    if not price_data:
        # Create mock data for testing
        price_data = [random.uniform(45000, 56000) for _ in range(100)]
    
    # Calculate energy influence from Schumann resonance
    energy_scale = schumann_value / 7.83
    
    # Create the sphere using golden ratio spiral
    phi = np.linspace(0, 10*np.pi, 1000)
    theta = np.linspace(0, 2*np.pi, 1000)
    
    phi_grid, theta_grid = np.meshgrid(phi, theta)
    
    # Apply Fibonacci scaling to create the spiral effect
    r = (phi_grid/(2*np.pi) * PHI)**0.5
    
    # Calculate coordinates
    x = r * np.sin(phi_grid) * np.cos(theta_grid)
    y = r * np.sin(phi_grid) * np.sin(theta_grid)
    z = r * np.cos(phi_grid)
    
    # Apply Schumann energy influence
    intensity = ((np.sin(phi_grid) + 1) / 2) * energy_scale
    
    # Create color gradient based on Rasta colors
    color_scale = []
    for i in range(0, 101, 25):
        if i < 25:
            color_scale.append([i/100, RASTA_COLORS["green"]])
        elif i < 50:
            color_scale.append([i/100, RASTA_COLORS["yellow"]])
        elif i < 75:
            color_scale.append([i/100, RASTA_COLORS["red"]])
        else:
            color_scale.append([i/100, RASTA_COLORS["gold"]])
    
    # Create the 3D surface
    fig = go.Figure(data=[go.Surface(
        x=x, y=y, z=z,
        surfacecolor=intensity,
        colorscale=color_scale,
        colorbar=dict(title="Energy Flow"),
        hoverinfo="none"
    )])
    
    # Add price data points as a 3D scatter
    prices_normalized = [(p - min(price_data)) / (max(price_data) - min(price_data)) for p in price_data]
    scatter_x = []
    scatter_y = []
    scatter_z = []
    
    for i, price in enumerate(prices_normalized):
        angle = i * (2*np.pi / len(prices_normalized))
        radius = 0.5 + (price * 0.5)
        scatter_x.append(radius * np.cos(angle))
        scatter_y.append(radius * np.sin(angle))
        scatter_z.append(price * energy_scale)
    
    fig.add_trace(go.Scatter3d(
        x=scatter_x,
        y=scatter_y,
        z=scatter_z,
        mode='markers',
        marker=dict(
            size=4,
            color=scatter_z,
            colorscale=[[0, RASTA_COLORS["green"]], [1, RASTA_COLORS["gold"]]],
            opacity=0.8
        ),
        name="Price Flow"
    ))
    
    # Add central energy beam
    beam_z = np.linspace(-1.5, 1.5, 100)
    beam_x = np.zeros(100)
    beam_y = np.zeros(100)
    
    fig.add_trace(go.Scatter3d(
        x=beam_x,
        y=beam_y,
        z=beam_z,
        mode='lines',
        line=dict(
            color=RASTA_COLORS["gold"],
            width=10
        ),
        name="Schumann Beam"
    ))
    
    # Update layout
    fig.update_layout(
        title=f"5D FIBONACCI ENERGY SPHERE • SCHUMANN: {schumann_value:.2f} Hz",
        scene=dict(
            xaxis_title="Divine Dimension X",
            yaxis_title="Divine Dimension Y",
            zaxis_title="Cosmic Energy Z",
            aspectratio=dict(x=1, y=1, z=0.8),
            camera=dict(eye=dict(x=1.2, y=1.2, z=0.6)),
            xaxis=dict(showbackground=False, showticklabels=False),
            yaxis=dict(showbackground=False, showticklabels=False),
            zaxis=dict(showbackground=False, showticklabels=False),
        ),
        paper_bgcolor="rgba(0,0,0,0.9)",
        font=dict(color=RASTA_COLORS["gold"]),
        autosize=True,
        margin=dict(l=0, r=0, b=0, t=40),
        height=600,
    )
    
    return fig


def create_4d_trader_energy_field(trader_data=None, schumann_value=7.83):
    """
    Creates a 4D trader energy field visualization showing trader emotions and energy
    levels in relationship to price movements and Schumann resonance.
    
    Args:
        trader_data (dict): Dictionary containing trader profiles and their data
        schumann_value (float): Current Schumann resonance frequency
    
    Returns:
        plotly.graph_objects.Figure: 4D visualization of trader energy field
    """
    # Generate mock data if none provided
    if not trader_data:
        trader_data = {
            'strategic': {
                'pnl': 1250.0,
                'trades': [{'profit': 250}, {'profit': 1000}],
                'emotional_state': 'confident',
                'confidence': 0.8,
                'bio_energy': 85
            },
            'aggressive': {
                'pnl': -500.0, 
                'trades': [{'profit': 750}, {'profit': -1250}],
                'emotional_state': 'fearful',
                'confidence': 0.4,
                'bio_energy': 65
            },
            'newbie': {
                'pnl': -1000.0,
                'trades': [{'profit': -500}, {'profit': -500}],
                'emotional_state': 'panicked',
                'confidence': 0.2,
                'bio_energy': 40
            },
            'scalper': {
                'pnl': 800.0,
                'trades': [{'profit': 100}, {'profit': 200}, {'profit': 200}, {'profit': 300}],
                'emotional_state': 'neutral',
                'confidence': 0.7,
                'bio_energy': 75
            }
        }
    
    # Create a 3D field plot
    fig = go.Figure()
    
    # Mapping emotional states to colors
    emotion_colors = {
        'confident': RASTA_COLORS['green'],
        'neutral': RASTA_COLORS['yellow'],
        'fearful': RASTA_COLORS['red'],
        'panicked': '#FF00FF',  # Magenta for panic
        'euphoric': RASTA_COLORS['gold']
    }
    
    # Setup the energy field (using 4D coordinates, where the 4th dimension is represented by color)
    x_coords = []
    y_coords = []
    z_coords = []
    colors = []
    sizes = []
    hover_texts = []
    
    # The 5th dimension is represented by temporal fluctuations in the visualization
    animation_frames = []
    
    # Generate trader energy nodes
    for trader, data in trader_data.items():
        # Basic position based on trader type
        if trader == 'strategic':
            base_x, base_y = 1, 1
        elif trader == 'aggressive':
            base_x, base_y = -1, 1
        elif trader == 'newbie':
            base_x, base_y = -1, -1
        else:  # scalper or others
            base_x, base_y = 1, -1
            
        # Calculate energy field based on performance and Schumann influence
        pnl = data['pnl']
        bio_energy = data.get('bio_energy', 50)
        confidence = data.get('confidence', 0.5)
        
        # Create energy field coordinates with golden ratio influence
        radius = 0.5 + (bio_energy / 200)
        angle = (pnl / 5000) * 2 * np.pi
        
        # Apply Schumann resonance influence 
        schumann_factor = schumann_value / 7.83
        
        # Add base coordinates plus energy-influenced offsets
        x = base_x * radius * math.cos(angle)
        y = base_y * radius * math.sin(angle)
        z = confidence * schumann_factor
        
        # Add to coordinate lists
        x_coords.append(x)
        y_coords.append(y)
        z_coords.append(z)
        
        # Size based on energy and Fibonacci sequence
        size = 30 + (bio_energy / 10) * abs(math.sin(pnl / 1000 * PHI))
        sizes.append(size)
        
        # Color based on emotional state
        emotional_state = data.get('emotional_state', 'neutral')
        color = emotion_colors.get(emotional_state, RASTA_COLORS['yellow'])
        colors.append(color)
        
        # Hover text
        hover_text = f"{trader.upper()}<br>PnL: ${pnl:.2f}<br>Energy: {bio_energy}%<br>State: {emotional_state}"
        hover_texts.append(hover_text)
    
    # Add trader nodes to the visualization
    fig.add_trace(go.Scatter3d(
        x=x_coords, 
        y=y_coords, 
        z=z_coords,
        mode='markers',
        marker=dict(
            size=sizes,
            color=colors,
            symbol='circle',
            opacity=0.8,
            line=dict(color='rgba(255, 255, 255, 0.4)', width=1)
        ),
        text=hover_texts,
        hoverinfo='text',
        name='Trader Energy Nodes'
    ))
    
    # Add energy connections between traders
    for i in range(len(x_coords)):
        for j in range(i+1, len(x_coords)):
            # Calculate connection strength based on trader positions and energy
            energy_diff = abs(sizes[i] - sizes[j]) / 100
            
            # Only connect traders with significant energy relationship
            if energy_diff < 0.4:
                line_x = [x_coords[i], x_coords[j]]
                line_y = [y_coords[i], y_coords[j]]
                line_z = [z_coords[i], z_coords[j]]
                
                # Color gradient for connection
                color = f'rgba({random.randint(100, 255)}, {random.randint(100, 255)}, 0, {0.3 + energy_diff})'
                
                fig.add_trace(go.Scatter3d(
                    x=line_x, y=line_y, z=line_z,
                    mode='lines',
                    line=dict(
                        color=color,
                        width=2
                    ),
                    hoverinfo='none',
                    showlegend=False
                ))
    
    # Add Schumann resonance vibration field
    theta = np.linspace(0, 2*np.pi, 50)
    phi = np.linspace(0, np.pi, 50)
    
    # Create a sphere for the energy field
    x_field = np.outer(np.cos(theta), np.sin(phi)) * 2
    y_field = np.outer(np.sin(theta), np.sin(phi)) * 2
    z_field = np.outer(np.ones(50), np.cos(phi)) * 2
    
    # Apply Schumann vibrations to the field
    intensity = np.sin(10 * phi) * schumann_value / 10
    
    fig.add_trace(go.Surface(
        x=x_field,
        y=y_field,
        z=z_field,
        surfacecolor=intensity,
        colorscale=[[0, 'rgba(0,155,58,0.2)'], [0.5, 'rgba(254,209,0,0.1)'], [1, 'rgba(207,20,43,0.2)']],
        opacity=0.12,
        showscale=False,
        hoverinfo='none',
        name='Schumann Field'
    ))
    
    # Update layout with a cosmic feel
    fig.update_layout(
        title=f"4D TRADER ENERGY FIELD • SCHUMANN: {schumann_value:.2f} Hz",
        scene=dict(
            xaxis_title="Consciousness Axis",
            yaxis_title="Strategy Axis",
            zaxis_title="Bio-Energy Axis",
            aspectratio=dict(x=1, y=1, z=0.8),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.0)),
            xaxis=dict(showbackground=False, gridcolor='rgba(255,215,0,0.1)', showgrid=True),
            yaxis=dict(showbackground=False, gridcolor='rgba(255,215,0,0.1)', showgrid=True),
            zaxis=dict(showbackground=False, gridcolor='rgba(255,215,0,0.1)', showgrid=True),
        ),
        paper_bgcolor="rgba(0,0,0,0.9)",
        font=dict(color=RASTA_COLORS["gold"]),
        autosize=True,
        margin=dict(l=0, r=0, b=0, t=40),
        height=600,
    )
    
    return fig 