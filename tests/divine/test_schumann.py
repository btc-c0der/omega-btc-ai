#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔱 OMEGA BTC AI - Schumann Resonance Divine Tests 🔱
This module contains comprehensive tests for the Schumann resonance divine feature.
"""

import unittest
import aiohttp
import asyncio
import pytest
from typing import Dict, List, Any
from datetime import datetime, timedelta

class TestSchumannResonance(unittest.TestCase):
    """Divine test suite for the Schumann resonance feature."""
    
    BASE_URL = "http://localhost:10083"
    
    @classmethod
    def setUpClass(cls):
        """Set up divine test environment."""
        print("\n🔱 Initializing Schumann Resonance Divine Tests 🔱")
        cls.session = None
    
    async def async_setUp(self):
        """Set up async test environment."""
        self.session = aiohttp.ClientSession()
    
    async def async_tearDown(self):
        """Clean up async test environment."""
        if self.session:
            await self.session.close()
    
    @pytest.mark.asyncio
    async def test_schumann_current(self):
        """Test the divine current Schumann resonance measurement."""
        async with self.session.get(f"{self.BASE_URL}/api/schumann/current") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("measurement", data)
            measurement = data["measurement"]
            
            # Verify measurement components
            self.assertIn("frequency", measurement)
            self.assertIn("amplitude", measurement)
            self.assertIn("timestamp", measurement)
            
            # Verify measurement values
            self.assertGreater(measurement["frequency"], 0)
            self.assertGreater(measurement["amplitude"], 0)
            self.assertIsInstance(measurement["timestamp"], str)
    
    @pytest.mark.asyncio
    async def test_schumann_history(self):
        """Test the divine Schumann resonance historical data."""
        async with self.session.get(f"{self.BASE_URL}/api/schumann/history/24h") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("history", data)
            history = data["history"]
            
            # Verify history data
            self.assertIsInstance(history, list)
            self.assertGreater(len(history), 0)
            
            # Verify data points
            for point in history:
                self.assertIn("frequency", point)
                self.assertIn("amplitude", point)
                self.assertIn("timestamp", point)
                
                # Verify timestamp format and range
                timestamp = datetime.fromisoformat(point["timestamp"])
                self.assertGreater(timestamp, datetime.now() - timedelta(hours=24))
                self.assertLessEqual(timestamp, datetime.now())
    
    @pytest.mark.asyncio
    async def test_schumann_analysis(self):
        """Test the divine Schumann resonance analysis."""
        async with self.session.get(f"{self.BASE_URL}/api/schumann/analyze/7d") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("analysis", data)
            analysis = data["analysis"]
            
            # Verify analysis components
            self.assertIn("average_frequency", analysis)
            self.assertIn("average_amplitude", analysis)
            self.assertIn("peak_frequency", analysis)
            self.assertIn("peak_amplitude", analysis)
            self.assertIn("variation", analysis)
            
            # Verify analysis values
            self.assertGreater(analysis["average_frequency"], 0)
            self.assertGreater(analysis["average_amplitude"], 0)
            self.assertGreater(analysis["peak_frequency"], 0)
            self.assertGreater(analysis["peak_amplitude"], 0)
            self.assertGreaterEqual(analysis["variation"], 0)
    
    @pytest.mark.asyncio
    async def test_schumann_prediction(self):
        """Test the divine Schumann resonance prediction."""
        async with self.session.get(f"{self.BASE_URL}/api/schumann/predict/1h") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("prediction", data)
            prediction = data["prediction"]
            
            # Verify prediction components
            self.assertIn("forecast", prediction)
            self.assertIn("confidence", prediction)
            self.assertIn("factors", prediction)
            
            # Verify prediction values
            self.assertIsInstance(prediction["forecast"], list)
            self.assertGreater(len(prediction["forecast"]), 0)
            self.assertGreater(prediction["confidence"], 0)
            self.assertLessEqual(prediction["confidence"], 1)
    
    @pytest.mark.asyncio
    async def test_schumann_correlation(self):
        """Test the divine Schumann resonance correlation analysis."""
        async with self.session.get(f"{self.BASE_URL}/api/schumann/correlate/btc") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("correlation", data)
            correlation = data["correlation"]
            
            # Verify correlation components
            self.assertIn("coefficient", correlation)
            self.assertIn("p_value", correlation)
            self.assertIn("strength", correlation)
            
            # Verify correlation values
            self.assertGreaterEqual(correlation["coefficient"], -1)
            self.assertLessEqual(correlation["coefficient"], 1)
            self.assertGreater(correlation["p_value"], 0)
            self.assertLessEqual(correlation["p_value"], 1)
    
    @pytest.mark.asyncio
    async def test_schumann_visualization(self):
        """Test the divine Schumann resonance visualization."""
        async with self.session.get(f"{self.BASE_URL}/api/schumann/visualize/24h") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("visualization", data)
            visualization = data["visualization"]
            
            # Verify visualization components
            self.assertIn("svg", visualization)
            self.assertIn("dimensions", visualization)
            self.assertIn("data_points", visualization)
            
            # Verify SVG content
            self.assertTrue(visualization["svg"].startswith("<svg"))
            self.assertTrue(visualization["svg"].endswith("</svg>"))
            
            # Verify dimensions
            self.assertIn("width", visualization["dimensions"])
            self.assertIn("height", visualization["dimensions"])
            self.assertGreater(visualization["dimensions"]["width"], 0)
            self.assertGreater(visualization["dimensions"]["height"], 0)
    
    @pytest.mark.asyncio
    async def test_schumann_alerts(self):
        """Test the divine Schumann resonance alert system."""
        async with self.session.get(f"{self.BASE_URL}/api/schumann/alerts") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("alerts", data)
            alerts = data["alerts"]
            
            # Verify alerts structure
            self.assertIsInstance(alerts, list)
            for alert in alerts:
                self.assertIn("type", alert)
                self.assertIn("severity", alert)
                self.assertIn("message", alert)
                self.assertIn("timestamp", alert)
                
                # Verify alert values
                self.assertIn(alert["severity"], ["low", "medium", "high", "critical"])
                self.assertGreater(len(alert["message"]), 0)
    
    @pytest.mark.asyncio
    async def test_schumann_validation(self):
        """Test the divine Schumann resonance input validation."""
        invalid_inputs = ["invalid", "-1h", "25h", "8d"]
        
        for invalid_input in invalid_inputs:
            async with self.session.get(f"{self.BASE_URL}/api/schumann/history/{invalid_input}") as response:
                self.assertEqual(response.status, 400)
                data = await response.json()
                self.assertIn("error", data)
                self.assertIn("message", data)

if __name__ == "__main__":
    unittest.main() 