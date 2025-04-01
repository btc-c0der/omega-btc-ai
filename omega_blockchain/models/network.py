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