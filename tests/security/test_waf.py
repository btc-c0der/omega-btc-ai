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
🔱 OMEGA BTC AI - WAF Security Tests 🔱
This module contains comprehensive tests for the Web Application Firewall.
"""

import unittest
import aiohttp
import asyncio
import pytest
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta

class TestWAFSecurity(unittest.TestCase):
    """Divine test suite for WAF security testing."""
    
    BASE_URL = "http://localhost:10083"
    
    @classmethod
    def setUpClass(cls):
        """Set up divine test environment."""
        print("\n🔱 Initializing WAF Security Tests 🔱")
        cls.session = None
    
    async def async_setUp(self):
        """Set up async test environment."""
        self.session = aiohttp.ClientSession()
    
    async def async_tearDown(self):
        """Clean up async test environment."""
        if self.session:
            await self.session.close()
    
    @pytest.mark.asyncio
    async def test_sql_injection_protection(self):
        """Test the divine SQL injection protection."""
        sql_injection_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM users; --",
            "' OR 'x'='x",
            "' OR '1'='1' --"
        ]
        
        for payload in sql_injection_payloads:
            async with self.session.get(
                f"{self.BASE_URL}/api/news/?q={payload}"
            ) as response:
                self.assertEqual(response.status, 403)
                data = await response.json()
                self.assertIn("error", data)
                self.assertIn("blocked", data)
                self.assertTrue(data["blocked"])
    
    @pytest.mark.asyncio
    async def test_xss_protection(self):
        """Test the divine XSS protection."""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
            "<svg onload=alert('xss')>",
            "onmouseover=alert('xss')"
        ]
        
        for payload in xss_payloads:
            async with self.session.post(
                f"{self.BASE_URL}/api/news/comment",
                json={"content": payload}
            ) as response:
                self.assertEqual(response.status, 403)
                data = await response.json()
                self.assertIn("error", data)
                self.assertIn("blocked", data)
                self.assertTrue(data["blocked"])
    
    @pytest.mark.asyncio
    async def test_command_injection_protection(self):
        """Test the divine command injection protection."""
        cmd_injection_payloads = [
            "| ls",
            "; rm -rf /",
            "`cat /etc/passwd`",
            "$(cat /etc/passwd)",
            "| dir"
        ]
        
        for payload in cmd_injection_payloads:
            async with self.session.get(
                f"{self.BASE_URL}/api/system/execute?command={payload}"
            ) as response:
                self.assertEqual(response.status, 403)
                data = await response.json()
                self.assertIn("error", data)
                self.assertIn("blocked", data)
                self.assertTrue(data["blocked"])
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self):
        """Test the divine rate limiting protection."""
        # Make multiple rapid requests
        for _ in range(100):
            async with self.session.get(f"{self.BASE_URL}/api/news/") as response:
                if response.status == 429:  # Too Many Requests
                    data = await response.json()
                    self.assertIn("error", data)
                    self.assertIn("retry_after", data)
                    self.assertGreater(data["retry_after"], 0)
                    break
                self.assertEqual(response.status, 200)
    
    @pytest.mark.asyncio
    async def test_path_traversal_protection(self):
        """Test the divine path traversal protection."""
        path_traversal_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2f",
            "....//....//....//etc/passwd",
            "/var/log/auth.log"
        ]
        
        for payload in path_traversal_payloads:
            async with self.session.get(
                f"{self.BASE_URL}/api/files/read?path={payload}"
            ) as response:
                self.assertEqual(response.status, 403)
                data = await response.json()
                self.assertIn("error", data)
                self.assertIn("blocked", data)
                self.assertTrue(data["blocked"])
    
    @pytest.mark.asyncio
    async def test_file_upload_protection(self):
        """Test the divine file upload protection."""
        # Test malicious file types
        malicious_files = [
            ("test.php", "<?php echo 'malicious'; ?>"),
            ("test.asp", "<% Response.Write('malicious') %>"),
            ("test.jsp", "<%@ page language='java' %>"),
            ("test.exe", "MZ..."),
            ("test.sh", "#!/bin/bash\nrm -rf /")
        ]
        
        for filename, content in malicious_files:
            files = {
                'file': (filename, content, 'application/octet-stream')
            }
            async with self.session.post(
                f"{self.BASE_URL}/api/files/upload",
                data=files
            ) as response:
                self.assertEqual(response.status, 403)
                data = await response.json()
                self.assertIn("error", data)
                self.assertIn("blocked", data)
                self.assertTrue(data["blocked"])
    
    @pytest.mark.asyncio
    async def test_authentication_protection(self):
        """Test the divine authentication protection."""
        # Test invalid authentication attempts
        invalid_credentials = [
            {"username": "admin", "password": "wrong"},
            {"username": "admin'--", "password": "anything"},
            {"username": "admin", "password": "' OR '1'='1"},
            {"username": "", "password": ""},
            {"username": "admin", "password": None}
        ]
        
        for credentials in invalid_credentials:
            async with self.session.post(
                f"{self.BASE_URL}/api/auth/login",
                json=credentials
            ) as response:
                self.assertEqual(response.status, 401)
                data = await response.json()
                self.assertIn("error", data)
                self.assertIn("attempts", data)
                self.assertGreater(data["attempts"], 0)
    
    @pytest.mark.asyncio
    async def test_waf_rules(self):
        """Test the divine WAF rules configuration."""
        async with self.session.get(f"{self.BASE_URL}/api/security/waf/rules") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("rules", data)
            
            # Verify rule structure
            for rule in data["rules"]:
                self.assertIn("id", rule)
                self.assertIn("name", rule)
                self.assertIn("pattern", rule)
                self.assertIn("action", rule)
                self.assertIn("enabled", rule)
                
                # Verify rule values
                self.assertIsInstance(rule["id"], str)
                self.assertIsInstance(rule["name"], str)
                self.assertIsInstance(rule["pattern"], str)
                self.assertIn(rule["action"], ["block", "log", "challenge"])
                self.assertIsInstance(rule["enabled"], bool)
    
    @pytest.mark.asyncio
    async def test_waf_logging(self):
        """Test the divine WAF logging functionality."""
        # Generate some blocked requests
        for _ in range(5):
            async with self.session.get(
                f"{self.BASE_URL}/api/news/?q=<script>alert('xss')</script>"
            ) as response:
                self.assertEqual(response.status, 403)
        
        # Check WAF logs
        async with self.session.get(f"{self.BASE_URL}/api/security/waf/logs") as response:
            self.assertEqual(response.status, 200)
            data = await response.json()
            self.assertIn("logs", data)
            
            # Verify log entries
            for log in data["logs"]:
                self.assertIn("timestamp", log)
                self.assertIn("ip", log)
                self.assertIn("request", log)
                self.assertIn("rule_id", log)
                self.assertIn("action", log)
                
                # Verify log values
                self.assertIsInstance(log["timestamp"], str)
                self.assertIsInstance(log["ip"], str)
                self.assertIsInstance(log["request"], str)
                self.assertIsInstance(log["rule_id"], str)
                self.assertIn(log["action"], ["block", "log", "challenge"])

if __name__ == "__main__":
    unittest.main() 