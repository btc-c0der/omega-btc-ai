"""Test configuration for V2 components.

This module provides configuration settings for testing V2 components:
1. WebSocket server
2. Database manager
3. Redis manager
4. Test environment
"""

import os
import ssl
import socket
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, UTC
import tempfile
from pathlib import Path

# ---- Test Configuration ----

@dataclass
class TestConfig:
    """Test configuration settings."""
    # WebSocket settings
    base_port: int = 9886
    ssl_port: int = 9887
    test_host: str = "localhost"
    max_connections: int = 100
    message_size_limit: int = 1024 * 1024  # 1MB
    
    # SSL settings
    ssl_cert_path: str = "./SSL_redis-btc-omega-redis.pem"
    ssl_key_path: str = "./SSL_redis-btc-omega-redis.pem"
    
    # Database settings
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "omega_btc_test"
    db_user: str = "omega_user"
    db_password: str = "omega_pass"
    db_pool_size: int = 2
    db_max_overflow: int = 2
    
    # Redis settings
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = "test_password"
    redis_username: Optional[str] = "test_user"
    redis_pool_size: int = 2
    redis_max_connections: int = 10
    redis_ssl: bool = False
    
    # Test environment
    test_data_dir: str = "tests/data"
    log_level: str = "INFO"
    test_timeout: int = 30

# ---- Helper Functions ----

def find_available_port(start_port: int, max_attempts: int = 10) -> int:
    """Find an available port starting from the given port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("", port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"No available ports found starting from {start_port}")

def create_ssl_context() -> ssl.SSLContext:
    """Create SSL context for testing."""
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    # Create self-signed certificate
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    from datetime import datetime, timedelta
    
    # Generate key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Generate certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost")
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(UTC)
    ).not_valid_after(
        datetime.now(UTC) + timedelta(days=1)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName("localhost")]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    # Save certificate and key
    with open(TestConfig.ssl_cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    with open(TestConfig.ssl_key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    context.load_cert_chain(TestConfig.ssl_cert_path, TestConfig.ssl_key_path)
    return context

def generate_test_data(size: int = 1000) -> Dict[str, Any]:
    """Generate test data for testing."""
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "data": "x" * size,
        "metadata": {
            "test": True,
            "size": size,
            "generated_at": datetime.now(UTC).isoformat()
        }
    }

def get_websocket_uri(use_ssl: bool = False) -> str:
    """Get WebSocket URI for testing."""
    port = TestConfig.ssl_port if use_ssl else TestConfig.base_port
    protocol = "wss" if use_ssl else "ws"
    return f"{protocol}://{TestConfig.test_host}:{port}"

# ---- Environment Setup ----

def setup_test_environment():
    """Set up test environment variables."""
    # Create SSL certificates
    ssl_context = create_ssl_context()
    if not ssl_context:
        raise RuntimeError("Failed to create SSL context for testing")
    
    # WebSocket settings
    os.environ["WEBSOCKET_HOST"] = TestConfig.test_host
    os.environ["WEBSOCKET_PORT"] = str(TestConfig.base_port)
    os.environ["WEBSOCKET_SSL_PORT"] = str(TestConfig.ssl_port)
    os.environ["WEBSOCKET_MAX_CONNECTIONS"] = str(TestConfig.max_connections)
    os.environ["WEBSOCKET_MESSAGE_SIZE_LIMIT"] = str(TestConfig.message_size_limit)
    os.environ["SSL_CERT_PATH"] = TestConfig.ssl_cert_path
    os.environ["SSL_KEY_PATH"] = TestConfig.ssl_key_path
    
    # Verify SSL certificate paths
    if not os.path.exists(TestConfig.ssl_cert_path):
        raise RuntimeError(f"SSL certificate not found at {TestConfig.ssl_cert_path}")
    if not os.path.exists(TestConfig.ssl_key_path):
        raise RuntimeError(f"SSL key not found at {TestConfig.ssl_key_path}")
    
    # Database settings
    os.environ["DB_HOST"] = TestConfig.db_host
    os.environ["DB_PORT"] = str(TestConfig.db_port)
    os.environ["DB_NAME"] = TestConfig.db_name
    os.environ["DB_USER"] = TestConfig.db_user
    os.environ["DB_PASSWORD"] = TestConfig.db_password
    os.environ["DB_POOL_SIZE"] = str(TestConfig.db_pool_size)
    os.environ["DB_MAX_OVERFLOW"] = str(TestConfig.db_max_overflow)
    
    # Redis settings
    os.environ["REDIS_HOST"] = TestConfig.redis_host
    os.environ["REDIS_PORT"] = str(TestConfig.redis_port)
    os.environ["REDIS_DB"] = str(TestConfig.redis_db)
    if TestConfig.redis_username is not None:
        os.environ["REDIS_USERNAME"] = TestConfig.redis_username
    if TestConfig.redis_password is not None:
        os.environ["REDIS_PASSWORD"] = TestConfig.redis_password
    os.environ["REDIS_POOL_SIZE"] = str(TestConfig.redis_pool_size)
    os.environ["REDIS_MAX_CONNECTIONS"] = str(TestConfig.redis_max_connections)
    os.environ["REDIS_SSL"] = str(TestConfig.redis_ssl).lower()
    
    # Test environment
    os.environ["TEST_DATA_DIR"] = TestConfig.test_data_dir
    os.environ["LOG_LEVEL"] = TestConfig.log_level
    os.environ["TEST_TIMEOUT"] = str(TestConfig.test_timeout)

# ---- Test Data Management ----

def create_test_data_file(filename: str, data: Dict[str, Any]) -> str:
    """Create a test data file."""
    import json
    import os
    
    os.makedirs(TestConfig.test_data_dir, exist_ok=True)
    filepath = os.path.join(TestConfig.test_data_dir, filename)
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    
    return filepath

def read_test_data_file(filename: str) -> Dict[str, Any]:
    """Read a test data file."""
    import json
    
    filepath = os.path.join(TestConfig.test_data_dir, filename)
    with open(filepath, "r") as f:
        return json.load(f)

# ---- Test Utilities ----

def get_test_config() -> TestConfig:
    """Get test configuration instance."""
    return TestConfig()

def cleanup_test_environment():
    """Clean up test environment."""
    # Remove test data directory
    import shutil
    if os.path.exists(TestConfig.test_data_dir):
        shutil.rmtree(TestConfig.test_data_dir)
    
    # Remove SSL certificates
    try:
        os.remove(TestConfig.ssl_cert_path)
        os.remove(TestConfig.ssl_key_path)
    except FileNotFoundError:
        pass
    
    # Clear environment variables
    for key in [
        "WEBSOCKET_HOST", "WEBSOCKET_PORT", "WEBSOCKET_SSL_PORT",
        "WEBSOCKET_MAX_CONNECTIONS", "WEBSOCKET_MESSAGE_SIZE_LIMIT",
        "SSL_CERT_PATH", "SSL_KEY_PATH",
        "DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD",
        "DB_POOL_SIZE", "DB_MAX_OVERFLOW", "REDIS_HOST", "REDIS_PORT",
        "REDIS_DB", "REDIS_PASSWORD", "REDIS_POOL_SIZE", "REDIS_MAX_CONNECTIONS",
        "TEST_DATA_DIR", "LOG_LEVEL", "TEST_TIMEOUT"
    ]:
        if key in os.environ:
            del os.environ[key] 