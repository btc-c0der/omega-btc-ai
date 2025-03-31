#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔱 OMEGA BTC AI - Redis State Management Tests 🔱
This module contains comprehensive tests for the Redis state management.
"""

import unittest
import aiohttp
import asyncio
import pytest
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta

class TestRedisStateManagement(unittest.TestCase):
    """Divine test suite for the Redis state management."""
    
    BASE_URL = "http://localhost:10083"
    
    @classmethod
    def setUpClass(cls):
        """Set up divine test environment."""
        print("\n🔱 Initializing Redis State Management Tests 🔱")
        cls.session = None
    
    async def async_setUp(self):
        """Set up async test environment."""
        self.session = aiohttp.ClientSession()
    
    async def async_tearDown(self):
        """Clean up async test environment."""
        if self.session:
            await self.session.close()
    
    @pytest.mark.asyncio
    async def test_redis_connection(self):
        """Test the divine Redis connection."""
        async with self.session.get(f"{self.BASE_URL}/api/state/health") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("status", data)
            self.assertEqual(data["status"], "connected")
            self.assertIn("info", data)
    
    @pytest.mark.asyncio
    async def test_state_storage(self):
        """Test the divine state storage operations."""
        test_data = {
            "key": "test_key",
            "value": "test_value",
            "timestamp": datetime.now().isoformat()
        }
        
        # Store state
        async with self.session.post(
            f"{self.BASE_URL}/api/state/store",
            json=test_data
        ) as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("status", data)
            self.assertEqual(data["status"], "success")
        
        # Retrieve state
        async with self.session.get(
            f"{self.BASE_URL}/api/state/retrieve/{test_data['key']}"
        ) as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("value", data)
            self.assertEqual(data["value"], test_data["value"])
    
    @pytest.mark.asyncio
    async def test_state_expiration(self):
        """Test the divine state expiration mechanism."""
        test_data = {
            "key": "expire_key",
            "value": "expire_value",
            "ttl": 5  # 5 seconds TTL
        }
        
        # Store state with TTL
        async with self.session.post(
            f"{self.BASE_URL}/api/state/store",
            json=test_data
        ) as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertEqual(data["status"], "success")
        
        # Wait for expiration
        await asyncio.sleep(6)
        
        # Verify expiration
        async with self.session.get(
            f"{self.BASE_URL}/api/state/retrieve/{test_data['key']}"
        ) as response:
            self.assertEqual(response.status, 404)
            data = await response.json()
            self.assertIn("error", data)
    
    @pytest.mark.asyncio
    async def test_state_batch_operations(self):
        """Test the divine batch state operations."""
        test_data = [
            {"key": f"batch_key_{i}", "value": f"batch_value_{i}"}
            for i in range(5)
        ]
        
        # Store batch
        async with self.session.post(
            f"{self.BASE_URL}/api/state/batch/store",
            json={"items": test_data}
        ) as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["count"], len(test_data))
        
        # Retrieve batch
        keys = [item["key"] for item in test_data]
        async with self.session.post(
            f"{self.BASE_URL}/api/state/batch/retrieve",
            json={"keys": keys}
        ) as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertEqual(len(data["values"]), len(test_data))
    
    @pytest.mark.asyncio
    async def test_state_pattern_matching(self):
        """Test the divine pattern matching operations."""
        # Store multiple keys with pattern
        test_data = [
            {"key": f"pattern:test:{i}", "value": f"value_{i}"}
            for i in range(3)
        ]
        
        for item in test_data:
            async with self.session.post(
                f"{self.BASE_URL}/api/state/store",
                json=item
            ) as response:
                self.assertEqual(response.status, 200)
        
        # Match pattern
        async with self.session.get(
            f"{self.BASE_URL}/api/state/match/pattern:test:*"
        ) as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertEqual(len(data["matches"]), len(test_data))
    
    @pytest.mark.asyncio
    async def test_state_snapshot(self):
        """Test the divine state snapshot functionality."""
        # Create snapshot
        async with self.session.post(f"{self.BASE_URL}/api/state/snapshot") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("snapshot_id", data)
            snapshot_id = data["snapshot_id"]
        
        # List snapshots
        async with self.session.get(f"{self.BASE_URL}/api/state/snapshots") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("snapshots", data)
            self.assertGreater(len(data["snapshots"]), 0)
        
        # Restore snapshot
        async with self.session.post(
            f"{self.BASE_URL}/api/state/restore/{snapshot_id}"
        ) as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertEqual(data["status"], "success")
    
    @pytest.mark.asyncio
    async def test_state_cleanup(self):
        """Test the divine state cleanup operations."""
        # Create test data
        test_data = [
            {"key": f"cleanup_key_{i}", "value": f"cleanup_value_{i}"}
            for i in range(5)
        ]
        
        for item in test_data:
            async with self.session.post(
                f"{self.BASE_URL}/api/state/store",
                json=item
            ) as response:
                self.assertEqual(response.status, 200)
        
        # Cleanup by pattern
        async with self.session.delete(
            f"{self.BASE_URL}/api/state/cleanup/cleanup_key_*"
        ) as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["count"], len(test_data))
        
        # Verify cleanup
        for item in test_data:
            async with self.session.get(
                f"{self.BASE_URL}/api/state/retrieve/{item['key']}"
            ) as response:
                self.assertEqual(response.status, 404)
    
    @pytest.mark.asyncio
    async def test_state_validation(self):
        """Test the divine state validation."""
        invalid_data = [
            {"key": "", "value": "test"},  # Empty key
            {"value": "test"},  # Missing key
            {"key": "test", "value": None},  # Invalid value
            {"key": "test" * 100, "value": "test"}  # Key too long
        ]
        
        for item in invalid_data:
            async with self.session.post(
                f"{self.BASE_URL}/api/state/store",
                json=item
            ) as response:
                self.assertEqual(response.status, 400)
                data = await response.json()
                self.assertIn("error", data)

if __name__ == "__main__":
    unittest.main() 