#!/usr/bin/env python3
"""OMEGA Dump Service Runner

This script runs the OMEGA Dump service for divine log management.
It monitors the logs directory, processes log files, and stores them in Redis.
"""

import os
import sys
import signal
import argparse
import logging
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from omega_ai.services.omega_dump import OMEGALogManager

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
            backup_interval=args.backup_interval
        )
        
        logger.info(f"Starting OMEGA Dump Service with configuration:")
        logger.info(f"  Logs directory: {args.logs_dir}")
        logger.info(f"  Backup directory: {args.backup_dir}")
        logger.info(f"  Redis URL: {args.redis_url}")
        logger.info(f"  Backup interval: {args.backup_interval} seconds")
        
        manager.start()
        
        # Keep running until interrupted
        signal.pause()
        
    except Exception as e:
        logger.error(f"Error running OMEGA Dump Service: {str(e)}")
        sys.exit(1) 