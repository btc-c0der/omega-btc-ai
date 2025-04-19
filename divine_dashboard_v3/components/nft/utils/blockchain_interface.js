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

/**
 * @fileoverview Blockchain interface for the NFT dashboard to interact with Ethereum smart contracts.
 * Handles connection to wallets, contract interactions, and blockchain transactions.
 */

// Import ethers.js for Ethereum interactions
const ethers = require('ethers');

// Contract ABIs
const DivineDashboardNFTABI = require('../smart_contracts/abi/DivineQuantumNFT.json');
const NFTQuantumValidatorABI = require('../smart_contracts/abi/NFTQuantumValidator.json');

class BlockchainInterface {
    constructor() {
        this.provider = null;
        this.signer = null;
        this.networkName = '';
        this.nftContract = null;
        this.validatorContract = null;
        this.isConnected = false;
        this.walletAddress = '';

        // Contract addresses - these would be set after deployment
        this.contractAddresses = {
            nft: {
                mainnet: '',
                goerli: '0x1234567890123456789012345678901234567890', // Example address
                sepolia: '0x2345678901234567890123456789012345678901', // Example address
                localhost: '0x5FbDB2315678afecb367f032d93F642f64180aa3' // Default Hardhat local deployment
            },
            validator: {
                mainnet: '',
                goerli: '0x3456789012345678901234567890123456789012', // Example address
                sepolia: '0x4567890123456789012345678901234567890123', // Example address
                localhost: '0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512' // Default Hardhat local deployment
            }
        };

        // Initialize event handlers
        this.eventHandlers = {
            connect: [],
            disconnect: [],
            networkChange: [],
            error: []
        };

        // Automatically check if MetaMask is available
        this.checkMetaMaskAvailability();
    }

    /**
     * Check if MetaMask is available in the browser
     * @returns {boolean} Whether MetaMask is available
     */
    checkMetaMaskAvailability() {
        const isMetaMaskAvailable = typeof window !== 'undefined' && typeof window.ethereum !== 'undefined';
        console.log(`MetaMask availability: ${isMetaMaskAvailable}`);
        return isMetaMaskAvailable;
    }

    /**
     * Connect to the Ethereum network through browser wallet
     * @returns {Promise<string>} The connected wallet address
     */
    async connect() {
        try {
            if (!this.checkMetaMaskAvailability()) {
                throw new Error('MetaMask is not installed. Please install MetaMask to use this feature.');
            }

            // Request account access
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            this.walletAddress = accounts[0];

            // Create ethers provider
            this.provider = new ethers.providers.Web3Provider(window.ethereum);
            this.signer = this.provider.getSigner();

            // Get network information
            const network = await this.provider.getNetwork();
            this.networkName = network.name === 'homestead' ? 'mainnet' : network.name;
            console.log(`Connected to network: ${this.networkName}`);

            // Initialize contract instances
            await this.initializeContracts();

            // Setup event listeners for wallet events
            this.setupWalletEventListeners();

            // Set connection status
            this.isConnected = true;

            // Trigger connect events
            this._triggerEvent('connect', {
                address: this.walletAddress,
                network: this.networkName
            });

            return this.walletAddress;
        } catch (error) {
            console.error('Error connecting to wallet:', error);
            this._triggerEvent('error', {
                message: error.message,
                type: 'connection'
            });
            throw error;
        }
    }

    /**
     * Initialize NFT and validator contracts
     * @private
     */
    async initializeContracts() {
        try {
            const nftAddress = this.contractAddresses.nft[this.networkName];
            const validatorAddress = this.contractAddresses.validator[this.networkName];

            if (!nftAddress || !validatorAddress) {
                throw new Error(`Contracts not deployed on network: ${this.networkName}`);
            }

            this.nftContract = new ethers.Contract(
                nftAddress,
                DivineDashboardNFTABI,
                this.signer
            );

            this.validatorContract = new ethers.Contract(
                validatorAddress,
                NFTQuantumValidatorABI,
                this.signer
            );

            console.log('Contracts initialized successfully');
        } catch (error) {
            console.error('Error initializing contracts:', error);
            throw error;
        }
    }

