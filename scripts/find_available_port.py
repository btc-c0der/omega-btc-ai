#!/usr/bin/env python3

import socket
import argparse
from typing import Optional, Tuple

def is_port_in_use(port: int, host: str = 'localhost') -> bool:
    """Check if a port is in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except socket.error:
            return True

def find_next_available_port(start_port: int, max_attempts: int = 100) -> Tuple[Optional[int], str]:
    """
    Find the next available port starting from start_port.
    Returns a tuple of (port number, status message).
    If no port is found, returns (None, error message).
    """
    for port in range(start_port, start_port + max_attempts):
        if not is_port_in_use(port):
            return port, f"Found available port: {port}"
    return None, f"No available ports found in range {start_port}-{start_port + max_attempts - 1}"

def main():
    parser = argparse.ArgumentParser(description='Find next available port')
    parser.add_argument('--start-port', type=int, default=8000,
                      help='Starting port number (default: 8000)')
    parser.add_argument('--max-attempts', type=int, default=100,
                      help='Maximum number of ports to check (default: 100)')
    args = parser.parse_args()

    port, message = find_next_available_port(args.start_port, args.max_attempts)
    if port is not None:
        print(port)  # Print just the port number for easy scripting
    else:
        print(message)
        exit(1)

if __name__ == '__main__':
    main() 