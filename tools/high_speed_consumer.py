#!/usr/bin/env python3

"""
High-Performance Queue Consumer
Rapidly processes items from mm_trap_queue:zset to clear the backlog
"""

import redis
import json
import time
import threading
import psutil
import argparse

# Redis connection
r = redis.Redis(
    host='localhost', 
    port=6379,
    db=0,
    socket_keepalive=True,
    socket_timeout=5,
    health_check_interval=10
)

class HighSpeedConsumer:
    def __init__(self, queue_name, worker_count=4, batch_size=1000):
        self.queue_name = queue_name
        self.worker_count = worker_count
        self.batch_size = batch_size
        self.processed = 0
        self.running = True
        self.lock = threading.Lock()
        self.start_time = time.time()
        
    def worker(self, worker_id):
        """Worker thread to process queue items"""
        local_processed = 0
        redis_conn = redis.Redis(host='localhost', port=6379, db=0)
        
        while self.running:
            # Get a batch of items with their scores
            items = redis_conn.zrange(
                self.queue_name, 
                0, 
                self.batch_size - 1, 
                withscores=True
            )
            
            if not items:
                time.sleep(0.05)
                continue
            
            # Process items (minimal processing for speed)
            item_scores = {}
            for item, score in items:
                try:
                    # Just decode the item to verify it can be processed
                    _ = json.loads(item) if isinstance(item, bytes) else item
                    item_scores[item] = score
                    local_processed += 1
                except:
                    # Skip invalid items
                    pass
            
            # Remove processed items
            if item_scores:
                redis_conn.zrem(self.queue_name, *item_scores.keys())
            
            # Update processed count
            with self.lock:
                self.processed += len(item_scores)
                
            # Small pause to prevent CPU overload
            time.sleep(0.001)
    
    def monitor(self):
        """Monitor thread to display progress"""
        queue_size_start = r.zcard(self.queue_name)
        last_processed = 0
        last_time = time.time()
        
        while self.running:
            current_queue_size = r.zcard(self.queue_name)
            current_time = time.time()
            elapsed = current_time - self.start_time
            
            with self.lock:
                total_processed = self.processed
            
            # Calculate processing rate
            time_diff = current_time - last_time
            items_diff = total_processed - last_processed
            rate_per_sec = items_diff / time_diff if time_diff > 0 else 0
            
            # Calculate estimated completion time
            remaining = current_queue_size
            eta_seconds = remaining / rate_per_sec if rate_per_sec > 0 else 0
            eta_str = f"{int(eta_seconds/60)}m {int(eta_seconds%60)}s" if eta_seconds > 0 else "unknown"
            
            # Get system stats
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            
            # Print progress
            print(f"\033[2J\033[H", end="")  # Clear screen
            print(f"Queue Processor - {self.queue_name}")
            print(f"Workers: {self.worker_count}, Batch Size: {self.batch_size}")
            print(f"System: CPU {cpu}%, Memory {mem}%")
            print("-" * 50)
            print(f"Initial Queue Size: {queue_size_start:,}")
            print(f"Current Queue Size: {current_queue_size:,}")
            print(f"Processed: {total_processed:,} items")
            print(f"Elapsed: {int(elapsed/60)}m {int(elapsed%60)}s")
            print(f"Processing Rate: {rate_per_sec:.1f} items/second")
            print(f"ETA: {eta_str}")
            print("-" * 50)
            print("Press Ctrl+C to stop processing")
            
            # Update reference values
            last_processed = total_processed
            last_time = current_time
            
            # Don't update too frequently
            time.sleep(1)
    
    def run(self):
        """Start workers and monitor"""
        print(f"Starting high-speed consumer for {self.queue_name}")
        print(f"Initial queue size: {r.zcard(self.queue_name):,}")
        
        # Start worker threads
        threads = []
        for i in range(self.worker_count):
            t = threading.Thread(target=self.worker, args=(i,))
            t.daemon = True
            t.start()
            threads.append(t)
            
        # Start monitor thread
        monitor_thread = threading.Thread(target=self.monitor)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        try:
            # Wait for worker threads to finish
            for t in threads:
                t.join()
        except KeyboardInterrupt:
            print("\nShutting down workers...")
            self.running = False
            time.sleep(1)
            print(f"Processed {self.processed:,} items before stopping")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='High-Speed Queue Consumer')
    parser.add_argument('--queue', default='rq:queue:mm_trap_queue:zset',
                        help='Queue name to process')
    parser.add_argument('--workers', type=int, default=4,
                        help='Number of worker threads')
    parser.add_argument('--batch', type=int, default=1000,
                        help='Batch size for each processing cycle')
    
    args = parser.parse_args()
    
    consumer = HighSpeedConsumer(
        queue_name=args.queue,
        worker_count=args.workers,
        batch_size=args.batch
    )
    consumer.run()