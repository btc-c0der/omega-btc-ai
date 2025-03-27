import json
import websocket
import time
import websockets
import websockets.exceptions
import logging
import asyncio
import redis
from datetime import datetime, UTC, timedelta
from enum import Enum
from typing import List, Dict, Optional, Union, Any
import threading
import random
import os

# Set Redis host environment variable
os.environ['REDIS_HOST'] = 'localhost'

from omega_ai.utils.redis_manager import RedisManager
import rel

# Configure logging with Rasta colors
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Rasta color constants
GREEN_RASTA = "\033[92m"  # Jah Green
YELLOW_RASTA = "\033[93m"  # Gold
RED_RASTA = "\033[91m"    # Babylon Red
BLUE_RASTA = "\033[94m"   # Zion Blue
MAGENTA_RASTA = "\033[95m"  # Royal Purple
CYAN_RASTA = "\033[96m"   # Ocean Blue
RESET = "\033[0m"
BOLD = "\033[1m"

# Rasta logging functions
def log_rasta(message: str, color: str = GREEN_RASTA, level: str = "info"):
    """Log with Rasta style and colors."""
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")
    if level == "error":
        print(f"{RED_RASTA}[{timestamp}] ❌ {message}{RESET}")
    elif level == "warning":
        print(f"{YELLOW_RASTA}[{timestamp}] ⚠️  {message}{RESET}")
    elif level == "success":
        print(f"{GREEN_RASTA}[{timestamp}] ✅ {message}{RESET}")
    else:
        print(f"{color}[{timestamp}] ℹ️  {message}{RESET}")

def display_rasta_banner():
    """Display the Rasta-style banner."""
    banner = f"""
{GREEN_RASTA}╔══════════════════════════════════════════════════════════╗
     ██████╗ ███╗   ███╗███████╗ ██████╗  █████╗ 
    ██╔═══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗
    ██║   ██║██╔████╔██║█████╗  ██║  ███╗███████║
    ██║   ██║██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║
    ╚██████╔╝██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║
     ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝
                {YELLOW_RASTA}BTC AI SYSTEM v1.0
              [ Rasta Price Feed - One Love ]{GREEN_RASTA}
╚══════════════════════════════════════════════════════════╝{RESET}
"""
    print(banner)

# Binance WebSocket API
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"

# MM WebSocket Server URL with updated port
MM_WS_URL = "ws://localhost:8765"

# Redis Connection - used by legacy functions
redis_conn = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', '6379')),
    db=0
)

# Redis health check function from Code version
def check_redis_health():
    """Perform a health check on Redis connection and data integrity."""
    try:
        # Check Redis connection using localhost directly
        redis_host = 'localhost'  # Use localhost directly
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_manager = RedisManager(host=redis_host, port=redis_port)
        redis_manager.ping()
        log_rasta(f"Redis connection: OK (Host: {redis_host}, Port: {redis_port})", GREEN_RASTA, "success")

        # Check if essential keys exist
        essential_keys = ["last_btc_price", "prev_btc_price", "btc_movement_history"]
        for key in essential_keys:
            if not redis_manager.get_cached(key) and key != "btc_movement_history":
                log_rasta(f"Essential key missing: {key}", YELLOW_RASTA, "warning")
            elif key == "btc_movement_history":
                # For list type, we need to check differently
                history = redis_manager.lrange(key, 0, 0)
                if not history:
                    log_rasta(f"Essential key missing: {key}", YELLOW_RASTA, "warning")
                else:
                    log_rasta(f"Essential key present: {key}", GREEN_RASTA, "success")
            else:
                log_rasta(f"Essential key present: {key}", GREEN_RASTA, "success")

        # Check data integrity
        btc_movement_history = redis_manager.lrange("btc_movement_history", 0, -1)
        log_rasta(f"BTC movement history length: {len(btc_movement_history) if btc_movement_history else 0}", BLUE_RASTA)
        
        # Check data format
        if btc_movement_history:
            sample = btc_movement_history[0]
            if "," in sample:
                try:
                    price_str, volume_str = sample.split(",")
                    price = float(price_str)
                    volume = float(volume_str)
                    log_rasta(f"Data format OK - Sample: Price=${price:.2f}, Volume={volume}", GREEN_RASTA, "success")
                except Exception as e:
                    log_rasta(f"Invalid data format in btc_movement_history: {e}", YELLOW_RASTA, "warning")
            else:
                log_rasta("Data format missing volume information", YELLOW_RASTA, "warning")

        return True
    except Exception as e:
        log_rasta(f"Redis health check failed: {e}", RED_RASTA, "error")
        return False

