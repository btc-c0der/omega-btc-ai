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

Tests for the Validator Privacy module in Quantum Proof-of-Work.

This test suite verifies the functionality of the validator privacy system
that protects validators in the qPoW network from being identified through
metadata analysis attacks.

JAH BLESS SATOSHI
"""

import unittest
import sys
import os
import json
import tempfile
import time
import threading
from unittest.mock import patch, MagicMock, Mock
from typing import Dict, Any, List

# Add the parent directory to the path so we can import quantum_pow
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules for testing
from quantum_pow.security.validator_privacy import (
    PrivacyThreatLevel,
    ValidatorMetadata,
    DandelionRouting,
    ValidatorPrivacyManager
)

class TestValidatorMetadata(unittest.TestCase):
    """Test cases for the ValidatorMetadata class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator_id = "validator1"
        self.node_id = "node1"
        self.metadata = ValidatorMetadata(
            validator_id=self.validator_id,
            node_id=self.node_id,
            ip_address="192.168.1.1"
        )
    
    def test_metadata_initialization(self):
        """Test that ValidatorMetadata initializes with the correct attributes."""
        self.assertEqual(self.metadata.validator_id, self.validator_id)
        self.assertEqual(self.metadata.node_id, self.node_id)
        self.assertEqual(self.metadata.ip_address, "192.168.1.1")
        self.assertIsInstance(self.metadata.attestation_pattern, list)
        self.assertIsInstance(self.metadata.message_sizes, list)
        self.assertIsInstance(self.metadata.block_proposal_times, list)
        self.assertIsInstance(self.metadata.subnet_activities, dict)
    
    def test_add_attestation(self):
        """Test adding attestation events."""
        # Add attestations and check they're recorded
        self.metadata.add_attestation(1000.0, 100)
        self.metadata.add_attestation(1010.0, 120)
        
        self.assertEqual(len(self.metadata.attestation_pattern), 2)
        self.assertEqual(self.metadata.attestation_pattern[0], 1000.0)
        self.assertEqual(self.metadata.attestation_pattern[1], 1010.0)
        self.assertEqual(self.metadata.message_sizes[0], 100)
        self.assertEqual(self.metadata.message_sizes[1], 120)
        self.assertEqual(self.metadata.last_attestation_time, 1010.0)
    
    def test_add_block_proposal(self):
        """Test adding block proposal events."""
        # Add block proposals and check they're recorded
        self.metadata.add_block_proposal(2000.0)
        self.metadata.add_block_proposal(2100.0)
        
        self.assertEqual(len(self.metadata.block_proposal_times), 2)
        self.assertEqual(self.metadata.block_proposal_times[0], 2000.0)
        self.assertEqual(self.metadata.block_proposal_times[1], 2100.0)
    
    def test_record_subnet_activity(self):
        """Test recording subnet activity."""
        # Record activities on different subnets
        self.metadata.record_subnet_activity("subnet1", 3000.0)
        self.metadata.record_subnet_activity("subnet1", 3010.0)
        self.metadata.record_subnet_activity("subnet2", 3020.0)
        
        self.assertEqual(len(self.metadata.subnet_activities), 2)
        self.assertEqual(len(self.metadata.subnet_activities["subnet1"]), 2)
        self.assertEqual(len(self.metadata.subnet_activities["subnet2"]), 1)
        self.assertEqual(self.metadata.subnet_activities["subnet1"][0], 3000.0)
        self.assertEqual(self.metadata.subnet_activities["subnet2"][0], 3020.0)
    
    def test_attestation_frequency(self):
        """Test calculation of attestation frequency."""
        # No attestations should return 0
        self.assertEqual(self.metadata.get_attestation_frequency(), 0.0)
        
        # Add attestations with known intervals
        self.metadata.add_attestation(1000.0, 100)
        self.metadata.add_attestation(1010.0, 120)
        self.metadata.add_attestation(1025.0, 110)
        
        # Average interval should be 12.5 ((10 + 15) / 2)
        self.assertAlmostEqual(self.metadata.get_attestation_frequency(), 12.5)
    
    def test_message_size_variance(self):
        """Test calculation of message size variance."""
        # No messages should return 0
        self.assertEqual(self.metadata.get_message_size_variance(), 0.0)
        
        # Add messages with known sizes
        self.metadata.add_attestation(1000.0, 100)
        self.metadata.add_attestation(1010.0, 100)
        
        # Variance should be 0 since both messages are the same size
        self.assertEqual(self.metadata.get_message_size_variance(), 0.0)
        
        # Add another message with a different size
        self.metadata.add_attestation(1020.0, 130)
        
        # Variance should be non-zero now
        self.assertGreater(self.metadata.get_message_size_variance(), 0.0)
    
    def test_list_size_limits(self):
        """Test that lists are limited to maximum sizes."""
        # Test attestation list limit (100)
        for i in range(110):
            self.metadata.add_attestation(1000.0 + i, 100)
        
        self.assertEqual(len(self.metadata.attestation_pattern), 100)
        self.assertEqual(len(self.metadata.message_sizes), 100)
        
        # Test block proposal list limit (20)
        for i in range(25):
            self.metadata.add_block_proposal(2000.0 + i)
        
        self.assertEqual(len(self.metadata.block_proposal_times), 20)
        
        # Test subnet activity list limit (50)
        for i in range(60):
            self.metadata.record_subnet_activity("subnet1", 3000.0 + i)
        
        self.assertEqual(len(self.metadata.subnet_activities["subnet1"]), 50)

