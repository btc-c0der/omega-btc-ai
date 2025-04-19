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
Launch script for the SHA256 vs SHA356 Quantum Comparison Dashboard.
"""

import sys
import os

# Ensure proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(parent_dir)

# Print welcome message
print("🧬 Launching SHA256 vs SHA356 Quantum Comparison Dashboard 🧬")
print("Loading modules...")

try:
    # Check for required packages
    missing_packages = []
    
    try:
        import gradio as gr
    except ImportError:
        missing_packages.append("gradio>=3.23.0")
    
    try:
        import numpy as np
    except ImportError:
        missing_packages.append("numpy>=1.20.0")
    
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        missing_packages.append("matplotlib>=3.5.0")
    
    # If packages are missing, suggest installing them
    if missing_packages:
        print("⚠️ Some required packages are missing:")
        for package in missing_packages:
            print(f"  - {package}")
        
        print("\nPlease install them using:")
        print(f"pip install {' '.join(missing_packages)}")
        sys.exit(1)
    
    # Import the dashboard module
    from sha356_vs_sha256_dashboard import demo
    
    # Launch the dashboard
    print("Starting Gradio interface...")
    print("The dashboard will be available at http://localhost:7860 (or other port if 7860 is in use)")
    demo.launch(share=False)

except Exception as e:
    print(f"❌ Error launching dashboard: {e}")
    print("\nTroubleshooting steps:")
    print("1. Make sure all dependencies are installed:")
    print("   pip install -r requirements.txt")
    print("2. Check that the SHA356 modules are correctly installed")
    print("3. For detailed error information run with debug mode:")
    print("   python launch_quantum_compare.py --debug")
    
    if "--debug" in sys.argv:
        raise  # Re-raise the exception with traceback in debug mode
    
    sys.exit(1) 