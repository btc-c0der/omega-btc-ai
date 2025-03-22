import asyncio
import json
import websockets
from datetime import datetime, UTC
from omega_ai.visualizer.backend.ascii_art import display_omega_banner, print_status
import os

MM_WS_PORT = 8765
MM_WS_PATH = "/ws"
MM_WS_URL = f"ws://localhost:{MM_WS_PORT}{MM_WS_PATH}"

connected_clients = set()

async def ws_handler(websocket):
    """Handles incoming WebSocket connections."""
    # In websockets 15.0+ the path is accessible via websocket.path
    if websocket.path != MM_WS_PATH:
        await websocket.close(1008, f"Path not found: {websocket.path}")
        return
        
    global connected_clients
    client_info = websocket.remote_address
    print_status(f"New WebSocket Connection: {client_info} on path {websocket.path}", "success")
    
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
    
    # In websockets 15.0+, the server checks paths automatically based on routes
    async with websockets.serve(ws_handler, "localhost", MM_WS_PORT):
        await asyncio.Future()  # Keeps server running indefinitely

if __name__ == "__main__":
    asyncio.run(start_server())
