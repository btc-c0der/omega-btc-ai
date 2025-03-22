#!/usr/bin/env python3
"""
Test script to check if the MM WebSocket server is working correctly.
"""

import asyncio
import websockets
import argparse
import json
import sys

async def test_connection(host, port, path, message=None):
    """Test connection to a WebSocket server."""
    url = f"ws://{host}:{port}{path}"
    print(f"Connecting to {url}...")
    
    try:
        async with websockets.connect(url, open_timeout=5) as websocket:
            print(f"Connection established to {url}")
            
            if message:
                # Send a test message
                print(f"Sending message: {message}")
                await websocket.send(message)
                print("Message sent successfully")
            
            # Wait for a response with timeout
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                print(f"Received response: {response}")
                return True
            except asyncio.TimeoutError:
                print("No response received within timeout period")
                return True  # Connection still successful even without response
                
    except websockets.WebSocketException as e:
        print(f"WebSocket protocol error: {e}")
        return False
    except (ConnectionRefusedError, OSError) as e:
        print(f"Connection error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Test MM WebSocket connection")
    parser.add_argument("--host", default="localhost", help="WebSocket server host (default: localhost)")
    parser.add_argument("--port", type=int, default=8765, help="WebSocket server port (default: 8765)")
    parser.add_argument("--path", default="/ws", help="WebSocket server path (default: /ws)")
    parser.add_argument("--message", help="Optional test message to send")
    parser.add_argument("--json", action="store_true", help="Format message as JSON before sending")
    
    args = parser.parse_args()
    
    message = args.message
    if message and args.json:
        try:
            # Try to format as JSON if it's not already
            json.loads(message)
        except json.JSONDecodeError:
            message = json.dumps({"type": "test", "content": message})
    
    result = asyncio.run(test_connection(args.host, args.port, args.path, message))
    
    return 0 if result else 1

if __name__ == "__main__":
    sys.exit(main()) 