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
import uvicorn
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True
)

# Create FastAPI app
app = FastAPI()

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

# Define API endpoints for different news sources
NEWS_APIS = {
    "cryptopanic": {
        "url": "https://cryptopanic.com/api/v1/posts/",
        "params": {
            "auth_token": os.environ.get("CRYPTOPANIC_API_KEY", ""),
            "public": "true",
            "kind": "news",
            "filter": "hot",
            "currencies": "BTC,ETH"
        },
        "enabled": True
    },
    "newsapi": {
        "url": "https://newsapi.org/v2/everything",
        "params": {
            "apiKey": os.environ.get("NEWSAPI_API_KEY", ""),
            "q": "bitcoin OR cryptocurrency OR blockchain",
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": 10
        },
        "enabled": os.environ.get("NEWSAPI_API_KEY", "") != ""
    },
    "coinpaprika": {
        "url": "https://api.coinpaprika.com/v1/coins/btc-bitcoin/events",
        "params": {},
        "enabled": True
    },
    "coingecko": {
        "url": "https://api.coingecko.com/api/v3/news",
        "params": {},
        "enabled": True
    }
}

# Sample news data for demonstration purposes when APIs aren't available
SAMPLE_NEWS = [
    {
        "id": "sample-1",
        "title": "Bitcoin Surges Past $90,000 as Financial Institutions Increase Cryptocurrency Holdings",
        "content": "Bitcoin surged past the $90,000 mark today, setting a new all-time high as several major financial institutions announced increases to their cryptocurrency holdings. Analysts suggest this could be the beginning of a new adoption wave.",
        "published_at": "2025-03-31T12:30:00Z",
        "source": "Matrix Financial News",
        "url": "https://example.com/bitcoin-surge",
        "sentiment": "positive"
    },
    {
        "id": "sample-2",
        "title": "New Quantum-Resistant Blockchain Protocol Announces Successful Test Network",
        "content": "A new blockchain protocol designed to be resistant to quantum computing attacks has announced the successful launch of its test network. The development could address one of the primary security concerns for cryptocurrency in the coming years.",
        "published_at": "2025-03-31T11:15:00Z",
        "source": "Crypto Quantum Insights",
        "url": "https://example.com/quantum-resistant",
        "sentiment": "positive"
    },
    {
        "id": "sample-3",
        "title": "Regulatory Agencies Worldwide Form Coalition to Create Unified Cryptocurrency Framework",
        "content": "Regulatory agencies from 24 countries have announced the formation of a coalition aimed at creating a unified framework for cryptocurrency regulation. The move is expected to reduce regulatory uncertainty that has plagued the industry.",
        "published_at": "2025-03-31T09:45:00Z",
        "source": "Global Regulatory Report",
        "url": "https://example.com/unified-crypto-framework",
        "sentiment": "neutral"
    },
    {
        "id": "sample-4",
        "title": "Major Vulnerability Discovered in Popular DeFi Protocol",
        "content": "Security researchers have discovered a critical vulnerability in a popular DeFi protocol that could potentially lead to significant fund losses. The protocol's developers are working on an emergency patch.",
        "published_at": "2025-03-31T10:20:00Z",
        "source": "DeFi Security Alert",
        "url": "https://example.com/defi-vulnerability",
        "sentiment": "negative"
    },
    {
        "id": "sample-5",
        "title": "Bitcoin Mining Now Using 70% Renewable Energy, Study Finds",
        "content": "A comprehensive study has found that Bitcoin mining operations now use approximately 70% renewable energy sources, challenging the narrative that cryptocurrency mining is environmentally harmful.",
        "published_at": "2025-03-31T08:30:00Z", 
        "source": "Sustainable Crypto Initiative",
        "url": "https://example.com/bitcoin-renewable-energy",
        "sentiment": "positive"
    }
]

last_news_update = datetime.datetime.now() - datetime.timedelta(minutes=10)
news_cache = []

