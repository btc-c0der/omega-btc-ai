
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

"""
Tests for the WebSocket Server V2 Component.

This test suite covers the enhanced features of the WebSocket server V2:
1. Client state tracking with ConnectionState enum
2. Client reconnection handling with configurable attempts
3. Client monitoring for inactive connections
4. Enhanced error handling and logging
5. SSL context handling for secure connections
"""

import pytest
import asyncio
import json
import ssl
from datetime import datetime, UTC
from unittest.mock import patch, AsyncMock, MagicMock
from websockets.legacy.server import WebSocketServerProtocol

from omega_ai.mm_trap_detector.mm_websocket_server_v2 import (
    handler, broadcast, validate_message, handle_client_reconnection,
    get_ssl_context, monitor_clients, ClientInfo, ConnectionState
)

# ---- Test Helpers ----

class MockWebSocketClosedError(Exception):
    """Mock WebSocket closed exception for testing."""
    pass

async def mock_generator(data):
    """Create an async generator that yields data then raises an exception."""
    for item in data:
        yield item
    raise MockWebSocketClosedError("Connection closed")

# ---- Fixtures ----

@pytest.fixture
def mock_websocket():
    """Create a mock WebSocket connection with controlled behavior."""
    websocket = AsyncMock(spec=WebSocketServerProtocol)
    websocket.remote_address = ("127.0.0.1", 1234)
    websocket.send.return_value = None
    return websocket

@pytest.fixture
def mock_connected_clients():
    """Create a mock dictionary for tracking connected clients."""
    return {}

@pytest.fixture
def mock_client_info(mock_websocket):
    """Create a mock ClientInfo instance."""
    return ClientInfo(
        websocket=mock_websocket,
        state=ConnectionState.CONNECTED,
        last_message=datetime.now(UTC),
        message_count=0,
        error_count=0
    )

# ---- Test Functions ----

@pytest.mark.asyncio
async def test_validate_message_success():
    """Test successful message validation."""
    message = json.dumps({"price": 80000})
    result = validate_message(message)
    assert result is not None
    assert result["price"] == 80000

@pytest.mark.asyncio
async def test_validate_message_invalid_json():
    """Test validation of invalid JSON message."""
    message = "invalid json"
    result = validate_message(message)
    assert result is None

@pytest.mark.asyncio
async def test_validate_message_too_large():
    """Test validation of message exceeding size limit."""
    large_message = "x" * (1024 * 1024 + 1)  # 1MB + 1 byte
    result = validate_message(large_message)
    assert result is None

@pytest.mark.asyncio
async def test_handler_new_connection(mock_websocket, mock_connected_clients):
    """Test handler with a new websocket connection."""
    # Arrange
    test_message = json.dumps({"price": 80000})
    mock_websocket.__aiter__.return_value = mock_generator([test_message])
    
    # Act
    with patch('omega_ai.mm_trap_detector.mm_websocket_server_v2.connected_clients', mock_connected_clients):
        with patch('omega_ai.mm_trap_detector.mm_websocket_server_v2.broadcast') as mock_broadcast:
            await handler(mock_websocket)
    
    # Assert
    client_id = f"{mock_websocket.remote_address[0]}:{mock_websocket.remote_address[1]}"
    assert client_id in mock_connected_clients
    client_info = mock_connected_clients[client_id]
    assert client_info.state == ConnectionState.DISCONNECTED
    assert client_info.message_count == 1
    mock_broadcast.assert_called_once_with(test_message)

@pytest.mark.asyncio
async def test_handle_client_reconnection(mock_websocket, mock_connected_clients):
    """Test client reconnection handling."""
    # Arrange
    client_id = f"{mock_websocket.remote_address[0]}:{mock_websocket.remote_address[1]}"
    client_info = ClientInfo(
        websocket=mock_websocket,
        state=ConnectionState.ERROR,
        last_message=datetime.now(UTC),
        message_count=0,
        error_count=0
    )
    mock_connected_clients[client_id] = client_info
    
    # Act
    with patch('omega_ai.mm_trap_detector.mm_websocket_server_v2.connected_clients', mock_connected_clients):
        result = await handle_client_reconnection(client_id, mock_websocket)
    
    # Assert
    assert result is True
    assert client_info.state == ConnectionState.CONNECTED
    assert client_info.error_count == 1

