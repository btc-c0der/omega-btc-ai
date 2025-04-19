
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

import pytest
import json
from jsonschema import validate, ValidationError
from datetime import datetime, timezone
import aiohttp
import asyncio
from typing import Dict, Any
from unittest.mock import patch
from fastapi.testclient import TestClient

# JSON Schemas for Backend API
BACKEND_SCHEMAS = {
    "health_response": {
        "type": "object",
        "required": ["status", "redis", "timestamp"],
        "properties": {
            "status": {"type": "string", "enum": ["healthy"]},
            "redis": {"type": "string", "enum": ["connected", "disconnected"]},
            "timestamp": {"type": "string", "format": "date-time"}
        }
    },
    "trap_probability_response": {
        "type": "object",
        "required": ["probability", "trap_type", "confidence", "components", "trend"],
        "properties": {
            "probability": {"type": "number", "minimum": 0, "maximum": 1},
            "trap_type": {"type": ["string", "null"]},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "components": {
                "type": "object",
                "required": ["volume_spike", "price_pattern", "market_sentiment", 
                           "fibonacci_match", "liquidity_concentration", "order_imbalance"],
                "properties": {
                    "volume_spike": {
                        "type": "object",
                        "required": ["value", "description"],
                        "properties": {
                            "value": {"type": "number", "minimum": 0, "maximum": 1},
                            "description": {"type": "string"}
                        }
                    },
                    "price_pattern": {
                        "type": "object",
                        "required": ["value", "description"],
                        "properties": {
                            "value": {"type": "number", "minimum": 0, "maximum": 1},
                            "description": {"type": "string"}
                        }
                    },
                    "market_sentiment": {
                        "type": "object",
                        "required": ["value", "description"],
                        "properties": {
                            "value": {"type": "number", "minimum": 0, "maximum": 1},
                            "description": {"type": "string"}
                        }
                    },
                    "fibonacci_match": {
                        "type": "object",
                        "required": ["value", "description"],
                        "properties": {
                            "value": {"type": "number", "minimum": 0, "maximum": 1},
                            "description": {"type": "string"}
                        }
                    },
                    "liquidity_concentration": {
                        "type": "object",
                        "required": ["value", "description"],
                        "properties": {
                            "value": {"type": "number", "minimum": 0, "maximum": 1},
                            "description": {"type": "string"}
                        }
                    },
                    "order_imbalance": {
                        "type": "object",
                        "required": ["value", "description"],
                        "properties": {
                            "value": {"type": "number", "minimum": 0, "maximum": 1},
                            "description": {"type": "string"}
                        }
                    }
                }
            },
            "trend": {"type": "string", "enum": ["bullish", "bearish", "stable"]}
        }
    },
    "position_response": {
        "type": "object",
        "required": ["has_position"],
        "properties": {
            "has_position": {"type": "boolean"}
        }
    },
    "redis_keys_response": {
        "type": "object",
        "required": ["keys", "total_keys", "displayed_keys"],
        "properties": {
            "keys": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["key", "type"],
                    "properties": {
                        "key": {"type": "string"},
                        "type": {"type": "string"},
                        "length": {"type": "integer"},
                        "fields": {"type": "integer"}
                    }
                }
            },
            "total_keys": {"type": "integer"},
            "displayed_keys": {"type": "integer"}
        }
    }
}

# JSON Schemas for Frontend API
FRONTEND_SCHEMAS = {
    "trap_data": {
        "type": "object",
        "required": ["type", "description", "timestamp", "probability", "severity"],
        "properties": {
            "type": {"type": "string"},
            "description": {"type": "string"},
            "timestamp": {"type": "string", "format": "date-time"},
            "probability": {"type": "number", "minimum": 0, "maximum": 1},
            "severity": {"type": "string", "enum": ["low", "medium", "high"]}
        }
    },
    "price_data": {
        "type": "object",
        "required": ["timestamp", "price", "volume", "indicators"],
        "properties": {
            "timestamp": {"type": "string", "format": "date-time"},
            "price": {"type": "number"},
            "volume": {"type": "number"},
            "indicators": {
                "type": "object",
                "required": ["rsi", "macd"],
                "properties": {
                    "rsi": {"type": "number"},
                    "macd": {"type": "number"}
                }
            }
        }
    },
    "timeline_event": {
        "type": "object",
        "required": ["timestamp", "event_type", "description", "severity"],
        "properties": {
            "timestamp": {"type": "string", "format": "date-time"},
            "event_type": {"type": "string"},
            "description": {"type": "string"},
            "severity": {"type": "string", "enum": ["low", "medium", "high"]}
        }
    },
    "metrics_response": {
        "type": "object",
        "required": ["total_traps", "success_rate", "average_probability", "timestamp"],
        "properties": {
            "total_traps": {"type": "integer"},
            "success_rate": {"type": "number", "minimum": 0, "maximum": 1},
            "average_probability": {"type": "number", "minimum": 0, "maximum": 1},
            "timestamp": {"type": "string", "format": "date-time"}
        }
    }
}

