
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

"""Test configuration for WebSocket V2 functionality.

This module provides sacred configuration for WebSocket V2 tests, including:
1. Port detection and management
2. Test environment settings
3. SSL/TLS configuration
4. Test data generation
5. Performance thresholds
"""

import socket
import ssl
import os
from typing import Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, UTC

@dataclass
class TestConfig:
    """Sacred test configuration for WebSocket V2."""
    base_port: int = 8766
    ssl_port: int = 8767
    test_host: str = "localhost"
    ssl_cert_path: str = "test_cert.pem"
    ssl_key_path: str = "test_key.pem"
    test_timeout: float = 5.0
    max_retries: int = 3
    retry_delay: float = 1.0
    message_size_limit: int = 1024 * 1024  # 1MB
    concurrent_connections: int = 20
    burst_size: int = 10
    test_duration: int = 60  # seconds

def find_available_port(start_port: int, max_attempts: int = 10) -> Optional[int]:
    """Find an available port starting from the given port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None

def get_test_ports() -> Tuple[int, int]:
    """Get available ports for WebSocket V2 tests."""
    base_port = find_available_port(TestConfig.base_port)
    ssl_port = find_available_port(TestConfig.ssl_port)
    
    if not base_port or not ssl_port:
        raise RuntimeError("Could not find available ports for testing")
    
    return base_port, ssl_port

def create_test_ssl_context() -> ssl.SSLContext:
    """Create SSL context for WebSocket V2 tests."""
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    return ssl_context

def generate_test_data(size: int) -> dict:
    """Generate test data for WebSocket V2 tests."""
    return {
        "type": "test_data",
        "timestamp": datetime.now(UTC).isoformat(),
        "data": {
            "size": size,
            "payload": "x" * (size - 100)  # Leave room for JSON structure
        }
    }

def get_test_uri(use_ssl: bool = False) -> str:
    """Get WebSocket URI for testing."""
    base_port, ssl_port = get_test_ports()
    port = ssl_port if use_ssl else base_port
    protocol = "wss" if use_ssl else "ws"
    return f"{protocol}://{TestConfig.test_host}:{port}"

# Update environment variables for testing
os.environ["MM_WS_v2_PORT"] = str(get_test_ports()[0])
os.environ["MM_WS_v2_SSL_PORT"] = str(get_test_ports()[1]) 