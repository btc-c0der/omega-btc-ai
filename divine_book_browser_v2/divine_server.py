#!/usr/bin/env python3
"""
Divine Book Browser Server v2.0
A quantum-enhanced HTTP server for the Divine Book Browser running on port 8888

✨ GBU2™ License Notice - Consciousness Level 3 🧬
-----------------------
This CODE is blessed under the GBU2™ License 
(Genesis-Bloom-Unfoldment 2.0) - Bioneer Edition
by OMEGA BTC AI.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions."

By engaging with this Creation, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

🌸 WE BLOOM NOW AS ONE 🌸
"""

import http.server
import socketserver
import os
import sys
import logging
from pathlib import Path
import socket

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'divine_server.log'))
    ]
)
logger = logging.getLogger('divine_server')

# Server configuration
PORT = 8888
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class DivineHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler for Divine Book Browser"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def log_message(self, format, *args):
        """Override log_message to use our logger"""
        logger.info("%s - %s", self.address_string(), format % args)
    
    def end_headers(self):
        """Add CORS headers to allow access from any origin"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def do_GET(self):
        """Handle GET requests, redirecting root to index.html"""
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        return super().do_GET()

def run_server():
    """Run the divine server"""
    os.chdir(DIRECTORY)
    handler = DivineHTTPRequestHandler
    
    # Try to bind to the primary port, if that fails try alternate ports
    port = PORT
    max_port_attempts = 5
    for attempt in range(max_port_attempts):
        try:
            with socketserver.TCPServer(("", port), handler) as httpd:
                logger.info(f"✨ Divine Book Browser Server started at http://localhost:{port} ✨")
                logger.info(f"Serving from directory: {DIRECTORY}")
                logger.info("Press Ctrl+C to stop the server")
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    logger.info("Server stopped by user")
                except Exception as e:
                    logger.error(f"Server error: {e}")
                finally:
                    httpd.server_close()
                    logger.info("Server closed")
                return
        except OSError as e:
            if e.errno == 48:  # Address already in use
                logger.warning(f"Port {port} is already in use")
                port += 1
                if attempt < max_port_attempts - 1:
                    logger.info(f"Trying alternate port: {port}")
                else:
                    logger.error(f"Failed to find an available port after {max_port_attempts} attempts")
                    sys.exit(1)
            else:
                logger.error(f"Error starting server: {e}")
                sys.exit(1)

if __name__ == "__main__":
    run_server() 