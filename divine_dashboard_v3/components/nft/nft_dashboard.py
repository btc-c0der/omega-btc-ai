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
import uuid

import gradio as gr
from fastapi import FastAPI, Request, File, UploadFile, Form, HTTPException

from .nft_generator import NFTGenerator
from .nft_blockchain import NFTBlockchain
from .nft_metadata import NFTMetadata

import sys

# Add parent directory to path to import redis_helper
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.redis_helper import (
    get_redis_client,
    set_json,
    get_json,
    log_event,
    record_metric,
    get_namespaced_key,
    push_to_list,
    get_list
)

# Redis integration flag
USE_REDIS = True

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
        with gr.Blocks(title="Divine NFT Dashboard") as dashboard:
            gr.Markdown(
                """
                # 🎨 Divine NFT Dashboard
                
                Create, mint, and manage divine NFTs with quantum-enhanced algorithms.
                
                This dashboard allows you to generate unique artworks infused with quantum entropy
                and mint them as NFTs on the blockchain.
                """
            )
            
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
                
                with gr.TabItem("NFT Gallery"):
                    gr.Markdown("## Recent NFTs")
                    nft_gallery = gr.Gallery(label="Your NFTs", preview=True)
                    refresh_gallery_button = gr.Button("🔄 Refresh Gallery")
                    nft_list_status = gr.Markdown("")
                
                with gr.TabItem("Blockchain Explorer"):
                    gr.Markdown("## Transaction Explorer")
                    tx_hash_input = gr.Textbox(label="Transaction Hash", placeholder="Enter transaction hash")
                    check_tx_button = gr.Button("🔍 Check Transaction")
                    tx_result = gr.JSON(label="Transaction Details")
                
                # Add a new tab for historical NFTs
                with gr.TabItem("Historical NFTs"):
                    with gr.Row():
                        refresh_btn = gr.Button("🔄 Refresh History")
                        history_status = gr.Markdown("*Loading NFT history...*")
                    
                    with gr.Row():
                        history_container = gr.HTML("")
                    
                    def format_nft_history(nft_history):
                        """Format NFT history as HTML"""
                        if not nft_history:
                            return "<div class='history-empty'>No NFT history found</div>"
                        
                        html = "<div class='nft-history-container'>"
                        for nft in nft_history:
                            # Extract key data
                            mint_id = nft.get("mint_id", "Unknown")
                            wallet = nft.get("wallet_address", "Unknown")
                            timestamp = nft.get("timestamp", "Unknown")
                            status = nft.get("status", "Unknown")
                            token_id = nft.get("token_id", "Pending")
                            
                            # Generate item HTML
                            status_color = {
                                "minted": "green",
                                "minting": "orange",
                                "error": "red"
                            }.get(status, "gray")
                            
                            html += f"""
                            <div class='nft-history-item'>
                                <div class='nft-history-header'>
                                    <span class='nft-id'>NFT #{mint_id[:8]}...</span>
                                    <span class='nft-timestamp'>{timestamp}</span>
                                </div>
                                <div class='nft-history-details'>
                                    <div class='nft-detail'>
                                        <span class='detail-label'>Wallet:</span>
                                        <span class='detail-value'>{wallet[:10]}...</span>
                                    </div>
                                    <div class='nft-detail'>
                                        <span class='detail-label'>Token ID:</span>
                                        <span class='detail-value'>{token_id}</span>
                                    </div>
                                    <div class='nft-detail'>
                                        <span class='detail-label'>Status:</span>
                                        <span class='detail-value' style='color: {status_color};'>{status.upper()}</span>
                                    </div>
                                </div>
                            </div>
                            """
                        
                        html += "</div>"
                        
                        # Add CSS
                        html += """
                        <style>
                            .nft-history-container {
                                display: flex;
                                flex-direction: column;
                                gap: 16px;
                                margin-top: 12px;
                            }
                            
                            .nft-history-item {
                                border: 1px solid #ddd;
                                border-radius: 8px;
                                padding: 16px;
                                background: rgba(0, 0, 0, 0.02);
                            }
                            
                            .nft-history-header {
                                display: flex;
                                justify-content: space-between;
                                margin-bottom: 12px;
                                border-bottom: 1px solid #eee;
                                padding-bottom: 8px;
                            }
                            
                            .nft-id {
                                font-weight: bold;
                                font-family: monospace;
                            }
                            
                            .nft-timestamp {
                                color: #666;
                                font-size: 0.9em;
                            }
                            
                            .nft-history-details {
                                display: grid;
                                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                                gap: 8px;
                            }
                            
                            .nft-detail {
                                display: flex;
                                justify-content: space-between;
                            }
                            
                            .detail-label {
                                font-weight: bold;
                                color: #555;
                            }
                            
                            .history-empty {
                                padding: 30px;
                                text-align: center;
                                color: #666;
                                background: rgba(0, 0, 0, 0.05);
                                border-radius: 8px;
                            }
                        </style>
                        """
                        
                        return html
                    
                    def refresh_nft_history():
                        """Refresh NFT history from Redis"""
                        if USE_REDIS:
                            try:
                                nft_history = get_nft_history(limit=20)
                                
                                if nft_history:
                                    return (
                                        f"*Showing {len(nft_history)} recent NFT transactions from Redis*",
                                        format_nft_history(nft_history)
                                    )
                                else:
                                    return (
                                        "*No NFT history found in Redis*",
                                        "<div class='history-empty'>No NFT history available yet.</div>"
                                    )
                            except Exception as e:
                                return (
                                    f"*Error retrieving NFT history: {str(e)}*",
                                    "<div class='history-empty'>Error loading NFT history.</div>"
                                )
                        else:
                            return (
                                "*Redis integration is disabled*",
                                "<div class='history-empty'>Redis integration is disabled. Enable Redis to see NFT history.</div>"
                            )
                    
                    # Trigger refresh on button click
                    refresh_btn.click(
                        fn=refresh_nft_history,
                        outputs=[history_status, history_container]
                    )
                    
                    # Initial load
                    gr.on_load(lambda: refresh_nft_history())
            
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

