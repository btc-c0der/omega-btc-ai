"""
Tests for the OmegaPRM mining algorithm.

This module tests the OmegaPRM (Process-supervised Reward Model with Monte Carlo Tree Search)
implementation for quantum-resistant blockchain mining.
"""

import os
import sys
import time
import unittest
import hashlib
from unittest.mock import MagicMock, patch

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quantum_pow.omega_prm import (
    MCTSNode, 
    OmegaPRMRewardModel, 
    OmegaPRMMiner, 
    mine_with_omega_prm
)
from quantum_pow.block_structure import QuantumBlock, BlockHeader, Transaction, bits_to_target, meets_target


class TestMCTSNode(unittest.TestCase):
    """Test the Monte Carlo Tree Search Node implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.initial_state = {
            'version': 1,
            'prev_block_hash': bytes([0] * 64),
            'merkle_root': bytes([0] * 64),
            'timestamp': int(time.time()),
            'bits': 0x1f00ffff,
            'nonce': 0
        }
        self.root = MCTSNode(state=self.initial_state)
    
    def test_initialization(self):
        """Test that node initializes with correct attributes."""
        self.assertEqual(self.root.state, self.initial_state)
        self.assertIsNone(self.root.parent)
        self.assertIsNone(self.root.action)
        self.assertEqual(self.root.visits, 0)
        self.assertEqual(self.root.reward, 0.0)
        self.assertGreater(len(self.root.untried_actions), 0)
    
    def test_expansion(self):
        """Test node expansion."""
        child = self.root.expand()
        self.assertIsNotNone(child)
        self.assertEqual(child.parent, self.root)
        self.assertIsNotNone(child.action)
        self.assertIn(child, self.root.children)
        self.assertEqual(len(self.root.children), 1)
        
        # Check that untried_actions was reduced
        self.assertEqual(len(self.root.untried_actions), len(self.root._get_untried_actions()) - 1)
    
    def test_update(self):
        """Test node statistics update."""
        self.root.update(1.5)
        self.assertEqual(self.root.visits, 1)
        self.assertEqual(self.root.reward, 1.5)
        
        self.root.update(2.5)
        self.assertEqual(self.root.visits, 2)
        self.assertEqual(self.root.reward, 4.0)
    
    def test_select_child(self):
        """Test child selection with UCB1."""
        # Create children with known statistics
        child1 = MCTSNode(state={'nonce': 1}, parent=self.root, action={'type': 'test1'})
        child1.visits = 10
        child1.reward = 8.0
        
        child2 = MCTSNode(state={'nonce': 2}, parent=self.root, action={'type': 'test2'})
        child2.visits = 5
        child2.reward = 6.0
        
        self.root.children = [child1, child2]
        self.root.visits = 15
        
        # Child2 should be selected (higher UCB value due to exploration term)
        selected = self.root.select_child(exploration_weight=1.0)
        self.assertEqual(selected, child2)
        
        # With lower exploration weight, child1 should be selected (higher reward)
        selected = self.root.select_child(exploration_weight=0.1)
        self.assertEqual(selected, child1)
    
    def test_best_child(self):
        """Test best child selection based on reward."""
        # Create children with known statistics
        child1 = MCTSNode(state={'nonce': 1}, parent=self.root, action={'type': 'test1'})
        child1.visits = 10
        child1.reward = 8.0
        
        child2 = MCTSNode(state={'nonce': 2}, parent=self.root, action={'type': 'test2'})
        child2.visits = 5
        child2.reward = 15.0  # Higher total reward
        
        self.root.children = [child1, child2]
        
        # Child2 should be selected (higher total reward)
        best = self.root.best_child()
        self.assertEqual(best, child2)
    
    def test_is_fully_expanded(self):
        """Test checking if node is fully expanded."""
        self.assertFalse(self.root.is_fully_expanded())
        
        # Expand all untried actions
        untried_count = len(self.root.untried_actions)
        for _ in range(untried_count):
            self.root.expand()
            
        self.assertTrue(self.root.is_fully_expanded())


class TestOmegaPRMRewardModel(unittest.TestCase):
    """Test the OmegaPRM reward model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.target_bits = 0x1f00ffff  # Easy difficulty for testing
        self.reward_model = OmegaPRMRewardModel(self.target_bits)
    
    def test_initialization(self):
        """Test that reward model initializes correctly."""
        self.assertEqual(self.reward_model.target_bits, self.target_bits)
        self.assertIsNotNone(self.reward_model.target)
        self.assertIsNotNone(self.reward_model.hash_function)
    
    def test_evaluate_meeting_target(self):
        """Test reward for hash meeting target."""
        # Create a mock header that produces a hash meeting the target
        header = MagicMock()
        header.hash.return_value = bytes([0] * 64)  # Very low hash value
        
        # This should meet any reasonable target
        reward = self.reward_model.evaluate(header)
        self.assertEqual(reward, 100.0)  # Solution reward
    
    def test_evaluate_not_meeting_target(self):
        """Test reward for hash not meeting target."""
        # Create a mock header that produces a hash not meeting the target
        header = MagicMock()
        header.hash.return_value = bytes([255] * 64)  # Very high hash value
        
        # Should get partial reward based on proximity
        reward = self.reward_model.evaluate(header)
        self.assertLess(reward, 100.0)  # Less than solution reward
        self.assertGreaterEqual(reward, 0.0)  # Non-negative reward
    
    def test_evaluate_subproblem_nonce_search(self):
        """Test evaluation of nonce search subproblem."""
        # Create a subproblem
        subproblem = {
            'type': 'nonce_search',
            'description': 'Find valid nonce'
        }
        
        # Create a state
        state = {
            'version': 1,
            'prev_block_hash': bytes([0] * 64),
            'merkle_root': bytes([0] * 64),
            'timestamp': int(time.time()),
            'bits': self.target_bits,
            'nonce': 0
        }
        
        # Evaluate
        reward = self.reward_model.evaluate_subproblem(subproblem, state)
        self.assertGreaterEqual(reward, 0.0)
    
    def test_evaluate_subproblem_transaction_selection(self):
        """Test evaluation of transaction selection subproblem."""
        # Create a subproblem
        subproblem = {
            'type': 'transaction_selection',
            'description': 'Select transactions for block'
        }
        
        # Create a state
        state = {'selected_tx_ids': [1, 2, 3]}
        
        # Evaluate
        reward = self.reward_model.evaluate_subproblem(subproblem, state)
        self.assertEqual(reward, 5.0)  # Fixed reward for this type
    
    def test_unknown_subproblem(self):
        """Test evaluation of unknown subproblem type."""
        # Create a subproblem
        subproblem = {
            'type': 'unknown',
            'description': 'Unknown type'
        }
        
        # Create a state
        state = {}
        
        # Evaluate
        reward = self.reward_model.evaluate_subproblem(subproblem, state)
        self.assertEqual(reward, 0.0)  # Default reward


