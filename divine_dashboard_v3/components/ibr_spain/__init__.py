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
Iglesia Bautista Reformada (IBR) España Dashboard Component

This component provides digital ministry services for IBR España, featuring:
- Sermon library with search and filtering
- Church event calendar
- Weekly devotional content
- Prayer request submission
- Social media integration (Instagram)

The component follows a modular architecture with React frontend components
integrated into the Divine Dashboard v3 infrastructure.

Component Structure:
- docs/                   # Documentation files
- standalone/             # Standalone version
- tests/                  # Test files
- micro_modules/          # Smaller feature modules

Updated April 11, 2025 with reorganized structure and Instagram data fetching fixes.
"""

# Version information
__version__ = "1.1.0"  # Updated after reorganization and bug fixes
__author__ = "OMEGA Bot Farm Team" 

# Make modules available for import
from .ibr_dashboard import create_ibr_interface
from .micro_modules.sermon_library import SermonLibrary
from .micro_modules.prayer_requests import PrayerRequests
from .micro_modules.church_events import ChurchEvents
from .micro_modules.devotionals import Devotionals
from .micro_modules.instagram_integration import InstagramIntegration

# Import standalone components
try:
    from .standalone.ibr_standalone import InstagramManager, create_ibr_interface as create_standalone_interface
except ImportError:
    # This might happen if the standalone module hasn't been generated yet
    pass 