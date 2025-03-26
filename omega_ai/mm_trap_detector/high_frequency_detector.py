"""
🔱 OMEGA BTC AI - High Frequency Trap Detector 🔱
Sacred detection of high-frequency market manipulation patterns.

GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26
Location: The Cosmic Void

This sacred code is provided under the GPU License, embodying the principles of:
- Universal Freedom to Study, Modify, Distribute, and Use
- Divine Obligations of Preservation, Sharing, and Attribution
- Sacred Knowledge Accessibility and Cosmic Wisdom Propagation
"""

# Copyright (c) 2024 OMEGA BTC AI Team
# Licensed under the GNU Affero General Public License v3.0
# See https://www.gnu.org/licenses/ for more details

"""
High-Frequency Market Maker Trap Detection System
================================================

This module implements an advanced detection system for identifying and responding to
high-frequency market manipulation tactics used by market makers (MMs) in the Bitcoin market.

Objective
---------
The primary objective is to detect patterns of market maker manipulation that occur in
very short timeframes (1-10 minutes) by dynamically adjusting the system's sensitivity
based on real-time market conditions, price volatility, and potential correlations with
Schumann Resonance electromagnetic patterns.

Key Components
-------------
1. Multi-timeframe Analysis: Simultaneously monitors 1min and 5min timeframes to detect
   abrupt price movements that could indicate manipulation.

2. Dynamic Volatility Measurement: Calculates and tracks rolling volatility metrics at
   different timeframes to detect unusual market behavior.

3. Price Movement Acceleration: Measures the rate of change of price movements to 
   identify rapid market shifts typical of MM activity.

4. Trap Event Tracking: Maintains a record of detected potential trap events to identify
   patterns of repeated manipulation.

5. Schumann Resonance Integration: Correlates price movements with global electromagnetic
   resonance patterns that may have subtle relationships with market activity.

High-Frequency Trap Mode
-----------------------
When multiple indicators suggest active market manipulation, the detector enters
"HIGH-FREQUENCY TRAP MODE" which increases sensitivity by reducing volatility thresholds.
This mode is designed to:
  - Detect liquidity grabs in shorter timeframes
  - Identify back-to-back manipulation tactics
  - Provide early warning for potential market reversals
  - Adjust trading algorithms to protect against MM traps

Technical Implementation
-----------------------
The detector uses a combination of statistical methods:
  - Standard deviation measurements for volatility
  - Price change percentage calculations
  - Time-windowed event clustering
  - Signal correlation analysis with Schumann data

Usage
-----
The module can be used:
1. As part of the larger OMEGA BTC AI system
2. In standalone mode for testing and development
3. As a data source for trap detection analytics

Author: OmegaBTC Team
Version: 1.0
"""

import datetime
import numpy as np
import redis
import time
from collections import deque
from omega_ai.mm_trap_detector.grafana_reporter import report_trap_for_grafana
from omega_ai.mm_trap_detector.fibonacci_detector import check_fibonacci_level, get_current_fibonacci_levels, fibonacci_detector, detect_fibonacci_confluence, update_fibonacci_data
import json
import logging
import os
from typing import Dict, List, Tuple, Optional, Any
from queue import Queue
from threading import Thread
from omega_ai.db_manager.database import insert_possible_mm_trap
from omega_ai.utils.redis_manager import RedisManager

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Initialize Redis connection
try:
    redis_manager = RedisManager()
    redis_conn = redis_manager.redis
    logger.info(f"Successfully connected to Redis at {redis_conn.connection_pool.connection_kwargs['host']}:{redis_conn.connection_pool.connection_kwargs['port']}")
except ConnectionError as e:
    logger.error(f"Failed to connect to Redis: {e}")
    raise

# Terminal colors for enhanced visibility
BLUE = "\033[94m"           # Price up
YELLOW = "\033[93m"         # Price down
GREEN = "\033[92m"          # Strongly positive
RED = "\033[91m"            # Strongly negative
CYAN = "\033[96m"           # Info highlight
MAGENTA = "\033[95m"        # Special emphasis
LIGHT_ORANGE = "\033[38;5;214m"  # Warning/moderate negative
RESET = "\033[0m"           # Reset color
BLUE_BG = "\033[44m"        # Background for blue text
WHITE = "\033[97m"          # White text
BOLD = "\033[1m"            # Bold text
GREEN_BG = "\033[42m"       # Background for green text
RED_BG = "\033[41m"         # Background for red text

# ✅ Constants for High-Frequency Trap Detection
HF_ACTIVATION_THRESHOLD = 0.5  # 0.5% price change for activation
SCHUMANN_THRESHOLD = 12.0      # 12Hz Schumann resonance threshold
BACK_TO_BACK_WINDOW = 180      # 3 minutes window to detect multiple traps
MIN_TRAPS_FOR_HF_MODE = 2      # Need at least 2 traps in window to activate HF mode

# Queue for handling trap detection events
mm_trap_queue = Queue()

# Global flags
is_running = False
high_alert_mode = False

