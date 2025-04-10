
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
🔱 OMEGA BTC AI - BTC WebSocket Unit Test Suite 🔱

This test suite validates the unit-level functionality of the Bitcoin
price feed WebSocket component in the OMEGA BTC AI system.

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
    ⚡ OMEGA BTC AI - BTC WEBSOCKET UNIT TEST SUITE ⚡
    
    🔱 TESTING UNIT FUNCTIONALITY 🔱
    🔱 VALIDATING COSMIC FLOW 🔱
    🔱 ENSURING QUANTUM HARMONY 🔱
""")

async def test_btc_websocket():
    """Test the divine unit functionality of the BTC Price Feed WebSocket.
    
    This test ensures proper connection and message handling from the
    Bitcoin price feed WebSocket server at the unit level.
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
    """Test the divine listener for BTC price updates at the unit level.
    
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
