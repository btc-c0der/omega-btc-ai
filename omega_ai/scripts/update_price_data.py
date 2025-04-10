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

"""Update BTC price data in Redis with proper timeframe aggregation."""

import json
import logging
import random
from datetime import datetime, timedelta
from typing import List, Dict
from omega_ai.utils.redis_connection import RedisConnectionManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PriceDataUpdater:
    """Update BTC price data in Redis."""
    
    def __init__(self):
        """Initialize the updater."""
        self.redis_manager = RedisConnectionManager()
        self.timeframes = ["1min", "5min", "15min", "60min"]
        
    def generate_test_data(self) -> List[Dict]:
        """Generate test price data with realistic movements."""
        data = []
        base_price = 51000.0
        current_price = base_price
        volatility = 0.005  # 0.5% volatility
        
        # Generate 24 hours of 1-minute data
        start_time = datetime.now() - timedelta(days=1)
        for i in range(24 * 60):  # 24 hours * 60 minutes
            # Random walk with mean reversion
            change = random.gauss(0, volatility)
            # Add mean reversion
            mean_reversion = (base_price - current_price) / base_price * 0.05
            current_price = max(1, min(100000, current_price * (1 + change + mean_reversion)))
            
            # Add some trend
            if i < 12 * 60:  # First 12 hours bullish
                current_price *= 1.0001
            else:  # Last 12 hours bearish
                current_price *= 0.9999
                
            # Add some spikes (less frequent, smaller magnitude)
            if random.random() < 0.005:  # 0.5% chance of spike
                current_price *= random.uniform(0.98, 1.02)
            
            data.append({
                'timestamp': (start_time + timedelta(minutes=i)).isoformat(),
                'price': round(current_price, 2)
            })
        
        return sorted(data, key=lambda x: x['timestamp'])  # Ensure chronological order
        
    def aggregate_timeframe(self, data: List[Dict], minutes: int) -> List[Dict]:
        """Aggregate 1-minute data into larger timeframes."""
        if not data:
            return []
            
        aggregated = []
        current_group = []
        current_time = datetime.fromisoformat(data[0]['timestamp'])
        next_time = current_time + timedelta(minutes=minutes)
        
        for point in data:
            point_time = datetime.fromisoformat(point['timestamp'])
            if point_time < next_time:
                current_group.append(point)
            else:
                if current_group:
                    # Calculate OHLC
                    prices = [p['price'] for p in current_group]
                    aggregated.append({
                        'timestamp': current_group[0]['timestamp'],
                        'price': sum(prices) / len(prices)  # Using average for now
                    })
                current_group = [point]
                current_time = point_time
                next_time = current_time + timedelta(minutes=minutes)
        
        # Handle last group
        if current_group:
            prices = [p['price'] for p in current_group]
            aggregated.append({
                'timestamp': current_group[0]['timestamp'],
                'price': sum(prices) / len(prices)
            })
        
        return aggregated
    
    def update_redis(self):
        """Update Redis with new price data."""
        try:
            # Generate 1-minute data
            one_min_data = self.generate_test_data()
            
            # Store data for each timeframe
            for timeframe in self.timeframes:
                minutes = int(''.join(filter(str.isdigit, timeframe)))
                data = one_min_data if minutes == 1 else self.aggregate_timeframe(one_min_data, minutes)
                
                # Clear existing data
                key = f"btc_movements_{timeframe}"
                self.redis_manager.delete(key)
                
                # Store new data
                for point in data:
                    self.redis_manager.rpush(key, json.dumps(point))
                
                logging.info(f"Updated {timeframe} data with {len(data)} points")
                
                # Log some stats
                if data:
                    prices = [p['price'] for p in data]
                    logging.info(f"{timeframe} price range: {min(prices):.2f} - {max(prices):.2f}")
                    
        except Exception as e:
            logging.error(f"Error updating price data: {e}")

def main():
    """Run the price data update."""
    updater = PriceDataUpdater()
    updater.update_redis()

if __name__ == "__main__":
    main() 