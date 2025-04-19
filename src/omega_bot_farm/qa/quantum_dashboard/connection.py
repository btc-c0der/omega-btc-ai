#!/usr/bin/env python3

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

"""
Quantum 5D QA Dashboard Connection Manager
----------------------------------------

This module provides connection management functionality for the Quantum 5D QA Dashboard,
including automatic port detection and availability checking.
"""

import os
import socket
import logging
import platform
import subprocess
from typing import Tuple, Optional, List

# Set up logging
logger = logging.getLogger("Quantum5DQADashboard.Connection")

class ConnectionManager:
    """Manages connections for the Quantum QA Dashboard."""
    
    DEFAULT_PORT = 8051
    DEFAULT_HOST = "0.0.0.0"
    MAX_PORT_ATTEMPTS = 10
    
    def __init__(self, host: str = None, port: int = None):
        """Initialize the connection manager.
        
        Args:
            host: Host IP to listen on (default: 0.0.0.0)
            port: Port to use (default: 8051, will auto-detect if taken)
        """
        self.host = host or self.DEFAULT_HOST
        self.requested_port = port or self.DEFAULT_PORT
        self.port = None
        self._find_available_port()
    
    def _is_port_available(self, port: int) -> bool:
        """Check if a port is available on the specified host.
        
        Args:
            port: Port number to check
            
        Returns:
            True if port is available, False otherwise
        """
        try:
            # Create a socket and try to bind to the port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.2)  # Set a small timeout
                result = s.connect_ex((self.host, port))
                # If result is not 0, the port is available
                return result != 0
        except Exception as e:
            logger.debug(f"Error checking port {port}: {e}")
            # If there's an error, assume the port is not available
            return False
    
    def _find_available_port(self) -> None:
        """Find an available port starting from the requested port."""
        current_port = self.requested_port
        
        for attempt in range(self.MAX_PORT_ATTEMPTS):
            if self._is_port_available(current_port):
                self.port = current_port
                
                if current_port != self.requested_port:
                    logger.warning(f"Requested port {self.requested_port} was not available. Using port {current_port} instead.")
                else:
                    logger.info(f"Using requested port {current_port}")
                
                return
            
            # If the port is not available, try the next port
            logger.debug(f"Port {current_port} is not available, trying next port")
            current_port += 1
        
        # If we get here, we've tried MAX_PORT_ATTEMPTS ports and none were available
        # Set to the last attempted port and show warning
        self.port = current_port - 1
        logger.warning(f"Could not find an available port after {self.MAX_PORT_ATTEMPTS} attempts. Using port {self.port}, but it may be in use.")
    
    def get_connection_info(self) -> Tuple[str, int]:
        """Get the host and port for the connection.
        
        Returns:
            Tuple of (host, port)
        """
        return self.host, self.port
    
    def get_urls(self) -> List[str]:
        """Get URLs that can be used to access the dashboard.
        
        Returns:
            List of URLs for accessing the dashboard
        """
        urls = []
        
        # If listening on all interfaces, add URLs for each network interface
        if self.host == "0.0.0.0":
            # Add localhost
            urls.append(f"http://localhost:{self.port}")
            urls.append(f"http://127.0.0.1:{self.port}")
            
            # Try to get local IP addresses
            try:
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                if local_ip and local_ip not in ("127.0.0.1", "::1"):
                    urls.append(f"http://{local_ip}:{self.port}")
            except Exception as e:
                logger.debug(f"Could not get local IP address: {e}")
        else:
            # If specific host, just use that
            urls.append(f"http://{self.host}:{self.port}")
        
        return urls
    
    def open_dashboard(self) -> bool:
        """Open the dashboard in the default browser.
        
        Returns:
            True if browser was opened, False otherwise
        """
        url = self.get_urls()[0]  # Use the first URL
        
        try:
            # Open URL in the browser based on the platform
            system = platform.system()
            
            if system == 'Darwin':  # macOS
                subprocess.run(['open', url], check=True)
            elif system == 'Windows':
                subprocess.run(['start', url], shell=True, check=True)
            elif system == 'Linux':
                subprocess.run(['xdg-open', url], check=True)
            else:
                logger.warning(f"Unsupported platform: {system}")
                return False
            
            logger.info(f"Opened dashboard in browser at {url}")
            return True
        except Exception as e:
            logger.error(f"Error opening browser: {e}")
            return False
    
    def print_connection_info(self) -> None:
        """Print connection information in a user-friendly format."""
        print(f"\n{'*' * 60}")
        print(f"* Quantum 5D QA Dashboard is running!")
        print(f"* {'*' * 56}")
        
        if self.port != self.requested_port:
            print(f"* ⚠️  Port {self.requested_port} was not available, using port {self.port} instead")
        
        print("\n* 🌐 Access from:")
        for i, url in enumerate(self.get_urls(), 1):
            print(f"*    {i}. {url}")
        
        print("\n* 🛑 Press Ctrl+C to stop the dashboard")
        print(f"{'*' * 60}\n")


def get_connection_manager(host: str = None, port: int = None) -> ConnectionManager:
    """Create and return a connection manager.
    
    Args:
        host: Host IP to listen on (default: 0.0.0.0)
        port: Port to use (default: 8051, will auto-detect if taken)
        
    Returns:
        Configured ConnectionManager instance
    """
    return ConnectionManager(host, port) 