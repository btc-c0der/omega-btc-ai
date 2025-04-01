#!/usr/bin/env python3
"""
🔱 OMEGA BTC AI - Dynamic WebSocket Server Test Runner 🔱

This script runs WebSocket server tests using dynamically assigned ports
to avoid conflicts with other running services.

Version: 0.2.0
GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2025-03-28
"""

import os
import sys
import time
import argparse
import asyncio
import logging
import unittest
import pytest
import socket
import signal
import subprocess
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import WebSocket server with port utilities
from omega_ai.mm_trap_detector.mm_websocket_server_v2 import (
    start_server, 
    stop_server, 
    find_available_port, 
    get_free_port_pair
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('dynamic_ws_test_runner')

# Server instance for cleanup
server_task = None
event_loop = None

# ASCII art banner
def print_banner():
    """Print divine ASCII art banner."""
    print("\n" + "=" * 80)
    print("""
    🔱 OMEGA BTC AI - DYNAMIC WEBSOCKET TEST RUNNER 🔱
    
    ⚡ DIVINE PORT DETECTION ⚡
    ⚡ AUTOMATIC TEST EXECUTION ⚡
    ⚡ COSMIC TEST COVERAGE ⚡
    """)
    print("=" * 80 + "\n")

async def start_test_server(options):
    """
    Start WebSocket server with auto-detected ports.
    
    Args:
        options: Command-line arguments
    
    Returns:
        tuple: Server task and ports (regular, SSL)
    """
    global server_task
    
    # Handle custom ports if specified
    if options.port and options.ssl_port:
        logger.info(f"Using custom ports: {options.port} (regular) and {options.ssl_port} (SSL)")
        os.environ['WEBSOCKET_PORT'] = str(options.port)
        os.environ['WEBSOCKET_SSL_PORT'] = str(options.ssl_port)
        detect_ports = False
    else:
        detect_ports = True or options.dynamic_ports
    
    # Start the server with auto-detection or custom ports
    logger.info(f"Starting WebSocket server...")
    server_task = asyncio.create_task(
        start_server(
            detect_ports=detect_ports, 
            start_port=options.start_port
        )
    )
    
    # Give it a moment to start
    await asyncio.sleep(1)
    
    # Get the actual ports from environment (set by server)
    port = int(os.environ.get('WEBSOCKET_PORT', '9886'))
    ssl_port = int(os.environ.get('WEBSOCKET_SSL_PORT', '9887'))
    logger.info(f"WebSocket server running on ports {port} (regular) and {ssl_port} (SSL)")
    
    return server_task, port, ssl_port

async def stop_test_server():
    """Stop the WebSocket server."""
    global server_task
    
    if server_task:
        logger.info("Stopping WebSocket server...")
        await stop_server()
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass
        server_task = None
        logger.info("WebSocket server stopped")

def run_tests(port, ssl_port, options):
    """
    Run the WebSocket tests with the specified ports.
    
    Args:
        port: Regular WebSocket port
        ssl_port: SSL WebSocket port
        options: Command-line arguments
        
    Returns:
        int: Exit code from pytest
    """
    # Set dynamic port environment variables for tests
    os.environ['DYNAMIC_PORTS_ENABLED'] = 'true' if options.dynamic_ports else 'false'
    os.environ['WEBSOCKET_PORT'] = str(port)
    os.environ['WEBSOCKET_SSL_PORT'] = str(ssl_port)
    os.environ['WEBSOCKET_HOST'] = 'localhost'
    
    # Construct pytest arguments
    pytest_args = [
        '-v',  # Verbose output
        '--no-header',  # No pytest header
    ]
    
    # Add specific arguments
    if options.no_ssl:
        pytest_args.append('--no-ssl')
    
    if options.test_file:
        pytest_args.append(options.test_file)
    else:
        pytest_args.append('tests/integration/websocket')
    
    if options.coverage:
        pytest_args.extend([
            '--cov=omega_ai.mm_trap_detector.mm_websocket_server_v2',
            '--cov-report=term-missing',
            '--cov-report=html'
        ])
    
    if options.external_server:
        pytest_args.append('--external-server')
    
    # Print test information
    logger.info(f"Running tests with ports: {port} (regular) and {ssl_port} (SSL)")
    logger.info(f"WebSocket URI: ws://{os.environ.get('WEBSOCKET_HOST', 'localhost')}:{port}")
    if not options.no_ssl:
        logger.info(f"WebSocket SSL URI: wss://{os.environ.get('WEBSOCKET_HOST', 'localhost')}:{ssl_port}")
    logger.info(f"Pytest arguments: {' '.join(pytest_args)}")
    
    # Run the tests
    # IMPORTANT: We need to run pytest in the main thread to avoid event loop issues
    result = pytest.main(pytest_args)
    return result

async def main_async():
    """Main async function to run the tests."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run WebSocket tests with dynamic port assignment')
    parser.add_argument('--no-ssl', action='store_true', help='Disable SSL testing')
    parser.add_argument('--test-file', help='Specific test file to run')
    parser.add_argument('--coverage', action='store_true', help='Generate test coverage report')
    parser.add_argument('--start-port', type=int, default=9000, help='Start port for searching')
    parser.add_argument('--port', type=int, help='Custom port for regular WebSocket server')
    parser.add_argument('--ssl-port', type=int, help='Custom port for SSL WebSocket server')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--dynamic-ports', action='store_true', help='Force dynamic port detection')
    parser.add_argument('--external-server', action='store_true', help='Use an externally started server')
    options = parser.parse_args()
    
    # Set debug logging if requested
    if options.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.DEBUG)
    
    # Print banner
    print_banner()
    
    try:
        # Skip server start if using external server
        if options.external_server:
            logger.info("Using externally started WebSocket server")
            # Just run tests without starting a server
            result = run_tests(
                int(os.environ.get('WEBSOCKET_PORT', '9886')), 
                int(os.environ.get('WEBSOCKET_SSL_PORT', '9887')), 
                options
            )
            return result
        
        # Start server
        server_task, port, ssl_port = await start_test_server(options)
        
        # Run tests
        result = run_tests(port, ssl_port, options)
        
        # Stop server
        await stop_test_server()
        
        return result
        
    except Exception as e:
        logger.error(f"Error running tests: {e}")
        await stop_test_server()
        return 1

def handle_sigint(signum, frame):
    """Handle SIGINT (Ctrl+C) to clean up servers."""
    logger.info("Interrupt received, cleaning up...")
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(stop_test_server())
    else:
        sys.exit(1)

def main():
    """Main entry point for the script."""
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_sigint)
    signal.signal(signal.SIGTERM, handle_sigint)
    
    # Run the async main function
    try:
        # Create a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(main_async())
        loop.close()
        sys.exit(result)
    except KeyboardInterrupt:
        logger.info("Interrupted by keyboard, exiting...")
        sys.exit(1)

if __name__ == '__main__':
    main() 