"""
Quantum Proof-of-Work (qPoW) network implementation.

This module contains classes for managing a network of nodes in the qPoW testnet,
including node discovery, block and transaction propagation, and consensus.
"""
import os
import sys
import time
import json
import socket
import threading
import logging
from typing import List, Dict, Any, Optional, Union, Tuple, Callable

from .block_structure import (
    Transaction,
    QuantumBlock,
    BlockHeader,
    HybridConsensus,
    bits_to_target,
    meets_target
)
from .hash_functions import QuantumResistantHash

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Node:
    """
    Represents a node in the qPoW testnet.
    
    Nodes communicate with each other to exchange blocks and transactions,
    maintain the blockchain, and participate in consensus.
    """
    def __init__(self, node_id: str, host: str, port: int):
        """
        Initialize a new node.
        
        Args:
            node_id: Unique identifier for this node
            host: Hostname or IP address
            port: Port number to listen on
        """
        self.node_id = node_id
        self.host = host
        self.port = port
        self.running = False
        self.peers = {}  # {node_id: (host, port)}
        self.socket = None
        self.server_thread = None
        self.known_blocks = {}  # {block_hash: block}
        self.known_transactions = {}  # {tx_hash: transaction}
        self.message_handlers = {}
        
        # Register default message handlers
        self.register_message_handler("block", self._handle_block_message)
        self.register_message_handler("transaction", self._handle_transaction_message)
        self.register_message_handler("get_blocks", self._handle_get_blocks_message)
        self.register_message_handler("get_transactions", self._handle_get_transactions_message)
    
    def start(self):
        """Start the node's networking service."""
        if self.running:
            return
        
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            logger.info(f"Node {self.node_id} listening on {self.host}:{self.port}")
            
            # Start server thread
            self.server_thread = threading.Thread(target=self._accept_connections)
            self.server_thread.daemon = True
            self.server_thread.start()
            
        except Exception as e:
            logger.error(f"Error starting node {self.node_id}: {e}")
            self.running = False
            if self.socket:
                self.socket.close()
                self.socket = None
    
    def stop(self):
        """Stop the node's networking service."""
        self.running = False
        if self.socket:
            self.socket.close()
            self.socket = None
        
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=1.0)
        
        logger.info(f"Node {self.node_id} stopped")
    
    def is_running(self):
        """Check if the node is currently running."""
        return self.running
    
    def _accept_connections(self):
        """Handle incoming connections from peers."""
        while self.running:
            try:
                client_socket, address = self.socket.accept()
                logger.info(f"Node {self.node_id} accepted connection from {address}")
                
                # Handle client in a new thread
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    logger.error(f"Error accepting connection: {e}")
    
    def _handle_client(self, client_socket, address):
        """
        Handle communication with a connected client.
        
        Args:
            client_socket: Socket connected to the client
            address: Client's address information
        """
        try:
            # Set a reasonable timeout
            client_socket.settimeout(10.0)
            
            # Receive data from client
            data = b""
            while self.running:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                data += chunk
                
                # Try to process complete messages
                try:
                    message = json.loads(data.decode('utf-8'))
                    # Process the message
                    self._process_message(message)
                    # Clear the data buffer after successful processing
                    data = b""
                except json.JSONDecodeError:
                    # Incomplete message, continue receiving
                    pass
                
        except Exception as e:
            logger.error(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
    
    def _process_message(self, message_data):
        """
        Process a received message.
        
        Args:
            message_data: The received message data as a JSON string
            or a dictionary
        """
        if isinstance(message_data, str):
            try:
                message = json.loads(message_data)
            except json.JSONDecodeError:
                logger.error("Invalid JSON message received")
                return
        else:
            message = message_data
        
        # Handle the message based on its type
        self.handle_message(message)
    
    def handle_message(self, message):
        """
        Handle a parsed message based on its type.
        
        Args:
            message: The parsed message as a dictionary
        """
        message_type = message.get("type")
        if not message_type:
            logger.error("Message missing 'type' field")
            return
        
        handler = self.message_handlers.get(message_type)
        if handler:
            try:
                handler(message)
            except Exception as e:
                logger.error(f"Error handling {message_type} message: {e}")
        else:
            logger.warning(f"No handler for message type: {message_type}")
    
    def register_message_handler(self, message_type, handler):
        """
        Register a handler for a specific message type.
        
        Args:
            message_type: The type of message to handle
            handler: Function to call when this message type is received
        """
        self.message_handlers[message_type] = handler
    
    def _handle_block_message(self, message):
        """
        Handle a block message.
        
        Args:
            message: The block message
        """
        block_data = message.get("block")
        if not block_data:
            return
        
        # In a real implementation, we would deserialize the block here
        # For now, just log it
        logger.info(f"Node {self.node_id} received block message")
    
    def _handle_transaction_message(self, message):
        """
        Handle a transaction message.
        
        Args:
            message: The transaction message
        """
        tx_data = message.get("transaction")
        if not tx_data:
            return
        
        # In a real implementation, we would deserialize the transaction here
        # For now, just log it
        logger.info(f"Node {self.node_id} received transaction message")
    
    def _handle_get_blocks_message(self, message):
        """
        Handle a get_blocks message, which requests blocks from a node.
        
        Args:
            message: The get_blocks message
        """
        # In a real implementation, we would find the requested blocks
        # and send them back to the requester
        logger.info(f"Node {self.node_id} received get_blocks message")
    
    def _handle_get_transactions_message(self, message):
        """
        Handle a get_transactions message, which requests transactions from a node.
        
        Args:
            message: The get_transactions message
        """
        # In a real implementation, we would find the requested transactions
        # and send them back to the requester
        logger.info(f"Node {self.node_id} received get_transactions message")
    
    def connect_to_peer(self, host, port):
        """
        Connect to a peer node.
        
        Args:
            host: Host of the peer
            port: Port of the peer
            
        Returns:
            True if connection was successful, False otherwise
        """
        try:
            # In a real implementation, we would establish a TCP connection
            # and perform a handshake
            # For testing purposes, we'll just simulate success
            logger.info(f"Node {self.node_id} connecting to peer at {host}:{port}")
            return True
        except Exception as e:
            logger.error(f"Error connecting to peer at {host}:{port}: {e}")
            return False
    
    def send_block(self, block):
        """
        Send a block to all connected peers.
        
        Args:
            block: The block to send
        """
        # In a real implementation, we would serialize the block and send it
        # to all connected peers
        logger.info(f"Node {self.node_id} sending block to peers")
    
    def send_transaction(self, transaction):
        """
        Send a transaction to all connected peers.
        
        Args:
            transaction: The transaction to send
        """
        # In a real implementation, we would serialize the transaction and send it
        # to all connected peers
        logger.info(f"Node {self.node_id} sending transaction to peers")


class NodeManager:
    """
    Manages a collection of nodes in the qPoW testnet.
    
    Provides functionality for starting and stopping nodes, connecting them to peers,
    and broadcasting messages across the network.
    """
    def __init__(self):
        """Initialize the node manager."""
        self.nodes = {}  # {node_id: Node}
    
    def add_node(self, node):
        """
        Add a node to the manager.
        
        Args:
            node: The node to add
        """
        self.nodes[node.node_id] = node
    
    def remove_node(self, node_id):
        """
        Remove a node from the manager.
        
        Args:
            node_id: ID of the node to remove
        """
        if node_id in self.nodes:
            node = self.nodes[node_id]
            if node.is_running():
                node.stop()
            del self.nodes[node_id]
    
    def get_node(self, node_id):
        """
        Get a node by its ID.
        
        Args:
            node_id: ID of the node to get
            
        Returns:
            The node if found, None otherwise
        """
        return self.nodes.get(node_id)
    
    def get_nodes(self):
        """
        Get all nodes managed by this manager.
        
        Returns:
            List of all nodes
        """
        return list(self.nodes.values())
    
    def start_all_nodes(self):
        """Start all nodes managed by this manager."""
        for node in self.nodes.values():
            if not node.is_running():
                node.start()
    
    def stop_all_nodes(self):
        """Stop all nodes managed by this manager."""
        for node in self.nodes.values():
            if node.is_running():
                node.stop()
    
    def connect_nodes(self, source_node_id, target_node_id):
        """
        Connect two nodes to each other.
        
        Args:
            source_node_id: ID of the source node
            target_node_id: ID of the target node
            
        Returns:
            True if successful, False otherwise
        """
        source_node = self.get_node(source_node_id)
        target_node = self.get_node(target_node_id)
        
        if not source_node or not target_node:
            return False
        
        # Connect the nodes
        source_node.connect_to_peer(target_node.host, target_node.port)
        target_node.connect_to_peer(source_node.host, source_node.port)
        
        return True
    
    def create_fully_connected_network(self):
        """
        Connect all nodes to each other to form a fully connected network.
        
        Returns:
            True if successful, False otherwise
        """
        nodes = list(self.nodes.values())
        if len(nodes) < 2:
            return True  # Nothing to connect
        
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                nodes[i].connect_to_peer(nodes[j].host, nodes[j].port)
                nodes[j].connect_to_peer(nodes[i].host, nodes[i].port)
        
        return True


class BlockPropagation:
    """
    Handles propagation of blocks and transactions across the network.
    
    Ensures that new blocks and transactions are efficiently broadcast to all nodes.
    """
    def __init__(self, node_manager):
        """
        Initialize the block propagation service.
        
        Args:
            node_manager: NodeManager instance managing the network nodes
        """
        self.node_manager = node_manager
    
    def propagate_block(self, block):
        """
        Propagate a block to all nodes in the network.
        
        Args:
            block: The block to propagate
        """
        for node in self.node_manager.get_nodes():
            node.send_block(block)
    
    def propagate_transaction(self, transaction):
        """
        Propagate a transaction to all nodes in the network.
        
        Args:
            transaction: The transaction to propagate
        """
        for node in self.node_manager.get_nodes():
            node.send_transaction(transaction)


class ConsensusManager:
    """
    Manages blockchain consensus across the network.
    
    Implements the consensus rules, validates blocks, and manages the blockchain.
    """
    def __init__(self, consensus_algorithm):
        """
        Initialize the consensus manager.
        
        Args:
            consensus_algorithm: The consensus algorithm to use (e.g., HybridConsensus)
        """
        self.consensus_algorithm = consensus_algorithm
        self.blockchain = []  # List of blocks in the blockchain
    
    def initialize_blockchain(self, genesis_block):
        """
        Initialize the blockchain with a genesis block.
        
        Args:
            genesis_block: The genesis block
        """
        self.blockchain = [genesis_block]
    
    def validate_block(self, block):
        """
        Validate a block according to consensus rules.
        
        Args:
            block: The block to validate
            
        Returns:
            True if the block is valid, False otherwise
        """
        # Check if the blockchain is initialized
        if not self.blockchain:
            return False
        
        # Get the latest block
        latest_block = self.blockchain[-1]
        
        # Check if the new block's previous hash matches the latest block's hash
        if block.header.prev_block_hash != latest_block.header.hash():
            return False
        
        # Check if the block has a valid proof of work
        target_hash = bits_to_target(block.header.bits)
        if not meets_target(block.header.hash(), target_hash):
            return False
        
        # Check if the block has valid transactions
        if not block.validate_transactions():
            return False
        
        return True
    
    def add_block(self, block):
        """
        Add a valid block to the blockchain.
        
        Args:
            block: The block to add
            
        Returns:
            True if the block was added, False otherwise
        """
        if self.validate_block(block):
            self.blockchain.append(block)
            return True
        return False
    
    def get_blockchain_length(self):
        """
        Get the current length of the blockchain.
        
        Returns:
            The number of blocks in the blockchain
        """
        return len(self.blockchain)
    
    def get_latest_block(self):
        """
        Get the latest block in the blockchain.
        
        Returns:
            The latest block, or None if the blockchain is empty
        """
        if not self.blockchain:
            return None
        return self.blockchain[-1]
    
    def resolve_conflicts(self, other_blockchain):
        """
        Resolve conflicts between blockchains using the longest chain rule.
        
        Args:
            other_blockchain: Another blockchain to compare with
            
        Returns:
            True if our blockchain was replaced, False otherwise
        """
        # Get the length of our blockchain
        our_length = len(self.blockchain)
        
        # Get the length of the other blockchain
        their_length = len(other_blockchain)
        
        # If their chain is longer, replace ours
        if their_length > our_length:
            # Validate the other blockchain
            for i in range(1, their_length):
                if not self._validate_block_linkage(other_blockchain[i-1], other_blockchain[i]):
                    return False
            
            # Replace our blockchain
            self.blockchain = other_blockchain
            return True
        
        return False
    
    def _validate_block_linkage(self, prev_block, current_block):
        """
        Validate that two blocks are correctly linked.
        
        Args:
            prev_block: The previous block
            current_block: The current block
            
        Returns:
            True if the blocks are correctly linked, False otherwise
        """
        # Check if the current block's previous hash matches the previous block's hash
        return current_block.header.prev_block_hash == prev_block.header.hash() 