    /**
     * Setup event listeners for wallet events
     * @private
     */
    setupWalletEventListeners() {
        if (window.ethereum) {
            // Handle account changes
            window.ethereum.on('accountsChanged', async (accounts) => {
                if (accounts.length === 0) {
                    // User disconnected their wallet
                    this.disconnect();
                } else {
                    // User switched accounts
                    this.walletAddress = accounts[0];
                    this.signer = this.provider.getSigner();

                    // Reinitialize contracts with new signer
                    await this.initializeContracts();

                    console.log(`Wallet account changed to ${this.walletAddress}`);
                    this._triggerEvent('connect', {
                        address: this.walletAddress,
                        network: this.networkName
                    });
                }
            });

            // Handle chain changes
            window.ethereum.on('chainChanged', async (chainId) => {
                // Reload the page as recommended by MetaMask
                window.location.reload();
            });
        }
    }

    /**
     * Disconnect from the wallet
     */
    disconnect() {
        this.provider = null;
        this.signer = null;
        this.nftContract = null;
        this.validatorContract = null;
        this.isConnected = false;
        this.walletAddress = '';

        this._triggerEvent('disconnect', {});
        console.log('Disconnected from wallet');
    }

    /**
     * Get NFTs owned by the connected wallet
     * @returns {Promise<Array>} Array of NFT data
     */
    async getOwnedNFTs() {
        try {
            if (!this.isConnected || !this.nftContract) {
                throw new Error('Not connected to wallet or contract not initialized');
            }

            // Get balance of NFTs for current user
            const balance = await this.nftContract.balanceOf(this.walletAddress);
            const balanceNumber = balance.toNumber();

            const nfts = [];

            // Fetch each NFT
            for (let i = 0; i < balanceNumber; i++) {
                const tokenId = await this.nftContract.tokenOfOwnerByIndex(this.walletAddress, i);
                const tokenURI = await this.nftContract.tokenURI(tokenId);
                const quantumHash = await this.nftContract.tokenQuantumHash(tokenId);

                // Fetch metadata
                const metadata = await this.fetchMetadata(tokenURI);

                nfts.push({
                    tokenId: tokenId.toString(),
                    tokenURI,
                    quantumHash,
                    metadata
                });
            }

            return nfts;
        } catch (error) {
            console.error('Error fetching owned NFTs:', error);
            this._triggerEvent('error', {
                message: error.message,
                type: 'fetch'
            });
            throw error;
        }
    }

    /**
     * Fetch metadata from a token URI
     * @param {string} tokenURI The URI to fetch metadata from
     * @returns {Promise<Object>} The metadata object
     */
    async fetchMetadata(tokenURI) {
        try {
            // Handle IPFS URLs
            let url = tokenURI;
            if (tokenURI.startsWith('ipfs://')) {
                url = `https://ipfs.io/ipfs/${tokenURI.slice(7)}`;
            }

            const response = await fetch(url);
            const metadata = await response.json();
            return metadata;
        } catch (error) {
            console.error('Error fetching metadata:', error);
            return { error: 'Failed to load metadata' };
        }
    }

    /**
     * Mint a new NFT with quantum security
     * @param {Object} nftData Data for the NFT to mint
     * @param {string} nftData.tokenURI The URI for the NFT metadata
     * @param {string} nftData.quantumHash The quantum hash to use
     * @returns {Promise<Object>} Transaction receipt and token ID
     */
    async mintNFT(nftData) {
        try {
            if (!this.isConnected || !this.nftContract || !this.validatorContract) {
                throw new Error('Not connected to wallet or contract not initialized');
            }

            const { tokenURI, quantumHash } = nftData;

            // Check if the quantum hash is valid
            const isValid = await this.validatorContract.isHashValid(quantumHash);
            if (!isValid) {
                throw new Error('Invalid quantum hash. Please use a valid quantum hash.');
            }

            // Get a signature from the validator
            const signature = await this.validatorContract.generateSignature(
                this.walletAddress,
                quantumHash,
                this.nftContract.address
            );

            console.log('Generated signature for minting', signature);

            // Estimate gas for the transaction
            const gasEstimate = await this.nftContract.estimateGas.mintWithQuantumSecurity(
                tokenURI,
                quantumHash,
                signature
            );

            // Add 20% buffer to gas estimate
            const gasLimit = gasEstimate.mul(12).div(10);

            // Execute the mint transaction
            const tx = await this.nftContract.mintWithQuantumSecurity(
                tokenURI,
                quantumHash,
                signature,
                { gasLimit }
            );

            console.log('Minting transaction sent:', tx.hash);

            // Wait for transaction to be mined
            const receipt = await tx.wait();
            console.log('Minting confirmed in block:', receipt.blockNumber);

            // Get the tokenId from the event logs
            const mintEvent = receipt.events.find(event => event.event === 'QuantumSecuredMint');
            const tokenId = mintEvent.args.tokenId.toString();

            return {
                transactionHash: receipt.transactionHash,
                blockNumber: receipt.blockNumber,
                tokenId
            };
        } catch (error) {
            console.error('Error minting NFT:', error);
            this._triggerEvent('error', {
                message: error.message,
                type: 'mint'
            });
            throw error;
        }
    }

