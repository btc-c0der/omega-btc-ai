#!/usr/bin/env python3
"""
Firewall Integration - Quantum Firewall & qPoW Integration
=========================================================

This module implements the integration between the Quantum Firewall with
Character Prefix Conditioning (CPC) and the Quantum-resistant Proof-of-Work (qPoW) system.

The integration provides comprehensive protection from network to blockchain layers.
"""

import os
import json
import time
import asyncio
import logging
from typing import Dict, List, Any, Tuple, Optional, Set, Union

from .quantum_firewall import QuantumFirewall, SecurityEvent
from .hash_functions import QuantumResistantHash
from .block_structure import QuantumBlock, Transaction, BlockHeader

# Configure module logger
logger = logging.getLogger(__name__)

class FirewallSecurityManager:
    """
    Integrates the Quantum Firewall with the qPoW system to provide
    comprehensive protection across network and blockchain layers.
    
    This class:
    1. Manages the quantum firewall for network protection
    2. Validates blockchain integrity using qPoW mechanisms
    3. Provides auto-healing capabilities for both layers
    4. Generates security reports and insights
    """
    
    def __init__(self, 
                 port: int = 9000, 
                 interface: str = '127.0.0.1',
                 qpow_dir: str = './quantum_chain',
                 personalization: str = 'OMEGA_BTC_AI'):
        """
        Initialize the firewall security manager.
        
        Args:
            port: Port for the quantum firewall
            interface: Network interface for the firewall
            qpow_dir: Directory for quantum blockchain data
            personalization: Personalization string for hash function
        """
        self.port = port
        self.interface = interface
        self.qpow_dir = qpow_dir
        self.personalization = personalization
        
        # Initialize the quantum firewall
        self.firewall = QuantumFirewall(port=port, interface=interface)
        
        # Initialize qPoW components
        self.hash_function = QuantumResistantHash(personalization=personalization)
        
        # Chain data
        self.chain_blocks: List[Dict[str, Any]] = []
        self.pending_transactions: List[Dict[str, Any]] = []
        
        # Ensure the quantum chain directory exists
        os.makedirs(qpow_dir, exist_ok=True)
        
        # Configure high-risk patterns to block
        self._configure_security_patterns()
        
        logger.info("FirewallSecurityManager initialized successfully")
    
    def start(self) -> None:
        """Start the security manager and all its components."""
        logger.info("Starting FirewallSecurityManager...")
        
        # Start the quantum firewall
        self.firewall.start()
        
        # Load chain data asynchronously
        asyncio.create_task(self._load_chain_data())
        
        # Start monitoring chain integrity
        asyncio.create_task(self._monitor_chain_integrity())
        
        logger.info("FirewallSecurityManager started successfully")
    
    def stop(self) -> None:
        """Stop the security manager and all its components."""
        logger.info("Stopping FirewallSecurityManager...")
        
        # Stop the quantum firewall
        self.firewall.stop()
        
        logger.info("FirewallSecurityManager stopped successfully")
    
    def _configure_security_patterns(self) -> None:
        """Configure security patterns to detect and block."""
        # Add patterns to detect common attacks
        self.firewall.add_blocked_pattern(r"<script>.*?</script>")  # XSS
        self.firewall.add_blocked_pattern(r"(?i)(?:union\s+select|insert\s+into|delete\s+from)")  # SQL Injection
        self.firewall.add_blocked_pattern(r"(?i)(?:eval\(|system\(|exec\()")  # Command injection
        self.firewall.add_blocked_pattern(r"/\.\./")  # Path traversal
        
        # Add patterns to detect quantum-specific attacks
        self.firewall.add_blocked_pattern(r"(?i)shor_\d+")  # Potential Shor's algorithm attack
        self.firewall.add_blocked_pattern(r"(?i)grover_search")  # Potential Grover's algorithm attack
        
        logger.info("Security patterns configured")
    
    async def _load_chain_data(self) -> None:
        """Load blockchain data from the filesystem."""
        chain_path = os.path.join(self.qpow_dir, "chain.json")
        pending_tx_path = os.path.join(self.qpow_dir, "pending_transactions.json")
        
        try:
            # Load chain data if it exists
            if os.path.exists(chain_path):
                with open(chain_path, 'r') as f:
                    self.chain_blocks = json.load(f)
                logger.info(f"Loaded {len(self.chain_blocks)} blocks from chain")
            else:
                logger.info("No existing chain found")
                self.chain_blocks = []
            
            # Load pending transactions if they exist
            if os.path.exists(pending_tx_path):
                with open(pending_tx_path, 'r') as f:
                    self.pending_transactions = json.load(f)
                logger.info(f"Loaded {len(self.pending_transactions)} pending transactions")
            else:
                logger.info("No pending transactions found")
                self.pending_transactions = []
                
        except Exception as e:
            logger.error(f"Error loading chain data: {str(e)}")
            # Ensure we have valid data structures even on error
            self.chain_blocks = []
            self.pending_transactions = []
    
    async def _save_chain_data(self) -> None:
        """Save blockchain data to the filesystem."""
        chain_path = os.path.join(self.qpow_dir, "chain.json")
        pending_tx_path = os.path.join(self.qpow_dir, "pending_transactions.json")
        
        try:
            # Save chain data
            with open(chain_path, 'w') as f:
                json.dump(self.chain_blocks, f, indent=2)
            
            # Save pending transactions
            with open(pending_tx_path, 'w') as f:
                json.dump(self.pending_transactions, f, indent=2)
                
            logger.info(f"Saved {len(self.chain_blocks)} blocks and {len(self.pending_transactions)} transactions")
            
        except Exception as e:
            logger.error(f"Error saving chain data: {str(e)}")
    
    async def _validate_chain(self) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Validate the integrity of the blockchain.
        
        Returns:
            A tuple of (is_valid, issues) where:
            - is_valid: boolean indicating if the chain is valid
            - issues: list of issue dictionaries with details
        """
        issues = []
        is_valid = True
        
        if not self.chain_blocks:
            # Empty chain is technically valid
            return True, []
        
        # Validate each block
        for i, block in enumerate(self.chain_blocks):
            # Skip genesis block validation for prev_hash
            if i > 0:
                # Validate previous hash
                prev_block = self.chain_blocks[i-1]
                if block["previous_hash"] != prev_block["hash"]:
                    issues.append({
                        "issue_type": "invalid_prev_hash",
                        "block_index": i,
                        "details": f"Block {i} has invalid previous hash"
                    })
                    is_valid = False
            
            # Validate merkle root
            txs = block.get("transactions", [])
            computed_merkle = self._compute_merkle_root(txs)
            if computed_merkle and block.get("merkle_root") != computed_merkle:
                issues.append({
                    "issue_type": "invalid_merkle_root",
                    "block_index": i,
                    "details": f"Block {i} has invalid merkle root"
                })
                is_valid = False
            
            # Validate each transaction
            for j, tx in enumerate(txs):
                if not self._validate_transaction(tx):
                    issues.append({
                        "issue_type": "invalid_transaction",
                        "block_index": i,
                        "tx_index": j,
                        "details": f"Block {i} has invalid transaction at index {j}"
                    })
                    is_valid = False
        
        if issues:
            logger.warning(f"Chain validation found {len(issues)} issues")
        else:
            logger.info("Chain validation successful - chain is valid")
            
        return is_valid, issues
    
    def _validate_transaction(self, transaction: Dict[str, Any]) -> bool:
        """
        Validate a single transaction.
        
        Args:
            transaction: Transaction dictionary
            
        Returns:
            True if valid, False otherwise
        """
        # Check required fields
        required_fields = ["sender", "recipient", "amount", "signature", "timestamp"]
        for field in required_fields:
            if field not in transaction:
                logger.warning(f"Transaction missing required field: {field}")
                return False
        
        # Check amount is positive
        if not isinstance(transaction["amount"], (int, float)) or transaction["amount"] < 0:
            logger.warning(f"Transaction has invalid amount: {transaction['amount']}")
            return False
        
        # Check timestamp is valid
        if not isinstance(transaction["timestamp"], (int, float)):
            logger.warning(f"Transaction has invalid timestamp: {transaction['timestamp']}")
            return False
        
        # Further validation could check signatures, but this is simplified for the demo
        return True
    
    def _compute_merkle_root(self, transactions: List[Dict[str, Any]]) -> Optional[str]:
        """
        Compute the merkle root of transactions.
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            Hexadecimal merkle root hash or None on error
        """
        if not transactions:
            return None
            
        try:
            # Convert transactions to strings
            tx_strings = [json.dumps(tx, sort_keys=True) for tx in transactions]
            
            # Hash each transaction
            tx_hashes = [self.hash_function.hash(tx.encode()).hex() for tx in tx_strings]
            
            # Compute merkle root (simplified)
            while len(tx_hashes) > 1:
                if len(tx_hashes) % 2 == 1:
                    tx_hashes.append(tx_hashes[-1])  # Duplicate last hash if odd
                
                next_level = []
                for i in range(0, len(tx_hashes), 2):
                    combined = tx_hashes[i] + tx_hashes[i+1]
                    next_level.append(self.hash_function.hash(combined.encode()).hex())
                
                tx_hashes = next_level
            
            return tx_hashes[0]
            
        except Exception as e:
            logger.error(f"Error computing merkle root: {str(e)}")
            return None
    
    async def _monitor_chain_integrity(self) -> None:
        """
        Continuously monitor blockchain integrity and perform healing if needed.
        
        This method runs as an asynchronous task that periodically validates
        the blockchain and attempts to recover from any detected issues.
        """
        check_interval = 60  # Check every 60 seconds
        
        while True:
            try:
                # Validate the chain
                is_valid, issues = await self._validate_chain()
                
                if not is_valid:
                    logger.warning(f"Chain integrity check failed with {len(issues)} issues")
                    
                    # Attempt to recover from the issues
                    recovery_success = await self._attempt_chain_recovery(issues)
                    
                    if recovery_success:
                        logger.info("Chain recovery successful")
                    else:
                        logger.error("Chain recovery failed")
                        
                        # Record critical security event
                        self._record_chain_security_event(issues)
                else:
                    logger.debug("Chain integrity check passed")
                
                # Wait before next check
                await asyncio.sleep(check_interval)
                
            except Exception as e:
                logger.error(f"Error in chain integrity monitor: {str(e)}")
                await asyncio.sleep(check_interval * 2)  # Wait longer after error
    
    async def _attempt_chain_recovery(self, issues: List[Dict[str, Any]]) -> bool:
        """
        Attempt to recover from chain integrity issues.
        
        Args:
            issues: List of detected issues
            
        Returns:
            True if recovery was successful, False otherwise
        """
        if not issues:
            return True  # No issues to recover from
        
        # Group issues by block index
        issues_by_block = {}
        for issue in issues:
            block_index = issue.get("block_index", -1)
            if block_index not in issues_by_block:
                issues_by_block[block_index] = []
            issues_by_block[block_index].append(issue)
        
        # Track whether all issues were resolved
        all_resolved = True
        
        # Handle issues by type
        for block_index, block_issues in issues_by_block.items():
            # Skip issues with invalid block index
            if block_index < 0 or block_index >= len(self.chain_blocks):
                continue
                
            for issue in block_issues:
                issue_type = issue.get("issue_type", "")
                
                if issue_type == "invalid_prev_hash":
                    # Fix previous hash
                    if block_index > 0:
                        prev_block = self.chain_blocks[block_index - 1]
                        self.chain_blocks[block_index]["previous_hash"] = prev_block["hash"]
                        logger.info(f"Fixed previous hash for block {block_index}")
                
                elif issue_type == "invalid_merkle_root":
                    # Recalculate merkle root
                    txs = self.chain_blocks[block_index].get("transactions", [])
                    new_merkle = self._compute_merkle_root(txs)
                    if new_merkle:
                        self.chain_blocks[block_index]["merkle_root"] = new_merkle
                        logger.info(f"Fixed merkle root for block {block_index}")
                    else:
                        all_resolved = False
                
                elif issue_type == "invalid_transaction":
                    # Handle invalid transaction
                    tx_index = issue.get("tx_index", -1)
                    if tx_index >= 0 and tx_index < len(self.chain_blocks[block_index].get("transactions", [])):
                        # Remove the invalid transaction
                        self.chain_blocks[block_index]["transactions"].pop(tx_index)
                        # Recalculate merkle root
                        txs = self.chain_blocks[block_index].get("transactions", [])
                        new_merkle = self._compute_merkle_root(txs)
                        if new_merkle:
                            self.chain_blocks[block_index]["merkle_root"] = new_merkle
                            logger.info(f"Removed invalid transaction and fixed merkle root for block {block_index}")
                        else:
                            all_resolved = False
                    else:
                        all_resolved = False
                
                else:
                    # Unknown issue type
                    all_resolved = False
                    logger.warning(f"Unknown issue type: {issue_type}")
        
        # Save the repaired chain data
        if all_resolved:
            await self._save_chain_data()
            
        return all_resolved
    
    def _record_chain_security_event(self, issues: List[Dict[str, Any]]) -> None:
        """
        Record a security event for chain integrity issues.
        
        Args:
            issues: List of detected issues
        """
        event = SecurityEvent(
            timestamp=time.time(),
            event_type="chain_integrity_violation",
            severity="high",
            source="blockchain",
            details={
                "issues_count": len(issues),
                "issue_summary": [
                    {
                        "type": issue["issue_type"],
                        "block": issue.get("block_index", "unknown"),
                        "details": issue.get("details", "")
                    }
                    for issue in issues[:5]  # Include up to 5 issues in the summary
                ]
            }
        )
        
        # Add to the firewall's security events
        self.firewall.security_events.append(event)
        logger.warning(f"Recorded chain security event: {event}")
    
    def get_security_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive security report.
        
        Returns:
            Security report dictionary with network and blockchain stats
        """
        # Get network security events from the firewall
        network_events = self.firewall.get_security_events()
        
        # Get blockchain security stats
        blockchain_stats = {
            "chain_length": len(self.chain_blocks),
            "pending_transactions": len(self.pending_transactions),
            "last_validation_time": time.time(),
            "chain_valid": True,  # Will be updated if validation finds issues
            "issues": []
        }
        
        # Validate the chain
        asyncio.create_task(self._update_security_report(blockchain_stats))
        
        return {
            "timestamp": time.time(),
            "network_security": {
                "events_count": len(network_events),
                "recent_events": network_events[:10]  # Last 10 events
            },
            "blockchain_security": blockchain_stats,
            "integration_status": {
                "firewall_running": self.firewall.running,
                "learning_mode": self.firewall.learning_mode
            }
        }
    
    async def _update_security_report(self, report_section: Dict[str, Any]) -> None:
        """
        Update the blockchain section of the security report with validation results.
        
        Args:
            report_section: The blockchain section of the report to update
        """
        # Validate the chain
        is_valid, issues = await self._validate_chain()
        
        # Update the report
        report_section["chain_valid"] = is_valid
        report_section["issues"] = [
            {
                "type": issue["issue_type"],
                "details": issue.get("details", ""),
                "block_index": issue.get("block_index", "unknown")
            }
            for issue in issues[:10]  # Include up to 10 issues
        ]
    
    def toggle_learning_mode(self, enabled: bool) -> None:
        """
        Toggle learning mode for the firewall.
        
        Args:
            enabled: True to enable learning mode, False to disable
        """
        self.firewall.toggle_learning_mode(enabled)
        logger.info(f"Learning mode {'enabled' if enabled else 'disabled'}")

async def main():
    """Run the firewall integration demo."""
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Create the security manager
    manager = FirewallSecurityManager()
    
    try:
        # Start the security manager
        manager.start()
        
        # Enable learning mode for 30 seconds
        manager.toggle_learning_mode(True)
        logger.info("Learning mode enabled for 30 seconds")
        await asyncio.sleep(30)
        
        # Disable learning mode
        manager.toggle_learning_mode(False)
        logger.info("Learning mode disabled, now in protection mode")
        
        # Run for 5 minutes
        logger.info("Running in protection mode for 5 minutes")
        await asyncio.sleep(300)
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    finally:
        # Stop the security manager
        manager.stop()
        logger.info("Security manager stopped")

if __name__ == "__main__":
    asyncio.run(main()) 