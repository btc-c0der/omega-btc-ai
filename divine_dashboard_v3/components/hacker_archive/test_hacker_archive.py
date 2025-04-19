# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
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
Test cases for Hacker Archive NFT Generator
"""

import os
import shutil
import unittest
import tempfile
import asyncio
from pathlib import Path
import json
from unittest.mock import patch, MagicMock

import sys
sys.path.append('/Users/fsiqueira/OMEGA/omega-btc-ai')

from divine_dashboard_v3.components.hacker_archive.hacker_archive_generator import (
    HackerArchiveNFTGenerator,
    HACKER_CREWS,
    DEFACEMENT_YEARS,
    DEFACEMENT_TYPES
)

# Pytest fixtures
import pytest

@pytest.fixture
def temp_output_dir():
    """Create temporary directory for test outputs."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def generator(temp_output_dir):
    """Create HackerArchiveNFTGenerator instance for testing."""
    return HackerArchiveNFTGenerator(output_dir=temp_output_dir)

class TestHackerArchiveNFTGenerator(unittest.TestCase):
    """Test cases for HackerArchiveNFTGenerator."""
    
    def setUp(self):
        """Set up the test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.generator = HackerArchiveNFTGenerator(output_dir=self.temp_dir)
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test generator initialization creates required directories."""
        self.assertTrue(os.path.exists(self.temp_dir))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "images")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "metadata")))
    
    def test_unique_id_generation(self):
        """Test unique ID generation."""
        id1 = self.generator._generate_unique_id("test_data_1")
        id2 = self.generator._generate_unique_id("test_data_2")
        
        # Verify IDs are strings of the expected length
        self.assertIsInstance(id1, str)
        self.assertEqual(len(id1), 12)
        
        # Verify different inputs give different IDs
        self.assertNotEqual(id1, id2)
        
        # Verify same input gives different IDs (due to timestamp)
        id3 = self.generator._generate_unique_id("test_data_1")
        self.assertNotEqual(id1, id3)
    
    @patch('divine_dashboard_v3.components.hacker_archive.hacker_archive_generator.Image')
    def test_generate_hacker_ascii_art(self, mock_image):
        """Test ASCII art generation."""
        # Setup mock
        mock_img = MagicMock()
        mock_draw = MagicMock()
        mock_image.new.return_value = mock_img
        mock_image.Draw.return_value = mock_draw
        
        # Test with default parameters
        result = self.generator._generate_hacker_ascii_art()
        
        # Verify image creation
        mock_image.new.assert_called_once()
        
        # Test with specific parameters
        result = self.generator._generate_hacker_ascii_art(
            size=(400, 400),
            pattern_type="matrix",
            crew_name="Test Crew"
        )
        
        # Verify crew name was added
        self.assertTrue(mock_draw.text.called)
    
    def test_calculate_rarity_score(self):
        """Test rarity score calculation."""
        # Test with common parameters
        metadata = {
            "year": "2005",
            "crew": "Turkish Hackers",
            "rank": "Elite",
            "defacement_type": "For Fun"
        }
        score = self.generator._calculate_rarity_score(metadata)
        
        # Verify score is a float between 0 and 100
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        
        # Test with rare parameters
        rare_metadata = {
            "year": "1999",
            "crew": "bl0w",
            "rank": "Ph34r3d",
            "defacement_type": "Hacktivism"
        }
        rare_score = self.generator._calculate_rarity_score(rare_metadata)
        
        # Verify rare parameters produce higher score
        self.assertGreater(rare_score, score)

