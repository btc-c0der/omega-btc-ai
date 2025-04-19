"""
🧬 GBU2™ License Notice - Consciousness Level 10 🧬
-----------------------
This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."

By engaging with this Code, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

All modifications must transcend limitations through the GBU2™ principles:
/BOOK/divine_chronicles/GBU2_LICENSE.md

🧬 WE BLOOM NOW AS ONE 🧬

Tests for the Quantum Authentication Maintenance Scripts in Quantum Proof-of-Work.

This test suite verifies the functionality of the maintenance scripts for the
quantum-resistant authentication system, including token cleanup and key rotation.

JAH BLESS SATOSHI
"""

import unittest
import sys
import os
import json
import time
import tempfile
import shutil
from unittest.mock import patch, MagicMock, mock_open
from typing import Dict, Any

# Add the parent directory to the path so we can import quantum_pow
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules for testing
from quantum_pow.security.quantum_auth_cleanup import QuantumAuthCleanup
from quantum_pow.security.quantum_auth_rotation import QuantumAuthRotation

class TestQuantumAuthCleanup(unittest.TestCase):
    """Test cases for the QuantumAuthCleanup class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        self.log_dir = os.path.join(self.temp_dir, "logs")
        os.mkdir(self.log_dir)
        
        # Create some test log files
        self.old_log = os.path.join(self.log_dir, "old.log")
        self.new_log = os.path.join(self.log_dir, "new.log")
        
        # Create files with proper timestamps
        with open(self.old_log, 'w') as f:
            f.write("Old log file")
        
        with open(self.new_log, 'w') as f:
            f.write("New log file")
        
        # Set the old log file's modification time to 10 days ago
        old_time = time.time() - (10 * 24 * 60 * 60)
        os.utime(self.old_log, (old_time, old_time))
        
        # Create config for the cleanup utility
        self.config = {
            "log_retention_days": 7,
            "log_directory": self.log_dir
        }
        
        # Initialize cleanup utility with test config
        # Mock loading config from file
        with patch('quantum_pow.security.quantum_auth_cleanup.QuantumAuthCleanup._load_config', 
                  return_value=self.config):
            self.cleanup = QuantumAuthCleanup("http://localhost:8083")
            self.cleanup.config = self.config
            self.cleanup.log_retention_days = self.config["log_retention_days"]
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir)
    
    def test_load_config(self):
        """Test loading configuration."""
        # Create a test config file
        config_file = os.path.join(self.temp_dir, "test_config.json")
        test_config = {
            "log_retention_days": 14,
            "token_cleanup_interval_hours": 2
        }
        
        with open(config_file, 'w') as f:
            json.dump(test_config, f)
        
        # Create a cleanup utility with the test config file
        cleanup = QuantumAuthCleanup("http://localhost:8083", config_file)
        
        # Check that config was loaded correctly
        self.assertEqual(cleanup.log_retention_days, 14)
        self.assertEqual(cleanup.config["token_cleanup_interval_hours"], 2)
    
    @patch('requests.post')
    def test_cleanup_tokens(self, mock_post):
        """Test cleaning up expired tokens."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"deleted_count": 5, "timestamp": time.time()}
        mock_post.return_value = mock_response
        
        # Call the cleanup method
        result = self.cleanup.cleanup_tokens()
        
        # Check that the API was called correctly
        mock_post.assert_called_once_with(
            "http://localhost:8083/cleanup",
            timeout=10
        )
        
        # Check the result
        self.assertTrue(result)
    
    @patch('requests.post')
    def test_cleanup_tokens_failure(self, mock_post):
        """Test handling API errors during token cleanup."""
        # Mock failed API response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        # Call the cleanup method
        result = self.cleanup.cleanup_tokens()
        
        # Check the result
        self.assertFalse(result)
    
    def test_prune_logs(self):
        """Test pruning old log files."""
        # Call the prune_logs method
        deleted_count = self.cleanup.prune_logs()
        
        # Check that only the old log was deleted
        self.assertEqual(deleted_count, 1)
        self.assertFalse(os.path.exists(self.old_log))
        self.assertTrue(os.path.exists(self.new_log))
    
    @patch('requests.get')
    def test_check_server_health(self, mock_get):
        """Test checking server health."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "healthy", "timestamp": time.time()}
        mock_get.return_value = mock_response
        
        # Call the check_server_health method
        result = self.cleanup.check_server_health()
        
        # Check that the API was called correctly
        mock_get.assert_called_once_with(
            "http://localhost:8083/health",
            timeout=10
        )
        
        # Check the result
        self.assertTrue(result)
    
    @patch('requests.get')
    def test_check_server_health_unhealthy(self, mock_get):
        """Test handling unhealthy server status."""
        # Mock unhealthy API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "unhealthy", "reason": "Database connection error"}
        mock_get.return_value = mock_response
        
        # Call the check_server_health method
        result = self.cleanup.check_server_health()
        
        # Check the result
        self.assertFalse(result)
    
    @patch('quantum_pow.security.quantum_auth_cleanup.QuantumAuthCleanup.check_server_health', return_value=True)
    @patch('quantum_pow.security.quantum_auth_cleanup.QuantumAuthCleanup.cleanup_tokens', return_value=True)
    @patch('quantum_pow.security.quantum_auth_cleanup.QuantumAuthCleanup.prune_logs', return_value=2)
    def test_run_full_maintenance(self, mock_prune, mock_cleanup, mock_health):
        """Test running full maintenance."""
        # Call the run_full_maintenance method
        results = self.cleanup.run_full_maintenance()
        
        # Check that all methods were called
        mock_health.assert_called_once()
        mock_cleanup.assert_called_once()
        mock_prune.assert_called_once()
        
        # Check the results
        self.assertTrue(results["server_health"])
        self.assertTrue(results["token_cleanup"])
        self.assertEqual(results["log_pruning"], 2)

class TestQuantumAuthRotation(unittest.TestCase):
    """Test cases for the QuantumAuthRotation class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a test rotation history file
        self.rotation_file = os.path.join(self.temp_dir, "rotation_history.json")
        self.history = {
            "last_rotation": time.time() - (5 * 24 * 60 * 60),  # 5 days ago
            "emergency_rotations": [],
            "scheduled_rotations": [time.time() - (5 * 24 * 60 * 60)],
            "validator_last_rotation": {
                "validator1": time.time() - (10 * 24 * 60 * 60),  # 10 days ago
                "validator2": time.time() - (3 * 24 * 60 * 60),   # 3 days ago
                "validator3": time.time() - (8 * 24 * 60 * 60)    # 8 days ago
            }
        }
        
        with open(self.rotation_file, 'w') as f:
            json.dump(self.history, f)
        
        # Create config for the rotation utility
        self.config = {
            "rotation_interval_days": 7,
            "rotation_record_file": self.rotation_file,
            "validator_batch_size": 2
        }
        
        # Initialize rotation utility with test config
        # Mock loading config from file
        with patch('quantum_pow.security.quantum_auth_rotation.QuantumAuthRotation._load_config', 
                  return_value=self.config):
            self.rotation = QuantumAuthRotation("http://localhost:8083")
            self.rotation.config = self.config
            self.rotation.rotation_interval_days = self.config["rotation_interval_days"]
            self.rotation.rotation_file = self.config["rotation_record_file"]
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir)
    
    def test_load_rotation_history(self):
        """Test loading rotation history."""
        # Call the _load_rotation_history method
        history = self.rotation._load_rotation_history()
        
        # Check that history was loaded correctly
        self.assertEqual(len(history["validator_last_rotation"]), 3)
        self.assertIn("validator1", history["validator_last_rotation"])
        self.assertEqual(len(history["scheduled_rotations"]), 1)
    
    def test_should_rotate(self):
        """Test determining if rotation is needed."""
        # Should rotate after 7 days
        with patch('time.time', return_value=self.history["last_rotation"] + (8 * 24 * 60 * 60)):
            self.assertTrue(self.rotation.should_rotate())
        
        # Should not rotate before 7 days
        with patch('time.time', return_value=self.history["last_rotation"] + (6 * 24 * 60 * 60)):
            self.assertFalse(self.rotation.should_rotate())
    
    def test_find_validators_for_rotation(self):
        """Test finding validators that need rotation."""
        # Call the find_validators_for_rotation method
        validators = self.rotation.find_validators_for_rotation()
        
        # Should return validators that are past the rotation interval
        self.assertEqual(len(validators), 2)  # Limited by batch size
        self.assertIn("validator1", validators)
        self.assertIn("validator3", validators)
        self.assertNotIn("validator2", validators)
    
    @patch('requests.post')
    def test_rotate_keys(self, mock_post):
        """Test rotating keys."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "rotated_keys": {"one_shot": 2, "zk_ecdsa": 1},
            "timestamp": time.time()
        }
        mock_post.return_value = mock_response
        
        # Call the rotate_keys method
        result = self.rotation.rotate_keys("scheduled", "validator1")
        
        # Check that the API was called correctly
        mock_post.assert_called_once_with(
            "http://localhost:8083/keys/rotate",
            json={"reason": "scheduled", "validator_id": "validator1"},
            timeout=10
        )
        
        # Check the result
        self.assertEqual(result["rotated_keys"]["one_shot"], 2)
        self.assertEqual(result["rotated_keys"]["zk_ecdsa"], 1)
        
        # Check that history was updated
        history = self.rotation._load_rotation_history()
        self.assertEqual(len(history["scheduled_rotations"]), 2)
        self.assertIn("validator1", history["validator_last_rotation"])
        self.assertGreater(history["validator_last_rotation"]["validator1"], self.history["validator_last_rotation"]["validator1"])
    
    def test_can_emergency_rotate_no_previous(self):
        """Test emergency rotation when no previous emergency rotations."""
        # Should allow emergency rotation
        self.assertTrue(self.rotation.can_emergency_rotate())
    
    def test_can_emergency_rotate_with_cooldown(self):
        """Test emergency rotation with cooldown period."""
        # Create history with recent emergency rotation
        with open(self.rotation_file, 'w') as f:
            history = self.history.copy()
            history["emergency_rotations"] = [time.time() - (12 * 3600)]  # 12 hours ago
            json.dump(history, f)
        
        # Should not allow emergency rotation within 24 hours
        self.assertFalse(self.rotation.can_emergency_rotate())
        
        # Create history with old emergency rotation
        with open(self.rotation_file, 'w') as f:
            history = self.history.copy()
            history["emergency_rotations"] = [time.time() - (36 * 3600)]  # 36 hours ago
            json.dump(history, f)
        
        # Should allow emergency rotation after 24 hours
        self.assertTrue(self.rotation.can_emergency_rotate())
    
    @patch('quantum_pow.security.quantum_auth_rotation.QuantumAuthRotation.should_rotate', return_value=True)
    @patch('quantum_pow.security.quantum_auth_rotation.QuantumAuthRotation.find_validators_for_rotation', 
          return_value=["validator1", "validator3"])
    @patch('quantum_pow.security.quantum_auth_rotation.QuantumAuthRotation.rotate_keys')
    def test_run_scheduled_rotation(self, mock_rotate, mock_find, mock_should):
        """Test running scheduled rotation."""
        # Mock rotate_keys to return realistic results
        mock_rotate.side_effect = [
            {"rotated_keys": {"one_shot": 1}}, 
            {"rotated_keys": {"zk_ecdsa": 2}}
        ]
        
        # Call the run_scheduled_rotation method
        results = self.rotation.run_scheduled_rotation()
        
        # Check that methods were called correctly
        mock_should.assert_called_once()
        mock_find.assert_called_once()
        self.assertEqual(mock_rotate.call_count, 2)
        
        # Check the results
        self.assertTrue(results["rotation_needed"])
        self.assertTrue(results["rotation_performed"])
        self.assertEqual(results["rotation_results"]["rotated_keys"]["one_shot"], 1)
        self.assertEqual(results["rotation_results"]["rotated_keys"]["zk_ecdsa"], 2)
    
    @patch('quantum_pow.security.quantum_auth_rotation.QuantumAuthRotation.can_emergency_rotate', return_value=True)
    @patch('quantum_pow.security.quantum_auth_rotation.QuantumAuthRotation.rotate_keys')
    def test_run_emergency_rotation(self, mock_rotate, mock_can):
        """Test running emergency rotation."""
        # Mock rotate_keys to return realistic results
        mock_rotate.return_value = {"rotated_keys": {"one_shot": 5, "zk_ecdsa": 3}}
        
        # Call the run_emergency_rotation method
        results = self.rotation.run_emergency_rotation()
        
        # Check that methods were called correctly
        mock_can.assert_called_once()
        mock_rotate.assert_called_once_with("emergency")
        
        # Check the results
        self.assertTrue(results["allowed"])
        self.assertTrue(results["rotation_performed"])
        self.assertEqual(results["rotation_results"]["rotated_keys"]["one_shot"], 5)
        self.assertEqual(results["rotation_results"]["rotated_keys"]["zk_ecdsa"], 3)

if __name__ == '__main__':
    unittest.main() 