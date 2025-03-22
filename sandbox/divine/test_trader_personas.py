#!/usr/bin/env python3
"""
OMEGA BTC AI - Divine Alignment Dashboard - Trader Personas Tests
=================================================================

Tests for the trader personas API endpoint in the Divine Alignment Dashboard.

Usage:
    python -m pytest test_trader_personas.py -v [--port PORT]

Options:
    --port PORT     Port to run the API on for testing (default: tries 5051-5100)

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
import socket
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Test constants
TEST_PORT = None  # Will be determined dynamically
API_URL = None  # Will be set once port is determined
PERSONAS_ENDPOINT = "/api/trader_personas"

def check_port_available(port):
    """Check if the port is available."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result != 0  # If result is 0, port is in use
    except socket.error:
        return False

def find_available_port(start_port, max_attempts=50):
    """Find an available port starting from the given port."""
    port = start_port
    for _ in range(max_attempts):
        if check_port_available(port):
            return port
        port += 1
    
    # If no ports are available in the range, return None
    return None

class TestTraderPersonas:
    """Test suite for trader personas functionality."""
    
    @classmethod
    def setup_class(cls):
        """Set up the test class by starting the API server."""
        global API_URL, TEST_PORT
        
        # Parse command line for custom port if provided
        parser = argparse.ArgumentParser(description='Test Trader Personas API')
        parser.add_argument('--port', type=int, help='Port to use for testing')
        args, unknown = parser.parse_known_args()
        
        # Find an available port
        if args.port:
            if check_port_available(args.port):
                TEST_PORT = args.port
            else:
                print(f"Requested port {args.port} is not available. Searching for an available port...")
                TEST_PORT = find_available_port(args.port + 1)
        else:
            TEST_PORT = find_available_port(5051)
        
        if not TEST_PORT:
            pytest.fail("No available ports found for testing")
        
        API_URL = f"http://localhost:{TEST_PORT}"
        print(f"Using port {TEST_PORT} for testing")
        
        # Start the API server in a subprocess
        script_dir = os.path.dirname(os.path.abspath(__file__))
        api_script = os.path.join(script_dir, 'golden_ratio_api.py')
        
        env = os.environ.copy()
        env["FLASK_APP"] = api_script
        env["FLASK_ENV"] = "development"
        
        cls.api_process = subprocess.Popen(
            [sys.executable, api_script, "--port", str(TEST_PORT)],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give the server time to start
        time.sleep(3)
        
        # Check if server started successfully
        try:
            response = requests.get(f"{API_URL}/api/trader_personas", timeout=2)
            if response.status_code != 200:
                raise Exception(f"Server returned status code {response.status_code}")
        except Exception as e:
            pytest.fail(f"Failed to connect to test server: {str(e)}")
    
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