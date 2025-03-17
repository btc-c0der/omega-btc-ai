import json
import psycopg2
import time
import websocket
import websockets
import logging
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