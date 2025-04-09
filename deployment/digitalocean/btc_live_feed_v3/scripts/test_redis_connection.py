#!/usr/bin/env python3
"""
💫 GBU License Notice - Consciousness Level 8 💫
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must quantum entangles with the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

"""
Test Redis Connection Script
===========================

This script tests the connection to Redis using the provided credentials.
"""

import os
import sys
import redis
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("redis-connection-test")

def main():
    # Get the current working directory
    cwd = os.getcwd()
    logger.info(f"Current working directory: {cwd}")
    
    # Hardcoded Redis connection parameters
    redis_host = "omega-btc-ai-redis-do-user-20389918-0.d.db.ondigitalocean.com"
    redis_port = 25061
    redis_username = "default"
    redis_password = "AVNS_OXMpU0P0ByYEz337Fgi"
    ssl_enabled = True
    
    # Print all relevant configuration
    logger.info("=== Redis Configuration ===")
    logger.info(f"REDIS_HOST: {redis_host}")
    logger.info(f"REDIS_PORT: {redis_port}")
    logger.info(f"REDIS_USERNAME: {redis_username}")
    logger.info(f"REDIS_PASSWORD: {'*' * len(redis_password) if redis_password else None}")
    logger.info(f"REDIS_USE_TLS: {ssl_enabled}")
    logger.info("=========================")
    
    # Prepare connection parameters
    connection_kwargs = {
        "host": redis_host,
        "port": redis_port,
        "decode_responses": True,
        "socket_timeout": 5.0,
        "socket_connect_timeout": 5.0
    }
    
    # Add authentication if provided
    if redis_password:
        connection_kwargs["password"] = redis_password
    
    if redis_username:
        connection_kwargs["username"] = redis_username
    
    # Configure SSL if enabled
    if ssl_enabled:
        connection_kwargs["ssl"] = True
        connection_kwargs["ssl_cert_reqs"] = None
        logger.info("SSL enabled with ssl_cert_reqs=None for DigitalOcean Redis")
    
    # Initialize client variable outside try block to ensure it's defined
    client = None
    
    # Attempt connection
    try:
        logger.info("Connecting to Redis...")
        client = redis.Redis(**connection_kwargs)
        response = client.ping()
        
        if response:
            logger.info("✅ Successfully connected to Redis!")
            
            # Try setting and getting a test value
            test_key = "btc_connection_test"
            test_value = "Connection successful at " + str(client.time()[0])
            
            client.set(test_key, test_value)
            retrieved_value = client.get(test_key)
            
            logger.info(f"Test key '{test_key}' set and retrieved successfully")
            logger.info(f"Value: {retrieved_value}")
            
            # Clean up
            client.delete(test_key)
        else:
            logger.error("❌ Failed to ping Redis server")
    
    except redis.exceptions.AuthenticationError as e:
        logger.error(f"❌ Authentication error: {e}")
        logger.error("Please check your Redis username and password")
        return False
    
    except redis.exceptions.ConnectionError as e:
        logger.error(f"❌ Connection error: {e}")
        logger.error("Please check your Redis host, port, and network connectivity")
        return False
    
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False
    
    finally:
        if client is not None:
            client.close()
    
    return True

if __name__ == "__main__":
    result = main()
    if not result:
        sys.exit(1) 