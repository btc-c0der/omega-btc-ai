#!/usr/bin/env python3
"""
OMEGA BTC AI - DigitalOcean BTC Live Feed V2 🔱
A robust Bitcoin price feed implementation with high-frequency trap detection
and enhanced security features.
"""

import os
import sys
import json
import redis
import asyncio
import websockets
import subprocess
from datetime import datetime, timedelta, UTC
from typing import Dict, Any, List, Optional, Union
from deployment.digitalocean.logging.omega_logger import OmegaLogger
from deployment.digitalocean.redis_manager import DigitalOceanRedisManager
import time

# Initialize logger
omega_logger = OmegaLogger()

# Constants
MAX_MESSAGE_SIZE = 2**20  # 1MB
WEBSOCKET_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"
MAX_PRICE_HISTORY = 1000
RATE_LIMIT_MESSAGES = 100
RATE_LIMIT_WINDOW = 1  # seconds

class MockHighFrequencyTrapDetector:
    """Mock class for testing high-frequency trading trap detection."""
    
    def __init__(self):
        self.price_history = []
        self.last_update = datetime.now(UTC)
        self.message_count = 0
        self.rate_limit_window = 1.0  # 1 second window
        self.rate_limit_messages = 10  # Max 10 messages per window
        self.max_history_size = 1000
    
    def update_price_data(self, price: float, timestamp: datetime) -> None:
        """Update price data with validation and rate limiting."""
        # Rate limiting check first
        now = datetime.now(UTC)
        if (now - self.last_update).total_seconds() <= self.rate_limit_window:
            self.message_count += 1
            if self.message_count > self.rate_limit_messages:
                raise ValueError("Rate limit exceeded")
        else:
            self.message_count = 1
            self.last_update = now
            
        # Validate price
        if not isinstance(price, (int, float)) or price <= 0 or price == float('inf'):
            raise ValueError("Invalid price value")
            
        # Validate timestamp
        if not isinstance(timestamp, datetime):
            raise ValueError("Timestamp must be a datetime object")
            
        if timestamp > datetime.now(UTC):
            raise ValueError("Future timestamp not allowed")
            
        # Update price history
        self.price_history.append((price, timestamp))
        if len(self.price_history) > self.max_history_size:
            self.price_history.pop(0)

def check_required_packages() -> None:
    """Check and install required packages securely."""
    required_packages = [
        'websockets',
        'redis',
        'asyncio'
    ]
    
    for package in required_packages:
        try:
            # Use secure command arguments
            cmd = [
                sys.executable,
                '-m',
                'pip',
                'install',
                '--user',
                package
            ]
            # Validate command arguments
            for arg in cmd:
                if not (arg.isalnum() or arg in ['-', '_', '.'] or arg == sys.executable):
                    raise ValueError("Invalid command arguments detected")
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}: {str(e)}")
            raise

async def send_to_mm_websocket(message: Any) -> None:
    """Send message to WebSocket with security measures."""
    if message is None:
        raise ValueError("Message cannot be None")
        
    # Handle string input (for large message test)
    if isinstance(message, str):
        try:
            message = json.loads(message)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
            
    # Convert number to dict format
    if isinstance(message, (float, int)):
        message = {"price": float(message)}
    elif not isinstance(message, dict):
        raise TypeError("Message must be a number or a dictionary")
        
    # Validate message format
    if isinstance(message, dict) and "price" in message:
        try:
            price = float(message["price"])
            if price <= 0:
                raise ValueError("Invalid price value")
        except (ValueError, TypeError):
            raise ValueError("Invalid price format")
            
    message_str = json.dumps(message)
    if len(message_str) > MAX_MESSAGE_SIZE:
        raise ValueError("Message too large")
        
    try:
        async with websockets.connect(
            WEBSOCKET_URL,
            max_size=MAX_MESSAGE_SIZE,
            ping_interval=30,
            ping_timeout=10
        ) as websocket:
            await websocket.send(message_str)
    except Exception as e:
        await omega_logger.error(f"WebSocket error: {str(e)}")
        raise

def display_price_chart(price: float, history: List[str]) -> str:
    """Display price chart with input validation."""
    if not isinstance(price, (int, float)) or price <= 0:
        raise ValueError("Invalid price value")
        
    for item in history:
        if not isinstance(item, str):
            raise ValueError("Invalid history data type")
        if len(item) > 100:  # Limit string length
            raise ValueError("History item too long")
        if any(c in item for c in [';', '|', '>', '<', '&', "'", '"']):  # Check for shell metacharacters
            raise ValueError("Invalid characters in history data")
    
    chart = f"Current Price: ${price:,.2f}\n"
    chart += "Price History:\n"
    for item in history[-10:]:  # Show last 10 entries
        chart += f"  {item}\n"
    return chart