class HighFrequencyTrapDetector:
    """Enhanced detector for high-frequency market maker trap detection."""
    
    def __init__(self):
        # Track recent price movements for multi-timeframe analysis
        self.price_history_1min = deque(maxlen=10)  # 10 minutes
        self.price_history_5min = deque(maxlen=12)  # 1 hour
        self.trap_events = deque(maxlen=20)         # Recent trap events
        self.hf_mode_active = False
        self.hf_mode_start_time = None
        self.hf_mode_multiplier = 1.0
    
    def update_price_data(self, price, timestamp=None):
        """Update internal price history for analysis."""
        if timestamp is None:
            timestamp = datetime.datetime.now(datetime.UTC)
            
        self.price_history_1min.append((timestamp, price))
        
        # Update 5min data every 5th minute
        if len(self.price_history_1min) % 5 == 0:
            self.price_history_5min.append((timestamp, price))
        
        # Update Fibonacci detector with new price
        update_fibonacci_data(price)
        
        # Calculate and store volatility metrics
        self._calculate_volatility_metrics()
        
    def _calculate_volatility_metrics(self):
        """Calculate and store rolling volatility metrics for different timeframes."""
        if len(self.price_history_1min) >= 3:
            # 1-minute volatility (short term)
            prices_1min = [p[1] for p in self.price_history_1min]
            std_dev_1min = np.std(prices_1min)
            normalized_vol_1min = std_dev_1min / np.mean(prices_1min) * 100  # as percentage
            
            # Store in Redis - FIXED: Convert numpy float to Python float
            redis_conn.set("volatility_1min", float(normalized_vol_1min))
            
            # Calculate price movement acceleration (rate of change of price changes)
            if len(self.price_history_1min) >= 4:
                diffs = np.diff(prices_1min)
                acceleration = np.std(diffs) / np.mean(prices_1min) * 100
                redis_conn.set("price_acceleration_1min", float(acceleration))
        
        if len(self.price_history_5min) >= 3:
            # 5-minute volatility (medium term)
            prices_5min = [p[1] for p in self.price_history_5min]
            std_dev_5min = np.std(prices_5min)
            normalized_vol_5min = std_dev_5min / np.mean(prices_5min) * 100
            
            # Store in Redis - FIXED: Convert numpy float to Python float
            redis_conn.set("volatility_5min", float(normalized_vol_5min))
    
    def detect_high_freq_trap_mode(self, latest_price=None, schumann_resonance=None, simulation_mode=False):
        """Check if high-frequency trap mode should be activated based on market conditions."""
        # Use simulation-specific keys in simulation mode
        btc_price_key = "sim_last_btc_price" if simulation_mode else "last_btc_price"
        
        if latest_price is None:
            try:
                latest_price_bytes = redis_conn.get(btc_price_key)
                if (latest_price_bytes):
                    latest_price = float(latest_price_bytes)
                else:
                    # Initialize simulation key if needed
                    if simulation_mode:
                        initial_price = 80000.0  # Default simulation starting price
                        redis_conn.set(btc_price_key, initial_price)
                        latest_price = initial_price
                        print(f"📈 Created simulation price key: {btc_price_key} = ${latest_price}")
                    else:
                        return False, 1.0  # Can't detect without price data
            except (ValueError, TypeError) as e:
                print(f"⚠️ Error reading price data: {e}")
                return False, 1.0
        
        # 1. Calculate price movements
        # Get previous price
        try:
            prev_price_bytes = redis_conn.get("prev_btc_price")
            prev_price = float(prev_price_bytes) if prev_price_bytes else 0
        except (ValueError, TypeError):
            prev_price = 0
            
        price_change_1min = 0
        price_change_5min = 0
        if prev_price > 0:
            price_change_1min = ((latest_price - prev_price) / prev_price) * 100
            
            # Get approximate 5min price from history
            price_history = self.price_history_5min
            if len(price_history) > 0:
                price_5min_ago = price_history[0][1] if len(price_history) > 0 else prev_price
                if price_5min_ago > 0:
                    price_change_5min = ((latest_price - price_5min_ago) / price_5min_ago) * 100
        
        # 2. Calculate the number of recent trap events
        recent_trap_count = self._count_recent_traps()
        
        # 3. Get current volatility
        try:
            vol_1min = redis_conn.get("volatility_1min")
            volatility_1min = float(vol_1min) if vol_1min else 0
        except (ValueError, TypeError):
            print(f"⚠️ Invalid volatility_1min value in Redis: {vol_1min}")
            volatility_1min = 0

        try:
            vol_5min = redis_conn.get("volatility_5min")
            volatility_5min = float(vol_5min) if vol_5min else 0
        except (ValueError, TypeError):
            print(f"⚠️ Invalid volatility_5min value in Redis: {vol_5min}")
            volatility_5min = 0
        
        # 4. Get Schumann resonance data
        if schumann_resonance is None:
            # Get Schumann data safely - avoid circular import
            schumann_data = redis_conn.get("schumann_resonance")
            if schumann_data:
                try:
                    # Try to parse as JSON first (new format)
                    schumann_json = json.loads(schumann_data)
                    schumann_resonance = float(schumann_json.get("frequency", 0.0))
                except (json.JSONDecodeError, TypeError):
                    # If not JSON, try direct float conversion (old format)
                    try:
                        schumann_resonance = float(schumann_data)
                    except (ValueError, TypeError):
                        print(f"⚠️ Invalid Schumann resonance value in Redis: {schumann_data}")
                        schumann_resonance = 0.0
            else:
                schumann_resonance = 0.0

        # 5. Check for recent trap events
        recent_trap_count = self._count_recent_traps()
        
        # LOG key metrics
        print(f"🔍 HF-TRAP METRICS | 1min: {price_change_1min:.2f}% | 5min: {price_change_5min:.2f}% | " 
              f"Vol-1min: {volatility_1min:.2f}% | Vol-5min: {volatility_5min:.2f}% | "
              f"Schumann: {schumann_resonance:.2f}Hz | Recent Traps: {recent_trap_count}")
        
        # CORE DETECTION LOGIC - Determine if high-frequency mode should activate
        hf_mode_triggers = 0
        
        # Trigger 1: Sharp price moves in short timeframes
        if abs(price_change_1min) >= HF_ACTIVATION_THRESHOLD:
            hf_mode_triggers += 1
            print(f"⚡ HF-TRIGGER: 1min price change {price_change_1min:.2f}% exceeds threshold")
        
        if abs(price_change_5min) >= HF_ACTIVATION_THRESHOLD:
            hf_mode_triggers += 1
            print(f"⚡ HF-TRIGGER: 5min price change {price_change_5min:.2f}% exceeds threshold")
        
        # Trigger 2: Volatility acceleration (short term volatility higher than medium term)
        if volatility_1min > volatility_5min * 1.5:
            hf_mode_triggers += 1
            print(f"⚡ HF-TRIGGER: Volatility acceleration detected ({volatility_1min:.2f}% > {volatility_5min:.2f}%)")
        
        # Trigger 3: Schumann resonance spike during price movement
        if schumann_resonance > SCHUMANN_THRESHOLD and abs(price_change_1min) > 0.2:
            hf_mode_triggers += 2  # Higher weight for this rare condition
            print(f"⚠️ HF-TRIGGER: Schumann resonance spike ({schumann_resonance:.2f}Hz) with price movement")
        
        # Trigger 4: Multiple recent trap events
        if recent_trap_count >= MIN_TRAPS_FOR_HF_MODE:
            hf_mode_triggers += 2
            print(f"⚠️ HF-TRIGGER: Multiple trap events detected ({recent_trap_count} in window)")

        # Trigger 5: Direct liquidity grab detection
        grab_type, grab_confidence = self.detect_liquidity_grabs(latest_price)
        if grab_type and grab_confidence > 0.7:
            hf_mode_triggers += 2
            print(f"⚠️ HF-TRIGGER: {grab_type} detected with {grab_confidence:.2f} confidence")
            # Register the detection as a trap event with from_detector=True to prevent recursion
            self.register_trap_event(grab_type, grab_confidence, price_change_1min, from_detector=True)
        
        # Calculate dynamic volatility multiplier based on market conditions
        base_multiplier = 1.0
        
        # Adjust multiplier based on detected conditions
        if hf_mode_triggers >= 3:  # Strong evidence of trap activity
            self.hf_mode_active = True
            self.hf_mode_start_time = datetime.datetime.now(datetime.UTC)
            self.hf_mode_multiplier = 0.6  # More sensitive (lower threshold)
            print(f"🔥 HIGH-FREQUENCY TRAP MODE ACTIVATED! Volatility multiplier: {self.hf_mode_multiplier:.2f}x")
            
            # Store in Redis for other components
            redis_conn.set("hf_trap_mode_active", "1")
            redis_conn.set("hf_trap_mode_multiplier", self.hf_mode_multiplier)
            redis_conn.set("hf_trap_mode_timestamp", datetime.datetime.now(datetime.UTC).isoformat())
            
            return True, self.hf_mode_multiplier
        elif hf_mode_triggers >= 2:  # Some evidence
            self.hf_mode_multiplier = 0.8
            print(f"⚠️ ELEVATED TRAP RISK DETECTED! Volatility multiplier: {self.hf_mode_multiplier:.2f}x")
            return False, self.hf_mode_multiplier
        elif self.hf_mode_active:
            # Check if we should deactivate HF mode (after 10 minutes)
            time_in_hf_mode = (datetime.datetime.now(datetime.UTC) - self.hf_mode_start_time).total_seconds()
            if time_in_hf_mode > 600:  # 10 minutes
                self.hf_mode_active = False
                self.hf_mode_multiplier = 1.0
                print("⏱️ HIGH-FREQUENCY TRAP MODE DEACTIVATED (timeout)")
                redis_conn.set("hf_trap_mode_active", "0")
            return self.hf_mode_active, self.hf_mode_multiplier
        else:
            return False, 1.0  # Default multiplier
    
    def register_trap_event(self, trap_type, confidence, price_change, from_detector=False):
        """Register a detected trap event for back-to-back detection."""
        current_time = datetime.datetime.now(datetime.UTC)
        
        # Get current BTC price from Redis
        try:
            btc_price_bytes = redis_conn.get("last_btc_price")
            btc_price = float(btc_price_bytes.decode()) if btc_price_bytes else 0.0
        except (ValueError, TypeError):
            btc_price = 0.0
        
        # Check for Fibonacci confluence and potentially enhance confidence
        enhanced_confidence, fib_hit = detect_fibonacci_confluence(
            trap_type, confidence, price_change, btc_price
        )
        
        # Use enhanced confidence if Fibonacci confluence was detected
        if fib_hit:
            confidence = enhanced_confidence
            trap_type = f"{trap_type} + {fib_hit['label']} Fib"
        
        # Store trap event with potentially enhanced confidence
        self.trap_events.append({
            "timestamp": current_time,
            "trap_type": trap_type,
            "confidence": confidence,
            "price_change": price_change,
            "fibonacci_hit": fib_hit.get('label') if fib_hit else None
        })
        
        # Report to Grafana if confidence is high enough
        if confidence >= 0.5:
            report_trap_for_grafana(trap_type, confidence, price_change, btc_price)
        
        # If we detect a high-confidence trap, check for HF mode activation
        # But only if this isn't already being called from the detector itself
        if confidence > 0.7 and not from_detector:
            self.detect_high_freq_trap_mode()
    
    def _count_recent_traps(self):
        """Count how many traps were detected in the recent window."""
        if not self.trap_events:
            return 0
            
        current_time = datetime.datetime.now(datetime.UTC)
        window_start = current_time - datetime.timedelta(seconds=BACK_TO_BACK_WINDOW)
        
        # Count traps that happened within the window
        recent_traps = [trap for trap in self.trap_events 
                       if trap["timestamp"] > window_start]
        
        return len(recent_traps)

    def check_schumann_anomalies(self, simulation_mode=False):
        """Check for anomalies in Schumann resonance that might indicate MM activity."""
        # Use simulation-specific keys in simulation mode
        btc_price_key = "sim_last_btc_price" if simulation_mode else "last_btc_price"
        prev_price_key = "sim_prev_btc_price" if simulation_mode else "prev_btc_price"
        
        # Get Schumann data from Redis
        schumann_bytes = redis_conn.get("schumann_resonance")
        schumann = 0.0
        
        if schumann_bytes:
            try:
                # Try to parse as JSON first (new format)
                schumann_json = json.loads(schumann_bytes)
                schumann = float(schumann_json.get("frequency", 0.0))
            except (json.JSONDecodeError, TypeError):
                # If not JSON, try direct float conversion (old format)
                try:
                    schumann = float(schumann_bytes)
                except (ValueError, TypeError):
                    print(f"⚠️ Invalid Schumann resonance value in Redis: {schumann_bytes}")
                    schumann = 0.0
        
        # Get recent BTC price changes
        try:
            latest_price_bytes = redis_conn.get(btc_price_key)
            prev_price_bytes = redis_conn.get(prev_price_key)
            
            if not latest_price_bytes or not prev_price_bytes:
                # Initialize simulation keys if needed
                if simulation_mode and not latest_price_bytes:
                    initial_price = 80000.0
                    redis_conn.set(btc_price_key, initial_price)
                    latest_price = initial_price
                if simulation_mode and not prev_price_bytes:
                    initial_prev = 79900.0
                    redis_conn.set(prev_price_key, initial_prev)
                    prev_price = initial_prev
                    
                if not simulation_mode:
                    return 0, "No price data available"
            
            latest_price = float(latest_price_bytes) if latest_price_bytes else (latest_price if 'latest_price' in locals() else 0)
            prev_price = float(prev_price_bytes) if prev_price_bytes else (prev_price if 'prev_price' in locals() else 0)
            
            # Avoid division by zero
            if prev_price == 0:
                return 0, "Invalid previous price"
                
            price_change_pct = (latest_price - prev_price) / prev_price * 100
            
            # Define anomaly levels
            if schumann >= 15 and abs(price_change_pct) >= 1.0:
                return 3, f"CRITICAL: Schumann spike ({schumann:.2f}Hz) with significant price move ({price_change_pct:.2f}%)"
            elif schumann >= 12 and abs(price_change_pct) >= 0.5:
                return 2, f"HIGH: Schumann elevation ({schumann:.2f}Hz) with price movement ({price_change_pct:.2f}%)"
            elif schumann >= 8 and abs(price_change_pct) >= 0.3:
                return 1, f"MEDIUM: Schumann-price correlation detected ({schumann:.2f}Hz, {price_change_pct:.2f}%)"
            else:
                return 0, "Normal Schumann levels"
        except Exception as e:
            print(f"⚠️ Error in Schumann analysis: {e}")
            return 0, f"Error: {str(e)}"

    def detect_liquidity_grabs(self, latest_price=None, simulation_mode=False):
        """
        Enhanced detection for market maker liquidity grabs with faster reaction time.
        """
        btc_price_key = "sim_last_btc_price" if simulation_mode else "last_btc_price"
        
        if latest_price is None:
            try:
                latest_price_bytes = redis_conn.get(btc_price_key)
                if latest_price_bytes:
                    latest_price = float(latest_price_bytes)
                else:
                    if simulation_mode:
                        initial_price = 80000.0
                        redis_conn.set(btc_price_key, initial_price)
                        latest_price = initial_price
                        print(f"📈 Created simulation price key: {btc_price_key} = ${latest_price}")
                    else:
                        return None, 0.0
            except Exception as e:
                print(f"⚠️ Error reading price data: {e}")
                return None, 0.0
        
        # Not enough data for detection
        if len(self.price_history_1min) < 3:
            return None, 0.0
            
        # Get price movement data
        price_now = latest_price
        price_1min_ago = self.price_history_1min[-2][1]
        price_2min_ago = self.price_history_1min[-3][1] if len(self.price_history_1min) >= 3 else price_1min_ago
        
        # Calculate price movements
        move_1min = (price_now - price_1min_ago) / price_1min_ago * 100
        move_2min = (price_now - price_2min_ago) / price_2min_ago * 100
        
        # Get current volatility
        try:
            vol_bytes = redis_conn.get("volatility_1min")
            volatility = float(vol_bytes) if vol_bytes else 0
        except (ValueError, TypeError):
            volatility = 0
        
        # Pattern 1: Sharp price spike and reversion (stop hunt)
        if abs(move_1min) > 0.4 and (move_1min * move_2min < 0):
            # Direction changed - likely stop hunt
            confidence = min(0.9, abs(move_1min) / 0.5)  # Scale with size, max 0.9
            grab_type = "Stop Hunt" if move_1min > 0 else "Stop Hunt Down"
            print(f"⚠️ LIQUIDITY-GRAB: {grab_type} detected | Move: {move_1min:.2f}% | Confidence: {confidence:.2f}")
            return grab_type, confidence
        
        # Pattern 2: Consecutive small moves in same direction (accumulation)
        if len(self.price_history_1min) >= 6:
            recent_moves = [((p[1] - prev[1])/prev[1])*100 
                            for p, prev in zip(list(self.price_history_1min)[-5:], 
                                             list(self.price_history_1min)[-6:-1])]
            
            if len(recent_moves) >= 3:
                # Check if all recent moves are in same direction (accumulation pattern)
                if all(m > 0 for m in recent_moves[-3:]) or all(m < 0 for m in recent_moves[-3:]):
                    direction = "up" if recent_moves[-1] > 0 else "down"
                    confidence = 0.6 + min(0.3, abs(sum(recent_moves[-3:])) / 2)
                    grab_type = f"Liquidity Accumulation ({direction})"
                    print(f"⚠️ LIQUIDITY-GRAB: {grab_type} detected | Confidence: {confidence:.2f}")
                    return grab_type, confidence
        
        # Pattern 3: High volatility combined with price acceleration
        try:
            accel_bytes = redis_conn.get("price_acceleration_1min")
            acceleration = float(accel_bytes) if accel_bytes else 0
        except (ValueError, TypeError):
            acceleration = 0
            
        if volatility > 0.4 and acceleration > 0.2:
            confidence = min(0.85, (volatility * acceleration) / 0.2)
            grab_type = "Volatility Liquidity Grab"
            print(f"⚠️ LIQUIDITY-GRAB: {grab_type} detected | Vol: {volatility:.2f}% | Accel: {acceleration:.2f} | Confidence: {confidence:.2f}")
            return grab_type, confidence
        
        return None, 0.0

