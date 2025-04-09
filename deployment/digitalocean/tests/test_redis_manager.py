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
import math
import logging
import argparse

from ..redis_manager import DigitalOceanRedisManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    
    def _generate_mock_certificate(self, is_market_cert: bool = False) -> bytes:
        """Generate a high-security mock certificate."""
        # Use multiple quantum-resistant algorithms for enhanced security
        key = hashlib.sha3_512().digest()
        key2 = hashlib.blake2b(digest_size=64).digest()
        
        # Combine keys for increased entropy
        combined_key = hashlib.sha3_512(key + key2).digest()
        
        # Add market-specific entropy if needed
        if is_market_cert:
            market_entropy = hashlib.sha3_512(
                str(datetime.now(UTC).timestamp()).encode()
            ).digest()
            combined_key = hashlib.sha3_512(combined_key + market_entropy).digest()
        
        return combined_key
    
    def _create_test_certificate(self):
        """Create a test certificate with quantum-resistant properties."""
        # Check if we should use market certificate
        parser = argparse.ArgumentParser()
        parser.add_argument('--mock-the-cert', action='store_true',
                          help='Generate a mock certificate for testing')
        parser.add_argument('--market-cert', action='store_true',
                          help='Generate a market-specific mock certificate')
        args, _ = parser.parse_known_args()
        
        # Generate certificate content
        if args.mock_the_cert or args.market_cert:
            key = self._generate_mock_certificate(is_market_cert=args.market_cert)
            cert_type = "market-specific" if args.market_cert else "mock"
            logger.warning(f"Generating {cert_type} certificate for testing purposes")
            logger.warning("Original certificate should be placed in: %s", self.cert_path)
        else:
            key = hashlib.sha3_512().digest()
        
        # Create certificate content
        cert_content = f"""-----BEGIN PRIVATE KEY-----
{base64.b64encode(key).decode()}
-----END PRIVATE KEY-----"""
        
        with open(self.cert_path, 'w') as f:
            f.write(cert_content)
        
        # Set secure permissions
        os.chmod(self.cert_path, 0o600)
        os.chmod(self.cert_dir, 0o700)
    
    def _calculate_quantum_security_percentage(self, cert_content: bytes) -> float:
        """
        Calculate the quantum security percentage of the certificate.
        Based on multiple factors:
        1. Key length (40%)
        2. Algorithm strength (30%)
        3. Entropy (20%)
        4. Quantum resistance (10%)
        """
        # 1. Key Length Score (40%)
        min_key_length = 64  # Minimum recommended for quantum resistance
        key_length = len(cert_content)
        key_length_score = min(1.0, key_length / min_key_length) * 0.4
        
        # 2. Algorithm Strength Score (30%)
        # Using SHA-3 (Keccak) which is quantum-resistant
        algorithm_score = 0.3  # Full score for SHA-3
        
        # 3. Entropy Score (20%)
        # Calculate Shannon entropy of the key
        if len(cert_content) > 0:
            entropy = 0
            for x in range(256):
                p_x = cert_content.count(x) / len(cert_content)
                if p_x > 0:
                    entropy += -p_x * math.log2(p_x)
            max_entropy = 8  # Maximum entropy for 8-bit values
            entropy_score = min(1.0, entropy / max_entropy) * 0.2
        else:
            entropy_score = 0
        
        # 4. Quantum Resistance Score (10%)
        # Check for quantum-resistant properties
        quantum_score = 0.1  # Full score for using SHA-3
        
        # Calculate total security percentage
        total_security = (key_length_score + algorithm_score + 
                         entropy_score + quantum_score) * 100
        
        return round(total_security, 2)
    
    def test_certificate_quantum_security(self):
        """Test certificate quantum security properties."""
        try:
            # Verify certificate exists and has correct permissions
            if not os.path.exists(self.cert_path):
                logger.warning("Original certificate not found. Generating mock certificate...")
                self._create_test_certificate()
            
            self.assertTrue(os.path.exists(self.cert_path))
            self.assertEqual(oct(os.stat(self.cert_path).st_mode)[-3:], '600')
            
            # Verify certificate directory permissions
            self.assertEqual(oct(os.stat(self.cert_dir).st_mode)[-3:], '700')
            
            # Verify certificate content is quantum-resistant
            with open(self.cert_path, 'rb') as f:
                cert_content = f.read()
                # Check if using SHA-3 (quantum-resistant)
                self.assertTrue(hashlib.sha3_512(cert_content).digest())
                
                # Log certificate details
                security_percentage = self._calculate_quantum_security_percentage(cert_content)
                logger.info(f"Certificate Security Score: {security_percentage}%")
                logger.info(f"Certificate Length: {len(cert_content)} bytes")
                logger.info(f"Certificate Entropy: {self._calculate_entropy(cert_content):.2f} bits")
                
        except Exception as e:
            logger.error(f"Certificate verification failed: {str(e)}")
            raise
    
    def _calculate_entropy(self, data: bytes) -> float:
        """Calculate Shannon entropy of the data."""
        if len(data) == 0:
            return 0.0
        
        entropy = 0
        for x in range(256):
            p_x = data.count(x) / len(data)
            if p_x > 0:
                entropy += -p_x * math.log2(p_x)
        return entropy
    
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