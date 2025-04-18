#!/usr/bin/env python

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

import redis
import time
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, RedirectResponse, HTMLResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="\033[1;36m%(asctime)s\033[0m \033[1;33m%(levelname)s\033[0m \033[1;35m%(name)s\033[0m: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("redis-monitor")

# Initialize FastAPI
app = FastAPI(title="Redis Monitor API", version="2.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Template for the root page with a more polished look
ROOT_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Redis Monitor</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #1a73e8;
            margin-top: 0;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        .endpoint {
            background-color: #f8f9fa;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
            border-left: 4px solid #1a73e8;
        }
        .endpoint h3 {
            margin-top: 0;
            color: #1a73e8;
        }
        pre {
            background-color: #f1f1f1;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
        .badge {
            display: inline-block;
            padding: 3px 7px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
            background-color: #e6f4ea;
            color: #137333;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Redis Monitor API <span class="badge">Running</span></h1>
        
        <p>This service provides monitoring of the Redis database with performance optimizations for large datasets.</p>
        
        <h2>Available Endpoints:</h2>
        
        <div class="endpoint">
            <h3>/api/health</h3>
            <p>Check the health and connectivity status of the Redis service.</p>
            <pre>GET /api/health</pre>
        </div>
        
        <div class="endpoint">
            <h3>/api/redis-info</h3>
            <p>Get general information about the Redis instance.</p>
            <pre>GET /api/redis-info</pre>
        </div>
        
        <div class="endpoint">
            <h3>/api/redis-keys</h3>
            <p>Get a sample of keys from Redis with their types and additional information.</p>
            <pre>GET /api/redis-keys?limit=20&pattern=*</pre>
            <p>Parameters:</p>
            <ul>
                <li><code>limit</code>: Maximum number of keys to return (default: 20)</li>
                <li><code>pattern</code>: Pattern to filter keys (default: *)</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

def test_redis_connection() -> bool:
    """Test if Redis is connected."""
    try:
        return redis_client.ping()
    except redis.exceptions.ConnectionError:
        return False

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with basic information."""
    return HTMLResponse(content=ROOT_PAGE_TEMPLATE)

@app.get("/api/health")
async def health_check():
    """Check Redis connection status."""
    start_time = time.time()
    is_connected = test_redis_connection()
    response_time = time.time() - start_time
    
    logger.info(f"Health check: Redis connected={is_connected}, response_time={response_time:.4f}s")
    
    return {
        "status": "healthy" if is_connected else "unhealthy",
        "connected": is_connected,
        "response_time": f"{response_time:.4f}s"
    }

@app.get("/api/redis-info")
async def redis_info():
    """Get Redis server information."""
    try:
        start_time = time.time()
        
        if not test_redis_connection():
            logger.error("Redis connection failed during info request")
            raise HTTPException(status_code=503, detail="Redis connection failed")
        
        info = redis_client.info()
        dbsize = redis_client.dbsize()
        
        # Extract useful information
        redis_version = info.get('redis_version', 'Unknown')
        uptime_days = info.get('uptime_in_days', 0)
        used_memory_human = info.get('used_memory_human', 'Unknown')
        connected_clients = info.get('connected_clients', 0)
        
        response_time = time.time() - start_time
        logger.info(f"Redis info request completed in {response_time:.4f}s")
        
        return {
            "status": "success",
            "info": {
                "version": redis_version,
                "uptime_days": uptime_days,
                "memory_usage": used_memory_human,
                "connected_clients": connected_clients,
                "total_keys": dbsize
            },
            "response_time": f"{response_time:.4f}s"
        }
    except Exception as e:
        logger.error(f"Error getting Redis info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting Redis info: {str(e)}")

@app.get("/api/redis-keys")
async def get_redis_keys(limit: int = 20, pattern: str = "*"):
    """
    Get a sample of Redis keys with type information.
    Uses scan for efficiency with large databases.
    """
    try:
        start_time = time.time()
        
        if not test_redis_connection():
            logger.error("Redis connection failed during keys request")
            raise HTTPException(status_code=503, detail="Redis connection failed")
        
        # Limit the number of keys to prevent performance issues
        if limit > 100:
            limit = 100
            logger.warning(f"Requested limit too high, capped at {limit}")
        
        # Initialize counters and result containers
        sample_keys = []
        cursor = 0
        scanned = 0
        max_scan = 10000  # Limit scanning to protect performance
        
        logger.info(f"Scanning Redis for keys matching pattern '{pattern}', limit={limit}")
        
        # Use scan instead of keys for efficiency with large DBs
        while len(sample_keys) < limit and (cursor != 0 or scanned == 0) and scanned < max_scan:
            cursor, keys = redis_client.scan(cursor=cursor, match=pattern, count=min(limit * 5, 1000))
            
            if not keys:
                continue
                
            # Add keys to our sample
            for key in keys[:limit - len(sample_keys)]:
                sample_keys.append(key)
                if len(sample_keys) >= limit:
                    break
            
            scanned += len(keys)
            
            # Safety check
            if scanned >= max_scan and len(sample_keys) < limit:
                logger.warning(f"Scan limit reached after {scanned} keys, returning partial results")
                break
        
        # No keys found
        if not sample_keys:
            logger.warning(f"No keys found matching pattern '{pattern}' after scanning {scanned} keys")
            return {
                "status": "success",
                "keys": [],
                "total_scanned": scanned,
                "total_returned": 0,
                "response_time": f"{time.time() - start_time:.4f}s"
            }
        
        # Get information about the keys
        keys_info = []
        for key in sample_keys:
            try:
                key_type = redis_client.type(key)
                key_info = {"key": key, "type": key_type}
                
                # Add type-specific information
                if key_type == "string":
                    value = redis_client.get(key)
                    # For binary or very large values, just show a placeholder
                    if value is None:
                        key_info["value"] = "(None)"
                    elif len(value) > 100:
                        key_info["value"] = f"{value[:100]}... (truncated, {len(value)} bytes)"
                    else:
                        key_info["value"] = value
                        
                elif key_type == "list":
                    key_info["length"] = redis_client.llen(key)
                    # Sample a few elements
                    key_info["sample"] = redis_client.lrange(key, 0, 2)
                    
                elif key_type == "hash":
                    key_info["size"] = redis_client.hlen(key)
                    # Sample a few fields
                    sample_data = {}
                    for field, value in list(redis_client.hscan_iter(key, count=3)):
                        sample_data[field] = value
                        if len(sample_data) >= 3:
                            break
                    key_info["sample"] = sample_data
                    
                elif key_type == "set":
                    key_info["size"] = redis_client.scard(key)
                    # Sample a few members
                    members = []
                    for member in redis_client.sscan_iter(key, count=3):
                        members.append(member)
                        if len(members) >= 3:
                            break
                    key_info["sample"] = members
                    
                elif key_type == "zset":
                    key_info["size"] = redis_client.zcard(key)
                    # Sample a few members with scores
                    key_info["sample"] = redis_client.zrange(key, 0, 2, withscores=True)
                
                # Add expiration information if available
                ttl = redis_client.ttl(key)
                if ttl > 0:
                    key_info["ttl"] = ttl
                    key_info["expires_in"] = f"{ttl} seconds"
                
                keys_info.append(key_info)
            except Exception as e:
                # Log the error but continue processing other keys
                logger.error(f"Error processing key '{key}': {str(e)}")
                keys_info.append({"key": key, "error": str(e)})
        
        response_time = time.time() - start_time
        logger.info(f"Redis keys request completed in {response_time:.4f}s, returned {len(keys_info)} keys")
        
        return {
            "status": "success",
            "keys": keys_info,
            "total_scanned": scanned,
            "total_returned": len(keys_info),
            "response_time": f"{response_time:.4f}s"
        }
        
    except Exception as e:
        logger.error(f"Error getting Redis keys: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting Redis keys: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Redis Monitor Server...")
    logger.info("Checking Redis connection...")
    
    if test_redis_connection():
        logger.info("✓ Successfully connected to Redis")
        logger.info(f"Total keys in Redis: {redis_client.dbsize()}")
    else:
        logger.error("✗ Failed to connect to Redis")
    
    logger.info("Starting server on http://0.0.0.0:5002")
    uvicorn.run("redis_monitor_server_optimized:app", host="0.0.0.0", port=5002) 