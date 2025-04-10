
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

"""Tests for edge cases and error handling in the MM Trap Visualizer.

MIT License

Copyright (c) 2024 Omega BTC AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

This module contains test cases for edge cases and error handling in the MM Trap Visualizer.
It tests various scenarios including:
- Corrupted data handling
- Invalid timestamp formats
- Missing required fields
- Invalid parameter values
- Empty data handling
- Timezone edge cases
- Edge case confidence values
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import datetime, UTC, timedelta
from omega_ai.utils.redis_manager import RedisManager
from omega_ai.visualizer.backend.src.mm_trap_visualizer.server import MMTrapVisualizerServer

@pytest.fixture
def redis_manager():
    """Create a mock Redis manager."""
    return Mock(spec=RedisManager)

@pytest.fixture
def server(redis_manager):
    """Create a test server instance."""
    return MMTrapVisualizerServer("Test MM Trap Visualizer", redis_manager)

@pytest.fixture
def client(server):
    """Create a test client."""
    return TestClient(server.app)

def test_metrics_with_corrupted_data(client, redis_manager):
    """Test metrics endpoint with corrupted data."""
    redis_manager.get_cached.return_value = {"traps": None}
    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["total_traps"] == 0
    assert data["traps_by_type"] == {}
    assert data["average_confidence"] == 0.0
    assert data["success_rate"] == 0.0

def test_traps_with_invalid_timestamps(client, redis_manager):
    """Test traps endpoint with invalid timestamp data."""
    redis_manager.get_cached.return_value = {
        "traps": [
            {
                "id": "1",
                "type": "TEST",
                "timestamp": "invalid_timestamp",  # Invalid timestamp
                "confidence": 0.85,
                "price": 35000.0,
                "volume": 100.0,
                "description": "Test trap",
                "success": True
            }
        ]
    }
    response = client.get("/api/traps")
    assert response.status_code == 500
    assert "error" in response.json()["detail"].lower()

def test_traps_with_missing_fields(client, redis_manager):
    """Test traps endpoint with missing required fields."""
    redis_manager.get_cached.return_value = {
        "traps": [
            {
                "id": "1",
                # Missing required fields
                "confidence": 0.85,
                "price": 35000.0
            }
        ]
    }
    response = client.get("/api/traps")
    assert response.status_code == 500
    assert "error" in response.json()["detail"].lower()

def test_timeline_with_invalid_hours(client, redis_manager):
    """Test timeline endpoint with invalid hours parameter."""
    # Test with hours < 1
    response = client.get("/api/timeline?hours=0")
    assert response.status_code == 422
    
    # Test with hours > 168
    response = client.get("/api/timeline?hours=169")
    assert response.status_code == 422

def test_timeline_with_empty_data(client, redis_manager):
    """Test timeline endpoint with empty data."""
    redis_manager.get_cached.return_value = {"traps": []}
    response = client.get("/api/timeline")
    assert response.status_code == 200
    assert response.json() == []

def test_traps_with_timezone_edge_cases(client, redis_manager):
    """Test traps endpoint with timezone edge cases."""
    # Test with UTC timestamp
    now = datetime.now(UTC)
    redis_manager.get_cached.return_value = {
        "traps": [
            {
                "id": "1",
                "type": "TEST",
                "timestamp": now,
                "confidence": 0.85,
                "price": 35000.0,
                "volume": 100.0,
                "description": "Test trap",
                "success": True
            }
        ]
    }
    response = client.get("/api/traps")
    assert response.status_code == 200
    
    # Test with naive timestamp
    naive_now = datetime.now()
    redis_manager.get_cached.return_value = {
        "traps": [
            {
                "id": "1",
                "type": "TEST",
                "timestamp": naive_now,
                "confidence": 0.85,
                "price": 35000.0,
                "volume": 100.0,
                "description": "Test trap",
                "success": True
            }
        ]
    }
    response = client.get("/api/traps")
    assert response.status_code == 200

def test_metrics_with_edge_case_confidence(client, redis_manager):
    """Test metrics endpoint with edge case confidence values."""
    redis_manager.get_cached.return_value = {
        "traps": [
            {
                "id": "1",
                "type": "TEST",
                "timestamp": datetime.now(UTC),
                "confidence": 0.0,  # Minimum confidence
                "price": 35000.0,
                "volume": 100.0,
                "description": "Test trap",
                "success": False
            },
            {
                "id": "2",
                "type": "TEST",
                "timestamp": datetime.now(UTC),
                "confidence": 1.0,  # Maximum confidence
                "price": 35000.0,
                "volume": 100.0,
                "description": "Test trap",
                "success": True
            }
        ]
    }
    response = client.get("/api/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["average_confidence"] == 0.5
    assert data["success_rate"] == 0.5 