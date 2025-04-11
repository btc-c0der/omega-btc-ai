#!/usr/bin/env python3

"""
"TEST COVERAGE" — "FASTAPI APPLICATION"
======================================

"VIRGIL ABLOH" / "OFF-WHITE™" INSPIRED TEST SUITE
TESTS THE FASTAPI ENDPOINTS FOR THE OMEGA GRID PORTAL

Copyright (c) 2024 OMEGA BTC AI
"""

import os
import sys
import json
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

# Add parent directory to path to allow imports
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

# Import the FastAPI app
from fastapi_app import app

# Create test client
client = TestClient(app)

# Mock the grid portal component functions
@pytest.fixture(autouse=True)
def mock_grid_portal_functions():
    """Mock the grid portal component functions"""
    with patch("fastapi_app.get_commands") as mock_get_commands, \
         patch("fastapi_app.get_bots") as mock_get_bots, \
         patch("fastapi_app.execute_command") as mock_execute_command:
        
        # Setup mock return values
        mock_get_commands.return_value = AsyncMock(return_value={
            "status": "success",
            "commands": [
                {
                    "id": "show_status",
                    "name": "SHOW STATUS",
                    "description": "Display the current status of all bots and services",
                    "emoji": "👁️‍🗨️"
                }
            ]
        })
        
        mock_get_bots.return_value = AsyncMock(return_value={
            "status": "success",
            "bots": [
                {"id": "test_bot", "name": "Test Bot", "status": "inactive"}
            ]
        })
        
        mock_execute_command.return_value = AsyncMock(return_value={
            "status": "success",
            "output": "Command executed successfully",
            "timestamp": "2024-01-01T00:00:00"
        })
        
        yield {
            "get_commands": mock_get_commands,
            "get_bots": mock_get_bots,
            "execute_command": mock_execute_command
        }

# Test root endpoint
def test_index():
    """
    "TEST ROOT" — "VERIFY ROOT ENDPOINT RETURNS HTML"
    """
    # Mock the FileResponse
    with patch("fastapi_app.FileResponse") as mock_file_response:
        mock_file_response.return_value = "HTML CONTENT"
        
        response = client.get("/")
        
        # Verify FileResponse was called
        mock_file_response.assert_called_once()
        
        # Check that we get the mocked response
        assert response.status_code == 200

# Test get commands endpoint
def test_grid_commands(mock_grid_portal_functions):
    """
    "TEST COMMANDS ENDPOINT" — "VERIFY API RETURNS COMMANDS"
    """
    response = client.get("/api/grid/commands")
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["commands"]) > 0
    
    # Verify our mock was called
    mock_grid_portal_functions["get_commands"].return_value.assert_called_once()

# Test get bots endpoint
def test_grid_bots(mock_grid_portal_functions):
    """
    "TEST BOTS ENDPOINT" — "VERIFY API RETURNS BOTS"
    """
    response = client.get("/api/grid/bots")
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["bots"]) > 0
    
    # Verify our mock was called
    mock_grid_portal_functions["get_bots"].return_value.assert_called_once()

# Test execute command endpoint
def test_grid_execute(mock_grid_portal_functions):
    """
    "TEST EXECUTE ENDPOINT" — "VERIFY API EXECUTES COMMANDS"
    """
    response = client.post(
        "/api/grid/execute",
        json={"commandId": "show_status"}
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["output"] == "Command executed successfully"
    
    # Verify our mock was called with the right arguments
    mock_grid_portal_functions["execute_command"].return_value.assert_called_once_with("show_status", None)

# Test execute command with parameter
def test_grid_execute_with_param(mock_grid_portal_functions):
    """
    "TEST PARAM EXECUTION" — "VERIFY API HANDLES COMMAND PARAMETERS"
    """
    response = client.post(
        "/api/grid/execute",
        json={"commandId": "start_bot", "param": "test_bot"}
    )
    
    assert response.status_code == 200
    
    # Verify our mock was called with the right arguments
    mock_grid_portal_functions["execute_command"].return_value.assert_called_once_with("start_bot", "test_bot")

# Test error handling for missing command ID
def test_grid_execute_missing_command(mock_grid_portal_functions):
    """
    "TEST ERROR HANDLING" — "VERIFY API HANDLES MISSING COMMAND ID"
    """
    response = client.post(
        "/api/grid/execute",
        json={"param": "test_bot"}
    )
    
    assert response.status_code == 400
    assert response.json()["status"] == "error"
    assert "Command ID is required" in response.json()["output"]

# Test error handling for exception during execution
def test_grid_execute_exception(mock_grid_portal_functions):
    """
    "TEST EXCEPTION HANDLING" — "VERIFY API HANDLES EXCEPTIONS"
    """
    # Mock execute_command to raise an exception
    mock_grid_portal_functions["execute_command"].return_value.side_effect = Exception("Test exception")
    
    response = client.post(
        "/api/grid/execute",
        json={"commandId": "show_status"}
    )
    
    assert response.status_code == 500
    assert response.json()["status"] == "error"
    assert "Error:" in response.json()["output"]

# Run the tests
if __name__ == "__main__":
    pytest.main(["-xvs", __file__]) 