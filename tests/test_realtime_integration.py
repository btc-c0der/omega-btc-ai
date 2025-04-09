import pytest
import asyncio
import json
import redis
import websockets
from typing import AsyncGenerator, Dict, Any
from omega_ai.blockchain.realtime import RedisBlockStore, WebSocketBlockStream, RealtimeBlockchainMonitor

# Test data
TEST_BLOCK = {
    "hash": "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f",
    "height": 0,
    "timestamp": 1231006505,
    "transactions": [
        {
            "txid": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
            "inputs": [],
            "outputs": [
                {
                    "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
                    "value": 5000000000
                }
            ]
        }
    ]
}

@pytest.fixture
def redis_client():
    client = redis.Redis(host='localhost', port=6379, db=0)
    yield client
    client.close()

@pytest.fixture
async def websocket_server() -> AsyncGenerator[Any, None]:
    async def handler(websocket):
        try:
            while True:
                message = await websocket.recv()
                await websocket.send(message)
        except websockets.exceptions.ConnectionClosed:
            pass

    server = await websockets.serve(handler, "localhost", 8766)
    yield server
    server.close()
    await server.wait_closed()

@pytest.mark.asyncio
async def test_redis_block_store(redis_client):
    store = RedisBlockStore(redis_client)
    
    # Test storing a block
    store.store_block(TEST_BLOCK)
    
    # Test retrieving a block
    stored_block = store.get_block(TEST_BLOCK["hash"])
    assert stored_block == TEST_BLOCK
    
    # Test deleting a block
    store.delete_block(TEST_BLOCK["hash"])
    assert store.get_block(TEST_BLOCK["hash"]) is None

@pytest.mark.asyncio
async def test_websocket_block_stream(websocket_server):
    stream = WebSocketBlockStream("ws://localhost:8766")
    
    # Test connecting
    await stream.connect()
    assert stream.is_connected()
    
    # Test sending a block
    await stream.send_block(TEST_BLOCK)
    
    # Test disconnecting
    await stream.disconnect()
    assert not stream.is_connected()

@pytest.mark.asyncio
async def test_realtime_blockchain_monitor(redis_client, websocket_server):
    monitor = RealtimeBlockchainMonitor(redis_client, "ws://localhost:8766")
    
    # Test starting the monitor
    await monitor.start()
    assert monitor.is_running()
    
    # Test processing a block
    await monitor.process_block(TEST_BLOCK)
    
    # Test stopping the monitor
    await monitor.stop()
    assert not monitor.is_running()

@pytest.mark.asyncio
async def test_block_validation_integration(redis_client, websocket_server):
    monitor = RealtimeBlockchainMonitor(redis_client, "ws://localhost:8766")
    await monitor.start()
    
    try:
        # Test invalid block
        invalid_block = {"hash": "invalid"}
        await monitor.process_block(invalid_block)
        
        # Verify block was not stored
        store = RedisBlockStore(redis_client)
        assert store.get_block(invalid_block["hash"]) is None
    finally:
        await monitor.stop()

@pytest.mark.asyncio
async def test_error_handling(redis_client, websocket_server):
    # Test Redis connection error
    invalid_redis = redis.Redis(host='invalid', port=6379)
    store = RedisBlockStore(invalid_redis)
    
    # Test WebSocket connection error
    stream = WebSocketBlockStream("ws://invalid:8766")
    with pytest.raises(Exception):
        await stream.connect()

@pytest.mark.asyncio
async def test_concurrent_block_processing(redis_client, websocket_server):
    monitor = RealtimeBlockchainMonitor(redis_client, "ws://localhost:8766")
    await monitor.start()
    
    # Create multiple blocks
    blocks = [
        {**TEST_BLOCK, "hash": f"block_{i}", "height": i}
        for i in range(5)
    ]
    
    # Process blocks concurrently
    tasks = [monitor.process_block(block) for block in blocks]
    await asyncio.gather(*tasks)
    
    # Verify all blocks were stored
    store = RedisBlockStore(redis_client)
    for block in blocks:
        assert store.get_block(block["hash"]) == block
    
    await monitor.stop()

@pytest.mark.asyncio
async def test_block_chain_continuity(redis_client, websocket_server):
    monitor = RealtimeBlockchainMonitor(redis_client, "ws://localhost:8766")
    await monitor.start()
    
    # Create a chain of blocks
    blocks = []
    prev_hash = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
    
    for i in range(5):
        block = {
            **TEST_BLOCK,
            "hash": f"block_{i}",
            "height": i,
            "previous_hash": prev_hash
        }
        blocks.append(block)
        prev_hash = block["hash"]
        await monitor.process_block(block)
    
    # Verify chain continuity
    store = RedisBlockStore(redis_client)
    for i in range(len(blocks) - 1):
        current_block = store.get_block(blocks[i]["hash"])
        next_block = store.get_block(blocks[i + 1]["hash"])
        assert current_block["hash"] == next_block["previous_hash"]
    
    await monitor.stop() 