# Create a static health endpoint
@app.get("/health")
async def health():
    return {"status": "UP", "service": "websocket-minimal", "timestamp": datetime.datetime.now().isoformat()}

# Socket.IO events
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('welcome', {"message": "Welcome to the Matrix Neo News Portal"}, room=sid)

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def subscribe_news(sid, data):
    print(f"Client {sid} subscribed to news: {data}")
    
    # Send cached news if available
    if news_cache:
        for news_item in news_cache[:5]:  # Send the 5 most recent items
            await sio.emit('news_update', news_item, room=sid)
    else:
        # Send a sample news item if cache is empty
        sample_news = random.choice(SAMPLE_NEWS)
        await sio.emit('news_update', sample_news, room=sid)

async def fetch_crypto_panic_news():
    """Fetch news from CryptoPanic API"""
    api_config = NEWS_APIS["cryptopanic"]
    if not api_config["enabled"]:
        return []
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_config["url"], params=api_config["params"]) as response:
                if response.status == 200:
                    data = await response.json()
                    results = []
                    for item in data.get("results", []):
                        news_item = {
                            "id": f"cryptopanic-{item.get('id')}",
                            "title": item.get("title"),
                            "content": item.get("title"),  # CryptoPanic doesn't provide full content
                            "published_at": item.get("published_at"),
                            "source": item.get("source", {}).get("title", "CryptoPanic"),
                            "url": item.get("url"),
                            "sentiment": item.get("votes", {}).get("sentiment", "neutral")
                        }
                        results.append(news_item)
                    return results
                else:
                    print(f"Error fetching from CryptoPanic: {response.status}")
                    return []
    except Exception as e:
        print(f"Exception fetching CryptoPanic news: {e}")
        return []

async def fetch_newsapi_news():
    """Fetch news from NewsAPI"""
    api_config = NEWS_APIS["newsapi"]
    if not api_config["enabled"]:
        return []
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_config["url"], params=api_config["params"]) as response:
                if response.status == 200:
                    data = await response.json()
                    results = []
                    for item in data.get("articles", []):
                        # Simple sentiment analysis based on title
                        sentiment = "neutral"
                        positive_words = ["surge", "rally", "gain", "rise", "soar", "positive", "bullish", "up", "high"]
                        negative_words = ["crash", "fall", "drop", "plunge", "bearish", "negative", "down", "low", "risk"]
                        
                        title_lower = item.get("title", "").lower()
                        if any(word in title_lower for word in positive_words):
                            sentiment = "positive"
                        elif any(word in title_lower for word in negative_words):
                            sentiment = "negative"
                        
                        news_item = {
                            "id": f"newsapi-{hash(item.get('url', ''))}",
                            "title": item.get("title"),
                            "content": item.get("description") or item.get("title"),
                            "published_at": item.get("publishedAt"),
                            "source": item.get("source", {}).get("name", "NewsAPI"),
                            "url": item.get("url"),
                            "sentiment": sentiment
                        }
                        results.append(news_item)
                    return results
                else:
                    print(f"Error fetching from NewsAPI: {response.status}")
                    return []
    except Exception as e:
        print(f"Exception fetching NewsAPI news: {e}")
        return []

async def fetch_coinpaprika_events():
    """Fetch Bitcoin events from Coinpaprika"""
    api_config = NEWS_APIS["coinpaprika"]
    if not api_config["enabled"]:
        return []
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_config["url"], params=api_config["params"]) as response:
                if response.status == 200:
                    data = await response.json()
                    results = []
                    for item in data:
                        # Skip events in the past
                        if not item.get("date_to"):
                            continue
                        
                        event_date = datetime.datetime.fromisoformat(item.get("date_to").replace("Z", "+00:00"))
                        if event_date < datetime.datetime.now(datetime.timezone.utc):
                            continue
                            
                        news_item = {
                            "id": f"coinpaprika-event-{item.get('id')}",
                            "title": f"Bitcoin Event: {item.get('name')}",
                            "content": item.get("description") or "Upcoming Bitcoin event",
                            "published_at": datetime.datetime.now().isoformat(),
                            "source": "Coinpaprika Events",
                            "url": item.get("link"),
                            "sentiment": "neutral",
                            "event_date": item.get("date_to")
                        }
                        results.append(news_item)
                    return results
                else:
                    print(f"Error fetching from Coinpaprika: {response.status}")
                    return []
    except Exception as e:
        print(f"Exception fetching Coinpaprika events: {e}")
        return []

