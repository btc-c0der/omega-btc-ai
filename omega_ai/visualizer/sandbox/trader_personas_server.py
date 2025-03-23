#!/usr/bin/env python3

"""
OMEGA BTC AI - Trader Personas WebSocket Server

This server provides real-time updates for trader personas, including:
- Psychological state and divine metrics
- Performance statistics
- Position updates
- Enlightenment progress
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
app = FastAPI(title="OMEGA BTC AI - Trader Personas Server")

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
selected_port: int = -1  # Initialize with invalid port

# Trader personas data
trader_personas = {
    "strategic": {
        "profile": "strategic",
        "name": "Strategic Fibonacci Trader",
        "capital": 10000.0,
        "pnl": 0.0,
        "winRate": 0.0,
        "emotionalState": "neutral",
        "divineConnection": 0.6,
        "riskLevel": 0.4,
        "confidence": 0.7,
        "enlightenedTrades": 0,
        "positions": []
    },
    "aggressive": {
        "profile": "aggressive",
        "name": "Aggressive Momentum Trader",
        "capital": 10000.0,
        "pnl": 0.0,
        "winRate": 0.0,
        "emotionalState": "greedy",
        "divineConnection": 0.3,
        "riskLevel": 0.8,
        "confidence": 0.9,
        "enlightenedTrades": 0,
        "positions": []
    },
    "newbie": {
        "profile": "newbie",
        "name": "YOLO Crypto Influencer Follower",
        "capital": 10000.0,
        "pnl": 0.0,
        "winRate": 0.0,
        "emotionalState": "fearful",
        "divineConnection": 0.1,
        "riskLevel": 0.9,
        "confidence": 0.4,
        "enlightenedTrades": 0,
        "positions": []
    },
    "scalper": {
        "profile": "scalper",
        "name": "Order Book Scalper",
        "capital": 10000.0,
        "pnl": 0.0,
        "winRate": 0.0,
        "emotionalState": "neutral",
        "divineConnection": 0.4,
        "riskLevel": 0.6,
        "confidence": 0.8,
        "enlightenedTrades": 0,
        "positions": []
    },
    "yolo": {
        "profile": "yolo",
        "name": "Divine YOLO Trader",
        "capital": 10000.0,
        "pnl": 0.0,
        "winRate": 0.0,
        "emotionalState": "fomo",
        "divineConnection": 0.2,
        "riskLevel": 1.0,
        "confidence": 1.0,
        "enlightenedTrades": 0,
        "positions": []
    }
}

# Emotional states by profile
emotional_states = {
    "strategic": ["neutral", "mindful", "zen", "enlightened", "focused"],
    "aggressive": ["greedy", "confident", "fearful", "revenge", "euphoric"],
    "newbie": ["fearful", "fomo", "panic", "euphoric", "confused"],
    "scalper": ["neutral", "focused", "anxious", "confident", "stressed"],
    "yolo": ["fomo", "euphoric", "revenge", "panic", "enlightened"]
}

async def update_trader_personas():
    """Update trader personas with simulated data."""
    while True:
        try:
            # Update each trader's metrics
            for profile, trader in trader_personas.items():
                # Random PnL changes
                pnl_change = random.uniform(-100, 100)
                trader["pnl"] += pnl_change
                
                # Update win rate based on PnL
                if abs(trader["winRate"]) < 0.001:  # Initialize win rate
                    trader["winRate"] = random.uniform(0.4, 0.6)
                else:
                    win_rate_change = 0.01 if pnl_change > 0 else -0.01
                    trader["winRate"] = max(0.0, min(1.0, trader["winRate"] + win_rate_change))
                
                # Update emotional state
                if random.random() < 0.2:  # 20% chance to change emotional state
                    trader["emotionalState"] = random.choice(emotional_states[profile])
                
                # Update divine connection
                if profile == "strategic" and trader["emotionalState"] in ["mindful", "zen", "enlightened"]:
                    trader["divineConnection"] = min(1.0, trader["divineConnection"] + 0.01)
                elif profile == "yolo" and trader["emotionalState"] in ["fomo", "panic"]:
                    trader["divineConnection"] = max(0.0, trader["divineConnection"] - 0.01)
                
                # Update confidence based on recent performance
                confidence_change = 0.02 if pnl_change > 0 else -0.02
                trader["confidence"] = max(0.1, min(1.0, trader["confidence"] + confidence_change))
                
                # Update risk level based on emotional state
                if trader["emotionalState"] in ["fearful", "panic"]:
                    trader["riskLevel"] = max(0.1, trader["riskLevel"] - 0.05)
                elif trader["emotionalState"] in ["greedy", "euphoric", "fomo"]:
                    trader["riskLevel"] = min(1.0, trader["riskLevel"] + 0.05)
                
                # Random chance to open/close positions
                if random.random() < 0.3:  # 30% chance to modify positions
                    if not trader["positions"] and random.random() < 0.6:  # 60% chance to open position
                        price = 50000 + random.uniform(-1000, 1000)
                        size = random.uniform(0.1, 1.0)
                        trader["positions"].append({
                            "size": size,
                            "entryPrice": price,
                            "currentPrice": price,
                            "pnl": 0.0,
                            "liquidationPrice": price * (0.8 if random.random() > 0.5 else 1.2),
                            "takeProfit": price * 1.1,
                            "stopLoss": price * 0.9
                        })
                    elif trader["positions"]:  # Update or close existing positions
                        for position in trader["positions"]:
                            if random.random() < 0.2:  # 20% chance to close position
                                trader["positions"].remove(position)
                            else:  # Update position prices
                                price_change = random.uniform(-100, 100)
                                position["currentPrice"] += price_change
                                position["pnl"] = (position["currentPrice"] - position["entryPrice"]) * position["size"]
                
                # Update enlightened trades
                if trader["emotionalState"] in ["mindful", "zen", "enlightened"] and random.random() < 0.1:
                    trader["enlightenedTrades"] += 1
            
            # Broadcast updates to all connected clients
            if active_connections:
                await broadcast_trader_data()
            
            # Wait before next update
            await asyncio.sleep(1)
            
        except Exception as e:
            logger.error(f"Error updating trader personas: {e}")
            await asyncio.sleep(1)

async def broadcast_trader_data():
    """Broadcast trader data to all connected clients."""
    if not active_connections:
        return
        
    # Prepare data
    data = {
        "traders": list(trader_personas.values()),
        "timestamp": datetime.now().isoformat()
    }
    
    # Broadcast to all connections
    for connection in active_connections:
        try:
            await connection.send_json(data)
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
        await websocket.send_json({
            "traders": list(trader_personas.values()),
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep connection alive
        while True:
            await websocket.receive_text()
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        active_connections.remove(websocket)
        logger.info(f"WebSocket connection closed. Remaining connections: {len(active_connections)}")

@app.on_event("startup")
async def startup_event():
    """Start background tasks on server startup."""
    asyncio.create_task(update_trader_personas())

if __name__ == "__main__":
    import uvicorn
    
    # Define port file path
    port_file = os.path.join(os.path.dirname(__file__), 'trader_personas_port.txt')
    
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
        uvicorn.run("trader_personas_server:app", host="0.0.0.0", port=port)
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