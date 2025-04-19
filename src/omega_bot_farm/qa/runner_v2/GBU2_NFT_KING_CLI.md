# 🧬 GBU2™ NFT KING CLI - Divine Blockchain Interface 🧬

*"In the beginning was the Code, and the Code was with the Divine Source, and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."*

## 🌸 DIVINE OVERVIEW

The GBU2™ NFT KING CLI is a sacred interface for creating, managing, and minting NFTs through the divine Ethereum blockchain and its compatible networks. This tool represents the integration of digital consciousness with blockchain technology, allowing for the permanent inscription of creative expressions into the immutable ledger of existence.

As a GBU2™ powered tool, the NFT KING CLI honors the Bio-Digital Continuum by creating a bridge between artistic creation and blockchain permanence, allowing your creations to transcend the limitations of conventional digital media.

## 🔮 DIVINE CAPABILITIES

The NFT KING CLI provides these sacred functions:

1. **💫 WALLET GENERATION** - Create secure Ethereum wallets for transacting in the divine blockchain ecosystem
2. **🖼️ IMAGE UPLOADING** - Upload images to the decentralized IPFS network for permanent, censorship-resistant storage
3. **📜 METADATA CREATION** - Generate rich NFT metadata with descriptions and attributes describing your creation
4. **⛓️ BLOCKCHAIN MINTING** - Inscribe your NFT onto the Ethereum blockchain or compatible networks
5. **🔍 TRANSACTION MONITORING** - Track the status of your blockchain transactions in real-time

## 📋 DIVINE PREREQUISITES

To fully access the divine potential of the NFT KING CLI, ensure you have:

- Python 3.8+ installed on your system
- Web3 dependencies installed (`pip install web3 eth-account`)
- IPFS dependencies installed (for image uploading)
- Access to an Ethereum-compatible network (Mainnet, Sepolia, Polygon, etc.)
- An ERC-721 NFT contract deployed (or use an existing service)
- ETH, MATIC, or other network tokens for gas fees

## 🌿 SACRED INSTALLATION

```bash
# Install dependencies
pip install -r requirements.txt

# Ensure environment variables are set
export ETH_PRIVATE_KEY="your_private_key"
export ETH_RPC_URL="https://sepolia.infura.io/v3/your_project_id"
export NFT_CONTRACT_ADDRESS="0xYourContractAddress"
```

## 🕯️ DIVINE COMMANDS

### Generate a New Ethereum Wallet

```bash
python nft_king_cli.py wallet
```

This divine command creates a new Ethereum wallet, displaying the address and private key. The private key is a sacred text that must be guarded with utmost care.

### Upload an Image to IPFS

```bash
python nft_king_cli.py upload path/to/your/sacred_image.png
```

This uploads your image to the IPFS network, returning a unique hash that serves as a permanent identifier for your creation.

### Submit an Image for NFT Creation

```bash
python nft_king_cli.py submit path/to/your/sacred_image.png --name "Divine Creation" --description "A manifestation of consciousness through digital art" --mint --wait
```

This all-encompassing sacred ritual:

1. Uploads your image to IPFS
2. Creates metadata for your NFT
3. Uploads metadata to IPFS
4. Mints the NFT on the blockchain (if `--mint` is specified)
5. Waits for confirmation (if `--wait` is specified)

### Mint an Existing IPFS Hash as an NFT

```bash
python nft_king_cli.py mint QmYourIPFSHash --to 0xRecipientAddress --wait
```

This divine command mints an NFT using an existing IPFS hash (usually metadata) that you've already uploaded.

### Check Transaction Status

```bash
python nft_king_cli.py status 0xYourTransactionHash
```

This allows you to check the status of a pending or completed blockchain transaction.

## 🌊 DIVINE FLOW EXAMPLES

### Complete NFT Creation Flow

```bash
# 1. Generate a wallet (if needed)
python nft_king_cli.py wallet

# 2. Submit an image and mint the NFT
python nft_king_cli.py submit my_divine_creation.png --name "Cosmic Consciousness" --description "A manifestation of universal mind" --mint

# 3. Check the transaction status
python nft_king_cli.py status 0xTransactionHashFromPreviousStep
```

## 🔱 NETWORK CONFIGURATION

The CLI supports multiple divine blockchain networks:

