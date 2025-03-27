"""
Tests for the base visualization server class.
"""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from omega_ai.visualizer.backend.base_server import BaseVisualizationServer
from omega_ai.utils.redis_manager import RedisManager

class TestServer(BaseVisualizationServer):
    """Test implementation of the base server."""
    
    def register_routes(self):
        @self.app.get("/test")
        async def test_route():
            return {"message": "test"}
        @self.app.get("/dump")
        async def dump_route():
            return self.load_latest_dump()

@pytest.fixture
def redis_manager():
    """Create a mock Redis manager."""
    manager = Mock(spec=RedisManager)
    manager.get_cached.return_value = {"test": "data"}
    return manager

@pytest.fixture
def server(redis_manager):
    """Create a test server instance."""
    return TestServer("Test Server", redis_manager)

@pytest.fixture
def client(server):
    """Create a test client."""
    return TestClient(server.app)

def test_server_initialization(server):
    """Test server initialization."""
    assert server.app.title == "Test Server"
    assert isinstance(server.redis_manager, Mock)
    assert server.logger.name == "TestServer"

def test_load_latest_dump(server, redis_manager):
    """Test loading latest dump."""
    data = server.load_latest_dump()
    assert data == {"test": "data"}
    redis_manager.get_cached.assert_called_once_with("omega:latest_dump")

def test_load_latest_dump_no_data(server, redis_manager):
    """Test loading latest dump when no data exists."""
    redis_manager.get_cached.return_value = None
    with pytest.raises(Exception) as exc_info:
        server.load_latest_dump()
    assert "No dump data found" in str(exc_info.value)

def test_parse_schumann_value(server):
    """Test parsing Schumann resonance values."""
    # Test string value
    assert server.parse_schumann_value("7.83") == 7.83
    
    # Test dict value
    assert server.parse_schumann_value({"value": "8.5"}) == 8.5
    
    # Test invalid value
    assert server.parse_schumann_value("invalid") == 7.83
    
    # Test None value
    assert server.parse_schumann_value(None) == 7.83

def test_test_route(client):
    """Test the test route."""
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "test"}

def test_dump_route(client, redis_manager):
    """Test the dump route."""
    response = client.get("/dump")
    assert response.status_code == 200
    assert response.json() == {"test": "data"}
    redis_manager.get_cached.assert_called_once_with("omega:latest_dump") 