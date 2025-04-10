
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
Pytest configuration for NFT component tests
"""

import os
import sys
import pytest

# Add parent directory to path to make imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# Configure pytest
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "asyncio: mark test as requiring asyncio"
    )
    
    # Set NFT API key for testing if not set
    if not os.environ.get("NFT_API_KEY"):
        os.environ["NFT_API_KEY"] = "test_api_key"
        
    # Set NFT contract address for testing if not set
    if not os.environ.get("NFT_CONTRACT_ADDRESS"):
        os.environ["NFT_CONTRACT_ADDRESS"] = "0xTESTCONTRACT" 