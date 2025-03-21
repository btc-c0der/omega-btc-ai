import pytest
from fastapi.testclient import TestClient
import json
from unittest.mock import patch, MagicMock, AsyncMock
import sys
import os
import redis
import asyncio
from fastapi import WebSocket, WebSocketDisconnect

# Import the server module
from omega_ai.visualizer.backend.reggae_dashboard_server import ReggaeDashboardServer

# Define fixtures for mock Redis
@pytest.fixture
def mock_redis_instance():
    """Create a mock Redis instance for testing"""
    mock = MagicMock()
    mock.ping.return_value = True
    return mock

@pytest.fixture
def mock_redis_with_data(mock_redis_instance):
    """Create a mock Redis instance with predefined test data"""
    mock = mock_redis_instance
    
    # Set up trap probability data
    trap_data = {
        "probability": 0.75,
        "trap_type": "bull_trap",
        "timestamp": "2023-01-01T00:00:00Z",
        "source": "simulator"
    }
    mock.get.side_effect = lambda key: (
        json.dumps(trap_data) if key == "current_trap_probability" 
        else json.dumps({
            "has_position": True,
            "position_side": "long",
            "entry_price": 65000,
            "current_price": 66000,
            "position_size": 0.5,
            "pnl_percent": 1.54,
            "pnl_usd": 500,
            "timestamp": "2023-06-01T12:00:00Z"
        }) if key == "current_position"
        else None
    )
    
    # Set up mock keys
    mock.keys.return_value = ["current_trap_probability", "current_position", "trap_history"]
    mock.type.return_value = "string"
    
    return mock

