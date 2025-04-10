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

"""
AIXBT Data Collector
===================

Collects data from various sources including Redis, stdout logs, and system metrics.
Prepares and transforms data for AI model training.

Features:
- Redis data collection for AIXBT and BTC prices
- Log parsing for extracting labeled data
- Volume data extraction and normalization
- System metrics collection
- Training data preparation
"""

import os
import re
import json
import time
import logging
import asyncio
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timezone, timedelta
import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("aixbt-data-collector")

# Try to import Redis components
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    logger.warning("Redis package not available. Some features will be limited.")
    REDIS_AVAILABLE = False

try:
    from omega_ai.utils.enhanced_redis_manager import EnhancedRedisManager
    ENHANCED_REDIS_AVAILABLE = True
except ImportError:
    logger.warning("EnhancedRedisManager not available. Using standard Redis client.")
    ENHANCED_REDIS_AVAILABLE = False

# Constants
LOG_PREFIX = "🧠 AIXBT DATA COLLECTOR"
DEFAULT_DATA_STORAGE_PATH = "data/aixbt_training_data"
DEFAULT_TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d"]
REQUIRED_FIELDS = [
    "timestamp", "aixbt_price", "btc_price", "correlation", 
    "volume_aixbt", "volume_btc", "market_phase"
]

