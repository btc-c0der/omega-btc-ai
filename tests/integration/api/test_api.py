
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

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest
from pathlib import Path
from mm_trap_visualizer.server import app, load_latest_dump
from datetime import datetime

def calculate_impact(confidence: float) -> str:
    """Calculate impact level based on confidence score."""
    if confidence >= 0.8:
        return "high"
    elif confidence >= 0.6:
        return "medium"
    else:
        return "low"

@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient):
    """Test the root endpoint."""
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to MM Trap Visualizer API"}

@pytest.mark.asyncio
async def test_metrics_endpoint(async_client: AsyncClient, mock_redis_dump: Path, monkeypatch):
    """Test the /api/metrics endpoint."""
    monkeypatch.setattr("mm_trap_visualizer.server.load_latest_dump", lambda: str(mock_redis_dump))
    response = await async_client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "total_traps" in data
    assert "traps_by_type" in data
    assert "average_confidence" in data
    assert "time_distribution" in data
    assert "success_rate" in data

@pytest.mark.asyncio
async def test_traps_endpoint(async_client: AsyncClient, mock_redis_dump: Path, monkeypatch):
    """Test the /api/traps endpoint."""
    monkeypatch.setattr("mm_trap_visualizer.server.load_latest_dump", lambda: str(mock_redis_dump))
    response = await async_client.get("/api/traps")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_traps_endpoint_with_filters(
    async_client: AsyncClient,
    mock_redis_dump: Path,
    monkeypatch
):
    """Test the /api/traps endpoint with filters."""
    monkeypatch.setattr("mm_trap_visualizer.server.load_latest_dump", lambda: str(mock_redis_dump))
    response = await async_client.get("/api/traps?trap_type=bullish")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_timeline_endpoint(async_client: AsyncClient, mock_redis_dump: Path, monkeypatch):
    """Test the /api/timeline endpoint."""
    monkeypatch.setattr("mm_trap_visualizer.server.load_latest_dump", lambda: str(mock_redis_dump))
    response = await async_client.get("/api/timeline")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_error_handling_no_dump(client: TestClient, monkeypatch):
    """Test error handling when no dump file is available."""
    def mock_load_latest_dump():
        raise FileNotFoundError("No dump file found")

    monkeypatch.setattr("mm_trap_visualizer.server.load_latest_dump", mock_load_latest_dump)

    response = client.get("/api/metrics")
    assert response.status_code == 500
    assert "detail" in response.json()
    assert response.json()["detail"] == "No dump file found"

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
        return {
            "trap_detections": [{
                "id": "1",
                "type": "invalid",
                "timestamp": "2024-03-20T12:00:00Z",
                "confidence": 0.5,
                "price": 50000.0,
                "volume": 100.0,
                "metadata": {}
            }]
        }

    monkeypatch.setattr("mm_trap_visualizer.server.load_latest_dump", mock_load_latest_dump)

    response = client.get(endpoint)
    assert response.status_code == 500
    assert "detail" in response.json()

@pytest.mark.parametrize("confidence,expected", [
    (0.9, "high"),
    (0.7, "medium"),
    (0.5, "low")
])
def test_impact_calculation(confidence: float, expected: str):
    """Test impact calculation based on confidence score."""
    assert calculate_impact(confidence) == expected 