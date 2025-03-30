"""Integration tests for the OMEGA NFT system."""

import pytest
from pathlib import Path
import json
from datetime import datetime
import asyncio
from omega_ai.blockchain.nft_creator import OMEGANFTCreator, CustomNFTRequest
from omega_ai.blockchain.whale_art import WhaleArtGenerator, WhaleMovement
from omega_ai.blockchain.omega_nft import OMEGANFTGenerator

@pytest.fixture
def output_dir(tmp_path):
    """Create a temporary output directory."""
    return tmp_path / "nft_output"

@pytest.fixture
def nft_creator(output_dir):
    """Create NFT creator instance."""
    return OMEGANFTCreator(output_dir=str(output_dir))

@pytest.fixture
def whale_art_generator(output_dir):
    """Create whale art generator instance."""
    return WhaleArtGenerator(output_dir=str(output_dir))

@pytest.fixture
def nft_generator(output_dir):
    """Create NFT generator instance."""
    return OMEGANFTGenerator(output_dir=str(output_dir))

@pytest.mark.asyncio
async def test_whale_movement_to_nft_flow(whale_art_generator, nft_generator):
    """Test complete flow from whale movement to NFT."""
    # Create whale movement
    movement = WhaleMovement(
        tx_hash="0xdivinetest",
        timestamp=int(datetime.now().timestamp()),
        value=1000.0,
        from_addresses=["divine1"],
        to_addresses=["divine2"],
        fibonacci_level=0.618,
        cluster_size=2
    )
    
    # Generate whale art
    art_result = await whale_art_generator.generate_nft(movement)
    assert "visualization" in art_result
    assert "metadata" in art_result
    
    # Generate NFT from whale art
    nft_result = await nft_generator.generate_nft(movement)
    assert "metadata" in nft_result
    assert "visualization" in nft_result
    assert "rarity_score" in nft_result
    assert "divine_metrics" in nft_result

@pytest.mark.asyncio
async def test_custom_nft_to_whale_art(nft_creator, whale_art_generator):
    """Test integration between custom NFT and whale art."""
    # Create custom NFT
    request = CustomNFTRequest(
        prompt="A divine whale movement visualization",
        name="Divine Whale",
        description="Sacred visualization of whale movement",
        attributes={"Type": "Divine", "Category": "Whale"}
    )
    
    nft_result = await nft_creator.create_nft(request)
    assert "image" in nft_result
    
    # Use NFT image for whale art
    movement = WhaleMovement(
        tx_hash="0xintegration",
        timestamp=int(datetime.now().timestamp()),
        value=500.0,
        from_addresses=["test1"],
        to_addresses=["test2"],
        fibonacci_level=0.618,
        cluster_size=2,
        visualization_path=nft_result["image"]
    )
    
    art_result = await whale_art_generator.generate_nft(movement)
    assert "visualization" in art_result
    assert "metadata" in art_result

@pytest.mark.asyncio
async def test_nft_collection_integration(nft_generator):
    """Test NFT collection generation with multiple components."""
    # Create multiple movements
    movements = [
        WhaleMovement(
            tx_hash=f"0xdivine{i}",
            timestamp=int(datetime.now().timestamp()) + i,
            value=100.0 * (i + 1),
            from_addresses=[f"from{i}"],
            to_addresses=[f"to{i}"],
            fibonacci_level=0.618,
            cluster_size=2
        )
        for i in range(3)
    ]
    
    # Generate collection
    collection = await nft_generator.generate_collection(movements)
    
    assert "collection_metadata" in collection
    assert "statistics" in collection
    assert "nfts" in collection
    assert len(collection["nfts"]) == 3
    
    # Verify collection metadata
    with open(collection["collection_metadata"]) as f:
        metadata = json.load(f)
        assert metadata["total_supply"] == 3
        assert len(metadata["nfts"]) == 3

@pytest.mark.asyncio
async def test_divine_metrics_consistency(nft_creator, nft_generator, whale_art_generator):
    """Test consistency of divine metrics across components."""
    # Create NFT with custom divine metrics
    request = CustomNFTRequest(
        prompt="Divine whale movement",
        divine_metrics={
            "sacred_resonance": 0.9,
            "divine_harmony": 0.8
        }
    )
    
    nft_result = await nft_creator.create_nft(request)
    initial_metrics = nft_result["divine_metrics"]
    
    # Create whale movement with same metrics
    movement = WhaleMovement(
        tx_hash="0xmetrics",
        timestamp=int(datetime.now().timestamp()),
        value=1000.0,
        from_addresses=["divine1"],
        to_addresses=["divine2"],
        fibonacci_level=0.618,
        cluster_size=2
    )
    
    # Generate NFT and verify metrics consistency
    nft_data = await nft_generator.generate_nft(movement)
    whale_metrics = nft_data["divine_metrics"]
    
    # Verify core divine metrics are present in both
    common_metrics = set(initial_metrics.keys()) & set(whale_metrics.keys())
    assert len(common_metrics) > 0
    
    # Verify metrics are within expected ranges
    for metric in whale_metrics:
        assert 0 <= whale_metrics[metric] <= 1 or metric in ["fibonacci_level", "rarity_score"]

@pytest.mark.asyncio
async def test_concurrent_nft_generation(nft_generator):
    """Test concurrent NFT generation."""
    # Create multiple movements
    movements = [
        WhaleMovement(
            tx_hash=f"0xconcurrent{i}",
            timestamp=int(datetime.now().timestamp()) + i,
            value=100.0 * (i + 1),
            from_addresses=[f"from{i}"],
            to_addresses=[f"to{i}"],
            fibonacci_level=0.618,
            cluster_size=2
        )
        for i in range(5)
    ]
    
    # Generate NFTs concurrently
    tasks = [nft_generator.generate_nft(movement) for movement in movements]
    results = await asyncio.gather(*tasks)
    
    assert len(results) == 5
    for result in results:
        assert "metadata" in result
        assert "visualization" in result
        assert "divine_metrics" in result

def test_error_handling_integration(nft_creator, whale_art_generator, nft_generator, tmp_path):
    """Test error handling across components."""
    # Test with invalid directory
    with pytest.raises(Exception):
        OMEGANFTCreator(output_dir="/nonexistent/path")
    
    # Test with invalid movement data
    with pytest.raises(Exception):
        WhaleMovement(
            tx_hash="",  # Invalid empty hash
            timestamp=-1,  # Invalid negative timestamp
            value=-100.0,  # Invalid negative value
            from_addresses=[],
            to_addresses=[],
            fibonacci_level=2.0,  # Invalid Fibonacci level
            cluster_size=0  # Invalid cluster size
        )
    
    # Test with invalid NFT request
    with pytest.raises(ValueError):
        CustomNFTRequest()  # Missing required fields 