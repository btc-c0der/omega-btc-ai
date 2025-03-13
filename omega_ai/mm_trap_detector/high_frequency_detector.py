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
# ✅ Redis connection
redis_conn = redis.Redis(host="localhost", port=6379, db=0)

# ✅ Constants for High-Frequency Trap Detection
HF_ACTIVATION_THRESHOLD = 0.5  # 0.5% price change for activation
SCHUMANN_THRESHOLD = 12.0      # 12Hz Schumann resonance threshold
BACK_TO_BACK_WINDOW = 180      # 3 minutes window to detect multiple traps
MIN_TRAPS_FOR_HF_MODE = 2      # Need at least 2 traps in window to activate HF mode

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
            except Exception as e:
                print(f"⚠️ Error reading price data: {e}")
                return False, 1.0
        
        # Check if we have enough historical data
        if len(self.price_history_1min) < 2 or len(self.price_history_5min) < 2:
            return False, 1.0
        
        # 1. Check for Sudden Price Spikes in 1min timeframe
        price_1min_ago = self.price_history_1min[-2][1]
        price_change_1min = (latest_price - price_1min_ago) / price_1min_ago * 100
        
        # 2. Check for Sudden Price Spikes in 5min timeframe
        price_5min_ago = self.price_history_5min[-2][1]
        price_change_5min = (latest_price - price_5min_ago) / price_5min_ago * 100
        
        # 3. Detect acceleration in volatility - with better error handling
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
            schumann_bytes = redis_conn.get("schumann_resonance")
            schumann_resonance = float(schumann_bytes) if schumann_bytes else 0.0

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
            btc_price = float(btc_price_bytes) if btc_price_bytes else 0.0
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
        schumann = float(schumann_bytes) if schumann_bytes else 0.0
        
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

def register_trap_detection(trap_type, confidence, price_change, btc_price):
    """Register a trap detection event"""
    try:
        # Update detector state
        hf_detector.register_trap_event(trap_type, confidence, price_change, btc_price)
        
    except Exception as e:
        print(f"Error registering trap: {e}")

# Update the simulate_price_updates function for Fibonacci reporting:
def simulate_price_updates():
    """Simulate price updates for testing the HF detector without affecting real data."""
    print("▶️ Starting price simulation with isolated Redis keys...")
    
    # Initial BTC price
    price = 83000.0
    
    # Initialize simulation keys
    redis_conn.set("sim_last_btc_price", price)
    redis_conn.set("sim_prev_btc_price", price * 0.99)  # Initial previous price
    
    # Track simulation statistics
    all_prices = [price]
    min_price = price
    max_price = price
    start_price = price
    
    # Simulate price updates
    for i in range(20):
        # Update price with some randomness
        change = np.random.normal(0, 100)  # Normal distribution with std dev of $100
        price += change
        
        # Track statistics
        all_prices.append(price)
        min_price = min(min_price, price)
        max_price = max(max_price, price)
        
        # Add to detector
        hf_detector.update_price_data(price)
        
        # Store in Redis using simulation-specific keys
        redis_conn.set("sim_prev_btc_price", redis_conn.get("sim_last_btc_price"))
        redis_conn.set("sim_last_btc_price", price)
        
        # Simulate a trap event occasionally
        if i % 5 == 0:
            trap_type = ["Liquidity Grab", "Stop Hunt", "Liquidity Accumulation (up)"][i % 3]
            confidence = 0.8
            # FIX: Pass the current price as btc_price parameter
            register_trap_detection(trap_type, confidence, 1.2, price)
            
        # Check HF mode with simulation flag
        hf_active, multiplier = hf_detector.detect_high_freq_trap_mode(price, simulation_mode=True)
        
        # Check if price is at a Fibonacci level
        fib_hit = check_fibonacci_level(price)
        fib_indicator = f"| 🔄 FIB: {fib_hit['label']}" if fib_hit else ""
        
        print(f"Price: ${price:.2f} | HF Mode: {'✅' if hf_active else '❌'} | Multiplier: {multiplier:.2f} {fib_indicator}")
        time.sleep(2)
    
    # Calculate and display simulation statistics
    print("\n📊 SIMULATION STATISTICS:")
    price_range = max_price - min_price
    print(f"Price Range: ${min_price:.2f} - ${max_price:.2f} (${price_range:.2f})")
    print(f"Total Movement: ${price - start_price:.2f} ({((price - start_price) / start_price * 100):.2f}%)")
    
    # Calculate standard statistical measures
    mean_price = sum(all_prices) / len(all_prices)
    std_dev = np.std(all_prices)
    print(f"Mean Price: ${mean_price:.2f}")
    print(f"Standard Deviation: ${std_dev:.2f}")
    
    # Display Fibonacci retracement levels based on simulation range
    print("\n🔄 FIBONACCI RETRACEMENT LEVELS:")
    fib_levels = get_current_fibonacci_levels()
    
    if fib_levels:
        for label, price in fib_levels.items():
            print(f"{label} Level: ${price:.2f}")
    else:
        print("No Fibonacci levels calculated yet")
    
    # Report on Fibonacci hits during simulation
    confluences = fibonacci_detector.trap_fib_confluences
    if confluences:
        print("\n🎯 FIBONACCI CONFLUENCE EVENTS:")
        for event in confluences:
            print(f"- {event['trap_type']} aligned with {event['fibonacci_level']} level at ${event['price']:.2f}")
            print(f"  Confidence: {event['confidence']:.2f} | Type: {event['confluence_type']}")
    
    # Clean up simulation keys when done
    print("\n🧹 Cleaning up simulation data...")
    redis_conn.delete("sim_last_btc_price", "sim_prev_btc_price")

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

if __name__ == "__main__":
    print("🚀 Starting High Frequency Trap Detector in Standalone Mode...")
    
    # Test options
    print("\n1. Run simulation with price updates")
    print("2. Run quick detector test")
    choice = input("Enter choice (1/2): ").strip()
    
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
    else:
        # Run quick test
        test_hf_detector()