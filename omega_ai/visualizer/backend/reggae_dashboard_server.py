#!/usr/bin/env python3

"""
OMEGA BTC AI - Reggae Hacker Omega UI Dashboard Server
======================================================

A real-time dashboard server that provides trap probability and trading position data
via WebSockets with a Reggae Hacker aesthetic.
"""

import asyncio
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Set

import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import redis
import uvicorn
from pathlib import Path
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("reggae_dashboard")

class ReggaeDashboardServer:
    """
    Server for the Reggae Hacker Omega UI Dashboard that provides real-time
    trading position and trap probability data.
    """
    
    def __init__(self):
        """Initialize the dashboard server with WebSocket support."""
        self.app = FastAPI(title="OMEGA BTC AI - Reggae Hacker Dashboard")
        
        # Active WebSocket connections
        self.active_connections: Set[WebSocket] = set()
        
        # Redis client for data access
        self.redis_client = self._init_redis_client()
        
        # CORS middleware for frontend connections
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # In production, replace with specific origins
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Set up routes
        self.setup_routes()
        
        # Background task for sending updates
        self.update_task = None
    
    def _init_redis_client(self) -> Optional[redis.Redis]:
        """Initialize Redis client using environment variables."""
        try:
            redis_host = os.environ.get("REDIS_HOST", "localhost")
            redis_port = int(os.environ.get("REDIS_PORT", 6379))
            
            # Create client without password
            client = redis.Redis(
                host=redis_host,
                port=redis_port,
                decode_responses=True
            )
            # Test connection
            client.ping()
            logger.info(f"Connected to Redis at {redis_host}:{redis_port}")
            return client
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            return None

    def setup_routes(self):
        """Set up API routes and WebSocket endpoint."""
        
        @self.app.get("/api/health")
        async def health_check():
            """Health check endpoint."""
            redis_status = "disconnected"
            
            # Try to connect to Redis directly
            try:
                # Create a new Redis client for testing
                r = redis.Redis(
                    host="localhost",
                    port=6379,
                    decode_responses=True
                )
                # Get trap probability data
                test_data = r.get("current_trap_probability")
                if test_data:
                    redis_status = "connected"
                    logger.info("Redis connection test successful")
                else:
                    if r.ping():
                        redis_status = "connected"
                        logger.info("Redis ping successful but no data found")
            except Exception as e:
                logger.error(f"Redis health check failed: {e}")
            
            return {
                "status": "healthy",
                "redis": redis_status,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        @self.app.get("/api/trap-probability")
        async def get_trap_probability():
            """Get the current trap probability data."""
            data = self._get_trap_probability()
            return data
        
        @self.app.get("/api/position")
        async def get_position():
            """Get the current trading position data."""
            data = self._get_position_data()
            return data
        
        @self.app.get("/api/redis-keys")
        async def get_redis_keys():
            """Get a list of recently updated Redis keys."""
            try:
                if not self.redis_client:
                    return {"error": "Redis not connected"}
                
                # Get recently updated keys
                recent_keys = []
                for key in self.redis_client.keys("*"):
                    try:
                        # Get key type and add some metadata
                        key_type = self.redis_client.type(key)
                        key_info = {
                            "key": key,
                            "type": key_type,
                        }
                        
                        # Add additional info based on type
                        if key_type == "string":
                            # Get string length
                            key_info["length"] = len(self.redis_client.get(key) or "")
                        elif key_type == "list":
                            # Get list length
                            key_info["length"] = self.redis_client.llen(key)
                        elif key_type == "hash":
                            # Get hash field count
                            key_info["fields"] = len(self.redis_client.hkeys(key))
                        
                        recent_keys.append(key_info)
                    except Exception as e:
                        logger.error(f"Error processing Redis key {key}: {e}")
                
                # Sort by key name
                recent_keys.sort(key=lambda x: x["key"])
                
                return {"keys": recent_keys[:100]}  # Limit to 100 keys
            except Exception as e:
                logger.error(f"Error getting Redis keys: {e}")
                return {"error": str(e)}
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time dashboard updates."""
            await websocket.accept()
            self.active_connections.add(websocket)
            try:
                while True:
                    # Wait for any message (ping)
                    msg = await websocket.receive_text()
                    if msg == "ping":
                        await websocket.send_text("pong")
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                self.active_connections.remove(websocket)
    
    def _get_trap_probability(self):
        """Get the current trap probability from Redis."""
        try:
            # Create a new Redis client for testing
            r = redis.Redis(
                host="localhost",
                port=6379,
                decode_responses=True
            )
            
            # Get trap probability data
            trap_json = r.get("current_trap_probability")
            if trap_json:
                # Parse JSON
                trap_data = json.loads(trap_json)
                return trap_data
        except Exception as e:
            logger.error(f"Error getting trap probability: {e}")
            
        # Return default data if Redis is not available
        jah_message = self._generate_jah_message(0.5)
        return {
            "probability": 0.5,
            "trap_type": "unknown",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": jah_message
        }

    def _get_position_data(self):
        """Get the current position data from Redis."""
        try:
            # Create a new Redis client for testing
            r = redis.Redis(
                host="localhost",
                port=6379,
                decode_responses=True
            )
            
            # Get position data
            position_json = r.get("current_position")
            if position_json:
                # Parse JSON
                position_data = json.loads(position_json)
                return position_data
        except Exception as e:
            logger.error(f"Error getting position data: {e}")
            
        # Return default data if Redis is not available
        return {
            "has_position": False,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def _generate_jah_message(self, data):
        """Generate a JAH message based on trap probability."""
        # Extract probability from data
        if isinstance(data, dict):
            probability = data.get("probability", 0.5)
        else:
            probability = float(data)
            
        # Generate message based on probability
        if probability <= 0.4:
            message = "JAH JAH AWARE! PEACEFUL TRADING WITH CLEAR VISION!"
        elif probability <= 0.6:
            message = "JAH GUIDES THE TRADING PATH! LOOK FOR SIGNS IN THE MARKET RHYTHM!"
        elif probability <= 0.8:
            message = "JAH JAH WARNS OF TRAP VIBRATIONS! STAY CONSCIOUS OF FALSE MOVEMENTS!"
        else:
            message = "HIGH TRAP ENERGY! JAH SYSTEM DETECTS MANIPULATION! USE CAUTION BRETHREN!"
            
        return message
    
    async def broadcast_updates(self):
        """Background task to broadcast real-time updates to all clients."""
        while True:
            try:
                # Skip if no active connections
                if not self.active_connections:
                    await asyncio.sleep(1)
                    continue
                
                # Get the latest data
                trap_data = self._get_trap_probability()
                position_data = self._get_position_data()
                
                # Combine into a single update
                update = {
                    "type": "update",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "trap_probability": trap_data,
                    "position": position_data
                }
                
                # Broadcast to all connected clients
                disconnected = set()
                for websocket in self.active_connections:
                    try:
                        await websocket.send_json(update)
                    except Exception:
                        disconnected.add(websocket)
                
                # Remove disconnected clients
                self.active_connections -= disconnected
                
                # Sleep for a bit
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error in broadcast task: {e}")
                await asyncio.sleep(5)  # Longer sleep on error
    
    async def startup(self):
        """Startup event handler to start the broadcast task."""
        self.update_task = asyncio.create_task(self.broadcast_updates())
        logger.info("Started broadcast task")
    
    async def shutdown(self):
        """Shutdown event handler to clean up resources."""
        if self.update_task:
            self.update_task.cancel()
            try:
                await self.update_task
            except asyncio.CancelledError:
                pass
        logger.info("Stopped broadcast task")

if __name__ == "__main__":
    # Create dashboard server instance
    dashboard = ReggaeDashboardServer()
    
    # Register startup and shutdown events
    dashboard.app.add_event_handler("startup", dashboard.startup)
    dashboard.app.add_event_handler("shutdown", dashboard.shutdown)
    
    # Start the server
    logger.info(f"Starting Reggae Dashboard server on 0.0.0.0:8000")
    
    # Run the app directly
    uvicorn.run(
        "reggae_dashboard_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
else:
    # For imported usage, create the app
    dashboard = ReggaeDashboardServer()
    app = dashboard.app 