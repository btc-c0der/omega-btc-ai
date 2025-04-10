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
🔱 OMEGA BTC AI - Simple WebSocket Security Test Runner 🔱

This script runs WebSocket security tests using a separate process to avoid event loop issues.

Version: 0.1.1
GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2025-03-28
"""

import os
import sys
import subprocess
import argparse
import logging
import time
import signal
import re
import tempfile
import threading
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ws_security_test_runner')

def print_banner():
    """Print divine ASCII art banner."""
    print("\n" + "=" * 80)
    print("""
    🔱 OMEGA BTC AI - WEBSOCKET SECURITY TEST RUNNER 🔱
    
    ⚡ ASYNC EVENT LOOP ISOLATION ⚡
    ⚡ QUANTUM TEST EXECUTION ⚡
    ⚡ COSMIC TEST COVERAGE ⚡
    """)
    print("=" * 80 + "\n")

def monitor_server_output(process, output_file):
    """Monitor server output and log important information."""
    with open(output_file, 'r') as f:
        # Move to the end of the file
        f.seek(0, 2)
        while process.poll() is None:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            line = line.strip()
            if "WebSocket Server Running on" in line or "Found available ports" in line:
                logger.info(f"Server: {line}")
            elif "Error" in line or "ERROR" in line:
                logger.error(f"Server error: {line}")

def start_websocket_server():
    """Start the WebSocket server in a separate process."""
    logger.info("Starting WebSocket server...")
    
    # Create a temporary file to capture the server output
    output_file = tempfile.NamedTemporaryFile(delete=False, mode='w+', prefix='ws_server_', suffix='.log')
    output_file.close()
    
    # Prepare the environment with mock settings if enabled
    env = os.environ.copy()
    
    # Set default ports in environment for tests to find
    env['WEBSOCKET_PORT'] = '9000'  
    env['WEBSOCKET_SSL_PORT'] = '9001'
    
    # Start server process with output redirection
    server_process = subprocess.Popen([
        sys.executable,
        "-c",
        """
import asyncio
import os
import logging
import sys

# Set up logging to ensure we capture port information
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Check if we should mock Redis
mock_redis = os.environ.get('OMEGA_MOCK_REDIS', 'False').lower() == 'true'
if mock_redis:
    # Apply monkey patching for Redis mocking
    import sys
    sys.modules['redis'] = type('MockRedis', (), {
        'Redis': type('MockRedisClient', (), {
            'from_url': lambda url, **kwargs: type('MockConnection', (), {
                'ping': lambda: True,
                'get': lambda key: None,
                'set': lambda key, value: True,
                'hget': lambda key, field: None,
                'hset': lambda key, field, value: True,
                'delete': lambda key: True,
                'exists': lambda key: False,
                'execute_command': lambda cmd, *args: None,
                'pubsub': lambda: type('MockPubSub', (), {
                    'subscribe': lambda channel: None,
                    'get_message': lambda timeout=None: None
                })()
            })()
        })
    })

# Import after setting up logging and mocks
from omega_ai.mm_trap_detector.mm_websocket_server_v2 import start_server

# Run the server
async def main():
    await start_server(detect_ports=True)

# Run the server
asyncio.run(main())
"""
    ], stdout=open(output_file.name, 'w'), stderr=subprocess.STDOUT, env=env)
    
    # Start a thread to monitor the server output
    monitor_thread = threading.Thread(
        target=monitor_server_output, 
        args=(server_process, output_file.name),
        daemon=True
    )
    monitor_thread.start()
    
    # Give server time to start
    time.sleep(2)
    
    # Try to extract the actual port numbers from the server output
    port = extract_port_from_output(output_file.name)
    
    # Return the server process and temporary file
    return server_process, output_file.name, port

def extract_port_from_output(output_file):
    """Extract the port numbers from the server output."""
    port = None
    
    try:
        with open(output_file, 'r') as f:
            content = f.read()
            # Look for port in the output
            websocket_match = re.search(r'Running on ws://localhost:(\d+)', content)
            if websocket_match:
                port = websocket_match.group(1)
            else:
                # Try another pattern
                port_match = re.search(r'Found available ports: (\d+)', content)
                if port_match:
                    port = port_match.group(1)
                else:
                    # Default port
                    port = "9000"
    except Exception as e:
        logger.error(f"Error extracting port from output: {e}")
        port = "9000"  # Default port
    
    return port

def run_security_tests(port, test_file=None, no_ssl=False):
    """Run the security tests."""
    logger.info(f"Running security tests: {test_file if test_file else 'all'} on port {port}")
    
    # Set environment variables for tests
    os.environ['WEBSOCKET_PORT'] = port
    os.environ['WEBSOCKET_HOST'] = 'localhost'
    
    # Set SSL environment variable based on no_ssl flag
    os.environ['WEBSOCKET_SSL_ENABLED'] = str(not no_ssl)
    
    # Prepare pytest command
    cmd = [
        sys.executable, "-m", "pytest",
        "-v"
    ]
    
    # Always use external server mode to avoid event loop issues
    cmd.append("--external-server")
    
    # Add test file or directory
    if test_file:
        cmd.append(test_file)
    else:
        cmd.append("tests/integration/websocket/test_websocket_v2_security_2.py")
    
    # Run tests
    logger.info(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Print output
    print("\n--- TEST OUTPUT ---\n")
    print(result.stdout)
    
    if result.stderr:
        print("\n--- TEST ERRORS ---\n")
        print(result.stderr)
    
    return result.returncode

def main():
    """Main function."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run WebSocket security tests')
    parser.add_argument('--test-file', help='Specific test file or test to run')
    parser.add_argument('--no-ssl', action='store_true', help='Disable SSL testing')
    parser.add_argument('--port', help='Specify WebSocket server port')
    parser.add_argument('--mock-redis', action='store_true', help='Use mock Redis for testing')
    options = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Set mock Redis environment if needed
    if options.mock_redis:
        logger.info("Using mock Redis for testing")
        os.environ['OMEGA_MOCK_REDIS'] = 'True'
        os.environ['REDIS_MOCK_MODE'] = 'True'
    
    # Use provided port or start server
    if options.port:
        port = options.port
        server_process = None
        output_file = None
        logger.info(f"Using specified port: {port}")
    else:
        # Start server
        server_process, output_file, port = start_websocket_server()
        logger.info(f"WebSocket server started on port {port}")
    
    try:
        # Run tests
        exit_code = run_security_tests(
            port=port,
            test_file=options.test_file,
            no_ssl=options.no_ssl
        )
        
        # Return the exit code
        return exit_code
        
    finally:
        # Stop server and clean up
        if server_process:
            logger.info("Stopping WebSocket server...")
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()
            logger.info("WebSocket server stopped")
        
        # Clean up temporary file
        if output_file and os.path.exists(output_file):
            try:
                os.unlink(output_file)
            except Exception as e:
                logger.warning(f"Error removing temporary file: {e}")

if __name__ == "__main__":
    # Handle SIGINT
    def signal_handler(sig, frame):
        logger.info("Interrupted, exiting...")
        sys.exit(1)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Run main function
    sys.exit(main()) 