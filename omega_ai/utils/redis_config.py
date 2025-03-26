"""Redis configuration module for OMEGA BTC AI system."""
import os

# Redis Labs configuration
REDIS_CONFIG = {
    'host': os.getenv('REDIS_HOST', 'redis-19332.fcrce173.eu-west-1-1.ec2.redns.redis-cloud.com'),
    'port': int(os.getenv('REDIS_PORT', '19332')),
    'username': os.getenv('REDIS_USERNAME', 'default'),
    'password': os.getenv('REDIS_PASSWORD', 'Gbzlwv6BgNK1oT2B9AvH8MuwAZ0JmQkj'),
    'decode_responses': True
}

def get_redis_config():
    """Get Redis configuration with environment variable overrides."""
    return {
        'host': os.getenv('REDIS_HOST', REDIS_CONFIG['host']),
        'port': int(os.getenv('REDIS_PORT', REDIS_CONFIG['port'])),
        'username': os.getenv('REDIS_USERNAME', REDIS_CONFIG['username']),
        'password': os.getenv('REDIS_PASSWORD', REDIS_CONFIG['password']),
        'decode_responses': True
    } 