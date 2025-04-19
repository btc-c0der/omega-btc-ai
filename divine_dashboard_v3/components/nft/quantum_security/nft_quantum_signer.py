
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
NFT Quantum Signer - Post-quantum cryptographic signature utilities

This module implements quantum-resistant signing mechanisms for NFTs,
providing security against attacks from quantum computers that could
potentially break traditional signature schemes like RSA or ECDSA.
"""

import os
import hashlib
import hmac
import json
import secrets
import base64
import time
from typing import Dict, List, Any, Optional, Tuple, Union, ByteString
from pathlib import Path

# Try to import post-quantum libraries
try:
    import oqs  # Open Quantum Safe library
    OQS_AVAILABLE = True
except ImportError:
    OQS_AVAILABLE = False

# Constants
HASH_OUTPUT_SIZE = 32  # 256 bits
LAMPORT_KEY_SIZE = 256  # 256-bit security level


class NFTQuantumSigner:
    """
    Quantum-resistant signing mechanism for NFTs.
    
    Implements multiple post-quantum signature schemes:
    1. CRYSTALS-Dilithium (if oqs available)
    2. FALCON (if oqs available)
    3. Lamport one-time signatures (always available)
    4. SPHINCS+ (if oqs available)
    
    Fall back to hash-based signature schemes when post-quantum libraries
    are not available.
    """
    
    def __init__(self, keys_dir: Optional[str] = None):
        """
        Initialize NFT Quantum Signer.
        
        Args:
            keys_dir: Directory to store keys (default: None - don't persist keys)
        """
        self.keys_dir = Path(keys_dir) if keys_dir else None
        if self.keys_dir:
            self.keys_dir.mkdir(exist_ok=True, parents=True)
            
        # Check for quantum libraries
        self.oqs_available = OQS_AVAILABLE
        if self.oqs_available:
            # Get list of supported algorithms
            self.supported_algs = {
                'dilithium': oqs.Signature.get_enabled_sig_algorithms(),
                'falcon': [alg for alg in oqs.Signature.get_enabled_sig_algorithms() if 'falcon' in alg.lower()],
            }
        else:
            self.supported_algs = {}
    
    #------------------------------------------------------------------
    # Dilithium signatures (CRYSTALS-Dilithium)
    #------------------------------------------------------------------
    
    def generate_dilithium_keys(self, alg_name: Optional[str] = None) -> Tuple[bytes, bytes]:
        """
        Generate CRYSTALS-Dilithium keys.
        
        Args:
            alg_name: Specific Dilithium algorithm variant (default: best available)
            
        Returns:
            Tuple of (public_key, private_key) as bytes
        """
        if not self.oqs_available:
            raise ImportError("OQS library not available, cannot use Dilithium")
        
        # Select algorithm
        if not alg_name:
            # Default to Dilithium5 if available
            dilithium_algs = [a for a in self.supported_algs['dilithium'] 
                             if 'dilithium' in a.lower()]
            if not dilithium_algs:
                raise ValueError("No Dilithium algorithms available")
            
            # Prefer Dilithium5 for higher security
            for alg in dilithium_algs:
                if '5' in alg:
                    alg_name = alg
                    break
            
            # Fallback to first available
            if not alg_name:
                alg_name = dilithium_algs[0]
        
        # Create signer
        with oqs.Signature(alg_name) as signer:
            # Generate keys
            public_key = signer.generate_keypair()
            private_key = signer.export_secret_key()
            
            # Save keys if directory specified
            if self.keys_dir:
                key_id = hashlib.sha256(public_key).hexdigest()[:16]
                with open(self.keys_dir / f"dilithium_pub_{key_id}.key", 'wb') as f:
                    f.write(public_key)
                with open(self.keys_dir / f"dilithium_priv_{key_id}.key", 'wb') as f:
                    f.write(private_key)
            
            return public_key, private_key
    
    def dilithium_sign(self, data: bytes, private_key: bytes, alg_name: Optional[str] = None) -> bytes:
        """
        Sign data using CRYSTALS-Dilithium.
        
        Args:
            data: Data to sign
            private_key: Dilithium private key
            alg_name: Specific Dilithium algorithm (default: detect from key)
            
        Returns:
            Signature bytes
        """
        if not self.oqs_available:
            raise ImportError("OQS library not available, cannot use Dilithium")
        
        # Detect algorithm or use default
        if not alg_name:
            # Default to strongest available
            dilithium_algs = [a for a in self.supported_algs['dilithium'] 
                              if 'dilithium' in a.lower()]
            if not dilithium_algs:
                raise ValueError("No Dilithium algorithms available")
            
            # Try strongest first
            for strength in [5, 3, 2]:
                for alg in dilithium_algs:
                    if str(strength) in alg:
                        alg_name = alg
                        break
                if alg_name:
                    break
            
            # Fallback to first available
            if not alg_name:
                alg_name = dilithium_algs[0]
        
        # Sign data
        with oqs.Signature(alg_name) as signer:
            signer.import_secret_key(private_key)
            signature = signer.sign(data)
            return signature
    
    def dilithium_verify(self, data: bytes, signature: bytes, public_key: bytes, 
                         alg_name: Optional[str] = None) -> bool:
        """
        Verify CRYSTALS-Dilithium signature.
        
        Args:
            data: Original data that was signed
            signature: Dilithium signature
            public_key: Dilithium public key
            alg_name: Specific Dilithium algorithm (default: detect from key)
            
        Returns:
            True if signature is valid, False otherwise
        """
        if not self.oqs_available:
            raise ImportError("OQS library not available, cannot use Dilithium")
        
        # Detect algorithm or use default
        if not alg_name:
            # Default using same approach as sign
            dilithium_algs = [a for a in self.supported_algs['dilithium'] 
                              if 'dilithium' in a.lower()]
            if not dilithium_algs:
                raise ValueError("No Dilithium algorithms available")
            
            # Try strongest first
            for strength in [5, 3, 2]:
                for alg in dilithium_algs:
                    if str(strength) in alg:
                        alg_name = alg
                        break
                if alg_name:
                    break
            
            # Fallback to first available
            if not alg_name:
                alg_name = dilithium_algs[0]
        
        # Verify signature
        try:
            with oqs.Signature(alg_name) as verifier:
                return verifier.verify(data, signature, public_key)
        except Exception:
            return False
    
    #------------------------------------------------------------------
    # FALCON signatures
    #------------------------------------------------------------------
    
    def generate_falcon_keys(self, alg_name: Optional[str] = None) -> Tuple[bytes, bytes]:
        """
        Generate FALCON keys.
        
        Args:
            alg_name: Specific FALCON algorithm variant (default: best available)
            
        Returns:
            Tuple of (public_key, private_key) as bytes
        """
        if not self.oqs_available:
            raise ImportError("OQS library not available, cannot use FALCON")
        
        # Select algorithm
        if not alg_name:
            # Check for FALCON algorithms
            falcon_algs = [a for a in self.supported_algs.get('falcon', []) 
                           if 'falcon' in a.lower()]
            if not falcon_algs:
                raise ValueError("No FALCON algorithms available")
            
            # Prefer FALCON-1024 for higher security
            for alg in falcon_algs:
                if '1024' in alg:
                    alg_name = alg
                    break
            
            # Fallback to first available
            if not alg_name:
                alg_name = falcon_algs[0]
        
        # Create signer
        with oqs.Signature(alg_name) as signer:
            # Generate keys
            public_key = signer.generate_keypair()
            private_key = signer.export_secret_key()
            
            # Save keys if directory specified
            if self.keys_dir:
                key_id = hashlib.sha256(public_key).hexdigest()[:16]
                with open(self.keys_dir / f"falcon_pub_{key_id}.key", 'wb') as f:
                    f.write(public_key)
                with open(self.keys_dir / f"falcon_priv_{key_id}.key", 'wb') as f:
                    f.write(private_key)
            
            return public_key, private_key
    
    def falcon_sign(self, data: bytes, private_key: bytes, alg_name: Optional[str] = None) -> bytes:
        """
        Sign data using FALCON.
        
        Args:
            data: Data to sign
            private_key: FALCON private key
            alg_name: Specific FALCON algorithm (default: detect from key)
            
        Returns:
            Signature bytes
        """
        if not self.oqs_available:
            raise ImportError("OQS library not available, cannot use FALCON")
        
        # Detect algorithm or use default
        if not alg_name:
            # Default to strongest available
            falcon_algs = [a for a in self.supported_algs.get('falcon', [])
                           if 'falcon' in a.lower()]
            if not falcon_algs:
                raise ValueError("No FALCON algorithms available")
            
            # Try strongest first (FALCON-1024)
            for alg in falcon_algs:
                if '1024' in alg:
                    alg_name = alg
                    break
            
            # Fallback to first available
            if not alg_name:
                alg_name = falcon_algs[0]
        
        # Sign data
        with oqs.Signature(alg_name) as signer:
            signer.import_secret_key(private_key)
            signature = signer.sign(data)
            return signature
    
    def falcon_verify(self, data: bytes, signature: bytes, public_key: bytes,
                     alg_name: Optional[str] = None) -> bool:
        """
        Verify FALCON signature.
        
        Args:
            data: Original data that was signed
            signature: FALCON signature
            public_key: FALCON public key
            alg_name: Specific FALCON algorithm (default: detect from key)
            
        Returns:
            True if signature is valid, False otherwise
        """
        if not self.oqs_available:
            raise ImportError("OQS library not available, cannot use FALCON")
        
        # Detect algorithm or use default
        if not alg_name:
            # Default using same approach as sign
            falcon_algs = [a for a in self.supported_algs.get('falcon', [])
                           if 'falcon' in a.lower()]
            if not falcon_algs:
                raise ValueError("No FALCON algorithms available")
            
            # Try strongest first
            for alg in falcon_algs:
                if '1024' in alg:
                    alg_name = alg
                    break
            
            # Fallback to first available
            if not alg_name:
                alg_name = falcon_algs[0]
        
        # Verify signature
        try:
            with oqs.Signature(alg_name) as verifier:
                return verifier.verify(data, signature, public_key)
        except Exception:
            return False
            
    #------------------------------------------------------------------
    # Lamport one-time signatures
    #------------------------------------------------------------------
    
    def generate_lamport_keys(self, 
                              hash_function=None) -> Tuple[List[List[bytes]], List[List[bytes]]]:
        """
        Generate Lamport one-time signature keys (quantum-resistant).
        
        This is a pure Python implementation that works without requiring
        external quantum libraries.
        
        Args:
            hash_function: Hash function to use (default: SHA3-256)
            
        Returns:
            Tuple of (public_key, private_key)
            Each key is a list of bit positions, with two random values per bit.
        """
        if hash_function is None:
            hash_function = hashlib.sha3_256
        
        # For each bit position, we need two random values in private key
        private_key = [
            [secrets.token_bytes(HASH_OUTPUT_SIZE), secrets.token_bytes(HASH_OUTPUT_SIZE)]
            for _ in range(LAMPORT_KEY_SIZE)
        ]
        
        # Public key contains hashes of the private key values
        public_key = [
            [hash_function(val).digest() for val in bit_pair]
            for bit_pair in private_key
        ]
        
        # Save keys if directory specified
        if self.keys_dir:
            # Convert to serializable format
            serializable_private = [
                [base64.b64encode(val).decode() for val in bit_pair]
                for bit_pair in private_key
            ]
            serializable_public = [
                [base64.b64encode(val).decode() for val in bit_pair]
                for bit_pair in public_key
            ]
            
            # Generate key ID
            key_id = hashlib.sha256(json.dumps(serializable_public).encode()).hexdigest()[:16]
            
            # Save keys
            with open(self.keys_dir / f"lamport_pub_{key_id}.json", 'w') as f:
                json.dump(serializable_public, f)
            with open(self.keys_dir / f"lamport_priv_{key_id}.json", 'w') as f:
                json.dump(serializable_private, f)
        
        return public_key, private_key
    
    def lamport_sign(self, data: bytes, private_key: List[List[bytes]], 
                     hash_function=None) -> List[bytes]:
        """
        Sign data using Lamport one-time signatures.
        
        Warning: Each private key should only be used ONCE.
        
        Args:
            data: Data to sign
            private_key: Lamport private key
            hash_function: Hash function to use (default: SHA3-256)
            
        Returns:
            Signature as list of bytes
        """
        if hash_function is None:
            hash_function = hashlib.sha3_256
        
        # Hash the data to a fixed length
        data_hash = hash_function(data).digest()
        
        # Convert hash to bits
        hash_bits = ''.join([bin(b)[2:].zfill(8) for b in data_hash])[:LAMPORT_KEY_SIZE]
        
        # For each bit in the hash, include the corresponding private key value
        signature = []
        for i, bit in enumerate(hash_bits):
            bit_val = int(bit)
            # Choose the corresponding private key value based on bit value
            signature.append(private_key[i][bit_val])
        
        return signature
    
    def lamport_verify(self, data: bytes, signature: List[bytes], 
                       public_key: List[List[bytes]], hash_function=None) -> bool:
        """
        Verify Lamport one-time signature.
        
        Args:
            data: Original data that was signed
            signature: Lamport signature
            public_key: Lamport public key
            hash_function: Hash function to use (default: SHA3-256)
            
        Returns:
            True if signature is valid, False otherwise
        """
        if hash_function is None:
            hash_function = hashlib.sha3_256
        
        try:
            # Hash the data to a fixed length
            data_hash = hash_function(data).digest()
            
            # Convert hash to bits
            hash_bits = ''.join([bin(b)[2:].zfill(8) for b in data_hash])[:LAMPORT_KEY_SIZE]
            
            # For each bit in the hash, verify the corresponding signature value
            for i, bit in enumerate(hash_bits):
                bit_val = int(bit)
                # Hash the signature value for this bit
                sig_hash = hash_function(signature[i]).digest()
                # Compare with the public key value
                if sig_hash != public_key[i][bit_val]:
                    return False
            
            return True
        except (IndexError, ValueError):
            return False
    
    #------------------------------------------------------------------
    # SPHINCS+ stateless hash-based signatures
    #------------------------------------------------------------------
    
    def generate_sphincs_keys(self, alg_name: Optional[str] = None) -> Tuple[bytes, bytes]:
        """
        Generate SPHINCS+ keys.
        
        Args:
            alg_name: Specific SPHINCS+ algorithm variant (default: best available)
            
        Returns:
            Tuple of (public_key, private_key) as bytes
        """
        if not self.oqs_available:
            raise ImportError("OQS library not available, cannot use SPHINCS+")
        
        # Select algorithm
        if not alg_name:
            # Find SPHINCS+ algorithms
            sphincs_algs = [a for a in oqs.Signature.get_enabled_sig_algorithms() 
                            if 'sphincs' in a.lower()]
            if not sphincs_algs:
                raise ValueError("No SPHINCS+ algorithms available")
            
            # Prefer SHA-256 variant for higher security
            for alg in sphincs_algs:
                if 'sha2' in alg.lower() and '256' in alg:
                    alg_name = alg
                    break
            
            # Fallback to first available
            if not alg_name:
                alg_name = sphincs_algs[0]
        
        # Create signer
        with oqs.Signature(alg_name) as signer:
            # Generate keys
            public_key = signer.generate_keypair()
            private_key = signer.export_secret_key()
            
            # Save keys if directory specified
            if self.keys_dir:
                key_id = hashlib.sha256(public_key).hexdigest()[:16]
                with open(self.keys_dir / f"sphincs_pub_{key_id}.key", 'wb') as f:
                    f.write(public_key)
                with open(self.keys_dir / f"sphincs_priv_{key_id}.key", 'wb') as f:
                    f.write(private_key)
            
            return public_key, private_key
    
    def sphincs_sign(self, data: bytes, private_key: bytes, alg_name: Optional[str] = None) -> bytes:
        """
        Sign data using SPHINCS+.
        
        Args:
            data: Data to sign
            private_key: SPHINCS+ private key
            alg_name: Specific SPHINCS+ algorithm (default: detect from key)
            
        Returns:
            Signature bytes
        """
        if not self.oqs_available:
            raise ImportError("OQS library not available, cannot use SPHINCS+")
        
        # Detect algorithm or use default
        if not alg_name:
            # Default to strongest available
            sphincs_algs = [a for a in oqs.Signature.get_enabled_sig_algorithms()
                            if 'sphincs' in a.lower()]
            if not sphincs_algs:
                raise ValueError("No SPHINCS+ algorithms available")
            
            # Try strongest SHA-256 variant first
            for alg in sphincs_algs:
                if 'sha2' in alg.lower() and '256' in alg:
                    alg_name = alg
                    break
            
            # Fallback to first available
            if not alg_name:
                alg_name = sphincs_algs[0]
        
        # Sign data
        with oqs.Signature(alg_name) as signer:
            signer.import_secret_key(private_key)
            signature = signer.sign(data)
            return signature
    
    def sphincs_verify(self, data: bytes, signature: bytes, public_key: bytes,
                      alg_name: Optional[str] = None) -> bool:
        """
        Verify SPHINCS+ signature.
        
        Args:
            data: Original data that was signed
            signature: SPHINCS+ signature
            public_key: SPHINCS+ public key
            alg_name: Specific SPHINCS+ algorithm (default: detect from key)
            
        Returns:
            True if signature is valid, False otherwise
        """
        if not self.oqs_available:
            raise ImportError("OQS library not available, cannot use SPHINCS+")
        
        # Detect algorithm or use default
        if not alg_name:
            # Default using same approach as sign
            sphincs_algs = [a for a in oqs.Signature.get_enabled_sig_algorithms()
                            if 'sphincs' in a.lower()]
            if not sphincs_algs:
                raise ValueError("No SPHINCS+ algorithms available")
            
            # Try strongest first
            for alg in sphincs_algs:
                if 'sha2' in alg.lower() and '256' in alg:
                    alg_name = alg
                    break
            
            # Fallback to first available
            if not alg_name:
                alg_name = sphincs_algs[0]
        
        # Verify signature
        try:
            with oqs.Signature(alg_name) as verifier:
                return verifier.verify(data, signature, public_key)
        except Exception:
            return False 