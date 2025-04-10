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
OMEGA BTC AI - Divine Port Finder
This script finds an available port on the system.
"""

import socket
import argparse
import sys
from contextlib import closing


def is_port_available(port):
    """Check if a port is available for use."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        return sock.connect_ex(('127.0.0.1', port)) != 0


def find_available_port(start_port, max_port=10000):
    """Find an available port starting from the given start_port."""
    for port in range(start_port, max_port + 1):
        if is_port_available(port):
            return port
    return None


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description='Find an available port on the system.')
    parser.add_argument('-s', '--start', type=int, default=8000,
                        help='Start port number to check (default: 8000)')
    parser.add_argument('-m', '--max', type=int, default=10000,
                        help='Maximum port number to check (default: 10000)')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Only output the port number')

    args = parser.parse_args()

    if not args.quiet:
        print(f"🔍 Searching for available port starting from {args.start}...")

    port = find_available_port(args.start, args.max)

    if port:
        if not args.quiet:
            print(f"✅ Found available port: {port}")
        # Just output the port for easy capture in shell scripts
        print(port)
        return 0
    else:
        if not args.quiet:
            print(f"❌ No available ports found between {args.start} and {args.max}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 