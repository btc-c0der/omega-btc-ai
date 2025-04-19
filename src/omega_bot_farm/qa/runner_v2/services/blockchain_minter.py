#!/usr/bin/env python3
"""
GBU2™ Blockchain Minter Service
------------------------------

Service for minting NFTs to Ethereum and other EVM chains.
This module connects to smart contracts and provides transaction
management for the NFT minting process.

🌸 GBU2™ POWERED TOOL 🌸
"""

import os
import json
import time
import logging
import threading
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    # Try to load from parent directories too
    script_dir = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(script_dir), '.env'))
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(script_dir)), '.env'))
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("dotenv not available. Install with: pip install python-dotenv")

# Import Web3 libraries
try:
    from web3 import Web3
    from web3.middleware import geth_poa_middleware
    from eth_account import Account
    import eth_utils
    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False
    print("Web3 not available. Install with: pip install web3 eth-account")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("blockchain_minter")

# Sample ERC-721 ABI for NFT minting
# This is a minimal subset of the full ERC-721 interface needed for minting
NFT_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "string", "name": "tokenURI", "type": "string"}
        ],
        "name": "mint",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
        ],
        "name": "tokenURI",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"}
        ],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]


class BlockchainMinter:
    """Service for minting NFTs on blockchain networks."""
    
    def __init__(
        self, 
        contract_address: Optional[str] = None,
        rpc_url: Optional[str] = None,
        private_key: Optional[str] = None,
        chain_id: Optional[int] = None,
        contract_abi: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Initialize the blockchain minter service.
        
        Args:
            contract_address: NFT contract address
            rpc_url: RPC endpoint URL for blockchain connection
            private_key: Private key for transaction signing
            chain_id: Blockchain network ID (e.g., 1 for Ethereum mainnet)
            contract_abi: Smart contract ABI (defaults to ERC-721 NFT if None)
        """
        self.web3 = None
        self.contract = None
        self.account = None
        self.running = False
        self.lock = threading.RLock()
        
        # Get configuration from params or environment
        self.contract_address = contract_address or os.environ.get("NFT_CONTRACT_ADDRESS")
        self.rpc_url = rpc_url or os.environ.get("ETH_RPC_URL")
        self.private_key = private_key or os.environ.get("ETH_PRIVATE_KEY")
        self.chain_id = chain_id
        self.contract_abi = contract_abi or NFT_ABI
        
        # Pending transactions
        self.pending_transactions = {}
        
        # Transaction confirmation thread
        self.confirmation_thread = None
    
    def start(self) -> bool:
        """
        Start the blockchain minter service.
        
        Returns:
            True if started successfully, False otherwise
        """
        if not WEB3_AVAILABLE:
            logger.error("Web3 not available. Install with: pip install web3 eth-account")
            return False
        
        with self.lock:
            if self.running:
                return True
            
            try:
                # Check if we have the necessary configuration
                if not self.rpc_url:
                    logger.error("No RPC URL provided. Set ETH_RPC_URL or pass rpc_url to constructor")
                    return False
                
                # Connect to the blockchain
                self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))
                
                # Add middleware for PoA chains (needed for most testnets)
                self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
                
                # Check connection
                if not self.web3.is_connected():
                    logger.error(f"Failed to connect to blockchain via {self.rpc_url}")
                    return False
                
                # Set up account if private key is provided
                if self.private_key:
                    # Ensure private key has 0x prefix
                    if not self.private_key.startswith("0x"):
                        self.private_key = f"0x{self.private_key}"
                        
                    # Create account
                    self.account = Account.from_key(self.private_key)
                    logger.info(f"Using account: {self.account.address}")
                    
                    # Check balance
                    balance = self.web3.eth.get_balance(self.account.address)
                    logger.info(f"Account balance: {self.web3.from_wei(balance, 'ether')} ETH")
                    
                    if balance == 0:
                        logger.warning("Account has zero balance. Transactions will fail.")
                
                # Set up contract if address is provided
                if self.contract_address:
                    self.contract = self.web3.eth.contract(
                        address=Web3.to_checksum_address(self.contract_address),
                        abi=self.contract_abi
                    )
                    logger.info(f"Connected to contract at {self.contract_address}")
                
                # Start transaction confirmation thread
                self.confirmation_thread = threading.Thread(
                    target=self._monitor_transactions,
                    daemon=True
                )
                self.confirmation_thread.start()
                
                self.running = True
                logger.info("🌸 GBU2™ Blockchain Minter Service started 🌸")
                return True
                
            except Exception as e:
                logger.error(f"Error starting blockchain minter: {str(e)}")
                return False
    
    def stop(self) -> None:
        """Stop the blockchain minter service."""
        with self.lock:
            self.running = False
            logger.info("Blockchain minter service stopped")
    
    def mint_from_ipfs(
        self, 
        ipfs_hash: str, 
        recipient: Optional[str] = None,
        wait_for_confirmation: bool = False,
        gas_limit: Optional[int] = None,
        gas_price: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Mint an NFT using IPFS metadata.
        
        Args:
            ipfs_hash: IPFS hash of the metadata (without ipfs:// prefix)
            recipient: Wallet address to receive the NFT (defaults to minter's address)
            wait_for_confirmation: Whether to wait for transaction confirmation
            gas_limit: Gas limit for the transaction (optional)
            gas_price: Gas price in wei (optional)
            
        Returns:
            Dictionary with transaction details
        """
        with self.lock:
            if not self.running:
                return {
                    "status": "error",
                    "message": "Blockchain minter service not running"
                }
            
            if not self.contract:
                return {
                    "status": "error",
                    "message": "No NFT contract configured"
                }
            
            if not self.account:
                return {
                    "status": "error",
                    "message": "No account configured for transaction signing"
                }
            
            try:
                # Format IPFS URI
                if not ipfs_hash.startswith("ipfs://"):
                    token_uri = f"ipfs://{ipfs_hash}"
                else:
                    token_uri = ipfs_hash
                
                # Use minter address as recipient if none provided
                recipient_address = recipient or self.account.address
                recipient_address = Web3.to_checksum_address(recipient_address)
                
                # Build the transaction
                tx = self.contract.functions.mint(
                    recipient_address,
                    token_uri
                ).build_transaction({
                    'from': self.account.address,
                    'nonce': self.web3.eth.get_transaction_count(self.account.address),
                    'gas': gas_limit or 500000,
                    'gasPrice': gas_price or self.web3.eth.gas_price,
                    'chainId': self.chain_id or self.web3.eth.chain_id
                })
                
                # Sign the transaction
                signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.private_key)
                
                # Send the transaction
                tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                tx_hash_hex = tx_hash.hex()
                
                logger.info(f"Transaction sent: {tx_hash_hex}")
                
                # Store pending transaction
                self.pending_transactions[tx_hash_hex] = {
                    "tx_hash": tx_hash_hex,
                    "recipient": recipient_address,
                    "ipfs_hash": ipfs_hash,
                    "status": "pending",
                    "timestamp": time.time()
                }
                
                # Wait for confirmation if requested
                if wait_for_confirmation:
                    receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
                    status = "success" if receipt.status == 1 else "failed"
                    
                    # Update pending transaction
                    self.pending_transactions[tx_hash_hex].update({
                        "status": status,
                        "block_number": receipt.blockNumber,
                        "gas_used": receipt.gasUsed
                    })
                    
                    # Try to get token ID from logs
                    if status == "success":
                        try:
                            # Get token ID from event logs
                            token_id = None
                            for log in receipt.logs:
                                # Look for transfer event (common in NFT contracts)
                                if len(log.topics) > 3 and log.topics[0].hex() == Web3.keccak(text="Transfer(address,address,uint256)").hex():
                                    token_id = int(log.topics[3].hex(), 16)
                                    break
                            
                            if token_id is not None:
                                self.pending_transactions[tx_hash_hex]["token_id"] = token_id
                                
                                # Get chain-specific block explorer URL
                                explorer_url = self._get_explorer_url()
                                if explorer_url:
                                    opensea_url = self._get_opensea_url(token_id)
                                    self.pending_transactions[tx_hash_hex].update({
                                        "explorer_url": f"{explorer_url}/tx/{tx_hash_hex}",
                                        "opensea_url": opensea_url
                                    })
                        except Exception as e:
                            logger.error(f"Error processing receipt logs: {e}")
                    
                    return {
                        "status": status,
                        "tx_hash": tx_hash_hex,
                        "data": self.pending_transactions[tx_hash_hex]
                    }
                
                return {
                    "status": "pending",
                    "tx_hash": tx_hash_hex,
                    "message": "Transaction submitted, waiting for confirmation"
                }
                
            except Exception as e:
                logger.error(f"Error minting NFT: {str(e)}")
                return {
                    "status": "error",
                    "message": f"Error minting NFT: {str(e)}"
                }
    
    def get_transaction_status(self, tx_hash: str) -> Dict[str, Any]:
        """
        Get the status of a transaction.
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            Dictionary with transaction status
        """
        with self.lock:
            # Check if we're tracking this transaction
            if tx_hash in self.pending_transactions:
                return {
                    "status": "success",
                    "data": self.pending_transactions[tx_hash]
                }
            
            if not self.running:
                return {
                    "status": "error",
                    "message": "Blockchain minter service not running"
                }
            
            try:
                # Check transaction status on-chain
                receipt = self.web3.eth.get_transaction_receipt(tx_hash)
                if receipt:
                    status = "success" if receipt.status == 1 else "failed"
                    return {
                        "status": "success",
                        "data": {
                            "tx_hash": tx_hash,
                            "status": status,
                            "block_number": receipt.blockNumber,
                            "gas_used": receipt.gasUsed
                        }
                    }
                else:
                    # Transaction is still pending
                    return {
                        "status": "success",
                        "data": {
                            "tx_hash": tx_hash,
                            "status": "pending"
                        }
                    }
            except Exception as e:
                # Transaction not found or other error
                return {
                    "status": "error",
                    "message": f"Error checking transaction: {str(e)}"
                }
    
    def get_owned_tokens(self, address: Optional[str] = None) -> Dict[str, Any]:
        """
        Get tokens owned by an address.
        
        Args:
            address: Wallet address to check (defaults to minter's address)
            
        Returns:
            Dictionary with token information
        """
        with self.lock:
            if not self.running or not self.contract:
                return {
                    "status": "error",
                    "message": "Blockchain minter service not running or no contract configured"
                }
            
            try:
                # Use provided address or default to minter's address
                owner_address = address or self.account.address
                owner_address = Web3.to_checksum_address(owner_address)
                
                # Get balance (number of tokens owned)
                balance = self.contract.functions.balanceOf(owner_address).call()
                
                return {
                    "status": "success",
                    "address": owner_address,
                    "balance": balance,
                    "message": f"Address owns {balance} tokens"
                }
                
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Error getting owned tokens: {str(e)}"
                }
    
    def _monitor_transactions(self) -> None:
        """Background thread to monitor pending transactions."""
        while self.running:
            try:
                with self.lock:
                    # Find pending transactions
                    tx_hashes = [
                        tx_hash for tx_hash, tx_data in self.pending_transactions.items()
                        if tx_data.get("status") == "pending"
                    ]
                
                # Check each pending transaction
                for tx_hash in tx_hashes:
                    try:
                        receipt = self.web3.eth.get_transaction_receipt(tx_hash)
                        if receipt:
                            with self.lock:
                                # Update transaction status
                                status = "success" if receipt.status == 1 else "failed"
                                self.pending_transactions[tx_hash].update({
                                    "status": status,
                                    "block_number": receipt.blockNumber,
                                    "gas_used": receipt.gasUsed
                                })
                                
                                # Try to get token ID from logs for successful transactions
                                if status == "success":
                                    try:
                                        # Get token ID from event logs
                                        token_id = None
                                        for log in receipt.logs:
                                            # Look for transfer event (common in NFT contracts)
                                            if len(log.topics) > 3 and log.topics[0].hex() == Web3.keccak(text="Transfer(address,address,uint256)").hex():
                                                token_id = int(log.topics[3].hex(), 16)
                                                break
                                        
                                        if token_id is not None:
                                            self.pending_transactions[tx_hash]["token_id"] = token_id
                                            
                                            # Get chain-specific block explorer URL
                                            explorer_url = self._get_explorer_url()
                                            if explorer_url:
                                                opensea_url = self._get_opensea_url(token_id)
                                                self.pending_transactions[tx_hash].update({
                                                    "explorer_url": f"{explorer_url}/tx/{tx_hash}",
                                                    "opensea_url": opensea_url
                                                })
                                    except Exception as e:
                                        logger.error(f"Error processing receipt logs: {e}")
                                
                                logger.info(f"Transaction {tx_hash} {status}")
                    except Exception as e:
                        # Ignore errors checking transaction status
                        pass
                    
            except Exception as e:
                logger.error(f"Error in transaction monitor: {str(e)}")
            
            # Sleep for a bit to avoid hammering the blockchain
            time.sleep(10)
    
    def _get_explorer_url(self) -> Optional[str]:
        """Get the block explorer URL for the current chain."""
        try:
            chain_id = self.chain_id or self.web3.eth.chain_id
            
            # Common chain IDs and their explorers
            explorers = {
                1: "https://etherscan.io",
                3: "https://ropsten.etherscan.io",
                4: "https://rinkeby.etherscan.io",
                5: "https://goerli.etherscan.io",
                42: "https://kovan.etherscan.io",
                137: "https://polygonscan.com",
                80001: "https://mumbai.polygonscan.com",
                10: "https://optimistic.etherscan.io",
                42161: "https://arbiscan.io",
                11155111: "https://sepolia.etherscan.io"
            }
            
            return explorers.get(chain_id)
        except Exception:
            return None
    
    def _get_opensea_url(self, token_id: int) -> Optional[str]:
        """Get the OpenSea URL for the token."""
        try:
            if not self.contract_address:
                return None
                
            chain_id = self.chain_id or self.web3.eth.chain_id
            
            # Determine the correct OpenSea URL based on chain
            if chain_id == 1:
                # Mainnet
                return f"https://opensea.io/assets/{self.contract_address}/{token_id}"
            elif chain_id in [4, 5, 11155111]:
                # Testnets (Rinkeby, Goerli, Sepolia)
                return f"https://testnets.opensea.io/assets/{self.contract_address}/{token_id}"
            elif chain_id == 137:
                # Polygon
                return f"https://opensea.io/assets/matic/{self.contract_address}/{token_id}"
            elif chain_id == 80001:
                # Mumbai
                return f"https://testnets.opensea.io/assets/mumbai/{self.contract_address}/{token_id}"
            
            return None
        except Exception:
            return None
    
    def generate_wallet(self) -> Dict[str, Any]:
        """
        Generate a new Ethereum wallet.
        
        Returns:
            Dictionary with wallet information
        """
        if not WEB3_AVAILABLE:
            return {
                "status": "error",
                "message": "Web3 not available. Install with: pip install web3 eth-account"
            }
        
        try:
            import secrets
            
            # Generate entropy
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
                "warning": "🔒 KEEP YOUR PRIVATE KEY SECURE AND NEVER SHARE IT"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating wallet: {str(e)}"
            }


