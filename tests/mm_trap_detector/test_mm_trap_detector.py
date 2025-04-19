
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
import json
import asyncio
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch, AsyncMock

from omega_ai.mm_trap_detector.mm_trap_detector import MMTrapDetector


@pytest.fixture
def mock_redis():
    """Mock Redis connection"""
    mock = MagicMock()
    mock.get.return_value = "80000"
    return mock


@pytest.fixture
def trap_detector():
    """Create a detector with mocked dependencies for testing"""
    with patch('omega_ai.mm_trap_detector.mm_trap_detector.redis.Redis', return_value=MagicMock()):
        with patch('omega_ai.mm_trap_detector.mm_trap_detector.InfluxDBClient', return_value=MagicMock()):
            detector = MMTrapDetector()
            detector.influxdb_client = MagicMock()
            detector.influxdb_client.ping.return_value = True
            detector.redis_conn = MagicMock()
            detector.redis_conn.get.return_value = "80000"
            detector.prev_btc_price = 80000.0
            detector.current_btc_price = 80000.0
            return detector


class TestMMTrapDetector:
    """Divine tests for Market Maker Trap Detector."""
    
    @pytest.mark.asyncio
    async def test_handle_websocket_message_string(self, trap_detector):
        """Test handling websocket message as string."""
        # Arrange
        json_msg = '{"btc_price": 81000.0}'
        
        # Mock process_price_update
        trap_detector.process_price_update = AsyncMock()
        
        # Act
        await trap_detector.handle_websocket_message(json_msg)
        
        # Assert
        trap_detector.process_price_update.assert_called_once_with(81000.0)
    
    @pytest.mark.asyncio
    async def test_handle_websocket_message_bytes(self, trap_detector):
        """Test handling websocket message as bytes."""
        # Arrange
        json_msg = b'{"btc_price": 81000.0}'
        
        # Mock process_price_update
        trap_detector.process_price_update = AsyncMock()
        
        # Act
        await trap_detector.handle_websocket_message(json_msg)
        
        # Assert
        trap_detector.process_price_update.assert_called_once_with(81000.0)
    
    @pytest.mark.asyncio
    async def test_handle_invalid_websocket_message(self, trap_detector):
        """Test handling invalid websocket message."""
        # Arrange
        invalid_msg = '{invalid json'
        
        # Mock process_price_update
        trap_detector.process_price_update = AsyncMock()
        
        # Act
        await trap_detector.handle_websocket_message(invalid_msg)
        
        # Assert
        trap_detector.process_price_update.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_process_price_update(self, trap_detector):
        """Test processing price updates."""
        # Arrange
        price = 81500.0
        trap_detector.analyze_movement = AsyncMock(return_value="Organic Movement")
        trap_detector.print_analysis_result = AsyncMock()
        trap_detector.register_trap_detection = MagicMock()
        trap_detector.get_current_volume = MagicMock(return_value=100.0)
        trap_detector.check_high_frequency_mode = MagicMock(return_value=False)
        trap_detector.calculate_dynamic_threshold = MagicMock(return_value=0.5)
        
        # Act
        await trap_detector.process_price_update(price)
        
        # Assert
        trap_detector.analyze_movement.assert_called_once()
        trap_detector.print_analysis_result.assert_called_once()
        assert trap_detector.prev_btc_price == price
        trap_detector.register_trap_detection.assert_not_called()  # No trap was detected
    
    @pytest.mark.asyncio
    async def test_process_price_update_with_trap(self, trap_detector):
        """Test processing price updates with trap detection."""
        # Arrange
        price = 81500.0
        trap_detector.analyze_movement = AsyncMock(return_value="TRAP detected: Fake Pump")
        trap_detector.print_analysis_result = AsyncMock()
        trap_detector.register_trap_detection = MagicMock()
        trap_detector.get_current_volume = MagicMock(return_value=100.0)
        trap_detector.check_high_frequency_mode = MagicMock(return_value=False)
        trap_detector.calculate_dynamic_threshold = MagicMock(return_value=0.5)
        
        # Act
        await trap_detector.process_price_update(price)
        
        # Assert
        trap_detector.analyze_movement.assert_called_once()
        trap_detector.print_analysis_result.assert_called_once()
        assert trap_detector.prev_btc_price == price
        trap_detector.register_trap_detection.assert_called_once()  # Trap was detected
    
    def test_get_current_volume(self, trap_detector):
        """Test getting current volume from Redis."""
        # Arrange
        trap_detector.redis_conn.get.return_value = "1500.25"
        
        # Act
        volume = trap_detector.get_current_volume()
        
        # Assert
        assert volume == 1500.25
        trap_detector.redis_conn.get.assert_called_once_with("last_btc_volume")
    
    def test_get_current_volume_error(self, trap_detector):
        """Test handling error when getting volume from Redis."""
        # Arrange
        trap_detector.redis_conn.get.return_value = None
        
        # Act
        volume = trap_detector.get_current_volume()
        
        # Assert
        assert volume == 0.0
    
    def test_calculate_dynamic_threshold(self, trap_detector):
        """Test calculation of dynamic threshold."""
        # Arrange
        trap_detector.redis_conn.get.side_effect = lambda key: {
            'rolling_volatility': '0.8',
            'market_regime': 'volatile',
            'directional_strength': '0.6'
        }.get(key, None)
        
        # Act
        threshold = trap_detector.calculate_dynamic_threshold(False)
        hf_threshold = trap_detector.calculate_dynamic_threshold(True)
        
        # Assert
        assert threshold == 0.8 * 0.75  # BASE * regime_multiplier
        assert hf_threshold < threshold  # HF mode should have lower threshold 