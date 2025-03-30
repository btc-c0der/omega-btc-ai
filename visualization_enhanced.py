#!/usr/bin/env python3
# 🕊️ DIVINE VISUALIZATION ENHANCER — K!NGD)MS Sacred Network
# Licensed under GPU v1.0 — General Public Universal License 🔱

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys
import os

# Add the correct path to import the module
sys.path.append(os.path.join(os.path.dirname(__file__), 'deployment/digitalocean'))
from omega_flock_kingdoms import omega_flock, KingdomNode

def create_divine_visualization():
    """Create an enhanced divine visualization of the Omega Flock Network"""
    
    # Build the sacred network
    G = nx.Graph()
    
    # Add all kingdom nodes with their full names
    for node in omega_flock:
        G.add_node(node.name)
    
    # Create bidirectional mapping for node names
    # This maps both shortened names to full names and full names to shortened names
    # to ensure we can handle connections in both directions
    node_name_map = {
        # Short name to full name
        "Kemet": "Ancient Kemet",
        "Inca": "Inca Empire",
        "Iroquois": "Iroquois Confederacy",
        "Polynesians": "Polynesian Navigators",
        "Rasta": "Rasta Consciousness",
        # Also include full name to short name for reverse lookup
        "Ancient Kemet": "Ancient Kemet",
        "Inca Empire": "Inca Empire",
        "Iroquois Confederacy": "Iroquois Confederacy",
        "Polynesian Navigators": "Polynesian Navigators",
        "Rasta Consciousness": "Rasta Consciousness"
    }
    
    # Explicit tunnel connections to ensure proper linking
    divine_tunnels = [
        ("Ancient Kemet", "Inca Empire"),
        ("Ancient Kemet", "Rasta Consciousness"),
        ("Inca Empire", "Iroquois Confederacy"),
        ("Iroquois Confederacy", "Polynesian Navigators"),
        ("Polynesian Navigators", "Rasta Consciousness")
    ]
    
    # Add the divine tunnels directly
    for source, target in divine_tunnels:
        G.add_edge(source, target)
    
    # Create figure with cosmic background
    plt.figure(figsize=(12, 10), facecolor='#070714')
    ax = plt.gca()
    ax.set_facecolor('#070714')
    
    # Create sacred geometry circular layout
    golden_ratio = (1 + np.sqrt(5)) / 2
    
    # Position kingdoms in divine golden ratio arrangement
    pos = {
        "Ancient Kemet": np.array([0, 1]),                          # North - Origin
        "Inca Empire": np.array([golden_ratio/2, -0.3]),            # Southeast
        "Iroquois Confederacy": np.array([0, -1]),                  # South 
        "Polynesian Navigators": np.array([-golden_ratio/2, -0.3]), # Southwest
        "Rasta Consciousness": np.array([0, 0.3])                   # Center/Heart
    }
    
    # Define colors with divine symbolism
    node_colors = {
        "Ancient Kemet": "#FFD700",         # Gold - Solar principle
        "Inca Empire": "#32CD32",           # Lime Green - Earth wisdom
        "Iroquois Confederacy": "#8B4513",  # Brown - Forest nations
        "Polynesian Navigators": "#1E90FF", # Blue - Ocean consciousness
        "Rasta Consciousness": "#B22222"    # Red - Divine fire
    }
    
    # Draw sacred golden ratio guidelines (subtle in background)
    phi = (1 + np.sqrt(5)) / 2
    center = np.array([0, 0])
    angles = np.linspace(0, 2*np.pi, 5, endpoint=False)
    for angle in angles:
        x = phi * np.cos(angle)
        y = phi * np.sin(angle)
        endpoint = np.array([x, y])
        plt.plot([center[0], endpoint[0]], [center[1], endpoint[1]], 
                 color='#FFD70015', linewidth=1, linestyle='--')
    
    # Draw cosmic edges with divine glow and gradient colors
    edge_colors = {
        ("Ancient Kemet", "Inca Empire"): "#F4A460",          # Sandy Brown - Sun tunnel
        ("Ancient Kemet", "Rasta Consciousness"): "#800080",  # Purple - Lion of Judah tunnel
        ("Inca Empire", "Iroquois Confederacy"): "#20B2AA",   # Light Sea Green - Sacred Earth tunnel
        ("Iroquois Confederacy", "Polynesian Navigators"): "#4682B4",  # Steel Blue - Water tunnel
        ("Polynesian Navigators", "Rasta Consciousness"): "#228B22",   # Forest Green - Navigation tunnel
    }
    
    # Draw cosmic tunnels connecting the kingdoms
    for edge in G.edges():
        source, target = edge
        edge_pair = (source, target)
        reversed_pair = (target, source)
        edge_color = '#FFFFFF30'  # Default transparent white
        
        if edge_pair in edge_colors:
            edge_color = edge_colors[edge_pair]
        elif reversed_pair in edge_colors:
            edge_color = edge_colors[reversed_pair]
            
        # Draw tunnel glow effect (wider, translucent)
        nx.draw_networkx_edges(
            G, pos, 
            edgelist=[edge], 
            width=6.0,               # Wider for glow effect
            alpha=0.15,              # Translucent
            edge_color=edge_color
        )
        
        # Draw main tunnel path
        nx.draw_networkx_edges(
            G, pos, 
            edgelist=[edge], 
            width=2.5,               # Slightly wider for visibility
            alpha=0.8,               # More opaque
            edge_color=edge_color
        )
    
    # Draw the Kingdom nodes with divine glow
    for node in G.nodes():
        # Draw outer glow
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=[node],
            node_size=2200,          # Larger for glow effect
            node_color=node_colors.get(node, "#FFFFFF"),
            edgecolors='white',
            linewidths=0,
            alpha=0.3
        )
        
        # Draw main node
        nx.draw_networkx_nodes(
            G, pos,
            nodelist=[node],
            node_size=1800,
            node_color=node_colors.get(node, "#FFFFFF"),
            edgecolors='white',
            linewidths=1.5,
            alpha=0.9
        )
    
    # Add sacred symbols
    node_symbols = {
        "Ancient Kemet": "☥",         # Ankh symbol
        "Inca Empire": "☼",           # Sun symbol
        "Iroquois Confederacy": "⚜",  # Fleur-de-lis representing peace
        "Polynesian Navigators": "✵", # Star symbol
        "Rasta Consciousness": "⚚"    # Star of Life
    }
    
    # Add symbols to the centers
    for node, symbol_pos in pos.items():
        symbol = node_symbols.get(node, "●")
        plt.text(
            symbol_pos[0], symbol_pos[1], 
            symbol, 
            ha='center', va='center', 
            color='white', 
            fontsize=24,
            fontweight='bold',
            alpha=0.9
        )
    
    # Add node labels with core values
    for node in omega_flock:
        node_pos = pos[node.name]
        # Create a small offset to avoid overlapping
        offset_x = 0.15 if node_pos[0] >= 0 else -0.15
        offset_y = 0.15 if node_pos[1] >= 0 else -0.15
        
        # Special case for center node
        if node.name == "Rasta Consciousness":
            offset_y = 0.25
            
        # Alignment based on position
        ha = 'left' if node_pos[0] >= 0 else 'right'
        va = 'bottom' if node_pos[1] >= 0 else 'top'
        
        # Label node with name and core values
        plt.text(
            node_pos[0] + offset_x, node_pos[1] + offset_y,
            f"{node.name}\n" + "\n".join([f"• {value}" for value in node.core_values]),
            ha=ha, va=va,
            color='#FFFFFF',
            fontsize=9,
            bbox=dict(facecolor='#00000070', edgecolor='none', pad=3),
            alpha=0.9
        )
    
    # Add tunnel names on the paths
    tunnel_names = {
        ("Ancient Kemet", "Inca Empire"): "Sun Tunnel",
        ("Ancient Kemet", "Rasta Consciousness"): "Lion of Judah Tunnel",
        ("Inca Empire", "Iroquois Confederacy"): "Sacred Earth Tunnel",
        ("Iroquois Confederacy", "Polynesian Navigators"): "Water Tunnel",
        ("Polynesian Navigators", "Rasta Consciousness"): "Navigation Tunnel",
    }
    
    # Add tunnel names on the edges
    for edge in G.edges():
        source, target = edge
        edge_pair = (source, target)
        reversed_pair = (target, source)
        
        # Get tunnel name
        tunnel_name = ""
        if edge_pair in tunnel_names:
            tunnel_name = tunnel_names[edge_pair]
        elif reversed_pair in tunnel_names:
            tunnel_name = tunnel_names[reversed_pair]
        
        if tunnel_name:
            # Find edge midpoint
            x1, y1 = pos[source]
            x2, y2 = pos[target]
            x_mid = (x1 + x2) / 2
            y_mid = (y1 + y2) / 2
            
            # Slight offset to not overlap with edge
            offset = 0.05
            angle = np.arctan2(y2 - y1, x2 - x1) + np.pi/2
            x_offset = offset * np.cos(angle)
            y_offset = offset * np.sin(angle)
            
            plt.text(
                x_mid + x_offset, y_mid + y_offset,
                tunnel_name,
                ha='center', va='center',
                color='#CCCCCC',
                fontsize=7,
                bbox=dict(facecolor='#00000070', edgecolor='none', pad=2),
                alpha=0.8
            )
    
    # Add divine code keys in subtle text
    for node in omega_flock:
        node_pos = pos[node.name]
        code_strings = []
        for code, meaning in node.divine_codes.items():
            code_strings.append(f"{code}: {meaning}")
        
        code_text = "\n".join(code_strings)
        
        # Opposite offset from the core values
        offset_x = -0.15 if node_pos[0] >= 0 else 0.15
        offset_y = -0.15 if node_pos[1] >= 0 else 0.15
        
        # Special case for center node
        if node.name == "Rasta Consciousness":
            offset_y = -0.25
            
        ha = 'right' if node_pos[0] >= 0 else 'left'
        va = 'top' if node_pos[1] >= 0 else 'bottom'
        
        plt.text(
            node_pos[0] + offset_x, node_pos[1] + offset_y,
            code_text,
            ha=ha, va=va,
            color='#CCCCCC',
            fontsize=7,
            alpha=0.7
        )
    
    # Add title with ZION reference
    plt.title("K!NGD)MS OF DIVINE W!SDOM - PATHWAYS TO ZION", 
              fontsize=20, 
              color='#FFD700', 
              fontweight='bold', 
              pad=20)
    
    # Add Omega symbol and JAH blessing
    plt.figtext(0.5, 0.02, "Ω", ha="center", fontsize=36, color='#FFD700')
    plt.figtext(0.5, 0.065, "JAH BLESS ALL K!NGD)MS", ha="center", fontsize=12, color='#FFD700')
    
    # Remove axis for cosmic effect
    plt.axis('off')
    
    # Save with high quality
    plt.tight_layout()
    plt.savefig("omega_kingdoms_divine_visualization.png", dpi=300, bbox_inches='tight', facecolor='#070714')
    print("🔱 Divine visualization created: omega_kingdoms_divine_visualization.png 🔱")
    print("🌊 All tunnels are now dry and flowing with divine energy 🌊")
    
if __name__ == "__main__":
    create_divine_visualization()
