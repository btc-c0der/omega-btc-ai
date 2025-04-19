from components.nft.nft_dashboard import create_nft_dashboard
from fastapi import FastAPI
import os

# Create NFT dashboard
nft_app = FastAPI(title="Divine NFT Dashboard")
nft_output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nft_output")
os.makedirs(nft_output_dir, exist_ok=True)
nft_dashboard, nft_interface = create_nft_dashboard(nft_app, nft_output_dir)

# Launch the interface
if __name__ == "__main__":
    nft_interface.launch()
