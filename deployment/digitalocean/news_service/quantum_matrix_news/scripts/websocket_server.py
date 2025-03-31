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
import time
import asyncio
import logging
import random
import hashlib
import datetime
from aiohttp import web
import socketio
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("matrix-news-websocket")

# Configuration from environment variables
PORT = int(os.environ.get("PORT", 10091))
FETCH_INTERVAL = int(os.environ.get("FETCH_INTERVAL", 30))

# Create a Socket.IO server
sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

# Mock news headlines for streaming updates
HEADLINES = [
    "Bitcoin Surges to New Heights as Institutional Adoption Accelerates",
    "Ethereum 2.0 Upgrade Completes Successfully, Gas Fees Plummet",
    "Central Banks Worldwide Exploring CBDC Options in Response to Crypto Growth",
    "Major Financial Institution Announces Bitcoin Custody Services",
    "NFT Market Shows Signs of Revival with New Use Cases",
    "Regulatory Clarity Emerges as EU Finalizes Comprehensive Crypto Framework",
    "DeFi Total Value Locked Reaches New All-Time High, Surpassing $150B",
    "Bitcoin Mining Difficulty Increases to Record Levels Following Hash Rate Surge",
    "Layer 2 Solutions See Exponential Growth in User Adoption",
    "Quantum Computing Advances Raise Questions About Blockchain Security",
    "Lightning Network Capacity Doubles in Six Months as Bitcoin Scaling Solution Gains Traction",
    "Corporate Treasury Allocations to Bitcoin Continue Trend as Inflation Hedge",
    "Decentralized Social Media Platforms Gain Users Amid Censorship Concerns",
    "Bitcoin ETF Trading Volume Surpasses Expectations in First Quarter",
    "Crypto Payment Solutions See Widespread Merchant Adoption",
    "Zero-Knowledge Proofs Enhance Privacy Features Across Multiple Blockchains",
    "Cross-Chain Bridges Improve Security Following Previous Exploits",
    "AI Integration with Blockchain Creates New Market Opportunities",
    "Nation States Continue Bitcoin Accumulation Strategy",
    "Metaverse Land Sales Increase as Major Brands Establish Virtual Presence"
]

# Mock price data for market updates
PRICE_DATA = {
    "BTC": {"price": 120000, "change_24h": 2.5},
    "ETH": {"price": 8500, "change_24h": 3.1},
    "BNB": {"price": 750, "change_24h": 1.8},
    "SOL": {"price": 320, "change_24h": 4.2},
    "ADA": {"price": 2.1, "change_24h": 2.9}
}

# Initialize rooms dict if it doesn't exist
clients = {}
rooms = {}

# Generate quantum entropy for sacred messages
def generate_quantum_entropy():
    timestamp = time.time()
    entropy_input = f"{timestamp}_{random.getrandbits(128)}"
    return hashlib.sha256(entropy_input.encode()).hexdigest()[:16]

# Routes
@sio.event
async def connect(sid, environ):
    logger.info(f"Client connected: {sid}")
    await sio.emit('welcome', {'message': 'Welcome to the Matrix Neo News WebSocket'}, room=sid)

@sio.event
async def disconnect(sid):
    logger.info(f"Client disconnected: {sid}")

@sio.event
async def set_consciousness_level(sid, data):
    logger.info(f"Client {sid} set consciousness level to {data.get('level', 5)}")
    await sio.emit('consciousness_set', {'status': 'success', 'level': data.get('level', 5)}, room=sid)

@sio.event
async def get_participants(sid, data):
    room = data.get('room')
    if not room:
        await sio.emit('error', {"message": "Room name is required"}, room=sid)
        return []
    
    if room in rooms:
        return list(rooms[room])
    return []

