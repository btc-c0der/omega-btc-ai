
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
🌌 OMEGA RASTA GOLDEN RATIO DETECTOR 🌌
======================================

Enhanced Fibonacci detector with divine Golden Ratio confluence analysis.
May the golden ratio be with you! 🚀
"""

import numpy as np
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
import json
import redis
from omega_ai.mm_trap_detector.fibonacci_detector import FibonacciDetector
import math

# ANSI color codes for divine output
MAGENTA = "\033[35m"
GREEN = "\033[32m"
RESET = "\033[0m"

# Divine Fibonacci levels
GOLDEN_RATIOS = {
    "61.8%": 0.618,
    "78.6%": 0.786
}

@dataclass
class LiquidityGrab:
    """Data class for liquidity grab analysis."""
    price: float
    timestamp: datetime
    volume: float
    order_book_depth: float
    confidence: float
    fibonacci_level: float
    is_golden_ratio: bool

@dataclass
class GoldenRatioConfluence:
    """Data class for Golden Ratio confluence analysis."""
    price: float
    timestamp: datetime
    fibonacci_level: float
    liquidity_grab: Optional[LiquidityGrab]
    confidence: float
    order_book_imbalance: float
    is_confirmed: bool

class GoldenRatioDetector(FibonacciDetector):
    """Enhanced Fibonacci detector with Golden Ratio confluence analysis."""
    
    def __init__(self, symbol: str, test_mode: bool = False):
        """Initialize the Golden Ratio detector."""
        super().__init__(symbol, test_mode)
        self.golden_ratios = list(GOLDEN_RATIOS.values())  # Divine Fibonacci levels
        self.liquidity_grab_threshold = 0.5  # Lower threshold for liquidity grab detection
        self.order_book_history: List[Dict] = []
        self.confluence_history: List[GoldenRatioConfluence] = []
        
        # Initialize Redis connection
        self.redis_conn = redis.Redis(host='localhost', port=6379, db=0)
        
        # Initialize swing points for testing
        if test_mode:
            self.recent_swing_high = 42000.0
            self.recent_swing_low = 40000.0
            self.fib_levels = ["0.236", "0.382", "0.500", "0.618", "0.786"]
    
    def generate_fibonacci_levels(self) -> Union[Dict[str, float], None]:
        """Generate Fibonacci levels based on swing points."""
        if not self.recent_swing_high or not self.recent_swing_low:
            return None
        
        price_range = self.recent_swing_high - self.recent_swing_low
        # Require at least 0.1% price range
        min_price_range = self.recent_swing_low * 0.001
        if price_range < min_price_range:
            return None
        
        # Calculate levels as floats
        levels = {}
        for level_str in self.fib_levels:
            level_float = float(level_str)
            level_price = self.recent_swing_low + (price_range * level_float)
            levels[level_str] = level_price
        
        return levels
    
    def detect_liquidity_grab(self, price: float, timestamp: datetime) -> Optional[LiquidityGrab]:
        """Detect potential liquidity grabs at Fibonacci levels."""
        if price is None:
            return None

        # Get current order book state
        order_book = self.get_order_book_state()
        if not order_book or not order_book['bids'] or not order_book['asks']:
            return None
    
        # Calculate order book depth and imbalance
        depth = self.calculate_order_book_depth(order_book)
        if depth == 0:
            return None
    
        imbalance = self.calculate_order_book_imbalance(order_book)
    
        # Check if price is near a Fibonacci level, swing high, or swing low
        levels = self.generate_fibonacci_levels()
        if not levels:
            return None
    
        # Add swing points to levels for checking
        all_levels = {
            **levels,
            'swing_high': self.recent_swing_high,
            'swing_low': self.recent_swing_low
        }
    
        # Find nearest level
        nearest_level = None
        min_diff = float('inf')
        for level_str, level_price in all_levels.items():
            if level_price is None:
                continue
            diff = abs(price - level_price)
            if diff < min_diff:
                min_diff = diff
                nearest_level = level_str
    
        if not nearest_level:
            return None

        # Get the level price
        level_price = all_levels[nearest_level]

        # Check if price is too far from the level (more than 5% away)
        if min_diff / level_price > 0.05:
            return None
    
        # Calculate confidence based on multiple factors
        confidence = self.calculate_liquidity_grab_confidence(
            price=price,
            fibonacci_level=level_price,
            order_book_depth=depth,
            order_book_imbalance=imbalance
        )

        # If confidence is too low, return None
        if confidence < 0.5:
            return None
    
        # Return liquidity grab object
        return LiquidityGrab(
            price=price,
            timestamp=timestamp,
            volume=order_book.get('volume', 0.0),
            order_book_depth=depth,
            confidence=confidence,
            fibonacci_level=level_price,
            is_golden_ratio=self.is_golden_ratio(level_price)
        )
    
    def is_golden_ratio(self, level: float) -> bool:
        """Check if a level is a golden ratio."""
        if not self.recent_swing_high or not self.recent_swing_low:
            return False
        
        price_range = self.recent_swing_high - self.recent_swing_low
        if price_range == 0:
            return False
        
        relative_level = (level - self.recent_swing_low) / price_range
        # More lenient golden ratio check (2% deviation)
        return any(abs(relative_level - ratio) < 0.02 for ratio in self.golden_ratios)
    
    def detect_golden_ratio_confluence(self, price: float, timestamp: datetime) -> Optional[GoldenRatioConfluence]:
        """Detect Golden Ratio confluence with liquidity analysis."""
        if price is None:
            return None

        # Check for minimum price range
        if not self.recent_swing_high or not self.recent_swing_low:
            return None
    
        price_range = self.recent_swing_high - self.recent_swing_low
        min_price_range = self.recent_swing_low * 0.001  # 0.1% minimum range
        if price_range < min_price_range:
            return None

        # Get order book state
        order_book = self.get_order_book_state()
        if not order_book or not order_book['bids'] or not order_book['asks']:
            return None
    
        # Detect liquidity grab
        liquidity_grab = self.detect_liquidity_grab(price, timestamp)
        if not liquidity_grab:
            # Check if price is at swing high or swing low
            if self.recent_swing_high and abs(price - self.recent_swing_high) / self.recent_swing_high < 0.001:
                # Create confluence at swing high
                return GoldenRatioConfluence(
                    price=price,
                    timestamp=timestamp,
                    fibonacci_level=self.recent_swing_high,
                    liquidity_grab=None,
                    confidence=0.9,  # High confidence for swing points
                    order_book_imbalance=0.0,  # No imbalance data
                    is_confirmed=True
                )
            elif self.recent_swing_low and abs(price - self.recent_swing_low) / self.recent_swing_low < 0.001:
                # Create confluence at swing low
                return GoldenRatioConfluence(
                    price=price,
                    timestamp=timestamp,
                    fibonacci_level=self.recent_swing_low,
                    liquidity_grab=None,
                    confidence=0.9,  # High confidence for swing points
                    order_book_imbalance=0.0,  # No imbalance data
                    is_confirmed=True
                )
            return None
        
        # Calculate confluence confidence
        confluence_confidence = self.calculate_confluence_confidence(liquidity_grab)
        
        # Check order book imbalance
        order_book = self.get_order_book_state()
        if not order_book:
            return None
        
        imbalance = self.calculate_order_book_imbalance(order_book)
        
        # Create confluence object with more lenient confirmation threshold
        confluence = GoldenRatioConfluence(
            price=price,
            timestamp=timestamp,
            fibonacci_level=liquidity_grab.fibonacci_level,
            liquidity_grab=liquidity_grab,
            confidence=confluence_confidence,
            order_book_imbalance=imbalance,
            is_confirmed=confluence_confidence > 0.7  # More lenient confirmation threshold
        )
        
        # Store in history
        self.confluence_history.append(confluence)
        self.save_confluence_data(confluence)
        
        return confluence
    
    def calculate_liquidity_grab_confidence(self, price: float, fibonacci_level: float,
                                          order_book_depth: float, order_book_imbalance: float) -> float:
        """Calculate confidence in liquidity grab detection."""
        # Base confidence from Fibonacci level proximity
        price_diff = abs(price - fibonacci_level)
        if price_diff == 0:
            level_confidence = 1.0
        else:
            # More lenient level confidence calculation
            level_confidence = max(0, 1.0 - (price_diff / (fibonacci_level * 0.01)))  # Allow 1% deviation
        
        # Boost confidence for Golden Ratio levels
        if self.is_golden_ratio(fibonacci_level):
            level_confidence = min(1.0, level_confidence * 1.5)
        
        # Factor in order book depth (normalized to [0, 1])
        depth_confidence = min(1.0, order_book_depth / 100.0)  # More lenient depth threshold
        
        # Factor in order book imbalance (already normalized to [-1, 1])
        imbalance_confidence = (abs(order_book_imbalance) + 1) / 2  # Normalize to [0, 1]
        
        # Combine confidences with weights
        confidence = (
            0.5 * level_confidence +    # Equal weight for level proximity
            0.3 * depth_confidence +    # Increased weight for depth
            0.2 * imbalance_confidence  # Reduced weight for imbalance
        )
        
        return min(1.0, max(0.0, confidence))
    
    def calculate_confluence_confidence(self, liquidity_grab: LiquidityGrab) -> float:
        """Calculate confidence in Golden Ratio confluence."""
        # Start with liquidity grab confidence
        confidence = liquidity_grab.confidence
        
        # Boost for Golden Ratio levels
        if liquidity_grab.is_golden_ratio:
            confidence *= 1.5
        
        # Factor in historical confluence patterns
        historical_boost = self.calculate_historical_boost(liquidity_grab.fibonacci_level)
        confidence *= (1.0 + historical_boost)
        
        return min(1.0, confidence)
    
    def calculate_historical_boost(self, fibonacci_level: float) -> float:
        """Calculate confidence boost from historical patterns."""
        if not self.confluence_history:
            return 0.0
        
        # Count successful confluences at this level with more lenient matching
        successful_confluences = 0
        total_confluences = 0
        
        for confluence in self.confluence_history:
            # More lenient level matching (2% deviation)
            if abs(confluence.fibonacci_level - fibonacci_level) / fibonacci_level < 0.02:
                total_confluences += 1
                if confluence.is_confirmed:
                    successful_confluences += 1
        
        if total_confluences == 0:
            return 0.0
        
        success_rate = successful_confluences / total_confluences
        # Minimum boost of 0.1 if there are any confluences
        return max(0.1, min(0.5, success_rate))
    
    def get_order_book_state(self) -> Optional[Dict]:
        """Get current order book state."""
        try:
            # In test mode, return mock data
            if self.test_mode:
                return {
                    'bids': [(42000.0, 1.0), (41900.0, 2.0)],
                    'asks': [(42100.0, 1.0), (42200.0, 2.0)],
                    'volume': 100.0
                }
            
            # TODO: Implement actual order book fetching
            return None
        except Exception:
            return None
    
    def calculate_order_book_depth(self, order_book: Dict) -> float:
        """Calculate order book depth."""
        try:
            if not order_book or 'bids' not in order_book or 'asks' not in order_book:
                return 0.0
            
            # Filter out invalid values and negative volumes
            valid_bids = [(price, volume) for price, volume in order_book.get('bids', [])
                         if isinstance(price, (int, float)) and isinstance(volume, (int, float))
                         and not (math.isnan(price) or math.isinf(price))
                         and not (math.isnan(volume) or math.isinf(volume))
                         and volume > 0]
            
            valid_asks = [(price, volume) for price, volume in order_book.get('asks', [])
                         if isinstance(price, (int, float)) and isinstance(volume, (int, float))
                         and not (math.isnan(price) or math.isinf(price))
                         and not (math.isnan(volume) or math.isinf(volume))
                         and volume > 0]
            
            bid_depth = sum(bid[1] for bid in valid_bids)
            ask_depth = sum(ask[1] for ask in valid_asks)
            
            return bid_depth + ask_depth
        except Exception:
            return 0.0
    
    def calculate_order_book_imbalance(self, order_book: Dict) -> float:
        """Calculate order book imbalance."""
        try:
            if not order_book or 'bids' not in order_book or 'asks' not in order_book:
                return 0.0
            
            # Filter out invalid values and negative volumes
            valid_bids = [(price, volume) for price, volume in order_book.get('bids', [])
                         if isinstance(price, (int, float)) and isinstance(volume, (int, float))
                         and not (math.isnan(price) or math.isinf(price))
                         and not (math.isnan(volume) or math.isinf(volume))
                         and volume > 0]
            
            valid_asks = [(price, volume) for price, volume in order_book.get('asks', [])
                         if isinstance(price, (int, float)) and isinstance(volume, (int, float))
                         and not (math.isnan(price) or math.isinf(price))
                         and not (math.isnan(volume) or math.isinf(volume))
                         and volume > 0]
            
            bid_volume = sum(bid[1] for bid in valid_bids)
            ask_volume = sum(ask[1] for ask in valid_asks)
            
            total_volume = bid_volume + ask_volume
            if total_volume == 0:
                return 0.0
            
            # Calculate imbalance ratio (-1 to 1)
            return (bid_volume - ask_volume) / total_volume
        except Exception:
            return 0.0
    
    def save_confluence_data(self, confluence: GoldenRatioConfluence) -> None:
        """Save confluence data to Redis."""
        if self.test_mode:
            return
        
        try:
            data = {
                'price': confluence.price,
                'timestamp': confluence.timestamp.isoformat(),
                'fibonacci_level': confluence.fibonacci_level,
                'confidence': confluence.confidence,
                'order_book_imbalance': confluence.order_book_imbalance,
                'is_confirmed': confluence.is_confirmed
            }
            
            key = f"golden_ratio_confluence:{self.symbol}"
            self.redis_conn.lpush(key, json.dumps(data))
        except redis.RedisError:
            # Silently handle Redis errors
            pass
    
    def get_confluence_history(self) -> List[GoldenRatioConfluence]:
        """Get historical confluence data."""
        if self.test_mode:
            return self.confluence_history
        
        key = f"golden_ratio_confluence:{self.symbol}"
        data = self.redis_conn.lrange(key, 0, -1)
        
        history = []
        for entry in data:
            try:
                entry_data = json.loads(entry)
                confluence = GoldenRatioConfluence(
                    price=entry_data['price'],
                    timestamp=datetime.fromisoformat(entry_data['timestamp']),
                    fibonacci_level=entry_data['fibonacci_level'],
                    liquidity_grab=None,  # Not stored in Redis
                    confidence=entry_data['confidence'],
                    order_book_imbalance=entry_data['order_book_imbalance'],
                    is_confirmed=entry_data['is_confirmed']
                )
                history.append(confluence)
            except (json.JSONDecodeError, KeyError):
                continue
        
        return history 