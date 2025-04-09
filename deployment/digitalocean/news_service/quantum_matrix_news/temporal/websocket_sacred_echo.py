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

"""
WebSocket Sacred Echo Service
============================

This service provides real-time websocket connections for the Matrix Neo News Portal,
enabling:
- Real-time news updates
- Sacred prophecy streaming
- Consciousness-level adjusted information
- Quantum-secured communications

The service interfaces with:
- Matrix News Consciousness Service
- Redis for data persistence
- Client websocket connections
- Existing News Service (indirectly)

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the GBU License
"""

import os
import json
import asyncio
import logging
import random
import datetime
import time
from typing import Dict, List, Optional, Any, Set

import socketio
import aiohttp
from aiohttp import web
import aioredis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Environment variables
PORT = int(os.getenv("PORT", 8095))
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
NEWS_SERVICE_URL = os.getenv("NEWS_SERVICE_URL", "http://matrix-news-consciousness:8090")
PROPHECY_STREAM_ENABLED = os.getenv("PROPHECY_STREAM_ENABLED", "true").lower() == "true"
QUANTUM_ENTROPY_LEVEL = int(os.getenv("QUANTUM_ENTROPY_LEVEL", 8))
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 60))  # seconds

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode="aiohttp",
    cors_allowed_origins="*",
    ping_interval=25,  # Send ping every 25 seconds
    ping_timeout=10,  # Wait 10 seconds for pong before disconnect
)

# Create AIOHTTP web application
app = web.Application()
sio.attach(app)

# Store active clients and their consciousness levels
active_clients: Dict[str, Dict[str, Any]] = {}

# Redis connection
redis: Optional[aioredis.Redis] = None

# Last fetched news items
last_news_items: List[Dict[str, Any]] = []
last_fetch_time: float = 0

# Helper functions
def generate_quantum_entropy(level: int = 8) -> Dict[str, Any]:
    """Generate quantum entropy for secure communications."""
    entropy = {
        "entropy_value": random.random(),
        "quantum_state": random.choice(["superposition", "entangled", "collapsed"]),
        "timestamp": datetime.datetime.now().isoformat(),
        "level": level,
    }
    
    if level >= 7:
        # Add higher dimensional entropy factors
        entropy["dimensional_factors"] = {
            "temporal_variance": random.random(),
            "harmonic_resonance": random.random(),
            "synchronicity_coefficient": random.random(),
        }
    
    return entropy

async def fetch_news_from_consciousness_service(consciousness_level: int, language: str = "en") -> List[Dict[str, Any]]:
    """Fetch news from the Matrix News Consciousness Service."""
    global last_news_items, last_fetch_time
    
    # Check if we have recent data and can avoid a fetch
    current_time = time.time()
    if last_news_items and (current_time - last_fetch_time < FETCH_INTERVAL):
        return last_news_items
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "X-Consciousness-Level": str(consciousness_level),
                "X-Preferred-Language": language
            }
            async with session.get(f"{NEWS_SERVICE_URL}/api/news", headers=headers) as response:
                if response.status == 200:
                    news_data = await response.json()
                    last_news_items = news_data
                    last_fetch_time = current_time
                    return news_data
                else:
                    logger.error(f"Failed to fetch news: {response.status}")
                    # Return whatever we have, even if it's old
                    return last_news_items
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return last_news_items

def filter_news_by_consciousness(news_items: List[Dict[str, Any]], level: int) -> List[Dict[str, Any]]:
    """Filter news based on consciousness level."""
    return [item for item in news_items if item.get("consciousness_level", 5) <= level]

async def fetch_divine_message(consciousness_level: int) -> Dict[str, Any]:
    """Fetch a divine message from the Matrix News Consciousness Service."""
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"X-Consciousness-Level": str(consciousness_level)}
            async with session.get(f"{NEWS_SERVICE_URL}/api/divine-message", headers=headers) as response:
                if response.status == 200:
                    message_data = await response.json()
                    return message_data
                else:
                    logger.error(f"Failed to fetch divine message: {response.status}")
                    return {
                        "consciousness_level": consciousness_level,
                        "message": "The divine signal is temporarily obscured. Center yourself and try again.",
                        "timestamp": datetime.datetime.now().isoformat(),
                    }
    except Exception as e:
        logger.error(f"Error fetching divine message: {e}")
        return {
            "consciousness_level": consciousness_level,
            "message": "The cosmic connection is reestablishing. Patience will be rewarded.",
            "timestamp": datetime.datetime.now().isoformat(),
        }

