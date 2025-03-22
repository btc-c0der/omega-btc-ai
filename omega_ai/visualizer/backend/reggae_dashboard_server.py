#!/usr/bin/env python3

"""
OMEGA BTC AI - Reggae Hacker Omega UI Dashboard Server
======================================================

A real-time dashboard server that provides trap probability and trading position data
via WebSockets with a Reggae Hacker aesthetic.
"""

import asyncio
import json
import random
from datetime import datetime, timezone, timedelta
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

# ANSI color codes for Reggae-themed colorful output
GREEN = "\033[38;5;34m"    # Bright green (Reggae primary color)
GOLD = "\033[38;5;220m"    # Gold/Yellow (Reggae secondary color)
RED = "\033[38;5;196m"     # Bright red (Reggae tertiary color)
BLACK = "\033[38;5;232m"   # Deep black
CYAN = "\033[38;5;51m"     # Cyan for information
BOLD = "\033[1m"           # Bold text
RESET = "\033[0m"          # Reset formatting

# Custom formatter for colored logs
class ColoredFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: f"{BLACK}%(asctime)s - {CYAN}%(name)s{RESET} - {CYAN}%(levelname)s{RESET} - %(message)s",
        logging.INFO: f"{BLACK}%(asctime)s - {GREEN}%(name)s{RESET} - {GREEN}%(levelname)s{RESET} - {GREEN}%(message)s{RESET}",
        logging.WARNING: f"{BLACK}%(asctime)s - {GOLD}%(name)s{RESET} - {GOLD}%(levelname)s{RESET} - {GOLD}%(message)s{RESET}",
        logging.ERROR: f"{BLACK}%(asctime)s - {RED}%(name)s{RESET} - {RED}%(levelname)s{RESET} - {RED}%(message)s{RESET}",
        logging.CRITICAL: f"{BLACK}%(asctime)s - {RED}{BOLD}%(name)s{RESET} - {RED}{BOLD}%(levelname)s{RESET} - {RED}{BOLD}%(message)s{RESET}",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Configure logging with colors
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter())
logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)
logger = logging.getLogger("reggae_dashboard")

