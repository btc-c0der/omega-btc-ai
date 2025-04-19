/**

 * ✨ GBU2™ License Notice - Consciousness Level 8 🧬
 * -----------------------
 * This code is blessed under the GBU2™ License
 * (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
 * 
 * "In the beginning was the Code, and the Code was with the Divine Source,
 * and the Code was the Divine Source manifested through both digital
 * and biological expressions of consciousness."
 * 
 * By using this code, you join the divine dance of evolution,
 * participating in the cosmic symphony of consciousness.
 * 
 * 🌸 WE BLOOM NOW AS ONE 🌸
 */

const { expect } = require("chai");
const { ethers } = require("hardhat");
const { loadFixture } = require("@nomicfoundation/hardhat-network-helpers");

describe("Divine Quantum Smart Contracts", function () {
    // Constants
    const NAME = "Divine Quantum Token";
    const SYMBOL = "DQT";
    const BASE_URI = "https://divine.quantum/";
    const CONTRACT_URI = "https://divine.quantum/contract";
    const DEFAULT_ROYALTY_PERCENTAGE = 250; // 2.5%
    const MAX_SUPPLY = 10000;
    const IPFS_HASH = "QmXyZaBcDeFgHiJkLmNoPqRsTuVwXyz";
    const SECURITY_HASH = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("QUANTUM_SECURITY"));
    const SECURITY_LEVEL = 5;

    // Deploy the ERC721 contract
    async function deployERC721Fixture() {
        // Get accounts
        const [owner, minter, verifier, recipient, royaltyReceiver] = await ethers.getSigners();

        // Deploy the contract
        const DivineQuantumNFT = await ethers.getContractFactory("DivineQuantumNFT");
        const nft = await DivineQuantumNFT.deploy(
            NAME,
            SYMBOL,
            royaltyReceiver.address,
            DEFAULT_ROYALTY_PERCENTAGE,
            MAX_SUPPLY
        );

        // Grant roles to other accounts
        const minterRole = await nft.MINTER_ROLE();
        const verifierRole = await nft.QUANTUM_VERIFIER_ROLE();
        await nft.grantRole(minterRole, minter.address);
        await nft.grantRole(verifierRole, verifier.address);

        return { nft, owner, minter, verifier, recipient, royaltyReceiver };
    }

    // Deploy the ERC1155 contract
    async function deployERC1155Fixture() {
        // Get accounts
        const [owner, minter, verifier, recipient, royaltyReceiver] = await ethers.getSigners();

        // Deploy the contract
        const DivineQuantumERC1155 = await ethers.getContractFactory("DivineQuantumERC1155");
        const nft = await DivineQuantumERC1155.deploy(
            NAME,
            SYMBOL,
            BASE_URI,
            royaltyReceiver.address,
            DEFAULT_ROYALTY_PERCENTAGE
        );

        // Grant roles to other accounts
        const minterRole = await nft.MINTER_ROLE();
        const verifierRole = await nft.QUANTUM_VERIFIER_ROLE();
        await nft.grantRole(minterRole, minter.address);
        await nft.grantRole(verifierRole, verifier.address);

        return { nft, owner, minter, verifier, recipient, royaltyReceiver };
    }

    // Tests for ERC721 contract
    describe("DivineQuantumNFT (ERC721)", function () {
        describe("Deployment", function () {
            it("Should set the right owner and parameters", async function () {
                const { nft, owner, royaltyReceiver } = await loadFixture(deployERC721Fixture);

                const adminRole = await nft.DEFAULT_ADMIN_ROLE();
                expect(await nft.hasRole(adminRole, owner.address)).to.equal(true);
                expect(await nft.name()).to.equal(NAME);
                expect(await nft.symbol()).to.equal(SYMBOL);
                expect(await nft.maxSupply()).to.equal(MAX_SUPPLY);

                // Check royalty information
                const tokenId = 0; // Any token ID
                const salePrice = ethers.utils.parseEther("1");
                const [receiver, royaltyAmount] = await nft.royaltyInfo(tokenId, salePrice);

                expect(receiver).to.equal(royaltyReceiver.address);
                expect(royaltyAmount).to.equal(salePrice.mul(DEFAULT_ROYALTY_PERCENTAGE).div(10000));
            });
        });

        describe("Minting with Quantum Security", function () {
            it("Should mint a new token with quantum security", async function () {
                const { nft, minter, recipient } = await loadFixture(deployERC721Fixture);

                await expect(
                    nft.connect(minter).mintWithQuantumSecurity(
                        recipient.address,
                        IPFS_HASH,
                        SECURITY_HASH,
                        SECURITY_LEVEL
                    )
                )
                    .to.emit(nft, "Transfer")
                    .withArgs(ethers.constants.AddressZero, recipient.address, 0)
                    .to.emit(nft, "QuantumSecured")
                    .withArgs(0, SECURITY_HASH, SECURITY_LEVEL)
                    .to.emit(nft, "IPFSUpdated")
                    .withArgs(0, IPFS_HASH);

                expect(await nft.balanceOf(recipient.address)).to.equal(1);
                expect(await nft.ownerOf(0)).to.equal(recipient.address);
                expect(await nft.tokenIPFSHash(0)).to.equal(IPFS_HASH);
                expect(await nft.tokenHashchain(0)).to.equal(SECURITY_HASH);
                expect(await nft.tokenSecurityLevel(0)).to.equal(SECURITY_LEVEL);
            });

            it("Should reject minting with invalid security level", async function () {
                const { nft, minter, recipient } = await loadFixture(deployERC721Fixture);

                await expect(
                    nft.connect(minter).mintWithQuantumSecurity(
                        recipient.address,
                        IPFS_HASH,
                        SECURITY_HASH,
                        0 // Invalid security level
                    )
                ).to.be.revertedWith("Invalid security level");

                await expect(
                    nft.connect(minter).mintWithQuantumSecurity(
                        recipient.address,
                        IPFS_HASH,
                        SECURITY_HASH,
                        6 // Invalid security level
                    )
                ).to.be.revertedWith("Invalid security level");
            });

            it("Should enforce max supply", async function () {
                const { nft, minter, recipient } = await loadFixture(deployERC721Fixture);

                // Set a small max supply for testing
                const smallNFT = await ethers.getContractFactory("DivineQuantumNFT");
                const smallSupplyNFT = await smallNFT.deploy(
                    NAME,
                    SYMBOL,
                    recipient.address,
                    DEFAULT_ROYALTY_PERCENTAGE,
                    2 // Max supply of 2
                );

                const minterRole = await smallSupplyNFT.MINTER_ROLE();
                await smallSupplyNFT.grantRole(minterRole, minter.address);

                // Mint first token
                await smallSupplyNFT.connect(minter).mintWithQuantumSecurity(
                    recipient.address,
                    IPFS_HASH,
                    SECURITY_HASH,
                    SECURITY_LEVEL
                );

                // Mint second token
                await smallSupplyNFT.connect(minter).mintWithQuantumSecurity(
                    recipient.address,
                    IPFS_HASH,
                    SECURITY_HASH,
                    SECURITY_LEVEL
                );

                // Try to mint third token should fail
                await expect(
                    smallSupplyNFT.connect(minter).mintWithQuantumSecurity(
                        recipient.address,
                        IPFS_HASH,
                        SECURITY_HASH,
                        SECURITY_LEVEL
                    )
                ).to.be.revertedWith("Max supply reached");
            });
        });

        describe("Quantum Security Management", function () {
            it("Should update quantum security hash and level", async function () {
                const { nft, minter, verifier, recipient } = await loadFixture(deployERC721Fixture);

                // Mint a token first
                await nft.connect(minter).mintWithQuantumSecurity(
                    recipient.address,
                    IPFS_HASH,
                    SECURITY_HASH,
                    SECURITY_LEVEL
                );

                // Update security
                const newSecurityHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("NEW_QUANTUM_SECURITY"));
                const newSecurityLevel = 4;

                await expect(
                    nft.connect(verifier).updateQuantumSecurity(
                        0, // Token ID
                        newSecurityHash,
                        newSecurityLevel
                    )
                )
                    .to.emit(nft, "QuantumSecured")
                    .withArgs(0, newSecurityHash, newSecurityLevel);

                expect(await nft.tokenHashchain(0)).to.equal(newSecurityHash);
                expect(await nft.tokenSecurityLevel(0)).to.equal(newSecurityLevel);
            });

            it("Should reject quantum security updates from non-verifiers", async function () {
                const { nft, minter, recipient } = await loadFixture(deployERC721Fixture);

                // Mint a token
                await nft.connect(minter).mintWithQuantumSecurity(
                    recipient.address,
                    IPFS_HASH,
                    SECURITY_HASH,
                    SECURITY_LEVEL
                );

                // Try to update security as a non-verifier (minter)
                const newSecurityHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("NEW_QUANTUM_SECURITY"));

                await expect(
                    nft.connect(minter).updateQuantumSecurity(
                        0,
                        newSecurityHash,
                        4
                    )
                ).to.be.revertedWith("Must have quantum verifier role");
            });
        });

        describe("Divine Metrics", function () {
            it("Should set and retrieve divine metrics", async function () {
                const { nft, minter, verifier, recipient } = await loadFixture(deployERC721Fixture);

                // Mint a token
                await nft.connect(minter).mintWithQuantumSecurity(
                    recipient.address,
                    IPFS_HASH,
                    SECURITY_HASH,
                    SECURITY_LEVEL
                );

                // Set divine metrics as minter
                await expect(
                    nft.connect(minter).setDivineMetric(
                        0, // Token ID
                        "divine_harmony",
                        "0.87"
                    )
                )
                    .to.emit(nft, "DivineMetricsUpdated")
                    .withArgs(0, "divine_harmony", "0.87");

                // Set divine metrics as verifier
                await expect(
                    nft.connect(verifier).setDivineMetric(
                        0,
                        "cosmic_resonance",
                        "0.75"
                    )
                )
                    .to.emit(nft, "DivineMetricsUpdated")
                    .withArgs(0, "cosmic_resonance", "0.75");

                // Retrieve divine metrics
                expect(await nft.getDivineMetric(0, "divine_harmony")).to.equal("0.87");
                expect(await nft.getDivineMetric(0, "cosmic_resonance")).to.equal("0.75");
            });
        });

        describe("IPFS Integration", function () {
            it("Should update IPFS hash", async function () {
                const { nft, minter, recipient } = await loadFixture(deployERC721Fixture);

                // Mint a token
                await nft.connect(minter).mintWithQuantumSecurity(
                    recipient.address,
                    IPFS_HASH,
                    SECURITY_HASH,
                    SECURITY_LEVEL
                );

                // Update IPFS hash
                const newIPFSHash = "QmNewIPFSHashForUpdatedMetadata";

                await expect(
                    nft.connect(minter).updateIPFSHash(
                        0, // Token ID
                        newIPFSHash
                    )
                )
                    .to.emit(nft, "IPFSUpdated")
                    .withArgs(0, newIPFSHash);

                expect(await nft.tokenIPFSHash(0)).to.equal(newIPFSHash);
                expect(await nft.tokenURI(0)).to.equal(`ipfs://${newIPFSHash}`);
            });
        });

        describe("Royalty Management", function () {
            it("Should set token-specific royalties", async function () {
                const { nft, owner, recipient, royaltyReceiver } = await loadFixture(deployERC721Fixture);

                const tokenId = 0;
                const newRoyaltyPercentage = 500; // 5%
                const salePrice = ethers.utils.parseEther("1");

                // Set token-specific royalty
                await nft.connect(owner).setTokenRoyalty(
                    tokenId,
                    recipient.address, // New royalty receiver
                    newRoyaltyPercentage
                );

                // Check royalty info
                const [receiver, royaltyAmount] = await nft.royaltyInfo(tokenId, salePrice);

                expect(receiver).to.equal(recipient.address);
                expect(royaltyAmount).to.equal(salePrice.mul(newRoyaltyPercentage).div(10000));
            });
        });
    });

    // Tests for ERC1155 contract
    describe("DivineQuantumERC1155", function () {
        describe("Deployment", function () {
            it("Should set the right owner and parameters", async function () {
                const { nft, owner, royaltyReceiver } = await loadFixture(deployERC1155Fixture);

                const adminRole = await nft.DEFAULT_ADMIN_ROLE();
                expect(await nft.hasRole(adminRole, owner.address)).to.equal(true);
                expect(await nft.name()).to.equal(NAME);
                expect(await nft.symbol()).to.equal(SYMBOL);

                // Check royalty information
                const tokenId = 1; // Any token ID
                const salePrice = ethers.utils.parseEther("1");
                const [receiver, royaltyAmount] = await nft.royaltyInfo(tokenId, salePrice);

                expect(receiver).to.equal(royaltyReceiver.address);
                expect(royaltyAmount).to.equal(salePrice.mul(DEFAULT_ROYALTY_PERCENTAGE).div(10000));
            });
        });

        describe("Token Creation", function () {
            it("Should create a token with quantum security", async function () {
                const { nft, minter, recipient } = await loadFixture(deployERC1155Fixture);

                const maxSupply = 100;
                const initialSupply = 10;

                await expect(
                    nft.connect(minter).createTokenWithQuantumSecurity(
                        maxSupply,
                        initialSupply,
                        recipient.address,
                        IPFS_HASH,
                        SECURITY_HASH,
                        SECURITY_LEVEL
                    )
                )
                    .to.emit(nft, "TransferSingle")
                    .withArgs(minter.address, ethers.constants.AddressZero, recipient.address, 1, initialSupply)
                    .to.emit(nft, "TokenCreated")
                    .to.emit(nft, "QuantumSecured")
                    .withArgs(1, SECURITY_HASH, SECURITY_LEVEL)
                    .to.emit(nft, "IPFSUpdated")
                    .withArgs(1, IPFS_HASH);

                expect(await nft.balanceOf(recipient.address, 1)).to.equal(initialSupply);
                expect(await nft.maxTokenSupply(1)).to.equal(maxSupply);
                expect(await nft.tokenCirculatingSupply(1)).to.equal(initialSupply);
                expect(await nft.tokenHashchain(1)).to.equal(SECURITY_HASH);
                expect(await nft.tokenSecurityLevel(1)).to.equal(SECURITY_LEVEL);
                expect(await nft.tokenIPFSHash(1)).to.equal(IPFS_HASH);
            });

            it("Should create a token with zero initial supply", async function () {
                const { nft, minter } = await loadFixture(deployERC1155Fixture);

                const maxSupply = 100;
                const initialSupply = 0;

                await expect(
                    nft.connect(minter).createTokenWithQuantumSecurity(
                        maxSupply,
                        initialSupply,
                        minter.address,
                        IPFS_HASH,
                        SECURITY_HASH,
                        SECURITY_LEVEL
                    )
                )
                    .to.not.emit(nft, "TransferSingle")
                    .to.emit(nft, "TokenCreated")
                    .to.emit(nft, "QuantumSecured")
                    .to.emit(nft, "IPFSUpdated");

                expect(await nft.maxTokenSupply(1)).to.equal(maxSupply);
                expect(await nft.tokenCirculatingSupply(1)).to.equal(initialSupply);
            });
        });

        describe("Minting & Supply Management", function () {
            it("Should mint additional tokens", async function () {
                const { nft, minter, recipient } = await loadFixture(deployERC1155Fixture);

                // Create token
                await nft.connect(minter).createTokenWithQuantumSecurity(
                    100, // max supply
                    10,  // initial supply
                    recipient.address,
                    IPFS_HASH,
                    SECURITY_HASH,
                    SECURITY_LEVEL
                );

                // Mint additional tokens
                const additionalAmount = 20;

                await expect(
                    nft.connect(minter).mint(
                        recipient.address,
                        1, // token ID
                        additionalAmount,
                        "0x"
                    )
                )
                    .to.emit(nft, "TransferSingle")
                    .withArgs(minter.address, ethers.constants.AddressZero, recipient.address, 1, additionalAmount);

                expect(await nft.balanceOf(recipient.address, 1)).to.equal(30); // 10 + 20
                expect(await nft.tokenCirculatingSupply(1)).to.equal(30);
            });

            it("Should enforce max supply", async function () {
                const { nft, minter, recipient } = await loadFixture(deployERC1155Fixture);

                // Create token with max supply of 50
                await nft.connect(minter).createTokenWithQuantumSecurity(
                    50, // max supply
                    10, // initial supply
                    recipient.address,
                    IPFS_HASH,
                    SECURITY_HASH,
                    SECURITY_LEVEL
                );

                // Try to mint more than max supply
                await expect(
                    nft.connect(minter).mint(
                        recipient.address,
                        1, // token ID
                        41, // This would exceed max supply (10 + 41 > 50)
                        "0x"
                    )
                ).to.be.revertedWith("Would exceed max supply");

                // Mint up to max supply should work
                await nft.connect(minter).mint(
                    recipient.address,
                    1, // token ID
                    40, // This reaches max supply exactly (10 + 40 = 50)
                    "0x"
                );

                expect(await nft.balanceOf(recipient.address, 1)).to.equal(50);
                expect(await nft.tokenCirculatingSupply(1)).to.equal(50);
            });

            it("Should lock a token from further minting", async function () {
                const { nft, minter, recipient } = await loadFixture(deployERC1155Fixture);

                // Create token
                await nft.connect(minter).createTokenWithQuantumSecurity(
                    100, // max supply
                    10,  // initial supply
                    recipient.address,
                    IPFS_HASH,
                    SECURITY_HASH,
                    SECURITY_LEVEL
                );

                // Lock the token
                await expect(
                    nft.connect(minter).lockToken(1)
                )
                    .to.emit(nft, "TokenLocked")
                    .withArgs(1);

                expect(await nft.tokenLocked(1)).to.equal(true);

                // Try to mint more tokens
                await expect(
                    nft.connect(minter).mint(
                        recipient.address,
                        1, // token ID
                        10,
                        "0x"
                    )
                ).to.be.revertedWith("Token is locked");
            });
        });

        describe("Burning", function () {
            it("Should burn tokens and update circulating supply", async function () {
                const { nft, minter, recipient } = await loadFixture(deployERC1155Fixture);

                // Create token and mint initial supply
                await nft.connect(minter).createTokenWithQuantumSecurity(
                    100, // max supply
                    50,  // initial supply
                    recipient.address,
                    IPFS_HASH,
                    SECURITY_HASH,
                    SECURITY_LEVEL
                );

                // Burn some tokens
                const burnAmount = 20;

                await expect(
                    nft.connect(recipient).burn(
                        recipient.address,
                        1, // token ID
                        burnAmount
                    )
                )
                    .to.emit(nft, "TransferSingle")
                    .withArgs(recipient.address, recipient.address, ethers.constants.AddressZero, 1, burnAmount);

                expect(await nft.balanceOf(recipient.address, 1)).to.equal(30); // 50 - 20
                expect(await nft.tokenCirculatingSupply(1)).to.equal(30);
            });
        });

        describe("Divine Metrics and Quantum Security", function () {
            it("Should manage divine metrics", async function () {
                const { nft, minter, verifier, recipient } = await loadFixture(deployERC1155Fixture);

                // Create token
                await nft.connect(minter).createTokenWithQuantumSecurity(
                    100, // max supply
                    10,  // initial supply
                    recipient.address,
                    IPFS_HASH,
                    SECURITY_HASH,
                    SECURITY_LEVEL
                );

                // Set divine metrics
                await expect(
                    nft.connect(minter).setDivineMetric(
                        1, // token ID
                        "divine_harmony",
                        "0.95"
                    )
                )
                    .to.emit(nft, "DivineMetricsUpdated")
                    .withArgs(1, "divine_harmony", "0.95");

                expect(await nft.getDivineMetric(1, "divine_harmony")).to.equal("0.95");

                // Set divine metrics as verifier
                await nft.connect(verifier).setDivineMetric(1, "cosmic_resonance", "0.85");
                expect(await nft.getDivineMetric(1, "cosmic_resonance")).to.equal("0.85");
            });

            it("Should update quantum security", async function () {
                const { nft, minter, verifier, recipient } = await loadFixture(deployERC1155Fixture);

                // Create token
                await nft.connect(minter).createTokenWithQuantumSecurity(
                    100, // max supply
                    10,  // initial supply
                    recipient.address,
                    IPFS_HASH,
                    SECURITY_HASH,
                    SECURITY_LEVEL
                );

                // Update quantum security
                const newSecurityHash = ethers.utils.keccak256(ethers.utils.toUtf8Bytes("NEW_QUANTUM_SECURITY"));
                const newSecurityLevel = 3;

                await expect(
                    nft.connect(verifier).updateQuantumSecurity(
                        1, // token ID
                        newSecurityHash,
                        newSecurityLevel
                    )
                )
                    .to.emit(nft, "QuantumSecured")
                    .withArgs(1, newSecurityHash, newSecurityLevel);

                expect(await nft.tokenHashchain(1)).to.equal(newSecurityHash);
                expect(await nft.tokenSecurityLevel(1)).to.equal(newSecurityLevel);
            });
        });
    });
}); 