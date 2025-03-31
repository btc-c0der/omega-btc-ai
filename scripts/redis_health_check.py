#!/usr/bin/env python3

# 🔱 OMEGA BTC AI - DIVINE REDIS HEALTH CHECK 🔱

import os
import sys
import time
import redis
import logging
import subprocess
from prometheus_client import start_http_server, Gauge, Counter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Divine Prometheus Metrics
redis_health = Gauge('redis_health', 'Redis health status (1=healthy, 0=unhealthy)')
redis_latency = Gauge('redis_latency_seconds', 'Redis operation latency in seconds')
redis_errors = Counter('redis_errors_total', 'Total number of Redis errors')
redis_uptime = Gauge('redis_uptime_seconds', 'Redis server uptime in seconds')

def check_redis_health():
    try:
        # Connect to Redis
        r = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            password=os.getenv('REDIS_PASSWORD', 'divine_omega_redis_password'),
            socket_timeout=5,
            socket_connect_timeout=5
        )

        # Test connection and basic operations
        start_time = time.time()
        r.ping()
        r.set('health_check', 'divine')
        r.get('health_check')
        r.delete('health_check')
        latency = time.time() - start_time

        # Get Redis info
        info = r.info()
        
        # Update metrics
        redis_health.set(1)
        redis_latency.set(latency)
        redis_uptime.set(info['uptime_in_seconds'])

        logger.info(f"✅ Redis health check passed - Latency: {latency:.3f}s")
        return True

    except redis.ConnectionError as e:
        logger.error(f"❌ Redis connection error: {e}")
        redis_health.set(0)
        redis_errors.inc()
        return False
    except redis.RedisError as e:
        logger.error(f"❌ Redis operation error: {e}")
        redis_health.set(0)
        redis_errors.inc()
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        redis_health.set(0)
        redis_errors.inc()
        return False

def main():
    # Start Prometheus metrics server
    port = int(os.getenv('METRICS_PORT', 9121))
    start_http_server(port)
    logger.info(f"🔱 Divine Redis Health Check metrics server started on port {port}")

    # Main health check loop
    while True:
        check_redis_health()
        time.sleep(15)  # Check every 15 seconds

if __name__ == "__main__":
    main() 