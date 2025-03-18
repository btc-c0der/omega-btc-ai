"""
Sophisticated Fibonacci Pattern Detection Module

This module implements advanced Fibonacci-based harmonic patterns including:
- Gartley Pattern
- Butterfly Pattern
- Bat Pattern
- Crab Pattern
- Cypher Pattern
"""

from typing import Dict, List, Tuple, Optional, Any
import numpy as np
from dataclasses import dataclass
from datetime import datetime
import logging

@dataclass
class PatternPoint:
    """Represents a point in a harmonic pattern."""
    price: float
    timestamp: datetime
    label: str = ""  # Optional label for the point (X, A, B, C, D)

@dataclass
class HarmonicPattern:
    """Represents a detected harmonic pattern."""
    pattern_type: str
    points: List[PatternPoint]
    confidence: float
    timeframes: List[str]
    detected_at: datetime

class FibonacciPatternDetector:
    """Detects sophisticated Fibonacci-based harmonic patterns."""
    
    # Standard Fibonacci ratios used in harmonic patterns
    FIB_RATIOS = {
        '0.382': 0.382,
        '0.5': 0.5,
        '0.618': 0.618,
        '0.786': 0.786,
        '0.886': 0.886,
        '1.272': 1.272,
        '1.618': 1.618,
        '2.618': 2.618,
        '3.618': 3.618,
        '4.236': 4.236
    }
    
    # Pattern definitions with their Fibonacci ratios
    PATTERN_DEFINITIONS = {
        'Bullish Gartley': {
            'XA': -1.0,    # Initial bearish move
            'AB': 0.618,   # 61.8% bullish retracement of XA
            'BC': -0.382,  # 38.2% bearish retracement of AB
            'CD': 1.272    # 127.2% bullish extension of BC
        },
        'Bearish Gartley': {
            'XA': 1.0,     # Initial bullish move
            'AB': -0.618,  # 61.8% bearish retracement of XA
            'BC': 0.382,   # 38.2% bullish retracement of AB
            'CD': -1.272   # 127.2% bearish extension of BC
        },
        'Bullish Butterfly': {
            'XA': -1.0,    # Initial bearish move
            'AB': 0.786,   # 78.6% bullish retracement of XA
            'BC': -0.382,  # 38.2% bearish retracement of AB
            'CD': 1.618    # 161.8% bullish extension of BC
        },
        'Bearish Butterfly': {
            'XA': 1.0,     # Initial bullish move
            'AB': -0.786,  # 78.6% bearish retracement of XA
            'BC': 0.382,   # 38.2% bullish retracement of AB
            'CD': -1.618   # 161.8% bearish extension of BC
        },
        'Bullish Bat': {
            'XA': -1.0,    # Initial bearish move
            'AB': 0.382,   # 38.2% bullish retracement of XA
            'BC': -0.382,  # 38.2% bearish retracement of AB
            'CD': 2.618    # 261.8% bullish extension of BC
        },
        'Bearish Bat': {
            'XA': 1.0,     # Initial bullish move
            'AB': -0.382,  # 38.2% bearish retracement of XA
            'BC': 0.382,   # 38.2% bullish retracement of AB
            'CD': -2.618   # 261.8% bearish extension of BC
        },
        'Crab': {
            'XA': 1.0,    # Initial move
            'AB': 0.382,  # 38.2% retracement of XA
            'BC': 0.886,  # 88.6% retracement of AB
            'CD': 3.618   # 361.8% extension of BC
        },
        'Deep Crab': {
            'XA': 1.0,    # Initial move
            'AB': 0.886,  # 88.6% retracement of XA
            'BC': 0.382,  # 38.2% retracement of AB
            'CD': 2.618   # 261.8% extension of BC
        },
        'Cypher': {
            'XA': 1.0,    # Initial move
            'AB': 0.382,  # 38.2% retracement of XA
            'BC': 1.272,  # 127.2% extension of AB
            'CD': 0.786   # 78.6% retracement of BC
        },
        'Shark': {
            'XA': 1.0,    # Initial move
            'AB': 0.886,  # 88.6% retracement of XA
            'BC': 1.13,   # 113.0% extension of AB
            'CD': 1.618   # 161.8% extension of BC
        },
        '5-0': {
            'XA': 1.0,    # Initial move
            'AB': 0.5,    # 50% retracement of XA
            'BC': 1.272,  # 127.2% extension of AB
            'CD': 0.5     # 50% retracement of BC
        },
        'Three Drives': {
            'XA': 1.0,    # Initial move (Drive 1)
            'AB': 0.618,  # 61.8% retracement
            'BC': 1.272,  # 127.2% extension (Drive 2)
            'CD': 0.786   # 78.6% retracement
        },
        'Anti-Gartley': {
            'XA': 1.0,    # Initial move
            'AB': 0.618,  # 61.8% retracement of XA
            'BC': 0.886,  # 88.6% retracement of AB
            'CD': 1.272   # 127.2% extension of BC
        },
        'Anti-Butterfly': {
            'XA': 1.0,    # Initial move
            'AB': 0.786,  # 78.6% retracement of XA
            'BC': 0.886,  # 88.6% retracement of AB
            'CD': 1.618   # 161.8% extension of BC
        }
    }
    
    def __init__(self, tolerance: float = 0.15):
        """Initialize the pattern detector."""
        self.tolerance = tolerance
        
        # Define harmonic patterns and their ratios
        self.PATTERN_DEFINITIONS = {
            'Bullish Gartley': {
                'XA': -1.0,    # Initial bearish move
                'AB': 0.618,   # 61.8% bullish retracement of XA
                'BC': -0.382,  # 38.2% bearish retracement of AB
                'CD': 1.272    # 127.2% bullish extension of BC
            },
            'Bearish Gartley': {
                'XA': 1.0,     # Initial bullish move
                'AB': -0.618,  # 61.8% bearish retracement of XA
                'BC': 0.382,   # 38.2% bullish retracement of AB
                'CD': -1.272   # 127.2% bearish extension of BC
            },
            'Bullish Butterfly': {
                'XA': -1.0,    # Initial bearish move
                'AB': 0.786,   # 78.6% bullish retracement of XA
                'BC': -0.382,  # 38.2% bearish retracement of AB
                'CD': 1.618    # 161.8% bullish extension of BC
            },
            'Bearish Butterfly': {
                'XA': 1.0,     # Initial bullish move
                'AB': -0.786,  # 78.6% bearish retracement of XA
                'BC': 0.382,   # 38.2% bullish retracement of AB
                'CD': -1.618   # 161.8% bearish extension of BC
            },
            'Bullish Bat': {
                'XA': -1.0,    # Initial bearish move
                'AB': 0.382,   # 38.2% bullish retracement of XA
                'BC': -0.382,  # 38.2% bearish retracement of AB
                'CD': 2.618    # 261.8% bullish extension of BC
            },
            'Bearish Bat': {
                'XA': 1.0,     # Initial bullish move
                'AB': -0.382,  # 38.2% bearish retracement of XA
                'BC': 0.382,   # 38.2% bullish retracement of AB
                'CD': -2.618   # 261.8% bearish extension of BC
            }
        }
        logging.info(f"Initialized FibonacciPatternDetector with tolerance: {tolerance}")
        logging.info(f"Pattern types available: {', '.join(self.PATTERN_DEFINITIONS.keys())}")
    
    def calculate_ratio(self, price1: float, price2: float) -> float:
        """Calculate the ratio between two price points, preserving direction."""
        try:
            if abs(price1 - price2) < 0.00001:
                logging.debug(f"Equal prices detected: {price1} = {price2}")
                return 1.0
                
            # Calculate the ratio with direction
            ratio = (price2 - price1) / abs(price1)
            logging.debug(f"Price move from {price1} to {price2}: {ratio:.4f}")
            return ratio
            
        except Exception as e:
            logging.error(f"Error calculating ratio: {e}")
            return 1.0  # Default to neutral ratio on error
            
    def detect_patterns(self, points: List[PatternPoint]) -> List[Dict[str, Any]]:
        """Detect harmonic patterns in the given price points."""
        if len(points) < 5:
            logging.warning("Not enough price points to detect patterns")
            return []
            
        logging.info(f"Analyzing {len(points)} price points for patterns")
        logging.debug(f"Price points: {[(p.price, p.timestamp) for p in points[-5:]]}")
        
        patterns = []
        
        # Get the last 5 points for pattern detection
        points = points[-5:]
        
        # Calculate the overall trend direction
        trend_direction = 1 if points[-1].price > points[0].price else -1
        logging.debug(f"Overall trend direction: {'Bullish' if trend_direction > 0 else 'Bearish'}")
        
        # Calculate leg lengths
        xa_length = abs(points[1].price - points[0].price)
        ab_length = abs(points[2].price - points[1].price)
        bc_length = abs(points[3].price - points[2].price)
        cd_length = abs(points[4].price - points[3].price)
        
        # Calculate ratios relative to previous legs
        ratios = {
            'XA': 1.0,  # First leg is reference
            'AB': ab_length / xa_length if xa_length > 0 else 1.0,  # AB relative to XA
            'BC': bc_length / ab_length if ab_length > 0 else 1.0,  # BC relative to AB
            'CD': cd_length / bc_length if bc_length > 0 else 1.0,  # CD relative to BC
        }
        
        # Apply direction to ratios
        for leg in ratios:
            if leg == 'XA':
                ratios[leg] *= trend_direction
            elif leg == 'AB':
                ratios[leg] *= trend_direction if points[2].price > points[1].price else -trend_direction
            elif leg == 'BC':
                ratios[leg] *= trend_direction if points[3].price > points[2].price else -trend_direction
            elif leg == 'CD':
                ratios[leg] *= trend_direction if points[4].price > points[3].price else -trend_direction
        
        logging.debug(f"Leg lengths: XA={xa_length:.4f}, AB={ab_length:.4f}, BC={bc_length:.4f}, CD={cd_length:.4f}")
        logging.debug(f"Calculated ratios: {ratios}")
        
        # Check each pattern
        for pattern_name, expected_ratios in self.PATTERN_DEFINITIONS.items():
            logging.info(f"Checking for {pattern_name} pattern")
            pattern_valid = True
            
            for leg, expected_ratio in expected_ratios.items():
                actual_ratio = ratios[leg]
                min_ratio = expected_ratio * (1 - self.tolerance)
                max_ratio = expected_ratio * (1 + self.tolerance)
                
                # For negative ratios, swap min and max
                if expected_ratio < 0:
                    min_ratio, max_ratio = max_ratio, min_ratio
                
                if not (min_ratio <= actual_ratio <= max_ratio):
                    logging.debug(f"Ratio {actual_ratio:.4f} outside tolerance for expected {expected_ratio:.4f} (tolerance: {self.tolerance})")
                    logging.debug(f"{pattern_name} pattern invalid: {leg} ratio {actual_ratio:.4f} vs expected {expected_ratio:.4f}")
                    pattern_valid = False
                    break
                    
            if pattern_valid:
                logging.info(f"✅ {pattern_name} pattern detected!")
                pattern = {
                    'type': pattern_name,
                    'points': [{'price': p.price, 'timestamp': p.timestamp} for p in points],
                    'ratios': ratios,
                    'trend_direction': 'Bullish' if trend_direction > 0 else 'Bearish'
                }
                patterns.append(pattern)
            else:
                logging.debug(f"❌ {pattern_name} pattern not detected")
                
        logging.info(f"Pattern detection complete. Found {len(patterns)} patterns")
        return patterns
    
    def get_pattern_signals(self, patterns: List[HarmonicPattern]) -> List[Dict]:
        """Generate trading signals based on detected patterns."""
        try:
            signals = []
            
            for pattern in patterns:
                is_bullish = pattern.points[-1].price > pattern.points[0].price
                logging.info(f"Generating signal for {pattern.pattern_type} pattern ({'BULLISH' if is_bullish else 'BEARISH'})")
                
                signal = {
                    'pattern': pattern.pattern_type,
                    'type': 'BULLISH' if is_bullish else 'BEARISH',
                    'confidence': pattern.confidence,
                    'timeframes': pattern.timeframes,
                    'detected_at': pattern.detected_at.isoformat(),
                    'price_levels': {
                        'entry': pattern.points[-1].price,
                        'stop_loss': min(p.price for p in pattern.points),
                        'take_profit': max(p.price for p in pattern.points)
                    },
                    'fibonacci_levels': {
                        'XA': self.calculate_ratio(pattern.points[0].price, pattern.points[1].price),
                        'AB': self.calculate_ratio(pattern.points[1].price, pattern.points[2].price),
                        'BC': self.calculate_ratio(pattern.points[2].price, pattern.points[3].price),
                        'CD': self.calculate_ratio(pattern.points[3].price, pattern.points[4].price),
                        'AD': self.calculate_ratio(pattern.points[0].price, pattern.points[4].price)
                    }
                }
                signals.append(signal)
                logging.info(f"Generated signal for {pattern.pattern_type}: {signal}")
            
            logging.info(f"Generated {len(signals)} trading signals")
            return signals
            
        except Exception as e:
            logging.error(f"Error generating pattern signals: {e}")
            return [] 