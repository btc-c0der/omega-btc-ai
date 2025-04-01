"""Sacred Punk Generator Module for OMEGA NFT Creator."""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import random
from PIL import Image, ImageDraw
import math
from .sacred_punk_traits import SacredPunkTraits, SacredPunkTrait
import json

class SacredPunkGenerator:
    """Generator for Sacred Punk NFTs combining punk traits with sacred geometry."""
    
    def __init__(self, output_dir: Path):
        """Initialize the Sacred Punk generator.
        
        Args:
            output_dir: Directory to store generated Sacred Punks
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.traits = SacredPunkTraits()
        
    def _create_base_image(self, size: Tuple[int, int] = (512, 512)) -> Image.Image:
        """Create base image with sacred background.
        
        Args:
            size: Image dimensions
            
        Returns:
            PIL Image with sacred background
        """
        # Create black background
        img = Image.new('RGB', size, color='black')
        draw = ImageDraw.Draw(img)
        
        # Add sacred geometry background pattern
        center = (size[0] // 2, size[1] // 2)
        radius = min(size) // 3
        
        # Draw Flower of Life pattern
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            x = center[0] + radius * math.cos(rad)
            y = center[1] + radius * math.sin(rad)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        outline='gold', width=1)
        
        # Add central circle
        draw.ellipse([center[0]-radius, center[1]-radius, 
                     center[0]+radius, center[1]+radius], 
                     outline='gold', width=1)
        
        return img
        
    def _add_sacred_pattern(self, img: Image.Image, pattern: str) -> Image.Image:
        """Add sacred geometry pattern to image.
        
        Args:
            img: Base image
            pattern: Name of sacred pattern to add
            
        Returns:
            Image with added sacred pattern
        """
        draw = ImageDraw.Draw(img)
        width, height = img.size
        center = (width // 2, height // 2)
        radius = min(width, height) // 4
        
        if pattern == "metatrons_cube":
            # Draw Metatron's Cube
            points = []
            for angle in range(0, 360, 60):
                rad = math.radians(angle)
                x = center[0] + radius * math.cos(rad)
                y = center[1] + radius * math.sin(rad)
                points.append((x, y))
                
            # Connect all points
            for i in range(len(points)):
                for j in range(i + 1, len(points)):
                    draw.line([points[i], points[j]], fill='white', width=1)
                    
        elif pattern == "sri_yantra":
            # Draw simplified Sri Yantra
            triangles = [
                [(center[0], center[1] - radius),
                 (center[0] - radius, center[1] + radius),
                 (center[0] + radius, center[1] + radius)],
                [(center[0], center[1] + radius),
                 (center[0] - radius, center[1] - radius),
                 (center[0] + radius, center[1] - radius)]
            ]
            for triangle in triangles:
                draw.polygon(triangle, outline='white')
                
        elif pattern == "golden_spiral":
            # Draw golden spiral
            phi = (1 + math.sqrt(5)) / 2
            points = []
            for t in range(0, 720, 5):
                rad = math.radians(t)
                r = radius * math.exp(0.2 * rad / phi)
                x = center[0] + r * math.cos(rad)
                y = center[1] + r * math.sin(rad)
                points.append((x, y))
            if len(points) > 1:
                draw.line(points, fill='white', width=1)
                
        return img
        
    def generate_sacred_punk(self, seed: Optional[int] = None) -> Dict:
        """Generate a Sacred Punk NFT.
        
        Args:
            seed: Random seed for reproducibility
            
        Returns:
            Dictionary containing NFT data
        """
        if seed is not None:
            random.seed(seed)
            
        # Create base image
        img = self._create_base_image()
        
        # Select traits
        selected_traits = []
        for category in ["divine_headwear", "sacred_eyes", "divine_mouth", "sacred_accessories"]:
            if random.random() > 0.2:  # 80% chance to have each trait
                rarity_threshold = random.random()
                trait = self.traits.get_trait(category, rarity_threshold)
                if trait:
                    selected_traits.append(trait)
                    # Add trait's sacred pattern
                    img = self._add_sacred_pattern(img, trait.geometry_pattern)
        
        # Calculate divine rarity
        divine_rarity = self.traits.calculate_divine_rarity(selected_traits)
        
        # Save image
        timestamp = Path(str(int(random.random() * 1000000)))
        image_path = self.output_dir / f"sacred_punk_{timestamp}.png"
        img.save(image_path)
        
        # Create metadata
        metadata = {
            "name": f"Sacred Punk #{timestamp}",
            "description": "A divine fusion of punk culture and sacred geometry",
            "image": str(image_path),
            "attributes": [
                {
                    "trait_type": trait.category,
                    "value": trait.name,
                    "description": trait.description,
                    "sacred_pattern": self.traits.get_sacred_pattern(trait.geometry_pattern)
                }
                for trait in selected_traits
            ],
            "divine_metrics": {
                "rarity": divine_rarity,
                "resonance": sum(t.divine_resonance for t in selected_traits) / len(selected_traits) if selected_traits else 0,
                "trait_count": len(selected_traits)
            }
        }
        
        # Save metadata
        metadata_path = image_path.with_suffix('.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return {
            "image": str(image_path),
            "metadata": metadata
        } 