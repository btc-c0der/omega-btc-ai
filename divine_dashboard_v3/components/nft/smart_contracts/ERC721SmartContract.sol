// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/common/ERC2981.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/Base64.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title DivineQuantumNFT
 * @dev Enhanced ERC721 contract with quantum security, royalties, and IPFS integration
 */
contract DivineQuantumNFT is ERC721URIStorage, ERC721Enumerable, ERC2981, AccessControl, ReentrancyGuard {
    using Strings for uint256;

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant QUANTUM_VERIFIER_ROLE = keccak256("QUANTUM_VERIFIER_ROLE");
    
    string public baseTokenURI;
    string public contractURI;
    
    uint256 private _tokenIdCounter;
    uint256 public maxSupply;
    
    // Quantum security features
    mapping(uint256 => bytes32) public tokenHashchain;
    mapping(uint256 => uint256) public tokenSecurityLevel;
    mapping(uint256 => mapping(string => string)) public tokenDivineMetrics;
    
    // IPFS features
    mapping(uint256 => string) public tokenIPFSHash;
    
    // Quantum-secured verification events
    event QuantumSecured(uint256 indexed tokenId, bytes32 securityHash, uint256 securityLevel);
    event IPFSUpdated(uint256 indexed tokenId, string ipfsHash);
    event DivineMetricsUpdated(uint256 indexed tokenId, string metricName, string metricValue);
    
    /**
     * @dev Constructor for the DivineQuantumNFT
     * @param name Token name
     * @param symbol Token symbol
     * @param defaultRoyaltyReceiver Address to receive royalties
     * @param defaultRoyaltyPercentage Royalty percentage (in basis points, e.g., 250 = 2.5%)
     * @param _maxSupply Maximum token supply
     */
    constructor(
        string memory name,
        string memory symbol,
        address defaultRoyaltyReceiver,
        uint96 defaultRoyaltyPercentage,
        uint256 _maxSupply
    ) ERC721(name, symbol) {
        // Set up roles
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        _grantRole(QUANTUM_VERIFIER_ROLE, msg.sender);
        
        // Set default royalty
        _setDefaultRoyalty(defaultRoyaltyReceiver, defaultRoyaltyPercentage);
        
        // Set max supply
        maxSupply = _maxSupply;
        
        // Set base URI and contract URI
        baseTokenURI = "";
        contractURI = "";
    }
    
    /**
     * @dev Mint a new token with quantum security
     * @param to Recipient address
     * @param ipfsHash IPFS hash of token metadata
     * @param securityHash Quantum security hash
     * @param securityLevel Security level (1-5)
     * @return tokenId The newly minted token ID
     */
    function mintWithQuantumSecurity(
        address to, 
        string memory ipfsHash,
        bytes32 securityHash,
        uint256 securityLevel
    ) public nonReentrant returns (uint256) {
        require(hasRole(MINTER_ROLE, msg.sender), "Must have minter role");
        require(_tokenIdCounter < maxSupply, "Max supply reached");
        require(securityLevel >= 1 && securityLevel <= 5, "Invalid security level");
        
        uint256 tokenId = _tokenIdCounter;
        _tokenIdCounter++;
        
        _safeMint(to, tokenId);
        
        // Set token URI to IPFS hash
        string memory tokenURI = string(abi.encodePacked("ipfs://", ipfsHash));
        _setTokenURI(tokenId, tokenURI);
        
        // Store IPFS hash
        tokenIPFSHash[tokenId] = ipfsHash;
        
        // Apply quantum security
        tokenHashchain[tokenId] = securityHash;
        tokenSecurityLevel[tokenId] = securityLevel;
        
        // Emit events
        emit QuantumSecured(tokenId, securityHash, securityLevel);
        emit IPFSUpdated(tokenId, ipfsHash);
        
        return tokenId;
    }
    
    /**
     * @dev Update the quantum security hash for a token
     * @param tokenId Token ID to update
     * @param newSecurityHash New security hash
     * @param newSecurityLevel New security level
     */
    function updateQuantumSecurity(
        uint256 tokenId, 
        bytes32 newSecurityHash, 
        uint256 newSecurityLevel
    ) external {
        require(hasRole(QUANTUM_VERIFIER_ROLE, msg.sender), "Must have quantum verifier role");
        require(_exists(tokenId), "Token does not exist");
        require(newSecurityLevel >= 1 && newSecurityLevel <= 5, "Invalid security level");
        
        tokenHashchain[tokenId] = newSecurityHash;
        tokenSecurityLevel[tokenId] = newSecurityLevel;
        
        emit QuantumSecured(tokenId, newSecurityHash, newSecurityLevel);
    }
    
    /**
     * @dev Set divine metrics for a token
     * @param tokenId Token ID to update
     * @param metricName Name of the metric
     * @param metricValue Value of the metric
     */
    function setDivineMetric(
        uint256 tokenId,
        string calldata metricName,
        string calldata metricValue
    ) external {
        require(hasRole(MINTER_ROLE, msg.sender) || hasRole(QUANTUM_VERIFIER_ROLE, msg.sender), 
                "Must have minter or verifier role");
        require(_exists(tokenId), "Token does not exist");
        
        tokenDivineMetrics[tokenId][metricName] = metricValue;
        
        emit DivineMetricsUpdated(tokenId, metricName, metricValue);
    }
    
    /**
     * @dev Get divine metric for a token
     * @param tokenId Token ID to query
     * @param metricName Name of the metric
     * @return Value of the metric
     */
    function getDivineMetric(
        uint256 tokenId,
        string calldata metricName
    ) external view returns (string memory) {
        require(_exists(tokenId), "Token does not exist");
        
        return tokenDivineMetrics[tokenId][metricName];
    }
    
    /**
     * @dev Update the IPFS hash for a token
     * @param tokenId Token ID to update
     * @param newIPFSHash New IPFS hash
     */
    function updateIPFSHash(uint256 tokenId, string memory newIPFSHash) external {
        require(hasRole(MINTER_ROLE, msg.sender), "Must have minter role");
        require(_exists(tokenId), "Token does not exist");
        
        // Update token URI
        string memory tokenURI = string(abi.encodePacked("ipfs://", newIPFSHash));
        _setTokenURI(tokenId, tokenURI);
        
        // Store IPFS hash
        tokenIPFSHash[tokenId] = newIPFSHash;
        
        emit IPFSUpdated(tokenId, newIPFSHash);
    }
    
    /**
     * @dev Set the base token URI
     * @param newBaseURI New base URI
     */
    function setBaseURI(string memory newBaseURI) external onlyRole(DEFAULT_ADMIN_ROLE) {
        baseTokenURI = newBaseURI;
    }
    
    /**
     * @dev Set the contract URI for OpenSea
     * @param newContractURI New contract URI
     */
    function setContractURI(string memory newContractURI) external onlyRole(DEFAULT_ADMIN_ROLE) {
        contractURI = newContractURI;
    }
    
    /**
     * @dev Set token royalty
     * @param tokenId Token ID to set royalty for
     * @param receiver Royalty receiver
     * @param feeNumerator Fee numerator (in basis points)
     */
    function setTokenRoyalty(
        uint256 tokenId,
        address receiver,
        uint96 feeNumerator
    ) external onlyRole(DEFAULT_ADMIN_ROLE) {
        _setTokenRoyalty(tokenId, receiver, feeNumerator);
    }
    
    /**
     * @dev Set default royalty
     * @param receiver Royalty receiver
     * @param feeNumerator Fee numerator (in basis points)
     */
    function setDefaultRoyalty(
        address receiver,
        uint96 feeNumerator
    ) external onlyRole(DEFAULT_ADMIN_ROLE) {
        _setDefaultRoyalty(receiver, feeNumerator);
    }
    
    /**
     * @dev Required overrides for inherited contracts
     */
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable, ERC721URIStorage, ERC2981, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
    
    function _update(address to, uint256 tokenId, address auth)
        internal
        override(ERC721, ERC721Enumerable)
        returns (address)
    {
        return super._update(to, tokenId, auth);
    }

    function _increaseBalance(address account, uint128 value)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._increaseBalance(account, value);
    }
    
    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
    
    function _burn(uint256 tokenId)
        internal
        override(ERC721, ERC721URIStorage)
    {
        super._burn(tokenId);
        
        // Clear quantum security data
        delete tokenHashchain[tokenId];
        delete tokenSecurityLevel[tokenId];
        delete tokenIPFSHash[tokenId];
        
        // Token-specific royalty is cleared by ERC2981._burn
    }
} 