"""
FastAPI server for the Market Maker Trap Visualizer.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="MM Trap Visualizer API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TrapData(BaseModel):
    """Model for trap detection data."""
    id: str
    type: str
    timestamp: datetime
    confidence: float
    price: float
    volume: float
    description: str = Field(default="")
    success: Optional[bool] = None

class MetricsResponse(BaseModel):
    """Model for metrics response."""
    total_traps: int
    traps_by_type: Dict[str, int]
    average_confidence: float
    time_distribution: Dict[str, int]
    success_rate: float

class TimelineEvent(BaseModel):
    """Model for timeline events."""
    type: str
    timestamp: datetime
    description: str
    confidence: float
    impact: str

def load_latest_dump() -> List[TrapData]:
    """Load and parse the latest Redis dump."""
    try:
        # TODO: Implement actual Redis dump loading
        # For now, return mock data
        return [
            TrapData(
                id="1",
                type="accumulation",
                timestamp=datetime.now() - timedelta(hours=2),
                confidence=0.85,
                price=45000.0,
                volume=1.5,
                description="Large accumulation detected",
                success=True
            ),
            TrapData(
                id="2",
                type="distribution",
                timestamp=datetime.now() - timedelta(hours=1),
                confidence=0.92,
                price=46000.0,
                volume=2.0,
                description="Distribution pattern observed",
                success=False
            )
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to MM Trap Visualizer API"}

@app.get("/api/metrics", response_model=MetricsResponse)
async def get_metrics() -> MetricsResponse:
    """Get trap detection metrics."""
    try:
        traps = load_latest_dump()
        
        total = len(traps)
        by_type: Dict[str, int] = {}
        confidence_sum = 0.0
        success_count = 0
        time_dist: Dict[str, int] = {}
        
        for trap in traps:
            by_type[trap.type] = by_type.get(trap.type, 0) + 1
            confidence_sum += trap.confidence
            if trap.success:
                success_count += 1
            hour = trap.timestamp.strftime("%H:00")
            time_dist[hour] = time_dist.get(hour, 0) + 1
        
        return MetricsResponse(
            total_traps=total,
            traps_by_type=by_type,
            average_confidence=confidence_sum / total if total > 0 else 0.0,
            time_distribution=time_dist,
            success_rate=success_count / total if total > 0 else 0.0
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/traps", response_model=List[TrapData])
async def get_traps(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    trap_type: Optional[str] = None
) -> List[TrapData]:
    """Get trap detections with optional filters."""
    try:
        traps = load_latest_dump()
        
        if start_time:
            traps = [t for t in traps if t.timestamp >= start_time]
        if end_time:
            traps = [t for t in traps if t.timestamp <= end_time]
        if trap_type:
            traps = [t for t in traps if t.type == trap_type]
        
        return traps
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/timeline", response_model=List[TimelineEvent])
async def get_timeline(
    last_hours: int = Query(default=24, ge=1, le=168)
) -> List[TimelineEvent]:
    """Get timeline of trap detections."""
    try:
        traps = load_latest_dump()
        start_time = datetime.now() - timedelta(hours=last_hours)
        
        events = []
        for trap in traps:
            if trap.timestamp >= start_time:
                impact = "high" if trap.confidence > 0.8 else "medium" if trap.confidence > 0.6 else "low"
                events.append(TimelineEvent(
                    type=trap.type,
                    timestamp=trap.timestamp,
                    description=trap.description,
                    confidence=trap.confidence,
                    impact=impact
                ))
        
        return sorted(events, key=lambda x: x.timestamp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 