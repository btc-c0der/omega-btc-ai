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

"""Simple HTTP server to serve the Reggae Dashboard static HTML."""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Default port
PORT = 8080

def main():
    """Run the HTTP server for the Reggae Dashboard."""
    # Get the directory of the current script
    current_dir = Path(__file__).parent.absolute()
    
    # Change to the directory containing the HTML files
    os.chdir(current_dir)
    
    # Create handler
    handler = http.server.SimpleHTTPRequestHandler
    
    # Create server
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving Reggae Dashboard at http://localhost:{PORT}")
        print(f"Press Ctrl+C to stop the server")
        
        # Serve until interrupted
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            sys.exit(0)

if __name__ == "__main__":
    main() 