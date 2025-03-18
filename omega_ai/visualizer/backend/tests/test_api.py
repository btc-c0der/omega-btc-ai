"""Tests for the MM Trap Visualizer API endpoints."""

import pytest
from httpx import AsyncClient
import json
from pathlib import Path
from datetime import datetime, timedelta, UTC
from typing import Dict, List, Any
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from omega_ai.utils.redis_manager import RedisManager
from omega_ai.visualizer.backend.src.mm_trap_visualizer.server import (
    MMTrapVisualizerServer,
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
    return MMTrapVisualizerServer("Test MM Trap Visualizer", redis_manager)

@pytest.fixture
def client(server):
    """Create a test client."""
    return TestClient(server.app)

@pytest.fixture
async def async_client(server):
    """Create an async test client."""
    async with AsyncClient(base_url="http://test", transport=server.app) as client:
        yield client

def test_root_endpoint(client: TestClient):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to MM Trap Visualizer API"}

def test_metrics_endpoint(client: TestClient):
    """Test the metrics endpoint."""
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

def test_traps_endpoint(client):
    """Test the traps endpoint with various filters."""
    # Test without filters
    response = client.get("/api/traps")
    assert response.status_code == 200
    traps = response.json()
    assert isinstance(traps, list)
    assert len(traps) > 0
    
    # Test with time filters
    now = datetime.now(UTC)
    start_time = (now - timedelta(hours=24)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    end_time = now.replace(microsecond=0).isoformat().replace("+00:00", "Z")
    
    response = client.get(f"/api/traps?start_time={start_time}&end_time={end_time}")
    if response.status_code == 422:
        print("Error response:", response.json())
    assert response.status_code == 200
    filtered_traps = response.json()
    assert isinstance(filtered_traps, list)
    
    # Test with trap type filter
    response = client.get("/api/traps?trap_type=FAKE_PUMP")
    assert response.status_code == 200
    type_filtered_traps = response.json()
    assert isinstance(type_filtered_traps, list)
    assert all(trap["type"] == "FAKE_PUMP" for trap in type_filtered_traps)

def test_timeline_endpoint(client: TestClient):
    """Test the timeline endpoint."""
    # Test with default hours
    response = client.get("/api/timeline")
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)
    
    # Test with custom hours
    response = client.get("/api/timeline?hours=48")
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)
    
    # Verify chronological order
    if len(events) > 1:
        timestamps = [event["timestamp"] for event in events]
        assert timestamps == sorted(timestamps)
    
    # Test invalid hours parameter
    response = client.get("/api/timeline?hours=169")  # > 168 hours
    assert response.status_code == 422  # Validation error

@pytest.mark.parametrize("endpoint", [
    "/api/metrics",
    "/api/traps",
    "/api/timeline"
])
def test_error_handling(endpoint: str, client: TestClient, redis_manager):
    """Test error handling when Redis fails."""
    redis_manager.get_cached.side_effect = Exception("Redis error")
    response = client.get(endpoint)
    assert response.status_code == 500
    assert "Redis error" in response.json()["detail"]

@pytest.mark.parametrize("confidence,expected_impact", [
    (0.9, "high"),
    (0.7, "medium"),
    (0.5, "low")
])
def test_impact_calculation(client: TestClient, redis_manager, confidence: float, expected_impact: str):
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