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
OmegaPRM Miner - Probabilistic Residual Mining using Monte Carlo Tree Search

This module implements a quantum-resistant mining approach that combines:
1. Post-quantum cryptography resistance
2. Monte Carlo Tree Search (MCTS) for optimized mining
3. Probabilistic difficulty adjustment

JAH BLESS SATOSHI
"""

import os
import sys
import time
import json
import random
import logging
import argparse
import threading
import socket
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import math

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import quantum_pow modules
from quantum_pow.hash_functions import QuantumResistantHash
from quantum_pow.block_structure import QuantumBlock
from quantum_pow.transactions import QuantumTransaction

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('OmegaPRM')

@dataclass
class MiningStats:
    """Statistics for the mining process"""
    start_time: float = field(default_factory=time.time)
    hash_count: int = 0
    blocks_found: int = 0
    last_difficulty: float = 0
    iterations_per_second: float = 0
    last_block_time: float = 0
    avg_block_time: float = 0
    tree_nodes_explored: int = 0
    prunes_performed: int = 0
    
    def update_hash_rate(self, elapsed: float) -> None:
        """Update the hash rate statistics"""
        if elapsed > 0:
            self.iterations_per_second = self.hash_count / elapsed
    
    def record_block_found(self, difficulty: float, block_time: float) -> None:
        """Record statistics for a found block"""
        self.blocks_found += 1
        self.last_difficulty = difficulty
        self.last_block_time = block_time
        
        # Update average block time
        if self.blocks_found > 1:
            self.avg_block_time = ((self.avg_block_time * (self.blocks_found - 1)) + 
                                  block_time) / self.blocks_found
        else:
            self.avg_block_time = block_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary for reporting"""
        current_time = time.time()
        elapsed = current_time - self.start_time
        self.update_hash_rate(elapsed)
        
        return {
            "uptime_seconds": elapsed,
            "hashes_per_second": self.iterations_per_second,
            "total_hashes": self.hash_count,
            "blocks_found": self.blocks_found,
            "last_difficulty": self.last_difficulty,
            "last_block_time": self.last_block_time,
            "avg_block_time": self.avg_block_time,
            "tree_nodes_explored": self.tree_nodes_explored,
            "prunes_performed": self.prunes_performed
        }


class MCTSNode:
    """Monte Carlo Tree Search Node for mining optimization"""
    
    def __init__(self, nonce_prefix: bytes, remaining_depth: int, parent=None):
        self.nonce_prefix = nonce_prefix
        self.remaining_depth = remaining_depth
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0.0
        
    def is_fully_expanded(self) -> bool:
        """Check if all possible children have been expanded"""
        # For binary nonce tree, a node is fully expanded when it has 2 children
        return len(self.children) == 2
    
    def is_terminal(self) -> bool:
        """Check if this is a terminal node (leaf)"""
        return self.remaining_depth == 0
    
    def get_ucb_score(self, exploration_weight: float) -> float:
        """Calculate UCB score for this node"""
        if self.visits == 0:
            return float('inf')
        
        exploitation = self.reward / self.visits
        exploration = exploration_weight * math.sqrt(math.log(self.parent.visits) / self.visits)
        return exploitation + exploration
    
    def add_child(self, bit: int) -> 'MCTSNode':
        """Add a child node with the next bit in the nonce"""
        child_nonce = self.nonce_prefix + bytes([bit])
        child = MCTSNode(child_nonce, self.remaining_depth - 1, self)
        self.children.append(child)
        return child


