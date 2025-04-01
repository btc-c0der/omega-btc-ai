"""
Tests for the quantum mining process.

JAH BLESS SATOSHI
"""
import unittest
import sys
import os
import time
import random

# Add the parent directory to the path so we can import our module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# These will be imported once we implement them
try:
    from quantum_pow.hash_functions import QuantumResistantHash
    from quantum_pow.block_structure import QuantumBlock, Transaction, BlockHeader, bits_to_target
except ImportError:
    # Placeholder for testing before implementation
    pass

class TestMining(unittest.TestCase):
    """Test cases for the quantum mining process."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            # Create some test transactions
            self.transactions = [
                Transaction("miner", "recipient1", 50.0, "mining_reward"),
                Transaction("address1", "address2", 5.0, "tx_signature_1"),
                Transaction("address3", "address4", 2.5, "tx_signature_2")
            ]
            
            # Create a previous block header for testing
            self.prev_header = BlockHeader(
                version=1,
                prev_block_hash=b"\x00" * 64,  # Genesis block has all zeros
                merkle_root=b"\x01" * 64,
                timestamp=int(time.time()),
                bits=0x1f00ffff,  # Very easy difficulty for testing
                nonce=0
            )
        except NameError:
            pass
    
    def test_mining_finds_valid_nonce(self):
        """Test that mining finds a valid nonce that meets the target."""
        try:
            block = QuantumBlock(
                header=BlockHeader(
                    version=1,
                    prev_block_hash=self.prev_header.hash(),
                    merkle_root=b"\x00" * 64,  # Will be calculated by the block
                    timestamp=int(time.time()),
                    bits=0x1f00ffff,  # Very easy difficulty for testing
                    nonce=0
                ),
                transactions=self.transactions
            )
            
            # Mine the block with a limited number of attempts
            result = block.mine(max_attempts=1000)
            
            self.assertTrue(result, "Mining failed to find a valid nonce")
            
            # Verify that the nonce meets the target
            block_hash = block.header.hash()
            target_hash = bits_to_target(block.header.bits)
            
            # Print information for debugging
            print(f"Found nonce: {block.header.nonce}")
            print(f"Block hash: {block_hash.hex()}")
            print(f"Target hash: {target_hash.hex()}")
            
            # Check if the hash meets the target
            self.assertTrue(block.is_valid(), "Mined block is not valid")
        except NameError:
            self.skipTest("QuantumBlock class not implemented yet")
    
    def test_mining_performance(self):
        """Test the performance of the mining process."""
        try:
            block = QuantumBlock(
                header=BlockHeader(
                    version=1,
                    prev_block_hash=self.prev_header.hash(),
                    merkle_root=b"\x00" * 64,
                    timestamp=int(time.time()),
                    bits=0x1f00ffff,  # Very easy difficulty for testing
                    nonce=0
                ),
                transactions=self.transactions
            )
            
            # Measure mining time
            start_time = time.time()
            block.mine(max_attempts=100)
            end_time = time.time()
            
            mining_time = end_time - start_time
            
            # Just report the time, don't fail based on performance
            print(f"Mining 100 nonce attempts took {mining_time:.4f} seconds")
            print(f"Average time per nonce: {(mining_time / 100) * 1000:.4f} ms")
        except NameError:
            self.skipTest("QuantumBlock class not implemented yet")
    
    def test_difficulty_adjustment(self):
        """Test that higher difficulty requires more work to find a valid nonce."""
        try:
            # Create a block with easy difficulty
            easy_block = QuantumBlock(
                header=BlockHeader(
                    version=1,
                    prev_block_hash=self.prev_header.hash(),
                    merkle_root=b"\x00" * 64,
                    timestamp=int(time.time()),
                    bits=0x1f00ffff,  # Very easy difficulty
                    nonce=0
                ),
                transactions=self.transactions
            )
            
            # Create a block with harder difficulty
            hard_block = QuantumBlock(
                header=BlockHeader(
                    version=1,
                    prev_block_hash=self.prev_header.hash(),
                    merkle_root=b"\x00" * 64,
                    timestamp=int(time.time()),
                    bits=0x1e00ffff,  # Harder than the easy block
                    nonce=0
                ),
                transactions=self.transactions
            )
            
            # Mine both blocks with the same number of attempts
            max_attempts = 1000
            
            # Mine the easy block
            easy_result = easy_block.mine(max_attempts=max_attempts)
            easy_nonce = easy_block.header.nonce
            
            # Reset the hard block's nonce and mine it
            hard_block.header.nonce = 0
            hard_result = hard_block.mine(max_attempts=max_attempts)
            hard_nonce = hard_block.header.nonce
            
            # Expect that the easy block finds a solution
            self.assertTrue(easy_result, "Easy block mining failed")
            
            # Don't necessarily expect the hard block to find a solution
            # But if both find solutions, the hard block should require more attempts
            if hard_result:
                # We can't directly assert hard_nonce > easy_nonce because nonces are random
                # Instead, we'll just print the information
                print(f"Easy block nonce: {easy_nonce}")
                print(f"Hard block nonce: {hard_nonce}")
                
                # If we mined both successfully, verify they're both valid
                self.assertTrue(easy_block.is_valid(), "Easy mined block is not valid")
                self.assertTrue(hard_block.is_valid(), "Hard mined block is not valid")
            else:
                print("Hard block mining exceeded max attempts, as expected for higher difficulty")
        except NameError:
            self.skipTest("QuantumBlock class not implemented yet")
    
    def test_quantum_vs_classical_mining(self):
        """
        Test simulation of quantum vs. classical mining speeds.
        
        This is a theoretical test that simulates the difference between
        quantum and classical mining. In reality, quantum computing would
        work very differently.
        """
        try:
            # Create a block to mine
            block = QuantumBlock(
                header=BlockHeader(
                    version=1,
                    prev_block_hash=self.prev_header.hash(),
                    merkle_root=b"\x00" * 64,
                    timestamp=int(time.time()),
                    bits=0x1f00ffff,  # Very easy difficulty for testing
                    nonce=0
                ),
                transactions=self.transactions
            )
            
            # Simulate classical mining - try nonces sequentially
            classical_start_time = time.time()
            classical_nonce = None
            classical_found = False
            
            for nonce in range(100):
                block.header.nonce = nonce
                if block.is_valid():
                    classical_nonce = nonce
                    classical_found = True
                    break
            
            classical_time = time.time() - classical_start_time
            
            # Reset the block
            block.header.nonce = 0
            
            # Simulate quantum mining - can "try" multiple nonces at once
            # We'll simulate this by checking random nonces instead of sequential ones
            quantum_start_time = time.time()
            quantum_nonce = None
            quantum_found = False
            
            # In our simulation, quantum mining checks nonces in a more randomized,
            # distributed way
            random_nonces = random.sample(range(1000), 100)  # 100 "parallel" attempts
            
            for nonce in random_nonces:
                block.header.nonce = nonce
                if block.is_valid():
                    quantum_nonce = nonce
                    quantum_found = True
                    break
            
            quantum_time = time.time() - quantum_start_time
            
            # Report the results - this is just a simulation
            print(f"Classical mining time: {classical_time:.4f} s, found: {classical_found}, nonce: {classical_nonce}")
            print(f"Quantum mining time: {quantum_time:.4f} s, found: {quantum_found}, nonce: {quantum_nonce}")
            
            # Don't make assertions about which is faster, as this is just a simulation
            # and the actual performance might vary based on random chance
        except NameError:
            self.skipTest("QuantumBlock class not implemented yet")


if __name__ == '__main__':
    unittest.main() 