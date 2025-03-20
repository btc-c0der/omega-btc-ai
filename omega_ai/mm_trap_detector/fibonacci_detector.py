"""
OMEGA RASTA FIBONACCI DETECTOR MODULE

Divine market analysis through Fibonacci sequence harmony
"""

import redis
import numpy as np
import datetime
import json
from collections import deque
import logging
from typing import Dict, Optional, List, Any, Tuple
from datetime import datetime, timezone

# Initialize Redis for divine data storage
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Terminal colors for enhanced visibility
BLUE = "\033[94m"           # Price up
YELLOW = "\033[93m"         # Price down
GREEN = "\033[92m"          # Strongly positive
RED = "\033[91m"            # Strongly negative
CYAN = "\033[96m"           # Info highlight
MAGENTA = "\033[95m"        # Special emphasis
RESET = "\033[0m"

class FibonacciDetector:
    """Enhanced detector for identifying price movements at Fibonacci levels."""
    
    def __init__(self):
        # Store recent price history for Fibonacci analysis
        self.price_history = deque(maxlen=1000)
        
        # Track important price points for Fibonacci calculations
        self.recent_swing_high = None
        self.recent_swing_low = None
        
        # Fibonacci levels to monitor (standard + extensions)
        self.fib_levels = {
            0.0: "0% (Base)",
            0.236: "23.6%",
            0.382: "38.2%",
            0.5: "50%",
            0.618: "61.8%",
            0.786: "78.6%",
            1.0: "100%",
            1.272: "127.2%",
            1.618: "161.8%"
        }
        
        # Track recent Fibonacci hits for confluence detection
        self.recent_fib_hits = deque(maxlen=20)
        
        # Track fib confluences with traps
        self.trap_fib_confluences = deque(maxlen=50)
        
        # Minimum price range for Fibonacci calculations
        self.min_price_range = 100
        
        # Minimum 0.5% difference for swing points
        self.min_swing_diff = 0.005
    
    def update_price_data(self, price: float, timestamp: datetime) -> None:
        """Update price data with validation."""
        if price is None or price <= 0:
            raise ValueError("Invalid price: must be a positive number")
            
        self.price_history.append((timestamp, price))
        self._update_swing_points()
    
    def _update_swing_points(self) -> None:
        """Update swing points based on price movement."""
        try:
            # Need at least 3 prices for swing detection
            if len(self.price_history) < 3:
                return
            
            # Get last 3 prices with timestamps
            price_points = list(self.price_history)[-3:]
            prices = [point[1] for point in price_points]  # Extract just the prices
            timestamps = [point[0] for point in price_points]  # Extract timestamps
            
            # Calculate price changes
            changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
            
            # Detect swing high
            if changes[0] > 0 and changes[1] < 0:
                # Price went up then down = swing high
                if self.recent_swing_high is None or prices[1] > self.recent_swing_high:
                    self.recent_swing_high = prices[1]
                    logger.info(f"New swing high detected: ${self.recent_swing_high:,.2f}")
                    # Store in Redis
                    try:
                        redis_conn.set("fibonacci:swing_high", self.recent_swing_high)
                        redis_conn.set("fibonacci:swing_high_timestamp", timestamps[1].isoformat())
                    except redis.RedisError as e:
                        logger.error(f"Redis error storing swing high: {str(e)}")
                
            # Detect swing low
            if changes[0] < 0 and changes[1] > 0:
                # Price went down then up = swing low
                if self.recent_swing_low is None or prices[1] < self.recent_swing_low:
                    self.recent_swing_low = prices[1]
                    logger.info(f"New swing low detected: ${self.recent_swing_low:,.2f}")
                    # Store in Redis
                    try:
                        redis_conn.set("fibonacci:swing_low", self.recent_swing_low)
                        redis_conn.set("fibonacci:swing_low_timestamp", timestamps[1].isoformat())
                    except redis.RedisError as e:
                        logger.error(f"Redis error storing swing low: {str(e)}")
            
            # Initialize swing points if not set
            if self.recent_swing_high is None:
                self.recent_swing_high = max(prices)
                logger.info(f"Initializing swing high: ${self.recent_swing_high:,.2f}")
            
            if self.recent_swing_low is None:
                self.recent_swing_low = min(prices)
                logger.info(f"Initializing swing low: ${self.recent_swing_low:,.2f}")
            
            # Log swing points
            if self.recent_swing_high is not None and self.recent_swing_low is not None:
                logger.info(f"Updated Fibonacci swing points: High=${self.recent_swing_high:,.2f}, Low=${self.recent_swing_low:,.2f}")
            
        except Exception as e:
            logger.error(f"Error updating swing points: {str(e)}")
            # Don't reset swing points on error to maintain state
            pass
    
    def check_fibonacci_level(self, current_price: float) -> Optional[Dict]:
        """Check if current price hits any Fibonacci level."""
        try:
            if not self.recent_swing_high or not self.recent_swing_low:
                return None
            
            # Calculate price range
            price_range = abs(self.recent_swing_high - self.recent_swing_low)
            min_range = min(self.recent_swing_high, self.recent_swing_low) * 0.001  # 0.1% minimum range
            
            if price_range < min_range:
                logger.debug(f"Price range {price_range:.2f} too small for Fibonacci analysis")
                return None
            
            # Calculate Fibonacci levels
            levels = self.generate_fibonacci_levels()
            if not levels:
                return None
            
            # Find closest level
            closest_hit = None
            min_distance_pct = float('inf')
            
            for level_str, level_price in levels.items():
                distance = abs(current_price - level_price)
                distance_pct = distance / level_price
                
                # Consider it a hit if within 0.5% of level
                if distance_pct <= 0.005:
                    if distance_pct < min_distance_pct:
                        min_distance_pct = distance_pct
                        # Convert level string to float (e.g. "61.8%" -> 0.618)
                        level_float = float(level_str.strip('%')) / 100
                        # Special label for Golden Ratio
                        label = "Golden Ratio" if level_str == "61.8%" else f"Fibonacci {level_str}"
                        closest_hit = {
                            "level": level_float,
                            "price": level_price,
                            "label": label,
                            "proximity": distance_pct,  # Raw distance percentage
                            "is_uptrend": current_price > self.recent_swing_low
                        }
                        
            if closest_hit:
                self._record_fibonacci_hit(current_price, closest_hit)
                
            return closest_hit
            
        except Exception as e:
            logger.error(f"Error checking Fibonacci level: {str(e)}")
            return None
    
    def _record_fibonacci_hit(self, current_price: float, hit_data: Dict) -> None:
        """Record a Fibonacci level hit in Redis."""
        try:
            redis_conn.zadd(
                "fibonacci:hits",
                {json.dumps({
                    "price": current_price,
                    "level": hit_data["level"],
                    "label": hit_data.get("label", ""),
                    "proximity": hit_data.get("proximity", 0),
                    "is_uptrend": hit_data.get("is_uptrend", True),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }): current_price}
            )
            logger.info(f"Recorded Fibonacci hit at level {hit_data['level']}")
        except redis.RedisError as e:
            logger.error(f"Redis error recording Fibonacci hit: {str(e)}")
        except Exception as e:
            logger.error(f"Error recording Fibonacci hit: {str(e)}")
    
    def detect_fibonacci_confluence(self, trap_type, confidence, price_change, current_price):
        """
        Check if a detected trap coincides with a Fibonacci level.
        Returns enhanced confidence if confluence is detected.
        """
        try:
            # Check if current price hits a Fibonacci level
            fib_hit = self.check_fibonacci_level(current_price)
            
            if not fib_hit:
                return confidence, None
            
            # Determine if this is a key Fibonacci level (the most significant ones)
            is_key_level = fib_hit["level"] in [0.382, 0.5, 0.618, 0.786]
            
            # Calculate confluence confidence boost
            # Strong levels and high-confidence traps create stronger confluence
            if is_key_level:
                # Major confluence at key levels
                confidence_boost = 0.2  # Increased for testing
                confluence_type = "MAJOR"
            else:
                # Minor confluence at standard levels
                confidence_boost = 0.1  # Increased for testing
                confluence_type = "MINOR"
            
            # Extra boost for 0.618 (Golden Ratio) level
            if fib_hit["level"] == 0.618:
                confidence_boost += 0.1  # Increased for testing
                confluence_type = "GOLDEN RATIO"
            
            # Cap the total confidence at 0.98 to avoid overconfidence
            enhanced_confidence = min(0.98, confidence + confidence_boost)
            
            # Record the confluence event
            self._record_trap_fibonacci_confluence(trap_type, enhanced_confidence, 
                                                  price_change, current_price,
                                                  fib_hit, confluence_type)
            
            return enhanced_confidence, fib_hit
            
        except Exception as e:
            logger.error(f"Error in detect_fibonacci_confluence: {str(e)}")
            return confidence, None
    
    def _record_trap_fibonacci_confluence(self, trap_type, confidence, price_change, 
                                         price, fib_hit, confluence_type):
        """Record when a trap aligns with a Fibonacci level."""
        try:
            timestamp = datetime.now(timezone.utc)
            
            # Create rich confluence data
            confluence_data = {
                "timestamp": timestamp.isoformat(),  # Convert to string for JSON
                "trap_type": trap_type,
                "confidence": confidence,
                "price": price,
                "price_change": price_change,
                "fibonacci_level": fib_hit["label"],
                "fib_price": fib_hit["price"],
                "is_uptrend": fib_hit["is_uptrend"],
                "confluence_type": confluence_type
            }
            
            # Store in local queue
            self.trap_fib_confluences.append(confluence_data)
            
            # Store in Redis for visualization and alerting
            try:
                redis_conn.zadd(
                    "grafana:fibonacci_trap_confluences",
                    {json.dumps(confluence_data): datetime.now(timezone.utc).timestamp()}
                )
                
                # Set a short-lived alert key for real-time systems
                alert_key = f"alert:fibonacci_confluence:{int(timestamp.timestamp())}"
                redis_conn.setex(alert_key, 300, json.dumps(confluence_data))  # 5-minute TTL
            except redis.RedisError as e:
                logger.error(f"Redis error recording trap confluence: {str(e)}")
            
            # Log to console with enhanced formatting
            print(f"\n🔥 {confluence_type} FIBONACCI CONFLUENCE DETECTED 🔥")
            print(f"⚠️ {trap_type} at ${price:.2f} aligned with {fib_hit['label']} Fibonacci level")
            print(f"📈 Enhanced confidence: {confidence:.2f} (Fibonacci confluence boost applied)")
            
        except Exception as e:
            logger.error(f"Error recording trap confluence: {str(e)}")
    
    def generate_fibonacci_levels(self) -> Optional[Dict]:
        """Generate all current Fibonacci levels for visualization."""
        try:
            if self.recent_swing_high is None or self.recent_swing_low is None:
                return None
                
            is_uptrend = self.recent_swing_high > self.recent_swing_low
            fib_range = abs(self.recent_swing_high - self.recent_swing_low)
            
            # Don't generate levels for very small ranges
            if fib_range < self.min_price_range:
                return None
            
            # Generate all levels
            levels = {}
            for level, label in self.fib_levels.items():
                if is_uptrend:
                    price = self.recent_swing_low + (fib_range * level)
                else:
                    price = self.recent_swing_high - (fib_range * level)
                    
                levels[label] = price
            
            try:
                # Store in Redis for reference
                redis_conn.set("fibonacci:current_levels", json.dumps(levels))
            except redis.RedisError as e:
                logger.error(f"Redis connection error: {str(e)}")
                # Continue without Redis storage
            
            return levels
            
        except Exception as e:
            logger.error(f"Error generating Fibonacci levels: {str(e)}")
            return None

    def detect_fractal_harmony(self, timeframe: str = "1h") -> List[Dict]:
        """Detect fractal harmony patterns in price movement."""
        try:
            if not self.recent_swing_high or not self.recent_swing_low:
                return []
            
            harmonics = []
            price_range = self.recent_swing_high - self.recent_swing_low
            
            # Define Fibonacci ratios for fractal analysis
            ratios = [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618]
            
            for ratio in ratios:
                projected_level = self.recent_swing_low + (price_range * ratio)
                
                # Check recent price history for hits near this level
                for timestamp, price in self.price_history:
                    distance_pct = abs(price - projected_level) / projected_level
                    
                    if distance_pct <= 0.005:  # Within 0.5%
                        harmonic = {
                            "ratio": ratio,
                            "level": projected_level,
                            "price": price,
                            "timeframe": timeframe,
                            "confidence": 1.0 - (distance_pct / 0.005),
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }
                        harmonics.append(harmonic)
                        
            return harmonics
            
        except Exception as e:
            logger.error(f"Error detecting fractal harmony: {str(e)}")
            return []

