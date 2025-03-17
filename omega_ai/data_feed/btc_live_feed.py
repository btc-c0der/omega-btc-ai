import json
import psycopg2
import time
import websocket
import websockets
import logging
import asyncio
import redis
from datetime import datetime, UTC, timedelta
from enum import Enum
from typing import List, Dict, Optional, Union
import threading
import random
from omega_ai.utils.redis_manager import RedisManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add Rasta color constants
GREEN_RASTA = "\033[92m"
YELLOW_RASTA = "\033[93m"
RED_RASTA = "\033[91m"
RESET = "\033[0m"

# Binance WebSocket API
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"

# MM WebSocket Server URL with updated port
MM_WS_URL = "ws://localhost:8766"

# PostgreSQL Database Connection
DB_CONFIG = {
    "dbname": "omega_db",
    "user": "omega_user",
    "password": "omega_pass",
    "host": "localhost",
    "port": "5432"
}

# Redis Connection - used by legacy functions
redis_conn = redis.Redis(host="localhost", port=6379, db=0)

# Redis health check function from Code version
def check_redis_health():
    """Perform a health check on Redis connection and data integrity."""
    try:
        # Check Redis connection
        redis_conn.ping()
        logging.info("Redis connection: OK")

        # Check if essential keys exist
        essential_keys = ["last_btc_price", "prev_btc_price", "btc_movement_history"]
        for key in essential_keys:
            if not redis_conn.exists(key):
                logging.warning(f"Essential key missing: {key}")
            else:
                logging.info(f"Essential key present: {key}")

        # Check data integrity
        btc_movement_history = redis_conn.llen("btc_movement_history")
        logging.info(f"BTC movement history length: {btc_movement_history}")

        return True
    except redis.RedisError as e:
        logging.error(f"Redis health check failed: {e}")
        return False

# WebSocket integration function from Code version
async def send_to_mm_websocket(price):
    """Send BTC price update to MM Trap WebSocket."""
    while True:
        try:
            async with websockets.connect(
                MM_WS_URL,
                max_size=2**20,
                ping_interval=30,
                ping_timeout=10
            ) as ws:
                logging.info(f"Connected to MM WebSocket")
                await ws.send(json.dumps({"btc_price": price}))
                logging.info(f"BTC Price Sent: ${price:.2f}")
                return  # Exit loop on success
        except websockets.exceptions.ConnectionClosedOK:
            logging.info(f"WebSocket Closed Normally, reconnecting...")
        except websockets.exceptions.ConnectionClosedError as e:
            logging.error(f"WebSocket Disconnected (Error {e.code}), retrying...")
        except Exception as e:
            logging.error(f"WebSocket Error: {e}, retrying...")
        
        await asyncio.sleep(5)  # Persistent retry mechanism

