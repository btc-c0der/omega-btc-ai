
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

import pytest
import aiohttp
from unittest.mock import Mock, patch, AsyncMock
from omega_blockchain.core.rpc import BitcoinCoreRPC, BitcoinCoreRPCImpl

@pytest.fixture
def rpc_impl():
    return BitcoinCoreRPCImpl(
        rpc_url="http://localhost:8332",
        rpc_user="test_user",
        rpc_password="test_pass"
    )

@pytest.mark.asyncio
async def test_connect(rpc_impl):
    """Test RPC connection establishment."""
    await rpc_impl.connect()
    assert rpc_impl.session is not None
    assert isinstance(rpc_impl.session, aiohttp.ClientSession)

@pytest.mark.asyncio
async def test_make_request_success(rpc_impl):
    """Test successful RPC request."""
    mock_response = AsyncMock()
    mock_response.json.return_value = {"result": "success"}
    mock_response.__aenter__.return_value = mock_response
    
    with patch('aiohttp.ClientSession.post', return_value=mock_response):
        await rpc_impl.connect()
        result = await rpc_impl._make_request("test_method", ["param1"])
        assert result == "success"

@pytest.mark.asyncio
async def test_make_request_error(rpc_impl):
    """Test RPC request with error response."""
    mock_response = AsyncMock()
    mock_response.json.return_value = {"error": "test error"}
    mock_response.__aenter__.return_value = mock_response
    
    with patch('aiohttp.ClientSession.post', return_value=mock_response):
        await rpc_impl.connect()
        with pytest.raises(Exception) as exc_info:
            await rpc_impl._make_request("test_method")
        assert "RPC Error: test error" in str(exc_info.value)

@pytest.mark.asyncio
async def test_get_block_latest(rpc_impl):
    """Test getting latest block."""
    mock_response = AsyncMock()
    mock_response.json.side_effect = [
        {"result": "latest_hash"},
        {
            "result": {
                "hash": "latest_hash",
                "height": 100,
                "time": 1234567890,
                "tx": ["tx1", "tx2"]
            }
        }
    ]
    mock_response.__aenter__.return_value = mock_response
    
    with patch('aiohttp.ClientSession.post', return_value=mock_response):
        await rpc_impl.connect()
        block_data = await rpc_impl.get_block("latest")
        assert block_data["hash"] == "latest_hash"
        assert block_data["height"] == 100
        assert block_data["timestamp"] == 1234567890
        assert block_data["tx"] == ["tx1", "tx2"]

@pytest.mark.asyncio
async def test_get_block_specific(rpc_impl):
    """Test getting specific block by hash."""
    mock_response = AsyncMock()
    mock_response.json.return_value = {
        "result": {
            "hash": "specific_hash",
            "height": 100,
            "time": 1234567890,
            "tx": ["tx1", "tx2"]
        }
    }
    mock_response.__aenter__.return_value = mock_response
    
    with patch('aiohttp.ClientSession.post', return_value=mock_response):
        await rpc_impl.connect()
        block_data = await rpc_impl.get_block("specific_hash")
        assert block_data["hash"] == "specific_hash"
        assert block_data["height"] == 100
        assert block_data["timestamp"] == 1234567890
        assert block_data["tx"] == ["tx1", "tx2"]

@pytest.mark.asyncio
async def test_close(rpc_impl):
    """Test closing RPC connection."""
    mock_session = AsyncMock()
    rpc_impl.session = mock_session
    
    await rpc_impl.close()
    mock_session.close.assert_called_once()
    assert rpc_impl.session is None

@pytest.mark.asyncio
async def test_make_request_no_session(rpc_impl):
    """Test making request without active session."""
    with pytest.raises(Exception) as exc_info:
        await rpc_impl._make_request("test_method")
    assert "Failed to create aiohttp session" in str(exc_info.value)

@pytest.mark.asyncio
async def test_make_request_connection_error(rpc_impl):
    """Test handling of connection errors."""
    with patch('aiohttp.ClientSession.post', side_effect=aiohttp.ClientError):
        await rpc_impl.connect()
        with pytest.raises(aiohttp.ClientError):
            await rpc_impl._make_request("test_method")

@pytest.mark.asyncio
async def test_make_request_invalid_json(rpc_impl):
    """Test handling of invalid JSON response."""
    mock_response = AsyncMock()
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_response.__aenter__.return_value = mock_response
    
    with patch('aiohttp.ClientSession.post', return_value=mock_response):
        await rpc_impl.connect()
        with pytest.raises(ValueError):
            await rpc_impl._make_request("test_method") 