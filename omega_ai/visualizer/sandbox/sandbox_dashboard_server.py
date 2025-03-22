#!/usr/bin/env python3

"""
OMEGA BTC AI - Reggae Hacker Omega UI Dashboard Server (SANDBOX VERSION)
========================================================================

A real-time dashboard server that provides trap probability and trading position data
via WebSockets with a Reggae Hacker aesthetic.

This is a sandbox version running on port 5002, leaving the original server untouched.
"""

import asyncio
import json
import random
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any, Set

import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
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
logger = logging.getLogger("sandbox_dashboard")

class SandboxDashboardServer:
    """
    Sandbox server for the Reggae Hacker Omega UI Dashboard that provides real-time
    trading position and trap probability data.
    """
    
    def __init__(self):
        """Initialize the dashboard server with WebSocket support."""
        self.app = FastAPI(title="OMEGA BTC AI - Sandbox Dashboard")
        
        # Active WebSocket connections
        self.active_connections = []
        
        # Redis client for data access
        self.redis_client = self._init_redis_client()
        
        # CORS middleware for frontend connections
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Mount static files for the dashboard
        current_dir = Path(__file__).parent.absolute()
        frontend_path = current_dir / "dashboard"
        if not frontend_path.exists():
            frontend_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created sandbox frontend directory at {frontend_path}")
            
        # Mount the frontend directory at /dashboard instead of root
        self.app.mount("/dashboard", StaticFiles(directory=str(frontend_path), html=True), name="dashboard")
        logger.info(f"Mounted frontend files from {frontend_path}")
        
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
            """Root endpoint that redirects to the dashboard."""
            return RedirectResponse(url="/dashboard/sandbox.html")
        
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
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "server": "sandbox"
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
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "server": "sandbox"
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
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "server": "sandbox"
            }
        
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
    dashboard = SandboxDashboardServer()
    app = dashboard.app
    
    # Register startup and shutdown events
    app.add_event_handler("startup", dashboard.startup)
    app.add_event_handler("shutdown", dashboard.shutdown)
    
    # Start the server
    logger.info(f"Starting Sandbox Reggae Dashboard server on 0.0.0.0:5002")
    
    # Print colorful banner
    print(f"\n{GREEN}{BOLD}========================================================{RESET}")
    print(f"{GREEN}{BOLD}    OMEGA BTC AI - SANDBOX REGGAE DASHBOARD SERVER    {RESET}")
    print(f"{GREEN}{BOLD}========================================================{RESET}")
    print(f"{GOLD}    JAH BLESS YOUR SANDBOXED TRADING JOURNEY    {RESET}")
    print(f"{GREEN}{BOLD}========================================================{RESET}\n")
    
    # Run the app with a different port
    uvicorn.run("sandbox_dashboard_server:app", host="0.0.0.0", port=5002)
else:
    # For imported usage, create the app
    dashboard = SandboxDashboardServer()
    app = dashboard.app 