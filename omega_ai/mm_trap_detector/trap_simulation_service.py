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


# Copyright (c) 2024 OMEGA BTC AI Team
# Licensed under the GNU Affero General Public License v3.0
# See https://www.gnu.org/licenses/ for more details

"""
Market Maker Trap Simulation Service
===================================

This service simulates Bitcoin price movements and market maker trap detection.
It stores all data in Redis with 'sim_' prefixes to avoid interfering with real data.

Features:
- Configurable volatility and trap frequency
- Multiple market regimes with realistic price movements
- Random trap generation with various types
- Statistics tracking and Redis storage
- Can run indefinitely or for a specified duration

Usage:
  python -m omega_ai.mm_trap_detector.trap_simulation_service [options]

Options:
  --duration HOURS    Run for specified hours (default: indefinite)
  --volatility SCALE  Volatility scale factor (default: 1.0)
  --frequency PROB    Trap frequency (0.0-1.0, default: 0.2)
  --sleep SECONDS     Sleep between iterations (default: 0.1)
"""

import sys
import time
import json
import redis
import argparse
import datetime
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from omega_ai.mm_trap_detector.redis_time_series import (
    store_time_series_data,
    compress_historical_data,
    get_time_series_data,
    TimeSeriesGranularity,
    cleanup_old_data
)

# Terminal Colors
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
BLACK = "\033[30m"

# Initialize Redis connection
redis_conn = redis.Redis(host="localhost", port=6379, db=0)

