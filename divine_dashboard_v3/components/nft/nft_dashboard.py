
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

"""
NFT Dashboard for Divine Dashboard v3
"""

import os
import base64
import logging
import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union, List, Tuple, Callable

import gradio as gr
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException

from .nft_generator import NFTGenerator
from .nft_blockchain import NFTBlockchain
from .nft_metadata import NFTMetadata

logger = logging.getLogger(__name__)

class NFTDashboard:
    """NFT Dashboard for Divine Dashboard v3."""
    
    def __init__(self, app: FastAPI, output_dir: str = "nft_output"):
        """Initialize NFT Dashboard.
        
        Args:
            app: FastAPI app to add routes to
            output_dir: Directory for NFT output
        """
        self.app = app
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Initialize components
        self.generator = NFTGenerator(output_dir=str(self.output_dir))
        self.blockchain = NFTBlockchain()
        
        # Register API routes
        self._register_routes()
        
        # Store generated NFTs
        self.generated_nfts = []
        
    def _register_routes(self):
        """Register API routes."""
        # NFT generation endpoint
        @self.app.post("/mint-nft")
        async def mint_nft_endpoint(request: Request):
            try:
                payload = await request.json()
                command = payload.get("command")
                
                if command == "mintNFT":
                    # Get params if available
                    params = payload.get("params", {})
                    image_data = params.get("image_data")
                    name = params.get("name", "Divine NFT")
                    description = params.get("description", "A divinely generated NFT")
                    
                    # If image data is not provided, use a sample image
                    if not image_data:
                        sample_image_path = Path(__file__).parent / "sample_image.png"
                        if not sample_image_path.exists():
                            # Create a simple sample image if it doesn't exist
                            from PIL import Image, ImageDraw
                            img = Image.new('RGB', (512, 512), color='black')
                            draw = ImageDraw.Draw(img)
                            draw.ellipse([100, 100, 400, 400], outline='gold', width=5)
                            img.save(sample_image_path)
                        
                        image_data = str(sample_image_path)
                    
                    # Generate NFT
                    result = await self.mint_nft(image_data, name, description)
                    
                    return result
                
                return {"status": "error", "message": "Unknown command"}
                
            except Exception as e:
                logger.error(f"Error in mint-nft endpoint: {e}")
                return {"status": "error", "message": str(e)}
        
    async def mint_nft(self, 
                       image_data: Union[str, bytes], 
                       name: str = "Divine NFT",
                       description: str = "A divinely generated NFT") -> Dict[str, Any]:
        """Generate and mint NFT.
        
        Args:
            image_data: Image data
            name: NFT name
            description: NFT description
            
        Returns:
            Dictionary with NFT information
        """
        try:
            # Step 1: Generate NFT
            nft_info = await self.generator.generate_nft(
                image_data=image_data,
                name=name,
                description=description
            )
            
            # Step 2: Mint NFT on blockchain
            mint_result = await self.blockchain.mint_nft(
                metadata_path=nft_info["metadata_path"]
            )
            
            # Combine results
            result = {
                "status": "success" if mint_result.get("success", False) else "error",
                "nft_info": nft_info,
                "mint_result": mint_result,
                "timestamp": datetime.now().isoformat()
            }
            
            # Add to generated NFTs
            self.generated_nfts.append(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error minting NFT: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def create_dashboard(self) -> gr.Blocks:
        """Create Gradio dashboard.
        
        Returns:
            Gradio Blocks component
        """
        with gr.Blocks(title="NFT Dashboard") as dashboard:
            gr.Markdown("# 🎨 Divine NFT Generator")
            
            with gr.Tabs():
                with gr.TabItem("Generate NFT"):
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("## Upload Image")
                            upload_image = gr.Image(type="pil", label="Upload Image")
                            nft_name = gr.Textbox(label="NFT Name", placeholder="Enter a name for your NFT")
                            nft_description = gr.Textbox(
                                label="NFT Description", 
                                placeholder="Enter a description for your NFT",
                                lines=3
                            )
                            divine_options = gr.CheckboxGroup(
                                choices=["Sacred Geometry", "Golden Ratio", "Divine Harmony"],
                                label="Divine Options",
                                value=["Divine Harmony"]
                            )
                            generate_button = gr.Button("⚡ Generate & Mint NFT", variant="primary")
                            
                        with gr.Column():
                            result_status = gr.Markdown("### Status: Ready")
                            result_image = gr.Image(label="NFT Preview", interactive=False)
                            with gr.Accordion("NFT Details", open=False):
                                nft_id = gr.Textbox(label="NFT ID")
                                nft_rarity = gr.Textbox(label="Rarity Score")
                                nft_ipfs = gr.Textbox(label="IPFS URL")
                                nft_transaction = gr.Textbox(label="Transaction Hash")
                    
                with gr.TabItem("Recent NFTs"):
                    gr.Markdown("## Recent NFTs")
                    nft_gallery = gr.Gallery(label="Your NFTs", preview=True)
                    refresh_gallery_button = gr.Button("🔄 Refresh Gallery")
                    nft_list_status = gr.Markdown("")
                
                with gr.TabItem("Blockchain Explorer"):
                    gr.Markdown("## Transaction Explorer")
                    tx_hash_input = gr.Textbox(label="Transaction Hash", placeholder="Enter transaction hash")
                    check_tx_button = gr.Button("🔍 Check Transaction")
                    tx_result = gr.JSON(label="Transaction Details")
            
            # Add hidden HTML component for postMessage communication
            message_html = gr.HTML("")
            
            # JavaScript for postMessage communication
            gr.HTML("""
            <script>
            // Listen for messages from parent window
            window.addEventListener('message', function(event) {
                console.log("Received message:", event.data);
                if (event.data && event.data.command === "mintNFT") {
                    // Trigger NFT generation
                    console.log("Triggering NFT mint from postMessage");
                    
                    // Get the generate button and click it
                    document.querySelector('button[aria-label="⚡ Generate & Mint NFT"]').click();
                }
            });
            
            // Function to send results back to parent
            function sendResultsToParent(status, result) {
                if (window.parent && window.parent !== window) {
                    window.parent.postMessage({
                        source: "nft-dashboard",
                        status: status,
                        result: result
                    }, "*");
                    console.log("Sent results to parent:", status, result);
                }
            }
            </script>
            """)
            
            # Define functions for Gradio components
            def on_generate_nft(image, name, description, divine_options):
                """Handle NFT generation button click."""
                if image is None:
                    return (
                        "### Status: ❌ Error - No image provided",
                        None, "", "", "", ""
                    )
                
                try:
                    # Set default name and description if not provided
                    name = name or f"Divine NFT {int(time.time())}"
                    description = description or "A divinely generated NFT"
                    
                    # Create event loop for async call
                    loop = asyncio.get_event_loop()
                    
                    # Run async mint_nft function
                    result = loop.run_until_complete(
                        self.mint_nft(image, name, description)
                    )
                    
                    if result.get("status") == "success":
                        nft_info = result.get("nft_info", {})
                        mint_result = result.get("mint_result", {})
                        
                        # Generate JavaScript to send results to parent window
                        js_code = f"""
                        sendResultsToParent("success", {json.dumps(result)});
                        """
                        
                        # Return UI updates
                        return (
                            f"### Status: ✅ Success - NFT Generated & Minted",
                            image,
                            nft_info.get("id", ""),
                            f"{nft_info.get('rarity_score', 0):.2f}",
                            mint_result.get("metadata_url", "Not available"),
                            mint_result.get("transaction_hash", "Not available"),
                            f"<script>{js_code}</script>"
                        )
                    else:
                        error_msg = result.get("message", "Unknown error")
                        return (
                            f"### Status: ❌ Error - {error_msg}",
                            None, "", "", "", "",
                            "<script>sendResultsToParent('error', {});</script>"
                        )
                
                except Exception as e:
                    logger.error(f"Error in generate_nft: {e}")
                    return (
                        f"### Status: ❌ Error - {str(e)}",
                        None, "", "", "", "",
                        "<script>sendResultsToParent('error', {});</script>"
                    )
            
            def on_refresh_gallery():
                """Handle gallery refresh button click."""
                try:
                    if not self.generated_nfts:
                        return [], "No NFTs generated yet."
                    
                    # Get image paths from generated NFTs
                    image_paths = []
                    for nft in self.generated_nfts:
                        nft_info = nft.get("nft_info", {})
                        image_path = nft_info.get("image_path")
                        if image_path:
                            image_paths.append(image_path)
                    
                    return image_paths, f"Found {len(image_paths)} NFTs."
                
                except Exception as e:
                    logger.error(f"Error refreshing gallery: {e}")
                    return [], f"Error refreshing gallery: {str(e)}"
            
            def on_check_transaction(tx_hash):
                """Handle transaction check button click."""
                if not tx_hash:
                    return {"error": "No transaction hash provided"}
                
                try:
                    # Create event loop for async call
                    loop = asyncio.get_event_loop()
                    
                    # Run async check_transaction function
                    result = loop.run_until_complete(
                        self.blockchain.check_transaction(tx_hash)
                    )
                    
                    return result
                
                except Exception as e:
                    logger.error(f"Error checking transaction: {e}")
                    return {"error": str(e)}
            
            # Connect functions to components
            generate_button.click(
                on_generate_nft,
                inputs=[upload_image, nft_name, nft_description, divine_options],
                outputs=[result_status, result_image, nft_id, nft_rarity, nft_ipfs, nft_transaction, message_html]
            )
            
            refresh_gallery_button.click(
                on_refresh_gallery,
                inputs=[],
                outputs=[nft_gallery, nft_list_status]
            )
            
            check_tx_button.click(
                on_check_transaction,
                inputs=[tx_hash_input],
                outputs=[tx_result]
            )
            
        return dashboard

def create_nft_dashboard(app: FastAPI, output_dir: str = "nft_output") -> Tuple[NFTDashboard, gr.Blocks]:
    """Create NFT dashboard.
    
    Args:
        app: FastAPI app
        output_dir: Output directory
        
    Returns:
        Tuple of (NFTDashboard, Gradio Blocks)
    """
    nft_dashboard = NFTDashboard(app, output_dir)
    gr_dashboard = nft_dashboard.create_dashboard()
    return nft_dashboard, gr_dashboard 