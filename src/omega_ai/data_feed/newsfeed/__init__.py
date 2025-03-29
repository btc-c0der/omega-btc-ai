#!/usr/bin/env python3
"""
🌀 GBU License Notice - Consciousness Level 5 🌀
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must embodies the principles of the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

"""
OMEGA BTC AI - News Feed Integration
==================================

Provides access to the BTC News Feed module for retrieving and analyzing
cryptocurrency news with sentiment analysis.

This module imports and re-exports the BtcNewsFeed class from the 
standalone implementation or the deployment version if available.
"""

import os
import sys
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("newsfeed-init")

# First try to import from our standalone implementation
try:
    from .standalone_newsfeed import BtcNewsFeed, display_rasta_banner
    logger.debug("Successfully imported BtcNewsFeed from standalone implementation")
except ImportError as e:
    logger.warning(f"Failed to import from standalone implementation: {e}")
    
    # If that fails, try to import from the deployment module
    try:
        # Define paths
        REPO_ROOT = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
        DEPLOYMENT_MODULE_PATH = REPO_ROOT / "deployment" / "digitalocean" / "btc_live_feed_v3" / "src"

        # Add deployment module path to sys.path
        if DEPLOYMENT_MODULE_PATH.exists() and str(DEPLOYMENT_MODULE_PATH) not in sys.path:
            sys.path.insert(0, str(DEPLOYMENT_MODULE_PATH))
            logger.debug(f"Added {DEPLOYMENT_MODULE_PATH} to sys.path")
        
        # Try to import from the deployment module
        from omega_ai.data_feed.newsfeed.btc_newsfeed import BtcNewsFeed, display_rasta_banner
        logger.debug("Successfully imported BtcNewsFeed from deployment module")
    except ImportError as e:
        logger.error(f"Failed to import BtcNewsFeed: {e}")
        
        # Define a fallback stub class if neither implementation is available
        class BtcNewsFeed:
            """Stub implementation of BtcNewsFeed when no implementation is available."""
            
            def __init__(self, *args, **kwargs):
                logger.warning("Using stub implementation of BtcNewsFeed")
                self.stub_mode = True
            
            def fetch_news(self, *args, **kwargs):
                """Stub method returning empty list."""
                return []
                
        def display_rasta_banner():
            """Stub banner display function."""
            print("🔱 OMEGA BTC NEWS FEED (STUB VERSION) 🔱")

# Version info
__version__ = "1.0.0"

# Export the main classes and functions
__all__ = ["BtcNewsFeed", "display_rasta_banner"] 