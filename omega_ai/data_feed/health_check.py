"""
OMEGA BTC AI - Health Check Module for BTC Live Feed v2
======================================================

Provides health check endpoints for monitoring the BTC Live Feed service.
"""

import os
import time
import json
import asyncio
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, Optional

# Global Redis manager - we'll use the one from btc_live_feed_v2 later
redis_manager = None

# Constants
HEALTHY_TIMEOUT = 60  # Maximum seconds since last update to consider service healthy
DEGRADED_TIMEOUT = 300  # Maximum seconds since last update to consider service degraded

# Initialize FastAPI app
app = FastAPI(
    title="OMEGA BTC AI - BTC Live Feed Health Check",
    description="Health monitoring for the BTC Live Feed service",
    version="2.0.0"
)

# Response models
class HealthResponse(BaseModel):
    status: str
    redis_connected: bool
    websocket_connected: bool
    last_price_update: Optional[str]
    uptime: float
    details: Dict[str, Any]

# Global variables
start_time = time.time()
btc_feed_instance = None

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint that verifies:
    - Redis connection
    - WebSocket connection status
    - Last price update time
    """
    try:
        global redis_manager
        redis_connected = False
        websocket_connected = False
        last_price_update = None
        details = {}
        last_update_time = None
        
        # Check Redis connection if we have a manager
        if redis_manager:
            try:
                # We'll use the check_health method from btc_feed_instance
                # which has access to the Redis manager
                if btc_feed_instance:
                    feed_health = await btc_feed_instance.check_health()
                    redis_connected = feed_health.get("redis_connected", False)
                    websocket_connected = feed_health.get("websocket_connected", False)
                    details["feed_status"] = feed_health.get("status", "unknown")
                    last_price = feed_health.get("last_price")
                    if last_price:
                        details["last_price"] = float(last_price)
                    
                    # Get current time and calculate time since last message
                    if "uptime" in feed_health and feed_health["uptime"]:
                        last_update_time = time.time() - feed_health["uptime"]
                        last_price_update = datetime.fromtimestamp(last_update_time, tz=timezone.utc).isoformat()
                        details["seconds_since_update"] = feed_health["uptime"]
            except Exception as e:
                details["redis_error"] = str(e)
        
        # Calculate uptime
        uptime = time.time() - start_time
        details["uptime_seconds"] = uptime
        
        # Determine overall status
        if redis_connected and websocket_connected:
            status = "healthy"
        elif redis_connected and last_update_time and (time.time() - last_update_time) < DEGRADED_TIMEOUT:
            status = "degraded"
        else:
            status = "unhealthy"
            
        # Return health status
        return HealthResponse(
            status=status,
            redis_connected=redis_connected,
            websocket_connected=websocket_connected,
            last_price_update=last_price_update,
            uptime=uptime,
            details=details
        )
        
    except Exception as e:
        # Log the error
        print(f"Health check error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}"
        )

@app.get("/")
async def root():
    """Root endpoint that redirects to health check"""
    return {"message": "OMEGA BTC AI - BTC Live Feed v2", "health_endpoint": "/health"}

async def start_health_check(feed_instance=None):
    """Start the health check server in the background."""
    global btc_feed_instance, redis_manager
    
    btc_feed_instance = feed_instance
    if hasattr(feed_instance, 'redis_manager'):
        redis_manager = feed_instance.redis_manager
    
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)
    
    await server.serve()

if __name__ == "__main__":
    # This allows running the health check service directly
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port) 