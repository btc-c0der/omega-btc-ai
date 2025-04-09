#!/usr/bin/env python3

"""
Database manager for the OMEGA BTC AI system.
Handles storage and retrieval of price movements, trend analysis, and market maker traps.
"""

import json
import logging
import sqlite3
import time
import os
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timezone
import redis

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Database configuration
DB_PATH = os.getenv('DB_PATH', 'omega_btc_ai.db')

# Redis connection
try:
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)
    redis_conn.ping()
    logger.info(f"Successfully connected to Redis at {redis_host}:{redis_port}")
except redis.ConnectionError as e:
    logger.error(f"Failed to connect to Redis: {e}")
    redis_conn = None

def get_db_connection():
    """Return the Redis connection object.
    
    Returns:
        Redis connection object or None if connection failed
    """
    return redis_conn

def initialize_database() -> None:
    """Initialize the database with required tables."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Table for storing BTC price movements
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            price REAL NOT NULL,
            volume REAL,
            timestamp TEXT NOT NULL,
            interval INTEGER NOT NULL,
            change_pct REAL,
            abs_change REAL
        )
        ''')
        
        # Table for storing market maker trap detections
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS mm_traps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            timeframe TEXT,
            confidence REAL NOT NULL,
            price_change REAL NOT NULL,
            price REAL,
            timestamp TEXT NOT NULL,
            validated INTEGER DEFAULT 0,
            validation_score REAL,
            fibonacci_level TEXT,
            volume_anomaly TEXT
        )
        ''')
        
        # Table for storing trend analysis
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS trend_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timeframe INTEGER NOT NULL,
            trend TEXT NOT NULL,
            change_pct REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
        ''')
        
        # Table for Fibonacci level detections
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS fibonacci_detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level_name TEXT NOT NULL,
            price REAL NOT NULL,
            current_price REAL NOT NULL,
            distance_pct REAL NOT NULL,
            confidence REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("Database initialized successfully")
        
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        raise

def insert_price_movement(price: float, volume: Optional[float] = None, 
                          interval: int = 1, change_pct: Optional[float] = None,
                          abs_change: Optional[float] = None) -> int:
    """
    Insert a price movement record into the database.
    
    Args:
        price: Current BTC price
        volume: Optional trading volume
        interval: Time interval in minutes
        change_pct: Optional percentage change
        abs_change: Optional absolute change
        
    Returns:
        int: ID of the inserted record
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        cursor.execute(
            '''
            INSERT INTO price_movements 
            (price, volume, timestamp, interval, change_pct, abs_change)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (price, volume, timestamp, interval, change_pct, abs_change)
        )
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Also update Redis cache if available
        if redis_conn:
            try:
                # Store price in Redis
                redis_conn.set("last_btc_price", str(price))
                
                # Store volume if provided
                if volume is not None:
                    redis_conn.set("last_btc_volume", str(volume))
                
                # Add to movement history
                if volume is not None:
                    movement_str = f"{price},{volume}"
                else:
                    movement_str = str(price)
                    
                redis_conn.lpush("btc_movement_history", movement_str)
                redis_conn.ltrim("btc_movement_history", 0, 999)  # Keep last 1000 entries
                
                # Store change percentage if provided
                if change_pct is not None:
                    redis_conn.lpush("btc_change_history", str(change_pct))
                    redis_conn.ltrim("btc_change_history", 0, 999)  # Keep last 1000 entries
                
                # Store absolute change if provided
                if abs_change is not None:
                    redis_conn.lpush("abs_price_change_history", str(abs_change))
                    redis_conn.ltrim("abs_price_change_history", 0, 999)  # Keep last 1000 entries
            except Exception as e:
                logger.warning(f"Failed to update Redis cache: {e}")
        
        return record_id
        
    except sqlite3.Error as e:
        logger.error(f"Error inserting price movement: {e}")
        return -1

def insert_trend_analysis(timeframe: int, trend: str, change_pct: float) -> int:
    """
    Insert a trend analysis record into the database.
    
    Args:
        timeframe: Time interval in minutes
        trend: Trend description (e.g., "Bullish", "Bearish")
        change_pct: Percentage price change
        
    Returns:
        int: ID of the inserted record
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        cursor.execute(
            '''
            INSERT INTO trend_analysis 
            (timeframe, trend, change_pct, timestamp)
            VALUES (?, ?, ?, ?)
            ''',
            (timeframe, trend, change_pct, timestamp)
        )
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Also update Redis cache if available
        if redis_conn:
            try:
                # Store trend analysis in Redis
                trend_data = {
                    "timeframe": timeframe,
                    "trend": trend,
                    "change_pct": change_pct,
                    "timestamp": timestamp
                }
                
                redis_conn.set(f"btc_trend_{timeframe}min", json.dumps(trend_data))
            except Exception as e:
                logger.warning(f"Failed to update Redis cache: {e}")
        
        return record_id
        
    except sqlite3.Error as e:
        logger.error(f"Error inserting trend analysis: {e}")
        return -1

def insert_possible_mm_trap(trap_data: Dict[str, Any]) -> int:
    """
    Insert a possible market maker trap detection into the database.
    
    Args:
        trap_data: Dictionary with trap detection data
            Required keys: type
            Optional keys: timeframe, confidence, price_change, price,
                          fibonacci_level, volume_anomaly
        
    Returns:
        int: ID of the inserted record
    """
    try:
        # Ensure required fields are present
        if "type" not in trap_data:
            logger.error("Missing required field 'type' in trap data")
            return -1
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Set default values
        trap_type = trap_data.get("type")
        timeframe = trap_data.get("timeframe")
        confidence = trap_data.get("confidence", 0.5)
        price_change = trap_data.get("price_change", 0.0)
        price = trap_data.get("price", 0.0)
        timestamp = trap_data.get("timestamp", datetime.now(timezone.utc).isoformat())
        validated = trap_data.get("validated", 0)
        validation_score = trap_data.get("validation_score", 0.0)
        fibonacci_level = trap_data.get("fibonacci_level")
        volume_anomaly = trap_data.get("volume_anomaly")
        
        # Convert complex objects to JSON strings
        if fibonacci_level and isinstance(fibonacci_level, dict):
            fibonacci_level = json.dumps(fibonacci_level)
            
        if volume_anomaly and isinstance(volume_anomaly, dict):
            volume_anomaly = json.dumps(volume_anomaly)
        
        cursor.execute(
            '''
            INSERT INTO mm_traps 
            (type, timeframe, confidence, price_change, price, timestamp, 
             validated, validation_score, fibonacci_level, volume_anomaly)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (trap_type, timeframe, confidence, price_change, price, timestamp,
             validated, validation_score, fibonacci_level, volume_anomaly)
        )
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Also update Redis cache if available
        if redis_conn:
            try:
                # Increment trap counter
                redis_conn.incr(f"mm_trap_count_{trap_type.replace(' ', '_').lower()}")
                
                # Store latest trap detection
                redis_conn.set("latest_mm_trap", json.dumps({
                    "id": record_id,
                    "type": trap_type,
                    "timeframe": timeframe,
                    "confidence": confidence,
                    "price_change": price_change,
                    "timestamp": timestamp
                }))
                
                # Add to recent traps list
                redis_conn.lpush("recent_mm_traps", json.dumps({
                    "id": record_id,
                    "type": trap_type,
                    "timeframe": timeframe,
                    "confidence": confidence,
                    "price_change": price_change,
                    "timestamp": timestamp
                }))
                
                redis_conn.ltrim("recent_mm_traps", 0, 49)  # Keep last 50 traps
            except Exception as e:
                logger.warning(f"Failed to update Redis cache: {e}")
        
        return record_id
        
    except sqlite3.Error as e:
        logger.error(f"Error inserting MM trap: {e}")
        return -1

