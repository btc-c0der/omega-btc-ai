"""Tests for the unified trap visualizer server."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import json
from datetime import datetime, UTC, timedelta
from omega_ai.utils.redis_manager import RedisManager
from omega_ai.visualizer.backend.unified_server import (
    TrapVisualizerServer,
    TrapData,
    MetricsResponse,
    TimelineEvent
)

@pytest.fixture
def redis_manager():
    """Create a mock Redis manager."""
    manager = Mock(spec=RedisManager)
    manager.get_cached.return_value = {
        "traps": [
            {
                "id": "1",
                "type": "FAKE_DUMP",
                "timestamp": datetime.now(UTC) - timedelta(hours=2),
                "confidence": 0.92,
                "price": 34500.0,
                "volume": 150.0,
                "description": "Fake dump detected",
                "success": False
            },
            {
                "id": "2",
                "type": "FAKE_PUMP",
                "timestamp": datetime.now(UTC) - timedelta(hours=1),
                "confidence": 0.85,
                "price": 35000.0,
                "volume": 100.0,
                "description": "Fake pump detected",
                "success": True
            }
        ]
    }
    return manager

@pytest.fixture
def server(redis_manager):
    """Create a test server instance."""
    return TrapVisualizerServer("Test Trap Visualizer", redis_manager)

@pytest.fixture
def client(server):
    """Create a test client."""
    return TestClient(server.app)

def test_root_endpoint(client):
    """Test the root endpoint returns correct message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to OMEGA BTC AI Trap Visualizer API"}

def test_get_metrics_success(client, redis_manager):
    """Test successful metrics retrieval."""
    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    
    assert "total_traps" in data
    assert data["total_traps"] == 2
    assert "traps_by_type" in data
    assert data["traps_by_type"] == {"FAKE_PUMP": 1, "FAKE_DUMP": 1}
    assert "average_confidence" in data
    assert abs(data["average_confidence"] - 0.885) < 0.01
    assert "success_rate" in data
    assert abs(data["success_rate"] - 0.5) < 0.01

def test_get_metrics_no_data(client, redis_manager):
    """Test metrics endpoint when no data is available."""
    redis_manager.get_cached.return_value = None

    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_traps"] == 0
    assert data["traps_by_type"] == {}
    assert data["average_confidence"] == 0.0
    assert data["success_rate"] == 0.0

def test_get_traps_success(client, redis_manager):
    """Test successful trap retrieval."""
    response = client.get("/api/traps")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 2
    assert data[0]["id"] == "1"
    assert data[0]["type"] == "FAKE_DUMP"
    assert data[0]["confidence"] == 0.92
    assert data[0]["success"] is False

