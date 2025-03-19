import pytest
import json
import os
import sys
import time
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Import components that interact with Redis
from omega_ai.tools.trap_probability_meter import TrapProbabilityMeter
from omega_ai.tools.redis_trap_monitor import RedisTrapMonitor

class TestRedisIntegration:
    """Integration tests for Redis-based component interactions"""
    
    def test_trap_monitor_reads_trap_probability_predictions(self, mock_redis_with_data):
        """Test that trap monitor can read predictions from trap probability meter"""
        # Create trap probability meter instance and inject mock Redis
        probability_meter = TrapProbabilityMeter()
        probability_meter.redis_client = mock_redis_with_data
        
        # Store a high probability trap prediction
        trap_type = "Bull Trap"
        probability = 0.85
        confidence = 0.8
        probability_meter._store_trap_prediction(trap_type, probability, confidence)
        
        # Check prediction was stored in Redis
        assert mock_redis_with_data.exists("trap_predictions")
        assert mock_redis_with_data.exists("latest_trap_prediction")
        
        # Create trap monitor with the same Redis client
        with patch('redis.Redis', return_value=mock_redis_with_data):
            monitor = RedisTrapMonitor()
            monitor.redis = mock_redis_with_data
            
            # Add the trap_predictions key pattern to processed_traps
            # so find_new_traps will look for it
            prediction_bytes = mock_redis_with_data.lrange("trap_predictions", 0, -1)[0]
            prediction = json.loads(prediction_bytes)
            
            # Assert the prediction data contains expected values
            assert prediction["type"] == trap_type
            assert prediction["probability"] == probability
            assert prediction["confidence"] == confidence
    
    def test_probability_meter_reads_monitor_trap_data(self, mock_redis_with_data):
        """Test that trap probability meter can read traps from monitor"""
        # Add some trap data to Redis (as the monitor would)
        trap_data = {
            "type": "Liquidity Grab",
            "confidence": 0.9,
            "price": 85000.0,
            "timestamp": datetime.now().isoformat()
        }
        mock_redis_with_data.lpush("recent_mm_traps", json.dumps(trap_data))
        
        # Create trap probability meter with the mock Redis
        probability_meter = TrapProbabilityMeter()
        probability_meter.redis_client = mock_redis_with_data
        
        # Call detect_likely_trap_type which should read from recent_mm_traps
        trap_type, confidence = probability_meter._detect_likely_trap_type()
        
        # Check the trap was properly detected
        assert trap_type is not None
        assert 0.0 <= confidence <= 1.0
        assert "Liquidity" in trap_type or "Grab" in trap_type  # Should match or be similar
    
    def test_full_probability_calculation_with_redis_data(self, mock_redis_with_data):
        """Test full probability calculation using data from Redis"""
        # Create trap probability meter with mock Redis
        probability_meter = TrapProbabilityMeter()
        probability_meter.redis_client = mock_redis_with_data
        
        # Calculate overall probability
        probability = probability_meter._calculate_probability()
        
        # Check probability is within expected range
        assert 0.0 <= probability <= 1.0
        
        # Check all components were updated
        for comp_name, comp_data in probability_meter.components.items():
            assert 0.0 <= comp_data["value"] <= 1.0
            assert comp_data["description"] != ""  # Description should be updated
    
    def test_data_flow_from_live_feed_to_probability_meter(self, mock_redis):
        """Test data flow from btc_live_feed to probability meter"""
        # Simulate btc_live_feed updating Redis
        price = 85000.0
        volume = 120.5
        
        # Mock the btc_live_feed.update_redis functionality directly
        mock_redis.set("last_btc_price", price)
        mock_redis.set("last_btc_volume", volume)
        
        # Add some price history
        for i in range(10):
            mock_redis.rpush("btc_movement_history", price + (i * 50))
        
        # Create trap probability meter with the mock Redis
        probability_meter = TrapProbabilityMeter()
        probability_meter.redis_client = mock_redis
        
        # Get price from Redis through the probability meter
        current_price = probability_meter._get_current_btc_price()
        current_volume, _ = probability_meter._get_volume_data()
        
        # Check values match what btc_live_feed would have updated
        assert current_price == price
        assert current_volume == volume
    
    def test_trap_alert_flow(self, mock_redis_with_data):
        """Test the full flow of trap detection, storage, and alerting"""
        # First simulate high probability from the meter
        probability_meter = TrapProbabilityMeter()
        probability_meter.redis_client = mock_redis_with_data
        
        # Store a high probability prediction
        probability_meter._store_trap_prediction("Bull Trap", 0.9, 0.85)
        
        # Now create a trap monitor
        with patch('redis.Redis', return_value=mock_redis_with_data):
            with patch('omega_ai.tools.redis_trap_monitor.send_alert') as mock_send_alert:
                monitor = RedisTrapMonitor()
                monitor.redis = mock_redis_with_data
                
                # Get a trap item from Redis
                prediction_bytes = mock_redis_with_data.lrange("trap_predictions", 0, -1)[0]
                prediction = json.loads(prediction_bytes)
                
                # Process the trap (which should trigger an alert)
                monitor.process_trap("trap_predictions:0", prediction)
                
                # Check alert was sent
                mock_send_alert.assert_called_once()
                
                # Check trap count was incremented
                assert monitor.trap_count == 1 