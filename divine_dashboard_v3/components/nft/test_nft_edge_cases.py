
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
Edge case tests for NFT components
"""

import pytest
import json
import asyncio
from pathlib import Path
from unittest.mock import patch, MagicMock
import io
import base64
import os
import random
from PIL import Image, UnidentifiedImageError

from divine_dashboard_v3.components.nft.nft_metadata import NFTMetadata
from divine_dashboard_v3.components.nft.nft_blockchain import NFTBlockchain
from divine_dashboard_v3.components.nft.nft_generator import NFTGenerator

# Fixtures
@pytest.fixture
def temp_output_dir(tmp_path):
    """Create temporary output directory."""
    output_dir = tmp_path / "nft_edge_test_output"
    output_dir.mkdir()
    return output_dir

@pytest.fixture
def blockchain(temp_output_dir):
    """Create NFTBlockchain instance."""
    return NFTBlockchain(
        api_key="test_key",
        contract_address="0xtest",
        network="testnet"
    )

@pytest.fixture
def generator(temp_output_dir):
    """Create NFTGenerator instance."""
    return NFTGenerator(output_dir=str(temp_output_dir))

@pytest.fixture
def corrupt_image_bytes():
    """Create corrupt image bytes."""
    return b'This is not a valid image file'

@pytest.fixture
def very_large_image():
    """Create a very large image."""
    return Image.new('RGB', (5000, 5000), color='red')

@pytest.fixture
def invalid_metadata():
    """Create invalid metadata object."""
    metadata = {
        "name": "Invalid NFT",
        # Missing required field 'image'
        "description": "Invalid metadata"
    }
    return metadata

# Edge Case Tests
class TestNFTEdgeCases:
    
    # Metadata Edge Cases
    def test_metadata_missing_required_fields(self):
        """Test metadata with missing required fields."""
        with pytest.raises(TypeError):
            NFTMetadata(name="Test NFT")  # Missing description and image
    
    def test_metadata_with_empty_fields(self):
        """Test metadata with empty fields."""
        metadata = NFTMetadata(
            name="",
            description="",
            image=""
        )
        assert metadata.name == ""
        assert metadata.description == ""
        assert metadata.image == ""
    
    def test_metadata_with_invalid_json(self):
        """Test loading metadata from invalid JSON."""
        with pytest.raises(json.JSONDecodeError):
            NFTMetadata.from_json("This is not valid JSON")
    
    def test_metadata_with_nonexistent_file(self):
        """Test loading metadata from nonexistent file."""
        with pytest.raises(FileNotFoundError):
            NFTMetadata.from_file("nonexistent_file.json")
    
    # Blockchain Edge Cases
    @pytest.mark.asyncio
    async def test_upload_empty_file(self, blockchain, temp_output_dir):
        """Test uploading an empty file to IPFS."""
        # Create empty file
        empty_file = temp_output_dir / "empty.txt"
        empty_file.touch()
        
        # Upload empty file
        result = await blockchain.upload_to_ipfs(empty_file)
        
        # Should still succeed with valid hash
        assert result["success"] is True
        assert "hash" in result
        assert result["size"] == 0
    
    @pytest.mark.asyncio
    async def test_upload_very_large_file(self, blockchain, temp_output_dir, very_large_image):
        """Test uploading a very large file to IPFS."""
        # Save large image
        large_file = temp_output_dir / "large.png"
        very_large_image.save(large_file)
        
        # Upload large file
        result = await blockchain.upload_to_ipfs(large_file)
        
        # Should handle large files
        assert result["success"] is True
        assert "hash" in result
    
    @pytest.mark.asyncio
    async def test_mint_with_invalid_metadata(self, blockchain, temp_output_dir):
        """Test minting with invalid metadata."""
        # Create invalid metadata file
        metadata_path = temp_output_dir / "invalid_metadata.json"
        with open(metadata_path, 'w') as f:
            f.write("This is not valid JSON")
        
        # Attempt to mint
        result = await blockchain.mint_nft(metadata_path)
        
        # Should fail with error
        assert result["success"] is False
        assert "error" in result
    
    @pytest.mark.asyncio
    async def test_mint_with_missing_image(self, blockchain, temp_output_dir):
        """Test minting with metadata referring to a missing image."""
        # Create metadata with non-existent image
        metadata = NFTMetadata(
            name="Missing Image NFT",
            description="Image doesn't exist",
            image="nonexistent.png"
        )
        
        # Save metadata
        metadata_path = temp_output_dir / "missing_image_metadata.json"
        metadata.save(str(metadata_path))
        
        # Attempt to mint
        result = await blockchain.mint_nft(metadata_path)
        
        # Should still succeed (simulated environment)
        assert result["success"] is True
    
    @pytest.mark.asyncio
    async def test_check_invalid_transaction(self, blockchain):
        """Test checking an invalid transaction hash."""
        # Invalid transaction hash (not hex format)
        result = await blockchain.check_transaction("not-a-valid-hash")
        
        # Should still return a status (simulated environment)
        assert "transaction_hash" in result
        assert "status" in result
    
    # Generator Edge Cases
    @pytest.mark.asyncio
    async def test_generate_from_corrupt_image(self, generator, corrupt_image_bytes):
        """Test generating NFT from corrupt image bytes."""
        # Should handle corrupt image gracefully
        with pytest.raises(Exception):
            await generator.generate_nft(
                image_data=corrupt_image_bytes,
                name="Corrupt Image NFT"
            )
    
    @pytest.mark.asyncio
    async def test_generate_with_very_large_image(self, generator, very_large_image):
        """Test generating NFT from very large image."""
        # Mock the potentially expensive operations
        with patch("divine_dashboard_v3.components.nft.nft_generator.NFTGenerator._calculate_divine_metrics", return_value={"test": 0.5}):
            with patch("divine_dashboard_v3.components.nft.nft_generator.NFTGenerator._calculate_rarity", return_value=50.0):
                # Generate NFT from large image
                result = await generator.generate_nft(
                    image_data=very_large_image,
                    name="Large Image NFT"
                )
                
                # Should handle large images
                assert "metadata" in result
                assert "image" in result
                assert Path(result["image"]).exists()
    
    @pytest.mark.asyncio
    async def test_generate_with_empty_name(self, generator, sample_image):
        """Test generating NFT with empty name."""
        # Create a sample image
        img = Image.new('RGB', (100, 100), color='blue')
        
        # Generate NFT with empty name
        result = await generator.generate_nft(
            image_data=img,
            name="",
            description="NFT with empty name"
        )
        
        # Should still generate with default or empty name
        assert "metadata" in result
        assert "image" in result
        
        # Verify metadata
        with open(result["metadata"]) as f:
            metadata = json.load(f)
            assert "name" in metadata
    
    @pytest.mark.asyncio
    async def test_generate_with_special_characters(self, generator):
        """Test generating NFT with special characters in name/description."""
        # Create a sample image
        img = Image.new('RGB', (100, 100), color='green')
        
        # Generate NFT with special characters
        result = await generator.generate_nft(
            image_data=img,
            name="Special 特殊 Характеры!@#$%^&*()",
            description="Description with 特殊 Характеры!@#$%^&*()"
        )
        
        # Should handle special characters
        assert "metadata" in result
        assert "image" in result
        
        # Verify metadata
        with open(result["metadata"]) as f:
            metadata = json.load(f)
            assert metadata["name"] == "Special 特殊 Характеры!@#$%^&*()"
            assert metadata["description"] == "Description with 特殊 Характеры!@#$%^&*()"
    
    # Integration Edge Cases
    @pytest.mark.asyncio
    async def test_full_flow_with_minimal_data(self, generator, blockchain, temp_output_dir):
        """Test full NFT creation flow with minimal data."""
        # Create a minimal image
        img = Image.new('RGB', (1, 1), color='black')
        
        # Generate NFT with minimal data
        nft_result = await generator.generate_nft(
            image_data=img,
            name="Minimal"
        )
        
        # Mint NFT with minimal data
        mint_result = await blockchain.mint_nft(
            metadata_path=nft_result["metadata"]
        )
        
        # Should succeed
        assert mint_result["success"] is True
        
    @pytest.mark.asyncio
    async def test_concurrent_nft_operations(self, generator, blockchain):
        """Test concurrent NFT operations."""
        # Create multiple images
        images = [Image.new('RGB', (50, 50), color=f'#{random.randint(0, 0xFFFFFF):06x}') for _ in range(5)]
        
        # Generate NFTs concurrently
        generate_tasks = [
            generator.generate_nft(
                image_data=img,
                name=f"Concurrent NFT {i}"
            )
            for i, img in enumerate(images)
        ]
        
        # Wait for all generation tasks
        generate_results = await asyncio.gather(*generate_tasks)
        
        # Mint NFTs concurrently
        mint_tasks = [
            blockchain.mint_nft(metadata_path=result["metadata"])
            for result in generate_results
        ]
        
        # Wait for all minting tasks
        mint_results = await asyncio.gather(*mint_tasks)
        
        # Verify all succeeded
        assert all(result["success"] for result in mint_results)
        assert len(mint_results) == 5 