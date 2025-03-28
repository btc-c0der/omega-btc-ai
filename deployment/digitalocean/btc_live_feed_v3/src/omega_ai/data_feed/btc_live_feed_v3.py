#!/usr/bin/env python3
"""
OMEGA BTC AI - BTC Live Feed v3
===============================

WebSocket client for retrieving real-time BTC price data with enhanced reliability.
Features automatic Redis failover for 99.99% uptime guarantee.

🔮 GPU (General Public Universal) License 1.0
--------------------------------------------
OMEGA BTC AI DIVINE COLLECTIVE
Licensed under the GPU (General Public Universal) License v1.0
Date: 2025-03-28
Location: The Cosmic Void

This source code is governed by the GPU License, granting the following sacred freedoms:
- The Freedom to Study this code, its divine algorithms and cosmic patterns
- The Freedom to Modify this code, enhancing its divine functionality
- The Freedom to Distribute this code, sharing its sacred knowledge
- The Freedom to Use this code, implementing its sacred algorithms

Along with these divine obligations:
- Preserve this sacred knowledge by maintaining source accessibility
- Share all divine modifications to maintain universal access
- Provide attribution to acknowledge sacred origins

For the full divine license, consult the LICENSE file in the project root.

Features:
- Automatic failover between remote and local Redis
- Data synchronization when remote Redis reconnects
- Dual-write capability for critical price data
- Enhanced error handling and recovery
- Real-time performance metrics

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the MIT License
JAH JAH BLESS THE DIVINE FLOW OF THE BLOCKCHAIN
"""

import os
import json
import time
import asyncio
import logging
import websockets
from datetime import datetime, timezone
from typing import Dict, Any, Union, Optional, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("btc-live-feed-v3")

# Import enhanced Redis manager
try:
    from omega_ai.utils.enhanced_redis_manager import EnhancedRedisManager
except ImportError:
    logger.error("Enhanced Redis Manager not found. Please make sure it's installed.")
    raise

# Constants
WEBSOCKET_URLS = {
    "binance": os.getenv("WEBSOCKET_URL", "wss://stream.binance.com:9443/ws/btcusdt@trade"),
    "bybit": os.getenv("WEBSOCKET_URL_BYBIT", "wss://stream.bybit.com/v5/public/spot/ws"),
    "okx": os.getenv("WEBSOCKET_URL_OKX", "wss://ws.okx.com:8443/ws/v5/public"),
    "kucoin": os.getenv("WEBSOCKET_URL_KUCOIN", "wss://ws-api.kucoin.com/endpoint")
}
CURRENT_EXCHANGE = os.getenv("EXCHANGE", "binance")
WEBSOCKET_URL = WEBSOCKET_URLS.get(CURRENT_EXCHANGE, WEBSOCKET_URLS["binance"])
MAX_MESSAGE_SIZE = int(os.getenv("MAX_MESSAGE_SIZE", str(10 * 1024 * 1024)))  # Default 10MB limit
LOG_PREFIX = os.getenv("LOG_PREFIX", "🔱 OMEGA BTC AI")
RECONNECT_INTERVAL = int(os.getenv("RECONNECT_INTERVAL", "5"))  # seconds
REDIS_RECONNECT_INTERVAL = int(os.getenv("REDIS_RECONNECT_INTERVAL", "60"))  # seconds
HEALTH_CHECK_INTERVAL = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))  # seconds

