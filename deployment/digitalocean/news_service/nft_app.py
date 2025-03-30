"""NFT Service Flask Application."""

from flask import Flask, jsonify, request
from pathlib import Path
from omega_ai.blockchain.sacred_punk_generator import SacredPunkGenerator
from omega_ai.blockchain.nft_creator import CustomNFTRequest, OMEGANFTCreator

app = Flask(__name__)

# Initialize NFT generators
NFT_ARCHIVE = Path("nft_archive")
sacred_punk_generator = SacredPunkGenerator(NFT_ARCHIVE / "sacred_punks")
nft_creator = OMEGANFTCreator(NFT_ARCHIVE / "divine_nfts")

@app.route("/api/nft/sacred-punk", methods=["POST"])
async def generate_sacred_punk():
    """Generate a Sacred Punk NFT."""
    data = request.get_json()
    seed = data.get("seed")
    
    try:
        result = sacred_punk_generator.generate_sacred_punk(seed=seed)
        return jsonify({
            "success": True,
            "image": result["image"],
            "metadata": result["metadata"]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/api/nft/divine", methods=["POST"])
async def create_divine_nft():
    """Create a divine NFT."""
    data = request.get_json()
    
    try:
        nft_request = CustomNFTRequest(
            prompt=data.get("prompt"),
            image_path=data.get("image_path"),
            name=data.get("name"),
            attributes=data.get("attributes", {}),
            divine_metrics=data.get("divine_metrics", {})
        )
        
        result = await nft_creator.create_nft(nft_request)
        return jsonify({
            "success": True,
            "image": result["image"],
            "metadata": result["metadata"]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/api/nft/metrics", methods=["GET"])
def get_nft_metrics():
    """Get NFT metrics."""
    try:
        sacred_punks_dir = NFT_ARCHIVE / "sacred_punks"
        divine_nfts_dir = NFT_ARCHIVE / "divine_nfts"
        
        return jsonify({
            "success": True,
            "metrics": {
                "sacred_punks_count": len(list(sacred_punks_dir.glob("*.png"))),
                "divine_nfts_count": len(list(divine_nfts_dir.glob("*.png"))),
                "total_nfts": len(list(sacred_punks_dir.glob("*.png"))) + len(list(divine_nfts_dir.glob("*.png")))
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000) 