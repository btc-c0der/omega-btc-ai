
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
Pytest configuration for WebSocket testing.

Version: 0.2.0
GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2025-03-28
"""
import pytest
import os
import asyncio
import logging
from omega_ai.mm_trap_detector.mm_websocket_server_v2 import start_server, stop_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('websocket_conftest')

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
async def global_websocket_server(disable_ssl, external_server, dynamic_ports, start_port):
    """
    Start a global WebSocket server for all tests.
    
    This fixture starts a WebSocket server that can be shared across multiple
    test functions, optimizing resource usage and test execution time.
    
    Args:
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