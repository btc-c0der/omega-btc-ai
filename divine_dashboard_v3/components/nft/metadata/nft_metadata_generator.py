"""
NFT Metadata Generator for Divine Dashboard v3

This module handles the generation of metadata for NFTs, including
properties, attributes, and other relevant information.
"""

import json
import time
import uuid
from typing import Dict, List, Any, Optional

class NFTMetadataGenerator:
    """
    Generator for NFT metadata following standard metadata schemas.
    """
    
    def __init__(self):
        """Initialize the NFT metadata generator with default settings"""
        self.schema_version = "1.0.0"
    
    def generate(
        self, 
        name: str,
        description: str,
        image: str,
        attributes: Optional[List[Dict[str, Any]]] = None,
        external_url: Optional[str] = None,
        animation_url: Optional[str] = None,
        background_color: Optional[str] = None,
        extra_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate standard NFT metadata.
        
        Args:
            name: Name of the NFT
            description: Description of the NFT
            image: URL or path to the NFT image
            attributes: List of attribute dictionaries (trait_type and value pairs)
            external_url: Optional external URL
            animation_url: Optional animation URL for animated NFTs
            background_color: Optional background color (hex without #)
            extra_metadata: Optional additional metadata to include
            
        Returns:
            Dict containing standard NFT metadata
        """
        # Create basic metadata
        metadata = {
            "name": name,
            "description": description,
            "image": image,
            "created_at": int(time.time())
        }
        
        # Add attributes if provided
        if attributes:
            metadata["attributes"] = attributes
        else:
            metadata["attributes"] = []
        
        # Add optional fields if provided
        if external_url:
            metadata["external_url"] = external_url
        
        if animation_url:
            metadata["animation_url"] = animation_url
        
        if background_color:
            metadata["background_color"] = background_color.lstrip("#")
        
        # Add any extra metadata
        if extra_metadata:
            for key, value in extra_metadata.items():
                metadata[key] = value
        
        # Add unique identifier
        metadata["id"] = str(uuid.uuid4())
        
        # Add schema version
        metadata["schema_version"] = self.schema_version
        
        return metadata
    
    def validate(self, metadata: Dict[str, Any]) -> bool:
        """
        Validate NFT metadata against schema requirements.
        
        Args:
            metadata: The metadata dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["name", "description", "image"]
        
        # Check required fields
        for field in required_fields:
            if field not in metadata:
                return False
        
        # Check attributes format if present
        if "attributes" in metadata and metadata["attributes"]:
            for attr in metadata["attributes"]:
                if not isinstance(attr, dict):
                    return False
                
                # Check if trait_type and value are present
                if "trait_type" not in attr or "value" not in attr:
                    return False
        
        return True
    
    def from_json(self, json_string: str) -> Dict[str, Any]:
        """
        Parse metadata from JSON string.
        
        Args:
            json_string: JSON string containing metadata
            
        Returns:
            Parsed metadata dictionary
        """
        metadata = json.loads(json_string)
        return metadata
    
    def to_json(self, metadata: Dict[str, Any], pretty: bool = True) -> str:
        """
        Convert metadata to JSON string.
        
        Args:
            metadata: Metadata dictionary
            pretty: Whether to format with indentation
            
        Returns:
            JSON string representation
        """
        indent = 2 if pretty else None
        return json.dumps(metadata, indent=indent)
    
    def enhance_with_divine_attributes(
        self, 
        metadata: Dict[str, Any],
        consciousness_level: int = 8,
        divine_metrics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Enhance metadata with divine attributes.
        
        Args:
            metadata: Existing metadata
            consciousness_level: Level of consciousness (1-10)
            divine_metrics: List of divine metrics to include
            
        Returns:
            Enhanced metadata
        """
        # Create a copy to avoid modifying the original
        enhanced = metadata.copy()
        
        # Ensure attributes list exists
        if "attributes" not in enhanced:
            enhanced["attributes"] = []
        
        # Add consciousness level
        enhanced["attributes"].append({
            "trait_type": "Consciousness Level",
            "value": str(consciousness_level),
            "max_value": "10"
        })
        
        # Add divine metrics if provided
        if divine_metrics:
            for metric in divine_metrics:
                enhanced["attributes"].append({
                    "trait_type": metric,
                    "value": "Enabled"
                })
        
        # Add special divine metadata section
        enhanced["divine_metadata"] = {
            "consciousness_level": consciousness_level,
            "divine_metrics": divine_metrics or [],
            "creation_intention": "Created with divine intention",
            "quantum_protected": True
        }
        
        return enhanced 