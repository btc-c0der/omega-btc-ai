#!/usr/bin/env python3
"""
OMEGA BTC AI - BTC Live Feed v2
===============================

Enhanced Bitcoin price feed with security measures, designed for Digital Ocean deployment.
"""

import os
import json
import time
import asyncio
import logging
import websockets
from datetime import datetime, timezone
from typing import Dict, Any, Union, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("btc-live-feed-v2")

# Constants
WEBSOCKET_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"
MAX_MESSAGE_SIZE = 10 * 1024 * 1024  # 10MB limit for security
LOG_PREFIX = "🔱 OMEGA BTC AI"
DEFAULT_REDIS_URL = "redis://localhost:6379"

# Redis connection class
class RedisManager:
    """Redis connection manager with security measures."""
    
    def __init__(self):
        """Initialize Redis connection with environment variables."""
        import redis
        
        # Get Redis configuration from environment variables
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", "6379"))
        redis_password = os.getenv("REDIS_PASSWORD", None)
        redis_ssl = os.getenv("REDIS_SSL", "false").lower() == "true"
        
        # SSL configuration
        ssl_cert_reqs = None
        ssl_ca_certs = None
        
        if redis_ssl:
            import ssl
            from cryptography.x509.base import load_pem_x509_certificate
            
            # Get SSL certificate requirement level
            ssl_cert_reqs_str = os.getenv("REDIS_SSL_CERT_REQS", "none").lower()
            if ssl_cert_reqs_str == "required":
                ssl_cert_reqs = ssl.CERT_REQUIRED
            elif ssl_cert_reqs_str == "optional":
                ssl_cert_reqs = ssl.CERT_OPTIONAL
            else:
                # Default to CERT_NONE if not specified or invalid
                ssl_cert_reqs = ssl.CERT_NONE
                logger.info(f"{LOG_PREFIX} - Using SSL CERT_NONE mode for Redis")
                
            # Get SSL certificate path
            ssl_cert_path = os.getenv("REDIS_SSL_CERT_PATH", None)
            if ssl_cert_path and os.path.exists(ssl_cert_path):
                ssl_ca_certs = ssl_cert_path
                logger.info(f"{LOG_PREFIX} - Using SSL certificate from: {ssl_cert_path}")
            else:
                logger.warning(f"{LOG_PREFIX} - SSL certificate path not found: {ssl_cert_path}")
        
        # Connection timeouts
        socket_timeout = int(os.getenv("REDIS_SOCKET_TIMEOUT", "5"))
        socket_connect_timeout = int(os.getenv("REDIS_SOCKET_CONNECT_TIMEOUT", "5"))
        
        try:
            # Initialize Redis client
            self.redis = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                ssl=redis_ssl,
                ssl_cert_reqs=ssl_cert_reqs,
                ssl_ca_certs=ssl_ca_certs,
                socket_timeout=socket_timeout,
                socket_connect_timeout=socket_connect_timeout,
                decode_responses=True
            )
            
            # Test connection
            if self.redis.ping():
                logger.info(f"{LOG_PREFIX} - Connected to Redis at {redis_host}:{redis_port}")
            else:
                logger.warning(f"{LOG_PREFIX} - Connected to Redis but ping failed")
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Redis connection error: {str(e)}")
            # Create a fallback Redis client without SSL if SSL connection fails
            if redis_ssl:
                logger.info(f"{LOG_PREFIX} - Attempting fallback to non-SSL Redis connection")
                try:
                    self.redis = redis.Redis(
                        host=redis_host,
                        port=redis_port,
                        password=redis_password,
                        ssl=False,
                        socket_timeout=socket_timeout,
                        socket_connect_timeout=socket_connect_timeout,
                        decode_responses=True
                    )
                    logger.info(f"{LOG_PREFIX} - Fallback Redis connection established")
                except Exception as e2:
                    logger.error(f"{LOG_PREFIX} - Fallback Redis connection also failed: {str(e2)}")
    
    async def ping(self) -> bool:
        """Check Redis connection with ping."""
        try:
            result = self.redis.ping()
            return bool(result)  # Convert to bool explicitly
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Redis ping failed: {str(e)}")
            return False
    
    async def get_cached(self, key: str) -> Optional[str]:
        """Get cached value from Redis."""
        try:
            return self.redis.get(key)
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Redis get failed: {str(e)}")
            return None
    
    async def set_cached(self, key: str, value: str) -> bool:
        """Set cached value in Redis."""
        try:
            result = self.redis.set(key, value)
            return bool(result) if result is not None else False
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Redis set failed: {str(e)}")
            return False
    
    async def publish(self, channel: str, message: str) -> int:
        """Publish message to Redis channel."""
        try:
            return self.redis.publish(channel, message)
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Redis publish failed: {str(e)}")
            return 0

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