# Create singleton instance
fibonacci_detector = FibonacciDetector()

# Exposed functions for other modules
def check_fibonacci_level(price, explicit_levels=None, tolerance=0.004):
    """
    Check if price is at a Fibonacci level with divine precision.
    
    Args:
        price: Current price to check
        explicit_levels: Optional dict of {level_name: price_value} to check against 
        tolerance: How close price must be to level (as percentage)
        
    Returns:
        Dict with hit level info or None
    """
    try:
        # If explicit levels provided, use those for divine guidance
        if explicit_levels is not None:
            closest_level = None
            min_distance_pct = float('inf')
            
            for level_name, level_price in explicit_levels.items():
                distance = abs(price - level_price)
                distance_pct = distance / level_price
                
                if distance_pct <= tolerance and distance_pct < min_distance_pct:
                    closest_level = {
                        "level": level_name,
                        "price": level_price,
                        "proximity": distance_pct,
                        "is_explicit": True
                    }
                    min_distance_pct = distance_pct
            
            return closest_level
        
        # Otherwise use internal fibonacci detection logic
        return fibonacci_detector.check_fibonacci_level(price)
        
    except Exception as e:
        logger.error(f"Error in check_fibonacci_level: {str(e)}")
        return None

def update_fibonacci_data(current_price: float) -> None:
    """Update Fibonacci data with the current price."""
    try:
        # Create detector instance
        detector = FibonacciDetector()
        
        # Update price data
        detector.update_price_data(current_price, datetime.now(timezone.utc))
        
        # Check for Fibonacci level hits
        fib_hit = detector.check_fibonacci_level(current_price)
        if fib_hit:
            # Record the hit
            detector._record_fibonacci_hit(current_price, fib_hit)
            
            # Store hit data in Redis
            try:
                redis_conn.zadd(
                    "fibonacci:hits",
                    {json.dumps({
                        "price": current_price,
                        "level": fib_hit["level"],
                        "label": fib_hit["label"],
                        "proximity": fib_hit["proximity"],
                        "is_uptrend": fib_hit["is_uptrend"],
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }): current_price}
                )
            except redis.RedisError as e:
                logger.error(f"Redis error updating Fibonacci data: {str(e)}")
            
    except ValueError as e:
        logger.error(f"Error updating Fibonacci data: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error updating Fibonacci data: {str(e)}")

