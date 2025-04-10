"""
NFT Generator for Divine Dashboard v3

This module handles the generation of NFT images and assets.
"""

import os
import json
import uuid
import time
import random
from typing import Dict, List, Any, Optional, Tuple, Union, cast, TYPE_CHECKING
from pathlib import Path

# Define dummy types for type checking
if TYPE_CHECKING:
    from PIL import Image as PILImage
    from PIL import ImageDraw as PILImageDraw
    from PIL import ImageFont as PILImageFont
    from PIL import ImageFilter as PILImageFilter
    from PIL import ImageEnhance as PILImageEnhance

# Check if PIL is available
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    # Create empty variables to avoid "possibly unbound" errors
    Image = None
    ImageDraw = None
    ImageFont = None
    ImageFilter = None
    ImageEnhance = None

class NFTGenerator:
    """
    Generator for creating NFT images and assets.
    """
    
    def __init__(self, output_dir: str = "output/nfts"):
        """
        Initialize the NFT generator.
        
        Args:
            output_dir: Directory to save generated NFTs
        """
        self.output_dir = output_dir
        self._ensure_output_dir()
        
        # Check for dependencies
        if not PILLOW_AVAILABLE:
            print("Warning: PIL/Pillow is not available. Image generation will not work.")
    
    def _ensure_output_dir(self) -> None:
        """Ensure the output directory exists"""
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_basic_nft(
        self,
        name: str,
        colors: Optional[List[str]] = None,
        size: Tuple[int, int] = (1024, 1024),
        pattern: str = "gradient",
        seed: Optional[int] = None
    ) -> str:
        """
        Generate a basic NFT image with patterns.
        
        Args:
            name: Base name for the NFT
            colors: List of colors to use (hex codes)
            size: Image dimensions as (width, height)
            pattern: Pattern style to generate
            seed: Optional seed for randomization
            
        Returns:
            Path to the generated image file
        """
        if not PILLOW_AVAILABLE:
            raise ImportError("PIL/Pillow is required for image generation")
            
        # Default colors if none provided
        if not colors:
            colors = ["#3498db", "#2ecc71", "#9b59b6", "#f1c40f"]
            
        # Set seed for reproducibility
        if seed is None:
            seed = int(time.time())
        random.seed(seed)
        
        # Create a new image
        image = Image.new('RGB', size, color=colors[0])  # type: ignore
        draw = ImageDraw.Draw(image)  # type: ignore
        
        if pattern == "gradient":
            self._draw_gradient(image, draw, colors, size)
        elif pattern == "circles":
            self._draw_circles(image, draw, colors, size)
        elif pattern == "squares":
            self._draw_squares(image, draw, colors, size)
        else:
            self._draw_abstract(image, draw, colors, size)
            
        # Add name to the image
        self._add_text_to_image(image, name)
        
        # Apply filters
        image = image.filter(ImageFilter.GaussianBlur(radius=1))  # type: ignore
        enhancer = ImageEnhance.Contrast(image)  # type: ignore
        image = enhancer.enhance(1.2)
        
        # Save the image
        filename = f"{name.replace(' ', '_')}_{uuid.uuid4().hex[:8]}.png"
        file_path = os.path.join(self.output_dir, filename)
        image.save(file_path)
        
        return file_path
    
    def _draw_gradient(self, image: Any, draw: Any, colors: List[str], size: Tuple[int, int]) -> None:
        """Draw a gradient pattern on the image"""
        width, height = size
        
        # Create gradient
        for y in range(height):
            # Calculate color based on y position
            r = int(colors[0][1:3], 16) + (int(colors[1][1:3], 16) - int(colors[0][1:3], 16)) * y // height
            g = int(colors[0][3:5], 16) + (int(colors[1][3:5], 16) - int(colors[0][3:5], 16)) * y // height
            b = int(colors[0][5:7], 16) + (int(colors[1][5:7], 16) - int(colors[0][5:7], 16)) * y // height
            
            # Draw horizontal line
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    def _draw_circles(self, image: Any, draw: Any, colors: List[str], size: Tuple[int, int]) -> None:
        """Draw circles pattern on the image"""
        width, height = size
        
        for _ in range(20):
            # Random position and size
            x = random.randint(0, width)
            y = random.randint(0, height)
            radius = random.randint(50, 200)
            color = random.choice(colors)
            
            # Convert hex to RGB
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # Draw circle
            draw.ellipse(
                [(x - radius, y - radius), (x + radius, y + radius)], 
                fill=(r, g, b, 128)
            )
    
    def _draw_squares(self, image: Any, draw: Any, colors: List[str], size: Tuple[int, int]) -> None:
        """Draw squares pattern on the image"""
        width, height = size
        
        for _ in range(15):
            # Random position and size
            x = random.randint(0, width)
            y = random.randint(0, height)
            square_size = random.randint(50, 200)
            color = random.choice(colors)
            
            # Convert hex to RGB
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # Draw square
            draw.rectangle(
                [(x, y), (x + square_size, y + square_size)], 
                fill=(r, g, b, 128)
            )
    
    def _draw_abstract(self, image: Any, draw: Any, colors: List[str], size: Tuple[int, int]) -> None:
        """Draw an abstract pattern on the image"""
        width, height = size
        
        # Draw multiple random lines
        for _ in range(100):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            color = random.choice(colors)
            
            # Convert hex to RGB
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            # Draw line
            width_line = random.randint(1, 10)
            draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=width_line)
    
    def _add_text_to_image(self, image: Any, text: str) -> None:
        """Add text to the image"""
        if not PILLOW_AVAILABLE:
            return
            
        # Get a drawing context
        draw = ImageDraw.Draw(image)  # type: ignore
        width, height = image.size
        
        # Use default font if custom font not available
        font = None
        try:
            font = ImageFont.truetype("arial.ttf", 40)  # type: ignore
        except IOError:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)  # type: ignore
            except IOError:
                font = ImageFont.load_default()  # type: ignore
        
        # Calculate text size and position
        text_width = 0
        text_height = 0
        
        # Handle different PIL versions for text sizing
        if hasattr(draw, 'textbbox'):
            # For PIL 8.0.0 and later
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            # For older PIL versions
            text_width, text_height = draw.textsize(text, font=font)  # type: ignore
            
        position = ((width - text_width) // 2, height - text_height - 50)
        
        # Add a shadow effect
        shadow_offset = 2
        draw.text((position[0] + shadow_offset, position[1] + shadow_offset), text, font=font, fill=(0, 0, 0, 128))
        
        # Draw the text
        draw.text(position, text, font=font, fill=(255, 255, 255, 255))
    
    def generate_collection(
        self,
        base_name: str,
        count: int,
        theme: str = "abstract",
        colors: Optional[List[str]] = None
    ) -> List[str]:
        """
        Generate a collection of NFTs.
        
        Args:
            base_name: Base name for the collection
            count: Number of NFTs to generate
            theme: Visual theme for the collection
            colors: Optional color palette to use
            
        Returns:
            List of paths to generated images
        """
        if not PILLOW_AVAILABLE:
            raise ImportError("PIL/Pillow is required for image generation")
        
        if colors is None:
            # Define color palettes by theme
            color_palettes = {
                "ocean": ["#1a4b77", "#2980b9", "#3498db", "#85c1e9", "#d4e6f1"],
                "forest": ["#145a32", "#196f3d", "#27ae60", "#58d68d", "#a9dfbf"],
                "sunset": ["#6e2c00", "#d35400", "#e67e22", "#f39c12", "#f9e79f"],
                "cosmic": ["#1b2631", "#34495e", "#5d6d7e", "#85929e", "#d6dbdf"],
                "abstract": ["#8e44ad", "#3498db", "#2ecc71", "#f1c40f", "#e74c3c"]
            }
            colors = color_palettes.get(theme, color_palettes["abstract"])
        
        # Generate each NFT
        paths = []
        patterns = ["gradient", "circles", "squares", "abstract"]
        
        for i in range(count):
            name = f"{base_name} #{i+1}"
            pattern = patterns[i % len(patterns)]
            path = self.generate_basic_nft(
                name=name,
                colors=colors,
                pattern=pattern,
                seed=i  # Use index as seed for reproducibility
            )
            paths.append(path)
        
        return paths
    
    def save_metadata(self, image_path: str, metadata: Dict[str, Any]) -> str:
        """
        Save metadata for an NFT image.
        
        Args:
            image_path: Path to the NFT image file
            metadata: Metadata dictionary
            
        Returns:
            Path to the saved metadata file
        """
        # Extract the base filename without extension
        base_filename = os.path.basename(image_path)
        name_without_ext = os.path.splitext(base_filename)[0]
        metadata_filename = f"{name_without_ext}_metadata.json"
        metadata_path = os.path.join(self.output_dir, metadata_filename)
        
        # Add image path to metadata
        metadata["image"] = image_path
        
        # Save metadata to JSON file
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return metadata_path 