
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
OMEGA BTC AI - BitGet WebSocket Integration
=========================================

This module implements real-time market data and position tracking using BitGet's WebSocket API.
Provides live monitoring of order statuses, positions, and market prices for precise execution.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import asyncio
import json
import logging
import time
import hmac
import hashlib
import base64
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass
from datetime import datetime
import websockets
from websockets.exceptions import ConnectionClosed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

@dataclass
class WebSocketConfig:
    """Configuration for WebSocket connections."""
    api_key: str
    secret_key: str
    passphrase: str
    use_testnet: bool = True
    ping_interval: int = 20
    ping_timeout: int = 10
    reconnect_interval: int = 5
    max_reconnect_attempts: int = 5

class BitGetWebSocket:
    """Handles WebSocket connections and data streaming for BitGet."""
    
    def __init__(self, config: WebSocketConfig):
        """
        Initialize the WebSocket client.
        
        Args:
            config: WebSocket configuration
        """
        self.config = config
        self.base_url = "wss://ws-testnet.bitget.com/spot/v1/stream" if config.use_testnet else "wss://ws.bitget.com/spot/v1/stream"
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.is_connected = False
        self.reconnect_attempts = 0
        self.subscriptions: Set[str] = set()
        self.callbacks: Dict[str, List[Callable]] = {
            'order': [],
            'position': [],
            'ticker': [],
            'kline': [],
            'trade': []
        }
        
        # Log initialization
        logger.info(f"{GREEN}Initialized BitGet WebSocket Client{RESET}")
        logger.info(f"{CYAN}Using {'TESTNET' if config.use_testnet else 'MAINNET'} environment{RESET}")
    
    def get_signature(self, timestamp: str) -> str:
        """
        Generate BitGet WebSocket signature.
        
        Args:
            timestamp: Current timestamp in milliseconds
            
        Returns:
            Base64 encoded signature
        """
        message = timestamp + "GET" + "/user/verify"
        return base64.b64encode(
            hmac.new(self.config.secret_key.encode(), message.encode(), hashlib.sha256).digest()
        ).decode()
    
    async def connect(self):
        """Establish WebSocket connection."""
        try:
            # Generate authentication parameters
            timestamp = str(int(time.time() * 1000))
            signature = self.get_signature(timestamp)
            
            # Prepare connection URL with authentication
            auth_params = {
                "apiKey": self.config.api_key,
                "passphrase": self.config.passphrase,
                "timestamp": timestamp,
                "sign": signature
            }
            auth_query = "&".join(f"{k}={v}" for k, v in auth_params.items())
            url = f"{self.base_url}?{auth_query}"
            
            # Connect to WebSocket
            self.ws = await websockets.connect(
                url,
                ping_interval=self.config.ping_interval,
                ping_timeout=self.config.ping_timeout
            )
            
            self.is_connected = True
            self.reconnect_attempts = 0
            logger.info(f"{GREEN}WebSocket connection established{RESET}")
            
            # Resubscribe to previous channels
            if self.subscriptions:
                await self.resubscribe()
                
        except Exception as e:
            logger.error(f"{RED}Failed to establish WebSocket connection: {str(e)}{RESET}")
            self.is_connected = False
            await self.handle_reconnect()
    
    async def handle_reconnect(self):
        """Handle reconnection logic."""
        if self.reconnect_attempts < self.config.max_reconnect_attempts:
            self.reconnect_attempts += 1
            logger.info(f"{YELLOW}Attempting to reconnect ({self.reconnect_attempts}/{self.config.max_reconnect_attempts}){RESET}")
            await asyncio.sleep(self.config.reconnect_interval)
            await self.connect()
        else:
            logger.error(f"{RED}Max reconnection attempts reached. Please check your connection.{RESET}")
    
    async def subscribe(self, channel: str, symbol: str):
        """
        Subscribe to a WebSocket channel.
        
        Args:
            channel: Channel name (order, position, ticker, etc.)
            symbol: Trading symbol
        """
        if not self.is_connected or not self.ws:
            logger.error(f"{RED}Cannot subscribe: WebSocket not connected{RESET}")
            return
            
        try:
            # Format subscription message
            subscription = f"{channel}:{symbol}"
            message = {
                "op": "subscribe",
                "args": [{
                    "instType": "UMCBL",
                    "channel": channel,
                    "instId": f"{symbol}_UMCBL"
                }]
            }
            
            # Send subscription request
            await self.ws.send(json.dumps(message))
            
            # Track subscription
            self.subscriptions.add(subscription)
            logger.info(f"{GREEN}Subscribed to {subscription}{RESET}")
            
        except Exception as e:
            logger.error(f"{RED}Failed to subscribe to {channel}: {str(e)}{RESET}")
    
    async def resubscribe(self):
        """Resubscribe to all previous channels."""
        for subscription in self.subscriptions:
            channel, symbol = subscription.split(":")
            await self.subscribe(channel, symbol)
    
    async def unsubscribe(self, channel: str, symbol: str):
        """
        Unsubscribe from a WebSocket channel.
        
        Args:
            channel: Channel name
            symbol: Trading symbol
        """
        if not self.is_connected or not self.ws:
            return
            
        try:
            subscription = f"{channel}:{symbol}"
            message = {
                "op": "unsubscribe",
                "args": [{
                    "instType": "UMCBL",
                    "channel": channel,
                    "instId": f"{symbol}_UMCBL"
                }]
            }
            
            await self.ws.send(json.dumps(message))
            self.subscriptions.remove(subscription)
            logger.info(f"{YELLOW}Unsubscribed from {subscription}{RESET}")
            
        except Exception as e:
            logger.error(f"{RED}Failed to unsubscribe from {channel}: {str(e)}{RESET}")
    
    def add_callback(self, event_type: str, callback: Callable):
        """
        Add a callback function for a specific event type.
        
        Args:
            event_type: Type of event (order, position, ticker, etc.)
            callback: Callback function to handle the event
        """
        if event_type in self.callbacks:
            self.callbacks[event_type].append(callback)
            logger.info(f"{GREEN}Added callback for {event_type} events{RESET}")
    
    async def handle_message(self, message: str):
        """
        Handle incoming WebSocket messages.
        
        Args:
            message: Raw WebSocket message
        """
        try:
            data = json.loads(message)
            
            # Handle ping messages
            if data.get("op") == "pong":
                return
                
            # Handle subscription responses
            if data.get("event") == "subscribe":
                logger.info(f"{GREEN}Subscription confirmed: {data.get('arg', {}).get('channel')}{RESET}")
                return
                
            # Handle error messages
            if data.get("code") != "0":
                logger.error(f"{RED}WebSocket error: {data.get('msg')}{RESET}")
                return
            
            # Process data based on channel
            channel = data.get("arg", {}).get("channel")
            if channel in self.callbacks:
                # Notify all callbacks for this channel
                for callback in self.callbacks[channel]:
                    try:
                        await callback(data)
                    except Exception as e:
                        logger.error(f"{RED}Error in callback for {channel}: {str(e)}{RESET}")
            
        except json.JSONDecodeError:
            logger.error(f"{RED}Failed to parse WebSocket message: {message}{RESET}")
        except Exception as e:
            logger.error(f"{RED}Error handling WebSocket message: {str(e)}{RESET}")
    
    async def start(self):
        """Start the WebSocket client and begin processing messages."""
        while True:
            try:
                if not self.is_connected:
                    await self.connect()
                
                if self.ws:
                    async for message in self.ws:
                        await self.handle_message(message)
                        
            except ConnectionClosed:
                logger.warning(f"{YELLOW}WebSocket connection closed{RESET}")
                self.is_connected = False
                await self.handle_reconnect()
                
            except Exception as e:
                logger.error(f"{RED}Error in WebSocket loop: {str(e)}{RESET}")
                self.is_connected = False
                await self.handle_reconnect()
    
    async def close(self):
        """Close the WebSocket connection."""
        if self.ws:
            await self.ws.close()
            self.is_connected = False
            self.subscriptions.clear()
            logger.info(f"{GREEN}WebSocket connection closed{RESET}")

# Example usage
async def example_callback(data: Dict[str, Any]):
    """Example callback function for handling WebSocket events."""
    channel = data.get("arg", {}).get("channel")
    print(f"{CYAN}Received {channel} update:{RESET}")
    print(json.dumps(data, indent=2))

async def main():
    """Example usage of the WebSocket client."""
    # Initialize WebSocket client
    config = WebSocketConfig(
        api_key="your_api_key",
        secret_key="your_secret_key",
        passphrase="your_passphrase",
        use_testnet=True
    )
    
    client = BitGetWebSocket(config)
    
    try:
        # Add callbacks
        client.add_callback("order", example_callback)
        client.add_callback("position", example_callback)
        client.add_callback("ticker", example_callback)
        
        # Subscribe to channels
        await client.subscribe("order", "BTCUSDT")
        await client.subscribe("position", "BTCUSDT")
        await client.subscribe("ticker", "BTCUSDT")
        
        # Start WebSocket client
        await client.start()
        
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Shutting down WebSocket client...{RESET}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main()) 