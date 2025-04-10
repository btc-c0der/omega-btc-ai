
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
OmegaPRM (Process-supervised Reward Model with Monte Carlo Tree Search) for qPoW

This module implements the OmegaPRM algorithm developed by Google DeepMind researchers,
adapted for quantum-resistant blockchain mining. It uses Monte Carlo Tree Search (MCTS)
to optimize the mining process by exploring solution paths and evaluating intermediate steps.

Inspired by: https://arxiv.org/abs/2310.04989
"""

import time
import math
import random
import logging
import json
from typing import List, Dict, Tuple, Optional, Any, Union, Callable
from collections import defaultdict

import numpy as np

from .hash_functions import QuantumResistantHash
from .block_structure import QuantumBlock, BlockHeader, Transaction, bits_to_target, meets_target

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCTSNode:
    """
    Monte Carlo Tree Search Node for mining optimization.
    
    Each node represents a partial solution state in the mining process.
    """
    
    def __init__(self, state: Dict[str, Any], parent=None, action=None):
        """
        Initialize a new MCTS node.
        
        Args:
            state: Current state representation (includes block header fields)
            parent: Parent node
            action: Action that led to this state from parent
        """
        self.state = state
        self.parent = parent
        self.action = action
        self.children = []
        self.visits = 0
        self.reward = 0.0
        self.untried_actions = self._get_untried_actions()
        
    def _get_untried_actions(self) -> List[Dict[str, Any]]:
        """Get list of untried actions from current state."""
        # For mining, actions are nonce modifications
        # We can't try all 2^32 nonce values, so we'll select promising ranges
        # based on quantum-resistant hash properties
        current_nonce = self.state.get('nonce', 0)
        
        # Generate a set of candidate nonce ranges to explore
        candidate_ranges = []
        
        # Add some ranges around the current nonce
        candidate_ranges.append({'type': 'increment', 'start': current_nonce, 'step': 1, 'count': 10})
        candidate_ranges.append({'type': 'decrement', 'start': current_nonce, 'step': 1, 'count': 10})
        
        # Add some larger jumps (quantum-inspired)
        for i in range(1, 5):
            jump = 2**(4*i)  # 16, 256, 4096, 65536
            candidate_ranges.append({'type': 'quantum_jump', 'start': current_nonce, 'jump': jump, 'count': 5})
        
        # Add some random ranges
        for _ in range(3):
            start = random.randint(0, 2**32 - 1)
            candidate_ranges.append({'type': 'random', 'start': start, 'count': 8})
            
        return candidate_ranges
    
    def select_child(self, exploration_weight: float = 1.0) -> 'MCTSNode':
        """
        Select a child node using UCB1 formula.
        
        Args:
            exploration_weight: Controls exploration vs exploitation
            
        Returns:
            Selected child node
        """
        # Use Upper Confidence Bound (UCB1) formula
        log_visits = math.log(self.visits) if self.visits > 0 else 0
        
        def ucb(child):
            exploitation = child.reward / child.visits if child.visits > 0 else 0
            exploration = exploration_weight * math.sqrt(log_visits / child.visits) if child.visits > 0 else float('inf')
            return exploitation + exploration
            
        return max(self.children, key=ucb)
    
    def expand(self) -> 'MCTSNode':
        """
        Expand by adding a new child node.
        
        Returns:
            The new child node
        """
        if not self.untried_actions:
            return None
            
        action = self.untried_actions.pop()
        next_state = self._apply_action(action)
        child = MCTSNode(state=next_state, parent=self, action=action)
        self.children.append(child)
        return child
    
    def _apply_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply an action to the current state.
        
        Args:
            action: The action to apply
            
        Returns:
            New state after applying the action
        """
        new_state = self.state.copy()
        
        if action['type'] == 'increment':
            # Try a sequence of incremented nonce values
            new_state['nonce'] = (self.state.get('nonce', 0) + 
                                 action['step'] * random.randint(1, action['count']))
        
        elif action['type'] == 'decrement':
            # Try a sequence of decremented nonce values
            decrement = action['step'] * random.randint(1, action['count'])
            new_state['nonce'] = max(0, self.state.get('nonce', 0) - decrement)
        
        elif action['type'] == 'quantum_jump':
            # Make a large jump (quantum-inspired)
            jump = action['jump']
            direction = random.choice([-1, 1])
            new_value = self.state.get('nonce', 0) + direction * jump * random.randint(1, action['count'])
            new_state['nonce'] = max(0, new_value) % (2**32)  # Ensure it's within 32-bit range
            
        elif action['type'] == 'random':
            # Try a random nonce value from the specified range
            new_state['nonce'] = action['start'] + random.randint(0, action['count'])
            
        return new_state
    
    def update(self, reward: float):
        """
        Update node statistics with simulation result.
        
        Args:
            reward: Reward value from simulation
        """
        self.visits += 1
        self.reward += reward
        
    def is_fully_expanded(self) -> bool:
        """Check if all possible actions have been tried."""
        return len(self.untried_actions) == 0
    
    def best_child(self) -> 'MCTSNode':
        """
        Get the child with the highest reward.
        
        Returns:
            Best child node
        """
        return max(self.children, key=lambda c: c.reward)


