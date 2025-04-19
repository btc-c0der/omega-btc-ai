# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
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
Hacker Archive NFT Generator

Generates NFTs based on legendary hacker crew defacements from the early 2000s,
preserving the digital underground history in immutable blockchain form.
"""

import os
import base64
import hashlib
import asyncio
import random
import uuid
import json
import logging
import time
import io
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Tuple

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

import sys
sys.path.append('/Users/fsiqueira/OMEGA/omega-btc-ai')
from divine_dashboard_v3.utils.redis_helper import (
    get_redis_client, set_json, get_json, log_event, record_metric,
    get_namespaced_key, push_to_list, increment, get_list
)

# Configure logging
logger = logging.getLogger(__name__)

# Constants
USE_REDIS = True
HACKER_CREWS = [
    "bl0w", "G-Force Pakistan", "The Digital Crew", "Turkish Hackers", 
    "World of Hell", "H4CK3R CR3W", "Anti-Security", "Global Hell",
    "Masters of Deception", "Legion of Doom", "Cult of the Dead Cow"
]

DEFACEMENT_YEARS = ["1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006"]
DEFACEMENT_TYPES = ["Political", "For Fun", "Challenge", "Revenge", "Hacktivism"]
HACKER_RANKS = ["Script Kiddie", "Elite", "G0d Mode", "0day Master", "Ph34r3d"]

# Define ASCII art patterns for NFT backgrounds
ASCII_PATTERNS = {
    "matrix": """
    01010111010100101010101010101010101010101
    10101010101010101010101010100101001010101
    01010111010010111110101010101010101010101
    10100101001010101010101011111010101010111
    01010010101010101010101010101010101010101
    """,
    "skull": """
    .-.   .-.     .--.
    | OO| | OO|   / _.-' .-.   .-.   .-.   .-.
    |   | |   |   \  '-. '-'   '-'   '-'   '-'
    '^^^' '^^^'    '--'
    """,
    "hacker": """
    H4X0R PWN3D
    SYSTEM COMPROMISED
    ROOT ACCESS GRANTED
    ALL YOUR BASE ARE BELONG TO US
    """
}

class HackerArchiveNFTGenerator:
    """Generator for Hacker Archive NFTs with Redis integration."""

    def __init__(self, output_dir: str = "hacker_nft_output"):
        """Initialize the Hacker Archive NFT generator.
        
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
        
        # Test Redis connection
        if USE_REDIS:
            try:
                redis_client = get_redis_client()
                logger.info("Redis connection successful")
                
                # Initialize daily stats counter
                today = datetime.now().strftime("%Y-%m-%d")
                self.daily_nft_counter_key = get_namespaced_key("hacker_archive", f"daily_nfts:{today}")
                self.total_nft_counter_key = get_namespaced_key("hacker_archive", "total_nfts")
                
                # Record component initialization
                log_event("component_init", {
                    "component": "HackerArchiveNFTGenerator",
                    "output_dir": str(self.output_dir)
                })
            except Exception as e:
                logger.error(f"Redis connection error: {e}")
                USE_REDIS = False

    def _generate_unique_id(self, data: Union[bytes, str]) -> str:
        """Generate a unique ID for the NFT.
        
        Args:
            data: Data to hash
            
        Returns:
            Unique ID string
        """
        # Create a hash combining data and timestamp for uniqueness
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        timestamp = datetime.now().isoformat().encode('utf-8')
        random_salt = os.urandom(8)
        
        # Combine all elements
        combined = data + timestamp + random_salt
        
        # Create SHA-256 hash
        hash_obj = hashlib.sha256(combined)
        
        # Return first 12 characters of the hash in hexadecimal
        return hash_obj.hexdigest()[:12]

    def _generate_hacker_ascii_art(self, 
                                   size: Tuple[int, int] = (800, 800),
                                   pattern_type: str = None,
                                   crew_name: str = None) -> Image.Image:
        """Generate ASCII art background for hacker defacement NFT.
        
        Args:
            size: Image dimensions
            pattern_type: Type of ASCII pattern to use
            crew_name: Name of hacker crew
            
        Returns:
            PIL Image with ASCII art
        """
        # Create base image
        background_color = (0, 0, 0)  # Black
        text_color = (0, 255, 0)  # Matrix green
        
        image = Image.new('RGB', size, background_color)
        draw = ImageDraw.Draw(image)
        
        # Select pattern
        if pattern_type is None:
            pattern_type = random.choice(list(ASCII_PATTERNS.keys()))
        
        pattern = ASCII_PATTERNS.get(pattern_type, ASCII_PATTERNS["matrix"])
        
        # Try to load a retro terminal font
        font = None
        try:
            # Try common monospace fonts
            for font_path in [
                "Courier New.ttf", 
                "/System/Library/Fonts/Monaco.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
            ]:
                try:
                    font = ImageFont.truetype(font_path, 16)
                    break
                except (OSError, IOError):
                    continue
        except Exception:
            pass
            
        # Fall back to default if no font was loaded
        if font is None:
            font = ImageFont.load_default()
        
        # Draw pattern across the image
        pattern_lines = pattern.strip().split('\n')
        line_height = 20
        
        for y_offset in range(0, size[1], len(pattern_lines) * line_height):
            for i, line in enumerate(pattern_lines):
                y = y_offset + i * line_height
                # Draw same line at multiple x positions
                for x_offset in range(0, size[0], 400):
                    draw.text((x_offset, y), line, fill=text_color, font=font)
        
        # Add crew name if provided
        if crew_name:
            # Create larger font for crew name
            try:
                large_font = ImageFont.truetype("Arial Bold.ttf", 60)
            except (OSError, IOError):
                large_font = ImageFont.load_default()
            
            # Center the crew name
            crew_text = f"{crew_name} WAS HERE"
            text_width, text_height = draw.textsize(crew_text, font=large_font)
            position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
            
            # Add text shadow for better visibility
            draw.text((position[0]+2, position[1]+2), crew_text, fill=(0, 0, 0), font=large_font)
            draw.text(position, crew_text, fill=(255, 0, 0), font=large_font)  # Red text
        
        # Apply CRT-like effect
        image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Add scan lines effect
        for y in range(0, size[1], 2):
            draw.line([(0, y), (size[0], y)], fill=(0, 0, 0, 50))
        
        return image

    def _calculate_rarity_score(self, metadata: Dict[str, Any]) -> float:
        """Calculate NFT rarity score based on metadata attributes.
        
        Args:
            metadata: NFT metadata
            
        Returns:
            Rarity score (0-100)
        """
        base_score = random.uniform(50, 85)  # Base rarity
        
        # Apply modifiers based on metadata
        modifiers = {
            # Older defacements are rarer
            "1999": 15.0,
            "2000": 12.0,
            "2001": 10.0,
            "2002": 8.0,
            "2003": 6.0,
            "2004": 4.0,
            "2005": 2.0,
            "2006": 1.0,
            
            # Rare crews get bonus
            "bl0w": 10.0,
            "Masters of Deception": 8.0,
            "Legion of Doom": 7.0,
            "Cult of the Dead Cow": 8.5,
            "Global Hell": 7.5,
            
            # Rank bonuses
            "G0d Mode": 5.0,
            "0day Master": 7.0,
            "Ph34r3d": 10.0,
            
            # Type bonuses
            "Political": 3.0,
            "Hacktivism": 4.0,
            "Revenge": 2.5
        }
        
        # Extract values from metadata to check against modifiers
        year = metadata.get("year", "")
        crew = metadata.get("crew", "")
        rank = metadata.get("rank", "")
        defacement_type = metadata.get("defacement_type", "")
        
        # Apply modifiers
        score = base_score
        score += modifiers.get(year, 0)
        score += modifiers.get(crew, 0)
        score += modifiers.get(rank, 0)
        score += modifiers.get(defacement_type, 0)
        
        # Cap at 100
        return min(score, 100.0)

    async def generate_hacker_nft(self,
                                 crew: Optional[str] = None,
                                 year: Optional[str] = None,
                                 defacement_type: Optional[str] = None,
                                 pattern: Optional[str] = None,
                                 custom_text: Optional[str] = None) -> Dict[str, Any]:
        """Generate an NFT for a historical hacker defacement.
        
        Args:
            crew: Optional hacker crew name
            year: Optional year of defacement
            defacement_type: Optional type of defacement
            pattern: Optional ASCII pattern to use
            custom_text: Optional custom text for the defacement
            
        Returns:
            Dictionary with NFT information
        """
        # Randomize missing parameters
        if crew is None:
            crew = random.choice(HACKER_CREWS)
        if year is None:
            year = random.choice(DEFACEMENT_YEARS)
        if defacement_type is None:
            defacement_type = random.choice(DEFACEMENT_TYPES)
        if pattern is None:
            pattern = random.choice(list(ASCII_PATTERNS.keys()))
        
        # Generate hacker rank
        rank = random.choice(HACKER_RANKS)
        
        # Generate unique ID based on parameters
        params_str = f"{crew}:{year}:{defacement_type}:{pattern}:{custom_text}"
        unique_id = self._generate_unique_id(params_str)
        
        # Create NFT name
        nft_name = f"{crew} Defacement {year}"
        
        # Generate description
        descriptions = [
            f"Historical reconstruction of a website defacement by {crew} from {year}.",
            f"Digital artifact preserving hacker history from {year} featuring {crew}.",
            f"Remember when {crew} roamed the early web? This {year} defacement lives forever.",
            f"Digital archaeology: {year} defacement by {crew}, now immortalized as an NFT."
        ]
        nft_description = random.choice(descriptions)
        
        # Generate defacement message
        messages = [
            f"SYSTEM OWNED BY {crew.upper()}",
            f"YOUR SECURITY IS A JOKE! HACKED BY {crew.upper()}",
            f"WE WERE HERE - {crew.upper()} - {year}",
            f"{crew.upper()} WUZ HERE"
        ]
        defacement_message = custom_text or random.choice(messages)
        
        # Generate ASCII art image
        img = self._generate_hacker_ascii_art(
            size=(800, 800),
            pattern_type=pattern,
            crew_name=crew
        )
        
        # Add defacement message
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("Impact.ttf", 36)
        except (OSError, IOError):
            font = ImageFont.load_default()
            
        # Position text
        width, height = img.size
        text_width, text_height = draw.textsize(defacement_message, font=font)
        position = ((width - text_width) // 2, height - text_height - 60)
        
        # Draw text with shadow
        draw.text((position[0]+2, position[1]+2), defacement_message, fill=(0, 0, 0), font=font)
        draw.text(position, defacement_message, fill=(255, 0, 0), font=font)
        
        # Save image
        img_filename = f"hacker_nft_{unique_id}.png"
        img_path = self.images_dir / img_filename
        img.save(img_path, format="PNG")
        
        # Create metadata
        metadata = {
            "name": nft_name,
            "description": nft_description,
            "image": str(img_path),
            "attributes": [
                {"trait_type": "Crew", "value": crew},
                {"trait_type": "Year", "value": year},
                {"trait_type": "Defacement Type", "value": defacement_type},
                {"trait_type": "Hacker Rank", "value": rank},
                {"trait_type": "Pattern", "value": pattern}
            ],
            "crew": crew,
            "year": year,
            "defacement_type": defacement_type,
            "rank": rank,
            "generation_date": datetime.now().isoformat()
        }
        
        # Calculate rarity score
        rarity_score = self._calculate_rarity_score(metadata)
        metadata["rarity_score"] = rarity_score
        
        # Determine rarity tier based on score
        if rarity_score >= 90:
            rarity_tier = "Legendary"
        elif rarity_score >= 80:
            rarity_tier = "Epic"
        elif rarity_score >= 70:
            rarity_tier = "Rare"
        elif rarity_score >= 60:
            rarity_tier = "Uncommon"
        else:
            rarity_tier = "Common"
            
        metadata["rarity_tier"] = rarity_tier
        metadata["attributes"].append({"trait_type": "Rarity Tier", "value": rarity_tier})
        metadata["attributes"].append({"trait_type": "Rarity Score", "value": round(rarity_score, 2)})
        
        # Save metadata
        metadata_filename = f"hacker_nft_{unique_id}_metadata.json"
        metadata_path = self.metadata_dir / metadata_filename
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Record in Redis if available
        if USE_REDIS:
            try:
                # Store NFT data
                nft_key = get_namespaced_key("hacker_archive", f"nft:{unique_id}")
                set_json(nft_key, metadata)
                
                # Add to list of generated NFTs
                nft_list_key = get_namespaced_key("hacker_archive", "nft_list")
                push_to_list(nft_list_key, nft_key)
                
                # Increment counters
                increment(self.daily_nft_counter_key)
                increment(self.total_nft_counter_key)
                
                # Record crew popularity
                crew_key = get_namespaced_key("hacker_archive", f"crew:{crew.lower().replace(' ', '_')}")
                increment(crew_key)
                
                # Log generation event
                log_event("hacker_nft_generated", {
                    "nft_id": unique_id,
                    "crew": crew,
                    "year": year,
                    "rarity_score": rarity_score,
                    "rarity_tier": rarity_tier
                })
                
                # Record metrics
                record_metric("hacker_nft_rarity", rarity_score)
            except Exception as e:
                logger.error(f"Redis error: {e}")
        
        # Return NFT information
        return {
            "id": unique_id,
            "name": nft_name,
            "description": nft_description,
            "image_path": str(img_path),
            "metadata_path": str(metadata_path),
            "crew": crew,
            "year": year,
            "defacement_type": defacement_type,
            "rarity_score": rarity_score,
            "rarity_tier": rarity_tier
        }

    async def batch_generate_nfts(self,
                                 count: int = 10,
                                 crews: Optional[List[str]] = None,
                                 years: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Generate multiple hacker archive NFTs in a batch.
        
        Args:
            count: Number of NFTs to generate
            crews: Optional list of crews to use
            years: Optional list of years to use
            
        Returns:
            List of dictionaries containing NFT information
        """
        results = []
        start_time = time.time()
        batch_id = str(uuid.uuid4())
        
        # Use provided crews/years or use all available
        use_crews = crews or HACKER_CREWS
        use_years = years or DEFACEMENT_YEARS
        
        # Log batch start in Redis
        if USE_REDIS:
            try:
                log_event("batch_generation_start", {
                    "batch_id": batch_id,
                    "count": count,
                    "crews": use_crews,
                    "years": use_years
                })
            except Exception as e:
                logger.error(f"Redis error logging batch start: {e}")
        
        # Generate each NFT
        for i in range(count):
            try:
                # Randomly select parameters
                crew = random.choice(use_crews)
                year = random.choice(use_years)
                defacement_type = random.choice(DEFACEMENT_TYPES)
                pattern = random.choice(list(ASCII_PATTERNS.keys()))
                
                # Generate the NFT
                logger.info(f"Generating NFT {i+1}/{count}: {crew} ({year})")
                nft_info = await self.generate_hacker_nft(
                    crew=crew,
                    year=year,
                    defacement_type=defacement_type,
                    pattern=pattern
                )
                
                # Add batch information
                nft_info["batch_id"] = batch_id
                nft_info["batch_index"] = i + 1
                
                results.append(nft_info)
                
            except Exception as e:
                logger.error(f"Error generating NFT {i+1}/{count}: {e}")
                # Add error information
                results.append({
                    "status": "error",
                    "batch_id": batch_id,
                    "batch_index": i + 1,
                    "error": str(e)
                })
        
        # Calculate batch statistics
        total_time = time.time() - start_time
        successful_nfts = [nft for nft in results if "status" not in nft or nft["status"] != "error"]
        
        # Log batch completion
        if USE_REDIS:
            try:
                log_event("batch_generation_complete", {
                    "batch_id": batch_id,
                    "total_time": total_time,
                    "success_rate": len(successful_nfts) / count,
                    "average_rarity": sum(nft.get("rarity_score", 0) for nft in successful_nfts) / len(successful_nfts) if successful_nfts else 0
                })
            except Exception as e:
                logger.error(f"Redis error logging batch completion: {e}")
        
        logger.info(f"Batch generation complete: {len(successful_nfts)}/{count} successful")
        logger.info(f"Total time: {total_time:.2f}s, Average per NFT: {total_time/count:.2f}s")
        
        return results

    def get_nft_stats(self) -> Dict[str, Any]:
        """Get statistics about generated NFTs.
        
        Returns:
            Dictionary with NFT statistics
        """
        stats = {
            "total_nfts": 0,
            "daily_nfts": 0,
            "crew_popularity": {},
            "rarity_distribution": {
                "Legendary": 0,
                "Epic": 0,
                "Rare": 0,
                "Uncommon": 0,
                "Common": 0
            }
        }
        
        if USE_REDIS:
            try:
                redis_client = get_redis_client()
                
                # Get counters
                stats["total_nfts"] = int(redis_client.get(self.total_nft_counter_key) or 0)
                stats["daily_nfts"] = int(redis_client.get(self.daily_nft_counter_key) or 0)
                
                # Get crew popularity
                for crew in HACKER_CREWS:
                    crew_key = get_namespaced_key("hacker_archive", f"crew:{crew.lower().replace(' ', '_')}")
                    count = int(redis_client.get(crew_key) or 0)
                    stats["crew_popularity"][crew] = count
                
                # Get rarity distribution from recent NFTs
                nft_list_key = get_namespaced_key("hacker_archive", "nft_list")
                recent_nft_keys = redis_client.lrange(nft_list_key, 0, 100)  # Get up to 100 recent NFTs
                
                for nft_key in recent_nft_keys:
                    nft_data = get_json(nft_key)
                    if nft_data and "rarity_tier" in nft_data:
                        tier = nft_data["rarity_tier"]
                        stats["rarity_distribution"][tier] = stats["rarity_distribution"].get(tier, 0) + 1
                        
            except Exception as e:
                logger.error(f"Error getting NFT stats from Redis: {e}")
        
        # If Redis failed or isn't available, try to get stats from files
        if stats["total_nfts"] == 0:
            try:
                # Count image files as NFTs
                image_files = list(self.images_dir.glob("*.png"))
                stats["total_nfts"] = len(image_files)
                
                # Count today's NFTs
                today = datetime.now().strftime("%Y-%m-%d")
                today_nfts = [f for f in image_files if today in f.stat().st_mtime.__str__()]
                stats["daily_nfts"] = len(today_nfts)
                
                # Sample metadata files for rarity distribution
                metadata_files = list(self.metadata_dir.glob("*.json"))
                sample_size = min(100, len(metadata_files))
                sample = random.sample(metadata_files, sample_size) if metadata_files else []
                
                for metadata_file in sample:
                    try:
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                            tier = metadata.get("rarity_tier", "Common")
                            stats["rarity_distribution"][tier] = stats["rarity_distribution"].get(tier, 0) + 1
                            
                            # Track crew popularity
                            crew = metadata.get("crew", "")
                            if crew:
                                stats["crew_popularity"][crew] = stats["crew_popularity"].get(crew, 0) + 1
                    except Exception:
                        pass
            except Exception as e:
                logger.error(f"Error calculating stats from files: {e}")
        
        return stats 