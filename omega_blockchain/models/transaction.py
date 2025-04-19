
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