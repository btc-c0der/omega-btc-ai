#!/usr/bin/env python3

"""
PostgreSQL Database Connection and Operations Test Script

This script tests the following:
1. Local PostgreSQL connection
2. Scaleway PostgreSQL connection
3. Schema initialization
4. CRUD operations (Create, Read, Update, Delete)
5. Transaction integrity
6. Performance for typical MM trap detection operations

Usage:
    python scripts/test_db_connection.py [--local] [--cloud]
"""

import sys
import os
import time
import json
import argparse
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime, timezone
import random

# Add project root to path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import directly from the file
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

# This is a direct import assuming we're in the scripts directory
# First, define the DatabaseManager class here to avoid import issues
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
            
            # Create mm_traps table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS mm_traps (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
                    trap_type VARCHAR(50) NOT NULL,
                    btc_price DECIMAL(16,8) NOT NULL,
                    price_change DECIMAL(8,4) NOT NULL,
                    confidence DECIMAL(4,3) NOT NULL,
                    liquidity_grabbed DECIMAL(10,2) NOT NULL,
                    confidence_score DECIMAL(4,3) NOT NULL,
                    volume_spike DECIMAL(10,2),
                    timeframe VARCHAR(10),
                    price_range DECIMAL(16,8),
                    description TEXT,
                    metadata JSON
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
    
    def save_trade(self, trade_data: dict) -> int:
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
                json.dumps(trade_data["market_condition"]),
                trade_data["signal_type"],
                json.dumps(trade_data["take_profits"])
            ))
            trade_id = cur.fetchone()[0]
            self.conn.commit()
            return trade_id
    
    def save_trade_exit(self, exit_data: dict) -> None:
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
    
    def close(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Database connection closed")

# Terminal colors for better output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    """Print formatted header."""
    print(f"\n{CYAN}{BOLD}{'=' * 80}{RESET}")
    print(f"{CYAN}{BOLD} {text} {RESET}")
    print(f"{CYAN}{BOLD}{'=' * 80}{RESET}")

def print_result(label, success, error=None, details=None):
    """Print formatted test result."""
    if success:
        status = f"{GREEN}✓ PASS{RESET}"
    else:
        status = f"{RED}✗ FAIL{RESET}"
        
    print(f"{BOLD}{label}:{RESET} {status}")
    if error and not success:
        print(f"  {RED}Error: {error}{RESET}")
    if details:
        print(f"  {BLUE}{details}{RESET}")
    print()

def test_local_connection():
    """Test connection to local PostgreSQL server."""
    print_header("Testing LOCAL PostgreSQL Connection")
    
    db_manager = DatabaseManager(
        host="localhost",
        port=5432,
        dbname="omega_db",
        user="fsiqueira",
        password=""
    )
    
    try:
        db_manager.connect()
        ping_start = time.time()
        # Quick query to check connection
        with db_manager.conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
        ping_time = (time.time() - ping_start) * 1000  # ms
        
        db_manager.close()
        print_result(
            "Local PostgreSQL Connection", 
            True, 
            details=f"Connected to: {version} | Ping: {ping_time:.2f}ms"
        )
        return True
    except Exception as e:
        print_result("Local PostgreSQL Connection", False, error=str(e))
        return False

def test_cloud_connection():
    """Test connection to Scaleway PostgreSQL server."""
    print_header("Testing SCALEWAY PostgreSQL Connection")
    
    # Get credentials from environment or ask user
    host = os.environ.get("POSTGRES_CLOUD_HOST")
    port = os.environ.get("POSTGRES_CLOUD_PORT", "5432")
    dbname = os.environ.get("POSTGRES_CLOUD_DB", "omega_btc")
    user = os.environ.get("POSTGRES_CLOUD_USER")
    password = os.environ.get("POSTGRES_CLOUD_PASSWORD")
    
    if not all([host, user, password]):
        print(f"{YELLOW}Cloud PostgreSQL credentials not found in environment variables.{RESET}")
        print("Please enter your Scaleway PostgreSQL credentials:")
        host = host or input("Host: ")
        port = port or input(f"Port [{port}]: ") or port
        dbname = dbname or input(f"Database name [{dbname}]: ") or dbname
        user = user or input("Username: ")
        password = password or input("Password: ")
    
    db_manager = DatabaseManager(
        host=host,
        port=int(port),
        dbname=dbname,
        user=user,
        password=password
    )
    
    try:
        db_manager.connect()
        ping_start = time.time()
        # Quick query to check connection
        with db_manager.conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
        ping_time = (time.time() - ping_start) * 1000  # ms
        
        db_manager.close()
        print_result(
            "Scaleway PostgreSQL Connection", 
            True, 
            details=f"Connected to: {version} | Ping: {ping_time:.2f}ms"
        )
        return True
    except Exception as e:
        print_result("Scaleway PostgreSQL Connection", False, error=str(e))
        return False

def test_schema_init(db_manager):
    """Test database schema initialization."""
    print_header("Testing Schema Initialization")
    
    try:
        db_manager.connect()
        db_manager.initialize_schema()
        
        # Verify tables exist
        tables = ["traders", "trades", "trade_exits", "trader_metrics", "mm_traps"]
        with db_manager.conn.cursor() as cursor:
            for table in tables:
                cursor.execute(f"SELECT EXISTS (SELECT FROM pg_tables WHERE tablename = '{table}');")
                exists = cursor.fetchone()[0]
                print_result(f"Table '{table}' exists", exists)
        
        db_manager.close()
        return True
    except Exception as e:
        print_result("Schema Initialization", False, error=str(e))
        return False

def test_crud_operations(db_manager):
    """Test CRUD operations."""
    print_header("Testing Database CRUD Operations")
    
    try:
        db_manager.connect()
        
        # Create test trader
        trader_name = f"Test_Trader_{int(time.time())}"
        try:
            trader_id = db_manager.save_trader(
                name=trader_name,
                profile_type="test",
                initial_capital=10000.0
            )
            print_result("Create trader", True, details=f"Trader ID: {trader_id}")
        except Exception as e:
            print_result("Create trader", False, error=str(e))
            return False
        
        # Create test trade
        try:
            trade_data = {
                "trader_id": trader_id,
                "direction": "LONG",
                "entry_price": 50000.0,
                "position_size": 0.1,
                "leverage": 5,
                "entry_reason": "Test trade",
                "stop_loss": 49000.0,
                "emotional_state": "calm",
                "market_condition": {"volatility": "medium", "trend": "bullish"},
                "signal_type": "test",
                "take_profits": {"tp1": 51000.0, "tp2": 52000.0}
            }
            trade_id = db_manager.save_trade(trade_data)
            print_result("Create trade", True, details=f"Trade ID: {trade_id}")
        except Exception as e:
            print_result("Create trade", False, error=str(e))
            return False
        
        # Read trader data
        try:
            with db_manager.conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT * FROM traders WHERE id = %s", (trader_id,))
                trader = cursor.fetchone()
            print_result("Read trader", True, details=f"Trader name: {trader['name']}")
        except Exception as e:
            print_result("Read trader", False, error=str(e))
            return False
        
        # Update trade (add exit)
        try:
            exit_data = {
                "trade_id": trade_id,
                "exit_type": "take_profit",
                "exit_price": 51000.0,
                "percentage": 1.0,
                "pnl": 100.0,
                "price_bar": 10,
                "reason": "Test exit",
                "is_complete": True,
                "total_pnl": 100.0,
                "duration_hours": 2.5,
                "liquidated": False
            }
            db_manager.save_trade_exit(exit_data)
            print_result("Update trade (exit)", True)
        except Exception as e:
            print_result("Update trade (exit)", False, error=str(e))
            return False
        
        # Delete test data
        try:
            with db_manager.conn.cursor() as cursor:
                cursor.execute("DELETE FROM trade_exits WHERE trade_id = %s", (trade_id,))
                cursor.execute("DELETE FROM trades WHERE id = %s", (trade_id,))
                cursor.execute("DELETE FROM traders WHERE id = %s", (trader_id,))
                db_manager.conn.commit()
            print_result("Delete test data", True)
        except Exception as e:
            print_result("Delete test data", False, error=str(e))
            return False
            
        db_manager.close()
        return True
    except Exception as e:
        print_result("CRUD Operations", False, error=str(e))
        return False

def test_transaction_integrity(db_manager):
    """Test transaction integrity."""
    print_header("Testing Transaction Integrity")
    
    try:
        db_manager.connect()
        
        # Create a test trader
        trader_name = f"Integrity_Test_{int(time.time())}"
        trader_id = db_manager.save_trader(
            name=trader_name,
            profile_type="test",
            initial_capital=10000.0
        )
        
        # Start a transaction that should fail
        try:
            with db_manager.conn.cursor() as cursor:
                # Start transaction
                db_manager.conn.autocommit = False
                
                # Insert a valid trade
                cursor.execute("""
                    INSERT INTO trades (
                        trader_id, direction, entry_price, position_size, leverage,
                        entry_reason, status
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (trader_id, "LONG", 50000.0, 0.1, 5, "Valid trade", "OPEN"))
                valid_trade_id = cursor.fetchone()[0]
                
                # Insert an invalid trade (violating NOT NULL constraint)
                cursor.execute("""
                    INSERT INTO trades (
                        trader_id, direction, entry_price, position_size, leverage,
                        entry_reason
                    )
                    VALUES (%s, %s, NULL, %s, %s, %s)
                    RETURNING id;
                """, (trader_id, "LONG", 0.1, 5, "Invalid trade"))
                
                # This should not be reached
                db_manager.conn.commit()
                transaction_failed = False
            print_result("Transaction rollback", False, 
                        error="Transaction with invalid data succeeded when it should have failed")
        except Exception as e:
            # Expected to fail
            db_manager.conn.rollback()
            db_manager.conn.autocommit = True
            transaction_failed = True
            print_result("Transaction rollback", True, 
                        details="Transaction with invalid data correctly failed and rolled back")
        
        # Verify the valid trade didn't persist
        with db_manager.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM trades WHERE trader_id = %s", (trader_id,))
            trade_count = cursor.fetchone()[0]
            valid_rollback = trade_count == 0
        print_result("Valid trade rollback", valid_rollback, 
                    details=f"Expected 0 trades, found {trade_count}")
        
        # Clean up
        with db_manager.conn.cursor() as cursor:
            cursor.execute("DELETE FROM traders WHERE id = %s", (trader_id,))
            db_manager.conn.commit()
        
        db_manager.close()
        return transaction_failed and valid_rollback
    except Exception as e:
        print_result("Transaction Integrity", False, error=str(e))
        return False

def test_mm_trap_operations(db_manager):
    """Test MM trap detection operations."""
    print_header("Testing MM Trap Detection Operations")
    
    try:
        db_manager.connect()
        
        # Adjusted: Create MM trap test data using the correct schema
        trap_data = {
            "timestamp": datetime.now(timezone.utc),
            "trap_type": "liquidity_grab",
            "btc_price": 50000.0,  # Changed from price_level
            "price_change": 0.025,  # Added to match schema
            "confidence": 0.85,    # Changed from confidence_score
            "liquidity_grabbed": 150.0  # Changed from volume_spike
            # No fields for timeframe, direction, price_range, or description in the schema
        }
        
        with db_manager.conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO mm_traps (
                    timestamp, trap_type, btc_price, 
                    price_change, confidence, liquidity_grabbed
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                trap_data["timestamp"],
                trap_data["trap_type"],
                trap_data["btc_price"],
                trap_data["price_change"],
                trap_data["confidence"],
                trap_data["liquidity_grabbed"]
            ))
            trap_id = cursor.fetchone()[0]
            db_manager.conn.commit()
            
        print_result("Insert MM trap", True, details=f"Trap ID: {trap_id}")
        
        # Test MM trap query by type
        with db_manager.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("""
                SELECT * FROM mm_traps 
                WHERE trap_type = %s 
                ORDER BY timestamp DESC 
                LIMIT 1;
            """, (trap_data["trap_type"],))
            retrieved_trap = cursor.fetchone()
            
        if retrieved_trap and retrieved_trap["trap_type"] == trap_data["trap_type"]:
            print_result("Query MM trap", True, 
                        details=f"Retrieved trap type: {retrieved_trap['trap_type']}")
        else:
            print_result("Query MM trap", False, 
                        error="Could not retrieve the inserted trap")
            
        # Clean up
        with db_manager.conn.cursor() as cursor:
            cursor.execute("DELETE FROM mm_traps WHERE id = %s", (trap_id,))
            db_manager.conn.commit()
            
        # Test performance with batch inserts
        trap_types = ["liquidity_grab", "stop_hunt", "fake_pump", "fake_dump"]
        
        print(f"\n{YELLOW}Testing batch insert performance...{RESET}")
        
        batch_size = 100
        trap_data_batch = []
        
        for i in range(batch_size):
            trap_data_batch.append({
                "timestamp": datetime.now(timezone.utc),
                "trap_type": random.choice(trap_types),
                "btc_price": random.uniform(48000.0, 52000.0),
                "price_change": random.uniform(-0.05, 0.05),
                "confidence": random.uniform(0.6, 0.95),
                "liquidity_grabbed": random.uniform(50.0, 200.0)
            })
        
        start_time = time.time()
        
        with db_manager.conn.cursor() as cursor:
            for trap in trap_data_batch:
                cursor.execute("""
                    INSERT INTO mm_traps (
                        timestamp, trap_type, btc_price,
                        price_change, confidence, liquidity_grabbed
                    )
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (
                    trap["timestamp"],
                    trap["trap_type"],
                    trap["btc_price"],
                    trap["price_change"],
                    trap["confidence"],
                    trap["liquidity_grabbed"]
                ))
            db_manager.conn.commit()
            
        end_time = time.time()
        total_time = end_time - start_time
        inserts_per_second = batch_size / total_time
        
        print_result("Batch insert performance", True, 
                    details=f"Inserted {batch_size} traps in {total_time:.2f}s ({inserts_per_second:.2f} inserts/sec)")
        
        # Clean up batch data
        with db_manager.conn.cursor() as cursor:
            cursor.execute("DELETE FROM mm_traps WHERE trap_type IN ('liquidity_grab', 'stop_hunt', 'fake_pump', 'fake_dump');")
            deleted_count = cursor.rowcount
            db_manager.conn.commit()
            
        print_result("Batch data cleanup", True, details=f"Deleted {deleted_count} test records")
        
        db_manager.close()
        return True
    except Exception as e:
        print_result("MM Trap Operations", False, error=str(e))
        return False

def main():
    """Run all database tests."""
    parser = argparse.ArgumentParser(description="Test PostgreSQL database connections and operations")
    parser.add_argument("--local", action="store_true", help="Test local PostgreSQL connection only")
    parser.add_argument("--cloud", action="store_true", help="Test Scaleway PostgreSQL connection only")
    args = parser.parse_args()
    
    # Determine which tests to run
    test_local = args.local or not args.cloud
    test_cloud = args.cloud or not args.local
    
    # Test database connections
    if test_local:
        local_success = test_local_connection()
    else:
        local_success = False
        
    if test_cloud:
        cloud_success = test_cloud_connection()
    else:
        cloud_success = False
    
    # Select database to use for further tests
    if cloud_success:
        print(f"\n{BLUE}Using Scaleway PostgreSQL for remaining tests{RESET}")
        db_manager = DatabaseManager(
            host=os.environ.get("POSTGRES_CLOUD_HOST"),
            port=int(os.environ.get("POSTGRES_CLOUD_PORT", "5432")),
            dbname=os.environ.get("POSTGRES_CLOUD_DB", "omega_btc"),
            user=os.environ.get("POSTGRES_CLOUD_USER"),
            password=os.environ.get("POSTGRES_CLOUD_PASSWORD")
        )
    elif local_success:
        print(f"\n{BLUE}Using local PostgreSQL for remaining tests{RESET}")
        db_manager = DatabaseManager(
            host="localhost",
            port=5432,
            dbname="omega_db",
            user="fsiqueira",
            password=""
        )
    else:
        print(f"\n{RED}No PostgreSQL connection available. Exiting.{RESET}")
        return 1
    
    # Run remaining tests
    schema_success = test_schema_init(db_manager)
    crud_success = test_crud_operations(db_manager)
    transaction_success = test_transaction_integrity(db_manager)
    mm_trap_success = test_mm_trap_operations(db_manager)
    
    # Print summary
    print_header("Test Summary")
    if test_local:
        print(f"Local Connection:    {'✓' if local_success else '✗'}")
    if test_cloud:
        print(f"Cloud Connection:    {'✓' if cloud_success else '✗'}")
    print(f"Schema Initialization: {'✓' if schema_success else '✗'}")
    print(f"CRUD Operations:       {'✓' if crud_success else '✗'}")
    print(f"Transaction Integrity: {'✓' if transaction_success else '✗'}")
    print(f"MM Trap Operations:    {'✓' if mm_trap_success else '✗'}")
    
    # Overall result
    tested_items = sum([test_local, test_cloud, schema_success, crud_success, transaction_success, mm_trap_success])
    successful_items = sum([
        local_success if test_local else 0,
        cloud_success if test_cloud else 0,
        schema_success,
        crud_success,
        transaction_success,
        mm_trap_success
    ])
    
    if successful_items == tested_items:
        print(f"\n{GREEN}All tests passed successfully!{RESET}")
        return 0
    else:
        print(f"\n{RED}Some tests failed ({successful_items}/{tested_items} passed){RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 