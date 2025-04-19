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
    """
    Test connecting to a local PostgreSQL database.
    
    This function attempts to establish a connection to the local PostgreSQL
    server using default credentials, then checks if the connection is valid.
    """
    print_header("TESTING LOCAL POSTGRESQL CONNECTION")
    
    try:
        db_manager = DatabaseManager(
            host="localhost",
            dbname="omega_btc",
            user="postgres",
            password="postgres"
        )
        
        db_manager.connect()
        success = db_manager.conn is not None and not db_manager.conn.closed
        db_manager.close()
        
        print_result("Local connection", success)
        return db_manager if success else None
    except Exception as e:
        print_result("Local connection", False, error=str(e))
        return None

def test_cloud_connection():
    """
    Test connecting to a cloud-hosted PostgreSQL database.
    
    This function attempts to establish a connection to a Scaleway PostgreSQL 
    database instance using provided credentials, then checks if the 
    connection is valid.
    """
    print_header("TESTING CLOUD POSTGRESQL CONNECTION")
    
    try:
        # Load config if available
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'db_config.json')
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            host = config.get('cloud_host', 'postgres-omega-btc.db-omega-btc.scw.cloud')
            port = config.get('cloud_port', 22410)
            dbname = config.get('cloud_dbname', 'omega_btc_db')
            user = config.get('cloud_user', 'omega_admin')
            password = config.get('cloud_password', '')
        else:
            host = 'postgres-omega-btc.db-omega-btc.scw.cloud'
            port = 22410
            dbname = 'omega_btc_db'
            user = 'omega_admin'
            password = input("Enter Scaleway DB Password: ")
        
        db_manager = DatabaseManager(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        
        db_manager.connect()
        success = db_manager.conn is not None and not db_manager.conn.closed
        
        print_result("Cloud connection", success)
        return db_manager if success else None
    except Exception as e:
        print_result("Cloud connection", False, error=str(e))
        return None
    
def test_schema_init(db_manager):
    """
    Test initializing the database schema.
    
    This function tests the schema initialization process by creating all required 
    tables for the OmegaBTC AI system and verifying their existence.
    
    Args:
        db_manager: The DatabaseManager instance to use for testing.
    """
    print_header("TESTING SCHEMA INITIALIZATION")
    
    try:
        # Initialize schema
        db_manager.initialize_schema()
        
        # Verify tables exist
        with db_manager.conn.cursor() as cursor:
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['traders', 'trades', 'trade_exits', 'mm_traps']
        missing_tables = [table for table in required_tables if table not in tables]
        
        success = len(missing_tables) == 0
        print_result("Schema initialization", success, 
                   details=f"Found tables: {', '.join(tables)}")
        
        return success
    except Exception as e:
        print_result("Schema initialization", False, error=str(e))
        return False

def test_crud_operations(db_manager):
    """
    Test basic CRUD (Create, Read, Update, Delete) operations.
    
    This function tests the database's ability to create, read, update, and 
    delete records in the database tables, verifying the correct functionality
    of these essential operations.
    
    Args:
        db_manager: The DatabaseManager instance to use for testing.
    """
    print_header("TESTING CRUD OPERATIONS")
    
    try:
        # 1. Create trader
        trader_name = f"Trader_{int(time.time())}"
        trader_id = db_manager.save_trader(
            name=trader_name,
            profile_type="aggressive",
            initial_capital=10000.0
        )
        
        # Verify trader creation
        with db_manager.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM traders WHERE id = %s", (trader_id,))
            trader = cursor.fetchone()
        
        if not trader or trader['name'] != trader_name:
            print_result("Create operation", False, error="Failed to create trader")
            return False
        
        # 2. Create trade
        trade_data = {
            "trader_id": trader_id,
            "symbol": "BTC/USD",
            "entry_price": 50000.0,
            "entry_time": datetime.now(timezone.utc),
            "position_size": 1.0,
            "direction": "long",
            "stop_loss": 49000.0,
            "take_profit": 52000.0,
            "status": "open",
            "entry_signal": "fibonacci_bounce",
            "risk_reward_ratio": 2.0
        }
        
        trade_id = db_manager.save_trade(trade_data)
        
        # 3. Read trade
        with db_manager.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM trades WHERE id = %s", (trade_id,))
            trade = cursor.fetchone()
        
        if not trade or trade['symbol'] != "BTC/USD":
            print_result("Read operation", False, error="Failed to read trade")
            return False
        
        # 4. Update trade
        with db_manager.conn.cursor() as cursor:
            cursor.execute(
                "UPDATE trades SET take_profit = %s WHERE id = %s",
                (53000.0, trade_id)
            )
            db_manager.conn.commit()
        
        # Verify update
        with db_manager.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT take_profit FROM trades WHERE id = %s", (trade_id,))
            updated_trade = cursor.fetchone()
        
        if not updated_trade or updated_trade['take_profit'] != 53000.0:
            print_result("Update operation", False, error="Failed to update trade")
            return False
        
        # 5. Delete trade
        with db_manager.conn.cursor() as cursor:
            cursor.execute("DELETE FROM trades WHERE id = %s", (trade_id,))
            db_manager.conn.commit()
        
        # Verify delete
        with db_manager.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM trades WHERE id = %s", (trade_id,))
            count = cursor.fetchone()[0]
        
        if count != 0:
            print_result("Delete operation", False, error="Failed to delete trade")
            return False
        
        print_result("CRUD operations", True, details="All operations successful")
        return True
        
    except Exception as e:
        print_result("CRUD operations", False, error=str(e))
        return False

def test_transaction_integrity(db_manager):
    """
    Test database transaction integrity.
    
    This function tests the atomicity of database transactions by attempting 
    to perform a series of operations within a transaction and then rolling back,
    ensuring that no changes persist after the rollback.
    
    Args:
        db_manager: The DatabaseManager instance to use for testing.
    """
    print_header("TESTING TRANSACTION INTEGRITY")
    
    try:
        # Count existing traders
        with db_manager.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM traders")
            initial_count = cursor.fetchone()[0]
        
        # Start transaction
        with db_manager.conn.cursor() as cursor:
            # Create 5 traders in a transaction
            for i in range(5):
                trader_name = f"Transaction_Test_Trader_{i}_{int(time.time())}"
                cursor.execute(
                    """
                    INSERT INTO traders (name, profile_type, initial_capital, created_at)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (trader_name, "conservative", 5000.0, datetime.now(timezone.utc))
                )
            
            # Count traders within transaction
            cursor.execute("SELECT COUNT(*) FROM traders")
            mid_count = cursor.fetchone()[0]
            
            # Verify count increased
            if mid_count != initial_count + 5:
                print_result("Transaction operations", False, 
                           error="Transaction didn't add expected rows")
                db_manager.conn.rollback()
                return False
            
            # Explicitly rollback
            db_manager.conn.rollback()
        
        # Count traders after rollback
        with db_manager.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM traders")
            final_count = cursor.fetchone()[0]
        
        # Verify rollback worked
        if final_count != initial_count:
            print_result("Transaction rollback", False, 
                       error=f"Rollback failed. Expected {initial_count}, got {final_count}")
            return False
        
        print_result("Transaction integrity", True, 
                   details=f"Transaction rolled back successfully")
        return True
        
    except Exception as e:
        print_result("Transaction integrity", False, error=str(e))
        return False

def test_mm_trap_operations(db_manager):
    """
    Test operations specific to Market Maker trap detection.
    
    This function tests the database operations related to storing and 
    retrieving Market Maker trap data, which is a core functionality of
    the OmegaBTC AI system for tracking manipulative market patterns.
    
    Args:
        db_manager: The DatabaseManager instance to use for testing.
    """
    print_header("TESTING MM TRAP OPERATIONS")
    
    try:
        # 1. Create MM traps
        trap_types = ["stop_hunt", "liquidity_grab", "fake_dump", "fake_pump"]
        trap_ids = []
        
        for i in range(10):
            trap_type = random.choice(trap_types)
            confidence = random.uniform(0.7, 0.99)
            price = 50000.0 + (random.uniform(-2000, 2000))
            timestamp = datetime.now(timezone.utc)
            
            # Insert trap
            with db_manager.conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO mm_traps (
                        type, confidence, price, detected_at, details, schumann_resonance,
                        success, confirmation_time
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        trap_type, 
                        confidence, 
                        price, 
                        timestamp, 
                        json.dumps({
                            "volume": random.uniform(10, 100),
                            "pattern": "v_shape",
                            "detection_algorithm": "fibonacci"
                        }),
                        random.uniform(7.0, 15.0),
                        random.choice([True, False, None]),
                        timestamp + (datetime.timedelta(minutes=random.randint(5, 30)) 
                                     if random.random() > 0.5 else None)
                    )
                )
                trap_id = cursor.fetchone()[0]
                trap_ids.append(trap_id)
            
            db_manager.conn.commit()
        
        # 2. Test simple queries
        with db_manager.conn.cursor(cursor_factory=DictCursor) as cursor:
            # Count by type
            cursor.execute(
                "SELECT type, COUNT(*) FROM mm_traps GROUP BY type"
            )
            type_counts = cursor.fetchall()
            
            # High confidence traps
            cursor.execute(
                "SELECT * FROM mm_traps WHERE confidence > 0.9"
            )
            high_confidence = cursor.fetchall()
            
            # Recent traps
            cursor.execute(
                "SELECT * FROM mm_traps WHERE detected_at > %s",
                (datetime.now(timezone.utc) - datetime.timedelta(hours=1),)
            )
            recent_traps = cursor.fetchall()
        
        # 3. Test complex query - success rate by trap type
        with db_manager.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT type,
                       COUNT(*) as total,
                       SUM(CASE WHEN success IS TRUE THEN 1 ELSE 0 END) as successful,
                       SUM(CASE WHEN success IS FALSE THEN 1 ELSE 0 END) as failed,
                       SUM(CASE WHEN success IS NULL THEN 1 ELSE 0 END) as pending,
                       AVG(confidence) as avg_confidence
                FROM mm_traps
                GROUP BY type
                """
            )
            trap_stats = cursor.fetchall()
        
        # Test passed if we can run all these operations
        success = (
            len(trap_ids) == 10 and
            len(type_counts) > 0 and
            len(trap_stats) > 0
        )
        
        print_result("MM trap operations", success, 
                   details=f"Created {len(trap_ids)} traps, ran stats queries successfully")
        
        return success
        
    except Exception as e:
        print_result("MM trap operations", False, error=str(e))
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