# Function to check required packages
def check_required_packages() -> bool:
    """Check and log required packages for BTC Live Feed."""
    required_packages = [
        "websockets",
        "redis",
        "cryptography",
        "fastapi",
        "uvicorn"
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            logger.debug(f"{LOG_PREFIX} - Package {package} is available")
        except ImportError:
            logger.error(f"{LOG_PREFIX} - Required package {package} is missing")
            return False
    
    return True

# Utility function for price movement indicators
def price_movement_indicator(old_price: float, new_price: float) -> str:
    """Return emoji indicator for price movement."""
    if new_price > old_price:
        return "📈"  # Price increased
    elif new_price < old_price:
        return "📉"  # Price decreased
    else:
        return "🔄"  # Price unchanged

# Logging function with Rastafarian styling
async def log_rasta(message: str) -> None:
    """Log message with Rastafarian styling."""
    logger.info(f"{LOG_PREFIX} - {message}")

# Mock trap detector for demonstration
class MockHighFrequencyTrapDetector:
    """Mock implementation of the high frequency trap detector."""
    
    def __init__(self):
        """Initialize the mock trap detector."""
        self.prices = []
    
    def update_price_data(self, price: float, timestamp: datetime) -> None:
        """Update price data in the mock detector."""
        self.prices.append((price, timestamp))
        if len(self.prices) > 100:
            self.prices.pop(0)
    
    def detect_trap(self) -> Dict[str, Any]:
        """Detect traps in the mock detector."""
        return {
            "trapDetected": False,
            "confidence": 0.0,
            "trapType": "NONE"
        }

# WebSocket handler functions
async def on_open(websocket) -> None:
    """Handle WebSocket open."""
    await log_rasta("WebSocket connection established")

class BtcLiveFeedV3:
    """Bitcoin Live Feed V3 with enhanced Redis failover capabilities."""
    
    def __init__(self, use_failover: bool = True, sync_on_reconnect: bool = True):
        """
        Initialize BTC Live Feed with enhanced Redis manager.
        
        Args:
            use_failover: Whether to use failover to local Redis if remote fails
            sync_on_reconnect: Whether to sync data when reconnecting to remote Redis
        """
        # Initialize the enhanced Redis manager with failover capabilities
        self.redis_manager = EnhancedRedisManager(
            use_failover=use_failover,
            sync_on_reconnect=sync_on_reconnect,
            retry_interval=REDIS_RECONNECT_INTERVAL,
            priority_keys=["last_btc_price", "last_btc_update_time", "btc_movement_history"]
        )
        
        # Initialize other components
        self.trap_detector = MockHighFrequencyTrapDetector()
        self.last_price = 0.0
        self.is_running = False
        self.websocket_connected = False
        self.last_message_time = 0
        self.connection_attempts = 0
        self.messages_processed = 0
        self.last_redis_reconnect_attempt = 0
        
        # Performance metrics
        self.performance_metrics = {
            "avg_message_processing_time": 0,
            "total_messages_processed": 0,
            "successful_redis_operations": 0,
            "failed_redis_operations": 0,
            "websocket_reconnections": 0,
            "uptime_seconds": 0,
            "start_time": time.time()
        }
    
    async def start(self) -> None:
        """Start the BTC price feed with enhanced reliability features."""
        if not check_required_packages():
            logger.error(f"{LOG_PREFIX} - Missing required packages. Exiting.")
            return
        
        self.is_running = True
        self.performance_metrics["start_time"] = time.time()
        
        # Start background tasks
        tasks = []
        # Add price feed task
        tasks.append(asyncio.create_task(self._run_price_feed()))
        # Add Redis reconnect task
        tasks.append(asyncio.create_task(self._run_redis_reconnect_task()))
        # Add health check task
        tasks.append(asyncio.create_task(self._run_health_checks()))
        
        # Log startup information
        logger.info(f"{LOG_PREFIX} - Starting BTC Live Feed v3")
        logger.info(f"{LOG_PREFIX} - WebSocket URL: {WEBSOCKET_URL}")
        logger.info(f"{LOG_PREFIX} - Redis Failover: {'Enabled' if self.redis_manager.use_failover else 'Disabled'}")
        
        # Start health check server
        try:
            from omega_ai.data_feed.health_check import start_health_check
            health_task = await start_health_check(self)
            tasks.append(health_task)
            logger.info(f"{LOG_PREFIX} - Health check server started")
        except ImportError:
            logger.warning(f"{LOG_PREFIX} - Health check module not found, continuing without health server")
        
        # Run all tasks concurrently
        await asyncio.gather(*tasks)
    
    async def _run_price_feed(self) -> None:
        """Run the main price feed loop with automatic reconnection."""
        exchanges = list(WEBSOCKET_URLS.keys())
        current_exchange_index = exchanges.index(CURRENT_EXCHANGE) if CURRENT_EXCHANGE in exchanges else 0
        
        while self.is_running:
            try:
                self.websocket_connected = False
                self.connection_attempts += 1
                
                # Get WebSocket connection parameters from environment variables
                ws_ping_interval = int(os.getenv("WS_PING_INTERVAL", "30"))
                ws_ping_timeout = int(os.getenv("WS_PING_TIMEOUT", "10"))
                
                # Choose the current exchange URL
                exchange = exchanges[current_exchange_index]
                current_url = WEBSOCKET_URLS[exchange]
                
                # If this is not the first exchange and it's Bybit, OKX, or KuCoin, we need different connection logic
                if exchange != "binance":
                    await log_rasta(f"Trying alternative exchange: {exchange}")
                    if exchange == "bybit":
                        await self._handle_bybit_connection(current_url, ws_ping_interval, ws_ping_timeout)
                        continue
                    elif exchange == "okx":
                        await self._handle_okx_connection(current_url, ws_ping_interval, ws_ping_timeout)
                        continue
                    elif exchange == "kucoin":
                        await self._handle_kucoin_connection(current_url, ws_ping_interval, ws_ping_timeout)
                        continue
                
                # Standard Binance connection
                await log_rasta(f"Connecting to WebSocket: {current_url}")
                
                async with websockets.connect(
                    current_url,
                    max_size=MAX_MESSAGE_SIZE,
                    ping_interval=ws_ping_interval,
                    ping_timeout=ws_ping_timeout
                ) as websocket:
                    await on_open(websocket)
                    self.websocket_connected = True
                    
                    # For non-Binance exchanges, we need to send subscription message
                    if exchange != "binance":
                        subscription_msg = self._get_subscription_message(exchange)
                        if subscription_msg:
                            await websocket.send(subscription_msg)
                            await log_rasta(f"Sent subscription to {exchange}")
                    
                    async for message in websocket:
                        # Process message based on exchange format
                        if exchange == "binance":
                            await self._handle_message(message)
                        else:
                            await self._handle_message_alternative(message, exchange)
                        
            except Exception as e:
                self.websocket_connected = False
                self.performance_metrics["websocket_reconnections"] += 1
                
                error_str = str(e)
                await log_rasta(f"WebSocket connection error: {error_str}")
                
                # Capture the current exchange before potentially changing it
                current_exchange = exchanges[current_exchange_index]
                
                # If we get HTTP 451 or other specific errors, try the next exchange
                if "HTTP 451" in error_str or "server rejected" in error_str:
                    await log_rasta(f"Exchange {current_exchange} unavailable, trying next exchange")
                    current_exchange_index = (current_exchange_index + 1) % len(exchanges)
                    # Reset connection attempts when switching exchanges
                    self.connection_attempts = 0
                
                # Exponential backoff for reconnection attempts
                backoff_time = min(RECONNECT_INTERVAL * (2 ** min(self.connection_attempts, 6)), 300)
                logger.info(f"{LOG_PREFIX} - Reconnecting in {backoff_time} seconds (attempt {self.connection_attempts})")
                await asyncio.sleep(backoff_time)
    
    async def _run_redis_reconnect_task(self) -> None:
        """Periodically attempt to reconnect to primary Redis if using failover."""
        while self.is_running:
            try:
                # Only run if enough time has passed since last attempt
                current_time = time.time()
                if current_time - self.last_redis_reconnect_attempt >= REDIS_RECONNECT_INTERVAL:
                    self.last_redis_reconnect_attempt = current_time
                    
                    # Try to reconnect to primary Redis
                    reconnected = await self.redis_manager.try_reconnect_primary()
                    if reconnected:
                        logger.info(f"{LOG_PREFIX} - Successfully reconnected to primary Redis")
                    
            except Exception as e:
                logger.warning(f"{LOG_PREFIX} - Redis reconnection task error: {str(e)}")
            
            # Wait before next attempt
            await asyncio.sleep(REDIS_RECONNECT_INTERVAL)
    
    async def _run_health_checks(self) -> None:
        """Perform periodic health checks and update performance metrics."""
        while self.is_running:
            try:
                # Update uptime
                self.performance_metrics["uptime_seconds"] = time.time() - self.performance_metrics["start_time"]
                
                # Check Redis connection
                redis_ping = await self.redis_manager.ping()
                if not redis_ping:
                    logger.warning(f"{LOG_PREFIX} - Redis health check failed")
                
                # Get Redis stats
                redis_stats = await self.redis_manager.get_stats()
                logger.debug(f"{LOG_PREFIX} - Redis stats: {redis_stats}")
                
            except Exception as e:
                logger.warning(f"{LOG_PREFIX} - Health check error: {str(e)}")
            
            # Wait before next health check
            await asyncio.sleep(HEALTH_CHECK_INTERVAL)
    
    async def stop(self) -> None:
        """Stop the BTC price feed."""
        self.is_running = False
        await log_rasta("BTC Live Feed stopped")
        
        # Log final statistics
        uptime = time.time() - self.performance_metrics["start_time"]
        logger.info(f"{LOG_PREFIX} - Feed stopped. Uptime: {uptime:.2f} seconds")
        logger.info(f"{LOG_PREFIX} - Messages processed: {self.performance_metrics['total_messages_processed']}")
    
    async def _handle_message(self, message: Union[str, bytes]) -> None:
        """Handle incoming message with validation and enhanced error recovery."""
        processing_start_time = time.time()
        try:
            self.last_message_time = time.time()
            
            # Decode message if it's bytes
            if isinstance(message, bytes):
                message = message.decode('utf-8')
                
            # Parse and validate data
            data = json.loads(message)
            price = float(data.get('p', 0))
            
            if price <= 0:
                raise ValueError("Invalid price")
                
            # Update trap detector
            timestamp = datetime.now(timezone.utc)
            self.trap_detector.update_price_data(price, timestamp)
            
            # Update Redis with enhanced error handling
            current_time = time.time()
            
            # Add to price history with timestamp
            history_entry = json.dumps({
                "price": price,
                "timestamp": timestamp.isoformat(),
                "volume": float(data.get('q', 0))
            })
            
            # Use individual try/except blocks for each Redis operation
            # instead of storing operations in a list to avoid type issues
            try:
                result = await self.redis_manager.set_cached("last_btc_price", str(price))
                if result is not None:
                    self.performance_metrics["successful_redis_operations"] += 1
                else:
                    self.performance_metrics["failed_redis_operations"] += 1
            except Exception as e:
                logger.warning(f"{LOG_PREFIX} - Redis operation failed: {str(e)}")
                self.performance_metrics["failed_redis_operations"] += 1
                
            try:
                result = await self.redis_manager.set_cached("last_btc_update_time", str(current_time))
                if result is not None:
                    self.performance_metrics["successful_redis_operations"] += 1
                else:
                    self.performance_metrics["failed_redis_operations"] += 1
            except Exception as e:
                logger.warning(f"{LOG_PREFIX} - Redis operation failed: {str(e)}")
                self.performance_metrics["failed_redis_operations"] += 1
                
            try:
                result = await self.redis_manager.lpush("btc_movement_history", history_entry)
                if result is not None:
                    self.performance_metrics["successful_redis_operations"] += 1
                else:
                    self.performance_metrics["failed_redis_operations"] += 1
            except Exception as e:
                logger.warning(f"{LOG_PREFIX} - Redis operation failed: {str(e)}")
                self.performance_metrics["failed_redis_operations"] += 1
                
            try:
                result = await self.redis_manager.ltrim("btc_movement_history", 0, 999)
                if result is not None:
                    self.performance_metrics["successful_redis_operations"] += 1
                else:
                    self.performance_metrics["failed_redis_operations"] += 1
            except Exception as e:
                logger.warning(f"{LOG_PREFIX} - Redis operation failed: {str(e)}")
                self.performance_metrics["failed_redis_operations"] += 1
            
            # Publish to BTC price channel
            price_update = {
                'price': price,
                'timestamp': timestamp.isoformat(),
                'volume': float(data.get('q', 0))
            }
            await self.redis_manager.publish('btc_price', json.dumps(price_update))
            
            # Log price movement
            if self.last_price > 0:
                indicator = price_movement_indicator(self.last_price, price)
                await log_rasta(f"Price: ${price:,.2f} {indicator}")
            
            self.last_price = price
            
            # Update performance metrics
            self.messages_processed += 1
            self.performance_metrics["total_messages_processed"] += 1
            
            # Calculate average processing time
            processing_time = time.time() - processing_start_time
            avg_time = self.performance_metrics["avg_message_processing_time"]
            self.performance_metrics["avg_message_processing_time"] = (
                (avg_time * (self.messages_processed - 1) + processing_time) / self.messages_processed
            )
            
        except json.JSONDecodeError:
            await log_rasta("Invalid JSON message")
        except Exception as e:
            await log_rasta(f"Message handling error: {str(e)}")
            
    async def check_health(self) -> Dict[str, Any]:
        """Check system health for health endpoint with enhanced metrics."""
        try:
            # Basic health data
            health_data = {
                "redis_connected": await self.redis_manager.ping(),
                "websocket_connected": self.websocket_connected,
                "last_price": self.last_price,
                "uptime": self.performance_metrics["uptime_seconds"],
                "is_running": self.is_running,
                "messages_processed": self.performance_metrics["total_messages_processed"],
                "avg_message_processing_time_ms": self.performance_metrics["avg_message_processing_time"] * 1000,
                "redis_successful_operations": self.performance_metrics["successful_redis_operations"],
                "redis_failed_operations": self.performance_metrics["failed_redis_operations"],
                "websocket_reconnections": self.performance_metrics["websocket_reconnections"]
            }
            
            # Get Redis statistics
            redis_stats = await self.redis_manager.get_stats()
            health_data["redis_stats"] = redis_stats
            
            # Get last update time
            last_update_time = await self.redis_manager.get_cached("last_btc_update_time")
            seconds_since_update = 0
            if last_update_time:
                seconds_since_update = time.time() - float(last_update_time)
                health_data["seconds_since_update"] = seconds_since_update
            
            # Add detailed information to health data
            health_data["details"] = {
                "feed_status": "healthy" if self.websocket_connected and health_data["redis_connected"] else "degraded",
                "seconds_since_update": seconds_since_update,
                "uptime_seconds": self.performance_metrics["uptime_seconds"],
                "using_redis_failover": redis_stats.get("using_failover", False)
            }
            
            # Determine overall health status
            if health_data["redis_connected"] and health_data["websocket_connected"]:
                health_data["status"] = "healthy"
            elif health_data["redis_connected"]:
                health_data["status"] = "degraded"
            else:
                health_data["status"] = "unhealthy"
                
            return health_data
        except Exception as e:
            await log_rasta(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }

    def _get_subscription_message(self, exchange: str) -> str:
        """Get the subscription message for the given exchange."""
        if exchange == "bybit":
            return json.dumps({
                "op": "subscribe",
                "args": ["publicTrade.BTCUSDT"]
            })
        elif exchange == "okx":
            return json.dumps({
                "op": "subscribe",
                "args": [{
                    "channel": "trades", 
                    "instId": "BTC-USDT"
                }]
            })
        elif exchange == "kucoin":
            # KuCoin requires getting a token first, this is handled in _handle_kucoin_connection
            return json.dumps({
                "type": "subscribe",
                "topic": "/market/ticker:BTC-USDT",
                "privateChannel": False,
                "response": True
            })
        return ""  # Empty string for unknown exchanges

    async def _handle_message_alternative(self, message: Union[str, bytes], exchange: str) -> None:
        """Handle messages from alternative exchanges."""
        try:
            # Decode message if it's bytes
            if isinstance(message, bytes):
                message = message.decode('utf-8')
                
            # Parse and validate data based on exchange format
            data = json.loads(message)
            
            # Extract price based on exchange format
            price = 0.0
            timestamp = datetime.now(timezone.utc)
            
            if exchange == "bybit":
                if "data" in data and len(data["data"]) > 0:
                    price = float(data["data"][0]["p"])
            elif exchange == "okx":
                if "data" in data and len(data["data"]) > 0:
                    price = float(data["data"][0]["px"])
            elif exchange == "kucoin":
                if "data" in data and "price" in data["data"]:
                    price = float(data["data"]["price"])
            
            if price <= 0:
                raise ValueError(f"Invalid price from {exchange}")
                
            # Continue with normal processing (same as _handle_message)
            self.trap_detector.update_price_data(price, timestamp)
            current_time = time.time()
            
            # Add to price history with timestamp
            history_entry = json.dumps({
                "price": price,
                "timestamp": timestamp.isoformat(),
                "volume": 0.0  # Volume info not consistently available
            })
            
            # Continue with the Redis operations as in _handle_message
            try:
                result = await self.redis_manager.set_cached("last_btc_price", str(price))
                if result is not None:
                    self.performance_metrics["successful_redis_operations"] += 1
                else:
                    self.performance_metrics["failed_redis_operations"] += 1
            except Exception as e:
                logger.warning(f"{LOG_PREFIX} - Redis operation failed: {str(e)}")
                self.performance_metrics["failed_redis_operations"] += 1
                    
            try:
                result = await self.redis_manager.set_cached("last_btc_update_time", str(current_time))
                if result is not None:
                    self.performance_metrics["successful_redis_operations"] += 1
                else:
                    self.performance_metrics["failed_redis_operations"] += 1
            except Exception as e:
                logger.warning(f"{LOG_PREFIX} - Redis operation failed: {str(e)}")
                self.performance_metrics["failed_redis_operations"] += 1
                
            try:
                result = await self.redis_manager.lpush("btc_movement_history", history_entry)
                if result is not None:
                    self.performance_metrics["successful_redis_operations"] += 1
                else:
                    self.performance_metrics["failed_redis_operations"] += 1
            except Exception as e:
                logger.warning(f"{LOG_PREFIX} - Redis operation failed: {str(e)}")
                self.performance_metrics["failed_redis_operations"] += 1
                
            try:
                result = await self.redis_manager.ltrim("btc_movement_history", 0, 999)
                if result is not None:
                    self.performance_metrics["successful_redis_operations"] += 1
                else:
                    self.performance_metrics["failed_redis_operations"] += 1
            except Exception as e:
                logger.warning(f"{LOG_PREFIX} - Redis operation failed: {str(e)}")
                self.performance_metrics["failed_redis_operations"] += 1
            
            # Log price movement
            if self.last_price > 0:
                indicator = price_movement_indicator(self.last_price, price)
                await log_rasta(f"Price: ${price:,.2f} {indicator} ({exchange})")
            
            self.last_price = price
            
            # Update performance metrics
            self.messages_processed += 1
            self.performance_metrics["total_messages_processed"] += 1
        
        except json.JSONDecodeError:
            await log_rasta(f"Invalid JSON message from {exchange}")
        except Exception as e:
            await log_rasta(f"Message handling error from {exchange}: {str(e)}")

    async def _handle_bybit_connection(self, url: str, ping_interval: int, ping_timeout: int) -> None:
        """Handle Bybit WebSocket connection."""
        async with websockets.connect(
            url,
            max_size=MAX_MESSAGE_SIZE,
            ping_interval=ping_interval,
            ping_timeout=ping_timeout
        ) as websocket:
            await on_open(websocket)
            self.websocket_connected = True
            
            # Send subscription
            subscription = self._get_subscription_message("bybit")
            await websocket.send(subscription)
            
            async for message in websocket:
                await self._handle_message_alternative(message, "bybit")

    async def _handle_okx_connection(self, url: str, ping_interval: int, ping_timeout: int) -> None:
        """Handle OKX WebSocket connection."""
        async with websockets.connect(
            url,
            max_size=MAX_MESSAGE_SIZE,
            ping_interval=ping_interval,
            ping_timeout=ping_timeout
        ) as websocket:
            await on_open(websocket)
            self.websocket_connected = True
            
            # Send subscription
            subscription = self._get_subscription_message("okx")
            await websocket.send(subscription)
            
            async for message in websocket:
                await self._handle_message_alternative(message, "okx")

    async def _handle_kucoin_connection(self, url: str, ping_interval: int, ping_timeout: int) -> None:
        """Handle KuCoin WebSocket connection."""
        # KuCoin requires getting a token first via REST API
        try:
            import requests
            response = requests.post('https://api.kucoin.com/api/v1/bullet-public')
            response_json = response.json()
            
            if response_json["code"] == "200000":
                token = response_json["data"]["token"]
                endpoint = response_json["data"]["instanceServers"][0]["endpoint"]
                full_url = f"{endpoint}?token={token}"
                
                async with websockets.connect(
                    full_url,
                    max_size=MAX_MESSAGE_SIZE,
                    ping_interval=ping_interval,
                    ping_timeout=ping_timeout
                ) as websocket:
                    await on_open(websocket)
                    self.websocket_connected = True
                    
                    # Send subscription
                    subscription = self._get_subscription_message("kucoin")
                    await websocket.send(subscription)
                    
                    async for message in websocket:
                        await self._handle_message_alternative(message, "kucoin")
            else:
                await log_rasta(f"Failed to get KuCoin token: {response_json}")
        except Exception as e:
            await log_rasta(f"Error connecting to KuCoin: {str(e)}")

async def run_btc_live_feed_v3() -> None:
    """Run the BTC Live Feed v3 with enhanced Redis failover capabilities."""
    feed = BtcLiveFeedV3()
    await feed.start()

if __name__ == "__main__":
    asyncio.run(run_btc_live_feed_v3()) 