class TestOmegaPRMMiner(unittest.TestCase):
    """Test the OmegaPRM miner."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a block with easy difficulty for testing
        self.header = BlockHeader(
            version=1,
            prev_block_hash=bytes([0] * 64),
            merkle_root=bytes([0] * 64),
            timestamp=int(time.time()),
            bits=0x1f00ffff,  # Very easy difficulty
            nonce=0
        )
        self.block = QuantumBlock(header=self.header)
        
        # Create a miner with limited iterations/time for testing
        self.miner = OmegaPRMMiner(max_iterations=100, time_limit=1.0)
    
    def test_initialization(self):
        """Test that miner initializes correctly."""
        self.assertEqual(self.miner.max_iterations, 100)
        self.assertEqual(self.miner.time_limit, 1.0)
        self.assertEqual(self.miner.exploration_weight, 1.414)
    
    def test_decompose_mining_problem(self):
        """Test problem decomposition."""
        subproblems = self.miner._decompose_mining_problem(self.block)
        self.assertGreaterEqual(len(subproblems), 1)
        
        # Check that there's a nonce search subproblem
        self.assertTrue(any(sp['type'] == 'nonce_search' for sp in subproblems))
    
    def test_simulation(self):
        """Test simulation function."""
        # Create a subproblem
        subproblem = {
            'type': 'nonce_search',
            'description': 'Find valid nonce'
        }
        
        # Create a state
        state = {
            'version': 1,
            'prev_block_hash': bytes([0] * 64),
            'merkle_root': bytes([0] * 64),
            'timestamp': int(time.time()),
            'bits': 0x1f00ffff,
            'nonce': 0
        }
        
        # Create a reward model
        reward_model = OmegaPRMRewardModel(0x1f00ffff)
        
        # Run simulation
        result = self.miner._simulate(subproblem, state, reward_model)
        
        # Check result structure
        self.assertIn('success', result)
        self.assertIn('reward', result)
        self.assertIsInstance(result['success'], bool)
        self.assertIsInstance(result['reward'], (int, float))
    
    def test_mcts_search(self):
        """Test MCTS search function."""
        # Create a subproblem
        subproblem = {
            'type': 'nonce_search',
            'description': 'Find valid nonce'
        }
        
        # Create a state
        state = {
            'version': 1,
            'prev_block_hash': bytes([0] * 64),
            'merkle_root': bytes([0] * 64),
            'timestamp': int(time.time()),
            'bits': 0x1f00ffff,
            'nonce': 0
        }
        
        # Create a reward model
        reward_model = OmegaPRMRewardModel(0x1f00ffff)
        
        # Run MCTS search
        start_time = time.time()
        result = self.miner._mcts_search(subproblem, state, reward_model, start_time)
        
        # Check result structure
        self.assertIn('success', result)
        self.assertIn('iterations', result)
        self.assertIn('reward', result)
        self.assertIn('nonce', result)
        self.assertIn('time_taken', result)
        
        # Check types
        self.assertIsInstance(result['success'], bool)
        self.assertIsInstance(result['iterations'], int)
        self.assertIsInstance(result['reward'], (int, float))
        self.assertIsInstance(result['nonce'], int)
        self.assertIsInstance(result['time_taken'], (int, float))
    
    @patch('quantum_pow.block_structure.meets_target')
    def test_mine_block_success(self, mock_meets_target):
        """Test successful mining."""
        # Mock meets_target to always return True after a few calls
        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            # Return True after 5 calls
            return call_count >= 5
        
        mock_meets_target.side_effect = side_effect
        
        # Mine the block
        result = self.miner.mine_block(self.block)
        
        # Check result
        self.assertTrue(result)
        self.assertGreaterEqual(mock_meets_target.call_count, 5)
    
    @patch('quantum_pow.block_structure.meets_target')
    def test_mine_block_failure(self, mock_meets_target):
        """Test failed mining."""
        # Mock meets_target to always return False
        mock_meets_target.return_value = False
        
        # Mine the block
        result = self.miner.mine_block(self.block)
        
        # Check result
        self.assertFalse(result)
        self.assertGreater(mock_meets_target.call_count, 0)


class TestClientAPI(unittest.TestCase):
    """Test the client-friendly API."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a block with easy difficulty for testing
        self.header = BlockHeader(
            version=1,
            prev_block_hash=bytes([0] * 64),
            merkle_root=bytes([0] * 64),
            timestamp=int(time.time()),
            bits=0x1f00ffff,  # Very easy difficulty
            nonce=0
        )
        self.block = QuantumBlock(header=self.header)
    
    @patch('quantum_pow.omega_prm.OmegaPRMMiner.mine_block')
    def test_mine_with_omega_prm(self, mock_mine_block):
        """Test the convenience function."""
        # Mock the mine_block method
        mock_mine_block.return_value = True
        
        # Mine the block
        result = mine_with_omega_prm(self.block, time_limit=2.0, max_iterations=100)
        
        # Check result
        self.assertTrue(result)
        self.assertEqual(mock_mine_block.call_count, 1)
        
        # Check that miner was created with correct parameters
        _, kwargs = mock_mine_block.call_args
        self.assertEqual(kwargs, {})  # No kwargs expected


