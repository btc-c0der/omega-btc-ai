#!/usr/bin/env python3

"""
GNU Affero General Public License v3.0

Copyright (c) 2024 OMEGA BTC AI Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""
Redis Time Series Optimization Module
====================================

This module provides optimized time series storage for simulation data in Redis.
It implements multiple granularity levels (minute, hourly, daily) with automatic
compression and cleanup to prevent Redis memory overflow during long simulations.

Key Features:
- Multi-granularity storage (minute, hourly, daily)
- Automatic data compression for older data
- Configurable retention periods for each granularity level
- Data aggregation with statistical metrics (min/max/avg/ohlc)
- Memory-efficient storage with automatic cleanup
"""

import json
import datetime
import enum
import redis
import statistics
from typing import Dict, List, Any, Optional, Union, TypedDict

# Initialize Redis connection
redis_conn = redis.Redis(host="localhost", port=6379, db=0)

# Prefix for all simulation keys
SIM_PREFIX = "sim_"

class TimeSeriesGranularity(enum.Enum):
    """Enum representing time series data granularity levels"""
    MINUTE = "minute"
    HOURLY = "hourly"
    DAILY = "daily"

# Retention period in days for each granularity level
RETENTION_PERIODS = {
    TimeSeriesGranularity.MINUTE: 7,    # Keep minute data for 7 days
    TimeSeriesGranularity.HOURLY: 30,   # Keep hourly data for 30 days
    TimeSeriesGranularity.DAILY: 90,    # Keep daily data for 90 days
}

def store_time_series_data(
    series_name: str, 
    data: Dict[str, Any], 
    timestamp: datetime.datetime,
    granularity: TimeSeriesGranularity = TimeSeriesGranularity.MINUTE
) -> bool:
    """
    Store time series data in Redis with the specified granularity.
    
    Args:
        series_name: Name of the time series (e.g., 'price_history')
        data: Dictionary containing the data to store
        timestamp: Timestamp for the data point
        granularity: Granularity level (minute, hourly, daily)
        
    Returns:
        bool: True if storage was successful, False otherwise
    """
    try:
        # Build the key with format: sim_<series_name>:YYYY-MM-DD:<granularity>
        key = f"{SIM_PREFIX}{series_name}:{timestamp.date().isoformat()}:{granularity.value}"
        
        # Store data as JSON string
        redis_conn.rpush(key, json.dumps(data))
        
        # Set expiration based on retention period
        retention_days = RETENTION_PERIODS[granularity]
        redis_conn.expire(key, 86400 * retention_days)  # 86400 seconds = 1 day
        
        return True
    except Exception as e:
        print(f"Error storing time series data: {e}")
        return False

def get_time_series_data(
    series_name: str,
    date: datetime.date,
    granularity: TimeSeriesGranularity = TimeSeriesGranularity.MINUTE,
    start_idx: int = 0,
    end_idx: int = -1
) -> List[Dict[str, Any]]:
    """
    Retrieve time series data from Redis.
    
    Args:
        series_name: Name of the time series (e.g., 'price_history')
        date: Date to retrieve data for
        granularity: Granularity level (minute, hourly, daily)
        start_idx: Start index for range query (0-based)
        end_idx: End index for range query (-1 for all)
        
    Returns:
        List of dictionaries containing the time series data
    """
    try:
        # Build the key with format: sim_<series_name>:YYYY-MM-DD:<granularity>
        key = f"{SIM_PREFIX}{series_name}:{date.isoformat()}:{granularity.value}"
        
        # Get data range from Redis
        data_bytes = redis_conn.lrange(key, start_idx, end_idx)
        
        # Parse JSON data
        return [json.loads(item) for item in data_bytes]
    except Exception as e:
        print(f"Error retrieving time series data: {e}")
        return []

