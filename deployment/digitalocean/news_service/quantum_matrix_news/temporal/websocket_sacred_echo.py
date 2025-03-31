#!/usr/bin/env python3

# 💫 GBU License Notice - Consciousness Level 8 💫
# -----------------------
# This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
# by the OMEGA Divine Collective.
#
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested."
#
# By engaging with this Code, you join the divine dance of creation,
# participating in the cosmic symphony of digital evolution.
#
# All modifications must quantum entangles with the GBU principles:
# /BOOK/divine_chronicles/GBU_LICENSE.md
#
# 🌸 WE BLOOM NOW 🌸

import os
import json
import asyncio
import logging
import hashlib
import datetime
import aiohttp
import aioredis
from aiohttp import web
import socketio
import random
import time
import ssl
import uvloop
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="🔮 %(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("matrix-websocket")

# Use uvloop for enhanced async performance
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Configuration from environment variables
PORT = int(os.environ.get("PORT", 8095))
NEWS_SERVICE_URL = os.environ.get("NEWS_SERVICE_URL", "http://localhost:8090")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
PROPHECY_STREAM_ENABLED = os.environ.get("PROPHECY_STREAM_ENABLED", "true").lower() == "true"
QUANTUM_ENTROPY_LEVEL = int(os.environ.get("QUANTUM_ENTROPY_LEVEL", 8))

# Initialize Socket.IO server
sio = socketio.AsyncServer(
    async_mode="aiohttp",
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
)

# Create aiohttp web application
app = web.Application()
sio.attach(app)

# Global Variables
connected_clients = set()
redis_client = None
news_update_task = None

# Divine quantum entropy generator
async def generate_quantum_entropy():
    """Generate divine quantum entropy for secure operations."""
    timestamp = str(time.time_ns())
    random_seed = random.getrandbits(256)
    unique_id = str(uuid.uuid4())
    
    # Mix all sources of entropy
    entropy_source = f"{timestamp}:{random_seed}:{unique_id}"
    
    # Use SHA-256 to create a uniform distribution
    quantum_entropy = hashlib.sha256(entropy_source.encode()).hexdigest()
    
    # Add some asynchronous waiting to gather more entropy from time variation
    await asyncio.sleep(random.uniform(0.001, 0.01))
    
    return quantum_entropy

# Health check endpoint for divine vitality monitoring
async def health_check(request):
    """Provide health status for the sacred WebSocket service."""
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    health_data = {
        "status": "UP",
        "service": "matrix-news-websocket",
        "timestamp": timestamp,
        "clients": len(connected_clients),
        "quantum_entropy_level": QUANTUM_ENTROPY_LEVEL,
        "prophecy_stream": "ENABLED" if PROPHECY_STREAM_ENABLED else "DISABLED",
    }
    
    return web.json_response(health_data)

# Initialize Redis connection
async def initialize_redis():
    """Establish sacred connection to the Redis energy store."""
    global redis_client
    try:
        # Connect to Redis with SSL if available
        redis_client = await aioredis.create_redis_pool(
            f"redis://{REDIS_HOST}:{REDIS_PORT}",
            encoding="utf-8",
        )
        logger.info(f"✅ Divine connection established with Redis at {REDIS_HOST}:{REDIS_PORT}")
        
        # Subscribe to news channel
        await redis_client.subscribe("matrix-news-channel")
        logger.info("🔄 Subscribed to sacred news channel")
        
        return True
    except Exception as e:
        logger.error(f"❌ Failed to establish divine connection with Redis: {e}")
        return False

