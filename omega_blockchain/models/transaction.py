from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict

@dataclass
class TransactionData:
    """Data model for Bitcoin transaction information."""
    txid: str
    value: int
    timestamp: datetime
    inputs: List[Dict]
    outputs: List[Dict]
    
    def to_dict(self):
        """Convert the transaction data to a dictionary."""
        return asdict(self) 