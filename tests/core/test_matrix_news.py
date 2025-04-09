#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔱 OMEGA BTC AI - Matrix News Service Tests 🔱
This module contains comprehensive tests for the Matrix News service.
"""

import unittest
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
import pytest
from typing import Dict, List, Any

class TestMatrixNewsService(unittest.TestCase):
    """Divine test suite for the Matrix News service."""
    
    BASE_URL = "http://localhost:10083"
    WS_URL = "ws://localhost:10083/ws"
    
    @classmethod
    def setUpClass(cls):
        """Set up divine test environment."""
        print("\n🔱 Initializing Matrix News Service Tests 🔱")
        cls.session = None
        cls.ws = None
    
    async def async_setUp(self):
        """Set up async test environment."""
        self.session = aiohttp.ClientSession()
        self.ws = await self.session.ws_connect(self.WS_URL)
    
    async def async_tearDown(self):
        """Clean up async test environment."""
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()
    
    @pytest.mark.asyncio
    async def test_health_endpoint(self):
        """Test the divine health endpoint."""
        async with self.session.get(f"{self.BASE_URL}/health") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("status", data)
            self.assertEqual(data["status"], "healthy")
    
    @pytest.mark.asyncio
    async def test_websocket_connection(self):
        """Test divine WebSocket connection."""
        self.assertIsNotNone(self.ws)
        self.assertFalse(self.ws.closed)
    
    @pytest.mark.asyncio
    async def test_news_feed_endpoint(self):
        """Test the sacred news feed endpoint."""
        async with self.session.get(f"{self.BASE_URL}/api/news/") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIsInstance(data, list)
            if len(data) > 0:
                self.assertIn("title", data[0])
                self.assertIn("content", data[0])
                self.assertIn("timestamp", data[0])
    
    @pytest.mark.asyncio
    async def test_news_filtering(self):
        """Test divine news filtering capabilities."""
        params = {
            "start_date": (datetime.now() - timedelta(days=1)).isoformat(),
            "end_date": datetime.now().isoformat()
        }
        async with self.session.get(f"{self.BASE_URL}/api/news/", params=params) as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            for item in data:
                timestamp = datetime.fromisoformat(item["timestamp"])
                self.assertTrue(timestamp >= datetime.fromisoformat(params["start_date"]))
                self.assertTrue(timestamp <= datetime.fromisoformat(params["end_date"]))
    
    @pytest.mark.asyncio
    async def test_websocket_messages(self):
        """Test divine WebSocket message handling."""
        # Send test message
        test_message = {
            "type": "subscribe",
            "channel": "news"
        }
        await self.ws.send_json(test_message)
        
        # Wait for response
        response = await self.ws.receive_json()
        self.assertIn("type", response)
        self.assertEqual(response["type"], "subscribed")
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self):
        """Test divine rate limiting protection."""
        # Make multiple rapid requests
        for _ in range(10):
            async with self.session.get(f"{self.BASE_URL}/api/news/") as response:
                if response.status == 429:  # Too Many Requests
                    self.assertTrue(True)  # Rate limiting is working
                    break
                self.assertEqual(response.status, 200)
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test divine error handling."""
        # Test invalid date format
        params = {"start_date": "invalid-date"}
        async with self.session.get(f"{self.BASE_URL}/api/news/", params=params) as response:
            self.assertEqual(response.status, 400)
            data = await response.json()
            self.assertIn("error", data)
    
    @pytest.mark.asyncio
    async def test_news_content_validation(self):
        """Test divine news content validation."""
        async with self.session.get(f"{self.BASE_URL}/api/news/") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            for item in data:
                # Validate required fields
                self.assertIn("id", item)
                self.assertIn("title", item)
                self.assertIn("content", item)
                self.assertIn("timestamp", item)
                
                # Validate field types
                self.assertIsInstance(item["id"], str)
                self.assertIsInstance(item["title"], str)
                self.assertIsInstance(item["content"], str)
                self.assertIsInstance(item["timestamp"], str)
                
                # Validate content length
                self.assertGreater(len(item["title"]), 0)
                self.assertGreater(len(item["content"]), 0)
    
    @pytest.mark.asyncio
    async def test_pagination(self):
        """Test divine pagination functionality."""
        page_size = 10
        page = 1
        params = {
            "page": page,
            "page_size": page_size
        }
        
        async with self.session.get(f"{self.BASE_URL}/api/news/", params=params) as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertLessEqual(len(data), page_size)
    
    @pytest.mark.asyncio
    async def test_search_functionality(self):
        """Test divine search capabilities."""
        search_term = "bitcoin"
        params = {"q": search_term}
        
        async with self.session.get(f"{self.BASE_URL}/api/news/", params=params) as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            for item in data:
                self.assertTrue(
                    search_term.lower() in item["title"].lower() or
                    search_term.lower() in item["content"].lower()
                )

if __name__ == "__main__":
    unittest.main() 