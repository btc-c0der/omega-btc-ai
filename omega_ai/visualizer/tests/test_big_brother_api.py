#!/usr/bin/env python3
"""
Test cases for Big Brother API endpoints
"""

import json
import pytest
import asyncio
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the server app for testing
from omega_ai.visualizer.backend.reggae_dashboard_server import ReggaeDashboardServer

# Create a test client
test_server = ReggaeDashboardServer()
client = TestClient(test_server.app)

@pytest.fixture
def mock_redis_data():
    """Mock Redis data for testing."""
    return {
        "long_position": {
            "entry_price": 84500,
            "size": 0.01,
            "leverage": 10,
            "direction": "LONG",
            "entry_time": "2023-03-22T10:00:00",
            "unrealized_pnl": 125.5,
            "take_profits": [{"percentage": 50, "price": 85500}],
            "stop_loss": 83000
        },
        "short_position": {
            "entry_price": 84200,
            "size": 0.015,
            "leverage": 5,
            "direction": "SHORT",
            "entry_time": "2023-03-22T10:00:00",
            "unrealized_pnl": -45.2,
            "take_profits": [{"percentage": 50, "price": 83200}],
            "stop_loss": 85700
        },
        "fibonacci:current_levels": {
            "direction": "LONG",
            "base_price": 84500,
            "levels": {
                "0.0": 84500,
                "0.236": 85003.2,
                "0.382": 85318.9,
                "0.5": 85565.0,
                "0.618": 85822.3,
                "0.786": 86178.5,
                "1.0": 86630.0,
                "1.618": 87845.7,
                "2.618": 89769.2
            }
        }
    }

def test_redis_connection_error():
    """Test behavior when Redis connection fails."""
    # Create server with no Redis connection
    app = ReggaeDashboardServer()
    app.redis_client = None
    
    client = TestClient(app.app)
    
    # Test big brother data endpoint
    response = client.get("/api/big-brother-data")
    assert response.status_code == 200
    assert "error" in response.json()
    
    # Test flow endpoints
    response = client.get("/api/flow/3d")
    assert response.status_code == 200
    assert "error" in response.json()
    
    response = client.get("/api/flow/2d")
    assert response.status_code == 200
    assert "error" in response.json()

# Let's test the frontend code instead, which is already in place
def test_frontend_components():
    """Test if all required frontend files for Big Brother panel exist."""
    # Check if HTML file exists
    html_path = Path("omega_ai/visualizer/frontend/reggae-dashboard/big_brother_panel.html")
    assert html_path.exists(), "big_brother_panel.html file not found"
    
    # Check if CSS file exists
    css_path = Path("omega_ai/visualizer/frontend/reggae-dashboard/big_brother_styles.css")
    assert css_path.exists(), "big_brother_styles.css file not found"
    
    # Check if JS file exists
    js_path = Path("omega_ai/visualizer/frontend/reggae-dashboard/big_brother_panel.js")
    assert js_path.exists(), "big_brother_panel.js file not found"
    
    # Check if HTML file contains key elements
    with open(html_path, 'r') as f:
        html_content = f.read()
        # Check for key components
        assert '<div class="big-brother-panel">' in html_content
        assert 'id="positions-tab"' in html_content
        assert 'id="flow-tab"' in html_content
        assert 'id="fibonacci-tab"' in html_content
        assert 'id="elite-exits-tab"' in html_content
        assert 'id="traps-tab"' in html_content
    
    # Check if JS file has proper functionality
    with open(js_path, 'r') as f:
        js_content = f.read()
        # Check for key functions
        assert 'function initBigBrotherPanel()' in js_content
        assert 'function setupTabNavigation()' in js_content
        assert 'function generate3DFlow()' in js_content
        assert 'function generate2DFlow()' in js_content

# Let's create a simpler test for the server API structure
def test_server_api_structure():
    """Test that the server has all the expected API endpoints."""
    # Test by making actual API calls rather than inspecting routes
    # This is more reliable and avoids linting issues
    
    # Test Big Brother data endpoint
    response = client.get("/api/big-brother-data")
    assert response.status_code != 404, "Big Brother data endpoint not found"
    
    # Test 3D flow endpoint
    response = client.get("/api/flow/3d")
    assert response.status_code != 404, "3D flow endpoint not found"
    
    # Test 2D flow endpoint
    response = client.get("/api/flow/2d")
    assert response.status_code != 404, "2D flow endpoint not found"

# Let's also check that the Redis methods exist as expected
def test_server_redis_methods():
    """Test that the server has methods for Redis interaction."""
    # Just verify the method names exist without trying to call them
    server_methods = dir(test_server)
    assert "_generate_mock_data" in server_methods, "Mock data generation method missing"
    
    # Also check that Redis client is initialized
    if test_server.redis_client:
        assert hasattr(test_server.redis_client, "get"), "Redis client missing get method"

# New test to check for the "Failed to load Big Brother panel" error
def test_dashboard_big_brother_integration():
    """Test the integration of the Big Brother panel with the main dashboard."""
    # Check if the panel HTML is in the correct location
    panel_html_path = Path("omega_ai/visualizer/frontend/reggae-dashboard/big_brother_panel.html")
    assert panel_html_path.exists(), "big_brother_panel.html not found, would cause loading error"
    
    # Check if the main dashboard HTML contains the code to load the panel
    dashboard_html_path = Path("omega_ai/visualizer/frontend/reggae-dashboard/live-dashboard.html")
    assert dashboard_html_path.exists(), "live-dashboard.html not found"
    
    with open(dashboard_html_path, 'r') as f:
        dashboard_content = f.read()
        
        # Check for the elements needed to load the Big Brother panel
        assert 'id="big-brother-content"' in dashboard_content, "The container for Big Brother panel is missing"
        assert 'function loadBigBrotherPanel' in dashboard_content, "The loading function is missing"
        assert "fetch('big_brother_panel.html')" in dashboard_content, "The fetch call is missing or incorrect"
        
        # Check for error handling code
        assert 'Failed to load Big Brother monitoring panel' in dashboard_content, "Error handling message is missing"
    
    # Verify the panel HTML is valid
    with open(panel_html_path, 'r') as f:
        panel_content = f.read()
        assert '<div class="big-brother-panel">' in panel_content, "Panel HTML doesn't contain expected content"
    
    # Verify the dashboard loads the panel on DOMContentLoaded
    assert "DOMContentLoaded" in dashboard_content and "loadBigBrotherPanel" in dashboard_content, "Panel is not automatically loaded"

if __name__ == "__main__":
    pytest.main(["-xvs", __file__]) 