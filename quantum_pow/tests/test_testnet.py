#!/usr/bin/env python3
"""
Tests for the Quantum Proof-of-Work (qPoW) testnet implementation.

These tests validate the networking capabilities of the qPoW system,
including node discovery, block propagation, and consensus mechanisms.
"""
import os
import sys
import time
import unittest
import tempfile
import threading
import socket
import json
from unittest.mock import MagicMock, patch

# Import the features we want to test
from quantum_pow.network import (
    Node,
    NodeManager,
    BlockPropagation,
    ConsensusManager
)
from quantum_pow.hash_functions import QuantumResistantHash
from quantum_pow.block_structure import (
    BlockHeader,
    Transaction, 
    QuantumBlock,
    HybridConsensus
)


class TestNetworkNode(unittest.TestCase):
    """Tests for the Node class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.node_id = "test_node_1"
        self.host = "127.0.0.1"
        self.port = self._find_available_port()
        self.node = Node(self.node_id, self.host, self.port)
    
    def _find_available_port(self):
        """Find an available port for testing."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]
    
    def tearDown(self):
        """Clean up after tests."""
        if hasattr(self, 'node') and self.node.is_running():
            self.node.stop()
    
    def test_node_initialization(self):
        """Test that the node initializes correctly."""
        self.assertEqual(self.node.node_id, self.node_id)
        self.assertEqual(self.node.host, self.host)
        self.assertEqual(self.node.port, self.port)
        self.assertFalse(self.node.is_running())
    
    def test_node_start_stop(self):
        """Test starting and stopping the node."""
        # Start the node
        self.node.start()
        self.assertTrue(self.node.is_running())
        
        # Stop the node
        self.node.stop()
        self.assertFalse(self.node.is_running())
    
    def test_node_peer_connection(self):
        """Test connecting to a peer node."""
        # Create a mock peer
        peer_node = MagicMock()
        peer_node.host = "127.0.0.1"
        peer_node.port = self._find_available_port()
        
        # Connect to the peer
        result = self.node.connect_to_peer(peer_node.host, peer_node.port)
        
        # Since this is a mock, we just check that the method runs without error
        self.assertIsNotNone(result)
    
    def test_node_message_handling(self):
        """Test that the node can handle incoming messages."""
        # Create a test message
        test_message = {
            "type": "test",
            "content": "Hello, testnet!"
        }
        
        # Mock the message handler
        self.node.handle_message = MagicMock()
        
        # Simulate receiving a message
        self.node._process_message(json.dumps(test_message))
        
        # Check that the message handler was called with the correct message
        self.node.handle_message.assert_called_once_with(test_message)


class TestNodeManager(unittest.TestCase):
    """Tests for the NodeManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.node_manager = NodeManager()
        
        # Create test nodes
        self.test_nodes = []
        for i in range(3):
            node_id = f"test_node_{i}"
            host = "127.0.0.1"
            port = self._find_available_port()
            node = Node(node_id, host, port)
            self.test_nodes.append(node)
    
    def _find_available_port(self):
        """Find an available port for testing."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]
    
    def tearDown(self):
        """Clean up after tests."""
        for node in self.test_nodes:
            if node.is_running():
                node.stop()
    
    def test_add_node(self):
        """Test adding a node to the manager."""
        for node in self.test_nodes:
            self.node_manager.add_node(node)
        
        self.assertEqual(len(self.node_manager.get_nodes()), len(self.test_nodes))
    
    def test_remove_node(self):
        """Test removing a node from the manager."""
        # Add all nodes
        for node in self.test_nodes:
            self.node_manager.add_node(node)
        
        # Remove one node
        self.node_manager.remove_node(self.test_nodes[0].node_id)
        
        # Check that it was removed
        self.assertEqual(len(self.node_manager.get_nodes()), len(self.test_nodes) - 1)
        self.assertNotIn(self.test_nodes[0], self.node_manager.get_nodes())
    
    def test_start_all_nodes(self):
        """Test starting all nodes in the manager."""
        # Add all nodes
        for node in self.test_nodes:
            self.node_manager.add_node(node)
        
        # Start all nodes
        self.node_manager.start_all_nodes()
        
        # Check that all nodes are running
        for node in self.test_nodes:
            self.assertTrue(node.is_running())
    
    def test_stop_all_nodes(self):
        """Test stopping all nodes in the manager."""
        # Add all nodes and start them
        for node in self.test_nodes:
            self.node_manager.add_node(node)
        self.node_manager.start_all_nodes()
        
        # Stop all nodes
        self.node_manager.stop_all_nodes()
        
        # Check that all nodes are stopped
        for node in self.test_nodes:
            self.assertFalse(node.is_running())


