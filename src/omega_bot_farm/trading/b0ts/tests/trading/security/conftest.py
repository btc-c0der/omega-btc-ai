#!/usr/bin/env python3

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
Fixtures for quantum security tests in Omega Bot Farm Trading.

This module provides common fixtures for testing quantum-resistant security
features across the trading components.
"""

import pytest
import os
import time
import uuid
import hashlib
from unittest.mock import MagicMock, AsyncMock

# Define SignatureScheme similar to what's in the main module
class SignatureScheme:
    """Available signature schemes for quantum resistance."""
    FALCON = "falcon"          # NIST PQC round 3 finalist (lattice-based)
    DILITHIUM = "dilithium"    # NIST PQC round 3 finalist (lattice-based)
    SPHINCS = "sphincs"        # NIST PQC round 3 alternate (hash-based)
    ONE_SHOT = "one_shot"      # One-shot signature scheme (quantum hybrid)
    ZK_ECDSA = "zk_ecdsa"      # Zero-knowledge proof with ECDSA (hybrid approach)


@pytest.fixture
def mock_keypair():
    """Create a mock keypair for quantum-resistant signatures."""
    keypair = MagicMock()
    keypair.id = str(uuid.uuid4())
    keypair.public_key = os.urandom(32).hex()
    keypair.private_key = os.urandom(32).hex()
    keypair.scheme = SignatureScheme.ONE_SHOT
    keypair.creation_time = time.time()
    keypair.expiration_time = time.time() + 30 * 24 * 60 * 60  # 30 days by default
    keypair.is_expired = MagicMock(return_value=False)
    
    return keypair


@pytest.fixture
def mock_token():
    """Create a mock one-time token for quantum authentication."""
    token = MagicMock()
    token.token_id = str(uuid.uuid4())
    token.token_value = os.urandom(16).hex()
    token.creation_time = time.time()
    token.expiration_time = time.time() + 300  # 5 minutes by default
    token.is_used = False
    token.used_time = None
    token.purpose = "authentication"
    token.is_valid = MagicMock(return_value=True)
    token.use_token = MagicMock(side_effect=lambda: setattr(token, 'is_used', True))
    
    return token


@pytest.fixture
def quantum_auth():
    """Create a mock QuantumResistantAuth class."""
    auth = MagicMock()
    
    # Setup mock keypairs and tokens stores
    auth._keypairs = {}
    auth._tokens = {}
    
    # Setup mock methods
    auth.generate_keypair.side_effect = _mock_generate_keypair
    auth.sign_message.side_effect = _mock_sign_message
    auth.verify_signature.side_effect = _mock_verify_signature
    auth.generate_one_time_token.side_effect = _mock_generate_token
    auth.validate_one_time_token.side_effect = _mock_validate_token
    auth.cleanup_expired_tokens.side_effect = _mock_cleanup_expired_tokens
    auth.emergency_key_rotation.side_effect = _mock_emergency_key_rotation
    
    return auth


def _mock_generate_keypair(scheme=None, expiration_days=None):
    """Mock implementation of generate_keypair."""
    scheme = scheme or SignatureScheme.ONE_SHOT
    
    keypair = MagicMock()
    keypair.id = str(uuid.uuid4())
    keypair.public_key = os.urandom(32).hex()
    keypair.private_key = os.urandom(32).hex()
    keypair.scheme = scheme
    keypair.creation_time = time.time()
    keypair.expiration_time = time.time() + (expiration_days or 30) * 24 * 60 * 60 if expiration_days is not None else None
    keypair.is_expired = MagicMock(return_value=False)
    
    return keypair


def _mock_sign_message(message, keypair):
    """Mock implementation of sign_message."""
    # Check if keypair is expired
    if keypair.is_expired():
        raise ValueError("Cannot sign with an expired keypair")
    
    # Create a signature based on the message and private key
    signature_base = f"{message.hex() if isinstance(message, bytes) else message}:{keypair.private_key}"
    signature = hashlib.sha256(signature_base.encode()).hexdigest()
    
    # For ONE_SHOT signatures, mark the keypair as expired after use
    if keypair.scheme == SignatureScheme.ONE_SHOT:
        keypair.is_expired.return_value = True
    
    return signature


def _mock_verify_signature(message, signature, public_key, scheme):
    """Mock implementation of verify_signature."""
    # For test purposes, we'll always return True unless it's a special test case
    if signature == "INVALID_SIGNATURE":
        return False
    
    return True


def _mock_generate_token(purpose="authentication", expiration_seconds=300):
    """Mock implementation of generate_one_time_token."""
    token = MagicMock()
    token.token_id = str(uuid.uuid4())
    token.token_value = os.urandom(16).hex()
    token.creation_time = time.time()
    token.expiration_time = time.time() + expiration_seconds
    token.is_used = False
    token.used_time = None
    token.purpose = purpose
    token.is_valid = MagicMock(return_value=True)
    token.use_token = MagicMock(side_effect=lambda: setattr(token, 'is_used', True))
    
    return token


def _mock_validate_token(token_id, token_value):
    """Mock implementation of validate_one_time_token."""
    # For test purposes, return True unless it's a special test case
    if token_id == "INVALID_TOKEN" or token_value == "INVALID_VALUE":
        return False
    
    return True


def _mock_cleanup_expired_tokens():
    """Mock implementation of cleanup_expired_tokens."""
    # Return a mock count of cleaned up tokens
    return 5


def _mock_emergency_key_rotation():
    """Mock implementation of emergency_key_rotation."""
    # Return a mock result of key rotation
    return {
        'rotated': 10,
        'failed': 0
    }


@pytest.fixture
def quantum_trading_client():
    """Create a mock trading client with quantum security integration."""
    client = MagicMock()
    client.quantum_auth = quantum_auth()
    
    # Add trading-specific methods
    client.execute_trade = MagicMock(side_effect=_mock_execute_trade)
    client.withdraw_funds = MagicMock(side_effect=_mock_withdraw_funds)
    client.verify_trade_signature = MagicMock(side_effect=_mock_verify_trade_signature)
    
    return client


def _mock_execute_trade(trade_data, keypair):
    """Mock implementation of execute_trade with quantum signatures."""
    # Check if keypair is valid
    if keypair.is_expired():
        return {"status": "error", "message": "Invalid quantum signature keypair"}
    
    # Sign the trade data
    signature = _mock_sign_message(str(trade_data).encode(), keypair)
    
    # Return success response with signature
    return {
        "status": "success",
        "trade_id": str(uuid.uuid4()),
        "signature": signature,
        "timestamp": time.time()
    }


def _mock_withdraw_funds(withdrawal_data, keypair):
    """Mock implementation of withdraw_funds with quantum signatures."""
    # Check if keypair is valid
    if keypair.is_expired():
        return {"status": "error", "message": "Invalid quantum signature keypair"}
    
    # Sign the withdrawal data
    signature = _mock_sign_message(str(withdrawal_data).encode(), keypair)
    
    # Return success response with signature
    return {
        "status": "success", 
        "withdrawal_id": str(uuid.uuid4()),
        "signature": signature,
        "timestamp": time.time()
    }


def _mock_verify_trade_signature(trade_data, signature, public_key, scheme):
    """Mock implementation of verify_trade_signature."""
    # Delegate to the general verify signature function
    return _mock_verify_signature(str(trade_data).encode(), signature, public_key, scheme) 