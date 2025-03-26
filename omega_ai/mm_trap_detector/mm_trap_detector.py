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
from typing import Optional, Dict, Any
from influxdb_client.client.influxdb_client import InfluxDBClient
from omega_ai.algos.omega_algorithms import OmegaAlgo
from omega_ai.db_manager.database import insert_mm_trap, insert_subtle_movement
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
        self.ws_url = "ws://localhost:8765"  # Binance WebSocket URL
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
            self.redis_conn.hset(
                f"trap_detection:{int(datetime.now(UTC).timestamp())}",
                mapping={
                    "price": str(price),
                    "volume": str(volume),
                    "price_change": str(price_change),
                    "timestamp": timestamp
                }
            )
        except Exception as e:
            print(f"❌ Error registering trap detection: {str(e)}")

    async def analyze_movement(self, current_btc_price: float, prev_btc_price: float, volume: float) -> str:
        """Analyze the current price movement for potential market manipulation."""
        try:
            analysis = await OmegaAlgo.is_fibo_organic(current_btc_price, prev_btc_price, volume)
            return analysis
        except Exception as e:
            print(f"❌ Error in analyze_movement: {str(e)}")
            return "Error in analysis"

    async def print_analysis_result(self, analysis: str, threshold: float) -> None:
        """Print the analysis result with appropriate formatting."""
        try:
            if "Organic" in analysis:
                print(f"{GREEN}✅ ORGANIC MOVEMENT - No manipulation detected{RESET}")
            elif "Insufficient" in analysis:
                print(f"{YELLOW}⚠️  {analysis}{RESET}")
            else:
                print(f"{RED}⛔️ POTENTIAL MANIPULATION DETECTED - {analysis}{RESET}")
                
            print(f"\nCurrent Threshold: ${threshold:.2f}")
        except Exception as e:
            print(f"❌ Error in print_analysis_result: {str(e)}")

    async def process_price_update(self, price: float) -> None:
        """Process a new price update from the WebSocket."""
        try:
            current_time = datetime.now(UTC)
            print(f"\n BTC CHECK | {current_time.strftime('%Y-%m-%d %H:%M:%S')} \n")
            print("═" * 17 + " PRICE UPDATE " + "═" * 17)
            
            # Calculate price changes
            abs_change = price - self.prev_btc_price
            pct_change = (abs_change / self.prev_btc_price) * 100 if self.prev_btc_price != 0 else 0
            
            # Print price information
            print(f"Current BTC: ${price:.2f} {'↑' if abs_change > 0 else '↓' if abs_change < 0 else '→'}")
            print(f"Previous:    ${self.prev_btc_price:.2f}")
            print(f"Abs Change:  ${abs_change:.2f}")
            print(f"% Change:    {pct_change:.4f}%")
            
            # Get current volume and check HF mode
            volume = self.get_current_volume()
            hf_mode = self.check_high_frequency_mode()
            
            # Calculate dynamic threshold
            dynamic_threshold = self.calculate_dynamic_threshold(hf_mode)
            
            print("\n═" * 17 + " MOVEMENT ANALYSIS " + "═" * 17)
            
            # Analyze the movement
            movement_analysis = await self.analyze_movement(price, self.prev_btc_price, volume)
            
            # Print analysis result
            await self.print_analysis_result(movement_analysis, dynamic_threshold)
            
            # Register trap detection if needed
            if "TRAP" in movement_analysis:
                self.register_trap_detection(price, volume, pct_change)
            
            # Update previous price
            self.prev_btc_price = price
            
        except Exception as e:
            print(f"❌ Error processing price update: {str(e)}")

    async def handle_websocket_message(self, message: str) -> None:
        """Handle incoming WebSocket message."""
        try:
            data = json.loads(message)
            price = float(data.get("btc_price", 0))
            print(f"📡 Received BTC Price: ${price:.2f}")
            await self.process_price_update(price)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"❌ Invalid WebSocket Message: {message} | Error: {e}")

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