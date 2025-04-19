#!/usr/bin/env python3
"""
OMEGA BTC AI - AIXBT Live Feed v1
================================

WebSocket client for retrieving real-time AIXBT price data with enhanced reliability.
Monitors the AIXBT token in relation to BTC price movements.

🔮 GBU2 (General Blockchain Universe) License 
-------------------------------------------
OMEGA BTC AI DIVINE COLLECTIVE
Licensed under the GBU2 License

This source code is governed by the GBU2 License, granting the following sacred freedoms:
- The Freedom to Study this code, its divine algorithms and cosmic patterns
- The Freedom to Modify this code, enhancing its divine functionality
- The Freedom to Distribute this code, sharing its sacred knowledge
- The Freedom to Use this code, implementing its sacred algorithms

Features:
- Automatic failover between remote and local Redis
- Data synchronization when remote Redis reconnects
- Dual-write capability for critical price data
- Enhanced error handling and recovery
- Real-time performance metrics
- BTC-AIXBT correlation coefficient tracking
- Price divergence detection
- Matrix-themed Virgil Abloh visualization

Copyright (c) 2025 OMEGA-BTC-AI
"THE GRID" — "FOR AIXBT" — "c/o OFF—WHITE™"
"""

import os
import json
import time
import asyncio
import logging
import websockets
import numpy as np
from datetime import datetime, timezone
from typing import Dict, Any, Union, Optional, List
from colorama import Fore, Style, init
import random
import sys
import subprocess
import argparse
import signal

# Initialize colorama
init(autoreset=True)

# ANSI colors for terminal output
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
RESET = Style.RESET_ALL
BOLD = Style.BRIGHT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("aixbt-live-feed-v1")

# Import enhanced Redis manager
try:
    from omega_ai.utils.enhanced_redis_manager import EnhancedRedisManager
except ImportError:
    logger.error("Enhanced Redis Manager not found. Using fallback Redis connection.")
    try:
        import redis
    except ImportError:
        logger.error("Redis package not found. Redis operations will be disabled.")
        redis = None
    EnhancedRedisManager = None

# Constants
AIXBT_WEBSOCKET_URL = "wss://stream.binance.com:9443/ws/aixbtusdt@ticker"
BTC_WEBSOCKET_URL = "wss://stream.binance.com:9443/ws/btcusdt@ticker"
MAX_MESSAGE_SIZE = 10 * 1024 * 1024  # 10MB limit for security
LOG_PREFIX = "🔱 OMEGA AIXBT MATRIX"
RECONNECT_INTERVAL = 5  # seconds
REDIS_RECONNECT_INTERVAL = 60  # seconds
HEALTH_CHECK_INTERVAL = 30  # seconds
AIXBT_DATA_TIMEOUT = 15  # seconds - If no AIXBT data received, use simulated data
AIXBT_PRICE_SIMULATOR_ENABLED = True  # Enable price simulation if no real data

# Redis connection details
REDIS_HOST = "omega-btc-ai-redis-do-user-20389918-0.d.db.ondigitalocean.com"
REDIS_PORT = 25061
REDIS_USERNAME = "default"
REDIS_PASSWORD = "AVNS_OXMpU0P0ByYEz337Fgi"
REDIS_SSL = True

# Check if running in tmux
IN_TMUX = os.environ.get('TMUX') is not None

