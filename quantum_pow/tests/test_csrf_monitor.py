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

Tests for the CSRF monitoring module in Quantum Proof-of-Work.

This test suite verifies the functionality of the CSRF monitoring system
that protects the qPoW API endpoints from Cross-Site Request Forgery attacks.
Inspired by the testing approach in the Apache ModSecurity CSRF project.

JAH BLESS SATOSHI
"""

import unittest
import sys
import os
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# Add the parent directory to the path so we can import quantum_pow
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules for testing
from quantum_pow.security.csrf_monitor import (
    CSRFRequest, 
    ParsingStrategy, 
    SQLRegexParsingStrategy,
    SQLASTParsingStrategy,
    WhitelistManager, 
    CSRFMonitor,
    CSRFProtectionMiddleware
)

class TestCSRFRequest(unittest.TestCase):
    """Test cases for the CSRFRequest class."""
    
    def test_request_creation(self):
        """Test that a CSRFRequest can be created with the correct attributes."""
        request = CSRFRequest(
            method="POST",
            path="/api/mine",
            params={"difficulty": "high"},
            headers={"Content-Type": "application/json"},
            body='{"nonce": 12345}',
            source_ip="127.0.0.1"
        )
        
        self.assertEqual(request.method, "POST")
        self.assertEqual(request.path, "/api/mine")
        self.assertEqual(request.params, {"difficulty": "high"})
        self.assertEqual(request.headers, {"Content-Type": "application/json"})
        self.assertEqual(request.body, '{"nonce": 12345}')
        self.assertEqual(request.source_ip, "127.0.0.1")
        self.assertTrue(hasattr(request, "timestamp"))
        self.assertTrue(hasattr(request, "request_hash"))
    
    def test_hash_calculation(self):
        """Test that the request hash is calculated correctly and consistently."""
        request1 = CSRFRequest(
            method="POST",
            path="/api/mine",
            params={"difficulty": "high"},
            headers={"Content-Type": "application/json"},
            body='{"nonce": 12345}',
            source_ip="127.0.0.1"
        )
        
        request2 = CSRFRequest(
            method="POST",
            path="/api/mine",
            params={"difficulty": "high"},
            headers={"Content-Type": "application/json"}, 
            body='{"nonce": 12345}',
            source_ip="192.168.1.1"  # Different IP shouldn't affect hash
        )
        
        # Same request parameters should produce the same hash
        self.assertEqual(request1.request_hash, request2.request_hash)
        
        # Different request parameters should produce different hashes
        request3 = CSRFRequest(
            method="POST",
            path="/api/mine",
            params={"difficulty": "low"},  # Changed parameter
            headers={"Content-Type": "application/json"},
            body='{"nonce": 12345}',
            source_ip="127.0.0.1"
        )
        
        self.assertNotEqual(request1.request_hash, request3.request_hash)
    
    def test_to_dict_and_from_dict(self):
        """Test serialization and deserialization of CSRFRequest."""
        original_request = CSRFRequest(
            method="POST",
            path="/api/mine",
            params={"difficulty": "high"},
            headers={"Content-Type": "application/json"},
            body='{"nonce": 12345}',
            source_ip="127.0.0.1"
        )
        
        # Convert to dict
        request_dict = original_request.to_dict()
        
        # Create new request from dict
        deserialized_request = CSRFRequest.from_dict(request_dict)
        
        # Check that the deserialized request matches the original
        self.assertEqual(deserialized_request.method, original_request.method)
        self.assertEqual(deserialized_request.path, original_request.path)
        self.assertEqual(deserialized_request.params, original_request.params)
        self.assertEqual(deserialized_request.headers, original_request.headers)
        self.assertEqual(deserialized_request.body, original_request.body)
        self.assertEqual(deserialized_request.source_ip, original_request.source_ip)
        
        # Hash should be recalculated and match the original
        self.assertEqual(deserialized_request.request_hash, original_request.request_hash)

class TestSQLRegexParsingStrategy(unittest.TestCase):
    """Test cases for the SQLRegexParsingStrategy."""
    
    def setUp(self):
        """Set up the test fixtures."""
        self.strategy = SQLRegexParsingStrategy()
    
    def test_sql_detection_in_body(self):
        """Test that SQL operations are detected in the request body."""
        # Test SELECT operation
        request = CSRFRequest(
            method="POST",
            path="/api/query",
            params={},
            headers={},
            body="SELECT * FROM users",
            source_ip="127.0.0.1"
        )
        self.assertTrue(self.strategy.parse(request))
        
        # Test INSERT operation
        request = CSRFRequest(
            method="POST",
            path="/api/query",
            params={},
            headers={},
            body="INSERT INTO users VALUES ('hacker', 'password')",
            source_ip="127.0.0.1"
        )
        self.assertTrue(self.strategy.parse(request))
        
        # Test UPDATE operation
        request = CSRFRequest(
            method="POST",
            path="/api/query",
            params={},
            headers={},
            body="UPDATE users SET password = 'hacked' WHERE username = 'admin'",
            source_ip="127.0.0.1"
        )
        self.assertTrue(self.strategy.parse(request))
        
        # Test DELETE operation
        request = CSRFRequest(
            method="POST",
            path="/api/query",
            params={},
            headers={},
            body="DELETE FROM users WHERE username = 'admin'",
            source_ip="127.0.0.1"
        )
        self.assertTrue(self.strategy.parse(request))
        
        # Test DROP operation
        request = CSRFRequest(
            method="POST",
            path="/api/query",
            params={},
            headers={},
            body="DROP TABLE users",
            source_ip="127.0.0.1"
        )
        self.assertTrue(self.strategy.parse(request))
    
    def test_sql_detection_in_params(self):
        """Test that SQL operations are detected in the request parameters."""
        # Test SELECT operation in params
        request = CSRFRequest(
            method="GET",
            path="/api/query",
            params={"query": "SELECT * FROM users"},
            headers={},
            body="",
            source_ip="127.0.0.1"
        )
        self.assertTrue(self.strategy.parse(request))
    
    def test_safe_requests(self):
        """Test that safe requests are not flagged."""
        # Test a safe request
        request = CSRFRequest(
            method="POST",
            path="/api/mine",
            params={"difficulty": "high"},
            headers={},
            body='{"nonce": 12345}',
            source_ip="127.0.0.1"
        )
        self.assertFalse(self.strategy.parse(request))
        
        # Test a request with SQL-like text that isn't actually SQL
        request = CSRFRequest(
            method="POST",
            path="/api/comment",
            params={},
            headers={},
            body="I like to select good movies from Netflix",
            source_ip="127.0.0.1"
        )
        self.assertFalse(self.strategy.parse(request))

class TestSQLASTParsingStrategy(unittest.TestCase):
    """Test cases for the SQLASTParsingStrategy."""
    
    def setUp(self):
        """Set up the test fixtures."""
        self.strategy = SQLASTParsingStrategy()
    
    def test_sql_detection(self):
        """Test that SQL operations are detected using AST parsing."""
        # Test SQL keywords in body
        request = CSRFRequest(
            method="POST",
            path="/api/query",
            params={},
            headers={},
            body="select id from users",
            source_ip="127.0.0.1"
        )
        self.assertTrue(self.strategy.parse(request))
    
    def test_safe_requests(self):
        """Test that safe requests are not flagged."""
        # Test a safe request
        request = CSRFRequest(
            method="POST",
            path="/api/mine",
            params={},
            headers={},
            body='{"nonce": 12345}',
            source_ip="127.0.0.1"
        )
        self.assertFalse(self.strategy.parse(request))

class TestWhitelistManager(unittest.TestCase):
    """Test cases for the WhitelistManager."""
    
    def setUp(self):
        """Set up the test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        self.whitelist_file = os.path.join(self.temp_dir, "test_whitelist.json")
        self.whitelist_manager = WhitelistManager(self.whitelist_file)
    
    def tearDown(self):
        """Clean up after the tests."""
        # Remove the temporary directory
        shutil.rmtree(self.temp_dir)
    
    def test_add_to_whitelist(self):
        """Test adding a request to the whitelist."""
        request = CSRFRequest(
            method="POST",
            path="/api/mine",
            params={"difficulty": "high"},
            headers={},
            body='{"nonce": 12345}',
            source_ip="127.0.0.1"
        )
        
        # Initially, request should not be whitelisted
        self.assertFalse(self.whitelist_manager.is_whitelisted(request))
        
        # Add request to whitelist
        self.whitelist_manager.add_to_whitelist(request)
        
        # Now request should be whitelisted
        self.assertTrue(self.whitelist_manager.is_whitelisted(request))
        
        # Check that the whitelist file was created and contains the correct data
        self.assertTrue(os.path.exists(self.whitelist_file))
        with open(self.whitelist_file, 'r') as f:
            whitelist_data = json.load(f)
            self.assertIn(request.request_hash, whitelist_data.get("whitelist", []))
    
    def test_load_existing_whitelist(self):
        """Test loading an existing whitelist file."""
        # Create a whitelist file with some hashes
        test_hashes = ["hash1", "hash2", "hash3"]
        with open(self.whitelist_file, 'w') as f:
            json.dump({"whitelist": test_hashes}, f)
        
        # Load the whitelist
        manager = WhitelistManager(self.whitelist_file)
        
        # Check that the hashes were loaded
        for test_hash in test_hashes:
            self.assertIn(test_hash, manager.whitelist)
    
    def test_handle_invalid_whitelist_file(self):
        """Test handling an invalid whitelist file."""
        # Create an invalid whitelist file
        with open(self.whitelist_file, 'w') as f:
            f.write("This is not valid JSON")
        
        # Load the whitelist - should not raise an exception and should create an empty whitelist
        manager = WhitelistManager(self.whitelist_file)
        self.assertEqual(len(manager.whitelist), 0)