class TestReggaeDashboardServer:
    """Test suite for ReggaeDashboardServer class"""
    
    def test_initialization(self):
        """Test basic initialization of ReggaeDashboardServer"""
        with patch('redis.Redis') as mock_redis:
            mock_redis_instance = MagicMock()
            mock_redis.return_value = mock_redis_instance
            # Mock ping to simulate successful connection
            mock_redis_instance.ping.return_value = True
            
            # Create server instance
            server = ReggaeDashboardServer()
            
            # Check basic attributes
            assert server.app is not None
            assert server.active_connections == set()
            assert server.redis_client is not None
    
    def test_health_check_endpoint(self):
        """Test health check endpoint"""
        with patch('redis.Redis') as mock_redis:
            mock_redis_instance = MagicMock()
            mock_redis.return_value = mock_redis_instance
            # Mock ping and get to simulate successful connection
            mock_redis_instance.ping.return_value = True
            mock_redis_instance.get.return_value = json.dumps({
                "probability": 0.7,
                "trap_type": "bull_trap",
                "timestamp": "2023-01-01T00:00:00Z"
            })
            
            # Create server instance and test client
            server = ReggaeDashboardServer()
            client = TestClient(server.app)
            
            # Test health check endpoint
            response = client.get("/api/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["redis"] == "connected"
            assert "timestamp" in data
    
    def test_health_check_endpoint_redis_disconnected(self):
        """Test health check endpoint when Redis is disconnected"""
        with patch('redis.Redis') as mock_redis:
            # Make both the class Redis connection and the health check connection fail
            mock_redis.side_effect = redis.ConnectionError("Connection failed")
            
            # Create a server with no Redis client
            server = ReggaeDashboardServer()
            server.redis_client = None  # Ensure redis client is None
            
            # Create a test client
            client = TestClient(server.app)
            
            # Override the health check Redis creation to simulate connection failure
            with patch('omega_ai.visualizer.backend.reggae_dashboard_server.redis.Redis') as mock_redis_in_health:
                mock_redis_in_health.side_effect = redis.ConnectionError("Connection failed during health check")
                
                # Test the health endpoint
                response = client.get("/api/health")
                assert response.status_code == 200
                
                # Verify response data shows disconnected
                data = response.json()
                assert data["status"] == "healthy"
                assert data["redis"] == "disconnected"
                assert "timestamp" in data
    
    def test_trap_probability_endpoint(self):
        """Test trap probability endpoint"""
        with patch('redis.Redis', autospec=True) as mock_redis_class:
            # Setup mock Redis
            mock_redis_instance = MagicMock()
            mock_redis_class.return_value = mock_redis_instance
            
            # Add trap probability data
            trap_data = {
                "probability": 0.75,
                "trap_type": "bull_trap",
                "timestamp": "2023-01-01T00:00:00Z",
                "source": "simulator"
            }
            mock_redis_instance.get.return_value = json.dumps(trap_data)
            
            # Create server with mock
            server = ReggaeDashboardServer()
            
            # Manual patch of the _get_trap_probability method
            with patch.object(server, '_get_trap_probability', return_value=trap_data):
                client = TestClient(server.app)
                
                # Test the endpoint
                response = client.get("/api/trap-probability")
                assert response.status_code == 200
                
                # Verify response
                data = response.json()
                assert data["probability"] == 0.75
                assert data["trap_type"] == "bull_trap"
                assert "timestamp" in data
    
    def test_position_endpoint(self):
        """Test position endpoint"""
        with patch('redis.Redis', autospec=True) as mock_redis_class:
            # Setup mock Redis
            mock_redis_instance = MagicMock()
            mock_redis_class.return_value = mock_redis_instance
            
            # Add position data
            position_data = {
                "has_position": True,
                "position_side": "long",
                "entry_price": 65000,
                "current_price": 66000,
                "position_size": 0.5,
                "pnl_percent": 1.54,
                "pnl_usd": 500,
                "timestamp": "2023-06-01T12:00:00Z"
            }
            mock_redis_instance.get.return_value = json.dumps(position_data)
            
            # Create server with mock
            server = ReggaeDashboardServer()
            
            # Manual patch of the _get_position_data method
            with patch.object(server, '_get_position_data', return_value=position_data):
                client = TestClient(server.app)
                
                # Test the endpoint
                response = client.get("/api/position")
                assert response.status_code == 200
                
                # Verify response
                data = response.json()
                assert data["has_position"] is True
                assert data["position_side"] == "long"
                assert data["pnl_percent"] == 1.54
                assert data["pnl_usd"] == 500
    
    def test_redis_keys_endpoint(self):
        """Test Redis keys endpoint"""
        with patch('redis.Redis') as mock_redis:
            mock_redis_instance = MagicMock()
            mock_redis.return_value = mock_redis_instance
            
            # Mock Redis keys method
            mock_redis_instance.keys.return_value = ["key1", "key2", "key3"]
            mock_redis_instance.type.return_value = "string"
            mock_redis_instance.get.return_value = "value"
            
            # Create server instance and test client
            server = ReggaeDashboardServer()
            server.redis_client = mock_redis_instance
            client = TestClient(server.app)
            
            # Test endpoint
            response = client.get("/api/redis-keys")
            assert response.status_code == 200
            data = response.json()
            assert "keys" in data
            assert len(data["keys"]) == 3
    
    def test_generate_jah_message(self):
        """Test JAH message generation"""
        with patch('redis.Redis'):
            server = ReggaeDashboardServer()
            
            # Test with low probability
            low_message = server._generate_jah_message(0.3)
            assert "AWARE" in low_message
            
            # Test with medium-low probability
            med_low_message = server._generate_jah_message(0.5)
            assert "PATH" in med_low_message
            
            # Test with medium-high probability
            med_high_message = server._generate_jah_message(0.7)
            assert "VIBRATIONS" in med_high_message
            
            # Test with high probability
            high_message = server._generate_jah_message(0.9)
            assert "HIGH TRAP" in high_message
            
            # Test with dict input
            dict_message = server._generate_jah_message({"probability": 0.3})
            assert "AWARE" in dict_message
    
    def test_broadcast_method(self):
        """Test broadcast method directly"""
        with patch('redis.Redis'):
            server = ReggaeDashboardServer()
            
            # Create mock WebSockets
            mock_socket1 = AsyncMock(spec=WebSocket)
            mock_socket2 = AsyncMock(spec=WebSocket)
            
            # Add sockets to active connections
            server.active_connections = {mock_socket1, mock_socket2}
            
            # Test broadcasting a message
            async def test_broadcast():
                message = {"test": "data"}
                await server.broadcast(message)
                
                # Verify both WebSockets got the message
                mock_socket1.send_json.assert_called_once_with(message)
                mock_socket2.send_json.assert_called_once_with(message)
            
            # Run the coroutine
            asyncio.run(test_broadcast())
    
    def test_update_task_attributes(self):
        """Test update task attributes in startup/shutdown methods"""
        with patch('redis.Redis'):
            server = ReggaeDashboardServer()
            
            # Initial state
            assert server.update_task is None
            
            # Mock the broadcast_updates method
            server.broadcast_updates = AsyncMock()
            
            # Call startup method directly
            async def test_startup():
                # Create a coroutine to test startup
                await server.startup()
                # Verify update_task is created
                assert server.update_task is not None
                # Call shutdown method
                await server.shutdown()
                # Verify update_task is cancelled
                assert server.update_task is None or server.update_task.cancelled()
            
            # Run the test
            asyncio.run(test_startup())
    
    def test_websocket_connection(self):
        """Test WebSocket connection handling"""
        with patch('redis.Redis'):
            server = ReggaeDashboardServer()
            
            # Create a mock WebSocket
            mock_socket = AsyncMock(spec=WebSocket)
            
            # Test accepting a WebSocket directly
            server.active_connections.add(mock_socket)
            
            # Verify socket was added to active connections
            assert mock_socket in server.active_connections
            
            # Test removing a WebSocket
            server.active_connections.remove(mock_socket)
            
            # Verify socket was removed from active connections
            assert mock_socket not in server.active_connections
            
    def test_websocket_endpoint(self):
        """Test WebSocket endpoint handling"""
        with patch('redis.Redis'):
            server = ReggaeDashboardServer()
            
            # Verify the websocket endpoint is registered
            assert any(route.path == "/ws" for route in server.app.routes) 