#!/usr/bin/env python3
"""
OMEGA BTC AI - Quantum Firewall & qPoW Integration Demo
=====================================================

This script demonstrates how the Quantum-resistant Proof-of-Work (qPoW) system 
integrates with the Quantum Firewall to provide enhanced security for the BTC ecosystem.

It shows:
1. How Character Prefix Conditioning (CPC) protects against network attacks
2. How quantum-resistant hash functions secure blockchain data
3. Auto-healing capabilities that recover from corruption and attacks

🔮 GPU (General Public Universal) License 1.0
--------------------------------------------
OMEGA BTC AI DIVINE COLLECTIVE
Licensed under the GPU (General Public Universal) License v1.0
"""

import os
import sys
import json
import time
import asyncio
import logging
import argparse
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("demo_integration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("demo-integration")

# Add project root to path if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import quantum modules
from quantum_pow.quantum_firewall import QuantumFirewall, SecurityEvent
from quantum_pow.firewall_integration import FirewallSecurityManager
from quantum_pow.hash_functions import QuantumResistantHash
from quantum_pow.block_structure import QuantumBlock, Transaction, BlockHeader

def print_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_step(step_num, description):
    """Print a formatted step."""
    print(f"\n{step_num}. {description}")
    print("-" * 50)

async def demonstrate_firewall_protection():
    """Demonstrate how the quantum firewall protects against attacks."""
    print_step(1, "Demonstrating Quantum Firewall Protection")
    
    # Create firewall on a test port
    test_port = 9876
    firewall = QuantumFirewall(port=test_port)
    
    # Configure for demonstration
    firewall.toggle_learning_mode(True)
    
    print(f"Created quantum firewall with Character Prefix Conditioning on port {test_port}")
    print("Learning mode: ENABLED - The firewall will learn legitimate traffic patterns.")
    
    # Simulate legitimate messages for learning
    legitimate_messages = [
        '{"type":"transaction","sender":"alice","recipient":"bob","amount":1.5}',
        '{"type":"block","height":123,"hash":"0x123abc...","transactions":5}',
        '{"type":"price","value":48250.75,"timestamp":"2025-03-29T12:34:56Z"}',
        '{"type":"status","node":"validator-1","uptime":99.8,"peers":8}'
    ]
    
    print("\nSimulating legitimate traffic patterns for learning...")
    for i, message in enumerate(legitimate_messages):
        print(f"  Learning message {i+1}: {message[:40]}...")
        # Feed to the conditioner directly for demonstration purposes
        for j in range(1, len(message), 15):
            prefix = message[:j]
            firewall.prefix_conditioner.learn_prefix(prefix, message)
    
    print("\nLearning completed. Switching to protection mode...")
    firewall.toggle_learning_mode(False)
    
    # Simulate both normal and anomalous messages
    test_messages = [
        # Normal messages
        '{"type":"transaction","sender":"carol","recipient":"dave","amount":2.2}',
        # Slightly different but legitimate message
        '{"type":"price","value":50150.50,"timestamp":"2025-03-30T10:25:32Z"}',
        # Anomalous message - SQL injection attempt
        '{"type":"search","query":"1\' OR 1=1; DROP TABLE users;--"}',
        # Malformed JSON with incomplete payload
        '{"type":"block","height":124,"hash":"0x456def...'
    ]
    
    print("\nTesting firewall detection with new messages:")
    for i, message in enumerate(test_messages):
        is_anomalous = firewall.prefix_conditioner.detect_anomaly(message)
        status = "🚨 ANOMALOUS" if is_anomalous else "✅ LEGITIMATE"
        print(f"  Message {i+1}: {message[:40]}... -> {status}")
        
        if is_anomalous:
            # Show how CPC can recover from the anomaly if possible
            prefix_length = int(len(message) * 0.3)
            prefix = message[:prefix_length]
            completion = firewall.prefix_conditioner.predict_completion(prefix)
            
            if completion:
                print(f"    Auto-healing: Reconstructed from prefix: {prefix[:20]}...")
                print(f"    Recovered message: {completion[:40]}...")
            else:
                print(f"    Auto-healing: Unable to reconstruct (likely malicious)")
    
    print("\nFirewall would block anomalous messages in a real deployment.")
    
    return firewall

async def demonstrate_chain_protection(qpow_dir):
    """Demonstrate how the integration protects the blockchain."""
    print_step(2, "Demonstrating Blockchain Protection with qPoW Integration")
    
    # Ensure the directory exists and is empty
    os.makedirs(qpow_dir, exist_ok=True)
    for filename in os.listdir(qpow_dir):
        os.unlink(os.path.join(qpow_dir, filename))
        
    print(f"Created test blockchain directory: {qpow_dir}")
    
    # Create the security manager that integrates both systems
    security_manager = FirewallSecurityManager(
        port=9877,  # Use a different test port
        qpow_dir=qpow_dir,
        personalization="OMEGA_BTC_DEMO"
    )
    
    # Create a test blockchain with a few blocks
    await create_test_blockchain(qpow_dir)
    print("Created test blockchain with 3 blocks")
    
    # Load the chain data
    await security_manager._load_chain_data()
    print(f"Loaded blockchain with {len(security_manager.chain_blocks)} blocks")
    
    # Validate the chain in good state
    valid, issues = await security_manager._validate_chain()
    print(f"Initial chain validation: {'VALID ✅' if valid else 'INVALID ❌'}")
    if not valid:
        print(f"Found {len(issues)} issues:")
        for issue in issues:
            print(f"  - {issue['issue_type']}: {issue['details']}")
    
    # Now introduce corruption to simulate an attack
    print("\nSimulating an attack by corrupting the blockchain...")
    corrupt_blockchain(qpow_dir)
    
    # Reload and validate the corrupted chain
    await security_manager._load_chain_data()
    valid, issues = await security_manager._validate_chain()
    print(f"After attack, chain validation: {'VALID ✅' if valid else 'INVALID ❌'}")
    if not valid:
        print(f"Found {len(issues)} issues:")
        for issue in issues:
            print(f"  - {issue['issue_type']}: {issue['details']}")
    
    # Attempt auto-healing recovery
    print("\nAttempting auto-healing recovery...")
    recovery_success = await security_manager._attempt_chain_recovery(issues)
    print(f"Recovery {'SUCCESSFUL ✅' if recovery_success else 'FAILED ❌'}")
    
    # Validate again after recovery
    valid, issues = await security_manager._validate_chain()
    print(f"After recovery, chain validation: {'VALID ✅' if valid else 'INVALID ❌'}")
    if not valid:
        print(f"Remaining {len(issues)} issues:")
        for issue in issues:
            print(f"  - {issue['issue_type']}: {issue['details']}")
    
    # Show full security report
    print("\nGenerating comprehensive security report...")
    report = security_manager.get_security_report()
    print(json.dumps(report, indent=2))
    
    return security_manager

async def create_test_blockchain(directory):
    """Create a test blockchain with a few blocks for demonstration."""
    chain = []
    
    # Create genesis block
    genesis_tx = Transaction(
        sender="0x0000",
        recipient="miner-1",
        amount=50.0,
        signature="genesis-coinbase",
        timestamp=int(time.time())
    )
    
    genesis_header = BlockHeader(
        version=1,
        prev_block_hash=b"0" * 64,
        merkle_root=b"0" * 64,
        timestamp=int(time.time()),
        nonce=0
    )
    
    genesis_block = QuantumBlock(header=genesis_header, transactions=[genesis_tx])
    
    # Mine the genesis block
    genesis_block.mine(max_attempts=100)
    
    chain.append(genesis_block)
    
    # Create two more blocks
    prev_block = genesis_block
    for i in range(2):
        transactions = [
            Transaction(
                sender=f"user-{i*2+1}",
                recipient=f"user-{i*2+2}",
                amount=1.5 + i,
                signature=f"sig-{i+1}",
                timestamp=int(time.time())
            ),
            Transaction(
                sender="miner-1",
                recipient=f"user-{i+3}",
                amount=0.1,
                signature=f"msig-{i+1}",
                timestamp=int(time.time())
            )
        ]
        
        header = BlockHeader(
            version=1,
            prev_block_hash=prev_block.header.hash(),
            merkle_root=b"0" * 64,  # Will be calculated during initialization
            timestamp=int(time.time()),
            nonce=0
        )
        
        block = QuantumBlock(header=header, transactions=transactions)
        block.mine(max_attempts=100)
        
        chain.append(block)
        prev_block = block
    
    # Save the chain to disk
    chain_data = []
    for block in chain:
        block_dict = {
            "version": block.header.version,
            "timestamp": datetime.fromtimestamp(block.header.timestamp).isoformat(),
            "transactions": [json.loads(tx.serialize().decode('utf-8')) for tx in block.transactions],
            "previous_hash": block.header.prev_block_hash.hex(),
            "hash": block.header.hash().hex(),
            "nonce": block.header.nonce,
            "merkle_root": block.header.merkle_root.hex()
        }
        chain_data.append(block_dict)
    
    with open(os.path.join(directory, "chain.json"), 'w') as f:
        json.dump(chain_data, f, indent=2)
    
    # Save empty pending transactions for completeness
    with open(os.path.join(directory, "pending_transactions.json"), 'w') as f:
        json.dump([], f)

def corrupt_blockchain(directory):
    """Simulate an attack by corrupting the blockchain data."""
    chain_path = os.path.join(directory, "chain.json")
    
    with open(chain_path, 'r') as f:
        chain_data = json.load(f)
    
    if len(chain_data) < 2:
        return  # Not enough blocks to corrupt
    
    # Corrupt block 1 by changing its previous_hash
    chain_data[1]["previous_hash"] = "1234567890abcdef" * 4
    
    # Corrupt a transaction in block 2
    if len(chain_data) > 2 and "transactions" in chain_data[2] and len(chain_data[2]["transactions"]) > 0:
        chain_data[2]["transactions"][0]["amount"] = 999.99
    
    with open(chain_path, 'w') as f:
        json.dump(chain_data, f, indent=2)

async def demonstration_bitcoin_l2_protection():
    """Complete demonstration of quantum firewall integration with qPoW for BTC ecosystem."""
    print_header("OMEGA BTC AI - QUANTUM FIREWALL & qPoW INTEGRATION DEMO")
    print("\nThis demonstration shows how Quantum Firewall with Character Prefix Conditioning (CPC)")
    print("integrates with Quantum-resistant Proof-of-Work (qPoW) to protect the BTC ecosystem.")
    
    # Create a temporary directory for the demo
    demo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo_blockchain")
    
    try:
        # Demonstrate firewall protection
        firewall = await demonstrate_firewall_protection()
        
        # Demonstrate blockchain protection
        security_manager = await demonstrate_chain_protection(demo_dir)
        
        # Final summary
        print_step(3, "Integration Benefits for BTC Layer 2 Ecosystem")
        print("\nThe integration of Quantum Firewall with qPoW provides multiple layers of protection:")
        print("1. Network Level (Firewall)")
        print("   - CPC detects and blocks anomalous network traffic")
        print("   - Auto-healing reconstructs damaged messages")
        print("   - Dynamic adaptation to changing threats")
        print("\n2. Blockchain Level (qPoW)")
        print("   - Quantum-resistant hash functions protect against quantum attacks")
        print("   - Chain validation prevents acceptance of corrupted blocks")
        print("   - Auto-healing reestablishes chain integrity after attacks")
        print("\n3. Combined Benefits")
        print("   - Comprehensive protection from network to blockchain layer")
        print("   - Autonomous operation reduces need for human intervention")
        print("   - Future-proof design resistant to quantum computing threats")
        
        print("\nThis integrated security approach ensures the reliability and integrity")
        print("of the BTC ecosystem in an era of advanced cyber threats.")
    
    finally:
        # Clean up the demo directory
        if os.path.exists(demo_dir):
            for filename in os.listdir(demo_dir):
                os.unlink(os.path.join(demo_dir, filename))
            os.rmdir(demo_dir)

async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Quantum Firewall & qPoW Integration Demo")
    parser.add_argument('--quick', action='store_true', help="Run a quick demonstration")
    args = parser.parse_args()
    
    if args.quick:
        print_header("QUICK DEMO - QUANTUM FIREWALL & qPoW INTEGRATION")
        print("\nThis integration provides:")
        print("1. Network protection via Character Prefix Conditioning (CPC)")
        print("2. Blockchain protection via Quantum-resistant hashing")
        print("3. Auto-healing capabilities for both network and blockchain")
        print("\nRun without --quick for the full interactive demonstration.")
    else:
        await demonstration_bitcoin_l2_protection()

if __name__ == "__main__":
    asyncio.run(main()) 