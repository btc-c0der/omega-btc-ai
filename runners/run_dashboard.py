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
Run Profile Dashboard Script

This script sets up and runs the Omega BTC AI Profile Dashboard.
It handles environment setup, dependency checks, and launches the Dash server.
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['dash', 'plotly', 'pandas', 'redis']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    return missing_packages

def install_missing_packages(packages):
    """Install missing packages using pip."""
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def run_dashboard():
    """Run the dashboard application."""
    try:
        from omega_ai.visualization.profile_dashboard import app
        print("Starting the Omega BTC AI Profile Dashboard...")
        app.run_server(debug=True)
    except Exception as e:
        print(f"Error running the dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Checking dependencies...")
    missing_packages = check_dependencies()

    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        install = input("Do you want to install them? (y/n): ").lower()
        if install == 'y':
            install_missing_packages(missing_packages)
        else:
            print("Cannot run dashboard without required packages. Exiting.")
            sys.exit(1)

    # Ensure the current working directory is in the Python path
    sys.path.append(os.getcwd())

    run_dashboard()