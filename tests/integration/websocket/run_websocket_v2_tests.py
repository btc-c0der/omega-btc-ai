#!/usr/bin/env python
"""
Run script for WebSocket v2 tests.

This script sets up the test environment and runs the WebSocket v2 performance tests.
"""

import os
import sys
import asyncio
import time
import subprocess
import signal
from pathlib import Path

# Ensure project root is in Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import necessary modules
from omega_ai.mm_trap_detector.mm_websocket_server_v2 import start_server, stop_server

async def start_test_server():
    """Start WebSocket server for testing"""
    # Override environment variables for testing
    os.environ["WEBSOCKET_PORT"] = "9886"
    os.environ["WEBSOCKET_SSL_PORT"] = "9887"
    os.environ["WEBSOCKET_HOST"] = "localhost"
    
    # Disable SSL for testing
    os.environ["SSL_CERT_PATH"] = ""
    os.environ["SSL_KEY_PATH"] = ""
    
    # Start server
    print("Starting WebSocket server for testing...")
    server_task = asyncio.create_task(start_server())
    
    # Wait for server to start
    await asyncio.sleep(1)
    
    return server_task

async def run_tests():
    """Run WebSocket v2 performance tests"""
    # Start server
    server_task = await start_test_server()
    
    try:
        # Run pytest
        cmd = [
            "python", "-m", "pytest",
            "tests/integration/websocket/test_websocket_v2_performance.py",
            "-v",
            "--no-ssl"  # Custom flag to disable SSL
        ]
        
        process = subprocess.Popen(cmd)
        process.wait()
        
    finally:
        # Stop server
        print("Stopping WebSocket server...")
        await stop_server()
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass

def handle_sigint(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\nInterrupted. Shutting down...")
    sys.exit(1)

if __name__ == "__main__":
    # Register signal handler
    signal.signal(signal.SIGINT, handle_sigint)
    
    # Run tests
    asyncio.run(run_tests()) 