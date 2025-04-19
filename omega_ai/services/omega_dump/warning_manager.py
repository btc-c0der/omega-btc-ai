
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

"""OMEGA Dump Service - Warning Manager Integration

This module integrates the Redis-based warning system with OMEGA Dump Service.
It provides functionality to extract warnings from Redis and convert them to LogEntry objects
for storage and monitoring through the standard logging infrastructure.
"""

import json
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

from .models import LogEntry

class WarningManager:
    """Warning Manager for Redis-based warnings integration with OMEGA Dump."""
    
    def __init__(self, redis_client):
        """Initialize the warning manager.
        
        Args:
            redis_client: Redis client instance
        """
        self.redis = redis_client
        self.logger = logging.getLogger(__name__)
    
    def get_warning_count(self) -> Dict[str, int]:
        """Get warning counts by type.
        
        Returns:
            Dictionary mapping warning types to count
        """
        try:
            return self.redis.hgetall("system:warning_counts") or {}
        except Exception as e:
            self.logger.error(f"Error retrieving warning counts: {str(e)}")
            return {}
    
    def get_warnings(self, 
                   warning_type: Optional[str] = None, 
                   limit: int = 100) -> List[Dict[str, Any]]:
        """Get warnings from Redis.
        
        Args:
            warning_type: Filter by warning type (or None for all)
            limit: Maximum number of warnings to retrieve
            
        Returns:
            List of warning data dictionaries
        """
        try:
            warnings = []
            
            # Determine which Redis key to use
            key = f"system:warnings:{warning_type}" if warning_type else "system:warnings"
            
            # Get warnings from Redis
            raw_warnings = self.redis.lrange(key, 0, limit - 1)
            
            # Parse warnings
            for raw_warning in raw_warnings:
                try:
                    warning = json.loads(raw_warning)
                    warnings.append(warning)
                except json.JSONDecodeError:
                    self.logger.warning(f"Failed to parse warning JSON: {raw_warning}")
            
            return warnings
            
        except Exception as e:
            self.logger.error(f"Error retrieving warnings: {str(e)}")
            return []
    
    def warnings_to_log_entries(self, warnings: List[Dict[str, Any]]) -> List[LogEntry]:
        """Convert warnings to LogEntry objects.
        
        Args:
            warnings: List of warning data dictionaries
            
        Returns:
            List of LogEntry objects
        """
        entries = []
        
        for warning in warnings:
            try:
                # Extract warning details
                timestamp = warning.get("timestamp", datetime.now().isoformat())
                warning_type = warning.get("type", "UNKNOWN")
                message = warning.get("message", "No message")
                source = warning.get("source", "unknown")
                
                # Convert warning to log entry
                entry = LogEntry(
                    timestamp=datetime.fromisoformat(timestamp.replace('Z', '+00:00')),
                    source=f"warning_system:{source}",
                    content=message,
                    level="WARNING",
                    metadata={
                        "warning_type": warning_type,
                        "warning_id": warning.get("id", ""),
                    }
                )
                
                entries.append(entry)
                
            except Exception as e:
                self.logger.error(f"Error converting warning to LogEntry: {str(e)}")
        
        return entries
    
    def store_warning_log_entries(self, entries: List[LogEntry]) -> None:
        """Store warning log entries in Redis.
        
        Args:
            entries: List of LogEntry objects
        """
        for entry in entries:
            try:
                # Create Redis key
                key = f"logs:warning:{entry.source}:{entry.timestamp.isoformat()}"
                
                # Store in Redis
                self.redis.set(key, json.dumps(entry.to_dict()))
                
            except Exception as e:
                self.logger.error(f"Error storing warning log entry: {str(e)}")
    
    def process_warnings(self, warning_type: Optional[str] = None, limit: int = 100) -> int:
        """Process warnings from the warning system and convert to log entries.
        
        Args:
            warning_type: Filter by warning type (or None for all)
            limit: Maximum number of warnings to process
            
        Returns:
            Number of warnings processed
        """
        # Get warnings
        warnings = self.get_warnings(warning_type, limit)
        
        if not warnings:
            return 0
            
        # Convert to log entries
        entries = self.warnings_to_log_entries(warnings)
        
        # Store log entries
        self.store_warning_log_entries(entries)
        
        return len(entries)
        
    def clear_warnings(self, warning_type: Optional[str] = None) -> bool:
        """Clear warnings from Redis.
        
        Args:
            warning_type: Type of warnings to clear (or None for all)
            
        Returns:
            Whether operation was successful
        """
        try:
            if warning_type:
                self.redis.delete(f"system:warnings:{warning_type}")
            else:
                # Get all warning type keys
                warning_types = []
                for key in self.redis.keys("system:warnings:*"):
                    if key != "system:warning_counts":
                        warning_types.append(key)
                
                # Delete all warning lists
                if warning_types:
                    self.redis.delete("system:warnings", *warning_types)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error clearing warnings: {str(e)}")
            return False 