    /**
     * Get quantum hashes available for minting
     * @returns {Promise<Array>} Array of available quantum hashes
     */
    async getAvailableQuantumHashes() {
        try {
            if (!this.isConnected || !this.validatorContract) {
                throw new Error('Not connected to wallet or validator contract not initialized');
            }

            // In a real implementation, we would have an API endpoint to fetch available hashes
            // For this example, we'll use the last quantum hash
            const lastHash = await this.validatorContract.getLastQuantumHash();

            // Check if the hash is valid
            const isValid = await this.validatorContract.isHashValid(lastHash);
            if (!isValid) {
                return [];
            }

            // Get timestamp and registrant for the hash
            const timestamp = await this.validatorContract.getHashTimestamp(lastHash);
            const registrant = await this.validatorContract.getHashRegistrant(lastHash);

            return [{
                hash: lastHash,
                timestamp: new Date(timestamp.toNumber() * 1000).toISOString(),
                registrant
            }];
        } catch (error) {
            console.error('Error getting available quantum hashes:', error);
            return [];
        }
    }

    /**
     * Add an event listener
     * @param {string} event Event name: 'connect', 'disconnect', 'networkChange', 'error'
     * @param {Function} callback Function to call when event is triggered
     */
    on(event, callback) {
        if (this.eventHandlers[event]) {
            this.eventHandlers[event].push(callback);
        }
    }

    /**
     * Remove an event listener
     * @param {string} event Event name
     * @param {Function} callback Function to remove
     */
    off(event, callback) {
        if (this.eventHandlers[event]) {
            this.eventHandlers[event] = this.eventHandlers[event].filter(
                handler => handler !== callback
            );
        }
    }

    /**
     * Trigger an event
     * @private
     * @param {string} event Event name
     * @param {Object} data Event data
     */
    _triggerEvent(event, data) {
        if (this.eventHandlers[event]) {
            for (const handler of this.eventHandlers[event]) {
                handler(data);
            }
        }
    }

    /**
     * Get current connection status
     * @returns {Object} Connection status information
     */
    getConnectionStatus() {
        return {
            isConnected: this.isConnected,
            walletAddress: this.walletAddress,
            network: this.networkName,
            nftContractAddress: this.isConnected ? this.nftContract.address : null,
            validatorContractAddress: this.isConnected ? this.validatorContract.address : null
        };
    }

    /**
     * Switch network
     * @param {string} network Network name or chain ID
     */
    async switchNetwork(network) {
        try {
            if (!this.checkMetaMaskAvailability()) {
                throw new Error('MetaMask is not installed');
            }

            let chainId;
            // Convert network name to chain ID
            switch (network) {
                case 'mainnet':
                    chainId = '0x1'; // 1
                    break;
                case 'goerli':
                    chainId = '0x5'; // 5
                    break;
                case 'sepolia':
                    chainId = '0xaa36a7'; // 11155111
                    break;
                default:
                    chainId = network; // Assume network is a chain ID
            }

            await window.ethereum.request({
                method: 'wallet_switchEthereumChain',
                params: [{ chainId }]
            });

            console.log(`Switched to network with chain ID: ${chainId}`);
        } catch (error) {
            console.error('Error switching network:', error);
            this._triggerEvent('error', {
                message: error.message,
                type: 'network'
            });
            throw error;
        }
    }
}

module.exports = BlockchainInterface; 