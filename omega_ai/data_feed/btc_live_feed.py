import json
import websocket
import time
import websockets.client
import websockets.exceptions
import logging
import asyncio
import redis
from datetime import datetime, UTC, timedelta
from enum import Enum
from typing import List, Dict, Optional, Union, Any
import threading
import random
from omega_ai.utils.redis_manager import RedisManager
import rel

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

# Redis Connection - used by legacy functions
redis_conn = redis.Redis(host="localhost", port=6379, db=0)

# Redis health check function from Code version
def check_redis_health():
    """Perform a health check on Redis connection and data integrity."""
    try:
        # Check Redis connection
        redis_manager = RedisManager()
        redis_manager.ping()
        logging.info("Redis connection: OK")

        # Check if essential keys exist
        essential_keys = ["last_btc_price", "prev_btc_price", "btc_movement_history"]
        for key in essential_keys:
            if not redis_manager.get_cached(key):
                logging.warning(f"Essential key missing: {key}")
            else:
                logging.info(f"Essential key present: {key}")

        # Check data integrity
        btc_movement_history = redis_manager.lrange("btc_movement_history", 0, -1)
        logging.info(f"BTC movement history length: {len(btc_movement_history) if btc_movement_history else 0}")

        return True
    except Exception as e:
        logging.error(f"Redis health check failed: {e}")
        return False

