#!/usr/bin/env python3

"""
Database manager for OmegaBTC AI trading simulations.
Provides PostgreSQL connection and schema for storing trading metrics.
"""

import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor, Json
import datetime
from typing import Dict, List, Any, Optional
import redis
import json
from datetime import datetime, timedelta

class DatabaseManager:
    """Manages database connections and operations for OmegaBTC AI."""
    
    def __init__(self, 
                host: str = "localhost", 
                port: int = 5432,
                dbname: str = "omega_btc",
                user: str = "postgres",
                password: str = None,
                redis_host='localhost', 
                redis_port=6379, 
                redis_db=0):
        """Initialize the database manager."""
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password or os.environ.get("POSTGRES_PASSWORD", "")
        self.conn = None
        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True
        )
        
    def connect(self) -> None:
        """Establish connection to PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            print(f"Connected to database {self.dbname} on {self.host}")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def initialize_schema(self) -> None:
        """Create required tables and indexes if they don't exist."""
        if not self.conn:
            self.connect()
        
        with self.conn.cursor() as cur:
            # Create traders table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS traders (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    profile_type VARCHAR(50) NOT NULL,
                    initial_capital DECIMAL(16,8) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                );
            """)
            
            # Create trades table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id SERIAL PRIMARY KEY,
                    trader_id INTEGER REFERENCES traders(id),
                    direction VARCHAR(10) NOT NULL,
                    entry_price DECIMAL(16,8) NOT NULL,
                    exit_price DECIMAL(16,8),
                    position_size DECIMAL(16,8) NOT NULL,
                    leverage INTEGER NOT NULL,
                    entry_reason TEXT NOT NULL,
                    exit_reason TEXT,
                    entry_time TIMESTAMP NOT NULL DEFAULT NOW(),
                    exit_time TIMESTAMP,
                    pnl DECIMAL(16,8),
                    fee DECIMAL(16,8) DEFAULT 0,
                    stop_loss DECIMAL(16,8),
                    emotional_state VARCHAR(50),
                    risk_reward_ratio DECIMAL(8,4),
                    market_condition JSON,
                    trade_duration_hours DECIMAL(10,4),
                    take_profits JSON,
                    trailing_stop BOOLEAN DEFAULT FALSE,
                    status VARCHAR(20) DEFAULT 'OPEN',
                    signal_type VARCHAR(50),
                    liquidated BOOLEAN DEFAULT FALSE
                );
            """)
            
            # Create trade_exits table for partial exits
            cur.execute("""
                CREATE TABLE IF NOT EXISTS trade_exits (
                    id SERIAL PRIMARY KEY,
                    trade_id INTEGER REFERENCES trades(id),
                    exit_type VARCHAR(50) NOT NULL,
                    exit_price DECIMAL(16,8) NOT NULL,
                    exit_time TIMESTAMP NOT NULL DEFAULT NOW(),
                    percentage DECIMAL(5,4) NOT NULL,
                    pnl DECIMAL(16,8) NOT NULL,
                    price_bar INTEGER,
                    reason TEXT
                );
            """)
            
            # Create trader_metrics table for time-series metric storage
            cur.execute("""
                CREATE TABLE IF NOT EXISTS trader_metrics (
                    id SERIAL PRIMARY KEY,
                    trader_id INTEGER REFERENCES traders(id),
                    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
                    current_capital DECIMAL(16,8) NOT NULL,
                    total_pnl DECIMAL(16,8) NOT NULL,
                    drawdown_percentage DECIMAL(8,4) NOT NULL,
                    win_rate DECIMAL(8,4) NOT NULL, 
                    total_trades INTEGER NOT NULL,
                    winning_trades INTEGER NOT NULL,
                    losing_trades INTEGER NOT NULL,
                    avg_win DECIMAL(16,8),
                    avg_loss DECIMAL(16,8),
                    emotional_state VARCHAR(50),
                    confidence_level DECIMAL(4,2),
                    risk_appetite DECIMAL(4,2),
                    avg_trade_duration_hours DECIMAL(10,4),
                    extra_metrics JSON
                );
            """)
            
            # Create indexes for better query performance
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trades_trader_id ON trades(trader_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trades_entry_time ON trades(entry_time);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trades_status ON trades(status);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trade_exits_trade_id ON trade_exits(trade_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trader_metrics_trader_id_timestamp ON trader_metrics(trader_id, timestamp);")
            
            self.conn.commit()
            print("Database schema initialized successfully")
    
    def save_trader(self, name: str, profile_type: str, initial_capital: float) -> int:
        """Save trader information and return the trader ID."""
        if not self.conn:
            self.connect()
            
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO traders (name, profile_type, initial_capital)
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (name, profile_type, initial_capital))
            trader_id = cur.fetchone()[0]
            self.conn.commit()
            return trader_id
    
    def save_trade(self, trade_data: Dict[str, Any]) -> int:
        """Save trade entry information and return the trade ID."""
        if not self.conn:
            self.connect()
            
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO trades (
                    trader_id, direction, entry_price, position_size, leverage,
                    entry_reason, stop_loss, emotional_state, market_condition,
                    signal_type, take_profits
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                trade_data["trader_id"],
                trade_data["direction"],
                trade_data["entry_price"],
                trade_data["position_size"],
                trade_data["leverage"],
                trade_data["entry_reason"],
                trade_data["stop_loss"],
                trade_data["emotional_state"],
                Json(trade_data["market_condition"]),
                trade_data["signal_type"],
                Json(trade_data["take_profits"])
            ))
            trade_id = cur.fetchone()[0]
            self.conn.commit()
            return trade_id
    
    def save_trade_exit(self, exit_data: Dict[str, Any]) -> None:
        """Save trade exit information."""
        if not self.conn:
            self.connect()
            
        with self.conn.cursor() as cur:
            # Insert exit record
            cur.execute("""
                INSERT INTO trade_exits (
                    trade_id, exit_type, exit_price, percentage, 
                    pnl, price_bar, reason
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (
                exit_data["trade_id"],
                exit_data["exit_type"],
                exit_data["exit_price"],
                exit_data["percentage"],
                exit_data["pnl"],
                exit_data["price_bar"],
                exit_data["reason"]
            ))
            
            # If this is a complete exit, update the trade record
            if exit_data.get("is_complete", False):
                cur.execute("""
                    UPDATE trades
                    SET exit_price = %s, 
                        exit_time = NOW(),
                        pnl = %s,
                        exit_reason = %s,
                        trade_duration_hours = %s,
                        status = 'CLOSED',
                        liquidated = %s
                    WHERE id = %s;
                """, (
                    exit_data["exit_price"],
                    exit_data["total_pnl"],
                    exit_data["reason"],
                    exit_data["duration_hours"],
                    exit_data.get("liquidated", False),
                    exit_data["trade_id"]
                ))
            
            self.conn.commit()
    
    def save_trader_metrics(self, metrics_data: Dict[str, Any]) -> None:
        """Save periodic trader performance metrics."""
        if not self.conn:
            self.connect()
            
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO trader_metrics (
                    trader_id, current_capital, total_pnl, drawdown_percentage,
                    win_rate, total_trades, winning_trades, losing_trades,
                    avg_win, avg_loss, emotional_state, confidence_level,
                    risk_appetite, avg_trade_duration_hours, extra_metrics
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                metrics_data["trader_id"],
                metrics_data["current_capital"],
                metrics_data["total_pnl"],
                metrics_data["drawdown_percentage"],
                metrics_data["win_rate"],
                metrics_data["total_trades"],
                metrics_data["winning_trades"],
                metrics_data["losing_trades"],
                metrics_data.get("avg_win", 0),
                metrics_data.get("avg_loss", 0),
                metrics_data["emotional_state"],
                metrics_data["confidence_level"],
                metrics_data["risk_appetite"],
                metrics_data.get("avg_trade_duration", 0),
                Json(metrics_data.get("extra_metrics", {}))
            ))
            self.conn.commit()
    
    def get_trader_trades(self, trader_id: int) -> List[Dict]:
        """Get all trades for a specific trader."""
        if not self.conn:
            self.connect()
            
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT * FROM trades
                WHERE trader_id = %s
                ORDER BY entry_time DESC;
            """, (trader_id,))
            return [dict(row) for row in cur.fetchall()]
    
    def get_trade_exits(self, trade_id: int) -> List[Dict]:
        """Get all exits for a specific trade."""
        if not self.conn:
            self.connect()
            
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT * FROM trade_exits
                WHERE trade_id = %s
                ORDER BY exit_time;
            """, (trade_id,))
            return [dict(row) for row in cur.fetchall()]
    
    def close(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Database connection closed")
    
    def health_check(self) -> bool:
        """Check if the database connection is working."""
        try:
            return self.redis.ping()
        except Exception:
            return False

# Initialize a global instance
db_manager = DatabaseManager()

def fetch_recent_movements(timeframe: str = '1h', limit: int = 100) -> List[Dict[str, Any]]:
    """
    Fetch recent price movements from the database.
    
    Args:
        timeframe: Timeframe of data to fetch ('1m', '5m', '15m', '1h', '4h', '1d')
        limit: Maximum number of records to return
        
    Returns:
        List of price data dictionaries
    """
    # Try to get data from Redis
    try:
        # Key where we store BTC price data for this timeframe
        key = f"btc_price_data:{timeframe}"
        
        # Get the latest data
        data = db_manager.redis.lrange(key, -limit, -1)
        
        if not data:
            # Fallback: If no data in Redis, return simulated data
            return _generate_simulated_price_data(limit)
        
        # Parse JSON data
        result = [json.loads(item) for item in data]
        return result
        
    except Exception as e:
        print(f"Error fetching recent price movements: {e}")
        # Return simulated data as fallback
        return _generate_simulated_price_data(limit)

def _generate_simulated_price_data(limit: int = 100) -> List[Dict[str, Any]]:
    """Generate simulated price data when real data isn't available."""
    import random
    
    data = []
    current_price = 80000.0  # Starting BTC price
    current_time = datetime.now()
    
    for i in range(limit):
        # Move backward in time
        timestamp = current_time - timedelta(hours=limit-i)
        
        # Random price movement (±2%)
        price_change = current_price * random.uniform(-0.02, 0.02)
        current_price += price_change
        
        # Generate OHLC data
        open_price = current_price
        high_price = open_price * random.uniform(1.0, 1.01)
        low_price = open_price * random.uniform(0.99, 1.0)
        close_price = open_price + random.uniform(-0.5, 0.5) * (high_price - low_price)
        
        # Generate volume
        volume = random.uniform(50, 500)
        
        data.append({
            'timestamp': timestamp.isoformat(),
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'volume': volume
        })
    
    return data

