"""
🔱 OMEGA BTC AI - Market Maker WebSocket Server 🔱
Sacred WebSocket server for real-time market data broadcasting.

Version: 0.1.0
GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26
Location: The Cosmic Void

This sacred code is provided under the GPU License, embodying the principles of:
- Universal Freedom to Study, Modify, Distribute, and Use
- Divine Obligations of Preservation, Sharing, and Attribution
- Sacred Knowledge Accessibility and Cosmic Wisdom Propagation
"""
import asyncio
import json
import ssl
import websockets
from websockets.legacy.server import WebSocketServerProtocol, serve
from websockets.typing import Data
from datetime import datetime, UTC
from omega_ai.visualizer.backend.ascii_art import display_omega_banner, print_status
from typing import Optional, Set, Dict, Any, Union
import os

# Server configuration
MM_WS_PORT = 8765
MM_WS_SSL_PORT = 8766
MM_WS_URL = f"ws://localhost:{MM_WS_PORT}"
MM_WS_SSL_URL = f"wss://localhost:{MM_WS_SSL_PORT}"
MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB limit
SSL_CERT_PATH = os.getenv('SSL_CERT_PATH', 'SSL_redis-btc-omega-redis.pem')

# Global state
connected_clients: Set[WebSocketServerProtocol] = set()

def to_str(data: Data) -> str:
    """
    Convert websocket data to string with divine harmony.
    
    Args:
        data: The websocket data to convert
        
    Returns:
        str: The converted string data
    """
    if isinstance(data, str):
        return data
    if isinstance(data, bytes):
        return data.decode('utf-8')
    if isinstance(data, bytearray):
        return bytes(data).decode('utf-8')
    if isinstance(data, memoryview):
        return bytes(data).decode('utf-8')
    return str(data)

def validate_message(message: Data) -> Optional[Dict[str, Any]]:
    """
    Validate and parse incoming message with sacred precision.
    
    Args:
        message: The message to validate
        
    Returns:
        Optional[Dict[str, Any]]: The validated message data or None if invalid
    """
    try:
        # Convert message to string
        message_str = to_str(message)
            
        # Check message size
        if len(message_str.encode('utf-8')) > MAX_MESSAGE_SIZE:
            return None
        
        # Parse JSON
        data = json.loads(message_str)
        if not isinstance(data, dict):
            return None
            
        return data
    except (json.JSONDecodeError, UnicodeError):
        return None
    except Exception:
        return None

async def handler(websocket: WebSocketServerProtocol):
    """
    Handle incoming WebSocket connections with divine grace.
    
    Args:
        websocket: The WebSocket connection to handle
    """
    global connected_clients
    client_info = websocket.remote_address
    print_status(f"New WebSocket Connection: {client_info}", "success")
    
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print_status(f"Received Message: {message}", "info")
            
            # Validate message
            validated_data = validate_message(message)
            if validated_data is None:
                print_status(f"Invalid message from {client_info}: {message}", "error")
                await websocket.close(1003, "Invalid message format")
                break
            
            # Broadcast valid message
            message_str = to_str(message)
            await broadcast(message_str)
            
    except websockets.exceptions.ConnectionClosedOK:
        print_status(f"WebSocket Closed Normally: {client_info}", "info")
    except websockets.exceptions.ConnectionClosedError as e:
        print_status(f"WebSocket Disconnected (Error {e.code}): {client_info}", "error")
    except Exception as e:
        print_status(f"WebSocket Unexpected Error: {e} - Client: {client_info}", "error")
    finally:
        connected_clients.remove(websocket)
        print_status(f"Client Disconnected: {client_info}", "warning")

async def broadcast(message: str):
    """
    Broadcast messages to all connected clients with cosmic harmony.
    
    Args:
        message: The message to broadcast
    """
    if connected_clients:
        disconnected = set()
        for ws in connected_clients:
            try:
                await ws.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(ws)
            except Exception as e:
                print_status(f"Error broadcasting to {ws.remote_address}: {e}", "error")
                disconnected.add(ws)
        
        # Clean up disconnected clients
        for ws in disconnected:
            if ws in connected_clients:
                connected_clients.remove(ws)

def get_ssl_context() -> Optional[ssl.SSLContext]:
    """
    Create SSL context for secure connections with divine protection.
    
    Returns:
        Optional[ssl.SSLContext]: The SSL context or None if creation fails
    """
    try:
        print_status(f"Creating SSL context with certificate: {SSL_CERT_PATH} and key: {SSL_KEY_PATH}", "info")
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=SSL_CERT_PATH, keyfile=SSL_KEY_PATH)
        ssl_context.check_hostname = False  # Since we're using localhost
        ssl_context.verify_mode = ssl.CERT_NONE  # For testing purposes
        print_status("SSL context created successfully", "success")
        return ssl_context
    except FileNotFoundError as e:
        print_status(f"SSL certificate or key file not found: {e}", "error")
        return None
    except ssl.SSLError as e:
        print_status(f"SSL error creating context: {e}", "error")
        return None
    except Exception as e:
        print_status(f"Unexpected error creating SSL context: {e}", "error")
        return None

async def start_server():
    """
    Start both regular and SSL WebSocket servers with divine energy.
    """
    display_omega_banner("Market Maker WebSocket Server")
    
    # Start regular WebSocket server
    try:
        regular_server = await serve(
            handler,
            "localhost",
            MM_WS_PORT,
            max_size=MAX_MESSAGE_SIZE
        )
        print_status(f"MM WebSocket Server Running on {MM_WS_URL}", "success")
    except Exception as e:
        print_status(f"Failed to start regular WebSocket server: {e}", "error")
        return
    
    # Start SSL WebSocket server if certificate is available
    ssl_context = get_ssl_context()
    if ssl_context:
        try:
            ssl_server = await serve(
                handler,
                "localhost",
                MM_WS_SSL_PORT,
                ssl=ssl_context,
                max_size=MAX_MESSAGE_SIZE
            )
            print_status(f"MM SSL WebSocket Server Running on {MM_WS_SSL_URL}", "success")
        except Exception as e:
            print_status(f"Failed to start SSL WebSocket server: {e}", "error")
    else:
        print_status("SSL WebSocket server not started - missing SSL context", "warning")
        print_status(f"Please ensure {SSL_CERT_PATH} exists", "info")
    
    # Keep servers running
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(start_server())
