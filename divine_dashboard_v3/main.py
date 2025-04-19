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
Divine Dashboard v3 - Main Entry Point

Launches the SHA256 Omega cryptographic dashboard with bio-aligned hashing capabilities.
"""

import os
import sys
import gradio as gr

# Add the current directory to the path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the SHA256 Omega dashboard module
from components.sha256_omega.sha256_omega_dashboard import create_interface

def main():
    """Main entry point for the Divine Dashboard v3."""
    print("🧬 Launching Divine Dashboard v3 - SHA256 Omega Module 🧬")
    print("Initializing bio-aligned cryptographic interfaces...")
    
    # Create the interface
    interface = create_interface()
    
    # Launch the interface
    interface.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7860,
        favicon_path="components/sha256_omega/assets/favicon.ico" if os.path.exists("components/sha256_omega/assets/favicon.ico") else None
    )
    
    print("✨ Divine Dashboard v3 is now running and accessible ✨")

if __name__ == "__main__":
    main() 