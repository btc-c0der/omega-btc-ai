from typing import Optional
from ..models.block import BlockData
from .rpc import BitcoinCoreRPC, BitcoinCoreRPCImpl

class OmegaBlockchainStream:
    """Divine connection to the Bitcoin blockchain."""
    
    def __init__(self, node_connection: Optional[BitcoinCoreRPC] = None):
        self.node_connection = node_connection
        self.block_stream = None
        self.transaction_monitor = None
        
    async def connect_to_chain(self):
        """Establish sacred connection to the blockchain."""
        if not self.node_connection:
            self.node_connection = BitcoinCoreRPCImpl()
        try:
            await self.node_connection.connect()
        except Exception as e:
            raise Exception(str(e))
        
    async def stream_blocks(self) -> BlockData:
        """Stream divine block data in real-time."""
        if not self.node_connection:
            await self.connect_to_chain()
            
        if not self.node_connection:
            raise Exception("Not connected to Bitcoin Core")
            
        try:
            block_data = await self.node_connection.get_block("latest")
            return BlockData(
                hash=block_data['hash'],
                height=block_data['height'],
                timestamp=block_data['timestamp'],
                transactions=block_data['tx']
            )
        except Exception as e:
            raise Exception(str(e)) 