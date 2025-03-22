#!/usr/bin/env python3
"""
Test cases for Big Brother API endpoints
"""

import json
import pytest
import asyncio
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the server app for testing
from omega_ai.visualizer.backend.reggae_dashboard_server import ReggaeDashboardServer

# Create a test client
test_server = ReggaeDashboardServer()
client = TestClient(test_server.app)

# Mock Redis data
@pytest.fixture
def mock_redis_data():
    return {
        "long_position": {
            "entry_price": 84500,
            "size": 0.01,
            "leverage": 10,
            "direction": "LONG",
            "entry_time": "2023-03-22T10:00:00",
            "unrealized_pnl": 125.5,
            "take_profits": [{"percentage": 50, "price": 85500}],
            "stop_loss": 83000
        },
        "short_position": {
            "entry_price": 84200,
            "size": 0.015,
            "leverage": 5,
            "direction": "SHORT",
            "entry_time": "2023-03-22T10:00:00",
            "unrealized_pnl": -45.2,
            "take_profits": [{"percentage": 50, "price": 83200}],
            "stop_loss": 85700
        },
        "fibonacci:current_levels": {
            "direction": "LONG",
            "base_price": 84500,
            "levels": {
                "0.0": 84500,
                "0.236": 85003.2,
                "0.382": 85318.9,
                "0.5": 85565.0,
                "0.618": 85822.3,
                "0.786": 86178.5,
                "1.0": 86630.0,
                "1.618": 87845.7,
                "2.618": 89769.2
            }
        }
    }

@pytest.fixture
def mock_redis_client(mock_redis_data):
    """Create a mock Redis client that returns predefined data."""
    mock_client = MagicMock()
    
    # Mock the get method to return appropriate data
    def mock_get(key):
        # Map the keys to the mock data
        key_mapping = {
            "long_trader_position": json.dumps(mock_redis_data["long_position"]),
            "current_long_position": json.dumps(mock_redis_data["long_position"]),
            "dual_trader_long": json.dumps(mock_redis_data["long_position"]),
            "short_trader_position": json.dumps(mock_redis_data["short_position"]),
            "current_short_position": json.dumps(mock_redis_data["short_position"]),
            "dual_trader_short": json.dumps(mock_redis_data["short_position"]),
            "fibonacci_levels": json.dumps(mock_redis_data["fibonacci:current_levels"]),
            "fib_levels": json.dumps(mock_redis_data["fibonacci:current_levels"]),
            "fibonacci:targets": json.dumps(mock_redis_data["fibonacci:current_levels"])
        }
        return key_mapping.get(key, None)
    
    mock_client.get.side_effect = mock_get
    
    # Mock other Redis methods as needed
    mock_client.type.return_value = "string"
    mock_client.ping.return_value = True
    
    return mock_client

@pytest.fixture
def app_with_redis(mock_redis_client):
    """Create an app instance with a mock Redis client."""
    app = ReggaeDashboardServer()
    app.redis_client = mock_redis_client
    return app

def test_big_brother_data_endpoint(app_with_redis):
    """Test the /api/big-brother-data endpoint."""
    client = TestClient(app_with_redis.app)
    response = client.get("/api/big-brother-data")
    assert response.status_code == 200
    
    data = response.json()
    assert "long_position" in data
    assert "short_position" in data
    assert "fibonacci_levels" in data
    
    # Verify position data
    assert data["long_position"]["entry_price"] == 84500
    assert data["short_position"]["entry_price"] == 84200
    
    # Verify Fibonacci levels
    assert data["fibonacci_levels"]["direction"] == "LONG"
    assert "0.618" in data["fibonacci_levels"]["levels"]

@patch("subprocess.run")
def test_flow_3d_endpoint(mock_subprocess, app_with_redis):
    """Test the /api/flow/3d endpoint."""
    # Mock subprocess.run to return success
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = "3D visualization saved as test_flow_3d.png"
    mock_subprocess.return_value = mock_process
    
    # Create a mock file that the endpoint can find
    Path("test_flow_3d.png").touch()
    
    client = TestClient(app_with_redis.app)
    response = client.get("/api/flow/3d?hours=24")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert "image_url" in data
    assert data["hours"] == 24
    
    # Clean up the test file
    Path("test_flow_3d.png").unlink(missing_ok=True)

@patch("subprocess.run")
def test_flow_2d_endpoint(mock_subprocess, app_with_redis):
    """Test the /api/flow/2d endpoint."""
    # Mock subprocess.run to return success
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_process.stdout = "2D visualization saved as test_flow_2d.png"
    mock_subprocess.return_value = mock_process
    
    # Create a mock file that the endpoint can find
    Path("test_flow_2d.png").touch()
    
    client = TestClient(app_with_redis.app)
    response = client.get("/api/flow/2d?hours=12")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert "image_url" in data
    assert data["hours"] == 12
    
    # Clean up the test file
    Path("test_flow_2d.png").unlink(missing_ok=True)

@patch("subprocess.run")
def test_flow_endpoints_with_error(mock_subprocess, app_with_redis):
    """Test flow endpoints with subprocess error."""
    # Mock subprocess.run to return an error
    mock_process = MagicMock()
    mock_process.returncode = 1
    mock_process.stderr = "Error generating visualization"
    mock_subprocess.return_value = mock_process
    
    client = TestClient(app_with_redis.app)
    
    # Test 3D endpoint with error
    response = client.get("/api/flow/3d?hours=24")
    assert response.status_code == 200  # It still returns 200 but with error details
    
    data = response.json()
    assert data["status"] == "error"
    assert "fallback_image_url" in data
    
    # Test 2D endpoint with error
    response = client.get("/api/flow/2d?hours=12")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "error"
    assert "fallback_image_url" in data

def test_redis_connection_error():
    """Test behavior when Redis connection fails."""
    # Create server with no Redis connection
    app = ReggaeDashboardServer()
    app.redis_client = None
    
    client = TestClient(app.app)
    
    # Test big brother data endpoint
    response = client.get("/api/big-brother-data")
    assert response.status_code == 200
    assert "error" in response.json()
    
    # Test flow endpoints
    response = client.get("/api/flow/3d")
    assert response.status_code == 200
    assert "error" in response.json()
    
    response = client.get("/api/flow/2d")
    assert response.status_code == 200
    assert "error" in response.json()

if __name__ == "__main__":
    pytest.main(["-xvs", __file__]) 