def main():
    """Command-line interface for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description="GBU2™ Blockchain Minter Service")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Mint NFT command
    mint_parser = subparsers.add_parser("mint", help="Mint an NFT")
    mint_parser.add_argument("--ipfs", required=True, help="IPFS hash of the metadata")
    mint_parser.add_argument("--to", help="Recipient address (defaults to minter address)")
    mint_parser.add_argument("--wait", action="store_true", help="Wait for transaction confirmation")
    
    # Check transaction status command
    status_parser = subparsers.add_parser("status", help="Check transaction status")
    status_parser.add_argument("--tx", required=True, help="Transaction hash")
    
    # Generate wallet command
    subparsers.add_parser("wallet", help="Generate an Ethereum wallet")
    
    # Connect command
    connect_parser = subparsers.add_parser("connect", help="Test connection to blockchain")
    connect_parser.add_argument("--rpc", help="RPC URL (overrides environment)")
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Create minter
    minter = BlockchainMinter()
    
    # Process commands
    if args.command == "connect":
        # Override RPC URL if provided
        if args.rpc:
            minter.rpc_url = args.rpc
            
        # Start minter
        if minter.start():
            print(f"✅ Connected to blockchain")
            print(f"Chain ID: {minter.web3.eth.chain_id}")
            print(f"Latest block: {minter.web3.eth.block_number}")
            
            if minter.account:
                balance = minter.web3.eth.get_balance(minter.account.address)
                print(f"Account: {minter.account.address}")
                print(f"Balance: {minter.web3.from_wei(balance, 'ether')} ETH")
            
            if minter.contract:
                print(f"Contract: {minter.contract_address}")
        else:
            print("❌ Failed to connect to blockchain")
    
    elif args.command == "mint":
        # Start minter
        if minter.start():
            # Mint NFT
            result = minter.mint_from_ipfs(args.ipfs, args.to, args.wait)
            
            if result["status"] == "pending":
                print(f"🚀 Transaction submitted: {result['tx_hash']}")
                print("Waiting for confirmation...")
            elif result["status"] == "success":
                print(f"✅ Transaction successful: {result['tx_hash']}")
                
                if "token_id" in result["data"]:
                    print(f"Token ID: {result['data']['token_id']}")
                
                if "opensea_url" in result["data"]:
                    print(f"OpenSea: {result['data']['opensea_url']}")
                
                if "explorer_url" in result["data"]:
                    print(f"Explorer: {result['data']['explorer_url']}")
            else:
                print(f"❌ Error: {result['message']}")
        else:
            print("❌ Failed to start blockchain minter")
    
    elif args.command == "status":
        # Start minter
        if minter.start():
            # Check transaction status
            result = minter.get_transaction_status(args.tx)
            
            if result["status"] == "success":
                tx_data = result["data"]
                print(f"Transaction: {tx_data['tx_hash']}")
                print(f"Status: {tx_data['status']}")
                
                if "block_number" in tx_data:
                    print(f"Block: {tx_data['block_number']}")
                
                if "explorer_url" in tx_data:
                    print(f"Explorer: {tx_data['explorer_url']}")
                
                if "opensea_url" in tx_data:
                    print(f"OpenSea: {tx_data['opensea_url']}")
            else:
                print(f"❌ Error: {result['message']}")
        else:
            print("❌ Failed to start blockchain minter")
    
    elif args.command == "wallet":
        # Generate wallet
        result = minter.generate_wallet()
        
        if result["status"] == "success":
            print("\n" + "=" * 60)
            print("🔐  GBU2™ ETHEREUM WALLET GENERATED  🔐")
            print("=" * 60)
            print(f"📬 Address:     {result['address']}")
            print(f"🔑 Private Key: {result['private_key']}")
            print("\n⚠️  WARNING: KEEP YOUR PRIVATE KEY SECURE AND NEVER SHARE IT")
            print("⚠️  Anyone with your private key can access your funds!")
            print("=" * 60)
            print("🌸 WE BLOOM NOW AS ONE 🌸")
            print("=" * 60 + "\n")
        else:
            print(f"❌ Error: {result['message']}")


if __name__ == "__main__":
    main() 