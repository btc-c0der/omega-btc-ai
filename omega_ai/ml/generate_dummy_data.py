
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

import redis
import random
import numpy as np
import json
import time
import os
import logging
from datetime import datetime, timezone, timedelta

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# ANSI Colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

class DummyDataGenerator:
    """Generate dummy market data for testing the market trends model."""
    
    def __init__(self, redis_host='localhost', redis_port=6379, days=30):
        """Initialize the data generator."""
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.days = days
        
        # Connect to Redis
        try:
            self.redis_conn = redis.StrictRedis(
                host=redis_host, 
                port=redis_port,
                db=0, 
                decode_responses=True
            )
            self.redis_conn.ping()
            logger.info(f"Connected to Redis at {redis_host}:{redis_port}")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    def generate_price_history(self, start_price=75000.0, volatility=0.02):
        """Generate price history with realistic BTC price movements."""
        logger.info(f"Generating {self.days} days of price history")
        
        # Parameters for quasi-random price generation
        points_per_day = 1440  # 1-minute intervals
        total_points = self.days * points_per_day
        
        # Generate time series with some realistic patterns
        prices = []
        volumes = []
        
        current_price = start_price
        current_trend = random.choice(["up", "down", "sideways"])
        trend_duration = random.randint(100, 1000)  # How long current trend lasts
        
        # Sine wave parameters for cyclical component
        cycle_amplitude = start_price * 0.05  # 5% amplitude
        cycle_period = points_per_day * 3  # 3-day cycle
        
        for i in range(total_points):
            # Change trend occasionally
            if i % trend_duration == 0:
                current_trend = random.choice(["up", "down", "sideways"])
                trend_duration = random.randint(100, 1000)
                logger.debug(f"New trend: {current_trend} for {trend_duration} points")
            
            # Trend component
            if current_trend == "up":
                trend_factor = 1.0002  # Slight uptrend
            elif current_trend == "down":
                trend_factor = 0.9998  # Slight downtrend
            else:
                trend_factor = 1.0  # Sideways
            
            # Random component (daily volatility converted to per-minute)
            random_factor = 1.0 + random.gauss(0, volatility / np.sqrt(points_per_day))
            
            # Cyclical component (sine wave)
            cycle_factor = 1.0 + (np.sin(2 * np.pi * i / cycle_period) * cycle_amplitude / start_price)
            
            # Calculate new price with all components
            current_price = current_price * trend_factor * random_factor * cycle_factor
            
            # Add occasional price shocks (1% chance)
            if random.random() < 0.01:
                shock_factor = random.uniform(0.95, 1.05)  # 5% shock up or down
                current_price *= shock_factor
                logger.debug(f"Price shock: {shock_factor}")
            
            # Generate volume (positively correlated with absolute price change)
            base_volume = 1000  # Base BTC volume
            price_change_pct = abs((current_price / start_price) - 1)
            volume = base_volume * (1 + price_change_pct * 10) * random.uniform(0.5, 1.5)
            
            prices.append(current_price)
            volumes.append(volume)
        
        # Store the generated data in Redis
        logger.info(f"Storing {len(prices)} price points in Redis")
        
        # Clear existing data
        self.redis_conn.delete("btc_movement_history")
        
        # Store new data (in reverse order - newest first)
        pipeline = self.redis_conn.pipeline()
        for price, volume in zip(reversed(prices), reversed(volumes)):
            pipeline.lpush("btc_movement_history", f"{price},{volume}")
        pipeline.execute()
        
        # Store current price
        self.redis_conn.set("last_btc_price", str(prices[-1]))
        self.redis_conn.set("last_btc_volume", str(volumes[-1]))
        
        logger.info(f"Price history generated and stored in Redis")
        logger.info(f"Current price: ${prices[-1]:.2f}")
        
        # Return the latest price for other generators
        return prices[-1]
    
    def generate_trend_data(self, current_price):
        """Generate trend data for different timeframes."""
        logger.info("Generating trend data for different timeframes")
        
        timeframes = [1, 5, 15, 30, 60, 240, 720, 1444]  # minutes
        
        for minutes in timeframes:
            # Get historical prices from our generated data
            history = self.redis_conn.lrange("btc_movement_history", 0, minutes)
            
            if not history:
                logger.warning(f"No history available for {minutes}min timeframe")
                continue
            
            # Parse prices
            try:
                past_price = float(history[-1].split(',')[0])
                
                # Calculate percentage change
                change_pct = ((current_price - past_price) / past_price) * 100
                
                # Determine trend
                if change_pct > 2.0:
                    trend = "Strongly Bullish"
                elif change_pct > 0.5:
                    trend = "Bullish"
                elif change_pct < -2.0:
                    trend = "Strongly Bearish"
                elif change_pct < -0.5:
                    trend = "Bearish"
                else:
                    trend = "Neutral"
                
                # Store in Redis
                trend_data = {
                    "trend": trend,
                    "change": change_pct,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                
                self.redis_conn.set(f"btc_trend_{minutes}min", json.dumps(trend_data))
                
                logger.info(f"Generated {minutes}min trend: {trend} ({change_pct:.2f}%)")
                
            except Exception as e:
                logger.error(f"Error generating trend for {minutes}min: {e}")
    
    def generate_fibonacci_levels(self, current_price):
        """Generate Fibonacci levels based on recent price history."""
        logger.info("Generating Fibonacci levels")
        
        # Get price history
        history = self.redis_conn.lrange("btc_movement_history", 0, 1000)
        if not history:
            logger.warning("No history available for Fibonacci calculations")
            return
        
        # Parse prices
        prices = [float(item.split(',')[0]) for item in history]
        
        # Find high and low
        high_price = max(prices)
        low_price = min(prices)
        price_range = high_price - low_price
        
        # Calculate Fibonacci levels
        fibonacci_levels = {
            "0.0": low_price,
            "0.236": low_price + 0.236 * price_range,
            "0.382": low_price + 0.382 * price_range,
            "0.5": low_price + 0.5 * price_range,
            "0.618": low_price + 0.618 * price_range,
            "0.786": low_price + 0.786 * price_range,
            "1.0": high_price,
            "1.618": high_price + 0.618 * price_range,
            "2.618": high_price + 1.618 * price_range
        }
        
        # Store in Redis
        self.redis_conn.set("fibonacci:current_levels", json.dumps(fibonacci_levels))
        
        logger.info(f"Generated Fibonacci levels (high: ${high_price:.2f}, low: ${low_price:.2f})")
        
        # Check if current price is near any Fibonacci level
        closest_level = None
        min_distance_pct = float('inf')
        
        for level, price in fibonacci_levels.items():
            distance_pct = abs((current_price - price) / price * 100)
            if distance_pct < min_distance_pct:
                min_distance_pct = distance_pct
                closest_level = level
        
        logger.info(f"Current price closest to Fibonacci level {closest_level} (${fibonacci_levels[closest_level]:.2f})")
    
    def generate_all_data(self):
        """Generate all necessary data for the market trends model."""
        print(f"\n{MAGENTA}{BOLD}🧠 GENERATING DUMMY MARKET DATA FOR AI MODEL 🧠{RESET}")
        print(f"{YELLOW}══════════════════════════════════════{RESET}")
        
        # Generate price history
        current_price = self.generate_price_history()
        
        # Generate trend data
        self.generate_trend_data(current_price)
        
        # Generate Fibonacci levels
        self.generate_fibonacci_levels(current_price)
        
        print(f"\n{GREEN}{BOLD}✅ DATA GENERATION COMPLETE{RESET}")
        print(f"{BLUE}Generated {self.days} days of market data{RESET}")
        print(f"{BLUE}Current price: ${current_price:.2f}{RESET}")
        print(f"{YELLOW}══════════════════════════════════════{RESET}")
        
        return current_price

def run_generator(days=30):
    """Run the data generator."""
    # Get Redis connection details from environment
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    
    generator = DummyDataGenerator(
        redis_host=redis_host,
        redis_port=redis_port,
        days=days
    )
    
    return generator.generate_all_data()

if __name__ == "__main__":
    run_generator(days=30) 