def insert_fibonacci_detection(level_name: str, price: float, current_price: float,
                              distance_pct: float, confidence: float) -> int:
    """
    Insert a Fibonacci level detection into the database.
    
    Args:
        level_name: Name of the Fibonacci level
        price: Price at the Fibonacci level
        current_price: Current BTC price
        distance_pct: Percentage distance from level
        confidence: Confidence score
        
    Returns:
        int: ID of the inserted record
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        cursor.execute(
            '''
            INSERT INTO fibonacci_detections 
            (level_name, price, current_price, distance_pct, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (level_name, price, current_price, distance_pct, confidence, timestamp)
        )
        
        record_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Also update Redis cache if available
        if redis_conn:
            try:
                # Store latest Fibonacci detection
                redis_conn.set("latest_fibonacci_detection", json.dumps({
                    "id": record_id,
                    "level_name": level_name,
                    "price": price,
                    "current_price": current_price,
                    "distance_pct": distance_pct,
                    "confidence": confidence,
                    "timestamp": timestamp
                }))
            except Exception as e:
                logger.warning(f"Failed to update Redis cache: {e}")
        
        return record_id
        
    except sqlite3.Error as e:
        logger.error(f"Error inserting Fibonacci detection: {e}")
        return -1

def fetch_multi_interval_movements(interval: int = 5, limit: int = 100) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Fetch price movements for a specific interval with summary statistics.
    
    Args:
        interval: Time interval in minutes
        limit: Maximum number of records to fetch
        
    Returns:
        Tuple of (movements list, summary dictionary)
    """
    try:
        # First try to get from Redis cache if available
        if redis_conn:
            try:
                cached_movements = redis_conn.get(f"cached_movements_{interval}min")
                cached_summary = redis_conn.get(f"cached_summary_{interval}min")
                
                if cached_movements and cached_summary:
                    return json.loads(cached_movements), json.loads(cached_summary)
            except Exception as e:
                logger.warning(f"Failed to get from Redis cache: {e}")
        
        # If not in cache or Redis not available, get from database
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            '''
            SELECT * FROM price_movements
            WHERE interval = ?
            ORDER BY timestamp DESC
            LIMIT ?
            ''',
            (interval, limit)
        )
        
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries
        movements = []
        for row in rows:
            movements.append(dict(row))
        
        # Calculate summary statistics
        summary = {}
        
        if movements:
            prices = [m["price"] for m in movements]
            changes = [m["change_pct"] for m in movements if m["change_pct"] is not None]
            
            summary = {
                "count": len(movements),
                "latest_price": movements[0]["price"] if movements else 0,
                "avg_price": sum(prices) / len(prices) if prices else 0,
                "min_price": min(prices) if prices else 0,
                "max_price": max(prices) if prices else 0,
                "avg_change": sum(changes) / len(changes) if changes else 0,
                "interval": interval
            }
        
        conn.close()
        
        # Cache in Redis if available
        if redis_conn:
            try:
                redis_conn.set(f"cached_movements_{interval}min", json.dumps(movements))
                redis_conn.expire(f"cached_movements_{interval}min", 60)  # Expire in 60 seconds
                
                redis_conn.set(f"cached_summary_{interval}min", json.dumps(summary))
                redis_conn.expire(f"cached_summary_{interval}min", 60)  # Expire in 60 seconds
            except Exception as e:
                logger.warning(f"Failed to cache in Redis: {e}")
        
        return movements, summary
        
    except sqlite3.Error as e:
        logger.error(f"Error fetching price movements: {e}")
        return [], {}