class BtcLiveFeed:
    """Bitcoin Live Feed V2 with enhanced security for Digital Ocean deployment."""
    
    def __init__(self):
        """Initialize BTC Live Feed with Redis manager."""
        self.redis_manager = RedisManager()
        self.trap_detector = MockHighFrequencyTrapDetector()
        self.last_price = 0.0
        self.is_running = False
        self.websocket_connected = False
        self.last_message_time = 0
        
    async def start(self) -> None:
        """Start the BTC price feed with security measures."""
        if not check_required_packages():
            logger.error(f"{LOG_PREFIX} - Missing required packages. Exiting.")
            return
        
        self.is_running = True
        
        # Start health check server
        from omega_ai.data_feed.health_check import start_health_check
        await asyncio.create_task(start_health_check(self))
        
        while self.is_running:
            try:
                self.websocket_connected = False
                
                async with websockets.connect(
                    WEBSOCKET_URL,
                    max_size=MAX_MESSAGE_SIZE,
                    ping_interval=30,
                    ping_timeout=10
                ) as websocket:
                    await on_open(websocket)
                    self.websocket_connected = True
                    
                    async for message in websocket:
                        await self._handle_message(message)
                        
            except Exception as e:
                self.websocket_connected = False
                await log_rasta(f"Connection error: {str(e)}")
                await asyncio.sleep(5)  # Backoff before retry
    
    async def stop(self) -> None:
        """Stop the BTC price feed."""
        self.is_running = False
        await log_rasta("BTC Live Feed stopped")
                
    async def _handle_message(self, message: Union[str, bytes]) -> None:
        """Handle incoming message with validation."""
        try:
            self.last_message_time = time.time()
            
            if isinstance(message, bytes):
                message = message.decode('utf-8')
                
            data = json.loads(message)
            price = float(data.get('p', 0))
            
            if price <= 0:
                raise ValueError("Invalid price")
                
            # Update trap detector
            self.trap_detector.update_price_data(price, datetime.now(timezone.utc))
            
            # Update Redis
            current_time = time.time()
            await self.redis_manager.set_cached("last_btc_price", str(price))
            await self.redis_manager.set_cached("last_btc_update_time", str(current_time))
            
            # Publish to BTC price channel
            await self.redis_manager.publish('btc_price', json.dumps({
                'price': price,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }))
            
            # Log price movement
            if self.last_price > 0:
                indicator = price_movement_indicator(self.last_price, price)
                await log_rasta(f"Price: ${price:,.2f} {indicator}")
            
            self.last_price = price
            
        except json.JSONDecodeError:
            await log_rasta("Invalid JSON message")
        except Exception as e:
            await log_rasta(f"Message handling error: {str(e)}")
            
    async def check_health(self) -> Dict[str, Any]:
        """Check system health for health endpoint."""
        try:
            health_data = {
                "redis_connected": await self.redis_manager.ping(),
                "websocket_connected": self.websocket_connected,
                "last_price": self.last_price,
                "uptime": time.time() - self.last_message_time if self.last_message_time > 0 else None,
                "is_running": self.is_running
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

async def run_btc_live_feed() -> None:
    """Run the BTC Live Feed v2."""
    feed = BtcLiveFeed()
    await feed.start()

if __name__ == "__main__":
    asyncio.run(run_btc_live_feed()) 