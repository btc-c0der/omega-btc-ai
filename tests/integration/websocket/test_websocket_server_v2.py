
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

"""Tests for WebSocket Server V2 functionality.

This test suite covers the enhanced features of the WebSocket Server V2:
1. Connection management
2. Message handling
3. SSL/TLS support
4. Error handling
5. Performance monitoring
6. Resource cleanup
7. Client state tracking
8. Security features
"""

import pytest
import asyncio
import websockets
import json
import os
from datetime import datetime, UTC
from typing import Dict, Any, List
from omega_ai.mm_trap_detector.mm_websocket_server_v2 import (
    start_server, stop_server, ConnectionState, ClientInfo
)
from tests.integration.config.test_config_v2 import (
    TestConfig, get_websocket_uri, setup_test_environment,
    cleanup_test_environment, generate_test_data, create_ssl_context
)

# ---- Test Helpers ----

@pytest.fixture
async def setup_and_teardown():
    """Set up and tear down the test environment."""
    # Set up test environment
    setup_test_environment()
    
    # Ensure Redis is not using SSL for tests
    os.environ["REDIS_SSL"] = "false"
    
    # Ensure SSL certificate paths are set
    os.environ["SSL_CERT_PATH"] = TestConfig.ssl_cert_path
    os.environ["SSL_KEY_PATH"] = TestConfig.ssl_key_path
    
    # Create SSL certificates
    ssl_context = create_ssl_context()
    if not ssl_context:
        raise RuntimeError("Failed to create SSL context for testing")
    
    # Verify SSL certificates exist
    if not os.path.exists(TestConfig.ssl_cert_path):
        raise RuntimeError(f"SSL certificate not found at {TestConfig.ssl_cert_path}")
    if not os.path.exists(TestConfig.ssl_key_path):
        raise RuntimeError(f"SSL key not found at {TestConfig.ssl_key_path}")
    
    # Start WebSocket server
    await start_server()
    
    yield
    
    # Stop WebSocket server
    await stop_server()
    
    # Clean up test environment
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
async def test_websocket_v2_initial_connection(setup_and_teardown):
    """Test initial WebSocket connection."""
    uri = get_websocket_uri(use_ssl=True)
    async with websockets.connect(uri, ssl=True) as websocket:
        # Send initial message
        message = {"type": "hello", "data": "test"}
        await websocket.send(json.dumps(message))
        
        # Receive response
        response = await websocket.recv()
        data = json.loads(response)
        
        assert data["type"] == "welcome"
        assert "timestamp" in data
        assert datetime.fromisoformat(data["timestamp"]) <= datetime.now(UTC)

@pytest.mark.asyncio
async def test_websocket_v2_client_message(setup_and_teardown):
    """Test sending and receiving messages."""
    uri = get_websocket_uri(use_ssl=True)
    async with websockets.connect(uri, ssl=True) as websocket:
        # Send test message
        message = {"type": "test", "data": "Hello, World!"}
        await websocket.send(json.dumps(message))
        
        # Receive acknowledgment
        response = await websocket.recv()
        data = json.loads(response)
        
        assert data["type"] == "ack"
        assert "timestamp" in data
        assert datetime.fromisoformat(data["timestamp"]) <= datetime.now(UTC)

@pytest.mark.asyncio
async def test_websocket_v2_disconnect(setup_and_teardown):
    """Test client disconnection handling."""
    uri = get_websocket_uri(use_ssl=True)
    async with websockets.connect(uri, ssl=True) as websocket:
        # Send message before disconnect
        message = {"type": "test", "data": "pre-disconnect"}
        await websocket.send(json.dumps(message))
        
        # Receive acknowledgment
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "ack"
    
    # Wait for server to process disconnect
    await asyncio.sleep(1)

@pytest.mark.asyncio
async def test_websocket_v2_broadcast(setup_and_teardown):
    """Test broadcasting messages to multiple clients."""
    uri = get_websocket_uri(use_ssl=True)
    clients = []
    try:
        # Connect multiple clients
        for _ in range(3):
            client = await websockets.connect(uri, ssl=True)
            clients.append(client)
        
        # Send broadcast message from first client
        message = {"type": "broadcast", "data": "Hello, everyone!"}
        await clients[0].send(json.dumps(message))
        
        # Verify all clients receive the broadcast
        for client in clients:
            response = await client.recv()
            data = json.loads(response)
            assert data["type"] == "broadcast"
            assert data["data"] == "Hello, everyone!"
            assert "timestamp" in data
    finally:
        # Clean up clients
        for client in clients:
            await client.close()