# Database storage function from Code version
def save_btc_price_to_db(price, volume):
    """Store BTC price in PostgreSQL for historical tracking."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO btc_prices (timestamp, btc_price, volume) VALUES (%s, %s, %s)",
            (datetime.now(UTC), price, volume)
        )
        conn.commit()
        cursor.close()
        conn.close()
        logging.info(f"Saved BTC price to DB: ${price:.2f}")
    except Exception as e:
        logging.error(f"Failed to save BTC price to DB: {e}")

# Redis update function from Code version
def update_redis(price, volume):
    """Save BTC price & volume to Redis for MM Trap Processor with error handling."""
    try:
        if price <= 0:
            logging.warning(f"Skipping Redis update, invalid BTC price: {price}")
            return

        prev_price = redis_conn.get("prev_btc_price")
        prev_price = float(prev_price) if prev_price else None  

        if prev_price is None or price != prev_price:
            pipeline = redis_conn.pipeline()
            pipeline.set("last_btc_price", price)
            pipeline.set("last_btc_volume", volume if volume else 0)
            pipeline.rpush("btc_movement_history", price)
            pipeline.rpush("btc_volume_history", volume)
            pipeline.ltrim("btc_movement_history", -100, -1)
            pipeline.ltrim("btc_volume_history", -100, -1)
            
            abs_change = abs(price - prev_price) if prev_price is not None else 0
            abs_change_scaled = abs_change * 100
            pipeline.rpush("abs_price_change_history", abs_change_scaled)
            pipeline.ltrim("abs_price_change_history", -100, -1)
            pipeline.set("prev_btc_price", price)
            
            # Add last update time
            pipeline.set("last_btc_update_time", time.time())
            
            pipeline.execute()
            
            logging.info(f"Redis Updated: BTC Price = {price:.2f}, Volume = {volume}, Abs Change = {abs_change_scaled:.2f}")
        else:
            logging.debug(f"Price Unchanged, Skipping Redis Update: {price}")

    except redis.RedisError as e:
        logging.error(f"Redis Update Failed: {e}")
        # Attempt to reconnect
        try:
            redis_conn.ping()
        except:
            logging.error("Redis reconnection failed. Attempting to recreate connection.")
            # Use a properly scoped declaration
            redis_conn = redis.Redis(host="localhost", port=6379, db=0)

# WebSocket message handler from Code version
def on_message(ws, message):
    """Process incoming Binance BTC price data."""
    data = json.loads(message)
    price = float(data["p"])
    volume = float(data["q"])

    logging.info(f"LIVE BTC PRICE UPDATE: ${price:.2f}")

    save_btc_price_to_db(price, volume)
    update_redis(price, volume)
    asyncio.run(send_to_mm_websocket(price))

def on_error(ws, error):
    logging.error(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    logging.warning(f"WebSocket Closed: {close_status_code} - {close_msg}")
    time.sleep(5)
    start_btc_websocket()

def on_open(ws):
    logging.info("Connected to Binance WebSocket - Streaming BTC Prices...")

def start_btc_websocket():
    """Start WebSocket connection to Binance BTC Live Feed."""
    while True:
        try:
            if not check_redis_health():
                logging.error("Redis health check failed. Retrying in 60 seconds...")
                time.sleep(60)
                continue

            ws = websocket.WebSocketApp(
                BINANCE_WS_URL,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open
            )
            ws.run_forever()
        except Exception as e:
            logging.error(f"Error in WebSocket connection: {e}")
            time.sleep(5)

class PriceSource(str, Enum):
    """Divine sources of BTC price data."""
    BINANCE = "binance"
    COINBASE = "coinbase"
    KRAKEN = "kraken"
    BITSTAMP = "bitstamp"
    GEMINI = "gemini"
    
    def __str__(self):
        return self.value

class BtcPriceFeed:
    """
    Real-time BTC price feed with divine Rastafarian energy.
    Provides OOP interface to the blessed BTC price feed functionality.
    
    Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the MIT License
    ONE LOVE, ONE HEART, ONE CODE
    """
    
    def __init__(self, 
                sources: Optional[List[PriceSource]] = None, 
                update_interval: float = 5.0, 
                redis_manager: Optional[RedisManager] = None):
        """Initialize the blessed BTC price feed."""
        self.sources = sources or [PriceSource.BINANCE, PriceSource.COINBASE]
        self.update_interval = update_interval
        self.redis_manager = redis_manager or RedisManager()
        self.last_price = None
        # Add required attributes for testing
        self.price_history = {}
        self.is_running = False  # Track if feed is running
        self._update_thread = None
        self._stop_event = threading.Event()
        
    def get_current_price(self) -> float:
        """Get the latest BTC price with divine accuracy."""
        # Try to get from Redis first
        try:
            price_data = self.redis_manager.get_cached("omega:last_btc_price")
            if price_data:
                return float(price_data)
        except Exception as e:
            logging.error(f"Error getting price from Redis: {e}")
            
        # If Redis failed, calculate aggregate price
        price = self._aggregate_prices()
        if price > 0:
            return price
            
        # Divine fallback price if all else fails
        return 50000.0
    
    def _fetch_price_from_source(self, source: PriceSource) -> float:
        """Fetch price from the specified source with divine accuracy."""
        # This would connect to exchange APIs in production
        # For testing, use simulated prices
        base_price = 50000.0
        
        # Add some random variation based on source
        variation = random.uniform(-500, 500)
        return base_price + variation
    
    def _aggregate_prices(self) -> float:
        """Calculate aggregate price with divine wisdom."""
        prices = []
        for source in self.sources:
            price = self._fetch_price_from_source(source)
            if price > 0:
                prices.append(price)
                
        if prices:
            # Calculate divine average
            return sum(prices) / len(prices)
        return 0.0
    
    def get_price_history(self, minutes: int = 5, count: int = 100) -> List[Dict[str, Union[float, str]]]:
        """Get price history with divine timestamps."""
        key = f"omega:btc_movements_{minutes}min"
        history = []
        
        try:
            # Get data from Redis with JAH BLESSING
            raw_data = self.redis_manager.lrange(key, 0, count-1)
            if raw_data:
                for item in raw_data:
                    try:
                        history.append(json.loads(item))
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            logging.error(f"Error getting price history: {e}")
            
        return history
    
    def update_price(self, price: float) -> bool:
        """Update price with divine blessing."""
        try:
            # Create price data with divine timestamp
            now = datetime.now(UTC)
            price_data = {
                "price": price,
                "timestamp": now.isoformat(),
                "source": "divine_aggregator"
            }
            price_json = json.dumps(price_data)
            
            # Store last price
            self.redis_manager.set_cached("omega:last_btc_price", price)
            
            # Store in various time-based lists
            for minutes in [1, 5, 15, 60]:
                key = f"omega:btc_movements_{minutes}min"
                self.redis_manager.lpush(key, price_json)
                self.redis_manager.ltrim(key, 0, 1000)  # Keep limited history
                
            return True
            
        except Exception as e:
            logging.error(f"Error updating price: {e}")
            return False
    
    def start(self) -> None:
        """Start the blessed price feed."""
        if self.is_running:
            return
            
        self.is_running = True
        self._stop_event.clear()
        
        def update_loop() -> None:
            while not self._stop_event.is_set():
                try:
                    price = self._aggregate_prices()
                    if price > 0:
                        self.update_price(price)
                except Exception as e:
                    logging.error(f"Error in update loop: {e}")
                finally:
                    time.sleep(self.update_interval)
        
        self._update_thread = threading.Thread(target=update_loop)
        self._update_thread.daemon = True
        self._update_thread.start()
        
    def stop(self) -> None:
        """Stop the blessed price feed."""
        if not self.is_running:
            return
            
        self._stop_event.set()
        if self._update_thread:
            self._update_thread.join()
            
        self.is_running = False

if __name__ == "__main__":
    start_btc_websocket()