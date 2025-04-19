
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

import unittest
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any
from omega_ai.blockchain.security import (
    validate_block_hash,
    verify_transaction_signature,
    check_block_timestamp,
    validate_merkle_root,
    verify_chain_continuity,
    check_difficulty_adjustment,
    validate_block_reward,
    verify_network_consensus
)

class TestBlockchainSecurity(unittest.TestCase):
    """Sacred tests for blockchain security mechanisms."""

    def setUp(self):
        """Set up divine test data."""
        self.test_block = {
            "index": 1,
            "timestamp": int(datetime.now(timezone.utc).timestamp()),
            "transactions": [
                {
                    "sender": "divine_address_1",
                    "recipient": "divine_address_2",
                    "amount": 0.1,
                    "signature": "sacred_signature_1"
                }
            ],
            "previous_hash": "0000000000000000000000000000000000000000000000000000000000000000",
            "merkle_root": "merkle_root_hash",
            "nonce": 0,
            "difficulty": 4
        }

    def test_block_hash_validation(self):
        """Test the sacred validation of block hashes."""
        # Test valid block hash
        self.assertTrue(validate_block_hash(self.test_block))
        
        # Test tampered block
        tampered_block = self.test_block.copy()
        tampered_block["transactions"][0]["amount"] = 0.2
        self.assertFalse(validate_block_hash(tampered_block))

    def test_transaction_signature_verification(self):
        """Test the divine verification of transaction signatures."""
        # Test valid signature
        self.assertTrue(verify_transaction_signature(
            self.test_block["transactions"][0]
        ))
        
        # Test invalid signature
        invalid_tx = self.test_block["transactions"][0].copy()
        invalid_tx["signature"] = "invalid_signature"
        self.assertFalse(verify_transaction_signature(invalid_tx))

    def test_block_timestamp_validation(self):
        """Test the cosmic validation of block timestamps."""
        # Test valid timestamp
        self.assertTrue(check_block_timestamp(self.test_block))
        
        # Test future timestamp
        future_block = self.test_block.copy()
        future_block["timestamp"] = int(datetime.now(timezone.utc).timestamp()) + 3600
        self.assertFalse(check_block_timestamp(future_block))

    def test_merkle_root_validation(self):
        """Test the sacred validation of Merkle roots."""
        # Test valid Merkle root
        self.assertTrue(validate_merkle_root(self.test_block))
        
        # Test invalid Merkle root
        invalid_block = self.test_block.copy()
        invalid_block["merkle_root"] = "invalid_merkle_root"
        self.assertFalse(validate_merkle_root(invalid_block))

    def test_chain_continuity(self):
        """Test the divine continuity of the blockchain."""
        # Create a chain of blocks
        blocks = [
            self.test_block,
            {
                "index": 2,
                "previous_hash": hashlib.sha256(json.dumps(self.test_block).encode()).hexdigest(),
                "timestamp": int(datetime.now(timezone.utc).timestamp()),
                "transactions": [],
                "merkle_root": "merkle_root_hash_2",
                "nonce": 0,
                "difficulty": 4
            }
        ]
        
        # Test valid chain
        self.assertTrue(verify_chain_continuity(blocks))
        
        # Test broken chain
        broken_blocks = blocks.copy()
        broken_blocks[1]["previous_hash"] = "invalid_previous_hash"
        self.assertFalse(verify_chain_continuity(broken_blocks))

    def test_difficulty_adjustment(self):
        """Test the cosmic adjustment of mining difficulty."""
        # Test valid difficulty adjustment
        self.assertTrue(check_difficulty_adjustment(self.test_block))
        
        # Test invalid difficulty
        invalid_block = self.test_block.copy()
        invalid_block["difficulty"] = -1
        self.assertFalse(check_difficulty_adjustment(invalid_block))

    def test_block_reward_validation(self):
        """Test the sacred validation of block rewards."""
        # Test valid block reward
        self.assertTrue(validate_block_reward(self.test_block))
        
        # Test invalid block reward
        invalid_block = self.test_block.copy()
        invalid_block["transactions"].append({
            "sender": "network",
            "recipient": "miner",
            "amount": 100.0,  # Invalid reward amount
            "signature": "reward_signature"
        })
        self.assertFalse(validate_block_reward(invalid_block))

    def test_network_consensus(self):
        """Test the divine verification of network consensus."""
        # Create a set of blocks from different nodes
        blocks = [
            self.test_block,
            {
                "index": 1,
                "timestamp": int(datetime.now(timezone.utc).timestamp()),
                "transactions": [
                    {
                        "sender": "divine_address_3",
                        "recipient": "divine_address_4",
                        "amount": 0.2,
                        "signature": "sacred_signature_2"
                    }
                ],
                "previous_hash": "0000000000000000000000000000000000000000000000000000000000000000",
                "merkle_root": "merkle_root_hash_alt",
                "nonce": 0,
                "difficulty": 4
            }
        ]
        
        # Test consensus validation
        self.assertTrue(verify_network_consensus(blocks))
        
        # Test consensus violation
        invalid_blocks = blocks.copy()
        invalid_blocks[1]["transactions"][0]["amount"] = 1000.0
        self.assertFalse(verify_network_consensus(invalid_blocks))

    def test_sacred_security_integration(self):
        """Test the divine integration of all security mechanisms."""
        # Create a valid chain
        blocks = [
            self.test_block,
            {
                "index": 2,
                "previous_hash": hashlib.sha256(json.dumps(self.test_block).encode()).hexdigest(),
                "timestamp": int(datetime.now(timezone.utc).timestamp()),
                "transactions": [
                    {
                        "sender": "divine_address_5",
                        "recipient": "divine_address_6",
                        "amount": 0.3,
                        "signature": "sacred_signature_3"
                    }
                ],
                "merkle_root": "merkle_root_hash_3",
                "nonce": 0,
                "difficulty": 4
            }
        ]
        
        # Test all security mechanisms
        self.assertTrue(all([
            validate_block_hash(block) for block in blocks
        ]))
        self.assertTrue(verify_chain_continuity(blocks))
        self.assertTrue(all([
            check_block_timestamp(block) for block in blocks
        ]))
        self.assertTrue(all([
            validate_merkle_root(block) for block in blocks
        ]))
        self.assertTrue(all([
            check_difficulty_adjustment(block) for block in blocks
        ]))
        self.assertTrue(all([
            validate_block_reward(block) for block in blocks
        ]))
        self.assertTrue(verify_network_consensus(blocks))

if __name__ == '__main__':
    unittest.main() 