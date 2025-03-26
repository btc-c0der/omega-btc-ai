#!/usr/bin/env python3

"""
Update Harmonic Patterns in Redis

This script analyzes price movements across multiple timeframes to detect
harmonic patterns and stores them in Redis for real-time access.
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from omega_ai.analysis.fibonacci_patterns import FibonacciPatternDetector, PatternPoint
from omega_ai.utils.redis_connection import RedisConnectionManager

# Set up logging with more detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('harmonic_patterns.log')
    ]
)

class HarmonicPatternUpdater:
    """Updates harmonic patterns in Redis."""
    
    def __init__(self):
        """Initialize the updater with Redis connection and pattern detector."""
        self.redis_manager = RedisConnectionManager()
        self.pattern_detector = FibonacciPatternDetector()
        self.timeframes = ["1min", "5min", "15min", "60min"]
        logging.info("Initialized HarmonicPatternUpdater")
    
    def get_price_points(self, timeframe: str) -> List[PatternPoint]:
        """Get price points for a specific timeframe from Redis."""
        try:
            movements_key = f"btc_movements_{timeframe}"
            movements_data = self.redis_manager.lrange(movements_key, -1000, -1)  # Get last 1000 points
            
            if not movements_data:
                logging.warning(f"No price movements found for {timeframe}")
                return []
            
            price_points = []
            last_price = None
            last_timestamp = None
            min_time_diff = {
                "1min": timedelta(minutes=5),
                "5min": timedelta(minutes=25),
                "15min": timedelta(hours=1),
                "60min": timedelta(hours=4)
            }[timeframe]
            
            for movement in movements_data:
                try:
                    data = json.loads(movement)
                    if isinstance(data, dict) and 'price' in data and 'timestamp' in data:
                        current_price = float(data['price'])
                        current_timestamp = datetime.fromisoformat(data['timestamp'])
                        
                        # Only add point if price has changed AND enough time has passed
                        if (last_price is None or abs(current_price - last_price) > 0.01) and \
                           (last_timestamp is None or current_timestamp - last_timestamp >= min_time_diff):
                            price_points.append(PatternPoint(
                                price=current_price,
                                timestamp=current_timestamp
                            ))
                            last_price = current_price
                            last_timestamp = current_timestamp
                except (json.JSONDecodeError, ValueError) as e:
                    logging.error(f"Error parsing movement data: {e}")
                    continue
            
            # Get last 5 points with significant price movement
            significant_points = []
            min_price_change = 0.1  # Minimum 0.1% price change
            
            for i in range(len(price_points)-1, -1, -1):
                if len(significant_points) == 0:
                    significant_points.append(price_points[i])
                else:
                    price_change_pct = abs(price_points[i].price - significant_points[-1].price) / significant_points[-1].price * 100
                    if price_change_pct >= min_price_change:
                        significant_points.append(price_points[i])
                        if len(significant_points) >= 5:
                            break
            
            significant_points.reverse()  # Put points in chronological order
            
            logging.info(f"Retrieved {len(price_points)} price points for {timeframe}")
            logging.info(f"Found {len(significant_points)} points with significant price movement")
            
            if len(significant_points) >= 5:
                price_changes = []
                time_diffs = []
                for i in range(1, len(significant_points)):
                    change_pct = (significant_points[i].price - significant_points[i-1].price) / significant_points[i-1].price * 100
                    price_changes.append(f"{change_pct:+.2f}%")
                    time_diff = significant_points[i].timestamp - significant_points[i-1].timestamp
                    time_diffs.append(str(time_diff))
                logging.info(f"Price changes between points: {', '.join(price_changes)}")
                logging.info(f"Time between points: {', '.join(time_diffs)}")
                return significant_points
            else:
                logging.warning(f"Insufficient points with significant price movement: {len(significant_points)} < 5")
                return []
            
        except Exception as e:
            logging.error(f"Error getting price points for {timeframe}: {e}")
            return []
    
    def update_patterns(self, timeframe: str, points: List[PatternPoint]) -> None:
        """Update harmonic patterns for a specific timeframe."""
        try:
            if len(points) < 5:
                logging.warning(f"Insufficient price points for {timeframe}: {len(points)} < 5")
                return
                
            # Detect patterns
            patterns = self.pattern_detector.detect_patterns(points)
            
            if patterns:
                # Store patterns in Redis
                key = f"harmonic_patterns_{timeframe}"
                self.redis_manager.delete(key)
                for pattern in patterns:
                    self.redis_manager.rpush(key, json.dumps(pattern))
                logging.info(f"Found {len(patterns)} patterns in {timeframe} timeframe")
            else:
                logging.info(f"No patterns found in {timeframe} timeframe")
                
        except Exception as e:
            logging.error(f"Error updating harmonic patterns: {e}")
            
    def run(self):
        """Run the harmonic pattern update."""
        try:
            for timeframe in self.timeframes:
                logging.info(f"Analyzing {timeframe} timeframe for harmonic patterns")
                
                # Get price points
                points = self.get_price_points(timeframe)
                if points:
                    self.update_patterns(timeframe, points)
                    
            logging.info("Harmonic pattern update completed successfully")
            
        except Exception as e:
            logging.error(f"Error updating harmonic patterns: {e}")
            raise

def main():
    """Main function to run the harmonic pattern updater."""
    try:
        updater = HarmonicPatternUpdater()
        updater.run()
    except Exception as e:
        logging.error(f"Fatal error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 