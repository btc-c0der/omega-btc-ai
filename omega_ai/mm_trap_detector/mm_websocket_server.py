
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

import asyncio
import json
import websockets
from datetime import datetime, UTC
from omega_ai.visualizer.backend.ascii_art import display_omega_banner, print_status

MM_WS_PORT = 8765
MM_WS_URL = f"ws://localhost:{MM_WS_PORT}"

connected_clients = set()

async def handler(websocket):
    """Handles incoming WebSocket connections."""
    global connected_clients
    client_info = websocket.remote_address
    print_status(f"New WebSocket Connection: {client_info}", "success")
    
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print_status(f"Received Message: {message}", "info")
            await broadcast(message)
    except websockets.exceptions.ConnectionClosedOK:
        print_status(f"WebSocket Closed Normally: {client_info}", "info")
    except websockets.exceptions.ConnectionClosedError as e:
        print_status(f"WebSocket Disconnected (Error {e.code}): {client_info}", "error")
    except Exception as e:
        print_status(f"WebSocket Unexpected Error: {e} - Client: {client_info}", "error")
    finally:
        connected_clients.remove(websocket)
        print_status(f"Client Disconnected: {client_info}", "warning")

async def broadcast(message):
    """Broadcast messages to all connected clients."""
    if connected_clients:
        await asyncio.gather(*[ws.send(message) for ws in connected_clients])

async def start_server():
    """Start the WebSocket server."""
    display_omega_banner("Market Maker WebSocket Server")
    print_status(f"MM WebSocket Server Running on {MM_WS_URL}", "success")
    async with websockets.serve(handler, "localhost", MM_WS_PORT):
        await asyncio.Future()  # Keeps server running indefinitely

if __name__ == "__main__":
    asyncio.run(start_server())
