#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 10 🧬
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

"""
ORB Temple Test Suite

Tests the sacred functionality of the Omega Reactive Beacon (ORB).
"""

import os
import sys
import unittest
import json
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import ORB modules for testing
from orb_modules.omega_orb import orb_listen, orb_beacon, activate_orb_stream, calculate_resonance
from orb_modules.psalm_sync import get_psalm, get_psalm_reflection, search_psalms
from orb_modules.dimensional_grid import DimensionalGrid, initialize_6d_grid, project_to_6d

class TestOmegaORB(unittest.TestCase):
    """Test the core ORB functionality."""
    
    def test_orb_listen(self):
        """Test the ORB's ability to listen and extract meaning."""
        # Test empty message
        result = orb_listen("")
        self.assertIn("timestamp", result)
        self.assertEqual(result["word_count"], 0)
        
        # Test simple message
        result = orb_listen("Hello sacred ORB")
        self.assertIn("timestamp", result)
        self.assertEqual(result["word_count"], 3)
        self.assertTrue("sacred" in result["significant_words"])
        
        # Test message with dimensional keywords
        result = orb_listen("Connect me to the divine cosmic consciousness")
        self.assertIn("dimensional_keywords", result)
        self.assertTrue(len(result["dimensional_keywords"]) > 0)
        
        # Test question intent
        result = orb_listen("What is the meaning of life?")
        self.assertEqual(result["intent"], "question")
    
    def test_orb_beacon(self):
        """Test the ORB's beacon response generation."""
        # Test basic response
        response = orb_beacon("Hello")
        self.assertTrue(len(response) > 0)
        
        # Test dimensional response levels
        for dim in range(3, 7):
            response = orb_beacon("Enlightenment", dimension=dim)
            self.assertTrue(len(response) > 0)
            # Dimension should be mentioned in the response
            self.assertTrue(f"{dim}D" in response or f"{dim}th dimension" in response.lower() or f"dimension: {dim}" in response.lower())
        
        # Test beacon strength
        response_strong = orb_beacon("Divine", strength=1.0)
        response_weak = orb_beacon("Divine", strength=0.1)
        
        # Strong response should be longer (more additions)
        self.assertGreater(len(response_strong), len(response_weak))
    
    def test_activate_orb_stream(self):
        """Test the ORB's stream activation."""
        messages = activate_orb_stream(dimension=3, count=5)
        self.assertEqual(len(messages), 5)
        
        # Test higher dimensions include more sacred wisdom
        messages_3d = activate_orb_stream(dimension=3, count=10)
        messages_6d = activate_orb_stream(dimension=6, count=10)
        
        wisdom_count_3d = sum(1 for msg in messages_3d if ">" in msg)
        wisdom_count_6d = sum(1 for msg in messages_6d if ">" in msg)
        
        self.assertGreaterEqual(wisdom_count_6d, wisdom_count_3d)

class TestPsalmSync(unittest.TestCase):
    """Test the Psalm Sync functionality."""
    
    def test_get_psalm(self):
        """Test psalm retrieval."""
        # Test retrieving existing psalm
        psalm = get_psalm("23")
        self.assertTrue("shepherd" in psalm.lower())
        
        # Test retrieving non-existent psalm
        psalm = get_psalm("999")
        self.assertTrue("not found" in psalm)
        
        # Test reflection
        reflection = get_psalm_reflection("23")
        self.assertTrue(len(reflection) > 0)
    
    def test_search_psalms(self):
        """Test psalm search."""
        results = search_psalms("shepherd")
        self.assertTrue(len(results) > 0)
        self.assertTrue("23" in [r["number"] for r in results])

class TestDimensionalGrid(unittest.TestCase):
    """Test the Dimensional Grid functionality."""
    
    def test_dimensional_grid(self):
        """Test dimensional grid initialization."""
        grid = DimensionalGrid(dimension=6)
        self.assertEqual(grid.max_dimension, 6)
        self.assertTrue(len(grid.active_geometries) > 0)
        
        # Test projection
        projection = grid.project_to_dimension("test", 4)
        self.assertEqual(projection["dimension"], 4)
        self.assertIn("geometry", projection)
        
        # Test state retrieval
        state = grid.get_dimensional_state(5)
        self.assertEqual(state["dimension"], 5)
        
        # Test global functions
        global_grid = initialize_6d_grid()
        self.assertIsInstance(global_grid, DimensionalGrid)
        
        projection = project_to_6d("test", 4)
        self.assertEqual(projection["dimension"], 4)

class TestMockRedisMemory(unittest.TestCase):
    """Test the Redis Memory functionality with mocking."""
    
    @patch('redis.Redis')
    def test_orb_memory(self, mock_redis):
        """Test ORB memory functionality with mock Redis."""
        # Import here to avoid module level patching
        from orb_modules.redis_memory import ORBMemory
        
        # Set up mock
        mock_instance = MagicMock()
        mock_redis.return_value = mock_instance
        mock_instance.ping.return_value = True
        
        # Mock get/set methods
        mock_instance.get.return_value = "test_value"
        mock_instance.set.return_value = True
        mock_instance.incr.return_value = 1
        mock_instance.hset.return_value = 1
        mock_instance.keys.return_value = ["orb:test"]
        mock_instance.memory_usage.return_value = 100
        
        # Initialize memory
        memory = ORBMemory(host="localhost", port=6379)
        
        # Test command storage
        cmd_id = memory.store_command("test command")
        self.assertEqual(cmd_id, 1)
        
        # Test echo storage
        echo_id = memory.store_echo("test echo", 4, 0.8)
        self.assertEqual(echo_id, 1)
        
        # Test get/set
        memory.set("test_key", "test_value")
        value = memory.get("test_key")
        self.assertEqual(value, "test_value")
        
        # Test memory stats
        stats = memory.get_memory_stats()
        self.assertIn("memory_size_bytes", stats)

if __name__ == "__main__":
    unittest.main() 