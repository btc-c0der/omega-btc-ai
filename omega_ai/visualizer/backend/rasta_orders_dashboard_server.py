#!/usr/bin/env python3

"""
OMEGA BTC AI - Rasta Orders Dashboard Server
=========================================

A real-time dashboard server that provides BitGet live trading order information
via WebSockets with a Rastafarian aesthetic.

This server streams order updates, position changes, and system status in real-time,
replicating the stdout of the bitget_live_trader.py to a web UI.
"""

import asyncio
import json
import random
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any, Set
import os
import sys
import logging
from pathlib import Path

import redis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create a global FastAPI app instance for uvicorn to find
app = FastAPI(title="OMEGA BTC AI - Rasta Orders Dashboard")

# Attempt to import BitGetLiveTraders - this may be used for direct integration
try:
    from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
    LIVE_TRADERS_AVAILABLE = True
except ImportError:
    LIVE_TRADERS_AVAILABLE = False
    print("BitGetLiveTraders not available - will use simulated data")

# ANSI color codes for Rastafarian-themed colorful output
GREEN_RASTA = "\033[38;5;34m"    # Bright green (primary color)
GOLD_RASTA = "\033[38;5;220m"    # Gold/Yellow (secondary color)
RED_RASTA = "\033[38;5;196m"     # Bright red (tertiary color)
BLACK_RASTA = "\033[38;5;232m"   # Deep black
CYAN_INFO = "\033[38;5;51m"      # Cyan for information
BOLD = "\033[1m"                 # Bold text
RESET = "\033[0m"                # Reset formatting

# Configure logging with colors
class RastaColoredFormatter(logging.Formatter):
    """Custom formatter for Rastafarian-themed colorful logs."""
    FORMATS = {
        logging.DEBUG: f"{BLACK_RASTA}%(asctime)s - {CYAN_INFO}%(name)s{RESET} - {CYAN_INFO}%(levelname)s{RESET} - %(message)s",
        logging.INFO: f"{BLACK_RASTA}%(asctime)s - {GREEN_RASTA}%(name)s{RESET} - {GREEN_RASTA}%(levelname)s{RESET} - {GREEN_RASTA}%(message)s{RESET}",
        logging.WARNING: f"{BLACK_RASTA}%(asctime)s - {GOLD_RASTA}%(name)s{RESET} - {GOLD_RASTA}%(levelname)s{RESET} - {GOLD_RASTA}%(message)s{RESET}",
        logging.ERROR: f"{BLACK_RASTA}%(asctime)s - {RED_RASTA}%(name)s{RESET} - {RED_RASTA}%(levelname)s{RESET} - {RED_RASTA}%(message)s{RESET}",
        logging.CRITICAL: f"{BLACK_RASTA}%(asctime)s - {RED_RASTA}{BOLD}%(name)s{RESET} - {RED_RASTA}{BOLD}%(levelname)s{RESET} - {RED_RASTA}{BOLD}%(message)s{RESET}",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Configure logging with colors
handler = logging.StreamHandler()
handler.setFormatter(RastaColoredFormatter())
logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)
logger = logging.getLogger("rasta_orders_dashboard")

class OrdersWebSocketManager:
    """Manager for WebSocket connections."""
    
    def __init__(self):
        """Initialize WebSocket connection manager."""
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accept and store a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"{GREEN_RASTA}New WebSocket client connected: {len(self.active_connections)} active connections{RESET}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a disconnected WebSocket."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"{GOLD_RASTA}WebSocket client disconnected: {len(self.active_connections)} active connections remaining{RESET}")
    
    async def broadcast(self, message: Dict):
        """Send a message to all connected WebSocket clients."""
        if not self.active_connections:
            return
        
        # Add timestamp to message
        if "timestamp" not in message:
            message["timestamp"] = datetime.now(timezone.utc).isoformat()
        
        # Serialize message to JSON
        json_message = json.dumps(message)
        
        # Send to all connected clients
        for connection in self.active_connections:
            try:
                await connection.send_text(json_message)
            except Exception as e:
                logger.error(f"{RED_RASTA}Error sending message to WebSocket client: {str(e)}{RESET}")
                # Don't disconnect here - wait for the actual disconnect event