class TestCSRFMonitor(unittest.TestCase):
    """Test cases for the CSRFMonitor."""
    
    def setUp(self):
        """Set up the test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        self.whitelist_file = os.path.join(self.temp_dir, "test_whitelist.json")
        self.csrf_monitor = CSRFMonitor(self.whitelist_file)
    
    def tearDown(self):
        """Clean up after the tests."""
        # Remove the temporary directory
        shutil.rmtree(self.temp_dir)
    
    def test_check_unsafe_request(self):
        """Test checking an unsafe request."""
        # Create a request with SQL injection
        request = CSRFRequest(
            method="POST",
            path="/api/query",
            params={},
            headers={},
            body="SELECT * FROM users",
            source_ip="127.0.0.1"
        )
        
        # Check the request - should be unsafe
        is_safe, reason = self.csrf_monitor.check_request(request)
        self.assertFalse(is_safe)
        self.assertIn("SQLRegexParsingStrategy", reason)
    
    def test_check_safe_request(self):
        """Test checking a safe request."""
        # Create a safe request
        request = CSRFRequest(
            method="POST",
            path="/api/mine",
            params={"difficulty": "high"},
            headers={},
            body='{"nonce": 12345}',
            source_ip="127.0.0.1"
        )
        
        # Check the request - should be safe
        is_safe, reason = self.csrf_monitor.check_request(request)
        self.assertTrue(is_safe)
        self.assertEqual(reason, "Request passed all security checks")
    
    def test_check_whitelisted_request(self):
        """Test checking a whitelisted request."""
        # Create a request
        request = CSRFRequest(
            method="POST",
            path="/api/query",
            params={},
            headers={},
            body="SELECT * FROM mining_stats",  # Would normally be unsafe
            source_ip="127.0.0.1"
        )
        
        # Add to whitelist
        self.csrf_monitor.add_to_whitelist(request)
        
        # Check the request - should be safe because it's whitelisted
        is_safe, reason = self.csrf_monitor.check_request(request)
        self.assertTrue(is_safe)
        self.assertEqual(reason, "Request is whitelisted")
    
    def test_add_parsing_strategy(self):
        """Test adding a new parsing strategy."""
        # Create a mock strategy
        mock_strategy = MagicMock(spec=ParsingStrategy)
        mock_strategy.__class__.__name__ = "MockStrategy"
        mock_strategy.parse.return_value = True  # Always flags requests as unsafe
        
        # Add the strategy
        self.csrf_monitor.add_parsing_strategy(mock_strategy)
        
        # Create a request that would normally be safe
        request = CSRFRequest(
            method="POST",
            path="/api/mine",
            params={"difficulty": "high"},
            headers={},
            body='{"nonce": 12345}',
            source_ip="127.0.0.1"
        )
        
        # Check the request - should be unsafe because of the mock strategy
        is_safe, reason = self.csrf_monitor.check_request(request)
        self.assertFalse(is_safe)
        self.assertIn("MockStrategy", reason)
        
        # Verify the mock was called
        mock_strategy.parse.assert_called_once()

class TestCSRFProtectionMiddleware(unittest.TestCase):
    """Test cases for the CSRFProtectionMiddleware."""
    
    def setUp(self):
        """Set up the test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        self.whitelist_file = os.path.join(self.temp_dir, "test_whitelist.json")
        self.middleware = CSRFProtectionMiddleware(self.whitelist_file)
    
    def tearDown(self):
        """Clean up after the tests."""
        # Remove the temporary directory
        shutil.rmtree(self.temp_dir)
    
    def test_process_safe_request(self):
        """Test processing a safe request."""
        # Process a safe request
        is_safe, reason = self.middleware.process_request(
            method="POST",
            path="/api/mine",
            params={"difficulty": "high"},
            headers={"Content-Type": "application/json"},
            body='{"nonce": 12345}',
            source_ip="127.0.0.1"
        )
        
        self.assertTrue(is_safe)
        self.assertEqual(reason, "Request passed all security checks")
    
    def test_process_unsafe_request(self):
        """Test processing an unsafe request."""
        # Process an unsafe request
        is_safe, reason = self.middleware.process_request(
            method="POST",
            path="/api/query",
            params={},
            headers={"Content-Type": "application/json"},
            body="SELECT * FROM users",
            source_ip="127.0.0.1"
        )
        
        self.assertFalse(is_safe)
        self.assertIn("SQLRegexParsingStrategy", reason)
    
    def test_add_to_whitelist(self):
        """Test adding a request to the whitelist."""
        # Add a request to the whitelist
        self.middleware.add_to_whitelist(
            method="POST",
            path="/api/query",
            params={},
            headers={"Content-Type": "application/json"},
            body="SELECT * FROM mining_stats",  # Would normally be unsafe
            source_ip="127.0.0.1"
        )
        
        # Process the same request - should be safe now
        is_safe, reason = self.middleware.process_request(
            method="POST",
            path="/api/query",
            params={},
            headers={"Content-Type": "application/json"},
            body="SELECT * FROM mining_stats",
            source_ip="127.0.0.1"
        )
        
        self.assertTrue(is_safe)
        self.assertEqual(reason, "Request is whitelisted")

if __name__ == '__main__':
    unittest.main() 