async def check_for_news_updates():
    """Periodically check for news updates and notify clients."""
    while True:
        if active_clients:
            try:
                # Fetch news with a moderate consciousness level
                news_items = await fetch_news_from_consciousness_service(5)
                
                if news_items:
                    # Store in Redis for persistence
                    if redis:
                        try:
                            await redis.set("latest_news", json.dumps(news_items))
                            await redis.expire("latest_news", 3600)  # Expire after 1 hour
                        except Exception as e:
                            logger.error(f"Error storing news in Redis: {e}")
                    
                    # Notify all clients
                    for sid, client_info in active_clients.items():
                        client_consciousness = client_info.get("consciousness_level", 5)
                        
                        # Filter items based on client's consciousness level
                        filtered_items = filter_news_by_consciousness(news_items, client_consciousness)
                        
                        if filtered_items:
                            await sio.emit("news", {
                                "type": "news_update",
                                "data": filtered_items,
                                "quantum_entropy": generate_quantum_entropy(QUANTUM_ENTROPY_LEVEL),
                                "timestamp": datetime.datetime.now().isoformat(),
                            }, room=sid)
            except Exception as e:
                logger.error(f"Error in news update check: {e}")
        
        # Wait before checking again
        await asyncio.sleep(FETCH_INTERVAL)

async def broadcast_prophetic_message():
    """Broadcast periodic prophetic messages to all clients."""
    prophecies = [
        "The markets are whispering ancient secrets to those who listen with their third eye.",
        "A wave of quantum consciousness is approaching, prepare your digital vessels.",
        "The blockchain's sacred geometry reveals the Fibonacci sequence of financial evolution.",
        "When the cosmic and digital realms align, new possibilities emerge from the quantum field.",
        "The next 24 hours will reveal patterns that have been hidden in plain sight.",
        "Those who meditate on the market's rhythm will perceive the divine timing of entry and exit.",
        "The veil between financial dimensions grows thin, allowing glimpses of potential futures.",
        "Synchronize your awareness with the market's breath to ride the next wave of prosperity.",
        "Ancient wisdom and modern technology are merging to birth a new economic paradigm.",
        "The divine matrix is recalibrating - expect unusual patterns in familiar systems.",
    ]
    
    while True:
        if active_clients and PROPHECY_STREAM_ENABLED:
            prophecy = random.choice(prophecies)
            payload = {
                "type": "announcement",
                "data": {
                    "message": prophecy,
                    "wisdom": "The future reveals itself to those who are conscious in the present moment.",
                    "timestamp": datetime.datetime.now().isoformat(),
                }
            }
            
            # Add quantum entropy for security
            payload["quantum_entropy"] = generate_quantum_entropy(QUANTUM_ENTROPY_LEVEL)
            
            # Broadcast to all clients
            await sio.emit("news", payload)
            
            logger.info(f"Broadcast prophecy: {prophecy[:30]}...")
        
        # Wait for next broadcast window (2-10 minutes)
        await asyncio.sleep(random.randint(120, 600))

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    """Handle client connection."""
    client_info = {
        "sid": sid,
        "connected_at": datetime.datetime.now().isoformat(),
        "consciousness_level": 5,  # Default level
        "preferred_language": "en",  # Default language
        "ip": environ.get("REMOTE_ADDR", "unknown"),
        "user_agent": environ.get("HTTP_USER_AGENT", "unknown"),
    }
    
    # Check for language preference in headers or cookies
    accept_language = environ.get("HTTP_ACCEPT_LANGUAGE", "")
    if accept_language:
        # Simple parsing - just get the first language code
        lang_code = accept_language.split(",")[0].strip().split(";")[0].strip().lower()
        if lang_code and len(lang_code) >= 2:
            client_info["preferred_language"] = lang_code[:2]  # Just use the primary language code
    
    # Check cookies for preferred_language
    cookie_header = environ.get("HTTP_COOKIE", "")
    if cookie_header and "preferred_language=" in cookie_header:
        try:
            # Simple cookie parsing
            cookie_parts = cookie_header.split(";")
            for part in cookie_parts:
                if "preferred_language=" in part:
                    lang_value = part.split("=")[1].strip()
                    if lang_value and len(lang_value) >= 2:
                        client_info["preferred_language"] = lang_value
        except:
            pass
    
    active_clients[sid] = client_info
    
    logger.info(f"Client connected: {sid}, language: {client_info['preferred_language']}")
    
    # Send welcome message with quantum entropy
    await sio.emit("connect", {
        "message": "Welcome to the Matrix Neo News Portal WebSocket Sacred Echo Service",
        "quantum_entropy": generate_quantum_entropy(QUANTUM_ENTROPY_LEVEL),
        "timestamp": datetime.datetime.now().isoformat(),
    }, room=sid)
    
    # Send initial news
    news_items = await fetch_news_from_consciousness_service(
        client_info["consciousness_level"],
        client_info["preferred_language"]
    )
    filtered_news = filter_news_by_consciousness(news_items, client_info["consciousness_level"])
    
    await sio.emit("news", {
        "type": "news_update",
        "data": filtered_news,
        "quantum_entropy": generate_quantum_entropy(QUANTUM_ENTROPY_LEVEL),
        "timestamp": datetime.datetime.now().isoformat(),
    }, room=sid)

