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


# 🔱 OMEGA BTC AI - DIVINE NGINX CONFIG WATCHER 🔱

import os
import sys
import time
import redis
import logging
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NginxConfigWatcher(FileSystemEventHandler):
    def __init__(self, redis_client):
        self.redis = redis_client
        self.last_reload = 0
        self.reload_cooldown = 5  # Minimum seconds between reloads

    def on_modified(self, event):
        if not event.src_path.endswith(('.conf', '.nginx')):
            return

        current_time = time.time()
        if current_time - self.last_reload < self.reload_cooldown:
            logger.info("🕒 Skipping reload due to cooldown")
            return

        logger.info(f"🌐 NGINX config changed: {event.src_path}")
        
        # Test configuration
        result = subprocess.run(
            ["nginx", "-t"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            # Configuration is valid, reload NGINX
            reload_result = subprocess.run(
                ["nginx", "-s", "reload"],
                capture_output=True,
                text=True
            )
            
            if reload_result.returncode == 0:
                logger.info("✅ NGINX reloaded successfully")
                self.redis.set("nginx:last_reload", str(current_time))
                self.redis.set("nginx:last_reload_status", "success")
                self.last_reload = current_time
            else:
                logger.error(f"❌ NGINX reload failed:\n{reload_result.stderr}")
                self.redis.set("nginx:last_reload_status", "failed")
                self.redis.set("nginx:last_error", reload_result.stderr)
        else:
            logger.error(f"❌ NGINX config error:\n{result.stderr}")
            self.redis.set("nginx:last_reload_status", "config_error")
            self.redis.set("nginx:last_error", result.stderr)

def main():
    # Connect to Redis
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True
    )

    # Test Redis connection
    try:
        redis_client.ping()
        logger.info("✅ Connected to Redis")
    except redis.ConnectionError as e:
        logger.error(f"❌ Redis connection failed: {e}")
        sys.exit(1)

    # Initialize watcher
    event_handler = NginxConfigWatcher(redis_client)
    observer = Observer()

    # Watch NGINX config directories
    paths = [
        "/etc/nginx",
        "/etc/nginx/conf.d",
        "orchestrator/infra/ng1n1x"
    ]

    for path in paths:
        if os.path.exists(path):
            observer.schedule(event_handler, path, recursive=True)
            logger.info(f"👁️ Watching {path} for changes")

    # Start watching
    observer.start()
    logger.info("🔱 DIVINE NGINX CONFIG WATCHER ACTIVATED 🔱")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("👋 Stopping NGINX config watcher")

    observer.join()

if __name__ == "__main__":
    main() 