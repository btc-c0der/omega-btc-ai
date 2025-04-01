#!/usr/bin/env python3
"""
OMEGA BTC AI - Temporal Analysis
===============================

Utility module for managing temporal analysis data in the Trinity Brinks Matrix.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime

@dataclass
class TemporalData:
    """Container for temporal analysis data."""
    past_data: Dict[str, Any]
    present_data: Dict[str, Any]
    future_data: Dict[str, Any]
    trinity_data: Dict[str, Any]
    
    def has_past_data(self) -> bool:
        """Check if temporal data has past data."""
        return (
            self.past_data is not None and
            isinstance(self.past_data, dict) and
            "phase" in self.past_data and
            "timestamp" in self.past_data
        )
        
    def has_present_data(self) -> bool:
        """Check if temporal data has present data."""
        return (
            self.present_data is not None and
            isinstance(self.present_data, dict) and
            "phase" in self.present_data and
            "timestamp" in self.present_data
        )
        
    def has_future_data(self) -> bool:
        """Check if temporal data has future data."""
        return (
            self.future_data is not None and
            isinstance(self.future_data, dict) and
            "phase" in self.future_data and
            "timestamp" in self.future_data
        )
        
    def has_trinity_data(self) -> bool:
        """Check if temporal data has Trinity data."""
        return (
            self.trinity_data is not None and
            isinstance(self.trinity_data, dict) and
            "phase" in self.trinity_data and
            "timestamp" in self.trinity_data
        ) 