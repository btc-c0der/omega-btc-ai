#!/usr/bin/env python3
"""
Quantum-resistant Proof-of-Work (qPoW) Demonstration

This script demonstrates the core functionality of the qPoW system,
including hash computation, block creation, transaction validation,
and mining.

JAH BLESS SATOSHI
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
    verify_hash_resistance
)

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


def main():
    """Main entry point for the demonstration."""
    parser = argparse.ArgumentParser(description="Quantum-resistant PoW Demonstration")
    parser.add_argument("--hash-only", action="store_true", help="Only demonstrate hash function")
    parser.add_argument("--tx-only", action="store_true", help="Only demonstrate transactions")
    parser.add_argument("--block-only", action="store_true", help="Only demonstrate block creation")
    
    args = parser.parse_args()
    
    print("=== Quantum-resistant Proof-of-Work (qPoW) Demonstration ===")
    print("JAH BLESS SATOSHI")
    
    if args.hash_only:
        demonstrate_hash_function()
    elif args.tx_only:
        demonstrate_transactions()
    elif args.block_only:
        demonstrate_block_creation()
    else:
        # Run all demonstrations
        demonstrate_hash_function()
        demonstrate_transactions()
        demonstrate_block_creation()


if __name__ == "__main__":
    main() 