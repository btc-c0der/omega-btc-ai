"""Test configuration and fixtures for the MM Trap Visualizer backend."""

import pytest
from fastapi.testclient import TestClient
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List

from ..server import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture
def mock_dump_data():
    """Create mock trap detection data for testing."""
    now = datetime.utcnow()
    return {
        "trap_detections": [
            {
                "type": "FAKE_PUMP",
                "timestamp": (now - timedelta(hours=1)).isoformat(),
                "confidence": 0.85,
                "price": 35000.0,
                "volume": 100.0
            },
            {
                "type": "FAKE_DUMP",
                "timestamp": (now - timedelta(hours=2)).isoformat(),
                "confidence": 0.92,
                "price": 34500.0,
                "volume": 150.0
            },
            {
                "type": "LIQUIDITY_GRAB",
                "timestamp": (now - timedelta(hours=3)).isoformat(),
                "confidence": 0.78,
                "price": 34800.0,
                "volume": 120.0
            }
        ],
        "raw_data": {
            "prices": [34500.0, 34800.0, 35000.0],
            "volumes": [150.0, 120.0, 100.0],
            "timestamps": [
                (now - timedelta(hours=2)).isoformat(),
                (now - timedelta(hours=3)).isoformat(),
                (now - timedelta(hours=1)).isoformat()
            ]
        }
    }

@pytest.fixture
def mock_redis_dumps(tmp_path, mock_dump_data):
    """Create a temporary directory with mock Redis dump files."""
    dumps_dir = tmp_path / "redis-dumps"
    dumps_dir.mkdir()
    
    # Create a mock dump file
    dump_file = dumps_dir / "mm_trap_data_test.json"
    dump_file.write_text(json.dumps(mock_dump_data))
    
    return str(dumps_dir)

@pytest.fixture
def mock_environment(monkeypatch, mock_redis_dumps):
    """Set up the test environment with mock data."""
    monkeypatch.setenv("REDIS_DUMPS_DIR", mock_redis_dumps)
    return mock_redis_dumps 