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

"""OMEGA Dump Service Runner

This script runs the OMEGA Dump service for divine log management.
It monitors the logs directory, processes log files, and stores them in Redis.
It also integrates with the Redis-based warning system to process warnings.
"""

import os
import sys
import signal
import argparse
import logging
import time
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from omega_ai.services.omega_dump import OMEGALogManager

# Global variable for manager
manager = None

def setup_logging():
    """Setup divine logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def signal_handler(signum, frame):
    """Handle divine interruption signals"""
    logging.info("Received signal to stop OMEGA Dump Service")
    if manager:
        manager.stop()
    sys.exit(0)

def main_loop():
    """Main service loop."""
    global manager
    
    try:
        # Keep running until interrupted
        while True:
            # Check if it's time to process warnings
            manager.check_warning_processing()
            
            # Sleep for a bit
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received")
        manager.stop()
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OMEGA Dump Service Runner")
    parser.add_argument(
        "--logs-dir",
        default="logs",
        help="Directory containing log files"
    )
    parser.add_argument(
        "--backup-dir",
        default="logs/backup",
        help="Directory for log backups"
    )
    parser.add_argument(
        "--redis-url",
        default="redis://localhost:6379/0",
        help="Redis connection URL"
    )
    parser.add_argument(
        "--backup-interval",
        type=int,
        default=3600,
        help="Backup interval in seconds"
    )
    parser.add_argument(
        "--warning-interval",
        type=int,
        default=300,
        help="Warning processing interval in seconds"
    )
    parser.add_argument(
        "--process-warnings",
        action="store_true",
        help="Process warnings from Redis-based warning system"
    )
    parser.add_argument(
        "--warning-type",
        help="Process only warnings of this type (requires --process-warnings)"
    )
    parser.add_argument(
        "--warning-limit",
        type=int,
        default=1000,
        help="Maximum number of warnings to process (requires --process-warnings)"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Initialize and start manager
        manager = OMEGALogManager(
            logs_dir=args.logs_dir,
            backup_dir=args.backup_dir,
            redis_url=args.redis_url,
            backup_interval=args.backup_interval,
            warning_processing_interval=args.warning_interval
        )
        
        logger.info(f"Starting OMEGA Dump Service with configuration:")
        logger.info(f"  Logs directory: {args.logs_dir}")
        logger.info(f"  Backup directory: {args.backup_dir}")
        logger.info(f"  Redis URL: {args.redis_url}")
        logger.info(f"  Backup interval: {args.backup_interval} seconds")
        logger.info(f"  Warning processing interval: {args.warning_interval} seconds")
        
        # Start the manager
        manager.start()
        
        # Process warnings immediately if requested
        if args.process_warnings:
            warning_count = manager.process_warnings(args.warning_type, args.warning_limit)
            logger.info(f"Processed {warning_count} warnings on startup")
            
            # Show warning counts
            warning_counts = manager.get_warning_counts()
            logger.info(f"Warning counts by type: {warning_counts}")
        
        # Run the main loop
        main_loop()
        
    except Exception as e:
        logger.error(f"Error running OMEGA Dump Service: {str(e)}")
        sys.exit(1) 