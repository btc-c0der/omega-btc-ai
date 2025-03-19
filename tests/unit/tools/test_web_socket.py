import asyncio
import websockets

async def test_connection():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send('{"btc_price": 90500}')
        response = await websocket.recv()
        print(f"📡 Received from WebSocket: {response}")

asyncio.run(test_connection())
