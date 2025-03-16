"""Tests for the MM Trap Visualizer API endpoints."""

import pytest
from httpx import AsyncClient
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any
from fastapi import FastAPI
from fastapi.testclient import TestClient
from mm_trap_visualizer.server import app, TrapData

@pytest.fixture
async def async_client() -> AsyncClient:
    """Create an async test client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def test_client() -> TestClient:
    """Create a sync test client."""
    return TestClient(app)

@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to MM Trap Visualizer API"}

@pytest.fixture
def mock_trap_data():
    return [
        {
            "id": "1",
            "type": "bullish",
            "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
            "confidence": 0.85,
            "price": 100
        },
        {
            "id": "2",
            "type": "bearish",
            "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
            "confidence": 0.92,
            "price": 110
        },
        {
            "id": "3",
            "type": "bullish",
            "timestamp": (datetime.now() - timedelta(hours=3)).isoformat(),
            "confidence": 0.78,
            "price": 105
        }
    ]

@pytest.fixture
def mock_redis_dump(tmp_path, mock_trap_data):
    dump_file = tmp_path / "test_dump.json"
    with open(dump_file, "w") as f:
        json.dump({"trap_detections": mock_trap_data}, f)
    return dump_file

@pytest.mark.asyncio
async def test_metrics_endpoint(
    async_client: AsyncClient,
    mock_redis_dump: Path,
    expected_metrics: Dict[str, Any],
    monkeypatch
):
    monkeypatch.setattr("server.get_latest_dump", lambda: str(mock_redis_dump))
    response = await async_client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_traps"] == expected_metrics["total_traps"]
    assert data["traps_by_type"] == expected_metrics["traps_by_type"]
    assert abs(data["average_confidence"] - expected_metrics["average_confidence"]) < 0.01
    assert data["success_rate"] == expected_metrics["success_rate"]

@pytest.mark.asyncio
async def test_traps_endpoint(
    async_client: AsyncClient,
    mock_redis_dump: Path,
    mock_trap_data: List[Dict[str, Any]],
    monkeypatch
):
    monkeypatch.setattr("server.get_latest_dump", lambda: str(mock_redis_dump))
    response = await async_client.get("/api/traps")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == len(mock_trap_data)
    assert all(key in data[0] for key in ["id", "type", "timestamp", "confidence", "price"])

@pytest.mark.asyncio
async def test_traps_endpoint_with_filters(
    async_client: AsyncClient,
    mock_redis_dump: Path,
    monkeypatch
):
    monkeypatch.setattr("server.get_latest_dump", lambda: str(mock_redis_dump))
    response = await async_client.get("/api/traps?trap_type=bullish")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 2
    assert all(trap["type"] == "bullish" for trap in data)

@pytest.mark.asyncio
async def test_timeline_endpoint(
    async_client: AsyncClient,
    mock_redis_dump: Path,
    mock_trap_data: List[Dict[str, Any]],
    monkeypatch
):
    monkeypatch.setattr("server.get_latest_dump", lambda: str(mock_redis_dump))
    response = await async_client.get("/api/timeline?last_hours=4")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == len(mock_trap_data)
    assert all(key in data[0] for key in ["timestamp", "type", "description", "confidence", "impact"])

@pytest.mark.asyncio
async def test_error_handling_no_dump(async_client: AsyncClient):
    response = await async_client.get("/api/metrics")
    assert response.status_code == 404
    assert "error" in response.json()

@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint", [
    "/api/metrics",
    "/api/traps",
    "/api/timeline"
])
async def test_error_handling_invalid_dump(
    endpoint: str,
    async_client: AsyncClient,
    mock_redis_dump: Path,
    monkeypatch
):
    monkeypatch.setattr("server.get_latest_dump", lambda: "nonexistent.json")
    response = await async_client.get(endpoint)
    assert response.status_code == 500
    assert "error" in response.json()

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
    assert "traps_by_type" in data
    assert "average_confidence" in data
    assert "time_distribution" in data
    assert "success_rate" in data
    
    assert isinstance(data["total_traps"], int)
    assert isinstance(data["traps_by_type"], dict)
    assert isinstance(data["average_confidence"], float)
    assert isinstance(data["time_distribution"], dict)
    assert isinstance(data["success_rate"], float)

def test_traps_endpoint(client: TestClient):
    """Test the traps endpoint with various filters."""
    # Test without filters
    response = client.get("/api/traps")
    assert response.status_code == 200
    traps = response.json()
    assert isinstance(traps, list)
    assert len(traps) > 0
    
    # Test with time filters
    now = datetime.now()
    start_time = (now - timedelta(hours=24)).isoformat()
    end_time = now.isoformat()
    
    response = client.get(f"/api/traps?start_time={start_time}&end_time={end_time}")
    assert response.status_code == 200
    filtered_traps = response.json()
    assert isinstance(filtered_traps, list)
    
    # Test with trap type filter
    response = client.get("/api/traps?trap_type=accumulation")
    assert response.status_code == 200
    type_filtered_traps = response.json()
    assert isinstance(type_filtered_traps, list)
    assert all(trap["type"] == "accumulation" for trap in type_filtered_traps)

def test_timeline_endpoint(client: TestClient):
    """Test the timeline endpoint."""
    # Test with default hours
    response = client.get("/api/timeline")
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)
    
    # Test with custom hours
    response = client.get("/api/timeline?last_hours=48")
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)
    
    # Verify chronological order
    if len(events) > 1:
        timestamps = [event["timestamp"] for event in events]
        assert timestamps == sorted(timestamps)
    
    # Test invalid hours parameter
    response = client.get("/api/timeline?last_hours=169")  # > 168 hours
    assert response.status_code == 422  # Validation error

def test_error_handling_no_dump(client: TestClient, monkeypatch):
    """Test error handling when no dump file is available."""
    def mock_load_latest_dump():
        raise FileNotFoundError("No dump file found")
    
    monkeypatch.setattr("mm_trap_visualizer.server.load_latest_dump", mock_load_latest_dump)
    
    response = client.get("/api/metrics")
    assert response.status_code == 500
    assert "error" in response.json()

@pytest.mark.parametrize("endpoint", [
    "/api/metrics",
    "/api/traps",
    "/api/timeline"
])
def test_error_handling_invalid_dump(
    endpoint: str,
    client: TestClient,
    mock_redis_dump: Path,
    monkeypatch
):
    """Test error handling with invalid dump data."""
    def mock_load_latest_dump():
        return "nonexistent.json"
    
    monkeypatch.setattr("mm_trap_visualizer.server.load_latest_dump", mock_load_latest_dump)
    
    response = client.get(endpoint)
    assert response.status_code == 500
    assert "error" in response.json()

@pytest.mark.parametrize("confidence,expected_impact", [
    (0.9, "high"),
    (0.7, "medium"),
    (0.5, "low")
])
def test_impact_calculation(client: TestClient, confidence: float, expected_impact: str):
    """Test impact calculation based on confidence scores."""
    trap = TrapData(
        id="test",
        type="test",
        timestamp=datetime.now(),
        confidence=confidence,
        price=45000.0,
        volume=1.0
    )
    
    response = client.get("/api/timeline")
    assert response.status_code == 200
    events = response.json()
    
    matching_events = [e for e in events if e["confidence"] == confidence]
    if matching_events:
        assert matching_events[0]["impact"] == expected_impact 