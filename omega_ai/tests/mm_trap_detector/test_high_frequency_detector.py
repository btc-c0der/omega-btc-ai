
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

# Copyright (c) 2024 OMEGA BTC AI Team
# Licensed under the GNU Affero General Public License v3.0
# See https://www.gnu.org/licenses/ for more details

"""
Tests for high-frequency market manipulation trap detector.
"""

import unittest
import datetime
import numpy as np
from unittest.mock import patch, MagicMock, ANY
import redis
import sys
import os
from typing import Dict, List, Any
from collections import deque

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import the module to test
from omega_ai.mm_trap_detector.high_frequency_detector import (
    HighFrequencyTrapDetector,
    check_high_frequency_mode,
    register_trap_detection,
    simulate_price_updates,
    run_continuous_simulation
)

class TestHighFrequencyDetector(unittest.TestCase):
    """Tests for high-frequency market manipulation trap detection"""

    def setUp(self):
        """Set up test fixtures"""
        # Create a mock Redis connection
        self.redis_mock = MagicMock()
        self.redis_patcher = patch('omega_ai.mm_trap_detector.high_frequency_detector.redis_conn', self.redis_mock)
        self.redis_patcher.start()

        # Initialize detector
        self.detector = HighFrequencyTrapDetector()

        # Sample price data
        self.sample_prices = [80000.0, 80100.0, 80200.0, 80300.0, 80400.0]
        self.sample_timestamps = [
            datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=i)
            for i in range(len(self.sample_prices))
        ]

    def tearDown(self):
        """Tear down test fixtures"""
        self.redis_patcher.stop()

    def test_price_history_update(self):
        """Test updating price history"""
        # Act
        for price, timestamp in zip(self.sample_prices, self.sample_timestamps):
            self.detector.update_price_data(price, timestamp)

        # Assert
        self.assertEqual(len(self.detector.price_history_1min), len(self.sample_prices))
        self.assertEqual(len(self.detector.price_history_5min), len(self.sample_prices) // 5)

    def test_volatility_calculation(self):
        """Test volatility calculation and storage"""
        # Arrange
        for price, timestamp in zip(self.sample_prices, self.sample_timestamps):
            self.detector.update_price_data(price, timestamp)

        # Act
        self.detector._calculate_volatility_metrics()

        # Assert
        self.redis_mock.set.assert_any_call("volatility_1min", ANY)
        self.redis_mock.set.assert_any_call("volatility_5min", ANY)
        self.redis_mock.set.assert_any_call("price_acceleration_1min", ANY)

    def test_high_frequency_mode_detection(self):
        """Test high-frequency mode detection"""
        # Arrange
        latest_price = 80500.0
        schumann_resonance = 7.83

        # Act
        hf_active, multiplier = self.detector.detect_high_freq_trap_mode(
            latest_price=latest_price,
            schumann_resonance=schumann_resonance
        )

        # Assert
        self.assertIsInstance(hf_active, bool)
        self.assertIsInstance(multiplier, float)
        self.assertGreaterEqual(multiplier, 0.5)
        self.assertLessEqual(multiplier, 1.0)

    def test_trap_event_registration(self):
        """Test registering trap events"""
        # Arrange
        trap_type = "Liquidity Grab"
        confidence = 0.85
        price_change = 0.015  # 1.5%

        # Act
        self.detector.register_trap_event(trap_type, confidence, price_change)

        # Assert
        self.assertEqual(len(self.detector.trap_events), 1)
        self.assertEqual(self.detector.trap_events[0]["trap_type"], trap_type)
        self.assertEqual(self.detector.trap_events[0]["confidence"], confidence)
        self.assertEqual(self.detector.trap_events[0]["price_change"], price_change)

    def test_recent_trap_counting(self):
        """Test counting recent trap events"""
        # Arrange
        current_time = datetime.datetime.now(datetime.UTC)
        trap_events = deque([
            {
                "timestamp": current_time - datetime.timedelta(minutes=i),
                "trap_type": "Liquidity Grab",
                "confidence": 0.85,
                "price_change": 0.015
            }
            for i in range(5)
        ])
        self.detector.trap_events = trap_events

        # Act
        count = self.detector._count_recent_traps()

        # Assert
        self.assertGreaterEqual(count, 0)
        self.assertLessEqual(count, len(trap_events))

    def test_schumann_anomaly_detection(self):
        """Test Schumann resonance anomaly detection"""
        # Act
        severity, message = self.detector.check_schumann_anomalies(simulation_mode=True)

        # Assert
        self.assertIsInstance(severity, int)
        self.assertIsInstance(message, str)
        self.assertGreaterEqual(severity, 0)
        self.assertLessEqual(severity, 3)

    def test_liquidity_grab_detection(self):
        """Test liquidity grab detection"""
        # Arrange
        latest_price = 80500.0

        # Act
        grab_type, confidence = self.detector.detect_liquidity_grabs(
            latest_price=latest_price,
            simulation_mode=True
        )

        # Assert
        self.assertIsInstance(grab_type, (str, type(None)))
        self.assertIsInstance(confidence, float)
        if grab_type is not None:
            self.assertGreaterEqual(confidence, 0.0)
            self.assertLessEqual(confidence, 1.0)

    def test_simulation_price_updates(self):
        """Test price update simulation"""
        # Act
        simulate_price_updates()

        # Assert
        self.redis_mock.set.assert_any_call("sim_last_btc_price", ANY)
        self.redis_mock.set.assert_any_call("sim_prev_btc_price", ANY)

    def test_continuous_simulation(self):
        """Test continuous simulation functionality"""
        # Act
        with patch('time.sleep') as mock_sleep:
            run_continuous_simulation(
                duration_hours=0.1,  # 6 minutes
                volatility_scale=1.0,
                trap_frequency=0.2
            )

        # Assert
        self.redis_mock.set.assert_any_call("sim_running", "1")
        self.redis_mock.set.assert_any_call("sim_running", "0")
        mock_sleep.assert_called()

if __name__ == '__main__':
    unittest.main() 