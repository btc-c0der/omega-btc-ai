
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

"""Tests for WebSocket functionality in the trap visualizer server."""

import pytest
from fastapi.testclient import TestClient
from fastapi import WebSocketDisconnect
from unittest.mock import Mock, patch, AsyncMock
import json
from datetime import datetime, UTC, timedelta
import asyncio
from omega_ai.utils.redis_manager import RedisManager
from omega_ai.visualizer.backend.unified_server import TrapVisualizerServer

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
            }
        ],
        "prices": [
            {
                "time": datetime.now(UTC).isoformat() + "Z",
                "open": 35000.0,
                "close": 35100.0,
                "high": 35200.0,
                "low": 34900.0
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

@pytest.mark.asyncio
async def test_websocket_initial_connection(client):
    """Test initial WebSocket connection and data."""
    with client.websocket_connect("/ws") as websocket:
        # Receive initial data
        data = websocket.receive_json()
        
        # Verify initial data structure
        assert data["type"] == "initial"
        assert "timestamp" in data
        assert "prices" in data
        assert "traps" in data
        assert "metrics" in data
        
        # Verify data content
        assert len(data["traps"]) == 1
        assert len(data["prices"]) == 1
        assert data["traps"][0]["type"] == "FAKE_DUMP"
        assert data["prices"][0]["open"] == 35000.0

@pytest.mark.asyncio
async def test_websocket_client_message(client):
    """Test handling of client messages."""
    with client.websocket_connect("/ws") as websocket:
        # Send test message
        websocket.send_text("ping")
        
        # Verify acknowledgment
        response = websocket.receive_json()
        assert response["type"] == "ack"
        assert response["message"] == "received"

@pytest.mark.asyncio
async def test_websocket_disconnect(client):
    """Test WebSocket disconnection handling."""
    with client.websocket_connect("/ws") as websocket:
        # Force disconnect
        websocket.close()
        
        # Verify connection is removed
        assert len(client.app.connection_manager.active_connections) == 0

@pytest.mark.asyncio
async def test_websocket_broadcast(client):
    """Test WebSocket broadcast functionality."""
    with client.websocket_connect("/ws") as websocket1, \
         client.websocket_connect("/ws") as websocket2:
        # Verify both connections are active
        assert len(client.app.connection_manager.active_connections) == 2
        
        # Simulate data update
        test_data = {
            "timestamp": datetime.now(UTC).isoformat() + "Z",
            "prices": [{"time": datetime.now(UTC).isoformat() + "Z", "open": 35000.0, "close": 35100.0, "high": 35200.0, "low": 34900.0}],
            "traps": [],
            "metrics": {"total_traps": 0, "traps_by_type": {}, "average_confidence": 0.0, "time_distribution": {}, "success_rate": 0.0}
        }
        
        # Broadcast test data
        await client.app.connection_manager.broadcast(test_data)
        
        # Verify both clients received the data
        data1 = websocket1.receive_json()
        data2 = websocket2.receive_json()
        assert data1 == test_data
        assert data2 == test_data

@pytest.mark.asyncio
async def test_websocket_reconnection(client):
    """Test WebSocket reconnection handling."""
    with client.websocket_connect("/ws") as websocket:
        # Simulate connection loss
        websocket.close()
        
        # Reconnect
        with client.websocket_connect("/ws") as new_websocket:
            # Verify new connection is established
            data = new_websocket.receive_json()
            assert data["type"] == "initial"
            assert len(client.app.connection_manager.active_connections) == 1

@pytest.mark.asyncio
async def test_websocket_large_message(client):
    """Test handling of large messages."""
    # Generate large test data
    large_traps = []
    for i in range(100):
        large_traps.append({
            "id": f"trap_{i}",
            "type": "FAKE_PUMP",
            "timestamp": datetime.now(UTC).isoformat() + "Z",
            "confidence": 0.85,
            "price": 35000.0,
            "volume": 100.0,
            "description": "Test trap",
            "success": True
        })
    
    test_data = {
        "timestamp": datetime.now(UTC).isoformat() + "Z",
        "prices": [],
        "traps": large_traps,
        "metrics": {"total_traps": len(large_traps), "traps_by_type": {"FAKE_PUMP": len(large_traps)}, "average_confidence": 0.85, "time_distribution": {}, "success_rate": 1.0}
    }
    
    with client.websocket_connect("/ws") as websocket:
        # Broadcast large data
        await client.app.connection_manager.broadcast(test_data)
        
        # Verify data is received correctly
        data = websocket.receive_json()
        assert len(data["traps"]) == 100
        assert data["metrics"]["total_traps"] == 100

@pytest.mark.asyncio
async def test_websocket_concurrent_connections(client):
    """Test handling of multiple concurrent connections."""
    connections = []
    try:
        # Create 10 concurrent connections
        for _ in range(10):
            websocket = client.websocket_connect("/ws")
            connections.append(websocket)
            websocket.__enter__()
        
        # Verify all connections are active
        assert len(client.app.connection_manager.active_connections) == 10
        
        # Test broadcast to all connections
        test_data = {
            "timestamp": datetime.now(UTC).isoformat() + "Z",
            "message": "test broadcast"
        }
        
        await client.app.connection_manager.broadcast(test_data)
        
        # Verify all connections received the message
        for websocket in connections:
            data = websocket.receive_json()
            assert data == test_data
            
    finally:
        # Clean up connections
        for websocket in connections:
            websocket.__exit__(None, None, None)

@pytest.mark.asyncio
async def test_websocket_error_handling(client):
    """Test WebSocket error handling."""
    with client.websocket_connect("/ws") as websocket:
        # Test invalid JSON message
        websocket.send_text("invalid json")
        response = websocket.receive_json()
        assert response["type"] == "ack"
        assert response["message"] == "received"
        
        # Test malformed message
        websocket.send_text(json.dumps({"type": "invalid"}))
        response = websocket.receive_json()
        assert response["type"] == "ack"
        assert response["message"] == "received"

@pytest.mark.asyncio
async def test_websocket_connection_timeout(client):
    """Test WebSocket connection timeout handling."""
    with patch("fastapi.WebSocket.accept") as mock_accept:
        mock_accept.side_effect = asyncio.TimeoutError()
        
        with pytest.raises(WebSocketDisconnect):
            with client.websocket_connect("/ws") as websocket:
                pass

@pytest.mark.asyncio
async def test_websocket_heartbeat(client):
    """Test WebSocket heartbeat mechanism."""
    with client.websocket_connect("/ws") as websocket:
        # Send heartbeat
        websocket.send_text("heartbeat")
        
        # Verify heartbeat response
        response = websocket.receive_json()
        assert response["type"] == "heartbeat"
        assert "timestamp" in response

@pytest.mark.asyncio
async def test_websocket_data_consistency(client, redis_manager):
    """Test data consistency across WebSocket updates."""
    # Set up test data
    test_time = datetime.now(UTC)
    test_data = {
        "traps": [
            {
                "id": "1",
                "type": "FAKE_PUMP",
                "timestamp": test_time.isoformat() + "Z",
                "confidence": 0.85,
                "price": 35000.0,
                "volume": 100.0,
                "description": "Test trap",
                "success": True
            }
        ]
    }
    redis_manager.get_cached.return_value = test_data
    
    with client.websocket_connect("/ws") as websocket:
        # Get initial data
        initial_data = websocket.receive_json()
        
        # Update Redis data
        redis_manager.get_cached.return_value = {
            "traps": test_data["traps"] + [{
                "id": "2",
                "type": "FAKE_DUMP",
                "timestamp": test_time.isoformat() + "Z",
                "confidence": 0.92,
                "price": 34500.0,
                "volume": 150.0,
                "description": "New trap",
                "success": False
            }]
        }
        
        # Wait for update
        await asyncio.sleep(1)
        
        # Get update data
        update_data = websocket.receive_json()
        
        # Verify data consistency
        assert len(update_data["traps"]) == 2
        assert update_data["traps"][0]["id"] == "1"
        assert update_data["traps"][1]["id"] == "2"
        assert update_data["traps"][1]["type"] == "FAKE_DUMP" 