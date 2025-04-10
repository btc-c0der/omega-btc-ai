
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
Unit tests for NFT components
"""

import pytest
import json
import asyncio
from pathlib import Path
from unittest.mock import patch, MagicMock
from PIL import Image
import io
import os
import base64
import random

from divine_dashboard_v3.components.nft.nft_metadata import NFTMetadata
from divine_dashboard_v3.components.nft.nft_blockchain import NFTBlockchain
from divine_dashboard_v3.components.nft.nft_generator import NFTGenerator

# Fixtures
@pytest.fixture
def sample_metadata():
    """Create sample NFT metadata for testing."""
    return NFTMetadata(
        name="Test NFT",
        description="Test Description",
        image="test.png",
        divine_metrics={
            "divine_harmony": 0.8,
            "sacred_balance": 0.7,
            "golden_ratio": 1.618
        },
        attributes=[{"trait_type": "Test", "value": "Value"}]
    )

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create temporary output directory."""
    output_dir = tmp_path / "nft_test_output"
    output_dir.mkdir()
    return output_dir

@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    img = Image.new('RGB', (100, 100), color='blue')
    return img

@pytest.fixture
def image_bytes(sample_image):
    """Convert sample image to bytes."""
    img_byte_arr = io.BytesIO()
    sample_image.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

@pytest.fixture
def blockchain():
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

# NFTMetadata Tests
class TestNFTMetadata:
    
    def test_initialization(self, sample_metadata):
        """Test NFTMetadata initialization."""
        assert sample_metadata.name == "Test NFT"
        assert sample_metadata.description == "Test Description"
        assert sample_metadata.image == "test.png"
        assert len(sample_metadata.attributes) == 1
        assert sample_metadata.divine_metrics["divine_harmony"] == 0.8
        assert sample_metadata.created_at is not None
        assert sample_metadata.updated_at is not None
    
    def test_to_dict(self, sample_metadata):
        """Test conversion to dictionary."""
        data = sample_metadata.to_dict()
        assert data["name"] == "Test NFT"
        assert data["description"] == "Test Description"
        assert data["divine_metrics"]["divine_harmony"] == 0.8
        assert "created_at" in data
    
    def test_to_json(self, sample_metadata):
        """Test conversion to JSON."""
        json_data = sample_metadata.to_json()
        data = json.loads(json_data)
        assert data["name"] == "Test NFT"
        assert data["description"] == "Test Description"
    
    def test_save_and_load(self, sample_metadata, temp_output_dir):
        """Test saving and loading metadata."""
        # Save metadata
        filepath = temp_output_dir / "test_metadata.json"
        sample_metadata.save(str(filepath))
        
        # Verify file exists
        assert filepath.exists()
        
        # Load metadata
        loaded = NFTMetadata.from_file(str(filepath))
        assert loaded.name == sample_metadata.name
        assert loaded.description == sample_metadata.description
        assert loaded.divine_metrics["divine_harmony"] == sample_metadata.divine_metrics["divine_harmony"]
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "name": "Dict NFT",
            "description": "Created from dict",
            "image": "dict.png",
            "divine_metrics": {"test": 0.5}
        }
        metadata = NFTMetadata.from_dict(data)
        assert metadata.name == "Dict NFT"
        assert metadata.description == "Created from dict"
        assert metadata.divine_metrics["test"] == 0.5
    
    def test_from_json(self):
        """Test creation from JSON."""
        json_str = '{"name": "JSON NFT", "description": "Created from JSON", "image": "json.png"}'
        metadata = NFTMetadata.from_json(json_str)
        assert metadata.name == "JSON NFT"
        assert metadata.description == "Created from JSON"
        assert metadata.image == "json.png"
        
    def test_post_init_defaults(self):
        """Test post initialization defaults."""
        metadata = NFTMetadata(name="Test", description="Test", image="test.png")
        assert isinstance(metadata.attributes, list)
        assert isinstance(metadata.divine_metrics, dict)
        assert isinstance(metadata.blockchain_data, dict)
        assert metadata.created_at == metadata.updated_at