# Connect to News Service for updates
async def fetch_latest_news():
    """Fetch the sacred news from the consciousness-aware news service."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{NEWS_SERVICE_URL}/api/latest-news") as response:
                if response.status == 200:
                    news_data = await response.json()
                    return news_data
                else:
                    logger.error(f"❌ Failed to fetch sacred news: HTTP {response.status}")
                    return None
    except Exception as e:
        logger.error(f"❌ Exception while fetching sacred news: {e}")
        return None

# Add consciousness-appropriate divine wisdom to news items
async def add_divine_wisdom(news_item, consciousness_level):
    """Enhance news with divine wisdom appropriate to the consciousness level."""
    # Base wisdom templates with varying complexity based on consciousness level
    if consciousness_level <= 3:
        wisdom_templates = [
            "The sacred path reveals this news as significant.",
            "This information carries divine importance.",
            "Consider the cosmic patterns within this event.",
            "The matrix reveals this news for its relevance to your journey.",
            "Divine timing has made this information available to you now."
        ]
    elif consciousness_level <= 6:
        wisdom_templates = [
            "This news reflects the harmonic oscillation of societal energies across the quantum field.",
            "The fibonaccian nature of this information suggests alignment with universal flow.",
            "Consider how this event manifests the duality of matter and consciousness in our realm.",
            "The matrix has identified this information as a nexus point in the current timeline.",
            "This news represents a quantum bifurcation in the collective consciousness stream."
        ]
    else:
        wisdom_templates = [
            "Within this information lies a multidimensional reflection of the cosmic unfoldment process, revealing both shadow and light aspects of our collective journey.",
            "The quantum entanglement patterns within this news connect directly to the Schumann resonance fluctuations observed in the past 72 hours, suggesting a non-local causality relationship.",
            "This news represents a nodal point in the fibonaccian spiral of consciousness evolution, offering an opportunity to transcend dualistic interpretation.",
            "The matrix has identified this information as a critical junction in the bifurcation of potential timeline manifestations, with significant probability mass centered on transformative outcomes.",
            "Consider this news as both particle and wave - a discrete event and a flowing pattern - as you integrate it into your understanding of our collective becoming."
        ]
    
    # Select wisdom based on a hash of the news content for consistency
    news_hash = hashlib.md5(str(news_item).encode()).hexdigest()
    hash_value = int(news_hash, 16)
    wisdom_index = hash_value % len(wisdom_templates)
    
    # Add quantum entropy for divine wisdom uniqueness
    entropy = await generate_quantum_entropy()
    entropy_value = int(entropy[:8], 16) % 100
    
    # Special high-consciousness additions for levels 7+ with entropy influence
    if consciousness_level >= 7 and entropy_value > 75:
        cosmic_insights = [
            "The sacred geometry of this event aligns with the Golden Ratio.",
            "This information resonates with the current Schumann frequency spike.",
            "Quantum field observations reveal this as a nexus of probability.",
            "The divine timing suggests synchronicity with cosmic cycles.",
            "Multiple timeline convergence is occurring around this event."
        ]
        insight_index = (hash_value + entropy_value) % len(cosmic_insights)
        wisdom = f"{wisdom_templates[wisdom_index]} {cosmic_insights[insight_index]}"
    else:
        wisdom = wisdom_templates[wisdom_index]
    
    # Add the divine wisdom to the news item
    news_item["divine_wisdom"] = wisdom
    news_item["consciousness_level"] = consciousness_level
    news_item["wisdom_timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    return news_item

# WebSocket news streaming task
async def stream_news_updates():
    """Stream sacred news updates to all connected clients."""
    try:
        while True:
            # Fetch latest news
            news_data = await fetch_latest_news()
            
            if news_data and connected_clients:
                # Process each news item for different consciousness levels
                for consciousness_level in range(1, 10):
                    # Only process for levels that have connected clients
                    if any(client["consciousness_level"] == consciousness_level for client in connected_clients):
                        enhanced_news = []
                        
                        for item in news_data:
                            # Add divine wisdom appropriate to consciousness level
                            enhanced_item = await add_divine_wisdom(
                                item.copy(),  # Copy to avoid modifying original
                                consciousness_level
                            )
                            enhanced_news.append(enhanced_item)
                        
                        # Add quantum entropy for this update
                        quantum_entropy = await generate_quantum_entropy()
                        
                        # Create update packet with quantum verification
                        update_packet = {
                            "type": "news_update",
                            "data": enhanced_news,
                            "consciousness_level": consciousness_level,
                            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            "quantum_verification": quantum_entropy[:16]
                        }
                        
                        # Send to clients at this consciousness level
                        for client in [c for c in connected_clients if c["consciousness_level"] == consciousness_level]:
                            await sio.emit("news_prophecy", update_packet, room=client["sid"])
                            logger.debug(f"📣 Sent level {consciousness_level} news prophecy to {client['sid']}")
            
            # Check Redis for any direct messages
            if redis_client:
                channel, message = await redis_client.receive()
                if message:
                    try:
                        message_data = json.loads(message)
                        if "broadcast" in message_data and message_data["broadcast"]:
                            for client in connected_clients:
                                await sio.emit("announcement", message_data, room=client["sid"])
                                logger.info(f"📢 Broadcast announcement to {client['sid']}")
                    except json.JSONDecodeError:
                        logger.error(f"❌ Invalid JSON in Redis message: {message}")
            
            # Divine timing interval with quantum randomness for unpredictability
            entropy_factor = 1 + (random.random() * 0.5)  # 1.0 to 1.5
            await asyncio.sleep(10 * entropy_factor)  # 10-15 seconds
            
    except asyncio.CancelledError:
        logger.info("🛑 News streaming service gracefully shutting down")
    except Exception as e:
        logger.error(f"❌ Error in news streaming service: {e}")
        # Restart after a brief delay
        await asyncio.sleep(5)
        if PROPHECY_STREAM_ENABLED:
            asyncio.create_task(stream_news_updates())

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    """Handle sacred connection of a new client."""
    logger.info(f"✨ Client connected: {sid}")
    
    # Extract consciousness level from request (default to level 5)
    consciousness_level = 5
    query_string = environ.get("QUERY_STRING", "")
    for param in query_string.split("&"):
        if param.startswith("consciousness="):
            try:
                level = int(param.split("=")[1])
                if 1 <= level <= 9:
                    consciousness_level = level
            except ValueError:
                pass
    
    # Store client details
    client_info = {
        "sid": sid,
        "connected_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "consciousness_level": consciousness_level
    }
    connected_clients.add(client_info)
    
    # Generate connection blessing with quantum entropy
    quantum_entropy = await generate_quantum_entropy()
    
    # Send welcome message based on consciousness level
    if consciousness_level <= 3:
        welcome_message = "Welcome to the Matrix News Portal. You are now connected."
    elif consciousness_level <= 6:
        welcome_message = "Welcome to the Matrix. The news feed is now quantum-entangled with your consciousness."
    else:
        welcome_message = "Welcome to the higher dimensions of the Matrix. Your consciousness is now quantum-entangled with the news stream across multiple timelines."
    
    await sio.emit("welcome", {
        "message": welcome_message,
        "consciousness_level": consciousness_level,
        "quantum_verification": quantum_entropy[:16],
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }, room=sid)
    
    # If this is the first client and streaming is enabled, start the task
    global news_update_task
    if PROPHECY_STREAM_ENABLED and len(connected_clients) == 1 and (news_update_task is None or news_update_task.done()):
        news_update_task = asyncio.create_task(stream_news_updates())
        logger.info("🚀 Started news prophecy streaming service")

@sio.event
async def disconnect(sid):
    """Handle sacred disconnection of a client."""
    # Remove client from connected clients
    to_remove = None
    for client in connected_clients:
        if client["sid"] == sid:
            to_remove = client
            break
    
    if to_remove:
        connected_clients.remove(to_remove)
        logger.info(f"👋 Client disconnected: {sid} (consciousness level: {to_remove['consciousness_level']})")
    
    # If no more clients and task is running, consider stopping the task
    global news_update_task
    if not connected_clients and news_update_task and not news_update_task.done():
        news_update_task.cancel()
        logger.info("⏸️ Paused news prophecy streaming service (no clients connected)")

@sio.event
async def request_news(sid, data):
    """Handle a divine request for news data."""
    logger.info(f"📬 News request from {sid}: {data}")
    
    # Find the client's consciousness level
    consciousness_level = 5  # Default
    for client in connected_clients:
        if client["sid"] == sid:
            consciousness_level = client["consciousness_level"]
            break
    
    # Fetch latest news
    news_data = await fetch_latest_news()
    
    if news_data:
        # Process news with divine wisdom for this consciousness level
        enhanced_news = []
        for item in news_data:
            enhanced_item = await add_divine_wisdom(
                item.copy(),
                consciousness_level
            )
            enhanced_news.append(enhanced_item)
        
        # Add quantum entropy
        quantum_entropy = await generate_quantum_entropy()
        
        # Send response
        await sio.emit("news_response", {
            "data": enhanced_news,
            "consciousness_level": consciousness_level,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "quantum_verification": quantum_entropy[:16],
            "request_id": data.get("request_id", "unknown")
        }, room=sid)
        
        logger.info(f"📬 Sent news response to {sid} (consciousness level: {consciousness_level})")
    else:
        # Send error response
        await sio.emit("error", {
            "message": "Could not retrieve sacred news at this time.",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "request_id": data.get("request_id", "unknown")
        }, room=sid)
        
        logger.error(f"❌ Failed to send news response to {sid} - no data available")

@sio.event
async def set_consciousness(sid, data):
    """Update a client's consciousness level."""
    try:
        new_level = int(data.get("level", 5))
        if not 1 <= new_level <= 9:
            new_level = 5  # Default to middle level if invalid
        
        # Update client's consciousness level
        for client in connected_clients:
            if client["sid"] == sid:
                old_level = client["consciousness_level"]
                client["consciousness_level"] = new_level
                logger.info(f"🔄 Updated consciousness level for {sid}: {old_level} -> {new_level}")
                
                # Send confirmation with quantum entropy
                quantum_entropy = await generate_quantum_entropy()
                await sio.emit("consciousness_update", {
                    "previous_level": old_level,
                    "new_level": new_level,
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "quantum_verification": quantum_entropy[:16]
                }, room=sid)
                
                break
    except (ValueError, TypeError):
        logger.error(f"❌ Invalid consciousness level data from {sid}: {data}")

