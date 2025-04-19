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

"""
Tests for Denarius-inspired features in the qPoW system.

These tests verify the functionality of components inspired by the Denarius cryptocurrency:
1. TribusQuantumResistantHash - Quantum-resistant version of Denarius's Tribus algorithm
2. HybridConsensus - Implementation of hybrid PoW/PoS approach with quantum security
3. FortunaStakes - Quantum-resistant version of Denarius's hybrid masternode concept
"""
import os
import sys
import time
import unittest
import tempfile
import hashlib
from unittest.mock import MagicMock, patch

# Import the features we want to test
from quantum_pow.hash_functions import (
    QuantumResistantHash,
    TribusQuantumResistantHash,
    QuantumResistantHashFactory
)
from quantum_pow.block_structure import (
    HybridConsensus,
    get_target_timespan,
    bits_to_target
)
from quantum_pow.ecosystem import FortunaStakes


class TestTribusQuantumResistantHash(unittest.TestCase):
    """Tests for the TribusQuantumResistantHash class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data = b"Denarius Tribus Test Data"
        self.tribus_hash = TribusQuantumResistantHash()
    
    def test_hash_output_length(self):
        """Test that the hash output is 64 bytes (512 bits)."""
        hash_output = self.tribus_hash.hash(self.test_data)
        self.assertEqual(len(hash_output), 64)
    
    def test_hash_determinism(self):
        """Test that the hash function produces the same output for the same input."""
        hash1 = self.tribus_hash.hash(self.test_data)
        hash2 = self.tribus_hash.hash(self.test_data)
        self.assertEqual(hash1, hash2)
    
    def test_hash_uniqueness(self):
        """Test that different inputs produce different hashes."""
        hash1 = self.tribus_hash.hash(self.test_data)
        hash2 = self.tribus_hash.hash(self.test_data + b"extra")
        self.assertNotEqual(hash1, hash2)
    
    def test_verify_method(self):
        """Test the verify method correctly verifies a hash."""
        hash_value = self.tribus_hash.hash(self.test_data)
        self.assertTrue(self.tribus_hash.verify(self.test_data, hash_value))
        self.assertFalse(self.tribus_hash.verify(self.test_data, b"\x00" * 64))
    
    def test_avalanche_effect(self):
        """Test that small changes in input result in significant changes in output."""
        hash1 = self.tribus_hash.hash(self.test_data)
        
        # Change a single bit in the input
        modified_data = bytearray(self.test_data)
        modified_data[0] = modified_data[0] ^ 1  # Flip the least significant bit
        hash2 = self.tribus_hash.hash(bytes(modified_data))
        
        # Count differing bits
        diff_bits = 0
        for a, b in zip(hash1, hash2):
            diff_bits += bin(a ^ b).count('1')
        
        # The avalanche effect should cause roughly ~50% of output bits to change
        # Allow some deviation but ensure significant change
        self.assertGreaterEqual(diff_bits, 128)  # At least 25% of bits changed
    
    def test_factory_creation(self):
        """Test creating the hash via factory."""
        hash_instance = QuantumResistantHashFactory.create("tribus")
        self.assertIsInstance(hash_instance, TribusQuantumResistantHash)


class TestHybridConsensus(unittest.TestCase):
    """Tests for the HybridConsensus class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.consensus = HybridConsensus()
    
    def test_initialization(self):
        """Test that the consensus mechanism initializes correctly."""
        self.assertEqual(self.consensus.pow_difficulty_bits, 24)
        self.assertEqual(self.consensus.pos_difficulty_modifier, 4)
        self.assertEqual(self.consensus.target_block_time, 30)
        self.assertEqual(self.consensus.stake_min_age, 8 * 60 * 60)  # 8 hours
    
    def test_custom_initialization(self):
        """Test initialization with custom parameters."""
        custom = HybridConsensus(pow_difficulty_bits=26, pos_difficulty_modifier=6, stake_min_age=12*60*60)
        self.assertEqual(custom.pow_difficulty_bits, 26)
        self.assertEqual(custom.pos_difficulty_modifier, 6)
        self.assertEqual(custom.stake_min_age, 12 * 60 * 60)
    
    def test_is_valid_stake_with_insufficient_age(self):
        """Test that stake validation rejects stakes with insufficient age."""
        insufficient_age = self.consensus.stake_min_age - 1
        stake_modifier = 12345
        target = 2**240
        
        self.assertFalse(self.consensus.is_valid_stake(insufficient_age, stake_modifier, target))
    
    def test_is_valid_stake_with_sufficient_age(self):
        """Test that stake validation accepts stakes with sufficient age."""
        sufficient_age = self.consensus.stake_min_age + 1
        stake_modifier = 12345
        target = 2**256 - 1  # A very easy target that should always be met
        
        self.assertTrue(self.consensus.is_valid_stake(sufficient_age, stake_modifier, target))
    
    def test_adjust_difficulty(self):
        """Test that difficulty adjustment works correctly."""
        blocks = [{"nonce": i} for i in range(10)]
        timestamps = [1000 * i for i in range(10)]
        
        # For PoW
        pow_difficulty = self.consensus.adjust_difficulty(blocks, timestamps, is_pos=False)
        self.assertEqual(pow_difficulty, self.consensus.pow_difficulty_bits)
        
        # For PoS
        pos_difficulty = self.consensus.adjust_difficulty(blocks, timestamps, is_pos=True)
        self.assertEqual(pos_difficulty, self.consensus.pow_difficulty_bits - self.consensus.pos_difficulty_modifier)
    
    def test_target_timespan(self):
        """Test that the target timespan matches Denarius's 30 seconds."""
        self.assertEqual(get_target_timespan(), 30)
    
    def test_get_pos_target(self):
        """Test getting the PoS target based on PoW target."""
        # Test that the function returns the correct difficulty bits
        pow_bits = 0x1d00ffff
        pos_bits = self.consensus.get_pos_target(pow_bits)
        
        # The PoS difficulty bits should be lower (which means easier mining)
        self.assertEqual(pos_bits, self.consensus.pow_difficulty_bits - self.consensus.pos_difficulty_modifier)
        
        # Confirm that PoS bits are 4 bits lower (as defined by the default pos_difficulty_modifier)
        self.assertEqual(pos_bits, self.consensus.pow_difficulty_bits - 4)
        
        # Create a custom consensus with different modifier
        custom_consensus = HybridConsensus(pow_difficulty_bits=26, pos_difficulty_modifier=6)
        custom_pos_bits = custom_consensus.get_pos_target(pow_bits)
        
        # Verify the custom consensus also behaves correctly
        self.assertEqual(custom_pos_bits, 20)  # 26 - 6 = 20