def compress_historical_data(
    series_name: str,
    date: datetime.date,
    source_granularity: TimeSeriesGranularity = TimeSeriesGranularity.MINUTE,
    target_granularity: TimeSeriesGranularity = TimeSeriesGranularity.HOURLY
) -> bool:
    """
    Compress historical data from a higher granularity to a lower one.
    For example, compress minute data into hourly aggregates.
    
    Args:
        series_name: Name of the time series (e.g., 'price_history')
        date: Date of the data to compress
        source_granularity: Source granularity level
        target_granularity: Target granularity level
        
    Returns:
        bool: True if compression was successful, False otherwise
    """
    try:
        # Build source and target keys
        source_key = f"{SIM_PREFIX}{series_name}:{date.isoformat()}:{source_granularity.value}"
        target_key = f"{SIM_PREFIX}{series_name}:{date.isoformat()}:{target_granularity.value}"
        
        # Get all data from source granularity
        data_bytes = redis_conn.lrange(source_key, 0, -1)
        
        if not data_bytes:
            return False
            
        # Parse JSON data
        data_points = [json.loads(item) for item in data_bytes]
        
        # Group data by hour if compressing minute->hourly or by day if hourly->daily
        grouped_data = {}
        
        for point in data_points:
            # Parse timestamp
            timestamp = datetime.datetime.strptime(
                point["timestamp"], 
                "%Y-%m-%d %H:%M:%S"
            ).replace(tzinfo=datetime.UTC)
            
            # Create group key based on target granularity
            if target_granularity == TimeSeriesGranularity.HOURLY:
                # Group by hour
                group_key = timestamp.replace(minute=0, second=0, microsecond=0)
            elif target_granularity == TimeSeriesGranularity.DAILY:
                # Group by day
                group_key = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                # Unsupported target granularity
                return False
                
            # Initialize group if needed
            if group_key not in grouped_data:
                grouped_data[group_key] = []
                
            # Add data point to group
            grouped_data[group_key].append(point)
        
        # Process each group and create compressed data points
        for group_time, points in grouped_data.items():
            # Extract price values for aggregation
            prices = [p.get("price", 0) for p in points]
            changes = [p.get("change_pct", 0) for p in points]
            
            # Skip if no valid prices
            if not prices:
                continue
                
            # Create compressed data point with statistics
            compressed_point = {
                "timestamp": group_time.strftime("%Y-%m-%d %H:%M:%S"),
                "price_avg": statistics.mean(prices) if prices else 0,
                "price_min": min(prices) if prices else 0,
                "price_max": max(prices) if prices else 0,
                "price_open": points[0].get("price", 0) if points else 0,
                "price_close": points[-1].get("price", 0) if points else 0,
                "change_pct_cumulative": sum(changes) if changes else 0,
                "regime": points[-1].get("regime", "Unknown") if points else "Unknown",
                "data_points": len(points)
            }
            
            # Store compressed data point
            redis_conn.rpush(target_key, json.dumps(compressed_point))
        
        # Set expiration for target key
        retention_days = RETENTION_PERIODS[target_granularity]
        redis_conn.expire(target_key, 86400 * retention_days)
        
        return True
    except Exception as e:
        print(f"Error compressing historical data: {e}")
        return False

def cleanup_old_data(
    series_name: str,
    current_date: datetime.date
) -> int:
    """
    Clean up old time series data beyond retention periods.
    
    Args:
        series_name: Name of the time series (e.g., 'price_history')
        current_date: Current date for age calculation
        
    Returns:
        int: Number of keys deleted
    """
    try:
        # Find all keys for this series
        pattern = f"{SIM_PREFIX}{series_name}:*"
        all_keys = redis_conn.keys(pattern)
        
        if not all_keys:
            return 0
            
        # Process each key
        for key in all_keys:
            try:
                # Convert bytes to string if needed
                key_str = key.decode('utf-8') if isinstance(key, bytes) else str(key)
                
                # Extract date from key (format: sim_<series_name>:YYYY-MM-DD:<granularity>)
                parts = key_str.split(':')
                if len(parts) < 3:
                    continue
                    
                date_str = parts[1]
                key_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                
                # Calculate age in days
                age_days = (current_date - key_date).days
                
                # Get granularity and retention period
                granularity = parts[2]
                try:
                    retention_days = RETENTION_PERIODS[TimeSeriesGranularity(granularity)]
                except (KeyError, ValueError):
                    retention_days = RETENTION_PERIODS[TimeSeriesGranularity.MINUTE]
                
                # Delete if beyond retention period
                if age_days > retention_days:
                    redis_conn.delete(key_str)
                    
            except (ValueError, IndexError) as e:
                print(f"Error processing key {key}: {e}")
                continue
        
        return len(all_keys)
        
    except Exception as e:
        print(f"Error cleaning up old data: {e}")
        return 0

