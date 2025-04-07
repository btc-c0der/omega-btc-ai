#!/usr/bin/env python3
"""
BTC Velocity Monitor - Real-time BTC monitoring using Redis data

This module provides real-time monitoring and analysis of Bitcoin price movements,
velocity, and market dynamics using data from the remote Redis database.
"""

import os
import sys
import time
import json
import math
import logging
import datetime
import statistics
from typing import List, Dict, Any, Optional, Tuple, Union

import redis
import numpy as np
import pandas as pd
from dateutil.parser import parse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("btc_velocity_monitor")

# Redis connection details
REDIS_HOST = "omega-btc-ai-redis-do-user-20389918-0.d.db.ondigitalocean.com"
REDIS_PORT = 25061
REDIS_USERNAME = "default"
REDIS_PASSWORD = "AVNS_OXMpU0P0ByYEz337Fgi"
REDIS_SSL = True

# ANSI color codes for terminal output
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
RESET = Style.RESET_ALL
BOLD = Style.BRIGHT

class RedisClient:
    """Redis client for connecting to the remote database"""
    
    def __init__(self):
        """Initialize Redis client with remote connection details"""
        self.redis_client = None
        self.connected = False
        
        self.connect()
        
    def connect(self) -> bool:
        """Connect to Redis server"""
        try:
            self.redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                username=REDIS_USERNAME,
                password=REDIS_PASSWORD,
                ssl=REDIS_SSL,
                socket_connect_timeout=5.0,
                decode_responses=False  # Keep raw bytes for proper handling
            )
            
            # Test connection
            self.redis_client.ping()
            self.connected = True
            logger.info(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.connected = False
            return False
    
    def get_all_keys(self) -> List[str]:
        """Get all keys from Redis database"""
        if not self.connected:
            logger.warning("Not connected to Redis")
            return []
        
        try:
            keys = self.redis_client.keys("*")
            return [k.decode() for k in keys]
        except Exception as e:
            logger.error(f"Error getting keys: {e}")
            return []
    
    def get_btc_keys(self) -> List[str]:
        """Get all BTC-related keys from Redis database"""
        if not self.connected:
            logger.warning("Not connected to Redis")
            return []
        
        try:
            # Get keys with common BTC prefixes/suffixes
            btc_keys = []
            for pattern in ["*btc*", "*bitcoin*", "*price*", "*swing*", "*fibonacci*", 
                           "*velocity*", "*volatility*", "*trap*", "*volume*"]:
                keys = self.redis_client.keys(pattern)
                btc_keys.extend([k.decode() for k in keys])
            
            # Remove duplicates
            return list(set(btc_keys))
        except Exception as e:
            logger.error(f"Error getting BTC keys: {e}")
            return []
    
    def get_key_info(self, key: str) -> Dict[str, Any]:
        """Get information about a Redis key"""
        if not self.connected:
            logger.warning("Not connected to Redis")
            return {}
        
        try:
            # Get key type
            key_type = self.redis_client.type(key).decode()
            
            # Get key value based on type
            value = None
            if key_type == "string":
                value = self.redis_client.get(key)
                try:
                    # Try to decode as string
                    value = value.decode()
                    
                    # Try to parse as JSON
                    try:
                        value = json.loads(value)
                    except:
                        pass
                except:
                    value = str(value)
            elif key_type == "list":
                list_length = self.redis_client.llen(key)
                sample = []
                if list_length > 0:
                    # Get the last few items (most recent)
                    items = self.redis_client.lrange(key, -3, -1)
                    for item in items:
                        try:
                            decoded = item.decode()
                            try:
                                sample.append(json.loads(decoded))
                            except:
                                sample.append(decoded)
                        except:
                            sample.append(str(item))
                value = {
                    "length": list_length,
                    "sample": sample
                }
            elif key_type == "hash":
                value = {k.decode(): v.decode() for k, v in self.redis_client.hgetall(key).items()}
                
            # Get TTL
            ttl = self.redis_client.ttl(key)
            
            return {
                "key": key,
                "type": key_type,
                "ttl": ttl,
                "value": value
            }
        except Exception as e:
            logger.error(f"Error getting info for key {key}: {e}")
            return {"key": key, "error": str(e)}

class BTCDataAnalyzer:
    """Analyze BTC data from Redis database"""
    
    def __init__(self, redis_client: RedisClient):
        """Initialize BTC data analyzer"""
        self.redis_client = redis_client
        self.btc_data = {}
        self.price_history = []
        self.velocity_history = []
        self.fibonacci_levels = {}
        
    def load_data(self) -> bool:
        """Load BTC data from Redis"""
        if not self.redis_client.connected:
            logger.warning("Redis client not connected")
            return False
        
        try:
            # Get all BTC-related keys
            btc_keys = self.redis_client.get_btc_keys()
            logger.info(f"Found {len(btc_keys)} BTC-related keys in Redis")
            
            # Get data for each key
            data = {}
            for key in btc_keys:
                data[key] = self.redis_client.get_key_info(key)
            
            self.btc_data = data
            
            # Extract price history data
            self._extract_price_history()
            
            return True
        except Exception as e:
            logger.error(f"Error loading BTC data: {e}")
            return False
    
    def _extract_price_history(self):
        """Extract price history data from Redis data"""
        # Check if btc_movement_history exists
        if "btc_movement_history" in self.btc_data:
            data = self.btc_data["btc_movement_history"]
            if data["type"] == "list" and data["value"]["sample"]:
                # Get full history
                try:
                    raw_items = self.redis_client.redis_client.lrange("btc_movement_history", 0, -1)
                    items = []
                    for item in raw_items:
                        try:
                            items.append(json.loads(item.decode()))
                        except:
                            pass
                    
                    # Sort by timestamp
                    self.price_history = sorted(items, key=lambda x: x.get("timestamp", ""))
                    logger.info(f"Extracted {len(self.price_history)} price history entries")
                except Exception as e:
                    logger.error(f"Error extracting price history: {e}")
        
        # Get current price
        if "last_btc_price" in self.btc_data:
            data = self.btc_data["last_btc_price"]
            if data["type"] == "string" and data["value"]:
                try:
                    self.current_price = float(data["value"])
                    logger.info(f"Current BTC price: {self.current_price}")
                except:
                    self.current_price = None
        
        # Get Fibonacci levels if available
        if "fibonacci_levels" in self.btc_data:
            data = self.btc_data["fibonacci_levels"]
            if data["type"] == "string" and data["value"]:
                try:
                    self.fibonacci_levels = json.loads(data["value"])
                except:
                    pass
    
    def calculate_velocity(self, timeframe_minutes: int = 5) -> Dict[str, Any]:
        """Calculate BTC velocity metrics"""
        if not self.price_history:
            logger.warning("No price history data available")
            return {}
        
        try:
            # Convert to pandas DataFrame
            df = pd.DataFrame(self.price_history)
            
            # Convert timestamp to datetime
            df["datetime"] = df["timestamp"].apply(lambda x: parse(x) if isinstance(x, str) else datetime.datetime.fromtimestamp(x))
            
            # Sort by datetime
            df = df.sort_values("datetime")
            
            # Calculate time difference in seconds
            df["time_diff"] = df["datetime"].diff().dt.total_seconds()
            
            # Calculate price difference
            df["price_diff"] = df["price"].diff()
            
            # Calculate velocity (price change per second)
            df["velocity"] = df["price_diff"] / df["time_diff"]
            
            # Calculate acceleration (change in velocity)
            df["acceleration"] = df["velocity"].diff() / df["time_diff"]
            
            # Filter out NaN values
            df = df.dropna()
            
            # Get recent data (last n minutes)
            now = datetime.datetime.now(datetime.timezone.utc)
            cutoff = now - datetime.timedelta(minutes=timeframe_minutes)
            recent_df = df[df["datetime"] > cutoff]
            
            # Calculate velocity statistics
            if len(recent_df) > 0:
                avg_velocity = recent_df["velocity"].mean()
                max_velocity = recent_df["velocity"].max()
                min_velocity = recent_df["velocity"].min()
                velocity_std = recent_df["velocity"].std()
                
                avg_acceleration = recent_df["acceleration"].mean()
                max_acceleration = recent_df["acceleration"].max()
                min_acceleration = recent_df["acceleration"].min()
                
                # Calculate price direction and momentum
                price_direction = "up" if avg_velocity > 0 else "down"
                momentum = abs(avg_velocity) * (len(recent_df) ** 0.5)
                
                # Keep history of velocity
                self.velocity_history.append({
                    "timestamp": now.isoformat(),
                    "avg_velocity": avg_velocity,
                    "momentum": momentum,
                    "direction": price_direction
                })
                
                # Limit history size
                if len(self.velocity_history) > 100:
                    self.velocity_history = self.velocity_history[-100:]
                
                return {
                    "time_period_minutes": timeframe_minutes,
                    "data_points": len(recent_df),
                    "avg_velocity": avg_velocity,
                    "max_velocity": max_velocity,
                    "min_velocity": min_velocity,
                    "velocity_std": velocity_std,
                    "avg_acceleration": avg_acceleration,
                    "max_acceleration": max_acceleration,
                    "min_acceleration": min_acceleration,
                    "price_direction": price_direction,
                    "momentum": momentum,
                    "current_price": self.current_price
                }
            else:
                logger.warning(f"No recent data within the last {timeframe_minutes} minutes")
                return {}
        except Exception as e:
            logger.error(f"Error calculating velocity: {e}")
            return {}
    
    def detect_price_anomalies(self, velocity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect price anomalies based on velocity data"""
        if not velocity_data:
            return {}
        
        try:
            # Check for extreme velocity
            extreme_velocity = abs(velocity_data["avg_velocity"]) > 0.05  # More than 5 cents per second
            
            # Check for rapid acceleration
            rapid_acceleration = abs(velocity_data["avg_acceleration"]) > 0.005  # More than 0.5 cents per second²
            
            # Check for momentum shift
            momentum_shift = False
            if len(self.velocity_history) >= 2:
                current_direction = self.velocity_history[-1]["direction"]
                previous_direction = self.velocity_history[-2]["direction"]
                momentum_shift = current_direction != previous_direction
            
            # Determine anomaly level
            anomaly_level = 0
            if extreme_velocity:
                anomaly_level += 1
            if rapid_acceleration:
                anomaly_level += 1
            if momentum_shift:
                anomaly_level += 1
            
            return {
                "extreme_velocity": extreme_velocity,
                "rapid_acceleration": rapid_acceleration,
                "momentum_shift": momentum_shift,
                "anomaly_level": anomaly_level
            }
        except Exception as e:
            logger.error(f"Error detecting price anomalies: {e}")
            return {}

class BTCVelocityMonitor:
    """Main module for monitoring BTC velocity"""
    
    def __init__(self):
        """Initialize BTC velocity monitor"""
        self.redis_client = RedisClient()
        self.analyzer = BTCDataAnalyzer(self.redis_client)
        
    def initialize(self) -> bool:
        """Initialize the monitoring system"""
        # Connect to Redis
        if not self.redis_client.connected:
            print(f"{RED}Failed to connect to Redis.{RESET}")
            print(f"{YELLOW}Please check your network connection and try again.{RESET}")
            return False
        
        # Load data
        print(f"{CYAN}Loading BTC data from Redis...{RESET}")
        success = self.analyzer.load_data()
        if not success:
            print(f"{RED}Failed to load BTC data.{RESET}")
            return False
        
        print(f"{GREEN}BTC Velocity Monitor initialized successfully.{RESET}")
        return True
    
    def display_redis_keys(self) -> None:
        """Display all BTC-related Redis keys"""
        keys = self.redis_client.get_btc_keys()
        
        if not keys:
            print(f"{YELLOW}No BTC-related keys found in Redis.{RESET}")
            return
        
        print(f"\n{CYAN}{BOLD}BTC-Related Redis Keys:{RESET}")
        for i, key in enumerate(sorted(keys), 1):
            # Get key type
            key_info = self.redis_client.get_key_info(key)
            key_type = key_info.get("type", "unknown")
            
            # Format based on type
            if key_type == "string":
                type_color = BLUE
            elif key_type == "list":
                type_color = GREEN
            elif key_type == "hash":
                type_color = MAGENTA
            else:
                type_color = YELLOW
                
            print(f"  {i:2d}. {CYAN}{key}{RESET} ({type_color}{key_type}{RESET})")
    
    def monitor_velocity(self, refresh_interval: int = 5) -> None:
        """Monitor BTC velocity in real-time"""
        try:
            while True:
                # Clear the screen
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # Reload data
                self.analyzer.load_data()
                
                # Calculate velocity metrics
                velocity_1min = self.analyzer.calculate_velocity(timeframe_minutes=1)
                velocity_5min = self.analyzer.calculate_velocity(timeframe_minutes=5)
                velocity_15min = self.analyzer.calculate_velocity(timeframe_minutes=15)
                
                # Detect anomalies
                anomalies = self.analyzer.detect_price_anomalies(velocity_5min)
                
                # Display header
                print(f"\n{CYAN}{BOLD}======== BTC VELOCITY MONITOR ========{RESET}")
                print(f"{YELLOW}Current Price: ${self.analyzer.current_price:.2f}{RESET}")
                print(f"{CYAN}Last Update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
                print(f"{CYAN}{'=' * 38}{RESET}\n")
                
                # Display velocity metrics
                self._display_velocity_metrics("1-MINUTE VELOCITY", velocity_1min)
                self._display_velocity_metrics("5-MINUTE VELOCITY", velocity_5min)
                self._display_velocity_metrics("15-MINUTE VELOCITY", velocity_15min)
                
                # Display anomalies
                self._display_anomalies(anomalies)
                
                # Wait for next update
                print(f"\n{CYAN}Refreshing in {refresh_interval} seconds... (Press Ctrl+C to exit){RESET}")
                time.sleep(refresh_interval)
        
        except KeyboardInterrupt:
            print(f"\n{GREEN}BTC Velocity Monitor stopped.{RESET}")
    
    def _display_velocity_metrics(self, title: str, metrics: Dict[str, Any]) -> None:
        """Display velocity metrics in a formatted way"""
        if not metrics:
            print(f"{YELLOW}{title}: No data available{RESET}")
            return
        
        # Determine direction color
        direction = metrics.get("price_direction", "")
        if direction == "up":
            direction_color = GREEN
            direction_symbol = "↗"
        else:
            direction_color = RED
            direction_symbol = "↘"
        
        # Format velocity (price change per second)
        avg_velocity = metrics.get("avg_velocity", 0)
        velocity_formatted = f"{abs(avg_velocity):.6f} $/sec"
        
        # Format momentum (strength of movement)
        momentum = metrics.get("momentum", 0)
        momentum_formatted = f"{momentum:.4f}"
        
        # Display section
        print(f"{BOLD}{CYAN}{title}{RESET}")
        print(f"  Direction: {direction_color}{direction} {direction_symbol}{RESET}")
        print(f"  Velocity: {direction_color}{velocity_formatted}{RESET}")
        print(f"  Momentum: {direction_color}{momentum_formatted}{RESET}")
        print(f"  Acceleration: {YELLOW}{metrics.get('avg_acceleration', 0):.8f} $/sec²{RESET}")
        print(f"  Data Points: {metrics.get('data_points', 0)}")
        print()
    
    def _display_anomalies(self, anomalies: Dict[str, Any]) -> None:
        """Display price anomalies"""
        if not anomalies:
            print(f"{YELLOW}Anomaly Detection: No data available{RESET}")
            return
        
        # Get anomaly level
        anomaly_level = anomalies.get("anomaly_level", 0)
        
        # Determine color based on anomaly level
        if anomaly_level == 0:
            level_color = GREEN
            level_text = "NORMAL"
        elif anomaly_level == 1:
            level_color = YELLOW
            level_text = "MILD"
        elif anomaly_level == 2:
            level_color = MAGENTA
            level_text = "MODERATE"
        else:
            level_color = RED
            level_text = "SEVERE"
        
        # Display section
        print(f"{BOLD}{CYAN}ANOMALY DETECTION{RESET}")
        print(f"  Status: {level_color}{level_text}{RESET}")
        
        # Display individual anomalies
        if anomalies.get("extreme_velocity", False):
            print(f"  {RED}• Extreme Velocity Detected{RESET}")
        
        if anomalies.get("rapid_acceleration", False):
            print(f"  {RED}• Rapid Acceleration Detected{RESET}")
        
        if anomalies.get("momentum_shift", False):
            print(f"  {MAGENTA}• Momentum Shift Detected{RESET}")
        
        if anomaly_level == 0:
            print(f"  {GREEN}• Normal Market Activity{RESET}")
        
        print()


def run_btc_velocity_monitor():
    """Run the BTC velocity monitor"""
    print(f"{CYAN}{BOLD}Starting BTC Velocity Monitor...{RESET}")
    
    # Initialize monitor
    monitor = BTCVelocityMonitor()
    if not monitor.initialize():
        print(f"{RED}Failed to initialize BTC Velocity Monitor.{RESET}")
        return
    
    # Display Redis keys
    monitor.display_redis_keys()
    
    # Monitor velocity
    print(f"\n{CYAN}Starting real-time monitoring...{RESET}")
    monitor.monitor_velocity()


if __name__ == "__main__":
    run_btc_velocity_monitor() 