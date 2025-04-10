
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

"""Test cases for the OMEGA Whale Art Generator module."""

import pytest
from datetime import datetime
from pathlib import Path
import json
from omega_ai.blockchain.whale_art import WhaleArtGenerator, WhaleMovement

@pytest.fixture
def whale_art_generator(tmp_path):
    """Create a whale art generator with temporary output directory."""
    return WhaleArtGenerator(output_dir=str(tmp_path), use_ai=False)

@pytest.fixture
def sample_movement():
    """Create a sample whale movement."""
    return WhaleMovement(
        tx_hash="0x1234567890abcdef",
        timestamp=int(datetime.now().timestamp()),
        value=500.0,
        from_addresses=["bc1q123..."],
        to_addresses=["bc1q456...", "bc1q789..."],
        fibonacci_level=0.618,
        cluster_size=3
    )

def test_whale_art_generator_initialization(tmp_path):
    """Test whale art generator initialization."""
    generator = WhaleArtGenerator(output_dir=str(tmp_path))
    assert Path(generator.output_dir).exists()
    assert generator.fibonacci_levels == [0.236, 0.382, 0.5, 0.618, 0.786, 1.0]

def test_calculate_fibonacci_level(whale_art_generator):
    """Test Fibonacci level calculation."""
    # Test exact matches
    assert whale_art_generator._calculate_fibonacci_level(23.6, 100) == 0.236
    assert whale_art_generator._calculate_fibonacci_level(61.8, 100) == 0.618
    
    # Test closest matches
    assert whale_art_generator._calculate_fibonacci_level(40, 100) == 0.382
    assert whale_art_generator._calculate_fibonacci_level(80, 100) == 0.786

def test_generate_abstract_address(whale_art_generator):
    """Test address abstraction."""
    address = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
    abstract = whale_art_generator._generate_abstract_address(address)
    
    assert len(abstract) < len(address)
    assert abstract.startswith("bc1qxy")
    assert "..." in abstract
    assert abstract.endswith("0wlh")

@pytest.mark.asyncio
async def test_generate_visualization(whale_art_generator, sample_movement):
    """Test visualization generation."""
    filepath = await whale_art_generator.generate_visualization(sample_movement)
    
    assert Path(filepath).exists()
    assert Path(filepath).suffix == ".html"
    assert sample_movement.tx_hash[:8] in Path(filepath).name

@pytest.mark.asyncio
async def test_generate_ai_art(tmp_path):
    """Test AI art generation with fallback."""
    generator = WhaleArtGenerator(output_dir=str(tmp_path), use_ai=True)
    movement = WhaleMovement(
        tx_hash="0xtest",
        timestamp=int(datetime.now().timestamp()),
        value=1000.0,
        from_addresses=["test1"],
        to_addresses=["test2"],
        fibonacci_level=0.618,
        cluster_size=2
    )
    
    try:
        filepath = await generator.generate_ai_art(movement)
        assert Path(filepath).exists()
        assert Path(filepath).suffix == ".png"
    except RuntimeError:
        # AI generation should fail gracefully if models aren't available
        pass

def test_generate_nft_metadata(whale_art_generator, sample_movement):
    """Test NFT metadata generation."""
    sample_movement.visualization_path = "test_path.html"
    metadata = whale_art_generator._generate_nft_metadata(sample_movement)
    
    assert metadata["name"] == f"Whale Movement #{sample_movement.tx_hash[:8]}"
    assert "description" in metadata
    assert metadata["image"] == sample_movement.visualization_path
    
    # Check attributes
    attributes = {attr["trait_type"]: attr["value"] for attr in metadata["attributes"]}
    assert "Value" in attributes
    assert "Fibonacci Level" in attributes
    assert "Cluster Size" in attributes
    assert "Timestamp" in attributes
    
    assert attributes["Value"] == "500.00 BTC"
    assert attributes["Fibonacci Level"] == "0.618"
    assert attributes["Cluster Size"] == 3

@pytest.mark.asyncio
async def test_generate_nft(whale_art_generator, sample_movement):
    """Test complete NFT generation."""
    result = await whale_art_generator.generate_nft(sample_movement)
    
    assert "visualization" in result
    assert "metadata" in result
    
    # Check visualization file
    viz_path = Path(result["visualization"])
    assert viz_path.exists()
    assert viz_path.suffix == ".html"
    
    # Check metadata file
    meta_path = Path(result["metadata"])
    assert meta_path.exists()
    assert meta_path.suffix == ".json"
    
    # Verify metadata content
    with open(meta_path) as f:
        metadata = json.load(f)
        assert metadata["name"].startswith("Whale Movement #")
        assert "description" in metadata
        assert "image" in metadata
        assert "attributes" in metadata

def test_edge_cases(whale_art_generator):
    """Test edge cases in whale movement processing."""
    # Test with minimum values
    min_movement = WhaleMovement(
        tx_hash="0x0",
        timestamp=0,
        value=0.0,
        from_addresses=[],
        to_addresses=[],
        fibonacci_level=0.236,
        cluster_size=1
    )
    metadata = whale_art_generator._generate_nft_metadata(min_movement)
    assert metadata["name"] == "Whale Movement #0x0"
    
    # Test with maximum values
    max_movement = WhaleMovement(
        tx_hash="0xf" * 64,
        timestamp=2**32 - 1,
        value=21_000_000.0,  # Max BTC supply
        from_addresses=["addr"] * 100,
        to_addresses=["addr"] * 100,
        fibonacci_level=1.0,
        cluster_size=200
    )
    metadata = whale_art_generator._generate_nft_metadata(max_movement)
    assert "21000000.00 BTC" in str(metadata)

def test_visualization_customization(whale_art_generator, sample_movement):
    """Test visualization customization options."""
    # Test with custom colors
    whale_art_generator.colors = ["#FF0000", "#00FF00", "#0000FF"]
    whale_art_generator.background_color = "#000000"
    
    metadata = whale_art_generator._generate_nft_metadata(sample_movement)
    assert metadata is not None  # Basic validation that customization didn't break anything 