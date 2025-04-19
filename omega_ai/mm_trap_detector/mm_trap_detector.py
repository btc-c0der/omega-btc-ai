
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
Market Maker Trap Detection System
=================================

This module implements a real-time Bitcoin price movement analyzer that identifies potential
market maker (MM) manipulation tactics such as liquidity grabs, fake pumps, and fake dumps.
It uses dynamic thresholds, Fibonacci patterns, and multi-timeframe analysis to distinguish
between organic market movements and manipulated price action.

Key Features
-----------
1. Real-time WebSocket connection to Binance for BTC price data
2. Dynamic threshold calculation based on market volatility
3. Multi-layer detection system for various MM tactics
4. Fibonacci-organic analysis
5. High-frequency pattern detection
6. Real-time visualization and alerts

Author: OmegaBTC Team
Version: 1.0
"""

import asyncio
import json
import redis
import websockets
from datetime import datetime, UTC
from typing import Optional, Dict, Any, Union
from influxdb_client.client.influxdb_client import InfluxDBClient
from omega_ai.algos.omega_algorithms import OmegaAlgo
from omega_ai.db_manager.database import insert_possible_mm_trap, insert_subtle_movement
from omega_ai.config import (
    REDIS_HOST, REDIS_PORT, INFLUXDB_URL, INFLUXDB_TOKEN, 
    INFLUXDB_ORG, INFLUXDB_BUCKET, MONITORING_INTERVAL, 
    ERROR_RETRY_INTERVAL, PRICE_PUMP_THRESHOLD, PRICE_DROP_THRESHOLD,
    BASE_TRAP_THRESHOLD
)

# Terminal Colors for visualization
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
BRIGHT_GREEN = "\033[96m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
GOLD = "\033[93m"
YELLOW = "\033[93m"
LIGHT_ORANGE = "\033[38;5;214m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BLACK = "\033[30m"
BLACK_BG = "\033[40m"
BLUE_BG = "\033[44m"
GREEN_BG = "\033[42m"
RED_BG = "\033[41m"
YELLOW_BG = "\033[43m"
BOLD = "\033[1m"

class MMTrapDetector:
    def __init__(self):
        self.redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        self.influxdb_client = None
        self.ws_url = "ws://localhost:8765"  # Updated WebSocket URL
        self.prev_btc_price = 0.0
        self.current_btc_price = 0.0
        self.initialize_influxdb()

    def initialize_influxdb(self) -> None:
        """Initialize InfluxDB connection."""
        try:
            self.influxdb_client = InfluxDBClient(
                url=INFLUXDB_URL,
                token=INFLUXDB_TOKEN,
                org=INFLUXDB_ORG
            )
            self.influxdb_client.ping()
        except Exception as e:
            print(f"❌ Error connecting to InfluxDB: {str(e)}")
            raise

    def get_current_volume(self) -> float:
        """Get the current trading volume from Redis."""
        try:
            volume = self.redis_conn.get("last_btc_volume")
            return float(volume) if volume is not None else 0.0
        except (ValueError, TypeError):
            return 0.0

    def check_high_frequency_mode(self) -> bool:
        """Check if high-frequency mode is active."""
        try:
            hf_mode = self.redis_conn.get("high_frequency_mode")
            return bool(int(hf_mode)) if hf_mode is not None else False
        except (ValueError, TypeError):
            return False

    def calculate_dynamic_threshold(self, hf_mode: bool) -> float:
        """Calculate dynamic threshold based on market conditions."""
        try:
            volatility = self.redis_conn.get("rolling_volatility")
            base_threshold = float(volatility) if volatility else BASE_TRAP_THRESHOLD
            
            market_regime = self.redis_conn.get("market_regime")
            regime = str(market_regime) if market_regime else "normal"
            
            regime_multiplier = {
                "trending": 1.5,
                "volatile": 0.75,
                "normal": 1.0
            }.get(regime, 1.0)
            
            directional_strength_str = self.redis_conn.get("directional_strength")
            directional_strength = float(directional_strength_str) if directional_strength_str else 0.5
            
            adjusted_threshold = base_threshold * regime_multiplier
            if hf_mode:
                adjusted_threshold *= 0.5
            
            print(f"📡 [DEBUG] Rolling Volatility: ${base_threshold:.2f} | Market Regime: {regime} | HF Mode: {'active' if hf_mode else 'inactive'} ({regime_multiplier:.2f}x) | Adjusted Threshold: ${adjusted_threshold:.2f}")
            
            return adjusted_threshold
            
        except Exception as e:
            print(f"❌ Error calculating dynamic threshold: {str(e)}")
            return BASE_TRAP_THRESHOLD

    def register_trap_detection(self, price: float, volume: float, price_change: float = 0.0) -> None:
        """Register a trap detection event."""
        try:
            timestamp = datetime.now(UTC).isoformat()
            trap_data = {
                "type": "price_trap",  # Default trap type
                "price": str(price),
                "volume": str(volume),
                "price_change": str(price_change),
                "timestamp": timestamp,
                "confidence": "0.85"  # Default confidence
            }
            
            # Add to sorted set queue with timestamp as score
            self.redis_conn.zadd(
                "mm_trap_queue:zset",
                {json.dumps(trap_data): int(datetime.now(UTC).timestamp())}
            )
            
            print(f"{GREEN}✅ Trap detection registered in queue{RESET}")
            
        except Exception as e:
            print(f"{RED_BG}{WHITE}❌ Error registering trap detection: {str(e)}{RESET}")
            if hasattr(e, '__traceback__'):
                import traceback
                print(f"{RED}Traceback:{RESET}")
                traceback.print_tb(e.__traceback__)

    async def analyze_movement(self, current_btc_price: float, prev_btc_price: float, volume: float) -> str:
        """Analyze the current price movement for potential market manipulation."""
        try:
            print(f"\n{CYAN}Starting movement analysis...{RESET}")
            print(f"Current Price: ${current_btc_price:.2f}")
            print(f"Previous Price: ${prev_btc_price:.2f}")
            print(f"Volume: {volume:.2f} BTC")
            
            # Calculate price movement metrics
            price_change = current_btc_price - prev_btc_price
            price_change_pct = (price_change / prev_btc_price) * 100 if prev_btc_price != 0 else 0
            
            print(f"\n{YELLOW}Price Movement Metrics:{RESET}")
            print(f"Absolute Change: ${price_change:.2f}")
            print(f"Percentage Change: {price_change_pct:.2f}%")
            
            # Get market conditions
            volatility = self.redis_conn.get("rolling_volatility")
            market_regime = self.redis_conn.get("market_regime")
            
            print(f"\n{YELLOW}Market Conditions:{RESET}")
            print(f"Volatility: ${float(volatility) if volatility else 0:.2f}")
            print(f"Market Regime: {market_regime if market_regime else 'Unknown'}")
            
            # Perform Fibonacci analysis
            print(f"\n{CYAN}Performing Fibonacci analysis...{RESET}")
            analysis = await OmegaAlgo.is_fibo_organic(current_btc_price, prev_btc_price, volume)
            
            # Log analysis result
            if "Organic" in analysis:
                print(f"{GREEN}✅ Analysis Result: Organic Movement{RESET}")
            elif "Insufficient" in analysis:
                print(f"{YELLOW}⚠️ Analysis Result: Insufficient Data{RESET}")
            else:
                print(f"{RED}⛔️ Analysis Result: Potential Manipulation{RESET}")
            
            return analysis
            
        except Exception as e:
            print(f"{RED_BG}{WHITE}❌ Error in analyze_movement: {str(e)}{RESET}")
            if hasattr(e, '__traceback__'):
                import traceback
                print(f"{RED}Traceback:{RESET}")
                traceback.print_tb(e.__traceback__)
            return "Error in analysis"

    async def print_analysis_result(self, analysis: str, threshold: float) -> None:
        """Print the analysis result with appropriate formatting."""
        try:
            print(f"\n{BOLD}{BLUE}═" * 20 + " ANALYSIS RESULT " + "═" * 20 + f"{RESET}")
            
            # Get market conditions for context
            volatility = self.redis_conn.get("rolling_volatility")
            market_regime = self.redis_conn.get("market_regime")
            directional_strength = self.redis_conn.get("directional_strength")
            
            print(f"\n{YELLOW}Market Context:{RESET}")
            print(f"Volatility: ${float(volatility) if volatility else 0:.2f}")
            print(f"Market Regime: {market_regime if market_regime else 'Unknown'}")
            print(f"Directional Strength: {float(directional_strength) if directional_strength else 0:.2f}")
            
            print(f"\n{YELLOW}Detection Threshold:{RESET}")
            print(f"Current Threshold: ${threshold:.2f}")
            
            print(f"\n{YELLOW}Analysis Result:{RESET}")
            if "Organic" in analysis:
                print(f"{GREEN_BG}{BLACK}✅ ORGANIC MOVEMENT{RESET}")
                print(f"{GREEN}No manipulation detected - Price movement follows natural market patterns{RESET}")
            elif "Insufficient" in analysis:
                print(f"{YELLOW_BG}{BLACK}⚠️ INSUFFICIENT DATA{RESET}")
                print(f"{YELLOW}Not enough data points to determine if movement is organic{RESET}")
            else:
                print(f"{RED_BG}{WHITE}⛔️ POTENTIAL MANIPULATION DETECTED{RESET}")
                print(f"{RED}Analysis indicates possible market manipulation:{RESET}")
                print(f"{RED}{analysis}{RESET}")
            
            print(f"\n{BOLD}{BLUE}═" * 50 + f"{RESET}\n")
            
        except Exception as e:
            print(f"{RED_BG}{WHITE}❌ Error in print_analysis_result: {str(e)}{RESET}")
            if hasattr(e, '__traceback__'):
                import traceback
                print(f"{RED}Traceback:{RESET}")
                traceback.print_tb(e.__traceback__)

    async def process_price_update(self, price: float) -> None:
        """Process a new price update from the WebSocket."""
        try:
            current_time = datetime.now(UTC)
            print(f"\n{BOLD}{BLUE}═" * 20 + " PRICE UPDATE " + "═" * 20 + f"{RESET}")
            print(f"{CYAN}Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
            
            # Calculate price changes
            abs_change = price - self.prev_btc_price
            pct_change = (abs_change / self.prev_btc_price) * 100 if self.prev_btc_price != 0 else 0
            
            # Print price information with enhanced formatting
            print(f"\n{GREEN}Current BTC: ${price:.2f} {'↑' if abs_change > 0 else '↓' if abs_change < 0 else '→'}{RESET}")
            print(f"Previous:    ${self.prev_btc_price:.2f}")
            print(f"Abs Change:  ${abs_change:.2f}")
            print(f"% Change:    {pct_change:.4f}%")
            
            # Get current volume and check HF mode
            volume = self.get_current_volume()
            hf_mode = self.check_high_frequency_mode()
            
            # Store price and volume in Redis for historical analysis
            if self.prev_btc_price != 0:  # Only store after we have a previous price
                data_point = f"{price},{volume}"
                self.redis_conn.rpush("btc_movement_history", data_point)
                self.redis_conn.ltrim("btc_movement_history", -1500, -1)  # Keep last 1500 data points
                
                # Store absolute change for volatility calculation
                self.redis_conn.rpush("abs_price_change_history", str(abs(pct_change)))
                self.redis_conn.ltrim("abs_price_change_history", -100, -1)  # Keep last 100 changes
                
                # Calculate and store rolling volatility
                abs_changes = self.redis_conn.lrange("abs_price_change_history", -30, -1)
                if len(abs_changes) > 10:  # Need at least 10 data points
                    volatility = sum(float(c) for c in abs_changes) / len(abs_changes)
                    self.redis_conn.set("rolling_volatility", volatility)
                    
                # Try to determine market regime and update
                try:
                    from omega_ai.algos.omega_algorithms import OmegaAlgo
                    market_regime, multiplier = OmegaAlgo.detect_market_regime()
                    if market_regime != "unknown":
                        self.redis_conn.set("market_regime", market_regime)
                        self.redis_conn.set("regime_multiplier", multiplier)
                except Exception as e:
                    print(f"⚠️ Error updating market regime: {e}")
            
            print(f"\n{YELLOW}Volume: {volume:.2f} BTC{RESET}")
            print(f"HF Mode: {'Active' if hf_mode else 'Inactive'}")
            
            # Calculate dynamic threshold
            dynamic_threshold = self.calculate_dynamic_threshold(hf_mode)
            
            print(f"\n{BOLD}{BLUE}═" * 20 + " MOVEMENT ANALYSIS " + "═" * 20 + f"{RESET}")
            
            # Analyze the movement
            print(f"\n{CYAN}Analyzing price movement...{RESET}")
            movement_analysis = await self.analyze_movement(price, self.prev_btc_price, volume)
            
            # Print analysis result with enhanced formatting
            await self.print_analysis_result(movement_analysis, dynamic_threshold)
            
            # Register trap detection if needed
            if "TRAP" in movement_analysis:
                print(f"\n{RED_BG}{WHITE}⚠️ TRAP DETECTED! Registering detection...{RESET}")
                self.register_trap_detection(price, volume, pct_change)
                print(f"{GREEN}✅ Trap detection registered successfully{RESET}")
            
            # Update previous price
            self.prev_btc_price = price
            
            print(f"\n{BOLD}{BLUE}═" * 50 + f"{RESET}\n")
            
        except Exception as e:
            print(f"{RED_BG}{WHITE}❌ Error processing price update: {str(e)}{RESET}")
            if hasattr(e, '__traceback__'):
                import traceback
                print(f"{RED}Traceback:{RESET}")
                traceback.print_tb(e.__traceback__)

    async def handle_websocket_message(self, message: Union[str, bytes]) -> None:
        """Handle incoming WebSocket message."""
        try:
            # Convert bytes to string if necessary
            if isinstance(message, bytes):
                message = message.decode('utf-8')
            
            print(f"{CYAN}[DEBUG] Raw WebSocket message: {message}{RESET}")
            data = json.loads(message)
            price = float(data.get("btc_price", 0))
            print(f"{CYAN}📡 Received BTC Price: ${price:.2f}{RESET}")
            await self.process_price_update(price)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"{RED_BG}{WHITE}❌ Invalid WebSocket Message: {message} | Error: {e}{RESET}")
        except Exception as e:
            print(f"{RED_BG}{WHITE}❌ Error handling WebSocket message: {str(e)}{RESET}")
            if hasattr(e, '__traceback__'):
                import traceback
                print(f"{RED}Traceback:{RESET}")
                traceback.print_tb(e.__traceback__)

    async def connect_websocket(self) -> None:
        """Connect to WebSocket and handle messages."""
        while True:
            try:
                async with websockets.connect(
                    self.ws_url,
                    max_size=2**24,
                    ping_interval=15,
                    ping_timeout=5,
                    close_timeout=2
                ) as ws:
                    print("✅ Connected to WebSocket Server")
                    async for message in ws:
                        await self.handle_websocket_message(message)
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"❌ WebSocket Disconnected (Error {e.code}) - Reconnecting in 5 seconds...")
                await asyncio.sleep(5)
            except websockets.exceptions.ConnectionClosedOK:
                print("✅ WebSocket Closed Normally. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)
            except websockets.exceptions.WebSocketException as e:
                print(f"❌ WebSocket Error: {e} - Restarting in 5 seconds...")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"❌ Unexpected Error: {e} - Restarting in 5 seconds...")
                await asyncio.sleep(5)

    async def run(self) -> None:
        """Main entry point for the MM Trap Detector."""
        try:
            print("\n 🚀 MM TRAP DETECTOR v1.0 ")
            print("Watching for market manipulation... Babylon can't hide! 🔱\n")
            
            # Get initial BTC price
            self.current_btc_price = float(self.redis_conn.get("last_btc_price") or 0)
            self.prev_btc_price = self.current_btc_price
            print(f"🔰 Last Recorded BTC Price: ${self.current_btc_price:.2f}\n")
            
            # Start WebSocket connection
            await self.connect_websocket()
            
        except KeyboardInterrupt:
            print("\n👋 Gracefully shutting down MM Trap Detector...")
        except Exception as e:
            print(f"❌ Fatal error: {str(e)}")

async def main():
    """Entry point for the MM Trap Detector."""
    detector = MMTrapDetector()
    await detector.run()

if __name__ == "__main__":
    asyncio.run(main()) 