# Health check route - main health endpoint
async def health_endpoint(request):
    try:
        # Get system metrics
        process = psutil.Process()
        memory_info = process.memory_info()
        cpu_percent = process.cpu_percent()
        
        # Get WebSocket metrics
        active_connections = len(clients)
        active_rooms = len(rooms)
        
        # Calculate uptime
        uptime = time.time() - process.create_time()
        
        # Get background task status
        news_broadcaster_status = "running" if 'news_broadcaster' in request.app else "stopped"
        market_broadcaster_status = "running" if 'market_broadcaster' in request.app else "stopped"
        
        return web.json_response({
            "status": "UP",
            "service": "matrix-news-websocket",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "metrics": {
                "clients_connected": active_connections,
                "active_rooms": active_rooms,
                "memory_usage_mb": round(memory_info.rss / (1024 * 1024), 2),
                "cpu_percent": cpu_percent,
                "uptime_seconds": round(uptime, 2)
            },
            "background_tasks": {
                "news_broadcaster": news_broadcaster_status,
                "market_broadcaster": market_broadcaster_status
            },
            "version": "1.0.0"  # Add version information
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return web.json_response({
            "status": "ERROR",
            "service": "matrix-news-websocket",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "error": str(e)
        }, status=500)

# WebSocket specific health endpoint for NGINX
async def ws_health_endpoint(request):
    try:
        # Basic health check for NGINX
        return web.json_response({
            'status': 'ok', 
            'service': 'matrix-news-websocket', 
            'timestamp': time.time(),
            'clients_connected': len(clients)
        })
    except Exception as e:
        logger.error(f"WebSocket health check error: {e}")
        return web.json_response({
            'status': 'error',
            'service': 'matrix-news-websocket',
            'error': str(e)
        }, status=500)

# Background task to emit news updates
async def news_broadcaster():
    """Broadcasts news updates to all connected clients"""
    while True:
        try:
            # Generate a news update
            headline = random.choice(HEADLINES)
            source = random.choice(["Crypto Matrix News", "Blockchain Observer", "Digital Asset Report", "Quantum Finance"])
            sentiment = round(random.uniform(0.3, 0.9), 2)
            
            # Create news update
            news_update = {
                "headline": headline,
                "source": source,
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "sentiment": sentiment,
                "id": generate_quantum_entropy()
            }
            
            logger.info(f"Broadcasting news update: {headline}")
            await sio.emit('news_update', news_update)
            
            # Wait for the next interval
            await asyncio.sleep(FETCH_INTERVAL)
        except Exception as e:
            logger.error(f"Error in news broadcaster: {e}")
            await asyncio.sleep(5)  # Short wait before retrying

# Background task to emit market updates
async def market_data_broadcaster():
    """Broadcasts market data updates to all connected clients"""
    while True:
        try:
            # Update mock price data
            for coin in PRICE_DATA:
                # Random price movement (-2% to +2%)
                change_pct = random.uniform(-2, 2)
                PRICE_DATA[coin]["price"] *= (1 + change_pct/100)
                PRICE_DATA[coin]["change_24h"] = round(random.uniform(-5, 5), 2)
            
            # Create market update
            market_update = {
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "data": PRICE_DATA,
                "trends": {
                    "short_term": random.choice(["bullish", "bearish", "neutral"]),
                    "mid_term": random.choice(["bullish", "bearish", "neutral"]),
                    "entropy": generate_quantum_entropy()
                }
            }
            
            logger.info("Broadcasting market update")
            await sio.emit('market_update', market_update)
            
            # Wait for the next interval (half of the news interval)
            await asyncio.sleep(FETCH_INTERVAL // 2)
        except Exception as e:
            logger.error(f"Error in market data broadcaster: {e}")
            await asyncio.sleep(5)  # Short wait before retrying

# Start the application
async def start_background_tasks(app):
    app['news_broadcaster'] = asyncio.create_task(news_broadcaster())
    app['market_broadcaster'] = asyncio.create_task(market_data_broadcaster())

async def cleanup_background_tasks(app):
    app['news_broadcaster'].cancel()
    app['market_broadcaster'].cancel()
    await app['news_broadcaster']
    await app['market_broadcaster']

app.router.add_get('/health', health_endpoint)
app.router.add_get('/ws/health', ws_health_endpoint)
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)

if __name__ == '__main__':
    logger.info(f"Starting Matrix News WebSocket Server on port {PORT}")
    
    # Create a health check app for port 10095
    health_app = web.Application()
    
    # Add health check routes to the health app
    health_app.router.add_get('/health', health_endpoint)
    health_app.router.add_get('/ws/health', ws_health_endpoint)
    
    # Start both servers
    runner = web.AppRunner(health_app)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runner.setup())
    
    # Start health server on port 10095
    health_site = web.TCPSite(runner, '0.0.0.0', 10095)
    loop.run_until_complete(health_site.start())
    logger.info(f"Health check server started on port 10095")
    
    # Start main server on port 10091
    web.run_app(app, port=PORT, access_log=None) 