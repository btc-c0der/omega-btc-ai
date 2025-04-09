import json
import asyncio
import websockets
from typing import Dict, List, Optional, Any
from redis.asyncio import Redis
from .whale_art import WhaleArtGenerator, WhaleMovement
from .omega_nft import OMEGANFTGenerator

# Redis channel names
BLOCK_CHANNEL = "blockchain:blocks"
TRANSACTION_ALERTS = "blockchain:tx_alerts"
NETWORK_STATUS = "blockchain:network_status"
WHALE_ART_CHANNEL = "blockchain:whale_art"
NFT_CHANNEL = "blockchain:nfts"

class RedisBlockStore:
    """Store and retrieve blockchain data in Redis."""
    
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client
        
    async def store_block(self, block: Dict[str, Any]) -> None:
        """Store a block in Redis and publish to subscribers."""
        key = f"block:{block['hash']}"
        await self.redis_client.set(key, json.dumps(block))
        # Publish block to subscribers
        await self.redis_client.publish(BLOCK_CHANNEL, json.dumps(block))
        
    async def get_block(self, block_hash: str) -> Optional[Dict[str, Any]]:
        """Retrieve a block from Redis by its hash."""
        key = f"block:{block_hash}"
        data = await self.redis_client.get(key)
        return json.loads(data) if data else None
        
    async def delete_block(self, block_hash: str) -> None:
        """Delete a block from Redis by its hash."""
        key = f"block:{block_hash}"
        await self.redis_client.delete(key)

    async def publish_transaction_alert(self, pattern: str, details: Dict[str, Any]) -> None:
        """Publish transaction pattern alerts."""
        alert = {
            "pattern": pattern,
            "details": details,
            "timestamp": asyncio.get_event_loop().time()
        }
        await self.redis_client.publish(TRANSACTION_ALERTS, json.dumps(alert))

    async def broadcast_network_status(self, metrics: Dict[str, Any]) -> None:
        """Broadcast network congestion and status metrics."""
        status = {
            "metrics": metrics,
            "timestamp": asyncio.get_event_loop().time()
        }
        await self.redis_client.publish(NETWORK_STATUS, json.dumps(status))

    async def publish_whale_art(self, art_data: Dict[str, Any]) -> None:
        """Publish whale movement visualization data."""
        await self.redis_client.publish(WHALE_ART_CHANNEL, json.dumps(art_data))
        
    async def publish_nft(self, nft_data: Dict[str, Any]) -> None:
        """Publish NFT data."""
        await self.redis_client.publish(NFT_CHANNEL, json.dumps(nft_data))

class WebSocketBlockStream:
    """Stream blockchain data via WebSocket."""
    
    def __init__(self, websocket_url: str):
        self.websocket_url = websocket_url
        self.websocket: Optional[Any] = None
        
    async def connect(self) -> None:
        """Connect to the WebSocket server."""
        self.websocket = await websockets.connect(self.websocket_url)
        
    async def disconnect(self) -> None:
        """Disconnect from the WebSocket server."""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            
    def is_connected(self) -> bool:
        """Check if the WebSocket connection is active."""
        return self.websocket is not None
        
    async def send_block(self, block: Dict[str, Any]) -> None:
        """Send a block through the WebSocket connection."""
        if not self.websocket:
            raise ConnectionError("WebSocket not connected")
            
        await self.websocket.send(json.dumps(block))

class RealtimeBlockchainMonitor:
    """Monitor blockchain in real-time with Redis and WebSocket integration."""
    
    def __init__(self, redis_client: Redis, websocket_url: str):
        self.redis_store = RedisBlockStore(redis_client)
        self.websocket_stream = WebSocketBlockStream(websocket_url)
        self.whale_art_generator = WhaleArtGenerator()
        self.nft_generator = OMEGANFTGenerator()
        self._running = False
        self._processing_lock = asyncio.Lock()
        self._max_tx_value = 0  # Track maximum transaction value for Fibonacci levels
        self._recent_movements: List[WhaleMovement] = []  # Track recent movements for collection generation
        
    async def start(self) -> None:
        """Start the blockchain monitor."""
        await self.websocket_stream.connect()
        self._running = True
        
    async def stop(self) -> None:
        """Stop the blockchain monitor."""
        await self.websocket_stream.disconnect()
        self._running = False
        
    def is_running(self) -> bool:
        """Check if the monitor is running."""
        return self._running
        
    async def process_block(self, block: Dict[str, Any]) -> None:
        """Process a new block."""
        if not self._running:
            raise RuntimeError("Monitor is not running")
            
        async with self._processing_lock:
            # Validate block
            if not self._validate_block(block):
                return
            
            # Store and broadcast block
            await self.redis_store.store_block(block)
            
            # Check for transaction patterns
            await self._analyze_transactions(block)
            
            # Update network status
            await self._update_network_status(block)
            
            # Broadcast block through WebSocket
            await self.websocket_stream.send_block(block)
        
    def _validate_block(self, block: Dict[str, Any]) -> bool:
        """Validate a block's structure and content."""
        required_fields = ["hash", "height", "timestamp", "transactions"]
        return all(field in block for field in required_fields)

    async def _analyze_transactions(self, block: Dict[str, Any]) -> None:
        """Analyze transactions for patterns and emit alerts."""
        # Example patterns to detect
        large_value_threshold = 100  # BTC
        
        for tx in block["transactions"]:
            value = tx.get("value", 0)
            
            # Update max transaction value
            self._max_tx_value = max(self._max_tx_value, value)
            
            # Check for large value transactions
            if value > large_value_threshold:
                # Create whale movement data
                movement = WhaleMovement(
                    tx_hash=tx["txid"],
                    timestamp=block["timestamp"],
                    value=value,
                    from_addresses=tx.get("inputs", []),
                    to_addresses=tx.get("outputs", []),
                    fibonacci_level=self.whale_art_generator._calculate_fibonacci_level(
                        value, self._max_tx_value
                    ),
                    cluster_size=len(tx.get("inputs", [])) + len(tx.get("outputs", []))
                )
                
                # Add to recent movements
                self._recent_movements.append(movement)
                
                # Keep only last 100 movements
                if len(self._recent_movements) > 100:
                    self._recent_movements.pop(0)
                
                # Generate whale art
                art_data = await self.whale_art_generator.generate_nft(movement)
                
                # Generate NFT
                nft_data = await self.nft_generator.generate_nft(movement)
                
                # Publish whale art data
                await self.redis_store.publish_whale_art(art_data)
                
                # Publish NFT data
                await self.redis_store.publish_nft(nft_data)
                
                # Publish transaction alert
                await self.redis_store.publish_transaction_alert(
                    "large_transaction",
                    {
                        "txid": tx["txid"],
                        "value": value,
                        "block_hash": block["hash"],
                        "art_data": art_data,
                        "nft_data": nft_data
                    }
                )
                
                # Generate collection if we have enough movements
                if len(self._recent_movements) >= 10:
                    collection_data = await self.nft_generator.generate_collection(self._recent_movements)
                    await self.redis_store.publish_nft(collection_data)

    async def _update_network_status(self, block: Dict[str, Any]) -> None:
        """Update and broadcast network status metrics."""
        metrics = {
            "block_height": block["height"],
            "tx_count": len(block["transactions"]),
            "block_size": block.get("size", 0),
            "timestamp": block["timestamp"],
            "max_tx_value": self._max_tx_value,
            "recent_movements": len(self._recent_movements)
        }
        
        await self.redis_store.broadcast_network_status(metrics) 