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
RASTA DASHBOARD RUNNER - Entry Point for the Divine Web Visualization
This script launches the Streamlit-based Rasta Dashboard for OMEGA BTC AI System,
providing a sacred web interface to visualize Bitcoin price flows, Fibonacci alignments,
Schumann resonance, and EXODUS flow metrics.

Psalm 19:1
"The heavens declare the glory of God; the skies proclaim the work of his hands."
"""

import os
import sys
import logging
import argparse
from pathlib import Path
import subprocess
import time

# Configure logging with RASTA COLORS
class ColoredFormatter(logging.Formatter):
    """Custom formatter with RASTA colors for logging"""
    
    COLORS = {
        'DEBUG': '\033[36m',  # Cyan
        'INFO': '\033[32m',   # Green
        'WARNING': '\033[33m', # Yellow
        'ERROR': '\033[31m',   # Red
        'CRITICAL': '\033[41m', # Red background
        'RESET': '\033[0m',    # Reset
    }
    
    def format(self, record):
        log_message = super().format(record)
        if hasattr(record, 'levelname'):
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            reset = self.COLORS['RESET']
            log_message = f"{color}{log_message}{reset}"
        return log_message

# Setup logger
logger = logging.getLogger("RASTA_DASHBOARD_RUNNER")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

def display_sacred_banner():
    """Display a sacred banner when starting the dashboard"""
    banner = """
    🔱 OMEGA BTC AI - RASTA DASHBOARD 🔱
    
    =======================================
    |       DIVINE VISUALIZATION         |
    |    FIBONACCI ALIGNED BTC FLOWS     |
    |   SCHUMANN RESONANCE INTEGRATION   |
    |      EXODUS ALGORITHM METRICS      |
    =======================================
    
    "Open your eyes to see the sacred patterns..."
    """
    print(banner)

def check_streamlit_installed():
    """Check if Streamlit is installed, install if not"""
    try:
        import streamlit
        logger.info("✅ Streamlit is already installed")
        return True
    except ImportError:
        logger.warning("⚠️ Streamlit not found, installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
            logger.info("✅ Streamlit installed successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to install Streamlit: {e}")
            return False

def check_dependencies():
    """Check and install required dependencies"""
    required_packages = [
        "pandas",
        "numpy",
        "plotly",
        "redis",
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            logger.debug(f"✅ {package} is already installed")
        except ImportError:
            logger.warning(f"⚠️ {package} not found, installing...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                logger.info(f"✅ {package} installed successfully")
            except Exception as e:
                logger.error(f"❌ Failed to install {package}: {e}")
                return False
    
    return True

def run_dashboard(port=8501, redis_host='localhost', redis_port=6379, redis_db=0):
    """Run the Streamlit dashboard with the given parameters"""
    # Determine the path to the dashboard script
    current_dir = Path(__file__).parent
    visualization_dir = current_dir / 'visualization'
    dashboard_path = visualization_dir / 'rasta_dashboard.py'
    
    if not dashboard_path.exists():
        logger.error(f"❌ Dashboard file not found at {dashboard_path}")
        return False
    
    # Build the Streamlit command
    cmd = [
        "streamlit", "run", str(dashboard_path),
        "--server.port", str(port),
        "--",  # Pass the following as script arguments
        "--redis-host", redis_host,
        "--redis-port", str(redis_port),
        "--redis-db", str(redis_db)
    ]
    
    logger.info(f"🚀 Launching Rasta Dashboard on port {port}")
    logger.info(f"🔌 Connecting to Redis at {redis_host}:{redis_port} DB {redis_db}")
    
    try:
        # Run the Streamlit process
        process = subprocess.Popen(cmd)
        logger.info("✅ Dashboard started successfully")
        
        # Open browser after a short delay
        time.sleep(3)
        
        # Keep the script running while the dashboard is active
        process.wait()
        return True
    except Exception as e:
        logger.error(f"❌ Failed to start dashboard: {e}")
        return False

def main():
    """Main function to parse arguments and run the dashboard"""
    parser = argparse.ArgumentParser(description="RASTA DASHBOARD - Divine Web Visualization for OMEGA BTC AI")
    
    parser.add_argument("--port", type=int, default=8501,
                        help="Port to run the Streamlit dashboard on (default: 8501)")
    parser.add_argument("--redis-host", type=str, default="localhost",
                        help="Redis server host (default: localhost)")
    parser.add_argument("--redis-port", type=int, default=6379,
                        help="Redis server port (default: 6379)")
    parser.add_argument("--redis-db", type=int, default=0,
                        help="Redis database number (default: 0)")
    
    args = parser.parse_args()
    
    # Display banner
    display_sacred_banner()
    
    # Check dependencies
    if not check_streamlit_installed() or not check_dependencies():
        logger.error("❌ Failed to install required dependencies. Exiting.")
        sys.exit(1)
    
    # Run the dashboard
    success = run_dashboard(
        port=args.port,
        redis_host=args.redis_host,
        redis_port=args.redis_port,
        redis_db=args.redis_db
    )
    
    if not success:
        logger.error("❌ Failed to run the dashboard. Please check the logs.")
        sys.exit(1)

if __name__ == "__main__":
    main() 