def test_get_traps_with_filters(client, redis_manager):
    """Test trap retrieval with time and type filters."""
    # Test with type filter
    response = client.get("/api/traps?trap_type=FAKE_PUMP")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["type"] == "FAKE_PUMP"

    # Test with time filter
    now = datetime.now(UTC)
    start_time = (now - timedelta(hours=3)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    response = client.get(f"/api/traps?start_time={start_time}")
    if response.status_code == 422:
        print("Error response:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_timeline_success(client, redis_manager):
    """Test successful timeline retrieval."""
    response = client.get("/api/timeline")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 2
    assert data[0]["type"] == "FAKE_DUMP"
    assert data[0]["impact"] == "HIGH"  # Based on 0.92 confidence
    assert data[1]["type"] == "FAKE_PUMP"
    assert data[1]["impact"] == "MEDIUM"  # Based on 0.85 confidence

@pytest.mark.parametrize("endpoint", [
    "/api/metrics",
    "/api/traps",
    "/api/timeline"
])
def test_error_handling(endpoint, client, redis_manager):
    """Test error handling when Redis fails."""
    redis_manager.get_cached.side_effect = Exception("Redis error")
    response = client.get(endpoint)
    assert response.status_code == 500
    assert "Redis error" in response.json()["detail"]

@pytest.mark.parametrize("confidence,expected_impact", [
    (0.9, "HIGH"),
    (0.7, "MEDIUM"),
    (0.5, "LOW")
])
def test_impact_calculation(client, redis_manager, confidence, expected_impact):
    """Test impact calculation based on confidence levels."""
    redis_manager.get_cached.return_value = {
        "traps": [
            {
                "id": "1",
                "type": "TEST",
                "timestamp": datetime.now(UTC) - timedelta(hours=1),
                "confidence": confidence,
                "price": 35000.0,
                "volume": 100.0,
                "description": "Test trap",
                "success": True
            }
        ]
    }
    
    response = client.get("/api/timeline")
    assert response.status_code == 200
    events = response.json()
    assert len(events) == 1
    assert events[0]["impact"] == expected_impact

def test_get_traps_invalid_timestamp(client, redis_manager):
    """Test trap retrieval with invalid timestamp formats."""
    # Test invalid start_time format
    response = client.get("/api/traps?start_time=invalid-timestamp")
    assert response.status_code == 422
    assert "Invalid start_time format" in response.json()["detail"]

    # Test invalid end_time format
    response = client.get("/api/traps?end_time=invalid-timestamp")
    assert response.status_code == 422
    assert "Invalid end_time format" in response.json()["detail"]

    # Test end_time before start_time
    now = datetime.now(UTC)
    start_time = now.isoformat().replace("+00:00", "Z")
    end_time = (now - timedelta(hours=1)).isoformat().replace("+00:00", "Z")
    response = client.get(f"/api/traps?start_time={start_time}&end_time={end_time}")
    assert response.status_code == 422
    assert "start_time must be before end_time" in response.json()["detail"]

def test_get_traps_invalid_type(client, redis_manager):
    """Test trap retrieval with invalid trap type."""
    response = client.get("/api/traps?trap_type=INVALID_TYPE")
    assert response.status_code == 422
    assert "Invalid trap_type" in response.json()["detail"]

def test_get_traps_missing_fields(client, redis_manager):
    """Test trap retrieval with missing required fields."""
    # Mock data with missing required fields
    redis_manager.get_cached.return_value = {
        "traps": [
            {
                "id": "1",
                # Missing type field
                "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                "confidence": 0.92,
                "price": 34500.0,
                "volume": 150.0
            }
        ]
    }
    
    response = client.get("/api/traps")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # Invalid trap should be filtered out

def test_get_prices_invalid_data(client, redis_manager):
    """Test price retrieval with invalid data."""
    # Mock data with invalid price values
    redis_manager.get_cached.return_value = {
        "prices": [
            {
                "time": "invalid-timestamp",
                "open": "not-a-number",
                "close": 35000.0,
                "high": 36000.0,
                "low": 34000.0
            },
            {
                "time": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                "open": 35000.0,
                "close": 35000.0,
                "high": 34000.0,  # High lower than low
                "low": 36000.0
            }
        ]
    }
    
    response = client.get("/api/prices")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # Invalid prices should be filtered out

def test_get_timeline_invalid_hours(client, redis_manager):
    """Test timeline retrieval with invalid last_hours parameter."""
    # Test negative hours
    response = client.get("/api/timeline?hours=-1")
    assert response.status_code == 422
    assert "hours must be between 1 and 168" in response.json()["detail"]

    # Test hours exceeding maximum
    response = client.get("/api/timeline?hours=169")
    assert response.status_code == 422
    assert "hours must be between 1 and 168" in response.json()["detail"]

def test_get_timeline_invalid_traps(client, redis_manager):
    """Test timeline retrieval with invalid trap data."""
    # Mock data with invalid trap data
    redis_manager.get_cached.return_value = {
        "traps": [
            {
                "id": "1",
                "type": "FAKE_PUMP",
                "timestamp": "invalid-timestamp",
                "confidence": 0.92,
                "price": 34500.0,
                "volume": 150.0
            },
            {
                "id": "2",
                "type": "FAKE_DUMP",
                "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                "confidence": "not-a-number",  # Invalid confidence
                "price": 35000.0,
                "volume": 100.0
            }
        ]
    }
    
    response = client.get("/api/timeline")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # Invalid traps should be filtered out

def test_redis_connection_error(client, redis_manager):
    """Test handling of Redis connection errors."""
    redis_manager.get_cached.side_effect = Exception("Redis connection failed")
    
    response = client.get("/api/traps")
    assert response.status_code == 500
    assert "Redis connection failed" in response.json()["detail"]

def test_malicious_input(client, redis_manager):
    """Test handling of malicious input."""
    # Test SQL injection attempt
    response = client.get("/api/traps?trap_type=' OR '1'='1")
    assert response.status_code == 422
    
    # Test path traversal attempt
    response = client.get("/api/traps?start_time=../../../etc/passwd")
    assert response.status_code == 422
    
    # Test large payload
    large_payload = "A" * 10000
    response = client.get(f"/api/traps?start_time={large_payload}")
    assert response.status_code == 422

def test_data_validation(client, redis_manager):
    """Test validation of data fields."""
    # Test invalid confidence values
    redis_manager.get_cached.return_value = {
        "traps": [
            {
                "id": "1",
                "type": "FAKE_PUMP",
                "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                "confidence": 1.5,  # Invalid confidence > 1
                "price": 35000.0,
                "volume": 100.0
            }
        ]
    }
    
    response = client.get("/api/traps")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # Invalid confidence should be filtered out

    # Test invalid price values
    redis_manager.get_cached.return_value = {
        "traps": [
            {
                "id": "1",
                "type": "FAKE_PUMP",
                "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                "confidence": 0.85,
                "price": -1000.0,  # Invalid negative price
                "volume": 100.0
            }
        ]
    }
    
    response = client.get("/api/traps")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # Invalid price should be filtered out 