# Function to check required packages
def check_required_packages() -> bool:
    """Check and log required packages for AIXBT Live Feed."""
    required_packages = [
        "websockets",
        "redis",
        "numpy",
        "colorama",
        "cryptography"
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
        return f"{GREEN}▲{RESET}"  # Price increased
    elif new_price < old_price:
        return f"{RED}▼{RESET}"  # Price decreased
    else:
        return f"{BLUE}■{RESET}"  # Price unchanged

# Calculate correlation coefficient between AIXBT and BTC
def calculate_correlation(aixbt_prices: List[float], btc_prices: List[float]) -> float:
    """Calculate Pearson correlation coefficient between AIXBT and BTC prices."""
    if len(aixbt_prices) < 5 or len(btc_prices) < 5:
        return 0.0
    
    try:
        # Use only the common length of both lists
        min_length = min(len(aixbt_prices), len(btc_prices))
        aixbt = aixbt_prices[-min_length:]
        btc = btc_prices[-min_length:]
        
        return np.corrcoef(aixbt, btc)[0, 1]
    except Exception as e:
        logger.error(f"{LOG_PREFIX} - Error calculating correlation: {e}")
        return 0.0

# Virgil Abloh inspired styling for terminal output
def virgil_abloh_print(message: str, category: str = "INFO", bordered: bool = False) -> None:
    """Print message in Virgil Abloh's design aesthetic."""
    category_color = CYAN if category == "INFO" else YELLOW if category == "WARNING" else RED if category == "ERROR" else MAGENTA
    
    if bordered:
        border = f"{CYAN}{'=' * 60}{RESET}"
        print(border)
        print(f"{category_color}\"" + message.upper() + f"\"   \"{category}\"{RESET}")
        print(border)
    else:
        print(f"{category_color}\"" + message.upper() + f"\"   \"{category}\"{RESET}")

# WebSocket handler
async def on_open(websocket, name: str) -> None:
    """Handle WebSocket open."""
    virgil_abloh_print(f"{name} WebSocket connection established", "CONNECTION")

class AixbtLiveFeedV1:
    """AIXBT Live Feed V1 with BTC correlation tracking."""
    
    def __init__(self, use_failover: bool = True, sync_on_reconnect: bool = True):
        """
        Initialize AIXBT Live Feed with enhanced Redis manager.
        
        Args:
            use_failover: Whether to use failover to local Redis if remote fails
            sync_on_reconnect: Whether to sync data when reconnecting to remote Redis
        """
        # Initialize Redis connection
        self.redis_manager = None
        self.redis_client = None
        
        try:
            # Try to import and use EnhancedRedisManager
            from omega_ai.utils.enhanced_redis_manager import EnhancedRedisManager
            self.redis_manager = EnhancedRedisManager(
                use_failover=use_failover,
                sync_on_reconnect=sync_on_reconnect
            )
            logger.info(f"{LOG_PREFIX} - Using EnhancedRedisManager for Redis operations")
        except ImportError:
            logger.error(f"{LOG_PREFIX} - Enhanced Redis Manager not found. Using fallback Redis connection.")
            try:
                import redis
                
                # Try to get Redis configuration from environment
                host = os.environ.get("REDIS_HOST", "localhost")
                port = int(os.environ.get("REDIS_PORT", 6379))
                db = int(os.environ.get("REDIS_DB", 0))
                password = os.environ.get("REDIS_PASSWORD", None)
                
                # Create direct Redis connection
                self.redis_client = redis.Redis(
                    host=host,
                    port=port,
                    db=db,
                    password=password,
                    decode_responses=True
                )
                logger.info(f"{LOG_PREFIX} - Connected to Redis at {host}:{port}")
            except ImportError:
                logger.error(f"{LOG_PREFIX} - Redis package not found. Redis operations will be disabled.")
            except Exception as e:
                logger.error(f"{LOG_PREFIX} - Failed to connect to Redis: {str(e)}")
        
        # Initialize price tracking
        self.last_aixbt_price = 0.0
        self.last_btc_price = 0.0
        self.aixbt_prices = []
        self.btc_prices = []
        self.correlation_history = []
        self.divergence_history = []
        
        # Initialize connection state
        self.is_running = False
        self.aixbt_websocket_connected = False
        self.btc_websocket_connected = False
        self.connection_attempts = 0
        self.messages_processed = 0
        
        # Track real data vs simulated data
        self.last_aixbt_real_data_time = 0
        self.using_simulated_data = True
        self.simulated_aixbt_base_price = 0.1  # Base price for simulation
        self.simulated_aixbt_variance = 0.02   # Variance for random fluctuations
        self.simulated_btc_correlation = 0.85  # How closely simulated AIXBT follows BTC
        self.aixbt_data_received = False       # Flag to indicate if real data received
        
        # Initialize performance metrics
        self.performance_metrics = {
            "avg_message_processing_time": 0,
            "total_messages_processed": 0,
            "successful_redis_operations": 0,
            "failed_redis_operations": 0,
            "websocket_reconnections": 0,
            "uptime_seconds": 0,
            "start_time": time.time()
        }

        # Initialize activity log history
        self.activity_logs = []
        self.max_log_entries = 10  # Maximum number of log entries to keep
        self.log_activity("System initialized", "SYSTEM", "🚀")
    
    async def start(self) -> None:
        """Start the AIXBT price feed with BTC correlation tracking."""
        if not check_required_packages():
            logger.error(f"{LOG_PREFIX} - Missing required packages. Exiting.")
            return
        
        self.is_running = True
        self.performance_metrics["start_time"] = time.time()
        
        # Clear terminal and show launch message
        os.system('cls' if os.name == 'nt' else 'clear')
        virgil_abloh_print("AIXBT LIVE FEED V1", "SYSTEM LAUNCH", bordered=True)
        virgil_abloh_print("MATRIX INTEGRATION ACTIVE", "GRID LAYER")
        
        # Start background tasks
        tasks = []
        # Add price feed tasks
        tasks.append(asyncio.create_task(self._run_aixbt_price_feed()))
        tasks.append(asyncio.create_task(self._run_btc_price_feed()))
        # Add correlation calculation task
        tasks.append(asyncio.create_task(self._run_correlation_calculator()))
        # Add data simulation task if enabled
        if AIXBT_PRICE_SIMULATOR_ENABLED:
            tasks.append(asyncio.create_task(self._run_price_simulator()))
        # Add visualization task
        tasks.append(asyncio.create_task(self._run_matrix_visualization()))
        
        # Log startup information
        logger.info(f"{LOG_PREFIX} - Starting AIXBT Live Feed v1")
        logger.info(f"{LOG_PREFIX} - AIXBT WebSocket URL: {AIXBT_WEBSOCKET_URL}")
        logger.info(f"{LOG_PREFIX} - BTC WebSocket URL: {BTC_WEBSOCKET_URL}")
        
        # Run all tasks concurrently
        await asyncio.gather(*tasks)
    
    async def _run_aixbt_price_feed(self) -> None:
        """Run the AIXBT price feed loop with automatic reconnection."""
        while self.is_running:
            try:
                self.aixbt_websocket_connected = False
                self.connection_attempts += 1
                
                async with websockets.connect(
                    AIXBT_WEBSOCKET_URL,
                    max_size=MAX_MESSAGE_SIZE,
                    ping_interval=30,
                    ping_timeout=10
                ) as websocket:
                    await on_open(websocket, "AIXBT")
                    self.aixbt_websocket_connected = True
                    
                    async for message in websocket:
                        await self._handle_aixbt_message(message)
                        
            except Exception as e:
                self.aixbt_websocket_connected = False
                self.performance_metrics["websocket_reconnections"] += 1
                logger.error(f"{LOG_PREFIX} - AIXBT WebSocket connection error: {str(e)}")
                
                # Exponential backoff for reconnection attempts
                backoff_time = min(RECONNECT_INTERVAL * (2 ** min(self.connection_attempts, 6)), 300)
                logger.info(f"{LOG_PREFIX} - Reconnecting in {backoff_time} seconds (attempt {self.connection_attempts})")
                await asyncio.sleep(backoff_time)
    
    async def _run_btc_price_feed(self) -> None:
        """Run the BTC price feed loop with automatic reconnection."""
        while self.is_running:
            try:
                self.btc_websocket_connected = False
                self.connection_attempts += 1
                
                async with websockets.connect(
                    BTC_WEBSOCKET_URL,
                    max_size=MAX_MESSAGE_SIZE,
                    ping_interval=30,
                    ping_timeout=10
                ) as websocket:
                    await on_open(websocket, "BTC")
                    self.btc_websocket_connected = True
                    
                    async for message in websocket:
                        await self._handle_btc_message(message)
                        
            except Exception as e:
                self.btc_websocket_connected = False
                self.performance_metrics["websocket_reconnections"] += 1
                logger.error(f"{LOG_PREFIX} - BTC WebSocket connection error: {str(e)}")
                
                # Exponential backoff for reconnection attempts
                backoff_time = min(RECONNECT_INTERVAL * (2 ** min(self.connection_attempts, 6)), 300)
                logger.info(f"{LOG_PREFIX} - Reconnecting in {backoff_time} seconds (attempt {self.connection_attempts})")
                await asyncio.sleep(backoff_time)
    
    async def _run_correlation_calculator(self) -> None:
        """Calculate correlation between AIXBT and BTC prices periodically."""
        while self.is_running:
            try:
                if len(self.aixbt_prices) >= 10 and len(self.btc_prices) >= 10:
                    # Calculate correlation
                    correlation = calculate_correlation(self.aixbt_prices, self.btc_prices)
                    
                    # Track correlation history
                    timestamp = datetime.now(timezone.utc).isoformat()
                    self.correlation_history.append({
                        "timestamp": timestamp,
                        "correlation": correlation
                    })
                    
                    # Keep history limited to prevent memory issues
                    if len(self.correlation_history) > 1000:
                        self.correlation_history = self.correlation_history[-1000:]
                    
                    # Calculate recent divergence
                    if len(self.aixbt_prices) >= 20 and len(self.btc_prices) >= 20:
                        aixbt_change = (self.aixbt_prices[-1] / self.aixbt_prices[-20]) - 1
                        btc_change = (self.btc_prices[-1] / self.btc_prices[-20]) - 1
                        divergence = aixbt_change - btc_change
                        
                        self.divergence_history.append({
                            "timestamp": timestamp,
                            "divergence": divergence
                        })
                        
                        # Keep history limited
                        if len(self.divergence_history) > 1000:
                            self.divergence_history = self.divergence_history[-1000:]
                        
                        # Log significant divergence events
                        if abs(divergence) > 0.02:  # 2% divergence threshold
                            if divergence > 0:
                                self.log_activity(f"AIXBT outperforming BTC by {divergence:.2%}", "SUCCESS", "🚀")
                            else:
                                self.log_activity(f"AIXBT underperforming BTC by {abs(divergence):.2%}", "WARNING", "📉")
                    
                    # Store in Redis using the new helper methods
                    correlation_data = {
                        "timestamp": timestamp,
                        "correlation": correlation,
                        "aixbt_price": self.last_aixbt_price,
                        "btc_price": self.last_btc_price
                    }
                    
                    await self._redis_set("aixbt_btc_correlation", json.dumps(correlation_data))
                    await self._redis_lpush("aixbt_btc_correlation_history", json.dumps(correlation_data), trim=True)
                    
                    # Log significant correlation changes
                    if len(self.correlation_history) > 1 and abs(self.correlation_history[-1]["correlation"] - self.correlation_history[-2]["correlation"]) > 0.1:
                        correlation_trend = "increasing" if self.correlation_history[-1]["correlation"] > self.correlation_history[-2]["correlation"] else "decreasing"
                        self.log_activity(f"Correlation {correlation_trend} to {correlation:.2f}", "INFO", "🔄")
            
            except Exception as e:
                logger.error(f"{LOG_PREFIX} - Error in correlation calculator: {e}")
                self.log_activity(f"Correlation calculation error: {str(e)[:30]}...", "ERROR", "❌")
            
            # Run calculation every 5 seconds
            await asyncio.sleep(5)
    
    async def _run_matrix_visualization(self) -> None:
        """Run the Matrix-themed visualization of AIXBT and BTC data."""
        while self.is_running:
            try:
                # Clear screen
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # Calculate uptime
                uptime = int(time.time() - self.performance_metrics["start_time"])
                uptime_str = f"{uptime // 3600}h {(uptime % 3600) // 60}m {uptime % 60}s"
                
                # Display Virgil Abloh style header
                print(f"{CYAN}{BOLD}{'=' * 60}{RESET}")
                print(f"{MAGENTA}{BOLD}\"AIXBT MATRIX FEED\"   \"LIVE DATA STREAM\"{RESET}")
                print(f"{CYAN}{BOLD}{'=' * 60}{RESET}")
                print(f"{YELLOW}\"TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\" 🕒{RESET}")
                print(f"{CYAN}\"UPTIME: {uptime_str}\" ⏱️  \"SYSTEM STABILITY\"{RESET}")
                print(f"{CYAN}{'─' * 60}{RESET}")
                
                # Display connection status
                aixbt_status = f"{GREEN}CONNECTED{RESET}" if self.aixbt_websocket_connected else f"{RED}DISCONNECTED{RESET}"
                btc_status = f"{GREEN}CONNECTED{RESET}" if self.btc_websocket_connected else f"{RED}DISCONNECTED{RESET}"
                print(f"{CYAN}\"CONNECTION STATUS\" 📡 \"NETWORK LAYER\"{RESET}")
                print(f"  {YELLOW}\"AIXBT WEBSOCKET:\" {aixbt_status}")
                print(f"  {YELLOW}\"BTC WEBSOCKET:\" {btc_status}")
                print(f"{CYAN}{'─' * 60}{RESET}")
                
                # Display price information with simulated data indicator
                aixbt_indicator = price_movement_indicator(self.aixbt_prices[-2] if len(self.aixbt_prices) > 1 else 0, self.last_aixbt_price)
                btc_indicator = price_movement_indicator(self.btc_prices[-2] if len(self.btc_prices) > 1 else 0, self.last_btc_price)
                
                # Add simulated data indicator
                sim_indicator = f" {MAGENTA}[SIM]{RESET}" if self.using_simulated_data else ""
                
                print(f"{CYAN}\"CURRENT PRICES\" 💰 \"MARKET DATA\"{RESET}")
                print(f"  {YELLOW}\"AIXBT:\" ${self.last_aixbt_price:.8f}{sim_indicator} {aixbt_indicator}")
                print(f"  {YELLOW}\"BTC:\" ${self.last_btc_price:.2f} {btc_indicator}")
                print(f"{CYAN}{'─' * 60}{RESET}")
                
                # Display correlation information
                if self.correlation_history:
                    current_correlation = self.correlation_history[-1]["correlation"]
                    correlation_color = GREEN if current_correlation > 0.7 else (YELLOW if current_correlation > 0.3 else RED)
                    correlation_text = f"{correlation_color}{current_correlation:.4f}{RESET}"
                    
                    correlation_strength = "STRONG" if abs(current_correlation) > 0.7 else ("MODERATE" if abs(current_correlation) > 0.3 else "WEAK")
                    correlation_type = "POSITIVE" if current_correlation > 0 else ("NEUTRAL" if current_correlation == 0 else "NEGATIVE")
                    
                    print(f"{CYAN}\"CORRELATION ANALYSIS\" 🔄 \"MATHEMATICAL LAYER\"{RESET}")
                    print(f"  {YELLOW}\"COEFFICIENT:\" {correlation_text}")
                    print(f"  {YELLOW}\"STRENGTH:\" \"{correlation_strength}\"")
                    print(f"  {YELLOW}\"TYPE:\" \"{correlation_type}\"")
                    print(f"{CYAN}{'─' * 60}{RESET}")
                
                # Display divergence information
                if self.divergence_history:
                    current_divergence = self.divergence_history[-1]["divergence"]
                    divergence_color = GREEN if current_divergence > 0 else (YELLOW if current_divergence == 0 else RED)
                    divergence_text = f"{divergence_color}{current_divergence:.4%}{RESET}"
                    
                    divergence_desc = "AIXBT OUTPERFORMING BTC" if current_divergence > 0.005 else (
                                      "AIXBT UNDERPERFORMING BTC" if current_divergence < -0.005 else "SIMILAR PERFORMANCE")
                    
                    print(f"{CYAN}\"DIVERGENCE ANALYSIS\" 📊 \"PERFORMANCE DELTA\"{RESET}")
                    print(f"  {YELLOW}\"DIVERGENCE:\" {divergence_text}")
                    print(f"  {YELLOW}\"STATUS:\" \"{divergence_desc}\"")
                    print(f"{CYAN}{'─' * 60}{RESET}")
                
                # Display messaging statistics
                print(f"{CYAN}\"SYSTEM METRICS\" ⚙️ \"PERFORMANCE LAYER\"{RESET}")
                print(f"  {YELLOW}\"MESSAGES PROCESSED:\" {self.messages_processed}")
                print(f"  {YELLOW}\"AVG PROCESS TIME:\" {self.performance_metrics['avg_message_processing_time']:.4f}ms")
                print(f"  {YELLOW}\"RECONNECTIONS:\" {self.performance_metrics['websocket_reconnections']}")
                
                # Bottom section with logs
                await self._display_activity_log()
                
            except Exception as e:
                logger.error(f"{LOG_PREFIX} - Error in visualization: {e}")
            
            # Update every 2 seconds
            await asyncio.sleep(2)

    async def _display_activity_log(self) -> None:
        """Display the most recent system activity logs in the terminal."""
        # Virgil-inspired logging section
        print(f"\n{CYAN}\"RECENT ACTIVITY\" 📝 \"SYSTEM LOGS\"{RESET}")
        print(f"{CYAN}{'─' * 60}{RESET}")
        
        # Display the most recent log entries
        if not self.activity_logs:
            print(f"{YELLOW}\"[{datetime.now().strftime('%H:%M:%S')}]\" {CYAN}\"No activity logged yet\" ⏳{RESET}")
        else:
            # Display most recent entries (newest first)
            for i, log in enumerate(self.activity_logs[:5]):  # Show up to 5 most recent logs
                category = log["category"]
                color = GREEN if category == "SUCCESS" else RED if category == "ERROR" else YELLOW if category == "WARNING" else BLUE if category == "SYSTEM" else CYAN
                print(f"{YELLOW}\"[{log['timestamp']}]\" {color}\"{log['message']}\" {log['emoji']}{RESET}")
        
        # Virgil-inspired footer
        print(f"{CYAN}{BOLD}{'=' * 60}{RESET}")
        print(f"{MAGENTA}\"THE GRID\"   \"FOR AIXBT\"   \"c/o OFF—WHITE™\"{RESET}")
        print(f"{YELLOW}\"TIME: {datetime.now().strftime('%H:%M:%S')}\" ⏰  \"MADE IN DIGITAL SPACE\"   \"PROTOTYPE-001\"{RESET}")

    async def _handle_aixbt_message(self, message: Union[str, bytes]) -> None:
        """Process AIXBT WebSocket message."""
        start_time = time.time()
        
        try:
            # Parse JSON message
            if isinstance(message, bytes):
                message = message.decode('utf-8')
            
            # Log the raw message for debugging
            logger.info(f"{LOG_PREFIX} - Received AIXBT message: {message[:200]}...")
            
            data = json.loads(message)
            
            # Extract price - handling different message formats
            # For ticker messages (@ticker endpoint), the price is usually in 'c' field
            if 'c' in data:
                # Ticker format (current price in closing price field)
                price = float(data['c'])
                logger.info(f"{LOG_PREFIX} - AIXBT ticker price extracted: {price} from 'c' field")
            elif 'p' in data:
                # Trade format
                price = float(data['p'])
                logger.info(f"{LOG_PREFIX} - AIXBT trade price extracted: {price} from 'p' field")
            elif 'a' in data and 'p' in data['a']:
                # Aggregate trade format
                price = float(data['a']['p'])
                logger.info(f"{LOG_PREFIX} - AIXBT aggTrade price extracted: {price} from 'a.p' field")
            elif 'lastPrice' in data:
                # Some other format
                price = float(data['lastPrice'])
                logger.info(f"{LOG_PREFIX} - AIXBT price extracted: {price} from 'lastPrice' field")
            else:
                # Print data structure for debugging
                logger.warning(f"{LOG_PREFIX} - Unknown AIXBT message format. Keys: {list(data.keys())}")
                # Try to extract any numeric field that might be a price
                possible_price_fields = ['price', 'close', 'last']
                for field in possible_price_fields:
                    if field in data and isinstance(data[field], (str, int, float)):
                        try:
                            price = float(data[field])
                            logger.info(f"{LOG_PREFIX} - AIXBT price extracted from '{field}': {price}")
                            break
                        except Exception:
                            pass
                else:
                    # No price found, log and return
                    logger.warning(f"{LOG_PREFIX} - Cannot extract AIXBT price from message. Skipping.")
                    self.log_activity("Failed to extract AIXBT price", "ERROR", "❌")
                    return
                
            self.last_aixbt_price = price
            
            # Mark as real data
            self.last_aixbt_real_data_time = time.time()
            if self.using_simulated_data:
                self.using_simulated_data = False
                self.log_activity("Switched to real AIXBT data", "SUCCESS", "🔄")
            self.aixbt_data_received = True
            
            # Add to price history
            self.aixbt_prices.append(price)
            if len(self.aixbt_prices) > 1000:
                self.aixbt_prices = self.aixbt_prices[-1000:]
            
            # Create movement data
            timestamp = datetime.now(timezone.utc).isoformat()
            movement_data = {
                "price": price,
                "timestamp": timestamp,
                "volume": float(data.get('q', 0)) if 'q' in data else (float(data.get('v', 0)) if 'v' in data else 0.0),
                "symbol": "AIXBTUSDT",
                "trade_id": data.get('t', 0) if 't' in data else (data.get('T', 0) if 'T' in data else 0),
                "simulated": False
            }
            
            # Store in Redis using the new helper methods
            redis_success = await self._redis_set("last_aixbt_price", str(price))
            await self._redis_set("last_aixbt_update_time", timestamp)
            await self._redis_lpush("aixbt_movement_history", json.dumps(movement_data), trim=True)
            
            # Log activity
            self.log_activity(f"AIXBT price update: ${price:.8f}", "INFO", "📈")
            
            # Update metrics
            self.messages_processed += 1
            process_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Update average processing time using weighted average
            curr_avg = self.performance_metrics["avg_message_processing_time"]
            total_msgs = self.performance_metrics["total_messages_processed"]
            
            if total_msgs == 0:
                self.performance_metrics["avg_message_processing_time"] = process_time
            else:
                self.performance_metrics["avg_message_processing_time"] = (
                    (curr_avg * total_msgs + process_time) / (total_msgs + 1)
                )
            
            self.performance_metrics["total_messages_processed"] += 1
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error processing AIXBT message: {e}")
            self.log_activity(f"Error processing AIXBT message: {str(e)[:30]}...", "ERROR", "❌")
            # Log the exception details for better debugging
            import traceback
            logger.error(f"{LOG_PREFIX} - Exception details: {traceback.format_exc()}")
    
    async def _handle_btc_message(self, message: Union[str, bytes]) -> None:
        """Process BTC WebSocket message."""
        start_time = time.time()
        
        try:
            # Parse JSON message
            if isinstance(message, bytes):
                message = message.decode('utf-8')
            
            # Log the raw message for debugging
            logger.info(f"{LOG_PREFIX} - Received BTC message: {message[:200]}...")
            
            data = json.loads(message)
            
            # Extract price - handling different message formats
            # For ticker messages (@ticker endpoint), the price is usually in 'c' field
            if 'c' in data:
                # Ticker format (current price in closing price field)
                price = float(data['c'])
                logger.info(f"{LOG_PREFIX} - BTC ticker price extracted: {price} from 'c' field")
            elif 'p' in data:
                # Trade format
                price = float(data['p'])
                logger.info(f"{LOG_PREFIX} - BTC trade price extracted: {price} from 'p' field")
            elif 'a' in data and 'p' in data['a']:
                # Aggregate trade format
                price = float(data['a']['p'])
                logger.info(f"{LOG_PREFIX} - BTC aggTrade price extracted: {price} from 'a.p' field")
            elif 'lastPrice' in data:
                # Some other format
                price = float(data['lastPrice'])
                logger.info(f"{LOG_PREFIX} - BTC price extracted: {price} from 'lastPrice' field")
            else:
                # Print data structure for debugging
                logger.warning(f"{LOG_PREFIX} - Unknown BTC message format. Keys: {list(data.keys())}")
                # Try to extract any numeric field that might be a price
                possible_price_fields = ['price', 'close', 'last']
                for field in possible_price_fields:
                    if field in data and isinstance(data[field], (str, int, float)):
                        try:
                            price = float(data[field])
                            logger.info(f"{LOG_PREFIX} - BTC price extracted from '{field}': {price}")
                            break
                        except Exception:
                            pass
                else:
                    # No price found, log and return
                    logger.warning(f"{LOG_PREFIX} - Cannot extract BTC price from message. Skipping.")
                    self.log_activity("Failed to extract BTC price", "ERROR", "❌")
                    return
                
            self.last_btc_price = price
            
            # Add to price history
            self.btc_prices.append(price)
            if len(self.btc_prices) > 1000:
                self.btc_prices = self.btc_prices[-1000:]
            
            # Create movement data
            timestamp = datetime.now(timezone.utc).isoformat()
            movement_data = {
                "price": price,
                "timestamp": timestamp,
                "volume": float(data.get('q', 0)) if 'q' in data else (float(data.get('v', 0)) if 'v' in data else 0.0),
                "symbol": "BTCUSDT",
                "trade_id": data.get('t', 0) if 't' in data else (data.get('T', 0) if 'T' in data else 0)
            }
            
            # Store in Redis using the new helper methods
            redis_success = await self._redis_set("last_btc_price", str(price))
            await self._redis_set("last_btc_update_time", timestamp)
            # We don't push to btc_movement_history as that's handled by the BTC live feed
            
            # Log activity
            self.log_activity(f"BTC price update: ${price:.2f}", "INFO", "💹")
            
            # Update metrics
            self.messages_processed += 1
            process_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Update average processing time
            curr_avg = self.performance_metrics["avg_message_processing_time"]
            total_msgs = self.performance_metrics["total_messages_processed"]
            
            if total_msgs == 0:
                self.performance_metrics["avg_message_processing_time"] = process_time
            else:
                self.performance_metrics["avg_message_processing_time"] = (
                    (curr_avg * total_msgs + process_time) / (total_msgs + 1)
                )
            
            self.performance_metrics["total_messages_processed"] += 1
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error processing BTC message: {e}")
            self.log_activity(f"Error processing BTC message: {str(e)[:30]}...", "ERROR", "❌")
            # Log the exception details for better debugging
            import traceback
            logger.error(f"{LOG_PREFIX} - Exception details: {traceback.format_exc()}")

    async def _run_price_simulator(self) -> None:
        """Simulate AIXBT prices when no real data is received."""
        logger.info(f"{LOG_PREFIX} - Price simulator initialized and ready")
        self.log_activity("Price simulator ready", "SYSTEM", "🤖")
        
        # Wait for initial BTC data
        while self.is_running and len(self.btc_prices) < 5:
            await asyncio.sleep(1)
        
        # Initialize simulated base price if needed
        if self.simulated_aixbt_base_price <= 0:
            # Set base price to approx 1/1000 of BTC price
            if self.last_btc_price > 0:
                self.simulated_aixbt_base_price = self.last_btc_price / 1000
            else:
                self.simulated_aixbt_base_price = 0.1  # Fallback
        
        sim_mode_notified = False
        
        while self.is_running:
            current_time = time.time()
            
            # Check if we need to use simulated data
            if (not self.aixbt_data_received or 
                (current_time - self.last_aixbt_real_data_time) > AIXBT_DATA_TIMEOUT):
                
                # If we haven't received data for a while, use simulation
                if not self.using_simulated_data:
                    self.using_simulated_data = True
                    self.log_activity("Switched to simulated AIXBT data", "WARNING", "🔮")
                    sim_mode_notified = True
                
                # Only generate new price if BTC data is available
                if len(self.btc_prices) > 0:
                    # Calculate new price based on:
                    # 1. Base price
                    # 2. BTC price movement
                    # 3. Random variance
                    
                    # Get BTC price change percent
                    btc_current = self.btc_prices[-1]
                    btc_prev = self.btc_prices[-2] if len(self.btc_prices) > 1 else btc_current
                    btc_change_pct = (btc_current / btc_prev) - 1 if btc_prev > 0 else 0
                    
                    # Calculate AIXBT movement
                    correlation_impact = btc_change_pct * self.simulated_btc_correlation
                    random_variance = (random.random() - 0.5) * self.simulated_aixbt_variance
                    aixbt_change = correlation_impact + random_variance
                    
                    # Calculate new price
                    last_price = self.last_aixbt_price if self.last_aixbt_price > 0 else self.simulated_aixbt_base_price
                    new_price = last_price * (1 + aixbt_change)
                    
                    # Ensure price doesn't go negative
                    new_price = max(0.00000001, new_price)
                    
                    # Update price data
                    self.last_aixbt_price = new_price
                    self.aixbt_prices.append(new_price)
                    if len(self.aixbt_prices) > 1000:
                        self.aixbt_prices = self.aixbt_prices[-1000:]
                    
                    # Store in Redis with simulation flag
                    timestamp = datetime.now(timezone.utc).isoformat()
                    movement_data = {
                        "price": new_price,
                        "timestamp": timestamp,
                        "volume": 0.0,
                        "symbol": "AIXBTUSDT",
                        "trade_id": 0,
                        "simulated": True
                    }
                    
                    # Use the new helper methods
                    await self._redis_set("last_aixbt_price", str(new_price))
                    await self._redis_set("last_aixbt_update_time", timestamp)
                    await self._redis_lpush("aixbt_movement_history", json.dumps(movement_data), trim=True)
                    
                    # Log significant price changes
                    if len(self.aixbt_prices) > 1:
                        pct_change = (new_price / self.aixbt_prices[-2] - 1) * 100
                        if abs(pct_change) > 1.0:  # Log changes greater than 1%
                            direction = "increased" if pct_change > 0 else "decreased"
                            self.log_activity(f"Simulated AIXBT price {direction} by {abs(pct_change):.2f}%", "INFO", "📊")
                    
                    logger.debug(f"{LOG_PREFIX} - Generated simulated AIXBT price: {new_price:.8f}")
            
            # Update every 5 seconds when using simulated data
            await asyncio.sleep(5)

    async def _redis_set(self, key: str, value: str) -> bool:
        """Set a value in Redis safely with proper error handling."""
        # Log available methods for debugging (only once)
        if self.redis_manager is not None and not hasattr(self, "_redis_methods_logged"):
            self._redis_methods_logged = True
            methods = [m for m in dir(self.redis_manager) if not m.startswith('_')]
            logger.info(f"{LOG_PREFIX} - Available EnhancedRedisManager methods: {methods}")
            self.log_activity(f"Redis manager detected with methods: {len(methods)}", "SYSTEM", "🗄️")
        
        # First try with EnhancedRedisManager
        if self.redis_manager is not None:
            try:
                if hasattr(self.redis_manager, "set"):
                    await self.redis_manager.set(key, value)
                    self.performance_metrics["successful_redis_operations"] += 1
                    self.log_activity(f"Redis SET via manager: {key[:15]}...", "SUCCESS", "✅")
                    return True
            except Exception as e:
                logger.error(f"{LOG_PREFIX} - Redis SET error with manager: {e}")
                # Continue to next method if this fails
        
        # Then try with direct Redis client
        if self.redis_client is not None:
            try:
                self.redis_client.set(key, value)
                self.performance_metrics["successful_redis_operations"] += 1
                self.log_activity(f"Redis SET via client: {key[:15]}...", "SUCCESS", "✅")
                return True
            except Exception as e:
                logger.error(f"{LOG_PREFIX} - Redis SET error with client: {e}")
                # Continue to next method if this fails
        
        # If no client, try to create one
        if self.redis_client is None:
            try:
                self._create_direct_redis_connection()
                if self.redis_client:
                    self.redis_client.set(key, value)
                    self.performance_metrics["successful_redis_operations"] += 1
                    self.log_activity(f"Redis SET via new client: {key[:15]}...", "SUCCESS", "✅")
                    return True
            except Exception as e:
                logger.error(f"{LOG_PREFIX} - Redis SET error with new client: {e}")
                self.log_activity(f"Redis SET error: {str(e)[:30]}...", "ERROR", "🔴")
                self.performance_metrics["failed_redis_operations"] += 1
        
        # If we get here, all methods failed
        logger.debug(f"{LOG_PREFIX} - No Redis connection available for SET {key}")
        self.performance_metrics["failed_redis_operations"] += 1
        return False

    async def _redis_lpush(self, key: str, value: str, trim: bool = False, trim_size: int = 9999) -> bool:
        """Push a value to a Redis list safely with proper error handling."""
        # First try with EnhancedRedisManager
        if self.redis_manager is not None:
            try:
                if hasattr(self.redis_manager, "lpush"):
                    await self.redis_manager.lpush(key, value)
                    if trim and hasattr(self.redis_manager, "ltrim"):
                        await self.redis_manager.ltrim(key, 0, trim_size)
                    self.performance_metrics["successful_redis_operations"] += 1
                    return True
            except Exception as e:
                logger.error(f"{LOG_PREFIX} - Redis LPUSH error with manager: {e}")
                # Continue to next method if this fails
        
        # Then try with direct Redis client
        if self.redis_client is not None:
            try:
                self.redis_client.lpush(key, value)
                if trim:
                    self.redis_client.ltrim(key, 0, trim_size)
                self.performance_metrics["successful_redis_operations"] += 1
                return True
            except Exception as e:
                logger.error(f"{LOG_PREFIX} - Redis LPUSH error with client: {e}")
                # Continue to next method if this fails
        
        # If no client, try to create one
        if self.redis_client is None:
            try:
                self._create_direct_redis_connection()
                if self.redis_client:
                    self.redis_client.lpush(key, value)
                    if trim:
                        self.redis_client.ltrim(key, 0, trim_size)
                    self.performance_metrics["successful_redis_operations"] += 1
                    return True
            except Exception as e:
                logger.error(f"{LOG_PREFIX} - Redis LPUSH error with new client: {e}")
                self.log_activity(f"Redis LPUSH error: {str(e)[:30]}...", "ERROR", "🔴")
                self.performance_metrics["failed_redis_operations"] += 1
        
        # If we get here, all methods failed
        logger.debug(f"{LOG_PREFIX} - No Redis connection available for LPUSH {key}")
        self.performance_metrics["failed_redis_operations"] += 1
        return False

    def _create_direct_redis_connection(self) -> None:
        """Create a direct Redis connection if not already available."""
        if self.redis_client is None:
            try:
                import redis
                
                # Try to get Redis configuration from environment
                host = os.environ.get("REDIS_HOST", "omega-btc-ai-redis-do-user-20389918-0.d.db.ondigitalocean.com")
                port = int(os.environ.get("REDIS_PORT", 25061))
                db = int(os.environ.get("REDIS_DB", 0)) 
                username = os.environ.get("REDIS_USERNAME", "default")
                password = os.environ.get("REDIS_PASSWORD", "AVNS_OXMpU0P0ByYEz337Fgi")
                ssl = os.environ.get("REDIS_SSL", "true").lower() in ("true", "1", "yes")
                
                # Log connection attempt
                logger.info(f"{LOG_PREFIX} - Creating direct Redis connection to {host}:{port} (SSL: {ssl})")
                self.log_activity(f"Connecting to Redis at {host}:{port}", "SYSTEM", "🔌")
                
                # Create direct Redis connection
                self.redis_client = redis.Redis(
                    host=host,
                    port=port,
                    db=db,
                    username=username,
                    password=password,
                    ssl=ssl,
                    decode_responses=True
                )
                
                # Test connection
                self.redis_client.ping()
                logger.info(f"{LOG_PREFIX} - Successfully connected to Digital Ocean Redis at {host}:{port}")
                self.log_activity(f"Connected to Digital Ocean Redis", "SUCCESS", "✅")
            except ImportError:
                logger.error(f"{LOG_PREFIX} - Redis package not found. Redis operations will be disabled.")
                self.log_activity("Redis package not found", "ERROR", "❌")
                self.redis_client = None
            except Exception as e:
                logger.error(f"{LOG_PREFIX} - Failed to create direct Redis connection: {str(e)}")
                self.log_activity(f"Redis connection failed: {str(e)[:30]}...", "ERROR", "❌")
                self.redis_client = None

    def log_activity(self, message: str, category: str = "INFO", emoji: str = "ℹ️") -> None:
        """Add an entry to the activity log with timestamp."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = {
            "timestamp": timestamp,
            "message": message,
            "category": category,
            "emoji": emoji
        }
        self.activity_logs.insert(0, log_entry)  # Add to beginning (newest first)
        if len(self.activity_logs) > self.max_log_entries:
            self.activity_logs.pop()  # Remove oldest entry

    async def _run_price_display(self) -> None:
        """Run the price display to show current status in the terminal."""
        # Initialize display refresh interval
        last_full_refresh = 0
        while not self.should_stop:
            try:
                current_time = time.time()
                
                # Only do a full display refresh every 0.5 seconds
                if current_time - last_full_refresh > 0.5:
                    # Don't clear the screen in tmux mode
                    if not IN_TMUX:
                        # Clear terminal and display status
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(self.generate_status_display())
                    
                    last_full_refresh = current_time
                
                # Sleep briefly to prevent high CPU usage
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"{LOG_PREFIX} - Display error: {e}")
                await asyncio.sleep(1)

    def generate_status_display(self) -> str:
        """Generate a string representation of the current system status for display."""
        uptime_seconds = int(time.time() - self.performance_metrics["start_time"])
        uptime_hours = uptime_seconds // 3600
        uptime_minutes = (uptime_seconds % 3600) // 60
        uptime_seconds = uptime_seconds % 60
        
        # Gather all status information
        status_lines = []
        
        # Header
        status_lines.append(f"{CYAN}{BOLD}{'=' * 60}{RESET}")
        status_lines.append(f"{BOLD}{MAGENTA}\"AIXBT MATRIX FEED\"   \"LIVE DATA STREAM\"{RESET}")
        status_lines.append(f"{CYAN}{BOLD}{'=' * 60}{RESET}")
        
        # Timestamp and uptime
        status_lines.append(f"{YELLOW}\"TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\" 🕒{RESET}")
        status_lines.append(f"{YELLOW}\"UPTIME: {uptime_hours}h {uptime_minutes}m {uptime_seconds}s\" ⏱️  \"SYSTEM STABILITY\"{RESET}")
        status_lines.append(f"{CYAN}{'-' * 60}{RESET}")
        
        # Connection status
        status_lines.append(f"{BOLD}\"CONNECTION STATUS\" 📡 \"NETWORK LAYER\"{RESET}")
        aixbt_status = f"{GREEN}CONNECTED{RESET}" if self.aixbt_websocket_connected else f"{RED}DISCONNECTED{RESET}"
        btc_status = f"{GREEN}CONNECTED{RESET}" if self.btc_websocket_connected else f"{RED}DISCONNECTED{RESET}"
        status_lines.append(f"  \"AIXBT WEBSOCKET:\" {aixbt_status}")
        status_lines.append(f"  \"BTC WEBSOCKET:\" {btc_status}")
        status_lines.append(f"{CYAN}{'-' * 60}{RESET}")
        
        # Price information
        status_lines.append(f"{BOLD}\"CURRENT PRICES\" 💰 \"MARKET DATA\"{RESET}")
        
        # AIXBT price with indicator
        if self.last_aixbt_price > 0:
            # Format with 8 decimal places for small values
            price_str = f"${self.last_aixbt_price:.8f}"
            # Add [SIM] tag if using simulated data
            sim_tag = f" [{YELLOW}SIM{RESET}]" if self.using_simulated_data else ""
            
            # Show price movement
            if len(self.aixbt_prices) > 1:
                prev_price = self.aixbt_prices[-2] if len(self.aixbt_prices) > 1 else self.last_aixbt_price
                movement = price_movement_indicator(prev_price, self.last_aixbt_price)
            else:
                movement = "■"
                
            status_lines.append(f"  \"AIXBT:\" {price_str}{sim_tag} {movement}")
        else:
            status_lines.append(f"  \"AIXBT:\" ${self.last_aixbt_price:.8f} {YELLOW}[SIM]{RESET} ■")
            
        # BTC price with indicator
        if self.last_btc_price > 0:
            # Format with 2 decimal places for BTC
            price_str = f"${self.last_btc_price:.2f}"
            
            # Show price movement
            if len(self.btc_prices) > 1:
                prev_price = self.btc_prices[-2] if len(self.btc_prices) > 1 else self.last_btc_price
                movement = price_movement_indicator(prev_price, self.last_btc_price)
            else:
                movement = "■"
                
            status_lines.append(f"  \"BTC:\" {price_str} {movement}")
        else:
            status_lines.append(f"  \"BTC:\" ${self.last_btc_price:.2f} ■")
            
        # Correlation information if we have sufficient data
        if len(self.aixbt_prices) > 5 and len(self.btc_prices) > 5:
            # Calculate correlation for different time frames
            short_corr = calculate_correlation(self.aixbt_prices[-10:], self.btc_prices[-10:])
            med_corr = calculate_correlation(self.aixbt_prices[-30:], self.btc_prices[-30:])
            long_corr = calculate_correlation(self.aixbt_prices[-100:], self.btc_prices[-100:]) if len(self.aixbt_prices) >= 100 else 0
            
            # Format correlations with appropriate colors
            short_color = GREEN if short_corr > 0.5 else RED if short_corr < -0.5 else YELLOW
            med_color = GREEN if med_corr > 0.5 else RED if med_corr < -0.5 else YELLOW
            long_color = GREEN if long_corr > 0.5 else RED if long_corr < -0.5 else YELLOW
            
            status_lines.append(f"  \"CORRELATION:\" 10m:{short_color}{short_corr:.2f}{RESET} 30m:{med_color}{med_corr:.2f}{RESET} ALL:{long_color}{long_corr:.2f}{RESET}")
            
        status_lines.append(f"{CYAN}{'-' * 60}{RESET}")
        
        # System metrics
        status_lines.append(f"{BOLD}\"SYSTEM METRICS\" ⚙️ \"PERFORMANCE LAYER\"{RESET}")
        status_lines.append(f"  \"MESSAGES PROCESSED:\" {self.messages_processed}")
        status_lines.append(f"  \"AVG PROCESS TIME:\" {self.performance_metrics['avg_message_processing_time']:.4f}ms")
        status_lines.append(f"  \"RECONNECTIONS:\" {self.performance_metrics['websocket_reconnections']}")
        
        # Activity log
        status_lines.append(f"{BOLD}\"RECENT ACTIVITY\" 📝 \"SYSTEM LOGS\"{RESET}")
        status_lines.append(f"{CYAN}{'-' * 60}{RESET}")
        
        # Show most recent log entries
        for i, log in enumerate(self.activity_logs[:5]):  # Show up to 5 most recent logs
            category = log["category"]
            color = GREEN if category == "SUCCESS" else RED if category == "ERROR" else YELLOW if category == "WARNING" else BLUE if category == "SYSTEM" else CYAN
            status_lines.append(f"{YELLOW}\"[{log['timestamp']}]\" {color}\"{log['message']}\" {log['emoji']}{RESET}")
        
        # Virgil-inspired footer
        status_lines.append(f"{CYAN}{BOLD}{'=' * 60}{RESET}")
        status_lines.append(f"{MAGENTA}\"THE GRID\"   \"FOR AIXBT\"   \"c/o OFF—WHITE™\"{RESET}")
        status_lines.append(f"{YELLOW}\"TIME: {datetime.now().strftime('%H:%M:%S')}\" ⏰  \"MADE IN DIGITAL SPACE\"   \"PROTOTYPE-001\"{RESET}")
        
        # Combine all lines into a single string
        return "\n".join(status_lines)

async def run_aixbt_live_feed_v1() -> None:
    """Run the AIXBT Live Feed V1 as a standalone application."""
    feed = AixbtLiveFeedV1()
    try:
        await feed.start()
    except KeyboardInterrupt:
        logger.info(f"{LOG_PREFIX} - Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"{LOG_PREFIX} - Unexpected error: {e}")
    finally:
        await feed.stop()
        logger.info(f"{LOG_PREFIX} - AIXBT Live Feed V1 stopped")

def main():
    """Entry point for running the AIXBT Live Feed V1 in normal mode."""
    try:
        asyncio.run(run_aixbt_live_feed_v1())
    except KeyboardInterrupt:
        print("\nAIXBT Live Feed V1 stopped. Exiting gracefully.")

def main_tmux():
    """Entry point for running the AIXBT Live Feed V1 with tmux support."""
    args = parse_args()
    
    try:
        if args.tmux:
            # Run with tmux split panels
            asyncio.run(run_aixbt_live_feed_v1_tmux())
        else:
            # Run in normal mode
            asyncio.run(run_aixbt_live_feed_v1())
    except KeyboardInterrupt:
        print("\nAIXBT Live Feed V1 stopped. Exiting gracefully.")

if __name__ == "__main__":
    main_tmux() 