
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

"""
NFT Quantum Hashchain - Secure blockchain-inspired structure for NFT provenance

This module implements a quantum-resistant hashchain for securing NFT provenance
and authenticity records, using advanced cryptographic techniques designed to
withstand potential attacks from quantum computers.
"""

import os
import time
import json
import hashlib
import hmac
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import base64

# Constants
DEFAULT_HASH_ITERATIONS = 10000  # Number of iterations for key stretching
DEFAULT_HASH_ALGORITHM = "sha3_512"  # Default hash algorithm


class NFTQuantumHashchain:
    """
    Quantum-resistant hashchain implementation for NFT security.
    
    This hashchain provides a secure, append-only data structure that:
    1. Creates a tamper-evident chain of NFT records
    2. Uses quantum-resistant hashing algorithms
    3. Incorporates multiple layers of entropy
    4. Implements key stretching to increase attack cost
    """
    
    def __init__(
        self,
        output_dir: str = "quantum_hashchain",
        hash_algorithm: str = DEFAULT_HASH_ALGORITHM,
        hash_iterations: int = DEFAULT_HASH_ITERATIONS
    ):
        """
        Initialize NFT Quantum Hashchain.
        
        Args:
            output_dir: Directory to store hashchain data
            hash_algorithm: Hash algorithm to use (sha3_256, sha3_512, blake2b)
            hash_iterations: Number of iterations for key stretching
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        self.hash_algorithm = hash_algorithm
        self.hash_iterations = hash_iterations
        self.chain = []
        self.current_index = 0
        
        # Try to load existing chain
        chain_file = self.output_dir / "quantum_hashchain.json"
        if chain_file.exists():
            try:
                self.import_chain(str(chain_file))
            except Exception as e:
                print(f"Warning: Could not load existing hashchain: {e}")
    
    def _get_hasher(self):
        """Get hash function based on selected algorithm."""
        if self.hash_algorithm == "sha3_256":
            return hashlib.sha3_256()
        elif self.hash_algorithm == "sha3_512":
            return hashlib.sha3_512()
        elif self.hash_algorithm == "blake2b":
            return hashlib.blake2b()
        else:
            # Default to SHA3-512 if algorithm not recognized
            return hashlib.sha3_512()
    
    def _compute_hash(self, data: Union[bytes, str], salt: Optional[bytes] = None) -> str:
        """
        Compute quantum-resistant hash with key stretching.
        
        Args:
            data: Data to hash (bytes or string)
            salt: Optional salt to add to the hash
            
        Returns:
            Hexadecimal hash string
        """
        # Ensure data is bytes
        if isinstance(data, str):
            data = data.encode()
        
        # Apply salt if provided
        if salt:
            data = salt + data
        
        # Get hasher
        hasher = self._get_hasher()
        
        # Initial hash
        hasher.update(data)
        hash_result = hasher.digest()
        
        # Key stretching with multiple iterations
        for _ in range(self.hash_iterations):
            hasher = self._get_hasher()
            hasher.update(hash_result)
            hash_result = hasher.digest()
        
        # Return as hex string
        return hash_result.hex()
    
    def create_genesis(self, entropy: bytes) -> Dict[str, Any]:
        """
        Create genesis block for hashchain.
        
        Args:
            entropy: Initial entropy for genesis block
            
        Returns:
            Genesis block as dictionary
        """
        # Create genesis block
        genesis_block = {
            "index": 0,
            "timestamp": int(time.time()),
            "data": "GENESIS",
            "prev_hash": "0" * 64,  # 64 zeros as previous hash for genesis
            "entropy_commitment": base64.b64encode(entropy).decode(),
        }
        
        # Compute hash for genesis block
        block_data = f"{genesis_block['index']}{genesis_block['timestamp']}{genesis_block['data']}{genesis_block['prev_hash']}{genesis_block['entropy_commitment']}"
        genesis_block["hash"] = self._compute_hash(block_data, entropy)
        
        # Add to chain
        self.chain = [genesis_block]
        self.current_index = 1
        
        # Save chain
        self._save_chain()
        
        return genesis_block
    
    def add_block(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add new block to hashchain with NFT data.
        
        Args:
            data: NFT data to add to block
            
        Returns:
            New block as dictionary
        """
        # Ensure chain has been initialized
        if not self.chain:
            raise ValueError("Hashchain not initialized. Create genesis block first.")
        
        # Get previous block hash
        prev_hash = self.chain[-1]["hash"]
        
        # Create new block
        new_block = {
            "index": self.current_index,
            "timestamp": int(time.time()),
            "data": data,
            "prev_hash": prev_hash,
        }
        
        # Generate random salt for this block
        block_salt = os.urandom(32)
        new_block["salt_commitment"] = base64.b64encode(block_salt).decode()
        
        # Compute hash for new block
        block_data = f"{new_block['index']}{new_block['timestamp']}{json.dumps(new_block['data'])}{new_block['prev_hash']}{new_block['salt_commitment']}"
        new_block["hash"] = self._compute_hash(block_data, block_salt)
        
        # Add to chain
        self.chain.append(new_block)
        self.current_index += 1
        
        # Save chain
        self._save_chain()
        
        return new_block
    
    def verify_block(self, block: Dict[str, Any]) -> bool:
        """
        Verify integrity of a single block.
        
        Args:
            block: Block to verify
            
        Returns:
            True if block is valid, False otherwise
        """
        # Convert salt commitment back to bytes
        salt = base64.b64decode(block["salt_commitment"]) if "salt_commitment" in block else None
        
        # Skip salt verification for genesis block which has entropy_commitment instead
        if block["index"] == 0:
            salt = base64.b64decode(block["entropy_commitment"])
            
        # Prepare block data for hashing
        block_data = f"{block['index']}{block['timestamp']}{json.dumps(block['data']) if isinstance(block['data'], dict) else block['data']}{block['prev_hash']}"
        
        if "salt_commitment" in block:
            block_data += block["salt_commitment"]
        elif "entropy_commitment" in block:
            block_data += block["entropy_commitment"]
        
        # Compute hash
        computed_hash = self._compute_hash(block_data, salt)
        
        # Compare with stored hash
        return computed_hash == block["hash"]
    
    def verify_chain(self) -> bool:
        """
        Verify integrity of entire hashchain.
        
        Returns:
            True if chain is valid, False otherwise
        """
        # Empty chain is invalid
        if not self.chain:
            return False
        
        # Verify each block
        for i in range(len(self.chain)):
            current_block = self.chain[i]
            
            # Verify block hash
            if not self.verify_block(current_block):
                print(f"Block {i} has invalid hash")
                return False
            
            # Verify block links (except for genesis)
            if i > 0:
                prev_block = self.chain[i - 1]
                if current_block["prev_hash"] != prev_block["hash"]:
                    print(f"Block {i} has invalid previous hash")
                    return False
        
        return True
    
    def _save_chain(self) -> None:
        """Save hashchain to file."""
        chain_file = self.output_dir / "quantum_hashchain.json"
        with open(chain_file, 'w') as f:
            json.dump(self.chain, f, indent=2)
    
    def export_chain(self, output_path: str) -> None:
        """
        Export hashchain to specified file.
        
        Args:
            output_path: Path to save hashchain
        """
        with open(output_path, 'w') as f:
            json.dump(self.chain, f, indent=2)
    
    def import_chain(self, input_path: str) -> None:
        """
        Import hashchain from file.
        
        Args:
            input_path: Path to load hashchain from
        """
        with open(input_path, 'r') as f:
            self.chain = json.load(f)
            self.current_index = len(self.chain)
    
    def get_block_by_index(self, index: int) -> Optional[Dict[str, Any]]:
        """
        Get block by index.
        
        Args:
            index: Block index
            
        Returns:
            Block or None if not found
        """
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None
    
    def get_latest_block(self) -> Optional[Dict[str, Any]]:
        """
        Get latest block in chain.
        
        Returns:
            Latest block or None if chain is empty
        """
        if self.chain:
            return self.chain[-1]
        return None
    
    def create_block_certificate(self, block_index: int) -> Dict[str, Any]:
        """
        Create verifiable certificate for a block.
        
        Args:
            block_index: Index of block to certify
            
        Returns:
            Certificate data
        """
        # Check if block exists
        block = self.get_block_by_index(block_index)
        if not block:
            raise ValueError(f"Block with index {block_index} not found")
        
        # Create certificate with verification info
        certificate = {
            "block_index": block_index,
            "block_hash": block["hash"],
            "timestamp": int(time.time()),
            "verification_path": []
        }
        
        # Add verification path (simplified Merkle path)
        # This allows verifying a single block without the entire chain
        for i in range(block_index + 1, min(block_index + 4, len(self.chain))):
            certificate["verification_path"].append({
                "index": self.chain[i]["index"],
                "hash": self.chain[i]["hash"],
                "prev_hash": self.chain[i]["prev_hash"]
            })
        
        return certificate 