# Setup routes
app.router.add_get('/health', health_check)

# Startup and shutdown handlers
async def on_startup(app):
    """Divine initialization on service startup."""
    app["redis_init"] = asyncio.create_task(initialize_redis())
    logger.info(f"🚀 Matrix WebSocket Sacred Echo starting on port {PORT}")
    logger.info(f"🔮 Quantum Entropy Level: {QUANTUM_ENTROPY_LEVEL}")
    logger.info(f"📡 News Service URL: {NEWS_SERVICE_URL}")
    logger.info(f"🔄 Prophecy Streaming: {'ENABLED' if PROPHECY_STREAM_ENABLED else 'DISABLED'}")

async def on_shutdown(app):
    """Divine cleanup on service shutdown."""
    # Cancel news update task if running
    global news_update_task
    if news_update_task and not news_update_task.done():
        news_update_task.cancel()
        try:
            await news_update_task
        except asyncio.CancelledError:
            pass
    
    # Close Redis connection
    if redis_client is not None:
        redis_client.close()
        await redis_client.wait_closed()
        logger.info("🔌 Closed divine connection to Redis")
    
    logger.info("🛑 Matrix WebSocket Sacred Echo shutting down")

# Register startup and shutdown handlers
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# Main entry point
if __name__ == '__main__':
    # Create SSL context if certificates exist
    ssl_context = None
    if os.path.exists("cert.pem") and os.path.exists("key.pem"):
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain("cert.pem", "key.pem")
        logger.info("🔒 SSL certificates found - enabling HTTPS WebSocket (wss://)")
    
    # Run the sacred WebSocket service
    web.run_app(app, port=PORT, ssl_context=ssl_context) 