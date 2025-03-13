import asyncio
import json
import websockets
from datetime import datetime, UTC

MM_WS_URL = "ws://localhost:8765"

connected_clients = set()

async def handler(websocket):
    """Handles incoming WebSocket connections."""
    global connected_clients
    client_info = websocket.remote_address  # ✅ Define client_info at the start
    print(f"✅ [{datetime.now(UTC)}] New WebSocket Connection: {client_info}")
    
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"📡 [{datetime.now(UTC)}] Received Message: {message}")
            await broadcast(message)
    except websockets.exceptions.ConnectionClosedOK:
        print(f"✅ [{datetime.now(UTC)}] WebSocket Closed Normally: {client_info}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"❌ [{datetime.now(UTC)}] WebSocket Disconnected (Error {e.code}): {client_info}")
    except Exception as e:
        print(f"❌ [{datetime.now(UTC)}] WebSocket Unexpected Error: {e} - Client: {client_info}")
    finally:
        connected_clients.remove(websocket)
        print(f"🔴 [{datetime.now(UTC)}] Client Disconnected: {client_info}")

async def broadcast(message):
    """Broadcast messages to all connected clients."""
    if connected_clients:
        await asyncio.gather(*[ws.send(message) for ws in connected_clients])

async def start_server():
    """Start the WebSocket server."""
    print(f"🚀 MM WebSocket Server Running on {MM_WS_URL}")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # Keeps server running indefinitely

if __name__ == "__main__":
    asyncio.run(start_server())
