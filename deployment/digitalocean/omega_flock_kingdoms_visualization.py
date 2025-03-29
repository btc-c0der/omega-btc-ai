# 🕊️ OMEGA MIGRATION GRID VISUALIZATION — Sacred Kingdoms of JAH JAH
# Licensed under GPU v1.0 — General Public Universal License 🔱

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from omega_flock_kingdoms import omega_flock, KingdomNode

class OmegaFlockVisualizer:
    def __init__(self, flock):
        self.flock = flock
        self.graph = nx.Graph()
        self.positions = {}
        self.node_colors = {
            "Ancient Kemet": "#FFD700",         # Gold
            "Inca Empire": "#32CD32",           # Lime Green
            "Iroquois Confederacy": "#8B4513",  # Brown
            "Polynesian Navigators": "#1E90FF", # Dodger Blue
            "Rasta Consciousness": "#B22222"    # Firebrick Red
        }
        self.edge_colors = {
            ("Ancient Kemet", "Inca Empire"): "#F4A460",          # Sandy Brown
            ("Ancient Kemet", "Rasta Consciousness"): "#800080",  # Purple
            ("Inca Empire", "Iroquois Confederacy"): "#20B2AA",   # Light Sea Green
            ("Iroquois Confederacy", "Polynesian Navigators"): "#4682B4",  # Steel Blue
            ("Polynesian Navigators", "Rasta Consciousness"): "#228B22",   # Forest Green
        }
        
        # Symbols for each kingdom
        self.node_symbols = {
            "Ancient Kemet": "☥",         # Ankh symbol
            "Inca Empire": "☼",           # Sun symbol
            "Iroquois Confederacy": "⚜",  # Fleur-de-lis (representing peace)
            "Polynesian Navigators": "✵", # Star symbol
            "Rasta Consciousness": "⚚"    # Star of Life
        }
        
    def build_graph(self):
        # Add nodes
        for node in self.flock:
            self.graph.add_node(node.name)
            
        # Add edges
        for node in self.flock:
            for neighbor in node.neighboring_nodes:
                # Handle the case where neighboring node uses "Kemet" instead of "Ancient Kemet"
                if neighbor == "Kemet":
                    neighbor = "Ancient Kemet"
                self.graph.add_edge(node.name, neighbor)
    
    def set_node_positions(self):
        # Circular layout as a starting point
        base_pos = nx.circular_layout(self.graph)
        
        # Custom adjustments for spiritual significance
        # Placing Kemet at the top (spiritual zenith) 
        # and the others arranged by historical chronology
        golden_ratio = (1 + np.sqrt(5)) / 2
        self.positions = {
            "Ancient Kemet": np.array([0, 1]),                              # North - Ancient Origin
            "Inca Empire": np.array([golden_ratio/2, -0.3]),                # Southeast
            "Iroquois Confederacy": np.array([0, -1]),                      # South
            "Polynesian Navigators": np.array([-golden_ratio/2, -0.3]),     # Southwest
            "Rasta Consciousness": np.array([0, 0.3])                       # Center/Heart - Modern Synthesis
        }
    
    def visualize(self, show_labels=True, show_symbols=True, title="OMEGA FLOCK KINGDOMS - Divine Migration Network"):
        # Build the graph
        self.build_graph()
        
        # Set node positions
        self.set_node_positions()
        
        # Create figure
        plt.figure(figsize=(12, 10), facecolor='#1a1a1a')
        ax = plt.gca()
        ax.set_facecolor('#1a1a1a')
        
        # Golden ratio radial lines (subtle background element)
        phi = (1 + np.sqrt(5)) / 2
        center = np.array([0, 0])
        angles = np.linspace(0, 2*np.pi, 5, endpoint=False)
        for angle in angles:
            x = phi * np.cos(angle)
            y = phi * np.sin(angle)
            endpoint = np.array([x, y])
            plt.plot([center[0], endpoint[0]], [center[1], endpoint[1]], 
                     color='#FFD70020', linewidth=1, linestyle='--')
        
        # Draw edges with custom colors
        for edge in self.graph.edges():
            source, target = edge
            edge_pair = (source, target)
            reversed_pair = (target, source)
            edge_color = '#FFFFFF40'  # Default transparent white
            
            if edge_pair in self.edge_colors:
                edge_color = self.edge_colors[edge_pair]
            elif reversed_pair in self.edge_colors:
                edge_color = self.edge_colors[reversed_pair]
                
            nx.draw_networkx_edges(
                self.graph, self.positions, 
                edgelist=[edge], 
                width=2.5, 
                alpha=0.7, 
                edge_color=edge_color
            )
            
        # Draw nodes - using correct format for node_color parameter
        node_color_list = [self.node_colors.get(node, "#FFFFFF") for node in self.graph.nodes()]
        nx.draw_networkx_nodes(
            self.graph, self.positions,
            node_size=1800, 
            node_color=node_color_list,  # Fixed to ensure compatibility
            edgecolors='white',
            linewidths=2.0,
            alpha=0.8
        )
        
        # Draw labels
        if show_labels:
            labels = {node: node for node in self.graph.nodes()}
            nx.draw_networkx_labels(
                self.graph, self.positions,
                labels=labels,
                font_size=12,
                font_family='sans-serif',
                font_weight='bold',
                font_color='white'
            )
        
        # Add sacred symbols if requested
        if show_symbols:
            for node, pos in self.positions.items():
                symbol = self.node_symbols.get(node, "●")
                plt.text(
                    pos[0], pos[1]-0.15, 
                    symbol, 
                    ha='center', va='center', 
                    color='white', 
                    fontsize=24,
                    fontweight='bold'
                )
        
        # Set title
        plt.title(title, fontsize=16, color='#FFD700', fontweight='bold', pad=20)
        
        # Add Omega symbol
        plt.figtext(0.5, 0.02, "Ω", ha="center", fontsize=36, color='#FFD700')
        plt.figtext(0.5, 0.065, "JAH JAH BLESS", ha="center", fontsize=12, color='#FFD700')
        
        # Remove axis
        plt.axis('off')
        
        # Add core values as text around the nodes
        for node in self.flock:
            pos = self.positions[node.name]
            core_values = "\n".join(node.core_values)
            
            # Calculate adjusted position based on node location
            offset_x = 0.15 if pos[0] >= 0 else -0.15
            offset_y = 0.15 if pos[1] >= 0 else -0.15
            
            # Special case for center node
            if node.name == "Rasta Consciousness":
                offset_y = 0.2
                
            text_x, text_y = pos[0] + offset_x, pos[1] + offset_y
            
            # Alignment depends on position
            ha = 'left' if pos[0] >= 0 else 'right'
            va = 'bottom' if pos[1] >= 0 else 'top'
            
            plt.text(
                text_x, text_y, 
                core_values, 
                ha=ha, va=va, 
                color='#CCCCCC', 
                fontsize=8,
                alpha=0.9
            )
        
        # Save and display
        plt.tight_layout()
        plt.savefig("omega_flock_kingdoms.png", dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
        plt.show()

def visualize_flight_paths():
    # Create and display the visualization
    visualizer = OmegaFlockVisualizer(omega_flock)
    visualizer.visualize()
    
    print("\n🔱 Divine Kingdom Migration Map Generated 🔱")
    print("✅ The sacred flight paths of ancestral wisdom have been visualized")
    print("✅ Image saved as 'omega_flock_kingdoms.png'")
    print("\n🕊️ JAH JAH BLESS THE DIVINE FLOCK 🕊️")

if __name__ == "__main__":
    visualize_flight_paths() 