class TestBlockPropagation(unittest.TestCase):
    """Tests for the BlockPropagation class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a test network with 3 nodes
        self.node_manager = NodeManager()
        self.test_nodes = []
        
        for i in range(3):
            node_id = f"test_node_{i}"
            host = "127.0.0.1"
            port = self._find_available_port()
            node = Node(node_id, host, port)
            self.test_nodes.append(node)
            self.node_manager.add_node(node)
        
        # Create the block propagation service
        self.block_prop = BlockPropagation(self.node_manager)
        
        # Create a test block to propagate
        self.test_block = self._create_test_block()
    
    def _find_available_port(self):
        """Find an available port for testing."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]
    
    def _create_test_block(self):
        """Create a test block for propagation tests."""
        header = BlockHeader(
            version=1,
            prev_block_hash=b"\x00" * 64,
            merkle_root=b"\x00" * 64,
            timestamp=int(time.time()),
            bits=0x1d00ffff,
            nonce=0
        )
        
        transactions = [
            Transaction("sender1", "receiver1", 1.0, "sig1"),
            Transaction("sender2", "receiver2", 2.0, "sig2")
        ]
        
        return QuantumBlock(header=header, transactions=transactions)
    
    def tearDown(self):
        """Clean up after tests."""
        self.node_manager.stop_all_nodes()
    
    def test_propagate_block(self):
        """Test block propagation to all nodes."""
        # Mock the send_block method on each node
        for node in self.test_nodes:
            node.send_block = MagicMock()
        
        # Propagate the block
        self.block_prop.propagate_block(self.test_block)
        
        # Verify that each node received the block
        for node in self.test_nodes:
            node.send_block.assert_called_once()
    
    def test_propagate_transaction(self):
        """Test transaction propagation to all nodes."""
        # Create a test transaction
        test_tx = Transaction("sender", "receiver", 1.0, "signature")
        
        # Mock the send_transaction method on each node
        for node in self.test_nodes:
            node.send_transaction = MagicMock()
        
        # Propagate the transaction
        self.block_prop.propagate_transaction(test_tx)
        
        # Verify that each node received the transaction
        for node in self.test_nodes:
            node.send_transaction.assert_called_once()


