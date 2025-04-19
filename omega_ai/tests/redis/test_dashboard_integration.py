
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

import pytest
import json
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timezone
from fastapi.testclient import TestClient
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

class TestDashboardIntegration:
    """Test suite for full dashboard integration"""
    
    def test_health_check_integration(self, mock_redis):
        """Test health check endpoint integration"""
        with patch('redis.Redis', return_value=mock_redis):
            server = ReggaeDashboardServer()
            client = TestClient(server.app)
            
            response = client.get("/api/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["redis"] == "connected"
            assert "timestamp" in data
    
    def test_trap_probability_integration(self, mock_redis, sample_trap_data):
        """Test trap probability endpoint integration"""
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
    
    def test_position_integration(self, mock_redis, sample_position_data):
        """Test position endpoint integration"""
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
    
    def test_redis_keys_integration(self, mock_redis):
        """Test Redis keys endpoint integration"""
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
    async def test_websocket_integration(self, mock_redis, sample_trap_data, sample_position_data):
        """Test WebSocket integration with Redis data updates"""
        mock_redis.get.side_effect = [
            json.dumps(sample_trap_data),
            json.dumps(sample_position_data)
        ]
        
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
                
                # Verify update was received
                update = websocket.receive_json()
                assert "trap_probability" in update
                assert "position" in update
                assert "timestamp" in update
                
                # Close connection
                websocket.close()
            
            # Verify connection was removed
            assert len(server.active_connections) == 0
            
            # Clean up broadcast task
            await server.shutdown()
    
    def test_error_handling_integration(self, mock_redis):
        """Test error handling integration"""
        mock_redis.get.side_effect = Exception("Redis error")
        
        with patch('redis.Redis', return_value=mock_redis):
            server = ReggaeDashboardServer()
            client = TestClient(server.app)
            
            # Test trap probability error handling
            response = client.get("/api/trap-probability")
            assert response.status_code == 200
            data = response.json()
            assert data["probability"] == 0.5  # Default value
            
            # Test position error handling
            response = client.get("/api/position")
            assert response.status_code == 200
            data = response.json()
            assert data["has_position"] is False  # Default value
    
    def test_concurrent_requests_integration(self, mock_redis, sample_trap_data, sample_position_data):
        """Test handling of concurrent requests"""
        mock_redis.get.side_effect = [
            json.dumps(sample_trap_data),
            json.dumps(sample_position_data)
        ]
        
        with patch('redis.Redis', return_value=mock_redis):
            server = ReggaeDashboardServer()
            client = TestClient(server.app)
            
            # Make concurrent requests
            responses = []
            for _ in range(5):
                responses.append(client.get("/api/trap-probability"))
                responses.append(client.get("/api/position"))
            
            # Verify all requests succeeded
            for response in responses:
                assert response.status_code == 200
                data = response.json()
                assert "timestamp" in data 