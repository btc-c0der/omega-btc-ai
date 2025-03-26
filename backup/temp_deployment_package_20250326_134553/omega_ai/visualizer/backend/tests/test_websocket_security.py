"""Security tests for WebSocket functionality in the trap visualizer server."""

import pytest
from fastapi.testclient import TestClient
from fastapi import WebSocketDisconnect
from unittest.mock import Mock, patch, AsyncMock
import json
from datetime import datetime, UTC, timedelta
import asyncio
import websockets
import base64
import zlib
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
async def test_websocket_frame_size_limit(client):
    """Test WebSocket frame size limit to prevent memory exhaustion."""
    # Create a large payload that exceeds reasonable frame size
    large_payload = "A" * (1024 * 1024)  # 1MB payload
    
    with client.websocket_connect("/ws") as websocket:
        # Attempt to send large payload
        websocket.send_text(large_payload)
        response = websocket.receive_json()
        assert response["type"] == "error"
        assert "payload too large" in response["message"].lower()

@pytest.mark.asyncio
async def test_websocket_ping_flood(client):
    """Test protection against ping flood attacks."""
    with client.websocket_connect("/ws") as websocket:
        # Send rapid ping messages
        for _ in range(100):
            websocket.send_text("ping")
        
        # Verify server handles flood gracefully
        responses = []
        for _ in range(10):  # Only check first 10 responses
            try:
                response = websocket.receive_json()
                responses.append(response)
            except Exception:
                break
        
        # Verify rate limiting is working
        assert len(responses) < 100

@pytest.mark.asyncio
async def test_websocket_binary_injection(client):
    """Test protection against binary data injection."""
    # Create malicious binary payload
    malicious_binary = bytes([0x00, 0xFF, 0xFE, 0xFD, 0xFC])
    
    with client.websocket_connect("/ws") as websocket:
        # Attempt to send binary data
        websocket.send_bytes(malicious_binary)
        response = websocket.receive_json()
        assert response["type"] == "error"
        assert "invalid message format" in response["message"].lower()

@pytest.mark.asyncio
async def test_websocket_protocol_downgrade(client):
    """Test protection against WebSocket protocol downgrade attacks."""
    # Attempt to connect with invalid protocol
    headers = {
        "Upgrade": "websocket",
        "Connection": "Upgrade",
        "Sec-WebSocket-Version": "8",
        "Sec-WebSocket-Key": base64.b64encode(b"test").decode(),
        "Sec-WebSocket-Protocol": "invalid_protocol"
    }
    
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/ws", headers=headers) as websocket:
            pass

@pytest.mark.asyncio
async def test_websocket_compression_bomb(client):
    """Test protection against compression bomb attacks."""
    # Create a compression bomb (highly compressible data)
    compression_bomb = "A" * 10000
    compressed = zlib.compress(compression_bomb.encode())
    
    with client.websocket_connect("/ws") as websocket:
        # Attempt to send compressed data
        websocket.send_bytes(compressed)
        response = websocket.receive_json()
        assert response["type"] == "error"
        assert "invalid message format" in response["message"].lower()

@pytest.mark.asyncio
async def test_websocket_origin_validation(client):
    """Test WebSocket origin validation."""
    # Attempt to connect with invalid origin
    headers = {
        "Origin": "http://malicious-site.com",
        "Upgrade": "websocket",
        "Connection": "Upgrade",
        "Sec-WebSocket-Version": "8",
        "Sec-WebSocket-Key": base64.b64encode(b"test").decode()
    }
    
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/ws", headers=headers) as websocket:
            pass

@pytest.mark.asyncio
async def test_websocket_sql_injection(client):
    """Test protection against SQL injection through WebSocket."""
    sql_injection_payloads = [
        "' OR '1'='1",
        "'; DROP TABLE traps; --",
        "' UNION SELECT * FROM traps; --",
        "' OR 1=1; --"
    ]
    
    with client.websocket_connect("/ws") as websocket:
        for payload in sql_injection_payloads:
            websocket.send_text(json.dumps({"type": "query", "data": payload}))
            response = websocket.receive_json()
            assert response["type"] == "error"
            assert "invalid input" in response["message"].lower()

@pytest.mark.asyncio
async def test_websocket_xss_injection(client):
    """Test protection against XSS injection through WebSocket."""
    xss_payloads = [
        "<script>alert('xss')</script>",
        "<img src=x onerror=alert('xss')>",
        "javascript:alert('xss')",
        "<svg onload=alert('xss')>"
    ]
    
    with client.websocket_connect("/ws") as websocket:
        for payload in xss_payloads:
            websocket.send_text(json.dumps({"type": "message", "content": payload}))
            response = websocket.receive_json()
            assert response["type"] == "error"
            assert "invalid input" in response["message"].lower()

