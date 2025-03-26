import os
from typing import Dict, Any
import ssl
import redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry

def get_redis_config() -> Dict[str, Any]:
    """
    Get Redis configuration from environment variables with fallback to defaults
    
    Returns:
        dict: Redis connection parameters
    """
    # Check if we're in test mode
    is_test = os.environ.get('OMEGA_TEST_USE_LOCAL_REDIS', 'false').lower() == 'true'
    
    if is_test:
        config = {
            'host': 'localhost',
            'port': 6379,
            'db': 0,
            'decode_responses': True
        }
        
        # Add test credentials if provided
        test_username = os.environ.get('TEST_REDIS_USERNAME')
        test_password = os.environ.get('TEST_REDIS_PASSWORD')
        if test_username:
            config['username'] = test_username
        if test_password:
            config['password'] = test_password
            
        return config
    else:
        # Remote Redis configuration
        config = {
            'host': os.environ.get('REDIS_HOST', 'redis-19332.fcrce173.eu-west-1-1.ec2.redns.redis-cloud.com'),
            'port': int(os.environ.get('REDIS_PORT', '19332')),
            'db': int(os.environ.get('REDIS_DB', '0')),
            'decode_responses': True,
            'username': os.environ.get('REDIS_USERNAME', 'omega'),
            'password': os.environ.get('REDIS_PASSWORD', 'VuKJU8Z.Z2V8Qn_'),
            'retry_on_timeout': True,
            'retry_on_error': [redis.ConnectionError],
            'retry': Retry(ExponentialBackoff(), retries=3)
        }
        
        # Temporarily disable SSL
        return config

    # SSL Configuration
    if os.environ.get('REDIS_USE_TLS', 'true').lower() == 'true':
        config['ssl'] = True
        config['ssl_cert_reqs'] = ssl.CERT_NONE  # Use ssl.CERT_NONE instead of 'none'
        config['ssl_check_hostname'] = False
        
        # Check for SSL certificate
        cert_path = os.environ.get('REDIS_CERT')
        if cert_path and os.path.exists(cert_path):
            config['ssl_ca_certs'] = cert_path
            config['ssl_cert_reqs'] = ssl.CERT_REQUIRED
            config['ssl_check_hostname'] = True
    
    return config 