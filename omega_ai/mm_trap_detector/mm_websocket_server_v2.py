"""
🔱 OMEGA BTC AI - Market Maker WebSocket Server v2 🔱
Sacred WebSocket server for real-time market data broadcasting with enhanced features.

Version: 0.2.0
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
from typing import Optional, Set, Dict, Any, Union, List
import os
import logging
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mm_websocket_v2')

class ConnectionState(Enum):
    """Divine connection states for WebSocket clients."""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    RECONNECTING = "reconnecting"
    ERROR = "error"

@dataclass
class ClientInfo:
    """Sacred information about connected clients."""
    websocket: WebSocketServerProtocol
    state: ConnectionState
    last_message: datetime
    message_count: int
    error_count: int

# Server configuration
MM_WS_PORT = 8765
MM_WS_SSL_PORT = 8766
MM_WS_URL = f"ws://localhost:{MM_WS_PORT}"
MM_WS_SSL_URL = f"wss://localhost:{MM_WS_SSL_PORT}"
MAX_MESSAGE_SIZE = 1024 * 1024  # 1MB limit
SSL_CERT_PATH = os.getenv('SSL_CERT_PATH', 'SSL_redis-btc-omega-redis.pem')
SSL_KEY_PATH = os.getenv('SSL_KEY_PATH', 'SSL_redis-btc-omega-redis.key')
MAX_RECONNECT_ATTEMPTS = 3
RECONNECT_DELAY = 5  # seconds

# Global state
connected_clients: Dict[str, ClientInfo] = {}

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
            logger.warning(f"Message exceeds size limit: {len(message_str.encode('utf-8'))} bytes")
            return None
        
        # Parse JSON
        data = json.loads(message_str)
        if not isinstance(data, dict):
            logger.warning("Message is not a JSON object")
            return None
            
        return data
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON: {e}")
        return None
    except UnicodeError as e:
        logger.warning(f"Unicode error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error validating message: {e}")
        return None

async def handle_client_reconnection(client_id: str, websocket: WebSocketServerProtocol):
    """
    Handle client reconnection with divine patience.
    
    Args:
        client_id: The client's unique identifier
        websocket: The WebSocket connection
    """
    client_info = connected_clients.get(client_id)
    if client_info:
        client_info.state = ConnectionState.RECONNECTING
        client_info.error_count += 1
        
        if client_info.error_count > MAX_RECONNECT_ATTEMPTS:
            logger.warning(f"Client {client_id} exceeded reconnection attempts")
            client_info.state = ConnectionState.ERROR
            return False
            
        await asyncio.sleep(RECONNECT_DELAY)
        client_info.state = ConnectionState.CONNECTED
        return True
    return False

async def handler(websocket: WebSocketServerProtocol):
    """
    Handle incoming WebSocket connections with divine grace.
    
    Args:
        websocket: The WebSocket connection to handle
    """
    global connected_clients
    client_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    client_info = ClientInfo(
        websocket=websocket,
        state=ConnectionState.CONNECTED,
        last_message=datetime.now(UTC),
        message_count=0,
        error_count=0
    )
    
    connected_clients[client_id] = client_info
    logger.info(f"New WebSocket Connection: {client_id}")
    
    try:
        async for message in websocket:
            client_info.last_message = datetime.now(UTC)
            client_info.message_count += 1
            logger.info(f"Received Message from {client_id}: {message}")
            
            # Validate message
            validated_data = validate_message(message)
            if validated_data is None:
                logger.error(f"Invalid message from {client_id}: {message}")
                await websocket.close(1003, "Invalid message format")
                break
            
            # Broadcast valid message
            message_str = to_str(message)
            await broadcast(message_str)
            
    except websockets.exceptions.ConnectionClosedOK:
        logger.info(f"WebSocket Closed Normally: {client_id}")
        client_info.state = ConnectionState.DISCONNECTED
    except websockets.exceptions.ConnectionClosedError as e:
        logger.error(f"WebSocket Disconnected (Error {e.code}): {client_id}")
        client_info.state = ConnectionState.ERROR
    except Exception as e:
        logger.error(f"WebSocket Unexpected Error: {e} - Client: {client_id}")
        client_info.state = ConnectionState.ERROR
    finally:
        if client_id in connected_clients:
            del connected_clients[client_id]
        logger.warning(f"Client Disconnected: {client_id}")

async def broadcast(message: str):
    """
    Broadcast messages to all connected clients with cosmic harmony.
    
    Args:
        message: The message to broadcast
    """
    if connected_clients:
        disconnected = []
        for client_id, client_info in connected_clients.items():
            try:
                await client_info.websocket.send(message)
            except websockets.exceptions.ConnectionClosed:
                logger.warning(f"Client {client_id} disconnected during broadcast")
                disconnected.append(client_id)
            except Exception as e:
                logger.error(f"Error broadcasting to {client_id}: {e}")
                disconnected.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected:
            if client_id in connected_clients:
                del connected_clients[client_id]

def get_ssl_context() -> Optional[ssl.SSLContext]:
    """
    Create SSL context for secure connections with divine protection.
    
    Returns:
        Optional[ssl.SSLContext]: The SSL context or None if creation fails
    """
    try:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(SSL_CERT_PATH, SSL_KEY_PATH)
        ssl_context.check_hostname = False  # Since we're using localhost
        ssl_context.verify_mode = ssl.CERT_NONE  # For testing purposes
        return ssl_context
    except FileNotFoundError as e:
        logger.warning(f"SSL certificate/key not found: {e}")
        return None
    except Exception as e:
        logger.error(f"Error creating SSL context: {e}")
        return None

async def monitor_clients():
    """
    Monitor connected clients and clean up inactive ones.
    """
    while True:
        current_time = datetime.now(UTC)
        inactive_clients = []
        
        for client_id, client_info in connected_clients.items():
            # Check for inactive clients (no messages for 5 minutes)
            if (current_time - client_info.last_message).total_seconds() > 300:
                logger.warning(f"Client {client_id} inactive for 5 minutes")
                inactive_clients.append(client_id)
        
        # Clean up inactive clients
        for client_id in inactive_clients:
            if client_id in connected_clients:
                client_info = connected_clients[client_id]
                try:
                    await client_info.websocket.close(1000, "Inactive client")
                except:
                    pass
                del connected_clients[client_id]
        
        await asyncio.sleep(60)  # Check every minute

async def start_server():
    """
    Start both regular and SSL WebSocket servers with divine energy.
    """
    display_omega_banner("Market Maker WebSocket Server v2")
    
    # Start client monitoring task
    monitor_task = asyncio.create_task(monitor_clients())
    
    # Start regular WebSocket server
    try:
        regular_server = await serve(
            handler,
            "localhost",
            MM_WS_PORT,
            max_size=MAX_MESSAGE_SIZE
        )
        logger.info(f"MM WebSocket Server Running on {MM_WS_URL}")
    except Exception as e:
        logger.error(f"Failed to start regular WebSocket server: {e}")
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
            logger.info(f"MM SSL WebSocket Server Running on {MM_WS_SSL_URL}")
        except Exception as e:
            logger.error(f"Failed to start SSL WebSocket server: {e}")
    else:
        logger.warning("SSL WebSocket server not started - missing SSL context")
        logger.info(f"Please ensure {SSL_CERT_PATH} and {SSL_KEY_PATH} exist")
    
    # Keep servers running
    try:
        await asyncio.gather(
            asyncio.Future(),  # regular server
            asyncio.Future() if ssl_context else asyncio.sleep(0),  # SSL server if available
            monitor_task  # client monitoring
        )
    except KeyboardInterrupt:
        logger.info("Shutting down WebSocket servers...")
    finally:
        logger.info("WebSocket servers stopped")

if __name__ == "__main__":
    asyncio.run(start_server()) 