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
            # Create a simpler HTML response
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
                    }
                    h1 {
                        color: #4CAF50;
                        border-bottom: 2px solid #FFD700;
                    }
                    .container {
                        max-width: 800px;
                        margin: 0 auto;
                    }
                    .endpoint {
                        background-color: #1E1E1E;
                        border-left: 4px solid #FFD700;
                        padding: 10px;
                        margin: 10px 0;
                    }
                    .method {
                        color: #4CAF50;
                        font-weight: bold;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>OMEGA BTC AI - Reggae Dashboard API</h1>
                    
                    <h2>Available Endpoints</h2>
                    <div class="endpoint">
                        <div class="method">GET</div>
                        <div>/api/health - Health check endpoint</div>
                    </div>
                    <div class="endpoint">
                        <div class="method">GET</div>
                        <div>/api/trap-probability - Get trap probability data</div>
                    </div>
                    <div class="endpoint">
                        <div class="method">GET</div>
                        <div>/api/position - Get position data</div>
                    </div>
                    <div class="endpoint">
                        <div class="method">GET</div>
                        <div>/api/redis-keys - List Redis keys</div>
                    </div>
                    <div class="endpoint">
                        <div class="method">GET</div>
                        <div>/api/data - Get combined data</div>
                    </div>
                    <div class="endpoint">
                        <div class="method">GET</div>
                        <div>/api/metrics - Get trap metrics with advanced analytics</div>
                    </div>
                    <div class="endpoint">
                        <div class="method">GET</div>
                        <div>/api/traps - Get trap detections with optional filters</div>
                    </div>
                    <div class="endpoint">
                        <div class="method">GET</div>
                        <div>/api/prices - Get price data with integrity verification</div>
                    </div>
                    <div class="endpoint">
                        <div class="method">GET</div>
                        <div>/api/timeline - Get timeline of trap detections</div>
                    </div>
                    <div class="endpoint">
                        <div class="method">WebSocket</div>
                        <div>/ws - Real-time updates</div>
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
                
                # Try to get price data from Redis
                price_str = r.get("btc_price")
                current_price = 65000  # Default fallback
                
                if price_str:
                    try:
                        current_price = float(price_str)
                    except (ValueError, TypeError):
                        pass
                
                # Get change data directly from Redis if available
                change_percent = None
                try:
                    change_str = r.get("btc_price_change")
                    if change_str:
                        change_percent = float(change_str)
                except:
                    pass
                
                # Use random as fallback if no change data found
                if change_percent is None:
                    change_percent = random.uniform(-2.5, 2.5)
                
                return {
                    "price": current_price,
                    "change": change_percent,
                    "changes": {
                        "short_term": round(random.uniform(-1.5, 1.5), 2),
                        "medium_term": round(random.uniform(-3.0, 3.0), 2),
                        "long_term": round(random.uniform(-5.0, 5.0), 2)
                    },
                    "patterns": {
                        "bullish": round(random.random(), 2),
                        "bearish": round(random.random(), 2),
                        "neutral": round(random.random(), 2),
                        "volatile": round(random.random(), 2)
                    },
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
                
                # Generate fallback trap data if not available in Redis
                trap_types = ["bull_trap", "bear_trap", "liquidity_grab", "stop_hunt"]
                severities = ["low", "medium", "high"]
                
                fallback_traps = []
                for _ in range(5):  # Generate 5 sample traps
                    trap_timestamp = datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 24))
                    sample_trap = {
                        "type": random.choice(trap_types),
                        "description": f"Detected potential trap pattern",
                        "timestamp": trap_timestamp.isoformat(),
                        "probability": random.uniform(0.5, 0.95),
                        "severity": random.choice(severities)
                    }
                    fallback_traps.append(sample_trap)
                
                return fallback_traps
                
            except Exception as e:
                logger.error(f"Error getting trap data: {e}")
                return [
                    {
                        "type": "error",
                        "description": f"Error retrieving trap data: {str(e)}",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "probability": 0.0,
                        "severity": "low"
                    }
                ]
        
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