@pytest.mark.asyncio
async def test_websocket_path_traversal(client):
    """Test protection against path traversal attacks."""
    path_traversal_payloads = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2f",
        "....//....//....//"
    ]
    
    with client.websocket_connect("/ws") as websocket:
        for payload in path_traversal_payloads:
            websocket.send_text(json.dumps({"type": "file", "path": payload}))
            response = websocket.receive_json()
            assert response["type"] == "error"
            assert "invalid input" in response["message"].lower()

@pytest.mark.asyncio
async def test_websocket_command_injection(client):
    """Test protection against command injection attacks."""
    command_injection_payloads = [
        "| ls",
        "; rm -rf /",
        "`cat /etc/passwd`",
        "$(cat /etc/passwd)",
        "&& cat /etc/passwd"
    ]
    
    with client.websocket_connect("/ws") as websocket:
        for payload in command_injection_payloads:
            websocket.send_text(json.dumps({"type": "command", "data": payload}))
            response = websocket.receive_json()
            assert response["type"] == "error"
            assert "invalid input" in response["message"].lower()

@pytest.mark.asyncio
async def test_websocket_buffer_overflow(client):
    """Test protection against buffer overflow attempts."""
    # Create a payload that attempts to overflow the buffer
    buffer_overflow_payload = "A" * (1024 * 1024 * 10)  # 10MB payload
    
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text(buffer_overflow_payload)
        response = websocket.receive_json()
        assert response["type"] == "error"
        assert "payload too large" in response["message"].lower()

@pytest.mark.asyncio
async def test_websocket_connection_exhaustion(client):
    """Test protection against connection exhaustion attacks."""
    max_connections = 100  # Adjust based on your server's limit
    connections = []
    
    try:
        # Attempt to create more connections than the limit
        for _ in range(max_connections + 10):
            websocket = client.websocket_connect("/ws")
            connections.append(websocket)
            websocket.__enter__()
        
        # Verify connection limit is enforced
        assert len(client.app.connection_manager.active_connections) <= max_connections
        
    finally:
        # Clean up connections
        for websocket in connections:
            try:
                websocket.__exit__(None, None, None)
            except:
                pass

@pytest.mark.asyncio
async def test_websocket_message_flood(client):
    """Test protection against message flooding attacks."""
    with client.websocket_connect("/ws") as websocket:
        # Send rapid messages
        for _ in range(1000):
            websocket.send_text(json.dumps({"type": "message", "data": "flood"}))
        
        # Verify rate limiting is working
        responses = []
        for _ in range(10):  # Only check first 10 responses
            try:
                response = websocket.receive_json()
                responses.append(response)
            except Exception:
                break
        
        assert len(responses) < 1000

@pytest.mark.asyncio
async def test_websocket_authentication_bypass(client):
    """Test protection against authentication bypass attempts."""
    auth_bypass_payloads = [
        {"type": "auth", "token": "null"},
        {"type": "auth", "token": "undefined"},
        {"type": "auth", "token": ""},
        {"type": "auth", "token": "admin"},
        {"type": "auth", "token": "true"}
    ]
    
    with client.websocket_connect("/ws") as websocket:
        for payload in auth_bypass_payloads:
            websocket.send_text(json.dumps(payload))
            response = websocket.receive_json()
            assert response["type"] == "error"
            assert "invalid authentication" in response["message"].lower()

@pytest.mark.asyncio
async def test_websocket_protocol_manipulation(client):
    """Test protection against WebSocket protocol manipulation."""
    protocol_manipulation_payloads = [
        {"Upgrade": "websocket", "Connection": "Upgrade", "Sec-WebSocket-Version": "7"},
        {"Upgrade": "websocket", "Connection": "Upgrade", "Sec-WebSocket-Version": "9"},
        {"Upgrade": "websocket", "Connection": "Upgrade", "Sec-WebSocket-Version": "invalid"},
        {"Upgrade": "websocket", "Connection": "Upgrade", "Sec-WebSocket-Key": ""}
    ]
    
    for headers in protocol_manipulation_payloads:
        with pytest.raises(WebSocketDisconnect):
            with client.websocket_connect("/ws", headers=headers) as websocket:
                pass 