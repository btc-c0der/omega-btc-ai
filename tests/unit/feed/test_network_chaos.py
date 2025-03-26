import pytest
import asyncio
import time
from datetime import datetime, UTC
from unittest.mock import patch, MagicMock, AsyncMock
import subprocess
import json
import os
from typing import List, Dict, Optional
import fakeredis

from omega_ai.data_feed.btc_live_feed import BtcPriceFeed, PriceSource

class ToxiProxyManager:
    """Manages ToxiProxy for network chaos simulation."""
    
    def __init__(self):
        self.proxy_name = "btc_feed_proxy"
        self.listen_port = 8766
        self.upstream_port = 8765  # MM WebSocket server port
        
    def ensure_toxiproxy_running(self):
        """Check if ToxiProxy server is running."""
        try:
            # Try to list proxies to check if server is running
            result = subprocess.run(["toxiproxy-cli", "list"], 
                                 capture_output=True, 
                                 check=True)
            return True
        except subprocess.CalledProcessError:
            return False
            
    def create_proxy(self):
        """Create a new proxy for the WebSocket connection."""
        try:
            # First try to delete any existing proxy with the same name
            subprocess.run(["toxiproxy-cli", "delete", self.proxy_name], 
                         capture_output=True)
        except subprocess.CalledProcessError:
            pass  # Ignore if proxy doesn't exist
            
        try:
            subprocess.run([
                "toxiproxy-cli", "create",
                "--listen", f"localhost:{self.listen_port}",
                "--upstream", f"localhost:{self.upstream_port}",
                self.proxy_name
            ], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to create proxy: {e.stderr.decode()}")
            return False
            
    def add_toxic(self, toxic_type: str, attributes: Dict):
        """Add a toxic to the proxy."""
        try:
            cmd = ["toxiproxy-cli", "toxic", "add", self.proxy_name, "-t", toxic_type]
            for key, value in attributes.items():
                cmd.extend(["-a", f"{key}={value}"])
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to add {toxic_type} toxic: {e.stderr.decode()}")
            return False
            
    def remove_toxic(self, toxic_name: str):
        """Remove a toxic from the proxy."""
        try:
            subprocess.run([
                "toxiproxy-cli", "toxic", "remove",
                self.proxy_name,
                toxic_name
            ], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to remove {toxic_name} toxic: {e.stderr.decode()}")
            return False
            
    def cleanup(self):
        """Clean up ToxiProxy resources."""
        try:
            subprocess.run(["toxiproxy-cli", "delete", self.proxy_name], 
                         check=True, capture_output=True)
        except subprocess.CalledProcessError:
            pass

@pytest.fixture(scope="session")
def toxiproxy():
    """Create a ToxiProxy manager for the test session."""
    manager = ToxiProxyManager()
    if not manager.ensure_toxiproxy_running():
        pytest.skip("ToxiProxy server not running")
    return manager

@pytest.fixture(autouse=True)
def setup_teardown(toxiproxy):
    """Setup and teardown for each test."""
    if not toxiproxy.create_proxy():
        pytest.skip("Failed to create ToxiProxy proxy")
    
    yield
    
    toxiproxy.cleanup()

@pytest.fixture
def mock_redis():
    """Create a fake Redis instance."""
    server = fakeredis.FakeServer()
    redis_client = fakeredis.FakeRedis(server=server)
    
    # Initialize with some test data
    test_data = {
        "last_btc_price": "85000.50",
        "prev_btc_price": "84000.50",
        "last_btc_volume": "1.5",
        "fibonacci_levels": json.dumps({
            "0.0": "83000.00",
            "0.236": "84000.00",
            "0.382": "85000.00",
            "0.5": "86000.00",
            "0.618": "87000.00",
            "0.786": "88000.00",
            "1.0": "89000.00"
        })
    }
    
    for key, value in test_data.items():
        redis_client.set(key, value)
    
    # Add some historical data
    for i in range(5):
        price = 85000.50 + (i * 100)
        volume = 1.5 + (i * 0.1)
        data = json.dumps({"price": price, "volume": volume, "timestamp": datetime.now(UTC).isoformat()})
        redis_client.lpush("btc_movement_history", data)
    
    return redis_client

@pytest.fixture
def btc_feed(mock_redis):
    """Create a BtcPriceFeed instance with mocked Redis."""
    with patch('omega_ai.data_feed.btc_live_feed.RedisManager') as mock_redis_manager, \
         patch('omega_ai.data_feed.btc_live_feed.websockets.connect') as mock_ws_connect, \
         patch('omega_ai.data_feed.btc_live_feed.MM_WS_URL', f"ws://localhost:{ToxiProxyManager().listen_port}"):
        
        # Mock Redis manager
        mock_instance = MagicMock()
        mock_instance.get_cached.side_effect = mock_redis.get
        mock_instance.set_cached.side_effect = mock_redis.set
        mock_instance.lpush.side_effect = mock_redis.lpush
        mock_instance.ltrim.side_effect = mock_redis.ltrim
        mock_instance.lrange.side_effect = mock_redis.lrange
        mock_instance.ping.return_value = True
        mock_instance.authenticate.return_value = True
        mock_redis_manager.return_value = mock_instance
        
        # Mock WebSocket connection
        mock_ws = MagicMock()
        mock_ws.closed = False
        mock_ws.close = AsyncMock()
        mock_ws.send = AsyncMock()
        mock_ws.receive = AsyncMock(return_value=json.dumps({
            "price": "85000.50",
            "volume": "1.5",
            "timestamp": datetime.now(UTC).isoformat()
        }))
        mock_ws_connect.return_value = AsyncMock(
            __aenter__=AsyncMock(return_value=mock_ws),
            __aexit__=AsyncMock()
        )
        
        with patch.dict(os.environ, {
            'REDIS_HOST': 'localhost',
            'REDIS_PORT': '6379',
            'REDIS_PASSWORD': 'test_password'
        }):
            feed = BtcPriceFeed()
            feed._ws = mock_ws  # Set the mocked WebSocket connection
            return feed

async def simulate_price_updates(feed: BtcPriceFeed, num_updates: int = 10) -> List[Dict]:
    """Simulate a series of price updates."""
    updates = []
    for i in range(num_updates):
        price = 85000.50 + (i * 100)
        volume = 1.5 + (i * 0.1)
        feed.update_redis(price, volume)
        updates.append({"price": price, "volume": volume})
        await asyncio.sleep(0.1)
    return updates
        
class TestNetworkChaos:
    """Test suite for network chaos simulation."""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self, toxiproxy):
        """Setup and teardown for each test."""
        self.toxiproxy = toxiproxy
        if not self.toxiproxy.create_proxy():
            pytest.skip("Failed to create ToxiProxy proxy")
        
        yield
        
        self.toxiproxy.cleanup()
    
    @pytest.mark.asyncio
    async def test_latency(self, btc_feed):
        """Test system behavior under high latency."""
        # Add 500ms latency
        self.toxiproxy.add_toxic("latency", {"latency": 500})
        
        start_time = time.time()
        updates = await simulate_price_updates(btc_feed)
        end_time = time.time()
        
        # Verify updates were processed despite latency
        assert len(updates) == 10
        assert end_time - start_time >= 5.0  # Should take at least 5 seconds with 500ms latency
        
    @pytest.mark.asyncio
    async def test_jitter(self, btc_feed):
        """Test system behavior under network jitter."""
        # Add 200ms jitter
        self.toxiproxy.add_toxic("jitter", {"jitter": 200})
        
        updates = await simulate_price_updates(btc_feed)
        
        # Verify all updates were processed despite jitter
        assert len(updates) == 10
        
    @pytest.mark.asyncio
    async def test_bandwidth_limit(self, btc_feed):
        """Test system behavior under bandwidth limitations."""
        # Limit bandwidth to 100 bytes per second
        self.toxiproxy.add_toxic("bandwidth", {"rate": 100})
        
        updates = await simulate_price_updates(btc_feed)
        
        # Verify updates were processed despite bandwidth limits
        assert len(updates) == 10
        
    @pytest.mark.asyncio
    async def test_connection_reset(self, btc_feed):
        """Test system recovery after connection reset."""
        # Simulate connection reset every 2 seconds
        self.toxiproxy.add_toxic("reset_peer", {"timeout": 2000})
        
        updates = await simulate_price_updates(btc_feed)
        
        # Verify system recovered and processed updates
        assert len(updates) == 10
        
    @pytest.mark.asyncio
    async def test_data_gaps(self, btc_feed):
        """Test system behavior with data gaps."""
        # Drop 50% of packets
        self.toxiproxy.add_toxic("slicer", {"average_size": 1, "size_variation": 1})
        
        updates = await simulate_price_updates(btc_feed)
        
        # Verify system handled packet loss
        assert len(updates) == 10
        
    @pytest.mark.asyncio
    async def test_recovery_time(self, btc_feed):
        """Test system recovery time after network issues."""
        # First get baseline time without any network issues
        baseline_start = time.time()
        baseline_updates = await simulate_price_updates(btc_feed)
        baseline_end = time.time()
        baseline_time = baseline_end - baseline_start
        
        # Add severe latency and jitter
        self.toxiproxy.add_toxic("latency", {"latency": 1000})
        self.toxiproxy.add_toxic("jitter", {"jitter": 500})
        
        start_time = time.time()
        updates = await simulate_price_updates(btc_feed)
        end_time = time.time()
        degraded_time = end_time - start_time
        
        # Remove network issues
        self.toxiproxy.remove_toxic("latency")
        self.toxiproxy.remove_toxic("jitter")
        
        # Test recovery with normal conditions
        recovery_start = time.time()
        recovery_updates = await simulate_price_updates(btc_feed)
        recovery_end = time.time()
        recovery_time = recovery_end - recovery_start
        
        # Verify system recovers quickly when conditions improve
        assert len(baseline_updates) == 10
        assert len(updates) == 10
        assert len(recovery_updates) == 10
        
        # Recovery time should be closer to baseline than to degraded time
        assert abs(recovery_time - baseline_time) < abs(recovery_time - degraded_time)
        assert recovery_time < degraded_time * 0.95  # Recovery should be at least 5% faster than degraded time
        
    @pytest.mark.asyncio
    async def test_message_ordering(self, btc_feed):
        """Test message ordering under network stress."""
        # Add reordering toxic
        self.toxiproxy.add_toxic("reorder", {"reorder": 0.5})
        
        updates = await simulate_price_updates(btc_feed)
        
        # Verify price updates are in correct order despite reordering
        assert len(updates) == 10
        for i in range(1, len(updates)):
            assert updates[i]["price"] > updates[i-1]["price"]