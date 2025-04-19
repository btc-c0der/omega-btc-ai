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
OMEGA BTC AI - Market Energy Detection
====================================

Utility module for managing market energy data in the Trinity Brinks Matrix.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime

@dataclass
class EnergyShift:
    """Container for market energy shift data."""
    magnitude: float
    direction: str
    confidence: float
    timestamp: datetime
    
    def is_valid(self) -> bool:
        """Check if energy shift is valid."""
        return (
            isinstance(self.magnitude, float) and
            isinstance(self.direction, str) and
            isinstance(self.confidence, float) and
            isinstance(self.timestamp, datetime)
        )
        
    def is_significant(self) -> bool:
        """Check if energy shift is significant."""
        return self.magnitude > 0.5 and self.confidence > 0.7
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert energy shift to dictionary."""
        return {
            "magnitude": self.magnitude,
            "direction": self.direction,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat()
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnergyShift':
        """Create energy shift from dictionary."""
        return cls(
            magnitude=data["magnitude"],
            direction=data["direction"],
            confidence=data["confidence"],
            timestamp=datetime.fromisoformat(data["timestamp"])
        ) 