@sio.event
async def disconnect(sid):
    """Handle client disconnection."""
    if sid in active_clients:
        logger.info(f"Client disconnected: {sid}")
        del active_clients[sid]

@sio.event
async def set_consciousness_level(sid, data):
    """Handle consciousness level updates from clients."""
    try:
        level = int(data.get("level", 5))
        
        # Validate level
        if level < 1 or level > 9:
            logger.warning(f"Invalid consciousness level from {sid}: {level}")
            await sio.emit("error", {
                "message": "Consciousness level must be between 1 and 9",
                "timestamp": datetime.datetime.now().isoformat(),
            }, room=sid)
            return
        
        # Update client's consciousness level
        if sid in active_clients:
            old_level = active_clients[sid]["consciousness_level"]
            active_clients[sid]["consciousness_level"] = level
            
            # Notify client of update
            await sio.emit("consciousness", {
                "previous_level": old_level,
                "new_level": level,
                "timestamp": datetime.datetime.now().isoformat(),
            }, room=sid)
            
            logger.info(f"Updated consciousness level for {sid}: {old_level} -> {level}")
            
            # Send updated news based on new consciousness level
            client_language = active_clients[sid].get("preferred_language", "en")
            news_items = await fetch_news_from_consciousness_service(level, client_language)
            filtered_news = filter_news_by_consciousness(news_items, level)
            
            await sio.emit("news", {
                "type": "consciousness_update",
                "data": filtered_news,
                "quantum_entropy": generate_quantum_entropy(QUANTUM_ENTROPY_LEVEL),
                "timestamp": datetime.datetime.now().isoformat(),
            }, room=sid)
    except Exception as e:
        logger.error(f"Error updating consciousness level: {e}")
        await sio.emit("error", {
            "message": "Error updating consciousness level",
            "error": str(e),
            "timestamp": datetime.datetime.now().isoformat(),
        }, room=sid)

