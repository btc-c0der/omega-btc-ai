
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


# Blockchain Tools for Quantum Test Runner V2

This directory contains standalone tools and services for blockchain and NFT integration.

## Overview

The blockchain tools provide:

1. Ethereum wallet generation and management
2. Network connectivity to Ethereum, Polygon, and other EVM-compatible chains
3. NFT minting capabilities for test reports
4. Smart contract interaction

## Installation

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Available Tools

### 1. Wallet Generator

Simple tool for generating Ethereum wallets:

```bash
python wallet_generator.py
```

Options:

- `--save`: Save wallet to file
- `--output PATH`: Output file path
- `--count N`: Generate multiple wallets

### 2. Quick Connect

Connect to Ethereum networks and display status:

```bash
python quick_connect.py --network sepolia --new-wallet
```

Options:

- `--network NETWORK`: Network to connect to (sepolia, mainnet, polygon, etc.)
- `--rpc URL`: Custom RPC URL
- `--key KEY`: Private key for account
- `--new-wallet`: Generate a new wallet and use it

### 3. NFT King CLI

Interface for the NFT generation and minting service:

```bash
python nft_king_cli.py submit path/to/image.png --name "My NFT"
python nft_king_cli.py mint your-nft-id
```

See `python nft_king_cli.py --help` for more options.

### 4. Blockchain Minter Service

Service for minting NFTs to Ethereum, Polygon, and other chains. Used by the NFT King CLI:

```python
from blockchain_minter import BlockchainMinter

minter = BlockchainMinter(
    contract_address="0xYourContract",
    rpc_url="https://ethereum-sepolia.publicnode.com",
    private_key="your-private-key",
    chain_id=11155111  # Sepolia testnet
)

minter.start()
```

## Environment Variables

Configure the tools with these environment variables:

```bash
# IPFS Configuration (Optional)
export PINATA_API_KEY="your_pinata_api_key"
export PINATA_API_SECRET="your_pinata_api_secret"

# Blockchain Configuration
export ETH_PRIVATE_KEY="your_private_key"
export ETH_RPC_URL="https://sepolia.infura.io/v3/your_project_id"
export NFT_CONTRACT_ADDRESS="0xYourContractAddress"
export DEFAULT_NFT_RECIPIENT="0xYourWalletAddress"

# Network-specific RPC URLs
export SEPOLIA_RPC_URL="https://ethereum-sepolia.publicnode.com"
export MAINNET_RPC_URL="https://eth.llamarpc.com"
export POLYGON_RPC_URL="https://polygon-rpc.com"
```

## Usage Example

```python
# Generate a wallet
from wallet_generator import generate_wallet
wallet = generate_wallet()
private_key = wallet["private_key"]

# Connect to Sepolia
from quick_connect import connect_to_network
web3, network, error = connect_to_network(
    network_id="sepolia",
    private_key=private_key
)

# Mint an NFT
from blockchain_minter import BlockchainMinter
minter = BlockchainMinter(
    contract_address="0xYourContract", 
    rpc_url=network["rpc_url"],
    private_key=private_key
)

minter.mint_from_ipfs(
    ipfs_hash="QmYourIPFSHash",
    recipient=wallet["address"]
)
```

## Security Considerations

- **NEVER** share private keys or commit them to version control
- Use dedicated wallets for test/development environments
- Test on testnets (Sepolia, Mumbai) before mainnet deployment
- Always keep enough ETH/MATIC for gas fees

## Troubleshooting

- For "Web3 not available" errors, install Web3.py: `pip install web3 eth-account`
- For RPC connection errors, check your internet connection and RPC endpoint
- For contract errors, verify your contract address and ABI
- Use testnet faucets to get testnet ETH: [Sepolia Faucet](https://sepoliafaucet.com/)
