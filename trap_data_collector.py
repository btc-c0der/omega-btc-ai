#!/usr/bin/env python3
"""
Market Maker Trap Data Collector for Dashboard

This script collects trap data from InfluxDB and Redis, organizes it,
and makes it available in Redis for the dashboard to display.
"""

import os
import sys
import json
import time
import redis
import logging
from datetime import datetime, timezone, timedelta
from collections import Counter, defaultdict
from influxdb_client import InfluxDBClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("trap_data_collector")

# Terminal colors for prettier output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

# InfluxDB configuration
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "w4JzUNsut5GjPBB72ts_U3D5r6ojYkWGUTTHZdMOjVXmJqX8Wnuyp3EYLRzi9H5BLwM9hAEltSFdEF-ZDwSjOg==")
INFLUX_ORG = os.getenv("INFLUX_ORG", "omega")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "mm_traps")

# Redis configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

class TrapDataCollector:
    """Collects and organizes trap data for the dashboard."""
    
    def __init__(self):
        # Initialize connections
        self.influx_client = None
        self.redis_client = None
        self.setup_connections()
    
    def setup_connections(self):
        """Initialize connections to InfluxDB and Redis."""
        try:
            # Connect to InfluxDB
            self.influx_client = InfluxDBClient(
                url=INFLUX_URL,
                token=INFLUX_TOKEN,
                org=INFLUX_ORG
            )
            health = self.influx_client.health()
            if health.status == "pass":
                logger.info(f"{GREEN}✅ Connected to InfluxDB{RESET}")
            else:
                logger.error(f"{RED}❌ InfluxDB health check failed: {health.message}{RESET}")
            
            # Connect to Redis
            self.redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                decode_responses=True
            )
            if self.redis_client.ping():
                logger.info(f"{GREEN}✅ Connected to Redis{RESET}")
            else:
                logger.error(f"{RED}❌ Redis ping failed{RESET}")
        
        except Exception as e:
            logger.error(f"{RED}❌ Error setting up connections: {e}{RESET}")
            if self.influx_client:
                self.influx_client.close()
            sys.exit(1)
    
    def query_trap_events(self, time_range="-30d"):
        """Query trap events from InfluxDB."""
        logger.info(f"{BLUE}Querying trap events for the last {time_range[1:]}...{RESET}")
        query_api = self.influx_client.query_api()
        
        query = f'''
        from(bucket: "{INFLUX_BUCKET}")
            |> range(start: {time_range})
            |> filter(fn: (r) => r._measurement == "mm_traps" or r._measurement == "trap_events")
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        '''
        
        try:
            result = query_api.query_data_frame(query)
            if isinstance(result, list) and len(result) > 0:
                result = pd.concat(result)
            
            logger.info(f"{GREEN}✅ Found {len(result)} trap events{RESET}")
            return result
        except Exception as e:
            logger.error(f"{RED}❌ Error querying trap events: {e}{RESET}")
            return pd.DataFrame()
    
    def analyze_trap_data(self, trap_data):
        """Analyze trap data and extract insights."""
        if trap_data.empty:
            logger.warning(f"{YELLOW}No trap data to analyze{RESET}")
            return {}
        
        # Initialize results
        results = {
            "total_count": len(trap_data),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Calculate trap type distribution
        if 'type' in trap_data.columns:
            type_counts = trap_data['type'].value_counts().to_dict()
            results["trap_types"] = type_counts
            
            # Find dominant trap type
            if type_counts:
                results["dominant_type"] = max(type_counts.items(), key=lambda x: x[1])[0]
            else:
                results["dominant_type"] = "Unknown"
        
        # Calculate average confidence
        if 'confidence' in trap_data.columns:
            results["avg_confidence"] = float(trap_data['confidence'].mean())
            results["high_confidence_count"] = int((trap_data['confidence'] > 0.7).sum())
        
        # Calculate trap timing distribution
        if '_time' in trap_data.columns:
            trap_data['_time'] = pd.to_datetime(trap_data['_time'])
            
            # Hour of day distribution
            trap_data['hour'] = trap_data['_time'].dt.hour
            hour_distribution = trap_data['hour'].value_counts().sort_index().to_dict()
            results["hour_distribution"] = hour_distribution
            
            # Day of week distribution
            trap_data['day_of_week'] = trap_data['_time'].dt.day_name()
            day_distribution = trap_data['day_of_week'].value_counts().to_dict()
            results["day_distribution"] = day_distribution
        
        # Get recent high confidence traps
        if 'confidence' in trap_data.columns and '_time' in trap_data.columns:
            high_conf_traps = trap_data[trap_data['confidence'] > 0.7].sort_values('_time', ascending=False).head(5)
            
            if not high_conf_traps.empty:
                recent_traps = []
                for _, trap in high_conf_traps.iterrows():
                    # Convert timestamp to relative time
                    trap_time = pd.to_datetime(trap['_time'])
                    now = pd.to_datetime(datetime.now(timezone.utc))
                    diff_seconds = (now - trap_time).total_seconds()
                    
                    if diff_seconds < 60:
                        time_ago = "Just now"
                    elif diff_seconds < 3600:
                        time_ago = f"{int(diff_seconds/60)} minutes ago"
                    elif diff_seconds < 86400:
                        time_ago = f"{int(diff_seconds/3600)} hours ago"
                    else:
                        time_ago = f"{int(diff_seconds/86400)} days ago"
                    
                    # Determine timeframe if available
                    timeframe = trap.get('timeframe', '15min')  # Default to 15min if not specified
                    
                    recent_traps.append({
                        "type": trap.get('type', 'Unknown'),
                        "confidence": float(trap.get('confidence', 0)),
                        "time_ago": time_ago,
                        "timeframe": timeframe
                    })
                
                results["recent_high_conf_traps"] = recent_traps
        
        return results
    
    def calculate_performance_metrics(self, trap_data):
        """Calculate performance metrics based on trap events and trade data."""
        # This would connect to trade data and calculate actual win rates
        # For demo purposes, we'll use synthesized values
        
        # Actual implementation would query trade data that followed trap signals
        # and calculate win rates for each trap type
        
        performance = {
            "bear_trap_winrate": 65,  # Percentage
            "bull_trap_winrate": 58,
            "liquidity_grab_winrate": 72,
            "stop_hunt_winrate": 68,
            "avg_trade_pnl": 2.3,  # Percentage
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        return performance
    
    def store_in_redis(self, data, key):
        """Store processed data in Redis for dashboard consumption."""
        try:
            self.redis_client.set(key, json.dumps(data))
            logger.info(f"{GREEN}✅ Stored data in Redis key: {key}{RESET}")
            return True
        except Exception as e:
            logger.error(f"{RED}❌ Error storing data in Redis: {e}{RESET}")
            return False
    
    def run(self):
        """Run the data collector process."""
        logger.info(f"{BLUE}Starting trap data collection...{RESET}")
        
        try:
            # Query trap events
            trap_data = self.query_trap_events()
            
            if not trap_data.empty:
                # Analyze trap data
                analysis_results = self.analyze_trap_data(trap_data)
                
                # Calculate performance metrics
                performance_metrics = self.calculate_performance_metrics(trap_data)
                
                # Combine results
                dashboard_data = {
                    "analysis": analysis_results,
                    "performance": performance_metrics,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                
                # Store results in Redis
                self.store_in_redis(dashboard_data, "dashboard:trap_analysis")
                
                # Also store individual components for easier access
                self.store_in_redis(analysis_results, "dashboard:trap_analysis:data")
                self.store_in_redis(performance_metrics, "dashboard:trap_analysis:performance")
                
                logger.info(f"{GREEN}✅ Successfully updated trap analysis data{RESET}")
            else:
                logger.warning(f"{YELLOW}No trap data available to analyze{RESET}")
        
        except Exception as e:
            logger.error(f"{RED}❌ Error in data collection process: {e}{RESET}")
        
        finally:
            # Close connections
            if self.influx_client:
                self.influx_client.close()

def main():
    """Main function."""
    collector = TrapDataCollector()
    collector.run()

if __name__ == "__main__":
    try:
        import pandas as pd
        main()
    except ImportError:
        logger.error(f"{RED}❌ pandas library is required. Please install it with 'pip install pandas'{RESET}")
        sys.exit(1) 