
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
NFT Quantum Verifier - Verification system for quantum-secure NFTs

This module provides mechanisms to verify the authenticity and integrity
of NFTs using quantum-resistant cryptographic techniques.
"""

import os
import time
import hashlib
import json
import base64
from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path

from divine_dashboard_v3.components.nft.quantum_security.nft_quantum_signer import NFTQuantumSigner


class NFTQuantumVerifier:
    """
    Quantum-resistant verification for NFTs.
    
    This verifier creates and validates quantum-resistant proofs for NFTs,
    ensuring their authenticity and integrity can be verified even in a
    post-quantum computing environment.
    """
    
    def __init__(self, keys_dir: Optional[str] = None):
        """
        Initialize NFT Quantum Verifier.
        
        Args:
            keys_dir: Directory for key storage (default: None - don't persist keys)
        """
        self.signer = NFTQuantumSigner(keys_dir=keys_dir)
        self.default_hash_alg = "sha3_512"
    
    def _get_hash_function(self, algorithm: str):
        """
        Get hash function by name.
        
        Args:
            algorithm: Hash algorithm name
            
        Returns:
            Hash function
        """
        if algorithm == "sha3_256":
            return hashlib.sha3_256
        elif algorithm == "sha3_512":
            return hashlib.sha3_512
        elif algorithm == "blake2b":
            return hashlib.blake2b
        elif algorithm == "sha256":
            return hashlib.sha256
        elif algorithm == "sha512":
            return hashlib.sha512
        else:
            # Default to SHA3-512
            return hashlib.sha3_512
    
    def _hash_data(self, data: Dict[str, Any], algorithm: str = "sha3_512") -> str:
        """
        Hash NFT data with specified algorithm.
        
        Args:
            data: NFT data to hash
            algorithm: Hash algorithm name
            
        Returns:
            Hexadecimal hash string
        """
        # Sort keys for consistent hashing
        sorted_data = json.dumps(data, sort_keys=True).encode()
        
        # Get hash function
        hash_func = self._get_hash_function(algorithm)
        
        # Compute hash
        return hash_func(sorted_data).hexdigest()
    
    def _prepare_data_for_proof(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare NFT data for proof creation by removing proof-related fields.
        
        Args:
            data: Original NFT data
            
        Returns:
            Cleaned data for proof creation
        """
        # Create a copy of the data
        proof_data = data.copy()
        
        # Remove any existing proof-related fields
        for field in ["quantum_proof", "signature", "hash", "proof", "verification"]:
            if field in proof_data:
                del proof_data[field]
        
        return proof_data
    
    def create_quantum_proof(self, data: Dict[str, Any], 
                            hash_algorithm: str = "sha3_512",
                            timestamp: Optional[int] = None) -> Dict[str, Any]:
        """
        Create quantum-resistant proof for NFT data.
        
        Args:
            data: NFT data to create proof for
            hash_algorithm: Hash algorithm to use
            timestamp: Proof timestamp (default: current time)
            
        Returns:
            Quantum proof data
        """
        # Prepare data
        proof_data = self._prepare_data_for_proof(data)
        
        # Generate keys
        # Prefer Dilithium if OQS is available, fall back to Lamport
        try:
            if self.signer.oqs_available:
                public_key, private_key = self.signer.generate_dilithium_keys()
                signature_method = "dilithium"
            else:
                public_key, private_key = self.signer.generate_lamport_keys()
                signature_method = "lamport"
        except Exception:
            # If Dilithium fails, use Lamport as fallback
            public_key, private_key = self.signer.generate_lamport_keys()
            signature_method = "lamport"
        
        # Set timestamp
        current_timestamp = timestamp or int(time.time())
        
        # Hash the data
        data_hash = self._hash_data(proof_data, hash_algorithm)
        
        # Create combined data for signing (hash + timestamp)
        sign_data = f"{data_hash}:{current_timestamp}".encode()
        
        # Sign the data
        if signature_method == "dilithium":
            signature = self.signer.dilithium_sign(sign_data, private_key)
            signature_b64 = base64.b64encode(signature).decode()
            public_key_b64 = base64.b64encode(public_key).decode()
        else:  # Lamport
            signature = self.signer.lamport_sign(sign_data, private_key)
            # Convert Lamport signature to JSON-serializable format
            signature_b64 = [base64.b64encode(sig).decode() for sig in signature]
            # Convert Lamport public key to JSON-serializable format
            public_key_b64 = [[base64.b64encode(val).decode() for val in pair] 
                             for pair in public_key]
        
        # Create proof
        proof = {
            "timestamp": current_timestamp,
            "hash_algorithm": hash_algorithm,
            "data_hash": data_hash,
            "signature_method": signature_method,
            "signature": signature_b64,
            "public_key": public_key_b64
        }
        
        return proof
    
    def verify_quantum_proof(self, data: Dict[str, Any], proof: Dict[str, Any]) -> bool:
        """
        Verify quantum-resistant proof for NFT data.
        
        Args:
            data: NFT data to verify
            proof: Quantum proof to verify
            
        Returns:
            True if proof is valid, False otherwise
        """
        try:
            # Extract proof components
            timestamp = proof["timestamp"]
            hash_algorithm = proof["hash_algorithm"]
            expected_hash = proof["data_hash"]
            signature_method = proof["signature_method"]
            signature_data = proof["signature"]
            public_key_data = proof["public_key"]
            
            # Prepare data
            proof_data = self._prepare_data_for_proof(data)
            
            # Hash the data
            actual_hash = self._hash_data(proof_data, hash_algorithm)
            
            # Check if hash matches
            if actual_hash != expected_hash:
                return False
            
            # Create combined data for signature verification (hash + timestamp)
            verify_data = f"{actual_hash}:{timestamp}".encode()
            
            # Verify signature
            if signature_method == "dilithium":
                # Convert back from base64
                signature = base64.b64decode(signature_data)
                public_key = base64.b64decode(public_key_data)
                
                # Verify Dilithium signature
                return self.signer.dilithium_verify(verify_data, signature, public_key)
            elif signature_method == "lamport":
                # Convert from base64
                signature = [base64.b64decode(sig) for sig in signature_data]
                public_key = [[base64.b64decode(val) for val in pair] 
                               for pair in public_key_data]
                
                # Verify Lamport signature
                return self.signer.lamport_verify(verify_data, signature, public_key)
            else:
                # Unknown signature method
                return False
        except (KeyError, ValueError, TypeError) as e:
            print(f"Proof verification error: {e}")
            return False
    
    def verify_quantum_proof_with_time(self, data: Dict[str, Any], proof: Dict[str, Any],
                                     max_age_seconds: Optional[int] = None) -> bool:
        """
        Verify quantum-resistant proof with time constraints.
        
        Args:
            data: NFT data to verify
            proof: Quantum proof to verify
            max_age_seconds: Maximum age of proof in seconds (default: no limit)
            
        Returns:
            True if proof is valid and within time constraints, False otherwise
        """
        # First verify the proof itself
        if not self.verify_quantum_proof(data, proof):
            return False
        
        # If time constraint specified, check it
        if max_age_seconds is not None:
            proof_timestamp = proof["timestamp"]
            current_time = int(time.time())
            
            # Check if proof is too old
            if current_time - proof_timestamp > max_age_seconds:
                return False
        
        return True
    
    def verify_bulk(self, nfts: List[Dict[str, Any]]) -> List[bool]:
        """
        Verify multiple NFTs with quantum proofs.
        
        Args:
            nfts: List of NFT data objects with embedded quantum_proof
            
        Returns:
            List of verification results (True/False for each NFT)
        """
        results = []
        
        for nft in nfts:
            # Skip NFTs without proof
            if "quantum_proof" not in nft:
                results.append(False)
                continue
            
            # Verify each NFT
            result = self.verify_quantum_proof(nft, nft["quantum_proof"])
            results.append(result)
        
        return results
    
    def evaluate_quantum_resistance(self, nft: Dict[str, Any]) -> int:
        """
        Evaluate quantum resistance level of an NFT.
        
        Args:
            nft: NFT data with quantum_proof
            
        Returns:
            Resistance level from 0 (none) to 5 (highest)
        """
        # Check if NFT has quantum proof
        if "quantum_proof" not in nft:
            return 0
        
        proof = nft["quantum_proof"]
        
        # Start with base level
        resistance_level = 1
        
        # Check signature method
        if "signature_method" in proof:
            if proof["signature_method"] == "dilithium":
                resistance_level += 2  # Higher level for Dilithium
            elif proof["signature_method"] == "falcon":
                resistance_level += 2  # Higher level for Falcon
            elif proof["signature_method"] == "sphincs":
                resistance_level += 2  # Higher level for SPHINCS+
            elif proof["signature_method"] == "lamport":
                resistance_level += 1  # Medium level for Lamport
        
        # Check hash algorithm
        if "hash_algorithm" in proof:
            if proof["hash_algorithm"] in ["sha3_512", "blake2b"]:
                resistance_level += 1  # Higher level for strong hash
        
        # Check if the proof is valid
        if self.verify_quantum_proof(nft, proof):
            resistance_level += 1  # Extra point for valid proof
        
        # Cap at level 5
        return min(resistance_level, 5)
    
    def get_resistance_properties(self, nft: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get detailed quantum resistance properties of an NFT.
        
        Args:
            nft: NFT data with quantum_proof
            
        Returns:
            Dictionary of resistance properties
        """
        properties = {
            "resistance_level": 0,
            "has_quantum_proof": False,
            "signature_scheme": "none",
            "hash_strength": "none",
            "valid_proof": False
        }
        
        # Check if NFT has quantum proof
        if "quantum_proof" not in nft:
            return properties
        
        proof = nft["quantum_proof"]
        properties["has_quantum_proof"] = True
        
        # Get signature method
        if "signature_method" in proof:
            properties["signature_scheme"] = proof["signature_method"]
        
        # Get hash algorithm
        if "hash_algorithm" in proof:
            algorithm = proof["hash_algorithm"]
            # Rate hash strength
            if algorithm in ["sha3_512", "blake2b"]:
                properties["hash_strength"] = "high"
            elif algorithm in ["sha3_256", "sha512"]:
                properties["hash_strength"] = "medium"
            else:
                properties["hash_strength"] = "standard"
        
        # Check proof validity
        properties["valid_proof"] = self.verify_quantum_proof(nft, proof)
        
        # Set overall resistance level
        properties["resistance_level"] = self.evaluate_quantum_resistance(nft)
        
        return properties 