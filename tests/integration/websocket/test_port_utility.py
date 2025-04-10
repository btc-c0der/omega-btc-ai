
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

"""Test the WebSocket port utility module.

This module contains tests for the WebSocket port utility functions.
"""

import unittest
import socket
from unittest.mock import patch, MagicMock
import os
import sys
import pytest

# Add the project root to path if needed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# Import the module to test
from tests.integration.websocket.port_utility import (
    find_available_port,
    get_free_port_pair,
    is_port_in_use,
    update_websocket_env_vars,
    get_websocket_uri
)


class TestPortUtility(unittest.TestCase):
    """Test class for WebSocket port utility functions."""

    def test_is_port_in_use_with_free_port(self):
        """Test that is_port_in_use returns False for an unused port."""
        # Find a port that is definitely free
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            free_port = s.getsockname()[1]
        
        # Now test our function with this known free port
        self.assertFalse(is_port_in_use(free_port))
    
    def test_is_port_in_use_with_used_port(self):
        """Test that is_port_in_use returns True for a used port."""
        # Create a socket and bind it to a port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 0))
        used_port = sock.getsockname()[1]
        sock.listen(1)
        
        try:
            # Test that our function detects the port is in use
            self.assertTrue(is_port_in_use(used_port))
        finally:
            sock.close()
    
    def test_find_available_port(self):
        """Test that find_available_port returns a usable port."""
        port = find_available_port()
        self.assertIsNotNone(port)
        
        # Verify the port is usable by binding to it
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('', port))
            success = True
        except OSError:
            success = False
        finally:
            sock.close()
        
        self.assertTrue(success, f"Port {port} returned by find_available_port was not usable")
    
    def test_find_available_port_with_start(self):
        """Test that find_available_port respects the start parameter."""
        start_port = 9000
        port = find_available_port(start_port=start_port)
        self.assertIsNotNone(port)
        self.assertGreaterEqual(port, start_port)
    
    def test_get_free_port_pair(self):
        """Test that get_free_port_pair returns two different usable ports."""
        port1, port2 = get_free_port_pair()
        self.assertIsNotNone(port1)
        self.assertIsNotNone(port2)
        self.assertNotEqual(port1, port2)
        
        # Verify both ports are usable
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            sock1.bind(('', port1))
            sock2.bind(('', port2))
            success = True
        except OSError:
            success = False
        finally:
            sock1.close()
            sock2.close()
        
        self.assertTrue(success, f"Ports {port1} and {port2} returned by get_free_port_pair were not both usable")
    
    def test_update_websocket_env_vars(self):
        """Test that update_websocket_env_vars sets proper environment variables."""
        # Mock environment
        with patch.dict(os.environ, {}, clear=True):
            port1, port2 = 9001, 9002
            update_websocket_env_vars(port1, port2)
            
            self.assertEqual(os.environ.get('WEBSOCKET_PORT'), str(port1))
            self.assertEqual(os.environ.get('WEBSOCKET_SSL_PORT'), str(port2))
    
    def test_get_websocket_uri(self):
        """Test that get_websocket_uri returns proper URIs."""
        port = 9001
        
        # Test regular URI
        uri = get_websocket_uri(port, use_ssl=False)
        self.assertEqual(uri, f"ws://localhost:{port}")
        
        # Test SSL URI
        uri = get_websocket_uri(port, use_ssl=True)
        self.assertEqual(uri, f"wss://localhost:{port}")


if __name__ == '__main__':
    unittest.main() 