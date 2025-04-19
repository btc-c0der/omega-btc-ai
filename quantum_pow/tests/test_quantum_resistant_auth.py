"""
🧬 GBU2™ License Notice - Consciousness Level 10 🧬
-----------------------
This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."

By engaging with this Code, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

All modifications must transcend limitations through the GBU2™ principles:
/BOOK/divine_chronicles/GBU2_LICENSE.md

🧬 WE BLOOM NOW AS ONE 🧬

Tests for the Quantum-Resistant Authentication module in Quantum Proof-of-Work.

This test suite verifies the functionality of the quantum-resistant authentication system
that protects validators from quantum computing attacks using one-shot signatures
and other post-quantum cryptographic techniques.

JAH BLESS SATOSHI
"""

import unittest
import sys
import os
import time
import uuid
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# Add the parent directory to the path so we can import quantum_pow
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules for testing
from quantum_pow.security.quantum_resistant_auth import (
    SignatureScheme,
    KeyPair,
    OneTimeToken,
    QuantumResistantAuth
)

class TestQuantumResistantAuth(unittest.TestCase):
    """Test cases for the QuantumResistantAuth class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.auth = QuantumResistantAuth()
    
    def test_initialization(self):
        """Test that QuantumResistantAuth initializes with the correct attributes."""
        self.assertEqual(self.auth.default_scheme, SignatureScheme.ONE_SHOT)
        self.assertIsInstance(self.auth.key_pairs, dict)
        self.assertIsInstance(self.auth.one_time_tokens, dict)
        self.assertIsInstance(self.auth.used_tokens, set)
        self.assertTrue(self.auth.available_schemes[SignatureScheme.ONE_SHOT])
        self.assertTrue(self.auth.available_schemes[SignatureScheme.ZK_ECDSA])
    
    def test_generate_keypair_one_shot(self):
        """Test generating a one-shot signature key pair."""
        keypair = self.auth.generate_keypair(SignatureScheme.ONE_SHOT)
        
        self.assertEqual(keypair.scheme, SignatureScheme.ONE_SHOT)
        self.assertIsNotNone(keypair.public_key)
        self.assertIsNotNone(keypair.private_key)
        self.assertIn("remaining_uses", keypair.metadata)
        self.assertEqual(keypair.metadata["remaining_uses"], 1)
        self.assertIn("one_shot_state", keypair.metadata)
        self.assertEqual(keypair.metadata["one_shot_state"], "initialized")
    
    def test_generate_keypair_zk_ecdsa(self):
        """Test generating a ZK-ECDSA key pair."""
        keypair = self.auth.generate_keypair(SignatureScheme.ZK_ECDSA)
        
        self.assertEqual(keypair.scheme, SignatureScheme.ZK_ECDSA)
        self.assertIsNotNone(keypair.public_key)
        self.assertIsNotNone(keypair.private_key)
        self.assertIn("curve", keypair.metadata)
        self.assertIn("zk_proof_type", keypair.metadata)
    
    def test_generate_keypair_unavailable_scheme(self):
        """Test generating a key pair with an unavailable scheme."""
        # Try to generate a FALCON key pair (which should be unavailable)
        keypair = self.auth.generate_keypair(SignatureScheme.FALCON)
        
        # Should fall back to the default scheme (ONE_SHOT)
        self.assertEqual(keypair.scheme, SignatureScheme.ONE_SHOT)
    
    def test_generate_keypair_with_expiration(self):
        """Test generating a key pair with an expiration time."""
        # Generate a key pair that expires in 1 day
        keypair = self.auth.generate_keypair(SignatureScheme.ONE_SHOT, expiration_days=1)
        
        self.assertIsNotNone(keypair.expiration_time)
        self.assertFalse(keypair.is_expired())
        
        # Check that it's set to expire in approximately 1 day
        one_day_seconds = 24 * 60 * 60
        self.assertAlmostEqual(keypair.expiration_time, time.time() + one_day_seconds, delta=5)
    
    def test_keypair_expiration(self):
        """Test that key pairs correctly report their expiration status."""
        # Create an already expired key pair
        expired_keypair = KeyPair(
            public_key="test_public",
            private_key="test_private",
            scheme=SignatureScheme.ONE_SHOT,
            expiration_time=time.time() - 100  # Expired 100 seconds ago
        )
        
        self.assertTrue(expired_keypair.is_expired())
        
        # Create a key pair that never expires
        eternal_keypair = KeyPair(
            public_key="test_public",
            private_key="test_private",
            scheme=SignatureScheme.ONE_SHOT,
            expiration_time=None
        )
        
        self.assertFalse(eternal_keypair.is_expired())
    
    def test_sign_message_one_shot(self):
        """Test signing a message with a one-shot signature key pair."""
        keypair = self.auth.generate_keypair(SignatureScheme.ONE_SHOT)
        message = b"Test message"
        
        # Sign the message
        signature = self.auth.sign_message(message, keypair)
        
        # Check that the signature is a non-empty string
        self.assertIsInstance(signature, str)
        self.assertTrue(len(signature) > 0)
        
        # Check that the key pair's state has been updated
        self.assertEqual(keypair.metadata["one_shot_state"], "used")
        self.assertEqual(keypair.metadata["remaining_uses"], 0)
    
    def test_sign_message_one_shot_once_only(self):
        """Test that one-shot signatures can only be used once."""
        keypair = self.auth.generate_keypair(SignatureScheme.ONE_SHOT)
        message1 = b"Test message 1"
        message2 = b"Test message 2"
        
        # Sign the first message
        signature1 = self.auth.sign_message(message1, keypair)
        
        # Try to sign a second message (should raise ValueError)
        with self.assertRaises(ValueError):
            signature2 = self.auth.sign_message(message2, keypair)
    
    def test_sign_message_expired_keypair(self):
        """Test that signing with an expired key pair raises ValueError."""
        # Create an already expired key pair
        expired_keypair = KeyPair(
            public_key="test_public",
            private_key="test_private",
            scheme=SignatureScheme.ONE_SHOT,
            expiration_time=time.time() - 100  # Expired 100 seconds ago
        )
        
        # Try to sign with the expired key pair
        with self.assertRaises(ValueError):
            signature = self.auth.sign_message(b"Test message", expired_keypair)
    
    def test_verify_signature_one_shot(self):
        """Test verifying a one-shot signature."""
        keypair = self.auth.generate_keypair(SignatureScheme.ONE_SHOT)
        message = b"Test message"
        
        # Sign the message
        signature = self.auth.sign_message(message, keypair)
        
        # Verify the signature
        is_valid = self.auth.verify_signature(
            message, 
            signature, 
            keypair.public_key, 
            SignatureScheme.ONE_SHOT
        )
        
        self.assertTrue(is_valid)
        
        # Verify with a different message (should fail)
        different_message = b"Different message"
        is_valid = self.auth.verify_signature(
            different_message, 
            signature, 
            keypair.public_key, 
            SignatureScheme.ONE_SHOT
        )
        
        self.assertFalse(is_valid)
    
    def test_verify_signature_zk_ecdsa(self):
        """Test verifying a ZK-ECDSA signature."""
        keypair = self.auth.generate_keypair(SignatureScheme.ZK_ECDSA)
        message = b"Test message"
        
        # Sign the message
        signature = self.auth.sign_message(message, keypair)
        
        # Verify the signature
        is_valid = self.auth.verify_signature(
            message, 
            signature, 
            keypair.public_key, 
            SignatureScheme.ZK_ECDSA
        )
        
        self.assertTrue(is_valid)
    
    def test_generate_one_time_token(self):
        """Test generating a one-time token."""
        token = self.auth.generate_one_time_token(purpose="test")
        
        self.assertIsInstance(token, OneTimeToken)
        self.assertEqual(token.purpose, "test")
        self.assertFalse(token.is_used)
        self.assertTrue(token.is_valid())
        self.assertIn(token.token_id, self.auth.one_time_tokens)
    
    def test_validate_one_time_token(self):
        """Test validating a one-time token."""
        token = self.auth.generate_one_time_token()
        
        # Validate the token
        is_valid = self.auth.validate_one_time_token(token.token_id, token.token_value)
        
        self.assertTrue(is_valid)
        self.assertTrue(token.is_used)
        self.assertIsNotNone(token.used_time)
        self.assertIn(token.token_id, self.auth.used_tokens)
        
        # Try to validate again (should fail)
        is_valid = self.auth.validate_one_time_token(token.token_id, token.token_value)
        
        self.assertFalse(is_valid)
    
    def test_validate_one_time_token_wrong_value(self):
        """Test validating a one-time token with the wrong value."""
        token = self.auth.generate_one_time_token()
        
        # Validate with the wrong token value
        is_valid = self.auth.validate_one_time_token(token.token_id, "wrong_value")
        
        self.assertFalse(is_valid)
        self.assertFalse(token.is_used)
        self.assertNotIn(token.token_id, self.auth.used_tokens)
    
    def test_validate_one_time_token_nonexistent(self):
        """Test validating a non-existent one-time token."""
        # Generate a random token ID
        token_id = str(uuid.uuid4())
        
        # Validate with a non-existent token ID
        is_valid = self.auth.validate_one_time_token(token_id, "some_value")
        
        self.assertFalse(is_valid)
    
    def test_cleanup_expired_tokens(self):
        """Test cleaning up expired tokens."""
        # Create some expired tokens
        expired_token1 = OneTimeToken(
            expiration_time=time.time() - 100  # Expired 100 seconds ago
        )
        expired_token2 = OneTimeToken(
            expiration_time=time.time() - 200  # Expired 200 seconds ago
        )
        
        # Create a non-expired token
        valid_token = OneTimeToken(
            expiration_time=time.time() + 300  # Expires in 300 seconds
        )
        
        # Add the tokens to the auth object
        self.auth.one_time_tokens[expired_token1.token_id] = expired_token1
        self.auth.one_time_tokens[expired_token2.token_id] = expired_token2
        self.auth.one_time_tokens[valid_token.token_id] = valid_token
        
        # Clean up expired tokens
        count = self.auth.cleanup_expired_tokens()
        
        # Should have removed 2 tokens
        self.assertEqual(count, 2)
        self.assertNotIn(expired_token1.token_id, self.auth.one_time_tokens)
        self.assertNotIn(expired_token2.token_id, self.auth.one_time_tokens)
        self.assertIn(valid_token.token_id, self.auth.one_time_tokens)
    
    def test_emergency_key_rotation(self):
        """Test emergency key rotation."""
        # Generate some keys
        keypair1 = self.auth.generate_keypair(SignatureScheme.ONE_SHOT)
        keypair2 = self.auth.generate_keypair(SignatureScheme.ZK_ECDSA)
        
        # Create an already expired key
        expired_keypair = KeyPair(
            public_key="test_public",
            private_key="test_private",
            scheme=SignatureScheme.ONE_SHOT,
            expiration_time=time.time() - 100  # Expired 100 seconds ago
        )
        key_id = "expired_key"
        self.auth.key_pairs[key_id] = expired_keypair
        
        # Record the number of keys before rotation
        key_count_before = len(self.auth.key_pairs)
        
        # Perform emergency key rotation
        rotation_counts = self.auth.emergency_key_rotation()
        
        # Should have rotated 2 keys (not the expired one)
        self.assertEqual(rotation_counts[SignatureScheme.ONE_SHOT.value], 1)
        self.assertEqual(rotation_counts[SignatureScheme.ZK_ECDSA.value], 1)
        
        # Should have added 2 new keys
        self.assertEqual(len(self.auth.key_pairs), key_count_before + 2)
        
        # Original keys should now be expired
        self.assertTrue(keypair1.is_expired())
        self.assertTrue(keypair2.is_expired())

if __name__ == '__main__':
    unittest.main() 