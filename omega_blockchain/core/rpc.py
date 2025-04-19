
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

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
import aiohttp

class BitcoinCoreRPC(ABC):
    """Abstract base class for Bitcoin Core RPC interface."""
    
    @abstractmethod
    async def connect(self):
        """Establish connection to Bitcoin Core node."""
        pass
    
    @abstractmethod
    async def get_block(self, block_hash: str) -> Dict[str, Any]:
        """Retrieve block data by hash."""
        pass
        
    @abstractmethod
    async def _make_request(self, method: str, params: Optional[List[Any]] = None) -> Dict[str, Any]:
        """Make RPC request to Bitcoin Core."""
        pass

class BitcoinCoreRPCImpl(BitcoinCoreRPC):
    """Concrete implementation of Bitcoin Core RPC interface."""
    
    def __init__(self, rpc_url: str = "http://localhost:8332", rpc_user: str = "", rpc_password: str = ""):
        self.rpc_url = rpc_url
        self.rpc_user = rpc_user
        self.rpc_password = rpc_password
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def connect(self):
        """Establish connection to Bitcoin Core node."""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def _make_request(self, method: str, params: Optional[List[Any]] = None) -> Dict[str, Any]:
        """Make RPC request to Bitcoin Core."""
        try:
            if not self.session:
                await self.connect()
                
            if not self.session:
                raise Exception("Failed to create aiohttp session")
                
            auth = aiohttp.BasicAuth(self.rpc_user, self.rpc_password)
            headers = {'content-type': 'application/json'}
            
            payload = {
                'method': method,
                'params': params or [],
                'jsonrpc': '2.0',
                'id': 1
            }
            
            async with self.session.post(self.rpc_url, json=payload, auth=auth, headers=headers) as response:
                result = await response.json()
                if 'error' in result:
                    raise Exception(f"RPC Error: {result['error']}")
                return result['result']
        except aiohttp.ClientError as e:
            raise Exception(f"Failed to create aiohttp session: {str(e)}")
            
    async def get_block(self, block_hash: str) -> Dict[str, Any]:
        """Retrieve block data by hash."""
        if block_hash == "latest":
            # Get the latest block hash first
            latest_hash = await self._make_request('getbestblockhash')
            block_hash = str(latest_hash)
            
        block_data = await self._make_request('getblock', [block_hash, True])
        return {
            'hash': str(block_data['hash']),
            'height': int(block_data['height']),
            'timestamp': int(block_data['time']),
            'tx': list(block_data['tx'])
        }
        
    async def close(self):
        """Close the RPC connection."""
        if self.session:
            await self.session.close()
            self.session = None 