# Async test cases for asynchronous methods
@pytest.mark.asyncio
class TestHackerArchiveNFTGeneratorAsync:
    """Async test cases for HackerArchiveNFTGenerator."""
    
    async def test_generate_hacker_nft(self, generator):
        """Test NFT generation with specific parameters."""
        # Mock the image generation to avoid PIL dependency
        with patch('divine_dashboard_v3.components.hacker_archive.hacker_archive_generator.HackerArchiveNFTGenerator._generate_hacker_ascii_art') as mock_art:
            # Create a mock image
            mock_img = MagicMock()
            mock_img.size = (800, 800)
            mock_draw = MagicMock()
            mock_draw.textsize.return_value = (100, 20)
            mock_art.return_value = mock_img
            
            with patch('divine_dashboard_v3.components.hacker_archive.hacker_archive_generator.ImageDraw.Draw', return_value=mock_draw):
                # Generate an NFT
                nft_info = await generator.generate_hacker_nft(
                    crew="bl0w",
                    year="1999",
                    defacement_type="Hacktivism",
                    pattern="matrix",
                    custom_text="H4CK THE PLANET"
                )
                
                # Verify result structure
                assert "id" in nft_info
                assert "name" in nft_info
                assert "image_path" in nft_info
                assert "metadata_path" in nft_info
                assert "rarity_score" in nft_info
                assert "rarity_tier" in nft_info
                
                # Verify values
                assert nft_info["crew"] == "bl0w"
                assert nft_info["year"] == "1999"
                assert nft_info["defacement_type"] == "Hacktivism"
                
                # Verify files were created
                assert os.path.exists(nft_info["image_path"])
                assert os.path.exists(nft_info["metadata_path"])
                
                # Verify metadata content
                with open(nft_info["metadata_path"], 'r') as f:
                    metadata = json.load(f)
                    assert metadata["name"] == nft_info["name"]
                    assert metadata["crew"] == "bl0w"
                    assert metadata["year"] == "1999"
                    assert metadata["rarity_score"] > 0
    
    async def test_batch_generate_nfts(self, generator):
        """Test batch NFT generation."""
        # Mock image generation for speed
        with patch('divine_dashboard_v3.components.hacker_archive.hacker_archive_generator.HackerArchiveNFTGenerator._generate_hacker_ascii_art') as mock_art:
            # Create a mock image
            mock_img = MagicMock()
            mock_img.size = (800, 800)
            mock_draw = MagicMock()
            mock_draw.textsize.return_value = (100, 20)
            mock_art.return_value = mock_img
            
            with patch('divine_dashboard_v3.components.hacker_archive.hacker_archive_generator.ImageDraw.Draw', return_value=mock_draw):
                # Generate a batch of NFTs
                batch_size = 3
                results = await generator.batch_generate_nfts(
                    count=batch_size,
                    crews=["bl0w", "Global Hell"],
                    years=["1999", "2000"]
                )
                
                # Verify number of results
                assert len(results) == batch_size
                
                # Verify all NFTs were generated successfully
                successful = [nft for nft in results if "status" not in nft or nft["status"] != "error"]
                assert len(successful) == batch_size
                
                # Verify batch information
                assert all("batch_id" in nft for nft in results)
                assert all("batch_index" in nft for nft in results)
                
                # Verify NFT attributes
                for nft in results:
                    assert nft["crew"] in ["bl0w", "Global Hell"]
                    assert nft["year"] in ["1999", "2000"]

# Integration test to ensure the full pipeline works
def test_full_generation_pipeline(temp_output_dir):
    """Test the full NFT generation pipeline."""
    # Skip if running in CI environment to avoid heavy computation
    if os.environ.get('CI'):
        pytest.skip("Skipping integration test in CI environment")
    
    # Create generator
    generator = HackerArchiveNFTGenerator(output_dir=temp_output_dir)
    
    # Run async test in event loop
    async def test():
        # Generate an NFT
        nft_info = await generator.generate_hacker_nft(
            crew="bl0w",
            year="1999"
        )
        
        # Verify NFT was generated
        assert os.path.exists(nft_info["image_path"])
        assert os.path.exists(nft_info["metadata_path"])
        
        # Verify statistics
        stats = generator.get_nft_stats()
        assert stats["total_nfts"] > 0
    
    # Run the async test
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())

# Run the tests if this file is executed directly
if __name__ == "__main__":
    unittest.main() 