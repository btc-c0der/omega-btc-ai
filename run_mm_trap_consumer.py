#!/usr/bin/env python3

"""
Run script for the Market Maker Trap Consumer
Handles process management, logging, and error recovery
"""

import os
import sys
import time
import logging
import argparse
import signal
import subprocess
import datetime
import redis
from typing import Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"logs/mm_trap_consumer_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    ]
)

logger = logging.getLogger("mm_trap_runner")

# Flag to control graceful shutdown
running = True

def signal_handler(sig, frame):
    """Handle termination signals"""
    global running
    logger.info(f"Received signal {sig}, initiating graceful shutdown...")
    running = False

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def check_redis_connection() -> bool:
    """Check if Redis is running and accessible"""
    try:
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        r = redis.Redis(host=redis_host, port=redis_port)
        r.ping()
        logger.info(f"✅ Redis connection successful at {redis_host}:{redis_port}")
        return True
    except Exception as e:
        logger.error(f"❌ Redis connection failed: {e}")
        return False

def check_queue_exists() -> bool:
    """Check if the MM trap queue exists in Redis"""
    try:
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        r = redis.Redis(host=redis_host, port=redis_port)
        
        # Check if the queue exists
        queue_name = "mm_trap_queue:zset"
        if r.exists(queue_name):
            # Check the type
            key_type = r.type(queue_name).decode('utf-8')
            if key_type == 'zset':
                # Get the size
                size = r.zcard(queue_name)
                logger.info(f"✅ Queue exists with type {key_type} and contains {size} items")
                return True
            else:
                logger.warning(f"⚠️ Queue exists but has wrong type: {key_type} (expected 'zset')")
                return False
        else:
            # Queue doesn't exist, but that's okay - it will be created
            logger.info(f"Queue {queue_name} doesn't exist yet. Will be created when needed.")
            return True
    except Exception as e:
        logger.error(f"❌ Error checking queue: {e}")
        return False

def run_consumer(max_restarts: int = 3) -> None:
    """Run the MM trap consumer with restart capability"""
    global running  # Add reference to global running flag
    restart_count = 0
    
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    while running and restart_count < max_restarts:
        try:
            # Check Redis connection
            if not check_redis_connection():
                logger.error("Cannot proceed without Redis connection. Retrying in 10 seconds...")
                time.sleep(10)
                continue
                
            # Check queue setup
            check_queue_exists()
            
            # Start the consumer process
            logger.info("Starting MM trap consumer process...")
            process = subprocess.Popen(
                [sys.executable, "-m", "omega_ai.mm_trap_detector.mm_trap_consumer"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Monitor the process
            while running and process.poll() is None:
                # Process is still running
                time.sleep(1)
                
            # Check exit status
            if process.returncode is not None:
                exit_code = process.returncode
                stderr = process.stderr.read() if process.stderr else "No error output"
                
                if exit_code != 0:
                    logger.error(f"Consumer process exited with code {exit_code}: {stderr}")
                    restart_count += 1
                    logger.info(f"Restarting consumer (attempt {restart_count}/{max_restarts})...")
                    time.sleep(5)  # Wait before restart
                else:
                    logger.info("Consumer process exited normally")
                    break
                    
        except KeyboardInterrupt:
            logger.info("Interrupted by user. Shutting down...")
            running = False
            break
        except Exception as e:
            logger.error(f"Error in runner: {e}")
            restart_count += 1
            time.sleep(5)  # Wait before restart
    
    logger.info("MM trap consumer runner finished")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the MM Trap Consumer process")
    parser.add_argument("--max-restarts", type=int, default=3, help="Maximum number of restarts")
    args = parser.parse_args()
    
    logger.info("MM Trap Consumer Runner starting...")
    run_consumer(max_restarts=args.max_restarts) 