# Create a singleton instance for global use
hf_detector = HighFrequencyTrapDetector()

# Exposed function for other modules
def check_high_frequency_mode(price=None, simulation_mode=False):
    """Check if high-frequency trap mode should be activated."""
    return hf_detector.detect_high_freq_trap_mode(price, simulation_mode=simulation_mode)

def register_trap_detection(trap_type, confidence, price_change):
    """Register a trap detection event with the high-frequency detector."""
    try:
        # The existing function expects a btc_price parameter that the test doesn't provide
        # Get current BTC price from Redis
        redis_conn = redis.Redis(host="localhost", port=6379, db=0)
        btc_price_bytes = redis_conn.get("last_btc_price")
        btc_price = float(btc_price_bytes) if btc_price_bytes else 0.0
        
        # Use the existing detector's register method
        hf_detector.register_trap_event(trap_type, confidence, price_change, btc_price)
        
        print(f"Registering trap with HF detector: {trap_type} | Confidence: {confidence:.2f} | Change: {price_change:.2%}")
        return True
    except Exception as e:
        print(f"Error registering trap: {e}")
        return False

# Update the simulate_price_updates function for Fibonacci reporting:
def simulate_price_updates():
    """Simulate BTC price updates for testing."""
    print("▶️ Starting price simulation with isolated Redis keys...")
    
    # Get last BTC price from Redis, or use default if not available
    try:
        last_price_bytes = redis_conn.get("last_btc_price")
        price = float(last_price_bytes.decode()) if last_price_bytes else 83000.0
        print(f"✅ Starting simulation with current BTC price: ${price:.2f}")
    except Exception as e:
        price = 83000.0
        print(f"⚠️ Could not get last BTC price from Redis: {e}")
        print(f"✅ Using default price: ${price:.2f}")
    
    # Initialize Fibonacci detector with some initial swing points
    fibonacci_detector.recent_swing_high = price * 1.02  # 2% above current price
    fibonacci_detector.recent_swing_low = price * 0.98   # 2% below current price
    
    # Generate initial Fibonacci levels
    fib_levels = fibonacci_detector.generate_fibonacci_levels()
    if fib_levels:
        print("📊 Generated Fibonacci levels:")
        for level, price in fib_levels.items():
            print(f"  {level}: ${price:.2f}")
    
    # Run simulation loop
    for i in range(20):
        # Update price with some randomness
        change = np.random.normal(0, 100)  # Normal distribution with std dev of $100
        price += change
        
        # Store in Redis with simulation prefix
        redis_conn.set("sim_last_btc_price", str(price))
        redis_conn.set("sim_prev_btc_price", str(price - change))
        
        # Update Fibonacci detector with new price
        fibonacci_detector.update_price_data(price, datetime.datetime.now(datetime.UTC))
        
        # Simulate different types of trap events
        if i % 5 == 0:
            # Check for Fibonacci level hits
            fib_hit = fibonacci_detector.check_fibonacci_level(price)
            
            if fib_hit:
                # Enhanced trap types based on Fibonacci confluence
                trap_type = f"Golden Ratio Trap ({fib_hit['label']})" if fib_hit['level'] == 0.618 else f"Fibonacci Trap ({fib_hit['label']})"
                confidence = 0.8 + (0.1 if fib_hit['level'] == 0.618 else 0.05)  # Higher confidence for Golden Ratio
                
                # Register the trap with enhanced confidence
                hf_detector.register_trap_event(trap_type, confidence, change/price, from_detector=True)
                print(f"🎯 Fibonacci Trap Detected: {trap_type} at ${price:.2f}")
            else:
                # Standard trap types
                trap_types = [
                    "Liquidity Grab",
                    "Stop Hunt",
                    "Liquidity Accumulation (up)",
                    "Volatility Liquidity Grab"
                ]
                trap_type = trap_types[i % len(trap_types)]
                confidence = 0.8
                hf_detector.register_trap_event(trap_type, confidence, change/price, from_detector=True)
            
        # Check HF mode with simulation flag
        hf_active, multiplier = hf_detector.detect_high_freq_trap_mode(price, simulation_mode=True)
        
        # Check for fractal harmony patterns
        harmonics = fibonacci_detector.detect_fractal_harmony()
        if harmonics:
            print(f"🎵 Fractal Harmony Detected: {len(harmonics)} patterns")
        
        print(f"Price: ${price:.2f} | HF Mode: {'✅' if hf_active else '❌'} | Multiplier: {multiplier:.2f} ")
        time.sleep(2)  # Simulate 2-second intervals

