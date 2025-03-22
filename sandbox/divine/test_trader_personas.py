#!/usr/bin/env python3
"""
OMEGA BTC AI - Divine Alignment Dashboard - Trader Personas Tests
=================================================================

Tests for the trader personas API endpoint in the Divine Alignment Dashboard.

Usage:
    python -m pytest test_trader_personas.py -v

Author: OMEGA BTC AI Team
Version: 1.0
"""

import os
import sys
import pytest
import requests
import json
import time
import subprocess
import threading
import signal
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test constants
API_URL = "http://localhost:5051"
PERSONAS_ENDPOINT = "/api/trader_personas"

class TestTraderPersonas:
    """Test suite for trader personas functionality."""
    
    @classmethod
    def setup_class(cls):
        """Set up the test class by starting the API server."""
        # Start the API server in a subprocess
        script_dir = os.path.dirname(os.path.abspath(__file__))
        api_script = os.path.join(script_dir, 'golden_ratio_api.py')
        
        env = os.environ.copy()
        env["FLASK_APP"] = api_script
        env["FLASK_ENV"] = "development"
        
        cls.api_process = subprocess.Popen(
            [sys.executable, api_script],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give the server time to start
        time.sleep(3)
    
    @classmethod
    def teardown_class(cls):
        """Tear down the test class by stopping the API server."""
        if cls.api_process and cls.api_process.poll() is None:
            cls.api_process.terminate()
            cls.api_process.wait(timeout=5)
    
    def test_trader_personas_endpoint_exists(self):
        """Test that the trader personas endpoint exists and returns valid JSON."""
        response = requests.get(f"{API_URL}{PERSONAS_ENDPOINT}")
        assert response.status_code == 200
        assert response.headers["Content-Type"].startswith("application/json")
    
    def test_trader_personas_data_structure(self):
        """Test that the trader personas endpoint returns the expected data structure."""
        response = requests.get(f"{API_URL}{PERSONAS_ENDPOINT}")
        data = response.json()
        
        # Check top-level keys
        expected_personas = ["strategic", "aggressive", "scalper", "divine"]
        for persona in expected_personas:
            assert persona in data, f"Persona '{persona}' not found in response"
        
        # Check fields for each persona
        for persona_key, persona_data in data.items():
            # Required fields
            assert "name" in persona_data
            assert "personality" in persona_data
            assert "style" in persona_data
            assert "risk_level" in persona_data
            assert "favorite_pattern" in persona_data
            assert "current_position" in persona_data
            
            # Performance metrics
            assert "performance" in persona_data
            assert "win_rate" in persona_data["performance"]
            assert "avg_profit" in persona_data["performance"]
            assert "max_drawdown" in persona_data["performance"]
            
            # Check data types
            assert isinstance(persona_data["name"], str)
            assert isinstance(persona_data["personality"], str)
            assert isinstance(persona_data["style"], str)
            assert isinstance(persona_data["risk_level"], str)
            assert isinstance(persona_data["favorite_pattern"], str)
            assert isinstance(persona_data["current_position"], str)
            assert isinstance(persona_data["performance"]["win_rate"], (int, float))
            assert isinstance(persona_data["performance"]["avg_profit"], (int, float))
            assert isinstance(persona_data["performance"]["max_drawdown"], (int, float))
    
    def test_divine_persona_exists(self):
        """Test that the new divine persona exists with the expected attributes."""
        response = requests.get(f"{API_URL}{PERSONAS_ENDPOINT}")
        data = response.json()
        
        assert "divine" in data
        divine = data["divine"]
        
        assert divine["name"] == "Divine Harmonizer"
        assert "intuitive" in divine["personality"].lower()
        assert "divine proportions" in divine["style"].lower()
        assert isinstance(divine["performance"]["win_rate"], (int, float))
        assert divine["performance"]["win_rate"] > 0
    
    def test_persona_performance_metrics_valid(self):
        """Test that the performance metrics for personas are valid."""
        response = requests.get(f"{API_URL}{PERSONAS_ENDPOINT}")
        data = response.json()
        
        for persona_key, persona_data in data.items():
            perf = persona_data["performance"]
            
            # Win rate should be between 0 and 100
            assert 0 <= perf["win_rate"] <= 100
            
            # Average profit should be reasonable (not extreme)
            assert -50 <= perf["avg_profit"] <= 100
            
            # Max drawdown should be positive (since it's a loss percentage)
            assert 0 <= perf["max_drawdown"] <= 100


if __name__ == '__main__':
    pytest.main(['-v', __file__]) 