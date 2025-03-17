import asyncio
import json
import redis
import websockets
from rq import Queue

MM_WS_URL = "ws://localhost:8765"

# ✅ Redis Connection
redis_conn = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# ✅ Use the existing MM Trap Queue
mm_queue = Queue("mm_trap_queue", connection=redis_conn)

async def handle_message(message):
    """Process incoming WebSocket message and enqueue it."""
    try:
        data = json.loads(message)
        price = float(data.get("btc_price", 0))
        print(f"📡 Received BTC Price: ${price:.2f}")

        # ✅ Instead of separate processing, push into MM Trap Queue
        mm_queue.enqueue("omega_ai.processors.trap_processor", price)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"❌ Invalid WebSocket Message: {message} | Error: {e}")

async def listen_to_btc_websocket():
    """Connects to MM WebSocket and pushes BTC prices into Redis queue."""
    while True:
        try:
            async with websockets.connect(
                MM_WS_URL,
                max_size=2**24,  
                ping_interval=15,  
                ping_timeout=5,  
                close_timeout=2  
            ) as ws:
                print("✅ Connected to MM WebSocket Server")
                async for message in ws:
                    await handle_message(message)
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"❌ WebSocket Disconnected (Error {e.code}) - Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except websockets.exceptions.ConnectionClosedOK:
            print("✅ WebSocket Closed Normally. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
        except websockets.exceptions.WebSocketException as e:
            print(f"❌ WebSocket Error: {e} - Restarting in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"❌ Unexpected Error: {e} - Restarting in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    print("🚀 Starting MM Trap Analyzer...")
    asyncio.run(listen_to_btc_websocket())