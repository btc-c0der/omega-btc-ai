
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
NFT Metadata for Divine Dashboard v3
"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass
class NFTMetadata:
    """Metadata for Divine Dashboard NFTs."""
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
    
    def to_json(self) -> str:
        """Convert metadata to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    def save(self, filepath: str) -> None:
        """Save metadata to file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
            
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NFTMetadata':
        """Create metadata from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})
    
    @classmethod
    def from_json(cls, json_str: str) -> 'NFTMetadata':
        """Create metadata from JSON string."""
        return cls.from_dict(json.loads(json_str))
    
    @classmethod
    def from_file(cls, filepath: str) -> 'NFTMetadata':
        """Load metadata from file."""
        with open(filepath, 'r') as f:
            return cls.from_dict(json.load(f)) 