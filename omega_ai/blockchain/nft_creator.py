
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

"""OMEGA NFT Creator Module for custom NFT generation."""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union
import hashlib
import json
from PIL import Image
import torch
from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion import StableDiffusionPipeline
from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion_img2img import StableDiffusionImg2ImgPipeline
from .omega_nft import OMEGANFTMetadata

@dataclass
class CustomNFTRequest:
    """Data class for custom NFT generation requests."""
    prompt: Optional[str] = None
    image_path: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    divine_metrics: Optional[Dict[str, float]] = None
    
    def __post_init__(self):
        """Validate NFT request data."""
        if not self.prompt and not self.image_path:
            raise ValueError("Either prompt or image_path must be provided")
        if self.image_path and not Path(self.image_path).exists():
            raise ValueError(f"Image file not found: {self.image_path}")
        self.attributes = self.attributes or {}
        self.divine_metrics = self.divine_metrics or {}

class OMEGANFTCreator:
    """Custom NFT creator using OMEGA's divine algorithms."""
    
    def __init__(self, output_dir: str = "generated_nfts"):
        """Initialize the NFT creator.
        
        Args:
            output_dir: Directory to store generated NFTs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create nft_output directory
        self.nft_output_dir = self.output_dir / "nft_output"
        self.nft_output_dir.mkdir(exist_ok=True)
        
        # Create visualizations directory inside nft_output
        self.visualizations_dir = self.nft_output_dir / "visualizations"
        self.visualizations_dir.mkdir(exist_ok=True)
        
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize AI models for generation and transformation."""
        try:
            # Initialize text-to-image model
            self.txt2img_model = StableDiffusionPipeline.from_pretrained(
                "stabilityai/stable-diffusion-2-1",
                torch_dtype=torch.float16
            )
            
            # Initialize image-to-image model
            self.img2img_model = StableDiffusionImg2ImgPipeline.from_pretrained(
                "stabilityai/stable-diffusion-2-1",
                torch_dtype=torch.float16
            )
            
            # Move to appropriate device
            if torch.cuda.is_available():
                device = "cuda"
                print("Using CUDA for GPU acceleration")
            elif torch.backends.mps.is_available():
                device = "mps"
                print("Using MPS (Metal Performance Shaders) for GPU acceleration")
            else:
                device = "cpu"
                print("Warning: No GPU acceleration available, using CPU")
                
            self.txt2img_model = self.txt2img_model.to(device)
            self.img2img_model = self.img2img_model.to(device)
                
        except Exception as e:
            print(f"Warning: Could not initialize AI models: {e}")
            self.txt2img_model = None
            self.img2img_model = None

    def _calculate_divine_metrics(self, image: Image.Image) -> Dict[str, float]:
        """Calculate divine metrics from the image.
        
        Args:
            image: PIL Image to analyze
            
        Returns:
            Dictionary of divine metrics
        """
        # Convert image to numpy array for analysis
        img_array = torch.tensor(list(image.getdata())).float()
        
        # Calculate divine metrics
        metrics = {
            "divine_harmony": float(torch.mean(img_array).item() / 255.0),
            "sacred_balance": float(torch.std(img_array).item() / 255.0),
            "golden_ratio_alignment": 0.618,  # Default to golden ratio
            "cosmic_resonance": float(torch.median(img_array).item() / 255.0),
            "ethereal_vibrance": float(torch.max(img_array).item() / 255.0)
        }
        
        return metrics

    def _enhance_prompt(self, prompt: str) -> str:
        """Enhance the user's prompt with divine elements.
        
        Args:
            prompt: Original prompt
            
        Returns:
            Enhanced prompt with divine elements
        """
        divine_elements = [
            "sacred geometry patterns",
            "golden ratio proportions",
            "ethereal lighting",
            "cosmic energy flows",
            "divine symmetry"
        ]
        
        enhanced = prompt + ", " + ", ".join(divine_elements)
        enhanced += ", highly detailed, professional digital art, trending on artstation"
        
        return enhanced

    async def _generate_from_prompt(self, prompt: str) -> str:
        """Generate image from text prompt.
        
        Args:
            prompt: Text prompt for image generation
            
        Returns:
            Path to generated image
        """
        if not self.txt2img_model:
            raise RuntimeError("Text-to-image model not available")
            
        # Enhance prompt with divine elements
        enhanced_prompt = self._enhance_prompt(prompt)
        
        # Generate image
        with torch.no_grad():
            output = self.txt2img_model(
                prompt=enhanced_prompt,
                num_inference_steps=50,
                guidance_scale=7.5,
            )
            image = output.images[0]
            
        # Save image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nft_prompt_{timestamp}.png"
        filepath = self.visualizations_dir / filename
        image.save(filepath)
        
        return str(filepath)

    async def _generate_from_image(self, image_path: str, strength: float = 0.75) -> str:
        """Generate new image from existing image.
        
        Args:
            image_path: Path to input image
            strength: Transformation strength (0-1)
            
        Returns:
            Path to generated image
        """
        if not self.img2img_model:
            raise RuntimeError("Image-to-image model not available")
            
        # Load and preprocess image
        init_image = Image.open(image_path).convert("RGB")
        init_image = init_image.resize((768, 768))
        
        # Generate divine prompt based on image
        prompt = "A divine transformation with sacred geometry, golden ratio patterns, and ethereal energy"
        
        # Generate image
        with torch.no_grad():
            output = self.img2img_model(
                prompt=prompt,
                image=init_image,
                strength=strength,
                guidance_scale=7.5,
                num_inference_steps=50
            )
            image = output.images[0]
            
        # Save image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nft_image_{timestamp}.png"
        filepath = self.visualizations_dir / filename
        image.save(filepath)
        
        return str(filepath)

    def _generate_metadata(
        self,
        request: CustomNFTRequest,
        image_path: str,
        divine_metrics: Dict[str, float]
    ) -> OMEGANFTMetadata:
        """Generate NFT metadata.
        
        Args:
            request: NFT generation request
            image_path: Path to generated image
            divine_metrics: Calculated divine metrics
            
        Returns:
            NFT metadata
        """
        # Generate unique identifier
        unique_id = hashlib.sha256(
            f"{datetime.now().isoformat()}-{image_path}".encode()
        ).hexdigest()[:8]
        
        # Create metadata
        return OMEGANFTMetadata(
            name=request.name or f"OMEGA Divine NFT #{unique_id}",
            description=request.description or "A divinely generated NFT using OMEGA's sacred algorithms",
            image=image_path,
            attributes=[
                {"trait_type": k, "value": v}
                for k, v in (request.attributes or {}).items()
            ],
            divine_metrics=divine_metrics,
            rarity_score=sum(divine_metrics.values()) / len(divine_metrics) * 100,
            created_at=datetime.now().isoformat()
        )

    async def create_nft(self, request: CustomNFTRequest) -> Dict[str, Any]:
        """Create an NFT from prompt or image.
        
        Args:
            request: NFT generation request
            
        Returns:
            Dictionary containing NFT data
        """
        # Generate image
        if request.prompt:
            image_path = await self._generate_from_prompt(request.prompt)
        elif request.image_path:
            image_path = await self._generate_from_image(request.image_path)
        else:
            raise ValueError("Either prompt or image_path must be provided")
            
        # Calculate divine metrics
        image = Image.open(image_path)
        divine_metrics = self._calculate_divine_metrics(image)
        divine_metrics.update(request.divine_metrics or {})
        
        # Generate metadata
        metadata = self._generate_metadata(request, image_path, divine_metrics)
        
        # Save metadata
        metadata_path = self.nft_output_dir / f"nft_{Path(image_path).stem}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata.to_dict(), f, indent=2)
            
        return {
            "image": image_path,
            "metadata": str(metadata_path),
            "divine_metrics": divine_metrics,
            "rarity_score": metadata.rarity_score
        } 