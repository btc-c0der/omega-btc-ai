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

# Import Redis manager based on environment
try:
    from omega_ai.utils.redis_manager import RedisManager
except ImportError:
    # Fallback to local implementation
    from .redis_manager import RedisManager

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
redis_manager = None

# Initialize Redis manager
def get_redis_manager():
    global redis_manager
    if redis_manager is None:
        # Get environment variables with fallbacks
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", "6379"))
        redis_password = os.getenv("REDIS_PASSWORD", None)
        redis_ssl = os.getenv("REDIS_SSL", "false").lower() == "true"
        
        # Initialize Redis manager
        redis_manager = RedisManager(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            ssl=redis_ssl
        )
    
    return redis_manager

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint that verifies:
    - Redis connection
    - WebSocket connection status
    - Last price update time
    """
    try:
        # Get Redis manager
        redis = get_redis_manager()
        redis_connected = False
        websocket_connected = False
        last_price_update = None
        details = {}
        
        # Check Redis connection
        try:
            await redis.ping()
            redis_connected = True
            
            # Check last price update time
            last_update_time = await redis.get_cached("last_btc_update_time")
            if last_update_time:
                last_update_time = float(last_update_time)
                last_price_update = datetime.fromtimestamp(last_update_time, tz=timezone.utc).isoformat()
                
                # Get current time and calculate time since last update
                current_time = time.time()
                time_since_update = current_time - last_update_time
                
                # Check WebSocket connection status based on last update time
                websocket_connected = time_since_update < HEALTHY_TIMEOUT
                details["seconds_since_update"] = time_since_update
                
                # Get last price
                last_price = await redis.get_cached("last_btc_price")
                if last_price:
                    details["last_price"] = float(last_price)
            else:
                details["warning"] = "No price updates recorded yet"
        except Exception as e:
            details["redis_error"] = str(e)
        
        # Calculate uptime
        uptime = time.time() - start_time
        details["uptime_seconds"] = uptime
        
        # Determine overall status
        if redis_connected and websocket_connected:
            status = "healthy"
        elif redis_connected and last_price_update and time.time() - float(last_update_time) < DEGRADED_TIMEOUT:
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

if __name__ == "__main__":
    # This allows running the health check service directly
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port) 