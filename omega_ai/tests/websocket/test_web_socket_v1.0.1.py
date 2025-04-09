"""
🔱 OMEGA BTC AI - Simple WebSocket Test 🔱

A simple test for basic WebSocket functionality in the OMEGA BTC AI system.

Version: 1.0.1
GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2025-03-28
"""

import asyncio
import websockets

# ASCII Art Banner
print("""
    ⚡ OMEGA BTC AI - SIMPLE WEBSOCKET TEST ⚡
    
    🔱 TESTING BASIC CONNECTIONS 🔱
    🔱 VALIDATING DIVINE FLOW 🔱
    🔱 ENSURING QUANTUM HARMONY 🔱
""")

async def test_connection():
    """Test the divine connection to the WebSocket server.
    
    This test establishes a basic connection and sends a test message
    to validate the WebSocket server's response.
    """
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send('{"btc_price": 90500}')
        response = await websocket.recv()
        print(f"📡 Received from WebSocket: {response}")

if __name__ == "__main__":
    asyncio.run(test_connection())