def detect_fibonacci_confluence(trap_type, confidence, price_change, price):
    """Check if trap aligns with Fibonacci level and get enhanced confidence."""
    try:
        return fibonacci_detector.detect_fibonacci_confluence(trap_type, confidence, price_change, price)
    except Exception as e:
        logger.error(f"Error in detect_fibonacci_confluence: {str(e)}")
        return confidence, None

def get_current_fibonacci_levels():
    """Get all current Fibonacci levels."""
    try:
        return fibonacci_detector.generate_fibonacci_levels()
    except Exception as e:
        logger.error(f"Error getting Fibonacci levels: {str(e)}")
        return None

def check_fibonacci_alignment() -> Optional[Dict]:
    """Check if current price aligns with any Fibonacci level."""
    try:
        # Get current price from Redis
        current_price = float(redis_conn.get("last_btc_price") or 0)
        if current_price == 0:
            logger.warning("No price data available for Fibonacci alignment check")
            return None
            
        # Get current Fibonacci levels
        levels = get_current_fibonacci_levels()
        if not levels:
            logger.warning("No Fibonacci levels available for alignment check")
            return None
            
        # Find closest Fibonacci level
        closest_level = None
        min_distance_pct = float('inf')
        
        for level_name, level_price in levels.items():
            distance = abs(current_price - level_price)
            distance_pct = distance / level_price
            
            if distance_pct < min_distance_pct:
                min_distance_pct = distance_pct
                closest_level = {
                    "level": level_name,
                    "price": level_price,
                    "distance_pct": distance_pct
                }
        
        if not closest_level:
            return None
            
        # Calculate confidence based on distance
        confidence = 1.0 - min(min_distance_pct, 0.05) / 0.05  # Max 5% distance
        
        # Special handling for Golden Ratio
        if "61.8%" in closest_level["level"]:
            confidence = min(confidence * 1.2, 1.0)  # 20% boost for Golden Ratio
            
        # Log alignment details
        logger.info(f"Fibonacci Alignment: {closest_level['level']} at {closest_level['price']:.2f} - {min_distance_pct:.2%} away")
        
        return {
            "type": "GOLDEN_RATIO" if "61.8%" in closest_level["level"] else "STANDARD",
            "level": closest_level["level"],
            "price": closest_level["price"],
            "distance_pct": closest_level["distance_pct"],
            "confidence": confidence,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except ValueError as e:
        logger.error(f"Error checking Fibonacci alignment: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error checking Fibonacci alignment: {str(e)}")
        return None