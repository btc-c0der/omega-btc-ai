import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import json
from datetime import datetime, UTC
from omega_ai.utils.redis_manager import RedisManager
from omega_ai.visualizer.backend.server import app, ConnectionManager

@pytest.fixture
def redis_manager():
    """Create a mock RedisManager."""
    mock_redis = Mock(spec=RedisManager)
    return mock_redis

@pytest.fixture
def test_client(redis_manager):
    """Create a test client with mocked RedisManager."""
    with patch("omega_ai.visualizer.backend.server.RedisManager", return_value=redis_manager):
        client = TestClient(app)
        yield client

@pytest.fixture
def connection_manager():
    """Create a ConnectionManager instance."""
    return ConnectionManager()

def test_root_endpoint(test_client):
    """Test the root endpoint returns correct message."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "0M3G4 TR4P V1SU4L1Z3R API"}

def test_get_metrics_success(test_client, redis_manager):
    """Test successful metrics retrieval."""
    # Mock Redis data
    mock_dump = {
        "trap_detections": [
            {
                "type": "bullish",
                "confidence": 0.85,
                "timestamp": datetime.now(UTC).isoformat()
            },
            {
                "type": "bearish",
                "confidence": 0.75,
                "timestamp": datetime.now(UTC).isoformat()
            }
        ]
    }
    redis_manager.get_cached.return_value = json.dumps(mock_dump)

    response = test_client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    
    assert "totalTraps" in data
    assert data["totalTraps"] == 2
    assert "trapsByType" in data
    assert data["trapsByType"] == {"bullish": 1, "bearish": 1}
    assert "averageConfidence" in data
    assert abs(data["averageConfidence"] - 0.8) < 0.01

def test_get_metrics_no_data(test_client, redis_manager):
    """Test metrics endpoint when no data is available."""
    redis_manager.get_cached.return_value = None

    response = test_client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    
    assert data["totalTraps"] == 0
    assert data["trapsByType"] == {}
    assert data["averageConfidence"] == 0.0

def test_get_traps_success(test_client, redis_manager):
    """Test successful trap retrieval."""
    # Mock Redis data
    mock_traps = [
        {
            "id": "trap_1",
            "type": "bullish",
            "timestamp": datetime.now(UTC).isoformat(),
            "confidence": 0.85,
            "price": 68500,
            "volume": 1200,
            "metadata": {"pattern": "double_bottom"}
        }
    ]
    redis_manager.get_cached.return_value = json.dumps({"traps": mock_traps})

    response = test_client.get("/api/traps")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert data[0]["id"] == "trap_1"
    assert data[0]["type"] == "bullish"
    assert data[0]["confidence"] == 0.85

def test_get_traps_with_filters(test_client, redis_manager):
    """Test trap retrieval with time and type filters."""
    now = datetime.now(UTC)
    mock_traps = [
        {
            "id": "trap_1",
            "type": "bullish",
            "timestamp": now.isoformat(),
            "confidence": 0.85,
            "price": 68500,
            "volume": 1200,
            "metadata": {"pattern": "double_bottom"}
        }
    ]
    redis_manager.get_cached.return_value = json.dumps({"traps": mock_traps})

    # Test with type filter
    response = test_client.get("/api/traps?trap_type=bullish")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["type"] == "bullish"

    # Test with time filter
    start_time = (now - timedelta(hours=1)).isoformat()
    response = test_client.get(f"/api/traps?start_time={start_time}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_get_prices_success(test_client, redis_manager):
    """Test successful price data retrieval."""
    mock_prices = [
        {
            "time": datetime.now(UTC).isoformat(),
            "open": 68000,
            "close": 68500,
            "high": 68600,
            "low": 67900
        }
    ]
    redis_manager.get_cached.return_value = json.dumps({"prices": mock_prices})

    response = test_client.get("/api/prices")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert "time" in data[0]
    assert "open" in data[0]
    assert "close" in data[0]
    assert "high" in data[0]
    assert "low" in data[0]

def test_get_timeline_success(test_client, redis_manager):
    """Test successful timeline retrieval."""
    now = datetime.now(UTC)
    mock_traps = [
        {
            "type": "bullish",
            "timestamp": now.isoformat(),
            "confidence": 0.85,
            "description": "Bullish trap detected"
        }
    ]
    redis_manager.get_cached.return_value = json.dumps({"trap_detections": mock_traps})

    response = test_client.get("/api/timeline")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert data[0]["type"] == "bullish"
    assert data[0]["impact"] == "HIGH"  # Based on 0.85 confidence

@pytest.mark.asyncio
async def test_websocket_connection(connection_manager):
    """Test WebSocket connection management."""
    mock_websocket = Mock()
    mock_websocket.accept = Mock()
    mock_websocket.send_json = Mock()
    
    # Test connect
    await connection_manager.connect(mock_websocket)
    assert mock_websocket in connection_manager.active_connections
    mock_websocket.accept.assert_called_once()
    
    # Test broadcast
    test_message = {"type": "update", "data": "test"}
    await connection_manager.broadcast(test_message)
    mock_websocket.send_json.assert_called_with(test_message)
    
    # Test disconnect
    connection_manager.disconnect(mock_websocket)
    assert mock_websocket not in connection_manager.active_connections 