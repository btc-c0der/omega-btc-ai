#!/usr/bin/env python3
"""
Minimal WebSocket server using FastAPI and socket.io
"""

import os
import json
import time
import datetime
import asyncio
import aiohttp
import socketio
import logging
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from omega_ai.data_feed.btc_live_feed_v3 import BtcLiveFeedV3

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
BROADCAST_INTERVAL = int(os.getenv("BROADCAST_INTERVAL", "30"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=False,
    engineio_logger=False
)

# Create FastAPI app
app = FastAPI(title="OMEGA BTC AI WebSocket Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Socket.IO app
socket_app = socketio.ASGIApp(sio)
app.mount("/socket.io", socket_app)

# Initialize price feed
price_feed = BtcLiveFeedV3()

# Cache for price data
price_cache: Dict = {}
last_price_update = datetime.datetime.now() - datetime.timedelta(minutes=10)

# Metrics for health check
metrics = {
    "active_connections": 0,
    "total_connections": 0,
    "failed_price_fetches": 0,
    "last_successful_price_update": None
}

# Create a detailed health endpoint
@app.get("/health")
async def health():
    """Enhanced health check endpoint with detailed metrics"""
    try:
        return {
            "status": "UP",
            "service": "websocket-minimal",
            "timestamp": datetime.datetime.now().isoformat(),
            "price_feed_status": "connected" if price_feed else "disconnected",
            "metrics": {
                "active_connections": metrics["active_connections"],
                "total_connections": metrics["total_connections"],
                "failed_price_fetches": metrics["failed_price_fetches"],
                "last_successful_price_update": metrics["last_successful_price_update"]
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

# Socket.IO events with enhanced error handling
@sio.event
async def connect(sid, environ):
    """Handle client connection with metrics tracking"""
    try:
        metrics["active_connections"] += 1
        metrics["total_connections"] += 1
        logger.info(f"Client connected: {sid}")
        
        await sio.emit('welcome', {
            "message": "Welcome to the OMEGA BTC AI Price Feed",
            "timestamp": datetime.datetime.now().isoformat()
        }, room=sid)
        
        # Send initial data
        if price_cache:
            await sio.emit('price_update', price_cache, room=sid)
    except Exception as e:
        logger.error(f"Error in connect handler: {e}")
        metrics["active_connections"] -= 1

@sio.event
async def disconnect(sid):
    """Handle client disconnection with metrics tracking"""
    try:
        metrics["active_connections"] -= 1
        logger.info(f"Client disconnected: {sid}")
    except Exception as e:
        logger.error(f"Error in disconnect handler: {e}")

@sio.event
async def subscribe_price(sid, data):
    """Handle price subscription with retry logic"""
    try:
        logger.info(f"Client {sid} subscribed to price updates: {data}")
        if price_cache:
            await sio.emit('price_update', price_cache, room=sid)
    except Exception as e:
        logger.error(f"Error in subscribe_price handler: {e}")

async def fetch_price_with_retry() -> Dict[str, str | float]:
    """Fetch price with retry logic"""
    global price_cache, last_price_update
    
    # Check if we should update the cache
    now = datetime.datetime.now()
    if (now - last_price_update).total_seconds() < BROADCAST_INTERVAL:
        return price_cache
        
    logger.info(f"Fetching fresh price at {now.isoformat()}")
    
    for attempt in range(MAX_RETRIES):
        try:
            # Get the latest price from the price feed
            if price_feed.last_price > 0:
                price_data = {
                    "price": price_feed.last_price,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "exchange": "binance"
                }
                
                # Update cache and timestamp
                price_cache = price_data
                last_price_update = now
                metrics["last_successful_price_update"] = now.isoformat()
                
                return price_data
            else:
                logger.warning("Price feed has not received any price updates yet")
                return price_cache if price_cache else {}
        except Exception as e:
            logger.error(f"Error fetching price (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            metrics["failed_price_fetches"] += 1
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY)
            else:
                logger.error("Max retries reached for price fetch")
                return price_cache if price_cache else {}

async def broadcast_updates():
    """Broadcast price updates to all connected clients"""
    while True:
        try:
            price_data = await fetch_price_with_retry()
            if price_data:
                await sio.emit('price_update', price_data)
            await asyncio.sleep(BROADCAST_INTERVAL)
        except Exception as e:
            logger.error(f"Error in broadcast loop: {e}")
            await asyncio.sleep(RETRY_DELAY)

@app.on_event("startup")
async def startup_event():
    """Start the broadcast loop on startup"""
    # Start the price feed
    await price_feed.start()
    # Start the broadcast loop
    asyncio.create_task(broadcast_updates())

# Run the app directly if invoked
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "10095"))
    uvicorn.run("websocket_minimal:app", host="0.0.0.0", port=port, reload=True) 