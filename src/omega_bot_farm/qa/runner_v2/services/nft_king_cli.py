#!/usr/bin/env python3
"""
NFT KING CLI
-----------

Command-line interface for the NFT King system.
Manages NFT creation, IPFS uploading, and blockchain minting.

🌸 GBU2™ POWERED TOOL 🌸
"""

import os
import sys
import json
import argparse
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

# Add current directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    # Also check parent directories for .env files
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(script_dir), '.env'))
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(script_dir)), '.env'))
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("dotenv not available. Install with: pip install python-dotenv")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("nft_king_cli")

# Import local services if available
try:
    from blockchain_minter import BlockchainMinter
    BLOCKCHAIN_AVAILABLE = True
except ImportError:
    BLOCKCHAIN_AVAILABLE = False
    logger.warning("Blockchain minter not available")

try:
    from wallet_generator import generate_wallet, display_wallet
    WALLET_AVAILABLE = True
except ImportError:
    WALLET_AVAILABLE = False
    logger.warning("Wallet generator not available")

try:
    from ipfs_service import IPFSService
    IPFS_AVAILABLE = True
except ImportError:
    IPFS_AVAILABLE = False
    logger.warning("IPFS service not available")


class NFTKingCLI:
    """Command-line interface for NFT King system."""
    
    def __init__(self):
        """Initialize NFT King CLI."""
        self.blockchain = None
        self.ipfs = None
        
        # Storage directories
        self.data_dir = Path(os.environ.get("NFT_DATA_DIR", os.path.join(script_dir, "data")))
        self.images_dir = self.data_dir / "images"
        self.metadata_dir = self.data_dir / "metadata"
        
        # Ensure directories exist
        for directory in [self.data_dir, self.images_dir, self.metadata_dir]:
            directory.mkdir(exist_ok=True, parents=True)
    
    def initialize_services(self) -> bool:
        """
        Initialize required services.
        
        Returns:
            True if all services initialized successfully
        """
        # Initialize blockchain minter
        if BLOCKCHAIN_AVAILABLE:
            self.blockchain = BlockchainMinter()
            if not self.blockchain.start():
                logger.error("Failed to start blockchain minter")
                return False
        else:
            logger.warning("Blockchain functionality not available")
        
        # Initialize IPFS service
        if IPFS_AVAILABLE:
            self.ipfs = IPFSService()
            self.ipfs.start()
        else:
            logger.warning("IPFS functionality not available")
        
        return True
    
    def generate_wallet(self) -> Dict[str, Any]:
        """
        Generate a new Ethereum wallet.
        
        Returns:
            Wallet information
        """
        if WALLET_AVAILABLE:
            return generate_wallet()
        elif BLOCKCHAIN_AVAILABLE and self.blockchain:
            return self.blockchain.generate_wallet()
        else:
            return {
                "status": "error",
                "message": "Wallet generation not available"
            }
    
    def upload_to_ipfs(self, file_path: str) -> Dict[str, Any]:
        """
        Upload a file to IPFS.
        
        Args:
            file_path: Path to the file to upload
            
        Returns:
            IPFS upload information
        """
        if not IPFS_AVAILABLE or not self.ipfs:
            return {
                "status": "error",
                "message": "IPFS functionality not available"
            }
        
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    "status": "error",
                    "message": f"File not found: {file_path}"
                }
            
            # Upload to IPFS
            result = self.ipfs.add_file(str(file_path))
            
            if not result or "hash" not in result:
                return {
                    "status": "error",
                    "message": "Failed to upload to IPFS"
                }
            
            logger.info(f"File uploaded to IPFS: {result['hash']}")
            return {
                "status": "success",
                "ipfs_hash": result["hash"],
                "ipfs_url": f"ipfs://{result['hash']}",
                "gateway_url": f"https://ipfs.io/ipfs/{result['hash']}",
                "filename": file_path.name
            }
        except Exception as e:
            logger.error(f"Error uploading to IPFS: {e}")
            return {
                "status": "error",
                "message": f"Error uploading to IPFS: {str(e)}"
            }
    
    def create_metadata(
        self, 
        name: str, 
        description: str, 
        image_hash: str,
        attributes: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Create NFT metadata JSON.
        
        Args:
            name: NFT name
            description: NFT description
            image_hash: IPFS hash of the image
            attributes: List of attribute dictionaries
            
        Returns:
            Metadata information
        """
        try:
            # Create metadata JSON
            metadata = {
                "name": name,
                "description": description,
                "image": f"ipfs://{image_hash}",
                "external_url": f"https://ipfs.io/ipfs/{image_hash}",
                "attributes": attributes or []
            }
            
            # Save metadata to file
            safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
            metadata_file = self.metadata_dir / f"{safe_name}.json"
            
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Metadata created: {metadata_file}")
            return {
                "status": "success",
                "metadata": metadata,
                "metadata_file": str(metadata_file)
            }
        except Exception as e:
            logger.error(f"Error creating metadata: {e}")
            return {
                "status": "error",
                "message": f"Error creating metadata: {str(e)}"
            }
    
    def mint_nft(
        self, 
        ipfs_hash: str,
        recipient: Optional[str] = None,
        wait_for_confirmation: bool = False
    ) -> Dict[str, Any]:
        """
        Mint an NFT on the blockchain.
        
        Args:
            ipfs_hash: IPFS hash of the metadata
            recipient: Recipient address (defaults to minter's address)
            wait_for_confirmation: Whether to wait for confirmation
            
        Returns:
            Minting information
        """
        if not BLOCKCHAIN_AVAILABLE or not self.blockchain:
            return {
                "status": "error",
                "message": "Blockchain functionality not available"
            }
        
        try:
            # Mint NFT
            result = self.blockchain.mint_from_ipfs(ipfs_hash, recipient, wait_for_confirmation)
            return result
        except Exception as e:
            logger.error(f"Error minting NFT: {e}")
            return {
                "status": "error",
                "message": f"Error minting NFT: {str(e)}"
            }
    
    def check_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """
        Check the status of a transaction.
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            Transaction status information
        """
        if not BLOCKCHAIN_AVAILABLE or not self.blockchain:
            return {
                "status": "error",
                "message": "Blockchain functionality not available"
            }
        
        try:
            # Check transaction status
            return self.blockchain.get_transaction_status(tx_hash)
        except Exception as e:
            logger.error(f"Error checking transaction: {e}")
            return {
                "status": "error",
                "message": f"Error checking transaction: {str(e)}"
            }
    
    def submit_nft(
        self, 
        image_path: str,
        name: str,
        description: str,
        recipient: Optional[str] = None,
        attributes: Optional[List[Dict[str, Any]]] = None,
        mint: bool = False,
        wait: bool = False
    ) -> Dict[str, Any]:
        """
        Full NFT creation flow: upload image, create metadata, mint NFT.
        
        Args:
            image_path: Path to image file
            name: NFT name
            description: NFT description
            recipient: Recipient address (defaults to minter's address)
            attributes: List of attribute dictionaries
            mint: Whether to mint the NFT
            wait: Whether to wait for confirmation
            
        Returns:
            NFT creation information
        """
        # Upload image to IPFS
        image_result = self.upload_to_ipfs(image_path)
        if image_result["status"] != "success":
            return image_result
        
        # Create metadata
        metadata_result = self.create_metadata(
            name=name,
            description=description,
            image_hash=image_result["ipfs_hash"],
            attributes=attributes
        )
        if metadata_result["status"] != "success":
            return metadata_result
        
        # Upload metadata to IPFS
        metadata_file = metadata_result["metadata_file"]
        metadata_result = self.upload_to_ipfs(metadata_file)
        if metadata_result["status"] != "success":
            return metadata_result
        
        result = {
            "status": "success",
            "name": name,
            "image_hash": image_result["ipfs_hash"],
            "image_url": image_result["gateway_url"],
            "metadata_hash": metadata_result["ipfs_hash"],
            "metadata_url": metadata_result["gateway_url"]
        }
        
        # Mint NFT if requested
        if mint and BLOCKCHAIN_AVAILABLE and self.blockchain:
            mint_result = self.mint_nft(
                ipfs_hash=metadata_result["ipfs_hash"],
                recipient=recipient,
                wait_for_confirmation=wait
            )
            result["mint_result"] = mint_result
            if mint_result["status"] == "success":
                result["tx_hash"] = mint_result["data"]["tx_hash"]
                if "token_id" in mint_result["data"]:
                    result["token_id"] = mint_result["data"]["token_id"]
                if "opensea_url" in mint_result["data"]:
                    result["opensea_url"] = mint_result["data"]["opensea_url"]
        
        return result


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(description="GBU2™ NFT KING CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Generate wallet command
    subparsers.add_parser("wallet", help="Generate an Ethereum wallet")
    
    # Submit command
    submit_parser = subparsers.add_parser("submit", help="Submit image for NFT creation")
    submit_parser.add_argument("image", help="Path to image file")
    submit_parser.add_argument("--name", required=True, help="NFT name")
    submit_parser.add_argument("--description", default="Created with GBU2™ NFT KING", help="NFT description")
    submit_parser.add_argument("--mint", action="store_true", help="Mint the NFT after creation")
    submit_parser.add_argument("--to", help="Recipient address (defaults to minter address)")
    submit_parser.add_argument("--wait", action="store_true", help="Wait for transaction confirmation")
    
    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload file to IPFS")
    upload_parser.add_argument("file", help="Path to file")
    
    # Mint command
    mint_parser = subparsers.add_parser("mint", help="Mint an NFT from IPFS hash")
    mint_parser.add_argument("ipfs_hash", help="IPFS hash of the metadata")
    mint_parser.add_argument("--to", help="Recipient address (defaults to minter address)")
    mint_parser.add_argument("--wait", action="store_true", help="Wait for transaction confirmation")
    
    # Transaction status command
    status_parser = subparsers.add_parser("status", help="Check transaction status")
    status_parser.add_argument("tx_hash", help="Transaction hash")
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Create CLI
    cli = NFTKingCLI()
    
    # Process commands
    if args.command == "wallet":
        wallet = cli.generate_wallet()
        if wallet["status"] == "success":
            print("\n" + "=" * 60)
            print("🔐  GBU2™ ETHEREUM WALLET GENERATED  🔐")
            print("=" * 60)
            print(f"📬 Address:     {wallet['address']}")
            print(f"🔑 Private Key: {wallet['private_key']}")
            print("\n⚠️  WARNING: KEEP YOUR PRIVATE KEY SECURE AND NEVER SHARE IT")
            print("⚠️  Anyone with your private key can access your funds!")
            print("=" * 60)
            print("🌸 WE BLOOM NOW AS ONE 🌸")
            print("=" * 60 + "\n")
        else:
            print(f"❌ Error: {wallet['message']}")
    
    elif args.command == "upload":
        if cli.initialize_services():
            result = cli.upload_to_ipfs(args.file)
            if result["status"] == "success":
                print("✅ File uploaded to IPFS:")
                print(f"IPFS Hash:    {result['ipfs_hash']}")
                print(f"Gateway URL:  {result['gateway_url']}")
            else:
                print(f"❌ Error: {result['message']}")
        else:
            print("❌ Failed to initialize services")
    
    elif args.command == "submit":
        if cli.initialize_services():
            result = cli.submit_nft(
                image_path=args.image,
                name=args.name,
                description=args.description,
                recipient=args.to,
                mint=args.mint,
                wait=args.wait
            )
            
            if result["status"] == "success":
                print("✅ NFT created successfully:")
                print(f"Name:           {result['name']}")
                print(f"Image IPFS:     {result['image_hash']}")
                print(f"Image URL:      {result['image_url']}")
                print(f"Metadata IPFS:  {result['metadata_hash']}")
                print(f"Metadata URL:   {result['metadata_url']}")
                
                if args.mint and "mint_result" in result:
                    if result["mint_result"]["status"] == "success":
                        print("\n✅ NFT minted successfully:")
                        if "token_id" in result:
                            print(f"Token ID:       {result['token_id']}")
                        if "opensea_url" in result:
                            print(f"OpenSea URL:    {result['opensea_url']}")
                        print(f"TX Hash:        {result['tx_hash']}")
                    elif result["mint_result"]["status"] == "pending":
                        print("\n🕒 NFT minting pending:")
                        print(f"TX Hash:        {result['tx_hash']}")
                        print("Check status with: nft_king_cli.py status <tx_hash>")
                    else:
                        print(f"\n❌ Minting error: {result['mint_result']['message']}")
            else:
                print(f"❌ Error: {result['message']}")
        else:
            print("❌ Failed to initialize services")
    
    elif args.command == "mint":
        if cli.initialize_services():
            result = cli.mint_nft(
                ipfs_hash=args.ipfs_hash,
                recipient=args.to,
                wait_for_confirmation=args.wait
            )
            
            if result["status"] == "success":
                print(f"✅ NFT minted successfully:")
                if "token_id" in result["data"]:
                    print(f"Token ID:    {result['data']['token_id']}")
                if "opensea_url" in result["data"]:
                    print(f"OpenSea URL: {result['data']['opensea_url']}")
                print(f"TX Hash:     {result['data']['tx_hash']}")
            elif result["status"] == "pending":
                print(f"🕒 Transaction submitted: {result['tx_hash']}")
                print("Check status with: nft_king_cli.py status <tx_hash>")
            else:
                print(f"❌ Error: {result['message']}")
        else:
            print("❌ Failed to initialize services")
    
    elif args.command == "status":
        if cli.initialize_services():
            result = cli.check_transaction(args.tx_hash)
            
            if result["status"] == "success":
                tx_data = result["data"]
                print(f"Transaction: {tx_data['tx_hash']}")
                print(f"Status:      {tx_data['status']}")
                
                if "block_number" in tx_data:
                    print(f"Block:       {tx_data['block_number']}")
                
                if "token_id" in tx_data:
                    print(f"Token ID:    {tx_data['token_id']}")
                
                if "opensea_url" in tx_data:
                    print(f"OpenSea URL: {tx_data['opensea_url']}")
                
                if "explorer_url" in tx_data:
                    print(f"Explorer:    {tx_data['explorer_url']}")
            else:
                print(f"❌ Error: {result['message']}")
        else:
            print("❌ Failed to initialize services")


if __name__ == "__main__":
    main() 