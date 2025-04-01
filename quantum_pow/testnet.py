#!/usr/bin/env python3
"""
Quantum Proof-of-Work (qPoW) Testnet Runner

This script sets up and runs a local testnet for the qPoW blockchain system.
It creates a network of nodes, connects them together, and simulates mining
and transaction propagation.
"""
import os
import sys
import time
import json
import argparse
import random
import logging
import threading
from typing import List, Dict, Any, Optional, Union

from quantum_pow.network import (
    Node,
    NodeManager,
    BlockPropagation,
    ConsensusManager
)
from quantum_pow.hash_functions import QuantumResistantHash
from quantum_pow.block_structure import (
    Transaction,
    BlockHeader,
    QuantumBlock,
    HybridConsensus
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("testnet.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TestnetConfig:
    """Configuration for the testnet environment."""
    def __init__(self, node_count=3, mine_interval=10, tx_interval=5):
        """
        Initialize testnet configuration.
        
        Args:
            node_count: Number of nodes to create in the testnet
            mine_interval: Interval between mining attempts (seconds)
            tx_interval: Interval between transaction creation (seconds)
        """
        self.node_count = node_count
        self.mine_interval = mine_interval
        self.tx_interval = tx_interval
        self.base_port = 9000  # Base port for nodes
        self.host = "127.0.0.1"  # Host for all nodes


class Testnet:
    """Local testnet environment for the qPoW system."""
    def __init__(self, config: TestnetConfig):
        """
        Initialize the testnet.
        
        Args:
            config: TestnetConfig instance with testnet parameters
        """
        self.config = config
        self.node_manager = NodeManager()
        self.block_propagation = BlockPropagation(self.node_manager)
        self.consensus = HybridConsensus()
        self.consensus_manager = ConsensusManager(self.consensus)
        self.running = False
        self.miner_thread = None
        self.tx_thread = None
        
        # Create the nodes
        self._create_nodes()
        
        # Create the genesis block
        self.genesis_block = self._create_genesis_block()
        self.consensus_manager.initialize_blockchain(self.genesis_block)
    
    def _create_nodes(self):
        """Create nodes for the testnet."""
        for i in range(self.config.node_count):
            node_id = f"node_{i}"
            port = self.config.base_port + i
            node = Node(node_id, self.config.host, port)
            self.node_manager.add_node(node)
            logger.info(f"Created node {node_id} at {self.config.host}:{port}")
    
    def _create_genesis_block(self):
        """Create the genesis block for the testnet."""
        header = BlockHeader(
            version=1,
            prev_block_hash=b"\x00" * 64,  # Genesis block has all zeros
            merkle_root=b"\x00" * 64,
            timestamp=int(time.time()),
            bits=0x1f00ffff,  # Very easy difficulty for testing
            nonce=0
        )
        
        # Add coinbase transaction
        coinbase_tx = Transaction(
            sender="genesis",
            recipient="miner_1",
            amount=50.0,
            signature="genesis_signature"
        )
        
        block = QuantumBlock(header=header, transactions=[coinbase_tx])
        
        # Mine the genesis block
        success = block.mine(max_attempts=10000)
        if not success:
            raise RuntimeError("Failed to mine genesis block")
        
        logger.info(f"Created genesis block with nonce {block.header.nonce}")
        return block
    
    def start(self):
        """Start the testnet."""
        if self.running:
            return
        
        self.running = True
        
        # Start all nodes
        logger.info("Starting all nodes...")
        self.node_manager.start_all_nodes()
        
        # Connect all nodes to form a fully connected network
        logger.info("Connecting nodes...")
        self.node_manager.create_fully_connected_network()
        
        # Start mining thread
        self.miner_thread = MiningThread(self)
        self.miner_thread.start()
        
        # Start transaction generation thread
        self.tx_thread = TransactionThread(self)
        self.tx_thread.start()
        
        logger.info("Testnet started")
    
    def stop(self):
        """Stop the testnet."""
        if not self.running:
            return
        
        self.running = False
        
        # Stop all nodes
        logger.info("Stopping all nodes...")
        self.node_manager.stop_all_nodes()
        
        # Wait for threads to finish
        if self.miner_thread:
            self.miner_thread.join()
        
        if self.tx_thread:
            self.tx_thread.join()
        
        logger.info("Testnet stopped")
    
    def get_blockchain_stats(self):
        """
        Get statistics about the current blockchain.
        
        Returns:
            Dictionary with blockchain statistics or a string message if not initialized
        """
        if not self.consensus_manager.blockchain:
            return {"status": "Blockchain not initialized", "length": 0}
        
        chain_length = self.consensus_manager.get_blockchain_length()
        latest_block = self.consensus_manager.get_latest_block()
        
        if latest_block is None:
            return {"status": "No blocks in chain", "length": 0}
        
        return {
            "status": "Active",
            "length": chain_length,
            "latest_block_hash": latest_block.header.hash().hex()[:10] + "...",
            "latest_block_timestamp": latest_block.header.timestamp,
            "latest_block_nonce": latest_block.header.nonce,
            "tx_count": len(latest_block.transactions)
        }


class MiningThread(threading.Thread):
    """Thread for simulating mining on the testnet."""
    def __init__(self, testnet: Testnet):
        """
        Initialize the mining thread.
        
        Args:
            testnet: Testnet instance to mine on
        """
        super().__init__()
        self.daemon = True
        self.testnet = testnet
    
    def run(self):
        """Run the mining thread."""
        logger.info("Mining thread started")
        
        while self.testnet.running:
            # Wait for mine_interval seconds
            time.sleep(self.testnet.config.mine_interval)
            
            # Get the latest block
            latest_block = self.testnet.consensus_manager.get_latest_block()
            if not latest_block:
                continue
            
            # Create a new block
            header = BlockHeader(
                version=1,
                prev_block_hash=latest_block.header.hash(),
                merkle_root=b"\x00" * 64,  # Will be calculated by the block
                timestamp=int(time.time()),
                bits=0x1f00ffff,  # Very easy difficulty for testing
                nonce=0
            )
            
            # Get transactions from the pool (simulated)
            transactions = self._get_transactions()
            
            # Create the block
            block = QuantumBlock(header=header, transactions=transactions)
            
            # Mine the block
            logger.info("Mining a new block...")
            success = block.mine(max_attempts=10000)
            
            if success:
                logger.info(f"Successfully mined block with nonce {block.header.nonce}")
                
                # Add the block to the blockchain
                if self.testnet.consensus_manager.add_block(block):
                    logger.info("Block added to blockchain")
                    
                    # Propagate the block to all nodes
                    self.testnet.block_propagation.propagate_block(block)
                else:
                    logger.warning("Block validation failed")
            else:
                logger.warning("Failed to mine block")
    
    def _get_transactions(self):
        """
        Get transactions for inclusion in a block.
        
        This is a simulated version that creates random transactions.
        
        Returns:
            List of Transaction objects
        """
        # Coinbase transaction
        coinbase = Transaction(
            sender="coinbase",
            recipient=f"miner_{random.randint(1, 10)}",
            amount=50.0,
            signature="coinbase_signature"
        )
        
        # Random number of regular transactions
        transactions = [coinbase]
        tx_count = random.randint(0, 5)
        
        for i in range(tx_count):
            tx = Transaction(
                sender=f"sender_{random.randint(1, 100)}",
                recipient=f"recipient_{random.randint(1, 100)}",
                amount=random.uniform(0.1, 10.0),
                signature=f"signature_{random.randint(1000, 9999)}"
            )
            transactions.append(tx)
        
        return transactions


class TransactionThread(threading.Thread):
    """Thread for simulating transaction creation on the testnet."""
    def __init__(self, testnet: Testnet):
        """
        Initialize the transaction thread.
        
        Args:
            testnet: Testnet instance to create transactions on
        """
        super().__init__()
        self.daemon = True
        self.testnet = testnet
    
    def run(self):
        """Run the transaction thread."""
        logger.info("Transaction thread started")
        
        while self.testnet.running:
            # Wait for tx_interval seconds
            time.sleep(self.testnet.config.tx_interval)
            
            # Create a random transaction
            tx = Transaction(
                sender=f"sender_{random.randint(1, 100)}",
                recipient=f"recipient_{random.randint(1, 100)}",
                amount=random.uniform(0.1, 10.0),
                signature=f"signature_{random.randint(1000, 9999)}"
            )
            
            logger.info(f"Created transaction from {tx.sender} to {tx.recipient} for {tx.amount:.2f}")
            
            # Propagate the transaction to all nodes
            self.testnet.block_propagation.propagate_transaction(tx)


def run_testnet(config: TestnetConfig, run_time: Optional[int] = None):
    """
    Run a testnet with the given configuration.
    
    Args:
        config: TestnetConfig instance with testnet parameters
        run_time: Time to run the testnet in seconds (None for indefinite)
    """
    testnet = Testnet(config)
    
    try:
        # Start the testnet
        testnet.start()
        
        if run_time is None:
            # Run indefinitely until interrupted
            while True:
                time.sleep(30)
                stats = testnet.get_blockchain_stats()
                logger.info(f"Blockchain stats: {stats}")
        else:
            # Run for the specified time
            logger.info(f"Running testnet for {run_time} seconds")
            start_time = time.time()
            end_time = start_time + run_time
            
            while time.time() < end_time:
                remaining = end_time - time.time()
                if remaining <= 0:
                    break
                sleep_time = min(30, remaining)
                time.sleep(sleep_time)
                stats = testnet.get_blockchain_stats()
                logger.info(f"Blockchain stats: {stats}")
    
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, stopping testnet")
    finally:
        # Stop the testnet
        testnet.stop()


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run a qPoW testnet")
    
    parser.add_argument(
        "--nodes", type=int, default=3,
        help="Number of nodes in the testnet (default: 3)"
    )
    
    parser.add_argument(
        "--mine-interval", type=int, default=10,
        help="Interval between mining attempts in seconds (default: 10)"
    )
    
    parser.add_argument(
        "--tx-interval", type=int, default=5,
        help="Interval between transaction creations in seconds (default: 5)"
    )
    
    parser.add_argument(
        "--run-time", type=int, default=None,
        help="Time to run the testnet in seconds (default: indefinite)"
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    config = TestnetConfig(
        node_count=args.nodes,
        mine_interval=args.mine_interval,
        tx_interval=args.tx_interval
    )
    
    run_testnet(config, args.run_time) 