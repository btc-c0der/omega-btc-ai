"""
MM Trap Visualizer Backend
=========================

FastAPI server that provides endpoints for the MM Trap Visualizer frontend.
Reads data from Redis dumps and serves it in a format suitable for visualization.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Union
import json
import os
from datetime import datetime, timedelta

app = FastAPI(title="MM Trap Visualizer API")

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class TrapData(BaseModel):
    id: str
    type: str
    timestamp: str
    confidence: float
    price: float
    volume: float
    metadata: Dict

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
    """Load the most recent Redis dump file."""
    dumps_dir = "redis-dumps"
    if not os.path.exists(dumps_dir):
        raise HTTPException(status_code=404, detail="No dumps directory found")
    
    dump_files = [f for f in os.listdir(dumps_dir) if f.endswith('.json')]
    if not dump_files:
        raise HTTPException(status_code=404, detail="No dump files found")
    
    latest_dump = max(dump_files, key=lambda x: os.path.getmtime(os.path.join(dumps_dir, x)))
    with open(os.path.join(dumps_dir, latest_dump), 'r') as f:
        return json.load(f)

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
    return {"message": "MM Trap Visualizer API"}

@app.get("/api/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get trap detection metrics."""
    data = load_latest_dump()
    return data.get('metrics', {
        'totalTraps': 0,
        'trapsByType': {},
        'averageConfidence': 0.0,
        'timeDistribution': {},
        'successRate': 0.0
    })

@app.get("/api/traps", response_model=List[TrapData])
async def get_traps(
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    trap_type: Optional[str] = None
):
    """Get trap detections with optional filtering."""
    data = load_latest_dump()
    traps = data.get('traps', [])
    
    # Apply filters
    if start_time:
        startDt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        traps = [t for t in traps if datetime.fromisoformat(t['timestamp'].replace('Z', '+00:00')) >= startDt]
    
    if end_time:
        endDt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        traps = [t for t in traps if datetime.fromisoformat(t['timestamp'].replace('Z', '+00:00')) <= endDt]
    
    if trap_type:
        traps = [t for t in traps if t.get('type') == trap_type]
    
    return traps

@app.get("/api/prices", response_model=List[PriceData])
async def get_prices():
    """Get price data."""
    data = load_latest_dump()
    return data.get('prices', [])

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
    uvicorn.run(app, host="0.0.0.0", port=8000) 