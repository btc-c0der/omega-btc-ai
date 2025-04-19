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
OMEGA BTC News Feed API Proxy

This script runs a simple FastAPI server to proxy requests to the
actual API server, handling the /api/ prefix routing.
"""

import os
import logging
import httpx
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger('api-proxy')

# Define FastAPI app
app = FastAPI(
    title="OMEGA BTC News Feed API Proxy",
    description="Proxy for Bitcoin news and sentiment analysis API",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base URL of the API server
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8080")
logger.info(f"Using API base URL: {API_BASE_URL}")

# Create httpx client
client = httpx.AsyncClient(base_url=API_BASE_URL, timeout=30.0)

@app.on_event("shutdown")
async def shutdown_event():
    """Close httpx client on shutdown."""
    await client.aclose()

@app.get("/api/latest-recommendation")
async def proxy_latest_recommendation():
    """Proxy for the latest recommendation endpoint."""
    try:
        logger.info(f"Proxying request to {API_BASE_URL}/latest-recommendation")
        response = await client.get("/latest-recommendation")
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except Exception as e:
        logger.error(f"Error proxying request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/latest-news")
async def proxy_latest_news():
    """Proxy for the latest news endpoint."""
    try:
        logger.info(f"Proxying request to {API_BASE_URL}/latest-news")
        response = await client.get("/latest-news")
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except Exception as e:
        logger.error(f"Error proxying request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    logger.info("Health check request received")
    try:
        response = await client.get("/health")
        if response.status_code == 200:
            return {"status": "healthy", "api_server": "healthy"}
        else:
            return {"status": "degraded", "api_server": "unhealthy"}
    except Exception as e:
        logger.error(f"API server health check failed: {e}")
        return {"status": "degraded", "api_server": "unreachable", "error": str(e)}

@app.get("/")
async def root():
    """Root endpoint."""
    logger.info("Root request received")
    return {
        "name": "OMEGA BTC News Feed API Proxy",
        "version": "1.0.0",
        "status": "operational"
    }

# Forward all other requests to the API server
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(request: Request, path: str):
    """Catch-all route to forward all other requests to the API server."""
    url = f"/{path}"
    logger.info(f"Forwarding request to {API_BASE_URL}{url}")
    
    try:
        method = request.method.lower()
        request_kwargs = {
            "method": method,
            "url": url,
            "headers": {k: v for k, v in request.headers.items() if k.lower() != "host"},
        }
        
        if method in ["post", "put", "patch"]:
            body = await request.body()
            if body:
                request_kwargs["content"] = body
                
        response = await client.request(**request_kwargs)
        
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
    except Exception as e:
        logger.error(f"Error forwarding request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PROXY_PORT", "5000"))
    
    # Log startup information
    logger.info("="*50)
    logger.info(f"🚀 Starting OMEGA BTC News Feed API Proxy")
    logger.info(f"💻 Running on port: {port}")
    logger.info(f"🔌 Proxying to: {API_BASE_URL}")
    logger.info(f"📋 Main endpoints:")
    logger.info(f"  - GET /                    -> Root info")
    logger.info(f"  - GET /api/latest-recommendation -> Latest trading recommendation")
    logger.info(f"  - GET /api/latest-news     -> Latest news items")
    logger.info(f"  - GET /health              -> Health check")
    logger.info("="*50)
    
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=port) 