def generate_nft(prompt, style, rarity, use_quantum=True):
    """
    Generate an NFT based on the given parameters
    """
    try:
        logger.info(f"Generating NFT with prompt: {prompt}, style: {style}, rarity: {rarity}, quantum: {use_quantum}")
        
        # Track NFT generation request in Redis
        if USE_REDIS:
            try:
                # Generate a unique ID for this NFT
                nft_id = str(uuid.uuid4())
                
                # Record generation request
                generation_data = {
                    "nft_id": nft_id,
                    "prompt": prompt,
                    "style": style,
                    "rarity": rarity,
                    "use_quantum": use_quantum,
                    "status": "generating",
                    "timestamp": datetime.now().isoformat()
                }
                
                # Store in Redis
                nft_key = get_namespaced_key("nft", nft_id)
                set_json(nft_key, generation_data)
                
                # Add to generation queue
                queue_key = get_namespaced_key("nft", "generation_queue")
                push_to_list(queue_key, nft_key)
                
                # Track metrics
                record_metric("nft_generation_requests", 1)
                record_metric(f"nft_style_{style}", 1)
                
                # Log event
                log_event("nft_generation_request", {
                    "nft_id": nft_id,
                    "prompt": prompt,
                    "style": style,
                    "rarity": rarity
                })
                
                logger.info(f"NFT generation request tracked in Redis with ID: {nft_id}")
            except Exception as e:
                logger.error(f"Redis error tracking NFT generation: {str(e)}")
        
        # Initialize NFT generator
        nft_generator = NFTGenerator()
        
        # Generate NFT
        image_path = nft_generator.generate(prompt, style, rarity, use_quantum)
        
        # Generate metadata
        metadata = NFTMetadata.create(prompt, style, rarity, image_path, use_quantum)
        
        # Update NFT data in Redis
        if USE_REDIS and 'nft_id' in locals():
            try:
                # Update generation data with success
                generation_data.update({
                    "status": "generated",
                    "image_path": image_path,
                    "metadata": metadata
                })
                
                # Store updated data
                set_json(nft_key, generation_data)
                
                # Log completion event
                log_event("nft_generation_complete", {
                    "nft_id": nft_id,
                    "image_path": image_path
                })
            except Exception as e:
                logger.error(f"Redis error updating NFT generation: {str(e)}")
        
        return image_path, metadata
    
    except Exception as e:
        logger.error(f"Error generating NFT: {str(e)}")
        
        # Log error in Redis
        if USE_REDIS and 'nft_id' in locals() and 'nft_key' in locals():
            try:
                # Update generation data with error
                generation_data.update({
                    "status": "error",
                    "error": str(e)
                })
                
                # Store updated data
                set_json(nft_key, generation_data)
                
                # Log error event
                log_event("nft_generation_error", {
                    "nft_id": nft_id,
                    "error": str(e)
                })
            except Exception as redis_err:
                logger.error(f"Redis error logging NFT generation error: {str(redis_err)}")
        
        raise e

