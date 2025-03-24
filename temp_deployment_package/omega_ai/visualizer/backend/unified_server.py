"""
Unified OMEGA BTC AI Trap Visualizer Server
=========================================
A comprehensive FastAPI server for monitoring BTC market manipulation traps.
Implements advanced logging, security features, and real-time WebSocket updates.
"""

from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator, ValidationError
from typing import Dict, List, Optional, Union, Set, Any
import json
import logging
import time
from datetime import datetime, timedelta, UTC
import hashlib
import uuid
import asyncio
import re
import html
from omega_ai.visualizer.backend.base_server import BaseVisualizationServer
from omega_ai.utils.redis_manager import RedisManager

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s 🎯 %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("omega_trap_visualizer")

# Constants
MAX_PAYLOAD_SIZE = 1000
VALID_TRAP_TYPES = {'FAKE_PUMP', 'FAKE_DUMP', 'WASH_TRADE', 'SPOOFING'}

class ConnectionManager:
    """Manages WebSocket connections and broadcasts."""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.last_data: Dict = {}
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"🔌 WebSocket client connected. Total connections: {len(self.active_connections)}")
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"🔌 WebSocket client disconnected. Total connections: {len(self.active_connections)}")
        
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients."""
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except RuntimeError:
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
            
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to a specific client."""
        try:
            await websocket.send_json(message)
        except RuntimeError:
            self.disconnect(websocket)

