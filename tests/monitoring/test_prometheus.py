#!/usr/bin/env python3

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
🔱 OMEGA BTC AI - Prometheus Monitoring Tests 🔱
This module contains comprehensive tests for the Prometheus monitoring service.
"""

import unittest
import aiohttp
import asyncio
import pytest
from typing import Dict, List, Any
from datetime import datetime, timedelta

class TestPrometheusMonitoring(unittest.TestCase):
    """Divine test suite for the Prometheus monitoring service."""
    
    BASE_URL = "http://localhost:9090"
    
    @classmethod
    def setUpClass(cls):
        """Set up divine test environment."""
        print("\n🔱 Initializing Prometheus Monitoring Tests 🔱")
        cls.session = None
    
    async def async_setUp(self):
        """Set up async test environment."""
        self.session = aiohttp.ClientSession()
    
    async def async_tearDown(self):
        """Clean up async test environment."""
        if self.session:
            await self.session.close()
    
    @pytest.mark.asyncio
    async def test_prometheus_health(self):
        """Test the divine Prometheus health endpoint."""
        async with self.session.get(f"{self.BASE_URL}/-/healthy") as response:
            self.assertEqual(response.status, 200)
            data = await response.text()
            self.assertIn("Prometheus is Healthy", data)
    
    @pytest.mark.asyncio
    async def test_target_status(self):
        """Test divine target discovery and status."""
        async with self.session.get(f"{self.BASE_URL}/api/v1/targets") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("data", data)
            self.assertIn("activeTargets", data["data"])
            
            # Check if all services are being scraped
            active_targets = data["data"]["activeTargets"]
            service_names = [target["labels"]["job"] for target in active_targets]
            self.assertIn("matrix-news", service_names)
            self.assertIn("consciousness", service_names)
            self.assertIn("temporal-worker", service_names)
    
    @pytest.mark.asyncio
    async def test_metrics_collection(self):
        """Test divine metrics collection."""
        # Query for specific metrics
        metrics = [
            "matrix_news_requests_total",
            "consciousness_processing_time_seconds",
            "temporal_workflow_executions_total"
        ]
        
        for metric in metrics:
            async with self.session.get(
                f"{self.BASE_URL}/api/v1/query",
                params={"query": metric}
            ) as response:
                self.assertEqual(response.status, 200)
                data = await response.json()
                self.assertIn("data", data)
                self.assertIn("result", data["data"])
    
    @pytest.mark.asyncio
    async def test_alert_rules(self):
        """Test divine alert rules configuration."""
        async with self.session.get(f"{self.BASE_URL}/api/v1/rules") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("data", data)
            self.assertIn("groups", data["data"])
            
            # Check for specific alert rules
            alert_rules = []
            for group in data["data"]["groups"]:
                for rule in group["rules"]:
                    alert_rules.append(rule["name"])
            
            expected_alerts = [
                "HighErrorRate",
                "HighLatency",
                "ServiceDown"
            ]
            
            for alert in expected_alerts:
                self.assertTrue(any(alert in rule for rule in alert_rules))
    
    @pytest.mark.asyncio
    async def test_metric_labels(self):
        """Test divine metric labels and dimensions."""
        async with self.session.get(
            f"{self.BASE_URL}/api/v1/labels",
            params={"match[]": "{job=~'.*'}"}
        ) as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("data", data)
            
            # Check for required labels
            required_labels = ["job", "instance", "environment"]
            for label in required_labels:
                self.assertIn(label, data["data"])
    
    @pytest.mark.asyncio
    async def test_metric_values(self):
        """Test divine metric value ranges and types."""
        # Query for specific metrics with value validation
        queries = [
            ("matrix_news_requests_total", "> 0"),
            ("consciousness_processing_time_seconds", "> 0"),
            ("temporal_workflow_executions_total", ">= 0")
        ]
        
        for metric, condition in queries:
            async with self.session.get(
                f"{self.BASE_URL}/api/v1/query",
                params={"query": f"{metric} {condition}"}
            ) as response:
                self.assertEqual(response.status, 200)
                data = await response.json()
                self.assertIn("data", data)
                self.assertIn("result", data["data"])
                self.assertGreater(len(data["data"]["result"]), 0)
    
    @pytest.mark.asyncio
    async def test_metric_aggregation(self):
        """Test divine metric aggregation functions."""
        aggregation_functions = [
            "sum",
            "avg",
            "max",
            "min"
        ]
        
        for func in aggregation_functions:
            query = f"{func}(matrix_news_requests_total[5m])"
            async with self.session.get(
                f"{self.BASE_URL}/api/v1/query",
                params={"query": query}
            ) as response:
                self.assertEqual(response.status, 200)
                data = await response.json()
                self.assertIn("data", data)
                self.assertIn("result", data["data"])
    
    @pytest.mark.asyncio
    async def test_metric_timestamps(self):
        """Test divine metric timestamp handling."""
        async with self.session.get(
            f"{self.BASE_URL}/api/v1/query",
            params={"query": "matrix_news_requests_total[1h]"}
        ) as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("data", data)
            self.assertIn("result", data["data"])
            
            # Check timestamp format and range
            for result in data["data"]["result"]:
                for value in result["values"]:
                    timestamp = value[0]
                    self.assertIsInstance(timestamp, (int, float))
                    self.assertGreater(timestamp, 0)
                    
                    # Convert to datetime and check range
                    dt = datetime.fromtimestamp(timestamp)
                    self.assertGreater(dt, datetime.now() - timedelta(hours=1))
                    self.assertLessEqual(dt, datetime.now())

if __name__ == "__main__":
    unittest.main() 