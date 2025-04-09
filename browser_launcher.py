#!/usr/bin/env python3
"""
OMEGA BTC AI - Browser Launcher
==============================

Handles opening URLs in different browsers based on the URL pattern.
"""

import sys
import webbrowser
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("Browser-Launcher")

def open_url_in_chrome_or_default(url: str) -> None:
    """
    Open URL in Chrome for localhost/127.0.0.1, otherwise use default browser.
    
    Args:
        url: The URL to open
    """
    try:
        if "localhost" in url or "127.0.0.1" in url:
            logger.info(f"Opening localhost URL in Chrome: {url}")
            chrome_path = "open -a /Applications/Google\ Chrome.app %s"
            webbrowser.get(chrome_path).open_new_tab(url)
        else:
            logger.info(f"Opening URL in default browser: {url}")
            webbrowser.open_new_tab(url)
    except Exception as e:
        logger.error(f"❌ Error opening URL: {str(e)}")
        # Fallback to default browser
        webbrowser.open_new_tab(url)

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) > 1:
        url = sys.argv[1]
        open_url_in_chrome_or_default(url)
    else:
        logger.error("❌ No URL provided")
        sys.exit(1)

if __name__ == "__main__":
    main() 