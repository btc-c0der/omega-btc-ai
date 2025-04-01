from dataclasses import dataclass, asdict
from typing import List

@dataclass
class BlockData:
    """Data model for Bitcoin block information."""
    hash: str
    height: int
    timestamp: int
    transactions: List[str]
    
    def to_dict(self):
        """Convert the block data to a dictionary."""
        return asdict(self) 