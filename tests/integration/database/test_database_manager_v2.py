
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

"""Tests for Database Manager V2 functionality.

This test suite covers the enhanced features of the Database Manager V2:
1. Connection pooling
2. Query optimization
3. Data validation
4. Transaction management
5. Error handling
6. Health monitoring
7. Performance optimization
8. Resource cleanup
"""

import pytest
import asyncio
from datetime import datetime, UTC
from typing import Dict, Any
from omega_ai.mm_trap_detector.database_manager_v2 import (
    DatabaseManagerV2, DatabaseConfig
)

# ---- Test Helpers ----

@pytest.fixture
def db_config():
    """Create test database configuration."""
    return DatabaseConfig(
        host="localhost",
        port=5432,
        database="omega_btc_test",
        user="omega_user",
        password="omega_pass",
        pool_size=2,
        max_overflow=2,
        pool_timeout=5,
        pool_recycle=300
    )

@pytest.fixture
async def db_manager(db_config):
    """Create database manager instance."""
    manager = DatabaseManagerV2(config=db_config)
    yield manager
    await manager.close()

# ---- Test Functions ----

@pytest.mark.asyncio
async def test_database_v2_initialization(db_manager):
    """Test database manager initialization."""
    assert db_manager is not None
    assert db_manager.engine is not None
    assert db_manager.SessionLocal is not None

@pytest.mark.asyncio
async def test_database_v2_connection_pool(db_manager):
    """Test database connection pool functionality."""
    # Get multiple sessions
    sessions = []
    for _ in range(3):
        with db_manager.get_session() as session:
            sessions.append(session)
            result = session.execute("SELECT 1")
            assert result.scalar() == 1
    
    # Verify pool is working
    assert len(sessions) == 3
    for session in sessions:
        assert not session.is_active

@pytest.mark.asyncio
async def test_database_v2_query_execution(db_manager):
    """Test database query execution."""
    query = "SELECT :value as test"
    params = {"value": "divine_test"}
    
    result = await db_manager.execute_query(query, params)
    assert len(result) == 1
    assert result[0]["test"] == "divine_test"

@pytest.mark.asyncio
async def test_database_v2_data_insertion(db_manager):
    """Test database data insertion."""
    table = "test_table"
    data = {
        "name": "divine_test",
        "value": 42,
        "created_at": datetime.now(UTC)
    }
    
    # Create test table
    create_table = """
    CREATE TABLE IF NOT EXISTS test_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        value INTEGER,
        created_at TIMESTAMP WITH TIME ZONE
    )
    """
    await db_manager.execute_query(create_table)
    
    # Insert data
    id = await db_manager.insert_data(table, data)
    assert id is not None
    
    # Verify insertion
    result = await db_manager.execute_query(
        "SELECT * FROM test_table WHERE id = :id",
        {"id": id}
    )
    assert len(result) == 1
    assert result[0]["name"] == "divine_test"
    assert result[0]["value"] == 42

@pytest.mark.asyncio
async def test_database_v2_data_update(db_manager):
    """Test database data update."""
    table = "test_table"
    data = {
        "name": "updated_test",
        "value": 84
    }
    condition = "id = 1"
    
    # Update data
    affected = await db_manager.update_data(table, data, condition)
    assert affected > 0
    
    # Verify update
    result = await db_manager.execute_query(
        "SELECT * FROM test_table WHERE id = 1"
    )
    assert len(result) == 1
    assert result[0]["name"] == "updated_test"
    assert result[0]["value"] == 84

@pytest.mark.asyncio
async def test_database_v2_data_deletion(db_manager):
    """Test database data deletion."""
    table = "test_table"
    condition = "id = 1"
    
    # Delete data
    affected = await db_manager.delete_data(table, condition)
    assert affected > 0
    
    # Verify deletion
    result = await db_manager.execute_query(
        "SELECT * FROM test_table WHERE id = 1"
    )
    assert len(result) == 0

@pytest.mark.asyncio
async def test_database_v2_health_check(db_manager):
    """Test database health check."""
    health = await db_manager.health_check()
    
    assert health["status"] == "healthy"
    assert "pool_size" in health
    assert "checkedin" in health
    assert "overflow" in health
    assert "checkedout" in health
    assert "database_size" in health
    assert "timestamp" in health

@pytest.mark.asyncio
async def test_database_v2_optimization(db_manager):
    """Test database optimization."""
    result = await db_manager.optimize_database()
    
    assert result["status"] == "optimized"
    assert "timestamp" in result

@pytest.mark.asyncio
async def test_database_v2_error_handling(db_manager):
    """Test database error handling."""
    # Test invalid query
    with pytest.raises(Exception):
        await db_manager.execute_query("INVALID SQL")
    
    # Test invalid table
    with pytest.raises(Exception):
        await db_manager.insert_data("nonexistent_table", {"test": "data"})
    
    # Test invalid condition
    with pytest.raises(Exception):
        await db_manager.update_data("test_table", {"test": "data"}, "invalid condition")

@pytest.mark.asyncio
async def test_database_v2_transaction_rollback(db_manager):
    """Test database transaction rollback."""
    table = "test_table"
    data = {
        "name": "rollback_test",
        "value": 42
    }
    
    try:
        # Start transaction
        with db_manager.get_session() as session:
            # Insert data
            session.execute(
                f"INSERT INTO {table} (name, value) VALUES (:name, :value)",
                data
            )
            # Force error
            raise Exception("Test rollback")
    except Exception:
        # Verify rollback
        result = await db_manager.execute_query(
            f"SELECT * FROM {table} WHERE name = :name",
            {"name": "rollback_test"}
        )
        assert len(result) == 0

@pytest.mark.asyncio
async def test_database_v2_connection_cleanup(db_manager):
    """Test database connection cleanup."""
    # Create multiple connections
    sessions = []
    for _ in range(3):
        with db_manager.get_session() as session:
            sessions.append(session)
    
    # Close manager
    await db_manager.close()
    
    # Verify cleanup
    for session in sessions:
        assert not session.is_active 