@pytest.mark.asyncio
async def test_websocket_v2_reconnection(setup_and_teardown):
    """Test client reconnection handling."""
    uri = get_websocket_uri(use_ssl=True)
    async with websockets.connect(uri, ssl=True) as websocket:
        # Initial connection
        message = {"type": "hello", "data": "initial"}
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        assert json.loads(response)["type"] == "welcome"
    
    # Reconnect
    async with websockets.connect(uri, ssl=True) as websocket:
        message = {"type": "hello", "data": "reconnected"}
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "welcome"

@pytest.mark.asyncio
async def test_websocket_v2_large_message(setup_and_teardown):
    """Test handling of large messages."""
    uri = get_websocket_uri(use_ssl=True)
    async with websockets.connect(uri, ssl=True) as websocket:
        # Generate large message
        large_data = "x" * (1024 * 1024 - 100)  # Just under 1MB
        message = {
            "type": "large_message",
            "data": large_data
        }
        await websocket.send(json.dumps(message))
        
        # Verify response
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "ack"
        assert "timestamp" in data

@pytest.mark.asyncio
async def test_websocket_v2_concurrent_connections(setup_and_teardown):
    """Test handling multiple concurrent connections."""
    uri = get_websocket_uri(use_ssl=True)
    clients = []
    try:
        # Create multiple concurrent connections
        for i in range(5):
            client = await websockets.connect(uri, ssl=True)
            clients.append(client)
            
            # Send message from each client
            message = {"type": "test", "data": f"client_{i}"}
            await client.send(json.dumps(message))
            
            # Verify response
            response = await client.recv()
            data = json.loads(response)
            assert data["type"] == "welcome"
            
        # Send messages from all clients simultaneously
        await asyncio.gather(*(
            client.send(json.dumps({"type": "test", "data": f"concurrent_{i}"}))
            for i, client in enumerate(clients)
        ))
        
        # Verify all responses
        responses = await asyncio.gather(*(
            client.recv()
            for client in clients
        ))
        
        for response in responses:
            data = json.loads(response)
            assert data["type"] == "ack"
            assert "timestamp" in data
    finally:
        # Clean up
        for client in clients:
            await client.close()

@pytest.mark.asyncio
async def test_websocket_v2_error_handling(setup_and_teardown):
    """Test error handling for invalid messages."""
    uri = get_websocket_uri(use_ssl=True)
    async with websockets.connect(uri, ssl=True) as websocket:
        # Send invalid JSON
        await websocket.send("invalid json")
        
        # Verify error response
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "error"
        assert "message" in data
        
        # Send message too large
        large_data = "x" * (1024 * 1024 + 100)  # Over 1MB
        message = {
            "type": "large_message",
            "data": large_data
        }
        await websocket.send(json.dumps(message))
        
        # Verify error response
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "error"
        assert "message" in data

@pytest.mark.asyncio
async def test_websocket_v2_connection_timeout(setup_and_teardown):
    """Test connection timeout handling."""
    uri = get_websocket_uri(use_ssl=True)
    async with websockets.connect(uri, ssl=True, close_timeout=0.1) as websocket:
        # Send initial message
        message = {"type": "hello", "data": "test"}
        await websocket.send(json.dumps(message))
        
        # Verify welcome response
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "welcome"
        
        # Wait for timeout
        await asyncio.sleep(0.2)
        
        # Attempt to send message after timeout
        try:
            await websocket.send(json.dumps({"type": "test", "data": "after_timeout"}))
            assert False, "Should have raised ConnectionClosed"
        except websockets.ConnectionClosed:
            pass

@pytest.mark.asyncio
async def test_websocket_v2_data_consistency(setup_and_teardown):
    """Test data consistency across multiple messages."""
    uri = get_websocket_uri(use_ssl=True)
    async with websockets.connect(uri, ssl=True) as websocket:
        # Send multiple messages with increasing sequence numbers
        for i in range(5):
            message = {
                "type": "sequence",
                "sequence": i,
                "data": f"message_{i}"
            }
            await websocket.send(json.dumps(message))
            
            # Verify response maintains sequence
            response = await websocket.recv()
            data = json.loads(response)
            assert data["type"] == "ack"
            assert "timestamp" in data
            if "sequence" in data:
                assert data["sequence"] == i

@pytest.mark.asyncio
async def test_websocket_v2_heartbeat(websocket_server):
    """Test heartbeat mechanism."""
    uri = get_websocket_uri(use_ssl=False)
    
    async with websockets.connect(uri) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Send heartbeat
        message = {
            "type": "heartbeat",
            "timestamp": datetime.now(UTC).isoformat()
        }
        await websocket.send(json.dumps(message))
        
        # Receive heartbeat response
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "heartbeat"
        assert "timestamp" in data
        assert "status" in data
        assert data["status"] == "alive" 