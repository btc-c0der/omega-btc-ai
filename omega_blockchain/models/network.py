
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

@dataclass
class NetworkMetrics:
    """Data model for Bitcoin network metrics."""
    hash_rate: int
    difficulty: int
    fee_rate: int
    mempool_size: int
    blocks: int = 0
    headers: int = 0
    connections: int = 0
    mempool_bytes: int = 0
    timestamp: int = 0
    
    def to_dict(self):
        """Convert the network metrics to a dictionary."""
        return asdict(self) 