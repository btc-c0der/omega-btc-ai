
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

"""Test cases for the OMEGA NFT Creator module."""

import pytest
import torch
import asyncio
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
from datetime import datetime
import math
from omega_ai.blockchain.nft_creator import OMEGANFTCreator, CustomNFTRequest

# Sacred NFT archive path
SACRED_NFT_PATH = Path("BOOK/divine_chronicles/nft_archive")

def create_sacred_geometry(size=(512, 512), pattern_type="flower_of_life"):
    """Create a sacred geometry pattern.
    
    Args:
        size: Image size (width, height)
        pattern_type: Type of sacred geometry pattern
        
    Returns:
        PIL Image with sacred geometry pattern
    """
    img = Image.new('RGB', size, color='black')
    draw = ImageDraw.Draw(img)
    
    # Golden ratio
    phi = (1 + math.sqrt(5)) / 2
    center = (size[0] // 2, size[1] // 2)
    radius = min(size) // 4
    
    if pattern_type == "flower_of_life":
        # Draw Flower of Life pattern
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            x = center[0] + radius * math.cos(rad)
            y = center[1] + radius * math.sin(rad)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], outline='gold', width=2)
        
        # Add central circle
        draw.ellipse([center[0]-radius, center[1]-radius, 
                     center[0]+radius, center[1]+radius], outline='gold', width=2)
        
        # Add divine spiral based on golden ratio
        points = []
        for t in range(0, 360, 5):
            rad = math.radians(t)
            r = radius * math.exp(0.2 * rad / phi)
            x = center[0] + r * math.cos(rad)
            y = center[1] + r * math.sin(rad)
            points.append((x, y))
        
        # Draw spiral
        if len(points) > 1:
            draw.line(points, fill='white', width=2)
            
    return img

@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    # Create sacred geometry test image
    img = create_sacred_geometry()
    
    # Save the image
    test_image_path = SACRED_NFT_PATH / "test_image.png"
    img.save(test_image_path)
    
    return str(test_image_path)

@pytest.fixture
def nft_creator():
    """Create an NFT creator with sacred output directory."""
    # Create directory structure step by step
    SACRED_NFT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SACRED_NFT_PATH.mkdir(exist_ok=True)
    (SACRED_NFT_PATH / "nft_output").mkdir(exist_ok=True)
    (SACRED_NFT_PATH / "nft_output/visualizations").mkdir(exist_ok=True)
    return OMEGANFTCreator(output_dir=str(SACRED_NFT_PATH))

def test_nft_creator_initialization():
    """Test NFT creator initialization and directory creation."""
    creator = OMEGANFTCreator(output_dir=str(SACRED_NFT_PATH))
    assert Path(creator.output_dir).exists()
    assert Path(creator.visualizations_dir).exists()

def test_custom_nft_request_validation_edge_cases():
    """Test validation of NFT request edge cases."""
    # Test empty request
    with pytest.raises(ValueError):
        CustomNFTRequest()
    
    # Test non-existent image path
    with pytest.raises(ValueError):
        CustomNFTRequest(image_path="nonexistent.png")
    
    # Test valid prompt
    request = CustomNFTRequest(prompt="Test prompt")
    assert request.prompt == "Test prompt"
    assert request.attributes == {}
    assert request.divine_metrics == {}

def test_calculate_divine_metrics(nft_creator, sample_image):
    """Test divine metrics calculation."""
    image = Image.open(sample_image)
    metrics = nft_creator._calculate_divine_metrics(image)
    
    assert isinstance(metrics, dict)
    assert all(0 <= v <= 1 for v in metrics.values())
    assert "divine_harmony" in metrics
    assert "sacred_balance" in metrics
    assert "golden_ratio_alignment" in metrics
    assert "cosmic_resonance" in metrics
    assert "ethereal_vibrance" in metrics

def test_enhance_prompt(nft_creator):
    """Test prompt enhancement with divine elements."""
    original = "A test prompt"
    enhanced = nft_creator._enhance_prompt(original)
    
    assert original in enhanced
    assert "sacred geometry" in enhanced.lower()
    assert "golden ratio" in enhanced.lower()
    assert "divine" in enhanced.lower() or "sacred" in enhanced.lower()

def test_model_fallback(nft_creator):
    """Test graceful fallback when models fail to initialize."""
    nft_creator.txt2img_model = None
    nft_creator.img2img_model = None
    
    with pytest.raises(RuntimeError):
        asyncio.run(nft_creator._generate_from_prompt("test"))
    
    with pytest.raises(RuntimeError):
        asyncio.run(nft_creator._generate_from_image("test.png"))