class TrapData(BaseModel):
    """Model for trap detection data."""
    id: str
    type: str
    timestamp: datetime
    confidence: float
    price: float
    volume: float
    description: str
    success: bool
    metadata: Dict[str, Union[str, float, int, bool]] = Field(default_factory=dict)

    @validator('timestamp')
    def validate_timestamp(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError('Invalid timestamp format. Expected ISO 8601 format (e.g., "2024-03-16T10:00:00Z")')
        return v

    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Confidence must be between 0 and 1')
        return v

    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v

    @validator('volume')
    def validate_volume(cls, v):
        if v < 0:
            raise ValueError('Volume cannot be negative')
        return v

    @validator('type')
    def validate_type(cls, v):
        if v not in VALID_TRAP_TYPES:
            raise ValueError(f'Invalid trap type. Must be one of: {", ".join(VALID_TRAP_TYPES)}')
        return v

class PriceData(BaseModel):
    """Model for price data."""
    time: datetime
    open: float
    close: float
    high: float
    low: float

    @validator('time')
    def validate_time(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError('Invalid timestamp format. Expected ISO 8601 format (e.g., "2024-03-16T10:00:00Z")')
        return v

    @validator('high')
    def validate_high(cls, v, values):
        if 'low' in values and v < values['low']:
            raise ValueError('High price cannot be lower than low price')
        return v

    @validator('open')
    def validate_open(cls, v, values):
        if 'high' in values and v > values['high']:
            raise ValueError('Open price cannot be higher than high price')
        if 'low' in values and v < values['low']:
            raise ValueError('Open price cannot be lower than low price')
        return v

    @validator('close')
    def validate_close(cls, v, values):
        if 'high' in values and v > values['high']:
            raise ValueError('Close price cannot be higher than high price')
        if 'low' in values and v < values['low']:
            raise ValueError('Close price cannot be lower than low price')
        return v

class MetricsResponse(BaseModel):
    """Model for metrics response."""
    total_traps: int
    traps_by_type: Dict[str, int]
    average_confidence: float
    time_distribution: Dict[str, int]
    success_rate: float

class TimelineEvent(BaseModel):
    """Model for timeline events."""
    id: str
    type: str
    timestamp: datetime
    description: str
    confidence: float
    impact: str

class TrapVisualizerServer(BaseVisualizationServer):
    """Unified server for trap visualization with WebSocket support."""
    
    def __init__(self, name: str, redis_manager: RedisManager):
        """Initialize the server."""
        super().__init__(title=name, redis_manager=redis_manager)
        self.connection_manager = ConnectionManager()
        self.register_routes()
    
    def sanitize_input(self, value: str) -> str:
        """Sanitize input string to prevent injection attacks."""
        if not isinstance(value, str):
            return value
            
        # Remove null bytes
        value = value.replace('\x00', '')
        
        # Remove path traversal attempts
        value = re.sub(r'\.\./', '', value)
        value = re.sub(r'\.\.\\', '', value)
        value = re.sub(r'%2e%2e%2f', '', value, flags=re.IGNORECASE)
        value = re.sub(r'\.\.\.\.//', '', value)
        
        # Remove XSS patterns
        value = re.sub(r'<script.*?>.*?</script>', '', value, flags=re.IGNORECASE)
        value = re.sub(r'<img.*?onerror=.*?>', '', value, flags=re.IGNORECASE)
        value = re.sub(r'<.*?on.*?=.*?>', '', value, flags=re.IGNORECASE)
        
        # Remove SQL injection patterns
        value = re.sub(r'(\s*([\0\b\'\"\n\r\t\%\_\\]*\s*(((select\s*.+\s*from\s*.+)|(insert\s*.+\s*into\s*.+)|(update\s*.+\s*set\s*.+)|(delete\s*.+\s*from\s*.+)|(drop\s*.+)|(truncate\s*.+)|(alter\s*.+)|(exec\s*.+)|(\s*(all|any|not|and|between|in|like|or|some|contains|containsall|containskey)\s*.+[\=\>\<=\!\~]+.*\s*))|(\s*[\/\*]+.*[\*\/]+)|(\s*(\-\-|\#).*\n+)|(union\s*(all)?\s*[([]\s*select)|(select\s*.+\s*from)|(insert\s*.+\s*into)|(update\s*.+\s*set)|(delete\s*.+\s*from)|(drop\s*.+)|(truncate\s*.+)|(alter\s*.+)|(exec\s*.+)|(union\s*(all)?\s*select))\s*[\;]*)+)', '', value, flags=re.IGNORECASE)
        
        # Escape any remaining HTML
        value = html.escape(value)
        
        return value
    
    async def broadcast_data_updates(self):
        """Background task to broadcast data updates to connected clients."""
        while True:
            try:
                data = self.load_latest_dump()
                current_time = datetime.now(UTC).isoformat() + "Z"
                
                # Get the last N items safely
                prices = data.get("prices", [])
                traps = data.get("traps", [])
                last_prices = prices[-100:] if prices else []
                last_traps = traps[-50:] if traps else []
                
                # Prepare update message
                update = {
                    "timestamp": current_time,
                    "prices": last_prices,
                    "traps": last_traps,
                    "metrics": self.calculate_metrics(data)
                }
                
                # Only broadcast if there are active connections
                if self.connection_manager.active_connections:
                    await self.connection_manager.broadcast(update)
                    logger.info(f"📡 Broadcasted update to {len(self.connection_manager.active_connections)} clients")
                
                # Wait before next update
                await asyncio.sleep(1)  # 1 second update interval
                
            except Exception as e:
                logger.error(f"❌ Error in broadcast task: {str(e)}")
                await asyncio.sleep(5)  # Wait longer on error
    
    def calculate_metrics(self, data: Dict) -> MetricsResponse:
        """Calculate metrics from trap data."""
        traps = data.get('traps', [])
        if not traps:
            return MetricsResponse(
                total_traps=0,
                traps_by_type={},
                average_confidence=0.0,
                time_distribution={},
                success_rate=0.0
            )
        
        # Count traps by type
        traps_by_type = {}
        total_confidence = 0
        success_count = 0
        time_dist = {f"{i:02d}-{(i+4):02d}": 0 for i in range(0, 24, 4)}
        
        for trap in traps:
            try:
                # Count by type
                trap_type = self.sanitize_input(trap.get('type', 'UNKNOWN'))
                traps_by_type[trap_type] = traps_by_type.get(trap_type, 0) + 1
                
                # Sum confidence
                confidence = trap.get('confidence', 0)
                total_confidence += confidence
                
                # Check success
                if confidence > 0.7:  # Consider high confidence as success
                    success_count += 1
                
                # Time distribution
                timestamp = trap.get('timestamp')
                if isinstance(timestamp, str):
                    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                if timestamp.tzinfo is None:
                    timestamp = timestamp.replace(tzinfo=UTC)
                hour = timestamp.hour
                time_slot = f"{(hour//4)*4:02d}-{((hour//4)*4+4):02d}"
                time_dist[time_slot] += 1
            except (ValueError, TypeError, AttributeError):
                continue
        
        return MetricsResponse(
            total_traps=len(traps),
            traps_by_type=traps_by_type,
            average_confidence=total_confidence / len(traps),
            time_distribution=time_dist,
            success_rate=success_count / len(traps)
        )
    
    def register_routes(self) -> None:
        """Register all API routes."""
        
        @self.app.middleware("http")
        async def track_requests(request: Request, call_next):
            """Track and log all incoming requests."""
            request_id = str(uuid.uuid4())
            client_host = request.client.host if request.client else "unknown"
            path = request.url.path
            
            # Calculate request signature
            content = await request.body()
            request_hash = hashlib.sha256(content).hexdigest()
            
            logger.info(f"[{request_id}] 🔥 Incoming request from {client_host}")
            logger.info(f"[{request_id}] 🎯 Target: {path}")
            logger.info(f"[{request_id}] 🔒 Request signature: {request_hash[:8]}")
            
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time
            
            logger.info(f"[{request_id}] ⚡ Response time: {process_time:.3f}s")
            return response
        
        @self.app.on_event("startup")
        async def startup_event():
            """Start background tasks on server startup."""
            asyncio.create_task(self.broadcast_data_updates())
            logger.info("🚀 Started real-time data broadcast task")
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time data streaming."""
            await self.connection_manager.connect(websocket)
            try:
                # Send initial data
                data = self.load_latest_dump()
                prices = data.get("prices", [])
                traps = data.get("traps", [])
                
                initial_data = {
                    "type": "initial",
                    "timestamp": datetime.now(UTC).isoformat() + "Z",
                    "prices": prices[-100:] if prices else [],
                    "traps": traps[-50:] if traps else [],
                    "metrics": self.calculate_metrics(data)
                }
                await self.connection_manager.send_personal_message(initial_data, websocket)
                
                # Keep connection alive and handle incoming messages
                while True:
                    data = await websocket.receive_text()
                    # Handle any client messages if needed
                    await self.connection_manager.send_personal_message({"type": "ack", "message": "received"}, websocket)
                    
            except WebSocketDisconnect:
                self.connection_manager.disconnect(websocket)
            except Exception as e:
                logger.error(f"❌ WebSocket error: {str(e)}")
                self.connection_manager.disconnect(websocket)
        
        @self.app.get("/")
        async def root() -> Dict[str, str]:
            """Root endpoint."""
            return {"message": "Welcome to OMEGA BTC AI Trap Visualizer API"}
        
        @self.app.get("/api/metrics", response_model=MetricsResponse)
        async def get_metrics(request: Request) -> MetricsResponse:
            """Get trap metrics with advanced analytics."""
            client_host = "unknown"
            if hasattr(request, 'client') and request.client is not None:
                client_host = request.client.host
            logger.info(f"📈 Metrics requested from {client_host}")
            data = self.load_latest_dump()
            metrics = self.calculate_metrics(data)
            logger.info(f"🎯 Total traps analyzed: {metrics.total_traps}")
            logger.info(f"📊 Success rate: {metrics.success_rate*100:.1f}%")
            return metrics
        
        @self.app.get("/api/traps", response_model=List[TrapData])
        async def get_traps(
            request: Request,
            start_time: Optional[datetime] = Query(None, description="Start time in ISO format (e.g. 2024-03-20T12:00:00Z)"),
            end_time: Optional[datetime] = Query(None, description="End time in ISO format (e.g. 2024-03-20T12:00:00Z)"),
            trap_type: Optional[str] = Query(None)
        ) -> List[TrapData]:
            """Get trap detections with optional filters."""
            try:
                # Sanitize trap_type input
                if trap_type:
                    trap_type = self.sanitize_input(trap_type)
                
                # Get data from Redis
                data = self.load_latest_dump()
                traps = data.get('traps', [])
                
                # Apply filters
                filtered_traps = []
                for trap in traps:
                    try:
                        # Sanitize string fields
                        trap["type"] = self.sanitize_input(trap.get("type", "UNKNOWN"))
                        trap["description"] = self.sanitize_input(trap.get("description", ""))
                        
                        # Ensure timestamp is timezone-aware
                        timestamp = trap.get("timestamp")
                        if isinstance(timestamp, str):
                            try:
                                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            except ValueError:
                                continue
                        
                        if timestamp.tzinfo is None:
                            timestamp = timestamp.replace(tzinfo=UTC)
                        trap["timestamp"] = timestamp
                        
                        # Apply time filters
                        if start_time and timestamp < start_time:
                            continue
                        if end_time and timestamp > end_time:
                            continue
                        if trap_type and trap.get("type") != trap_type:
                            continue
                        
                        filtered_traps.append(TrapData(**trap))
                    except (ValueError, TypeError, ValidationError) as e:
                        continue
                
                return filtered_traps
                
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Error in get_traps: {str(e)}")
                return []
        
        @self.app.get("/api/prices", response_model=List[PriceData])
        async def get_prices(request: Request) -> List[PriceData]:
            """Get price data with integrity verification."""
            logger.info(f"💰 Price data requested from {request.client.host}")
            data = self.load_latest_dump()
            prices = data.get('prices', [])
            logger.info(f"📊 Returning {len(prices)} price points")
            return prices
        
        @self.app.get("/api/timeline", response_model=List[TimelineEvent])
        async def get_timeline(
            hours: int = Query(24, ge=1, le=168)
        ) -> List[TimelineEvent]:
            """Get timeline of trap detections."""
            try:
                data = self.load_latest_dump()
                traps = data.get('traps', [])
                
                cutoff_time = datetime.now(UTC) - timedelta(hours=hours)
                timeline_events = []
                
                for trap in traps:
                    try:
                        # Sanitize string fields
                        trap["type"] = self.sanitize_input(trap.get("type", "UNKNOWN"))
                        trap["description"] = self.sanitize_input(trap.get("description", "No description available"))
                        
                        # Ensure timestamp is timezone-aware
                        timestamp = trap.get("timestamp")
                        if isinstance(timestamp, str):
                            try:
                                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            except ValueError:
                                continue
                        
                        if timestamp.tzinfo is None:
                            timestamp = timestamp.replace(tzinfo=UTC)
                        
                        if timestamp < cutoff_time:
                            continue
                        
                        confidence = trap.get("confidence", 0)
                        impact = "HIGH" if confidence >= 0.8 else "MEDIUM" if confidence >= 0.6 else "LOW"
                        
                        timeline_events.append(TimelineEvent(
                            id=f"event_{len(timeline_events)}",
                            type=trap.get("type", "UNKNOWN"),
                            timestamp=timestamp,
                            description=f"{trap.get('type', 'Unknown trap')} detected with {confidence*100:.1f}% confidence",
                            confidence=confidence,
                            impact=impact
                        ))
                    except (ValueError, TypeError, ValidationError) as e:
                        continue
                
                return sorted(timeline_events, key=lambda x: x.timestamp, reverse=True)
                
            except Exception as e:
                logger.error(f"Error processing timeline: {str(e)}")
                return []

if __name__ == "__main__":
    redis_manager = RedisManager()
    server = TrapVisualizerServer("OMEGA BTC AI Trap Visualizer", redis_manager)
    server.run(host="0.0.0.0", port=8000) 