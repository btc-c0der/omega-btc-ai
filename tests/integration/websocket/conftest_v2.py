
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

"""
🔱 OMEGA BTC AI - WebSocket V2 Test Configuration 🔱

This module provides test fixtures and configuration for WebSocket V2 tests.

Version: 1.0.1
GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2025-03-28
"""

import pytest
import asyncio
import os
import logging
import sys
from typing import Generator, AsyncGenerator
from omega_ai.mm_trap_detector.mm_websocket_server_v2 import start_server, stop_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('websocket_conftest_v2')

# ASCII Art Banner
print("""
    ⚡ OMEGA BTC AI - WEBSOCKET V2 TEST CONFIG ⚡
    
    🔱 CONFIGURING DIVINE TESTS 🔱
    🔱 SETTING UP COSMIC ENVIRONMENT 🔱
    🔱 ENSURING QUANTUM HARMONY 🔱
""")

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for the test session."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
async def setup_teardown():
    """Set up and tear down test environment."""
    # Set test environment variables
    os.environ["WEBSOCKET_PORT"] = "9886"
    os.environ["WEBSOCKET_SSL_PORT"] = "9888"
    os.environ["WEBSOCKET_HOST"] = "localhost"
    os.environ["REDIS_HOST"] = "localhost"
    os.environ["REDIS_PORT"] = "6379"
    os.environ["REDIS_DB"] = "0"
    os.environ["REDIS_PASSWORD"] = ""  # Empty for test environment
    
    yield
    
    # Clean up environment variables
    for key in ["WEBSOCKET_PORT", "WEBSOCKET_SSL_PORT", "WEBSOCKET_HOST",
                "REDIS_HOST", "REDIS_PORT", "REDIS_DB", "REDIS_PASSWORD"]:
        os.environ.pop(key, None)

@pytest.fixture(scope="session")
async def websocket_server():
    """Start WebSocket server for testing."""
    logger.info("Starting WebSocket server...")
    server_task = asyncio.create_task(start_server())
    await asyncio.sleep(1)  # Give server time to start
    yield server_task
    logger.info("Stopping WebSocket server...")
    await stop_server()
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

def pytest_addoption(parser):
    """Add custom command line options to pytest."""
    parser.addoption(
        "--no-ssl", 
        action="store_true", 
        default=False, 
        help="Disable SSL for testing"
    )
    parser.addoption(
        "--external-server", 
        action="store_true", 
        default=False, 
        help="Use an externally started server"
    )
    parser.addoption(
        "--dynamic-ports",
        action="store_true",
        default=False,
        help="Use dynamic port detection"
    )
    parser.addoption(
        "--start-port",
        type=int,
        default=9000,
        help="Starting port for port detection (default: 9000)"
    )
    parser.addoption(
        "--max-clients",
        type=int,
        default=100,
        help="Maximum number of clients for load tests (default: 100)"
    )
    parser.addoption(
        "--test-duration",
        type=int,
        default=10,
        help="Duration of performance tests in seconds (default: 10)"
    )

@pytest.fixture(scope="session")
def disable_ssl(request):
    """Fixture to check if SSL should be disabled."""
    return request.config.getoption("--no-ssl")

@pytest.fixture(scope="session")
def external_server(request):
    """Fixture to check if using an external server."""
    return request.config.getoption("--external-server")

@pytest.fixture(scope="session")
def dynamic_ports(request):
    """Fixture to check if dynamic port detection should be used."""
    return request.config.getoption("--dynamic-ports")

@pytest.fixture(scope="session")
def start_port(request):
    """Fixture to get the starting port for port detection."""
    return request.config.getoption("--start-port")

@pytest.fixture(scope="session")
def max_clients(request):
    """Fixture to get the maximum number of clients for load tests."""
    return request.config.getoption("--max-clients")

@pytest.fixture(scope="session")
def test_duration(request):
    """Fixture to get the duration of performance tests in seconds."""
    return request.config.getoption("--test-duration")