def schedule_compression_task(series_name: str, date: Optional[datetime.date] = None):
    """
    Schedule a compression task for the specified date.
    This should be called at the end of each day to compress that day's data.
    
    Args:
        series_name: Name of the time series (e.g., 'price_history')
        date: Date to compress, defaults to yesterday
    """
    if date is None:
        # Default to yesterday
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    try:
        # Compress minute data to hourly
        minute_to_hourly = compress_historical_data(
            series_name, 
            date,
            TimeSeriesGranularity.MINUTE,
            TimeSeriesGranularity.HOURLY
        )
        
        # Compress hourly data to daily
        hourly_to_daily = compress_historical_data(
            series_name,
            date,
            TimeSeriesGranularity.HOURLY,
            TimeSeriesGranularity.DAILY
        )
        
        # Clean up old data
        deleted = cleanup_old_data(series_name, datetime.date.today())
        
        print(f"Compression results for {date.isoformat()}:")
        print(f"  Minute → Hourly: {'Success' if minute_to_hourly else 'Failed'}")
        print(f"  Hourly → Daily: {'Success' if hourly_to_daily else 'Failed'}")
        print(f"  Deleted {deleted} expired keys")
        
        return minute_to_hourly and hourly_to_daily
    except Exception as e:
        print(f"Error scheduling compression task: {e}")
        return False

class MLTrainingData(TypedDict):
    """Type definition for ML training data"""
    timestamp: str
    label: str
    confidence: float
    features: Dict[str, Union[float, int]]  # Allow both float and int values
    market_regime: str  # Added as separate field

class GrafanaMetrics(TypedDict):
    """Type definition for Grafana metrics"""
    trap_count: int
    confidence_avg: float
    price_change_avg: float
    volatility: float

def validate_features(features: Dict[str, Any]) -> bool:
    """
    Validate that all feature values are numeric.
    
    Args:
        features: Dictionary of features to validate
        
    Returns:
        bool: True if all features are valid
    """
    try:
        for key, value in features.items():
            if not isinstance(value, (int, float)):
                print(f"Invalid feature value for {key}: {value}")
                return False
        return True
    except Exception as e:
        print(f"Error validating features: {e}")
        return False

def store_ml_training_data(
    trap_data: Dict[str, Any],
    market_data: Dict[str, Any]
) -> bool:
    """
    Store ML training data in Redis for external model training.
    
    Args:
        trap_data: Dictionary containing trap detection data
        market_data: Dictionary containing market state data
        
    Returns:
        bool: True if storage was successful
    """
    try:
        # Extract technical indicators
        technical = market_data.get("technical_indicators", {})
        volume = market_data.get("volume_metrics", {})
        context = market_data.get("market_context", {})
        
        # Combine all features
        features = {
            # Base trap features
            **trap_data.get("features", {}),
            
            # Market data
            "price": market_data["price"],
            "volume_24h": market_data["volume_24h"],
            "market_volatility": market_data["volatility"],
            
            # Technical indicators
            "rsi_14": technical.get("rsi_14", 0.0),
            "macd": technical.get("macd", 0.0),
            "macd_signal": technical.get("macd_signal", 0.0),
            "bb_upper": technical.get("bb_upper", 0.0),
            "bb_lower": technical.get("bb_lower", 0.0),
            "ma_50": technical.get("ma_50", 0.0),
            "ma_200": technical.get("ma_200", 0.0),
            
            # Volume metrics
            "buy_volume_ratio": volume.get("buy_volume_ratio", 0.0),
            "volume_ma_ratio": volume.get("volume_ma_ratio", 0.0),
            "large_trades_ratio": volume.get("large_trades_ratio", 0.0),
            
            # Market context
            "funding_rate": context.get("funding_rate", 0.0),
            "open_interest": context.get("open_interest", 0.0),
            "long_short_ratio": context.get("long_short_ratio", 0.0)
        }
        
        # Validate features
        if not validate_features(features):
            return False
            
        # Create training data entry
        training_data: MLTrainingData = {
            "timestamp": trap_data["timestamp"],
            "label": trap_data["trap_type"],
            "confidence": trap_data["confidence"],
            "features": features,
            "market_regime": market_data["regime"]
        }
        
        # Store in Redis
        redis_conn.rpush("sim_ml_training_data", json.dumps(training_data))
        
        # Set reasonable expiration (30 days)
        redis_conn.expire("sim_ml_training_data", 86400 * 30)
        
        return True
    except Exception as e:
        print(f"Error storing ML training data: {e}")
        return False