# WebSocket integration function from Code version
async def send_to_mm_websocket(price):
    """Send BTC price update to MM WebSocket."""
    while True:
        try:
            async with websockets.client.connect(
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

def on_error(ws, error):
    """Handle WebSocket errors with divine grace."""
    logging.error(f"WebSocket Error: {error}")
    time.sleep(5)  # Add delay before reconnect

def on_close(ws, close_status_code, close_msg):
    """Handle WebSocket closure with Rastafarian resilience."""
    logging.warning(f"WebSocket Closed: {close_status_code} - {close_msg}")
    time.sleep(5)  # Add delay before reconnect
    start_btc_websocket()

def on_open(ws):
    """Handle WebSocket opening with divine blessing."""
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
    
    def __init__(self, sources: Optional[List[PriceSource]] = None, update_interval: float = 5.0):
        """Initialize the blessed BTC price feed."""
        self.sources = sources or [PriceSource.BINANCE, PriceSource.COINBASE]
        self.update_interval = update_interval
        self.redis_manager = RedisManager()
        self.last_price = None
        self.is_running = False
        self._ws = None
        
        # Initialize WebSocket connection immediately
        self.connect_websocket()
    
    def connect_websocket(self):
        """Initialize WebSocket connection to Binance."""
        if not self._ws:
            websocket.enableTrace(True)
            self._ws = websocket.WebSocketApp(
                BINANCE_WS_URL,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
                on_open=self._on_open
            )
            # Start WebSocket connection in a separate thread
            self._ws_thread = threading.Thread(target=self._run_websocket)
            self._ws_thread.daemon = True
            self._ws_thread.start()
    
    def _run_websocket(self):
        """Run WebSocket connection with automatic reconnection."""
        while True:
            try:
                if self._ws:
                    self._ws.run_forever(dispatcher=rel)
                    rel.signal(2, rel.abort)  # Keyboard Interrupt
                    rel.dispatch()
            except Exception as e:
                logging.error(f"WebSocket connection error: {e}")
                time.sleep(5)  # Wait before reconnecting
    
    def _on_message(self, ws: websocket.WebSocket, message: Any) -> None:
        """Process incoming Binance BTC price data."""
        try:
            data = json.loads(message)
            price = float(data["p"])
            volume = float(data["q"])

            logging.info(f"LIVE BTC PRICE UPDATE: ${price:.2f}")
            self.last_price = price
            self.update_redis(price, volume)
        except Exception as e:
            logging.error(f"Error processing message: {e}")

    def _on_error(self, ws: websocket.WebSocket, error: Any) -> None:
        """Handle WebSocket errors with divine grace."""
        logging.error(f"WebSocket Error: {error}")

    def _on_close(self, ws: websocket.WebSocket, close_status_code: Any, close_msg: Any) -> None:
        """Handle WebSocket closure with Rastafarian resilience."""
        logging.warning(f"WebSocket Closed: {close_status_code} - {close_msg}")

    def _on_open(self, ws: websocket.WebSocket) -> None:
        """Handle WebSocket opening with divine blessing."""
        logging.info("Connected to Binance WebSocket - Streaming BTC Prices...")
    
    def update_redis(self, price: float, volume: float) -> None:
        """Save BTC price & volume to Redis for MM Trap Processor with error handling."""
        try:
            if price <= 0:
                logging.warning(f"Skipping Redis update, invalid BTC price: {price}")
                return

            prev_price = self.redis_manager.get_cached("prev_btc_price")
            prev_price = float(prev_price) if prev_price else None  

            if prev_price is None or price != prev_price:
                # Update Redis values using the RedisManager's methods
                self.redis_manager.set_cached("last_btc_price", str(price))
                self.redis_manager.set_cached("last_btc_volume", str(volume if volume else 0))
                self.redis_manager.lpush("btc_movement_history", str(price))
                self.redis_manager.lpush("btc_volume_history", str(volume))
                self.redis_manager.ltrim("btc_movement_history", -100, -1)
                self.redis_manager.ltrim("btc_volume_history", -100, -1)
                
                abs_change = abs(price - prev_price) if prev_price is not None else 0
                abs_change_scaled = abs_change * 100
                self.redis_manager.lpush("abs_price_change_history", str(abs_change_scaled))
                self.redis_manager.ltrim("abs_price_change_history", -100, -1)
                self.redis_manager.set_cached("prev_btc_price", str(price))
                
                # Add last update time
                self.redis_manager.set_cached("last_btc_update_time", str(time.time()))
                
                logging.info(f"Redis Updated: BTC Price = {price:.2f}, Volume = {volume}, Abs Change = {abs_change_scaled:.2f}")
            else:
                logging.debug(f"Price Unchanged, Skipping Redis Update: {price}")

        except Exception as e:
            logging.error(f"Redis Update Failed: {e}")
            # Attempt to reconnect
            try:
                self.redis_manager = RedisManager()
                self.redis_manager.ping()
            except:
                logging.error("Redis reconnection failed.")

    def get_current_price(self) -> float:
        """Get the latest BTC price with divine accuracy."""
        try:
            # Try to get from Redis first
            price_data = self.redis_manager.get_cached("last_btc_price")
            if price_data:
                return float(price_data)
        except Exception as e:
            logging.error(f"Error getting price from Redis: {e}")
        
        # If Redis failed, ensure WebSocket is running
        self.connect_websocket()
        
        # Wait briefly for price update
        time.sleep(0.5)
        try:
            price_data = self.redis_manager.get_cached("last_btc_price")
            if price_data:
                return float(price_data)
        except Exception as e:
            logging.error(f"Error getting price after WebSocket update: {e}")
        
        return 0.0
    
    def _fetch_price_from_source(self, source: PriceSource) -> float:
        """Fetch price from the specified source with divine accuracy."""
        try:
            # Get the latest price from Redis
            price_data = self.redis_manager.get_cached("last_btc_price")
            if price_data:
                return float(price_data)
            
            # If Redis doesn't have the price, ensure WebSocket is running
            if source == PriceSource.BINANCE:
                self.connect_websocket()
                time.sleep(0.5)
                price_data = self.redis_manager.get_cached("last_btc_price")
                if price_data:
                    return float(price_data)
            
            return 0.0
            
        except Exception as e:
            logging.error(f"Error fetching price from {source}: {e}")
            return 0.0
    
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
            
            # Store last price with consistent key
            self.redis_manager.set_cached("last_btc_price", price)
            
            # Store in various time-based lists
            for minutes in [1, 5, 15, 60]:
                key = f"btc_movements_{minutes}min"
                self.redis_manager.lpush(key, price_json)
                self.redis_manager.ltrim(key, 0, 1000)
                
            return True
            
        except Exception as e:
            logging.error(f"Error updating price: {e}")
            return False
    
    def start(self) -> None:
        """Start the blessed price feed."""
        if self.is_running:
            return
            
        self.is_running = True
        
        def update_loop() -> None:
            while self.is_running:
                try:
                    price = self._aggregate_prices()
                    if price > 0:
                        self.update_price(price)
                except Exception as e:
                    logging.error(f"Error in update loop: {e}")
                finally:
                    time.sleep(self.update_interval)
        
        self._ws_thread = threading.Thread(target=update_loop)
        self._ws_thread.daemon = True
        self._ws_thread.start()
        
    def stop(self) -> None:
        """Stop the blessed price feed."""
        self.is_running = False
        if self._ws_thread:
            self._ws_thread.join()

if __name__ == "__main__":
    start_btc_websocket()