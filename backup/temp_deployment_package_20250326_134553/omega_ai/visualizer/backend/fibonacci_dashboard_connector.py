#!/usr/bin/env python3

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
OMEGA BTC AI - Fibonacci Dashboard Connector
============================================

This script connects the enhanced market trend analyzer (with extended Fibonacci levels)
to the Reggae Dashboard UI by updating the Redis keys used by the dashboard.

It extracts Fibonacci data from the monitor_market_trends.py output and 
formats it for display in the dashboard.
"""

import redis
import json
import time
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
import threading
import asyncio
import random

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("fibonacci_dashboard_connector")

# Terminal colors for enhanced visibility
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

class FibonacciDashboardConnector:
    """Connects the Fibonacci analyzer to the Reggae Dashboard."""
    
    def __init__(self, 
                redis_host: str = "localhost", 
                redis_port: int = 6379,
                update_interval: float = 1.0):
        """
        Initialize the dashboard connector.
        
        Args:
            redis_host: Redis host
            redis_port: Redis port
            update_interval: Update interval in seconds
        """
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.update_interval = update_interval
        self.running = False
        self._thread = None
        
        # Connect to Redis
        try:
            self.redis = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=0,
                decode_responses=True
            )
            # Test connection
            self.redis.ping()
            logger.info(f"Connected to Redis at {redis_host}:{redis_port}")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    def get_fibonacci_data(self) -> Tuple[Dict[str, float], float]:
        """
        Get Fibonacci levels and current price from Redis.
        
        Returns:
            Tuple of (fib_levels_dict, current_price)
        """
        try:
            # Get current price
            current_price = float(self.redis.get("last_btc_price") or 0)
            
            # Get Fibonacci levels from Redis
            fib_levels = {}
            fib_levels_json = self.redis.get("fibonacci:current_levels")
            
            if fib_levels_json:
                try:
                    fib_levels = json.loads(fib_levels_json)
                except json.JSONDecodeError:
                    logger.warning("Failed to parse Fibonacci levels JSON")
            
            return fib_levels, current_price
        except Exception as e:
            logger.error(f"Error getting Fibonacci data: {e}")
            return {}, 0.0
    
    def get_market_trend_data(self) -> Dict[str, Any]:
        """
        Get market trend data from various Redis keys.
        
        Returns:
            Dictionary with market trend data
        """
        try:
            result = {}
            
            # Get current price
            result["current_price"] = float(self.redis.get("last_btc_price") or 0)
            
            # Get various timeframe trends
            timeframes = [1, 5, 15, 30, 60, 240, 720, 1444]
            result["timeframes"] = {}
            
            for tf in timeframes:
                key = f"btc_trend_{tf}min"
                trend_data = self.redis.get(key)
                if trend_data:
                    try:
                        result["timeframes"][f"{tf}min"] = json.loads(trend_data)
                    except json.JSONDecodeError:
                        pass
            
            return result
        except Exception as e:
            logger.error(f"Error getting market trend data: {e}")
            return {}
    
    def check_fibonacci_alignment(self, fib_levels: Dict[str, float], current_price: float) -> Optional[Dict[str, Any]]:
        """
        Check if current price aligns with any Fibonacci level.
        
        Args:
            fib_levels: Dictionary of Fibonacci levels
            current_price: Current BTC price
            
        Returns:
            Alignment data if found, None otherwise
        """
        if not fib_levels or current_price == 0:
            return None
        
        # Check each Fibonacci level for alignment
        best_alignment = None
        min_distance_pct = float('inf')
        
        for level, price in fib_levels.items():
            # Calculate distance percentage
            distance_pct = abs((current_price - price) / price * 100)
            
            # If this is the closest level so far
            if distance_pct < min_distance_pct:
                min_distance_pct = distance_pct
                best_alignment = {
                    "type": "GOLDEN_RATIO",
                    "level": level,
                    "price": price,
                    "distance_pct": distance_pct,
                    "confidence": max(0, 1 - (distance_pct / 5))  # 5% max distance for confidence
                }
        
        # Only return if we're within 5% of a level
        if best_alignment and best_alignment["distance_pct"] <= 5.0:
            return best_alignment
        
        return None
    
    def update_trap_probability_data(self, fib_levels: Dict[str, float], current_price: float) -> None:
        """
        Update the trap probability data in Redis for the dashboard.
        
        Args:
            fib_levels: Dictionary of Fibonacci levels
            current_price: Current BTC price
        """
        try:
            # Check for Fibonacci alignment
            alignment = self.check_fibonacci_alignment(fib_levels, current_price)
            
            # Get market trend data 
            market_data = self.get_market_trend_data()
            
            # Prepare base probability data
            base_probability = 0.3  # Base probability
            
            # Increase probability if there's a Fibonacci alignment
            if alignment:
                probability = base_probability + (alignment["confidence"] * 0.6)
                trap_type = f"Fibonacci Confluence ({alignment['level']})"
                confidence = alignment["confidence"]
                jah_message = f"JAH WISDOM REVEALS GOLDEN RATIO AT {alignment['level']} (${alignment['price']:,.2f})!"
            else:
                probability = base_probability
                trap_type = "Potential Pattern"
                confidence = 0.4
                jah_message = "JAH GUIDES THE TRADING PATH. SEEK THE GOLDEN RATIO!"
            
            # Add components analysis
            components = {
                "fibonacci_alignment": 0.0,
                "price_action": 0.0,
                "trend_strength": 0.0,
                "volume_analysis": 0.0,
                "market_regime": 0.0
            }
            
            # Set component values based on data
            if alignment:
                components["fibonacci_alignment"] = alignment["confidence"]
            
            # Get trend from 15min timeframe if available
            trend_direction = "neutral"
            trend_strength = 0.5
            
            if "timeframes" in market_data and "15min" in market_data["timeframes"]:
                tf_data = market_data["timeframes"]["15min"]
                if "trend" in tf_data:
                    trend = tf_data["trend"]
                    if "Bullish" in trend:
                        trend_direction = "bullish"
                        components["trend_strength"] = 0.7
                        if "Strongly" in trend:
                            components["trend_strength"] = 0.9
                    elif "Bearish" in trend:
                        trend_direction = "bearish"
                        components["trend_strength"] = 0.7
                        if "Strongly" in trend:
                            components["trend_strength"] = 0.9
            
            # Set other components with some randomness for now
            components["price_action"] = random.uniform(0.3, 0.8)
            components["volume_analysis"] = random.uniform(0.2, 0.7)
            components["market_regime"] = random.uniform(0.4, 0.6)
            
            # Create the trap probability data structure
            trap_data = {
                "probability": probability,
                "trap_type": trap_type,
                "confidence": confidence,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "trend": trend_direction,
                "components": components,
                "jah_message": jah_message
            }
            
            # Add extended Fibonacci data
            trap_data["fibonacci_data"] = {
                "current_price": current_price,
                "levels": fib_levels,
                "alignment": alignment
            }
            
            # Store in Redis for dashboard
            self.redis.set("current_trap_probability", json.dumps(trap_data))
            
            # Add to history
            self.redis.lpush("trap_probability_history", json.dumps(trap_data))
            self.redis.ltrim("trap_probability_history", 0, 99)  # Keep last 100 records
            
            logger.info(f"Updated trap probability: {probability:.2f} (Type: {trap_type})")
        except Exception as e:
            logger.error(f"Error updating trap probability: {e}")
    
    def run_update_loop(self):
        """Run the update loop in a separate thread."""
        self.running = True
        
        while self.running:
            try:
                # Get Fibonacci data
                fib_levels, current_price = self.get_fibonacci_data()
                
                # Update trap probability data
                self.update_trap_probability_data(fib_levels, current_price)
                
                # Sleep for the update interval
                time.sleep(self.update_interval)
            except Exception as e:
                logger.error(f"Error in update loop: {e}")
                time.sleep(5)  # Sleep longer on error
    
    def start(self):
        """Start the connector in a separate thread."""
        if self._thread is not None and self._thread.is_alive():
            logger.warning("Connector is already running")
            return
        
        logger.info("Starting Fibonacci Dashboard Connector")
        self._thread = threading.Thread(target=self.run_update_loop)
        self._thread.daemon = True
        self._thread.start()
    
    def stop(self):
        """Stop the connector."""
        logger.info("Stopping Fibonacci Dashboard Connector")
        self.running = False
        if self._thread is not None:
            self._thread.join(timeout=5.0)
            self._thread = None

def main():
    """Main entry point."""
    print(f"\n{CYAN}=== OMEGA BTC AI - FIBONACCI DASHBOARD CONNECTOR ==={RESET}")
    print(f"{GREEN}Connecting enhanced Fibonacci analysis to Reggae Dashboard...{RESET}")
    
    connector = FibonacciDashboardConnector()
    
    try:
        connector.start()
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Stopping Fibonacci Dashboard Connector...{RESET}")
        connector.stop()
    
if __name__ == "__main__":
    main() 