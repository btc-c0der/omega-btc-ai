"""
NFT Creator UI Component for Divine Dashboard v3

This module provides a Gradio-based UI for creating, viewing, and managing NFTs
with quantum security features.
"""

import os
import json
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union

try:
    import gradio as gr
except ImportError:
    print("Gradio not installed. Please install with: pip install gradio")

from divine_dashboard_v3.components.nft.metadata.nft_metadata_generator import NFTMetadataGenerator
from divine_dashboard_v3.components.nft.generator.nft_generator import NFTGenerator
from divine_dashboard_v3.components.nft.blockchain.nft_blockchain_integration import NFTBlockchainIntegration
from divine_dashboard_v3.components.nft.quantum_security import (
    NFTQuantumHashchain, 
    NFTQuantumSigner, 
    EntropyCollector,
    NFTQuantumVerifier
)

class NFTCreatorUI:
    """UI component for creating and managing NFTs with quantum security features."""
    
    def __init__(self, output_dir: str = "output/nfts"):
        """
        Initialize the NFT Creator UI.
        
        Args:
            output_dir: Directory to store generated NFTs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.metadata_generator = NFTMetadataGenerator()
        self.nft_generator = NFTGenerator(output_dir=str(self.output_dir))
        self.blockchain = NFTBlockchainIntegration()
        
        # Initialize quantum security components
        self.entropy_collector = EntropyCollector()
        self.quantum_hashchain = NFTQuantumHashchain()
        self.quantum_signer = NFTQuantumSigner()
        self.quantum_verifier = NFTQuantumVerifier()
        
        # Track generated NFTs
        self.generated_nfts = []
    
    def create_ui(self) -> gr.Blocks:
        """
        Create the Gradio UI for NFT creation and management.
        
        Returns:
            gr.Blocks: The Gradio interface
        """
        with gr.Blocks(title="Divine NFT Creator", theme="default") as interface:
            with gr.Row():
                gr.Markdown("# 🌟 Divine NFT Creator")
            
            with gr.Tabs():
                with gr.TabItem("Create NFT"):
                    with gr.Row():
                        with gr.Column():
                            name_input = gr.Textbox(label="NFT Name", placeholder="Enter a name for your NFT")
                            description_input = gr.Textbox(label="Description", placeholder="Describe your NFT", lines=3)
                            
                            with gr.Row():
                                image_input = gr.Image(label="Upload Image", type="filepath")
                                generate_btn = gr.Button(value="Generate from Text", variant="secondary")
                            
                            text_prompt = gr.Textbox(label="Text Prompt (for generation)", 
                                                    placeholder="Describe the image to generate",
                                                    visible=False)
                            
                            attributes_input = gr.Textbox(label="Attributes (JSON)", 
                                                        placeholder='[{"trait_type": "Background", "value": "Blue"}]',
                                                        lines=3)
                            
                            with gr.Row():
                                security_level = gr.Dropdown(
                                    label="Quantum Security Level",
                                    choices=["Standard", "Enhanced", "Maximum"],
                                    value="Enhanced"
                                )
                            
                            create_btn = gr.Button(value="Create NFT", variant="primary")
                            
                        with gr.Column():
                            preview = gr.Image(label="NFT Preview")
                            status_output = gr.Textbox(label="Status", interactive=False)
                            entropy_meter = gr.Slider(minimum=0, maximum=100, value=0, 
                                                    label="Entropy Collection")
                
                with gr.TabItem("My NFTs"):
                    with gr.Row():
                        refresh_btn = gr.Button(value="Refresh Gallery")
                    
                    gallery = gr.Gallery(label="My NFTs").style(grid=3, height="auto")
                    
                    with gr.Row():
                        selected_nft = gr.Textbox(label="Selected NFT ID", interactive=False)
                    
                    with gr.Row():
                        view_metadata_btn = gr.Button(value="View Metadata")
                        verify_btn = gr.Button(value="Verify Authenticity")
                        mint_btn = gr.Button(value="Mint on Blockchain")
                    
                    with gr.Row():
                        output_display = gr.Textbox(label="Output", interactive=False, lines=10)
                
                with gr.TabItem("Blockchain"):
                    with gr.Row():
                        transaction_id = gr.Textbox(label="Transaction ID", placeholder="Enter transaction ID")
                        check_tx_btn = gr.Button(value="Check Transaction")
                    
                    blockchain_status = gr.Textbox(label="Blockchain Status", interactive=False, lines=5)
            
            # Event handlers
            generate_btn.click(
                fn=self._toggle_text_prompt,
                inputs=[],
                outputs=[text_prompt]
            )
            
            create_btn.click(
                fn=self.create_nft,
                inputs=[name_input, description_input, image_input, text_prompt, 
                        attributes_input, security_level],
                outputs=[preview, status_output, entropy_meter]
            )
            
            refresh_btn.click(
                fn=self.refresh_gallery,
                inputs=[],
                outputs=[gallery]
            )
            
            gallery.select(
                fn=self._on_gallery_select,
                inputs=[gallery],
                outputs=[selected_nft]
            )
            
            view_metadata_btn.click(
                fn=self.view_metadata,
                inputs=[selected_nft],
                outputs=[output_display]
            )
            
            verify_btn.click(
                fn=self.verify_nft,
                inputs=[selected_nft],
                outputs=[output_display]
            )
            
            mint_btn.click(
                fn=self.mint_nft,
                inputs=[selected_nft],
                outputs=[output_display]
            )
            
            check_tx_btn.click(
                fn=self.check_transaction,
                inputs=[transaction_id],
                outputs=[blockchain_status]
            )
            
        return interface
    
    def _toggle_text_prompt(self) -> Dict[str, Any]:
        """
        Toggle visibility of text prompt field.
        
        Returns:
            Dict containing update for text prompt visibility
        """
        return {"visible": True, "__type__": "update"}
    
    async def create_nft(
        self, 
        name: str, 
        description: str, 
        image_path: Optional[str], 
        text_prompt: str,
        attributes_json: str,
        security_level: str
    ) -> Tuple[Optional[str], str, float]:
        """
        Create a new NFT with the provided details.
        
        Args:
            name: Name of the NFT
            description: Description of the NFT
            image_path: Path to the uploaded image
            text_prompt: Text prompt for generating an image
            attributes_json: JSON string of NFT attributes
            security_level: Quantum security level
        
        Returns:
            Tuple containing:
            - Path to the generated NFT image
            - Status message
            - Entropy level (0-100)
        """
        if not name:
            return None, "Error: Name is required", 0
        
        try:
            # Parse attributes
            attributes = []
            if attributes_json:
                attributes = json.loads(attributes_json)
            
            # Collect entropy for quantum security
            entropy_level = 0
            for i in range(10):
                await asyncio.sleep(0.1)  # Simulate entropy collection
                entropy = self.entropy_collector.collect_entropy()
                entropy_level = min((i + 1) * 10, 100)
                yield None, f"Collecting entropy: {entropy_level}%", entropy_level
            
            # Generate or use provided image
            image_output_path = None
            if text_prompt and not image_path:
                yield None, "Generating image from text prompt...", entropy_level
                image_output_path = self.nft_generator.generate_from_text(text_prompt)
            elif image_path:
                yield None, "Processing uploaded image...", entropy_level
                image_output_path = self.nft_generator.process_image(image_path)
            else:
                return None, "Error: Either upload an image or provide a text prompt", entropy_level
            
            # Generate metadata
            metadata = self.metadata_generator.generate(
                name=name,
                description=description,
                image=os.path.basename(image_output_path),
                attributes=attributes
            )
            
            # Sign with quantum security
            signature = self.quantum_signer.sign(json.dumps(metadata))
            metadata["quantum_signature"] = signature
            metadata["security_level"] = security_level
            
            # Save metadata
            nft_id = f"{int(time.time())}_{name.replace(' ', '_')}"
            metadata_path = self.output_dir / f"{nft_id}.json"
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
            
            # Add to hashchain for provenance
            self.quantum_hashchain.add_entry(nft_id, metadata)
            
            # Track the generated NFT
            self.generated_nfts.append({
                "id": nft_id,
                "name": name,
                "image": image_output_path,
                "metadata": metadata_path
            })
            
            return image_output_path, f"NFT created successfully! ID: {nft_id}", entropy_level
        
        except Exception as e:
            return None, f"Error creating NFT: {str(e)}", 0
    
    def _on_gallery_select(self, evt: Dict[str, Any]) -> str:
        """
        Handle gallery selection event.
        
        Args:
            evt: Event data containing selected index
            
        Returns:
            Selected NFT ID
        """
        if evt is None or "index" not in evt:
            return ""
        
        index = evt["index"]
        if 0 <= index < len(self.generated_nfts):
            return self.generated_nfts[index]["id"]
        return ""
    
    async def refresh_gallery(self) -> List[str]:
        """
        Refresh the NFT gallery.
        
        Returns:
            List of paths to NFT images
        """
        # Scan output directory for NFTs
        self.generated_nfts = []
        
        try:
            # Look for image files with corresponding JSON metadata
            image_extensions = [".png", ".jpg", ".jpeg", ".gif"]
            for file in self.output_dir.glob("*"):
                if any(file.name.endswith(ext) for ext in image_extensions):
                    # Check for corresponding metadata
                    metadata_path = self.output_dir / f"{file.stem}.json"
                    if metadata_path.exists():
                        with open(metadata_path, "r") as f:
                            metadata = json.load(f)
                        
                        self.generated_nfts.append({
                            "id": file.stem,
                            "name": metadata.get("name", "Unnamed NFT"),
                            "image": str(file),
                            "metadata": str(metadata_path)
                        })
            
            # Return images for gallery
            images = [nft["image"] for nft in self.generated_nfts]
            return images
        except Exception as e:
            self.generated_nfts = []
            return []
    
    async def view_metadata(self, nft_id: str) -> str:
        """
        View metadata for the selected NFT.
        
        Args:
            nft_id: ID of the NFT to view
        
        Returns:
            Formatted metadata as string
        """
        if not nft_id:
            return "No NFT selected"
        
        for nft in self.generated_nfts:
            if nft["id"] == nft_id:
                try:
                    with open(nft["metadata"], "r") as f:
                        metadata = json.load(f)
                    
                    return json.dumps(metadata, indent=2)
                except Exception as e:
                    return f"Error reading metadata: {str(e)}"
        
        return f"NFT with ID {nft_id} not found"
    
    async def verify_nft(self, nft_id: str) -> str:
        """
        Verify the authenticity of an NFT using quantum verification.
        
        Args:
            nft_id: ID of the NFT to verify
        
        Returns:
            Verification result as string
        """
        if not nft_id:
            return "No NFT selected"
        
        for nft in self.generated_nfts:
            if nft["id"] == nft_id:
                try:
                    with open(nft["metadata"], "r") as f:
                        metadata = json.load(f)
                    
                    # Extract and remove signature for verification
                    signature = metadata.pop("quantum_signature", None)
                    if not signature:
                        return "No quantum signature found in metadata"
                    
                    # Verify using quantum verifier
                    is_valid = self.quantum_verifier.verify(
                        json.dumps(metadata),
                        signature
                    )
                    
                    # Check hashchain for provenance
                    in_hashchain = self.quantum_hashchain.verify_entry(nft_id)
                    
                    if is_valid and in_hashchain:
                        return "✅ NFT VERIFIED: Authentic and unmodified"
                    elif is_valid:
                        return "⚠️ Partially Verified: Signature valid but not found in hashchain"
                    elif in_hashchain:
                        return "⚠️ Partially Verified: Found in hashchain but signature invalid"
                    else:
                        return "❌ VERIFICATION FAILED: NFT may have been tampered with"
                    
                except Exception as e:
                    return f"Error verifying NFT: {str(e)}"
        
        return f"NFT with ID {nft_id} not found"
    
    async def mint_nft(self, nft_id: str) -> str:
        """
        Mint the selected NFT on the blockchain.
        
        Args:
            nft_id: ID of the NFT to mint
        
        Returns:
            Minting result as string
        """
        if not nft_id:
            return "No NFT selected"
        
        for nft in self.generated_nfts:
            if nft["id"] == nft_id:
                try:
                    with open(nft["metadata"], "r") as f:
                        metadata = json.load(f)
                    
                    # Mint on blockchain
                    transaction = self.blockchain.mint_nft(
                        metadata=metadata,
                        image_path=nft["image"]
                    )
                    
                    # Update metadata with transaction info
                    metadata["blockchain"] = {
                        "transaction_id": transaction["id"],
                        "timestamp": transaction["timestamp"],
                        "block": transaction["block"]
                    }
                    
                    # Save updated metadata
                    with open(nft["metadata"], "w") as f:
                        json.dump(metadata, f, indent=2)
                    
                    return (f"NFT minted successfully!\n\n"
                            f"Transaction ID: {transaction['id']}\n"
                            f"Block: {transaction['block']}\n"
                            f"Gas used: {transaction['gas_used']}\n"
                            f"Timestamp: {transaction['timestamp']}")
                    
                except Exception as e:
                    return f"Error minting NFT: {str(e)}"
        
        return f"NFT with ID {nft_id} not found"
    
    def check_transaction(self, transaction_id: str) -> str:
        """
        Check the status of a blockchain transaction.
        
        Args:
            transaction_id: ID of the transaction to check
        
        Returns:
            Transaction status as string
        """
        if not transaction_id:
            return "No transaction ID provided"
        
        try:
            tx_info = self.blockchain.get_transaction(transaction_id)
            
            if not tx_info:
                return f"Transaction {transaction_id} not found"
                
            status = "Confirmed" if tx_info["confirmations"] > 12 else "Pending"
            
            return (f"Transaction: {tx_info['id']}\n"
                    f"Status: {status}\n"
                    f"Confirmations: {tx_info['confirmations']}\n"
                    f"Block: {tx_info['block']}\n"
                    f"Timestamp: {tx_info['timestamp']}")
            
        except Exception as e:
            return f"Error checking transaction: {str(e)}" 