#!/usr/bin/env python3
"""
ZOROBABEL K1L1 - 5D Geospatial Visualization System
--------------------------------------------------
Divine spiral mapping system for sacred locations with cosmic resonance points.

🌀 PACKAGE: Geospatial Visualization System
🧭 CONSCIOUSNESS LEVEL: 7 - Wisdom

This package provides geospatial visualization tools for mapping sacred sites
and cosmic energetic patterns using digital elevation models and spiritual overlays.
"""

__version__ = '0.1.0'
__author__ = 'GBU2™ Divine Team'
__license__ = 'GBU2™ LICENSE - Genesis-Bloom-Unfoldment 2.0'

# Import main classes and functions for easier access
try:
    from .zorobabel_k1l1 import ZorobabelMapper
    from .dem_util import DEMDownloader, ensure_dem_available
except ImportError:
    # Handle the case when dependencies are not installed
    # This allows the package to be imported but will raise errors
    # only when the specific modules are used
    pass


def run_web_interface(port=8050, auto_open_browser=True):
    """
    Run the web interface for the Zorobabel K1L1 visualization system.
    
    Args:
        port: Port to use for the web server (will auto-find if occupied)
        auto_open_browser: Whether to automatically open a web browser
    """
    try:
        from .zorobabel_ui import main
        main(default_port=port, auto_open_browser=auto_open_browser)
    except ImportError as e:
        print(f"⚠️ Error: Could not start web interface: {e}")
        print("⚠️ Please ensure all dependencies are installed.")
        print("⚠️ Try running: pip install -r geospatial/requirements.txt")


# Define public API
__all__ = [
    "ZorobabelMapper",
    "DEMDownloader",
    "ensure_dem_available",
    "run_web_interface",
]


# ASCII art signature
__signature__ = """
┌───────────────────────────────────────────────────┐
│                                                   │
│              🌀 ZOROBABEL K1L1 🌀                │
│         5D Sacred Geospatial System               │
│                                                   │
│        "The divine spiral of sacred wisdom"       │
│                                                   │
│       🌸 WE BLOOM NOW AS ONE 🌸                  │
│                                                   │
└───────────────────────────────────────────────────┘
"""

# Print the signature when the package is imported directly
if __name__ != "__main__":
    print(__signature__) 