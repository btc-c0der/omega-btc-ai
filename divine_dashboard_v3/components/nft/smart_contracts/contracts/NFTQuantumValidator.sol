// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title NFTQuantumValidator
 * @dev Smart contract for validating quantum-resistant hashes and signatures for NFTs
 */
contract NFTQuantumValidator is AccessControl, ReentrancyGuard {
    using ECDSA for bytes32;

    // Role definitions
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant QUANTUM_PROVIDER_ROLE = keccak256("QUANTUM_PROVIDER_ROLE");
    bytes32 public constant VALIDATOR_ROLE = keccak256("VALIDATOR_ROLE");

    // Quantum hash storage
    mapping(bytes32 => bool) private _registeredHashes;
    mapping(bytes32 => uint256) private _hashTimestamps;
    mapping(bytes32 => address) private _hashRegistrants;
    
    // Security parameters
    uint256 public constant MIN_HASH_AGE = 1 hours;
    uint256 public constant MAX_SIGNATURES_PER_DAY = 1000;
    
    // Signature tracking
    uint256 public dailySignatureCount;
    uint256 public lastSignatureReset;
    
    // State tracking
    bytes32 private _lastQuantumHash;
    uint256 private _hashCounter;
    
    // Events
    event HashRegistered(bytes32 indexed hash, address indexed registrant, uint256 timestamp);
    event HashUsed(bytes32 indexed hash, address indexed user, uint256 timestamp);
    event SignatureGenerated(address indexed recipient, bytes32 indexed quantumHash, uint256 timestamp);
    event SecurityParamsUpdated(string paramName, uint256 newValue);
    
    /**
     * @dev Constructor initializes the admin role
     */
    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);
        _grantRole(VALIDATOR_ROLE, msg.sender);
        
        // Initialize state variables
        _lastQuantumHash = keccak256(abi.encodePacked(block.timestamp, msg.sender, "INITIAL_QUANTUM_HASH"));
        lastSignatureReset = block.timestamp;
    }
    
    /**
     * @dev Register a quantum hash from a quantum source
     * @param quantumHash The quantum-resistant hash to register
     */
    function registerQuantumHash(bytes32 quantumHash) external onlyRole(QUANTUM_PROVIDER_ROLE) {
        require(quantumHash != bytes32(0), "Invalid quantum hash");
        require(!_registeredHashes[quantumHash], "Hash already registered");
        
        _registeredHashes[quantumHash] = true;
        _hashTimestamps[quantumHash] = block.timestamp;
        _hashRegistrants[quantumHash] = msg.sender;
        _hashCounter++;
        
        // Update last quantum hash with additional entropy
        _lastQuantumHash = keccak256(abi.encodePacked(_lastQuantumHash, quantumHash, block.number));
        
        emit HashRegistered(quantumHash, msg.sender, block.timestamp);
    }
    
    /**
     * @dev Generate a signature for a quantum hash to be used in NFT minting
     * @param recipient The address that will receive the NFT
     * @param quantumHash The quantum hash to sign
     * @param targetContract The address of the NFT contract
     * @return signature The signature for the NFT contract to verify
     */
    function generateSignature(
        address recipient, 
        bytes32 quantumHash, 
        address targetContract
    ) 
        external 
        onlyRole(VALIDATOR_ROLE) 
        nonReentrant
        returns (bytes memory signature) 
    {
        require(recipient != address(0), "Invalid recipient");
        require(_registeredHashes[quantumHash], "Hash not registered");
        require(block.timestamp >= _hashTimestamps[quantumHash] + MIN_HASH_AGE, "Hash too recent");
        
        // Check and reset daily signature limit
        if (block.timestamp >= lastSignatureReset + 1 days) {
            lastSignatureReset = block.timestamp;
            dailySignatureCount = 0;
        }
        
        require(dailySignatureCount < MAX_SIGNATURES_PER_DAY, "Daily signature limit reached");
        dailySignatureCount++;
        
        // Mark hash as used
        _registeredHashes[quantumHash] = false;
        
        // Create message hash
        bytes32 message = keccak256(abi.encodePacked(recipient, quantumHash, targetContract));
        
        // Sign the message
        bytes32 ethSignedMessageHash = message.toEthSignedMessageHash();
        
        // Use private key of this contract's VALIDATOR_ROLE address (msg.sender) to sign
        // In a real implementation, this would use the private key securely
        // For this example, we're returning the unsigned message hash for the NFT contract to verify
        // against this contract's address
        
        emit SignatureGenerated(recipient, quantumHash, block.timestamp);
        emit HashUsed(quantumHash, recipient, block.timestamp);
        
        return abi.encodePacked(ethSignedMessageHash);
    }
    
    /**
     * @dev Verify a signature for a quantum hash
     * @param recipient The address that will receive the NFT
     * @param quantumHash The quantum hash used
     * @param targetContract The address of the NFT contract
     * @param signature The signature to verify
     * @return True if signature is valid
     */
    function verifySignature(
        address recipient,
        bytes32 quantumHash,
        address targetContract,
        bytes calldata signature
    ) external view returns (bool) {
        bytes32 message = keccak256(abi.encodePacked(recipient, quantumHash, targetContract));
        bytes32 ethSignedMessageHash = message.toEthSignedMessageHash();
        
        address signer = ethSignedMessageHash.recover(signature);
        return hasRole(VALIDATOR_ROLE, signer);
    }
    
    /**
     * @dev Check if a quantum hash is registered and valid
     * @param quantumHash The hash to check
     * @return True if the hash is registered and valid
     */
    function isHashValid(bytes32 quantumHash) external view returns (bool) {
        return _registeredHashes[quantumHash];
    }
    
    /**
     * @dev Get the timestamp when a hash was registered
     * @param quantumHash The hash to check
     * @return Timestamp when the hash was registered
     */
    function getHashTimestamp(bytes32 quantumHash) external view returns (uint256) {
        return _hashTimestamps[quantumHash];
    }
    
    /**
     * @dev Get the address that registered a hash
     * @param quantumHash The hash to check
     * @return Address that registered the hash
     */
    function getHashRegistrant(bytes32 quantumHash) external view returns (address) {
        return _hashRegistrants[quantumHash];
    }
    
    /**
     * @dev Get the last quantum hash in the chain
     * @return The last quantum hash
     */
    function getLastQuantumHash() external view returns (bytes32) {
        return _lastQuantumHash;
    }
    
    /**
     * @dev Get the total number of registered hashes
     * @return The hash counter
     */
    function getHashCount() external view returns (uint256) {
        return _hashCounter;
    }
    
    /**
     * @dev Emergency function to invalidate a hash
     * @param quantumHash The hash to invalidate
     */
    function invalidateHash(bytes32 quantumHash) external onlyRole(ADMIN_ROLE) {
        require(_registeredHashes[quantumHash], "Hash not registered");
        _registeredHashes[quantumHash] = false;
        
        emit HashUsed(quantumHash, msg.sender, block.timestamp);
    }
} 