class OmegaPRMRewardModel:
    """
    Process-supervised Reward Model for mining optimization.
    
    This model assigns rewards to intermediate mining states based on how promising
    they are for finding a valid nonce.
    """
    
    def __init__(self, target_bits: int):
        """
        Initialize the reward model.
        
        Args:
            target_bits: Mining difficulty target in bits format
        """
        self.target_bits = target_bits
        self.target = bits_to_target(target_bits)
        self.hash_function = QuantumResistantHash()
        
    def evaluate(self, block_header: BlockHeader) -> float:
        """
        Evaluate a mining state and assign a reward.
        
        Args:
            block_header: Block header with the current nonce
            
        Returns:
            Reward value indicating how promising this state is
        """
        # Hash the block header
        hash_result = block_header.hash()
        
        # Check if it meets the target
        if meets_target(hash_result, self.target):
            return 100.0  # Solution found!
        
        # If not, provide a scaled reward based on how close we are
        hash_int = int.from_bytes(hash_result[:8], byteorder='big')
        target_int = int.from_bytes(self.target[:8], byteorder='big')
        
        # Calculate reward based on how close we are to the target
        # The smaller the hash_int, the closer to success
        if target_int == 0:  # Avoid division by zero
            proximity = 0.0
        else:
            # Higher value means closer to target
            proximity = 1.0 - min(1.0, hash_int / (target_int * 2.0))
        
        # Scale to a reasonable reward range
        scaled_reward = 10.0 * proximity
        
        # Add some reward for exploration
        exploration_bonus = 0.01
        
        return scaled_reward + exploration_bonus
        
    def evaluate_subproblem(self, subproblem: Dict[str, Any], state: Dict[str, Any]) -> float:
        """
        Evaluate a specific subproblem in the mining process.
        
        Args:
            subproblem: Description of the subproblem
            state: Current state of the solution
            
        Returns:
            Reward for this specific subproblem
        """
        if subproblem['type'] == 'nonce_search':
            # Create a block header to test
            header = BlockHeader(
                version=state.get('version', 1),
                prev_block_hash=state.get('prev_block_hash', bytes(32)),
                merkle_root=state.get('merkle_root', bytes(32)),
                timestamp=state.get('timestamp', int(time.time())),
                bits=self.target_bits,
                nonce=state.get('nonce', 0)
            )
            
            # Basic evaluation of the nonce search
            return self.evaluate(header)
            
        elif subproblem['type'] == 'transaction_selection':
            # Evaluate the selection of transactions for the block
            # In practice, this would consider fees, dependencies, etc.
            return 5.0  # Simplified reward
            
        return 0.0  # Default for unknown subproblems


