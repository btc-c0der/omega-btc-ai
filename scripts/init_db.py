import psycopg2
import os
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """Initialize database tables."""
    conn = None
    try:
        # Determine if we're running in a container
        is_container = os.getenv('OMEGA_ENV') == 'production'
        
        # Set host based on environment
        host = 'postgres' if is_container else 'localhost'
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB', 'omega_db'),
            user=os.getenv('POSTGRES_USER', 'omega_user'),
            password=os.getenv('POSTGRES_PASSWORD', 'omega_pass'),
            host=host,
            port=os.getenv('POSTGRES_PORT', '5432')
        )
        
        with conn.cursor() as cur:
            # Create BTC price history table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS btc_prices (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ DEFAULT NOW(),
                    btc_price DECIMAL(18,8) NOT NULL,
                    volume DECIMAL(18,8) NOT NULL
                );
            """)
            
            # Create subtle movements table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS subtle_movements (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ DEFAULT NOW(),
                    btc_price DECIMAL(18,8) NOT NULL,
                    prev_price DECIMAL(18,8) NOT NULL,
                    absolute_change DECIMAL(18,8) NOT NULL,
                    price_change_percentage DECIMAL(18,8) NOT NULL,
                    movement_tag VARCHAR(50) NOT NULL,
                    volume DECIMAL(18,8) NOT NULL
                );
            """)
            
            # Create indexes
            cur.execute("CREATE INDEX IF NOT EXISTS idx_btc_prices_timestamp ON btc_prices(timestamp);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_subtle_movements_timestamp ON subtle_movements(timestamp);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_subtle_movements_tag ON subtle_movements(movement_tag);")
            
            conn.commit()
            logger.info("✅ Database tables created successfully")
            
    except Exception as e:
        logger.error(f"❌ Error initializing database: {e}")
        raise
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_db() 