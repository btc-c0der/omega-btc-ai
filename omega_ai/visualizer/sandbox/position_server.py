#!/usr/bin/env python3

"""
OMEGA BTC AI - Position WebSocket Server

This server provides real-time updates for trading positions, including:
- Entry and current prices
- PnL calculations
- Position size and leverage
- Take profit and stop loss levels
"""

import os
import sys
import json
import asyncio
import random
import logging
import socket
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

def find_available_port(start_port: int = 5000, max_port: int = 5999) -> int:
    """Find an available port by scanning from start_port to max_port."""
    for port in range(start_port, max_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"No available ports found between {start_port} and {max_port}")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="OMEGA BTC AI - Position Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active WebSocket connections
active_connections: List[WebSocket] = []

# Store the selected port for access by other components
selected_port: int = -1

# Current position data
position_data = {
    "has_position": False,
    "position": None,
    "timestamp": datetime.now().isoformat()
}

# Mount static files for the dashboard
frontend_path = os.path.join(os.path.dirname(__file__), "dashboard")
if os.path.exists(frontend_path):
    app.mount("/dashboard", StaticFiles(directory=frontend_path, html=True), name="dashboard")
    logger.info(f"Mounted frontend files from {frontend_path}")
else:
    logger.warning(f"Frontend directory not found at {frontend_path}")

async def update_position():
    """Update position with simulated data."""
    while True:
        try:
            # 30% chance to open/close position
            if random.random() < 0.3:
                if not position_data["has_position"] and random.random() < 0.6:
                    # Open new position
                    entry_price = 50000 + random.uniform(-1000, 1000)
                    position_data.update({
                        "has_position": True,
                        "position": {
                            "size": random.uniform(0.1, 1.0),
                            "leverage": random.choice([1, 2, 3, 5, 10, 20]),
                            "entry_price": entry_price,
                            "current_price": entry_price,
                            "liquidation_price": entry_price * (0.8 if random.random() > 0.5 else 1.2),
                            "pnl_percentage": 0.0,
                            "pnl_usd": 0.0,
                            "margin_ratio": random.uniform(20, 50),
                            "take_profit": entry_price * 1.1,
                            "stop_loss": entry_price * 0.9
                        },
                        "timestamp": datetime.now().isoformat()
                    })
                elif position_data["has_position"] and random.random() < 0.2:
                    # Close position
                    position_data.update({
                        "has_position": False,
                        "position": None,
                        "timestamp": datetime.now().isoformat()
                    })
            
            # Update existing position
            if position_data["has_position"]:
                position = position_data["position"]
                # Update current price
                price_change = random.uniform(-100, 100)
                position["current_price"] += price_change
                
                # Calculate PnL
                price_diff = position["current_price"] - position["entry_price"]
                position["pnl_percentage"] = (price_diff / position["entry_price"]) * 100 * position["leverage"]
                position["pnl_usd"] = price_diff * position["size"] * position["leverage"]
                
                # Update margin ratio
                position["margin_ratio"] = max(0, position["margin_ratio"] + random.uniform(-1, 1))
            
            # Broadcast updates to all connected clients
            if active_connections:
                await broadcast_position_data()
            
            # Wait before next update
            await asyncio.sleep(1)
            
        except Exception as e:
            logger.error(f"Error updating position: {e}")
            await asyncio.sleep(1)

async def broadcast_position_data():
    """Broadcast position data to all connected clients."""
    if not active_connections:
        return
    
    # Broadcast to all connections
    for connection in active_connections:
        try:
            await connection.send_json(position_data)
        except Exception as e:
            logger.error(f"Error broadcasting to client: {e}")
            active_connections.remove(connection)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections."""
    await websocket.accept()
    active_connections.append(websocket)
    logger.info(f"New WebSocket connection. Total connections: {len(active_connections)}")
    
    try:
        # Send initial data
        await websocket.send_json(position_data)
        
        # Keep connection alive
        while True:
            await websocket.receive_text()
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        active_connections.remove(websocket)
        logger.info(f"WebSocket connection closed. Remaining connections: {len(active_connections)}")

@app.get("/position")
async def get_position():
    """Get current position data."""
    return position_data

@app.post("/close_position")
async def close_position():
    """Close the current position."""
    if position_data["has_position"]:
        position_data.update({
            "has_position": False,
            "position": None,
            "timestamp": datetime.now().isoformat()
        })
        return {"success": True}
    return {"success": False, "error": "No position to close"}

@app.on_event("startup")
async def startup_event():
    """Start background tasks on server startup."""
    asyncio.create_task(update_position())

if __name__ == "__main__":
    import uvicorn
    
    # Define port file path
    port_file = os.path.join(os.path.dirname(__file__), 'position_server_port.txt')
    
    try:
        # Find an available port
        port = find_available_port(5000, 5999)
        selected_port = port
        
        # Create a file to store the port number for other components
        with open(port_file, 'w') as f:
            f.write(str(port))
        
        logger.info(f"Selected available port: {port}")
        logger.info(f"Port number saved to: {port_file}")
        
        # Run the server
        uvicorn.run("position_server:app", host="0.0.0.0", port=port)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)
    finally:
        # Clean up port file
        try:
            if os.path.exists(port_file):
                os.remove(port_file)
        except Exception as e:
            logger.error(f"Failed to clean up port file: {e}") 