# NFTBlockchain Tests
class TestNFTBlockchain:
    
    def test_initialization(self):
        """Test NFTBlockchain initialization."""
        blockchain = NFTBlockchain(
            api_key="test_key",
            contract_address="0xtest",
            network="testnet"
        )
        assert blockchain.api_key == "test_key"
        assert blockchain.contract_address == "0xtest"
        assert blockchain.network == "testnet"
        
    def test_initialization_from_env(self, monkeypatch):
        """Test initialization from environment variables."""
        monkeypatch.setenv("NFT_API_KEY", "env_key")
        monkeypatch.setenv("NFT_CONTRACT_ADDRESS", "0xenv")
        
        blockchain = NFTBlockchain()
        assert blockchain.api_key == "env_key"
        assert blockchain.contract_address == "0xenv"
        
    @pytest.mark.asyncio
    async def test_upload_to_ipfs(self, blockchain, temp_output_dir):
        """Test uploading to IPFS."""
        # Create test file
        test_file = temp_output_dir / "test_upload.txt"
        test_file.write_text("Test content")
        
        # Upload to IPFS
        result = await blockchain.upload_to_ipfs(test_file)
        
        assert result["success"] is True
        assert "hash" in result
        assert result["hash"].startswith("Qm")
        assert result["name"] == "test_upload.txt"
        assert result["size"] == len("Test content")
        assert "ipfs.io" in result["url"]
        
    @pytest.mark.asyncio
    async def test_upload_to_ipfs_error(self, blockchain):
        """Test IPFS upload error handling."""
        # Test with non-existent file
        result = await blockchain.upload_to_ipfs("nonexistent_file.txt")
        
        assert result["success"] is False
        assert "error" in result
        
    @pytest.mark.asyncio
    async def test_mint_nft(self, blockchain, sample_metadata, temp_output_dir):
        """Test minting NFT."""
        # Save metadata
        metadata_path = temp_output_dir / "mint_test_metadata.json"
        sample_metadata.save(str(metadata_path))
        
        # Create image file
        image_path = temp_output_dir / "test.png"
        Image.new('RGB', (10, 10)).save(str(image_path))
        
        # Update metadata with correct image path
        sample_metadata.image = str(image_path)
        sample_metadata.save(str(metadata_path))
        
        # Mock upload_to_ipfs to return success
        original_upload = blockchain.upload_to_ipfs
        
        async def mock_upload(*args, **kwargs):
            return {
                "success": True,
                "hash": "QmTest",
                "name": Path(args[0]).name,
                "size": 100,
                "url": f"https://ipfs.io/ipfs/QmTest"
            }
            
        blockchain.upload_to_ipfs = mock_upload
        
        # Mint NFT
        result = await blockchain.mint_nft(metadata_path, "0xrecipient")
        
        # Restore original method
        blockchain.upload_to_ipfs = original_upload
        
        assert result["success"] is True
        assert "transaction_hash" in result
        assert result["transaction_hash"].startswith("0x")
        assert result["recipient"] == "0xrecipient"
        assert "metadata_url" in result
        assert "image_url" in result
        
    @pytest.mark.asyncio
    async def test_mint_nft_metadata_upload_failure(self, blockchain, sample_metadata, temp_output_dir):
        """Test minting NFT with metadata upload failure."""
        # Save metadata
        metadata_path = temp_output_dir / "mint_fail_metadata.json"
        sample_metadata.save(str(metadata_path))
        
        # Mock upload_to_ipfs to return failure
        original_upload = blockchain.upload_to_ipfs
        
        async def mock_upload(*args, **kwargs):
            return {
                "success": False,
                "error": "Test upload error"
            }
            
        blockchain.upload_to_ipfs = mock_upload
        
        # Mint NFT
        result = await blockchain.mint_nft(metadata_path)
        
        # Restore original method
        blockchain.upload_to_ipfs = original_upload
        
        assert result["success"] is False
        assert "error" in result
        
    @pytest.mark.asyncio
    async def test_check_transaction(self, blockchain):
        """Test checking transaction status."""
        tx_hash = "0x" + "".join(random.choices("0123456789abcdef", k=64))
        
        result = await blockchain.check_transaction(tx_hash)
        
        assert "transaction_hash" in result
        assert result["transaction_hash"] == tx_hash
        assert "status" in result
        assert result["status"] in ["pending", "confirmed", "failed"]
        
        if result["status"] == "confirmed":
            assert "block_number" in result
            assert result["confirmation_count"] > 0
        else:
            assert result["confirmation_count"] == 0

