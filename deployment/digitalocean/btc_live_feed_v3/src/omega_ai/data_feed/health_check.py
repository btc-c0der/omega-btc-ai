#!/usr/bin/env python3
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
import uvicorn
from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("health-check")

# Constants from environment variables
DEFAULT_HOST = os.getenv("HEALTH_CHECK_DEFAULT_HOST", "0.0.0.0")
DEFAULT_PORT = int(os.getenv("HEALTH_CHECK_PORT", "8080"))
LOG_PREFIX = os.getenv("HEALTH_CHECK_LOG_PREFIX", "🔱 OMEGA HEALTH")

# Initialize FastAPI app with configurable metadata
app = FastAPI(
    title=os.getenv("HEALTH_CHECK_TITLE", "OMEGA BTC AI Health Check"),
    description=os.getenv("HEALTH_CHECK_DESCRIPTION", "Health check API for OMEGA BTC AI Live Feed V3"),
    version=os.getenv("VERSION", "0.3.0"),
)

# Add CORS middleware with configurable settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
    allow_credentials=os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true",
    allow_methods=os.getenv("CORS_ALLOW_METHODS", "GET,POST,OPTIONS").split(","),
    allow_headers=os.getenv("CORS_ALLOW_HEADERS", "*").split(","),
)

# Global reference to the feed instance
feed_instance = None

@app.get("/")
async def root():
    return {
        "status": "alive",
        "service": "OMEGA BTC AI Live Feed v3",
        "message": "Health check API is operational"
    }

@app.get("/health")
async def health():
    """Digital Ocean App Platform compatibility health check endpoint."""
    # This endpoint is required by Digital Ocean for readiness probes
    return {
        "status": "up",
        "message": "Service is healthy"
    }

@app.get("/live")
async def liveness():
    """Kubernetes-style liveness probe."""
    return {
        "status": "live",
        "uptime": "unknown",  # Would be implemented with service start time tracking
        "message": "Service is live"
    }

@app.get("/ready")
async def readiness():
    """Kubernetes-style readiness probe."""
    # Return 200 OK status to indicate service is ready to handle traffic
    return {
        "status": "ready",
        "message": "Service is ready to accept traffic"
    }

@app.get("/ping")
async def ping():
    """Basic ping endpoint that always returns pong."""
    return {"ping": "pong"}

@app.get("/healthz", status_code=200)
async def healthz():
    """
    Standard health check endpoint compatible with most monitoring systems.
    Returns 200 OK when the service is healthy.
    """
    return Response(content="OK", media_type="text/plain")

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

async def start_health_check():
    """Start the health check server."""
    config = {
        "host": DEFAULT_HOST,
        "port": DEFAULT_PORT,
    }
    
    print(f"{LOG_PREFIX} - Starting health check server on {config['host']}:{config['port']}")
    
    server = uvicorn.Server(uvicorn.Config(
        app=app,
        host=config['host'],
        port=config['port'],
        log_level="info",
    ))
    
    await server.serve()

def main():
    """Run the health check server."""
    print(f"{LOG_PREFIX} - Starting health check server on {DEFAULT_HOST}:{DEFAULT_PORT}")
    uvicorn.run(
        app,
        host=DEFAULT_HOST,
        port=DEFAULT_PORT,
        log_level="info",
    )

if __name__ == "__main__":
    main() 