def mint_nft(image_path, metadata, wallet_address):
    """
    Mint an NFT with the given metadata and image
    """
    try:
        logger.info(f"Minting NFT from {image_path} to wallet {wallet_address}")
        
        # Track NFT minting in Redis
        if USE_REDIS:
            try:
                # Generate a unique ID for this minting operation
                mint_id = str(uuid.uuid4())
                
                # Extract NFT ID from metadata if available
                nft_id = metadata.get("id", mint_id)
                
                # Record minting request
                minting_data = {
                    "mint_id": mint_id,
                    "nft_id": nft_id,
                    "wallet_address": wallet_address,
                    "image_path": image_path,
                    "metadata": metadata,
                    "status": "minting",
                    "timestamp": datetime.now().isoformat()
                }
                
                # Store in Redis
                mint_key = get_namespaced_key("nft", f"mint_{mint_id}")
                set_json(mint_key, minting_data)
                
                # Add to minting history
                history_key = get_namespaced_key("nft", "minting_history")
                push_to_list(history_key, mint_key)
                
                # Track metrics
                record_metric("nft_minting_requests", 1)
                
                # Log event
                log_event("nft_minting_request", {
                    "mint_id": mint_id,
                    "nft_id": nft_id,
                    "wallet_address": wallet_address
                })
                
                logger.info(f"NFT minting request tracked in Redis with ID: {mint_id}")
            except Exception as e:
                logger.error(f"Redis error tracking NFT minting: {str(e)}")
        
        # Initialize blockchain
        blockchain = NFTBlockchain()
        
        # Mint NFT
        token_id = blockchain.mint(image_path, metadata, wallet_address)
        
        # Update minting data in Redis
        if USE_REDIS and 'mint_id' in locals():
            try:
                # Update minting data with success
                minting_data.update({
                    "status": "minted",
                    "token_id": token_id,
                    "completion_time": datetime.now().isoformat()
                })
                
                # Store updated data
                set_json(mint_key, minting_data)
                
                # Log completion event
                log_event("nft_minting_complete", {
                    "mint_id": mint_id,
                    "token_id": token_id
                })
            except Exception as e:
                logger.error(f"Redis error updating NFT minting: {str(e)}")
        
        return token_id
    
    except Exception as e:
        logger.error(f"Error minting NFT: {str(e)}")
        
        # Log error in Redis
        if USE_REDIS and 'mint_id' in locals() and 'mint_key' in locals():
            try:
                # Update minting data with error
                minting_data.update({
                    "status": "error",
                    "error": str(e)
                })
                
                # Store updated data
                set_json(mint_key, minting_data)
                
                # Log error event
                log_event("nft_minting_error", {
                    "mint_id": mint_id,
                    "error": str(e)
                })
            except Exception as redis_err:
                logger.error(f"Redis error logging NFT minting error: {str(redis_err)}")
        
        raise e

def get_nft_history(limit=10):
    """Get NFT minting history from Redis"""
    if not USE_REDIS:
        return []
    
    try:
        # Get the list of minting keys
        history_key = get_namespaced_key("nft", "minting_history")
        mint_keys = get_list(history_key, start=0, end=limit-1)
        
        # Retrieve each minting record
        results = []
        for key in mint_keys:
            mint_data = get_json(key)
            if mint_data:
                results.append(mint_data)
        
        return results
    except Exception as e:
        logger.error(f"Error retrieving NFT history: {str(e)}")
        return [] 