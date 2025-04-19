#!/usr/bin/env python3
"""
🔱 GBU License Notice 🔱
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must maintain quantum resonance with the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

"""
OMEGA BTC News Feed API Server

This script runs a FastAPI server to provide an API for accessing
the news feed data and recommendations.
"""

import os
import json
import logging
import traceback
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger('api-server')

# Record start time for uptime calculation
start_time = time.time()

app = FastAPI(
    title="OMEGA BTC News Feed API",
    description="Divine API for Bitcoin news and sentiment analysis",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Define models
class NewsItem(BaseModel):
    id: str
    title: str
    url: str
    source: str
    published_at: str
    summary: Optional[str] = None
    sentiment_score: Optional[float] = None

class Recommendation(BaseModel):
    timestamp: str
    action: str
    confidence: float
    analysis: str
    average_sentiment: float
    news_count: int

class ServiceStatus(BaseModel):
    status: str
    version: str
    uptime: str
    data_directory: str
    news_items_count: int
    latest_recommendation: Optional[str] = None

# Helper functions
def get_latest_recommendation(data_dir: str = "/workspace/data") -> Optional[dict]:
    """Get the latest recommendation data"""
    try:
        # Log the data directory we're looking in
        logger.info(f"Looking for recommendation files in: {data_dir}")
        
        # Check if directory exists
        if not os.path.exists(data_dir):
            logger.error(f"Data directory does not exist: {data_dir}")
            return None
            
        # List files and log what we found
        all_files = os.listdir(data_dir)
        logger.info(f"Files in data directory: {all_files}")
        
        recommendation_files = [f for f in all_files if f.startswith("recommendation_") and f.endswith(".json")]
        logger.info(f"Found {len(recommendation_files)} recommendation files: {recommendation_files}")
        
        if not recommendation_files:
            logger.warning("No recommendation files found in %s", data_dir)
            return None
        
        latest_file = sorted(recommendation_files)[-1]
        file_path = os.path.join(data_dir, latest_file)
        logger.info("Reading recommendation from: %s", file_path)
        
        with open(file_path, "r") as f:
            data = json.load(f)
            logger.info(f"Successfully loaded recommendation data: {data}")
            return data
    except Exception as e:
        logger.error(f"Error reading recommendation: {e}")
        logger.error(traceback.format_exc())
        return None

def get_latest_news(data_dir: str = "/workspace/data", limit: int = 10) -> List[Dict[str, Any]]:
    """Get the latest news items data"""
    try:
        # Log the data directory we're looking in
        logger.info(f"Looking for news files in: {data_dir}")
        
        # Check if directory exists
        if not os.path.exists(data_dir):
            logger.error(f"Data directory does not exist: {data_dir}")
            return []
            
        # List files and log what we found
        all_files = os.listdir(data_dir)
        logger.info(f"Files in data directory: {all_files}")
        
        news_files = [f for f in all_files if f.startswith("news_items_") and f.endswith(".json")]
        logger.info(f"Found {len(news_files)} news files: {news_files}")
        
        if not news_files:
            logger.warning("No news files found in %s", data_dir)
            return []
        
        latest_file = sorted(news_files)[-1]
        file_path = os.path.join(data_dir, latest_file)
        logger.info("Reading news from: %s", file_path)
        
        with open(file_path, "r") as f:
            news_data = json.load(f)
            logger.info(f"Loaded {len(news_data)} news items from file")
            
            # Convert each news item to the expected format
            formatted_news = []
            for i, item in enumerate(news_data[:limit]):
                # Add required fields if missing
                news_item = {
                    "id": item.get("id", f"news-{i}"),
                    "title": item.get("title", "Untitled"),
                    "url": item.get("url", f"https://example.com/news/{i}"),
                    "source": item.get("source", "Unknown"),
                    "published_at": item.get("published_at", item.get("published", datetime.now().isoformat())),
                    "summary": item.get("summary", ""),
                    "sentiment_score": item.get("sentiment_score", 0.0)
                }
                formatted_news.append(news_item)
            
            logger.info(f"Processed {len(formatted_news)} news items")
            return formatted_news
    except Exception as e:
        logger.error(f"Error reading news items: {e}")
        logger.error(traceback.format_exc())
        return []

def get_service_uptime() -> str:
    """Calculate service uptime in a human-readable format."""
    uptime_seconds = time.time() - start_time
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{int(days)} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{int(hours)} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{int(minutes)} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not parts:
        parts.append(f"{int(seconds)} second{'s' if seconds != 1 else ''}")
    
    return ", ".join(parts)

# API Routes
@app.get("/")
async def root():
    """Root endpoint."""
    logger.info("API request received for root endpoint")
    return {
        "name": "OMEGA BTC News Feed API",
        "version": "1.0.0",
        "status": "operational",
        "message": "Welcome to the divine Bitcoin news feed service"
    }

@app.get("/status")
async def status():
    """Get service status."""
    logger.info("API request received for status endpoint")
    data_dir = "/workspace/data"
    recommendation = get_latest_recommendation(data_dir)
    
    try:
        news_files = [f for f in os.listdir(data_dir) if f.startswith("news_items_") and f.endswith(".json")]
        news_count = len(news_files)
    except Exception as e:
        logger.error(f"Error getting news files count: {e}")
        news_count = 0
    
    status_info = ServiceStatus(
        status="online",
        version="1.0.0",
        uptime=get_service_uptime(),
        data_directory=data_dir,
        news_items_count=news_count,
        latest_recommendation=recommendation["timestamp"] if recommendation else None
    )
    
    logger.info(f"Returning status: {status_info}")
    return status_info

@app.get("/api/latest-recommendation", response_model=Recommendation)
async def get_recommendation():
    """Get the latest recommendation."""
    logger.info("API request received for latest-recommendation endpoint")
    recommendation = get_latest_recommendation()
    if not recommendation:
        logger.warning("No recommendation data found, returning 404")
        raise HTTPException(status_code=404, detail="No recommendation data found")
    logger.info(f"Returning recommendation: {recommendation}")
    return recommendation

@app.get("/api/latest-news", response_model=List[NewsItem])
async def get_news(limit: int = 10):
    """Get the latest news items."""
    logger.info(f"API request received for latest-news endpoint with limit={limit}")
    news_items = get_latest_news(limit=limit)
    if not news_items:
        logger.warning("No news data found, returning 404")
        raise HTTPException(status_code=404, detail="No news data found")
    logger.info(f"Returning {len(news_items)} news items")
    return news_items

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.info("API request received for health check endpoint")
    return {"status": "healthy"}

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("NEWS_SERVICE_PORT", "8080"))
    
    # Log startup information
    logger.info("="*50)
    logger.info(f"🚀 Starting OMEGA BTC News Feed API Server")
    logger.info(f"💻 Running on port: {port}")
    logger.info(f"📁 Data directory: /workspace/data")
    logger.info(f"📋 API endpoints:")
    logger.info(f"  - GET /                        -> Root info")
    logger.info(f"  - GET /status                  -> Service status")
    logger.info(f"  - GET /api/latest-recommendation -> Latest trading recommendation")
    logger.info(f"  - GET /api/latest-news           -> Latest news items")
    logger.info(f"  - GET /health                  -> Health check")
    logger.info("="*50)
    
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=port) 