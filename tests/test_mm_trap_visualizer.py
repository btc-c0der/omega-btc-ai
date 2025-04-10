
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
Tests for the Market Maker Trap Visualizer server.
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from omega_ai.visualizer.backend.src.mm_trap_visualizer.server import (
    MMTrapVisualizerServer,
    TrapData,
    MetricsResponse,
    TimelineEvent
)
from omega_ai.utils.redis_manager import RedisManager

@pytest.fixture
def mock_trap_data():
    """Create mock trap data."""
    return {
        'traps': [
            {
                'id': '1',
                'type': 'accumulation',
                'timestamp': datetime.now() - timedelta(hours=2),
                'confidence': 0.85,
                'price': 45000.0,
                'volume': 1.5,
                'description': 'Large accumulation detected',
                'success': True
            },
            {
                'id': '2',
                'type': 'distribution',
                'timestamp': datetime.now() - timedelta(hours=1),
                'confidence': 0.92,
                'price': 46000.0,
                'volume': 2.0,
                'description': 'Distribution pattern observed',
                'success': False
            }
        ]
    }

@pytest.fixture
def redis_manager(mock_trap_data):
    """Create a mock Redis manager."""
    manager = Mock(spec=RedisManager)
    manager.get_cached.return_value = mock_trap_data
    return manager

@pytest.fixture
def server(redis_manager):
    """Create a test server instance."""
    return MMTrapVisualizerServer("Test MM Trap Visualizer", redis_manager)

@pytest.fixture
def client(server):
    """Create a test client."""
    return TestClient(server.app)

def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to MM Trap Visualizer API"}

def test_metrics_endpoint(client, mock_trap_data):
    """Test the metrics endpoint."""
    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_traps"] == 2
    assert data["traps_by_type"]["accumulation"] == 1
    assert data["traps_by_type"]["distribution"] == 1
    assert 0.85 < data["average_confidence"] < 0.92
    assert data["success_rate"] == 0.5

def test_traps_endpoint(client, mock_trap_data):
    """Test the traps endpoint."""
    response = client.get("/api/traps")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 2
    assert data[0]["type"] == "accumulation"
    assert data[1]["type"] == "distribution"

def test_traps_endpoint_with_filters(client, mock_trap_data):
    """Test the traps endpoint with filters."""
    # Test with type filter
    response = client.get("/api/traps?trap_type=accumulation")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["type"] == "accumulation"
    
    # Test with time filters
    now = datetime.now()
    start_time = (now - timedelta(hours=3)).isoformat()
    end_time = (now - timedelta(hours=0.5)).isoformat()
    
    response = client.get(f"/api/traps?start_time={start_time}&end_time={end_time}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_timeline_endpoint(client, mock_trap_data):
    """Test the timeline endpoint."""
    response = client.get("/api/timeline")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 2
    assert data[0]["type"] == "accumulation"
    assert data[1]["type"] == "distribution"
    assert data[0]["impact"] == "high"
    assert data[1]["impact"] == "high"

def test_error_handling(client, redis_manager):
    """Test error handling."""
    redis_manager.get_cached.side_effect = Exception("Redis error")
    
    response = client.get("/api/metrics")
    assert response.status_code == 500
    assert "Redis error" in response.json()["detail"]
    
    response = client.get("/api/traps")
    assert response.status_code == 500
    assert "Redis error" in response.json()["detail"]
    
    response = client.get("/api/timeline")
    assert response.status_code == 500
    assert "Redis error" in response.json()["detail"] 