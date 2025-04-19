# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
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
Redis Metrics Module

Handles tracking and storing metrics for the Hacker Archive NFT Generator.
"""

import json
import time
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import sys

# Configure logging
logger = logging.getLogger(__name__)

# Define fallback functions for when Redis is not available
def fallback_get_redis_client():
    """Fallback function that returns None when Redis is not available."""
    return None

def fallback_set_json(key, data):
    """Fallback function for set_json."""
    logger.warning(f"Redis not available, can't set JSON for {key}")
    return False

def fallback_get_json(key):
    """Fallback function for get_json."""
    logger.warning(f"Redis not available, can't get JSON for {key}")
    return None

def fallback_log_event(event_type, data):
    """Fallback function for log_event."""
    logger.warning(f"Redis not available, can't log event {event_type}")
    return False

def fallback_record_metric(metric_name, value, labels=None):
    """Fallback function for record_metric."""
    logger.warning(f"Redis not available, can't record metric {metric_name}")
    return False

def fallback_get_namespaced_key(namespace, key):
    """Fallback function for get_namespaced_key."""
    return f"{namespace}:{key}"

def fallback_push_to_list(list_name, value):
    """Fallback function for push_to_list."""
    logger.warning(f"Redis not available, can't push to list {list_name}")
    return False

def fallback_increment(key, amount=1):
    """Fallback function for increment."""
    logger.warning(f"Redis not available, can't increment {key}")
    return 0

def fallback_get_list(list_name, start=0, end=-1):
    """Fallback function for get_list."""
    logger.warning(f"Redis not available, can't get list {list_name}")
    return []

# Try to import Redis helper
try:
    sys.path.append('/Users/fsiqueira/OMEGA/omega-btc-ai')
    from divine_dashboard_v3.utils.redis_helper import (
        get_redis_client, set_json, get_json, log_event, 
        record_metric, get_namespaced_key, push_to_list, 
        increment, get_list
    )
    REDIS_AVAILABLE = True
except ImportError:
    logger.warning("Redis helper not found, metrics will be stored locally")
    REDIS_AVAILABLE = False
    # Set fallback functions
    get_redis_client = fallback_get_redis_client
    set_json = fallback_set_json
    get_json = fallback_get_json
    log_event = fallback_log_event
    record_metric = fallback_record_metric
    get_namespaced_key = fallback_get_namespaced_key
    push_to_list = fallback_push_to_list
    increment = fallback_increment
    get_list = fallback_get_list

class RedisMetrics:
    """Handles Redis metrics and tracking for NFT generation."""
    
    def __init__(self, namespace: str = "hacker_archive"):
        """
        Initialize the Redis metrics tracker.
        
        Args:
            namespace: Redis namespace for keys
        """
        self.namespace = namespace
        self.use_redis = REDIS_AVAILABLE
        self.redis_client = None
        self.local_metrics: Dict[str, Any] = {
            'counters': {},
            'events': [],
            'lists': {},
            'json_data': {}
        }
        
        # Initialize Redis connection if available
        if self.use_redis:
            try:
                self.redis_client = get_redis_client()
                logger.info("Redis connection successful for metrics")
                
                # Initialize daily stats counter
                today = datetime.now().strftime("%Y-%m-%d")
                self.daily_counter_key = get_namespaced_key(self.namespace, f"daily_nfts:{today}")
                self.total_counter_key = get_namespaced_key(self.namespace, "total_nfts")
                
                # Test Redis connection with a ping
                if self.redis_client is not None:
                    self.redis_client.ping()
                else:
                    raise Exception("Redis client is None")
            except Exception as e:
                logger.error(f"Redis connection error: {e}")
                self.use_redis = False
    
    def increment_counter(self, key: str, amount: int = 1) -> int:
        """
        Increment a counter in Redis.
        
        Args:
            key: Counter key name
            amount: Amount to increment by
            
        Returns:
            New counter value
        """
        full_key = get_namespaced_key(self.namespace, key) if self.use_redis else key
        
        if self.use_redis:
            try:
                return increment(full_key, amount)
            except Exception as e:
                logger.error(f"Redis error incrementing counter {key}: {e}")
                # Fall back to local storage
                self.local_metrics['counters'][key] = self.local_metrics['counters'].get(key, 0) + amount
                return self.local_metrics['counters'][key]
        else:
            # Store in local dict
            self.local_metrics['counters'][key] = self.local_metrics['counters'].get(key, 0) + amount
            return self.local_metrics['counters'][key]
    
    def log_nft_generated(self, metadata: Dict[str, Any]) -> None:
        """
        Log that an NFT was generated.
        
        Args:
            metadata: NFT metadata
        """
        # Increment counters
        self.increment_counter("total_nfts")
        
        # Increment daily counter
        today = datetime.now().strftime("%Y-%m-%d")
        self.increment_counter(f"daily_nfts:{today}")
        
        # Track by crew
        if 'crew' in metadata:
            crew_key = f"crew:{metadata['crew'].lower().replace(' ', '_')}"
            self.increment_counter(crew_key)
            
        # Track by rarity tier
        if 'rarity_tier' in metadata:
            tier_key = f"rarity:{metadata['rarity_tier'].lower()}"
            self.increment_counter(tier_key)
            
        # Log the event
        self.log_event('nft_generated', {
            'nft_id': metadata.get('id', ''),
            'crew': metadata.get('crew', ''),
            'rarity_tier': metadata.get('rarity_tier', ''),
            'rarity_score': metadata.get('rarity_score', 0)
        })
        
        # Store the full metadata
        if 'id' in metadata:
            self.store_json(f"nft:{metadata['id']}", metadata)
            self.add_to_list('nft_list', f"nft:{metadata['id']}")
    
    def log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Log an event to Redis.
        
        Args:
            event_type: Type of event
            data: Event data
        """
        event_data = {
            'type': event_type,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        if self.use_redis:
            try:
                log_event(event_type, data)
            except Exception as e:
                logger.error(f"Redis error logging event {event_type}: {e}")
                # Fall back to local storage
                self.local_metrics['events'].append(event_data)
        else:
            # Store in local list
            self.local_metrics['events'].append(event_data)
    
    def store_json(self, key: str, data: Dict[str, Any]) -> bool:
        """
        Store JSON data in Redis.
        
        Args:
            key: Key to store data under
            data: JSON-serializable data
            
        Returns:
            True if successful
        """
        full_key = get_namespaced_key(self.namespace, key) if self.use_redis else key
        
        if self.use_redis:
            try:
                return set_json(full_key, data)
            except Exception as e:
                logger.error(f"Redis error storing JSON for {key}: {e}")
                # Fall back to local storage
                self.local_metrics['json_data'][key] = data
                return False
        else:
            # Store in local dict
            self.local_metrics['json_data'][key] = data
            return True
    
    def get_json(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve JSON data from Redis.
        
        Args:
            key: Key to retrieve
            
        Returns:
            JSON data or None if not found
        """
        full_key = get_namespaced_key(self.namespace, key) if self.use_redis else key
        
        if self.use_redis:
            try:
                return get_json(full_key)
            except Exception as e:
                logger.error(f"Redis error getting JSON for {key}: {e}")
                # Fall back to local storage
                return self.local_metrics['json_data'].get(key)
        else:
            # Get from local dict
            return self.local_metrics['json_data'].get(key)
    
    def add_to_list(self, list_name: str, value: str) -> bool:
        """
        Add a value to a Redis list.
        
        Args:
            list_name: Name of the list
            value: Value to add
            
        Returns:
            True if successful
        """
        full_key = get_namespaced_key(self.namespace, list_name) if self.use_redis else list_name
        
        if self.use_redis:
            try:
                result = push_to_list(full_key, value)
                return True if result else False
            except Exception as e:
                logger.error(f"Redis error adding to list {list_name}: {e}")
                # Fall back to local storage
                if list_name not in self.local_metrics['lists']:
                    self.local_metrics['lists'][list_name] = []
                self.local_metrics['lists'][list_name].append(value)
                return False
        else:
            # Store in local list
            if list_name not in self.local_metrics['lists']:
                self.local_metrics['lists'][list_name] = []
            self.local_metrics['lists'][list_name].append(value)
            return True
    
    def get_list(self, list_name: str, start: int = 0, end: int = -1) -> List[str]:
        """
        Get values from a Redis list.
        
        Args:
            list_name: Name of the list
            start: Start index
            end: End index (-1 for all)
            
        Returns:
            List of values
        """
        full_key = get_namespaced_key(self.namespace, list_name) if self.use_redis else list_name
        
        if self.use_redis:
            try:
                return get_list(full_key, start, end)
            except Exception as e:
                logger.error(f"Redis error getting list {list_name}: {e}")
                # Fall back to local storage
                local_list = self.local_metrics['lists'].get(list_name, [])
                end_idx = len(local_list) if end == -1 else end + 1
                return local_list[start:end_idx]
        else:
            # Get from local list
            local_list = self.local_metrics['lists'].get(list_name, [])
            end_idx = len(local_list) if end == -1 else end + 1
            return local_list[start:end_idx]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about NFT generation.
        
        Returns:
            Dictionary with NFT statistics
        """
        stats = {
            'total_nfts': 0,
            'daily_nfts': 0,
            'crew_popularity': {},
            'rarity_distribution': {}
        }
        
        if self.use_redis and self.redis_client is not None:
            try:
                # Get counters
                total_nfts = self.redis_client.get(self.total_counter_key)
                daily_nfts = self.redis_client.get(self.daily_counter_key)
                stats['total_nfts'] = int(total_nfts or 0)
                stats['daily_nfts'] = int(daily_nfts or 0)
                
                # Get crew popularity
                crew_keys = self.redis_client.keys(get_namespaced_key(self.namespace, "crew:*"))
                for key in crew_keys:
                    crew_name = key.decode().split(":")[-1].replace("_", " ")
                    count = int(self.redis_client.get(key) or 0)
                    stats['crew_popularity'][crew_name] = count
                
                # Get rarity distribution
                rarity_keys = self.redis_client.keys(get_namespaced_key(self.namespace, "rarity:*"))
                for key in rarity_keys:
                    tier = key.decode().split(":")[-1].capitalize()
                    count = int(self.redis_client.get(key) or 0)
                    stats['rarity_distribution'][tier] = count
                
            except Exception as e:
                logger.error(f"Redis error getting stats: {e}")
        
        # If Redis failed or metrics are local
        if not self.use_redis or stats['total_nfts'] == 0:
            # Get from local metrics
            stats['total_nfts'] = self.local_metrics['counters'].get('total_nfts', 0)
            
            today = datetime.now().strftime("%Y-%m-%d")
            stats['daily_nfts'] = self.local_metrics['counters'].get(f'daily_nfts:{today}', 0)
            
            # Get crew popularity
            for key, value in self.local_metrics['counters'].items():
                if key.startswith('crew:'):
                    crew_name = key.split(":")[-1].replace("_", " ")
                    stats['crew_popularity'][crew_name] = value
            
            # Get rarity distribution
            for key, value in self.local_metrics['counters'].items():
                if key.startswith('rarity:'):
                    tier = key.split(":")[-1].capitalize()
                    stats['rarity_distribution'][tier] = value
        
        return stats 