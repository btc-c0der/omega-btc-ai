
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

import os
from typing import Dict, Any

def get_redis_config() -> Dict[str, Any]:
    """
    Get Redis configuration from environment variables with fallback to defaults
    
    Returns:
        dict: Redis connection parameters
    """
    # Check for environment variable to determine if we use cloud or local Redis
    use_cloud = os.environ.get('OMEGA_USE_CLOUD_REDIS', 'false').lower() == 'true'
    
    if use_cloud:
        # Cloud Redis configuration
        return {
            'host': os.environ.get('REDIS_HOST', 'redis-19332.fcrce173.eu-west-1-1.ec2.redns.redis-cloud.com'),
            'port': int(os.environ.get('REDIS_PORT', '19332')),
            'username': os.environ.get('REDIS_USERNAME', 'omega'),
            'password': os.environ.get('REDIS_PASSWORD', ''),
            'ssl': True,
            'ssl_ca_certs': os.environ.get('REDIS_CERT', 'SSL_redis-btc-omega-redis.pem')
        }
    else:
        # Local Redis configuration
        return {
            'host': os.environ.get('REDIS_HOST', 'localhost'),
            'port': int(os.environ.get('REDIS_PORT', '6379')),
            'db': int(os.environ.get('REDIS_DB', '0')),
            'username': os.environ.get('REDIS_USERNAME', None),
            'password': os.environ.get('REDIS_PASSWORD', None),
            'ssl': False
        } 