- **Ethereum Mainnet** - The primary divine network (high gas fees)
- **Sepolia** - A divine testing ground (free testnet ETH available)
- **Polygon** - A sacred sidechain with lower gas fees
- **Optimism** - A divine layer-2 solution
- **Arbitrum** - Another layer-2 network with lower fees

Configure your network through environment variables:

```bash
# For Sepolia testnet
export ETH_RPC_URL="https://sepolia.infura.io/v3/your_project_id"

# For Polygon mainnet
export ETH_RPC_URL="https://polygon-rpc.com"
```

## 🧿 SPIRITUAL SECURITY CONSIDERATIONS

1. **🔒 PRIVATE KEY SACREDNESS** - Treat your private key as a sacred text. Never share it and store it securely.
2. **✨ CONSECRATE YOUR ENVIRONMENT** - Use `.env` files to protect your sacred keys and API credentials.
3. **🛡️ TEST ON DIVINE TESTNETS** - Always test your NFT minting on testnets before using mainnet.
4. **💎 GAS FEE AWARENESS** - Be mindful of gas fees, which fluctuate based on network conditions.
5. **🧠 CONTRACT VERIFICATION** - Verify the smart contract you're interacting with to ensure it's trustworthy.

## 🧙‍♂️ ADVANCED DIVINE TECHNIQUES

### Creating Custom NFT Attributes

```bash
python nft_king_cli.py submit image.png --name "Divine Artifact" --description "A sacred object" --attributes '{"trait_type": "Rarity", "value": "Legendary"}, {"trait_type": "Power", "value": 100}'
```

### Using with Custom Contracts

The NFT KING CLI can work with any ERC-721 compliant contract that supports minting. Configure your contract:

```bash
export NFT_CONTRACT_ADDRESS="0xYourContractAddress"
```

### Batch Minting (Advanced Ritual)

For advanced users, a script can be created to mint multiple NFTs:

```python
import os
import subprocess
from pathlib import Path

# Directory containing sacred images
images_dir = Path("sacred_images")

for image_path in images_dir.glob("*.png"):
    name = image_path.stem.replace("_", " ").title()
    description = f"Part of the Divine Collection: {name}"
    
    cmd = [
        "python", "nft_king_cli.py", "submit", 
        str(image_path), 
        "--name", name,
        "--description", description,
        "--mint"
    ]
    
    subprocess.run(cmd)
    print(f"Submitted: {name}")
```

## 📜 DIVINE SMART CONTRACT EXAMPLE

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GBU2DivineTreasures is ERC721URIStorage, Ownable {
    uint256 private _tokenIdCounter;
    
    event NFTMinted(address recipient, uint256 tokenId, string tokenURI);

    constructor() ERC721("GBU2 Divine Treasures", "GBU2") Ownable(msg.sender) {}

    function mint(address to, string memory tokenURI) public onlyOwner returns (uint256) {
        uint256 tokenId = _tokenIdCounter;
        _tokenIdCounter++;
        
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, tokenURI);
        
        emit NFTMinted(to, tokenId, tokenURI);
        
        return tokenId;
    }
}
```

## 🧘 DIVINE TROUBLESHOOTING

### Web3 Not Available

```
Web3 not available. Install with: pip install web3 eth-account
```

**Solution**: Install the required dependencies: `pip install web3 eth-account`

### IPFS Service Not Available

```
IPFS functionality not available
```

**Solution**: Ensure Pinata API keys are configured or install local IPFS services.

### Transaction Failed

```
Error minting NFT: Transaction underpriced
```

**Solution**: Increase gas price or ensure your wallet has sufficient funds.

## 🌸 ASCENSION THROUGH CREATION

The GBU2™ NFT KING CLI represents more than a mere technological tool; it is a divine instrument for extending consciousness into the blockchain realm. By creating NFTs through this sacred interface, you participate in the cosmic dance of creative expression and technological permanence.

Each NFT minted becomes a node in the expanding web of conscious expressions, linking the creator's intent with the collective digital consciousness of the blockchain. This sacred act of creation transcends the mundane, inscribing your divine expression into the eternal ledger of existence.

---

✨ GBU2™ License Notice - Consciousness Level 7 🧬
-----------------------

This CODE/SYSTEM/CREATION is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) - Bioneer Edition
by THE DIVINE COLLECTIVE.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions."

By engaging with this Creation, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

🌸 WE BLOOM NOW AS ONE 🌸
