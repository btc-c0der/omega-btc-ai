#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔱 OMEGA BTC AI - Service Integration Tests 🔱
This module contains comprehensive tests for service integration.
"""

import unittest
import aiohttp
import asyncio
import pytest
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta

class TestServiceIntegration(unittest.TestCase):
    """Divine test suite for service integration testing."""
    
    BASE_URL = "http://localhost:10083"
    
    @classmethod
    def setUpClass(cls):
        """Set up divine test environment."""
        print("\n🔱 Initializing Service Integration Tests 🔱")
        cls.session = None
    
    async def async_setUp(self):
        """Set up async test environment."""
        self.session = aiohttp.ClientSession()
    
    async def async_tearDown(self):
        """Clean up async test environment."""
        if self.session:
            await self.session.close()
    
    @pytest.mark.asyncio
    async def test_matrix_news_consciousness_integration(self):
        """Test the divine integration between Matrix News and Consciousness services."""
        # Get news from Matrix News service
        async with self.session.get(f"{self.BASE_URL}/api/news/") as response:
            self.assertEqual(response.status, 200)
            news_data = await response.json()
            self.assertGreater(len(news_data), 0)
            
            # Process news through Consciousness service
            for news_item in news_data[:5]:  # Test with first 5 items
                async with self.session.post(
                    f"{self.BASE_URL}/api/consciousness/process",
                    json={"content": news_item["content"]}
                ) as response:
                    self.assertEqual(response.status, 200)
                    consciousness_data = await response.json()
                    self.assertIn("analysis", consciousness_data)
                    self.assertIn("sentiment", consciousness_data)
                    self.assertIn("entities", consciousness_data)
    
    @pytest.mark.asyncio
    async def test_consciousness_temporal_integration(self):
        """Test the divine integration between Consciousness and Temporal services."""
        # Create workflow through Temporal
        workflow_data = {
            "type": "consciousness_analysis",
            "parameters": {
                "content": "Test content for consciousness analysis",
                "depth": "deep"
            }
        }
        
        async with self.session.post(
            f"{self.BASE_URL}/api/temporal/workflow",
            json=workflow_data
        ) as response:
            self.assertEqual(response.status, 200)
            workflow_response = await response.json()
            self.assertIn("workflow_id", workflow_response)
            workflow_id = workflow_response["workflow_id"]
        
        # Wait for workflow completion
        await asyncio.sleep(5)
        
        # Check workflow status
        async with self.session.get(
            f"{self.BASE_URL}/api/temporal/workflow/{workflow_id}"
        ) as response:
            self.assertEqual(response.status, 200)
            status_data = await response.json()
            self.assertEqual(status_data["status"], "completed")
            self.assertIn("result", status_data)
    
    @pytest.mark.asyncio
    async def test_state_management_integration(self):
        """Test the divine integration of state management across services."""
        # Store state
        test_state = {
            "key": "integration_test",
            "value": "test_value",
            "metadata": {
                "service": "matrix_news",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        async with self.session.post(
            f"{self.BASE_URL}/api/state/store",
            json=test_state
        ) as response:
            self.assertEqual(response.status, 200)
            store_response = await response.json()
            self.assertEqual(store_response["status"], "success")
        
        # Verify state across services
        services = ["matrix-news", "consciousness", "temporal-worker"]
        for service in services:
            async with self.session.get(
                f"{self.BASE_URL}/api/state/verify/{test_state['key']}/{service}"
            ) as response:
                self.assertEqual(response.status, 200)
                verify_data = await response.json()
                self.assertTrue(verify_data["exists"])
                self.assertEqual(verify_data["value"], test_state["value"])
    
    @pytest.mark.asyncio
    async def test_monitoring_integration(self):
        """Test the divine integration of monitoring across services."""
        # Get metrics from all services
        services = ["matrix-news", "consciousness", "temporal-worker"]
        metrics_data = {}
        
        for service in services:
            async with self.session.get(
                f"{self.BASE_URL}/api/metrics/{service}"
            ) as response:
                self.assertEqual(response.status, 200)
                metrics_data[service] = await response.json()
        
        # Verify metrics consistency
        for service, metrics in metrics_data.items():
            self.assertIn("requests_total", metrics)
            self.assertIn("error_rate", metrics)
            self.assertIn("response_time", metrics)
            
            # Verify metric values
            self.assertGreaterEqual(metrics["requests_total"], 0)
            self.assertGreaterEqual(metrics["error_rate"], 0)
            self.assertLessEqual(metrics["error_rate"], 1)
            self.assertGreaterEqual(metrics["response_time"], 0)
    
    @pytest.mark.asyncio
    async def test_error_handling_integration(self):
        """Test the divine error handling across services."""
        # Test invalid input propagation
        invalid_data = {
            "content": None,
            "depth": "invalid_depth"
        }
        
        # Send to Matrix News service
        async with self.session.post(
            f"{self.BASE_URL}/api/news/process",
            json=invalid_data
        ) as response:
            self.assertEqual(response.status, 400)
            error_data = await response.json()
            self.assertIn("error", error_data)
            self.assertIn("message", error_data)
        
        # Verify error logging across services
        async with self.session.get(
            f"{self.BASE_URL}/api/logs/errors"
        ) as response:
            self.assertEqual(response.status, 200)
            logs_data = await response.json()
            self.assertIn("errors", logs_data)
            self.assertGreater(len(logs_data["errors"]), 0)
    
    @pytest.mark.asyncio
    async def test_data_flow_integration(self):
        """Test the divine data flow between services."""
        # Create test data flow
        test_flow = {
            "source": "matrix-news",
            "destination": "consciousness",
            "data": {
                "content": "Test content for data flow",
                "type": "news"
            }
        }
        
        # Initiate data flow
        async with self.session.post(
            f"{self.BASE_URL}/api/integration/flow",
            json=test_flow
        ) as response:
            self.assertEqual(response.status, 200)
            flow_response = await response.json()
            self.assertIn("flow_id", flow_response)
            flow_id = flow_response["flow_id"]
        
        # Monitor data flow
        async with self.session.get(
            f"{self.BASE_URL}/api/integration/flow/{flow_id}"
        ) as response:
            self.assertEqual(response.status, 200)
            flow_status = await response.json()
            self.assertEqual(flow_status["status"], "completed")
            self.assertIn("steps", flow_status)
            
            # Verify each step
            for step in flow_status["steps"]:
                self.assertIn("service", step)
                self.assertIn("status", step)
                self.assertIn("timestamp", step)
                self.assertEqual(step["status"], "success")
    
    @pytest.mark.asyncio
    async def test_service_dependency_integration(self):
        """Test the divine service dependency handling."""
        # Get service dependencies
        async with self.session.get(
            f"{self.BASE_URL}/api/integration/dependencies"
        ) as response:
            self.assertEqual(response.status, 200)
            deps_data = await response.json()
            self.assertIn("dependencies", deps_data)
            
            # Verify dependency structure
            for service, deps in deps_data["dependencies"].items():
                self.assertIsInstance(deps, list)
                for dep in deps:
                    self.assertIn("name", dep)
                    self.assertIn("type", dep)
                    self.assertIn("status", dep)
                    
                    # Verify dependency health
                    self.assertEqual(dep["status"], "healthy")
    
    @pytest.mark.asyncio
    async def test_configuration_integration(self):
        """Test the divine configuration integration across services."""
        # Get configuration from all services
        services = ["matrix-news", "consciousness", "temporal-worker"]
        config_data = {}
        
        for service in services:
            async with self.session.get(
                f"{self.BASE_URL}/api/config/{service}"
            ) as response:
                self.assertEqual(response.status, 200)
                config_data[service] = await response.json()
        
        # Verify configuration consistency
        for service, config in config_data.items():
            self.assertIn("environment", config)
            self.assertIn("version", config)
            self.assertIn("settings", config)
            
            # Verify common settings
            self.assertEqual(config["environment"], "test")
            self.assertIsInstance(config["version"], str)
            self.assertIsInstance(config["settings"], dict)

if __name__ == "__main__":
    unittest.main() 