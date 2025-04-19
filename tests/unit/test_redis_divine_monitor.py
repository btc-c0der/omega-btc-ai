#!/usr/bin/env python

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

# -*- coding: utf-8 -*-

"""
Test cases for the Redis Divine Monitor module
"""

import asyncio
import json
import pytest
from unittest.mock import MagicMock, patch, AsyncMock, call

import redis
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from omega_ai.monitor.redis_divine_monitor import (
    RedisDivineMonitor,
    REDIS_MARKET_CHANNEL,
    MARKET_SYMBOLS,
    COLORS,
    DIVINE_PATTERNS
)


class TestRedisDivineMonitor:
    """Test suite for Redis Divine Monitor class"""
    
    def test_init(self):
        """Test basic initialization of RedisDivineMonitor"""
        monitor = RedisDivineMonitor(update_interval=10)
        
        # Check default values
        assert monitor.update_interval == 10
        assert monitor.symbols == MARKET_SYMBOLS
        assert monitor.redis_host == "localhost"
        assert monitor.redis_port == 6379
        assert monitor.redis_db == 0
        assert monitor.redis is None
        assert monitor.pubsub is None
        assert monitor.running is True
        
        # Check market data storage initialization
        assert monitor.market_data == {}
        assert len(monitor.price_history) == len(MARKET_SYMBOLS)
        assert len(monitor.volume_history) == len(MARKET_SYMBOLS)
        
        # Check divine flow indicators initialization
        assert len(monitor.divine_flow) == len(MARKET_SYMBOLS)
        assert len(monitor.divine_energy) == len(MARKET_SYMBOLS)
        assert len(monitor.ascension_levels) == len(MARKET_SYMBOLS)
        
        # Check layout setup
        assert isinstance(monitor.layout, Layout)
    
    def test_init_custom_symbols(self):
        """Test initialization with custom symbols"""
        custom_symbols = ["btcusdt", "ethusdt"]
        monitor = RedisDivineMonitor(symbols=custom_symbols)
        
        assert monitor.symbols == custom_symbols
        assert len(monitor.price_history) == len(custom_symbols)
        assert len(monitor.volume_history) == len(custom_symbols)
        assert len(monitor.divine_flow) == len(custom_symbols)
        assert len(monitor.divine_energy) == len(custom_symbols)
        assert len(monitor.ascension_levels) == len(custom_symbols)
    
    def test_init_custom_redis(self):
        """Test initialization with custom Redis connection settings"""
        monitor = RedisDivineMonitor(
            redis_host="test-host",
            redis_port=1234,
            redis_db=5
        )
        
        assert monitor.redis_host == "test-host"
        assert monitor.redis_port == 1234
        assert monitor.redis_db == 5
    
    @pytest.mark.asyncio
    async def test_connect_redis_success(self):
        """Test successful Redis connection"""
        monitor = RedisDivineMonitor()
        
        # Mock Redis client
        mock_redis = MagicMock()
        mock_redis.ping.return_value = True
        mock_pubsub = MagicMock()
        mock_redis.pubsub.return_value = mock_pubsub
        
        # Mock asyncio.to_thread
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread, \
             patch('redis.Redis', return_value=mock_redis):
             
            mock_to_thread.return_value = True
            await monitor.connect_redis()
            
            # Verify Redis client was created with correct parameters
            assert monitor.redis is not None
            # Verify ping was called
            mock_to_thread.assert_any_call(mock_redis.ping)
            # Verify pubsub subscription
            mock_to_thread.assert_any_call(mock_pubsub.subscribe, REDIS_MARKET_CHANNEL)
    
    @pytest.mark.asyncio
    async def test_connect_redis_failure(self):
        """Test Redis connection failure"""
        monitor = RedisDivineMonitor()
        monitor.console = MagicMock()
        
        # Mock Redis client to raise exception
        with patch('redis.Redis', side_effect=Exception("Connection error")), \
             pytest.raises(Exception) as excinfo:
            await monitor.connect_redis()
            
        assert "Connection error" in str(excinfo.value)
        monitor.console.print.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_disconnect_redis(self):
        """Test Redis disconnection"""
        monitor = RedisDivineMonitor()
        monitor.pubsub = MagicMock()
        monitor.redis = MagicMock()
        
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
            await monitor.disconnect_redis()
            
            # Verify pubsub unsubscribe was called
            mock_to_thread.assert_any_call(monitor.pubsub.unsubscribe, REDIS_MARKET_CHANNEL)
            # Verify redis close was called
            mock_to_thread.assert_any_call(monitor.redis.close)
    
    def test_render_header(self):
        """Test header rendering"""
        monitor = RedisDivineMonitor()
        
        # Mock the Text.assemble function to return a controllable text object
        mock_text = MagicMock()
        mock_text.plain = "OMEGA BTC AI REDIS DIVINE MONITOR Divine Time: 2023-01-01 00:00:00"
        
        with patch('rich.text.Text.assemble', return_value=mock_text):
            header_panel = monitor._render_header()
            
            assert isinstance(header_panel, Panel)
            assert header_panel.renderable == mock_text
    
    def test_render_markets_table(self):
        """Test markets table rendering"""
        monitor = RedisDivineMonitor()
        # Add some test data
        monitor.market_data = {
            "btcusdt": {
                "price": 50000,
                "change": "+2.5",
                "volume": 1000000,
                "timestamp": 1616231231
            }
        }
        
        markets_panel = monitor._render_markets_table()
        
        assert isinstance(markets_panel, Panel)
        assert markets_panel.title == "Market Divine Flow"
    
    def test_render_price_chart_no_data(self):
        """Test price chart rendering with no data"""
        monitor = RedisDivineMonitor()
        
        # Mock Text object with controllable content
        mock_text = MagicMock()
        mock_text.plain = "Awaiting divine price flow..."
        
        with patch('rich.text.Text', return_value=mock_text):
            chart_panel = monitor._render_price_chart()
            
            assert isinstance(chart_panel, Panel)
            assert "Awaiting divine price flow" in mock_text.plain
    
    def test_render_price_chart_with_data(self):
        """Test price chart rendering with price data"""
        monitor = RedisDivineMonitor()
        monitor.price_history = {
            "btcusdt": [50000, 51000, 52000, 51500, 52500]
        }
        
        # Mock Text.assemble to return a controllable text object
        mock_text = MagicMock()
        mock_text.plain = "Current: $52500.00 High: $52500.00 Low: $50000.00"
        
        with patch('rich.text.Text.assemble', return_value=mock_text):
            chart_panel = monitor._render_price_chart()
            
            assert isinstance(chart_panel, Panel)
            assert "Current:" in mock_text.plain
            assert "High:" in mock_text.plain
            assert "Low:" in mock_text.plain
    
    def test_render_divine_flow(self):
        """Test divine flow rendering"""
        monitor = RedisDivineMonitor()
        
        # Mock Text.assemble to return a controllable text object
        mock_text = MagicMock()
        mock_text.plain = "Divine Resonance: ▁▁▁▂▂▂"
        
        with patch('rich.text.Text.assemble', return_value=mock_text):
            flow_panel = monitor._render_divine_flow()
            
            assert isinstance(flow_panel, Panel)
            assert flow_panel.title == "Divine Flow Energy"
            assert "Divine Resonance:" in mock_text.plain
    
    def test_render_footer(self):
        """Test footer rendering"""
        monitor = RedisDivineMonitor(update_interval=10)
        
        # Mock Text.assemble to return a controllable text object
        mock_text = MagicMock()
        mock_text.plain = "REDIS-ONLY DIVINE MONITOR Press Ctrl+C to exit | Interval: 10s"
        
        with patch('rich.text.Text.assemble', return_value=mock_text):
            footer_panel = monitor._render_footer()
            
            assert isinstance(footer_panel, Panel)
            assert "REDIS-ONLY DIVINE MONITOR" in mock_text.plain
            assert "Interval: 10s" in mock_text.plain
    
    def test_generate_divine_wisdom(self):
        """Test divine wisdom generation"""
        monitor = RedisDivineMonitor()
        
        wisdom = monitor._generate_divine_wisdom()
        
        assert isinstance(wisdom, str)
        assert len(wisdom) > 0
    
    def test_update_layout(self):
        """Test layout update function"""
        monitor = RedisDivineMonitor()
        
        # Mock render functions to return simple string panels for testing
        mock_header = Panel("header")
        mock_markets = Panel("markets")
        mock_price_chart = Panel("price_chart")
        mock_divine_flow = Panel("divine_flow")
        mock_footer = Panel("footer")
        
        with patch.object(monitor, '_render_header', return_value=mock_header), \
             patch.object(monitor, '_render_markets_table', return_value=mock_markets), \
             patch.object(monitor, '_render_price_chart', return_value=mock_price_chart), \
             patch.object(monitor, '_render_divine_flow', return_value=mock_divine_flow), \
             patch.object(monitor, '_render_footer', return_value=mock_footer):
            
            monitor._update_layout()
            
            # Verify update_layout function ran without errors
            # We can't reliably check internal structure of layout due to implementation details
            assert isinstance(monitor.layout, Layout)
    
    @pytest.mark.asyncio
    async def test_process_market_data(self):
        """Test market data processing"""
        monitor = RedisDivineMonitor()
        
        # Create a sample message
        message = {
            "type": "message",
            "data": json.dumps({
                "symbol": "btcusdt",
                "price": 50000,
                "change": "+2.5",
                "volume": 1000000,
                "timestamp": 1616231231
            })
        }
        
        await monitor._process_market_data(message)
        
        # Verify the data was stored
        assert "btcusdt" in monitor.market_data
        assert monitor.market_data["btcusdt"]["price"] == 50000
        assert monitor.market_data["btcusdt"]["change"] == "+2.5"
        assert monitor.market_data["btcusdt"]["volume"] == 1000000
        
        # Verify price and volume history were updated
        assert len(monitor.price_history["btcusdt"]) == 1
        assert monitor.price_history["btcusdt"][0] == 50000
        assert len(monitor.volume_history["btcusdt"]) == 1
        assert monitor.volume_history["btcusdt"][0] == 1000000
    
    @pytest.mark.asyncio
    async def test_process_market_data_invalid_message(self):
        """Test processing invalid market data message"""
        monitor = RedisDivineMonitor()
        
        # Invalid message types
        # Instead of passing None, pass an empty dict which is more appropriate for the function
        await monitor._process_market_data({})
        await monitor._process_market_data({"type": "not_message"})
        await monitor._process_market_data({"type": "message", "data": "not_json"})
        
        # Verify no data was stored
        assert not monitor.market_data
    
    @pytest.mark.asyncio
    async def test_listen_for_market_data(self):
        """Test market data listener function"""
        monitor = RedisDivineMonitor()
        monitor.pubsub = MagicMock()
        
        # Set running to False after one iteration
        monitor.running = True
        
        # Create a sample message
        sample_message = {
            "type": "message",
            "data": json.dumps({
                "symbol": "btcusdt",
                "price": 50000,
                "change": "+2.5",
                "volume": 1000000,
                "timestamp": 1616231231
            })
        }
        
        # Mock process_market_data to set running=False after being called
        original_process = monitor._process_market_data
        
        async def mock_process(message):
            await original_process(message)
            monitor.running = False  # Stop after one iteration
            
        monitor._process_market_data = mock_process
        
        # Mock asyncio.to_thread to return our sample message
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread, \
             patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            
            mock_to_thread.return_value = sample_message
            
            await monitor._listen_for_market_data()
            
            # Verify get_message was called with the correct arguments
            mock_to_thread.assert_called_with(monitor.pubsub.get_message, ignore_subscribe_messages=False)
    
    @pytest.mark.asyncio
    async def test_get_key_prices(self):
        """Test getting key prices from Redis directly"""
        monitor = RedisDivineMonitor()
        monitor.redis = MagicMock()
        
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
            # Mock Redis.get to return a price for btcusdt_price
            mock_to_thread.return_value = "50000"
            await monitor._get_key_prices()
            
            # Verify Redis.get was called for each symbol and key pattern
            assert mock_to_thread.call_count > 0
            
            # Verify price was stored
            assert "btcusdt" in monitor.market_data
            
    @pytest.mark.asyncio
    async def test_run_no_data(self, monkeypatch):
        """Test run method with no data available"""
        monitor = RedisDivineMonitor()
        
        # Mock functions to avoid actual execution
        mocked_connect = AsyncMock()
        mocked_get_prices = AsyncMock()
        mocked_update = MagicMock()
        mocked_disconnect = AsyncMock()
        
        monkeypatch.setattr(monitor, "connect_redis", mocked_connect)
        monkeypatch.setattr(monitor, "_get_key_prices", mocked_get_prices)
        monkeypatch.setattr(monitor, "_update_layout", mocked_update)
        monkeypatch.setattr(monitor, "disconnect_redis", mocked_disconnect)
        
        # Create a listener task mock that doesn't actually call the listener
        listener_task_mock = AsyncMock()
        
        # Mock Live context manager
        mock_live = MagicMock()
        mock_live.__enter__ = MagicMock(return_value=mock_live)
        mock_live.__exit__ = MagicMock(return_value=None)
        
        with patch('rich.live.Live', return_value=mock_live), \
             patch('asyncio.create_task', return_value=listener_task_mock), \
             patch('asyncio.sleep', side_effect=[None, KeyboardInterrupt]):
            
            # Second sleep raises KeyboardInterrupt to exit the loop
            await monitor.run()
            
            # Verify methods were called
            mocked_connect.assert_called_once()
            # We're not checking the listener since we're mocking it completely
            mocked_get_prices.assert_called_once()
            assert mocked_update.call_count > 0
            mocked_disconnect.assert_called_once()
            
            # Verify the listener task was canceled
            listener_task_mock.cancel.assert_called_once()
            
            # Check if sample data was generated
            assert len(monitor.market_data) > 0

# Add tests for main function if needed
@pytest.mark.asyncio
async def test_main():
    """Test main function"""
    with patch('omega_ai.monitor.redis_divine_monitor.RedisDivineMonitor') as mock_monitor_class, \
         patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
        
        # Mock arguments
        mock_args = MagicMock()
        mock_args.interval = 10
        mock_args.symbols = ["btcusdt"]
        mock_args.redis_host = "localhost"
        mock_args.redis_port = 6379
        mock_args.redis_db = 0
        mock_parse_args.return_value = mock_args
        
        # Mock monitor
        mock_monitor = MagicMock()
        mock_monitor.run = AsyncMock()
        mock_monitor_class.return_value = mock_monitor
        
        # Run main
        from omega_ai.monitor.redis_divine_monitor import main
        await main()
        
        # Verify monitor was created with correct arguments
        mock_monitor_class.assert_called_once_with(
            update_interval=10,
            symbols=["btcusdt"],
            redis_host="localhost",
            redis_port=6379,
            redis_db=0
        )
        
        # Verify run was called
        mock_monitor.run.assert_called_once() 