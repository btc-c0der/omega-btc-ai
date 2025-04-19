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
Metadata Formatter Module

Formats NFT metadata for different blockchain standards and platforms.
"""

import json
import time
import hashlib
import base64
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime
import uuid

class MetadataFormatter:
    """Formats NFT metadata according to different standards."""
    
    # Metadata schemas
    SCHEMAS = {
        'opensea': 'OpenSea',
        'ethereum': 'ERC721',
        'solana': 'Metaplex',
        'cardano': 'CIP25'
    }
    
    def __init__(self, schema: str = 'opensea', version: str = '1.0'):
        """
        Initialize the metadata formatter.
        
        Args:
            schema: Metadata schema to use
            version: Schema version
        """
        self.schema = schema.lower() if schema.lower() in self.SCHEMAS else 'opensea'
        self.version = version
        self.schema_name = self.SCHEMAS.get(self.schema, 'OpenSea')
        
    def _generate_unique_id(self, seed: Optional[str] = None) -> str:
        """Generate a unique ID for the NFT metadata."""
        if seed:
            base = str(seed).encode()
        else:
            base = str(uuid.uuid4()).encode()
            
        timestamp = datetime.now().isoformat().encode()
        unique_hash = hashlib.sha256(base + timestamp).hexdigest()[:16]
        return unique_hash
    
    def format_ethereum(self, 
                      name: str,
                      description: str,
                      image: str,
                      attributes: Optional[List[Dict[str, Any]]] = None,
                      external_url: Optional[str] = None,
                      **kwargs) -> Dict[str, Any]:
        """
        Format metadata following ERC721 Ethereum standard.
        
        Args:
            name: NFT name
            description: NFT description
            image: URL or base64 encoded image
            attributes: List of attribute objects
            external_url: Optional external URL
            
        Returns:
            Formatted metadata dictionary
        """
        # Generate unique ID if not provided
        token_id = kwargs.get('token_id', self._generate_unique_id())
        
        metadata = {
            "name": name,
            "description": description,
            "image": image,
            "attributes": attributes or []
        }
        
        if external_url:
            metadata["external_url"] = external_url
            
        # Add any additional properties passed as kwargs
        for key, value in kwargs.items():
            if key not in metadata and key != 'token_id':
                metadata[key] = value
                
        return metadata
    
    def format_opensea(self,
                     name: str,
                     description: str,
                     image: str,
                     attributes: Optional[List[Dict[str, Any]]] = None,
                     external_url: Optional[str] = None,
                     **kwargs) -> Dict[str, Any]:
        """
        Format metadata following OpenSea standard.
        
        Args:
            name: NFT name
            description: NFT description
            image: URL or base64 encoded image
            attributes: List of attribute objects
            external_url: Optional external URL
            
        Returns:
            Formatted metadata dictionary
        """
        # Build basic ERC721 metadata
        metadata = self.format_ethereum(
            name=name,
            description=description,
            image=image,
            attributes=attributes,
            external_url=external_url,
            **kwargs
        )
        
        # Add OpenSea specific fields
        metadata["compiler"] = "HackerArchive NFT Generator"
        
        # Add collection info if provided
        collection = kwargs.get('collection')
        if collection:
            metadata["collection"] = collection
            
        # Add animation_url if provided
        animation_url = kwargs.get('animation_url')
        if animation_url:
            metadata["animation_url"] = animation_url
            
        # Add background_color if provided
        background_color = kwargs.get('background_color')
        if background_color:
            metadata["background_color"] = background_color
            
        return metadata
    
    def format_solana(self,
                    name: str,
                    description: str,
                    image: str,
                    attributes: Optional[List[Dict[str, Any]]] = None,
                    **kwargs) -> Dict[str, Any]:
        """
        Format metadata following Solana Metaplex standard.
        
        Args:
            name: NFT name
            description: NFT description
            image: URL or base64 encoded image
            attributes: List of attribute objects
            
        Returns:
            Formatted metadata dictionary
        """
        # Convert attributes to Metaplex format if needed
        metaplex_attributes = []
        if attributes:
            for attr in attributes:
                # Check if already in Metaplex format
                if 'trait_type' in attr and 'value' in attr:
                    metaplex_attributes.append({
                        'trait_type': attr['trait_type'],
                        'value': attr['value']
                    })
                # Convert from other format
                else:
                    for key, value in attr.items():
                        metaplex_attributes.append({
                            'trait_type': key,
                            'value': value
                        })
        
        # Create Metaplex metadata
        metadata = {
            "name": name,
            "description": description,
            "image": image,
            "attributes": metaplex_attributes,
            "properties": {
                "files": [
                    {
                        "uri": image,
                        "type": "image/png"
                    }
                ],
                "category": "image",
                "creators": [
                    {
                        "address": kwargs.get('creator_address', ''),
                        "share": 100
                    }
                ]
            }
        }
        
        # Add any additional properties passed as kwargs
        for key, value in kwargs.items():
            if key not in metadata and key != 'creator_address':
                metadata[key] = value
                
        return metadata
    
    def format_cardano(self,
                     name: str,
                     description: str,
                     image: str,
                     attributes: Optional[List[Dict[str, Any]]] = None,
                     **kwargs) -> Dict[str, Any]:
        """
        Format metadata following Cardano CIP-25 standard.
        
        Args:
            name: NFT name
            description: NFT description
            image: URL or base64 encoded image
            attributes: List of attribute objects
            
        Returns:
            Formatted metadata dictionary
        """
        # Create Cardano metadata
        asset_name = kwargs.get('asset_name', name.replace(' ', ''))
        policy_id = kwargs.get('policy_id', '')
        
        # Convert attributes to Cardano format
        cardano_attributes = {}
        if attributes:
            for attr in attributes:
                if 'trait_type' in attr and 'value' in attr:
                    cardano_attributes[attr['trait_type']] = attr['value']
                else:
                    for key, value in attr.items():
                        cardano_attributes[key] = value
        
        metadata = {
            "721": {
                policy_id: {
                    asset_name: {
                        "name": name,
                        "description": description,
                        "image": image,
                        "mediaType": "image/png",
                        "attributes": cardano_attributes
                    }
                }
            }
        }
        
        # Add any additional properties
        for key, value in kwargs.items():
            if key not in ['asset_name', 'policy_id']:
                metadata["721"][policy_id][asset_name][key] = value
                
        return metadata
    
    def format_metadata(self, 
                      name: str,
                      description: str,
                      image: str,
                      attributes: Optional[List[Dict[str, Any]]] = None,
                      **kwargs) -> Dict[str, Any]:
        """
        Format metadata according to the selected schema.
        
        Args:
            name: NFT name
            description: NFT description
            image: URL or base64 encoded image
            attributes: List of attribute objects
            
        Returns:
            Formatted metadata dictionary
        """
        # Select formatter function based on schema
        if self.schema == 'ethereum':
            return self.format_ethereum(name, description, image, attributes, **kwargs)
        elif self.schema == 'solana':
            return self.format_solana(name, description, image, attributes, **kwargs)
        elif self.schema == 'cardano':
            return self.format_cardano(name, description, image, attributes, **kwargs)
        else:
            # Default to OpenSea format
            return self.format_opensea(name, description, image, attributes, **kwargs)
    
    def to_json(self, metadata: Dict[str, Any], pretty: bool = True) -> str:
        """Convert metadata dictionary to JSON string."""
        if pretty:
            return json.dumps(metadata, indent=2, sort_keys=True)
        return json.dumps(metadata)
        
    def from_json(self, json_str: str) -> Dict[str, Any]:
        """Parse JSON string into metadata dictionary."""
        try:
            return json.loads(json_str)
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return {} 