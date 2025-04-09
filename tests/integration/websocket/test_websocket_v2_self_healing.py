"""
🔱 OMEGA BTC AI - WebSocket V2 Self-Healing Test Suite 🔱

This module tests the self-healing capabilities of the WebSocket V2 server.

Version: 1.0.1
GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2025-03-28
"""

import pytest
import asyncio
import websockets
import json
import logging
import os
from typing import AsyncGenerator, Dict, Any
from websockets.asyncio.client import ClientConnection
from omega_ai.mm_trap_detector.mm_websocket_server_v2 import start_server, stop_server
from tests.integration.websocket.conftest_v2 import websocket_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('websocket_v2_self_healing')

# ASCII Art Banner
print("""
    ⚡ OMEGA BTC AI - WEBSOCKET V2 SELF-HEALING TESTS ⚡
    
    🔱 TESTING DIVINE RESILIENCE 🔱
    🔱 VALIDATING COSMIC RECOVERY 🔱
    🔱 ENSURING QUANTUM HARMONY 🔱
""")

@pytest.fixture
async def websocket_client(websocket_server) -> AsyncGenerator[ClientConnection, None]:
    """Create a WebSocket client for testing."""
    uri = f"ws://localhost:{os.getenv('WEBSOCKET_PORT', '9886')}"
    async with websockets.connect(uri) as websocket:
        yield websocket

@pytest.mark.asyncio
async def test_connection_recovery(websocket_client: ClientConnection):
    """Test the server's ability to recover from connection interruptions."""
    logger.info("Testing connection recovery...")
    
    # Send initial message
    await websocket_client.send(json.dumps({
        "type": "ping",
        "data": {"timestamp": asyncio.get_event_loop().time()}
    }))
    
    # Simulate connection interruption
    await websocket_client.close()
    
    # Attempt to reconnect
    uri = f"ws://localhost:{os.getenv('WEBSOCKET_PORT', '9886')}"
    async with websockets.connect(uri) as new_client:
        # Verify reconnection
        await new_client.send(json.dumps({
            "type": "ping",
            "data": {"timestamp": asyncio.get_event_loop().time()}
        }))
        response = await new_client.recv()
        assert json.loads(response)["type"] == "pong"

@pytest.mark.asyncio
async def test_error_handling(websocket_client: ClientConnection):
    """Test the server's error handling and recovery capabilities."""
    logger.info("Testing error handling...")
    
    # Send malformed message
    await websocket_client.send("invalid json")
    
    # Server should not crash and should respond with error
    response = await websocket_client.recv()
    error_response = json.loads(response)
    assert error_response["type"] == "error"
    assert "Invalid JSON" in error_response["message"]

@pytest.mark.asyncio
async def test_load_recovery(websocket_client: ClientConnection):
    """Test the server's ability to recover from high load conditions."""
    logger.info("Testing load recovery...")
    
    # Send multiple messages rapidly
    for _ in range(10):
        await websocket_client.send(json.dumps({
            "type": "ping",
            "data": {"timestamp": asyncio.get_event_loop().time()}
        }))
    
    # Verify server handles load and responds
    for _ in range(10):
        response = await websocket_client.recv()
        assert json.loads(response)["type"] == "pong"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 