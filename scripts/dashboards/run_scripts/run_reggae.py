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
Simple launcher for Reggae Dashboard
"""
import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run Reggae Dashboard")
    parser.add_argument("--port", type=int, default=5001, help="Port to run on")
    parser.add_argument("--bg", action="store_true", help="Run in background")
    args = parser.parse_args()

    # Change to the reggae-dashboard directory
    dashboard_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "omega_ai", "visualizer", "frontend", "reggae-dashboard"
    )
    os.chdir(dashboard_dir)
    
    # Execute the server
    cmd = f"python3 live-api-server.py --port {args.port}"
    if args.bg:
        cmd += " &"
    
    print(f"Starting Reggae Dashboard on port {args.port}")
    os.system(cmd)

if __name__ == "__main__":
    main() 