async def log_rasta(message: str) -> None:
    """Log message with sanitization."""
    # Sanitize message
    message = str(message)
    message = message.replace(';', '')  # Remove potential command injection
    message = ' '.join(message.split())  # Normalize whitespace
    message = message[:1000]  # Limit message length
    
    await omega_logger.info(f"🔱 {message}")

def price_movement_indicator(old_price: float, new_price: float) -> str:
    """Generate price movement indicator with validation."""
    if not all(isinstance(p, (int, float)) for p in [old_price, new_price]):
        raise ValueError("Invalid price values")
    
    diff = new_price - old_price
    if diff > 0:
        return "⬆️"
    elif diff < 0:
        return "⬇️"
    return "➡️"

async def on_message(websocket, message: Union[str, bytes]) -> None:
    """Handle incoming WebSocket message."""
    try:
        if isinstance(message, bytes):
            message = message.decode('utf-8')
            
        data = json.loads(message)
        if not isinstance(data, dict):
            raise ValueError("Invalid message format")
        
        price = float(data.get('p', 0))
        if price <= 0:
            raise ValueError("Invalid price value")
            
        await log_rasta(f"Received price: ${price:,.2f}")
        await send_to_mm_websocket(price)
        
    except json.JSONDecodeError:
        await log_rasta("Invalid JSON message")
    except Exception as e:
        await log_rasta(f"Message handling error: {str(e)}")

async def on_error(websocket, error: Exception) -> None:
    """Handle WebSocket error."""
    await log_rasta(f"WebSocket error: {str(error)}")

async def on_close(websocket, close_status_code: int, close_msg: str) -> None:
    """Handle WebSocket close."""
    await log_rasta(f"WebSocket closed: {close_status_code} - {close_msg}")

async def on_open(websocket) -> None:
    """Handle WebSocket open."""
    await log_rasta("WebSocket connection established")

def get_redis_client() -> redis.Redis:
    """Get a secure Redis client with SSL verification."""
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    redis_password = os.getenv('REDIS_PASSWORD')
    
    # Configure Redis with SSL certificate verification
    connection_kwargs = {
        'host': redis_host,
        'port': redis_port,
        'password': redis_password,
        'ssl': True,
        'ssl_cert_reqs': 'required',
        'decode_responses': True,
        'socket_timeout': 5,
        'socket_connect_timeout': 5,
        'retry_on_timeout': True
    }
    
    redis_client = redis.Redis(**connection_kwargs)
    
    # Test connection
    try:
        redis_client.ping()
    except redis.ConnectionError as e:
        raise ConnectionError(f"Failed to connect to Redis: {str(e)}")
    
    return redis_client

class BtcLiveFeed:
    """Bitcoin Live Feed V2 with enhanced security."""
    
    def __init__(self, redis_manager: DigitalOceanRedisManager):
        """Initialize BTC Live Feed with Redis manager."""
        self.redis_manager = redis_manager
        self.trap_detector = MockHighFrequencyTrapDetector()
        self.last_price = 0.0
        
    async def start(self) -> None:
        """Start the BTC price feed with security measures."""
        check_required_packages()
        
        while True:
            try:
                async with websockets.connect(
                    WEBSOCKET_URL,
                    max_size=MAX_MESSAGE_SIZE,
                    ping_interval=30,
                    ping_timeout=10
                ) as websocket:
                    await on_open(websocket)
                    
                    async for message in websocket:
                        await self._handle_message(message)
                        
            except Exception as e:
                await log_rasta(f"Connection error: {str(e)}")
                await asyncio.sleep(5)  # Backoff before retry
                
    async def _handle_message(self, message: Union[str, bytes]) -> None:
        """Handle incoming message with validation."""
        try:
            if isinstance(message, bytes):
                message = message.decode('utf-8')
                
            data = json.loads(message)
            price = float(data.get('p', 0))
            
            if price <= 0:
                raise ValueError("Invalid price")
                
            # Update trap detector
            self.trap_detector.update_price_data(price, datetime.now(UTC))
            
            # Update Redis
            await self.redis_manager.publish('btc_price', json.dumps({
                'price': price,
                'timestamp': datetime.now(UTC).isoformat()
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
            
    async def check_health(self) -> bool:
        """Check system health."""
        try:
            # Check Redis connection
            await self.redis_manager.ping()
            return True
        except Exception as e:
            await log_rasta(f"Health check failed: {str(e)}")
            return False 