# Create a fixture for one-time server setup
@pytest.fixture(scope="session")
async def global_websocket_server(event_loop, disable_ssl, external_server, dynamic_ports, start_port):
    """
    Start a global WebSocket server for all tests.
    
    This fixture starts a WebSocket server that can be shared across multiple
    test functions, optimizing resource usage and test execution time.
    
    Args:
        event_loop: The event loop to use
        disable_ssl: Whether to disable SSL for testing
        external_server: Whether to use an externally started server
        dynamic_ports: Whether to use dynamic port detection
        start_port: Starting port for port detection
        
    Yields:
        asyncio.Task: The server task, or None if using an external server
    """
    if external_server:
        # If using an external server, just yield None
        logger.info("Using external WebSocket server for testing")
        yield None
        return
    
    # Set environment variables for testing
    if not dynamic_ports:
        # Use fixed ports if not using dynamic port detection
        os.environ["WEBSOCKET_PORT"] = "9886"
        os.environ["WEBSOCKET_SSL_PORT"] = "9887"
        logger.info("Using fixed ports: 9886 (regular) and 9887 (SSL)")
    
    os.environ["WEBSOCKET_HOST"] = "localhost"
    
    if disable_ssl:
        # Disable SSL for testing
        os.environ["SSL_CERT_PATH"] = ""
        os.environ["SSL_KEY_PATH"] = ""
        logger.info("SSL disabled for testing")
    
    # Start server
    logger.info("Starting WebSocket server for testing...")
    server_task = asyncio.create_task(
        start_server(detect_ports=dynamic_ports, start_port=start_port)
    )
    await asyncio.sleep(1)  # Give server time to start
    
    # Log actual ports used
    port = os.environ.get("WEBSOCKET_PORT", "9886")
    ssl_port = os.environ.get("WEBSOCKET_SSL_PORT", "9887")
    logger.info(f"WebSocket server running on ports {port} (regular) and {ssl_port} (SSL)")
    
    yield server_task
    
    # Stop server
    logger.info("Stopping WebSocket server...")
    await stop_server()
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass
    logger.info("WebSocket server stopped")

def get_test_websocket_uri(disable_ssl=False):
    """
    Get WebSocket URI for testing with dynamic port detection.
    
    Args:
        disable_ssl (bool): Whether to use SSL or not
        
    Returns:
        str: The WebSocket URI to connect to
    """
    host = os.environ.get("WEBSOCKET_HOST", "localhost")
    port = os.environ.get("WEBSOCKET_PORT", "9886")
    
    protocol = "ws"
    if not disable_ssl and os.environ.get("WEBSOCKET_SSL_PORT"):
        protocol = "wss"
        port = os.environ.get("WEBSOCKET_SSL_PORT", "9887")
        
    return f"{protocol}://{host}:{port}"

# Per-function connection fixture for simpler test cases
@pytest.fixture
async def websocket_client(disable_ssl):
    """
    Create a WebSocket client connection for a test function.
    
    This fixture creates a new WebSocket connection for each test function.
    It's useful for simple test cases that only need a single connection.
    
    Args:
        disable_ssl (bool): Whether to use SSL or not
        
    Yields:
        websockets.WebSocketClientProtocol: A connected WebSocket client
    """
    import websockets
    
    uri = get_test_websocket_uri(disable_ssl)
    logger.info(f"Connecting to {uri} for test...")
    
    client = None
    try:
        client = await websockets.connect(uri)
        
        # Skip initial welcome message if any
        try:
            await asyncio.wait_for(client.recv(), timeout=0.5)
        except asyncio.TimeoutError:
            pass  # No welcome message received, that's OK
        except Exception as e:
            logger.warning(f"Error receiving initial message: {e}")
        
        yield client
        
    finally:
        # Close the connection
        if client is not None:
            # Check if we can close the connection
            try:
                await client.close()
            except Exception as e:
                logger.warning(f"Error closing connection: {e}") 