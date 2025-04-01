"""WebSocket port utility module.

This module provides functions for finding available ports, checking if ports are in use,
and generating WebSocket URIs. It helps ensure the WebSocket server tests don't conflict 
with running services.

Version: 0.1.0
GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
"""

import socket
import random
import os
from typing import Tuple, Optional


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
    first_port = find_available_port(start_port)
    if not first_port:
        raise RuntimeError("Could not find initial available port")
    
    # Try to find a second port with some gap
    gap = random.randint(min_gap, max_gap)
    second_port = find_available_port(first_port + gap)
    
    # If that fails, try a broader search
    if not second_port:
        second_port = find_available_port(first_port + max_gap + 1)
    
    if not second_port:
        raise RuntimeError("Could not find second available port")
    
    return first_port, second_port


def update_websocket_env_vars(port: int, ssl_port: int) -> None:
    """
    Update environment variables for WebSocket server configuration.
    
    Args:
        port (int): Regular WebSocket port
        ssl_port (int): SSL WebSocket port
    """
    os.environ['WEBSOCKET_PORT'] = str(port)
    os.environ['WEBSOCKET_SSL_PORT'] = str(ssl_port)


def get_websocket_uri(port: int, host: str = 'localhost', use_ssl: bool = False) -> str:
    """
    Get WebSocket URI for connecting to the server.
    
    Args:
        port (int): Port number
        host (str): Hostname
        use_ssl (bool): Whether to use SSL (wss:// vs ws://)
        
    Returns:
        str: WebSocket URI
    """
    protocol = 'wss' if use_ssl else 'ws'
    return f"{protocol}://{host}:{port}" 