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
from unittest.mock import Mock
from omega_ai.utils.redis_manager import RedisManager
from omega_ai.visualizer.backend.src.mm_trap_visualizer.server import MMTrapVisualizerServer

@pytest.fixture
def redis_manager():
    """Create a mock Redis manager."""
    manager = Mock(spec=RedisManager)
    manager.get_cached.return_value = {
        "traps": [
            {
                "id": "1",
                "type": "FAKE_PUMP",
                "timestamp": datetime.now() - timedelta(hours=1),
                "confidence": 0.85,
                "price": 35000.0,
                "volume": 100.0,
                "description": "Fake pump detected",
                "success": True
            },
            {
                "id": "2",
                "type": "FAKE_DUMP",
                "timestamp": datetime.now() - timedelta(hours=2),
                "confidence": 0.92,
                "price": 34500.0,
                "volume": 150.0,
                "description": "Fake dump detected",
                "success": False
            }
        ]
    }
    return manager

@pytest.fixture
def server(redis_manager):
    """Create a test server instance."""
    return MMTrapVisualizerServer("Test MM Trap Visualizer", redis_manager)

@pytest.fixture
def client(server):
    """Create a test client."""
    return TestClient(server.app)

@pytest.fixture
async def async_client(server):
    """Create an async test client."""
    async with AsyncClient(base_url="http://test", transport=server.app) as client:
        yield client

@pytest.fixture
def mock_trap_data():
    """Create mock trap data."""
    return {
        'traps': [
            {
                'id': '1',
                'type': 'accumulation',
                'timestamp': datetime.now() - timedelta(hours=2),
                'confidence': 0.85,
                'price': 45000.0,
                'volume': 1.5,
                'description': 'Large accumulation detected',
                'success': True
            },
            {
                'id': '2',
                'type': 'distribution',
                'timestamp': datetime.now() - timedelta(hours=1),
                'confidence': 0.92,
                'price': 46000.0,
                'volume': 2.0,
                'description': 'Distribution pattern observed',
                'success': False
            }
        ]
    }

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