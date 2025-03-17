#!/usr/bin/env python3
"""
OMEGA BTC AI - Main Entry Point
==============================

This script orchestrates the startup of all OMEGA BTC AI components:
1. Market Maker WebSocket Server
2. BTC Live Price Feed
3. MM Trap Detector
4. Visualizer Backend
5. System Monitoring

Copyright (c) 2024 OMEGA BTC AI Team
Licensed under MIT License
"""

import asyncio
import logging
import os
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Import OMEGA components
from omega_ai.mm_trap_detector.mm_websocket_server import start_server as start_mm_ws
from omega_ai.data_feed.btc_live_feed import start_btc_websocket
from omega_ai.mm_trap_detector.mm_trap_processor import process_mm_trap
from omega_ai.visualizer.backend.server import app as visualizer_app

def display_banner():
    """Display OMEGA BTC AI startup banner."""
    banner = """
    🔱 OMEGA BTC AI v1.0 🔱
    =======================
    Market Maker Trap Detection System
    Copyright (c) 2024 OMEGA BTC AI Team
    """
    print(banner)
    logger.info("Starting OMEGA BTC AI components...")

async def start_visualizer():
    """Start the Visualizer Backend."""
    import uvicorn
    config = uvicorn.Config(
        visualizer_app,
        host="0.0.0.0",
        port=8050,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()

async def start_all_components():
    """Start all OMEGA BTC AI components concurrently."""
    display_banner()
    
    # Create thread pool for CPU-bound tasks
    executor = ThreadPoolExecutor(max_workers=3)
    loop = asyncio.get_event_loop()
    
    try:
        # Start components
        mm_ws_task = loop.create_task(start_mm_ws())
        btc_feed_task = loop.run_in_executor(executor, start_btc_websocket)
        trap_processor_task = loop.run_in_executor(executor, process_mm_trap)
        visualizer_task = loop.create_task(start_visualizer())
        
        # Wait for all components
        await asyncio.gather(
            mm_ws_task,
            asyncio.wrap_future(btc_feed_task),
            asyncio.wrap_future(trap_processor_task),
            visualizer_task
        )
    except Exception as e:
        logger.error(f"Error starting components: {e}")
        raise
    finally:
        executor.shutdown(wait=True)

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Received shutdown signal. Cleaning up...")
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start all components
        asyncio.run(start_all_components())
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt. Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1) 