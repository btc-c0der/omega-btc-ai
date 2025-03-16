"""Tests for the MM Trap Visualizer API endpoints."""

import pytest
from datetime import datetime, timedelta
from fastapi import status

def test_root_endpoint(client):
    """Test the root endpoint returns the correct message."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "MM Trap Visualizer API"}

def test_metrics_endpoint(client, mock_environment):
    """Test the metrics endpoint returns correct statistics."""
    response = client.get("/api/metrics")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "total_traps" in data
    assert data["total_traps"] == 3
    assert "traps_by_type" in data
    assert len(data["traps_by_type"]) == 3
    assert data["traps_by_type"]["FAKE_PUMP"] == 1
    assert data["average_confidence"] > 0.8
    assert 0 <= data["success_rate"] <= 1

def test_traps_endpoint(client, mock_environment):
    """Test the traps endpoint with various filters."""
    # Test without filters
    response = client.get("/api/traps")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3
    
    # Test with time filter
    now = datetime.utcnow()
    start_time = (now - timedelta(hours=2)).isoformat()
    response = client.get(f"/api/traps?start_time={start_time}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    
    # Test with trap type filter
    response = client.get("/api/traps?trap_type=FAKE_PUMP")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["type"] == "FAKE_PUMP"

def test_timeline_endpoint(client, mock_environment):
    """Test the timeline endpoint returns events in correct order."""
    response = client.get("/api/timeline")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 3
    
    # Check chronological order (newest first)
    timestamps = [event["timestamp"] for event in data]
    assert timestamps == sorted(timestamps, reverse=True)
    
    # Test with last_hours filter
    response = client.get("/api/timeline?last_hours=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2

def test_error_handling(client, tmp_path):
    """Test error handling when data is missing or invalid."""
    # Test with non-existent dumps directory
    response = client.get("/api/metrics")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "No dumps directory found" in response.json()["detail"]
    
    # Test with invalid date format
    response = client.get("/api/traps?start_time=invalid-date")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.parametrize("confidence,expected_impact", [
    (0.9, "HIGH"),
    (0.7, "MEDIUM"),
    (0.5, "LOW")
])
def test_impact_calculation(client, mock_environment, confidence, expected_impact):
    """Test impact level calculation based on confidence scores."""
    now = datetime.utcnow()
    test_trap = {
        "type": "FAKE_PUMP",
        "timestamp": now.isoformat(),
        "confidence": confidence,
        "price": 35000.0
    }
    
    # Add test trap to mock data
    with open(f"{mock_environment}/mm_trap_data_test.json", "r+") as f:
        data = f.read()
        mock_data = eval(data)
        mock_data["trap_detections"].append(test_trap)
        f.seek(0)
        f.write(str(mock_data))
        f.truncate()
    
    response = client.get("/api/timeline")
    assert response.status_code == status.HTTP_200_OK
    
    events = [e for e in response.json() if e["timestamp"] == now.isoformat()]
    assert len(events) == 1
    assert events[0]["impact"] == expected_impact 