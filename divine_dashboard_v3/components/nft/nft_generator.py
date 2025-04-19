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
NFT Generator for Divine Dashboard v3
"""

import os
import base64
import hashlib
import math
import asyncio
import random
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
import json
import logging
import io
from PIL import Image
import uuid
import time

from .nft_metadata import NFTMetadata

logger = logging.getLogger(__name__)

class NFTGenerator:
    """Generator for Divine Dashboard NFTs."""

    def __init__(self, output_dir: str = "nft_output"):
        """Initialize the NFT generator.
        
        Args:
            output_dir: Directory to store generated NFTs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Create subdirectories
        self.images_dir = self.output_dir / "images"
        self.images_dir.mkdir(exist_ok=True)
        
        self.metadata_dir = self.output_dir / "metadata"
        self.metadata_dir.mkdir(exist_ok=True)

    def _calculate_divine_metrics(self, image: Image.Image) -> Dict[str, float]:
        """Calculate divine metrics from image.
        
        Args:
            image: PIL Image to analyze
            
        Returns:
            Dictionary of divine metrics
        """
        try:
            # Convert image to RGB if it's not already
            if image.mode != 'RGB':
                image = image.convert('RGB')
                
            # Get image data
            width, height = image.size
            pixels = list(image.getdata())
            
            # Calculate average RGB values
            avg_r = sum(p[0] for p in pixels) / len(pixels)
            avg_g = sum(p[1] for p in pixels) / len(pixels)
            avg_b = sum(p[2] for p in pixels) / len(pixels)
            
            # Calculate standard deviation
            std_r = math.sqrt(sum((p[0] - avg_r) ** 2 for p in pixels) / len(pixels))
            std_g = math.sqrt(sum((p[1] - avg_g) ** 2 for p in pixels) / len(pixels))
            std_b = math.sqrt(sum((p[2] - avg_b) ** 2 for p in pixels) / len(pixels))
            
            # Calculate divine metrics
            divine_harmony = (avg_r + avg_g + avg_b) / (3 * 255)  # Average brightness normalized to 0-1
            sacred_balance = (std_r + std_g + std_b) / (3 * 255)  # Average color variation
            
            # Golden ratio alignment
            golden_ratio = (1 + math.sqrt(5)) / 2  # Approximately 1.618
            aspect_ratio = width / height
            golden_ratio_alignment = 1 - min(abs(aspect_ratio - golden_ratio), abs(1/aspect_ratio - golden_ratio)) / golden_ratio
            
            # Calculate additional metrics
            cosmic_resonance = min(avg_r, avg_g, avg_b) / 255  # Darker colors have higher cosmic resonance
            ethereal_vibrance = max(avg_r, avg_g, avg_b) / 255  # Brighter colors have higher ethereal vibrance
            
            return {
                "divine_harmony": divine_harmony,
                "sacred_balance": sacred_balance,
                "golden_ratio_alignment": golden_ratio_alignment,
                "cosmic_resonance": cosmic_resonance,
                "ethereal_vibrance": ethereal_vibrance
            }
        except Exception as e:
            logger.error(f"Error calculating divine metrics: {e}")
            return {
                "divine_harmony": 0.5,
                "sacred_balance": 0.5,
                "golden_ratio_alignment": 0.618,
                "cosmic_resonance": 0.5,
                "ethereal_vibrance": 0.5
            }

    def _calculate_rarity(self, divine_metrics: Dict[str, float]) -> float:
        """Calculate rarity score from divine metrics.
        
        Args:
            divine_metrics: Dictionary of divine metrics
            
        Returns:
            Rarity score from 0-100
        """
        # Calculate weighted average of metrics
        weights = {
            "divine_harmony": 0.25,
            "sacred_balance": 0.2,
            "golden_ratio_alignment": 0.3,
            "cosmic_resonance": 0.15,
            "ethereal_vibrance": 0.1
        }
        
        score = sum(weights.get(k, 0) * v for k, v in divine_metrics.items())
        
        # Apply non-linear transformation to spread out scores
        return score * 100

    def _generate_unique_id(self, image_data: Union[bytes, str]) -> str:
        """Generate a unique ID for the NFT.
        
        Args:
            image_data: Image data as bytes or base64 string
            
        Returns:
            Unique ID string
        """
        # Create a hash of the image data and current timestamp
        if isinstance(image_data, str):
            data = image_data.encode('utf-8')
        else:
            data = image_data
            
        timestamp = datetime.now().isoformat().encode('utf-8')
        
        # Combine image data and timestamp
        # Convert data to bytes if it's not already
        if not isinstance(data, bytes):
            data = str(data).encode('utf-8')
            
        # Combine with timestamp
        combined = data + timestamp
        
        # Create SHA-256 hash
        hash_obj = hashlib.sha256(combined)
        
        # Return first 8 characters of the hash
        return hash_obj.hexdigest()[:8]

    async def generate_nft(self, 
                         image_data: Union[str, bytes, Image.Image], 
                         name: Optional[str] = None,
                         description: Optional[str] = None,
                         attributes: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Generate NFT from image data.
        
        Args:
            image_data: Image data as base64 string, bytes, or PIL Image
            name: Name for the NFT
            description: Description for the NFT
            attributes: List of attribute dictionaries
            
        Returns:
            Dictionary with NFT information
        """
        try:
            # Process image data
            if isinstance(image_data, str) and image_data.startswith('data:image'):
                # Base64 encoded image
                image_data = image_data.split(',')[1]
                image_bytes = base64.b64decode(image_data)
                img = Image.open(io.BytesIO(image_bytes))
            elif isinstance(image_data, str):
                # File path
                img = Image.open(image_data)
            elif isinstance(image_data, bytes):
                # Raw bytes
                img = Image.open(io.BytesIO(image_data))
            elif isinstance(image_data, Image.Image):
                # PIL Image
                img = image_data
            else:
                raise ValueError(f"Unsupported image data type: {type(image_data)}")
            
            # Generate unique ID
            unique_id = self._generate_unique_id(str(img.tobytes()))
            
            # Calculate divine metrics
            divine_metrics = self._calculate_divine_metrics(img)
            
            # Calculate rarity score
            rarity_score = self._calculate_rarity(divine_metrics)
            
            # Save image
            img_filename = f"divine_nft_{unique_id}.png"
            img_path = self.images_dir / img_filename
            img.save(img_path, format="PNG")
            
            # Create metadata
            nft_name = name or f"Divine NFT #{unique_id}"
            nft_description = description or "A divinely generated NFT using sacred algorithms"
            
            metadata = NFTMetadata(
                name=nft_name,
                description=nft_description,
                image=str(img_path),
                attributes=attributes or [],
                divine_metrics=divine_metrics,
                rarity_score=rarity_score
            )
            
            # Generate additional attributes based on divine metrics
            auto_attributes = []
            for metric_name, metric_value in divine_metrics.items():
                # Format the metric name for display
                display_name = " ".join(word.capitalize() for word in metric_name.split("_"))
                # Round metric value to 3 decimal places
                formatted_value = round(metric_value, 3)
                auto_attributes.append({
                    "trait_type": display_name,
                    "value": formatted_value
                })
            
            # Add rarity score attribute
            auto_attributes.append({
                "trait_type": "Rarity Score",
                "value": round(rarity_score, 2)
            })
            
            # Add attributes to metadata
            if metadata.attributes is None:
                metadata.attributes = auto_attributes
            else:
                metadata.attributes.extend(auto_attributes)
            
            # Save metadata
            metadata_filename = f"divine_nft_{unique_id}_metadata.json"
            metadata_path = self.metadata_dir / metadata_filename
            metadata.save(str(metadata_path))
            
            # Return NFT information
            return {
                "id": unique_id,
                "name": nft_name,
                "description": nft_description,
                "image_path": str(img_path),
                "metadata_path": str(metadata_path),
                "divine_metrics": divine_metrics,
                "rarity_score": rarity_score,
                "attributes": metadata.attributes
            }
        
        except Exception as e:
            logger.error(f"Error generating NFT: {e}")
            raise 

    async def batch_generate_nfts(self,
                                image_data_list: List[Union[str, bytes, Image.Image]],
                                names: Optional[List[str]] = None,
                                descriptions: Optional[List[str]] = None,
                                attributes_list: Optional[List[Optional[List[Dict[str, Any]]]]] = None,
                                batch_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Generate multiple NFTs in a batch.
        
        Args:
            image_data_list: List of image data for each NFT
            names: Optional list of names for each NFT
            descriptions: Optional list of descriptions for each NFT
            attributes_list: Optional list of attributes for each NFT
            batch_id: Optional unique identifier for this batch
            
        Returns:
            List of dictionaries containing NFT information
        """
        if not image_data_list:
            logger.warning("No image data provided for batch NFT generation")
            return []
            
        # Create default values if not provided
        batch_size = len(image_data_list)
        if names is None:
            names = [f"Divine NFT #{i+1}" for i in range(batch_size)]
        if descriptions is None:
            descriptions = [f"Divinely generated NFT #{i+1}" for i in range(batch_size)]
        if attributes_list is None:
            attributes_list = [[] for _ in range(batch_size)]
            
        # Generate batch ID if not provided
        batch_id = batch_id or str(uuid.uuid4())
        
        # Process each NFT
        results = []
        start_time = time.time()
        
        for i, image_data in enumerate(image_data_list):
            try:
                # Get corresponding metadata for this index
                name = names[i] if i < len(names) else f"Divine NFT #{i+1}"
                description = descriptions[i] if i < len(descriptions) else f"Divinely generated NFT #{i+1}"
                attributes = attributes_list[i] if i < len(attributes_list) else []
                
                # Ensure attributes is a list
                if attributes is None:
                    attributes = []
                
                # Add batch information to attributes
                attributes.append({"trait_type": "Batch ID", "value": batch_id})
                attributes.append({"trait_type": "Batch Index", "value": i+1})
                
                # Generate the NFT
                logger.info(f"Generating NFT {i+1}/{batch_size}: {name}")
                nft_info = await self.generate_nft(
                    image_data=image_data,
                    name=name,
                    description=description,
                    attributes=attributes
                )
                
                # Add batch information to the result
                nft_info["batch_id"] = batch_id
                nft_info["batch_index"] = i+1
                nft_info["batch_size"] = batch_size
                
                results.append(nft_info)
                
            except Exception as e:
                logger.error(f"Error generating NFT {i+1}/{batch_size}: {e}")
                # Add error information to results
                results.append({
                    "status": "error",
                    "batch_id": batch_id,
                    "batch_index": i+1,
                    "error": str(e)
                })
        
        # Calculate batch statistics
        total_time = time.time() - start_time
        successful_nfts = [nft for nft in results if "status" not in nft or nft["status"] != "error"]
        
        logger.info(f"Batch generation complete: {len(successful_nfts)}/{batch_size} successful")
        logger.info(f"Total time: {total_time:.2f}s, Average per NFT: {total_time/batch_size:.2f}s")
        
        return results 