import asyncio
import json
import redis
import websockets

async def test_btc_websocket():
    """Test WebSocket Connection to BTC Price Feed"""
    async with websockets.connect("ws://localhost:8765") as ws:
        print("✅ Connected to BTC WebSocket")
        try:
            async for message in ws:
                data = json.loads(message)
                print(f"📡 [DEBUG] BTC Price Update Received: {data}")
        except websockets.exceptions.ConnectionClosedError:
            print("❌ WebSocket Connection Lost!")

# asyncio.run(test_btc_websocket())

redis_conn = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

btc_price = redis_conn.get("live_btc_price")
print(f"📡 [DEBUG] BTC Price in Redis: {btc_price}")

def get_live_btc_price():
    """Fetches the latest BTC price stored in Redis & DEBUGS Redis Read Issues."""
    try:
        price = redis_conn.get("live_btc_price")
        print(f"📡 [DEBUG] Fetching BTC Price from Redis: {price}")  # 🔥 ADDED DEBUG
        return float(price) if price else 0
    except Exception as e:
        print(f"❌ [DEBUG] Redis Fetch Error: {e}")
        return 0

# get_live_btc_price()

async def test_websocket_listener():
    """Test if the WebSocket listener receives BTC price updates"""
    async with websockets.connect("ws://localhost:8765") as ws:
        print("✅ Connected to BTC WebSocket")
        async for message in ws:
            data = json.loads(message)
            print(f"📡 [DEBUG] BTC Price Update Received: {data}")

asyncio.run(test_websocket_listener())
