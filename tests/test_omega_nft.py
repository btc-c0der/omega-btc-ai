import pytest
import json
from datetime import datetime
from pathlib import Path
from omega_ai.blockchain.omega_nft import OMEGANFTMetadata, OMEGANFTGenerator
from omega_ai.blockchain.whale_art import WhaleMovement

@pytest.fixture
def test_movement():
    """Create a test whale movement."""
    return WhaleMovement(
        tx_hash="test_hash_123",
        timestamp=int(datetime.now().timestamp()),
        value=150.5,
        from_addresses=["addr1", "addr2"],
        to_addresses=["addr3", "addr4"],
        fibonacci_level=0.618,
        cluster_size=4
    )

@pytest.fixture
def nft_generator(tmp_path):
    """Create an NFT generator with temporary output directory."""
    return OMEGANFTGenerator(output_dir=str(tmp_path))

def test_omeganft_metadata_initialization():
    """Test OMEGANFTMetadata initialization and default values."""
    metadata = OMEGANFTMetadata(
        name="Test NFT",
        description="Test Description",
        image="test.png"
    )
    
    assert metadata.name == "Test NFT"
    assert metadata.description == "Test Description"
    assert metadata.image == "test.png"
    assert metadata.attributes == []
    assert metadata.blockchain_data == {}
    assert metadata.divine_metrics == {}
    assert metadata.rarity_score == 0.0
    assert metadata.edition == 1
    assert metadata.total_editions == 1

def test_calculate_divine_metrics(nft_generator, test_movement):
    """Test divine metrics calculation."""
    metrics = nft_generator._calculate_divine_metrics(test_movement)
    
    assert "divine_alignment" in metrics
    assert "cluster_harmony" in metrics
    assert "temporal_resonance" in metrics
    assert "fibonacci_level" in metrics
    assert "golden_ratio_alignment" in metrics
    assert "silver_ratio_alignment" in metrics
    
    # Check value ranges
    assert 0 <= metrics["divine_alignment"] <= 1
    assert 0 <= metrics["cluster_harmony"] <= 1
    assert 0 <= metrics["temporal_resonance"] <= 1
    assert metrics["fibonacci_level"] == 0.618

def test_calculate_rarity_score(nft_generator):
    """Test rarity score calculation."""
    divine_metrics = {
        "divine_alignment": 0.2,
        "cluster_harmony": 0.3,
        "temporal_resonance": 0.4,
        "fibonacci_level": 0.618
    }
    
    score = nft_generator._calculate_rarity_score(divine_metrics)
    
    assert 0 <= score <= 100
    assert isinstance(score, float)

def test_generate_blockchain_data(nft_generator, test_movement):
    """Test blockchain data generation."""
    data = nft_generator._generate_blockchain_data(test_movement)
    
    assert data["transaction_hash"] == test_movement.tx_hash
    assert data["block_timestamp"] == test_movement.timestamp
    assert data["value_btc"] == test_movement.value
    assert data["from_addresses"] == test_movement.from_addresses
    assert data["to_addresses"] == test_movement.to_addresses
    assert data["cluster_size"] == test_movement.cluster_size
    assert data["network"] == "Bitcoin"
    assert data["chain_id"] == "mainnet"

def test_generate_attributes(nft_generator, test_movement):
    """Test NFT attributes generation."""
    divine_metrics = {
        "divine_alignment": 0.2,
        "cluster_harmony": 0.3,
        "temporal_resonance": 0.4,
        "fibonacci_level": 0.618
    }
    rarity_score = 85.5
    
    attributes = nft_generator._generate_attributes(
        test_movement,
        divine_metrics,
        rarity_score
    )
    
    assert len(attributes) == 6
    assert any(attr["trait_type"] == "Value" for attr in attributes)
    assert any(attr["trait_type"] == "Fibonacci Level" for attr in attributes)
    assert any(attr["trait_type"] == "Cluster Size" for attr in attributes)
    assert any(attr["trait_type"] == "Divine Alignment" for attr in attributes)
    assert any(attr["trait_type"] == "Temporal Resonance" for attr in attributes)
    assert any(attr["trait_type"] == "Rarity Score" for attr in attributes)

@pytest.mark.asyncio
async def test_generate_nft(nft_generator, test_movement):
    """Test complete NFT generation."""
    nft_data = await nft_generator.generate_nft(test_movement)
    
    assert "metadata" in nft_data
    assert "visualization" in nft_data
    assert "rarity_score" in nft_data
    assert "divine_metrics" in nft_data
    
    # Check metadata file exists and is valid JSON
    metadata_path = Path(nft_data["metadata"])
    assert metadata_path.exists()
    
    with open(metadata_path) as f:
        metadata = json.load(f)
        assert metadata["name"].startswith("OMEGA Whale Movement #")
        assert "description" in metadata
        assert "image" in metadata
        assert "attributes" in metadata
        assert "blockchain_data" in metadata
        assert "divine_metrics" in metadata
        assert "rarity_score" in metadata
        assert "created_at" in metadata
        assert "updated_at" in metadata

@pytest.mark.asyncio
async def test_generate_collection(nft_generator, test_movement):
    """Test collection generation."""
    # Create multiple movements
    movements = [
        WhaleMovement(
            tx_hash=f"test_hash_{i}",
            timestamp=int(datetime.now().timestamp()) + i,
            value=100 + i * 10,
            from_addresses=[f"addr{i}"],
            to_addresses=[f"addr{i+1}"],
            fibonacci_level=0.618,
            cluster_size=2
        )
        for i in range(10)
    ]
    
    collection_data = await nft_generator.generate_collection(movements)
    
    assert "collection_metadata" in collection_data
    assert "statistics" in collection_data
    assert "nfts" in collection_data
    
    # Check collection metadata file exists and is valid JSON
    collection_path = Path(collection_data["collection_metadata"])
    assert collection_path.exists()
    
    with open(collection_path) as f:
        metadata = json.load(f)
        assert metadata["name"] == "OMEGA Whale Movement Collection"
        assert "description" in metadata
        assert metadata["total_supply"] == 10
        assert "created_at" in metadata
        assert "statistics" in metadata
        assert "nfts" in metadata
        assert len(metadata["nfts"]) == 10
    
    # Check statistics
    stats = collection_data["statistics"]
    assert stats["total_nfts"] == 10
    assert "average_rarity" in stats
    assert "max_rarity" in stats
    assert "min_rarity" in stats
    assert "rarity_distribution" in stats
    
    # Check rarity distribution
    distribution = stats["rarity_distribution"]
    assert all(key in distribution for key in ["legendary", "epic", "rare", "uncommon", "common"])
    assert sum(distribution.values()) == 10

def test_output_directory_creation(tmp_path):
    """Test output directory creation."""
    output_dir = tmp_path / "test_nfts"
    generator = OMEGANFTGenerator(output_dir=str(output_dir))
    
    assert output_dir.exists()
    assert (output_dir / "visualizations").exists() 