# NFTGenerator Tests
@patch("divine_dashboard_v3.components.nft.nft_generator.NFTGenerator._calculate_divine_metrics")
@patch("divine_dashboard_v3.components.nft.nft_generator.NFTGenerator._calculate_rarity")
@patch("divine_dashboard_v3.components.nft.nft_generator.NFTGenerator._generate_unique_id")
class TestNFTGenerator:
    
    def test_initialization(self, mock_id, mock_rarity, mock_metrics, temp_output_dir):
        """Test NFTGenerator initialization."""
        generator = NFTGenerator(output_dir=str(temp_output_dir))
        assert generator.output_dir == str(temp_output_dir)
        
        # Verify output directories are created
        assert Path(generator.output_dir).exists()
        assert Path(generator.output_dir, "images").exists()
        assert Path(generator.output_dir, "metadata").exists()
        
    @pytest.mark.asyncio
    async def test_generate_nft_from_image(self, mock_id, mock_rarity, mock_metrics, generator, sample_image):
        """Test generating NFT from image."""
        # Mock return values
        mock_id.return_value = "test123"
        mock_metrics.return_value = {
            "divine_harmony": 0.8, 
            "sacred_balance": 0.7
        }
        mock_rarity.return_value = 85.0
        
        # Generate NFT
        result = await generator.generate_nft(
            image_data=sample_image,
            name="Test NFT",
            description="Test Description",
            attributes=[{"trait_type": "Test", "value": "Value"}]
        )
        
        # Verify result
        assert "metadata" in result
        assert "image" in result
        assert "divine_metrics" in result
        assert "rarity" in result
        assert result["rarity"] == 85.0
        assert result["divine_metrics"]["divine_harmony"] == 0.8
        
        # Verify files were created
        metadata_file = Path(result["metadata"])
        image_file = Path(result["image"])
        assert metadata_file.exists()
        assert image_file.exists()
        
        # Verify metadata content
        with open(metadata_file) as f:
            metadata = json.load(f)
            assert metadata["name"] == "Test NFT"
            assert metadata["description"] == "Test Description"
            assert metadata["image"] == str(image_file)
            assert metadata["divine_metrics"] == {"divine_harmony": 0.8, "sacred_balance": 0.7}
            assert metadata["rarity_score"] == 85.0
            
    @pytest.mark.asyncio
    async def test_generate_nft_from_bytes(self, mock_id, mock_rarity, mock_metrics, generator, image_bytes):
        """Test generating NFT from image bytes."""
        # Mock return values
        mock_id.return_value = "bytes123"
        mock_metrics.return_value = {"divine_harmony": 0.6}
        mock_rarity.return_value = 70.0
        
        # Generate NFT
        result = await generator.generate_nft(
            image_data=image_bytes,
            name="Bytes NFT"
        )
        
        # Verify result
        assert "metadata" in result
        assert "image" in result
        assert Path(result["image"]).exists()
        
    @pytest.mark.asyncio
    async def test_generate_nft_from_path(self, mock_id, mock_rarity, mock_metrics, generator, temp_output_dir, sample_image):
        """Test generating NFT from image path."""
        # Create test image
        test_img_path = temp_output_dir / "source_test.png"
        sample_image.save(str(test_img_path))
        
        # Mock return values
        mock_id.return_value = "path123"
        mock_metrics.return_value = {"sacred_balance": 0.9}
        mock_rarity.return_value = 95.0
        
        # Generate NFT
        result = await generator.generate_nft(
            image_data=str(test_img_path),
            name="Path NFT"
        )
        
        # Verify result
        assert "metadata" in result
        assert "image" in result
        assert Path(result["image"]).exists()
        assert result["divine_metrics"]["sacred_balance"] == 0.9
        
    def test_calculate_divine_metrics_real(self, mock_id, mock_rarity, mock_metrics, generator, sample_image):
        """Test actual divine metrics calculation."""
        # Restore actual method for this test
        real_calculate_metrics = NFTGenerator._calculate_divine_metrics
        
        try:
            # Replace mock with real method for this test only
            NFTGenerator._calculate_divine_metrics = real_calculate_metrics
            
            # Calculate metrics
            metrics = generator._calculate_divine_metrics(sample_image)
            
            # Verify metrics structure
            assert isinstance(metrics, dict)
            assert len(metrics) > 0
            assert all(isinstance(v, float) for v in metrics.values())
            assert all(0 <= v <= 1 for v in metrics.values() if v != 1.618)  # Golden ratio can be 1.618
            
        finally:
            # Restore mock
            NFTGenerator._calculate_divine_metrics = mock_metrics
        
    def test_calculate_rarity_real(self, mock_id, mock_rarity, mock_metrics, generator):
        """Test actual rarity calculation."""
        # Restore actual method for this test
        real_calculate_rarity = NFTGenerator._calculate_rarity
        
        try:
            # Replace mock with real method for this test only
            NFTGenerator._calculate_rarity = real_calculate_rarity
            
            # Calculate rarity
            divine_metrics = {
                "divine_harmony": 0.8,
                "sacred_balance": 0.7,
                "ethereal_vibrance": 0.9,
                "golden_ratio": 1.618
            }
            
            rarity = generator._calculate_rarity(divine_metrics)
            
            # Verify rarity
            assert isinstance(rarity, float)
            assert 0 <= rarity <= 100
            
        finally:
            # Restore mock
            NFTGenerator._calculate_rarity = mock_rarity
            
    def test_generate_unique_id_real(self, mock_id, mock_rarity, mock_metrics, generator):
        """Test actual unique ID generation."""
        # Restore actual method for this test
        real_generate_id = NFTGenerator._generate_unique_id
        
        try:
            # Replace mock with real method for this test only
            NFTGenerator._generate_unique_id = real_generate_id
            
            # Generate IDs
            id1 = generator._generate_unique_id("test1")
            id2 = generator._generate_unique_id("test2")
            
            # Verify IDs
            assert isinstance(id1, str)
            assert len(id1) > 8  # Should be reasonably long
            assert id1 != id2  # Should be unique
            
        finally:
            # Restore mock
            NFTGenerator._generate_unique_id = mock_id

