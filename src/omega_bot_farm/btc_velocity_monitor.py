#!/usr/bin/env python3
"""
BTC Velocity Monitor - Real-time BTC monitoring using Redis data

This module provides real-time monitoring and analysis of Bitcoin price movements,
velocity, and market dynamics using data from the remote Redis database.

"THE GRID" — "FOR BTC VELOCITY" — "c/o OFF—WHITE™"
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
WHITE = Fore.WHITE

# VIRGIL ABLOH DESIGN CONSTANTS
VIRGIL_BORDER = f"{CYAN}{'=' * 60}{RESET}"
VIRGIL_SEPARATOR = f"{CYAN}{'─' * 60}{RESET}"
VIRGIL_QUOTE = lambda text, category="": f"{CYAN}\"{text.upper()}\"   \"{category}\"{RESET}"

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
                           "*velocity*", "*volatility*", "*trap*", "*volume*", "*aixbt*", "*correlation*"]:
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
        self.aixbt_data = {}
        self.aixbt_correlation = None
        self.aixbt_price = 0.0
        
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
            
            # Extract AIXBT correlation data
            self._extract_aixbt_data()
            
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
    
    def _extract_aixbt_data(self):
        """Extract AIXBT data and correlation metrics from Redis"""
        try:
            # Get AIXBT price
            if "last_aixbt_price" in self.btc_data:
                data = self.btc_data["last_aixbt_price"]
                if data["type"] == "string" and data["value"]:
                    try:
                        self.aixbt_price = float(data["value"])
                        logger.info(f"Current AIXBT price: {self.aixbt_price}")
                    except:
                        self.aixbt_price = None
            
            # Get correlation data
            if "aixbt_btc_correlation" in self.btc_data:
                data = self.btc_data["aixbt_btc_correlation"]
                if data["type"] == "string" and data["value"]:
                    try:
                        if isinstance(data["value"], dict):
                            self.aixbt_correlation = data["value"]
                        else:
                            self.aixbt_correlation = json.loads(data["value"])
                        logger.info(f"Loaded AIXBT-BTC correlation: {self.aixbt_correlation.get('correlation', 'N/A')}")
                    except Exception as e:
                        logger.error(f"Error parsing AIXBT correlation: {e}")
                        self.aixbt_correlation = None
        
        except Exception as e:
            logger.error(f"Error extracting AIXBT data: {e}")
    
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
    
    def calculate_aixbt_coefficient(self) -> Dict[str, Any]:
        """Calculate the coefficient between AIXBT and BTC price movements"""
        if not self.aixbt_correlation:
            return {
                "correlation": None,
                "correlation_strength": "UNKNOWN",
                "aixbt_price": self.aixbt_price,
                "btc_price": self.current_price
            }
        
        try:
            correlation = self.aixbt_correlation.get('correlation', 0)
            
            # Determine correlation strength
            if abs(correlation) > 0.7:
                strength = "STRONG"
            elif abs(correlation) > 0.3:
                strength = "MODERATE"
            else:
                strength = "WEAK"
            
            # Determine correlation type
            if correlation > 0:
                correlation_type = "POSITIVE"
            elif correlation < 0:
                correlation_type = "NEGATIVE"
            else:
                correlation_type = "NEUTRAL"
            
            # Get timestamp of correlation measurement
            timestamp = self.aixbt_correlation.get('timestamp', 'N/A')
            
            return {
                "correlation": correlation,
                "correlation_strength": strength,
                "correlation_type": correlation_type,
                "aixbt_price": self.aixbt_price,
                "btc_price": self.current_price,
                "timestamp": timestamp
            }
        except Exception as e:
            logger.error(f"Error calculating AIXBT coefficient: {e}")
            return {
                "correlation": None,
                "correlation_strength": "ERROR",
                "aixbt_price": self.aixbt_price,
                "btc_price": self.current_price
            }

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
            print(f"\n{VIRGIL_QUOTE('NO BTC-RELATED KEYS FOUND IN REDIS', 'DATABASE EMPTY')}")
            return
        
        print(f"\n{VIRGIL_QUOTE('BTC-RELATED REDIS KEYS', 'DATABASE LAYER')}")
        print(VIRGIL_SEPARATOR)
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
                
            print(f"  {i:2d}. {CYAN}\"{key}\"{RESET} {type_color}(\"{key_type}\"){RESET}")
        print(VIRGIL_SEPARATOR)
    
    def monitor_velocity(self, refresh_interval: int = 5) -> None:
        """Monitor BTC velocity in real-time with Virgil Abloh Matrix theme"""
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
                
                # Calculate AIXBT coefficient
                aixbt_coefficient = self.analyzer.calculate_aixbt_coefficient()
                
                # Detect anomalies
                anomalies = self.analyzer.detect_price_anomalies(velocity_5min)
                
                # Calculate uptime
                now = datetime.datetime.now()
                uptime_str = now.strftime("%d-%m-%Y %H:%M:%S")
                
                # Display Virgil Abloh Matrix-themed header
                print(VIRGIL_BORDER)
                print(f"{MAGENTA}{BOLD}\"BTC VELOCITY MONITOR\"   \"MATRIX EDITION\"{RESET}")
                print(VIRGIL_BORDER)
                print(f"{YELLOW}\"TIMESTAMP: {uptime_str}\"   \"QUANTUM LAYER\"{RESET}")
                
                # Display current prices section
                print(VIRGIL_SEPARATOR)
                print(f"{YELLOW}\"MARKET PRICES\"   \"REAL-TIME DATA\"{RESET}")
                print(f"  {CYAN}\"BTC:\" ${self.analyzer.current_price:.2f}{RESET}")
                if self.analyzer.aixbt_price:
                    print(f"  {CYAN}\"AIXBT:\" ${self.analyzer.aixbt_price:.8f}{RESET}")
                print(VIRGIL_SEPARATOR)
                
                # Display velocity metrics
                self._display_velocity_metrics("1-MINUTE VELOCITY", velocity_1min)
                self._display_velocity_metrics("5-MINUTE VELOCITY", velocity_5min)
                self._display_velocity_metrics("15-MINUTE VELOCITY", velocity_15min)
                
                # Display anomalies
                self._display_anomalies(anomalies)
                
                # Display AIXBT correlation if available
                if aixbt_coefficient["correlation"] is not None:
                    self._display_aixbt_correlation(aixbt_coefficient)
                
                # Display Virgil Abloh-inspired footer
                print(VIRGIL_BORDER)
                print(f"{MAGENTA}\"THE GRID\"   \"FOR BTC VELOCITY\"   \"c/o OFF—WHITE™\"{RESET}")
                print(f"{YELLOW}\"TIME: {now.strftime('%H:%M:%S')}\"   \"MADE IN DIGITAL SPACE\"   \"PROTOTYPE-003\"{RESET}")
                
                # Wait for next update
                print(f"\n{CYAN}\"REFRESHING IN {refresh_interval} SECONDS...\"   \"PRESS CTRL+C TO EXIT\"{RESET}")
                time.sleep(refresh_interval)
        
        except KeyboardInterrupt:
            print(f"\n{GREEN}\"BTC VELOCITY MONITOR STOPPED\"   \"USER COMMAND\"{RESET}")
    
    def _display_velocity_metrics(self, title: str, metrics: Dict[str, Any]) -> None:
        """Display velocity metrics in a Virgil Abloh Matrix theme"""
        if not metrics:
            print(f"{YELLOW}\"{title}: NO DATA AVAILABLE\"   \"WAITING FOR DATA\"{RESET}")
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
        print(f"{CYAN}\"{title}\"   \"TIME DIMENSION\"{RESET}")
        print(f"  {YELLOW}\"DIRECTION:\"{RESET} {direction_color}\"{direction.upper()} {direction_symbol}\"{RESET}")
        print(f"  {YELLOW}\"VELOCITY:\"{RESET} {direction_color}\"{velocity_formatted}\"{RESET}")
        print(f"  {YELLOW}\"MOMENTUM:\"{RESET} {direction_color}\"{momentum_formatted}\"{RESET}")
        print(f"  {YELLOW}\"ACCELERATION:\"{RESET} {MAGENTA}\"{metrics.get('avg_acceleration', 0):.8f} $/sec²\"{RESET}")
        print(f"  {YELLOW}\"DATA POINTS:\"{RESET} {BLUE}\"{metrics.get('data_points', 0)}\"{RESET}")
        print(VIRGIL_SEPARATOR)
    
    def _display_anomalies(self, anomalies: Dict[str, Any]) -> None:
        """Display price anomalies in Virgil Abloh Matrix theme"""
        if not anomalies:
            print(f"{YELLOW}\"ANOMALY DETECTION: NO DATA AVAILABLE\"   \"WAITING FOR DATA\"{RESET}")
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
        print(f"{CYAN}\"ANOMALY DETECTION\"   \"PATTERN RECOGNITION\"{RESET}")
        print(f"  {YELLOW}\"STATUS:\"{RESET} {level_color}\"{level_text}\"{RESET}")
        
        # Display individual anomalies
        if anomalies.get("extreme_velocity", False):
            print(f"  {RED}• \"EXTREME VELOCITY DETECTED\"   \"PRICE CHANGE RATE\"{RESET}")
        
        if anomalies.get("rapid_acceleration", False):
            print(f"  {RED}• \"RAPID ACCELERATION DETECTED\"   \"VELOCITY CHANGE\"{RESET}")
        
        if anomalies.get("momentum_shift", False):
            print(f"  {MAGENTA}• \"MOMENTUM SHIFT DETECTED\"   \"DIRECTION CHANGE\"{RESET}")
        
        if anomaly_level == 0:
            print(f"  {GREEN}• \"NORMAL MARKET ACTIVITY\"   \"STABILITY CONFIRMED\"{RESET}")
        
        print(VIRGIL_SEPARATOR)
    
    def _display_aixbt_correlation(self, correlation_data: Dict[str, Any]) -> None:
        """Display AIXBT-BTC correlation data in Virgil Abloh Matrix theme"""
        correlation = correlation_data.get("correlation", 0)
        strength = correlation_data.get("correlation_strength", "UNKNOWN")
        corr_type = correlation_data.get("correlation_type", "UNKNOWN")
        
        # Determine color based on correlation strength
        if strength == "STRONG":
            strength_color = GREEN if corr_type == "POSITIVE" else RED
        elif strength == "MODERATE":
            strength_color = YELLOW
        else:
            strength_color = BLUE
        
        # Display section
        print(f"{CYAN}\"AIXBT-BTC CORRELATION\"   \"TOKEN RELATIONSHIP\"{RESET}")
        print(f"  {YELLOW}\"COEFFICIENT:\"{RESET} {strength_color}\"{correlation:.4f}\"{RESET}")
        print(f"  {YELLOW}\"STRENGTH:\"{RESET} {strength_color}\"{strength}\"{RESET}")
        print(f"  {YELLOW}\"TYPE:\"{RESET} {strength_color}\"{corr_type}\"{RESET}")
        
        # Display price comparison
        aixbt_price = correlation_data.get("aixbt_price", 0)
        btc_price = correlation_data.get("btc_price", 0)
        
        if aixbt_price and btc_price:
            # Calculate relative price (AIXBT/BTC)
            relative_price = (aixbt_price / btc_price) * 100000000  # Convert to satoshis
            print(f"  {YELLOW}\"AIXBT/BTC RATIO:\"{RESET} {CYAN}\"{relative_price:.8f} SATS\"{RESET}")
        
        print(VIRGIL_SEPARATOR)


def run_btc_velocity_monitor():
    """Run the BTC velocity monitor with Virgil Abloh Matrix theme"""
    # Clear the screen for dramatic effect
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Display Virgil Abloh-style intro
    print(VIRGIL_BORDER)
    print(f"{MAGENTA}{BOLD}\"BTC VELOCITY MONITOR\"   \"MATRIX EDITION\"{RESET}")
    print(f"{CYAN}\"POWERED BY OFF—WHITE™ FOR BLOCKCHAIN\"   \"VIRGIL ABLOH 2025\"{RESET}")
    print(VIRGIL_BORDER)
    
    # Initialize monitor
    monitor = BTCVelocityMonitor()
    if not monitor.initialize():
        print(f"{RED}\"FAILED TO INITIALIZE BTC VELOCITY MONITOR\"   \"CONNECTION ERROR\"{RESET}")
        return
    
    # Display Redis keys
    monitor.display_redis_keys()
    
    # Display launch message
    print(f"\n{CYAN}\"STARTING REAL-TIME MONITORING...\"   \"MATRIX INTERFACE ACTIVE\"{RESET}")
    print(f"{YELLOW}\"VIRGIL ABLOH MATRIX THEME ENABLED\"   \"DESIGN MODE\"{RESET}")
    
    # Monitor velocity
    monitor.monitor_velocity()


if __name__ == "__main__":
    run_btc_velocity_monitor() 