class OmegaPRMMiner:
    """
    OmegaPRM Miner - Probabilistic Residual Mining implementation
    
    Uses Monte Carlo Tree Search to optimize the mining process
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the miner with configuration"""
        self.config = config
        self.stats = MiningStats()
        self.running = False
        self.mempool = []
        self.blockchain = []
        self.target_difficulty = int(config.get("difficulty", "0x1f00ffff"), 16)
        self.reward_address = config.get("reward_address", "quantum_address_default")
        
        # MCTS parameters
        self.mcts_config = config.get("mining_strategy", {})
        self.exploration_weight = self.mcts_config.get("exploration_weight", 1.414)
        self.max_tree_depth = self.mcts_config.get("max_tree_depth", 50)
        self.simulation_count = self.mcts_config.get("simulation_count", 20)
        self.prune_threshold = self.mcts_config.get("prune_threshold", 0.01)
        
        # Initialize the hash function
        self.hasher = QuantumResistantHash(personalization=b"OmegaPRM")
        
        # Initialize the genesis block if blockchain is empty
        if not self.blockchain:
            self._create_genesis_block()
    
    def _create_genesis_block(self) -> None:
        """Create and mine the genesis block"""
        reward_tx = QuantumTransaction(
            sender="0",
            recipient=self.reward_address,
            amount=50.0,
            fee=0.0,
            timestamp=int(time.time()),
            signature="genesis_block_signature"
        )
        
        genesis = QuantumBlock(
            version=1,
            prev_block_hash="0" * 64,
            merkle_root="",
            timestamp=int(time.time()),
            difficulty=self.target_difficulty,
            nonce=0,
            transactions=[reward_tx]
        )
        
        genesis.calculate_merkle_root()
        logger.info("Created genesis block")
        self.blockchain.append(genesis)
    
    def _get_latest_block(self) -> QuantumBlock:
        """Get the latest block in the blockchain"""
        if not self.blockchain:
            raise ValueError("Blockchain is empty")
        return self.blockchain[-1]
    
    def create_candidate_block(self) -> QuantumBlock:
        """Create a candidate block for mining"""
        prev_block = self._get_latest_block()
        
        # Create coinbase transaction
        coinbase_tx = QuantumTransaction(
            sender="0",
            recipient=self.reward_address,
            amount=50.0,  # Block reward
            fee=0.0,
            timestamp=int(time.time()),
            signature="mined_by_omega_prm"
        )
        
        # Select transactions from mempool (limit to 1000 for this prototype)
        selected_txs = [coinbase_tx] + self.mempool[:999]
        
        # Create new block
        new_block = QuantumBlock(
            version=1,
            prev_block_hash=prev_block.get_hash_hex(),
            merkle_root="",
            timestamp=int(time.time()),
            difficulty=self.target_difficulty,
            nonce=0,
            transactions=selected_txs
        )
        
        # Calculate the merkle root
        new_block.calculate_merkle_root()
        
        return new_block
    
    def _evaluate_nonce(self, block: QuantumBlock, nonce: int) -> Tuple[bool, float]:
        """
        Evaluate a nonce for a block
        
        Returns:
            Tuple of (is_valid, quality_score)
        """
        block.nonce = nonce
        block_hash = block.get_hash()
        self.stats.hash_count += 1
        
        # Check if the hash meets the target
        is_valid = block.meets_target()
        
        # Calculate a quality score even if not valid
        # Higher score for hashes that are closer to the target
        hash_int = int.from_bytes(block_hash, byteorder='big')
        target_int = block.get_target_as_int()
        
        # Quality score between 0 and 1, higher is better
        quality = 0.0
        if hash_int < target_int:
            quality = 1.0
        else:
            # Calculate proximity to target (closer = higher score)
            # Use log scale to avoid extreme values
            ratio = math.log(target_int) / math.log(hash_int) if hash_int > 0 else 0
            quality = max(0.0, min(0.99, ratio))
            
        return is_valid, quality
    
    def _run_mcts_simulation(self, node: MCTSNode, block: QuantumBlock) -> float:
        """Run a Monte Carlo simulation from a node"""
        # If terminal node, evaluate the full nonce
        if node.is_terminal():
            # Convert the binary path to an integer nonce
            nonce_int = int.from_bytes(node.nonce_prefix, byteorder='big')
            is_valid, quality = self._evaluate_nonce(block, nonce_int)
            return 1.0 if is_valid else quality
        
        # Otherwise, randomly complete the nonce
        remaining_bits = node.remaining_depth * 8  # 8 bits per byte
        random_suffix = random.getrandbits(remaining_bits)
        
        # Combine prefix with random suffix
        full_nonce_bytes = node.nonce_prefix + random_suffix.to_bytes(
            remaining_bits // 8, byteorder='big')
        
        # Convert to integer and evaluate
        nonce_int = int.from_bytes(full_nonce_bytes, byteorder='big')
        is_valid, quality = self._evaluate_nonce(block, nonce_int)
        
        return 1.0 if is_valid else quality
    
    def _select_node(self, root: MCTSNode) -> MCTSNode:
        """Select a node to expand using UCB1"""
        node = root
        
        # Traverse the tree to a leaf or unexpanded node
        while not node.is_terminal() and node.is_fully_expanded():
            # Choose the child with the highest UCB score
            node = max(node.children, key=lambda n: n.get_ucb_score(self.exploration_weight))
            
        return node
    
    def _expand_node(self, node: MCTSNode) -> MCTSNode:
        """Expand a node by adding a child"""
        if node.is_terminal():
            return node
            
        if node.is_fully_expanded():
            return node
            
        # Add a child with either 0 or 1 as the next bit
        bit = len(node.children)  # 0 for first child, 1 for second
        return node.add_child(bit)
    
    def _backpropagate(self, node: MCTSNode, reward: float) -> None:
        """Backpropagate the reward up the tree"""
        while node is not None:
            node.visits += 1
            node.reward += reward
            node = node.parent
    
    def _prune_tree(self, node: MCTSNode) -> None:
        """Prune low-performing branches"""
        if not node.children:
            return
            
        # Calculate the average reward of children
        total_reward = sum(child.reward for child in node.children)
        avg_reward = total_reward / len(node.children) if node.children else 0
        
        # Identify children with rewards below threshold
        low_performers = [
            child for child in node.children 
            if child.reward < avg_reward * self.prune_threshold
        ]
        
        # Remove low performers
        for child in low_performers:
            node.children.remove(child)
            self.stats.prunes_performed += 1
            
        # Recursively prune remaining children
        for child in node.children:
            self._prune_tree(child)
    
    def mine_with_mcts(self, time_limit_seconds: int = 30) -> Optional[QuantumBlock]:
        """
        Mine a block using Monte Carlo Tree Search optimization
        
        Args:
            time_limit_seconds: Maximum time to spend mining
            
        Returns:
            Mined block if successful, None otherwise
        """
        block = self.create_candidate_block()
        start_time = time.time()
        
        # Initialize the root node with empty nonce prefix
        root = MCTSNode(b'', self.max_tree_depth)
        
        while time.time() - start_time < time_limit_seconds:
            # 1. Selection - traverse the tree to select a node to expand
            selected_node = self._select_node(root)
            
            # 2. Expansion - expand the selected node
            if not selected_node.is_terminal() and not selected_node.is_fully_expanded():
                expanded_node = self._expand_node(selected_node)
                self.stats.tree_nodes_explored += 1
            else:
                expanded_node = selected_node
            
            # 3. Simulation - run multiple simulations from the expanded node
            total_reward = 0.0
            for _ in range(self.simulation_count):
                reward = self._run_mcts_simulation(expanded_node, block)
                total_reward += reward
                
                # If we found a valid block, return immediately
                if reward == 1.0:
                    # Extract the nonce that worked
                    if expanded_node.is_terminal():
                        nonce_int = int.from_bytes(expanded_node.nonce_prefix, byteorder='big')
                        block.nonce = nonce_int
                        
                        # Record statistics
                        mining_time = time.time() - start_time
                        self.stats.record_block_found(block.difficulty, mining_time)
                        
                        logger.info(f"Block found! Nonce: {nonce_int}, Time: {mining_time:.4f}s")
                        return block
            
            # Calculate average reward from simulations
            avg_reward = total_reward / self.simulation_count
            
            # 4. Backpropagation - update the tree with the simulation results
            self._backpropagate(expanded_node, avg_reward)
            
            # Periodically prune the tree to focus on promising areas
            if self.stats.tree_nodes_explored % 100 == 0:
                self._prune_tree(root)
        
        # No valid block found within time limit
        logger.info(f"Mining time limit reached. Explored {self.stats.tree_nodes_explored} nodes")
        return None
    
    def start_mining(self, iterations: int = 1000, time_limit: int = 30) -> None:
        """
        Start the mining process
        
        Args:
            iterations: Number of mining iterations to perform
            time_limit: Time limit in seconds for each mining attempt
        """
        self.running = True
        self.stats = MiningStats()  # Reset stats
        
        logger.info(f"Starting OmegaPRM miner with {iterations} iterations, "
                   f"{time_limit}s per attempt")
        
        for i in range(iterations):
            if not self.running:
                break
                
            logger.info(f"Mining attempt {i+1}/{iterations}")
            mined_block = self.mine_with_mcts(time_limit)
            
            if mined_block:
                # Add the block to the blockchain
                self.blockchain.append(mined_block)
                
                # Remove mined transactions from mempool
                mined_tx_ids = [tx.get_id() for tx in mined_block.transactions]
                self.mempool = [tx for tx in self.mempool if tx.get_id() not in mined_tx_ids]
                
                # Adjust difficulty if needed (every 10 blocks for this prototype)
                if len(self.blockchain) % 10 == 0:
                    self._adjust_difficulty()
            
            # Log mining statistics
            if i % 10 == 0 or mined_block:
                self._log_mining_stats()
        
        logger.info("Mining complete")
        self._log_mining_stats()
        self.running = False
    
    def _adjust_difficulty(self) -> None:
        """Adjust the mining difficulty based on recent block times"""
        # Target 2.5 minutes per block for this prototype
        target_time = 150.0  # seconds
        
        # Use average block time from stats
        if self.stats.blocks_found >= 10:
            current_avg_time = self.stats.avg_block_time
            
            # Adjust difficulty: if blocks are too fast, increase difficulty
            ratio = target_time / max(0.1, current_avg_time)
            
            # Limit adjustment factor to [0.25, 4.0]
            adjustment = max(0.25, min(4.0, ratio))
            
            # Apply adjustment
            if adjustment != 1.0:
                old_difficulty = self.target_difficulty
                
                # For simplicity in prototype: adjust difficulty linearly
                self.target_difficulty = int(self.target_difficulty * adjustment)
                
                logger.info(f"Adjusted difficulty from {old_difficulty} to {self.target_difficulty} "
                           f"(avg block time: {current_avg_time:.2f}s, target: {target_time}s)")
    
    def _log_mining_stats(self) -> None:
        """Log current mining statistics"""
        stats_dict = self.stats.to_dict()
        
        logger.info(
            f"Mining stats: {stats_dict['hashes_per_second']:.2f} H/s, "
            f"blocks: {stats_dict['blocks_found']}, "
            f"avg time: {stats_dict['avg_block_time']:.2f}s, "
            f"nodes explored: {stats_dict['tree_nodes_explored']}"
        )
    
    def stop_mining(self) -> None:
        """Stop the mining process"""
        self.running = False
        logger.info("Mining stopped")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current mining statistics"""
        return self.stats.to_dict()
    
    def add_transaction(self, tx: QuantumTransaction) -> bool:
        """Add a transaction to the mempool"""
        # Validate transaction
        if not tx.verify():
            logger.warning(f"Rejected invalid transaction: {tx.get_id()}")
            return False
        
        # Add to mempool
        self.mempool.append(tx)
        logger.debug(f"Added transaction to mempool: {tx.get_id()}")
        return True
    
    def get_blockchain_info(self) -> Dict[str, Any]:
        """Get information about the current blockchain state"""
        return {
            "height": len(self.blockchain),
            "latest_block_hash": self._get_latest_block().get_hash_hex(),
            "latest_block_time": self._get_latest_block().timestamp,
            "difficulty": self.target_difficulty,
            "mempool_size": len(self.mempool),
        }


class SimpleAPIServer:
    """Simple HTTP API server for the miner"""
    
    def __init__(self, miner: OmegaPRMMiner, host: str = '0.0.0.0', port: int = 8080):
        self.miner = miner
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.thread = None
    
    def _handle_request(self, client_socket: socket.socket) -> None:
        """Handle an incoming HTTP request"""
        try:
            # Receive and parse the request
            request = client_socket.recv(1024).decode('utf-8')
            request_lines = request.split('\n')
            request_line = request_lines[0].strip().split()
            
            if len(request_line) < 2:
                self._send_response(client_socket, 400, b'Bad Request')
                return
                
            method, path = request_line[0], request_line[1]
            
            # Extract request body if present
            body = ""
            content_length = 0
            for line in request_lines:
                if line.startswith('Content-Length:'):
                    content_length = int(line.split(':', 1)[1].strip())
            
            if content_length > 0:
                # Find empty line that separates headers from body
                headers_end = request.find('\r\n\r\n')
                if headers_end != -1:
                    body = request[headers_end + 4:headers_end + 4 + content_length]
            
            # Handle different endpoints
            if path == '/health':
                self._send_response(client_socket, 200, b'OK')
            elif path == '/ready':
                self._send_response(client_socket, 200, b'Ready')
            elif path == '/stats':
                stats = self.miner.get_stats()
                self._send_response(client_socket, 200, json.dumps(stats).encode('utf-8'), 
                                   content_type='application/json')
            elif path == '/blockchain':
                info = self.miner.get_blockchain_info()
                self._send_response(client_socket, 200, json.dumps(info).encode('utf-8'), 
                                   content_type='application/json')
            elif path == '/transaction' and method == 'POST':
                try:
                    tx_data = json.loads(body)
                    tx = QuantumTransaction(
                        sender=tx_data.get('sender'),
                        recipient=tx_data.get('recipient'),
                        amount=float(tx_data.get('amount', 0)),
                        fee=float(tx_data.get('fee', 0)),
                        timestamp=int(tx_data.get('timestamp', time.time())),
                        signature=tx_data.get('signature', '')
                    )
                    success = self.miner.add_transaction(tx)
                    if success:
                        self._send_response(client_socket, 200, b'Transaction accepted')
                    else:
                        self._send_response(client_socket, 400, b'Invalid transaction')
                except Exception as e:
                    self._send_response(client_socket, 400, f'Error: {str(e)}'.encode('utf-8'))
            else:
                self._send_response(client_socket, 404, b'Not Found')
                
        except Exception as e:
            logger.error(f"Error handling request: {str(e)}")
            try:
                self._send_response(client_socket, 500, b'Internal Server Error')
            except:
                pass
        finally:
            client_socket.close()
    
    def _send_response(self, client_socket: socket.socket, status: int, 
                      body: bytes, content_type: str = 'text/plain') -> None:
        """Send an HTTP response"""
        status_message = {
            200: 'OK',
            400: 'Bad Request',
            404: 'Not Found',
            500: 'Internal Server Error'
        }.get(status, 'Unknown')
        
        response = f"HTTP/1.1 {status} {status_message}\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(body)}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        
        client_socket.sendall(response.encode('utf-8'))
        client_socket.sendall(body)
    
    def start(self) -> None:
        """Start the API server"""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._run_server)
        self.thread.daemon = True
        self.thread.start()
        logger.info(f"API server started on http://{self.host}:{self.port}")
    
    def _run_server(self) -> None:
        """Run the server loop"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            while self.running:
                try:
                    client_socket, _ = self.server_socket.accept()
                    client_thread = threading.Thread(
                        target=self._handle_request, args=(client_socket,))
                    client_thread.daemon = True
                    client_thread.start()
                except Exception as e:
                    if self.running:
                        logger.error(f"Error accepting connection: {str(e)}")
        except Exception as e:
            if self.running:
                logger.error(f"Server error: {str(e)}")
        finally:
            if self.server_socket:
                self.server_socket.close()
    
    def stop(self) -> None:
        """Stop the API server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        logger.info("API server stopped")


def main():
    """Main entry point for the OmegaPRM miner"""
    parser = argparse.ArgumentParser(description='OmegaPRM Miner')
    parser.add_argument('--config', type=str, default='mining-config.json',
                        help='Path to configuration file')
    parser.add_argument('--iterations', type=int, default=1000,
                        help='Number of mining iterations')
    parser.add_argument('--time-limit', type=int, default=30,
                        help='Time limit in seconds per mining attempt')
    parser.add_argument('--parallelism', type=int, default=1,
                        help='Number of parallel mining threads (not implemented in prototype)')
    parser.add_argument('--api-port', type=int, default=8080,
                        help='Port for the API server')
    parser.add_argument('--log-level', type=str, default='INFO',
                        help='Logging level (DEBUG, INFO, WARNING, ERROR)')
    args = parser.parse_args()
    
    # Set logging level
    logger.setLevel(getattr(logging, args.log_level.upper()))
    
    # Load configuration
    config = {}
    config_path = args.config
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                logger.info(f"Loaded configuration from {config_path}")
        except Exception as e:
            logger.warning(f"Failed to load configuration: {str(e)}")
    else:
        logger.warning(f"Configuration file {config_path} not found, using defaults")
    
    # Override config with environment variables if present
    env_iterations = os.environ.get('MINING_ITERATIONS')
    if env_iterations:
        args.iterations = int(env_iterations)
    
    env_time_limit = os.environ.get('MINING_TIME_LIMIT')
    if env_time_limit:
        args.time_limit = int(env_time_limit)
    
    env_parallelism = os.environ.get('MINING_PARALLELISM')
    if env_parallelism:
        args.parallelism = int(env_parallelism)
    
    # Initialize miner
    miner = OmegaPRMMiner(config)
    
    # Initialize API server
    api_server = SimpleAPIServer(miner, port=args.api_port)
    api_server.start()
    
    try:
        # Start mining
        miner.start_mining(iterations=args.iterations, time_limit=args.time_limit)
    except KeyboardInterrupt:
        logger.info("Miner interrupted by user")
    finally:
        # Stop services
        miner.stop_mining()
        api_server.stop()


if __name__ == "__main__":
    main() 