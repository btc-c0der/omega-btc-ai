
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