# WebSocket integration function from Code version
async def send_to_mm_websocket(price):
    """Send BTC price update to MM WebSocket."""
    while True:
        try:
            async with websockets.connect(
                MM_WS_URL,
                max_size=2**20,
                ping_interval=30,
                ping_timeout=10
            ) as ws:
                log_rasta(f"Connected to MM WebSocket", GREEN_RASTA, "success")
                await ws.send(json.dumps({"btc_price": price}))
                log_rasta(f"BTC Price Sent: ${price:.2f}", BLUE_RASTA)
                return  # Exit loop on success
        except websockets.exceptions.ConnectionClosedOK:
            log_rasta(f"WebSocket Closed Normally, reconnecting...", YELLOW_RASTA, "warning")
        except websockets.exceptions.ConnectionClosedError as e:
            log_rasta(f"WebSocket Disconnected (Error {e.code}), retrying...", RED_RASTA, "error")
        except Exception as e:
            log_rasta(f"WebSocket Error: {e}, retrying...", RED_RASTA, "error")
        
        await asyncio.sleep(5)  # Persistent retry mechanism

def on_error(ws, error):
    """Handle WebSocket errors with divine grace."""
    log_rasta(f"WebSocket Error: {error}", RED_RASTA, "error")
    time.sleep(5)  # Add delay before reconnect

def on_message(ws, message):
    """Process incoming Binance BTC price data."""
    try:
        data = json.loads(message)
        price = float(data["p"])
        volume = float(data["q"])

        log_rasta(f"LIVE BTC PRICE UPDATE: ${price:.2f} (Vol: {volume})", BLUE_RASTA)
        
        # Update Redis values using the RedisManager with localhost connection
        redis_host = 'localhost'  # Use localhost directly
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_manager = RedisManager(host=redis_host, port=redis_port)
        prev_price = redis_manager.get_cached("prev_btc_price")
        prev_price = float(prev_price) if prev_price else None

        if prev_price is None or price != prev_price:
            # Store both price and volume values separately
            redis_manager.set_cached("last_btc_price", str(price))
            redis_manager.set_cached("last_btc_volume", str(volume))
            
            # Store combined price and volume data in history
            combined_data = f"{price},{volume}"
            redis_manager.lpush("btc_movement_history", combined_data)
            redis_manager.ltrim("btc_movement_history", -100, -1)
            
            abs_change = abs(price - prev_price) if prev_price is not None else 0
            abs_change_scaled = abs_change * 100
            redis_manager.lpush("abs_price_change_history", str(abs_change_scaled))
            redis_manager.ltrim("abs_price_change_history", -100, -1)
            redis_manager.set_cached("prev_btc_price", str(price))
            
            # Add last update time
            redis_manager.set_cached("last_btc_update_time", str(time.time()))
            
            log_rasta(f"Redis Updated: BTC Price = {price:.2f}, Volume = {volume}, Abs Change = {abs_change_scaled:.2f}", GREEN_RASTA)
            
            # Send price update to MM WebSocket server
            asyncio.run(send_to_mm_websocket(price))
            
            # Notify the high frequency detector about price update
            try:
                # Import here to avoid circular import issues
                from omega_ai.mm_trap_detector.high_frequency_detector import hf_detector
                
                # Update the detector with the new price
                timestamp = datetime.now(UTC)
                hf_detector.update_price_data(price, timestamp)
                
                # Check for high frequency mode activation
                hf_active, multiplier = hf_detector.detect_high_freq_trap_mode(price)
                if hf_active:
                    log_rasta(f"⚠️ HIGH FREQUENCY TRAP MODE ACTIVATED! Multiplier: {multiplier}", RED_RASTA, "warning")
            except ImportError:
                log_rasta("MM Trap Detector module not available", YELLOW_RASTA, "warning")
            except Exception as e:
                log_rasta(f"Error notifying MM Trap Detector: {e}", YELLOW_RASTA, "warning")
        else:
            log_rasta(f"Price Unchanged, Skipping Redis Update: {price}", YELLOW_RASTA)

    except Exception as e:
        log_rasta(f"Error processing message: {e}", RED_RASTA, "error")

