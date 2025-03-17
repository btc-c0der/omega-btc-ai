"""
0M3G4 BTC TR4P V1SU4L1Z3R B4CK3ND
================================
H4x0r-grade FastAPI server for monitoring BTC market manipulation traps.
Implements advanced logging and security features for tracking suspicious activities.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Union
import json
import os
import logging
import time
from datetime import datetime, timedelta
import hashlib
import uuid
from functools import wraps

# Initialize 1337 logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s 🎯 %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("0m3g4_tr4pp3r")

# Initialize the h4x0r API
app = FastAPI(title="0M3G4 TR4P V1SU4L1Z3R API")

# Security middleware for request tracking
@app.middleware("http")
async def track_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    ip = request.client.host
    path = request.url.path
    
    # Calculate request signature
    content = await request.body()
    request_hash = hashlib.sha256(content).hexdigest()
    
    logger.info(f"[{request_id}] 🔥 Incoming request from {ip}")
    logger.info(f"[{request_id}] 🎯 Target: {path}")
    logger.info(f"[{request_id}] 🔒 Request signature: {request_hash[:8]}")
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(f"[{request_id}] ⚡ Response time: {process_time:.3f}s")
    return response

# Enable CORS with security headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models with advanced validation
class TrapData(BaseModel):
    id: str
    type: str
    timestamp: str
    confidence: float
    price: float
    volume: float
    metadata: Dict

    class Config:
        schema_extra = {
            "example": {
                "id": "tr4p_1337",
                "type": "bullish",
                "timestamp": "2024-03-16T10:00:00Z",
                "confidence": 0.85,
                "price": 68500,
                "volume": 1200,
                "metadata": {
                    "pattern": "double_bottom",
                    "timeframe": "1h"
                }
            }
        }

class PriceData(BaseModel):
    time: str
    open: float
    close: float
    high: float
    low: float

class MetricsResponse(BaseModel):
    totalTraps: int
    trapsByType: Dict[str, int]
    averageConfidence: float
    timeDistribution: Dict[str, int]
    successRate: float

class TimelineEvent(BaseModel):
    id: str
    type: str
    timestamp: str
    description: str
    confidence: float
    impact: str

def load_latest_dump() -> Dict:
    """Load the most recent dump with integrity verification."""
    dumps_dir = "redis-dumps"
    if not os.path.exists(dumps_dir):
        logger.error("❌ No dumps directory found!")
        raise HTTPException(status_code=404, detail="No dumps directory found")
    
    dump_files = [f for f in os.listdir(dumps_dir) if f.endswith('.json')]
    if not dump_files:
        logger.error("❌ No dump files found!")
        raise HTTPException(status_code=404, detail="No dump files found")
    
    latest_dump = max(dump_files, key=lambda x: os.path.getmtime(os.path.join(dumps_dir, x)))
    logger.info(f"🎯 Loading dump: {latest_dump}")
    
    try:
        with open(os.path.join(dumps_dir, latest_dump), 'r') as f:
            data = json.load(f)
            # Calculate data integrity hash
            data_hash = hashlib.sha256(json.dumps(data).encode()).hexdigest()
            logger.info(f"✅ Data integrity hash: {data_hash[:8]}")
            return data
    except json.JSONDecodeError:
        logger.error("❌ Invalid JSON data detected!")
        raise HTTPException(status_code=500, detail="Corrupted dump file")

def calculate_metrics(data: Dict) -> MetricsResponse:
    """Calculate metrics from trap data."""
    traps = data.get('trap_detections', [])
    if not traps:
        return MetricsResponse(
            totalTraps=0,
            trapsByType={},
            averageConfidence=0.0,
            timeDistribution={},
            successRate=0.0
        )
    
    # Count traps by type
    trapsByType = {}
    totalConfidence = 0
    successCount = 0
    timeDist = {f"{i:02d}-{(i+4):02d}": 0 for i in range(0, 24, 4)}
    
    for trap in traps:
        # Count by type
        trapType = trap.get('type', 'UNKNOWN')
        trapsByType[trapType] = trapsByType.get(trapType, 0) + 1
        
        # Sum confidence
        confidence = trap.get('confidence', 0)
        totalConfidence += confidence
        
        # Check success
        if confidence > 0.7:  # Consider high confidence as success
            successCount += 1
        
        # Time distribution
        timestamp = datetime.fromisoformat(trap.get('timestamp', '').replace('Z', '+00:00'))
        hour = timestamp.hour
        timeSlot = f"{(hour//4)*4:02d}-{((hour//4)*4+4):02d}"
        timeDist[timeSlot] += 1
    
    return MetricsResponse(
        totalTraps=len(traps),
        trapsByType=trapsByType,
        averageConfidence=totalConfidence / len(traps),
        timeDistribution=timeDist,
        successRate=successCount / len(traps)
    )

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "0M3G4 TR4P V1SU4L1Z3R API"}

@app.get("/api/metrics", response_model=MetricsResponse)
async def get_metrics(request: Request):
    """Get trap metrics with advanced analytics."""
    logger.info(f"📈 Metrics requested from {request.client.host}")
    data = load_latest_dump()
    metrics = data.get('metrics', {
        'totalTraps': 0,
        'trapsByType': {},
        'averageConfidence': 0.0,
        'timeDistribution': {},
        'successRate': 0.0
    })
    logger.info(f"🎯 Total traps analyzed: {metrics['totalTraps']}")
    logger.info(f"📊 Success rate: {metrics['successRate']*100:.1f}%")
    return metrics

@app.get("/api/traps", response_model=List[TrapData])
async def get_traps(
    request: Request,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    trap_type: Optional[str] = None
):
    """Get trap detections with advanced filtering and logging."""
    logger.info(f"🔍 Scanning for traps from {request.client.host}")
    data = load_latest_dump()
    traps = data.get('traps', [])
    
    # Apply temporal filters
    if start_time:
        startDt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        traps = [t for t in traps if datetime.fromisoformat(t['timestamp'].replace('Z', '+00:00')) >= startDt]
        logger.info(f"⏰ Time filter applied: {len(traps)} traps after {start_time}")
    
    if end_time:
        endDt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        traps = [t for t in traps if datetime.fromisoformat(t['timestamp'].replace('Z', '+00:00')) <= endDt]
        logger.info(f"⏰ Time filter applied: {len(traps)} traps before {end_time}")
    
    if trap_type:
        traps = [t for t in traps if t.get('type') == trap_type]
        logger.info(f"🎯 Type filter applied: {len(traps)} {trap_type} traps found")
    
    logger.info(f"✅ Returning {len(traps)} traps")
    return traps

@app.get("/api/prices", response_model=List[PriceData])
async def get_prices(request: Request):
    """Get price data with integrity verification."""
    logger.info(f"💰 Price data requested from {request.client.host}")
    data = load_latest_dump()
    prices = data.get('prices', [])
    logger.info(f"📊 Returning {len(prices)} price points")
    return prices

@app.get("/api/timeline", response_model=List[TimelineEvent])
async def get_timeline(last_hours: Optional[int] = 24):
    """Get timeline of trap detections."""
    data = load_latest_dump()
    traps = data.get('trap_detections', [])
    
    if last_hours:
        cutoff = datetime.utcnow() - timedelta(hours=last_hours)
        traps = [t for t in traps if datetime.fromisoformat(t['timestamp'].replace('Z', '+00:00')) >= cutoff]
    
    timeline = []
    for i, trap in enumerate(traps):
        confidence = trap.get('confidence', 0)
        impact = 'HIGH' if confidence > 0.8 else 'MEDIUM' if confidence > 0.6 else 'LOW'
        
        event = TimelineEvent(
            id=f"event_{i}",
            type=trap.get('type', 'UNKNOWN'),
            timestamp=trap['timestamp'],
            description=f"{trap.get('type', 'Unknown trap')} detected with {confidence*100:.1f}% confidence",
            confidence=confidence,
            impact=impact
        )
        timeline.append(event)
    
    return sorted(timeline, key=lambda x: x.timestamp, reverse=True)

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Initializing 0M3G4 TR4P V1SU4L1Z3R")
    logger.info("💀 H4x0r mode: ENABLED")
    uvicorn.run(app, host="0.0.0.0", port=8000) 