class TestIntegration(unittest.TestCase):
    """Integration tests for the OmegaPRM mining."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a block with easy difficulty for testing
        self.header = BlockHeader(
            version=1,
            prev_block_hash=bytes([0] * 64),
            merkle_root=bytes([0] * 64),
            timestamp=int(time.time()),
            bits=0x1f00ffff,  # Very easy difficulty for tests
            nonce=0
        )
        self.block = QuantumBlock(header=self.header)
    
    def test_end_to_end_mining(self):
        """Test the entire mining process."""
        # Mine the block with very limited resources to keep test quick
        result = mine_with_omega_prm(self.block, time_limit=0.5, max_iterations=50)
        
        # For very easy difficulty, it should succeed
        # If not, the difficulty might need to be adjusted for testing
        self.assertTrue(result, "Mining failed - consider reducing difficulty for testing")
        
        # Verify that the block hash meets the target
        block_hash = self.block.header.hash()
        target = bits_to_target(self.block.header.bits)
        self.assertTrue(meets_target(block_hash, target))
        
        # Check that nonce was updated
        self.assertNotEqual(self.block.header.nonce, 0)
    
    def test_comparative_performance(self):
        """Compare OmegaPRM to naive mining."""
        # Skip for regular testing - only run this for benchmarking
        self.skipTest("Performance test - run manually for benchmarking")
        
        # Create two identical blocks
        header1 = BlockHeader(
            version=1,
            prev_block_hash=bytes([0] * 64),
            merkle_root=bytes([0] * 64),
            timestamp=int(time.time()),
            bits=0x1f00ffff,  # Moderate difficulty
            nonce=0
        )
        block1 = QuantumBlock(header=header1)
        
        header2 = BlockHeader(
            version=1,
            prev_block_hash=bytes([0] * 64),
            merkle_root=bytes([0] * 64),
            timestamp=int(time.time()),
            bits=0x1f00ffff,  # Same difficulty
            nonce=0
        )
        block2 = QuantumBlock(header=header2)
        
        # Time OmegaPRM mining
        start_time = time.time()
        omega_result = mine_with_omega_prm(block1, time_limit=5.0)
        omega_time = time.time() - start_time
        
        # Time naive mining
        start_time = time.time()
        naive_result = self._naive_mine(block2, max_attempts=100000)
        naive_time = time.time() - start_time
        
        print(f"\nOmegaPRM: {omega_time:.4f}s, success={omega_result}")
        print(f"Naive: {naive_time:.4f}s, success={naive_result}")
        
        # Compare results - not making assertions about speed
        # as it depends on hardware and test conditions
        self.assertEqual(omega_result, naive_result, 
                         "Both methods should either both succeed or both fail")
    
    def _naive_mine(self, block, max_attempts=100000):
        """Naive mining approach for comparison."""
        target = bits_to_target(block.header.bits)
        
        for nonce in range(max_attempts):
            block.header.nonce = nonce
            hash_result = block.header.hash()
            
            if meets_target(hash_result, target):
                return True
                
        return False


if __name__ == '__main__':
    unittest.main() 