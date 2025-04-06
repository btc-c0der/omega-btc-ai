# Blockchain NFT Minting for Quantum Test Runner V2

This documentation explains how to use the blockchain integration features to mint NFTs from the Quantum Test Runner V2.

## Overview

The blockchain minting service allows you to:

1. Generate NFTs locally with rich metadata
2. Upload images and metadata to IPFS via Pinata
3. Mint NFTs as ERC-721 tokens on Ethereum-compatible networks
4. Track transaction status and view your NFTs on marketplaces like OpenSea

## Prerequisites

To use the blockchain features, you need:

- Ethereum account with ETH for gas fees (or relevant testnet tokens for testnets)
- RPC endpoint URL (from Infura, Alchemy, or other providers)
- Deployed ERC-721 compatible NFT contract
- Pinata API credentials for IPFS storage

## Installation

```bash
# Install dependencies
pip install -r services/requirements.txt
```

## Configuration

Set up the following environment variables:

```bash
# IPFS Configuration
export PINATA_API_KEY="your_pinata_api_key"
export PINATA_API_SECRET="your_pinata_api_secret"

# OpenAI for metadata generation (optional)
export OPENAI_API_KEY="your_openai_api_key"

# Blockchain Configuration
export ETH_PRIVATE_KEY="your_private_key"  # Without 0x prefix
export ETH_RPC_URL="https://sepolia.infura.io/v3/your_project_id"
export NFT_CONTRACT_ADDRESS="0xYourContractAddress"
export DEFAULT_NFT_RECIPIENT="0xYourWalletAddress" # Default recipient for minted NFTs
```

## Usage with NFT KING CLI

```bash
# Generate a new wallet (for testing)
python -m qa.runner_v2.services.nft_king_cli wallet

# Create a new NFT from an image
python -m qa.runner_v2.services.nft_king_cli submit path/to/image.png --name "My Amazing NFT"

# Check the status of your NFT
python -m qa.runner_v2.services.nft_king_cli status your-nft-id

# List all generated NFTs
python -m qa.runner_v2.services.nft_king_cli list

# Mint an NFT to the blockchain
python -m qa.runner_v2.services.nft_king_cli mint your-nft-id --recipient 0xYourWalletAddress
```

## Creating Your Own NFT Contract

For full functionality, deploy your own ERC-721 contract with minting and URI setting capabilities. A minimal contract example:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract QuantumNFT is ERC721URIStorage, Ownable {
    constructor() ERC721("QuantumNFT", "QNFT") Ownable(msg.sender) {}

    function mint(address to, uint256 tokenId) public onlyOwner {
        _safeMint(to, tokenId);
    }

    function setTokenURI(uint256 tokenId, string memory uri) public onlyOwner {
        _setTokenURI(tokenId, uri);
    }
}
```

You can deploy this contract using tools like Remix, Hardhat, or Foundry.

## Supported Networks

The blockchain minter supports various networks:

- Ethereum Mainnet (Chain ID: 1)
- Goerli Testnet (Chain ID: 5)
- Sepolia Testnet (Chain ID: 11155111) - Default
- Polygon Mainnet (Chain ID: 137)
- Mumbai Testnet (Chain ID: 80001)
- Avalanche C-Chain (Chain ID: 43114)
- Fuji Testnet (Chain ID: 43113)

To use a different network, modify the `chain_id` parameter when initializing the `BlockchainMinter`.

## Viewing Your NFTs

After minting, you can view your NFTs on:

- **Testnets:** [OpenSea Testnet](https://testnets.opensea.io/)
- **Mainnet:** [OpenSea](https://opensea.io/)

## Security Considerations

- **NEVER** share your private key or commit it to version control
- Use a dedicated wallet for minting operations
- Consider using hardware wallets for production use
- Test thoroughly on testnets before using mainnet

## Troubleshooting

Common issues:

1. **Insufficient gas:** Make sure your wallet has enough ETH/tokens for gas fees
2. **RPC errors:** Verify your RPC URL is correct and the endpoint is responsive
3. **Contract issues:** Ensure your contract implements the required mint and setTokenURI methods
4. **IPFS upload failures:** Check your Pinata API credentials and network connectivity
