import redis
import numpy as np
import datetime
import json
from collections import deque

# Redis connection
redis_conn = redis.Redis(host="localhost", port=6379, db=0)

class FibonacciDetector:
    """Enhanced detector for identifying price movements at Fibonacci levels."""
    
    def __init__(self):
        # Store recent price history for Fibonacci analysis
        self.price_history = deque(maxlen=500)
        
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
    
    def update_price_data(self, price, timestamp=None):
        """Add new price data and update swing points."""
        if timestamp is None:
            timestamp = datetime.datetime.now(datetime.UTC)
        
        self.price_history.append((timestamp, price))
        
        # Only update swing points when we have enough data
        if len(self.price_history) < 10:
            return
            
        # Find recent swing high/low for Fibonacci reference points
        self._update_swing_points()
    
    def _update_swing_points(self):
        """Identify swing high and low points for Fibonacci calculations."""
        prices = [p[1] for p in self.price_history]
        
        # Use a rolling window to detect swings
        window_size = min(30, len(prices))
        
        if len(prices) >= window_size:
            # Look for swing high (peak in the window)
            window_prices = prices[-window_size:]
            max_idx = np.argmax(window_prices)
            min_idx = np.argmin(window_prices)
            
            # Current swing high and low for this window
            current_swing_high = window_prices[max_idx]
            current_swing_low = window_prices[min_idx]
            
            # Only update if we found a new significant swing
            if self.recent_swing_high is None or current_swing_high > self.recent_swing_high:
                self.recent_swing_high = current_swing_high
                # Store in Redis for visualization
                redis_conn.set("fibonacci:swing_high", current_swing_high)
                redis_conn.set("fibonacci:swing_high_timestamp", 
                              self.price_history[-window_size + max_idx][0].isoformat())
            
            if self.recent_swing_low is None or current_swing_low < self.recent_swing_low:
                self.recent_swing_low = current_swing_low
                # Store in Redis for visualization
                redis_conn.set("fibonacci:swing_low", current_swing_low)
                redis_conn.set("fibonacci:swing_low_timestamp", 
                              self.price_history[-window_size + min_idx][0].isoformat())
    
    def check_fibonacci_level(self, current_price):
        """
        Check if current price is near a significant Fibonacci retracement level.
        Returns: Dictionary with level info, None if no level is hit
        """
        if self.recent_swing_high is None or self.recent_swing_low is None:
            return None
            
        # Determine if we're in an uptrend or downtrend for proper Fibonacci calculation
        is_uptrend = self.recent_swing_high > self.recent_swing_low
        fib_range = abs(self.recent_swing_high - self.recent_swing_low)
        
        # Don't calculate for very small ranges (avoid noise)
        if fib_range < 100:
            return None
        
        # Calculate tolerance based on price level (dynamic adjustment)
        # More precise at higher price levels
        base_tolerance = fib_range * 0.004  # 0.4% of the range
        
        # Check each Fibonacci level
        hit_levels = []
        
        # Calculate from both directions for more complete detection
        for level, label in self.fib_levels.items():
            # Calculate both uptrend and downtrend Fibonacci prices
            # This provides more comprehensive detection regardless of current trend
            if is_uptrend:
                fib_price = self.recent_swing_low + (fib_range * level)
            else:
                fib_price = self.recent_swing_high - (fib_range * level)
            
            # Check if current price is within tolerance of this level
            price_diff = abs(current_price - fib_price)
            
            # Calculate percentage proximity to level
            proximity_pct = (price_diff / fib_range) * 100
            
            if proximity_pct <= 0.4:  # Within 0.4% of the Fibonacci level
                hit_levels.append({
                    "level": level,
                    "label": label,
                    "price": fib_price,
                    "proximity": proximity_pct,
                    "is_uptrend": is_uptrend
                })
        
        # Return the closest level or None if no level is hit
        if hit_levels:
            # Sort by proximity (closest first)
            hit_levels.sort(key=lambda x: x["proximity"])
            hit_level = hit_levels[0]
            
            # Record this hit for confluence detection
            self._record_fibonacci_hit(current_price, hit_level)
            
            return hit_level
        else:
            return None
    
    def _record_fibonacci_hit(self, current_price, hit_level):
        """Record when price hits a Fibonacci level."""
        timestamp = datetime.datetime.now(datetime.UTC)
        
        # Create record of the hit
        hit_data = {
            "price": current_price,
            "level": hit_level["level"],
            "label": hit_level["label"],
            "timestamp": timestamp.isoformat(),  # Convert to ISO format string instead of datetime object
            "is_uptrend": hit_level["is_uptrend"]
        }
        
        # Store in Redis as a time-series event
        redis_conn.zadd(
            "fibonacci:hits", 
            {json.dumps(hit_data): timestamp.timestamp()}
        )
        
        # Also store the most recent hit
        redis_conn.set("fibonacci:last_hit", json.dumps(hit_data))
    
    def detect_fibonacci_confluence(self, trap_type, confidence, price_change, current_price):
        """
        Check if a detected trap coincides with a Fibonacci level.
        Returns enhanced confidence if confluence is detected.
        """
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
            confidence_boost = 0.12
            confluence_type = "MAJOR"
        else:
            # Minor confluence at standard levels
            confidence_boost = 0.06
            confluence_type = "MINOR"
        
        # Extra boost for 0.618 (Golden Ratio) level
        if fib_hit["level"] == 0.618:
            confidence_boost += 0.05
            confluence_type = "GOLDEN RATIO"
        
        # Cap the total confidence at 0.98 to avoid overconfidence
        enhanced_confidence = min(0.98, confidence + confidence_boost)
        
        # Record the confluence event
        self._record_trap_fibonacci_confluence(trap_type, enhanced_confidence, 
                                              price_change, current_price,
                                              fib_hit, confluence_type)
        
        return enhanced_confidence, fib_hit
    
    def _record_trap_fibonacci_confluence(self, trap_type, confidence, price_change, 
                                         price, fib_hit, confluence_type):
        """Record when a trap aligns with a Fibonacci level."""
        timestamp = datetime.datetime.now(datetime.UTC)
        
        # Create rich confluence data
        confluence_data = {
            "timestamp": timestamp,
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
        redis_conn.zadd(
            "grafana:fibonacci_trap_confluences",
            {json.dumps(confluence_data): timestamp.timestamp()}
        )
        
        # Set a short-lived alert key for real-time systems
        alert_key = f"alert:fibonacci_confluence:{int(timestamp.timestamp())}"
        redis_conn.setex(alert_key, 300, json.dumps(confluence_data))  # 5-minute TTL
        
        # Log to console with enhanced formatting
        print(f"\n🔥 {confluence_type} FIBONACCI CONFLUENCE DETECTED 🔥")
        print(f"⚠️ {trap_type} at ${price:.2f} aligned with {fib_hit['label']} Fibonacci level")
        print(f"📈 Enhanced confidence: {confidence:.2f} (Fibonacci confluence boost applied)")
    
    def generate_fibonacci_levels(self):
        """Generate all current Fibonacci levels for visualization."""
        if self.recent_swing_high is None or self.recent_swing_low is None:
            return None
            
        is_uptrend = self.recent_swing_high > self.recent_swing_low
        fib_range = abs(self.recent_swing_high - self.recent_swing_low)
        
        # Generate all levels
        levels = {}
        for level, label in self.fib_levels.items():
            if is_uptrend:
                price = self.recent_swing_low + (fib_range * level)
            else:
                price = self.recent_swing_high - (fib_range * level)
                
            levels[label] = price
        
        # Store in Redis for reference
        redis_conn.set("fibonacci:current_levels", json.dumps(levels))
        
        return levels

# Create singleton instance
fibonacci_detector = FibonacciDetector()

# Exposed functions for other modules
def check_fibonacci_level(price):
    """Check if price is at a Fibonacci level."""
    return fibonacci_detector.check_fibonacci_level(price)

def update_fibonacci_data(price):
    """Update Fibonacci detector with new price data."""
    fibonacci_detector.update_price_data(price)
    
def detect_fibonacci_confluence(trap_type, confidence, price_change, price):
    """Check if trap aligns with Fibonacci level and get enhanced confidence."""
    return fibonacci_detector.detect_fibonacci_confluence(trap_type, confidence, price_change, price)

def get_current_fibonacci_levels():
    """Get all current Fibonacci levels."""
    return fibonacci_detector.generate_fibonacci_levels()