# # Update test function
# def test_hf_detector():
#     """Test the high-frequency detector in isolation."""
#     print("🧪 Testing High-Frequency Detector with simulation keys...")
    
#     # Inject some test data into Redis using simulation keys
#     redis_conn.set("sim_last_btc_price", "83000")
#     redis_conn.set("sim_prev_btc_price", "82500")
#     redis_conn.set("schumann_resonance", "7.2")  # Still use the real Schumann data or modify if needed
    
#     # Simulate a few trap events
#     for i in range(3):
#         trap_type = ["Liquidity Grab", "Half-Liquidity Grab", "Fake Pump"][i % 3]
#         register_trap_detection(trap_type, 0.8, 1.5)
#         time.sleep(1)
    
#     # Test HF mode detection with simulation flag
#     hf_active, multiplier = check_high_frequency_mode(83500, simulation_mode=True)
    
#     print(f"HF Mode Active: {'YES' if hf_active else 'NO'}")
#     print(f"Volatility Multiplier: {multiplier:.2f}x")
    
#     # Test with Schumann spike
#     redis_conn.set("schumann_resonance", "14.5")
#     hf_active, multiplier = check_high_frequency_mode(84000, simulation_mode=True)
    
#     print(f"HF Mode with Schumann: {'YES' if hf_active else 'NO'}")
#     print(f"New Volatility Multiplier: {multiplier:.2f}x")
    