# Integration Tests
class TestNFTIntegration:
    
    @pytest.mark.asyncio
    async def test_full_nft_creation_flow(self, temp_output_dir, sample_image):
        """Test full NFT creation flow from generator to blockchain."""
        # Create generator and blockchain
        generator = NFTGenerator(output_dir=str(temp_output_dir))
        blockchain = NFTBlockchain(api_key="test_key", contract_address="0xtest")
        
        # Generate NFT
        nft_result = await generator.generate_nft(
            image_data=sample_image,
            name="Integration Test NFT",
            description="Testing the full NFT creation flow"
        )
        
        # Verify NFT generation
        assert "metadata" in nft_result
        assert "image" in nft_result
        
        # Mint NFT
        mint_result = await blockchain.mint_nft(
            metadata_path=nft_result["metadata"],
            recipient="0xintegration"
        )
        
        # Verify minting
        assert mint_result["success"] is True
        assert "transaction_hash" in mint_result
        
        # Check transaction
        tx_result = await blockchain.check_transaction(mint_result["transaction_hash"])
        
        # Verify transaction check
        assert tx_result["transaction_hash"] == mint_result["transaction_hash"]
        assert "status" in tx_result
        
    @pytest.mark.asyncio
    async def test_metadata_blockchain_integration(self, temp_output_dir):
        """Test integration between metadata and blockchain components."""
        # Create metadata
        metadata = NFTMetadata(
            name="Blockchain Test NFT",
            description="Testing metadata and blockchain integration",
            image="placeholder.png",
            divine_metrics={"test": 0.5},
            attributes=[{"trait_type": "Test", "value": "Integration"}]
        )
        
        # Save metadata
        metadata_path = temp_output_dir / "integration_metadata.json"
        metadata.save(str(metadata_path))
        
        # Create placeholder image
        image_path = temp_output_dir / "placeholder.png"
        Image.new('RGB', (10, 10)).save(str(image_path))
        
        # Update metadata with real image path
        metadata.image = str(image_path)
        metadata.save(str(metadata_path))
        
        # Initialize blockchain
        blockchain = NFTBlockchain()
        
        # Mint NFT
        mint_result = await blockchain.mint_nft(metadata_path)
        
        # Verify minting
        assert mint_result["success"] is True 