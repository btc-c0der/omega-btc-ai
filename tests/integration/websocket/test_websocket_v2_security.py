
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

"""Tests for WebSocket Server V2 security.

This test suite covers the security aspects of the WebSocket Server V2:
1. SSL/TLS encryption
2. Message validation
3. Rate limiting
4. Input sanitization
5. Connection authentication
6. Data encryption
7. Access control
8. Protocol validation
9. Security headers
"""

import pytest
import asyncio
import websockets
import json
import ssl
from datetime import datetime, UTC
from typing import Dict, Any, List
from omega_ai.mm_trap_detector.mm_websocket_server_v2 import (
    start_server, ConnectionState, ClientInfo
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
    yield server_task
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

# ---- Test Functions ----

@pytest.mark.asyncio
async def test_websocket_v2_ssl_encryption(websocket_server):
    """Test SSL/TLS encryption."""
    uri = get_websocket_uri(use_ssl=True)
    
    # Create SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Send sensitive data
        message = {
            "type": "secure_test",
            "data": "sensitive information",
            "timestamp": datetime.now(UTC).isoformat()
        }
        await websocket.send(json.dumps(message))
        
        # Verify secure response
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "secure_test"
        assert "encrypted" in data

@pytest.mark.asyncio
async def test_websocket_v2_message_validation(websocket_server):
    """Test message validation."""
    uri = get_websocket_uri()
    
    async with websockets.connect(uri) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Test invalid message format
        invalid_messages = [
            "invalid json",
            json.dumps({"type": ""}),  # Empty type
            json.dumps({"type": "test"}),  # Missing required fields
            json.dumps({"type": "test", "data": None}),  # Invalid data type
            json.dumps({"type": "test", "timestamp": "invalid"})  # Invalid timestamp
        ]
        
        for msg in invalid_messages:
            await websocket.send(msg)
            response = await websocket.recv()
            data = json.loads(response)
            assert data["type"] == "error"
            assert "validation" in data["message"].lower()

@pytest.mark.asyncio
async def test_websocket_v2_rate_limiting(websocket_server):
    """Test rate limiting."""
    uri = get_websocket_uri()
    
    async with websockets.connect(uri) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Send rapid messages
        for _ in range(20):
            message = {
                "type": "test",
                "timestamp": datetime.now(UTC).isoformat()
            }
            await websocket.send(json.dumps(message))
            await asyncio.sleep(0.1)  # Rapid sending
        
        # Verify rate limiting
        rate_limit_received = False
        for _ in range(20):
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=1)
                data = json.loads(response)
                if data["type"] == "rate_limit":
                    rate_limit_received = True
                    break
            except asyncio.TimeoutError:
                break
        
        assert rate_limit_received

@pytest.mark.asyncio
async def test_websocket_v2_input_sanitization(websocket_server):
    """Test input sanitization."""
    uri = get_websocket_uri()
    
    async with websockets.connect(uri) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Test potentially malicious input
        malicious_inputs = [
            {"type": "test", "data": "<script>alert('xss')</script>"},
            {"type": "test", "data": "'; DROP TABLE users; --"},
            {"type": "test", "data": "../../../etc/passwd"},
            {"type": "test", "data": "&lt;script&gt;alert('xss')&lt;/script&gt;"}
        ]
        
        for msg in malicious_inputs:
            await websocket.send(json.dumps(msg))
            response = await websocket.recv()
            data = json.loads(response)
            assert data["type"] == "error" or "sanitized" in data

@pytest.mark.asyncio
async def test_websocket_v2_connection_authentication(websocket_server):
    """Test connection authentication."""
    uri = get_websocket_uri()
    
    # Test without authentication
    async with websockets.connect(uri) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Try to access protected endpoint
        message = {
            "type": "protected_test",
            "timestamp": datetime.now(UTC).isoformat()
        }
        await websocket.send(json.dumps(message))
        
        # Verify authentication error
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "error"
        assert "authentication" in data["message"].lower()
    
    # Test with authentication
    async with websockets.connect(uri) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Authenticate
        auth_message = {
            "type": "authenticate",
            "token": "test_token",
            "timestamp": datetime.now(UTC).isoformat()
        }
        await websocket.send(json.dumps(auth_message))
        
        # Verify authentication success
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "authenticated"
        
        # Try protected endpoint again
        message = {
            "type": "protected_test",
            "timestamp": datetime.now(UTC).isoformat()
        }
        await websocket.send(json.dumps(message))
        
        # Verify access granted
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "protected_test"

@pytest.mark.asyncio
async def test_websocket_v2_data_encryption(websocket_server):
    """Test data encryption."""
    uri = get_websocket_uri(use_ssl=True)
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Send sensitive data
        sensitive_data = {
            "type": "encrypted_test",
            "data": {
                "username": "test_user",
                "password": "test_pass",
                "credit_card": "4111111111111111"
            },
            "timestamp": datetime.now(UTC).isoformat()
        }
        await websocket.send(json.dumps(sensitive_data))
        
        # Verify encryption
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "encrypted_test"
        assert "encrypted" in data
        assert "sensitive_data" not in data

@pytest.mark.asyncio
async def test_websocket_v2_access_control(websocket_server):
    """Test access control."""
    uri = get_websocket_uri()
    
    async with websockets.connect(uri) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Test unauthorized access
        message = {
            "type": "admin_test",
            "timestamp": datetime.now(UTC).isoformat()
        }
        await websocket.send(json.dumps(message))
        
        # Verify access denied
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "error"
        assert "access" in data["message"].lower()
        
        # Test with admin token
        admin_message = {
            "type": "admin_test",
            "token": "admin_token",
            "timestamp": datetime.now(UTC).isoformat()
        }
        await websocket.send(json.dumps(admin_message))
        
        # Verify admin access
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "admin_test"

@pytest.mark.asyncio
async def test_websocket_v2_protocol_validation(websocket_server):
    """Test protocol validation."""
    uri = get_websocket_uri()
    
    async with websockets.connect(uri) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Test invalid protocol versions
        invalid_protocols = [
            {"type": "test", "protocol": "v1"},
            {"type": "test", "protocol": "v3"},
            {"type": "test", "protocol": "invalid"}
        ]
        
        for msg in invalid_protocols:
            await websocket.send(json.dumps(msg))
            response = await websocket.recv()
            data = json.loads(response)
            assert data["type"] == "error"
            assert "protocol" in data["message"].lower()

@pytest.mark.asyncio
async def test_websocket_v2_security_headers(websocket_server):
    """Test security headers."""
    uri = get_websocket_uri()
    
    async with websockets.connect(uri) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Send request to check headers
        message = {
            "type": "headers_test",
            "timestamp": datetime.now(UTC).isoformat()
        }
        await websocket.send(json.dumps(message))
        
        # Verify security headers
        response = await websocket.recv()
        data = json.loads(response)
        assert data["type"] == "headers_test"
        assert "headers" in data
        headers = data["headers"]
        
        # Check for required security headers
        required_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Strict-Transport-Security"
        ]
        for header in required_headers:
            assert header in headers 