# Test data
TEST_DATA = {
    "trap_probability": {
        "probability": 0.75,
        "trap_type": None,
        "confidence": 0.0,
        "components": {
            "volume_spike": {
                "value": 0.5,
                "description": "Abnormal trading volume detected"
            },
            "price_pattern": {
                "value": 0.6,
                "description": "Price pattern analysis"
            },
            "market_sentiment": {
                "value": 0.7,
                "description": "Crowd sentiment indicator"
            },
            "fibonacci_match": {
                "value": 0.8,
                "description": "Fibonacci retracement correlation"
            },
            "liquidity_concentration": {
                "value": 0.9,
                "description": "Order book liquidity analysis"
            },
            "order_imbalance": {
                "value": 0.4,
                "description": "Bid/ask imbalance detection"
            }
        },
        "trend": "stable"
    },
    "position": {
        "has_position": True
    },
    "trap_data": {
        "type": "bull_trap",
        "description": "Detected potential bull trap pattern",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "probability": 0.75,
        "severity": "high"
    },
    "price_data": {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "price": 65432.10,
        "volume": 123.45,
        "indicators": {
            "rsi": 65.5,
            "macd": 123.45
        }
    }
}

@pytest.mark.asyncio
async def test_backend_health_endpoint():
    """Test the backend health endpoint."""
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8000/api/health") as response:
            assert response.status == 200
            data = await response.json()
            validate(instance=data, schema=BACKEND_SCHEMAS["health_response"])
            assert data["status"] == "healthy"
            assert data["redis"] in ["connected", "disconnected"]
            assert datetime.fromisoformat(data["timestamp"])

@pytest.mark.asyncio
async def test_backend_trap_probability_endpoint():
    """Test the backend trap probability endpoint."""
    # Create test data
    test_data = {
        "probability": 0.75,
        "trap_type": "bull_trap",
        "confidence": 0.85,
        "trend": "bullish",
        "components": {
            "price_pattern": {"value": 0.7, "description": "Recent price pattern analysis"},
            "market_sentiment": {"value": 0.5, "description": "Current market sentiment"},
            "fibonacci_match": {"value": 0.6, "description": "Fibonacci level alignment"},
            "liquidity_concentration": {"value": 0.8, "description": "Normalized trading volume"},
            "order_imbalance": {"value": 0.5, "description": "Buy/Sell order ratio"}
        }
    }

    # Mock Redis manager
    with patch('redis.Redis') as mock_redis:
        mock_instance = mock_redis.return_value
        mock_instance.get.return_value = json.dumps(test_data)

        # Create server with mock Redis
        server = MMTrapVisualizerServer()
        server.redis_manager.redis = mock_instance

        # Create test client
        client = TestClient(server.app)

        # Test the endpoint
        response = client.get("/api/trap-probability")
        assert response.status_code == 200
        data = response.json()

        # Validate response against schema
        validate(instance=data, schema=BACKEND_SCHEMAS["trap_probability_response"])
        assert 0 <= data["probability"] <= 1
        assert data["trap_type"] is None or isinstance(data["trap_type"], str)
        assert 0 <= data["confidence"] <= 1
        assert isinstance(data["components"], dict)
        assert data["trend"] in ["bullish", "bearish", "stable"]

        # Validate component values
        for component in data["components"].values():
            assert 0 <= component["value"] <= 1
            assert isinstance(component["description"], str)

@pytest.mark.asyncio
async def test_backend_position_endpoint():
    """Test the backend position endpoint."""
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8000/api/position") as response:
            assert response.status == 200
            data = await response.json()
            validate(instance=data, schema=BACKEND_SCHEMAS["position_response"])
            assert isinstance(data["has_position"], bool)

@pytest.mark.asyncio
async def test_backend_redis_keys_endpoint():
    """Test the backend Redis keys endpoint."""
    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8000/api/redis-keys") as response:
            assert response.status == 200
            data = await response.json()
            validate(instance=data, schema=BACKEND_SCHEMAS["redis_keys_response"])
            assert isinstance(data["keys"], list)
            assert isinstance(data["total_keys"], int)
            assert isinstance(data["displayed_keys"], int)
            if data["keys"]:
                key = data["keys"][0]
                assert "key" in key
                assert "type" in key

@pytest.mark.asyncio
async def test_backend_websocket():
    """Test WebSocket connection for backend."""
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect("ws://localhost:8000/ws") as ws:
            await ws.send_str("ping")
            response = await ws.receive_str()
            assert response == "pong"

def test_schema_validation():
    """Test JSON schema validation with test data."""
    validate(instance=TEST_DATA["trap_probability"], 
             schema=BACKEND_SCHEMAS["trap_probability_response"])
    validate(instance=TEST_DATA["position"], 
             schema=BACKEND_SCHEMAS["position_response"])

def test_invalid_data():
    """Test schema validation with invalid data."""
    # Test invalid trap probability
    invalid_trap_prob = TEST_DATA["trap_probability"].copy()
    invalid_trap_prob["probability"] = 1.5  # Invalid probability
    with pytest.raises(ValidationError):
        validate(instance=invalid_trap_prob, 
                schema=BACKEND_SCHEMAS["trap_probability_response"])

    # Test missing required field
    invalid_position = TEST_DATA["position"].copy()
    del invalid_position["has_position"]  # Remove required field
    with pytest.raises(ValidationError):
        validate(instance=invalid_position, 
                schema=BACKEND_SCHEMAS["position_response"]) 