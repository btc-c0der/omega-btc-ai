#!/usr/bin/env python3
"""
OMEGA BTC AI - Health Check Script
================================
Monitors the health of all system components and services.

Copyright (c) 2024 OMEGA BTC AI Team
Licensed under MIT License
"""

import os
import sys
import redis
import psycopg2
import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def check_redis():
    """Check Redis connection and data integrity."""
    try:
        redis_host = os.getenv('REDIS_HOST', 'redis')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        
        # Ping Redis
        r.ping()
        logger.info("✅ Redis connection: OK")
        
        # Check essential keys
        essential_keys = ["last_btc_price", "btc_movement_history"]
        for key in essential_keys:
            if not r.exists(key):
                logger.warning(f"⚠️ Missing key: {key}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Redis error: {e}")
        return False

def check_postgres():
    """Check PostgreSQL connection and tables."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB', 'omega_db'),
            user=os.getenv('POSTGRES_USER', 'omega_user'),
            password=os.getenv('POSTGRES_PASSWORD', 'omega_pass'),
            host=os.getenv('POSTGRES_HOST', 'postgres'),
            port=os.getenv('POSTGRES_PORT', '5432')
        )
        cur = conn.cursor()
        
        # Check tables
        tables = ['btc_prices', 'subtle_movements']
        for table in tables:
            cur.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}')")
            if not cur.fetchone()[0]:
                logger.warning(f"⚠️ Missing table: {table}")
        
        cur.close()
        conn.close()
        logger.info("✅ PostgreSQL connection: OK")
        return True
    except Exception as e:
        logger.error(f"❌ PostgreSQL error: {e}")
        return False

def check_api_endpoints():
    """Check if API endpoints are responding."""
    try:
        endpoints = [
            "http://localhost:8050/",
            "http://localhost:8050/api/metrics",
            "http://localhost:8050/api/traps"
        ]
        
        for endpoint in endpoints:
            response = requests.get(endpoint)
            if response.status_code == 200:
                logger.info(f"✅ Endpoint {endpoint}: OK")
            else:
                logger.warning(f"⚠️ Endpoint {endpoint} returned {response.status_code}")
        
        return True
    except Exception as e:
        logger.error(f"❌ API error: {e}")
        return False

def check_disk_space():
    """Check available disk space."""
    try:
        # Check space in important directories
        dirs = ['/app/logs', '/app/data', '/app/redis_data', '/app/postgres_data']
        for d in dirs:
            if os.path.exists(d):
                total, used, free = os.statvfs(d).f_blocks, os.statvfs(d).f_bfree, os.statvfs(d).f_bavail
                free_percent = (free / total) * 100
                if free_percent < 20:
                    logger.warning(f"⚠️ Low disk space in {d}: {free_percent:.1f}% free")
                else:
                    logger.info(f"✅ Disk space {d}: {free_percent:.1f}% free")
        
        return True
    except Exception as e:
        logger.error(f"❌ Disk space check error: {e}")
        return False

def main():
    """Run all health checks."""
    print("\n🔱 OMEGA BTC AI - System Health Check")
    print("=====================================")
    
    checks = [
        ("Redis", check_redis),
        ("PostgreSQL", check_postgres),
        ("API Endpoints", check_api_endpoints),
        ("Disk Space", check_disk_space)
    ]
    
    all_passed = True
    for name, check in checks:
        print(f"\nChecking {name}...")
        if not check():
            all_passed = False
    
    if all_passed:
        print("\n✅ All systems operational")
        return 0
    else:
        print("\n⚠️ Some checks failed")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 