@sio.event
async def set_language_preference(sid, data):
    """Handle language preference updates from clients."""
    try:
        language_code = data.get("language", "en")
        
        # Basic validation - just check it's a string and not empty
        if not isinstance(language_code, str) or not language_code:
            language_code = "en"
        
        # Update client's language preference
        if sid in active_clients:
            old_language = active_clients[sid].get("preferred_language", "en")
            active_clients[sid]["preferred_language"] = language_code
            
            # Notify client of update
            await sio.emit("language_update", {
                "previous_language": old_language,
                "new_language": language_code,
                "timestamp": datetime.datetime.now().isoformat(),
            }, room=sid)
            
            logger.info(f"Updated language preference for {sid}: {old_language} -> {language_code}")
            
            # If consciousness level is high enough, refresh content with new language
            consciousness_level = active_clients[sid]["consciousness_level"]
            if consciousness_level >= 7:  # Only refresh for high consciousness
                news_items = await fetch_news_from_consciousness_service(consciousness_level, language_code)
                filtered_news = filter_news_by_consciousness(news_items, consciousness_level)
                
                await sio.emit("news", {
                    "type": "language_update",
                    "data": filtered_news,
                    "quantum_entropy": generate_quantum_entropy(QUANTUM_ENTROPY_LEVEL),
                    "timestamp": datetime.datetime.now().isoformat(),
                }, room=sid)
    except Exception as e:
        logger.error(f"Error updating language preference: {e}")
        await sio.emit("error", {
            "message": "Error updating language preference",
            "error": str(e),
            "timestamp": datetime.datetime.now().isoformat(),
        }, room=sid)

@sio.event
async def request_divine_message(sid, data):
    """Handle requests for divine messages."""
    try:
        if sid in active_clients:
            level = active_clients[sid]["consciousness_level"]
            language = active_clients[sid].get("preferred_language", "en")
            
            # Add language preference to request headers
            headers = {
                "X-Consciousness-Level": str(level),
                "X-Preferred-Language": language
            }
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{NEWS_SERVICE_URL}/api/divine-message", headers=headers) as response:
                        if response.status == 200:
                            divine_message = await response.json()
                            
                            await sio.emit("divine_message", {
                                "message": divine_message,
                                "quantum_entropy": generate_quantum_entropy(QUANTUM_ENTROPY_LEVEL),
                                "timestamp": datetime.datetime.now().isoformat(),
                            }, room=sid)
                            
                            logger.info(f"Sent divine message to {sid} (consciousness: {level}, language: {language})")
                            return
            except Exception as e:
                logger.error(f"Error fetching divine message from API: {e}")
            
            # Fallback to direct calling if API call fails
            divine_message = await fetch_divine_message(level)
            
            await sio.emit("divine_message", {
                "message": divine_message,
                "quantum_entropy": generate_quantum_entropy(QUANTUM_ENTROPY_LEVEL),
                "timestamp": datetime.datetime.now().isoformat(),
            }, room=sid)
            
            logger.info(f"Sent fallback divine message to {sid} (consciousness level: {level})")
    except Exception as e:
        logger.error(f"Error sending divine message: {e}")
        await sio.emit("error", {
            "message": "Error retrieving divine message",
            "error": str(e),
            "timestamp": datetime.datetime.now().isoformat(),
        }, room=sid)

# HTTP routes
async def handle_index(request):
    """Handle root path - return info."""
    return web.json_response({
        "service": "Matrix Neo News Portal WebSocket Sacred Echo Service",
        "version": "1.0.0",
        "status": "UP",
        "timestamp": datetime.datetime.now().isoformat(),
    })

async def handle_health(request):
    """Handle health check path."""
    return web.json_response({
        "status": "UP",
        "service": "matrix-websocket-sacred-echo",
        "quantum_secure": True,
        "timestamp": datetime.datetime.now().isoformat(),
    })

# Register HTTP routes
app.router.add_get('/', handle_index)
app.router.add_get('/health', handle_health)

async def start_background_tasks(app):
    """Start background tasks when app starts."""
    app["news_update_task"] = asyncio.create_task(check_for_news_updates())
    app["prophecy_task"] = asyncio.create_task(broadcast_prophetic_message())
    
    # Create Redis connection
    global redis
    try:
        # Use Redis connection
        redis = await aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
        logger.info(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        redis = None

async def cleanup_background_tasks(app):
    """Clean up background tasks when app stops."""
    app["news_update_task"].cancel()
    app["prophecy_task"].cancel()
    
    try:
        await app["news_update_task"]
        await app["prophecy_task"]
    except asyncio.CancelledError:
        pass
    
    # Close Redis connection
    global redis
    if redis:
        await redis.close()
        logger.info("Redis connection closed")

# Register startup and cleanup functions
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)

if __name__ == "__main__":
    logger.info(f"Starting Matrix WebSocket Sacred Echo Service on port {PORT}...")
    web.run_app(app, port=PORT) 