def on_close(ws, close_status_code, close_msg):
    """Handle WebSocket closure with Rastafarian resilience."""
    log_rasta(f"WebSocket Closed: {close_status_code} - {close_msg}", YELLOW_RASTA, "warning")
    time.sleep(5)  # Add delay before reconnect
    start_btc_websocket()

def on_open(ws):
    """Handle WebSocket opening with divine blessing."""
    log_rasta("Connected to Binance WebSocket - Streaming BTC Prices...", GREEN_RASTA, "success")

def start_btc_websocket():
    """Start WebSocket connection to Binance BTC Live Feed."""
    while True:
        try:
            if not check_redis_health():
                log_rasta("Redis health check failed. Retrying in 60 seconds...", RED_RASTA, "error")
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
            log_rasta(f"Error in WebSocket connection: {e}", RED_RASTA, "error")
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
        
        # Use direct localhost connection for Redis
        redis_host = 'localhost'
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        self.redis_manager = RedisManager(host=redis_host, port=redis_port)
        
        self.last_price = None
        self.last_volume = None
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
                log_rasta(f"WebSocket connection error: {e}", RED_RASTA, "error")
                time.sleep(5)  # Wait before reconnecting
    
    def _on_message(self, ws: websocket.WebSocket, message: Any) -> None:
        """Process incoming Binance BTC price data."""
        try:
            data = json.loads(message)
            price = float(data["p"])
            volume = float(data["q"])

            log_rasta(f"LIVE BTC PRICE UPDATE: ${price:.2f} (Vol: {volume})", BLUE_RASTA)
            self.last_price = price
            self.last_volume = volume
            self.update_redis(price, volume)
        except Exception as e:
            log_rasta(f"Error processing message: {e}", RED_RASTA, "error")

    def _on_error(self, ws: websocket.WebSocket, error: Any) -> None:
        """Handle WebSocket errors with divine grace."""
        log_rasta(f"WebSocket Error: {error}", RED_RASTA, "error")

    def _on_close(self, ws: websocket.WebSocket, close_status_code: Any, close_msg: Any) -> None:
        """Handle WebSocket closure with Rastafarian resilience."""
        log_rasta(f"WebSocket Closed: {close_status_code} - {close_msg}", YELLOW_RASTA, "warning")

    def _on_open(self, ws: websocket.WebSocket) -> None:
        """Handle WebSocket opening with divine blessing."""
        log_rasta("Connected to Binance WebSocket - Streaming BTC Prices...", GREEN_RASTA, "success")
    
    def update_redis(self, price: float, volume: float) -> None:
        """Save BTC price & volume to Redis for MM Trap Processor with error handling."""
        try:
            if price <= 0:
                log_rasta(f"Skipping Redis update, invalid BTC price: {price}", YELLOW_RASTA)
                return

            prev_price = self.redis_manager.get_cached("prev_btc_price")
            prev_price = float(prev_price) if prev_price else None  

            if prev_price is None or price != prev_price:
                # Update Redis values using the RedisManager's methods
                self.redis_manager.set_cached("last_btc_price", str(price))
                self.redis_manager.set_cached("last_btc_volume", str(volume if volume else 0))
                
                # Store combined price and volume data
                combined_data = f"{price},{volume}"
                self.redis_manager.lpush("btc_movement_history", combined_data)
                self.redis_manager.ltrim("btc_movement_history", -100, -1)
                
                abs_change = abs(price - prev_price) if prev_price is not None else 0
                abs_change_scaled = abs_change * 100
                self.redis_manager.lpush("abs_price_change_history", str(abs_change_scaled))
                self.redis_manager.ltrim("abs_price_change_history", -100, -1)
                self.redis_manager.set_cached("prev_btc_price", str(price))
                
                # Add last update time
                self.redis_manager.set_cached("last_btc_update_time", str(time.time()))
                
                log_rasta(f"Redis Updated: BTC Price = {price:.2f}, Volume = {volume}, Abs Change = {abs_change_scaled:.2f}", GREEN_RASTA)
                
                # Notify the high frequency detector about price update
                try:
                    # Import here to avoid circular import issues
                    from omega_ai.mm_trap_detector.high_frequency_detector import hf_detector
                    
                    # Update the detector with the new price
                    timestamp = datetime.now(UTC)
                    hf_detector.update_price_data(price, timestamp)
                    
                    # Check for high frequency mode activation
                    hf_active, multiplier = hf_detector.detect_high_freq_trap_mode(price)
                    if hf_active:
                        log_rasta(f"⚠️ HIGH FREQUENCY TRAP MODE ACTIVATED! Multiplier: {multiplier}", RED_RASTA, "warning")
                except ImportError:
                    log_rasta("MM Trap Detector module not available", YELLOW_RASTA, "warning")
                except Exception as e:
                    log_rasta(f"Error notifying MM Trap Detector: {e}", YELLOW_RASTA, "warning")
            else:
                log_rasta(f"Price Unchanged, Skipping Redis Update: {price}", YELLOW_RASTA)

        except Exception as e:
            log_rasta(f"Redis Update Failed: {e}", RED_RASTA, "error")
            # Attempt to reconnect
            try:
                self.redis_manager = RedisManager()
                self.redis_manager.ping()
            except:
                log_rasta("Redis reconnection failed.", RED_RASTA, "error")

    def get_current_price(self) -> float:
        """Get the latest BTC price with divine accuracy."""
        try:
            # Try to get from Redis first
            price_data = self.redis_manager.get_cached("last_btc_price")
            if price_data:
                return float(price_data)
        except Exception as e:
            log_rasta(f"Error getting price from Redis: {e}", RED_RASTA, "error")
        
        # If Redis failed, ensure WebSocket is running
        self.connect_websocket()
        
        # Wait briefly for price update
        time.sleep(0.5)
        try:
            price_data = self.redis_manager.get_cached("last_btc_price")
            if price_data:
                return float(price_data)
        except Exception as e:
            log_rasta(f"Error getting price after WebSocket update: {e}", RED_RASTA, "error")
        
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
            log_rasta(f"Error fetching price from {source}: {e}", RED_RASTA, "error")
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
            if not raw_data:
                # Try the main btc_movement_history key
                raw_data = self.redis_manager.lrange("btc_movement_history", 0, count-1)
                
            if raw_data:
                for item in raw_data:
                    try:
                        # Try to parse as JSON first (for formatted data)
                        data_item = json.loads(item)
                        history.append(data_item)
                    except json.JSONDecodeError:
                        # Handle raw format "price,volume"
                        if "," in item:
                            try:
                                price_str, volume_str = item.split(",")
                                price = float(price_str)
                                volume = float(volume_str)
                                timestamp = datetime.now(UTC).isoformat()
                                history.append({
                                    "price": price,
                                    "volume": volume,
                                    "timestamp": timestamp
                                })
                            except Exception:
                                # Fallback to just price
                                price = float(item)
                                history.append({
                                    "price": price,
                                    "timestamp": datetime.now(UTC).isoformat()
                                })
                        else:
                            # Simple price format
                            price = float(item)
                            history.append({
                                "price": price,
                                "timestamp": datetime.now(UTC).isoformat()
                            })
        except Exception as e:
            log_rasta(f"Error getting price history: {e}", RED_RASTA, "error")
            
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
            log_rasta(f"Error updating price: {e}", RED_RASTA, "error")
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
                    log_rasta(f"Error in update loop: {e}", RED_RASTA, "error")
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
    display_rasta_banner()
    log_rasta("Initializing Rasta Price Feed...", GREEN_RASTA)
    log_rasta(f"Redis Host: {os.getenv('REDIS_HOST', 'localhost')}", BLUE_RASTA)
    log_rasta("Connecting to Binance WebSocket...", BLUE_RASTA)
    start_btc_websocket()