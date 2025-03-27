"""
🔱 OMEGA BTC AI - BTC WebSocket Test Suite 🔱

This test suite validates the Bitcoin price feed WebSocket functionality,
ensuring divine connection to the cosmic BTC price stream.

Version: 1.0.1
GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2025-03-28
"""

import asyncio
import json
import redis
import websockets

# ASCII Art Banner
print("""
    ⚡ OMEGA BTC AI - BTC WEBSOCKET TEST SUITE ⚡
    
    🔱 TESTING BTC PRICE FEED 🔱
    🔱 VALIDATING COSMIC FLOW 🔱
    🔱 ENSURING QUANTUM HARMONY 🔱
""")

async def test_btc_websocket():
    """Test the divine connection to the BTC Price Feed WebSocket.
    
    This test ensures proper connection and message handling from the
    Bitcoin price feed WebSocket server.
    """
    async with websockets.connect("ws://localhost:8765") as ws:
        print("✅ Connected to BTC WebSocket")
        try:
            async for message in ws:
                data = json.loads(message)
                print(f"📡 [DEBUG] BTC Price Update Received: {data}")
        except websockets.exceptions.ConnectionClosedError:
            print("❌ WebSocket Connection Lost!")

# Redis connection for price verification
redis_conn = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def get_live_btc_price():
    """Fetch the latest BTC price from Redis with divine error handling.
    
    Returns:
        float: The current BTC price or 0 if unavailable
    """
    try:
        price = redis_conn.get("live_btc_price")
        print(f"📡 [DEBUG] Fetching BTC Price from Redis: {price}")
        return float(price) if price else 0
    except Exception as e:
        print(f"❌ [DEBUG] Redis Fetch Error: {e}")
        return 0

async def test_websocket_listener():
    """Test the divine listener for BTC price updates.
    
    This test validates that the WebSocket listener correctly receives
    and processes BTC price updates from the feed.
    """
    async with websockets.connect("ws://localhost:8765") as ws:
        print("✅ Connected to BTC WebSocket")
        async for message in ws:
            data = json.loads(message)
            print(f"📡 [DEBUG] BTC Price Update Received: {data}")

if __name__ == "__main__":
    asyncio.run(test_websocket_listener())
