"""OMEGA Dump Service - Divine Log Models"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class LogEntry:
    """Divine Log Entry Model"""
    timestamp: datetime
    source: str  # Source file/component
    content: str  # Log content
    level: str  # Log level (INFO, WARNING, ERROR, etc.)
    metadata: Optional[Dict[str, Any]] = None  # Additional metadata
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "content": self.content,
            "level": self.level,
            "metadata": self.metadata or {}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LogEntry':
        """Create from dictionary"""
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            source=data["source"],
            content=data["content"],
            level=data["level"],
            metadata=data.get("metadata", {})
        ) 