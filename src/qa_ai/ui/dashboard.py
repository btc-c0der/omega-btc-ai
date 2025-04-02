from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
from typing import Dict, List
import json

app = FastAPI(title="QA AI Metrics Dashboard")

# Mount static files
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Mock data for demonstration
MOCK_METRICS = {
    "test_coverage": {
        "unit": 85,
        "integration": 75,
        "e2e": 65,
        "overall": 75
    },
    "test_results": {
        "total": 1000,
        "passed": 850,
        "failed": 100,
        "skipped": 50
    },
    "performance_metrics": {
        "response_time": {
            "avg": 250,
            "p95": 450,
            "p99": 600
        },
        "throughput": {
            "requests_per_second": 1000,
            "concurrent_users": 500
        }
    },
    "business_impact": {
        "critical_issues": 5,
        "high_priority": 15,
        "medium_priority": 30,
        "low_priority": 50
    }
}

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the main dashboard"""
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "metrics": MOCK_METRICS,
            "title": "QA AI Metrics Dashboard"
        }
    )

@app.get("/api/metrics")
async def get_metrics():
    """API endpoint for metrics data"""
    return MOCK_METRICS

@app.get("/api/personas")
async def get_personas():
    """API endpoint for QA personas"""
    return {
        "personas": [
            {
                "name": "The Architect",
                "expertise": ["System Architecture", "Integration Testing"],
                "active_tests": 150
            },
            {
                "name": "The Explorer",
                "expertise": ["Exploratory Testing", "Edge Cases"],
                "active_tests": 200
            },
            {
                "name": "The Guardian",
                "expertise": ["Security Testing", "Compliance"],
                "active_tests": 100
            }
        ]
    }

def run_server(host: str = "0.0.0.0", port: int = 3000):
    """Run the dashboard server"""
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run_server() 