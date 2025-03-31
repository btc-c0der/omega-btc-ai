#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔱 OMEGA BTC AI - Performance Testing 🔱
This module contains comprehensive tests for the system's performance.
"""

import unittest
import aiohttp
import asyncio
import pytest
import json
import time
from typing import Dict, List, Any
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

class TestSystemPerformance(unittest.TestCase):
    """Divine test suite for system performance testing."""
    
    BASE_URL = "http://localhost:10083"
    CONCURRENT_REQUESTS = 50
    REQUEST_TIMEOUT = 30
    
    @classmethod
    def setUpClass(cls):
        """Set up divine test environment."""
        print("\n🔱 Initializing Performance Tests 🔱")
        cls.session = None
        cls.executor = ThreadPoolExecutor(max_workers=cls.CONCURRENT_REQUESTS)
    
    async def async_setUp(self):
        """Set up async test environment."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.REQUEST_TIMEOUT)
        )
    
    async def async_tearDown(self):
        """Clean up async test environment."""
        if self.session:
            await self.session.close()
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test the divine concurrent request handling."""
        start_time = time.time()
        tasks = []
        
        # Create concurrent requests
        for _ in range(self.CONCURRENT_REQUESTS):
            tasks.append(
                self.session.get(f"{self.BASE_URL}/api/health")
            )
        
        # Execute requests concurrently
        responses = await asyncio.gather(*tasks)
        
        # Calculate metrics
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / self.CONCURRENT_REQUESTS
        
        # Verify responses
        success_count = sum(1 for r in responses if r.status == 200)
        self.assertEqual(success_count, self.CONCURRENT_REQUESTS)
        
        # Log performance metrics
        print(f"\nConcurrent Request Metrics:")
        print(f"Total Time: {total_time:.2f}s")
        print(f"Average Time: {avg_time:.2f}s")
        print(f"Requests per Second: {self.CONCURRENT_REQUESTS/total_time:.2f}")
    
    @pytest.mark.asyncio
    async def test_memory_usage(self):
        """Test the divine memory usage under load."""
        # Get initial memory usage
        async with self.session.get(f"{self.BASE_URL}/api/metrics/memory") as response:
            initial_data = await response.json()
            initial_memory = initial_data["memory_usage"]
        
        # Generate load
        tasks = []
        for _ in range(self.CONCURRENT_REQUESTS):
            tasks.append(
                self.session.get(f"{self.BASE_URL}/api/news/")
            )
        await asyncio.gather(*tasks)
        
        # Get final memory usage
        async with self.session.get(f"{self.BASE_URL}/api/metrics/memory") as response:
            final_data = await response.json()
            final_memory = final_data["memory_usage"]
        
        # Calculate memory increase
        memory_increase = final_memory - initial_memory
        
        # Verify memory usage
        self.assertLess(memory_increase, 500 * 1024 * 1024)  # Less than 500MB increase
        
        # Log memory metrics
        print(f"\nMemory Usage Metrics:")
        print(f"Initial Memory: {initial_memory/1024/1024:.2f}MB")
        print(f"Final Memory: {final_memory/1024/1024:.2f}MB")
        print(f"Memory Increase: {memory_increase/1024/1024:.2f}MB")
    
    @pytest.mark.asyncio
    async def test_response_time_distribution(self):
        """Test the divine response time distribution."""
        response_times = []
        
        # Make multiple requests
        for _ in range(100):
            start_time = time.time()
            async with self.session.get(f"{self.BASE_URL}/api/news/") as response:
                await response.json()
            end_time = time.time()
            response_times.append(end_time - start_time)
        
        # Calculate statistics
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        min_time = min(response_times)
        p95_time = sorted(response_times)[int(len(response_times) * 0.95)]
        
        # Verify response times
        self.assertLess(avg_time, 1.0)  # Average less than 1 second
        self.assertLess(p95_time, 2.0)  # 95th percentile less than 2 seconds
        
        # Log timing metrics
        print(f"\nResponse Time Distribution:")
        print(f"Average: {avg_time*1000:.2f}ms")
        print(f"Maximum: {max_time*1000:.2f}ms")
        print(f"Minimum: {min_time*1000:.2f}ms")
        print(f"95th Percentile: {p95_time*1000:.2f}ms")
    
    @pytest.mark.asyncio
    async def test_error_rate_under_load(self):
        """Test the divine error rate under load."""
        error_count = 0
        total_requests = 1000
        
        # Make requests under load
        for _ in range(total_requests):
            try:
                async with self.session.get(f"{self.BASE_URL}/api/news/") as response:
                    if response.status != 200:
                        error_count += 1
            except Exception:
                error_count += 1
        
        # Calculate error rate
        error_rate = error_count / total_requests
        
        # Verify error rate
        self.assertLess(error_rate, 0.01)  # Less than 1% error rate
        
        # Log error metrics
        print(f"\nError Rate Metrics:")
        print(f"Total Requests: {total_requests}")
        print(f"Error Count: {error_count}")
        print(f"Error Rate: {error_rate*100:.2f}%")
    
    @pytest.mark.asyncio
    async def test_connection_pooling(self):
        """Test the divine connection pooling efficiency."""
        start_time = time.time()
        
        # Make multiple requests with connection reuse
        for _ in range(100):
            async with self.session.get(f"{self.BASE_URL}/api/news/") as response:
                await response.json()
        
        # Calculate metrics
        end_time = time.time()
        total_time = end_time - start_time
        
        # Get connection pool stats
        async with self.session.get(f"{self.BASE_URL}/api/metrics/connections") as response:
            pool_stats = await response.json()
        
        # Verify connection pooling
        self.assertGreater(pool_stats["reused_connections"], 0)
        self.assertLess(pool_stats["new_connections"], 100)
        
        # Log connection metrics
        print(f"\nConnection Pooling Metrics:")
        print(f"Total Time: {total_time:.2f}s")
        print(f"Reused Connections: {pool_stats['reused_connections']}")
        print(f"New Connections: {pool_stats['new_connections']}")
    
    @pytest.mark.asyncio
    async def test_resource_utilization(self):
        """Test the divine resource utilization under load."""
        # Start resource monitoring
        async with self.session.post(f"{self.BASE_URL}/api/metrics/monitor/start") as response:
            self.assertEqual(response.status, 200)
        
        # Generate load
        tasks = []
        for _ in range(self.CONCURRENT_REQUESTS):
            tasks.append(
                self.session.get(f"{self.BASE_URL}/api/news/")
            )
        await asyncio.gather(*tasks)
        
        # Get resource metrics
        async with self.session.get(f"{self.BASE_URL}/api/metrics/resources") as response:
            metrics = await response.json()
        
        # Verify resource utilization
        self.assertLess(metrics["cpu_usage"], 80)  # Less than 80% CPU usage
        self.assertLess(metrics["memory_usage"], 80)  # Less than 80% memory usage
        self.assertLess(metrics["disk_io"], 1000)  # Less than 1000 IOPS
        
        # Log resource metrics
        print(f"\nResource Utilization Metrics:")
        print(f"CPU Usage: {metrics['cpu_usage']}%")
        print(f"Memory Usage: {metrics['memory_usage']}%")
        print(f"Disk IO: {metrics['disk_io']} IOPS")
    
    @pytest.mark.asyncio
    async def test_scaling_efficiency(self):
        """Test the divine scaling efficiency."""
        request_counts = [10, 50, 100, 200]
        response_times = []
        
        for count in request_counts:
            start_time = time.time()
            tasks = []
            for _ in range(count):
                tasks.append(
                    self.session.get(f"{self.BASE_URL}/api/news/")
                )
            await asyncio.gather(*tasks)
            end_time = time.time()
            response_times.append(end_time - start_time)
        
        # Calculate scaling efficiency
        scaling_factors = []
        for i in range(1, len(request_counts)):
            time_ratio = response_times[i] / response_times[0]
            request_ratio = request_counts[i] / request_counts[0]
            scaling_factors.append(time_ratio / request_ratio)
        
        # Verify scaling efficiency
        avg_scaling_factor = sum(scaling_factors) / len(scaling_factors)
        self.assertLess(avg_scaling_factor, 1.5)  # Good scaling efficiency
        
        # Log scaling metrics
        print(f"\nScaling Efficiency Metrics:")
        for i, count in enumerate(request_counts):
            print(f"{count} requests: {response_times[i]:.2f}s")
        print(f"Average Scaling Factor: {avg_scaling_factor:.2f}")

if __name__ == "__main__":
    unittest.main() 