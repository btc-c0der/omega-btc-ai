#!/usr/bin/env python3
"""
Ethereum Quick Connect
---------------------

Simple utility for quickly connecting to Ethereum networks.
Uses the wallet generator to create accounts and Web3 to connect
to various Ethereum networks (mainnet, testnets, L2s).

This can be used as a standalone tool or imported as a module.

🌸 GBU2™ POWERED TOOL 🌸
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

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

# Try to import Web3 libraries
try:
    from web3 import Web3, HTTPProvider
    from web3.middleware import geth_poa_middleware
    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False
    print("Web3 not available. Install with: pip install web3 eth-account")

# Import wallet generator
try:
    from wallet_generator import generate_wallet, display_wallet
    WALLET_MODULE_AVAILABLE = True
except ImportError:
    WALLET_MODULE_AVAILABLE = False
    print("Wallet generator module not found in path.")


# Known networks and their configurations
NETWORKS = {
    "mainnet": {
        "name": "Ethereum Mainnet",
        "chain_id": 1,
        "rpc_url": os.environ.get("MAINNET_RPC_URL", "https://mainnet.infura.io/v3/YOUR_PROJECT_ID"),
        "explorer": "https://etherscan.io",
        "currency": "ETH"
    },
    "sepolia": {
        "name": "Sepolia Testnet",
        "chain_id": 11155111,
        "rpc_url": os.environ.get("SEPOLIA_RPC_URL", "https://sepolia.infura.io/v3/YOUR_PROJECT_ID"),
        "explorer": "https://sepolia.etherscan.io",
        "currency": "ETH",
        "faucet": "https://sepoliafaucet.com/"
    },
    "polygon": {
        "name": "Polygon Mainnet",
        "chain_id": 137,
        "rpc_url": os.environ.get("POLYGON_RPC_URL", "https://polygon-rpc.com"),
        "explorer": "https://polygonscan.com",
        "currency": "MATIC"
    },
    "mumbai": {
        "name": "Polygon Mumbai Testnet",
        "chain_id": 80001,
        "rpc_url": os.environ.get("MUMBAI_RPC_URL", "https://rpc-mumbai.maticvigil.com"),
        "explorer": "https://mumbai.polygonscan.com",
        "currency": "MATIC",
        "faucet": "https://faucet.polygon.technology/"
    },
    "arbitrum": {
        "name": "Arbitrum One",
        "chain_id": 42161,
        "rpc_url": os.environ.get("ARBITRUM_RPC_URL", "https://arb1.arbitrum.io/rpc"),
        "explorer": "https://arbiscan.io",
        "currency": "ETH"
    },
    "optimism": {
        "name": "Optimism",
        "chain_id": 10,
        "rpc_url": os.environ.get("OPTIMISM_RPC_URL", "https://mainnet.optimism.io"),
        "explorer": "https://optimistic.etherscan.io",
        "currency": "ETH"
    }
}


def connect_to_network(
    network_id: str, 
    rpc_url: Optional[str] = None,
    private_key: Optional[str] = None
) -> Tuple[Optional[Web3], Optional[Dict[str, Any]], Optional[str]]:
    """
    Connect to an Ethereum network.
    
    Args:
        network_id: Network identifier (e.g., "mainnet", "sepolia")
        rpc_url: Custom RPC URL to override default
        private_key: Private key to use for signing transactions
        
    Returns:
        Tuple of (Web3 instance, network info, error message)
    """
    if not WEB3_AVAILABLE:
        return None, None, "Web3 not available. Install with: pip install web3 eth-account"
    
    # Check if network is valid
    if network_id not in NETWORKS:
        return None, None, f"Unknown network: {network_id}. Available networks: {', '.join(NETWORKS.keys())}"
    
    # Get network info
    network = NETWORKS[network_id].copy()
    
    # Override RPC URL if provided
    if rpc_url:
        network["rpc_url"] = rpc_url
    elif "ETH_RPC_URL" in os.environ and "YOUR_PROJECT_ID" in network["rpc_url"]:
        # Try default environment variable
        network["rpc_url"] = os.environ["ETH_RPC_URL"]
    
    # Check if the RPC URL is properly set
    if "YOUR_PROJECT_ID" in network["rpc_url"]:
        # Try environment variable
        env_rpc = os.environ.get(f"{network_id.upper()}_RPC_URL")
        if env_rpc:
            network["rpc_url"] = env_rpc
        else:
            return None, None, f"Please provide an RPC URL for {network['name']} or set {network_id.upper()}_RPC_URL environment variable"
    
    try:
        # Create Web3 instance
        web3 = Web3(HTTPProvider(network["rpc_url"]))
        
        # Add middleware for PoA chains (testnets)
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        # Check connection
        if not web3.is_connected():
            return None, None, f"Failed to connect to {network['name']} via {network['rpc_url']}"
        
        # Set up account if private key is provided
        if private_key:
            if not private_key.startswith("0x"):
                private_key = f"0x{private_key}"
                
            from eth_account import Account
            account = Account.from_key(private_key)
            address = account.address
            network["account"] = {
                "address": address,
                "balance": web3.from_wei(web3.eth.get_balance(address), "ether")
            }
        elif "ETH_PRIVATE_KEY" in os.environ:
            # Try loading from environment
            from eth_account import Account
            private_key = os.environ["ETH_PRIVATE_KEY"]
            if not private_key.startswith("0x"):
                private_key = f"0x{private_key}"
                
            account = Account.from_key(private_key)
            address = account.address
            network["account"] = {
                "address": address,
                "balance": web3.from_wei(web3.eth.get_balance(address), "ether")
            }
        
        # Get network info
        network["latest_block"] = web3.eth.block_number
        network["gas_price"] = web3.from_wei(web3.eth.gas_price, "gwei")
        
        return web3, network, None
        
    except Exception as e:
        return None, None, f"Error connecting to {network['name']}: {str(e)}"


def display_connection_info(network: Dict[str, Any]) -> None:
    """Display connection information to console."""
    print("\n" + "=" * 60)
    print(f"🌐  GBU2™ CONNECTED TO {network['name'].upper()}  🌐")
    print("=" * 60)
    print(f"🔗 Chain ID:      {network['chain_id']}")
    print(f"📊 Latest Block:  {network['latest_block']}")
    print(f"⛽ Gas Price:     {network['gas_price']} Gwei")
    
    if "account" in network:
        print(f"\n👛 Address:       {network['account']['address']}")
        print(f"💰 Balance:       {network['account']['balance']} {network['currency']}")
    
    print(f"\n🔍 Explorer:      {network['explorer']}")
    
    if "faucet" in network:
        print(f"🚰 Faucet:        {network['faucet']}")
    
    print("=" * 60)
    print("🌸 WE BLOOM NOW AS ONE 🌸")
    print("=" * 60 + "\n")


def generate_wallet_internal() -> Dict[str, Any]:
    """Generate a wallet using internal implementation if wallet_generator not available."""
    if not WEB3_AVAILABLE:
        return {
            "status": "error",
            "message": "Web3 not available. Install with: pip install web3 eth-account"
        }
    
    try:
        import secrets
        from eth_account import Account
        
        # Generate strong entropy
        entropy = secrets.token_bytes(32)
        
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


def display_wallet_internal(wallet: Dict[str, Any]) -> None:
    """Display wallet info using internal implementation if wallet_generator not available."""
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
    parser = argparse.ArgumentParser(description="GBU2™ Ethereum Quick Connect")
    parser.add_argument("--network", default="sepolia", help="Network to connect to")
    parser.add_argument("--rpc", help="Custom RPC URL")
    parser.add_argument("--key", help="Private key for account")
    parser.add_argument("--new-wallet", action="store_true", help="Generate a new wallet")
    parser.add_argument("--env", action="store_true", help="Use environment variables")
    
    args = parser.parse_args()
    
    # Check if Web3 is available
    if not WEB3_AVAILABLE:
        print("❌ Web3 not available. Install with: pip install web3 eth-account")
        return
        
    # Use environment variables if requested
    if args.env and DOTENV_AVAILABLE and not args.key:
        if "ETH_PRIVATE_KEY" in os.environ:
            args.key = os.environ["ETH_PRIVATE_KEY"]
    
    # Generate new wallet if requested
    if args.new_wallet:
        if WALLET_MODULE_AVAILABLE:
            wallet = generate_wallet()
            display_wallet(wallet)
        else:
            # Use internal implementation
            wallet = generate_wallet_internal()
            display_wallet_internal(wallet)
            
        if wallet.get("status") == "success":
            args.key = wallet["private_key"]
        else:
            return
    
    # Connect to network
    web3, network, error = connect_to_network(args.network, args.rpc, args.key)
    
    if error:
        print(f"❌ {error}")
        return
    
    # Display connection info
    if network:
        display_connection_info(network)
        
        # Show example commands
        print("📝 Example code to use this connection:")
        print("```python")
        print(f"from web3 import Web3")
        print(f"web3 = Web3(Web3.HTTPProvider('{network['rpc_url']}'))")
        
        if "account" in network:
            print(f"from eth_account import Account")
            print(f"account = Account.from_key('YOUR_PRIVATE_KEY')")
            print(f"# Current address: {network['account']['address']}")
            
        print(f"# Latest block: {network['latest_block']}")
        print(f"# Current gas price: {network['gas_price']} Gwei")
        print("```")


if __name__ == "__main__":
    main() 