class TrapSimulator:
    """
    Simulates market maker trap detection with realistic price movements.
    
    This class provides a complete simulation environment for testing market maker
    trap detection algorithms. It generates realistic price movements, simulates
    different market regimes, and creates trap events with varying types and
    confidence levels.
    
    The simulator stores all data in Redis with 'sim_' prefixes to avoid
    interfering with real market data. This allows parallel testing without
    affecting production systems.
    
    Key features:
    - Realistic price movement simulation based on volatility and market regimes
    - Dynamic trap generation with configurable frequency
    - High-frequency mode detection when multiple traps occur in sequence
    - Complete statistics tracking and reporting
    - Redis integration for data storage and retrieval
    
    Usage:
        simulator = TrapSimulator(volatility_scale=1.5, trap_frequency=0.3)
        simulator.run(duration_hours=2.0)
    """
    
    def __init__(self, 
                 volatility_scale: float = 1.0, 
                 trap_frequency: float = 0.2,
                 sleep_interval: float = 0.1):
        """
        Initialize the trap simulator.
        
        Args:
            volatility_scale: Multiplier for price volatility (1.0 = normal)
            trap_frequency: Probability of trap events (0.0-1.0)
            sleep_interval: Seconds to sleep between iterations
        """
        self.volatility_scale = volatility_scale
        self.trap_frequency = trap_frequency
        self.sleep_interval = sleep_interval
        
        # Get current real price as starting point
        last_price_bytes = redis_conn.get("last_btc_price")
        self.price = float(last_price_bytes) if last_price_bytes else 80000.0
        self.prev_price = self.price * 0.998  # 0.2% lower as initial previous price
        
        # Initialize counters and state
        self.iteration = 0
        self.start_time = datetime.datetime.now(datetime.UTC)
        self.trap_count = 0
        self.hf_activations = 0
        self.trap_history = []
        
        # Market regime and trend settings
        self.regimes = [
            ("Low Volatility Neutral", 0.5),
            ("Moderate Volatility Bullish", 1.0),
            ("Moderate Volatility Bearish", 1.2),
            ("High Volatility Bullish", 1.5),
            ("High Volatility Bearish", 1.8)
        ]
        self.current_regime = self.regimes[1]  # Start with moderate volatility
        self.regime_change_prob = 0.05  # 5% chance to change regime each minute
        self.trend_direction = 1  # 1 = up, -1 = down
        self.trend_change_prob = 0.1  # 10% chance to change trend each minute
        
        # Trap types and their probabilities
        self.trap_types = [
            ("Liquidity Grab", 0.3),
            ("Stop Hunt", 0.25),
            ("Bull Trap", 0.2),
            ("Bear Trap", 0.15),
            ("Fibonacci Trap", 0.1)
        ]
        
        # Initialize Redis with simulation data
        self._initialize_redis()
        
    def _initialize_redis(self):
        """Initialize Redis with simulation data."""
        # Store initial price in simulation keys
        redis_conn.set("sim_last_btc_price", self.price)
        redis_conn.set("sim_prev_btc_price", self.prev_price)
        redis_conn.set("sim_start_time", datetime.datetime.now(datetime.UTC).isoformat())
        redis_conn.set("sim_running", "1")
        redis_conn.set("sim_market_regime", self.current_regime[0])
        
        # Clear old simulation data
        keys_to_delete = redis_conn.keys("sim_*_history*")
        if keys_to_delete:
            redis_conn.delete(*keys_to_delete)
        
    def run(self, duration_hours: Optional[float] = None):
        """
        Run the simulation for a specified duration or indefinitely.
        
        Args:
            duration_hours: Optional duration in hours, or None for indefinite
        """
        print(f"\n{BLUE}{BOLD} 🚀 STARTING TRAP SIMULATION {RESET}")
        print(f"{YELLOW}Simulation will run {'for ' + str(duration_hours) + ' hours' if duration_hours else 'indefinitely'}{RESET}")
        print(f"{YELLOW}Volatility Scale: {self.volatility_scale}x | Trap Frequency: {self.trap_frequency:.2f}{RESET}")
        print(f"{YELLOW}{'═' * 50}{RESET}")
        print(f"{CYAN}Starting simulation at ${self.price:.2f}{RESET}")
        
        try:
            while True:
                # Check if we should stop based on duration
                if duration_hours:
                    elapsed = (datetime.datetime.now(datetime.UTC) - self.start_time).total_seconds() / 3600
                    if elapsed >= duration_hours:
                        print(f"\n{RED}Simulation duration ({duration_hours}h) reached. Stopping.{RESET}")
                        break
                
                self._run_iteration()
                time.sleep(self.sleep_interval)
                
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Simulation manually interrupted. Cleaning up...{RESET}")
        finally:
            # Update final statistics
            self._save_final_statistics()
    
    def _run_iteration(self):
        """
        Run a single simulation iteration.
        
        This method:
        1. Updates the iteration counter and gets current timestamp
        2. Potentially changes market regime or trend direction
        3. Generates realistic price movement based on volatility settings
        4. Updates and stores price data in Redis
        5. Logs status information
        6. Potentially generates trap events
        7. Reports statistics periodically
        """
        # Update iteration counter
        self.iteration += 1
        current_time = datetime.datetime.now(datetime.UTC)
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Maybe change market regime
        if np.random.random() < self.regime_change_prob:
            self.current_regime = self.regimes[np.random.randint(0, len(self.regimes))]
            print(f"\n{YELLOW}⚠️ MARKET REGIME CHANGE: {self.current_regime[0]}{RESET}")
            redis_conn.set("sim_market_regime", self.current_regime[0])
        
        # Maybe change trend direction
        if np.random.random() < self.trend_change_prob:
            self.trend_direction *= -1
            print(f"{YELLOW}Trend direction changed to {'up' if self.trend_direction > 0 else 'down'}{RESET}")
        
        # Generate realistic price movement
        # Get historical volatility from Redis if available
        try:
            vol_bytes = redis_conn.get("volatility_1min")
            historical_volatility = float(vol_bytes) if vol_bytes else 0.05  # 0.05% default
        except (ValueError, TypeError):
            historical_volatility = 0.05
            
        # Calculate price movement based on:
        # 1. Historical volatility
        # 2. Current regime volatility
        # 3. Volatility scale parameter
        # 4. Trend direction
        base_volatility = historical_volatility * self.current_regime[1] * self.volatility_scale
        
        # Generate random price movement (normal distribution around trend)
        movement_pct = np.random.normal(0.01 * self.trend_direction, base_volatility)
        
        # Store previous price
        self.prev_price = self.price
        
        # Update price with movement
        self.price = self.price * (1 + movement_pct)
        abs_change = abs(self.price - self.prev_price)
        
        # Store in Redis simulation keys
        redis_conn.set("sim_last_btc_price", self.price)
        redis_conn.set("sim_prev_btc_price", self.prev_price)
        redis_conn.set("sim_price_change_pct", movement_pct * 100)
        redis_conn.set("sim_timestamp", timestamp)
        
        # Store price history using time series storage
        price_data = {
            "timestamp": timestamp,
            "price": self.price,
            "change_pct": movement_pct * 100,
            "regime": self.current_regime[0]
        }
        store_time_series_data("price_history", price_data, current_time)
        
        # Log basic status every 5 iterations
        if self.iteration % 5 == 0:
            print(f"\n{BLUE}[{timestamp}] Sim iteration #{self.iteration}{RESET}")
            print(f"{GREEN if movement_pct > 0 else RED}Price: ${self.price:.2f} ({movement_pct*100:+.3f}%){RESET}")
            print(f"Market Regime: {self.current_regime[0]} | Direction: {'up' if self.trend_direction > 0 else 'down'}")
        
        # Maybe generate a trap event
        self._maybe_generate_trap(movement_pct, timestamp)
            
        # Periodically report simulation statistics
        if self.iteration % 60 == 0:  # Every ~minute
            self._report_statistics()
            
            # Compress historical data if needed
            if self.iteration % 3600 == 0:  # Every hour
                compress_historical_data(
                    "price_history",
                    current_time.date(),
                    TimeSeriesGranularity.MINUTE,
                    TimeSeriesGranularity.HOURLY
                )
    
    def _maybe_generate_trap(self, movement_pct: float, timestamp: str):
        """
        Maybe generate a trap event based on trap frequency and market conditions.
        
        This method determines if a trap should be generated in the current
        iteration. The probability is affected by the base trap frequency,
        current market regime, and randomness. If a trap is generated, its
        type and confidence are determined based on weighted selection and
        price movement characteristics.
        
        Args:
            movement_pct: Percentage price movement for this iteration
            timestamp: Current timestamp string
        """
        # Adjust trap probability based on market regime
        regime_boost = 2.0 if "High Volatility" in self.current_regime[0] else 1.0
        trap_prob = self.trap_frequency * regime_boost
        
        # Generate trap based on probability
        if np.random.random() < trap_prob:
            # Choose trap type based on weights
            trap_type = self._weighted_choice(self.trap_types)
            
            # Calculate confidence based on trap type and price movement
            confidence = 0.6 + (np.random.random() * 0.35)  # Between 0.6-0.95
            
            # Make larger price movements more confident
            confidence = min(0.95, confidence + (abs(movement_pct) * 5))
            
            # Register the trap
            self.trap_count += 1
            
            # Store trap event for internal tracking
            trap_data = {
                "timestamp": timestamp,
                "trap_type": trap_type,
                "confidence": confidence,
                "price": self.price,
                "price_change_pct": movement_pct * 100,
                "market_regime": self.current_regime[0]
            }
            self.trap_history.append(trap_data)
            
            # Store trap event using time series storage
            store_time_series_data("trap_history", trap_data, datetime.datetime.now(datetime.UTC))
            
            # Log the trap
            print(f"\n{RED}{BOLD} 🚨 SIMULATED TRAP DETECTED #{self.trap_count} {RESET}")
            print(f"{RED}Type: {trap_type}{RESET}")
            print(f"{RED}Confidence: {confidence:.2f}{RESET}")
            print(f"{RED}Price Movement: {movement_pct*100:+.3f}%{RESET}")
            
            # Check for high-frequency mode activation (multiple traps in short window)
            self._check_hf_mode(trap_data)
    
    def _check_hf_mode(self, trap_data: Dict[str, Any]):
        """
        Check if high-frequency mode should be activated.
        
        High-frequency mode activates when multiple trap events are detected within
        a short time window (default: 3 minutes). When activated, the system becomes
        more sensitive to potential trap events by reducing volatility thresholds.
        
        This simulates real-world behavior where market maker activity often
        intensifies during short periods, creating multiple trap events in sequence.
        
        Args:
            trap_data: Dictionary containing details about the current trap
        """
        # Count traps in the last 3 minutes
        current_time = datetime.datetime.now(datetime.UTC)
        window_start = current_time - datetime.timedelta(minutes=3)
        
        # Get recent traps using time series storage
        recent_traps = get_time_series_data(
            "trap_history",
            current_time.date(),
            TimeSeriesGranularity.MINUTE
        )
        
        # Filter traps within the window
        recent_traps = [
            trap for trap in recent_traps
            if datetime.datetime.strptime(trap["timestamp"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.UTC) > window_start
        ]
        
        # Check for HF mode activation - need at least 2 traps in window
        if len(recent_traps) >= 2:
            self.hf_activations += 1
            
            # Calculate volatility multiplier based on trap frequency
            multiplier = max(0.5, 1.0 - (len(recent_traps) * 0.1))
            
            print(f"\n{MAGENTA}{BOLD} 🔥 HF MODE ACTIVATED #{self.hf_activations} {RESET}")
            print(f"{MAGENTA}Recent traps: {len(recent_traps)}{RESET}")
            print(f"{MAGENTA}Multiplier: {multiplier:.2f}x{RESET}")
            
            # Store HF mode activation event using time series storage
            activation_data = {
                "timestamp": trap_data["timestamp"],
                "multiplier": multiplier,
                "price": trap_data["price"],
                "market_regime": trap_data["market_regime"],
                "traps_in_window": len(recent_traps),
                "trap_types": [t["trap_type"] for t in recent_traps]
            }
            store_time_series_data("hf_activations", activation_data, current_time)
            
            # Store current HF mode state in Redis
            redis_conn.set("sim_hf_mode_active", "1")
            redis_conn.set("sim_hf_mode_multiplier", multiplier)
            redis_conn.set("sim_hf_mode_timestamp", datetime.datetime.now(datetime.UTC).isoformat())
            
            # Expire HF mode after 10 minutes
            redis_conn.expire("sim_hf_mode_active", 600)
    
    def _report_statistics(self):
        """Report simulation statistics."""
        elapsed_minutes = (datetime.datetime.now(datetime.UTC) - self.start_time).total_seconds() / 60
        
        print(f"\n{YELLOW}{BOLD} 📊 SIMULATION STATS {RESET}")
        print(f"{YELLOW}Run time: {elapsed_minutes:.1f} minutes{RESET}")
        print(f"{YELLOW}Iterations: {self.iteration}{RESET}")
        print(f"{YELLOW}Traps detected: {self.trap_count} ({self.trap_count/self.iteration*100:.2f}%){RESET}")
        print(f"{YELLOW}HF mode activations: {self.hf_activations}{RESET}")
        print(f"{YELLOW}Current price: ${self.price:.2f}{RESET}")
        print(f"{YELLOW}{'═' * 50}{RESET}")
        
        # Store stats in Redis
        redis_conn.hmset("sim_statistics", {
            "iterations": str(self.iteration),
            "traps_detected": str(self.trap_count),
            "hf_activations": str(self.hf_activations),
            "run_time_minutes": str(elapsed_minutes),
            "current_price": str(self.price),
            "start_price": str(redis_conn.get("sim_last_btc_price")),
            "market_regime": self.current_regime[0]
        })
    
    def _save_final_statistics(self):
        """Save final simulation statistics."""
        elapsed_minutes = (datetime.datetime.now(datetime.UTC) - self.start_time).total_seconds() / 60
        
        # Store final simulation summary
        redis_conn.hmset("sim_statistics", {
            "iterations": str(self.iteration),
            "traps_detected": str(self.trap_count), 
            "hf_activations": str(self.hf_activations),
            "run_time_minutes": str(elapsed_minutes),
            "current_price": str(self.price),
            "start_price": str(redis_conn.get("sim_last_btc_price")),
            "market_regime": self.current_regime[0],
            "completed": "stopped"
        })
        redis_conn.set("sim_running", "0")
        
        print(f"\n{BLUE}{BOLD} 📊 FINAL SIMULATION RESULTS {RESET}")
        print(f"{GREEN}Run time: {elapsed_minutes:.1f} minutes{RESET}")
        print(f"{GREEN}Iterations: {self.iteration}{RESET}")
        print(f"{GREEN}Traps detected: {self.trap_count} ({self.trap_count/self.iteration*100:.2f}%){RESET}")
        print(f"{GREEN}HF mode activations: {self.hf_activations}{RESET}")
        print(f"{GREEN}Final price: ${self.price:.2f}{RESET}")
        print(f"{GREEN}Trap frequency: {self.trap_count/self.iteration:.4f} (per iteration){RESET}")
        print(f"{GREEN}HF activation frequency: {self.hf_activations/self.iteration:.4f} (per iteration){RESET}")
    
    def _weighted_choice(self, choices):
        """
        Make a weighted random choice from a list of (item, weight) tuples.
        
        This implements a weighted random selection algorithm where the probability
        of selecting an item is proportional to its weight. This allows for more
        realistic simulation of trap types, with some types (like liquidity grabs)
        being more common than others (like Fibonacci traps).
        
        Args:
            choices: List of (item, weight) tuples
            
        Returns:
            Selected item based on weighted probability
        """
        total = sum(weight for _, weight in choices)
        r = np.random.random() * total
        
        running_sum = 0
        for item, weight in choices:
            running_sum += weight
            if r <= running_sum:
                return item
        
        return choices[0][0]  # Fallback to first item

def main():
    """Run the trap simulation service with command line arguments."""
    parser = argparse.ArgumentParser(description="Market Maker Trap Simulation Service")
    parser.add_argument(
        "--duration", 
        type=float, 
        help="Duration in hours (default: indefinite)",
        default=None
    )
    parser.add_argument(
        "--volatility", 
        type=float, 
        help="Volatility scale (default: 1.0)",
        default=1.0
    )
    parser.add_argument(
        "--frequency", 
        type=float, 
        help="Trap frequency 0.0-1.0 (default: 0.2)",
        default=0.2
    )
    parser.add_argument(
        "--sleep", 
        type=float, 
        help="Sleep interval in seconds (default: 0.1)",
        default=0.1
    )
    
    args = parser.parse_args()
    
    try:
        # Create and run simulator
        simulator = TrapSimulator(
            volatility_scale=args.volatility,
            trap_frequency=args.frequency,
            sleep_interval=args.sleep
        )
        
        simulator.run(duration_hours=args.duration)
        return 0
        
    except Exception as e:
        print(f"\n{RED}Error in simulation: {e}{RESET}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 