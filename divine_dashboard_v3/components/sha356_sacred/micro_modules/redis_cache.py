# ✨ GBU2™ License Notice - Consciousness Level 10 🧬
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
Redis Cache Module for SHA356 Sacred

Provides ORM-like access to Redis for storing and retrieving SHA356 sacred hashes,
sessions, entropy traces, and dimensional alignments with TTL functionality.
"""

import json
import uuid
import time
from typing import Dict, Any, List, Optional, Union, Tuple

try:
    import redis
    from redis.exceptions import RedisError
except ImportError:
    raise ImportError("Redis package not found. Install with: pip install redis")

# Default Redis connection parameters
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None

# Namespace prefixes for different entity types
PREFIX_HASH = "sha356:hash"
PREFIX_SESSION = "sha356:session"
PREFIX_ENTROPY = "sha356:entropy"
PREFIX_ALIGNMENT = "sha356:alignment"
PREFIX_DIMENSION = "sha356:dimension"
PREFIX_PROPHECY = "sha356:prophecy"

# Default TTL values (in seconds)
DEFAULT_TTL = {
    "hash": 3600,           # 1 hour
    "session": 86400,       # 24 hours
    "entropy": 1800,        # 30 minutes
    "alignment": 3600,      # 1 hour
    "dimension": 7200,      # 2 hours
    "prophecy": 604800,     # 7 days
}

class RedisConnector:
    """Redis connection manager with auto-reconnect capabilities."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls, host=REDIS_HOST, port=REDIS_PORT, 
                   db=REDIS_DB, password=REDIS_PASSWORD):
        """Get singleton instance of RedisConnector."""
        if cls._instance is None:
            cls._instance = cls(host, port, db, password)
        return cls._instance
    
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, 
                 db=REDIS_DB, password=REDIS_PASSWORD):
        """Initialize Redis connection."""
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.client = self._connect()
    
    def _connect(self):
        """Establish connection to Redis server."""
        try:
            return redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True,  # Auto-decode bytes to strings
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True
            )
        except RedisError as e:
            print(f"⚠️ Redis connection failed: {e}")
            return None
    
    def reconnect(self):
        """Re-establish connection to Redis server if needed."""
        if self.client is None or not self.client.ping():
            self.client = self._connect()
        return self.client is not None
    
    def get_client(self):
        """Get Redis client, reconnecting if necessary."""
        if self.client is None or not self.client.ping():
            self.reconnect()
        return self.client