class TestConsensusManager(unittest.TestCase):
    """Tests for the ConsensusManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create consensus manager with hybrid consensus
        self.hybrid_consensus = HybridConsensus()
        self.consensus_manager = ConsensusManager(self.hybrid_consensus)
        
        # Create test blocks for chain validation
        self.genesis_block = self._create_genesis_block()
        self.valid_block = self._create_valid_block(self.genesis_block)
        self.invalid_block = self._create_invalid_block()
    
    def _create_genesis_block(self):
        """Create a genesis block for testing."""
        header = BlockHeader(
            version=1,
            prev_block_hash=b"\x00" * 64,
            merkle_root=b"\x00" * 64,
            timestamp=int(time.time()) - 3600,  # 1 hour ago
            bits=0x1d00ffff,
            nonce=0
        )
        
        # Add some transactions
        transactions = [
            Transaction("genesis", "receiver1", 50.0, "genesis_sig")
        ]
        
        block = QuantumBlock(header=header, transactions=transactions)
        # Simulate successful mining
        block.header.nonce = 12345
        return block
    
    def _create_valid_block(self, prev_block):
        """Create a valid block that builds on the previous block."""
        header = BlockHeader(
            version=1,
            prev_block_hash=prev_block.header.hash(),
            merkle_root=b"\x01" * 64,
            timestamp=int(time.time()),
            bits=0x1d00ffff,
            nonce=0
        )
        
        transactions = [
            Transaction("sender1", "receiver1", 1.0, "sig1"),
            Transaction("sender2", "receiver2", 2.0, "sig2")
        ]
        
        block = QuantumBlock(header=header, transactions=transactions)
        # Simulate successful mining
        block.header.nonce = 67890
        return block
    
    def _create_invalid_block(self):
        """Create an invalid block with incorrect proof of work."""
        header = BlockHeader(
            version=1,
            prev_block_hash=b"\xff" * 64,  # Invalid previous hash
            merkle_root=b"\x02" * 64,
            timestamp=int(time.time()),
            bits=0x1d00ffff,
            nonce=0  # No mining performed
        )
        
        transactions = [
            Transaction("sender1", "receiver1", 1.0, "sig1")
        ]
        
        return QuantumBlock(header=header, transactions=transactions)
    
    def test_initialize_blockchain(self):
        """Test initializing the blockchain with a genesis block."""
        self.consensus_manager.initialize_blockchain(self.genesis_block)
        
        # Verify the blockchain was initialized
        self.assertEqual(len(self.consensus_manager.blockchain), 1)
        self.assertEqual(self.consensus_manager.blockchain[0], self.genesis_block)
    
    def test_validate_block(self):
        """Test validating a block for addition to the blockchain."""
        # Initialize with genesis block
        self.consensus_manager.initialize_blockchain(self.genesis_block)
        
        # Validate a valid block
        valid_result = self.consensus_manager.validate_block(self.valid_block)
        self.assertTrue(valid_result)
        
        # Validate an invalid block
        invalid_result = self.consensus_manager.validate_block(self.invalid_block)
        self.assertFalse(invalid_result)
    
    def test_add_block(self):
        """Test adding a block to the blockchain."""
        # Initialize with genesis block
        self.consensus_manager.initialize_blockchain(self.genesis_block)
        
        # Add a valid block
        add_result = self.consensus_manager.add_block(self.valid_block)
        self.assertTrue(add_result)
        
        # Verify the block was added
        self.assertEqual(len(self.consensus_manager.blockchain), 2)
        self.assertEqual(self.consensus_manager.blockchain[1], self.valid_block)
    
    def test_get_blockchain_length(self):
        """Test getting the current blockchain length."""
        # Initialize with genesis block
        self.consensus_manager.initialize_blockchain(self.genesis_block)
        
        # Check initial length
        self.assertEqual(self.consensus_manager.get_blockchain_length(), 1)
        
        # Add a block and check updated length
        self.consensus_manager.add_block(self.valid_block)
        self.assertEqual(self.consensus_manager.get_blockchain_length(), 2)
    
    def test_get_latest_block(self):
        """Test getting the latest block in the chain."""
        # Initialize with genesis block
        self.consensus_manager.initialize_blockchain(self.genesis_block)
        
        # Check initial latest block
        self.assertEqual(self.consensus_manager.get_latest_block(), self.genesis_block)
        
        # Add a block and check updated latest block
        self.consensus_manager.add_block(self.valid_block)
        self.assertEqual(self.consensus_manager.get_latest_block(), self.valid_block)


class TestIntegrationMining(unittest.TestCase):
    """Integration tests for mining and propagation."""
    
    @unittest.skip("Integration test requires actual network")
    def test_mine_and_propagate(self):
        """Test the full mining and propagation flow."""
        # This test would require actual network infrastructure
        # Skipped for unit testing purposes
        pass


if __name__ == '__main__':
    unittest.main() 