
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

import redis
import requests
import pandas as pd
import datetime
import time
import threading
import os
from pathlib import Path
import json

# ✅ Constants
UPDATE_INTERVAL = 60  # Fetch Schumann data every 60 seconds
HEARTMATH_API_URL = "https://nocc.heartmath.org/power_levels/public/charts/power_levels.php"
SCHUMANN_CSV_PATH = "data/schumann_history.csv"
SCHUMANN_CACHE_SIZE = 1000  # Keep last 1000 readings in Redis

# ✅ Redis connection
redis_conn = redis.Redis(host="localhost", port=6379, db=0)

# ✅ Terminal colors
BLUE = "\033[94m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

class SchumannResonanceMonitor:
    """Real-time Schumann Resonance monitoring service."""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.last_timestamp = None
        self.history_df = None
        self.load_history()
    
    def load_history(self):
        """Load historical Schumann data if available."""
        try:
            path = Path(SCHUMANN_CSV_PATH)
            if path.exists():
                self.history_df = pd.read_csv(path)
                self.history_df['Timestamp'] = pd.to_datetime(self.history_df['Timestamp'])
                last_row = self.history_df.iloc[-1]
                self.last_timestamp = last_row['Timestamp']
                print(f"{GREEN}✅ Loaded {len(self.history_df)} historical Schumann readings{RESET}")
            else:
                print(f"{YELLOW}⚠️ No historical Schumann data found. Will create new history.{RESET}")
                self.history_df = pd.DataFrame(columns=["Timestamp", "Schumann"])
                
        except Exception as e:
            print(f"{RED}❌ Error loading Schumann history: {e}{RESET}")
            self.history_df = pd.DataFrame(columns=["Timestamp", "Schumann"])
    
    def fetch_current_schumann(self):
        """Fetch the most recent Schumann resonance data point."""
        try:
            # Calculate time window (last 24 hours)
            now = datetime.datetime.now()
            end_time = int(now.timestamp())
            start_time = end_time - (24 * 60 * 60)  # 24 hours in seconds
            
            # Debug the actual timestamps
            print(f"{CYAN}🔍 Time window: {datetime.datetime.fromtimestamp(start_time)} to {now}{RESET}")
            
            # Construct URL with millisecond timestamps as expected by the API
            url = f"{HEARTMATH_API_URL}?start={start_time * 1000}&end={end_time * 1000}"
            print(f"{CYAN}📡 Fetching Schumann data from: {url}{RESET}")
            
            response = requests.get(url, timeout=10)
            
            if (response.status_code == 200):
                data = response.json()
                
                # Debug raw response to see exact format
                print(f"{CYAN}🔍 Raw API Response: {data}{RESET}")
                
                # Check if response is array with valid data
                if isinstance(data, list) and data and isinstance(data[0], list):
                    # Get non-empty entries that have at least 4 elements
                    valid_entries = [entry for entry in data if len(entry) >= 4 and entry[3] is not None]
                    
                    if valid_entries:
                        # Sort by timestamp to get most recent
                        sorted_data = sorted(valid_entries, key=lambda x: x[0], reverse=True)
                        latest_entry = sorted_data[0]
                        
                        # Extract timestamp and value
                        timestamp_ms = latest_entry[0]  # This is in milliseconds
                        timestamp_sec = timestamp_ms / 1000  # Convert to seconds
                        schumann_value = latest_entry[3]  # Extract Schumann power
                        
                        # Convert to timestamp and datetime
                        dt = datetime.datetime.fromtimestamp(timestamp_sec)
                        
                        print(f"{GREEN}✅ Parsed Schumann value: {schumann_value} at {dt}{RESET}")
                        
                        return {
                            "timestamp": dt,
                            "value": float(schumann_value),
                            "unix_time": int(timestamp_sec)
                        }
                    else:
                        print(f"{YELLOW}⚠️ No valid Schumann data entries found in response{RESET}")
                else:
                    print(f"{YELLOW}⚠️ Unexpected response format from API{RESET}")
            else:
                print(f"{RED}❌ API request failed with status code: {response.status_code}{RESET}")
                
            # If we reach here, no valid data was found
            return self._generate_fallback_data()
                
        except Exception as e:
            print(f"{RED}❌ Error fetching Schumann data: {e}{RESET}")
            return self._generate_fallback_data()
    
    def _generate_fallback_data(self):
        """Generate fallback Schumann data for testing when API fails."""
        print(f"{YELLOW}⚠️ Using fallback Schumann data for testing{RESET}")
        
        # Import here to avoid polluting global namespace
        import random
        
        # Generate semi-random Schumann value based on time of day
        now = datetime.datetime.now()
        hour = now.hour
        
        # Schumann tends to be higher during daylight hours
        # Base values between 7.0 to 8.5 depending on time of day
        base_value = 7.0 + (hour % 12) / 4.0
        
        # Add random components - occasional spikes
        if random.random() < 0.05:  # 5% chance of spike
            spike = random.uniform(3.0, 7.0)
            print(f"{RED}⚠️ Generating artificial Schumann spike! (+{spike:.2f}Hz){RESET}")
            value = base_value + spike
        else:
            # Normal variation
            value = base_value + random.uniform(-0.8, 1.2)
        
        return {
            "timestamp": now,
            "value": value,
            "unix_time": int(now.timestamp()),
            "is_fallback": True
        }
    
    def update_schumann_data(self):
        """Update Schumann data and store in Redis and CSV."""
        current_data = self.fetch_current_schumann()
        
        if not current_data:
            print(f"{YELLOW}⚠️ Failed to get current Schumann data{RESET}")
            return
        
        is_fallback = current_data.get("is_fallback", False)
        fallback_indicator = " (FALLBACK)" if is_fallback else ""
        
        # Store in Redis
        redis_conn.set("schumann_resonance", current_data["value"])
        redis_conn.set("schumann_timestamp", current_data["unix_time"])
        redis_conn.set("schumann_is_fallback", "1" if is_fallback else "0")
        
        # Add to historical list in Redis
        entry = f"{current_data['unix_time']}:{current_data['value']}"
        redis_conn.rpush("schumann_history", entry)
        redis_conn.ltrim("schumann_history", -SCHUMANN_CACHE_SIZE, -1)  # Keep last N entries
        
        # Add to dataframe and save CSV periodically
        new_row = pd.DataFrame({
            "Timestamp": [current_data["timestamp"]],
            "Schumann": [current_data["value"]]
        })
        
        self.history_df = pd.concat([self.history_df, new_row], ignore_index=True)
        
        # Save CSV every 10 updates (approximately every 10 minutes)
        if len(self.history_df) % 10 == 0:
            os.makedirs(os.path.dirname(SCHUMANN_CSV_PATH), exist_ok=True)
            self.history_df.to_csv(SCHUMANN_CSV_PATH, index=False)
            print(f"{GREEN}✅ Updated Schumann history CSV with {len(self.history_df)} records{RESET}")
        
        # Print status with color-coding based on Schumann levels
        self._print_schumann_status(current_data["value"], fallback_indicator)
    
    def _print_schumann_status(self, value, suffix=""):
        """Print colored Schumann resonance status based on intensity."""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Color code based on Schumann intensity
        if value >= 12:
            color = RED
            intensity = "EXTREME"
            alert = "⚠️ "
        elif value >= 8:
            color = YELLOW
            intensity = "HIGH"
            alert = "⚠️ "
        elif value >= 5:
            color = CYAN
            intensity = "MODERATE"
            alert = ""
        else:
            color = BLUE
            intensity = "NORMAL"
            alert = ""
        
        print(f"{MAGENTA}[{timestamp}]{RESET} {alert}Schumann Resonance: {color}{value:.2f} Hz{suffix} {RESET}({intensity})")
        
        # Only log to Redis if significant
        if value >= 8:
            redis_conn.hset(
                f"schumann_spike:{int(time.time())}", 
                mapping={
                    "value": str(value),
                    "intensity": intensity,
                    "timestamp": timestamp
                }
            )
    
    def monitor_loop(self):
        """Main monitoring loop for Schumann resonance data."""
        while self.running:
            try:
                self.update_schumann_data()
                
                # Calculate correlations with BTC price movement
                self._analyze_schumann_price_correlation()
                
            except Exception as e:
                print(f"{RED}❌ Error in Schumann monitor loop: {e}{RESET}")
            
            # Wait for next update
            time.sleep(UPDATE_INTERVAL)
    
    def _analyze_schumann_price_correlation(self):
        """Analyze correlation between Schumann resonance and recent BTC price movements."""
        try:
            # Get latest BTC movements from Redis
            btc_movements = redis_conn.lrange("btc_movement_history", -20, -1)
            
            if not btc_movements or len(btc_movements) < 5:
                return  # Not enough data
                
            # Get Schumann history from Redis
            schumann_history = redis_conn.lrange("schumann_history", -20, -1)
            
            if not schumann_history or len(schumann_history) < 5:
                return  # Not enough data
            
            # Simple correlation check (naive implementation for now)
            try:
                # Convert both datasets to pandas series - properly decode bytes to strings
                schumann_data = []
                for item in schumann_history:
                    if isinstance(item, bytes):
                        item = item.decode('utf-8')  # Convert bytes to string
                    parts = item.split(":")
                    if len(parts) >= 2:
                        schumann_data.append(float(parts[1]))
                
                btc_data = []
                for item in btc_movements:
                    if isinstance(item, bytes):
                        item = item.decode('utf-8')  # Convert bytes to string
                    parts = item.split(":")
                    if len(parts) >= 2:
                        btc_data.append(float(parts[1]))
                
                if len(schumann_data) > 0 and len(btc_data) > 0:
                    # Simple directional check (are they moving together?)
                    schumann_direction = schumann_data[-1] - schumann_data[0]
                    btc_direction = btc_data[-1] - btc_data[0]
                    
                    print(f"{CYAN}📊 Correlation analysis: Schumann direction: {schumann_direction:.2f}, BTC direction: {btc_direction:.2f}{RESET}")
                    
                    if (schumann_direction > 0 and btc_direction > 0) or \
                       (schumann_direction < 0 and btc_direction < 0):
                        # Directional correlation detected
                        print(f"{CYAN}📊 Schumann-BTC directional correlation detected!{RESET}")
                        
                        # Store in Redis
                        redis_conn.set("schumann_btc_correlation", "1")
                    else:
                        redis_conn.set("schumann_btc_correlation", "0")
            except Exception as e:
                print(f"{YELLOW}⚠️ Error in correlation calculation: {e}{RESET}")
                import traceback
                traceback.print_exc()  # Print full stack trace for debugging
            
        except Exception as e:
            print(f"{YELLOW}⚠️ Error analyzing Schumann-BTC correlation: {e}{RESET}")
    
    def start(self):
        """Start the Schumann monitoring service."""
        if self.running:
            print(f"{YELLOW}⚠️ Schumann monitor already running{RESET}")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self.monitor_loop)
        self.thread.daemon = True
        self.thread.start()
        print(f"{GREEN}✅ Schumann Resonance Monitor Started{RESET}")
    
    def stop(self):
        """Stop the Schumann monitoring service."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5.0)
        print(f"{YELLOW}⚠️ Schumann Resonance Monitor Stopped{RESET}")

# Singleton instance
schumann_monitor = SchumannResonanceMonitor()

# Helper functions for other modules
def get_current_schumann():
    """Get the current Schumann resonance value."""
    try:
        value = redis_conn.get("schumann_resonance")
        if value:
            if isinstance(value, bytes):
                value = value.decode('utf-8')
            return float(value)
    except (ValueError, TypeError) as e:
        print(f"{YELLOW}⚠️ Error retrieving Schumann value: {e}{RESET}")
    return 0.0

def start_schumann_monitor():
    """Start the Schumann resonance monitor."""
    schumann_monitor.start()

def stop_schumann_monitor():
    """Stop the Schumann resonance monitor."""
    schumann_monitor.stop()

# At the bottom of the file
if __name__ == "__main__":
    print(f"{MAGENTA}🌍 Schumann Resonance Monitor{RESET}")
    print(f"{CYAN}1. Start monitor service (continuous){RESET}")
    print(f"{CYAN}2. Test single API fetch{RESET}")
    print(f"{CYAN}3. Generate sample fallback data{RESET}")
    
    choice = input("Select option (1-3): ").strip()
    
    if choice == "2":
        # Test single fetch
        print(f"{MAGENTA}Testing single API fetch...{RESET}")
        monitor = SchumannResonanceMonitor()
        data = monitor.fetch_current_schumann()
        print(f"{GREEN}Fetch result: {data}{RESET}")
    elif choice == "3":
        # Generate fallback
        print(f"{MAGENTA}Generating 5 sample fallback values...{RESET}")
        monitor = SchumannResonanceMonitor()
        for i in range(5):
            data = monitor._generate_fallback_data()
            print(f"{GREEN}Sample {i+1}: {data['value']:.2f}Hz at {data['timestamp']}{RESET}")
            time.sleep(1)
    else:
        # Start service
        print(f"{MAGENTA}🌍 Starting Schumann Resonance Monitor Service...{RESET}")
        schumann_monitor.start()
        
        try:
            # Keep main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"{YELLOW}Shutting down Schumann Monitor...{RESET}")
            schumann_monitor.stop()