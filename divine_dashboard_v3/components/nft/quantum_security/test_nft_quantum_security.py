
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
Quantum Security Tests for NFT Components

These tests verify the quantum resistance properties of the NFT system,
ensuring that NFTs remain secure even in a post-quantum computing world.
"""

import pytest
import os
import hashlib
import random
import secrets
import json
from pathlib import Path
import base64
import hmac
import time
from unittest.mock import patch, MagicMock

# Import standard cryptography libraries
import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa, ec
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Import specialized quantum-resistant libraries
try:
    # Check for post-quantum cryptography libraries
    import oqs  # Open Quantum Safe
    QUANTUM_LIBRARIES_AVAILABLE = True
except ImportError:
    QUANTUM_LIBRARIES_AVAILABLE = False
    print("WARNING: Quantum-resistant libraries not available. Some tests will be skipped.")

# Import local NFT modules
from divine_dashboard_v3.components.nft.quantum_security.nft_quantum_hashchain import NFTQuantumHashchain
from divine_dashboard_v3.components.nft.quantum_security.nft_quantum_signer import NFTQuantumSigner
from divine_dashboard_v3.components.nft.quantum_security.nft_entropy_collector import EntropyCollector
from divine_dashboard_v3.components.nft.quantum_security.nft_quantum_verifier import NFTQuantumVerifier
from divine_dashboard_v3.components.nft.nft_metadata import NFTMetadata

# Constants for testing
TEST_ENTROPY_SIZE = 256  # bits
QUANTUM_HASH_ITERATIONS = 10000
MIN_ENTROPY_THRESHOLD = 0.75  # Shannon entropy minimum threshold

# Fixtures
@pytest.fixture
def temp_dir(tmp_path):
    """Create temporary directory for test outputs."""
    test_dir = tmp_path / "quantum_security_tests"
    test_dir.mkdir()
    return test_dir

@pytest.fixture
def entropy_collector():
    """Create entropy collector instance."""
    return EntropyCollector(sources=["system", "network", "temporal"])

@pytest.fixture
def quantum_hashchain(temp_dir):
    """Create quantum-resistant hashchain instance."""
    return NFTQuantumHashchain(
        output_dir=str(temp_dir),
        hash_iterations=QUANTUM_HASH_ITERATIONS
    )

@pytest.fixture
def quantum_signer():
    """Create quantum-resistant signer instance."""
    return NFTQuantumSigner()

@pytest.fixture
def quantum_verifier():
    """Create quantum verification instance."""
    return NFTQuantumVerifier()

@pytest.fixture
def sample_nft_data():
    """Generate sample NFT data for security testing."""
    return {
        "name": "Quantum Secured NFT",
        "description": "NFT with quantum security features",
        "image": "quantum_secure_image.png",
        "attributes": [
            {"trait_type": "Security Level", "value": "Quantum Resistant"},
            {"trait_type": "Encryption", "value": "Post-Quantum"}
        ],
        "quantum_commitment": "",  # Will be filled by tests
        "creation_timestamp": int(time.time())
    }

# Entropy Collection Tests
class TestEntropyCollection:
    """Tests for entropy collection and randomness quality."""
    
    def test_entropy_generation(self, entropy_collector):
        """Test that sufficient entropy is generated."""
        entropy = entropy_collector.collect(bits=TEST_ENTROPY_SIZE)
        
        # Verify output size
        assert len(entropy) >= TEST_ENTROPY_SIZE // 8  # Convert bits to bytes
        
        # Verify entropy amount using Shannon entropy calculation
        shannon_entropy = calculate_shannon_entropy(entropy)
        assert shannon_entropy > MIN_ENTROPY_THRESHOLD, f"Insufficient entropy: {shannon_entropy}"
    
    def test_entropy_uniqueness(self, entropy_collector):
        """Test that entropy is unique across multiple collections."""
        entropy_samples = [
            entropy_collector.collect(bits=TEST_ENTROPY_SIZE)
            for _ in range(5)
        ]
        
        # Check that all samples are different
        for i in range(len(entropy_samples)):
            for j in range(i + 1, len(entropy_samples)):
                assert entropy_samples[i] != entropy_samples[j], "Entropy samples are not unique"
    
    def test_entropy_sources(self, entropy_collector):
        """Test that multiple entropy sources can be used."""
        # Test system source
        system_entropy = entropy_collector.collect_from_source("system", bits=128)
        assert len(system_entropy) >= 16  # 128 bits = 16 bytes
        
        # Test network source
        network_entropy = entropy_collector.collect_from_source("network", bits=128)
        assert len(network_entropy) >= 16
        
        # Test temporal source
        temporal_entropy = entropy_collector.collect_from_source("temporal", bits=128)
        assert len(temporal_entropy) >= 16
        
        # Test combined sources
        combined_entropy = entropy_collector.collect(bits=128)
        assert len(combined_entropy) >= 16
        
        # Verify sources produce different entropy
        assert system_entropy != network_entropy
        assert network_entropy != temporal_entropy
        assert temporal_entropy != system_entropy
    
    @pytest.mark.skipif(not QUANTUM_LIBRARIES_AVAILABLE, reason="Quantum libraries not available")
    def test_quantum_random_generation(self, entropy_collector):
        """Test quantum random number generation if available."""
        quantum_entropy = entropy_collector.collect_quantum_random(bits=128)
        
        # Verify output
        assert len(quantum_entropy) >= 16
        
        # Check entropy quality
        shannon_entropy = calculate_shannon_entropy(quantum_entropy)
        assert shannon_entropy > MIN_ENTROPY_THRESHOLD

# Quantum Hashchain Tests
class TestQuantumHashchain:
    """Tests for quantum-resistant hashchain implementation."""
    
    def test_hashchain_initialization(self, quantum_hashchain):
        """Test hashchain initialization and configuration."""
        assert quantum_hashchain.hash_iterations == QUANTUM_HASH_ITERATIONS
        assert quantum_hashchain.current_index == 0
    
    def test_generate_genesis_block(self, quantum_hashchain, entropy_collector):
        """Test generation of genesis block with quantum entropy."""
        # Get entropy for genesis
        entropy = entropy_collector.collect(bits=256)
        
        # Generate genesis block
        genesis = quantum_hashchain.create_genesis(entropy)
        
        # Verify genesis block
        assert "index" in genesis and genesis["index"] == 0
        assert "timestamp" in genesis
        assert "hash" in genesis
        assert "prev_hash" in genesis and genesis["prev_hash"] == "0" * 64
        assert "entropy_commitment" in genesis
    
    def test_add_nft_to_hashchain(self, quantum_hashchain, sample_nft_data):
        """Test adding NFT data to quantum hashchain."""
        # First create genesis if not exists
        if quantum_hashchain.current_index == 0:
            quantum_hashchain.create_genesis(os.urandom(32))
        
        # Add NFT to hashchain
        block = quantum_hashchain.add_block(sample_nft_data)
        
        # Verify block
        assert block["index"] == 1
        assert "timestamp" in block
        assert "hash" in block
        assert "prev_hash" in block
        assert block["prev_hash"] == quantum_hashchain.chain[0]["hash"]
        assert "data" in block
        assert block["data"] == sample_nft_data
    
    def test_hashchain_verification(self, quantum_hashchain, sample_nft_data):
        """Test verification of quantum hashchain integrity."""
        # Create chain with multiple blocks
        quantum_hashchain.create_genesis(os.urandom(32))
        quantum_hashchain.add_block({"test": "data1"})
        quantum_hashchain.add_block({"test": "data2"})
        quantum_hashchain.add_block(sample_nft_data)
        
        # Verify chain
        is_valid = quantum_hashchain.verify_chain()
        assert is_valid, "Hashchain verification failed"
    
    def test_hashchain_tamper_detection(self, quantum_hashchain, sample_nft_data):
        """Test that tampering with the hashchain is detected."""
        # Create chain
        quantum_hashchain.create_genesis(os.urandom(32))
        quantum_hashchain.add_block(sample_nft_data)
        quantum_hashchain.add_block({"test": "data"})
        
        # Attempt to tamper with data
        original_data = quantum_hashchain.chain[1]["data"].copy()
        quantum_hashchain.chain[1]["data"]["name"] = "Tampered NFT"
        
        # Verify chain (should fail)
        is_valid = quantum_hashchain.verify_chain()
        assert not is_valid, "Hashchain tamper detection failed"
        
        # Restore data for cleanup
        quantum_hashchain.chain[1]["data"] = original_data
    
    def test_export_and_import_hashchain(self, quantum_hashchain, temp_dir, sample_nft_data):
        """Test exporting and importing hashchain."""
        # Create chain
        quantum_hashchain.create_genesis(os.urandom(32))
        quantum_hashchain.add_block(sample_nft_data)
        
        # Export chain
        export_path = temp_dir / "hashchain_export.json"
        quantum_hashchain.export_chain(str(export_path))
        
        # Verify export file exists
        assert export_path.exists()
        
        # Create new hashchain instance
        new_hashchain = NFTQuantumHashchain(output_dir=str(temp_dir))
        
        # Import chain
        new_hashchain.import_chain(str(export_path))
        
        # Verify imported chain
        assert len(new_hashchain.chain) == len(quantum_hashchain.chain)
        assert new_hashchain.chain[0]["hash"] == quantum_hashchain.chain[0]["hash"]
        assert new_hashchain.chain[1]["hash"] == quantum_hashchain.chain[1]["hash"]
        assert new_hashchain.chain[1]["data"] == quantum_hashchain.chain[1]["data"]

# Quantum Signature Tests
class TestQuantumSignatures:
    """Tests for quantum-resistant signature schemes."""
    
    @pytest.mark.skipif(not QUANTUM_LIBRARIES_AVAILABLE, reason="Quantum libraries not available")
    def test_dilithium_signatures(self, quantum_signer, sample_nft_data):
        """Test CRYSTALS-Dilithium (quantum-resistant) signatures."""
        # Generate Dilithium keys
        public_key, private_key = quantum_signer.generate_dilithium_keys()
        
        # Convert NFT data to bytes
        nft_bytes = json.dumps(sample_nft_data).encode()
        
        # Sign data
        signature = quantum_signer.dilithium_sign(nft_bytes, private_key)
        
        # Verify signature
        is_valid = quantum_signer.dilithium_verify(nft_bytes, signature, public_key)
        assert is_valid, "Dilithium signature verification failed"
        
        # Test against tampering
        tampered_data = json.dumps({**sample_nft_data, "name": "Tampered"}).encode()
        is_valid_tampered = quantum_signer.dilithium_verify(tampered_data, signature, public_key)
        assert not is_valid_tampered, "Dilithium failed to detect tampering"
    
    @pytest.mark.skipif(not QUANTUM_LIBRARIES_AVAILABLE, reason="Quantum libraries not available")
    def test_falcon_signatures(self, quantum_signer, sample_nft_data):
        """Test FALCON (quantum-resistant) signatures."""
        # Generate Falcon keys
        public_key, private_key = quantum_signer.generate_falcon_keys()
        
        # Convert NFT data to bytes
        nft_bytes = json.dumps(sample_nft_data).encode()
        
        # Sign data
        signature = quantum_signer.falcon_sign(nft_bytes, private_key)
        
        # Verify signature
        is_valid = quantum_signer.falcon_verify(nft_bytes, signature, public_key)
        assert is_valid, "Falcon signature verification failed"
    
    def test_lamport_signatures(self, quantum_signer, sample_nft_data):
        """Test Lamport one-time signatures (quantum-resistant)."""
        # Generate Lamport keys
        public_key, private_key = quantum_signer.generate_lamport_keys()
        
        # Convert NFT data to bytes
        nft_bytes = json.dumps(sample_nft_data).encode()
        
        # Sign data with Lamport (hash-based) scheme
        signature = quantum_signer.lamport_sign(nft_bytes, private_key)
        
        # Verify signature
        is_valid = quantum_signer.lamport_verify(nft_bytes, signature, public_key)
        assert is_valid, "Lamport signature verification failed"
        
        # Test against tampering
        tampered_data = json.dumps({**sample_nft_data, "name": "Tampered"}).encode()
        is_valid_tampered = quantum_signer.lamport_verify(tampered_data, signature, public_key)
        assert not is_valid_tampered, "Lamport failed to detect tampering"
    
    def test_sphincs_signatures(self, quantum_signer, sample_nft_data):
        """Test SPHINCS+ stateless hash-based signatures (quantum-resistant)."""
        if not hasattr(quantum_signer, 'generate_sphincs_keys'):
            pytest.skip("SPHINCS+ implementation not available")
        
        # Generate SPHINCS+ keys
        public_key, private_key = quantum_signer.generate_sphincs_keys()
        
        # Convert NFT data to bytes
        nft_bytes = json.dumps(sample_nft_data).encode()
        
        # Sign data
        signature = quantum_signer.sphincs_sign(nft_bytes, private_key)
        
        # Verify signature
        is_valid = quantum_signer.sphincs_verify(nft_bytes, signature, public_key)
        assert is_valid, "SPHINCS+ signature verification failed"

# NFT Quantum Verification Tests
class TestNFTQuantumVerification:
    """Tests for quantum-resistant NFT verification."""
    
    def test_create_quantum_proof(self, quantum_verifier, quantum_signer, sample_nft_data):
        """Test creation of quantum-resistant proof for NFT."""
        # Generate quantum proof
        proof = quantum_verifier.create_quantum_proof(sample_nft_data)
        
        # Verify proof structure
        assert "timestamp" in proof
        assert "hash_algorithm" in proof
        assert "data_hash" in proof
        assert "signature" in proof
        assert "public_key" in proof
        
        # Verify proof is valid
        is_valid = quantum_verifier.verify_quantum_proof(sample_nft_data, proof)
        assert is_valid, "Quantum proof verification failed"
    
    def test_bulk_verification(self, quantum_verifier, quantum_hashchain, sample_nft_data):
        """Test bulk verification of multiple NFTs."""
        # Create multiple NFTs with proofs
        nfts = []
        for i in range(5):
            nft_data = {**sample_nft_data, "name": f"Quantum NFT {i}"}
            proof = quantum_verifier.create_quantum_proof(nft_data)
            nft_data["quantum_proof"] = proof
            quantum_hashchain.add_block(nft_data)
            nfts.append(nft_data)
        
        # Perform bulk verification
        verification_results = quantum_verifier.verify_bulk(nfts)
        
        # Check all verifications succeeded
        assert all(result for result in verification_results)
        assert len(verification_results) == 5
    
    def test_tamper_detection(self, quantum_verifier, sample_nft_data):
        """Test detection of tampering with NFT data."""
        # Create quantum proof
        proof = quantum_verifier.create_quantum_proof(sample_nft_data)
        
        # Create tampered data
        tampered_data = {**sample_nft_data, "name": "Tampered Quantum NFT"}
        
        # Verify with tampered data (should fail)
        is_valid = quantum_verifier.verify_quantum_proof(tampered_data, proof)
        assert not is_valid, "Tamper detection failed"
    
    def test_temporal_verification(self, quantum_verifier, sample_nft_data):
        """Test time-based verification of quantum proofs."""
        # Create quantum proof with custom timestamp (1 hour ago)
        one_hour_ago = int(time.time()) - 3600
        proof = quantum_verifier.create_quantum_proof(sample_nft_data, timestamp=one_hour_ago)
        
        # Verify with time constraints
        is_valid_future = quantum_verifier.verify_quantum_proof_with_time(
            sample_nft_data, proof, max_age_seconds=7200  # 2 hours
        )
        assert is_valid_future, "Temporal verification failed for valid time"
        
        is_valid_past = quantum_verifier.verify_quantum_proof_with_time(
            sample_nft_data, proof, max_age_seconds=1800  # 30 minutes
        )
        assert not is_valid_past, "Temporal verification failed to detect expired proof"

# Integration Tests with NFT Metadata
class TestNFTQuantumIntegration:
    """Integration tests between quantum security and NFT metadata."""
    
    def test_nft_with_quantum_security(self, quantum_verifier, quantum_hashchain):
        """Test end-to-end creation of NFT with quantum security features."""
        # Create NFT metadata
        metadata = NFTMetadata(
            name="Quantum Protected NFT",
            description="NFT with full quantum security suite",
            image="quantum_image.png"
        )
        
        # Add quantum proof
        quantum_proof = quantum_verifier.create_quantum_proof(metadata.to_dict())
        metadata.quantum_proof = quantum_proof
        
        # Add to hashchain
        block = quantum_hashchain.add_block(metadata.to_dict())
        
        # Verify NFT integrity
        is_valid_proof = quantum_verifier.verify_quantum_proof(metadata.to_dict(), metadata.quantum_proof)
        is_valid_chain = quantum_hashchain.verify_chain()
        
        assert is_valid_proof, "Quantum proof verification failed"
        assert is_valid_chain, "Hashchain verification failed"
    
    def test_nft_quantum_resistance_level(self, quantum_verifier, sample_nft_data):
        """Test evaluation of NFT's quantum resistance level."""
        # Standard proof
        standard_proof = quantum_verifier.create_quantum_proof(sample_nft_data)
        sample_nft_data["quantum_proof"] = standard_proof
        
        # Evaluate quantum resistance level
        resistance_level = quantum_verifier.evaluate_quantum_resistance(sample_nft_data)
        
        # Verify resistance level
        assert resistance_level >= 3, f"Insufficient quantum resistance level: {resistance_level}"
        
        # Verify resistance properties
        resistance_properties = quantum_verifier.get_resistance_properties(sample_nft_data)
        assert "hash_strength" in resistance_properties
        assert "signature_scheme" in resistance_properties
        assert "entropy_quality" in resistance_properties

# Helper functions
def calculate_shannon_entropy(data):
    """Calculate Shannon entropy of data (measure of randomness)."""
    if not data:
        return 0
    
    # Count byte frequencies
    counts = {}
    for byte in data:
        counts[byte] = counts.get(byte, 0) + 1
    
    # Calculate entropy
    entropy = 0
    for count in counts.values():
        probability = count / len(data)
        entropy -= probability * (math.log2(probability) if probability > 0 else 0)
    
    # Normalize entropy (max entropy for bytes is 8 bits)
    return entropy / 8 