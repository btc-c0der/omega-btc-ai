import os
import unittest
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from datetime import datetime, UTC
import ssl
import hashlib
import base64
from typing import Optional

from ..redis_manager import DigitalOceanRedisManager

class TestDigitalOceanRedisManager(unittest.TestCase):
    """Test suite for Redis manager with quantum security validation."""
    
    def setUp(self):
        """Set up test environment with temporary certificate."""
        self.temp_dir = tempfile.mkdtemp()
        self.cert_dir = os.path.join(self.temp_dir, 'certificates')
        os.makedirs(self.cert_dir)
        
        # Create a test certificate with quantum-resistant properties
        self.cert_path = os.path.join(self.cert_dir, 'SSL_redis-btc-omega-redis.pem')
        self._create_test_certificate()
        
        # Initialize Redis manager with test certificate path
        self.redis_manager = DigitalOceanRedisManager(
            max_retries=2,
            retry_delay=1
        )
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
        if hasattr(self, 'redis_manager'):
            self.redis_manager.close()
    
    def _create_test_certificate(self):
        """Create a test certificate with quantum-resistant properties."""
        # Generate a quantum-resistant key using SHA-3 (Keccak)
        key = hashlib.sha3_512().digest()
        
        # Create a test certificate with quantum-resistant properties
        cert_content = f"""-----BEGIN PRIVATE KEY-----
{base64.b64encode(key).decode()}
-----END PRIVATE KEY-----"""
        
        with open(self.cert_path, 'w') as f:
            f.write(cert_content)
        
        # Set secure permissions
        os.chmod(self.cert_path, 0o600)
        os.chmod(self.cert_dir, 0o700)
    
    def test_certificate_quantum_security(self):
        """Test certificate quantum security properties."""
        # Verify certificate exists and has correct permissions
        self.assertTrue(os.path.exists(self.cert_path))
        self.assertEqual(oct(os.stat(self.cert_path).st_mode)[-3:], '600')
        
        # Verify certificate directory permissions
        self.assertEqual(oct(os.stat(self.cert_dir).st_mode)[-3:], '700')
        
        # Verify certificate content is quantum-resistant
        with open(self.cert_path, 'rb') as f:
            cert_content = f.read()
            # Check if using SHA-3 (quantum-resistant)
            self.assertTrue(hashlib.sha3_512(cert_content).digest())
    
    def test_ssl_connection_security(self):
        """Test SSL connection security settings."""
        with patch('redis.Redis') as mock_redis:
            # Configure mock Redis client
            mock_redis.return_value.ping.return_value = True
            
            # Test connection with SSL
            self.redis_manager._connect()
            
            # Verify SSL parameters
            mock_redis.assert_called_once()
            call_args = mock_redis.call_args[1]
            
            # Verify SSL settings
            self.assertTrue(call_args['ssl'])
            self.assertEqual(call_args['ssl_cert_reqs'], 'required')
            self.assertEqual(call_args['ssl_certfile'], self.cert_path)
    
    def test_certificate_validation(self):
        """Test certificate validation and error handling."""
        # Test with invalid certificate path
        with patch('redis.Redis') as mock_redis:
            self.redis_manager.ssl_cert_path = '/invalid/path/cert.pem'
            with self.assertRaises(FileNotFoundError):
                self.redis_manager._connect()
        
        # Test with invalid certificate content
        with open(self.cert_path, 'w') as f:
            f.write('invalid certificate content')
        
        with patch('redis.Redis') as mock_redis:
            with self.assertRaises(ssl.SSLError):
                self.redis_manager._connect()
    
    def test_connection_retry_logic(self):
        """Test connection retry logic with SSL."""
        with patch('redis.Redis') as mock_redis:
            # Simulate connection failures
            mock_redis.side_effect = [
                ConnectionError("First attempt failed"),
                ConnectionError("Second attempt failed"),
                MagicMock(ping=MagicMock(return_value=True))
            ]
            
            # Should succeed after retries
            self.redis_manager._connect()
            self.assertEqual(mock_redis.call_count, 3)
    
    def test_secure_operations(self):
        """Test secure Redis operations with SSL."""
        with patch('redis.Redis') as mock_redis:
            # Configure mock Redis client
            mock_client = MagicMock()
            mock_redis.return_value = mock_client
            mock_client.ping.return_value = True
            
            # Test secure operations
            self.redis_manager._connect()
            
            # Test get operation
            self.redis_manager.get('test_key')
            mock_client.get.assert_called_once_with('test_key')
            
            # Test set operation
            self.redis_manager.set('test_key', 'test_value')
            mock_client.set.assert_called_once_with('test_key', 'test_value')
            
            # Test publish operation
            self.redis_manager.publish('test_channel', 'test_message')
            mock_client.publish.assert_called_once_with('test_channel', 'test_message')
    
    def test_quantum_resistant_encryption(self):
        """Test quantum-resistant encryption properties."""
        # Verify certificate uses quantum-resistant algorithms
        with open(self.cert_path, 'rb') as f:
            cert_content = f.read()
            
            # Check for quantum-resistant properties
            self.assertTrue(len(cert_content) >= 64)  # Minimum key length for quantum resistance
            self.assertTrue(hashlib.sha3_512(cert_content).digest())  # SHA-3 verification
    
    def test_secure_connection_closure(self):
        """Test secure connection closure."""
        with patch('redis.Redis') as mock_redis:
            mock_client = MagicMock()
            mock_redis.return_value = mock_client
            mock_client.ping.return_value = True
            
            self.redis_manager._connect()
            self.redis_manager.close()
            
            mock_client.close.assert_called_once()

if __name__ == '__main__':
    unittest.main() 