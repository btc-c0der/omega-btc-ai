"""Tests for WebSocket V2 functionality in the trap visualizer server.

This test suite covers the enhanced features of the WebSocket server V2:
1. Client state tracking and management
2. Enhanced error handling and recovery
3. SSL/TLS security features
4. Improved performance monitoring
5. Advanced connection management
"""

import pytest
import asyncio
import json
import websockets
from datetime import datetime, UTC
from websockets.exceptions import ConnectionClosed

from omega_ai.mm_trap_detector.mm_websocket_server_v2 import (
    ClientInfo, ConnectionState, validate_message, handle_client_reconnection
)

# ---- Test Helpers ----

@pytest.fixture
async def client():
    """Create a WebSocket client for testing."""
    uri = "ws://localhost:8766"  # Using SSL port for V2
    async with websockets.connect(uri) as websocket:
        yield websocket

@pytest.fixture
def mock_client_info():
    """Create a mock ClientInfo instance."""
    return ClientInfo(
        websocket=None,
        state=ConnectionState.CONNECTED,
        last_message=datetime.now(UTC),
        message_count=0,
        error_count=0
    )

# ---- Test Functions ----

@pytest.mark.asyncio
async def test_websocket_v2_initial_connection(client):
    """Test initial WebSocket V2 connection and data."""
    # Test connection establishment
    assert client.open
    
    # Test initial state
    initial_data = await client.recv()
    data = json.loads(initial_data)
    assert "server_version" in data
    assert data["server_version"] == "2.0.0"
    assert "connection_id" in data
    assert "ssl_enabled" in data
    assert data["ssl_enabled"] is True

@pytest.mark.asyncio
async def test_websocket_v2_client_message(client):
    """Test WebSocket V2 client message handling."""
    # Send a test message
    test_message = {
        "type": "price_update",
        "data": {"price": 80000}
    }
    await client.send(json.dumps(test_message))
    
    # Verify message was processed
    response = await client.recv()
    data = json.loads(response)
    assert data["status"] == "success"
    assert "processed_at" in data

@pytest.mark.asyncio
async def test_websocket_v2_disconnect(client):
    """Test WebSocket V2 disconnection handling."""
    # Send disconnect message
    await client.send(json.dumps({"type": "disconnect"}))
    
    # Verify graceful disconnect
    with pytest.raises(ConnectionClosed):
        await client.recv()

@pytest.mark.asyncio
async def test_websocket_v2_broadcast(client):
    """Test WebSocket V2 broadcast functionality."""
    # Connect multiple clients
    uri = "ws://localhost:8766"
    async with websockets.connect(uri) as client2:
        # Send broadcast message
        broadcast_msg = {
            "type": "broadcast",
            "data": {"message": "test broadcast"}
        }
        await client.send(json.dumps(broadcast_msg))
        
        # Verify both clients receive the message
        response1 = await client.recv()
        response2 = await client2.recv()
        
        data1 = json.loads(response1)
        data2 = json.loads(response2)
        assert data1["message"] == "test broadcast"
        assert data2["message"] == "test broadcast"

@pytest.mark.asyncio
async def test_websocket_v2_reconnection(client):
    """Test WebSocket V2 reconnection handling."""
    # Force disconnect
    await client.close()
    
    # Attempt reconnection
    uri = "ws://localhost:8766"
    async with websockets.connect(uri) as new_client:
        # Verify reconnection success
        response = await new_client.recv()
        data = json.loads(response)
        assert data["status"] == "reconnected"
        assert "reconnection_count" in data

@pytest.mark.asyncio
async def test_websocket_v2_large_message(client):
    """Test WebSocket V2 large message handling."""
    # Create large message (just under 1MB limit)
    large_data = {
        "type": "large_data",
        "data": {"payload": "x" * (1024 * 1024 - 100)}  # Leave room for JSON structure
    }
    
    # Send large message
    await client.send(json.dumps(large_data))
    
    # Verify message was processed
    response = await client.recv()
    data = json.loads(response)
    assert data["status"] == "success"
    assert "size" in data
    assert data["size"] < 1024 * 1024

@pytest.mark.asyncio
async def test_websocket_v2_concurrent_connections():
    """Test WebSocket V2 concurrent connection handling."""
    uri = "ws://localhost:8766"
    num_clients = 10
    
    async def connect_client():
        async with websockets.connect(uri) as websocket:
            await websocket.recv()  # Wait for initial message
            return websocket
    
    # Create multiple concurrent connections
    clients = await asyncio.gather(*[connect_client() for _ in range(num_clients)])
    
    # Verify all connections are active
    assert len(clients) == num_clients
    for client in clients:
        assert client.open
    
    # Clean up
    for client in clients:
        await client.close()

@pytest.mark.asyncio
async def test_websocket_v2_error_handling(client):
    """Test WebSocket V2 error handling."""
    # Send invalid message
    invalid_message = "invalid json"
    await client.send(invalid_message)
    
    # Verify error response
    response = await client.recv()
    data = json.loads(response)
    assert data["status"] == "error"
    assert "error_type" in data
    assert data["error_type"] == "invalid_message"

@pytest.mark.asyncio
async def test_websocket_v2_connection_timeout():
    """Test WebSocket V2 connection timeout handling."""
    uri = "ws://localhost:8766"
    with pytest.raises(ConnectionClosed):
        async with websockets.connect(uri, close_timeout=0.1) as websocket:
            await websocket.recv()

@pytest.mark.asyncio
async def test_websocket_v2_heartbeat(client):
    """Test WebSocket V2 heartbeat mechanism."""
    # Wait for heartbeat
    response = await client.recv()
    data = json.loads(response)
    assert data["type"] == "heartbeat"
    assert "timestamp" in data

@pytest.mark.asyncio
async def test_websocket_v2_data_consistency(client):
    """Test data consistency across WebSocket V2 updates."""
    # Send multiple updates
    updates = [
        {"price": 80000},
        {"price": 81000},
        {"price": 82000}
    ]
    
    for update in updates:
        await client.send(json.dumps({"type": "price_update", "data": update}))
        response = await client.recv()
        data = json.loads(response)
        assert data["status"] == "success"
        assert data["data"]["price"] == update["price"] 