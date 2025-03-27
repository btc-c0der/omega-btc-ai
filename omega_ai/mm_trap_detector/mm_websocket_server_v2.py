"""
🔱 OMEGA BTC AI - Market Maker WebSocket Server v2 🔱
Sacred WebSocket server for real-time market data broadcasting with enhanced features.

Version: 0.2.2
GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2025-03-28
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
from websockets.legacy.server import WebSocketServerProtocol, serve, WebSocketServer
from websockets.typing import Data
from datetime import datetime, UTC
from omega_ai.visualizer.backend.ascii_art import display_omega_banner, print_status
from typing import Optional, Set, Dict, Any, Union, List, Tuple
import os
import logging
from dataclasses import dataclass
from enum import Enum
import pathlib
import socket

__all__ = ['start_server', 'stop_server', 'ConnectionState', 'ClientInfo', 'find_available_port']

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
MM_WS_PORT = int(os.getenv('WEBSOCKET_PORT', '9886'))
MM_WS_SSL_PORT = int(os.getenv('WEBSOCKET_SSL_PORT', '9887'))
MM_WS_HOST = os.getenv('WEBSOCKET_HOST', 'localhost')
MM_WS_URL = f"ws://{MM_WS_HOST}:{MM_WS_PORT}"
MM_WS_SSL_URL = f"wss://{MM_WS_HOST}:{MM_WS_SSL_PORT}"
MAX_MESSAGE_SIZE = int(os.getenv('WEBSOCKET_MESSAGE_SIZE_LIMIT', str(1024 * 1024)))  # 1MB

# SSL configuration
SSL_CERT_PATH = os.getenv('SSL_CERT_PATH', './SSL_redis-btc-omega-redis.pem')
SSL_KEY_PATH = os.getenv('SSL_KEY_PATH', './SSL_redis-btc-omega-redis.pem')

MAX_RECONNECT_ATTEMPTS = int(os.getenv('WEBSOCKET_MAX_RECONNECT_ATTEMPTS', '3'))
RECONNECT_DELAY = int(os.getenv('WEBSOCKET_RECONNECT_DELAY', '5'))  # seconds

# Global state
connected_clients: Dict[str, ClientInfo] = {}

# Global server instances
regular_server = None
ssl_server = None

def is_port_in_use(port: int) -> bool:
    """
    Check if a port is already in use.
    
    Args:
        port (int): The port number to check
        
    Returns:
        bool: True if the port is in use, False otherwise
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('', port))
            return False
        except OSError:
            return True

def find_available_port(start_port: int = 9000, max_attempts: int = 100) -> Optional[int]:
    """
    Find an available port starting from the given port.
    
    Args:
        start_port (int): The port number to start checking from
        max_attempts (int): Maximum number of ports to check
        
    Returns:
        Optional[int]: An available port or None if none found
    """
    for port in range(start_port, start_port + max_attempts):
        if not is_port_in_use(port):
            return port
    return None

def get_free_port_pair(start_port: int = 9000, min_gap: int = 1, max_gap: int = 10) -> Tuple[int, int]:
    """
    Get a pair of free ports for WebSocket server (regular and SSL).
    
    Args:
        start_port (int): Starting port number for search
        min_gap (int): Minimum gap between the two ports
        max_gap (int): Maximum gap between the two ports
        
    Returns:
        Tuple[int, int]: A pair of available ports
        
    Raises:
        RuntimeError: If unable to find available ports
    """
    import random
    
    # Try to find first available port
    first_port = find_available_port(start_port)
    if not first_port:
        # If we can't find a port starting from specified value, try with a higher range
        backup_start = start_port + 1000
        logger.warning(f"Could not find available port starting from {start_port}, trying {backup_start}")
        first_port = find_available_port(backup_start)
        
    if not first_port:
        raise RuntimeError(f"Could not find initial available port starting from {start_port}")
    
    # Try to find a second port with some gap
    gap = random.randint(min_gap, max_gap)
    second_port = find_available_port(first_port + gap)
    
    # If that fails, try a broader search
    if not second_port:
        logger.warning(f"Could not find second port with gap {gap}, trying wider search")
        for backup_gap in [20, 50, 100]:
            second_port = find_available_port(first_port + backup_gap)
            if second_port:
                break
    
    if not second_port:
        raise RuntimeError(f"Could not find second available port after port {first_port}")
    
    return first_port, second_port

