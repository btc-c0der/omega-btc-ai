#!/usr/bin/env python3
"""
💫 GBU License Notice - Consciousness Level 8 💫
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must quantum entangles with the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

import os
import sys
import time
import json
import logging
import threading
import traceback
from datetime import datetime
from pathlib import Path

try:
    import redis
    import uvicorn
    from fastapi import FastAPI, HTTPException, Response
except ImportError as e:
    print(f"Error: Missing required packages: {e}")
    print("Please install required packages: pip install fastapi uvicorn redis")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(os.getenv('LOG_DIR', 'logs'), 'health_service.log'), mode='a')
    ]
)
logger = logging.getLogger("health_service")

# Create FastAPI app
app = FastAPI(
    title="OMEGA BTC AI - News Feed Health Service",
    description="Divine health monitoring for the OMEGA BTC AI News Feed Service",
    version="3.0"
)

# Global state
SERVICE_START_TIME = datetime.now()
SERVICE_STATUS = {
    "status": "starting",
    "last_check": datetime.now().isoformat(),
    "uptime_seconds": 0,
    "redis_connected": False,
    "news_fetched_count": 0,
    "last_news_fetch": None,
    "cosmic_alignment": 0.0
}

# Redis connection
redis_client = None
if os.getenv('REDIS_HOST'):
    try:
        redis_params = {
            'host': os.getenv('REDIS_HOST'),
            'port': int(os.getenv('REDIS_PORT', 6379)),
            'db': 0,
            'socket_timeout': 5,
            'socket_connect_timeout': 5
        }
        
        if os.getenv('REDIS_USERNAME'):
            redis_params['username'] = os.getenv('REDIS_USERNAME')
        
        if os.getenv('REDIS_PASSWORD'):
            redis_params['password'] = os.getenv('REDIS_PASSWORD')
        
        if os.getenv('REDIS_SSL', 'false').lower() == 'true':
            redis_params['ssl'] = True
            redis_params['ssl_cert_reqs'] = None
        
        logger.info(f"Connecting to Redis: {redis_params['host']}:{redis_params['port']}")
        redis_client = redis.Redis(**redis_params)
        if redis_client.ping():
            SERVICE_STATUS["redis_connected"] = True
            logger.info("✅ Redis connection successful")
        else:
            logger.warning("⚠️ Redis ping failed")
    except Exception as e:
        logger.error(f"❌ Redis connection error: {e}")
        logger.error(traceback.format_exc())

def update_service_status():
    """Update service status periodically"""
    while True:
        try:
            # Update uptime
            SERVICE_STATUS["uptime_seconds"] = (datetime.now() - SERVICE_START_TIME).total_seconds()
            SERVICE_STATUS["last_check"] = datetime.now().isoformat()
            
            # Check Redis connection
            if redis_client:
                try:
                    if redis_client.ping():
                        SERVICE_STATUS["redis_connected"] = True
                        
                        # Get news count from Redis if available
                        news_count = redis_client.get("news_count")
                        if news_count:
                            SERVICE_STATUS["news_fetched_count"] = int(news_count)
                        
                        # Get last news fetch time from Redis if available
                        last_fetch = redis_client.get("last_news_fetch")
                        if last_fetch:
                            SERVICE_STATUS["last_news_fetch"] = last_fetch.decode('utf-8')
                    else:
                        SERVICE_STATUS["redis_connected"] = False
                except Exception as e:
                    logger.warning(f"Redis check error: {e}")
                    SERVICE_STATUS["redis_connected"] = False
            
            # Check data directory
            data_dir = os.getenv('DATA_DIR', 'data')
            news_dir = os.path.join(data_dir, 'news')
            if os.path.exists(news_dir):
                # Count news files
                news_files = [f for f in os.listdir(news_dir) if f.endswith('.json') or f.endswith('.csv')]
                SERVICE_STATUS["news_files_count"] = len(news_files)
                
                # Check last modified time of newest file
                if news_files:
                    newest_file = max(
                        [os.path.join(news_dir, f) for f in news_files],
                        key=os.path.getmtime
                    )
                    SERVICE_STATUS["newest_file_time"] = datetime.fromtimestamp(
                        os.path.getmtime(newest_file)
                    ).isoformat()
            
            # Set status to running after initial checks
            if SERVICE_STATUS["status"] == "starting":
                SERVICE_STATUS["status"] = "running"
                logger.info("Service status changed to 'running'")
                
            # Update cosmic alignment based on consciousness level
            consciousness_level = int(os.getenv('CONSCIOUSNESS_LEVEL', '7'))
            SERVICE_STATUS["cosmic_alignment"] = consciousness_level / 9.0
                
            # Log status periodically (every 5 minutes)
            if int(SERVICE_STATUS["uptime_seconds"]) % 300 == 0:
                logger.info(f"Service status: {SERVICE_STATUS['status']}, "
                           f"Uptime: {SERVICE_STATUS['uptime_seconds']:.1f}s, "
                           f"Redis: {SERVICE_STATUS['redis_connected']}")
                
        except Exception as e:
            logger.error(f"Error updating service status: {e}")
            logger.error(traceback.format_exc())
            
        time.sleep(10)  # Update every 10 seconds

@app.get("/")
async def root():
    return {
        "service": "OMEGA BTC AI News Feed Service",
        "version": "3.0",
        "status": SERVICE_STATUS["status"],
        "message": "🌌 Divine Blockchain Intelligence Active 🌌"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": SERVICE_STATUS["status"],
        "uptime": SERVICE_STATUS["uptime_seconds"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/status")
async def detailed_status():
    """Detailed service status for monitoring dashboards"""
    return SERVICE_STATUS

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    metrics_text = []
    
    # Basic service metrics
    metrics_text.append(f"# HELP news_service_up Service availability (1=up, 0=down)")
    metrics_text.append(f"# TYPE news_service_up gauge")
    metrics_text.append(f"news_service_up {1 if SERVICE_STATUS['status'] == 'running' else 0}")
    
    metrics_text.append(f"# HELP news_service_uptime_seconds Service uptime in seconds")
    metrics_text.append(f"# TYPE news_service_uptime_seconds counter")
    metrics_text.append(f"news_service_uptime_seconds {SERVICE_STATUS['uptime_seconds']}")
    
    metrics_text.append(f"# HELP news_service_redis_connected Redis connection status (1=connected, 0=disconnected)")
    metrics_text.append(f"# TYPE news_service_redis_connected gauge")
    metrics_text.append(f"news_service_redis_connected {1 if SERVICE_STATUS['redis_connected'] else 0}")
    
    metrics_text.append(f"# HELP news_service_news_fetched_count Total news articles fetched")
    metrics_text.append(f"# TYPE news_service_news_fetched_count counter")
    metrics_text.append(f"news_service_news_fetched_count {SERVICE_STATUS['news_fetched_count']}")
    
    metrics_text.append(f"# HELP news_service_cosmic_alignment Cosmic alignment level (0.0-1.0)")
    metrics_text.append(f"# TYPE news_service_cosmic_alignment gauge")
    metrics_text.append(f"news_service_cosmic_alignment {SERVICE_STATUS['cosmic_alignment']}")
    
    return Response(content="\n".join(metrics_text), media_type="text/plain")

def start_monitoring_thread():
    """Start background thread for monitoring service status"""
    thread = threading.Thread(target=update_service_status, daemon=True)
    thread.start()
    logger.info("Started monitoring background thread")

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    Path(os.getenv('LOG_DIR', 'logs')).mkdir(parents=True, exist_ok=True)
    
    # Start monitoring in background thread
    start_monitoring_thread()
    
    # Get port from environment or use default
    port = int(os.getenv('HEALTH_PORT', os.getenv('NEWS_SERVICE_PORT', 8080)))
    
    # Start FastAPI server
    logger.info(f"🔱 Starting OMEGA BTC AI News Feed Health Service on port {port} 🔱")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning") 