class OrdersDataStore:
    """Store and manage order and trading data."""
    
    def __init__(self):
        """Initialize data store."""
        # Order history
        self.orders: List[Dict] = []
        self.positions: Dict[str, Dict] = {}
        self.system_status: Dict = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "is_running": False,
            "traders": {},
            "total_pnl": 0.0,
            "active_positions": 0
        }
        
        # Keep limited history (last 1000 orders)
        self.max_orders = 1000
        
        # Redis client for data persistence
        self.redis_client = self._init_redis_client()
        
        # Load initial data from Redis if available
        self._load_initial_data()
    
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
            logger.info(f"{GREEN_RASTA}Connected to Redis at {redis_host}:{redis_port}{RESET}")
            return client
        except Exception as e:
            logger.warning(f"{GOLD_RASTA}Failed to connect to Redis: {e} - using in-memory storage{RESET}")
            return None
    
    def _load_initial_data(self):
        """Load initial data from Redis if available."""
        if not self.redis_client:
            return
        
        try:
            # Load orders
            orders_json = self.redis_client.get("orders_history")
            if orders_json:
                self.orders = json.loads(orders_json)
                if len(self.orders) > self.max_orders:
                    self.orders = self.orders[-self.max_orders:]
            
            # Load positions
            positions_json = self.redis_client.get("current_positions")
            if positions_json:
                self.positions = json.loads(positions_json)
            
            # Load system status
            status_json = self.redis_client.get("system_status")
            if status_json:
                self.system_status.update(json.loads(status_json))
            
            logger.info(f"{GREEN_RASTA}Loaded initial data from Redis: {len(self.orders)} orders, {len(self.positions)} positions{RESET}")
        except Exception as e:
            logger.error(f"{RED_RASTA}Error loading initial data from Redis: {str(e)}{RESET}")
    
    def add_order(self, order: Dict):
        """Add a new order to the history."""
        # Add timestamp if not present
        if "timestamp" not in order:
            order["timestamp"] = datetime.now(timezone.utc).isoformat()
        
        # Add order to history
        self.orders.append(order)
        
        # Trim history if needed
        if len(self.orders) > self.max_orders:
            self.orders = self.orders[-self.max_orders:]
        
        # Save to Redis if available
        if self.redis_client:
            try:
                self.redis_client.set("orders_history", json.dumps(self.orders))
            except Exception as e:
                logger.error(f"{RED_RASTA}Error saving orders to Redis: {str(e)}{RESET}")
    
    def update_positions(self, positions: Dict):
        """Update current positions."""
        self.positions = positions
        
        # Save to Redis if available
        if self.redis_client:
            try:
                self.redis_client.set("current_positions", json.dumps(self.positions))
            except Exception as e:
                logger.error(f"{RED_RASTA}Error saving positions to Redis: {str(e)}{RESET}")
    
    def update_system_status(self, status: Dict):
        """Update system status."""
        self.system_status.update(status)
        
        # Save to Redis if available
        if self.redis_client:
            try:
                self.redis_client.set("system_status", json.dumps(self.system_status))
            except Exception as e:
                logger.error(f"{RED_RASTA}Error saving system status to Redis: {str(e)}{RESET}")
    
    def get_orders(self, limit: int = 100) -> List[Dict]:
        """Get recent orders."""
        return self.orders[-limit:] if self.orders else []
    
    def get_positions(self) -> Dict[str, Dict]:
        """Get current positions."""
        return self.positions
    
    def get_system_status(self) -> Dict:
        """Get system status."""
        return self.system_status