def test_model_initialization():
    """Test model initialization with MPS support."""
    creator = OMEGANFTCreator(output_dir=str(SACRED_NFT_PATH))
    
    # Check if models were initialized
    assert creator.txt2img_model is not None
    assert creator.img2img_model is not None
    
    # Check if models are on the correct device
    if torch.backends.mps.is_available():
        assert "mps" in str(creator.txt2img_model.device)
        assert "mps" in str(creator.img2img_model.device)
        print("Models successfully initialized on MPS device")
    elif torch.cuda.is_available():
        assert "cuda" in str(creator.txt2img_model.device)
        assert "cuda" in str(creator.img2img_model.device)
        print("Models successfully initialized on CUDA device")
    else:
        assert "cpu" in str(creator.txt2img_model.device)
        assert "cpu" in str(creator.img2img_model.device)
        print("Models successfully initialized on CPU")

@pytest.mark.asyncio
async def test_generate_from_prompt(nft_creator):
    """Test NFT generation from text prompt."""
    if not (torch.cuda.is_available() or torch.backends.mps.is_available()):
        pytest.skip("Skipping test_generate_from_prompt as no GPU acceleration is available")

    prompt = "A divine whale swimming through cosmic energy"
    image_path = await nft_creator._generate_from_prompt(prompt)

    assert Path(image_path).exists()
    assert Path(image_path).suffix == ".png"
    assert "nft_prompt_" in Path(image_path).name

@pytest.mark.asyncio
async def test_generate_from_image(nft_creator, sample_image):
    """Test NFT generation from existing image."""
    if not (torch.cuda.is_available() or torch.backends.mps.is_available()):
        pytest.skip("Skipping test_generate_from_image as no GPU acceleration is available")

    image_path = await nft_creator._generate_from_image(sample_image)

    assert Path(image_path).exists()
    assert Path(image_path).suffix == ".png"
    assert "nft_image_" in Path(image_path).name

@pytest.mark.asyncio
async def test_create_nft_from_prompt(nft_creator):
    """Test complete NFT creation from prompt."""
    if not (torch.cuda.is_available() or torch.backends.mps.is_available()):
        pytest.skip("Skipping test_create_nft_from_prompt as no GPU acceleration is available")

    request = CustomNFTRequest(
        prompt="A divine whale in cosmic ocean",
        name="Divine Whale",
        description="A sacred NFT of a divine whale",
        attributes={"Divinity": "Cosmic", "Element": "Water"},
        divine_metrics={"sacred_resonance": 0.9}
    )

    result = await nft_creator.create_nft(request)

    assert "image" in result
    assert "metadata" in result
    assert "divine_metrics" in result
    assert "rarity_score" in result

    assert Path(result["image"]).exists()
    assert Path(result["metadata"]).exists()

    # Verify divine metrics
    assert result["divine_metrics"]["sacred_resonance"] == 0.9
    assert len(result["divine_metrics"]) > 1

@pytest.mark.asyncio
async def test_create_nft_from_image(nft_creator, sample_image):
    """Test complete NFT creation from image."""
    if not (torch.cuda.is_available() or torch.backends.mps.is_available()):
        pytest.skip("Skipping test_create_nft_from_image as no GPU acceleration is available")

    request = CustomNFTRequest(
        image_path=sample_image,
        name="Sacred Image",
        description="A divinely transformed image",
        attributes={"Origin": "Divine", "Type": "Transformed"}
    )

    result = await nft_creator.create_nft(request)

    assert "image" in result
    assert "metadata" in result
    assert "divine_metrics" in result
    assert "rarity_score" in result

    assert Path(result["image"]).exists()
    assert Path(result["metadata"]).exists()

def test_divine_metrics_calculation_edge_cases(nft_creator):
    """Test divine metrics calculation with edge case images."""
    # Test with black image
    black_img = Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8))
    black_metrics = nft_creator._calculate_divine_metrics(black_img)
    assert black_metrics["divine_harmony"] == 0
    assert black_metrics["ethereal_vibrance"] == 0

    # Test with white image
    white_img = Image.fromarray(np.ones((100, 100, 3), dtype=np.uint8) * 255)
    white_metrics = nft_creator._calculate_divine_metrics(white_img)
    assert white_metrics["divine_harmony"] == 1
    assert white_metrics["ethereal_vibrance"] == 1

    # Test with gradient image
    gradient = np.linspace(0, 255, 100, dtype=np.uint8)
    gradient = np.stack([gradient] * 3, axis=-1)  # Create RGB gradient
    gradient_img = Image.fromarray(np.tile(gradient, (100, 1, 1)))  # Repeat vertically
    gradient_metrics = nft_creator._calculate_divine_metrics(gradient_img)
    assert 0 < gradient_metrics["divine_harmony"] < 1
    assert 0 < gradient_metrics["sacred_balance"] < 1 