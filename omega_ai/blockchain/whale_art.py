
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

import json
import asyncio
from typing import Dict, List, Any, Tuple
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from datetime import datetime
import hashlib
from pathlib import Path
import math
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image, ImageDraw

@dataclass
class WhaleMovement:
    """Data class for tracking significant whale movements."""
    tx_hash: str
    timestamp: int
    value: float
    from_addresses: List[str]
    to_addresses: List[str]
    fibonacci_level: float
    cluster_size: int
    visualization_path: str = ""

    def __post_init__(self):
        """Validate whale movement data."""
        if not self.tx_hash:
            raise ValueError("Transaction hash is required")
        if self.timestamp <= 0:
            raise ValueError("Invalid timestamp")
        if self.value <= 0:
            raise ValueError("Value must be positive")
        if not self.from_addresses and not self.to_addresses:
            raise ValueError("At least one address is required")
        if not 0 <= self.fibonacci_level <= 1:
            raise ValueError("Fibonacci level must be between 0 and 1")
        if self.cluster_size < 2:
            raise ValueError("Cluster size must be at least 2")

class WhaleArtGenerator:
    """Generate artistic visualizations of whale movements."""
    
    def __init__(self, output_dir: str = "whale_art", use_ai: bool = True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.fibonacci_levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
        self.use_ai = use_ai
        if use_ai:
            self._initialize_ai_model()
        
    def _initialize_ai_model(self):
        """Initialize the Stable Diffusion model."""
        try:
            self.ai_model = StableDiffusionPipeline.from_pretrained(
                "stabilityai/stable-diffusion-2-1",
                torch_dtype=torch.float16
            )
            if torch.cuda.is_available():
                self.ai_model = self.ai_model.to("cuda")
            else:
                print("Warning: CUDA not available, using CPU for image generation")
        except Exception as e:
            print(f"Warning: Could not initialize AI model: {e}")
            self.use_ai = False

    def _generate_prompt(self, movement: WhaleMovement) -> str:
        """Generate a detailed prompt for AI image generation based on whale movement characteristics."""
        # Map Fibonacci level to artistic style
        styles = {
            0: "minimalist",
            0.236: "abstract expressionist",
            0.382: "surrealist",
            0.5: "digital art",
            0.618: "sacred geometry",
            0.786: "cyberpunk",
            1: "baroque"
        }
        
        # Find closest Fibonacci level
        style = styles[min(self.fibonacci_levels, key=lambda x: abs(x - movement.fibonacci_level))]
        
        # Map value to scale/grandeur
        scale = "massive" if movement.value > 1000 else "large" if movement.value > 100 else "medium"
        
        # Map cluster size to complexity
        complexity = "intricate" if movement.cluster_size > 5 else "balanced" if movement.cluster_size > 2 else "simple"
        
        # Generate base prompt
        prompt = f"A {style} visualization of cryptocurrency movement, {scale} scale, {complexity} composition. "
        prompt += f"Sacred geometry patterns with golden ratio proportions, flowing energy represented in "
        
        # Add color scheme based on value
        if movement.value > 1000:
            prompt += "deep purples and golds, "
        elif movement.value > 100:
            prompt += "blues and silvers, "
        else:
            prompt += "greens and bronzes, "
            
        # Add final artistic elements
        prompt += "featuring mathematical patterns, blockchain symbols, and ethereal lighting. "
        prompt += "Highly detailed, professional digital art, trending on artstation"
        
        return prompt

    async def generate_ai_art(self, movement: WhaleMovement) -> str:
        """Generate artistic visualization using Stable Diffusion."""
        if not self.use_ai:
            raise RuntimeError("AI art generation is not available")
            
        # Generate prompt
        prompt = self._generate_prompt(movement)
        
        try:
            # Generate image
            with torch.no_grad():
                image = self.ai_model(
                    prompt,
                    num_inference_steps=50,
                    guidance_scale=7.5,
                ).images[0]
            
            # Save image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"whale_movement_ai_{timestamp}_{movement.tx_hash[:8]}.png"
            filepath = self.output_dir / filename
            
            # Add watermark with movement details
            draw = ImageDraw.Draw(image)
            draw.text(
                (10, image.height - 30),
                f"Whale Movement #{movement.tx_hash[:8]} | {movement.value:.2f} BTC",
                fill=(255, 255, 255, 128)
            )
            
            image.save(filepath)
            return str(filepath)
            
        except Exception as e:
            print(f"Error generating AI art: {e}")
            return await self.generate_visualization(movement)  # Fallback to traditional visualization

    def _generate_abstract_address(self, address: str) -> str:
        """Generate an abstract representation of an address."""
        # Take first 6 chars and last 4 chars, replace middle with dots
        return f"{address[:6]}...{address[-4:]}"
        
    def _calculate_fibonacci_level(self, value: float, max_value: float) -> float:
        """Calculate which Fibonacci level the value corresponds to."""
        normalized = value / max_value
        return min(self.fibonacci_levels, key=lambda x: abs(x - normalized))
        
    def _create_transaction_graph(self, movement: WhaleMovement) -> nx.DiGraph:
        """Create a directed graph for the transaction."""
        G = nx.DiGraph()
        
        # Add nodes for each address
        for addr in movement.from_addresses:
            G.add_node(self._generate_abstract_address(addr), 
                      node_type="source",
                      value=movement.value)
                      
        for addr in movement.to_addresses:
            G.add_node(self._generate_abstract_address(addr),
                      node_type="destination",
                      value=movement.value)
                      
        # Add edges with value flow
        for from_addr in movement.from_addresses:
            for to_addr in movement.to_addresses:
                G.add_edge(self._generate_abstract_address(from_addr),
                          self._generate_abstract_address(to_addr),
                          value=movement.value)
                          
        return G
        
    def _generate_artistic_style(self, movement: WhaleMovement, G: nx.DiGraph) -> Dict[str, Any]:
        """Generate artistic style parameters based on movement characteristics."""
        # Use Fibonacci level to determine color scheme
        fib_idx = self.fibonacci_levels.index(movement.fibonacci_level)
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD', '#D4A5A5', '#9B59B6']
        
        return {
            'node_colors': [colors[fib_idx] if G.nodes[node]['node_type'] == 'source' 
                          else colors[(fib_idx + 1) % len(colors)] 
                          for node in G.nodes()],
            'edge_colors': [colors[fib_idx] for _ in G.edges()],
            'node_sizes': [movement.value * 100 for _ in G.nodes()],
            'edge_widths': [movement.value * 2 for _ in G.edges()],
            'alpha': 0.7
        }
        
    async def generate_visualization(self, movement: WhaleMovement) -> str:
        """Generate and save a visualization of the whale movement."""
        # Create transaction graph
        G = self._create_transaction_graph(movement)
        
        # Generate artistic style
        style = self._generate_artistic_style(movement, G)
        
        # Create figure with artistic background
        plt.figure(figsize=(12, 8))
        plt.style.use('dark_background')
        
        # Draw the graph
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos,
                             node_color=style['node_colors'],
                             node_size=style['node_sizes'],
                             alpha=style['alpha'])
                             
        # Draw edges
        nx.draw_networkx_edges(G, pos,
                             edge_color=style['edge_colors'],
                             width=style['edge_widths'],
                             alpha=style['alpha'])
                             
        # Add labels
        nx.draw_networkx_labels(G, pos, font_size=8)
        
        # Add title and metadata
        plt.title(f"Whale Movement Visualization\n{datetime.fromtimestamp(movement.timestamp)}",
                 fontsize=14, pad=20)
                 
        # Add Fibonacci level indicator
        plt.figtext(0.02, 0.02,
                   f"Fibonacci Level: {movement.fibonacci_level:.3f}\n"
                   f"Cluster Size: {movement.cluster_size}",
                   fontsize=8)
                   
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"whale_movement_{timestamp}_{movement.tx_hash[:8]}.png"
        filepath = self.output_dir / filename
        
        # Save the visualization
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        # Update movement with visualization path
        movement.visualization_path = str(filepath)
        
        return str(filepath)
        
    def _generate_nft_metadata(self, movement: WhaleMovement) -> Dict[str, Any]:
        """Generate NFT metadata for the visualization."""
        return {
            "name": f"Whale Movement #{movement.tx_hash[:8]}",
            "description": f"Artistic visualization of a significant blockchain movement",
            "image": movement.visualization_path,
            "attributes": [
                {
                    "trait_type": "Value",
                    "value": f"{movement.value:.2f} BTC"
                },
                {
                    "trait_type": "Fibonacci Level",
                    "value": f"{movement.fibonacci_level:.3f}"
                },
                {
                    "trait_type": "Cluster Size",
                    "value": movement.cluster_size
                },
                {
                    "trait_type": "Timestamp",
                    "value": datetime.fromtimestamp(movement.timestamp).isoformat()
                }
            ]
        }
        
    async def generate_nft(self, movement: WhaleMovement) -> Dict[str, Any]:
        """Generate NFT-ready visualization and metadata."""
        # Generate visualization (AI or traditional)
        if self.use_ai:
            try:
                movement.visualization_path = await self.generate_ai_art(movement)
            except Exception as e:
                print(f"Failed to generate AI art, falling back to traditional: {e}")
                movement.visualization_path = await self.generate_visualization(movement)
        else:
            movement.visualization_path = await self.generate_visualization(movement)
        
        # Generate metadata
        metadata = self._generate_nft_metadata(movement)
        
        # Save metadata
        metadata_path = self.output_dir / f"{movement.tx_hash[:8]}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
            
        return {
            "visualization": movement.visualization_path,
            "metadata": str(metadata_path)
        } 