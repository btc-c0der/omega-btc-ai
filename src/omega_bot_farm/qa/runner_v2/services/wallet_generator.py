#!/usr/bin/env python3
"""
Ethereum Wallet Generator
------------------------

Simple micro module for generating Ethereum wallets with Web3.py.
Used by the Quantum Test Runner V2 for blockchain operations.

This can be used as a standalone tool or imported as a module.

🌸 GBU2™ POWERED TOOL 🌸
"""

import os
import json
import argparse
import secrets
from pathlib import Path
from typing import Dict, Any, Optional

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("dotenv not available. Install with: pip install python-dotenv")

# Try to import Web3 libraries
try:
    from web3 import Web3
    from eth_account.account import Account
    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False
    print("Web3 not available. Install with: pip install web3 eth-account")


def generate_wallet(entropy_bytes: int = 32) -> Dict[str, Any]:
    """
    Generate a new Ethereum wallet with strong entropy.
    
    Args:
        entropy_bytes: Number of bytes of entropy to use (default: 32)
        
    Returns:
        Dict containing wallet info (address, private_key)
    """
    if not WEB3_AVAILABLE:
        return {
            "status": "error",
            "message": "Web3 not available. Install with: pip install web3 eth-account"
        }
    
    try:
        # Generate strong entropy
        entropy = secrets.token_bytes(entropy_bytes)
        
        # Create account
        account = Account.create(entropy)
        
        # Get private key and address
        private_key = account.key.hex()
        address = account.address
        
        # Calculate checksum address
        checksum_address = Web3.to_checksum_address(address)
        
        return {
            "status": "success",
            "address": checksum_address,
            "private_key": private_key,
            "warning": "KEEP YOUR PRIVATE KEY SECURE AND NEVER SHARE IT"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating wallet: {str(e)}"
        }


def save_wallet(wallet: Dict[str, Any], output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Save wallet information to a JSON file.
    
    Args:
        wallet: Wallet information dictionary
        output_path: Path to save wallet info (default: ./wallet_{address}.json)
        
    Returns:
        Dict with status and file path
    """
    if wallet.get("status") != "success":
        return {
            "status": "error",
            "message": "Cannot save invalid wallet"
        }
    
    try:
        address = wallet["address"]
        # Remove 0x prefix for filename
        address_short = address[2:10]
        
        # Create output path if not provided
        if not output_path:
            output_path = f"wallet_{address_short}_{secrets.token_hex(4)}.json"
        
        # Create output directory if needed
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Save wallet info
        with open(output_path, "w") as f:
            json.dump(wallet, f, indent=2)
        
        return {
            "status": "success",
            "file_path": output_path,
            "message": f"Wallet saved to {output_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error saving wallet: {str(e)}"
        }


def display_wallet(wallet: Dict[str, Any]) -> None:
    """Display wallet information to console."""
    if wallet.get("status") != "success":
        print(f"❌ Error: {wallet.get('message', 'Unknown error')}")
        return
    
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


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(description="GBU2™ Ethereum Wallet Generator")
    parser.add_argument("--save", action="store_true", help="Save wallet to file")
    parser.add_argument("--output", help="Output file path (used with --save)")
    parser.add_argument("--count", type=int, default=1, help="Number of wallets to generate")
    
    args = parser.parse_args()
    
    # Check if Web3 is available
    if not WEB3_AVAILABLE:
        print("❌ Web3 not available. Install with: pip install web3 eth-account")
        return
    
    # Generate requested number of wallets
    for i in range(args.count):
        if args.count > 1:
            print(f"\nGenerating wallet {i+1}/{args.count}")
        
        # Generate wallet
        wallet = generate_wallet()
        
        # Display wallet info
        display_wallet(wallet)
        
        # Save wallet if requested
        if args.save:
            output_path = args.output
            if args.count > 1 and args.output:
                # Add index to filename if generating multiple wallets
                path = Path(args.output)
                output_path = str(path.with_stem(f"{path.stem}_{i+1}"))
            
            save_result = save_wallet(wallet, output_path)
            if save_result["status"] == "success":
                print(f"✅ {save_result['message']}")
            else:
                print(f"❌ {save_result['message']}")


if __name__ == "__main__":
    main() 