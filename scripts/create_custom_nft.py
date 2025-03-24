#!/usr/bin/env python3
"""Example script for creating custom NFTs using the OMEGA NFT Creator."""

import asyncio
import argparse
from pathlib import Path
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from omega_ai.blockchain.nft_creator import OMEGANFTCreator, CustomNFTRequest

async def main():
    """Create a custom NFT using either a prompt or an image."""
    parser = argparse.ArgumentParser(description="Create a custom NFT using OMEGA's divine algorithms")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompt", type=str, help="Text prompt for generating the NFT")
    group.add_argument("--image", type=str, help="Path to image file to transform into an NFT")
    parser.add_argument("--name", type=str, help="Name for the NFT")
    parser.add_argument("--description", type=str, help="Description for the NFT")
    parser.add_argument("--output-dir", type=str, default="generated_nfts",
                       help="Directory to store generated NFTs")
    args = parser.parse_args()
    
    # Create NFT creator
    creator = OMEGANFTCreator(output_dir=args.output_dir)
    
    # Create NFT request
    request = CustomNFTRequest(
        prompt=args.prompt,
        image_path=args.image,
        name=args.name,
        description=args.description,
        attributes={
            "Creation Method": "Text-to-Image" if args.prompt else "Image-to-Image",
            "Source": args.prompt if args.prompt else Path(args.image).name
        }
    )
    
    print("Generating NFT...")
    print(f"Method: {'Text-to-Image' if args.prompt else 'Image-to-Image'}")
    if args.prompt:
        print(f"Prompt: {args.prompt}")
    else:
        print(f"Input Image: {args.image}")
    
    # Generate NFT
    result = await creator.create_nft(request)
    
    print("\nNFT Generation Complete!")
    print(f"Image: {result['image']}")
    print(f"Metadata: {result['metadata']}")
    print("\nDivine Metrics:")
    for metric, value in result['divine_metrics'].items():
        print(f"  {metric}: {value:.4f}")
    print(f"\nRarity Score: {result['rarity_score']:.2f}")

if __name__ == "__main__":
    asyncio.run(main())