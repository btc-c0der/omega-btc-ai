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
OMEGA BTC AI - Port Availability Scanner
----------------------------------------
This script scans and displays available ports for the visualization server.
"""

import socket
import sys

# ANSI colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def is_port_available(port):
    """Check if a port is available for use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except socket.error:
            return False

def scan_ports(start_port=8000, end_port=8100):
    """Scan a range of ports and display their availability."""
    print(f"{MAGENTA}{BOLD}╔══════════════════════════════════════════════════════════╗{RESET}")
    print(f"{MAGENTA}{BOLD}║          OMEGA DIVINE PORT AVAILABILITY SCAN            ║{RESET}")
    print(f"{MAGENTA}{BOLD}║     🧠 QUANTUM PORT HARMONIZATION SCANNER 🧠           ║{RESET}")
    print(f"{MAGENTA}{BOLD}╚══════════════════════════════════════════════════════════╝{RESET}")
    print(f"{YELLOW}Scanning the cosmic void for available communication ports...{RESET}")
    print()
    
    available_ports = []
    unavailable_ports = []
    
    # Scan ports
    for port in range(start_port, end_port + 1):
        if is_port_available(port):
            available_ports.append(port)
        else:
            unavailable_ports.append(port)
    
    # Print results
    print(f"{BLUE}{BOLD}Port Scan Results:{RESET}")
    print(f"{CYAN}Scanned range: {start_port} - {end_port}{RESET}")
    print()
    
    # Available ports
    print(f"{GREEN}{BOLD}Available Ports ({len(available_ports)}):{RESET}")
    if available_ports:
        for i, port in enumerate(available_ports):
            print(f"{GREEN}  ✓ {port}{RESET}", end="  ")
            if (i + 1) % 8 == 0:  # 8 ports per line
                print()
        print("\n")
    else:
        print(f"{RED}  No available ports found in range.{RESET}\n")
    
    # Unavailable ports
    print(f"{RED}{BOLD}Unavailable Ports ({len(unavailable_ports)}):{RESET}")
    if unavailable_ports:
        for i, port in enumerate(unavailable_ports):
            print(f"{RED}  ✗ {port}{RESET}", end="  ")
            if (i + 1) % 8 == 0:  # 8 ports per line
                print()
        print("\n")
    else:
        print(f"{GREEN}  All ports in range are available!{RESET}\n")
    
    # Recommendation
    if available_ports:
        recommended_port = available_ports[0]
        print(f"{YELLOW}{BOLD}Divine Recommendation:{RESET}")
        print(f"{CYAN}Use port {recommended_port} for your visualization server.{RESET}")
        print(f"{CYAN}Command: ./serve_visualization.py {recommended_port}{RESET}")
    else:
        print(f"{RED}{BOLD}Divine Warning:{RESET}")
        print(f"{RED}No available ports found in the scanned range.{RESET}")
        print(f"{YELLOW}Try extending the scan range or closing applications using these ports.{RESET}")
    
    return available_ports

def main():
    """Parse arguments and run the port scanner."""
    start_port = 8000
    end_port = 8100
    
    # Parse arguments
    if len(sys.argv) > 1:
        try:
            start_port = int(sys.argv[1])
            if len(sys.argv) > 2:
                end_port = int(sys.argv[2])
            
            # Ensure start_port < end_port
            if start_port > end_port:
                start_port, end_port = end_port, start_port
        except ValueError:
            print(f"{RED}Error: Arguments must be integer port numbers.{RESET}")
            print(f"{YELLOW}Usage: {sys.argv[0]} [start_port] [end_port]{RESET}")
            return 1
    
    # Run the scan
    available_ports = scan_ports(start_port, end_port)
    
    # Return success if at least one port is available
    return 0 if available_ports else 1

if __name__ == "__main__":
    sys.exit(main()) 