class TestFortunaStakes(unittest.TestCase):
    """Tests for the FortunaStakes class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_network = MagicMock()
        self.fortuna = FortunaStakes(self.mock_network)
        
        # Standard test data
        self.test_address = "QRAddressXYZ123456789"
        self.test_txid = "txid1234567890abcdef"
        self.test_signature = "quantum_sig_test"
    
    def test_initialization(self):
        """Test that Fortuna Stakes initializes correctly."""
        self.assertEqual(self.fortuna.required_collateral, 5000)
        self.assertEqual(self.fortuna.reward_percentage, 33)
        self.assertEqual(self.fortuna.active_stakes, {})
    
    def test_custom_initialization(self):
        """Test initialization with custom parameters."""
        custom = FortunaStakes(self.mock_network, required_collateral=10000, reward_percentage=40)
        self.assertEqual(custom.required_collateral, 10000)
        self.assertEqual(custom.reward_percentage, 40)
    
    def test_register_stake(self):
        """Test registering a new stake."""
        result = self.fortuna.register_stake(
            self.test_address,
            self.test_txid,
            self.test_signature
        )
        
        self.assertTrue(result)
        self.assertEqual(len(self.fortuna.active_stakes), 1)
        
        # Get the stake ID
        stake_id = list(self.fortuna.active_stakes.keys())[0]
        
        # Verify stake data
        stake_info = self.fortuna.active_stakes[stake_id]
        self.assertEqual(stake_info['owner'], self.test_address)
        self.assertEqual(stake_info['collateral'], self.test_txid)
        self.assertIsInstance(stake_info['registered_at'], int)
        self.assertEqual(stake_info['last_reward'], 0)
        
        # Verify signature storage
        self.assertEqual(self.fortuna.stake_signatures[stake_id], self.test_signature)
    
    def test_generate_stake_id(self):
        """Test that stake ID generation is consistent."""
        stake_id1 = self.fortuna._generate_stake_id(self.test_address, self.test_txid)
        stake_id2 = self.fortuna._generate_stake_id(self.test_address, self.test_txid)
        self.assertEqual(stake_id1, stake_id2)
        
        # Different inputs should give different IDs
        different_id = self.fortuna._generate_stake_id(self.test_address, "different_txid")
        self.assertNotEqual(stake_id1, different_id)
    
    def test_calculate_reward(self):
        """Test reward calculation."""
        block_reward = 10.0
        expected_reward = (block_reward * self.fortuna.reward_percentage) // 100
        actual_reward = self.fortuna.calculate_reward(block_reward)
        
        self.assertEqual(actual_reward, expected_reward)
    
    def test_distribute_rewards_no_stakes(self):
        """Test reward distribution with no active stakes."""
        distributions = self.fortuna.distribute_rewards(12345, 10.0)
        self.assertEqual(distributions, {})
    
    def test_distribute_rewards_with_stakes(self):
        """Test reward distribution with active stakes."""
        # Register two stakes
        self.fortuna.register_stake("address1", "txid1", "sig1")
        self.fortuna.register_stake("address2", "txid2", "sig2")
        
        # Get the stake IDs
        stake_ids = list(self.fortuna.active_stakes.keys())
        
        # Distribute rewards
        block_reward = 10.0
        distributions = self.fortuna.distribute_rewards(12345, block_reward)
        
        # Expected total stake reward
        stake_reward = self.fortuna.calculate_reward(block_reward)
        expected_per_stake = stake_reward // 2  # Split between 2 stakes
        
        # Verify distributions
        self.assertEqual(len(distributions), 2)
        for stake_id in stake_ids:
            self.assertIn(stake_id, distributions)
            self.assertEqual(distributions[stake_id], expected_per_stake)
            
            # Verify last_reward was updated
            self.assertEqual(self.fortuna.active_stakes[stake_id]['last_reward'], 12345)
    
    def test_get_eligible_stakes(self):
        """Test getting eligible stakes for reward."""
        # Register some stakes
        self.fortuna.register_stake("address1", "txid1", "sig1")
        self.fortuna.register_stake("address2", "txid2", "sig2")
        
        # Get eligible stakes
        eligible = self.fortuna._get_eligible_stakes(12345)
        
        # All stakes should be eligible in our implementation
        self.assertEqual(len(eligible), 2)
        for stake_id in self.fortuna.active_stakes:
            self.assertIn(stake_id, eligible)


if __name__ == '__main__':
    unittest.main() 