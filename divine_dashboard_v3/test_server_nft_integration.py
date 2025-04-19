
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

"""
Test suite for integrating NFT functionality with the divine_server.py
"""

import pytest
import os
import asyncio
from unittest.mock import patch, MagicMock
import threading
import json
from pathlib import Path
import tempfile
import shutil

# Add server imports
from divine_dashboard_v3.divine_server import app, gradio_app, run_servers

@pytest.fixture
def temp_nft_dir():
    """Create a temporary directory for NFT output."""
    temp_dir = tempfile.mkdtemp(prefix="nft_test_")
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_nft_dashboard():
    """Create a mock NFT dashboard."""
    mock_dashboard = MagicMock()
    mock_interface = MagicMock()
    return mock_dashboard, mock_interface

@pytest.fixture
def patched_server_env(temp_nft_dir, mock_nft_dashboard):
    """Patch environment for server integration tests."""
    mock_dashboard, mock_interface = mock_nft_dashboard
    
    # Create patches
    patches = [
        patch('divine_dashboard_v3.divine_server.NFT_OUTPUT_DIR', temp_nft_dir),
        patch('divine_dashboard_v3.divine_server.create_nft_dashboard', return_value=(mock_dashboard, mock_interface)),
        patch('divine_dashboard_v3.divine_server.threading.Thread'),
        patch('divine_dashboard_v3.divine_server.uvicorn.run'),
        patch('divine_dashboard_v3.divine_server.gr.mount_gradio_app')
    ]
    
    # Apply all patches
    for p in patches:
        p.start()
    
    yield {
        'temp_dir': temp_nft_dir,
        'mock_dashboard': mock_dashboard,
        'mock_interface': mock_interface
    }
    
    # Stop all patches
    for p in patches:
        p.stop()

# Test server integration with NFT dashboard
class TestServerNFTIntegration:
    
    def test_nft_port_configuration(self):
        """Test NFT port configuration in server."""
        from divine_dashboard_v3.divine_server import NFT_PORT
        assert isinstance(NFT_PORT, int)
        assert NFT_PORT > 0
    
    def test_nft_output_dir_creation(self, patched_server_env):
        """Test NFT output directory creation."""
        from divine_dashboard_v3.divine_server import NFT_OUTPUT_DIR
        
        # Call function that should create output dir
        from divine_dashboard_v3.divine_server import run_nft_dashboard
        run_nft_dashboard()
        
        # Verify directory was created
        assert os.path.exists(NFT_OUTPUT_DIR)
    
    def test_run_nft_dashboard(self, patched_server_env):
        """Test run_nft_dashboard function."""
        from divine_dashboard_v3.divine_server import run_nft_dashboard
        
        # Run the function
        result = run_nft_dashboard()
        
        # Verify dashboard was created
        assert patched_server_env['mock_dashboard'] is not None
        assert patched_server_env['mock_interface'] is not None
        
        # Verify create_nft_dashboard was called
        from divine_dashboard_v3.divine_server import create_nft_dashboard
        create_nft_dashboard.assert_called_once()
    
    def test_nft_thread_creation(self, patched_server_env):
        """Test NFT dashboard thread creation."""
        # Call run_servers to trigger thread creation
        with patch('divine_dashboard_v3.divine_server.run_dashboard_server'):
            run_servers()
        
        # Verify Thread was created for NFT dashboard
        from divine_dashboard_v3.divine_server import threading
        
        # Find the call for the NFT thread
        nft_thread_created = False
        for call in threading.Thread.call_args_list:
            args, kwargs = call
            if 'target' in kwargs and kwargs['target'].__name__ == 'run_nft_dashboard':
                nft_thread_created = True
                break
        
        assert nft_thread_created
    
    @pytest.mark.asyncio
    async def test_nft_integration_flow(self, patched_server_env):
        """Test the complete NFT integration flow."""
        from divine_dashboard_v3.divine_server import run_nft_dashboard
        
        # Set up mocks for the NFT dashboard
        mock_dashboard = patched_server_env['mock_dashboard']
        
        # Mock the mint_nft method to return a successful result
        async def mock_mint_nft(*args, **kwargs):
            return {
                "success": True,
                "image": "test.png",
                "metadata": "test_metadata.json",
                "transaction_hash": "0xtest"
            }
            
        mock_dashboard.mint_nft = mock_mint_nft
        
        # Initialize the dashboard
        run_nft_dashboard()
        
        # Simulate a request to mint an NFT
        test_data = {
            "image_data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVQI12P4//8/AAX+Av7czFnnAAAAAElFTkSuQmCC",
            "name": "Test NFT",
            "description": "Integration Test"
        }
        
        # Call the endpoint directly (without HTTP)
        from divine_dashboard_v3.divine_server import app
        
        # Access the endpoint handler
        for route in app.routes:
            if route.path == "/mint-nft" and route.methods == {"POST"}:
                handler = route.endpoint
                break
        
        # Create a mock request
        mock_request = MagicMock()
        mock_request.json = lambda: test_data
        
        # Call the handler
        response = await handler(mock_request)
        
        # Verify response
        assert response["success"] is True
        assert "transaction_hash" in response
    
    def test_server_initialization_with_nft(self, patched_server_env):
        """Test server initialization with NFT components."""
        # Call the function that initializes the server
        with patch('divine_dashboard_v3.divine_server.run_dashboard_server'):
            run_servers()
        
        # Verify that NFT components were initialized
        from divine_dashboard_v3.divine_server import create_nft_dashboard
        create_nft_dashboard.assert_called_once()
        
        # Verify uvicorn was configured to run NFT server
        from divine_dashboard_v3.divine_server import uvicorn
        
        # Find the call for running the NFT server
        nft_server_started = False
        for call in uvicorn.run.call_args_list:
            args, kwargs = call
            if 'port' in kwargs and kwargs['port'] == 7862:  # NFT_PORT
                nft_server_started = True
                break
                
        assert nft_server_started 