class RastaOrdersDashboardServer:
    """
    Server for the Rasta Orders Dashboard that provides real-time
    BitGet live trading order information.
    """
    
    def __init__(self, port: int = 8420):
        """Initialize the dashboard server with WebSocket support."""
        # Use the global app instance
        self.app = app
        self.port = port
        
        # WebSocket connection manager
        self.ws_manager = OrdersWebSocketManager()
        
        # Data store
        self.data_store = OrdersDataStore()
        
        # CORS middleware for frontend connections
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # In production, replace with specific origins
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Mount static files for the dashboard
        static_dir = Path("omega_ai/visualizer/frontend/orders-dashboard/static").absolute()
        self.app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
        
        # Set up routes
        self.setup_routes()
        
        # Background task for generating order updates
        self.update_task = None
        self.is_running = False
    
    def setup_routes(self):
        """Set up API routes and WebSocket endpoint."""
        
        @self.app.get("/")
        async def root():
            """Root endpoint that redirects to the dashboard."""
            return RedirectResponse(url="/dashboard")
        
        @self.app.get("/dashboard", response_class=HTMLResponse)
        async def dashboard():
            """Serve the dashboard HTML page."""
            dashboard_path = Path("omega_ai/visualizer/frontend/orders-dashboard/index.html").absolute()
            if dashboard_path.exists():
                return FileResponse(dashboard_path)
            else:
                # Return basic HTML if file doesn't exist
                return """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>OMEGA BTC AI - Rasta Orders Dashboard</title>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
                            padding-bottom: 10px;
                        }
                        .container {
                            max-width: 800px;
                            margin: 0 auto;
                            background-color: #1E1E1E;
                            padding: 30px;
                            border-radius: 8px;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>OMEGA BTC AI - Rasta Orders Dashboard</h1>
                        <p>Dashboard frontend not found. Please build the frontend files.</p>
                    </div>
                </body>
                </html>
                """
        
        @self.app.get("/api/health")
        async def health_check():
            """Check system health."""
            redis_health = bool(self.data_store.redis_client)
            return {
                "status": "operational",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "redis": "connected" if redis_health else "disconnected"
            }
        
        @self.app.get("/api/orders")
        async def get_orders(limit: int = 100):
            """Get recent orders."""
            return {
                "orders": self.data_store.get_orders(limit),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        @self.app.get("/api/positions")
        async def get_positions():
            """Get current positions."""
            return {
                "positions": self.data_store.get_positions(),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        @self.app.get("/api/system")
        async def get_system_status():
            """Get system status."""
            return {
                "system": self.data_store.get_system_status(),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        @self.app.get("/api/combined")
        async def get_combined_data():
            """Get all data combined."""
            return {
                "orders": self.data_store.get_orders(100),
                "positions": self.data_store.get_positions(),
                "system": self.data_store.get_system_status(),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time updates."""
            await self.ws_manager.connect(websocket)
            
            # Send initial data
            initial_data = {
                "type": "initial_data",
                "orders": self.data_store.get_orders(100),
                "positions": self.data_store.get_positions(),
                "system": self.data_store.get_system_status(),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            await websocket.send_text(json.dumps(initial_data))
            
            try:
                # Keep connection alive and process any client messages
                while True:
                    data = await websocket.receive_text()
                    # Could process client messages here if needed
                    logger.debug(f"Received message from client: {data}")
            except WebSocketDisconnect:
                self.ws_manager.disconnect(websocket)
    
    async def simulate_live_trading(self):
        """Simulate live trading data for development/demo purposes."""
        logger.info(f"{GREEN_RASTA}Starting simulated trading data generation{RESET}")
        
        # Trader profiles
        trader_profiles = ["strategic", "aggressive", "newbie", "scalper"]
        
        # Trading pairs
        trading_pairs = ["BTC/USDT:USDT"]
        
        # Initialize system status
        system_status = {
            "is_running": True,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "traders": {profile: {"total_pnl": 0.0, "win_rate": 0.0} for profile in trader_profiles},
            "total_pnl": 0.0,
            "active_positions": 0
        }
        self.data_store.update_system_status(system_status)
        await self.ws_manager.broadcast({"type": "system_update", "system": system_status})
        
        # Initialize prices
        btc_price = 50000.0
        
        # Main simulation loop
        while self.is_running:
            try:
                # Update BTC price with some randomness (between -1% and +1%)
                price_change = btc_price * (random.uniform(-0.01, 0.01))
                btc_price += price_change
                
                # Generate random events
                for profile in trader_profiles:
                    if random.random() < 0.1:  # 10% chance of a trading event
                        # Determine event type
                        event_type = random.choice(["new_order", "close_position", "add_to_position", "system_update"])
                        
                        if event_type == "new_order":
                            # Generate new order
                            side = random.choice(["long", "short"])
                            symbol = random.choice(trading_pairs)
                            order = {
                                "type": "new_order",
                                "profile": profile,
                                "symbol": symbol,
                                "side": side,
                                "price": btc_price,
                                "size": round(random.uniform(0.001, 0.1), 3),
                                "leverage": random.choice([1, 2, 3, 5, 10, 20]),
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                                "order_id": f"order_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
                                "status": "filled"
                            }
                            
                            # Add to orders history
                            self.data_store.add_order(order)
                            
                            # Add to positions
                            position_id = f"{profile}_{symbol}_{side}"
                            self.data_store.positions[position_id] = {
                                "profile": profile,
                                "symbol": symbol,
                                "side": side,
                                "entry_price": btc_price,
                                "size": order["size"],
                                "leverage": order["leverage"],
                                "unrealized_pnl": 0.0,
                                "opened_at": datetime.now(timezone.utc).isoformat()
                            }
                            
                            # Update system status
                            system_status["active_positions"] = len(self.data_store.positions)
                            self.data_store.update_system_status(system_status)
                            
                            # Send updates
                            await self.ws_manager.broadcast(order)
                            await self.ws_manager.broadcast({
                                "type": "position_update", 
                                "positions": self.data_store.positions
                            })
                            await self.ws_manager.broadcast({
                                "type": "system_update", 
                                "system": system_status
                            })
                            
                            logger.info(f"{GREEN_RASTA}New {side} order for {profile}: {order['size']} @ ${btc_price:.2f}{RESET}")
                            
                        elif event_type == "close_position" and self.data_store.positions:
                            # Close a random position
                            position_id = random.choice(list(self.data_store.positions.keys()))
                            position = self.data_store.positions[position_id]
                            
                            # Calculate PnL
                            entry_price = position["entry_price"]
                            size = position["size"]
                            leverage = position["leverage"]
                            
                            if position["side"] == "long":
                                pnl = (btc_price - entry_price) / entry_price * size * entry_price * leverage
                            else:
                                pnl = (entry_price - btc_price) / entry_price * size * entry_price * leverage
                            
                            # Generate close order
                            close_order = {
                                "type": "close_position",
                                "profile": position["profile"],
                                "symbol": position["symbol"],
                                "side": "sell" if position["side"] == "long" else "buy",
                                "price": btc_price,
                                "size": position["size"],
                                "pnl": round(pnl, 2),
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                                "order_id": f"order_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
                                "status": "filled"
                            }
                            
                            # Add to orders history
                            self.data_store.add_order(close_order)
                            
                            # Update trader PnL
                            system_status["traders"][position["profile"]]["total_pnl"] += pnl
                            system_status["total_pnl"] += pnl
                            
                            # Update win rate
                            total_trades = len([o for o in self.data_store.orders if o["profile"] == position["profile"] and o["type"] == "close_position"])
                            winning_trades = len([o for o in self.data_store.orders if o["profile"] == position["profile"] and o["type"] == "close_position" and o.get("pnl", 0) > 0])
                            system_status["traders"][position["profile"]]["win_rate"] = winning_trades / max(total_trades, 1)
                            
                            # Remove position
                            del self.data_store.positions[position_id]
                            
                            # Update system status
                            system_status["active_positions"] = len(self.data_store.positions)
                            self.data_store.update_system_status(system_status)
                            
                            # Send updates
                            await self.ws_manager.broadcast(close_order)
                            await self.ws_manager.broadcast({
                                "type": "position_update", 
                                "positions": self.data_store.positions
                            })
                            await self.ws_manager.broadcast({
                                "type": "system_update", 
                                "system": system_status
                            })
                            
                            logger.info(f"{GOLD_RASTA}Closed position for {position['profile']}: {position['side']} {position['size']} with PnL ${pnl:.2f}{RESET}")
                            
                        elif event_type == "add_to_position" and self.data_store.positions:
                            # Add to a random position
                            position_id = random.choice(list(self.data_store.positions.keys()))
                            position = self.data_store.positions[position_id]
                            
                            # Generate additional size
                            additional_size = round(position["size"] * random.uniform(0.1, 0.5), 3)
                            
                            # Generate add order
                            add_order = {
                                "type": "add_to_position",
                                "profile": position["profile"],
                                "symbol": position["symbol"],
                                "side": position["side"],
                                "price": btc_price,
                                "size": additional_size,
                                "leverage": position["leverage"],
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                                "order_id": f"order_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
                                "status": "filled"
                            }
                            
                            # Add to orders history
                            self.data_store.add_order(add_order)
                            
                            # Update position
                            new_size = position["size"] + additional_size
                            new_entry_price = (position["entry_price"] * position["size"] + btc_price * additional_size) / new_size
                            
                            position["size"] = new_size
                            position["entry_price"] = new_entry_price
                            
                            # Update positions
                            self.data_store.positions[position_id] = position
                            
                            # Send updates
                            await self.ws_manager.broadcast(add_order)
                            await self.ws_manager.broadcast({
                                "type": "position_update", 
                                "positions": self.data_store.positions
                            })
                            
                            logger.info(f"{CYAN_INFO}Added {additional_size} to {position['side']} position for {position['profile']} @ ${btc_price:.2f}{RESET}")
                            
                        elif event_type == "system_update":
                            # Update system status with current market info
                            market_update = {
                                "type": "market_update",
                                "price": btc_price,
                                "timestamp": datetime.now(timezone.utc).isoformat()
                            }
                            
                            # Send update
                            await self.ws_manager.broadcast(market_update)
                
                # Update unrealized PnL for all positions
                for position_id, position in self.data_store.positions.items():
                    entry_price = position["entry_price"]
                    size = position["size"]
                    leverage = position["leverage"]
                    
                    if position["side"] == "long":
                        unrealized_pnl = (btc_price - entry_price) / entry_price * size * entry_price * leverage
                    else:
                        unrealized_pnl = (entry_price - btc_price) / entry_price * size * entry_price * leverage
                    
                    position["unrealized_pnl"] = round(unrealized_pnl, 2)
                    self.data_store.positions[position_id] = position
                
                # Send position updates with updated PnL
                if self.data_store.positions:
                    await self.ws_manager.broadcast({
                        "type": "position_update", 
                        "positions": self.data_store.positions
                    })
                
                # Sleep for a random interval (0.5-2 seconds)
                await asyncio.sleep(random.uniform(0.5, 2))
                
            except Exception as e:
                logger.error(f"{RED_RASTA}Error in simulation loop: {str(e)}{RESET}")
                await asyncio.sleep(1)
    
    async def startup(self):
        """Start the dashboard server and background tasks."""
        logger.info(f"{GREEN_RASTA}Starting Rasta Orders Dashboard Server on port {self.port}{RESET}")
        self.is_running = True
        
        # Start simulated data generation
        self.update_task = asyncio.create_task(self.simulate_live_trading())
    
    async def shutdown(self):
        """Shutdown the dashboard server and cleanup resources."""
        logger.info(f"{GOLD_RASTA}Shutting down Rasta Orders Dashboard Server{RESET}")
        self.is_running = False
        
        # Cancel background task
        if self.update_task:
            self.update_task.cancel()
            try:
                await self.update_task
            except asyncio.CancelledError:
                pass

# Global server instance
server = None

def run_server(port: int = 8420):
    """Run the dashboard server."""
    global server
    # Create and configure the server
    server = RastaOrdersDashboardServer(port=port)
    
    # Initialize server before setting up event handlers
    startup_handler = server.startup
    shutdown_handler = server.shutdown
    
    # Set up event handlers
    @app.on_event("startup")
    async def startup_event():
        await startup_handler()
    
    @app.on_event("shutdown")
    async def shutdown_event():
        await shutdown_handler()
    
    # Run uvicorn directly using the command line interface
    if __name__ == "__main__":
        import argparse
        
        parser = argparse.ArgumentParser(description="Run the Rasta Orders Dashboard Server")
        parser.add_argument("--port", type=int, default=8420, help="Port to run the server on (default: 8420)")
        
        args = parser.parse_args()
        
        # Set up the server with provided port
        run_server(port=args.port)
        
        # Run the uvicorn server
        uvicorn.run("rasta_orders_dashboard_server:app", host="0.0.0.0", port=args.port) 