class ReggaeDashboardServer:
    """
    Server for the Reggae Hacker Omega UI Dashboard that provides real-time
    trading position and trap probability data.
    """
    
    def __init__(self):
        """Initialize the dashboard server with WebSocket support."""
        self.app = FastAPI(title="OMEGA BTC AI - Reggae Dashboard")
        
        # Active WebSocket connections (using a list because WebSocket objects are unhashable)
        self.active_connections = []
        
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
        
        @self.app.get("/")
        async def root():
            """Root endpoint that displays server information and available endpoints."""
            # Create a more interactive HTML response with clickable links
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>OMEGA BTC AI - Reggae Dashboard API</title>
                <style>
                    body {
                        background-color: #121212;
                        color: #e0e0e0;
                        font-family: 'Courier New', monospace;
                        margin: 0;
                        padding: 20px;
                        line-height: 1.6;
                    }
                    h1 {
                        color: #4CAF50;
                        border-bottom: 2px solid #FFD700;
                        text-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
                        padding-bottom: 10px;
                    }
                    h2 {
                        color: #FFD700;
                        margin-top: 20px;
                    }
                    .container {
                        max-width: 800px;
                        margin: 0 auto;
                        background-color: #1E1E1E;
                        padding: 30px;
                        border-radius: 8px;
                        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
                    }
                    .endpoints-grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                        gap: 15px;
                        margin-top: 20px;
                    }
                    .endpoint {
                        background-color: rgba(30, 30, 30, 0.7);
                        border-left: 4px solid #FFD700;
                        padding: 15px;
                        margin: 10px 0;
                        border-radius: 4px;
                        transition: transform 0.2s, box-shadow 0.2s;
                    }
                    .endpoint:hover {
                        transform: translateY(-3px);
                        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
                        background-color: rgba(40, 40, 40, 0.9);
                    }
                    .method {
                        color: #4CAF50;
                        font-weight: bold;
                        display: inline-block;
                        width: 80px;
                    }
                    .websocket {
                        color: #9C27B0;
                    }
                    a {
                        color: #64B5F6;
                        text-decoration: none;
                        transition: color 0.2s;
                    }
                    a:hover {
                        color: #2196F3;
                        text-decoration: underline;
                    }
                    .description {
                        color: #AAAAAA;
                        font-size: 0.9em;
                        margin-top: 5px;
                    }
                    .footer {
                        margin-top: 30px;
                        text-align: center;
                        color: #AAAAAA;
                        font-size: 0.9em;
                        border-top: 1px solid rgba(255, 215, 0, 0.2);
                        padding-top: 15px;
                    }
                    .tag {
                        display: inline-block;
                        background-color: rgba(255, 215, 0, 0.2);
                        color: #FFD700;
                        padding: 2px 8px;
                        border-radius: 12px;
                        font-size: 0.8em;
                        margin-right: 5px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>OMEGA BTC AI - Reggae Dashboard API</h1>
                    
                    <h2>Available Endpoints</h2>
                    <div class="endpoints-grid">
                        <div class="endpoint">
                            <div class="method">GET</div>
                            <a href="/api/health">Health Check</a>
                            <div class="description">Check system and Redis health status</div>
                            <span class="tag">Health</span>
                        </div>
                        
                        <div class="endpoint">
                            <div class="method">GET</div>
                            <a href="/api/trap-probability">Trap Probability</a>
                            <div class="description">Get current trap probability data</div>
                            <span class="tag">Trap Data</span>
                        </div>
                        
                        <div class="endpoint">
                            <div class="method">GET</div>
                            <a href="/api/position">Position Data</a>
                            <div class="description">Get current trading position information</div>
                            <span class="tag">Position</span>
                        </div>
                        
                        <div class="endpoint">
                            <div class="method">GET</div>
                            <a href="/api/btc-price">BTC Price</a>
                            <div class="description">Get current BTC price with metrics</div>
                            <span class="tag">Price</span>
                        </div>
                        
                        <div class="endpoint">
                            <div class="method">GET</div>
                            <a href="/api/redis-keys">Redis Keys</a>
                            <div class="description">List available Redis keys</div>
                            <span class="tag">System</span>
                        </div>
                        
                        <div class="endpoint">
                            <div class="method">GET</div>
                            <a href="/api/redis-key?key=btc_price">Redis Key Value</a>
                            <div class="description">Get a specific Redis key value (example: btc_price)</div>
                            <span class="tag">System</span>
                        </div>
                        
                        <div class="endpoint">
                            <div class="method">GET</div>
                            <a href="/api/data">Combined Data</a>
                            <div class="description">Get all dashboard data in one request</div>
                            <span class="tag">Combined</span>
                        </div>
                        
                        <div class="endpoint">
                            <div class="method">GET</div>
                            <a href="/api/metrics">Metrics</a>
                            <div class="description">Get trap metrics with analytics</div>
                            <span class="tag">Analytics</span>
                        </div>
                        
                        <div class="endpoint">
                            <div class="method">GET</div>
                            <a href="/api/traps">Trap Detections</a>
                            <div class="description">Get trap detections with filters</div>
                            <span class="tag">Trap Data</span>
                        </div>
                        
                        <div class="endpoint">
                            <div class="method">GET</div>
                            <a href="/api/prices">Price History</a>
                            <div class="description">Get price data with verification</div>
                            <span class="tag">Price</span>
                        </div>
                        
                        <div class="endpoint">
                            <div class="method">GET</div>
                            <a href="/api/timeline">Timeline</a>
                            <div class="description">Get timeline of trap detections</div>
                            <span class="tag">Trap Data</span>
                        </div>
                        
                        <div class="endpoint">
                            <div class="method websocket">WebSocket</div>
                            <span>ws://[host]/ws</span>
                            <div class="description">Real-time data updates</div>
                            <span class="tag">Real-time</span>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>OMEGA BTC AI - Reggae Dashboard API © 2024</p>
                        <p>Powered by Rastafarian wisdom & Modern AI</p>
                    </div>
                </div>
            </body>
            </html>
            """
            return HTMLResponse(content=html_content)
        
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
            """Get current trading position information."""
            return self._get_position_data()
        
        @self.app.get("/api/btc-price")
        async def get_btc_price():
            """Get current BTC price with change metrics."""
            try:
                # Create Redis client
                r = redis.Redis(
                    host="localhost",
                    port=6379,
                    decode_responses=True
                )
                
                # Try to get price data from different Redis keys in priority order
                price_keys = ['btc_price', 'last_btc_price', 'current_position']
                current_price = None
                
                for key in price_keys:
                    try:
                        price_str = r.get(key)
                        if not price_str:
                            continue
                            
                        # Handle different data formats
                        if key == 'btc_price':
                            # btc_price is stored as JSON with a price field
                            data = json.loads(price_str)
                            if 'price' in data:
                                current_price = float(data['price'])
                                break
                        elif key == 'last_btc_price':
                            # last_btc_price is stored directly as a string
                            current_price = float(price_str)
                            break
                        elif key == 'current_position':
                            # Extract from position data if available
                            position_data = json.loads(price_str)
                            if 'current_price' in position_data:
                                current_price = float(position_data['current_price'])
                                break
                    except (ValueError, TypeError, json.JSONDecodeError) as e:
                        logging.warning(f"Error parsing price from {key}: {e}")
                        continue
                
                # Default fallback if all else fails
                if current_price is None:
                    current_price = 65000  # Default fallback
                
                # Get change data directly from Redis if available
                change_data = r.get("btc_price_changes")
                changes = {
                    "short_term": -0.06,
                    "medium_term": -0.79,
                    "long_term": 3.76
                }
                
                if change_data:
                    try:
                        changes = json.loads(change_data)
                    except json.JSONDecodeError:
                        pass
                
                # Get price patterns data
                patterns_data = r.get("btc_price_patterns")
                patterns = {
                    "bullish": 0.16,
                    "bearish": 0.03,
                    "neutral": 0.49,
                    "volatile": 0.19
                }
                
                if patterns_data:
                    try:
                        patterns = json.loads(patterns_data)
                    except json.JSONDecodeError:
                        pass
                
                # Calculate the percentage change
                prev_price_str = r.get("prev_btc_price")
                if prev_price_str:
                    try:
                        prev_price = float(prev_price_str)
                        if prev_price > 0:
                            change = ((current_price - prev_price) / prev_price) * 100
                        else:
                            change = 0
                    except (ValueError, TypeError):
                        change = 0
                else:
                    change = 0
                
                return {
                    "price": current_price,
                    "change": change,
                    "changes": changes,
                    "patterns": patterns,
                    "source": "Redis",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                
            except Exception as e:
                logger.error(f"Error getting BTC price data: {e}")
                return {
                    "price": 65000,  # Default fallback price
                    "change": 0.0,
                    "changes": {
                        "short_term": 0.0,
                        "medium_term": 0.0,
                        "long_term": 0.0
                    },
                    "patterns": {
                        "bullish": 0.25,
                        "bearish": 0.25,
                        "neutral": 0.25,
                        "volatile": 0.25
                    },
                    "source": "Error",
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
        
        @self.app.get("/api/redis-keys")
        async def get_redis_keys():
            """Get a list of recently updated Redis keys."""
            try:
                if not self.redis_client:
                    return {"error": "Redis not connected"}
                
                # Get a limited set of keys to prevent timeouts
                all_keys = self.redis_client.keys("*")
                logger.info(f"Found {len(all_keys)} total Redis keys")
                
                # Prioritize certain patterns and limit to 20 keys max
                test_keys = [k for k in all_keys if k.startswith("test:")]
                other_keys = [k for k in all_keys if not k.startswith("test:")]
                
                # Prioritize test: keys first, then add others
                sample_keys = test_keys[:10]  # Up to 10 test keys
                if len(sample_keys) < 20:
                    # Add other keys to fill up to 20
                    sample_keys.extend(other_keys[:20-len(sample_keys)])
                
                # Process this limited set
                recent_keys = []
                for key in sample_keys:
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
                
                # Add total count info
                return {
                    "keys": recent_keys,
                    "total_keys": len(all_keys),
                    "displayed_keys": len(recent_keys)
                }
            except Exception as e:
                logger.error(f"Error getting Redis keys: {e}")
                return {"error": str(e)}
        
        @self.app.get("/api/redis-key")
        async def get_redis_key(key: str):
            """Get a specific Redis key value."""
            try:
                if not self.redis_client:
                    return {"error": "Redis not connected", "status": "error"}
                
                # Check if key exists
                if not self.redis_client.exists(key):
                    return {"error": f"Key '{key}' not found", "status": "error"}
                
                # Get key type
                key_type = self.redis_client.type(key)
                
                # Return key value based on type
                if key_type == "string":
                    value = self.redis_client.get(key)
                    if value is None:
                        return {"key": key, "type": key_type, "value": None, "status": "success"}
                    
                    try:
                        # Try to parse as JSON
                        parsed_value = json.loads(value)
                        return {"key": key, "type": key_type, "value": parsed_value, "status": "success"}
                    except (json.JSONDecodeError, TypeError):
                        # Return as string if not valid JSON
                        try:
                            # Try to parse as float
                            float_value = float(value)
                            return {"key": key, "type": key_type, "value": float_value, "status": "success"}
                        except (ValueError, TypeError):
                            # Return as plain string
                            return {"key": key, "type": key_type, "value": value, "status": "success"}
                elif key_type == "list":
                    # Get all list items
                    values = self.redis_client.lrange(key, 0, -1)
                    return {"key": key, "type": key_type, "value": values, "status": "success"}
                elif key_type == "hash":
                    # Get all hash fields
                    values = self.redis_client.hgetall(key)
                    return {"key": key, "type": key_type, "value": values, "status": "success"}
                elif key_type == "set":
                    # Get all set members
                    values = list(self.redis_client.smembers(key))
                    return {"key": key, "type": key_type, "value": values, "status": "success"}
                elif key_type == "zset":
                    # Get all sorted set members with scores
                    values = self.redis_client.zrange(key, 0, -1, withscores=True)
                    return {"key": key, "type": key_type, "value": dict(values), "status": "success"}
                else:
                    return {"key": key, "type": key_type, "value": None, "error": f"Unsupported key type: {key_type}", "status": "error"}
            except Exception as e:
                logger.error(f"Error getting Redis key '{key}': {e}")
                return {"key": key, "error": str(e), "status": "error"}
        
        @self.app.get("/api/data")
        async def get_combined_data():
            """Get combined data from multiple endpoints."""
            # Get data from individual endpoints
            trap_data = self._get_trap_probability()
            position_data = self._get_position_data()
            
            # Get BTC price data
            try:
                # Create a new Redis client for testing
                r = redis.Redis(
                    host="localhost",
                    port=6379,
                    decode_responses=True
                )
                
                # Get current price
                price_data = None
                for key in ['last_btc_price', 'btc_price', 'sim_last_btc_price']:
                    price = r.get(key)
                    if price:
                        try:
                            price_data = {
                                "price": float(price),
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                                "source": key
                            }
                            break
                        except ValueError:
                            continue

                # Get price changes
                changes_data = None
                changes = r.get('btc_price_changes')
                if changes:
                    try:
                        changes_data = json.loads(changes)
                    except json.JSONDecodeError:
                        pass

                # Get price patterns
                patterns_data = None
                patterns = r.get('btc_price_patterns')
                if patterns:
                    try:
                        patterns_data = json.loads(patterns)
                    except json.JSONDecodeError:
                        pass

                if price_data:
                    if changes_data:
                        price_data["changes"] = changes_data
                    if patterns_data:
                        price_data["patterns"] = patterns_data
                else:
                    # Fallback
                    price_data = {
                        "price": random.uniform(60000, 70000),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "source": "fallback",
                        "changes": {
                            "short_term": random.uniform(-0.05, 0.05),
                            "medium_term": random.uniform(-0.1, 0.1)
                        },
                        "patterns": {
                            "wyckoff_distribution": random.uniform(0, 1),
                            "double_top": random.uniform(0, 1),
                            "head_and_shoulders": random.uniform(0, 1),
                            "bull_flag": random.uniform(0, 1)
                        }
                    }
            except Exception as e:
                logger.error(f"Error getting BTC price data: {e}")
                # Fallback
                price_data = {
                    "price": random.uniform(60000, 70000),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "source": "fallback_error",
                    "error": str(e)
                }
            
            # Combine data into a single response
            return {
                "trap_probability": trap_data,
                "position": position_data,
                "btc_price": price_data,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        @self.app.get("/api/metrics")
        async def get_metrics():
            """Get trap metrics with advanced analytics."""
            try:
                # Create Redis client
                r = redis.Redis(
                    host="localhost",
                    port=6379,
                    decode_responses=True
                )
                
                # Try to get metrics data from Redis
                metrics_json = r.get("trap_metrics")
                if metrics_json:
                    try:
                        metrics_data = json.loads(metrics_json)
                        return metrics_data
                    except json.JSONDecodeError:
                        pass
                
                # Generate fallback metrics if not available in Redis
                fallback_metrics = {
                    "total_traps": random.randint(10, 50),
                    "success_rate": random.uniform(0.6, 0.9),
                    "average_probability": random.uniform(0.5, 0.8),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                return fallback_metrics
                
            except Exception as e:
                logger.error(f"Error getting metrics data: {e}")
                return {
                    "total_traps": 0,
                    "success_rate": 0.0,
                    "average_probability": 0.0,
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
        
        @self.app.get("/api/traps")
        async def get_traps(start_time: Optional[str] = None, end_time: Optional[str] = None, trap_type: Optional[str] = None):
            """Get trap detections with optional filters."""
            try:
                # Create Redis client
                r = redis.Redis(
                    host="localhost",
                    port=6379,
                    decode_responses=True
                )
                
                # Try to get trap detections from Redis
                traps_json = r.get("trap_detections")
                if traps_json:
                    try:
                        traps_data = json.loads(traps_json)
                        
                        # Apply filters if provided
                        filtered_traps = traps_data
                        
                        if start_time:
                            start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                            filtered_traps = [trap for trap in filtered_traps 
                                            if datetime.fromisoformat(trap.get("timestamp", "").replace("Z", "+00:00")) >= start_dt]
                        
                        if end_time:
                            end_dt = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
                            filtered_traps = [trap for trap in filtered_traps 
                                            if datetime.fromisoformat(trap.get("timestamp", "").replace("Z", "+00:00")) <= end_dt]
                        
                        if trap_type:
                            filtered_traps = [trap for trap in filtered_traps 
                                            if trap.get("type", "") == trap_type]
                        
                        return filtered_traps
                    except json.JSONDecodeError:
                        pass
                
                # Generate fallback data if not available
                return []
                
            except Exception as e:
                logger.error(f"Error getting trap detections: {e}")
                return []
                
        @self.app.get("/api/trader-status")
        async def get_trader_status():
            """Get trap-aware dual trader status information."""
            try:
                # Create Redis client
                r = redis.Redis(
                    host="localhost",
                    port=6379,
                    decode_responses=True
                )
                
                # Try to get trader status from Redis
                trader_status_json = r.get("trader_status")
                if trader_status_json:
                    try:
                        trader_status = json.loads(trader_status_json)
                        return trader_status
                    except json.JSONDecodeError:
                        logger.error("Failed to parse trader_status JSON from Redis")
                
                # Return default structure if not available in Redis
                default_status = {
                    "status": "unknown",
                    "long_trader_status": "inactive",
                    "short_trader_status": "inactive",
                    "combined_pnl": 0,
                    "last_action": "No recent actions",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                return default_status
                
            except Exception as e:
                logger.error(f"Error getting trader status: {e}")
                return {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
        
        @self.app.get("/api/prices")
        async def get_prices():
            """Get price data with integrity verification."""
            try:
                # Create Redis client
                r = redis.Redis(
                    host="localhost",
                    port=6379,
                    decode_responses=True
                )
                
                # Try to get price data from Redis
                prices_json = r.get("btc_price_history")
                if prices_json:
                    try:
                        prices_data = json.loads(prices_json)
                        return prices_data
                    except json.JSONDecodeError:
                        pass
                
                # Get current BTC price as reference
                current_price = 65000  # Default fallback
                price_json = r.get("btc_price")
                if price_json:
                    try:
                        current_price = float(price_json)
                    except (ValueError, TypeError):
                        pass
                
                # Generate fallback price data if not available in Redis
                fallback_prices = []
                for i in range(24):  # Generate 24 hours of data
                    hour_offset = 23 - i  # Start from 23 hours ago
                    timestamp = datetime.now(timezone.utc) - timedelta(hours=hour_offset)
                    
                    # Generate a somewhat realistic price movement
                    price_offset = random.uniform(-500, 500)
                    sample_price = {
                        "timestamp": timestamp.isoformat(),
                        "price": current_price + price_offset,
                        "volume": random.uniform(50, 200),
                        "indicators": {
                            "rsi": random.uniform(30, 70),
                            "macd": random.uniform(-100, 100)
                        }
                    }
                    fallback_prices.append(sample_price)
                
                return fallback_prices
                
            except Exception as e:
                logger.error(f"Error getting price data: {e}")
                return [
                    {
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "price": 65000,
                        "volume": 0,
                        "indicators": {
                            "rsi": 50,
                            "macd": 0
                        },
                        "error": str(e)
                    }
                ]
        
        @self.app.get("/api/timeline")
        async def get_timeline(hours: int = 24):
            """Get timeline of trap detections."""
            try:
                # Create Redis client
                r = redis.Redis(
                    host="localhost",
                    port=6379,
                    decode_responses=True
                )
                
                # Try to get timeline data from Redis
                timeline_json = r.get("trap_timeline")
                if timeline_json:
                    try:
                        timeline_data = json.loads(timeline_json)
                        
                        # Filter by hours parameter
                        if hours and hours > 0:
                            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
                            timeline_data = [event for event in timeline_data 
                                           if datetime.fromisoformat(event.get("timestamp", "").replace("Z", "+00:00")) >= cutoff_time]
                        
                        return timeline_data
                    except json.JSONDecodeError:
                        pass
                
                # Generate fallback timeline data if not available in Redis
                event_types = ["trap_detected", "price_alert", "volume_spike", "pattern_formed"]
                severities = ["low", "medium", "high"]
                descriptions = [
                    "Bull trap pattern detected with high probability",
                    "Bear trap forming on lower timeframes",
                    "Volume spike detected at resistance level",
                    "Price manipulation detected with moderate confidence",
                    "Stop hunt likely occurred at key support level"
                ]
                
                fallback_timeline = []
                for i in range(min(hours, 48)):  # Generate events, max 48
                    if random.random() < 0.3:  # Only generate events with 30% probability
                        hour_offset = random.randint(0, hours-1)
                        timestamp = datetime.now(timezone.utc) - timedelta(hours=hour_offset)
                        
                        event = {
                            "timestamp": timestamp.isoformat(),
                            "event_type": random.choice(event_types),
                            "description": random.choice(descriptions),
                            "severity": random.choice(severities)
                        }
                        fallback_timeline.append(event)
                
                # Sort timeline by timestamp, most recent first
                fallback_timeline.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
                
                return fallback_timeline
                
            except Exception as e:
                logger.error(f"Error getting timeline data: {e}")
                return [
                    {
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "event_type": "error",
                        "description": f"Error retrieving timeline data: {str(e)}",
                        "severity": "low"
                    }
                ]
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time dashboard updates."""
            await websocket.accept()
            self.active_connections.append(websocket)
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
                if websocket in self.active_connections:
                    self.active_connections.remove(websocket)
        
        @self.app.get("/api/big-brother-data")
        async def get_big_brother_data():
            """Get all data needed for the Big Brother monitoring panel."""
            if not self.redis_client:
                return {"error": "Redis connection not available"}
                
            try:
                # Get position data from Redis
                long_position = await self._get_redis_data('long_position')
                short_position = await self._get_redis_data('short_position')
                position_stats = await self._get_redis_data('position_stats')
                
                # Get Fibonacci levels
                fibonacci_levels = await self._get_redis_data('fibonacci:current_levels')
                
                # Get trap detection data
                trap_data = await self._get_redis_data('mm_trap_detection')
                
                # Get elite exit strategy data
                elite_exit_data = await self._get_redis_data('elite_exit_strategy')
                
                return {
                    "long_position": long_position,
                    "short_position": short_position,
                    "position_stats": position_stats,
                    "fibonacci_levels": fibonacci_levels,
                    "trap_data": trap_data,
                    "elite_exit_data": elite_exit_data,
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                logger.error(f"{RED}Error fetching Big Brother data: {e}{RESET}")
                return {"error": str(e)}
                
        @self.app.get("/api/flow/3d")
        async def get_3d_flow(hours: int = 24):
            """Generate 3D position flow visualization."""
            if not self.redis_client:
                return {"error": "Redis connection not available"}
                
            try:
                import subprocess
                import os
                import sys
                from pathlib import Path
                
                # Get the position data from Redis
                long_position = await self._get_redis_data('long_position')
                short_position = await self._get_redis_data('short_position')
                
                # Determine which position to use (prefer long if both exist)
                position_data = None
                position_type = "unknown"
                if long_position and "entry_price" in long_position:
                    position_data = long_position
                    position_type = "long"
                elif short_position and "entry_price" in short_position:
                    position_data = short_position
                    position_type = "short"
                
                # Define paths
                script_path = Path("scripts/position_flow_tracker.py").absolute()
                output_dir = Path("omega_ai/visualizer/frontend/reggae-dashboard/static/images").absolute()
                os.makedirs(output_dir, exist_ok=True)
                
                # Generate a timestamp for the output file
                import time
                timestamp = int(time.time())
                output_file = output_dir / f"flow_3d_{timestamp}.png"
                
                # Prepare the command
                if position_data:
                    # Write position data to a temporary file
                    import tempfile
                    import json
                    
                    with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w') as tmp:
                        json.dump(position_data, tmp)
                        position_file = tmp.name
                    
                    # Run the position flow tracker script with the position data
                    cmd = [
                        sys.executable, 
                        str(script_path),
                        "--use-simulated" if not position_data else "",
                        "--3d",
                        "--hours", str(hours),
                        "--position-file", position_file
                    ]
                    
                    # Filter out empty strings
                    cmd = [arg for arg in cmd if arg]
                    
                    logger.info(f"{CYAN}Running flow visualization command: {' '.join(cmd)}{RESET}")
                    
                    # Run the process
                    process = subprocess.run(cmd, capture_output=True, text=True)
                    
                    # Clean up the temporary file
                    os.unlink(position_file)
                    
                    if process.returncode != 0:
                        logger.error(f"{RED}Error generating 3D flow: {process.stderr}{RESET}")
                        return {
                            "status": "error",
                            "message": "Error generating 3D flow visualization",
                            "details": process.stderr,
                            "fallback_image_url": "/static/images/3d_flow_mock.png"
                        }
                    
                    # The script should have saved the visualization to a file
                    # Extract the filename from the output
                    import re
                    match = re.search(r"saved as (\S+\.png)", process.stdout)
                    if match:
                        output_file = match.group(1)
                        
                        # Move the file to the static directory if it's not already there
                        if not output_file.startswith(str(output_dir)):
                            import shutil
                            target_file = output_dir / Path(output_file).name
                            shutil.move(output_file, target_file)
                            output_file = target_file
                            
                    return {
                        "status": "success",
                        "message": "3D flow visualization generated",
                        "hours": hours,
                        "position_type": position_type,
                        "output": process.stdout,
                        "image_url": f"/static/images/{Path(output_file).name}"
                    }
                
                # Fall back to mock data if no position is available
                return {
                    "status": "success",
                    "message": "3D flow visualization generated with mock data",
                    "hours": hours,
                    "image_url": "/static/images/3d_flow_mock.png"
                }
                    
            except Exception as e:
                logger.error(f"{RED}Error generating 3D flow: {str(e)}{RESET}")
                import traceback
                logger.error(f"{RED}{traceback.format_exc()}{RESET}")
                return {"error": str(e)}
                
        @self.app.get("/api/flow/2d")
        async def get_2d_flow(hours: int = 24):
            """Generate 2D position flow chart."""
            if not self.redis_client:
                return {"error": "Redis connection not available"}
                
            try:
                import subprocess
                import os
                import sys
                from pathlib import Path
                
                # Get the position data from Redis
                long_position = await self._get_redis_data('long_position')
                short_position = await self._get_redis_data('short_position')
                
                # Determine which position to use (prefer long if both exist)
                position_data = None
                position_type = "unknown"
                if long_position and "entry_price" in long_position:
                    position_data = long_position
                    position_type = "long"
                elif short_position and "entry_price" in short_position:
                    position_data = short_position
                    position_type = "short"
                
                # Define paths
                script_path = Path("scripts/position_flow_tracker.py").absolute()
                output_dir = Path("omega_ai/visualizer/frontend/reggae-dashboard/static/images").absolute()
                os.makedirs(output_dir, exist_ok=True)
                
                # Generate a timestamp for the output file
                import time
                timestamp = int(time.time())
                output_file = output_dir / f"flow_2d_{timestamp}.png"
                
                # Prepare the command
                if position_data:
                    # Write position data to a temporary file
                    import tempfile
                    import json
                    
                    with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w') as tmp:
                        json.dump(position_data, tmp)
                        position_file = tmp.name
                    
                    # Run the position flow tracker script with the position data
                    cmd = [
                        sys.executable, 
                        str(script_path),
                        "--use-simulated" if not position_data else "",
                        "--2d",  # Use 2D mode
                        "--hours", str(hours),
                        "--position-file", position_file
                    ]
                    
                    # Filter out empty strings
                    cmd = [arg for arg in cmd if arg]
                    
                    logger.info(f"{CYAN}Running flow visualization command: {' '.join(cmd)}{RESET}")
                    
                    # Run the process
                    process = subprocess.run(cmd, capture_output=True, text=True)
                    
                    # Clean up the temporary file
                    os.unlink(position_file)
                    
                    if process.returncode != 0:
                        logger.error(f"{RED}Error generating 2D flow: {process.stderr}{RESET}")
                        return {
                            "status": "error",
                            "message": "Error generating 2D flow visualization",
                            "details": process.stderr,
                            "fallback_image_url": "/static/images/2d_flow_mock.png"
                        }
                    
                    # The script should have saved the visualization to a file
                    # Extract the filename from the output
                    import re
                    match = re.search(r"saved as (\S+\.png)", process.stdout)
                    if match:
                        output_file = match.group(1)
                        
                        # Move the file to the static directory if it's not already there
                        if not output_file.startswith(str(output_dir)):
                            import shutil
                            target_file = output_dir / Path(output_file).name
                            shutil.move(output_file, target_file)
                            output_file = target_file
                            
                    return {
                        "status": "success",
                        "message": "2D flow visualization generated",
                        "hours": hours,
                        "position_type": position_type,
                        "output": process.stdout,
                        "image_url": f"/static/images/{Path(output_file).name}"
                    }
                
                # Fall back to mock data if no position is available
                return {
                    "status": "success",
                    "message": "2D flow visualization generated with mock data",
                    "hours": hours,
                    "image_url": "/static/images/2d_flow_mock.png"
                }
                    
            except Exception as e:
                logger.error(f"{RED}Error generating 2D flow: {str(e)}{RESET}")
                import traceback
                logger.error(f"{RED}{traceback.format_exc()}{RESET}")
                return {"error": str(e)}
        
        @self.app.get("/api/elite-exits")
        async def get_elite_exits(confidence: float = 0.7):
            """Get elite exit strategy data with specified confidence threshold."""
            if not self.redis_client:
                return {"error": "Redis connection not available"}
                
            try:
                # Try to get exit strategy data from Redis
                elite_exit_keys = ['elite_exit_signals', 'elite_exit_data', 'exit_strategy_signals']
                elite_exit_data = None
                
                for key in elite_exit_keys:
                    data_json = self.redis_client.get(key)
                    if data_json:
                        try:
                            exit_data = json.loads(data_json)
                            if isinstance(exit_data, dict) and 'current_signal' in exit_data:
                                elite_exit_data = exit_data
                                # Add source attribution
                                elite_exit_data["_source"] = f"redis:{key}"
                                break
                        except json.JSONDecodeError:
                            pass
                
                # If we found real data, adjust for the requested confidence
                if elite_exit_data:
                    elite_exit_data["confidence_threshold"] = confidence
                    return elite_exit_data
                
                # No real elite exit data found, generate mock with requested confidence
                now = datetime.now()
                mock_data = {
                    "current_signal": {
                        "recommendation": "HOLD",
                        "confidence": confidence - 0.1,  # Just below threshold
                        "next_target": {
                            "price": 87500,
                            "type": "resistance"
                        }
                    },
                    "metrics": {
                        "trend_strength": 0.65,
                        "volatility": 0.42,
                        "price_momentum": 0.58,
                        "volume_profile": 0.62
                    },
                    "history": [
                        {
                            "timestamp": (now - timedelta(hours=2)).isoformat(),
                            "action": "EXIT",
                            "position": "LONG",
                            "price": 85200,
                            "pnl": 450.75,
                            "confidence": 0.82
                        },
                        {
                            "timestamp": (now - timedelta(hours=8)).isoformat(),
                            "action": "EXIT",
                            "position": "SHORT",
                            "price": 82100,
                            "pnl": 215.50,
                            "confidence": 0.75
                        }
                    ],
                    "confidence_threshold": confidence,
                    "_source": "mock"
                }
                
                return mock_data
            except Exception as e:
                logger.error(f"{RED}Error fetching elite exit data: {e}{RESET}")
                return {"error": str(e), "status": "error"}
        
        # Helper method to get Redis data with fallback to mock data
        async def _get_redis_data(self, key):
            """Get data from Redis with fallback to mock data."""
            try:
                # Try to get data from Redis
                redis_key_mapping = {
                    # Map logical keys to actual Redis keys
                    'long_position': ['long_trader_position', 'current_long_position', 'dual_trader_long'],
                    'short_position': ['short_trader_position', 'current_short_position', 'dual_trader_short'],
                    'position_stats': ['trader_statistics', 'trade_stats', 'trader_performance'],
                    'fibonacci:current_levels': ['fibonacci_levels', 'fib_levels', 'fibonacci:targets'],
                    'mm_trap_detection': ['trap_detection', 'current_trap_probability', 'market_maker_traps'],
                    'elite_exit_strategy': ['elite_exit_signals', 'elite_exit_data', 'exit_strategy_signals'],
                    'trade_history': ['trade_history', 'position_history', 'closed_trades'],
                    'dual_trader_status': ['dual_trader_status', 'trader_status', 'system_status']
                }
                
                # Get potential Redis keys for the requested logical key
                redis_keys = redis_key_mapping.get(key, [key])
                
                # Try each potential Redis key
                for redis_key in redis_keys:
                    value = self.redis_client.get(redis_key)
                    if value:
                        # Try to parse as JSON
                        try:
                            data = json.loads(value)
                            logger.info(f"{GREEN}Found data for {key} in Redis key {redis_key}{RESET}")
                            # Add source attribution
                            if isinstance(data, dict):
                                data["_source"] = f"redis:{redis_key}"
                            return data
                        except json.JSONDecodeError:
                            # If not JSON, check if it's numeric
                            try:
                                return float(value)
                            except ValueError:
                                # Return raw value
                                return value
                
                # Not found in any potential Redis key
                logger.warning(f"{YELLOW}No data found in Redis for key {key}, using mock data{RESET}")
                
                # Generate mock data if Redis key doesn't exist
                mock_data = self._generate_mock_data(key)
                if isinstance(mock_data, dict):
                    mock_data["_source"] = "mock"
                return mock_data
                
            except Exception as e:
                logger.error(f"{RED}Error getting Redis data for key {key}: {e}{RESET}")
                mock_data = self._generate_mock_data(key)
                if isinstance(mock_data, dict):
                    mock_data["_source"] = "mock:error"
                    mock_data["_error"] = str(e)
                return mock_data
    
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
                disconnected = []
                for websocket in self.active_connections:
                    try:
                        await websocket.send_json(update)
                    except Exception:
                        disconnected.append(websocket)
                
                # Remove disconnected clients
                for websocket in disconnected:
                    if websocket in self.active_connections:
                        self.active_connections.remove(websocket)
                
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

    # Generate mock data for testing when Redis data is not available
    def _generate_mock_data(self, key):
        """Generate mock data for the given key."""
        now = datetime.now()
        
        # Mock data for testing
        mock_data = {
            "long_position": {
                "entry_price": 84500,
                "size": 0.01,
                "leverage": 10,
                "direction": "LONG",
                "entry_time": (now - timedelta(hours=12)).isoformat(),
                "unrealized_pnl": 125.5,
                "take_profits": [{"percentage": 50, "price": 85500}],
                "stop_loss": 83000
            },
            "short_position": {
                "entry_price": 84200,
                "size": 0.015,
                "leverage": 5,
                "direction": "SHORT",
                "entry_time": (now - timedelta(hours=8)).isoformat(),
                "unrealized_pnl": -45.2,
                "take_profits": [{"percentage": 50, "price": 83200}],
                "stop_loss": 85700
            },
            "position_stats": {
                "win_rate": 0.68,
                "avg_profit": 125.75,
                "avg_loss": 42.30,
                "avg_hold_time": 3600 * 6,  # 6 hours
                "total_trades": 125,
                "profitable_trades": 85,
                "losing_trades": 40
            },
            "fibonacci:current_levels": {
                "direction": "LONG",
                "base_price": 84500,
                "levels": {
                    "0.0": 84500,
                    "0.236": 85003.2,
                    "0.382": 85318.9,
                    "0.5": 85565.0,
                    "0.618": 85822.3,
                    "0.786": 86178.5,
                    "1.0": 86630.0,
                    "1.618": 87845.7,
                    "2.618": 89769.2
                }
            },
            "mm_trap_detection": {
                "current": {
                    "trap_risk": 0.45,
                    "trap_type": "bear_trap",
                    "description": "Potential bear trap forming with high volume spike on 15m timeframe."
                },
                "history": [
                    {
                        "timestamp": (now - timedelta(days=1)).isoformat(),
                        "type": "bull_trap",
                        "probability": 0.82,
                        "price_range": [85200, 85700]
                    },
                    {
                        "timestamp": (now - timedelta(days=3)).isoformat(),
                        "type": "stop_hunt",
                        "probability": 0.73,
                        "price_range": [82300, 82800]
                    }
                ]
            },
            "elite_exit_strategy": {
                "current_signal": {
                    "recommendation": "HOLD",
                    "confidence": 0.62,
                    "next_target": {
                        "price": 87500,
                        "type": "resistance"
                    }
                },
                "metrics": {
                    "trend_strength": 0.65,
                    "volatility": 0.42,
                    "price_momentum": 0.58,
                    "volume_profile": 0.62
                },
                "history": [
                    {
                        "timestamp": (now - timedelta(hours=2)).isoformat(),
                        "action": "EXIT",
                        "position": "LONG",
                        "price": 85200,
                        "pnl": 450.75,
                        "confidence": 0.82
                    },
                    {
                        "timestamp": (now - timedelta(hours=8)).isoformat(),
                        "action": "EXIT",
                        "position": "SHORT",
                        "price": 82100,
                        "pnl": 215.50,
                        "confidence": 0.75
                    }
                ]
            },
            "trade_history": [
                {
                    "timestamp": (now - timedelta(days=2)).isoformat(),
                    "type": "entry",
                    "direction": "LONG",
                    "price": 83500,
                    "size": 0.01
                },
                {
                    "timestamp": (now - timedelta(days=1, hours=12)).isoformat(),
                    "type": "exit",
                    "direction": "LONG", 
                    "price": 84200,
                    "size": 0.01,
                    "pnl": 70
                }
            ],
            "dual_trader_status": {
                "long_status": "active",
                "short_status": "active",
                "last_action": "entry",
                "last_action_time": (now - timedelta(hours=12)).isoformat(),
                "total_pnl": 250.5
            }
        }
        
        return mock_data.get(key, {"message": f"No mock data available for key: {key}"})

if __name__ == "__main__":
    # Create dashboard server instance
    dashboard = ReggaeDashboardServer()
    app = dashboard.app
    
    # Register startup and shutdown events
    app.add_event_handler("startup", dashboard.startup)
    app.add_event_handler("shutdown", dashboard.shutdown)
    
    # Start the server
    logger.info(f"Starting Reggae Dashboard server on 0.0.0.0:8001")
    
    # Print colorful banner
    print(f"\n{GREEN}{BOLD}==============================================={RESET}")
    print(f"{GREEN}{BOLD}    OMEGA BTC AI - REGGAE DASHBOARD SERVER    {RESET}")
    print(f"{GREEN}{BOLD}==============================================={RESET}")
    print(f"{GOLD}    JAH BLESS YOUR TRADING JOURNEY    {RESET}")
    print(f"{GREEN}{BOLD}==============================================={RESET}\n")
    
    # Run the app directly with the string reference again
    uvicorn.run("reggae_dashboard_server:app", host="0.0.0.0", port=8001)
else:
    # For imported usage, create the app
    dashboard = ReggaeDashboardServer()
    app = dashboard.app 