class OmegaPRMMiner:
    """
    OmegaPRM-based miner for quantum-resistant blockchain.
    
    Uses Monte Carlo Tree Search with a process-supervised reward model
    to efficiently find valid nonces for mining.
    """
    
    def __init__(self, 
                 max_iterations: int = 1000, 
                 exploration_weight: float = 1.414,
                 time_limit: float = 10.0):
        """
        Initialize the OmegaPRM miner.
        
        Args:
            max_iterations: Maximum number of MCTS iterations
            exploration_weight: UCB1 exploration weight
            time_limit: Time limit for mining in seconds
        """
        self.max_iterations = max_iterations
        self.exploration_weight = exploration_weight
        self.time_limit = time_limit
        
    def mine_block(self, block: QuantumBlock) -> bool:
        """
        Mine a block using OmegaPRM algorithm.
        
        Args:
            block: The block to mine
            
        Returns:
            True if mining successful, False otherwise
        """
        # Create the reward model based on block difficulty
        reward_model = OmegaPRMRewardModel(block.header.bits)
        
        # Decompose the mining problem into subproblems
        subproblems = self._decompose_mining_problem(block)
        
        # For each subproblem, use MCTS to find the best solution
        solutions = []
        for subproblem in subproblems:
            start_time = time.time()
            
            # Initialize root state for this subproblem
            initial_state = {
                'version': block.header.version,
                'prev_block_hash': block.header.prev_block_hash,
                'merkle_root': block.header.merkle_root,
                'timestamp': block.header.timestamp,
                'bits': block.header.bits,
                'nonce': block.header.nonce
            }
            
            # Run MCTS
            solution = self._mcts_search(
                subproblem, 
                initial_state, 
                reward_model,
                start_time
            )
            
            solutions.append(solution)
            
            # If this is a nonce search and we found a solution, update the block
            if subproblem['type'] == 'nonce_search' and solution.get('success', False):
                block.header.nonce = solution.get('nonce', block.header.nonce)
                logger.info(f"OmegaPRM found valid nonce: {block.header.nonce}")
                return True
        
        # Check if we found a valid nonce
        block_hash = block.header.hash()
        target = bits_to_target(block.header.bits)
        if meets_target(block_hash, target):
            logger.info(f"OmegaPRM mining successful with nonce: {block.header.nonce}")
            return True
            
        logger.warning(f"OmegaPRM mining failed after {self.max_iterations} iterations")
        return False
    
    def _decompose_mining_problem(self, block: QuantumBlock) -> List[Dict[str, Any]]:
        """
        Decompose mining into subproblems using divide-and-conquer.
        
        Args:
            block: The block to mine
            
        Returns:
            List of subproblems
        """
        subproblems = []
        
        # Main subproblem: Find a valid nonce
        subproblems.append({
            'type': 'nonce_search',
            'description': 'Find a nonce that produces a hash meeting the target difficulty',
            'block_header': block.header
        })
        
        # In a more sophisticated implementation, we might also include:
        # - Transaction selection optimization
        # - Timestamp optimization
        # - Block structure optimization
        
        return subproblems
    
    def _mcts_search(self, 
                    subproblem: Dict[str, Any], 
                    initial_state: Dict[str, Any],
                    reward_model: OmegaPRMRewardModel,
                    start_time: float) -> Dict[str, Any]:
        """
        Perform Monte Carlo Tree Search for a given subproblem.
        
        Args:
            subproblem: The subproblem to solve
            initial_state: Initial state for the search
            reward_model: Reward model for evaluating states
            start_time: Start time for time limit tracking
            
        Returns:
            Dictionary with solution information
        """
        # Create root node
        root = MCTSNode(state=initial_state)
        
        # Main MCTS loop
        iteration = 0
        best_reward = 0.0
        best_state = None
        solution_found = False
        
        while (iteration < self.max_iterations and 
               time.time() - start_time < self.time_limit and
               not solution_found):
            
            # Selection phase: select best node to expand
            node = root
            while node.is_fully_expanded() and node.children:
                node = node.select_child(self.exploration_weight)
            
            # Expansion phase: expand the selected node
            if not node.is_fully_expanded():
                node = node.expand()
                if node is None:  # No more expansions possible
                    continue
            
            # Simulation phase: simulate from the new node
            simulation_result = self._simulate(subproblem, node.state, reward_model)
            reward = simulation_result['reward']
            
            # Check if we found a solution
            if simulation_result.get('success', False):
                solution_found = True
                best_state = node.state
                best_reward = reward
            
            # Backpropagation phase: update node and ancestors
            while node:
                node.update(reward)
                node = node.parent
                
            # Track best state found so far
            if reward > best_reward:
                best_reward = reward
                best_state = node.state
                
            iteration += 1
            
        # Return best solution found
        return {
            'success': solution_found,
            'iterations': iteration,
            'reward': best_reward,
            'nonce': best_state.get('nonce', initial_state.get('nonce', 0)) if best_state else initial_state.get('nonce', 0),
            'time_taken': time.time() - start_time
        }
    
    def _simulate(self, 
                 subproblem: Dict[str, Any], 
                 state: Dict[str, Any],
                 reward_model: OmegaPRMRewardModel) -> Dict[str, Any]:
        """
        Perform a simulation from a given state.
        
        Args:
            subproblem: The subproblem being solved
            state: Current state
            reward_model: Reward model for evaluation
            
        Returns:
            Simulation result including reward
        """
        # For nonce search, check if the current nonce works
        if subproblem['type'] == 'nonce_search':
            # Create a block header with the state's nonce
            header = BlockHeader(
                version=state.get('version', 1),
                prev_block_hash=state.get('prev_block_hash', bytes(32)),
                merkle_root=state.get('merkle_root', bytes(32)),
                timestamp=state.get('timestamp', int(time.time())),
                bits=state.get('bits', 0),
                nonce=state.get('nonce', 0)
            )
            
            # Check if this nonce produces a valid hash
            hash_result = header.hash()
            target = bits_to_target(state.get('bits', 0))
            success = meets_target(hash_result, target)
            
            # Evaluate the state
            reward = reward_model.evaluate(header)
            
            return {
                'success': success,
                'reward': reward
            }
            
        # For other subproblem types, evaluate with the reward model
        reward = reward_model.evaluate_subproblem(subproblem, state)
        
        return {
            'success': False,  # We don't have success criteria for other subproblems yet
            'reward': reward
        }


