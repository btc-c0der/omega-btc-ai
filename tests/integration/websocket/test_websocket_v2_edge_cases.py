"""Tests for WebSocket V2 edge cases and error handling.

This test suite covers edge cases and error handling scenarios for the WebSocket server V2:
1. Invalid message formats
2. Connection timeouts
3. SSL/TLS errors
4. Resource limits
5. Concurrent access
6. Error recovery
7. State transitions
8. Memory management
"""

import pytest
import asyncio
import json
import websockets
import ssl
from datetime import datetime, UTC
from typing import Dict, Any, List
from websockets.exceptions import ConnectionClosed
from omega_ai.mm_trap_detector.mm_websocket_server_v2 import (
    start_server, stop_server, ConnectionState, ClientInfo,
    validate_message, handle_client_reconnection, create_ssl_context
)
from tests.integration.config.test_config_v2 import (
    TestConfig, get_websocket_uri, setup_test_environment,
    cleanup_test_environment, generate_test_data
)

# ---- Test Helpers ----

@pytest.fixture(autouse=True)
async def setup_teardown():
    """Set up and tear down test environment."""
    setup_test_environment()
    yield
    cleanup_test_environment()

@pytest.fixture
async def websocket_server():
    """Start WebSocket server for testing."""
    server_task = asyncio.create_task(start_server())
    await asyncio.sleep(0.1)  # Give server time to start
    yield server_task
    await stop_server()
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

# ---- Test Functions ----

@pytest.mark.asyncio
async def test_websocket_v2_invalid_message_format(websocket_server):
    """Test handling of invalid message formats."""
    uri = get_websocket_uri()
    
    async with websockets.connect(uri) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Test invalid JSON
        await websocket.send("invalid json")
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "error"
        assert "invalid json" in data["message"].lower()
        
        # Test missing required fields
        message = {"type": "test"}  # Missing data field
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "error"
        assert "missing required" in data["message"].lower()

@pytest.mark.asyncio
async def test_websocket_v2_message_size_limit(websocket_server):
    """Test message size limit enforcement."""
    uri = get_websocket_uri()
    
    async with websockets.connect(uri) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Generate message exceeding size limit
        large_data = "x" * (1024 * 1024 + 1)  # 1MB + 1 byte
        message = {
            "type": "large_message",
            "data": large_data
        }
        await websocket.send(json.dumps(message))
        
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "error"
        assert "size limit" in data["message"].lower()

@pytest.mark.asyncio
async def test_websocket_v2_ssl_errors(websocket_server):
    """Test SSL/TLS error handling."""
    uri = get_websocket_uri(use_ssl=True)
    
    # Test with invalid certificate
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    with pytest.raises(ConnectionClosed):
        async with websockets.connect(uri, ssl=ssl_context) as websocket:
            await websocket.recv()

@pytest.mark.asyncio
async def test_websocket_v2_concurrent_access(websocket_server):
    """Test handling of concurrent access patterns."""
    uri = get_websocket_uri()
    clients = []
    try:
        # Create multiple concurrent connections
        for i in range(10):
            client = await websockets.connect(uri)
            clients.append(client)
            
            # Send messages simultaneously
            message = {
                "type": "concurrent_test",
                "data": f"client_{i}",
                "timestamp": datetime.now(UTC).isoformat()
            }
            await client.send(json.dumps(message))
        
        # Verify all responses
        responses = await asyncio.gather(*(
            client.recv()
            for client in clients
        ))
        
        for response in responses:
            data = json.loads(response)
            assert data["type"] in ["welcome", "ack"]
            assert "timestamp" in data
    finally:
        # Clean up
        for client in clients:
            await client.close()

@pytest.mark.asyncio
async def test_websocket_v2_error_recovery(websocket_server):
    """Test error recovery mechanisms."""
    uri = get_websocket_uri()
    
    async with websockets.connect(uri) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Simulate connection error
        message = {
            "type": "error_test",
            "data": "trigger_error",
            "timestamp": datetime.now(UTC).isoformat()
        }
        await websocket.send(json.dumps(message))
        
        # Verify error response
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "error"
        
        # Verify recovery
        message = {
            "type": "test",
            "data": "recovery_test",
            "timestamp": datetime.now(UTC).isoformat()
        }
        await websocket.send(json.dumps(message))
        
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "ack"

@pytest.mark.asyncio
async def test_websocket_v2_state_transitions(websocket_server):
    """Test client state transitions."""
    uri = get_websocket_uri()
    
    async with websockets.connect(uri) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Test state transitions
        states = [
            {"type": "state_test", "state": "connected"},
            {"type": "state_test", "state": "reconnecting"},
            {"type": "state_test", "state": "error"}
        ]
        
        for state_msg in states:
            await websocket.send(json.dumps(state_msg))
            response = await websocket.recv()
            data = json.loads(response)
            assert data["type"] == "state_update"
            assert data["state"] == state_msg["state"]

@pytest.mark.asyncio
async def test_websocket_v2_memory_management(websocket_server):
    """Test memory management and cleanup."""
    uri = get_websocket_uri()
    clients = []
    try:
        # Create multiple connections
        for i in range(20):
            client = await websockets.connect(uri)
            clients.append(client)
            
            # Send large messages
            message = {
                "type": "memory_test",
                "data": "x" * (100 * 1024),  # 100KB
                "timestamp": datetime.now(UTC).isoformat()
            }
            await client.send(json.dumps(message))
        
        # Verify responses
        responses = await asyncio.gather(*(
            client.recv()
            for client in clients
        ))
        
        for response in responses:
            data = json.loads(response)
            assert data["type"] == "ack"
    finally:
        # Clean up
        for client in clients:
            await client.close()

@pytest.mark.asyncio
async def test_websocket_v2_connection_limits(websocket_server):
    """Test connection limit handling."""
    uri = get_websocket_uri()
    clients = []
    try:
        # Attempt to exceed connection limit
        for i in range(100):  # Assuming limit is less than 100
            try:
                client = await websockets.connect(uri)
                clients.append(client)
            except ConnectionClosed:
                # Expected when limit is reached
                break
        
        # Verify at least some connections succeeded
        assert len(clients) > 0
        
        # Clean up
        for client in clients:
            await client.close()
    except Exception as e:
        # Clean up on any error
        for client in clients:
            await client.close()
        raise e 