#!/usr/bin/env python3
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

Demonstration script for the Quantum Proof-of-Work (qPoW) system.

This script showcases the key features of the qPoW implementation including:
- Quantum-resistant hash computation
- Transaction creation and validation
- Block creation, validation, and mining
- Blockchain compatibility features
"""
import os
import sys
import time
import json
import argparse
from datetime import datetime

from quantum_pow import (
    QuantumResistantHash,
    QuantumResistantHashFactory,
    Transaction,
    BlockHeader,
    QuantumBlock,
    verify_hash_resistance,
)

# Add imports for the Denarius-inspired features
from quantum_pow.ecosystem import FortunaStakes
from quantum_pow.block_structure import HybridConsensus

def demonstrate_hash_function():
    """Demonstrate the quantum-resistant hash function."""
    print("\n=== Quantum-Resistant Hash Function ===")
    
    # Create a hash function
    qhash = QuantumResistantHash()
    
    # Hash a string
    test_data = b"JAH BLESS SATOSHI - Quantum-resistant PoW"
    hash_result = qhash.hash(test_data)
    
    print(f"Input: {test_data.decode()}")
    print(f"Hash result: {hash_result.hex()}")
    print(f"Hash length: {len(hash_result)} bytes ({len(hash_result) * 8} bits)")
    
    # Show avalanche effect
    test_data2 = b"JAH BLESS SATOSHI - Quantum-resistant PoW!"  # One character different
    hash_result2 = qhash.hash(test_data2)
    
    # Count bit differences
    bit_diff = sum(bin(hash_result[i] ^ hash_result2[i]).count('1') for i in range(len(hash_result)))
    percent_diff = (bit_diff / (len(hash_result) * 8)) * 100
    
    print(f"\nAvalanche Effect Demonstration:")
    print(f"Input 2: {test_data2.decode()}")
    print(f"Hash result 2: {hash_result2.hex()}")
    print(f"Bit differences: {bit_diff} out of {len(hash_result) * 8} bits ({percent_diff:.2f}%)")
    
    # Compare with SHA-256
    import hashlib
    sha_result = hashlib.sha256(test_data).digest()
    print(f"\nSHA-256 result: {sha_result.hex()}")
    print(f"SHA-256 length: {len(sha_result)} bytes ({len(sha_result) * 8} bits)")
    
    # Verify quantum resistance
    resistance_score = verify_hash_resistance(qhash)
    print(f"\nQuantum resistance score: {resistance_score:.4f} out of 1.0")


def demonstrate_transactions():
    """Demonstrate quantum-resistant transactions."""
    print("\n=== Quantum-Resistant Transactions ===")
    
    # Create a classical transaction
    classical_tx = Transaction(
        sender="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",  # First Bitcoin address (Satoshi)
        recipient="1CounterpartyXXXXXXXXXXXXXXXUWLpVr",  # Counterparty address
        amount=50.0,
        signature="classical_signature_data"
    )
    
    # Create a quantum-signed transaction
    quantum_tx = Transaction(
        sender="quantum_address_1a2b3c4d5e6f",
        recipient="quantum_address_6f5e4d3c2b1a",
        amount=25.0,
        signature="quantum_signature_data_with_lattice_based_cryptography",
        is_quantum_signed=True
    )
    
    # Display transactions
    print("Classical Transaction:")
    print(f"  Sender: {classical_tx.sender}")
    print(f"  Recipient: {classical_tx.recipient}")
    print(f"  Amount: {classical_tx.amount}")
    print(f"  Is quantum-signed: {classical_tx.is_quantum_signed}")
    print(f"  Transaction hash: {classical_tx.hash().hex()[:16]}...")
    print(f"  Signature valid: {classical_tx.verify_signature()}")
    
    print("\nQuantum Transaction:")
    print(f"  Sender: {quantum_tx.sender}")
    print(f"  Recipient: {quantum_tx.recipient}")
    print(f"  Amount: {quantum_tx.amount}")
    print(f"  Is quantum-signed: {quantum_tx.is_quantum_signed}")
    print(f"  Transaction hash: {quantum_tx.hash().hex()[:16]}...")
    print(f"  Signature valid: {quantum_tx.verify_signature()}")
    
    # Serialize and deserialize
    serialized = quantum_tx.serialize()
    deserialized = Transaction.deserialize(serialized)
    
    print("\nSerialization Test:")
    print(f"  Original hash: {quantum_tx.hash().hex()[:16]}...")
    print(f"  Deserialized hash: {deserialized.hash().hex()[:16]}...")
    print(f"  Match: {quantum_tx.hash() == deserialized.hash()}")


def demonstrate_block_creation():
    """Demonstrate quantum-resistant block creation and mining."""
    print("\n=== Quantum-Resistant Block Creation and Mining ===")
    
    # Create some transactions
    transactions = [
        Transaction("miner", "miner_reward", 50.0, "mining_reward"),
        Transaction("address1", "address2", 10.0, "tx_signature_1"),
        Transaction("address3", "address4", 5.0, "tx_signature_2")
    ]
    
    # Create a genesis block (no previous block)
    genesis_block = QuantumBlock(
        header=BlockHeader(
            version=1,
            prev_block_hash=b"\x00" * 64,  # Genesis block has all zeros
            merkle_root=b"\x00" * 64,  # Will be calculated by the block
            timestamp=int(time.time()),
            bits=0x1f00ffff,  # Very easy difficulty for testing
            nonce=0
        ),
        transactions=transactions
    )
    
    # Print block info
    print("Genesis Block:")
    print(f"  Version: {genesis_block.header.version}")
    print(f"  Previous hash: {genesis_block.header.prev_block_hash.hex()[:16]}...")
    print(f"  Merkle root: {genesis_block.header.merkle_root.hex()[:16]}...")
    print(f"  Timestamp: {datetime.fromtimestamp(genesis_block.header.timestamp)}")
    print(f"  Transactions: {len(genesis_block.transactions)}")
    
    # Mine the block
    print("\nMining genesis block...")
    start_time = time.time()
    result = genesis_block.mine(max_attempts=1000)
    end_time = time.time()
    
    if result:
        print(f"  Mining successful! Time: {end_time - start_time:.4f} seconds")
        print(f"  Nonce: {genesis_block.header.nonce}")
        print(f"  Block hash: {genesis_block.header.hash().hex()}")
    else:
        print("  Mining failed to find a valid nonce within the attempt limit")
    
    # Create a second block that builds on the genesis block
    transactions2 = [
        Transaction("miner", "miner_reward", 50.0, "mining_reward_2"),
        Transaction("address5", "address6", 15.0, "tx_signature_3")
    ]
    
    second_block = QuantumBlock(
        header=BlockHeader(
            version=1,
            prev_block_hash=genesis_block.header.hash(),  # Reference the genesis block
            merkle_root=b"\x00" * 64,  # Will be calculated by the block
            timestamp=int(time.time()),
            bits=0x1f00ffff,  # Same difficulty
            nonce=0
        ),
        transactions=transactions2
    )
    
    # Mine the second block
    print("\nMining second block...")
    start_time = time.time()
    result = second_block.mine(max_attempts=1000)
    end_time = time.time()
    
    if result:
        print(f"  Mining successful! Time: {end_time - start_time:.4f} seconds")
        print(f"  Nonce: {second_block.header.nonce}")
        print(f"  Block hash: {second_block.header.hash().hex()}")
    else:
        print("  Mining failed to find a valid nonce within the attempt limit")
    
    # Demonstrate backwards compatibility
    print("\nClassical Bitcoin Compatibility:")
    classical_format = second_block.to_classical_format()
    print(f"  Compatible JSON format: {classical_format[:100]}...")


def demonstrate_denarius_inspired_features():
    """
    Demonstrate features inspired by the Denarius cryptocurrency.
    
    This function showcases how our quantum-resistant implementation incorporates
    concepts from Denarius, including:
    
    1. Tribus-inspired hash function
    2. Fortuna Stakes hybrid masternode system
    3. Hybrid PoW/PoS consensus
    4. 30-second block time
    """
    print("\n" + "="*80)
    print("DENARIUS-INSPIRED QUANTUM-RESISTANT FEATURES")
    print("="*80)
    
    # 1. Demonstrate Tribus-inspired hash function
    print("\n1. Tribus-Inspired Quantum-Resistant Hash Function")
    print("-"*50)
    
    # Create a Tribus-inspired hash function
    tribus_hash = QuantumResistantHashFactory.create("tribus")
    
    # Hash a test string
    test_data = b"Inspired by Denarius's Tribus algorithm"
    hash_result = tribus_hash.hash(test_data)
    
    print(f"Input data: {test_data.decode()}")
    print(f"Tribus-Quantum hash (hex): {hash_result.hex()[:24]}...{hash_result.hex()[-24:]}")
    print(f"Hash length: {len(hash_result) * 8} bits")
    
    # Show avalanche effect
    modified_data = bytearray(test_data)
    modified_data[0] = modified_data[0] ^ 1  # Flip one bit
    modified_hash = tribus_hash.hash(bytes(modified_data))
    
    # Count differing bits
    diff_bits = 0
    for a, b in zip(hash_result, modified_hash):
        diff_bits += bin(a ^ b).count('1')
    
    print(f"Avalanche effect: Changed 1 bit in input, {diff_bits} bits changed in output ({diff_bits/(len(hash_result)*8)*100:.2f}%)")
    
    # 2. Demonstrate Fortuna Stakes
    print("\n2. Fortuna Stakes - Quantum-Resistant Hybrid Masternodes")
    print("-"*50)
    
    # Create a mock network
    class MockNetwork:
        def broadcast(self, message):
            pass
    
    # Initialize Fortuna Stakes system
    fortuna = FortunaStakes(MockNetwork())
    
    # Register some stakes
    stake1 = fortuna.register_stake(
        "QRAddressXYZ123456789",
        "txid1234567890abcdef",
        "quantum_sig_1"  # This would be a real quantum signature
    )
    
    stake2 = fortuna.register_stake(
        "QRAddressABC987654321",
        "txid0987654321fedcba",
        "quantum_sig_2"
    )
    
    # Show active stakes
    active_stakes = fortuna.get_active_stakes()
    print(f"Active Fortuna Stakes: {len(active_stakes)}")
    for stake_id, stake_info in active_stakes.items():
        print(f"  Stake ID: {stake_id[:8]}...{stake_id[-8:]}")
        print(f"  Owner: {stake_info['owner']}")
        print(f"  Collateral: {stake_info['collateral'][:8]}...{stake_info['collateral'][-8:]}")
        print(f"  Registered: {stake_info['registered_at']}")
        print()
    
    # Calculate and distribute rewards
    block_reward = 10.0
    stake_reward = fortuna.calculate_reward(block_reward)
    print(f"Block reward: {block_reward} coins")
    print(f"Fortuna Stake reward ({fortuna.reward_percentage}%): {stake_reward} coins")
    
    distributions = fortuna.distribute_rewards(12345, block_reward)
    print(f"Distributed to {len(distributions)} stakes")
    for stake_id, amount in distributions.items():
        print(f"  Stake {stake_id[:8]}...{stake_id[-8:]}: {amount} coins")
    
    # 3. Demonstrate Hybrid PoW/PoS Consensus
    print("\n3. Hybrid PoW/PoS Consensus")
    print("-"*50)
    
    # Create hybrid consensus
    hybrid = HybridConsensus()
    
    print(f"Target block time: {hybrid.target_block_time} seconds (like Denarius)")
    print(f"Minimum stake age: {hybrid.stake_min_age/3600} hours (like Denarius)")
    
    # Show difficulty adjustment for PoW vs PoS
    pow_difficulty = hybrid.pow_difficulty_bits
    pos_difficulty = hybrid.pow_difficulty_bits - hybrid.pos_difficulty_modifier
    
    print(f"PoW difficulty bits: {pow_difficulty}")
    print(f"PoS difficulty bits: {pos_difficulty} (easier than PoW)")
    
    # Simulate stake validation
    coin_age = 9 * 60 * 60  # 9 hours
    stake_modifier = 12345678
    target = 2**240  # Example target
    
    is_valid = hybrid.is_valid_stake(coin_age, stake_modifier, target)
    print(f"Stake validation with {coin_age/3600} hour coin age: {'Valid' if is_valid else 'Invalid'}")
    
    # Show how it's more accessible than just PoW
    print("\nHybrid Consensus Benefits:")
    print("- Secures network through both quantum-resistant PoW and PoS")
    print("- Reduces energy consumption compared to pure PoW")
    print("- Provides network security even if quantum mining becomes centralized")
    print("- Fast 30-second block times for quick transaction confirmation")
    print("- Incentivizes holding coins through staking rewards")


def main():
    parser = argparse.ArgumentParser(description="Quantum-resistant Proof-of-Work Demo")
    parser.add_argument("--hash", action="store_true", help="Demonstrate hash function")
    parser.add_argument("--tx", action="store_true", help="Demonstrate transactions")
    parser.add_argument("--block", action="store_true", help="Demonstrate block creation")
    parser.add_argument("--denarius", action="store_true", help="Demonstrate Denarius-inspired features")
    parser.add_argument("--all", action="store_true", help="Demonstrate everything")
    
    args = parser.parse_args()
    
    # If no arguments, show everything
    if not (args.hash or args.tx or args.block or args.denarius):
        args.all = True
    
    if args.hash or args.all:
        demonstrate_hash_function()
        
    if args.tx or args.all:
        demonstrate_transactions()
        
    if args.block or args.all:
        demonstrate_block_creation()
        
    if args.denarius or args.all:
        demonstrate_denarius_inspired_features()


if __name__ == "__main__":
    main() 