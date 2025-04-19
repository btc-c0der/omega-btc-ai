
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

"""Test cases for the Sacred Punk Generator module."""

import pytest
from pathlib import Path
from PIL import Image
from omega_ai.blockchain.sacred_punk_generator import SacredPunkGenerator
from omega_ai.blockchain.sacred_punk_traits import SacredPunkTraits

# Use the sacred NFT archive for tests
SACRED_NFT_PATH = Path("BOOK/divine_chronicles/nft_archive")

@pytest.fixture
def sacred_punk_generator():
    """Create a Sacred Punk generator instance."""
    output_dir = SACRED_NFT_PATH / "sacred_punks"
    output_dir.mkdir(parents=True, exist_ok=True)
    return SacredPunkGenerator(output_dir)

def test_sacred_punk_generation(sacred_punk_generator):
    """Test generating a Sacred Punk NFT."""
    # Generate with fixed seed for reproducibility
    result = sacred_punk_generator.generate_sacred_punk(seed=42)
    
    # Verify image was created
    assert Path(result["image"]).exists()
    
    # Load and verify image
    img = Image.open(result["image"])
    assert img.size == (512, 512)
    assert img.mode == "RGB"
    
    # Verify metadata
    metadata = result["metadata"]
    assert metadata["name"].startswith("Sacred Punk #")
    assert "divine_metrics" in metadata
    assert 0 <= metadata["divine_metrics"]["rarity"] <= 1
    assert 0 <= metadata["divine_metrics"]["resonance"] <= 1
    assert metadata["divine_metrics"]["trait_count"] > 0
    
    # Verify attributes
    assert len(metadata["attributes"]) > 0
    for attr in metadata["attributes"]:
        assert "trait_type" in attr
        assert "value" in attr
        assert "description" in attr
        assert "sacred_pattern" in attr
        assert attr["sacred_pattern"] in SacredPunkTraits.SACRED_PATTERNS.values()

def test_sacred_patterns(sacred_punk_generator):
    """Test all sacred geometry patterns."""
    base_img = sacred_punk_generator._create_base_image()
    
    for pattern in SacredPunkTraits.SACRED_PATTERNS:
        # Add each pattern to a fresh base image
        img = sacred_punk_generator._add_sacred_pattern(base_img.copy(), pattern)
        assert isinstance(img, Image.Image)
        
        # Save pattern for visual inspection
        pattern_path = SACRED_NFT_PATH / "sacred_punks" / f"test_pattern_{pattern}.png"
        img.save(pattern_path)
        assert pattern_path.exists()

def test_trait_selection(sacred_punk_generator):
    """Test trait selection and rarity calculation."""
    # Generate multiple punks to test trait distribution
    results = [
        sacred_punk_generator.generate_sacred_punk(seed=i)
        for i in range(5)
    ]
    
    # Verify trait categories
    all_categories = set()
    for result in results:
        for attr in result["metadata"]["attributes"]:
            all_categories.add(attr["trait_type"])
    
    expected_categories = {
        "headwear", "eyes", "mouth", "accessories"
    }
    assert all_categories.intersection(expected_categories)
    
    # Verify divine metrics
    for result in results:
        metrics = result["metadata"]["divine_metrics"]
        assert 0 <= metrics["rarity"] <= 1
        assert 0 <= metrics["resonance"] <= 1
        assert metrics["trait_count"] > 0

def test_reproducibility(sacred_punk_generator):
    """Test that the same seed produces the same punk."""
    seed = 42
    result1 = sacred_punk_generator.generate_sacred_punk(seed=seed)
    result2 = sacred_punk_generator.generate_sacred_punk(seed=seed)
    
    # Compare metadata (excluding image paths which contain timestamps)
    metadata1 = result1["metadata"].copy()
    metadata2 = result2["metadata"].copy()
    
    # Remove variable parts
    del metadata1["image"]
    del metadata2["image"]
    del metadata1["name"]
    del metadata2["name"]
    
    assert metadata1 == metadata2 