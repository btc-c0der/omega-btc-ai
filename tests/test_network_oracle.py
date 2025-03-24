import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
from omega_blockchain.oracles.network import NetworkHealthOracle, RateLimitExceeded
from omega_blockchain.models.network import NetworkMetrics

@pytest.fixture
def mock_node_connection():
    mock = AsyncMock()
    mock._make_request = AsyncMock()
    return mock

@pytest.fixture
def network_oracle(mock_node_connection):
    oracle = NetworkHealthOracle(node_connection=mock_node_connection)
    return oracle

@pytest.mark.asyncio
async def test_check_network_health_success(network_oracle, mock_node_connection):
    """Test successful network health check."""
    # Mock responses
    mock_node_connection._make_request.side_effect = [
        {"difficulty": 1000, "blocks": 100, "headers": 100, "connections": 10},
        1000000000,  # hash_rate
        {"size": 1000, "bytes": 1000000},  # mempool_info
        {"feerate": 0.00001}  # fee_info
    ]
    
    metrics = await network_oracle.check_network_health()
    
    assert isinstance(metrics, NetworkMetrics)
    assert metrics.hash_rate == 1000000000
    assert metrics.difficulty == 1000
    assert metrics.fee_rate == 1  # 0.00001 BTC/kB converted to sat/vB
    assert metrics.mempool_size == 1000
    assert metrics.blocks == 100
    assert metrics.headers == 100
    assert metrics.connections == 10
    assert metrics.mempool_bytes == 1000000
    assert metrics.timestamp > 0

@pytest.mark.asyncio
async def test_check_network_health_rate_limit(network_oracle):
    """Test rate limiting behavior."""
    # Make requests up to rate limit
    for _ in range(network_oracle.rate_limit):
        await network_oracle._check_rate_limit()
    
    # Next request should raise RateLimitExceeded
    with pytest.raises(RateLimitExceeded):
        await network_oracle._check_rate_limit()

@pytest.mark.asyncio
async def test_check_network_health_concurrent_requests(network_oracle):
    """Test concurrent request limiting."""
    # Make requests up to max concurrent limit
    for _ in range(network_oracle.max_concurrent_requests):
        await network_oracle._check_concurrent_requests()
    
    # Next request should raise exception
    with pytest.raises(Exception) as exc_info:
        await network_oracle._check_concurrent_requests()
    assert "Too many concurrent requests" in str(exc_info.value)

@pytest.mark.asyncio
async def test_predict_congestion(network_oracle, mock_node_connection):
    """Test congestion prediction."""
    # Mock responses
    mock_node_connection._make_request.side_effect = [
        {"size": 2000, "bytes": 2000000},  # mempool_info
        {"feerate": 0.00002}  # fee_info
    ]
    
    # Add some historical metrics
    network_oracle.historical_metrics = [
        NetworkMetrics(
            hash_rate=1000000000,
            difficulty=1000,
            fee_rate=1,
            mempool_size=1000,
            blocks=100,
            headers=100,
            connections=10,
            mempool_bytes=1000000,
            timestamp=int((datetime.now() - timedelta(hours=1)).timestamp())
        ),
        NetworkMetrics(
            hash_rate=1000000000,
            difficulty=1000,
            fee_rate=1,
            mempool_size=2000,
            blocks=101,
            headers=101,
            connections=10,
            mempool_bytes=2000000,
            timestamp=int(datetime.now().timestamp())
        )
    ]
    
    prediction = await network_oracle.predict_congestion()
    
    assert isinstance(prediction, dict)
    assert "congestion_level" in prediction
    assert "confidence" in prediction
    assert "mempool_bytes" in prediction
    assert "mempool_size" in prediction
    assert "next_block_eta" in prediction
    assert "estimated_fee_rate" in prediction
    assert "trend" in prediction

@pytest.mark.asyncio
async def test_analyze_mempool(network_oracle, mock_node_connection):
    """Test mempool analysis."""
    # Mock response
    mock_node_connection._make_request.return_value = {
        "size": 2000,
        "bytes": 2000000
    }
    
    analysis = await network_oracle.analyze_mempool()
    
    assert isinstance(analysis, dict)
    assert "mempool_size" in analysis
    assert "mempool_bytes" in analysis
    assert "utilization" in analysis
    assert "fee_histogram" in analysis
    assert "size_histogram" in analysis
    assert "transaction_types" in analysis

@pytest.mark.asyncio
async def test_check_synchronization(network_oracle, mock_node_connection):
    """Test synchronization status check."""
    # Mock response
    mock_node_connection._make_request.return_value = {
        "headers": 100,
        "blocks": 95,
        "initialblockdownload": False,
        "verificationprogress": 0.95
    }
    
    status = await network_oracle.check_synchronization()
    
    assert isinstance(status, dict)
    assert "is_synced" in status
    assert "blocks_behind" in status
    assert "initial_block_download" in status
    assert "estimated_time_remaining" in status
    assert "hours_remaining" in status
    assert "progress" in status
    assert "verification_progress" in status

@pytest.mark.asyncio
async def test_make_request_with_retry(network_oracle, mock_node_connection):
    """Test request retry logic."""
    # Mock connection error followed by success
    mock_node_connection._make_request.side_effect = [
        Exception("Connection timeout"),
        {"result": "success"}
    ]
    
    result = await network_oracle._make_request_with_retry("test_method")
    assert result == {"result": "success"}

@pytest.mark.asyncio
async def test_make_request_with_retry_max_attempts(network_oracle, mock_node_connection):
    """Test request retry logic with max attempts reached."""
    # Mock continuous connection errors
    mock_node_connection._make_request.side_effect = [
        Exception("Connection timeout") for _ in range(network_oracle.retry_attempts)
    ]
    
    with pytest.raises(Exception) as exc_info:
        await network_oracle._make_request_with_retry("test_method")
    assert "Failed to retrieve network metrics" in str(exc_info.value)
    assert "Connection failed after" in str(exc_info.value) 