class AixbtDataCollector:
    """Data collector for AIXBT AI model training."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the data collector.
        
        Args:
            config: Configuration dictionary (optional)
        """
        self.config = config or {}
        self.redis_client = None
        self.redis_manager = None
        self.data_storage_path = self.config.get("data_storage_path", DEFAULT_DATA_STORAGE_PATH)
        
        # Ensure data directory exists
        os.makedirs(self.data_storage_path, exist_ok=True)
        
        # Initialize Redis connection
        self._setup_redis_connection()
        
        # Initialize data storage
        self.raw_data = {
            "aixbt_prices": [],
            "btc_prices": [],
            "correlations": [],
            "divergences": [],
            "volumes_aixbt": [],
            "volumes_btc": [],
            "system_metrics": [],
            "log_entries": []
        }
        
        # Training data
        self.training_data = pd.DataFrame()
        self.feature_columns = []
        self.target_columns = []
        
        # Define regex patterns for log parsing
        self.log_patterns = {
            "aixbt_price": r"AIXBT price update: \$([0-9.]+)",
            "btc_price": r"BTC price update: \$([0-9.]+)",
            "correlation": r"Correlation (increasing|decreasing) to ([0-9.-]+)",
            "divergence": r"AIXBT (outperforming|underperforming) BTC by ([0-9.-]+)%",
            "market_phase": r"Market phase changed to: ([A-Z_]+)"
        }
        
        # Market phase mapping
        self.market_phases = {
            "ACCUMULATION": 0,
            "BULL": 1,
            "DISTRIBUTION": 2,
            "BEAR": 3,
            "CONSOLIDATION": 4,
            "UNKNOWN": 5
        }
        
        logger.info(f"{LOG_PREFIX} - Data collector initialized with storage at {self.data_storage_path}")
    
    def _setup_redis_connection(self) -> None:
        """Set up the Redis connection for data collection."""
        if not REDIS_AVAILABLE:
            logger.error(f"{LOG_PREFIX} - Redis package not available. Cannot connect to Redis.")
            return
            
        # Try Enhanced Redis Manager first if available
        if ENHANCED_REDIS_AVAILABLE:
            try:
                self.redis_manager = EnhancedRedisManager(
                    use_failover=True,
                    sync_on_reconnect=True
                )
                logger.info(f"{LOG_PREFIX} - Connected to Redis using EnhancedRedisManager")
                return
            except Exception as e:
                logger.error(f"{LOG_PREFIX} - Error connecting to Redis with EnhancedRedisManager: {e}")
        
        # Fall back to standard Redis
        try:
            # Get Redis configuration from environment
            host = os.environ.get("REDIS_HOST", "localhost")
            port = int(os.environ.get("REDIS_PORT", 6379))
            username = os.environ.get("REDIS_USERNAME", "")
            password = os.environ.get("REDIS_PASSWORD", "")
            ssl = os.environ.get("REDIS_SSL", "false").lower() in ("true", "1", "yes")
            
            # Create connection
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                username=username,
                password=password,
                ssl=ssl,
                decode_responses=True
            )
            
            # Test connection
            self.redis_client.ping()
            logger.info(f"{LOG_PREFIX} - Connected to Redis at {host}:{port}")
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error connecting to Redis: {e}")
            self.redis_client = None
    
    async def get_price_data_from_redis(self, timeframe: str = "1h", limit: int = 1000) -> pd.DataFrame:
        """
        Retrieve price data from Redis and format as DataFrame.
        
        Args:
            timeframe: Time frame to retrieve data for
            limit: Maximum number of entries to retrieve
            
        Returns:
            DataFrame with price data
        """
        data = []
        
        try:
            # Determine keys based on timeframe
            aixbt_key = f"aixbt_movement_history"
            btc_key = f"btc_movement_history"
            correlation_key = f"aixbt_btc_correlation_history"
            
            # Get data from Redis
            if self.redis_manager is not None:
                # Using Enhanced Redis Manager
                aixbt_data = await self.redis_manager.lrange(aixbt_key, 0, limit-1)
                btc_data = await self.redis_manager.lrange(btc_key, 0, limit-1)
                correlation_data = await self.redis_manager.lrange(correlation_key, 0, limit-1)
            elif self.redis_client is not None:
                # Using standard Redis client
                aixbt_data = self.redis_client.lrange(aixbt_key, 0, limit-1)
                btc_data = self.redis_client.lrange(btc_key, 0, limit-1)
                correlation_data = self.redis_client.lrange(correlation_key, 0, limit-1)
            else:
                logger.error(f"{LOG_PREFIX} - No Redis connection available")
                return pd.DataFrame()
            
            # Parse JSON data
            aixbt_parsed = [json.loads(item) for item in aixbt_data if item]
            btc_parsed = [json.loads(item) for item in btc_data if item]
            correlation_parsed = [json.loads(item) for item in correlation_data if item]
            
            # Store raw data for later processing
            self.raw_data["aixbt_prices"] = aixbt_parsed
            self.raw_data["btc_prices"] = btc_parsed
            self.raw_data["correlations"] = correlation_parsed
            
            # Create lookup dictionaries for easier merging
            btc_dict = {item.get("timestamp"): item for item in btc_parsed}
            correlation_dict = {item.get("timestamp"): item for item in correlation_parsed}
            
            # Merge data based on timestamps
            for aixbt_item in aixbt_parsed:
                timestamp = aixbt_item.get("timestamp")
                if not timestamp:
                    continue
                    
                # Find closest matching timestamp for BTC and correlation data
                btc_item = self._find_closest_entry(timestamp, btc_dict)
                correlation_item = self._find_closest_entry(timestamp, correlation_dict)
                
                # Combine data
                entry = {
                    "timestamp": timestamp,
                    "aixbt_price": aixbt_item.get("price", 0.0),
                    "btc_price": btc_item.get("price", 0.0) if btc_item else 0.0,
                    "volume_aixbt": aixbt_item.get("volume", 0.0),
                    "volume_btc": btc_item.get("volume", 0.0) if btc_item else 0.0,
                    "correlation": correlation_item.get("correlation", 0.0) if correlation_item else 0.0,
                    "is_simulated": aixbt_item.get("simulated", False)
                }
                
                data.append(entry)
            
            # Create DataFrame and sort by timestamp
            df = pd.DataFrame(data)
            if not df.empty:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                df = df.sort_values("timestamp")
                
                # Resample to desired timeframe
                if timeframe != "1m":
                    df = self._resample_dataframe(df, timeframe)
            
            return df
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error retrieving price data from Redis: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return pd.DataFrame()
    
    def _find_closest_entry(self, timestamp: str, data_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find the closest matching timestamp in a dictionary of entries."""
        if timestamp in data_dict:
            return data_dict[timestamp]
            
        # Parse timestamp
        target_dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        
        # Find closest match
        closest_entry = None
        min_diff = timedelta(hours=1)  # Maximum allowed difference
        
        for ts, entry in data_dict.items():
            try:
                entry_dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                diff = abs(entry_dt - target_dt)
                
                if diff < min_diff:
                    min_diff = diff
                    closest_entry = entry
            except (ValueError, TypeError):
                continue
                
        return closest_entry
    
    def _resample_dataframe(self, df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """Resample DataFrame to a specific timeframe."""
        # Define resampling rules
        rules = {
            "1m": "1min",
            "5m": "5min",
            "15m": "15min",
            "30m": "30min",
            "1h": "1H",
            "4h": "4H",
            "1d": "1D"
        }
        
        rule = rules.get(timeframe, "1H")
        
        # Set timestamp as index for resampling
        df = df.set_index("timestamp")
        
        # Define aggregation functions
        agg_dict = {
            "aixbt_price": "last",
            "btc_price": "last",
            "volume_aixbt": "sum",
            "volume_btc": "sum",
            "correlation": "mean",
            "is_simulated": "last"
        }
        
        # Resample and reset index
        resampled = df.resample(rule).agg(agg_dict).reset_index()
        return resampled
    
    def parse_log_data(self, log_file: str) -> List[Dict[str, Any]]:
        """
        Parse log file to extract labeled data for training.
        
        Args:
            log_file: Path to log file
            
        Returns:
            List of extracted data entries
        """
        data = []
        
        try:
            with open(log_file, 'r') as f:
                log_content = f.readlines()
                
            for line in log_content:
                entry = self._parse_log_line(line)
                if entry:
                    data.append(entry)
                    
            # Store parsed log entries
            self.raw_data["log_entries"] = data
            return data
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error parsing log file: {e}")
            return []
    
    def _parse_log_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a single log line to extract relevant data."""
        # Extract timestamp
        timestamp_match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})", line)
        if not timestamp_match:
            return None
            
        timestamp = datetime.strptime(timestamp_match.group(1), "%Y-%m-%d %H:%M:%S,%f")
        
        # Initialize data entry
        entry = {"timestamp": timestamp}
        
        # Extract data using regex patterns
        for field, pattern in self.log_patterns.items():
            match = re.search(pattern, line)
            if match:
                if field == "aixbt_price" or field == "btc_price":
                    entry[field] = float(match.group(1))
                elif field == "correlation":
                    direction = match.group(1)
                    value = float(match.group(2))
                    entry[field] = value
                    entry["correlation_direction"] = 1 if direction == "increasing" else -1
                elif field == "divergence":
                    direction = match.group(1)
                    value = float(match.group(2))
                    entry[field] = value if direction == "outperforming" else -value
                elif field == "market_phase":
                    phase = match.group(1)
                    entry[field] = self.market_phases.get(phase, self.market_phases["UNKNOWN"])
                
        # Return if any relevant data was found
        return entry if len(entry) > 1 else None
    
    def prepare_training_data(self, lookback_window: int = 10) -> pd.DataFrame:
        """
        Prepare training data from collected data sources.
        
        Args:
            lookback_window: Number of historical data points to include as features
            
        Returns:
            DataFrame with prepared training data
        """
        try:
            # Combine data from different sources
            combined_data = []
            
            # Start with price data if available
            if self.raw_data["aixbt_prices"] and self.raw_data["btc_prices"]:
                # Create price and volume features
                for i, aixbt_entry in enumerate(self.raw_data["aixbt_prices"]):
                    if i < lookback_window:
                        continue
                        
                    # Get timestamp
                    timestamp = aixbt_entry.get("timestamp")
                    if not timestamp:
                        continue
                        
                    # Create entry with basic information
                    entry = {
                        "timestamp": timestamp,
                        "aixbt_price": aixbt_entry.get("price", 0.0),
                        "aixbt_volume": aixbt_entry.get("volume", 0.0),
                        "is_simulated": aixbt_entry.get("simulated", False)
                    }
                    
                    # Add lookback features
                    for j in range(1, lookback_window + 1):
                        if i - j >= 0:
                            hist_entry = self.raw_data["aixbt_prices"][i - j]
                            entry[f"aixbt_price_t-{j}"] = hist_entry.get("price", 0.0)
                            entry[f"aixbt_volume_t-{j}"] = hist_entry.get("volume", 0.0)
                    
                    combined_data.append(entry)
            
            # Convert to DataFrame
            df = pd.DataFrame(combined_data) if combined_data else pd.DataFrame()
            
            if not df.empty:
                # Convert timestamp to datetime
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                
                # Add derived features
                df = self._add_derived_features(df)
                
                # Set feature and target columns
                self.feature_columns = [col for col in df.columns if col.startswith("aixbt_") 
                                        or col.startswith("btc_") 
                                        or col.startswith("correlation_")
                                        or col.startswith("volume_")]
                
                self.target_columns = ["aixbt_price_next", "correlation_next", "divergence_next"]
                
                # Store training data
                self.training_data = df
                
                logger.info(f"{LOG_PREFIX} - Training data prepared with {len(df)} rows and {len(self.feature_columns)} features")
                
            return df
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error preparing training data: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return pd.DataFrame()
    
    def _add_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived features for model training."""
        if df.empty:
            return df
            
        # Add target variables (future values)
        df["aixbt_price_next"] = df["aixbt_price"].shift(-1)
        df["correlation_next"] = df.get("correlation", 0).shift(-1)
        
        if "btc_price" in df.columns:
            # Calculate current divergence
            df["divergence"] = (df["aixbt_price"] / df["aixbt_price"].shift(1) - 
                               df["btc_price"] / df["btc_price"].shift(1)) * 100
            
            # Future divergence
            df["divergence_next"] = df["divergence"].shift(-1)
            
            # Correlation features if both coins are available
            df["price_ratio"] = df["aixbt_price"] / df["btc_price"]
            
            if "volume_btc" in df.columns and "volume_aixbt" in df.columns:
                df["volume_ratio"] = df["volume_aixbt"] / df["volume_btc"].replace(0, 1)
        
        # Technical indicators
        if len(df) >= 14:
            # Price momentum
            df["aixbt_momentum_3"] = df["aixbt_price"] / df["aixbt_price"].shift(3) - 1
            df["aixbt_momentum_7"] = df["aixbt_price"] / df["aixbt_price"].shift(7) - 1
            df["aixbt_momentum_14"] = df["aixbt_price"] / df["aixbt_price"].shift(14) - 1
            
            if "btc_price" in df.columns:
                df["btc_momentum_3"] = df["btc_price"] / df["btc_price"].shift(3) - 1
                df["btc_momentum_7"] = df["btc_price"] / df["btc_price"].shift(7) - 1
                df["btc_momentum_14"] = df["btc_price"] / df["btc_price"].shift(14) - 1
                
                # Relative momentum
                df["relative_momentum_3"] = df["aixbt_momentum_3"] - df["btc_momentum_3"]
                df["relative_momentum_7"] = df["aixbt_momentum_7"] - df["btc_momentum_7"]
                df["relative_momentum_14"] = df["aixbt_momentum_14"] - df["btc_momentum_14"]
        
        # Time-based features 
        df["hour"] = df["timestamp"].dt.hour
        df["day_of_week"] = df["timestamp"].dt.dayofweek
        
        # Drop rows with NaN values
        df = df.dropna()
        
        return df
    
    def save_training_data(self, filename: str = "aixbt_training_data.csv") -> str:
        """
        Save prepared training data to CSV file.
        
        Args:
            filename: Name of the CSV file
            
        Returns:
            Path to the saved file
        """
        if self.training_data.empty:
            logger.warning(f"{LOG_PREFIX} - No training data available to save")
            return ""
            
        file_path = os.path.join(self.data_storage_path, filename)
        
        try:
            self.training_data.to_csv(file_path, index=False)
            logger.info(f"{LOG_PREFIX} - Training data saved to {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error saving training data: {e}")
            return ""
    
    def load_training_data(self, filename: str = "aixbt_training_data.csv") -> pd.DataFrame:
        """
        Load training data from CSV file.
        
        Args:
            filename: Name of the CSV file
            
        Returns:
            DataFrame with loaded training data
        """
        file_path = os.path.join(self.data_storage_path, filename)
        
        try:
            if not os.path.exists(file_path):
                logger.warning(f"{LOG_PREFIX} - Training data file not found: {file_path}")
                return pd.DataFrame()
                
            df = pd.read_csv(file_path)
            
            # Convert timestamp to datetime if present
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                
            # Store loaded data
            self.training_data = df
            
            # Identify feature and target columns
            self.feature_columns = [col for col in df.columns if col.startswith("aixbt_") 
                                    or col.startswith("btc_") 
                                    or col.startswith("correlation_")
                                    or col.startswith("volume_")]
            
            self.target_columns = [col for col in df.columns if col.endswith("_next")]
            
            logger.info(f"{LOG_PREFIX} - Training data loaded from {file_path} with {len(df)} rows")
            return df
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error loading training data: {e}")
            return pd.DataFrame()

    async def collect_data(self, timeframe: str = "1h", limit: int = 1000) -> pd.DataFrame:
        """
        Main method to collect all required data and prepare for model training.
        
        Args:
            timeframe: Time frame to collect data for
            limit: Maximum number of entries to collect
            
        Returns:
            DataFrame with prepared data
        """
        try:
            # Get price data from Redis
            price_data = await self.get_price_data_from_redis(timeframe, limit)
            
            # Prepare training data
            training_data = self.prepare_training_data()
            
            # Save training data
            if not training_data.empty:
                filename = f"aixbt_training_data_{timeframe}_{datetime.now().strftime('%Y%m%d')}.csv"
                self.save_training_data(filename)
            
            return training_data
            
        except Exception as e:
            logger.error(f"{LOG_PREFIX} - Error collecting data: {e}")
            return pd.DataFrame()

async def main():
    """Run the data collector as a standalone script."""
    # Create data collector
    collector = AixbtDataCollector()
    
    # Collect data for different timeframes
    for timeframe in DEFAULT_TIMEFRAMES:
        logger.info(f"Collecting data for timeframe: {timeframe}")
        df = await collector.collect_data(timeframe)
        if not df.empty:
            logger.info(f"Collected {len(df)} entries for {timeframe}")
        else:
            logger.warning(f"No data collected for {timeframe}")
    
    logger.info("Data collection complete")

if __name__ == "__main__":
    asyncio.run(main()) 