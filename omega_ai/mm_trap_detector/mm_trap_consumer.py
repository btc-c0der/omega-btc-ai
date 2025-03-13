#!/usr/bin/env python3

"""
Market Maker Trap Queue Consumer
Efficiently processes the mm_trap_queue with sorted sets
"""

import redis
import json
import time
import signal
import datetime
import threading
from redis.exceptions import ConnectionError
from omega_ai.utils.redis_connection import RedisConnectionManager

# Initialize Redis connection manager
redis_manager = RedisConnectionManager()

# Configuration
QUEUE_NAME = "mm_trap_queue:zset"  # Using the new sorted set queue
BATCH_SIZE = 50
SLEEP_WHEN_EMPTY = 0.1  # seconds
PROCESSING_TIMEOUT = 60  # seconds

# Control flag for graceful shutdown
running = True

def signal_handler(sig, frame):
    """Handle termination signals for graceful shutdown"""
    global running
    print("Shutdown signal received, finishing current batch...")
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
            if isinstance(trap_data, str) and trap_data.startswith('{'):
                trap_data = json.loads(trap_data)
            
            # Extract trap details
            trap_type = trap_data.get('type', 'Unknown')
            confidence = trap_data.get('confidence', 0)
            price = trap_data.get('price', 0)
            
            # Process trap based on confidence
            if confidence > 0.8:
                # High confidence trap - log to database
                print(f"⚠️ HIGH CONFIDENCE TRAP: {trap_type} at ${price} ({confidence:.2f})")
                # Here you would call your database code to store the trap
                # from omega_ai.db_manager.database import log_mm_trap
                # log_mm_trap(trap_type, price, confidence)
            else:
                # Low confidence trap - just log
                print(f"ℹ️ Low confidence trap: {trap_type} ({confidence:.2f})")
            
            return True
        except Exception as e:
            print(f"Error processing trap: {e}")
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
        print(f"Starting trap consumer for {QUEUE_NAME}")
        empty_count = 0
        
        while running:
            try:
                # Get items from sorted set with scores
                # ZRANGE returns newest items first with REV
                items = redis_manager.client.zrange(QUEUE_NAME, 0, BATCH_SIZE-1)
                
                if not items:
                    empty_count += 1
                    if empty_count % 100 == 0:
                        print(f"Queue empty for {empty_count} checks")
                    time.sleep(SLEEP_WHEN_EMPTY)
                    continue
                
                # Reset empty counter
                empty_count = 0
                
                # Process this batch
                successful, errors = self.process_batch(items)
                
                # Remove processed items from the queue
                if successful > 0:
                    # Get the highest score we've processed
                    scores = redis_manager.client.zmscore(QUEUE_NAME, items[:successful])
                    if scores:
                        max_score = max(scores)
                        # Remove all items with scores up to max_score
                        redis_manager.client.zremrangebyscore(QUEUE_NAME, '-inf', max_score)
                
                # Print stats periodically
                if self.stats["processed"] % 500 == 0 and self.stats["processed"] > 0:
                    self.print_stats()
                    
            except ConnectionError:
                print("Redis connection error. Retrying...")
                time.sleep(5)
            except Exception as e:
                print(f"Error in consumer loop: {e}")
                time.sleep(1)
    
    def print_stats(self):
        """Print processing statistics"""
        with self.stats_lock:
            elapsed = time.time() - self.stats["start_time"]
            print("\n--- Trap Consumer Stats ---")
            print(f"Processed: {self.stats['processed']} traps")
            print(f"Errors: {self.stats['errors']}")
            print(f"Running for: {elapsed:.1f} seconds")
            print(f"Processing rate: {self.stats['processing_rate']:.2f} traps/second")
            print(f"Queue length: {redis_manager.client.zcard(QUEUE_NAME)}")
            print("---------------------------\n")

if __name__ == "__main__":
    processor = TrapProcessor()
    processor.run_consumer()