class TestDandelionRouting(unittest.TestCase):
    """Test cases for the DandelionRouting class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.node_id = "node1"
        self.peers = ["node2", "node3", "node4"]
        self.dandelion = DandelionRouting(stem_probability=0.8, max_stem_length=5)
    
    def test_initialization(self):
        """Test initialization with peers."""
        self.dandelion.initialize(self.node_id, self.peers)
        
        self.assertEqual(self.dandelion.node_id, self.node_id)
        self.assertEqual(self.dandelion.peers, self.peers)
        self.assertIn(self.node_id, self.dandelion.stem_peers)
        self.assertIn(self.dandelion.stem_peers[self.node_id], self.peers)
    
    def test_update_peers(self):
        """Test updating the peer list."""
        self.dandelion.initialize(self.node_id, self.peers)
        
        # Update peers
        new_peers = ["node5", "node6"]
        self.dandelion.update_peers(new_peers)
        
        self.assertEqual(self.dandelion.peers, new_peers)
        self.assertIn(self.node_id, self.dandelion.stem_peers)
        self.assertIn(self.dandelion.stem_peers[self.node_id], new_peers)
    
    def test_stem_phase_routing(self):
        """Test routing in stem phase."""
        self.dandelion.initialize(self.node_id, self.peers)
        
        # Force stem phase by patching random.random to return a value less than stem_probability
        with patch('random.random', return_value=0.5):  # 0.5 < 0.8
            next_hop, message, is_fluff = self.dandelion.route_message("test_message")
            
            self.assertFalse(is_fluff)
            self.assertEqual(next_hop, self.dandelion.stem_peers[self.node_id])
            self.assertEqual(message, "test_message")
    
    def test_fluff_phase_by_probability(self):
        """Test transition to fluff phase based on probability."""
        self.dandelion.initialize(self.node_id, self.peers)
        
        # Force fluff phase by patching random.random to return a value greater than stem_probability
        with patch('random.random', return_value=0.9):  # 0.9 > 0.8
            next_hop, message, is_fluff = self.dandelion.route_message("test_message")
            
            self.assertTrue(is_fluff)
            self.assertEqual(next_hop, "broadcast")
            self.assertEqual(message, "test_message")
    
    def test_fluff_phase_by_length(self):
        """Test transition to fluff phase based on stem length."""
        self.dandelion.initialize(self.node_id, self.peers)
        
        # Force stem phase for probability check
        with patch('random.random', return_value=0.5):
            # But exceed max stem length
            next_hop, message, is_fluff = self.dandelion.route_message("test_message", stem_length=6)
            
            self.assertTrue(is_fluff)
            self.assertEqual(next_hop, "broadcast")
            self.assertEqual(message, "test_message")
    
    def test_no_peers_routing(self):
        """Test routing behavior with no peers."""
        # Initialize with empty peer list
        self.dandelion.initialize(self.node_id, [])
        
        next_hop, message, is_fluff = self.dandelion.route_message("test_message")
        
        self.assertTrue(is_fluff)
        self.assertEqual(next_hop, "")
        self.assertEqual(message, "test_message")

class TestValidatorPrivacyManager(unittest.TestCase):
    """Test cases for the ValidatorPrivacyManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.node_id = "node1"
        self.validator_id = "validator1"
        
        # Create a temporary config file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_config.json")
        
        # Create a basic config for testing
        config = {
            "privacy_mode": "enhanced",
            "trusted_proxies": ["proxy1", "proxy2"],
            "randomize_timing": True,
            "message_padding": True
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
        
        # Create manager with the test config
        self.manager = ValidatorPrivacyManager(self.node_id, self.config_file)
    
    def tearDown(self):
        """Clean up after tests."""
        # Stop the manager if it's running
        if self.manager.is_running:
            self.manager.stop()
        
        # Remove temporary directory
        os.unlink(self.config_file)
        os.rmdir(self.temp_dir)
    
    def test_initialization(self):
        """Test initialization and configuration loading."""
        self.assertEqual(self.manager.node_id, self.node_id)
        self.assertEqual(self.manager.config["privacy_mode"], "enhanced")
        self.assertEqual(len(self.manager.trusted_proxies), 2)
        self.assertIn("proxy1", self.manager.trusted_proxies)
        self.assertTrue(self.manager.config["randomize_timing"])
        self.assertTrue(self.manager.config["message_padding"])
    
    def test_default_config(self):
        """Test loading default configuration when no file is provided."""
        manager = ValidatorPrivacyManager("node2")
        
        self.assertEqual(manager.config["privacy_mode"], "standard")
        self.assertEqual(manager.trusted_proxies, [])
        self.assertTrue(manager.config["randomize_timing"])
        self.assertTrue(manager.config["message_padding"])
        self.assertEqual(manager.config["dandelion"]["stem_probability"], 0.9)
    
    def test_start_stop(self):
        """Test starting and stopping the manager."""
        # Manager should not be running initially
        self.assertFalse(self.manager.is_running)
        
        # Start the manager
        self.manager.start()
        self.assertTrue(self.manager.is_running)
        self.assertIsNotNone(self.manager.router_thread)
        self.assertTrue(self.manager.router_thread.is_alive())
        
        # Stop the manager
        self.manager.stop()
        self.assertFalse(self.manager.is_running)
        # Allow some time for the thread to stop
        time.sleep(0.1)
        self.assertFalse(self.manager.router_thread.is_alive())
    
    def test_validator_registration(self):
        """Test registering validators."""
        # Register a validator
        self.manager.register_validator(self.validator_id, "192.168.1.1")
        
        # Check it was registered correctly
        self.assertIn(self.validator_id, self.manager.validators)
        self.assertEqual(self.manager.validators[self.validator_id].ip_address, "192.168.1.1")
        self.assertIn("192.168.1.1", self.manager.ip_to_node)
        self.assertIn(self.validator_id, self.manager.ip_to_node["192.168.1.1"])
        
        # Register another validator with the same IP
        self.manager.register_validator("validator2", "192.168.1.1")
        
        # Check both validators are mapped to the same IP
        self.assertEqual(len(self.manager.ip_to_node["192.168.1.1"]), 2)
        
        # Update the IP of the first validator
        self.manager.register_validator(self.validator_id, "192.168.1.2")
        
        # Check the mappings were updated
        self.assertEqual(self.manager.validators[self.validator_id].ip_address, "192.168.1.2")
        self.assertEqual(len(self.manager.ip_to_node["192.168.1.1"]), 1)
        self.assertIn("192.168.1.2", self.manager.ip_to_node)
        self.assertIn(self.validator_id, self.manager.ip_to_node["192.168.1.2"])
    
    def test_validator_unregistration(self):
        """Test unregistering validators."""
        # Register validators
        self.manager.register_validator(self.validator_id, "192.168.1.1")
        self.manager.register_validator("validator2", "192.168.1.1")
        
        # Unregister one validator
        self.manager.unregister_validator(self.validator_id)
        
        # Check it was unregistered correctly
        self.assertNotIn(self.validator_id, self.manager.validators)
        self.assertNotIn(self.validator_id, self.manager.ip_to_node["192.168.1.1"])
        self.assertEqual(len(self.manager.ip_to_node["192.168.1.1"]), 1)
        
        # Unregister the last validator with that IP
        self.manager.unregister_validator("validator2")
        
        # The IP mapping should be removed
        self.assertNotIn("192.168.1.1", self.manager.ip_to_node)
    
    @patch('time.sleep')  # Mock sleep to speed up tests
    def test_attestation_processing(self, mock_sleep):
        """Test processing attestations with privacy enhancements."""
        self.manager.start()
        
        # Register a validator
        self.manager.register_validator(self.validator_id, "192.168.1.1")
        
        # Mock the dandelion routing
        self.manager.dandelion.route_message = MagicMock(return_value=("node2", {"message": b"padded_data"}, False))
        
        # Submit an attestation
        self.manager.submit_attestation(self.validator_id, {"message": b"test_attestation", "slot": 1234})
        
        # Allow time for processing
        time.sleep(0.1)  # This won't actually sleep due to the mock
        
        # Check that routing was called
        self.manager.dandelion.route_message.assert_called_once()
        
        # Check that metadata was updated
        self.assertIn(self.validator_id, self.manager.validators)
        metadata = self.manager.validators[self.validator_id]
        self.assertEqual(len(metadata.attestation_pattern), 1)
        self.assertGreater(len(metadata.message_sizes), 0)
    
    @patch('random.choice', return_value="proxy1")  # Mock random.choice for proxy selection
    def test_block_proposal_processing(self, mock_choice):
        """Test processing block proposals with proxy routing."""
        self.manager.start()
        
        # Register a validator
        self.manager.register_validator(self.validator_id, "192.168.1.1")
        
        # Submit a block proposal
        self.manager.submit_block_proposal(self.validator_id, {"block": b"test_block", "slot": 1234})
        
        # Allow time for processing
        time.sleep(0.1)
        
        # Check that proxy selection was called
        mock_choice.assert_called_once_with(self.manager.trusted_proxies)
        
        # Check that metadata was updated
        metadata = self.manager.validators[self.validator_id]
        self.assertEqual(len(metadata.block_proposal_times), 1)
    
    def test_privacy_risk_analysis(self):
        """Test analyzing privacy risks for validators."""
        # Register validators
        self.manager.register_validator(self.validator_id, "192.168.1.1")
        self.manager.register_validator("validator2", "192.168.1.1")  # Same IP
        self.manager.register_validator("validator3", "192.168.1.2")  # Different IP
        
        # Add some activity for the first validator
        metadata = self.manager.validators[self.validator_id]
        
        # Add regular attestations - higher privacy risk
        for i in range(10):
            metadata.add_attestation(1000.0 + i * 10, 100)  # Very regular intervals, same size
        
        # Add block proposals
        metadata.add_block_proposal(1500.0)
        
        # Analyze risks
        risks = self.manager.analyze_privacy_risks()
        
        # Check overall structure
        self.assertIn(self.validator_id, risks)
        self.assertIn("validator2", risks)
        self.assertIn("validator3", risks)
        
        # Check risk factors for first validator
        v1_risks = risks[self.validator_id]
        self.assertIn("risk_factors", v1_risks)
        self.assertIn("overall_risk", v1_risks)
        self.assertIn("threat_level", v1_risks)
        self.assertIn("recommendations", v1_risks)
        
        # Regular attestation pattern should have high risk
        self.assertGreater(v1_risks["risk_factors"]["attestation_pattern_regularity"], 0.5)
        
        # Same message size should have high risk
        self.assertGreater(v1_risks["risk_factors"]["message_size_uniqueness"], 0.5)
        
        # Shared IP should have lower risk
        self.assertLess(v1_risks["risk_factors"]["ip_address_exposure"], 1.0)
        
        # Single-validator IP should have high risk
        v3_risks = risks["validator3"]
        self.assertEqual(v3_risks["risk_factors"]["ip_address_exposure"], 1.0)
        
        # Check recommendations
        self.assertIsInstance(v1_risks["recommendations"], list)
        
    def test_peer_updates(self):
        """Test updating peers."""
        self.manager.start()
        
        # Mock the dandelion routing
        self.manager.dandelion.update_peers = MagicMock()
        
        # Update peers
        peers = ["node2", "node3", "node4"]
        self.manager.update_peers(peers)
        
        # Allow time for processing
        time.sleep(0.1)
        
        # Check that update_peers was called
        self.manager.dandelion.update_peers.assert_called_once_with(peers)

if __name__ == '__main__':
    unittest.main() 