def store_price_data(timeframe: str, price_data: Dict[str, Any]) -> bool:
    """
    Store price data in Redis.
    
    Args:
        timeframe: Timeframe of data ('1m', '5m', '15m', '1h', '4h', '1d')
        price_data: Dictionary with price data
        
    Returns:
        Success status
    """
    try:
        key = f"btc_price_data:{timeframe}"
        db_manager.redis.rpush(key, json.dumps(price_data))
        # Keep only the last 10000 items
        db_manager.redis.ltrim(key, -10000, -1)
        return True
    except Exception as e:
        print(f"Error storing price data: {e}")
        return False

def insert_mm_trap(trap_data: Dict[str, Any]) -> bool:
    """
    Insert detected market manipulation trap into the database.
    
    Args:
        trap_data: Dictionary containing trap information
            - timestamp: When the trap was detected
            - trap_type: Type of manipulation ('stop_hunt', 'liquidity_grab', etc.)
            - price_level: Price at which trap occurred
            - direction: 'up' or 'down'
            - confidence_score: How confident the detection is (0.0-1.0)
            - volume_spike: Volume increase percentage
            - timeframe: Timeframe where trap was detected
            - price_range: Price range of the trap
            - description: Human-readable description
            
    Returns:
        Success status
    """
    # First initialize schema if needed
    try:
        if not db_manager.conn:
            db_manager.connect()
        
        # Create mm_traps table if it doesn't exist
        with db_manager.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS mm_traps (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
                    trap_type VARCHAR(50) NOT NULL,
                    price_level DECIMAL(16,8) NOT NULL,
                    direction VARCHAR(10) NOT NULL,
                    confidence_score DECIMAL(4,3) NOT NULL,
                    volume_spike DECIMAL(10,2),
                    timeframe VARCHAR(10),
                    price_range DECIMAL(16,8),
                    description TEXT,
                    metadata JSON
                );
            """)
            db_manager.conn.commit()
        
        # Insert the trap data
        with db_manager.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO mm_traps (
                    timestamp, trap_type, price_level, direction, 
                    confidence_score, volume_spike, timeframe, 
                    price_range, description, metadata
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                trap_data.get("timestamp", datetime.now()),
                trap_data["trap_type"],
                trap_data["price_level"],
                trap_data["direction"],
                trap_data["confidence_score"],
                trap_data.get("volume_spike", 0),
                trap_data.get("timeframe", "1h"),
                trap_data.get("price_range", 0),
                trap_data.get("description", ""),
                Json(trap_data.get("metadata", {}))
            ))
            trap_id = cur.fetchone()[0]
            db_manager.conn.commit()
            
        # Also store in Redis for quick access by real-time systems
        key = f"mm_trap:{trap_data['trap_type']}:{int(datetime.now().timestamp())}"
        db_manager.redis.set(key, json.dumps(trap_data))
        db_manager.redis.expire(key, 60*60*24)  # Expire after 24 hours
            
        return True
        
    except Exception as e:
        print(f"Error inserting MM trap: {e}")
        
        # Fallback to just Redis if PostgreSQL fails
        try:
            key = f"mm_trap:{trap_data['trap_type']}:{int(datetime.now().timestamp())}"
            db_manager.redis.set(key, json.dumps(trap_data))
            db_manager.redis.expire(key, 60*60*24)  # Expire after 24 hours
            return True
        except:
            return False

def get_recent_mm_traps(hours: int = 24, trap_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get recent market manipulation traps.
    
    Args:
        hours: How many hours back to look
        trap_type: Optional filter by trap type
        
    Returns:
        List of trap data dictionaries
    """
    try:
        if not db_manager.conn:
            db_manager.connect()
            
        with db_manager.conn.cursor(cursor_factory=DictCursor) as cur:
            if trap_type:
                cur.execute("""
                    SELECT * FROM mm_traps
                    WHERE timestamp > NOW() - INTERVAL %s HOUR
                    AND trap_type = %s
                    ORDER BY timestamp DESC;
                """, (hours, trap_type))
            else:
                cur.execute("""
                    SELECT * FROM mm_traps
                    WHERE timestamp > NOW() - INTERVAL %s HOUR
                    ORDER BY timestamp DESC;
                """, (hours,))
                
            return [dict(row) for row in cur.fetchall()]
            
    except Exception as e:
        print(f"Error retrieving MM traps: {e}")
        
        # Fallback to Redis
        try:
            traps = []
            for key in db_manager.redis.keys("mm_trap:*"):
                trap_data = json.loads(db_manager.redis.get(key))
                
                # Apply filters if needed
                if trap_type and trap_data.get("trap_type") != trap_type:
                    continue
                    
                # Add to results
                traps.append(trap_data)
                
            return traps
        except:
            return []

def fetch_recent_movements(minutes=15):
    """Fetch recent price movements from Redis."""
    try:
        # Get data from Redis
        movements = r.lrange("btc_movement_history", 0, -1)
        if not movements:
            return []
            
        # Convert string data to tuples
        parsed_movements = []
        current_time = datetime.datetime.now(datetime.UTC)
        cutoff_time = current_time - datetime.timedelta(minutes=minutes)
        
        for movement in movements:
            try:
                # Parse movement data
                movement_data = json.loads(movement)
                timestamp = datetime.datetime.fromisoformat(movement_data['timestamp'])
                
                if timestamp >= cutoff_time:
                    parsed_movements.append((
                        timestamp,
                        float(movement_data['price']),
                        float(movement_data.get('volume', 0)),
                        float(movement_data.get('high', 0)),
                        float(movement_data.get('low', 0)),
                        float(movement_data.get('volume', 0))
                    ))
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Error parsing movement data: {e}")
                continue
                
        return parsed_movements
        
    except Exception as e:
        print(f"Error fetching movements: {e}")
        return []
