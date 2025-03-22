#!/usr/bin/env python3
"""
Tool to check if the MM WebSocket server is running.
This script can be used by other components to verify the status of the MM WebSocket server.
"""

import socket
import sys
import argparse
import json

def check_mm_server_running(port):
    """Check if the MM WebSocket server is running on the specified port."""
    try:
        # Try to create a simple socket connection to the port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        if result == 0:
            # Port is open, but we need to verify it's our MM WebSocket server
            # For now, just assume it's the MM WebSocket server if the port is open
            return True
        return False
    except Exception:
        return False

def main():
    """Main function to check MM WebSocket server status."""
    parser = argparse.ArgumentParser(description="Check if MM WebSocket server is running")
    parser.add_argument("--port", type=int, default=8765, help="Port to check (default: 8765)")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    
    args = parser.parse_args()
    
    is_running = check_mm_server_running(args.port)
    
    if args.json:
        result = {
            "is_running": is_running,
            "port": args.port
        }
        print(json.dumps(result))
    else:
        if is_running:
            print(f"MM WebSocket server is running on port {args.port}")
        else:
            print(f"MM WebSocket server is NOT running on port {args.port}")
    
    return 0 if is_running else 1

if __name__ == "__main__":
    sys.exit(main()) 