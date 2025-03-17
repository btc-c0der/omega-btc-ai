from sqlalchemy import create_engine, text

# Database connection (Modify as needed)
DB_TYPE = "postgresql"  # Change to "mysql" or "sqlite"
DB_NAME = "omega_db"
DB_USER = "omega_user"
DB_PASS = "omega_pass"
DB_HOST = "localhost"  # Use "localhost" if running locally
DB_PORT = "5432"  # Change to MySQL's 3306 or SQLite doesn't need a port

# Create DB connection
engine = create_engine(f"{DB_TYPE}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def get_mm_trap_summary():
    query = text("""
        SELECT 
            COUNT(*) AS total_traps,
            MAX(timestamp) AS latest_trap,
            SUM(liquidity_grabbed) AS total_liquidity
        FROM mm_traps
    """)
    
    with engine.connect() as conn:
        result = conn.execute(query).fetchone()
    
    # Extract results
    total_traps, latest_trap, total_liquidity = result
    return {
        "Total MM Traps Detected": total_traps,
        "Latest Trap Timestamp": latest_trap,
        "Total Liquidity Grabbed": total_liquidity
    }

# Run query and print summary
if __name__ == "__main__":
    summary = get_mm_trap_summary()
    print("🔍 MM Trap Summary Results:")
    for key, value in summary.items():
        print(f"➡ {key}: {value}")
