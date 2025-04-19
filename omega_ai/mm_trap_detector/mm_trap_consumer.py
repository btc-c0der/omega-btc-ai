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
Market Maker Trap Queue Consumer
Efficiently processes the mm_trap_queue with sorted sets
"""

import json
import time
import signal
import datetime
import threading
import logging
from typing import Dict, Any, List, Optional, Tuple
from redis.exceptions import ConnectionError, ResponseError

# Import the improved RedisManager
from omega_ai.utils.redis_manager import RedisManager
from omega_ai.alerts.alerts_orchestrator import send_mm_trap_alert
from omega_ai.db_manager.database import insert_possible_mm_trap

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Initialize Redis manager
redis_manager = RedisManager()

# Configuration
QUEUE_NAME = "mm_trap_queue:zset"  # Using sorted set queue
BATCH_SIZE = 50
SLEEP_WHEN_EMPTY = 0.1  # seconds
PROCESSING_TIMEOUT = 60  # seconds

# Control flag for graceful shutdown
running = True

def signal_handler(sig, frame):
    """Handle termination signals for graceful shutdown"""
    global running
    logger.info("Shutdown signal received, finishing current batch...")
    running = False

# Set up signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

class TrapProcessor:
    """Process market maker traps from queue"""
    
    def __init__(self):
        self.stats = {
            "processed": 0,
            "errors": 0,
            "start_time": time.time(),
            "last_processed": None,
            "processing_rate": 0
        }
        self.stats_lock = threading.Lock()
    
    def update_stats(self, processed=0, errors=0):
        """Update processing statistics"""
        with self.stats_lock:
            self.stats["processed"] += processed
            self.stats["errors"] += errors
            self.stats["last_processed"] = datetime.datetime.now()
            
            elapsed = time.time() - self.stats["start_time"]
            if elapsed > 0:
                self.stats["processing_rate"] = self.stats["processed"] / elapsed
    
    def process_trap(self, trap_data):
        """Process a single trap event"""
        try:
            # Decode binary data if needed
            if isinstance(trap_data, bytes):
                trap_data = trap_data.decode('utf-8')
                
            # Parse JSON if it's a JSON string
            if isinstance(trap_data, str):
                try:
                    trap_data = json.loads(trap_data)
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON format: {e}")
                    return False
            
            # Ensure trap_data is a dictionary at this point
            if not isinstance(trap_data, dict):
                logger.error(f"Expected dictionary for trap_data, got {type(trap_data)}")
                return False
            
            # Extract trap details
            trap_type = trap_data.get('type', 'Unknown')
            confidence = trap_data.get('confidence', 0)
            price = trap_data.get('price', 0)
            price_change = trap_data.get('price_change', 0)
            liquidity_grabbed = trap_data.get('liquidity_grabbed', 0)
            
            # Standardize trap data format
            standardized_trap = {
                "trap_type": trap_type.lower().replace("-", "_").replace(" ", "_"),
                "btc_price": float(price) if isinstance(price, str) else price,
                "price_change": float(price_change) if isinstance(price_change, str) else price_change,
                "confidence": float(confidence) if isinstance(confidence, str) else confidence,
                "liquidity_grabbed": float(liquidity_grabbed) if isinstance(liquidity_grabbed, str) else liquidity_grabbed,
                "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
            }
            
            # Process trap based on confidence
            if standardized_trap["confidence"] > 0.8:
                # High confidence trap - log to database and send alert
                logger.info(f"⚠️ HIGH CONFIDENCE TRAP: {trap_type} at ${standardized_trap['btc_price']:.2f} ({standardized_trap['confidence']:.2f})")
                
                # Prepare data for database
                db_trap_data = {
                    "type": standardized_trap["trap_type"],
                    "price": standardized_trap["btc_price"],
                    "price_change": standardized_trap["price_change"],
                    "confidence": standardized_trap["confidence"],
                    "timeframe": "1h",  # Default timeframe
                    "timestamp": standardized_trap["timestamp"]
                }
                
                # Store in database
                insert_possible_mm_trap(db_trap_data)
                
                # Send specialized alert with highlighted formatting
                send_mm_trap_alert(standardized_trap)
            else:
                # Low confidence trap - just log
                logger.info(f"ℹ️ Low confidence trap: {trap_type} ({standardized_trap['confidence']:.2f})")
            
            return True
        except Exception as e:
            logger.error(f"Error processing trap: {e}")
            return False
    
    def process_batch(self, batch):
        """Process a batch of trap events"""
        successful = 0
        errors = 0
        
        for item in batch:
            if self.process_trap(item):
                successful += 1
            else:
                errors += 1
                
        self.update_stats(processed=successful, errors=errors)
        return successful, errors
        
    def run_consumer(self):
        """Main consumer loop"""
        logger.info(f"Starting trap consumer for {QUEUE_NAME}")
        empty_count = 0
        
        while running:
            try:
                # Get items from sorted set (newest first)
                items = None
                try:
                    # We need to use redis directly for zrange, since our RedisManager might not
                    # fully implement this for sorted sets
                    items = redis_manager.redis.zrange(QUEUE_NAME, 0, BATCH_SIZE-1)
                    logger.debug(f"Retrieved {len(items) if items else 0} items from queue")
                except ResponseError as e:
                    logger.error(f"Redis response error: {e}")
                    # If this is a WRONGTYPE error, the key might exist but as wrong type
                    if "WRONGTYPE" in str(e):
                        logger.warning(f"Queue key {QUEUE_NAME} exists but has wrong type. Attempting recovery...")
                        # Try to read the actual type
                        key_type = redis_manager.get_key_type(QUEUE_NAME)
                        logger.info(f"Found key type: {key_type}")
                        if key_type and key_type != 'zset':
                            # Try to fix it by creating proper zset
                            try:
                                # First rename the existing key to backup
                                backup_key = f"{QUEUE_NAME}_backup_{int(time.time())}"
                                redis_manager.redis.rename(QUEUE_NAME, backup_key)
                                logger.info(f"Renamed problematic key to {backup_key}")
                            except Exception as rename_error:
                                logger.error(f"Error renaming key: {rename_error}")
                    time.sleep(1)
                    continue
                except Exception as e:
                    logger.error(f"Error retrieving items from queue: {e}")
                    time.sleep(1)
                    continue
                    
                if not items:
                    empty_count += 1
                    if empty_count % 100 == 0:
                        logger.info(f"Queue empty for {empty_count} checks")
                    time.sleep(SLEEP_WHEN_EMPTY)
                    continue
                
                # Reset empty counter
                empty_count = 0
                
                # Process this batch
                successful, errors = self.process_batch(items)
                
                # Remove processed items from the queue
                if successful > 0:
                    try:
                        # Get the items we need to remove - we're taking the first "successful" items
                        items_to_remove = items[:successful]
                        
                        # Remove these items from the queue using zrem
                        removed = redis_manager.redis.zrem(QUEUE_NAME, *items_to_remove)
                        
                        logger.debug(f"Removed {removed} of {successful} processed items from queue")
                    except Exception as e:
                        logger.error(f"Error removing processed items from queue: {e}")
                
                # Print stats periodically
                if self.stats["processed"] % 100 == 0 and self.stats["processed"] > 0:
                    self.print_stats()
                    
            except ConnectionError:
                logger.error("Redis connection error. Retrying...")
                time.sleep(5)
            except Exception as e:
                logger.error(f"Error in consumer loop: {e}")
                time.sleep(1)
    
    def print_stats(self):
        """Print processing statistics"""
        with self.stats_lock:
            elapsed = time.time() - self.stats["start_time"]
            logger.info("\n--- Trap Consumer Stats ---")
            logger.info(f"Processed: {self.stats['processed']} traps")
            logger.info(f"Errors: {self.stats['errors']}")
            logger.info(f"Running for: {elapsed:.1f} seconds")
            logger.info(f"Processing rate: {self.stats['processing_rate']:.2f} traps/second")
            
            # Safely get queue info
            try:
                queue_length = redis_manager.redis.zcard(QUEUE_NAME)
                logger.info(f"Queue length: {queue_length}")
                
                # Get a sample of recent items for diagnostic purposes
                if queue_length > 0:
                    sample_items = redis_manager.redis.zrange(QUEUE_NAME, -5, -1, withscores=True)
                    if sample_items:
                        logger.info(f"Recent items in queue: {len(sample_items)}")
                        for item, score in sample_items:
                            item_time = datetime.datetime.fromtimestamp(score)
                            logger.debug(f"Item from {item_time}: {item[:50]}...")
            except Exception as e:
                logger.error(f"Error getting queue info: {e}")
                
            logger.info("---------------------------\n")

if __name__ == "__main__":
    processor = TrapProcessor()
    try:
        processor.run_consumer()
    except KeyboardInterrupt:
        logger.info("Consumer stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error in trap consumer: {e}")
        raise