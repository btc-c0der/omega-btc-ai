#!/usr/bin/env python3
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