async def fetch_coingecko_news():
    """Fetch news from CoinGecko"""
    api_config = NEWS_APIS["coingecko"]
    if not api_config["enabled"]:
        return []
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_config["url"], params=api_config["params"]) as response:
                if response.status == 200:
                    data = await response.json()
                    results = []
                    
                    if not isinstance(data, list):
                        data = data.get("data", [])
                        
                    for item in data:
                        news_item = {
                            "id": f"coingecko-{hash(item.get('url', ''))}",
                            "title": item.get("title"),
                            "content": item.get("description", ""),
                            "published_at": item.get("published_at") or datetime.datetime.now().isoformat(),
                            "source": "CoinGecko News",
                            "url": item.get("url"),
                            "sentiment": "neutral"
                        }
                        results.append(news_item)
                    return results
                else:
                    print(f"Error fetching from CoinGecko: {response.status}")
                    return []
    except Exception as e:
        print(f"Exception fetching CoinGecko news: {e}")
        return []

async def fetch_all_news():
    """Fetch news from all configured sources"""
    global news_cache, last_news_update
    
    # Check if we should update the cache (every 5 minutes)
    now = datetime.datetime.now()
    if (now - last_news_update).total_seconds() < 300:
        return news_cache
        
    print(f"Fetching fresh news at {now.isoformat()}")
    
    # Fetch news from all sources concurrently
    tasks = [
        fetch_crypto_panic_news(),
        fetch_newsapi_news(),
        fetch_coinpaprika_events(),
        fetch_coingecko_news()
    ]
    
    results = await asyncio.gather(*tasks)
    
    # Flatten and sort by published_at
    all_news = []
    for source_news in results:
        all_news.extend(source_news)
    
    # If we got no results from APIs, use sample news
    if not all_news:
        print("No news from APIs, using sample news")
        all_news = SAMPLE_NEWS
    
    # Sort by published_at (most recent first)
    all_news.sort(key=lambda x: x.get("published_at", ""), reverse=True)
    
    # Update cache and timestamp
    news_cache = all_news
    last_news_update = now
    
    return all_news

async def broadcast_news_updates():
    """Periodically fetch and broadcast news updates to all clients"""
    while True:
        try:
            # Fetch all news
            news_items = await fetch_all_news()
            
            if news_items:
                # Broadcast the most recent news item to all connected clients
                latest_news = news_items[0]
                print(f"Broadcasting news: {latest_news['title']}")
                await sio.emit('news_update', latest_news)
            
            # Send a heartbeat to all clients
            await sio.emit('heartbeat', {
                "type": "heartbeat",
                "timestamp": datetime.datetime.now().isoformat()
            })
            
            # Wait before next update (30 seconds)
            await asyncio.sleep(30)
        except Exception as e:
            print(f"Error in news broadcast: {e}")
            await asyncio.sleep(10)  # Shorter wait on error

@sio.event
async def get_latest_news(sid, data=None):
    """Send the latest news items to the requesting client"""
    news_items = await fetch_all_news()
    
    # Limit to 10 most recent items
    for item in news_items[:10]:
        await sio.emit('news_update', item, room=sid)

@app.on_event("startup")
async def startup_event():
    """Start background tasks when the application starts"""
    sio.start_background_task(broadcast_news_updates)

# Run the app directly if invoked
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10095"))
    uvicorn.run("websocket_minimal:app", host="0.0.0.0", port=port, reload=True) 