def create_ssl_context() -> Optional[ssl.SSLContext]:
    """Create SSL context for secure WebSocket connections."""
    try:
        cert_path = pathlib.Path(SSL_CERT_PATH).resolve()
        key_path = pathlib.Path(SSL_KEY_PATH).resolve()
        
        if not cert_path.exists():
            logger.warning(f"SSL certificate not found at {cert_path}")
            return None
            
        if not key_path.exists():
            logger.warning(f"SSL key not found at {key_path}")
            return None
            
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        try:
            # Load the certificate and key
            context.load_cert_chain(certfile=str(cert_path), keyfile=str(key_path))
            logger.info(f"SSL context created successfully with cert: {cert_path} and key: {key_path}")
            return context
        except ssl.SSLError as e:
            logger.error(f"Failed to load SSL certificate/key: {e}")
            return None
            
    except Exception as e:
        logger.error(f"Failed to create SSL context: {e}")
        return None

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

async def start_server(detect_ports: bool = False, start_port: int = 9000):
    """
    Start the WebSocket server with divine grace.
    
    Args:
        detect_ports (bool): Whether to auto-detect available ports
        start_port (int): Starting port number for port detection
    """
    global regular_server, ssl_server, MM_WS_PORT, MM_WS_SSL_PORT, MM_WS_URL, MM_WS_SSL_URL
    
    try:
        # Auto-detect ports if requested
        if detect_ports:
            try:
                logger.info(f"Auto-detecting available ports starting from {start_port}...")
                MM_WS_PORT, MM_WS_SSL_PORT = get_free_port_pair(start_port)
                MM_WS_URL = f"ws://{MM_WS_HOST}:{MM_WS_PORT}"
                MM_WS_SSL_URL = f"wss://{MM_WS_HOST}:{MM_WS_SSL_PORT}"
                logger.info(f"Found available ports: {MM_WS_PORT} (regular) and {MM_WS_SSL_PORT} (SSL)")
                
                # Update environment variables
                os.environ['WEBSOCKET_PORT'] = str(MM_WS_PORT)
                os.environ['WEBSOCKET_SSL_PORT'] = str(MM_WS_SSL_PORT)
            except Exception as e:
                logger.error(f"Failed to auto-detect ports: {e}")
                logger.warning("Falling back to default ports. This may cause conflicts.")
                # Continue with default ports
                
        # Start the client monitor task first
        monitor_task = asyncio.create_task(monitor_clients())
        
        # Start regular WebSocket server
        try:
            regular_server = await serve(
                handler,
                MM_WS_HOST,
                MM_WS_PORT,
                max_size=MAX_MESSAGE_SIZE,
                ping_interval=20,
                ping_timeout=10
            )
            logger.info(f"MM WebSocket Server Running on {MM_WS_URL}")
        except OSError as e:
            logger.error(f"Failed to start regular WebSocket server on port {MM_WS_PORT}: {e}")
            if not detect_ports:
                logger.info("Consider using port auto-detection with detect_ports=True")
            raise
        
        # Create SSL context and start SSL server
        ssl_context = create_ssl_context()
        if ssl_context:
            try:
                ssl_server = await serve(
                    handler,
                    MM_WS_HOST,
                    MM_WS_SSL_PORT,
                    ssl=ssl_context,
                    max_size=MAX_MESSAGE_SIZE,
                    ping_interval=20,
                    ping_timeout=10
                )
                logger.info(f"MM WebSocket SSL Server Running on {MM_WS_SSL_URL}")
            except OSError as e:
                logger.error(f"Failed to start SSL WebSocket server on port {MM_WS_SSL_PORT}: {e}")
                # Continue without SSL server
        else:
            logger.warning("SSL WebSocket server not started - missing SSL context")
            
    except Exception as e:
        logger.error(f"Failed to start WebSocket server: {e}")
        raise

async def stop_server():
    """Stop the WebSocket server with divine grace."""
    global regular_server, ssl_server, connected_clients
    
    try:
        # Close all client connections
        for client_id, client_info in connected_clients.items():
            try:
                await client_info.websocket.close()
                logger.info(f"Closed connection for client: {client_id}")
            except Exception as e:
                logger.error(f"Error closing connection for client {client_id}: {e}")
        
        # Clear connected clients
        connected_clients.clear()
        
        # Close servers
        if regular_server:
            regular_server.close()
            await regular_server.wait_closed()
            logger.info("Regular WebSocket server stopped")
            
        if ssl_server:
            ssl_server.close()
            await ssl_server.wait_closed()
            logger.info("SSL WebSocket server stopped")
            
        logger.info("WebSocket servers stopped")
        
    except Exception as e:
        logger.error(f"Error stopping WebSocket server: {e}")
        raise

if __name__ == "__main__":
    # When run directly, use port auto-detection to avoid conflicts
    asyncio.run(start_server(detect_ports=True)) 