# Client-friendly wrapper
def mine_with_omega_prm(block: QuantumBlock, 
                        time_limit: float = 10.0, 
                        max_iterations: int = 1000) -> bool:
    """
    Mine a block using the OmegaPRM algorithm.
    
    This is a convenience function for clients that don't want to
    instantiate the OmegaPRMMiner class directly.
    
    Args:
        block: The block to mine
        time_limit: Maximum time to spend mining (seconds)
        max_iterations: Maximum MCTS iterations
        
    Returns:
        True if mining successful, False otherwise
    """
    miner = OmegaPRMMiner(
        max_iterations=max_iterations,
        time_limit=time_limit
    )
    
    start_time = time.time()
    result = miner.mine_block(block)
    elapsed = time.time() - start_time
    
    logger.info(f"OmegaPRM mining {'successful' if result else 'failed'} in {elapsed:.4f}s")
    
    return result


if __name__ == "__main__":
    # Simple test: create a block and try to mine it
    print("=== OmegaPRM Mining Test ===")
    
    # Create a test block
    header = BlockHeader(
        version=1,
        prev_block_hash=bytes([0] * 64),  # Zero hash
        merkle_root=bytes([0] * 64),  # Zero merkle root
        timestamp=int(time.time()),
        bits=0x1f00ffff,  # Very easy difficulty for testing
        nonce=0
    )
    
    block = QuantumBlock(header=header)
    
    # Try to mine it
    start_time = time.time()
    success = mine_with_omega_prm(block, time_limit=5.0)
    elapsed = time.time() - start_time
    
    if success:
        print(f"Successfully mined block in {elapsed:.4f}s")
        print(f"Nonce: {block.header.nonce}")
        print(f"Hash: {block.header.hash().hex()}")
    else:
        print(f"Failed to mine block in {elapsed:.4f}s") 