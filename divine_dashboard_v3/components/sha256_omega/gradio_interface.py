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
SHA256 Omega Gradio Interface Launcher

This script launches the Gradio interface for the SHA256 Omega dashboard, 
providing a web interface for biologically-inspired hash transformations.
"""

import sys
import os

# Add the parent directory to the path to ensure imports work correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import the dashboard module
from components.sha256_omega.sha256_omega_dashboard import demo

def main():
    """Launch the SHA256 Omega Gradio interface"""
    print("🧬 Launching SHA256 Omega Dashboard - Bio-Aligned Cryptographic System")
    print("✨ Aligning with cosmic frequencies...")
    
    # Launch the interface
    demo.launch()
    
    print("🌸 Dashboard is now in bloom")

if __name__ == "__main__":
    main() 