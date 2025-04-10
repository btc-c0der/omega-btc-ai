
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

import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys
from os.path import dirname, abspath

# Add the project root directory to Python path
project_root = dirname(dirname(abspath(__file__)))
sys.path.insert(0, project_root)

from omega_ai.blockchain.omega_nft import OMEGANFTGenerator
from omega_ai.blockchain.whale_art import WhaleMovement

async def generate_whale_nft():
    """Generate an NFT from a real whale movement."""
    
    # Create output directory if it doesn't exist
    output_dir = Path("generated_nfts")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize NFT generator
    nft_generator = OMEGANFTGenerator(output_dir=str(output_dir))
    
    # Create a whale movement with real data
    # This is a significant whale movement from March 2024
    movement = WhaleMovement(
        tx_hash="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        timestamp=int(datetime(2024, 3, 24, 12, 0, 0).timestamp()),
        value=150.5,  # 150.5 BTC
        from_addresses=["bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"],
        to_addresses=["bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"],
        fibonacci_level=0.618,  # Golden ratio level
        cluster_size=2
    )
    
    print("Generating NFT for whale movement...")
    print(f"Transaction Hash: {movement.tx_hash}")
    print(f"Value: {movement.value} BTC")
    print(f"Timestamp: {datetime.fromtimestamp(movement.timestamp)}")
    
    # Generate the NFT
    nft_data = await nft_generator.generate_nft(movement)
    
    # Print NFT details
    print("\nNFT Generation Complete!")
    print(f"Metadata file: {nft_data['metadata']}")
    print(f"Visualization file: {nft_data['visualization']}")
    print(f"Rarity Score: {nft_data['rarity_score']}")
    
    # Print divine metrics
    print("\nDivine Metrics:")
    for metric, value in nft_data['divine_metrics'].items():
        print(f"{metric}: {value:.4f}")
    
    # Load and print metadata
    with open(nft_data['metadata']) as f:
        metadata = json.load(f)
        print("\nNFT Metadata:")
        print(json.dumps(metadata, indent=2))

if __name__ == "__main__":
    asyncio.run(generate_whale_nft()) 