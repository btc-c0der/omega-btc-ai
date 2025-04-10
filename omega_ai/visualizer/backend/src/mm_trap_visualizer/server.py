
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

"""Market Maker Trap Visualizer Server."""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import logging
import asyncio
from pydantic import BaseModel

class TrapData(BaseModel):
    """Data model for market maker traps."""
    id: str
    type: str
    timestamp: datetime
    confidence: float
    price: float
    volume: float
    description: str
    success: bool

class MetricsResponse(BaseModel):
    """Response model for trap metrics."""
    total_traps: int
    traps_by_type: Dict[str, int]
    average_confidence: float
    success_rate: float

class TimelineEvent(BaseModel):
    """Data model for timeline events."""
    type: str
    timestamp: datetime
    impact: str
    description: str
    price: float
    volume: float

class MMTrapVisualizerServer:
    """Server for visualizing market maker traps."""
    
    def __init__(self, title: str, redis_manager):
        """Initialize the server."""
        self.title = title
        self.redis_manager = redis_manager
        self.app = FastAPI(title=title)
        self.active_connections: List[WebSocket] = []
        
        # Setup CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Mount static files
        static_dir = Path(__file__).parent.parent / "static"
        if static_dir.exists():
            self.app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
        
        # Setup routes
        self.setup_routes()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def setup_routes(self):
        """Setup API routes."""
        @self.app.get("/")
        async def root():
            """Root endpoint."""
            return {"message": "Welcome to MM Trap Visualizer API"}
        
        @self.app.get("/api/traps")
        async def get_traps():
            """Get all traps from Redis."""
            try:
                data = self.redis_manager.get_cached()
                # Convert datetime objects to ISO format strings
                if 'traps' in data:
                    for trap in data['traps']:
                        if 'timestamp' in trap:
                            trap['timestamp'] = trap['timestamp'].isoformat()
                return JSONResponse(content=data)
            except Exception as e:
                self.logger.error(f"Error getting traps: {e}")
                return JSONResponse(
                    status_code=500,
                    content={"error": "Failed to get traps"}
                )
        
        @self.app.get("/api/metrics")
        async def get_metrics():
            """Get trap metrics."""
            try:
                data = self.redis_manager.get_cached()
                traps = data.get('traps', [])
                
                metrics = MetricsResponse(
                    total_traps=len(traps),
                    traps_by_type={},
                    average_confidence=0.0,
                    success_rate=0.0
                )
                
                if traps:
                    # Calculate metrics
                    type_counts = {}
                    total_confidence = 0.0
                    success_count = 0
                    
                    for trap in traps:
                        trap_type = trap['type']
                        type_counts[trap_type] = type_counts.get(trap_type, 0) + 1
                        total_confidence += trap['confidence']
                        if trap['success']:
                            success_count += 1
                    
                    metrics.traps_by_type = type_counts
                    metrics.average_confidence = total_confidence / len(traps)
                    metrics.success_rate = success_count / len(traps)
                
                return metrics
            except Exception as e:
                self.logger.error(f"Error getting metrics: {e}")
                return JSONResponse(
                    status_code=500,
                    content={"detail": f"Error getting metrics: {str(e)}"}
                )
        
        @self.app.get("/api/timeline")
        async def get_timeline():
            """Get trap timeline."""
            try:
                data = self.redis_manager.get_cached()
                traps = data.get('traps', [])
                
                timeline = []
                for trap in traps:
                    event = TimelineEvent(
                        type=trap['type'],
                        timestamp=trap['timestamp'],
                        impact="high" if trap['volume'] > 1.0 else "medium",
                        description=trap['description'],
                        price=trap['price'],
                        volume=trap['volume']
                    )
                    timeline.append(event)
                
                return timeline
            except Exception as e:
                self.logger.error(f"Error getting timeline: {e}")
                return JSONResponse(
                    status_code=500,
                    content={"error": "Failed to get timeline"}
                )
        
        @self.app.get("/api/trap-probability")
        async def get_trap_probability():
            """Get trap probability metrics."""
            try:
                data = self.redis_manager.get_cached()
                traps = data.get('traps', [])
                
                # Default values when no traps found
                if not traps:
                    return {
                        "probability": 0.0,
                        "confidence": 0.0,
                        "trend": "stable",  # Default to stable when no data
                        "components": {
                            "price_pattern": {"value": 0.0, "description": "No recent price patterns detected"},
                            "market_sentiment": {"value": 0.0, "description": "Insufficient market sentiment data"},
                            "fibonacci_match": {"value": 0.0, "description": "No Fibonacci levels matched"},
                            "liquidity_concentration": {"value": 0.0, "description": "No significant liquidity events"},
                            "order_imbalance": {"value": 0.0, "description": "No order imbalance detected"}
                        }
                    }
                
                # Get the latest two traps for trend analysis
                sorted_traps = sorted(traps, key=lambda x: x['timestamp'])
                latest_traps = sorted_traps[-2:]
                
                # Calculate trend based on price movement
                if len(latest_traps) >= 2:
                    price_change = latest_traps[1]['price'] - latest_traps[0]['price']
                    if abs(price_change) < 0.01:  # If change is very small
                        trend = "stable"
                    else:
                        trend = "bullish" if price_change > 0 else "bearish"
                else:
                    trend = "stable"  # Default to stable if not enough data
                
                # Calculate components based on latest trap
                latest_trap = sorted_traps[-1]
                volume_normalized = min(1.0, latest_trap.get('volume', 0) / 100.0)  # Normalize volume to 0-1
                
                return {
                    "probability": min(1.0, latest_trap.get('confidence', 0)),
                    "confidence": min(1.0, latest_trap.get('confidence', 0)),
                    "trend": trend,  # Will always be one of: bullish, bearish, or stable
                    "components": {
                        "price_pattern": {"value": 0.7, "description": "Recent price pattern analysis"},
                        "market_sentiment": {"value": 0.5, "description": "Current market sentiment"},
                        "fibonacci_match": {"value": 0.6, "description": "Fibonacci level alignment"},
                        "liquidity_concentration": {"value": volume_normalized, "description": "Normalized trading volume"},
                        "order_imbalance": {"value": 0.5, "description": "Buy/Sell order ratio"}
                    }
                }
            except Exception as e:
                self.logger.error(f"Error getting trap probability: {e}")
                return JSONResponse(
                    status_code=500,
                    content={"detail": f"Error getting trap probability: {str(e)}"}
                )
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time updates."""
            await websocket.accept()
            self.active_connections.append(websocket)
            try:
                while True:
                    data = await websocket.receive_text()
                    # Broadcast to all connected clients
                    for connection in self.active_connections:
                        await connection.send_text(data)
            except Exception as e:
                self.logger.error(f"WebSocket error: {e}")
            finally:
                self.active_connections.remove(websocket)
    
    async def broadcast_trap(self, trap_data: Dict[str, Any]):
        """Broadcast trap data to all connected clients."""
        for connection in self.active_connections:
            try:
                await connection.send_json(trap_data)
            except Exception as e:
                self.logger.error(f"Error broadcasting trap: {e}")
                self.active_connections.remove(connection)

 