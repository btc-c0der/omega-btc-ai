// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155URIStorage.sol";
import "@openzeppelin/contracts/token/common/ERC2981.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title DivineQuantumERC1155
 * @dev Enhanced ERC1155 contract with quantum security, royalties, and IPFS integration
 */
contract DivineQuantumERC1155 is ERC1155URIStorage, ERC2981, AccessControl, ReentrancyGuard {
    using Strings for uint256;
    using Counters for Counters.Counter;

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant QUANTUM_VERIFIER_ROLE = keccak256("QUANTUM_VERIFIER_ROLE");
    
    string public name;
    string public symbol;
    string public contractURI;
    
    Counters.Counter private _tokenIdTracker;
    
    // Collection metadata
    mapping(uint256 => uint256) public maxTokenSupply;
    mapping(uint256 => uint256) public tokenCirculatingSupply;
    mapping(uint256 => bool) public tokenLocked;
    
    // Quantum security features
    mapping(uint256 => bytes32) public tokenHashchain;
    mapping(uint256 => uint256) public tokenSecurityLevel;
    mapping(uint256 => mapping(string => string)) public tokenDivineMetrics;
    
    // IPFS features
    mapping(uint256 => string) public tokenIPFSHash;
    
    // Events
    event TokenCreated(uint256 indexed tokenId, uint256 maxSupply, string uri);
    event QuantumSecured(uint256 indexed tokenId, bytes32 securityHash, uint256 securityLevel);
    event IPFSUpdated(uint256 indexed tokenId, string ipfsHash);
    event DivineMetricsUpdated(uint256 indexed tokenId, string metricName, string metricValue);
    event TokenLocked(uint256 indexed tokenId);
    
    /**
     * @dev Constructor
     * @param _name Collection name
     * @param _symbol Collection symbol
     * @param _uri Base URI for token metadata
     * @param defaultRoyaltyReceiver Default royalty recipient
     * @param defaultRoyaltyPercentage Default royalty percentage (in basis points)
     */
    constructor(
        string memory _name,
        string memory _symbol,
        string memory _uri,
        address defaultRoyaltyReceiver,
        uint96 defaultRoyaltyPercentage
    ) ERC1155(_uri) {
        name = _name;
        symbol = _symbol;
        
        // Set up roles
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        _grantRole(QUANTUM_VERIFIER_ROLE, msg.sender);
        
        // Set default royalty
        _setDefaultRoyalty(defaultRoyaltyReceiver, defaultRoyaltyPercentage);
    }
    
    /**
     * @dev Create a new token type with quantum security
     * @param maxSupply Maximum supply of this token
     * @param initialSupply Initial amount to mint
     * @param recipient Recipient of initial tokens
     * @param ipfsHash IPFS hash for token metadata
     * @param securityHash Quantum security hash
     * @param securityLevel Security level (1-5)
     * @return New token ID
     */
    function createTokenWithQuantumSecurity(
        uint256 maxSupply,
        uint256 initialSupply,
        address recipient,
        string memory ipfsHash,
        bytes32 securityHash,
        uint256 securityLevel
    ) external nonReentrant returns (uint256) {
        require(hasRole(MINTER_ROLE, msg.sender), "Must have minter role");
        require(securityLevel >= 1 && securityLevel <= 5, "Invalid security level");
        require(initialSupply <= maxSupply, "Initial supply exceeds max supply");
        
        // Get new token ID
        _tokenIdTracker.increment();
        uint256 tokenId = _tokenIdTracker.current();
        
        // Set max supply
        maxTokenSupply[tokenId] = maxSupply;
        
        // Set token URI to IPFS hash
        string memory tokenURI = string(abi.encodePacked("ipfs://", ipfsHash));
        _setURI(tokenId, tokenURI);
        
        // Store IPFS hash
        tokenIPFSHash[tokenId] = ipfsHash;
        
        // Apply quantum security
        tokenHashchain[tokenId] = securityHash;
        tokenSecurityLevel[tokenId] = securityLevel;
        
        // Mint initial supply
        if (initialSupply > 0) {
            _mint(recipient, tokenId, initialSupply, "");
            tokenCirculatingSupply[tokenId] = initialSupply;
        }
        
        // Emit events
        emit TokenCreated(tokenId, maxSupply, tokenURI);
        emit QuantumSecured(tokenId, securityHash, securityLevel);
        emit IPFSUpdated(tokenId, ipfsHash);
        
        return tokenId;
    }
    
    /**
     * @dev Mint additional tokens
     * @param to Recipient address
     * @param tokenId Token ID to mint
     * @param amount Amount to mint
     * @param data Additional data to pass to receiver
     */
    function mint(
        address to,
        uint256 tokenId,
        uint256 amount,
        bytes memory data
    ) external nonReentrant {
        require(hasRole(MINTER_ROLE, msg.sender), "Must have minter role");
        require(amount > 0, "Amount must be greater than zero");
        require(!tokenLocked[tokenId], "Token is locked");
        require(tokenCirculatingSupply[tokenId] + amount <= maxTokenSupply[tokenId], 
                "Would exceed max supply");
        
        _mint(to, tokenId, amount, data);
        tokenCirculatingSupply[tokenId] += amount;
    }
    
    /**
     * @dev Mint batch of tokens
     * @param to Recipient address
     * @param tokenIds Array of token IDs
     * @param amounts Array of amounts
     * @param data Additional data
     */
    function mintBatch(
        address to,
        uint256[] memory tokenIds,
        uint256[] memory amounts,
        bytes memory data
    ) external nonReentrant {
        require(hasRole(MINTER_ROLE, msg.sender), "Must have minter role");
        require(tokenIds.length == amounts.length, "Arrays length mismatch");
        
        for (uint256 i = 0; i < tokenIds.length; i++) {
            uint256 tokenId = tokenIds[i];
            uint256 amount = amounts[i];
            
            require(!tokenLocked[tokenId], "Token is locked");
            require(tokenCirculatingSupply[tokenId] + amount <= maxTokenSupply[tokenId], 
                    "Would exceed max supply");
                    
            tokenCirculatingSupply[tokenId] += amount;
        }
        
        _mintBatch(to, tokenIds, amounts, data);
    }
    
    /**
     * @dev Burn tokens
     * @param account Account to burn from
     * @param tokenId Token ID to burn
     * @param amount Amount to burn
     */
    function burn(
        address account,
        uint256 tokenId,
        uint256 amount
    ) external {
        require(
            account == msg.sender || isApprovedForAll(account, msg.sender),
            "Caller is not owner nor approved"
        );
        
        _burn(account, tokenId, amount);
        tokenCirculatingSupply[tokenId] -= amount;
    }
    
    /**
     * @dev Burn batch of tokens
     * @param account Account to burn from
     * @param tokenIds Array of token IDs
     * @param amounts Array of amounts
     */
    function burnBatch(
        address account,
        uint256[] memory tokenIds,
        uint256[] memory amounts
    ) external {
        require(
            account == msg.sender || isApprovedForAll(account, msg.sender),
            "Caller is not owner nor approved"
        );
        
        _burnBatch(account, tokenIds, amounts);
        
        for (uint256 i = 0; i < tokenIds.length; i++) {
            tokenCirculatingSupply[tokenIds[i]] -= amounts[i];
        }
    }
    
    /**
     * @dev Lock a token from further minting
     * @param tokenId Token ID to lock
     */
    function lockToken(uint256 tokenId) external onlyRole(MINTER_ROLE) {
        require(!tokenLocked[tokenId], "Token already locked");
        tokenLocked[tokenId] = true;
        emit TokenLocked(tokenId);
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
    ) external onlyRole(QUANTUM_VERIFIER_ROLE) {
        require(_tokenIdTracker.current() >= tokenId && tokenId > 0, "Token does not exist");
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
        require(
            hasRole(MINTER_ROLE, msg.sender) || hasRole(QUANTUM_VERIFIER_ROLE, msg.sender),
            "Must have minter or verifier role"
        );
        require(_tokenIdTracker.current() >= tokenId && tokenId > 0, "Token does not exist");
        
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
        require(_tokenIdTracker.current() >= tokenId && tokenId > 0, "Token does not exist");
        
        return tokenDivineMetrics[tokenId][metricName];
    }
    
    /**
     * @dev Update the IPFS hash for a token
     * @param tokenId Token ID to update
     * @param newIPFSHash New IPFS hash
     */
    function updateIPFSHash(
        uint256 tokenId,
        string memory newIPFSHash
    ) external onlyRole(MINTER_ROLE) {
        require(_tokenIdTracker.current() >= tokenId && tokenId > 0, "Token does not exist");
        
        // Update token URI
        string memory tokenURI = string(abi.encodePacked("ipfs://", newIPFSHash));
        _setURI(tokenId, tokenURI);
        
        // Store IPFS hash
        tokenIPFSHash[tokenId] = newIPFSHash;
        
        emit IPFSUpdated(tokenId, newIPFSHash);
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
        override(ERC1155, ERC2981, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
} 