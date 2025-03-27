# Copyright (c) 2024 OMEGA BTC AI Team
# Licensed under the GNU Affero General Public License v3.0
# See https://www.gnu.org/licenses/ for more details

"""
Tests for ML training data export and Grafana integration.
"""

import unittest
import json
import datetime
from unittest.mock import patch, MagicMock
import redis
import sys
import os
from typing import Dict, List, Any

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the module to test
from omega_ai.mm_trap_detector.redis_time_series import (
    store_ml_training_data,
    export_ml_training_data,
    store_grafana_metrics,
    export_grafana_dashboard,
    TimeSeriesGranularity
)

class TestDataExport(unittest.TestCase):
    """Tests for ML training data export and Grafana integration"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a mock Redis connection
        self.redis_mock = MagicMock()
        self.redis_patcher = patch('omega_ai.mm_trap_detector.redis_time_series.redis_conn', self.redis_mock)
        self.redis_patcher.start()

        # Sample trap data
        self.sample_trap = {
            "timestamp": "2024-03-20 14:30:00",
            "trap_type": "Liquidity Grab",
            "confidence": 0.85,
            "price": 85000.0,
            "price_change_pct": 1.5,
            "market_regime": "High Volatility Bullish",
            "features": {
                "volatility_1min": 0.05,
                "volatility_5min": 0.12,
                "price_acceleration": 0.08,
                "volume_change": 150.0,
                "schumann_resonance": 7.83,
                "fibonacci_level": 0.618,
                "trap_count_1h": 3,
                "trap_count_24h": 12,
                "consecutive_traps": 2
            }
        }

        # Sample market data with enhanced metrics
        self.sample_market_data = {
            "timestamp": "2024-03-20 14:30:00",
            "price": 85000.0,
            "volume_24h": 1500.0,
            "volatility": 0.05,
            "trend": "bullish",
            "regime": "High Volatility Bullish",
            "technical_indicators": {
                "rsi_14": 65.5,
                "macd": 125.5,
                "macd_signal": 110.2,
                "bb_upper": 86000.0,
                "bb_lower": 84000.0,
                "ma_50": 82500.0,
                "ma_200": 80000.0
            },
            "volume_metrics": {
                "buy_volume_ratio": 1.2,
                "volume_ma_ratio": 1.5,
                "large_trades_ratio": 0.8
            },
            "market_context": {
                "funding_rate": 0.01,
                "open_interest": 2500000000,
                "long_short_ratio": 1.25
            }
        }

    def tearDown(self):
        """Tear down test fixtures"""
        self.redis_patcher.stop()

    def test_store_ml_training_data(self):
        """Test storing ML training data with enhanced features"""
        # Act
        success = store_ml_training_data(
            trap_data=self.sample_trap,
            market_data=self.sample_market_data
        )

        # Assert
        self.assertTrue(success)
        
        # Verify the call to Redis
        self.redis_mock.rpush.assert_called_once()
        call_args = self.redis_mock.rpush.call_args[0]
        self.assertEqual(call_args[0], "sim_ml_training_data")
        
        # Parse stored data
        stored_data = json.loads(call_args[1])
        
        # Verify basic fields
        self.assertEqual(stored_data["timestamp"], self.sample_trap["timestamp"])
        self.assertEqual(stored_data["label"], self.sample_trap["trap_type"])
        self.assertEqual(stored_data["confidence"], self.sample_trap["confidence"])
        self.assertEqual(stored_data["market_regime"], self.sample_market_data["regime"])
        
        # Verify enhanced features
        features = stored_data["features"]
        self.assertIn("fibonacci_level", features)
        self.assertIn("trap_count_1h", features)
        self.assertIn("trap_count_24h", features)
        self.assertIn("consecutive_traps", features)
        
        # Verify technical indicators
        self.assertIn("rsi_14", features)
        self.assertIn("macd", features)
        self.assertIn("macd_signal", features)
        self.assertIn("bb_upper", features)
        self.assertIn("bb_lower", features)
        self.assertIn("ma_50", features)
        self.assertIn("ma_200", features)
        
        # Verify volume metrics
        self.assertIn("buy_volume_ratio", features)
        self.assertIn("volume_ma_ratio", features)
        self.assertIn("large_trades_ratio", features)
        
        # Verify market context
        self.assertIn("funding_rate", features)
        self.assertIn("open_interest", features)
        self.assertIn("long_short_ratio", features)
        
        # Verify all feature values are numeric
        for key, value in features.items():
            self.assertIsInstance(value, (int, float), f"Feature {key} should be numeric")

    def test_validate_ml_features(self):
        """Test validation of ML training data features"""
        # Create data with invalid features
        invalid_trap = self.sample_trap.copy()
        invalid_trap["features"]["invalid_metric"] = "not_a_number"
        
        # Act
        success = store_ml_training_data(
            trap_data=invalid_trap,
            market_data=self.sample_market_data
        )
        
        # Assert
        self.assertFalse(success)  # Should fail validation

    def test_export_ml_training_data(self):
        """Test exporting ML training data"""
        # Arrange
        training_data = {
            "timestamp": self.sample_trap["timestamp"],
            "label": self.sample_trap["trap_type"],
            "confidence": self.sample_trap["confidence"],
            "features": {
                **self.sample_trap["features"],
                "price": self.sample_market_data["price"],
                "volume_24h": self.sample_market_data["volume_24h"],
                "market_volatility": self.sample_market_data["volatility"],
                "market_regime": self.sample_market_data["regime"]
            }
        }
        self.redis_mock.lrange.return_value = [json.dumps(training_data)]

        # Act
        data = export_ml_training_data(start_date=datetime.date(2024, 3, 20))

        # Assert
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["label"], self.sample_trap["trap_type"])
        self.assertTrue("features" in data[0])
        self.assertEqual(data[0]["confidence"], self.sample_trap["confidence"])

    def test_store_grafana_metrics(self):
        """Test storing Grafana metrics"""
        # Act
        success = store_grafana_metrics(
            timestamp=datetime.datetime.now(datetime.UTC),
            metrics={
                "trap_count": 5,
                "confidence_avg": 0.85,
                "price_change_avg": 1.2,
                "volatility": 0.05
            }
        )

        # Assert
        self.assertTrue(success)
        self.redis_mock.hset.assert_called()

    def test_export_grafana_dashboard(self):
        """Test exporting Grafana dashboard data"""
        # Arrange
        current_time = datetime.datetime.now(datetime.UTC)
        self.redis_mock.hgetall.return_value = {
            b"trap_count": b"5",
            b"confidence_avg": b"0.85",
            b"price_change_avg": b"1.2",
            b"volatility": b"0.05"
        }

        # Act
        dashboard_data = export_grafana_dashboard(
            start_time=current_time - datetime.timedelta(hours=1),
            end_time=current_time
        )

        # Assert
        self.assertTrue("panels" in dashboard_data)
        self.assertTrue("datasource" in dashboard_data)
        self.assertEqual(len(dashboard_data["panels"]), 4)  # 4 metrics

if __name__ == '__main__':
    unittest.main() 