@pytest.mark.asyncio
async def test_handle_client_reconnection_max_attempts(mock_websocket, mock_connected_clients):
    """Test client reconnection handling with max attempts exceeded."""
    # Arrange
    client_id = f"{mock_websocket.remote_address[0]}:{mock_websocket.remote_address[1]}"
    client_info = ClientInfo(
        websocket=mock_websocket,
        state=ConnectionState.ERROR,
        last_message=datetime.now(UTC),
        message_count=0,
        error_count=4  # Exceeds MAX_RECONNECT_ATTEMPTS
    )
    mock_connected_clients[client_id] = client_info
    
    # Act
    with patch('omega_ai.mm_trap_detector.mm_websocket_server_v2.connected_clients', mock_connected_clients):
        result = await handle_client_reconnection(client_id, mock_websocket)
    
    # Assert
    assert result is False
    assert client_info.state == ConnectionState.ERROR

@pytest.mark.asyncio
async def test_monitor_clients(mock_websocket, mock_connected_clients):
    """Test client monitoring for inactive connections."""
    # Arrange
    client_id = f"{mock_websocket.remote_address[0]}:{mock_websocket.remote_address[1]}"
    old_time = datetime.now(UTC).replace(minute=0)
    client_info = ClientInfo(
        websocket=mock_websocket,
        state=ConnectionState.CONNECTED,
        last_message=old_time,  # 5 minutes old
        message_count=0,
        error_count=0
    )
    mock_connected_clients[client_id] = client_info
    
    # Act
    with patch('omega_ai.mm_trap_detector.mm_websocket_server_v2.connected_clients', mock_connected_clients):
        await monitor_clients()
    
    # Assert
    assert client_id not in mock_connected_clients
    mock_websocket.close.assert_called_once_with(1000, "Inactive client")

@pytest.mark.asyncio
async def test_broadcast_to_multiple_clients(mock_connected_clients):
    """Test broadcasting to multiple clients with error handling."""
    # Arrange
    client1 = AsyncMock()
    client2 = AsyncMock()
    client2.send.side_effect = Exception("Send failed")
    
    client_id1 = "127.0.0.1:1234"
    client_id2 = "127.0.0.1:5678"
    
    mock_connected_clients[client_id1] = ClientInfo(
        websocket=client1,
        state=ConnectionState.CONNECTED,
        last_message=datetime.now(UTC),
        message_count=0,
        error_count=0
    )
    mock_connected_clients[client_id2] = ClientInfo(
        websocket=client2,
        state=ConnectionState.CONNECTED,
        last_message=datetime.now(UTC),
        message_count=0,
        error_count=0
    )
    
    message = json.dumps({"btc_price": 81000})
    
    # Act
    with patch('omega_ai.mm_trap_detector.mm_websocket_server_v2.connected_clients', mock_connected_clients):
        await broadcast(message)
    
    # Assert
    client1.send.assert_called_once_with(message)
    client2.send.assert_called_once_with(message)
    assert client_id2 not in mock_connected_clients  # Failed client should be removed

def test_get_ssl_context():
    """Test SSL context creation."""
    # Arrange
    with patch('ssl.create_default_context') as mock_create_context:
        mock_context = MagicMock()
        mock_create_context.return_value = mock_context
        
        # Act
        context = get_ssl_context()
        
        # Assert
        assert context is not None
        mock_context.load_cert_chain.assert_called_once()
        assert mock_context.check_hostname is False
        assert mock_context.verify_mode == ssl.CERT_NONE

def test_get_ssl_context_missing_cert():
    """Test SSL context creation with missing certificate."""
    # Arrange
    with patch('ssl.create_default_context') as mock_create_context:
        mock_create_context.side_effect = FileNotFoundError("Certificate not found")
        
        # Act
        context = get_ssl_context()
        
        # Assert
        assert context is None 