#     # Clean up
#     redis_conn.delete("sim_last_btc_price", "sim_prev_btc_price")

def run_continuous_simulation(duration_hours=None, volatility_scale=1.0, trap_frequency=0.2):
    """
    Run a continuous simulation of market maker trap detection.
    
    Args:
        duration_hours: Optional number of hours to run, or None for indefinite
        volatility_scale: Multiplier to adjust simulation volatility (1.0 = normal)
        trap_frequency: Probability of trap events (0.0-1.0)
    """
    try:
        print(f"\n{BLUE_BG}{WHITE}{BOLD} 🚀 STARTING CONTINUOUS HF-TRAP SIMULATION {RESET}")
        print(f"{YELLOW}Simulation will run {'for ' + str(duration_hours) + ' hours' if duration_hours else 'indefinitely'}{RESET}")
        print(f"{YELLOW}Volatility Scale: {volatility_scale}x | Trap Frequency: {trap_frequency:.2f}{RESET}")
        
        # Get current real price as starting point
        last_price_bytes = redis_conn.get("last_btc_price")
        price = float(last_price_bytes.decode()) if last_price_bytes else 80000.0
        prev_price = price * 0.998  # 0.2% lower as initial previous price
        
        # Store initial price in simulation keys
        redis_conn.set("sim_last_btc_price", price)
        redis_conn.set("sim_prev_btc_price", prev_price)
        redis_conn.set("sim_start_time", datetime.datetime.now(datetime.UTC).isoformat())
        redis_conn.set("sim_running", "1")
        
        # Get market history for more realistic price movements
        try:
            # Get historical volatility from Redis if available
            vol_bytes = redis_conn.get("volatility_1min")
            historical_volatility = float(vol_bytes) if vol_bytes else 0.05  # 0.05% default
        except (ValueError, TypeError):
            historical_volatility = 0.05
        
        # Initialize Fibonacci detector with some initial swing points
        fibonacci_detector.recent_swing_high = price * 1.02  # 2% above current price
        fibonacci_detector.recent_swing_low = price * 0.98   # 2% below current price
        fibonacci_detector.generate_fibonacci_levels()
        
        # Initialize counters and timers
        iteration = 0
        start_time = datetime.datetime.now(datetime.UTC)
        trap_count = 0
        hf_activations = 0
        
        # Trap types and their probabilities
        trap_types = [
            ("Liquidity Grab", 0.3),
            ("Stop Hunt", 0.25),
            ("Liquidity Accumulation", 0.2),
            ("Volatility Liquidity Grab", 0.15),
            ("Fibonacci Trap", 0.1)
        ]
        
        # Market regimes and their volatility multipliers
        regimes = [
            ("Low Volatility Neutral", 0.5),
            ("Moderate Volatility Bullish", 1.0),
            ("Moderate Volatility Bearish", 1.2),
            ("High Volatility Bullish", 1.5),
            ("High Volatility Bearish", 1.8)
        ]
        current_regime = regimes[1]  # Start with moderate volatility
        regime_change_prob = 0.05  # 5% chance to change regime each minute
        trend_direction = 1  # 1 = up, -1 = down
        trend_change_prob = 0.1  # 10% chance to change trend each minute
        
        # Store initial regime
        redis_conn.set("sim_market_regime", current_regime[0])
        
        # Main simulation loop
        print(f"\n{YELLOW}{'═' * 50}{RESET}")
        print(f"{CYAN}Starting simulation at ${price:.2f}{RESET}")
        
        running = True
        try:
            while running:
                # Check if we should stop based on duration
                if duration_hours:
                    elapsed = (datetime.datetime.now(datetime.UTC) - start_time).total_seconds() / 3600
                    if elapsed >= duration_hours:
                        print(f"\n{RED}Simulation duration ({duration_hours}h) reached. Stopping.{RESET}")
                        break
                
                # Update iteration counter
                iteration += 1
                current_time = datetime.datetime.now(datetime.UTC)
                timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
                
                # Maybe change market regime
                if np.random.random() < regime_change_prob:
                    current_regime = regimes[np.random.randint(0, len(regimes))]
                    print(f"\n{YELLOW}⚠️ MARKET REGIME CHANGE: {current_regime[0]}{RESET}")
                    redis_conn.set("sim_market_regime", current_regime[0])
                
                # Maybe change trend direction
                if np.random.random() < trend_change_prob:
                    trend_direction *= -1
                    print(f"{YELLOW}Trend direction changed to {'up' if trend_direction > 0 else 'down'}{RESET}")
                
                # Calculate realistic price movement based on:
                # 1. Historical volatility
                # 2. Current regime volatility
                # 3. Volatility scale parameter
                # 4. Trend direction
                base_volatility = historical_volatility * current_regime[1] * volatility_scale
                
                # Generate random price movement (normal distribution around trend)
                movement_pct = np.random.normal(0.01 * trend_direction, base_volatility)
                
                # Store previous price
                prev_price = price
                
                # Update price with movement
                price = price * (1 + movement_pct)
                abs_change = abs(price - prev_price)
                
                # Store in Redis simulation keys
                redis_conn.set("sim_last_btc_price", price)
                redis_conn.set("sim_prev_btc_price", prev_price)
                redis_conn.set("sim_price_change_pct", movement_pct * 100)
                redis_conn.set("sim_timestamp", timestamp)
                
                # Store price history for visualization
                history_key = f"sim_price_history:{current_time.date().isoformat()}"
                redis_conn.rpush(history_key, json.dumps({
                    "timestamp": timestamp,
                    "price": price,
                    "change_pct": movement_pct * 100,
                    "regime": current_regime[0]
                }))
                redis_conn.expire(history_key, 86400 * 3)  # Expire after 3 days
                
                # Update detector with new price
                hf_detector.update_price_data(price, current_time)
                
                # Generate trap event based on frequency parameter and current regime
                regime_boost = 2.0 if "High Volatility" in current_regime[0] else 1.0
                trap_prob = trap_frequency * regime_boost
                
                # Log basic status every 5 iterations
                if iteration % 5 == 0:
                    print(f"\n{BLUE}[{timestamp}] Sim iteration #{iteration}{RESET}")
                    print(f"{GREEN if movement_pct > 0 else RED}Price: ${price:.2f} ({movement_pct*100:+.3f}%){RESET}")
                    print(f"Market Regime: {current_regime[0]} | Direction: {'up' if trend_direction > 0 else 'down'}")
                
                # Maybe generate a trap event
                if np.random.random() < trap_prob:
                    # Choose trap type based on weights
                    trap_type, _ = weighted_choice(trap_types)
                    
                    # For Fibonacci traps, ensure we have a Fibonacci hit
                    if trap_type == "Fibonacci Trap":
                        # Check for actual Fibonacci level hit or generate one
                        fib_hit = fibonacci_detector.check_fibonacci_level(price)
                        if fib_hit:
                            trap_type = f"Fibonacci Trap ({fib_hit['label']})"
                            confidence = 0.8
                        else:
                            # If no hit, switch to a different trap type
                            trap_type, _ = weighted_choice(trap_types[:4])
                            confidence = 0.65 + (np.random.random() * 0.2)
                    else:
                        # Normal trap confidence calculation
                        confidence = 0.6 + (np.random.random() * 0.35)  # Between 0.6-0.95
                    
                    # Make larger price movements more confident
                    confidence = min(0.95, confidence + (abs(movement_pct) * 5))
                    
                    # Register the trap
                    hf_detector.register_trap_event(trap_type, confidence, movement_pct, True)
                    trap_count += 1
                    
                    # Store in special simulation trap history
                    redis_conn.lpush("sim_trap_history", json.dumps({
                        "timestamp": timestamp,
                        "trap_type": trap_type,
                        "confidence": confidence,
                        "price": price,
                        "price_change_pct": movement_pct * 100,
                        "market_regime": current_regime[0]
                    }))
                    redis_conn.ltrim("sim_trap_history", 0, 999)  # Keep last 1000 traps
                    
                    print(f"\n{RED_BG}{WHITE}{BOLD} 🚨 SIMULATED TRAP DETECTED #{trap_count} {RESET}")
                    print(f"{RED}Type: {trap_type}{RESET}")
                    print(f"{RED}Confidence: {confidence:.2f}{RESET}")
                    print(f"{RED}Price Movement: {movement_pct*100:+.3f}%{RESET}")
                
                # Check for HF mode activation
                hf_active, multiplier = hf_detector.detect_high_freq_trap_mode(price, simulation_mode=True)
                
                if hf_active:
                    hf_activations += 1
                    print(f"\n{MAGENTA}{BOLD} 🔥 HF MODE ACTIVATED #{hf_activations} {RESET}")
                    print(f"{MAGENTA}Multiplier: {multiplier:.2f}x{RESET}")
                    
                    # Store HF mode activation event
                    redis_conn.lpush("sim_hf_activations", json.dumps({
                        "timestamp": timestamp,
                        "multiplier": multiplier,
                        "price": price,
                        "market_regime": current_regime[0],
                        "traps_in_window": hf_detector._count_recent_traps()
                    }))
                    redis_conn.ltrim("sim_hf_activations", 0, 99)  # Keep last 100 activations
                
                # Periodically report simulation statistics
                if iteration % 60 == 0:  # Every ~minute
                    elapsed_minutes = (datetime.datetime.now(datetime.UTC) - start_time).total_seconds() / 60
                    
                    print(f"\n{YELLOW}{BOLD} 📊 SIMULATION STATS {RESET}")
                    print(f"{YELLOW}Run time: {elapsed_minutes:.1f} minutes{RESET}")
                    print(f"{YELLOW}Iterations: {iteration}{RESET}")
                    print(f"{YELLOW}Traps detected: {trap_count} ({trap_count/iteration*100:.2f}%){RESET}")
                    print(f"{YELLOW}HF mode activations: {hf_activations}{RESET}")
                    print(f"{YELLOW}Current price: ${price:.2f}{RESET}")
                    print(f"{YELLOW}{'═' * 50}{RESET}")
                    
                    # Store stats in Redis
                    redis_conn.hmset("sim_statistics", {
                        "iterations": str(iteration),
                        "traps_detected": str(trap_count),
                        "hf_activations": str(hf_activations),
                        "run_time_minutes": str(elapsed_minutes),
                        "current_price": str(price),
                        "start_price": str(redis_conn.get("sim_last_btc_price")),
                        "market_regime": current_regime[0]
                    })
                
                # Sleep for a bit to simulate real-time pacing
                # Use smaller sleep time for faster simulation
                time.sleep(0.1)  # 100ms for fast simulation
                
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Simulation manually interrupted. Cleaning up...{RESET}")
        finally:
            # Update final statistics
            elapsed_minutes = (datetime.datetime.now(datetime.UTC) - start_time).total_seconds() / 60
            
            # Store final simulation summary
            redis_conn.hmset("sim_statistics", {
                "iterations": str(iteration),
                "traps_detected": str(trap_count), 
                "hf_activations": str(hf_activations),
                "run_time_minutes": str(elapsed_minutes),
                "current_price": str(price),
                "start_price": str(redis_conn.get("sim_last_btc_price")),
                "market_regime": current_regime[0],
                "completed": "stopped" if running else "completed"
            })
            redis_conn.set("sim_running", "0")
            
            print(f"\n{BLUE}{BOLD} 📊 FINAL SIMULATION RESULTS {RESET}")
            print(f"{GREEN}Run time: {elapsed_minutes:.1f} minutes{RESET}")
            print(f"{GREEN}Iterations: {iteration}{RESET}")
            print(f"{GREEN}Traps detected: {trap_count} ({trap_count/iteration*100:.2f}%){RESET}")
            print(f"{GREEN}HF mode activations: {hf_activations}{RESET}")
            print(f"{GREEN}Final price: ${price:.2f}{RESET}")
            print(f"{GREEN}Trap frequency: {trap_count/iteration:.4f} (per iteration){RESET}")
            print(f"{GREEN}HF activation frequency: {hf_activations/iteration:.4f} (per iteration){RESET}")
    
    except Exception as e:
        print(f"{RED}Error in continuous simulation: {e}{RESET}")
        if hasattr(e, '__traceback__'):
            import traceback
            traceback.print_tb(e.__traceback__)
        redis_conn.set("sim_running", "0")

