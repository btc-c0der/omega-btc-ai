"""
Test Redis configuration for OMEGA BTC AI.
This file contains test-specific Redis settings that won't interfere with production data.
"""

import os
from typing import Dict, Any

def get_test_redis_config() -> Dict[str, Any]:
    """
    Get test Redis configuration from environment variables with fallback to defaults.
    
    Returns:
        dict: Redis connection parameters for testing
    """
    # Check if we should use local Redis for testing
    use_local = os.getenv('OMEGA_USE_LOCAL_REDIS', 'true').lower() == 'true'
    
    if use_local:
        # Local test Redis configuration
        return {
            'host': os.getenv('TEST_REDIS_HOST', 'localhost'),
            'port': int(os.getenv('TEST_REDIS_PORT', '6379')),
            'db': int(os.getenv('TEST_REDIS_DB', '1')),  # Use different DB for tests
            'decode_responses': True
        }
    else:
        # Remote test Redis configuration
        return {
            'host': os.getenv('TEST_REDIS_HOST', 'redis-19332.fcrce173.eu-west-1-1.ec2.redns.redis-cloud.com'),
            'port': int(os.getenv('TEST_REDIS_PORT', '19332')),
            'username': os.getenv('TEST_REDIS_USERNAME', 'omega'),
            'password': os.getenv('TEST_REDIS_PASSWORD', 'VuKJU8Z.Z2V8Qn_'),
            'ssl': True,
            'ssl_ca_certs': os.getenv('TEST_REDIS_CERT', 'SSL_redis-btc-omega-redis.pem'),
            'decode_responses': True
        } 