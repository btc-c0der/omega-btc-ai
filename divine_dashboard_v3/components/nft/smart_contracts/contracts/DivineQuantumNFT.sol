// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/common/ERC2981.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/Base64.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

/**
 * @title DivineQuantumNFT
 * @dev Implementation of an ERC721 token with quantum security features
 */
contract DivineQuantumNFT is ERC721URIStorage, ERC721Enumerable, ERC2981, AccessControl {
    using Strings for uint256;
    using ECDSA for bytes32;

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    
    address public immutable quantumValidator;
    
    // Base URI for metadata
    string private _baseTokenURI;
    
    // Fallback image data for on-chain rendering if IPFS is unavailable
    string private _fallbackImageData;
    
    // Counter for token IDs
    uint256 private _nextTokenId;
    
    // Maximum supply
    uint256 public maxSupply;
    
    // Mapping from token ID to quantum hash
    mapping(uint256 => bytes32) private _tokenQuantumHashes;
    
    // Events
    event QuantumMint(address indexed to, uint256 indexed tokenId, bytes32 quantumHash);
    event BaseURIUpdated(string newBaseURI);
    event MaxSupplyUpdated(uint256 newMaxSupply);
    event FallbackImageUpdated(string newFallbackImage);
    
    /**
     * @dev Constructor
     * @param name_ Name of the NFT collection
     * @param symbol_ Symbol of the NFT collection
     * @param quantumValidator_ Address of the quantum validator contract
     * @param baseURI_ Base URI for token metadata
     * @param maxSupply_ Maximum number of tokens that can be minted
     */
    constructor(
        string memory name_,
        string memory symbol_,
        address quantumValidator_,
        string memory baseURI_,
        uint256 maxSupply_
    ) ERC721(name_, symbol_) {
        require(quantumValidator_ != address(0), "Invalid validator address");
        
        quantumValidator = quantumValidator_;
        _baseTokenURI = baseURI_;
        maxSupply = maxSupply_;
        
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, msg.sender);
        
        // Set default royalty to 5%
        _setDefaultRoyalty(msg.sender, 500);
    }
    
    /**
     * @dev Mint a new token with quantum security
     * @param to Address to mint the token to
     * @param quantumHash Hash from the quantum validator
     * @param validatorSignature Signature from the quantum validator
     * @param uri Token URI for metadata
     */
    function mintWithQuantumSecurity(
        address to,
        bytes32 quantumHash,
        bytes calldata validatorSignature,
        string memory uri
    ) external onlyRole(MINTER_ROLE) {
        require(_nextTokenId < maxSupply, "Max supply reached");
        
        // Verify the signature from the quantum validator
        bytes32 message = keccak256(abi.encodePacked(to, quantumHash, address(this)));
        bytes32 ethSignedMessage = message.toEthSignedMessageHash();
        address recoveredSigner = ethSignedMessage.recover(validatorSignature);
        
        require(recoveredSigner == quantumValidator, "Invalid quantum signature");
        
        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
        _tokenQuantumHashes[tokenId] = quantumHash;
        
        emit QuantumMint(to, tokenId, quantumHash);
    }
    
    /**
     * @dev Update the base URI for token metadata
     * @param newBaseURI New base URI
     */
    function setBaseURI(string memory newBaseURI) external onlyRole(ADMIN_ROLE) {
        _baseTokenURI = newBaseURI;
        emit BaseURIUpdated(newBaseURI);
    }
    
    /**
     * @dev Update the maximum supply
     * @param newMaxSupply New maximum supply
     */
    function setMaxSupply(uint256 newMaxSupply) external onlyRole(ADMIN_ROLE) {
        require(newMaxSupply >= _nextTokenId, "New max supply must be >= current supply");
        maxSupply = newMaxSupply;
        emit MaxSupplyUpdated(newMaxSupply);
    }
    
    /**
     * @dev Set the fallback image data for on-chain rendering
     * @param imageData SVG or Base64 encoded image data
     */
    function setFallbackImage(string memory imageData) external onlyRole(ADMIN_ROLE) {
        _fallbackImageData = imageData;
        emit FallbackImageUpdated(imageData);
    }
    
    /**
     * @dev Get the quantum hash for a token
     * @param tokenId Token ID
     * @return quantum hash
     */
    function getTokenQuantumHash(uint256 tokenId) external view returns (bytes32) {
        require(_exists(tokenId), "Token does not exist");
        return _tokenQuantumHashes[tokenId];
    }
    
    /**
     * @dev Generate on-chain fallback token URI if IPFS is unavailable
     * @param tokenId Token ID
     * @return on-chain token URI
     */
    function generateFallbackTokenURI(uint256 tokenId) public view returns (string memory) {
        require(_exists(tokenId), "Token does not exist");
        
        bytes memory dataURI = abi.encodePacked(
            '{',
                '"name": "Divine Quantum NFT #', tokenId.toString(), '",',
                '"description": "A quantum-secured NFT on the Divine platform",',
                '"image": "', _fallbackImageData, '",',
                '"attributes": [',
                    '{',
                        '"trait_type": "Quantum Hash",',
                        '"value": "', uint256(uint160(_tokenQuantumHashes[tokenId])).toHexString(), '"',
                    '}',
                ']',
            '}'
        );
        
        return string(
            abi.encodePacked(
                "data:application/json;base64,",
                Base64.encode(dataURI)
            )
        );
    }
    
    /**
     * @dev Internal function to get the base URI
     */
    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }
    
    // The following functions are overrides required by Solidity
    
    function _update(address to, uint256 tokenId, address auth) 
        internal override(ERC721, ERC721Enumerable) returns (address) 
    {
        return super._update(to, tokenId, auth);
    }
    
    function _increaseBalance(address account, uint128 amount) 
        internal override(ERC721, ERC721Enumerable) 
    {
        super._increaseBalance(account, amount);
    }
    
    function tokenURI(uint256 tokenId) 
        public view override(ERC721, ERC721URIStorage) returns (string memory) 
    {
        return super.tokenURI(tokenId);
    }
    
    function supportsInterface(bytes4 interfaceId)
        public view override(ERC721, ERC721Enumerable, ERC721URIStorage, ERC2981, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
    
    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
        
        // Clear quantum hash when token is burned
        delete _tokenQuantumHashes[tokenId];
    }
    
    /**
     * @dev Check if a token exists
     * @param tokenId Token ID
     * @return bool whether the token exists
     */
    function _exists(uint256 tokenId) internal view returns (bool) {
        return tokenId < _nextTokenId && _ownerOf(tokenId) != address(0);
    }
} 