def export_ml_training_data(
    start_date: datetime.date,
    end_date: Optional[datetime.date] = None
) -> List[MLTrainingData]:
    """
    Export ML training data for external model consumption.
    
    Args:
        start_date: Start date for data export
        end_date: Optional end date (defaults to today)
        
    Returns:
        List of training data entries
    """
    try:
        if end_date is None:
            end_date = datetime.date.today()
            
        # Get all training data
        data_bytes = redis_conn.lrange("sim_ml_training_data", 0, -1)
        
        # Parse and filter by date range
        training_data = []
        for item in data_bytes:
            entry = json.loads(item)
            entry_date = datetime.datetime.strptime(
                entry["timestamp"],
                "%Y-%m-%d %H:%M:%S"
            ).date()
            
            if start_date <= entry_date <= end_date:
                training_data.append(entry)
        
        return training_data
    except Exception as e:
        print(f"Error exporting ML training data: {e}")
        return []

def store_grafana_metrics(
    timestamp: datetime.datetime,
    metrics: GrafanaMetrics
) -> bool:
    """
    Store metrics for Grafana visualization.
    
    Args:
        timestamp: Timestamp for the metrics
        metrics: Dictionary of metric values
        
    Returns:
        bool: True if storage was successful
    """
    try:
        # Create key with timestamp
        key = f"sim_grafana_metrics:{timestamp.strftime('%Y-%m-%d:%H')}"
        
        # Store metrics
        redis_conn.hset(key, mapping={
            k: str(v) for k, v in metrics.items()
        })
        
        # Set expiration (7 days)
        redis_conn.expire(key, 86400 * 7)
        
        return True
    except Exception as e:
        print(f"Error storing Grafana metrics: {e}")
        return False

def export_grafana_dashboard(
    start_time: datetime.datetime,
    end_time: datetime.datetime
) -> Dict[str, Any]:
    """
    Export data in Grafana dashboard format.
    
    Args:
        start_time: Start time for dashboard data
        end_time: End time for dashboard data
        
    Returns:
        Dictionary containing Grafana dashboard configuration
    """
    try:
        # Get metrics for time range
        metrics_data = []
        current = start_time
        
        while current <= end_time:
            key = f"sim_grafana_metrics:{current.strftime('%Y-%m-%d:%H')}"
            data = redis_conn.hgetall(key)
            
            if data:
                metrics = {
                    k.decode('utf-8'): float(v.decode('utf-8'))
                    for k, v in data.items()
                }
                metrics["timestamp"] = current.isoformat()
                metrics_data.append(metrics)
                
            current += datetime.timedelta(hours=1)
        
        # Create Grafana dashboard configuration
        dashboard = {
            "dashboard": {
                "id": None,
                "title": "Market Maker Trap Detection",
                "tags": ["btc", "market-maker", "traps"],
                "timezone": "browser",
                "refresh": "5s",
                "schemaVersion": 21,
                "version": 0,
                "time": {
                    "from": start_time.isoformat(),
                    "to": end_time.isoformat()
                }
            },
            "datasource": {
                "type": "redis-datasource",
                "uid": "redis_omega"
            },
            "panels": [
                {
                    "id": 1,
                    "title": "Trap Detection Count",
                    "type": "graph",
                    "datasource": "${DS_REDIS}",
                    "targets": [{
                        "query": "trap_count",
                        "type": "timeseries"
                    }]
                },
                {
                    "id": 2,
                    "title": "Average Confidence",
                    "type": "gauge",
                    "datasource": "${DS_REDIS}",
                    "targets": [{
                        "query": "confidence_avg",
                        "type": "timeseries"
                    }]
                },
                {
                    "id": 3,
                    "title": "Price Change %",
                    "type": "graph",
                    "datasource": "${DS_REDIS}",
                    "targets": [{
                        "query": "price_change_avg",
                        "type": "timeseries"
                    }]
                },
                {
                    "id": 4,
                    "title": "Market Volatility",
                    "type": "heatmap",
                    "datasource": "${DS_REDIS}",
                    "targets": [{
                        "query": "volatility",
                        "type": "timeseries"
                    }]
                }
            ],
            "data": metrics_data
        }
        
        return dashboard
    except Exception as e:
        print(f"Error exporting Grafana dashboard: {e}")
        return {} 