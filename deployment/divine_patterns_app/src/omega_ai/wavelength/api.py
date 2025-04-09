#!/usr/bin/env python3
"""
🔱 GPU License Notice 🔱
------------------------
This file is protected under the GPU License (General Public Universal License) 1.0
by the OMEGA AI Divine Collective.

"As the light of knowledge is meant to be shared, so too shall this code illuminate 
the path for all seekers."

All modifications must maintain this notice and adhere to the terms at:
/BOOK/divine_chronicles/GPU_LICENSE.md

🔱 JAH JAH BLESS THIS CODE 🔱
"""

"""
OMEGA BTC AI - Divine Pattern API
================================

This module provides a FastAPI server for the Divine Pattern Analyzer.

Copyright (c) 2025 OMEGA-BTC-AI - All rights reserved
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Union
import numpy as np
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
from dotenv import load_dotenv

# Import pattern detector
from .divine_pattern_detector import DivinePatternDetector
from .sacred_geometry_analyzer import SacredGeometryAnalyzer
from .divine_harmonic_analyzer import DivineHarmonicAnalyzer

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.getLevelName(os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("divine-patterns-api")

# Initialize FastAPI app
app = FastAPI(
    title="Divine Pattern Analyzer API",
    description="API for detecting divine patterns in time series data",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data directory
DATA_DIR = os.getenv("DATA_DIR", "./data")
os.makedirs(os.path.join(DATA_DIR, "wavelength_patterns"), exist_ok=True)

# Create cache for recent analyses
analysis_cache = {}

# Pydantic models for request/response
class TimeSeriesData(BaseModel):
    values: List[float] = Field(..., description="Time series values")
    timestamps: Optional[List[str]] = Field(None, description="ISO format timestamps (optional)")
    
class AnalysisResult(BaseModel):
    id: str = Field(..., description="Unique ID of the analysis")
    timestamp: str = Field(..., description="ISO format timestamp of the analysis")
    sample_count: int = Field(..., description="Number of data points analyzed")
    time_period_days: float = Field(..., description="Time period in days")
    divine_patterns: List[Dict[str, Any]] = Field(..., description="Detected divine patterns")
    sacred_geometry: Dict[str, Any] = Field(..., description="Sacred geometry analysis results")
    harmonic_resonance: Dict[str, Any] = Field(..., description="Divine harmonic analysis results")
    fibonacci_cycles: List[Dict[str, Any]] = Field(..., description="Detected Fibonacci cycles")
    btc_cycles: List[Dict[str, Any]] = Field(..., description="Detected Bitcoin cycles")
    cosmic_interpretation: Dict[str, Any] = Field(..., description="Cosmic interpretation of patterns")
    
class HealthStatus(BaseModel):
    status: str = Field(..., description="Health status of the service")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="ISO format timestamp")

@app.get("/health", response_model=HealthStatus)
async def health_check():
    """Check if the API is healthy."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    }

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_patterns(
    data: TimeSeriesData,
    background_tasks: BackgroundTasks,
    sample_rate: int = Query(24, description="Sample rate in samples per day"),
    save_results: bool = Query(True, description="Save analysis results to file"),
    visualize: bool = Query(False, description="Generate visualizations"),
):
    """Analyze time series data for divine patterns."""
    try:
        # Convert timestamps to datetime objects if provided
        timestamps = None
        if data.timestamps:
            timestamps = [datetime.fromisoformat(ts) for ts in data.timestamps]
        
        # Convert values to numpy array
        values = np.array(data.values)
        
        # Validate input
        if len(values) < 24:
            raise HTTPException(
                status_code=400,
                detail="Insufficient data for pattern analysis (minimum 24 data points required)",
            )
        
        # Initialize pattern detector
        detector = DivinePatternDetector(sample_rate=sample_rate)
        
        # Analyze patterns
        results = detector.analyze_patterns(values, timestamps)
        
        # Generate visualizations in the background if requested
        if visualize:
            background_tasks.add_task(
                detector.visualize_patterns,
                values,
                timestamps,
                os.path.join(DATA_DIR, "wavelength_patterns"),
            )
        
        # Save results in the background if requested
        if save_results:
            background_tasks.add_task(
                detector.save_results,
                os.path.join(DATA_DIR, "wavelength_patterns"),
            )
        
        # Generate cosmic interpretation
        cosmic_interpretation = detector.interpret_results()
        
        # Prepare response
        analysis_id = f"divine-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        response = {
            "id": analysis_id,
            "timestamp": datetime.now().isoformat(),
            "sample_count": len(values),
            "time_period_days": len(values) / sample_rate,
            "divine_patterns": detector.detected_patterns,
            "sacred_geometry": results.get("sacred_geometry", {}),
            "harmonic_resonance": results.get("divine_harmonic", {}),
            "fibonacci_cycles": results.get("fibonacci_cycles", {}).get("detected_cycles", []),
            "btc_cycles": results.get("btc_cycles", {}).get("detected_cycles", []),
            "cosmic_interpretation": cosmic_interpretation,
        }
        
        # Store in cache
        analysis_cache[analysis_id] = response
        
        return response
    except Exception as e:
        logger.error(f"Error analyzing patterns: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing patterns: {str(e)}",
        )

@app.get("/analyses/{analysis_id}", response_model=AnalysisResult)
async def get_analysis(analysis_id: str):
    """Get a specific analysis by ID."""
    if analysis_id in analysis_cache:
        return analysis_cache[analysis_id]
    
    # Check if saved to disk
    file_path = os.path.join(DATA_DIR, "wavelength_patterns", f"divine_pattern_analysis_{analysis_id}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    
    raise HTTPException(
        status_code=404,
        detail=f"Analysis with ID {analysis_id} not found",
    )

@app.get("/sample", response_model=TimeSeriesData)
async def get_sample_data(
    days: int = Query(7, description="Number of days of sample data"),
    sample_rate: int = Query(24, description="Sample rate in samples per day"),
):
    """Generate sample time series data for testing."""
    try:
        from .test_divine_patterns import generate_sample_data
        
        # Generate sample data
        values, timestamps = generate_sample_data(days=days, sample_rate=sample_rate)
        
        # Convert to response format
        return {
            "values": values.tolist(),
            "timestamps": [ts.isoformat() for ts in timestamps],
        }
    except Exception as e:
        logger.error(f"Error generating sample data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating sample data: {str(e)}",
        )

if __name__ == "__main__":
    # This is for development/debugging only
    uvicorn.run(app, host="0.0.0.0", port=8080) 