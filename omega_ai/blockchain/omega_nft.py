
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

"""OMEGA NFT Generator Module"""

import json
import asyncio
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import plotly.graph_objects as go
from .whale_art import WhaleMovement
import math

@dataclass
class OMEGANFTMetadata:
    """Metadata for OMEGA blockchain NFTs."""
    name: str
    description: str
    image: str
    animation_url: Optional[str] = None
    external_url: Optional[str] = None
    attributes: Optional[List[Dict[str, Any]]] = None
    background_color: Optional[str] = None
    blockchain_data: Optional[Dict[str, Any]] = None
    divine_metrics: Optional[Dict[str, float]] = None
    rarity_score: float = 0.0
    edition: int = 1
    total_editions: int = 1
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        """Initialize optional fields and timestamps."""
        self.attributes = self.attributes or []
        self.blockchain_data = self.blockchain_data or {}
        self.divine_metrics = self.divine_metrics or {}
        now = datetime.now().isoformat()
        self.created_at = self.created_at or now
        self.updated_at = self.updated_at or self.created_at

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {k: v for k, v in asdict(self).items() if v is not None}

class OMEGANFTGenerator:
    """Generator for OMEGA blockchain NFTs."""

    def __init__(self, output_dir: str = "generated_nfts"):
        """Initialize the NFT generator.
        
        Args:
            output_dir: Directory to store generated NFTs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.visualizations_dir = self.output_dir / "visualizations"
        self.visualizations_dir.mkdir(exist_ok=True)

    def _calculate_divine_metrics(self, movement: WhaleMovement) -> Dict[str, float]:
        """Calculate divine metrics for the NFT.
        
        Args:
            movement: Whale movement data
            
        Returns:
            Dictionary of divine metrics
        """
        # Calculate divine alignment based on Fibonacci level
        divine_alignment = abs(movement.fibonacci_level - 0.618) / 0.618
        
        # Calculate cluster harmony based on cluster size
        cluster_harmony = 1.0 / (1.0 + movement.cluster_size)
        
        # Calculate temporal resonance based on timestamp
        hour = datetime.fromtimestamp(movement.timestamp).hour
        temporal_resonance = abs(math.sin(hour * math.pi / 12))
        
        # Calculate golden ratio alignment
        golden_ratio = (1 + math.sqrt(5)) / 2
        golden_ratio_alignment = abs(movement.value / 100 - golden_ratio) / golden_ratio
        
        # Calculate silver ratio alignment
        silver_ratio = 1 + math.sqrt(2)
        silver_ratio_alignment = abs(movement.value / 100 - silver_ratio) / silver_ratio
        
        return {
            "divine_alignment": divine_alignment,
            "cluster_harmony": cluster_harmony,
            "temporal_resonance": temporal_resonance,
            "fibonacci_level": movement.fibonacci_level,
            "golden_ratio_alignment": golden_ratio_alignment,
            "silver_ratio_alignment": silver_ratio_alignment
        }

    def _calculate_rarity_score(self, divine_metrics: Dict[str, float]) -> float:
        """Calculate rarity score based on divine metrics.
        
        Args:
            divine_metrics: Dictionary of divine metrics
            
        Returns:
            Rarity score between 0 and 100
        """
        weights = {
            "divine_alignment": 0.3,
            "cluster_harmony": 0.2,
            "temporal_resonance": 0.2,
            "fibonacci_level": 0.3
        }
        
        score = sum(
            weights.get(metric, 0) * value
            for metric, value in divine_metrics.items()
            if metric in weights
        )
        
        return score * 100

    def _generate_blockchain_data(self, movement: WhaleMovement) -> Dict[str, Any]:
        """Generate blockchain data for the NFT.
        
        Args:
            movement: Whale movement data
            
        Returns:
            Dictionary of blockchain data
        """
        return {
            "transaction_hash": movement.tx_hash,
            "block_timestamp": movement.timestamp,
            "value_btc": movement.value,
            "from_addresses": movement.from_addresses,
            "to_addresses": movement.to_addresses,
            "cluster_size": movement.cluster_size,
            "network": "Bitcoin",
            "chain_id": "mainnet"
        }

    def _generate_attributes(
        self,
        movement: WhaleMovement,
        divine_metrics: Dict[str, float],
        rarity_score: float
    ) -> List[Dict[str, Any]]:
        """Generate NFT attributes.
        
        Args:
            movement: Whale movement data
            divine_metrics: Dictionary of divine metrics
            rarity_score: Calculated rarity score
            
        Returns:
            List of attribute dictionaries
        """
        return [
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
                "trait_type": "Divine Alignment",
                "value": f"{divine_metrics['divine_alignment']:.4f}"
            },
            {
                "trait_type": "Temporal Resonance",
                "value": f"{divine_metrics['temporal_resonance']:.4f}"
            },
            {
                "trait_type": "Rarity Score",
                "value": f"{rarity_score:.2f}"
            }
        ]

    async def _generate_visualization(
        self,
        movement: WhaleMovement,
        divine_metrics: Dict[str, float],
        output_path: Path
    ) -> None:
        """Generate NFT visualization.
        
        Args:
            movement: Whale movement data
            divine_metrics: Dictionary of divine metrics
            output_path: Path to save the visualization
        """
        # Create a polar plot for divine metrics
        fig = go.Figure()
        
        # Add divine metrics on a polar plot
        theta = ["Divine Alignment", "Cluster Harmony", "Temporal Resonance", 
                "Fibonacci Level", "Golden Ratio Alignment", "Silver Ratio Alignment"]
        r = [divine_metrics[k.lower().replace(" ", "_")] for k in theta]
        
        fig.add_trace(go.Scatterpolar(
            r=r,
            theta=theta,
            fill='toself',
            name='Divine Metrics'
        ))
        
        # Update layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=False,
            title=f"OMEGA Whale Movement NFT<br>Value: {movement.value:.2f} BTC"
        )
        
        # Save the visualization
        fig.write_html(str(output_path))

    async def generate_nft(self, movement: WhaleMovement) -> Dict[str, Any]:
        """Generate an NFT from a whale movement.
        
        Args:
            movement: Whale movement data
            
        Returns:
            Dictionary containing NFT data
        """
        # Calculate divine metrics
        divine_metrics = self._calculate_divine_metrics(movement)
        
        # Calculate rarity score
        rarity_score = self._calculate_rarity_score(divine_metrics)
        
        # Generate visualization
        viz_path = self.visualizations_dir / f"whale_movement_{movement.tx_hash[:8]}.html"
        await self._generate_visualization(movement, divine_metrics, viz_path)
        
        # Create metadata
        metadata = OMEGANFTMetadata(
            name=f"OMEGA Whale Movement #{movement.tx_hash[:8]}",
            description=f"A significant whale movement of {movement.value:.2f} BTC "
                       f"captured on {datetime.fromtimestamp(movement.timestamp)}",
            image=str(viz_path),
            attributes=self._generate_attributes(movement, divine_metrics, rarity_score),
            blockchain_data=self._generate_blockchain_data(movement),
            divine_metrics=divine_metrics,
            rarity_score=rarity_score
        )
        
        # Save metadata
        metadata_path = self.output_dir / f"whale_movement_{movement.tx_hash[:8]}.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata.to_dict(), f, indent=2)
        
        return {
            "metadata": str(metadata_path),
            "visualization": str(viz_path),
            "rarity_score": rarity_score,
            "divine_metrics": divine_metrics
        }

    async def generate_collection(
        self,
        movements: List[WhaleMovement]
    ) -> Dict[str, Any]:
        """Generate a collection of NFTs from whale movements.
        
        Args:
            movements: List of whale movements
            
        Returns:
            Dictionary containing collection data
        """
        nfts = []
        total_rarity = 0
        max_rarity = 0
        min_rarity = float('inf')
        rarity_counts = {
            "legendary": 0,
            "epic": 0,
            "rare": 0,
            "uncommon": 0,
            "common": 0
        }
        
        # Generate NFTs
        for movement in movements:
            nft_data = await self.generate_nft(movement)
            nfts.append(nft_data)
            
            # Update rarity statistics
            rarity = nft_data["rarity_score"]
            total_rarity += rarity
            max_rarity = max(max_rarity, rarity)
            min_rarity = min(min_rarity, rarity)
            
            # Classify rarity
            if rarity >= 90:
                rarity_counts["legendary"] += 1
            elif rarity >= 80:
                rarity_counts["epic"] += 1
            elif rarity >= 70:
                rarity_counts["rare"] += 1
            elif rarity >= 60:
                rarity_counts["uncommon"] += 1
            else:
                rarity_counts["common"] += 1
        
        # Create collection metadata
        collection_metadata = {
            "name": "OMEGA Whale Movement Collection",
            "description": "A collection of significant whale movements on the Bitcoin network",
            "total_supply": len(movements),
            "created_at": datetime.now().isoformat(),
            "statistics": {
                "total_nfts": len(movements),
                "average_rarity": total_rarity / len(movements),
                "max_rarity": max_rarity,
                "min_rarity": min_rarity,
                "rarity_distribution": rarity_counts
            },
            "nfts": nfts
        }
        
        # Save collection metadata
        collection_path = self.output_dir / "collection_metadata.json"
        with open(collection_path, 'w') as f:
            json.dump(collection_metadata, f, indent=2)
        
        return {
            "collection_metadata": str(collection_path),
            "statistics": collection_metadata["statistics"],
            "nfts": nfts
        } 