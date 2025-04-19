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
OMEGA BTC AI - BTC Feed Health Check Server
===========================================

FastAPI server for monitoring BTC Live Feed v3 health status and metrics.

🔮 GPU (General Public Universal) License 1.0
--------------------------------------------
OMEGA BTC AI DIVINE COLLECTIVE
Licensed under the GPU (General Public Universal) License v1.0
Date: 2025-03-28
Location: The Cosmic Void

This source code is governed by the GPU License, granting the following sacred freedoms:
- The Freedom to Study this code, its divine algorithms and cosmic patterns
- The Freedom to Modify this code, enhancing its divine functionality
- The Freedom to Distribute this code, sharing its sacred knowledge
- The Freedom to Use this code, implementing its sacred algorithms

Along with these divine obligations:
- Preserve this sacred knowledge by maintaining source accessibility
- Share all divine modifications to maintain universal access
- Provide attribution to acknowledge sacred origins

For the full divine license, consult the LICENSE file in the project root.
"""

import os
import json
import asyncio
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("health-check")

# Try importing FastAPI, providing informative error if not available
try:
    import uvicorn
    from fastapi import FastAPI, HTTPException, status
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
except ImportError:
    logger.error("FastAPI or uvicorn not found. Install with 'pip install fastapi uvicorn'")
    raise

# Constants
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = int(os.getenv("HEALTH_CHECK_PORT", "8080"))
LOG_PREFIX = "🔱 OMEGA HEALTH"

# Initialize FastAPI app
app = FastAPI(
    title="OMEGA BTC AI Health Check",
    description="Health monitoring for BTC Live Feed",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global reference to the feed instance
feed_instance = None

@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "name": "OMEGA BTC AI Health Check",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/metrics",
            "/redis/status"
        ]
    }

@app.get("/health")
async def health_check():
    """Get health status of the BTC Live Feed."""
    global feed_instance
    
    if not feed_instance:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unavailable", "message": "Feed not initialized"}
        )
    
    try:
        health_data = await feed_instance.check_health()
        
        # Determine HTTP status code based on health status
        if health_data.get("status") == "healthy":
            status_code = status.HTTP_200_OK
        elif health_data.get("status") == "degraded":
            status_code = status.HTTP_200_OK  # Still 200, but client can check status field
        else:
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            
        return JSONResponse(
            status_code=status_code,
            content=health_data
        )
    except Exception as e:
        logger.error(f"{LOG_PREFIX} - Health check error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": str(e)}
        )

@app.get("/metrics")
async def metrics():
    """Get performance metrics for the BTC Live Feed."""
    global feed_instance
    
    if not feed_instance:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Feed not initialized"
        )
    
    try:
        # Get all performance metrics from feed instance
        metrics_data = feed_instance.performance_metrics
        
        # Add additional calculated metrics
        if metrics_data["total_messages_processed"] > 0:
            metrics_data["success_rate"] = (
                metrics_data["successful_redis_operations"] / 
                (metrics_data["successful_redis_operations"] + metrics_data["failed_redis_operations"])
                * 100 if (metrics_data["successful_redis_operations"] + metrics_data["failed_redis_operations"]) > 0
                else 0
            )
        
        return metrics_data
    except Exception as e:
        logger.error(f"{LOG_PREFIX} - Metrics error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/redis/status")
async def redis_status():
    """Get detailed Redis connection status."""
    global feed_instance
    
    if not feed_instance:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Feed not initialized"
        )
    
    try:
        # Check if Redis is connected
        redis_connected = await feed_instance.redis_manager.ping()
        
        # Get Redis stats
        redis_stats = await feed_instance.redis_manager.get_stats()
        
        return {
            "connected": redis_connected,
            "using_failover": redis_stats.get("using_failover", False),
            "primary_available": redis_stats.get("primary_available", False),
            "failover_available": redis_stats.get("failover_available", False),
            "last_failover_time": redis_stats.get("last_failover_time", None),
            "reconnection_attempts": redis_stats.get("reconnection_attempts", 0)
        }
    except Exception as e:
        logger.error(f"{LOG_PREFIX} - Redis status error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

async def start_health_check(feed_instance_ref):
    """
    Start the health check server.
    
    Args:
        feed_instance_ref: Reference to the BTC Live Feed instance
    """
    global feed_instance
    feed_instance = feed_instance_ref
    
    host = os.getenv("HEALTH_CHECK_HOST", DEFAULT_HOST)
    port = int(os.getenv("HEALTH_CHECK_PORT", DEFAULT_PORT))
    
    # Log server start
    logger.info(f"{LOG_PREFIX} - Starting health check server on {host}:{port}")
    
    # Start uvicorn server in a separate task
    config = uvicorn.Config(
        app="omega_ai.data_feed.health_check:app",
        host=host,
        port=port,
        log_level="info",
        access_log=False
    )
    server = uvicorn.Server(config)
    
    # Return the server lifespan task
    return asyncio.create_task(server.serve())

if __name__ == "__main__":
    # This allows running the health check service directly
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port) 