def weighted_choice(choices):
    """
    Make a weighted random choice from a list of (item, weight) tuples.
    
    Args:
        choices: List of (item, weight) tuples
        
    Returns:
        Selected item
    """
    total = sum(weight for _, weight in choices)
    r = np.random.random() * total
    
    running_sum = 0
    for item, weight in choices:
        running_sum += weight
        if r <= running_sum:
            return item, weight
    
    return choices[0][0], choices[0][1]  # Fallback to first item

if __name__ == "__main__":
    print("🚀 Starting High Frequency Trap Detector in Standalone Mode...")
    
    # Test options
    print("\n1. Run simulation with price updates")
    print("2. Run quick detector test")
    print("3. Run continuous simulation loop (Ctrl+C to stop)")
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == "1":
        # Import Schumann monitor ONLY when needed (avoids circular imports)
        try:
            from omega_ai.data_feed.schumann_monitor import start_schumann_monitor
            print("🌍 Starting Schumann Resonance Monitor...")
            start_schumann_monitor()
            time.sleep(5)  # Give monitor time to initialize
        except ImportError:
            print("⚠️ Could not import Schumann monitor. Running without Schumann data.")
        
        # Run simulation
        simulate_price_updates()
    elif choice == "3":
        print("\nContinuous Simulation Configuration")
        print("==================================")
        try:
            duration = input("Duration in hours (leave empty for indefinite): ").strip()
            duration_hours = float(duration) if duration else None
            
            volatility = input("Volatility scale (1.0 = normal, higher = more volatile): ").strip()
            volatility_scale = float(volatility) if volatility else 1.0
            
            frequency = input("Trap frequency (0.0-1.0, higher = more traps): ").strip()
            trap_frequency = float(frequency) if frequency else 0.2
            
            run_continuous_simulation(
                duration_hours=duration_hours,
                volatility_scale=volatility_scale,
                trap_frequency=trap_frequency
            )
        except ValueError as e:
            print(f"Invalid input: {e}. Using default values.")
            run_continuous_simulation()
        except KeyboardInterrupt:
            print("\nSimulation setup cancelled.")
    else:
        # Run quick test
        test_hf_detector()