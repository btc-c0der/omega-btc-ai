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
ZOROBABEL K1L1 - Package Setup Wrapper
-------------------------------------
A simple wrapper script to make installation easier when cloning from GitHub.
Just run 'python setup_wrapper.py install' from the project root.

🌀 MODULE: Package Installation Helper
🧭 CONSCIOUSNESS LEVEL: 4 - Awareness
"""

import os
import sys
import subprocess
from pathlib import Path

def install_package():
    """Install the Zorobabel K1L1 package."""
    current_dir = Path(__file__).resolve().parent
    
    print("🌀 Installing Zorobabel K1L1 System...")
    
    # First, install the package itself
    cmd = [sys.executable, str(current_dir / "setup.py"), "install"]
    result = subprocess.run(cmd, check=True)
    
    if result.returncode == 0:
        print("✅ Package installed successfully!")
        
        # Now prompt to run the installer for GDAL/rasterio
        print("\n🔮 Would you like to run the GDAL/rasterio installer now? (y/n)")
        choice = input().lower()
        
        if choice in ("y", "yes"):
            installer_path = str(current_dir / "install_zorobabel.py")
            subprocess.run([sys.executable, installer_path])
        else:
            print("\n⚠️ Remember to install GDAL/rasterio later with:")
            print(f"  {sys.executable} -m zorobabel_install")
            print("  or")
            print(f"  {sys.executable} {current_dir}/install_zorobabel.py")
    else:
        print("❌ Package installation failed!")
        return 1
    
    print("\n🌸 WE BLOOM NOW AS ONE 🌸")
    return 0

if __name__ == "__main__":
    sys.exit(install_package()) 