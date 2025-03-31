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
from omega_ai.data_feed.newsfeed.btc_newsfeed import BtcNewsFeed
from omega_ai.data_feed.btc_live_feed_v3 import BtcLiveFeedV3

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
NEWS_UPDATE_INTERVAL = int(os.getenv("NEWS_UPDATE_INTERVAL", "300"))
BROADCAST_INTERVAL = int(os.getenv("BROADCAST_INTERVAL", "30"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=logger,
    engineio_logger=True
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

# Initialize news feed and price feed
news_feed = BtcNewsFeed()
price_feed = BtcLiveFeedV3()

# Cache for news and price data
news_cache: List[Dict] = []
price_cache: Dict = {}
last_news_update = datetime.datetime.now() - datetime.timedelta(minutes=10)
last_price_update = datetime.datetime.now() - datetime.timedelta(minutes=10)

# Metrics for health check
metrics = {
    "active_connections": 0,
    "total_connections": 0,
    "failed_news_fetches": 0,
    "failed_price_fetches": 0,
    "last_successful_news_update": None,
    "last_successful_price_update": None
}

# Create a detailed health endpoint
@app.get("/health")
async def health():
    """Enhanced health check endpoint with detailed metrics"""
    try:
        # Check Redis connection if configured
        redis_status = "connected" if hasattr(news_feed, "redis") and news_feed.redis.ping() else "disconnected"
        
        return {
            "status": "UP",
            "service": "websocket-minimal",
            "timestamp": datetime.datetime.now().isoformat(),
            "news_feed_status": "connected" if news_feed else "disconnected",
            "price_feed_status": "connected" if price_feed else "disconnected",
            "redis_status": redis_status,
            "metrics": {
                "active_connections": metrics["active_connections"],
                "total_connections": metrics["total_connections"],
                "failed_news_fetches": metrics["failed_news_fetches"],
                "failed_price_fetches": metrics["failed_price_fetches"],
                "last_successful_news_update": metrics["last_successful_news_update"],
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
            "message": "Welcome to the OMEGA BTC AI News Portal",
            "timestamp": datetime.datetime.now().isoformat()
        }, room=sid)
        
        # Send initial data
        if news_cache:
            for news_item in news_cache[:5]:
                await sio.emit('news_update', news_item, room=sid)
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
async def subscribe_news(sid, data):
    """Handle news subscription with retry logic"""
    try:
        logger.info(f"Client {sid} subscribed to news: {data}")
        if news_cache:
            for news_item in news_cache[:5]:
                await sio.emit('news_update', news_item, room=sid)
    except Exception as e:
        logger.error(f"Error in subscribe_news handler: {e}")

@sio.event
async def subscribe_price(sid, data):
    """Handle price subscription with retry logic"""
    try:
        logger.info(f"Client {sid} subscribed to price updates: {data}")
        if price_cache:
            await sio.emit('price_update', price_cache, room=sid)
    except Exception as e:
        logger.error(f"Error in subscribe_price handler: {e}")

async def fetch_news_with_retry() -> List[Dict]:
    """Fetch news with retry logic"""
    global news_cache, last_news_update
    
    # Check if we should update the cache
    now = datetime.datetime.now()
    if (now - last_news_update).total_seconds() < NEWS_UPDATE_INTERVAL:
        return news_cache
        
    logger.info(f"Fetching fresh news at {now.isoformat()}")
    
    for attempt in range(MAX_RETRIES):
        try:
            # Fetch news from multiple sources
            sources = ["cointelegraph", "decrypt", "bitcoinmagazine"]
            all_entries = []
            
            for source in sources:
                entries = news_feed.fetch_news(source)
                all_entries.extend(entries)
            
            # Apply cosmic adjustments
            all_entries = news_feed.adjust_sentiment_with_cosmic_factors(all_entries)
            
            # Sort by publish date (newest first)
            all_entries.sort(key=lambda x: x['published'], reverse=True)
            
            # Update cache and timestamp
            news_cache = all_entries
            last_news_update = now
            metrics["last_successful_news_update"] = now.isoformat()
            
            return all_entries
        except Exception as e:
            logger.error(f"Error fetching news (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            metrics["failed_news_fetches"] += 1
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY)
            else:
                logger.error("Max retries reached for news fetch")
                return news_cache if news_cache else []

async def broadcast_updates():
    """Periodically fetch and broadcast news and price updates with enhanced error handling"""
    while True:
        try:
            # Fetch news updates
            news_items = await fetch_news_with_retry()
            if news_items:
                latest_news = news_items[0]
                logger.info(f"Broadcasting news: {latest_news['title']}")
                await sio.emit('news_update', latest_news)
            
            # Get price updates from price feed
            if price_feed and hasattr(price_feed, 'last_price') and price_feed.last_price:
                price_data = {
                    "price": price_feed.last_price,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "exchange": os.getenv("EXCHANGE", "binance")
                }
                metrics["last_successful_price_update"] = datetime.datetime.now().isoformat()
                await sio.emit('price_update', price_data)
            
            # Send heartbeat
            await sio.emit('heartbeat', {
                "type": "heartbeat",
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            # Wait before next update
            await asyncio.sleep(BROADCAST_INTERVAL)
        except Exception as e:
            logger.error(f"Error in broadcast: {e}")
            metrics["failed_price_fetches"] += 1
            await asyncio.sleep(RETRY_DELAY)

@sio.event
async def get_latest_news(sid, data=None):
    """Send the latest news items to the requesting client with error handling"""
    try:
        news_items = await fetch_news_with_retry()
        for item in news_items[:10]:
            await sio.emit('news_update', item, room=sid)
    except Exception as e:
        logger.error(f"Error in get_latest_news handler: {e}")

@app.on_event("startup")
async def startup_event():
    """Start background tasks when the application starts"""
    try:
        # Start news and price feed tasks
        sio.start_background_task(broadcast_updates)
        if price_feed:
            sio.start_background_task(price_feed.start)
        logger.info("WebSocket service started successfully")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

# Run the app directly if invoked
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "10095"))
    uvicorn.run("websocket_minimal:app", host="0.0.0.0", port=port, reload=True) 