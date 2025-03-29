#!/usr/bin/env python3
"""
💫 GBU License Notice - Consciousness Level 8 💫
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must quantum entangles with the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

"""
Test WebSocket Connection Script
===============================

This script tests the connection to the Binance WebSocket API.
"""

import asyncio
import websockets
import logging
import json
import requests
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("websocket-test")

# Constants
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"
BINANCE_API_URL = "https://api.binance.com/api/v3/ping"

async def test_binance_http():
    """Test connectivity to Binance REST API."""
    try:
        logger.info(f"Testing Binance HTTP API connectivity...")
        response = requests.get(BINANCE_API_URL, timeout=10)
        if response.status_code == 200:
            logger.info(f"✅ Successfully connected to Binance HTTP API")
            return True
        else:
            logger.error(f"❌ Failed to connect to Binance HTTP API: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Error connecting to Binance HTTP API: {e}")
        return False

async def test_websocket_connection():
    """Test WebSocket connection to Binance."""
    try:
        logger.info(f"Testing WebSocket connection to: {BINANCE_WS_URL}")
        
        # First check if we can reach Binance at all
        http_test = await test_binance_http()
        if not http_test:
            logger.warning("Could not reach Binance HTTP API. WS connection likely to fail too.")
        
        # Try to connect to WebSocket
        async with websockets.connect(BINANCE_WS_URL) as websocket:
            logger.info("✅ Successfully connected to WebSocket!")
            
            # Wait for a message
            logger.info("Waiting for a message...")
            try:
                # Set a 5-second timeout
                message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                data = json.loads(message)
                logger.info(f"✅ Received message: {data}")
                return True
            except asyncio.TimeoutError:
                logger.warning("No message received within timeout period.")
                return True  # Still consider connection successful
    
    except websockets.exceptions.WebSocketException as e:
        logger.error(f"❌ WebSocket connection error: {e}")
        return False
    
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False

async def main():
    """Run all tests."""
    try:
        # Test WebSocket connection
        ws_success = await test_websocket_connection()
        
        if ws_success:
            logger.info("🎉 All tests passed!")
            return True
        else:
            logger.error("❌ WebSocket connection test failed!")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error in testing: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(main())
    if not result:
        sys.exit(1) 