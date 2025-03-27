import pytest
import json
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from omega_ai.visualizer.backend.reggae_dashboard_server import ReggaeDashboardServer

# Test data fixtures
@pytest.fixture
def sample_trap_data():
    return {
        "probability": 0.75,
        "trap_type": "bear_trap",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "message": "JAH WARNS OF TRAP VIBRATIONS!"
    }

@pytest.fixture
def sample_position_data():
    return {
        "has_position": True,
        "position_side": "long",
        "entry_price": 65000.0,
        "current_price": 65789.42,
        "position_size": 0.1,
        "pnl_percent": 1.21,
        "pnl_usd": 78.94,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@pytest.fixture
def mock_redis():
    redis_mock = MagicMock()
    redis_mock.ping.return_value = True
    return redis_mock

class TestReggaeDashboardServer:
    """Test suite for ReggaeDashboardServer"""
    
    def test_initialization(self, mock_redis):
        """Test server initialization"""
        with patch('redis.Redis', return_value=mock_redis):
            server = ReggaeDashboardServer()
            assert server.active_connections == []
            assert server.update_task is None
            assert server.redis_client is not None
    
    def test_redis_connection_failure(self):
        """Test handling of Redis connection failure"""
        with patch('redis.Redis', side_effect=Exception("Connection failed")):
            server = ReggaeDashboardServer()
            assert server.redis_client is None
    
    def test_health_check_endpoint(self, mock_redis):
        """Test health check endpoint"""
        with patch('redis.Redis', return_value=mock_redis):
            server = ReggaeDashboardServer()
            client = TestClient(server.app)
            
            response = client.get("/api/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["redis"] == "connected"
            assert "timestamp" in data
    
    def test_trap_probability_endpoint(self, mock_redis, sample_trap_data):
        """Test trap probability endpoint"""
        mock_redis.get.return_value = json.dumps(sample_trap_data)
        
        with patch('redis.Redis', return_value=mock_redis):
            server = ReggaeDashboardServer()
            client = TestClient(server.app)
            
            response = client.get("/api/trap-probability")
            assert response.status_code == 200
            data = response.json()
            assert data["probability"] == sample_trap_data["probability"]
            assert data["trap_type"] == sample_trap_data["trap_type"]
            assert "message" in data
    
    def test_position_endpoint(self, mock_redis, sample_position_data):
        """Test position endpoint"""
        mock_redis.get.return_value = json.dumps(sample_position_data)
        
        with patch('redis.Redis', return_value=mock_redis):
            server = ReggaeDashboardServer()
            client = TestClient(server.app)
            
            response = client.get("/api/position")
            assert response.status_code == 200
            data = response.json()
            assert data["has_position"] == sample_position_data["has_position"]
            assert data["position_side"] == sample_position_data["position_side"]
            assert data["entry_price"] == sample_position_data["entry_price"]
    
    def test_redis_keys_endpoint(self, mock_redis):
        """Test Redis keys endpoint"""
        # Mock Redis keys and their types
        mock_redis.keys.return_value = ["test:key1", "test:key2"]
        mock_redis.type.side_effect = ["string", "hash"]
        mock_redis.get.return_value = "test_value"
        mock_redis.hkeys.return_value = ["field1", "field2"]
        
        with patch('redis.Redis', return_value=mock_redis):
            server = ReggaeDashboardServer()
            client = TestClient(server.app)
            
            response = client.get("/api/redis-keys")
            assert response.status_code == 200
            data = response.json()
            assert "keys" in data
            assert len(data["keys"]) > 0
            assert "total_keys" in data
            assert "displayed_keys" in data
    
    @pytest.mark.asyncio
    async def test_websocket_connection(self, mock_redis):
        """Test WebSocket connection handling"""
        with patch('redis.Redis', return_value=mock_redis):
            server = ReggaeDashboardServer()
            client = TestClient(server.app)
            
            # Start the broadcast task
            await server.startup()
            
            # Connect to WebSocket
            with client.websocket_connect("/ws") as websocket:
                # Verify connection was added
                assert len(server.active_connections) == 1
                
                # Send ping
                websocket.send_text("ping")
                
                # Receive pong
                response = websocket.receive_text()
                assert response == "pong"
                
                # Close connection
                websocket.close()
            
            # Verify connection was removed
            assert len(server.active_connections) == 0
            
            # Clean up broadcast task
            await server.shutdown()
    
    def test_generate_jah_message(self):
        """Test JAH message generation"""
        server = ReggaeDashboardServer()
        
        # Test different probability ranges
        assert "PEACEFUL" in server._generate_jah_message(0.3)
        assert "GUIDES" in server._generate_jah_message(0.5)
        assert "WARNS" in server._generate_jah_message(0.7)
        assert "HIGH TRAP ENERGY" in server._generate_jah_message(0.9)
    
    @pytest.mark.asyncio
    async def test_broadcast_updates(self, mock_redis, sample_trap_data, sample_position_data):
        """Test broadcast updates functionality"""
        mock_redis.get.side_effect = [
            json.dumps(sample_trap_data),
            json.dumps(sample_position_data)
        ]
        
        with patch('redis.Redis', return_value=mock_redis):
            server = ReggaeDashboardServer()
            
            # Create a mock WebSocket
            websocket = AsyncMock()
            server.active_connections.append(websocket)
            
            # Start broadcast task
            broadcast_task = asyncio.create_task(server.broadcast_updates())
            
            # Cancel after first update
            await asyncio.sleep(0.1)
            broadcast_task.cancel()
            
            try:
                await broadcast_task
            except asyncio.CancelledError:
                pass
            
            # Verify update was sent
            websocket.send_json.assert_called_once()
            update_data = websocket.send_json.call_args[0][0]
            assert "trap_probability" in update_data
            assert "position" in update_data
            assert "timestamp" in update_data
    
    def test_error_handling(self, mock_redis):
        """Test error handling in endpoints"""
        mock_redis.get.side_effect = Exception("Redis error")
        
        with patch('redis.Redis', return_value=mock_redis):
            server = ReggaeDashboardServer()
            client = TestClient(server.app)
            
            # Test trap probability endpoint error handling
            response = client.get("/api/trap-probability")
            assert response.status_code == 200
            data = response.json()
            assert data["probability"] == 0.5  # Default value
            
            # Test position endpoint error handling
            response = client.get("/api/position")
            assert response.status_code == 200
            data = response.json()
            assert data["has_position"] is False  # Default value 