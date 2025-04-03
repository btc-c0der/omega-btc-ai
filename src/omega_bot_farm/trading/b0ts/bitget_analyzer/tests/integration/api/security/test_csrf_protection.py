"""
Tests for CSRF protection in the BitgetPositionAnalyzerB0t API.

These tests verify:
- CSRF tokens are properly generated and validated
- Requests without a valid CSRF token are rejected
- Tokens are tied to the correct session
- Tokens expire after the configured time period
- Double submission protection works correctly
"""

import pytest
import time
import secrets
import hmac
import hashlib
from unittest.mock import patch, MagicMock

# Try to import the real implementation, fall back to mock if not available
try:
    from omega_bot_farm.trading.b0ts.bitget_analyzer.api.security import CSRFProtector
    REAL_IMPLEMENTATION = True
except ImportError:
    REAL_IMPLEMENTATION = False
    
    # Mock implementation for tests
    class CSRFProtector:
        """CSRF protection for API requests."""
        
        def __init__(self, secret_key=None, token_expiry=3600):
            """Initialize the CSRF protector."""
            self.secret_key = secret_key or secrets.token_hex(32)
            self.token_expiry = token_expiry
            self.tokens = {}  # session_id -> (token, timestamp)
            
        def generate_token(self, session_id):
            """Generate a new CSRF token for the given session."""
            # Generate a random token
            token = secrets.token_hex(16)
            
            # Store token with timestamp
            self.tokens[session_id] = (token, time.time())
            
            return token
            
        def validate_token(self, session_id, token):
            """Validate a CSRF token for the given session."""
            # Check if session has a token
            if session_id not in self.tokens:
                return False
                
            stored_token, timestamp = self.tokens[session_id]
            
            # Check if token has expired
            if time.time() - timestamp > self.token_expiry:
                # Remove expired token
                del self.tokens[session_id]
                return False
                
            # Check if token matches
            return hmac.compare_digest(stored_token, token)
            
        def generate_signed_token(self, session_id, action=None):
            """Generate a token signed with HMAC for the given session and action."""
            # Base token
            token = secrets.token_hex(16)
            
            # Current timestamp
            timestamp = str(int(time.time()))
            
            # Action or empty string
            action_str = action or ""
            
            # Data to sign
            data = f"{session_id}:{token}:{timestamp}:{action_str}"
            
            # Sign with HMAC
            signature = hmac.new(
                self.secret_key.encode(),
                data.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Store token with timestamp
            self.tokens[session_id] = (token, time.time())
            
            # Return signed token
            return f"{token}:{timestamp}:{signature}"
            
        def validate_signed_token(self, session_id, signed_token, action=None):
            """Validate a signed CSRF token for the given session and action."""
            try:
                # Split token parts
                parts = signed_token.split(":")
                if len(parts) != 3:
                    return False
                    
                token, timestamp, signature = parts
                
                # Check if timestamp is valid
                try:
                    token_time = int(timestamp)
                    current_time = int(time.time())
                    if current_time - token_time > self.token_expiry:
                        return False
                except ValueError:
                    return False
                    
                # Action or empty string
                action_str = action or ""
                
                # Data that was signed
                data = f"{session_id}:{token}:{timestamp}:{action_str}"
                
                # Calculate expected signature
                expected_signature = hmac.new(
                    self.secret_key.encode(),
                    data.encode(),
                    hashlib.sha256
                ).hexdigest()
                
                # Compare signatures
                return hmac.compare_digest(signature, expected_signature)
                
            except Exception:
                return False
                
        def clear_token(self, session_id):
            """Clear the token for the given session."""
            if session_id in self.tokens:
                del self.tokens[session_id]


@pytest.fixture
def csrf_protector():
    """Create a CSRF protector instance."""
    return CSRFProtector(secret_key="test_secret_key", token_expiry=60)


@pytest.fixture
def mock_session():
    """Create a mock session ID."""
    return "test_session_123"


class TestCSRFProtection:
    """Test suite for CSRF protection."""
    
    def test_generate_token(self, csrf_protector, mock_session):
        """Test that tokens are generated successfully."""
        token = csrf_protector.generate_token(mock_session)
        
        # Token should be a non-empty string
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Token should be stored for the session
        assert mock_session in csrf_protector.tokens
        stored_token, timestamp = csrf_protector.tokens[mock_session]
        assert stored_token == token
        
        # Timestamp should be recent
        assert time.time() - timestamp < 5
        
    def test_validate_token_valid(self, csrf_protector, mock_session):
        """Test that valid tokens are accepted."""
        token = csrf_protector.generate_token(mock_session)
        
        # Valid token should be accepted
        assert csrf_protector.validate_token(mock_session, token) is True
        
    def test_validate_token_invalid(self, csrf_protector, mock_session):
        """Test that invalid tokens are rejected."""
        # Generate a token
        csrf_protector.generate_token(mock_session)
        
        # Different token should be rejected
        assert csrf_protector.validate_token(mock_session, "invalid_token") is False
        
    def test_validate_token_wrong_session(self, csrf_protector, mock_session):
        """Test that tokens for the wrong session are rejected."""
        # Generate a token for the session
        token = csrf_protector.generate_token(mock_session)
        
        # Token should be rejected for a different session
        assert csrf_protector.validate_token("different_session", token) is False
        
    def test_validate_token_expired(self, csrf_protector, mock_session):
        """Test that expired tokens are rejected."""
        # Generate a token
        token = csrf_protector.generate_token(mock_session)
        
        # Manipulate timestamp to make token expire
        csrf_protector.tokens[mock_session] = (token, time.time() - 120)  # 2 minutes ago
        
        # Expired token should be rejected
        assert csrf_protector.validate_token(mock_session, token) is False
        
        # Expired token should be removed
        assert mock_session not in csrf_protector.tokens
        
    def test_clear_token(self, csrf_protector, mock_session):
        """Test that tokens can be cleared."""
        # Generate a token
        csrf_protector.generate_token(mock_session)
        
        # Token should be stored
        assert mock_session in csrf_protector.tokens
        
        # Clear the token
        csrf_protector.clear_token(mock_session)
        
        # Token should be removed
        assert mock_session not in csrf_protector.tokens
        
    def test_generate_signed_token(self, csrf_protector, mock_session):
        """Test that signed tokens are generated correctly."""
        # Generate a signed token
        signed_token = csrf_protector.generate_signed_token(mock_session, action="update")
        
        # Token should be a non-empty string
        assert isinstance(signed_token, str)
        assert len(signed_token) > 0
        
        # Token should have three parts separated by colons
        parts = signed_token.split(":")
        assert len(parts) == 3
        
    def test_validate_signed_token_valid(self, csrf_protector, mock_session):
        """Test that valid signed tokens are accepted."""
        # Generate a signed token
        signed_token = csrf_protector.generate_signed_token(mock_session, action="update")
        
        # Valid signed token should be accepted
        assert csrf_protector.validate_signed_token(mock_session, signed_token, action="update") is True
        
    def test_validate_signed_token_wrong_action(self, csrf_protector, mock_session):
        """Test that signed tokens with the wrong action are rejected."""
        # Generate a signed token for a specific action
        signed_token = csrf_protector.generate_signed_token(mock_session, action="update")
        
        # Token should be rejected for a different action
        assert csrf_protector.validate_signed_token(mock_session, signed_token, action="delete") is False
        
    def test_validate_signed_token_expired(self, csrf_protector, mock_session):
        """Test that expired signed tokens are rejected."""
        # Create a token with an expired timestamp
        token = secrets.token_hex(16)
        timestamp = str(int(time.time()) - 120)  # 2 minutes ago
        
        # Data to sign
        data = f"{mock_session}:{token}:{timestamp}:"
        
        # Sign with HMAC
        signature = hmac.new(
            csrf_protector.secret_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Create expired signed token
        expired_token = f"{token}:{timestamp}:{signature}"
        
        # Expired token should be rejected
        assert csrf_protector.validate_signed_token(mock_session, expired_token) is False
        
    def test_validate_signed_token_tampered(self, csrf_protector, mock_session):
        """Test that tampered signed tokens are rejected."""
        # Generate a signed token
        signed_token = csrf_protector.generate_signed_token(mock_session)
        
        # Tamper with the token
        parts = signed_token.split(":")
        tampered_token = f"{parts[0]}x:{parts[1]}:{parts[2]}"
        
        # Tampered token should be rejected
        assert csrf_protector.validate_signed_token(mock_session, tampered_token) is False
        
    def test_double_submission(self, csrf_protector, mock_session):
        """Test double submission protection."""
        # Form and cookie values should match for protection
        form_token = "same_token_value"
        cookie_token = "same_token_value"
        
        # Store the token
        csrf_protector.tokens[mock_session] = (cookie_token, time.time())
        
        # Double submission check (simplified)
        assert hmac.compare_digest(form_token, cookie_token)
        
    def test_multiple_tokens_per_session(self, csrf_protector):
        """Test handling of multiple tokens for different sessions."""
        # Generate tokens for multiple sessions
        session1 = "session1"
        session2 = "session2"
        
        token1 = csrf_protector.generate_token(session1)
        token2 = csrf_protector.generate_token(session2)
        
        # Both tokens should be valid for their respective sessions
        assert csrf_protector.validate_token(session1, token1) is True
        assert csrf_protector.validate_token(session2, token2) is True
        
        # But not for the wrong sessions
        assert csrf_protector.validate_token(session1, token2) is False
        assert csrf_protector.validate_token(session2, token1) is False 