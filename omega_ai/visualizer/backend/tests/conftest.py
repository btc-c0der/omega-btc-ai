"""Test configuration and fixtures for the MM Trap Visualizer backend."""

import pytest
from fastapi.testclient import TestClient
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, AsyncGenerator
from pathlib import Path
from httpx import AsyncClient
from fastapi import FastAPI
import tempfile

from mm_trap_visualizer.server import app

@pytest.fixture
def client() -> TestClient:
    """Create a test client."""
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

@pytest.fixture
def test_data_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for test data."""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    return data_dir

@pytest.fixture
def mock_trap_data() -> List[Dict[str, Any]]:
    """Generate mock trap detection data."""
    return [
        {
            "id": "1",
            "type": "bullish",
            "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
            "confidence": 0.85,
            "price": 100
        },
        {
            "id": "2",
            "type": "bearish",
            "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
            "confidence": 0.92,
            "price": 110
        },
        {
            "id": "3",
            "type": "bullish",
            "timestamp": (datetime.now() - timedelta(hours=3)).isoformat(),
            "confidence": 0.78,
            "price": 105
        }
    ]

@pytest.fixture
def mock_redis_dump(test_data_dir: Path, mock_trap_data: List[Dict[str, Any]]) -> Path:
    """Create a mock Redis dump file with test data."""
    dump_file = test_data_dir / "test_dump.json"
    with open(dump_file, "w") as f:
        json.dump({"trap_detections": mock_trap_data}, f)
    return dump_file

@pytest.fixture
def expected_metrics(mock_trap_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate expected metrics from mock data."""
    total_traps = len(mock_trap_data)
    traps_by_type = {}
    total_confidence = 0

    for trap in mock_trap_data:
        trap_type = trap["type"]
        traps_by_type[trap_type] = traps_by_type.get(trap_type, 0) + 1
        total_confidence += trap["confidence"]

    return {
        "total_traps": total_traps,
        "traps_by_type": traps_by_type,
        "average_confidence": total_confidence / total_traps if total_traps > 0 else 0,
        "success_rate": 0.85  # Mock success rate for testing
    }

@pytest.fixture
async def async_client() -> AsyncClient:
    """Create an async test client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def mock_redis_dump() -> Path:
    """Create a mock Redis dump file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        dump_path = Path(temp_dir) / "test_dump.json"
        now = datetime.utcnow()
        data = {
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
            ]
        }
        dump_path.write_text(json.dumps(data))
        yield dump_path

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers",
        "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers",
        "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers",
        "asyncio: mark test as an async test"
    ) 