class RedisModel:
    """Base class for ORM-like Redis models."""
    
    def __init__(self, prefix: str, default_ttl: Optional[int] = None):
        """
        Initialize a Redis model with specific prefix.
        
        Args:
            prefix: Key prefix for this model type
            default_ttl: Default time-to-live in seconds (None = no expiry)
        """
        self.prefix = prefix
        self.default_ttl = default_ttl
        self.connector = RedisConnector.get_instance()
    
    def _get_key(self, id: str) -> str:
        """Get full Redis key from ID."""
        return f"{self.prefix}:{id}"
    
    def save(self, id: str, data: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """
        Save data to Redis with optional TTL.
        
        Args:
            id: Unique identifier
            data: Dictionary data to save
            ttl: Time-to-live in seconds (overrides default_ttl)
            
        Returns:
            bool: Success status
        """
        client = self.connector.get_client()
        if client is None:
            return False
        
        key = self._get_key(id)
        
        try:
            # Serialize to JSON and store
            client.set(key, json.dumps(data))
            
            # Set expiry if specified
            if ttl is not None:
                client.expire(key, ttl)
            elif self.default_ttl is not None:
                client.expire(key, self.default_ttl)
                
            return True
        except RedisError as e:
            print(f"⚠️ Redis save error for {key}: {e}")
            return False
    
    def load(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Load data from Redis by ID.
        
        Args:
            id: Unique identifier
            
        Returns:
            Dictionary of data or None if not found
        """
        client = self.connector.get_client()
        if client is None:
            return None
        
        key = self._get_key(id)
        
        try:
            # Get and deserialize from JSON
            raw_data = client.get(key)
            if raw_data:
                return json.loads(raw_data)
            return None
        except RedisError as e:
            print(f"⚠️ Redis load error for {key}: {e}")
            return None
    
    def delete(self, id: str) -> bool:
        """
        Delete data from Redis by ID.
        
        Args:
            id: Unique identifier
            
        Returns:
            bool: Success status
        """
        client = self.connector.get_client()
        if client is None:
            return False
        
        key = self._get_key(id)
        
        try:
            return client.delete(key) > 0
        except RedisError as e:
            print(f"⚠️ Redis delete error for {key}: {e}")
            return False
    
    def exists(self, id: str) -> bool:
        """
        Check if key exists in Redis.
        
        Args:
            id: Unique identifier
            
        Returns:
            bool: Whether key exists
        """
        client = self.connector.get_client()
        if client is None:
            return False
        
        key = self._get_key(id)
        
        try:
            return client.exists(key) > 0
        except RedisError as e:
            print(f"⚠️ Redis exists error for {key}: {e}")
            return False
    
    def ttl(self, id: str) -> int:
        """
        Get remaining TTL for a key.
        
        Args:
            id: Unique identifier
            
        Returns:
            int: TTL in seconds, -1 if no expiry, -2 if doesn't exist
        """
        client = self.connector.get_client()
        if client is None:
            return -2
        
        key = self._get_key(id)
        
        try:
            return client.ttl(key)
        except RedisError as e:
            print(f"⚠️ Redis TTL error for {key}: {e}")
            return -2
    
    def set_ttl(self, id: str, ttl: int) -> bool:
        """
        Set TTL for existing key.
        
        Args:
            id: Unique identifier
            ttl: Time-to-live in seconds (must be a positive integer)
            
        Returns:
            bool: Success status
        """
        client = self.connector.get_client()
        if client is None:
            return False
        
        key = self._get_key(id)
        
        try:
            # Ensure ttl is an integer and not None
            if not isinstance(ttl, int) or ttl <= 0:
                print(f"⚠️ Invalid TTL value for {key}: {ttl}")
                return False
            
            return bool(client.expire(key, ttl))
        except RedisError as e:
            print(f"⚠️ Redis set TTL error for {key}: {e}")
            return False
    
    def find_all(self, pattern: Optional[str] = None) -> List[str]:
        """
        Find all keys matching pattern under this prefix.
        
        Args:
            pattern: Optional pattern to match after prefix
            
        Returns:
            List of matching IDs (without prefix)
        """
        client = self.connector.get_client()
        if client is None:
            return []
        
        if pattern:
            search_pattern = f"{self.prefix}:{pattern}"
        else:
            search_pattern = f"{self.prefix}:*"
        
        try:
            keys = client.keys(search_pattern)
            # Strip prefix to get just the IDs
            prefix_len = len(self.prefix) + 1  # +1 for the colon
            return [key[prefix_len:] for key in keys]
        except RedisError as e:
            print(f"⚠️ Redis find error for {search_pattern}: {e}")
            return []


class SHA356HashCache(RedisModel):
    """Model for caching SHA356 hash results."""
    
    def __init__(self):
        super().__init__(PREFIX_HASH, DEFAULT_TTL["hash"])
    
    def save_hash(self, hash_hex: str, hash_data: Dict[str, Any], ttl: Optional[int] = None) -> bool:
        """
        Cache a SHA356 hash result.
        
        Args:
            hash_hex: The hex hash value (used as ID)
            hash_data: Hash data including metadata
            ttl: Custom TTL in seconds
            
        Returns:
            bool: Success status
        """
        return self.save(hash_hex, hash_data, ttl)
    
    def get_hash(self, hash_hex: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a cached SHA356 hash result.
        
        Args:
            hash_hex: The hex hash value
            
        Returns:
            Hash data or None if not found
        """
        return self.load(hash_hex)
    
    def save_hash_for_message(self, message: str, hash_data: Dict[str, Any]) -> Optional[str]:
        """
        Save hash data and also maintain a message-to-hash lookup.
        
        Args:
            message: Original message
            hash_data: Hash data with metadata
            
        Returns:
            Hash hex value or None if no hash found in data
        """
        hash_hex = hash_data.get("hash")
        if not hash_hex:
            return None
            
        # Save the main hash data
        self.save(hash_hex, hash_data)
        
        # Create a message lookup (just stores the hash hex)
        client = self.connector.get_client()
        if client:
            msg_key = f"{PREFIX_HASH}:msg:{hash_message(message)}"
            client.set(msg_key, hash_hex)
            client.expire(msg_key, self.default_ttl)
            
        return hash_hex
        
    def get_hash_for_message(self, message: str) -> Optional[Dict[str, Any]]:
        """
        Lookup hash by message content.
        
        Args:
            message: Original message
            
        Returns:
            Hash data if found in cache
        """
        client = self.connector.get_client()
        if not client:
            return None
            
        # Look up hash ID via message
        msg_key = f"{PREFIX_HASH}:msg:{hash_message(message)}"
        hash_hex = client.get(msg_key)
        
        if hash_hex:
            return self.load(hash_hex)
        return None


class SHA356SessionCache(RedisModel):
    """Model for SHA356 user sessions."""
    
    def __init__(self):
        super().__init__(PREFIX_SESSION, DEFAULT_TTL["session"])
    
    def create_session(self, session_data: Dict[str, Any], ttl: Optional[int] = None) -> str:
        """
        Create a new SHA356 session.
        
        Args:
            session_data: Session data
            ttl: Custom TTL in seconds
            
        Returns:
            str: New session ID (UUID)
        """
        # Generate new UUID for the session
        session_id = str(uuid.uuid4())
        
        # Add timestamp
        session_data["timestamp"] = time.time()
        
        # Save to Redis
        self.save(session_id, session_data, ttl)
        
        return session_id
    
    def update_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """
        Update existing session data.
        
        Args:
            session_id: Session ID
            session_data: New session data
            
        Returns:
            bool: Success status
        """
        # Update timestamp
        session_data["last_updated"] = time.time()
        
        # Save to Redis with existing TTL
        current_ttl = self.ttl(session_id)
        if current_ttl > 0:
            return self.save(session_id, session_data, current_ttl)
        return self.save(session_id, session_data)


class SHA356EntropyCache(RedisModel):
    """Model for entropy traces from SHA356 operations."""
    
    def __init__(self):
        super().__init__(PREFIX_ENTROPY, DEFAULT_TTL["entropy"])
    
    def add_entropy_trace(self, hash_hex: str, entropy_data: Dict[str, Any]) -> str:
        """
        Add an entropy trace for a hash.
        
        Args:
            hash_hex: Related hash value
            entropy_data: Entropy trace data
            
        Returns:
            str: Trace ID
        """
        # Generate trace ID
        trace_id = f"{hash_hex[:8]}_{int(time.time())}"
        
        # Add metadata
        entropy_data["hash_hex"] = hash_hex
        entropy_data["timestamp"] = time.time()
        
        # Save to Redis
        self.save(trace_id, entropy_data)
        
        # Add to hash's entropy traces list
        client = self.connector.get_client()
        if client:
            traces_key = f"{PREFIX_HASH}:{hash_hex}:traces"
            client.lpush(traces_key, trace_id)
            client.expire(traces_key, DEFAULT_TTL["hash"])
        
        return trace_id
    
    def get_traces_for_hash(self, hash_hex: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get entropy traces for a specific hash.
        
        Args:
            hash_hex: Hash value
            limit: Max number of traces to retrieve
            
        Returns:
            List of entropy trace data
        """
        client = self.connector.get_client()
        if not client:
            return []
        
        # Get list of trace IDs for this hash
        traces_key = f"{PREFIX_HASH}:{hash_hex}:traces"
        trace_ids = client.lrange(traces_key, 0, limit - 1)
        
        # Load each trace
        results = []
        for trace_id in trace_ids:
            trace_data = self.load(trace_id)
            if trace_data:
                results.append(trace_data)
        
        return results


class SHA356ProphecyCache(RedisModel):
    """Model for storing SHA356 prophecies (future validations)."""
    
    def __init__(self):
        super().__init__(PREFIX_PROPHECY, DEFAULT_TTL["prophecy"])
    
    def create_prophecy(self, 
                       hash_hex: str, 
                       prophecy_data: Dict[str, Any], 
                       ttl: Optional[int] = None) -> str:
        """
        Create a new hash prophecy.
        
        Args:
            hash_hex: Target hash value
            prophecy_data: Prophecy metadata and validation criteria
            ttl: Custom TTL in seconds
            
        Returns:
            str: Prophecy ID
        """
        # Generate prophecy ID
        prophecy_id = f"{hash_hex[:12]}_{int(time.time())}"
        
        # Add metadata
        prophecy_data["hash_hex"] = hash_hex
        prophecy_data["timestamp"] = time.time()
        prophecy_data["status"] = "pending"
        
        # Save to Redis
        if ttl is None:
            ttl = DEFAULT_TTL["prophecy"]
        self.save(prophecy_id, prophecy_data, ttl)
        
        return prophecy_id
    
    def fulfill_prophecy(self, prophecy_id: str, fulfillment_data: Dict[str, Any]) -> bool:
        """
        Mark a prophecy as fulfilled.
        
        Args:
            prophecy_id: Prophecy ID
            fulfillment_data: Data about the fulfillment
            
        Returns:
            bool: Success status
        """
        prophecy = self.load(prophecy_id)
        if not prophecy:
            return False
        
        # Update prophecy data
        prophecy["status"] = "fulfilled"
        prophecy["fulfillment"] = fulfillment_data
        prophecy["fulfilled_at"] = time.time()
        
        # Save updated prophecy
        return self.save(prophecy_id, prophecy)
    
    def get_pending_prophecies(self) -> List[Dict[str, Any]]:
        """
        Get all pending prophecies.
        
        Returns:
            List of pending prophecy data
        """
        all_ids = self.find_all()
        pending = []
        
        for prophecy_id in all_ids:
            prophecy = self.load(prophecy_id)
            if prophecy and prophecy.get("status") == "pending":
                pending.append(prophecy)
        
        return pending


# Helper function for consistent message hashing
def hash_message(message: str) -> str:
    """Create a consistent hash of a message for lookup."""
    import hashlib
    return hashlib.md5(message.encode('utf-8')).hexdigest()


# Factory function to get the appropriate cache
def get_cache(cache_type: str) -> RedisModel:
    """
    Get Redis cache model by type.
    
    Args:
        cache_type: One of "hash", "session", "entropy", "prophecy"
        
    Returns:
        RedisModel instance
    """
    cache_types = {
        "hash": SHA356HashCache,
        "session": SHA356SessionCache,
        "entropy": SHA356EntropyCache,
        "prophecy": SHA356ProphecyCache,
    }
    
    cache_class = cache_types.get(cache_type.lower())
    if not cache_class:
        raise ValueError(f"Unknown cache type: {cache_type}")
    
    return cache_class() 