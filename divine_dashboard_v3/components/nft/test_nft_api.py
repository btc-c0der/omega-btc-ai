
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
Test suite for NFT Dashboard API
"""

import pytest
import json
import asyncio
from pathlib import Path
from unittest.mock import patch, MagicMock
import base64
import io
from PIL import Image

from fastapi import FastAPI
from fastapi.testclient import TestClient

from divine_dashboard_v3.components.nft.nft_dashboard import NFTDashboard, create_nft_dashboard

# Fixtures
@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    img = Image.new('RGB', (100, 100), color='blue')
    return img

@pytest.fixture
def image_base64(sample_image):
    """Convert sample image to base64."""
    buffered = io.BytesIO()
    sample_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create temporary output directory."""
    output_dir = tmp_path / "nft_test_output"
    output_dir.mkdir()
    return output_dir

@pytest.fixture
def mock_app():
    """Create a mock FastAPI app."""
    return FastAPI()

@pytest.fixture
def nft_dashboard(mock_app, temp_output_dir):
    """Create NFTDashboard instance."""
    with patch("divine_dashboard_v3.components.nft.nft_dashboard.NFTGenerator"):
        with patch("divine_dashboard_v3.components.nft.nft_dashboard.NFTBlockchain"):
            dashboard = NFTDashboard(mock_app, output_dir=str(temp_output_dir))
            return dashboard

@pytest.fixture
def client(mock_app, nft_dashboard):
    """Create a test client."""
    return TestClient(mock_app)

# API Tests
class TestNFTDashboardAPI:
    
    def test_initialization(self, mock_app, temp_output_dir):
        """Test NFTDashboard initialization."""
        with patch("divine_dashboard_v3.components.nft.nft_dashboard.NFTGenerator"):
            with patch("divine_dashboard_v3.components.nft.nft_dashboard.NFTBlockchain"):
                dashboard = NFTDashboard(mock_app, output_dir=str(temp_output_dir))
                assert dashboard.app == mock_app
                assert dashboard.output_dir == str(temp_output_dir)
                assert dashboard.generator is not None
                assert dashboard.blockchain is not None
    
    def test_mint_nft_endpoint(self, client, image_base64, nft_dashboard):
        """Test mint NFT endpoint."""
        # Mock mint_nft to return a mock result
        async def mock_mint(*args, **kwargs):
            return {
                "success": True,
                "image": "test.png",
                "metadata": "test_metadata.json",
                "transaction_hash": "0xtest"
            }
        
        # Apply the mock
        nft_dashboard.mint_nft = mock_mint
        
        # Make the request
        response = client.post(
            "/mint-nft",
            json={
                "image_data": f"data:image/png;base64,{image_base64}",
                "name": "Test NFT",
                "description": "API Test"
            }
        )
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "transaction_hash" in data
    
    def test_mint_nft_endpoint_failure(self, client, image_base64, nft_dashboard):
        """Test mint NFT endpoint failure."""
        # Mock mint_nft to return a failure
        async def mock_mint(*args, **kwargs):
            return {
                "success": False,
                "error": "Test error"
            }
        
        # Apply the mock
        nft_dashboard.mint_nft = mock_mint
        
        # Make the request
        response = client.post(
            "/mint-nft",
            json={
                "image_data": f"data:image/png;base64,{image_base64}",
                "name": "Test NFT",
                "description": "API Test"
            }
        )
        
        # Verify response
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "error" in data
    
    @pytest.mark.asyncio
    async def test_mint_nft_function(self, nft_dashboard, image_base64):
        """Test mint_nft function."""
        # Mock generator and blockchain
        async def mock_generate(*args, **kwargs):
            return {
                "image": "test.png",
                "metadata": "test_metadata.json",
                "divine_metrics": {"test": 0.5},
                "rarity": 80.0
            }
        
        async def mock_mint(*args, **kwargs):
            return {
                "success": True,
                "transaction_hash": "0xtest",
                "token_id": 123
            }
        
        nft_dashboard.generator.generate_nft = mock_generate
        nft_dashboard.blockchain.mint_nft = mock_mint
        
        # Call mint_nft
        result = await nft_dashboard.mint_nft(
            image_data=f"data:image/png;base64,{image_base64}",
            name="Test NFT",
            description="Function Test"
        )
        
        # Verify result
        assert result["success"] is True
        assert result["image"] == "test.png"
        assert result["metadata"] == "test_metadata.json"
        assert result["transaction_hash"] == "0xtest"
        assert result["divine_metrics"]["test"] == 0.5
    
    @pytest.mark.asyncio
    async def test_mint_nft_function_generator_error(self, nft_dashboard, image_base64):
        """Test mint_nft function with generator error."""
        # Mock generator to raise exception
        async def mock_generate(*args, **kwargs):
            raise Exception("Test generator error")
        
        nft_dashboard.generator.generate_nft = mock_generate
        
        # Call mint_nft
        result = await nft_dashboard.mint_nft(
            image_data=f"data:image/png;base64,{image_base64}",
            name="Test NFT",
            description="Error Test"
        )
        
        # Verify result
        assert result["success"] is False
        assert "error" in result
        assert "Test generator error" in result["error"]
    
    @pytest.mark.asyncio
    async def test_mint_nft_function_blockchain_error(self, nft_dashboard, image_base64):
        """Test mint_nft function with blockchain error."""
        # Mock generator and blockchain
        async def mock_generate(*args, **kwargs):
            return {
                "image": "test.png",
                "metadata": "test_metadata.json",
                "divine_metrics": {"test": 0.5},
                "rarity": 80.0
            }
        
        async def mock_mint(*args, **kwargs):
            raise Exception("Test blockchain error")
        
        nft_dashboard.generator.generate_nft = mock_generate
        nft_dashboard.blockchain.mint_nft = mock_mint
        
        # Call mint_nft
        result = await nft_dashboard.mint_nft(
            image_data=f"data:image/png;base64,{image_base64}",
            name="Test NFT",
            description="Error Test"
        )
        
        # Verify result
        assert result["success"] is False
        assert "error" in result
        assert "Test blockchain error" in result["error"]
    
    def test_create_nft_dashboard(self, mock_app, temp_output_dir):
        """Test create_nft_dashboard function."""
        with patch("divine_dashboard_v3.components.nft.nft_dashboard.NFTGenerator"):
            with patch("divine_dashboard_v3.components.nft.nft_dashboard.NFTBlockchain"):
                with patch("divine_dashboard_v3.components.nft.nft_dashboard.gr.Blocks") as mock_blocks:
                    # Mock the Blocks instance
                    mock_interface = MagicMock()
                    mock_blocks.return_value = mock_interface
                    
                    # Call create_nft_dashboard
                    dashboard, interface = create_nft_dashboard(mock_app, str(temp_output_dir))
                    
                    # Verify result
                    assert isinstance(dashboard, NFTDashboard)
                    assert interface == mock_interface 