import pytest
import asyncio
import websockets
import json
from unittest.mock import patch, AsyncMock, MagicMock, call

from omega_ai.mm_trap_detector.mm_websocket_server import handler, broadcast

class TestWebSocketServer:
    """Tests for the Market Maker Trap WebSocket Server."""
    
    @pytest.mark.asyncio
    async def test_handler_new_connection(self):
        """Test handler with a new websocket connection."""
        # Arrange
        connected = set()
        websocket = AsyncMock()
        
        # Setup receive behavior: first return valid message, then raise connection closed
        websocket.recv.side_effect = [
            json.dumps({"price": 80000}), 
            websockets.exceptions.ConnectionClosedOK(None, None)  # This is a proper exception
        ]
        path = "/"
        
        # Act
        with patch('omega_ai.mm_trap_detector.mm_websocket_server.CONNECTED', connected):
            await handler(websocket, path)
        
        # Assert
        assert websocket in connected
        websocket.recv.assert_called()
        websocket.send.assert_called_once_with(json.dumps({"price": 80000}))
        assert len(connected) == 0  # Should be removed on disconnect
    
    @pytest.mark.asyncio
    async def test_broadcast(self):
        """Test broadcasting messages to connected clients."""
        # Arrange
        websocket1 = AsyncMock()
        websocket2 = AsyncMock()
        connected = {websocket1, websocket2}
        message = json.dumps({"btc_price": 81000.0})
        
        # Act
        with patch('omega_ai.mm_trap_detector.mm_websocket_server.CONNECTED', connected):
            await broadcast(message)
        
        # Assert
        websocket1.send.assert_called_once_with(message)
        websocket2.send.assert_called_once_with(message)
    
    @pytest.mark.asyncio
    async def test_broadcast_with_connection_error(self):
        """Test broadcasting with connection errors."""
        # Arrange
        websocket1 = AsyncMock()
        websocket2 = AsyncMock()
        
        # Make one of the websockets fail on send with a proper exception
        websocket2.send.side_effect = websockets.exceptions.ConnectionClosedOK(None, None)
        
        connected = {websocket1, websocket2}
        message = json.dumps({"btc_price": 81000.0})
        
        # Act
        with patch('omega_ai.mm_trap_detector.mm_websocket_server.CONNECTED', connected):
            await broadcast(message)
        
        # Assert
        websocket1.send.assert_called_once_with(message)
        websocket2.send.assert_called_once_with(message)
        assert websocket2 not in connected  # Should be removed on error 

@pytest.mark.asyncio
async def test_handler():
    """Test handler with a new websocket connection."""
    # Arrange
    from omega_ai.mm_trap_detector.mm_websocket_server import handler, connected_clients
    
    # Create a clean test environment
    original_clients = set()
    
    # Mock websocket
    websocket = AsyncMock()
    websocket.remote_address = ("127.0.0.1", 1234)
    
    # Define a side effect for the __aiter__ call
    async def mock_aiter():
        yield json.dumps({"price": 80000})
        raise Exception("Connection closed")
    
    # Setup the mock to use our generator
    websocket.__aiter__.return_value = mock_aiter()
    
    # Act
    with patch('omega_ai.mm_trap_detector.mm_websocket_server.connected_clients', original_clients):
        with patch('omega_ai.mm_trap_detector.mm_websocket_server.broadcast') as mock_broadcast:
            await handler(websocket)
    
    # Assert
    mock_broadcast.assert_called_once_with(json.dumps({"price": 80000}))

@pytest.mark.asyncio
async def test_broadcast():
    """Test broadcasting messages to connected clients."""
    # Arrange
    from omega_ai.mm_trap_detector.mm_websocket_server import broadcast
    
    websocket1 = AsyncMock()
    websocket2 = AsyncMock()
    clients = {websocket1, websocket2}
    message = json.dumps({"btc_price": 81000.0})
    
    # Act
    with patch('omega_ai.mm_trap_detector.mm_websocket_server.connected_clients', clients):
        await broadcast(message)
    
    # Assert
    websocket1.send.assert_called_once_with(message)
    websocket2.send.assert_called_once_with(message) 