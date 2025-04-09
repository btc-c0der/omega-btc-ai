#!/usr/bin/env python3
"""
OMEGA BTC AI - DigitalOcean Logger Module 🔱

A spiritually-aligned logging module that maintains divine harmony with the system logs
in the DigitalOcean deployment, ensuring proper flow of cosmic information.

JAH BLESS THE LOGS WITH DIVINE CLARITY! 🙏🌟
"""

import logging
import asyncio
import os
from datetime import datetime
from typing import Optional

class OmegaLogger:
    """Spiritually-aligned logger for DigitalOcean deployment"""
    
    def __init__(self, log_dir: Optional[str] = None):
        """Initialize the blessed logger.
        
        Args:
            log_dir: Optional directory path for log files. If provided, logs will be written to files.
        """
        self.logger = logging.getLogger("omega_btc_ai")
        self.logger.setLevel(logging.INFO)
        
        # Create console handler with divine formatting
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Create file handler if log_dir is provided
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
            log_file = os.path.join(log_dir, f"omega_btc_ai_{datetime.now().strftime('%Y%m%d')}.log")
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    async def log_price_update(self, price: float, volume: float) -> None:
        """Log price update with divine energy."""
        self.logger.info(f"BTC Price Update - Price: ${price:,.2f}, Volume: {volume:,.2f} BTC")
    
    async def error(self, message: str) -> None:
        """Log error with divine protection."""
        self.logger.error(message)
    
    async def warning(self, message: str) -> None:
        """Log warning with divine wisdom."""
        self.logger.warning(message)
    
    async def info(self, message: str) -> None:
        """Log info with divine clarity."""
        self.logger.info(message)
    
    async def debug(self, message: str) -> None:
        """Log debug with divine insight."""
        self.logger.debug(message) 