#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
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
SHA-356 vs SHA-256 Comparison Runner

This script safely wraps the comparison dashboard to handle dependencies.
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

# Get the current directory
current_dir = Path(__file__).parent.absolute()

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = ["numpy", "matplotlib", "gradio"]
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"⚠️ Missing required packages: {', '.join(missing_packages)}")
        install = input(f"Would you like to install these packages now? (y/n): ")
        if install.lower() in ("y", "yes"):
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
                print("✅ Dependencies installed successfully!")
                return True
            except subprocess.CalledProcessError:
                print("❌ Failed to install dependencies. Please install them manually.")
                print(f"Run: pip install {' '.join(missing_packages)}")
                return False
        else:
            print("⚠️ Cannot continue without required dependencies.")
            return False
    
    return True

def main():
    """Main entry point for the comparison runner."""
    print("🔄 SHA-356 vs SHA-256 Quantum Comparison 🔄")
    print("------------------------------------------")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Add current directory to path
    sys.path.insert(0, str(current_dir))
    
    try:
        # First try to import the dashboard if it exists
        try:
            from sha356_vs_sha256_dashboard import demo
            print("📊 Launching SHA-356 vs SHA-256 Dashboard...")
            demo.launch()
        except ImportError:
            # Fall back to simple comparison script
            print("📊 Running SHA-356 vs SHA-256 Comparison...")
            from compare_sha256 import main as compare_main
            compare_main()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 