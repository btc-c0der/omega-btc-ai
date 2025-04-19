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
NFT Local Generator for Quantum Test Runner V2
---------------------------------------------

This service enables local NFT generation with:
1. Image submission from the "KING" user
2. Automated metadata generation via LLM
3. Direct Pinata IPFS integration
4. Local metadata caching

Designed for the p1n4t4_om3g4_k1ng workflow pattern.
"""

import os
import json
import time
import logging
import requests
import hashlib
import base64
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
import threading
import uuid
import shutil
import sys
from types import ModuleType

# Global flag for OpenAI availability
OPENAI_AVAILABLE = False

# Try importing OpenAI for metadata generation
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    # Create a placeholder module to avoid unbound variable errors
    class ChatCompletionStub:
        @staticmethod
        def create(*args, **kwargs):
            raise ImportError("OpenAI package is not installed")
    
    # Create a module-like object
    openai = ModuleType("openai")
    openai.api_key = None
    openai.ChatCompletion = ChatCompletionStub
    sys.modules["openai"] = openai
    
logger = logging.getLogger("quantum_runner_v2.nft_local_generator")


class NFTLocalGenerator:
    """
    Service for generating NFTs locally with LLM-enhanced metadata.
    
    This service handles:
    - Image processing and conversion
    - LLM-based metadata generation 
    - IPFS uploading via Pinata
    - Local caching of generated assets
    """
    
    def __init__(
        self, 
        ipfs_service=None,
        cache_dir: Optional[Union[str, Path]] = None,
        openai_api_key: Optional[str] = None,
        llm_model: str = "gpt-4-turbo"
    ):
        """
        Initialize the NFT Local Generator.
        
        Args:
            ipfs_service: Reference to IPFS service for content upload
            cache_dir: Directory to cache generated assets (uses .quantum/nft_cache if not provided)
            openai_api_key: OpenAI API key for metadata generation (uses env var if not provided)
            llm_model: LLM model to use for metadata generation
        """
        self.ipfs_service = ipfs_service
        self.running = False
        
        # Set up cache directory
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            # Default to .quantum/nft_cache within the project
            script_dir = Path(__file__).resolve().parent
            project_root = script_dir.parent.parent.parent.parent.parent
            self.cache_dir = project_root / ".quantum" / "nft_cache"
            
        # Create cache subdirectories
        self.images_dir = self.cache_dir / "images"
        self.metadata_dir = self.cache_dir / "metadata"
        self.uploads_dir = self.cache_dir / "uploads"
        
        # Ensure directories exist
        for dir_path in [self.cache_dir, self.images_dir, self.metadata_dir, self.uploads_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # LLM configuration
        self.openai_api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
        self.llm_model = llm_model
        
        # Set LLM availability flag
        self.llm_available = False
        
        # OpenAI client initialization
        if OPENAI_AVAILABLE and self.openai_api_key:
            # Use a try-except block for the assignment in case the property is readonly
            try:
                openai.api_key = self.openai_api_key
                self.llm_available = True
                logger.info("LLM metadata generation is available")
            except Exception as e:
                logger.warning(f"Error setting OpenAI API key: {e}")
        
        if not self.llm_available:
            logger.warning(
                "LLM metadata generation is not available. "
                "Install openai package and set OPENAI_API_KEY to enable."
            )
        
        # Processing queues and locks
        self._processing_queue = []
        self._lock = threading.Lock()
        self._worker_thread = None
    
    def start(self):
        """Start the NFT Local Generator service."""
        if self.running:
            return
            
        self.running = True
        logger.info("NFT Local Generator service started")
        
        # Start background worker thread
        self._worker_thread = threading.Thread(
            target=self._process_queue, 
            daemon=True
        )
        self._worker_thread.start()
    
    def stop(self):
        """Stop the NFT Local Generator service."""
        if not self.running:
            return
            
        self.running = False
        logger.info("NFT Local Generator service stopped")
        
        # Wait for worker thread to finish current operations
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=5.0)
    
    def _process_queue(self):
        """Process the generation queue in background."""
        while self.running:
            # Check if there's anything in the queue
            with self._lock:
                if not self._processing_queue:
                    time.sleep(1)
                    continue
                
                # Get the next item
                image_path, name, description, attributes, king_id = self._processing_queue.pop(0)
            
            # Process the NFT generation
            try:
                self._generate_nft(image_path, name, description, attributes, king_id)
            except Exception as e:
                logger.error(f"Failed to generate NFT: {e}")
                
            # Small delay between processing
            time.sleep(0.5)
    
    def _generate_nft(
        self, 
        image_path: Union[str, Path],
        name: str,
        description: Optional[str] = None,
        attributes: Optional[List[Dict[str, Any]]] = None,
        king_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Generate an NFT with the provided image and metadata.
        
        Args:
            image_path: Path to image file
            name: Name of the NFT
            description: Description of the NFT (generated if None)
            attributes: List of attribute dictionaries (generated if None)
            king_id: Identifier for the KING user
            
        Returns:
            Generated NFT metadata if successful, None otherwise
        """
        try:
            image_path = Path(image_path)
            
            if not image_path.exists():
                logger.error(f"Image file not found: {image_path}")
                return None
            
            # Generate unique identifier for this NFT
            nft_id = str(uuid.uuid4())
            timestamp = int(time.time())
            
            # Create a copy of the image in our cache
            cached_image_path = self.images_dir / f"{nft_id}{image_path.suffix}"
            shutil.copy2(image_path, cached_image_path)
            
            # Generate metadata if needed
            if description is None or attributes is None:
                generated_metadata = self._generate_metadata(cached_image_path, name)
                
                if generated_metadata:
                    description = description or generated_metadata.get("description", "")
                    attributes = attributes or generated_metadata.get("attributes", [])
            
            # Prepare base metadata
            metadata = {
                "name": name,
                "description": description or f"NFT created by p1n4t4_om3g4_k1ng at {time.strftime('%Y-%m-%d %H:%M:%S')}",
                "image": f"ipfs://placeholder-cid-to-be-replaced",  # Will be updated after upload
                "attributes": attributes or [],
                "p1n4t4_om3g4_k1ng": {
                    "generator": "nft_local_generator_v1",
                    "created_at": timestamp,
                    "king_id": king_id or "anonymous"
                }
            }
            
            # Add some default attributes if none provided
            if not metadata["attributes"]:
                metadata["attributes"] = [
                    {"trait_type": "Generation", "value": "Quantum Runner V2"},
                    {"trait_type": "Created", "value": time.strftime("%Y-%m-%d")}
                ]
            
            # Save metadata to cache
            metadata_path = self.metadata_dir / f"{nft_id}.json"
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
            
            # Upload to IPFS if service available
            if self.ipfs_service:
                # Upload image first
                image_upload = self.ipfs_service.upload_artifact(
                    file_path=cached_image_path,
                    artifact_type="nft_image",
                    metadata={
                        "name": name,
                        "king_id": king_id,
                        "nft_id": nft_id
                    }
                )
                
                if image_upload and "ipfs_hash" in image_upload:
                    # Update metadata with actual IPFS image link
                    image_ipfs_hash = image_upload["ipfs_hash"]
                    metadata["image"] = f"ipfs://{image_ipfs_hash}"
                    
                    # Save updated metadata
                    with open(metadata_path, "w") as f:
                        json.dump(metadata, f, indent=2)
                    
                    # Upload metadata
                    metadata_upload = self.ipfs_service.upload_artifact(
                        file_path=metadata_path,
                        artifact_type="nft_metadata",
                        metadata={
                            "name": name,
                            "king_id": king_id,
                            "nft_id": nft_id
                        }
                    )
                    
                    if metadata_upload and "ipfs_hash" in metadata_upload:
                        metadata_ipfs_hash = metadata_upload["ipfs_hash"]
                        
                        # Create full NFT record with all IPFS references
                        nft_record = {
                            "nft_id": nft_id,
                            "name": name,
                            "king_id": king_id,
                            "timestamp": timestamp,
                            "image_path": str(cached_image_path),
                            "metadata_path": str(metadata_path),
                            "image_ipfs": {
                                "hash": image_ipfs_hash,
                                "url": f"ipfs://{image_ipfs_hash}",
                                "gateway_url": image_upload.get("gateway_url")
                            },
                            "metadata_ipfs": {
                                "hash": metadata_ipfs_hash,
                                "url": f"ipfs://{metadata_ipfs_hash}",
                                "gateway_url": metadata_upload.get("gateway_url")
                            },
                            "metadata": metadata
                        }
                        
                        # Save the complete record
                        record_path = self.uploads_dir / f"{nft_id}.json"
                        with open(record_path, "w") as f:
                            json.dump(nft_record, f, indent=2)
                            
                        logger.info(f"NFT generation completed: {nft_id}")
                        return nft_record
                    else:
                        logger.error("Failed to upload metadata to IPFS")
                else:
                    logger.error("Failed to upload image to IPFS")
            
            # Return local metadata if IPFS upload wasn't available/successful
            return {
                "nft_id": nft_id,
                "name": name,
                "king_id": king_id,
                "timestamp": timestamp,
                "image_path": str(cached_image_path),
                "metadata_path": str(metadata_path),
                "metadata": metadata
            }
                
        except Exception as e:
            logger.error(f"Error generating NFT: {e}")
            return None
    
    def _generate_metadata(
        self, 
        image_path: Path,
        name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Generate metadata for an image using LLM.
        
        Args:
            image_path: Path to image
            name: Name of the NFT
            
        Returns:
            Generated metadata dictionary if successful, None otherwise
        """
        if not self.llm_available:
            logger.warning("LLM metadata generation not available")
            return None
        
        try:
            # Read the image and encode as base64
            with open(image_path, "rb") as img_file:
                image_data = base64.b64encode(img_file.read()).decode('utf-8')
            
            # Get image mime type
            mime_type = f"image/{image_path.suffix.lstrip('.')}"
            if image_path.suffix.lower() == ".jpg":
                mime_type = "image/jpeg"
            
            # Create LLM prompt
            system_prompt = """You are an expert NFT metadata creator. Given an image, create rich, 
            detailed metadata for an NFT including:
            1. A compelling description (1-3 paragraphs)
            2. A list of attributes/traits that would be relevant for an NFT collection
            
            Format the response as JSON with keys:
            - description: string
            - attributes: array of objects with trait_type and value properties
            
            Make the attributes creative and specific to what you see in the image.
            Include at least 5-7 attributes."""
            
            user_prompt = f"Create metadata for an NFT named '{name}'. Use the image to inform your description and attributes."
            
            # Create the API call
            response = openai.ChatCompletion.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": [
                        {"type": "text", "text": user_prompt},
                        {"type": "image_url", "image_url": {
                            "url": f"data:{mime_type};base64,{image_data}"
                        }}
                    ]}
                ],
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            content = response.choices[0].message.content
            metadata = json.loads(content)
            
            # Ensure proper format
            if "description" not in metadata:
                metadata["description"] = f"NFT {name} generated via p1n4t4_om3g4_k1ng"
                
            if "attributes" not in metadata or not isinstance(metadata["attributes"], list):
                metadata["attributes"] = []
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error generating metadata with LLM: {e}")
            return {
                "description": f"NFT '{name}' created by p1n4t4_om3g4_k1ng - AI metadata generation unavailable",
                "attributes": [
                    {"trait_type": "Generation", "value": "Quantum Runner V2"},
                    {"trait_type": "Created", "value": time.strftime("%Y-%m-%d")},
                    {"trait_type": "AI Metadata", "value": "Unavailable"}
                ]
            }
    
    def queue_nft_generation(
        self,
        image_path: Union[str, Path],
        name: str,
        description: Optional[str] = None,
        attributes: Optional[List[Dict[str, Any]]] = None,
        king_id: Optional[str] = None
    ):
        """
        Queue an NFT for generation.
        
        Args:
            image_path: Path to image file
            name: Name of the NFT
            description: Optional description (generated via LLM if None)
            attributes: Optional attributes (generated via LLM if None)
            king_id: Identifier for the KING user
        """
        with self._lock:
            self._processing_queue.append((image_path, name, description, attributes, king_id))
            
        logger.debug(f"Queued NFT generation for {name}")
        
        return {
            "status": "queued",
            "name": name,
            "king_id": king_id,
            "timestamp": int(time.time()),
            "queue_position": len(self._processing_queue)
        }
    
    def generate_from_king_image(
        self,
        image_path: Union[str, Path],
        name: Optional[str] = None,
        king_id: str = "p1n4t4_om3g4_k1ng"
    ) -> Dict[str, Any]:
        """
        Generate NFT from a KING-provided image.
        
        Args:
            image_path: Path to image file submitted by KING
            name: Name for the NFT (defaults to filename if not provided)
            king_id: Identifier for the KING user
            
        Returns:
            Status information dictionary
        """
        image_path = Path(image_path)
        
        if not image_path.exists():
            logger.error(f"KING image not found: {image_path}")
            return {
                "status": "error",
                "message": "Image file not found",
                "path": str(image_path)
            }
        
        # Default name to filename if not provided
        if not name:
            name = image_path.stem.replace("_", " ").title()
        
        # Queue the generation
        return self.queue_nft_generation(
            image_path=image_path,
            name=name,
            king_id=king_id
        )
    
    def get_nft_status(self, nft_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status information for a generated NFT.
        
        Args:
            nft_id: ID of the NFT
            
        Returns:
            Status information if found, None otherwise
        """
        # Check uploads first (completed NFTs)
        record_path = self.uploads_dir / f"{nft_id}.json"
        if record_path.exists():
            try:
                with open(record_path, "r") as f:
                    record = json.load(f)
                return record
            except Exception as e:
                logger.error(f"Error reading NFT record: {e}")
                return None
        
        # Check metadata (partially completed)
        metadata_path = self.metadata_dir / f"{nft_id}.json"
        if metadata_path.exists():
            try:
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                
                # Check if image exists
                for ext in [".png", ".jpg", ".jpeg", ".gif"]:
                    image_path = self.images_dir / f"{nft_id}{ext}"
                    if image_path.exists():
                        return {
                            "nft_id": nft_id,
                            "status": "processing",
                            "name": metadata.get("name", "Unknown"),
                            "image_path": str(image_path),
                            "metadata_path": str(metadata_path),
                            "metadata": metadata
                        }
            except Exception as e:
                logger.error(f"Error reading NFT metadata: {e}")
                return None
        
        return None
    
    def list_generated_nfts(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        List recently generated NFTs.
        
        Args:
            limit: Maximum number of NFTs to return
            
        Returns:
            List of NFT records
        """
        nfts = []
        
        try:
            # Get all record files
            record_files = list(self.uploads_dir.glob("*.json"))
            
            # Sort by modification time (newest first)
            record_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Load the records
            for record_file in record_files[:limit]:
                try:
                    with open(record_file, "r") as f:
                        record = json.load(f)
                    nfts.append(record)
                except Exception as e:
                    logger.error(f"Error reading NFT record {record_file}: {e}")
        except Exception as e:
            logger.error(f"Error listing NFTs: {e}")
            
        return nfts
    
    def get_pinata_uri(self, nft_id: str) -> Optional[Dict[str, str]]:
        """
        Get Pinata gateway URI for a generated NFT.
        
        Args:
            nft_id: ID of the NFT
            
        Returns:
            Dictionary with gateway URLs if available
        """
        record = self.get_nft_status(nft_id)
        
        if record and "image_ipfs" in record and "metadata_ipfs" in record:
            return {
                "image_gateway_url": record["image_ipfs"]["gateway_url"],
                "image_ipfs_uri": record["image_ipfs"]["url"],
                "metadata_gateway_url": record["metadata_ipfs"]["gateway_url"],
                "metadata_ipfs_uri": record["metadata_ipfs"]["url"],
                "opensea_url": f"https://testnets.opensea.io/assets/testnet/{record['metadata'].get('p1n4t4_om3g4_k1ng', {}).get('contract', '')}/{nft_id}"
            }
        
        return None 