def fetch_recent_mm_traps(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch recent market maker trap detections.
    
    Args:
        limit: Maximum number of records to fetch
        
    Returns:
        List of trap detections
    """
    try:
        # First try to get from Redis cache if available
        if redis_conn:
            try:
                cached_traps = redis_conn.lrange("recent_mm_traps", 0, limit - 1)
                if cached_traps:
                    return [json.loads(trap) for trap in cached_traps]
            except Exception as e:
                logger.warning(f"Failed to get from Redis cache: {e}")
        
        # If not in cache or Redis not available, get from database
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            '''
            SELECT * FROM mm_traps
            ORDER BY timestamp DESC
            LIMIT ?
            ''',
            (limit,)
        )
        
        rows = cursor.fetchall()
        
        # Convert to list of dictionaries
        traps = []
        for row in rows:
            trap = dict(row)
            
            # Parse JSON strings
            if trap["fibonacci_level"]:
                try:
                    trap["fibonacci_level"] = json.loads(trap["fibonacci_level"])
                except:
                    pass
                
            if trap["volume_anomaly"]:
                try:
                    trap["volume_anomaly"] = json.loads(trap["volume_anomaly"])
                except:
                    pass
            
            traps.append(trap)
        
        conn.close()
        
        # Cache in Redis if available
        if redis_conn and traps:
            try:
                redis_conn.delete("recent_mm_traps")
                for trap in traps:
                    redis_conn.rpush("recent_mm_traps", json.dumps(trap))
            except Exception as e:
                logger.warning(f"Failed to cache in Redis: {e}")
        
        return traps
        
    except sqlite3.Error as e:
        logger.error(f"Error fetching MM traps: {e}")
        return []

def validate_price_change(change_pct: float, timeframe_minutes: int) -> Tuple[bool, str]:
    """
    Validate if a price change percentage is realistic for the given timeframe.
    
    Args:
        change_pct: The percentage change to validate
        timeframe_minutes: The timeframe in minutes
        
    Returns:
        Tuple of (is_valid, reason)
    """
    # Define maximum allowed percentage changes based on timeframe
    # These are reasonable limits that can be adjusted based on market volatility
    max_changes = {
        1: 5.0,      # 1min: max 5% change
        5: 8.0,      # 5min: max 8% change
        15: 12.0,    # 15min: max 12% change
        30: 15.0,    # 30min: max 15% change
        60: 20.0,    # 1hr: max 20% change
        240: 30.0,   # 4hr: max 30% change
        720: 40.0,   # 12hr: max 40% change
        1440: 50.0,  # 24hr: max 50% change
    }
    
    # Get the maximum allowed change for this timeframe
    max_allowed = max_changes.get(timeframe_minutes, 50.0)
    
    # Check if the change exceeds the maximum allowed (in either direction)
    if abs(change_pct) > max_allowed:
        return False, f"Price change of {change_pct:.2f}% exceeds maximum of {max_allowed:.2f}% for {timeframe_minutes}min timeframe"
    
    return True, "Valid price change"

def format_price(price: float) -> str:
    """
    Format a price value consistently.
    
    Args:
        price: The price to format
        
    Returns:
        Formatted price string with commas and 2 decimal places
    """
    return f"${price:,.2f}"

def format_percentage(percentage: float) -> str:
    """
    Format a percentage value consistently.
    
    Args:
        percentage: The percentage to format
        
    Returns:
        Formatted percentage string with 2 decimal places and % sign
    """
    if percentage is None:
        percentage = 0.0
    elif isinstance(percentage, str):
        try:
            percentage = float(percentage)
        except ValueError:
            percentage = 0.0
    
    return f"{percentage:.2f}%"

def get_fallback_trend_data(minutes: int) -> Tuple[str, float]:
    """
    Get fallback trend data when primary sources are unavailable.
    Uses multiple fallback mechanisms in a cascading manner.
    
    Args:
        minutes: Timeframe in minutes
        
    Returns:
        Tuple of (trend_description, percent_change)
    """
    logger.info(f"Using fallback mechanism for {minutes}min trend data")
    
    # Fallback 1: Try to get data from a nearby timeframe
    nearby_timeframes = [1, 5, 15, 30, 60, 240, 720, 1440]
    nearby_timeframes.sort(key=lambda x: abs(x - minutes))
    
    for tf in nearby_timeframes[1:3]:  # Try the 2 closest timeframes
        try:
            if redis_conn:
                cached_trend = redis_conn.get(f"btc_trend_{tf}min")
                if cached_trend:
                    trend_data = json.loads(cached_trend)
                    logger.info(f"Using {tf}min data as fallback for {minutes}min")
                    change_pct = trend_data.get("change_pct", 0.0)
                    # Ensure change_pct is a float
                    if isinstance(change_pct, str):
                        try:
                            change_pct = float(change_pct)
                        except ValueError:
                            change_pct = 0.0
                    return trend_data.get("trend", "Neutral"), change_pct
        except Exception as e:
            logger.warning(f"Failed to get fallback data from {tf}min: {e}")
    
    # Fallback 2: Try to calculate from price history
    try:
        if redis_conn:
            price_history = redis_conn.lrange("btc_movement_history", 0, 1)
            if len(price_history) >= 2:
                # Parse price history entries
                latest_price = float(price_history[0].split(",")[0])
                reference_price = float(price_history[-1].split(",")[0])
                
                if reference_price > 0:
                    change_pct = ((latest_price - reference_price) / reference_price) * 100
                    
                    # Determine trend
                    if change_pct > 3.0:
                        trend = "Strongly Bullish"
                    elif change_pct > 0.5:
                        trend = "Bullish"
                    elif change_pct < -3.0:
                        trend = "Strongly Bearish"
                    elif change_pct < -0.5:
                        trend = "Bearish"
                    else:
                        trend = "Neutral"
                        
                    logger.info(f"Calculated fallback trend from price history: {trend} ({change_pct:.2f}%)")
                    return trend, change_pct
    except Exception as e:
        logger.warning(f"Failed to calculate trend from price history: {e}")
    
    # Fallback 3: Default to neutral with zero change
    logger.warning(f"All fallback mechanisms failed for {minutes}min, using default neutral")
    return "Neutral", 0.0

def analyze_price_trend(minutes: int) -> Tuple[str, float]:
    """
    Analyze price trend for the given timeframe with enhanced validation and fallbacks.
    
    Args:
        minutes: Time interval in minutes
        
    Returns:
        Tuple of (trend_description, percent_change)
    """
    try:
        # First check if we have cached results in Redis
        if redis_conn:
            try:
                cached_trend = redis_conn.get(f"btc_trend_{minutes}min")
                if cached_trend:
                    trend_data = json.loads(cached_trend)
                    now = datetime.now(timezone.utc)
                    timestamp = datetime.fromisoformat(trend_data.get("timestamp", now.isoformat()))
                    
                    # Also validate cached data
                    age_minutes = (now - timestamp).total_seconds() / 60
                    if age_minutes < 1.0 and "trend" in trend_data and "change_pct" in trend_data:
                        # Ensure the change_pct is a float
                        change_pct = trend_data["change_pct"]
                        if isinstance(change_pct, str):
                            try:
                                change_pct = float(change_pct)
                            except ValueError:
                                change_pct = 0.0
                        # Return cached result
                        return trend_data["trend"], float(change_pct)
            except Exception as e:
                logger.warning(f"Failed to retrieve cached trend for {minutes}min: {e}")
        
        # If no valid cached data, calculate trend
        # Get price data from database
        price_data, _ = fetch_multi_interval_movements(minutes)
        
        if not price_data or len(price_data) < 2:
            logger.warning(f"Missing price data for {minutes}min trend analysis")
            return get_fallback_trend_data(minutes)
            
        # Extract current and old prices
        try:
            current_candle = price_data[0]
            old_candle = price_data[-1]
            
            # Check for invalid price data
            if not isinstance(current_candle, dict) or not isinstance(old_candle, dict):
                logger.warning(f"Invalid candle data format for {minutes}min")
                return get_fallback_trend_data(minutes)
                
            # Safely access candle data
            current_price = current_candle.get('c', 0)
            reference_price = old_candle.get('o', 0)
            
            # Ensure values are floats
            if isinstance(current_price, str):
                try:
                    current_price = float(current_price)
                except ValueError:
                    current_price = 0.0
            if isinstance(reference_price, str):
                try:
                    reference_price = float(reference_price)
                except ValueError:
                    reference_price = 0.0
                    
            if current_price <= 0 or reference_price <= 0:
                logger.warning(f"Invalid price values (0 or negative) for {minutes}min trend analysis")
                return get_fallback_trend_data(minutes)
            
            # Calculate price change
            price_diff = current_price - reference_price
            percent_change = (price_diff / reference_price) * 100
            
            # Validate the calculated change
            is_valid, reason = validate_price_change(percent_change, minutes)
            if not is_valid:
                logger.warning(reason)
                # Cap the change to maximum allowed
                max_changes = {
                    1: 5.0, 5: 8.0, 15: 12.0, 30: 15.0, 
                    60: 20.0, 240: 30.0, 720: 40.0, 1440: 50.0
                }
                max_allowed = max_changes.get(minutes, 50.0)
                # Preserve direction but cap magnitude
                if percent_change > 0:
                    percent_change = min(percent_change, max_allowed)
                else:
                    percent_change = max(percent_change, -max_allowed)
            
            # Classify the trend based on percentage change
            if percent_change > 3.0:
                trend = "Strongly Bullish"
            elif percent_change > 0.5:
                trend = "Bullish"
            elif percent_change < -3.0:
                trend = "Strongly Bearish"
            elif percent_change < -0.5:
                trend = "Bearish"
            else:
                trend = "Neutral"
                
            # Log the result
            logger.info(f"Analyzed {minutes}min trend: {trend} ({percent_change:.2f}%) from {format_price(reference_price)} to {format_price(current_price)}")
            
            # Cache the result in Redis
            try:
                if redis_conn:
                    result = {
                        "trend": trend,
                        "change_pct": percent_change,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                    redis_conn.set(f"btc_trend_{minutes}min", json.dumps(result))
            except Exception as e:
                logger.warning(f"Failed to cache trend result: {e}")
                
            return trend, percent_change
            
        except (IndexError, KeyError, TypeError) as e:
            logger.warning(f"Error accessing price data for {minutes}min: {e}")
            return get_fallback_trend_data(minutes)
            
    except Exception as e:
        logger.error(f"Error in trend analysis for {minutes}min: {e}")
        return get_fallback_trend_data(minutes)

# Ensure database is initialized
try:
    initialize_database()
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")

# Module testing
if __name__ == "__main__":
    # Test database functionality
    print("Testing database functionality...")
    
    # Insert test price movement
    price_id = insert_price_movement(
        price=59000.0,
        volume=1200.5,
        interval=5,
        change_pct=0.5,
        abs_change=300.0
    )
    
    print(f"Inserted price movement with ID: {price_id}")
    
    # Insert test trap
    trap_id = insert_possible_mm_trap({
        "type": "Bull Trap",
        "timeframe": "15min",
        "confidence": 0.75,
        "price_change": 1.5,
        "price": 59000.0
    })
    
    print(f"Inserted MM trap with ID: {trap_id}")
    
    # Test fetching movements
    movements, summary = fetch_multi_interval_movements(interval=5, limit=10)
    print(f"Fetched {len(movements)} movements for 5-minute interval")
    print(f"Summary: {summary}")
    
    # Test trend analysis
    trend, change = analyze_price_trend(15)
    print(f"15-minute trend: {trend} ({change:.2f}%)")
    
    print("Database tests completed")