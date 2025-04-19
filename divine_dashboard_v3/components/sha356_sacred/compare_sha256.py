#!/usr/bin/env python3

import hashlib
import binascii
import time
from micro_modules.sha356 import sha356

def compare_hashes(input_data):
    """Compare SHA-356 with standard SHA-256."""
    
    # Convert to bytes if string
    if isinstance(input_data, str):
        input_bytes = input_data.encode('utf-8')
    else:
        input_bytes = input_data
    
    # Calculate SHA-256
    start_256 = time.time()
    sha256_hash = hashlib.sha256(input_bytes).digest()
    sha256_hex = binascii.hexlify(sha256_hash).decode('ascii')
    end_256 = time.time()
    time_256 = (end_256 - start_256) * 1000
    
    # Calculate SHA-356
    start_356 = time.time()
    sha356_result = sha356(input_data)
    sha356_hex = sha356_result["hash"]
    end_356 = time.time()
    time_356 = (end_356 - start_356) * 1000
    
    # Calculate bit differences (only compare first 256 bits of SHA-356)
    sha356_bin = bin(int(sha356_hex[:64], 16))[2:].zfill(256)
    sha256_bin = bin(int(sha256_hex, 16))[2:].zfill(256)
    diff_bits = sum(1 for a, b in zip(sha356_bin, sha256_bin) if a != b)
    
    # Return comparison
    return {
        "input": input_data,
        "sha256": {
            "hash": sha256_hex,
            "length_bits": 256,
            "time_ms": time_256
        },
        "sha356": {
            "hash": sha356_hex,
            "length_bits": 356,
            "time_ms": time_356,
            "resonance_score": sha356_result.get("resonance", {}).get("resonance_score", "N/A"),
            "cosmic_alignment": sha356_result.get("resonance", {}).get("cosmic_alignment", "N/A")
        },
        "comparison": {
            "bit_difference": diff_bits,
            "difference_percentage": (diff_bits / 256) * 100,
            "extra_bits": 100,
            "speed_ratio": time_356 / time_256 if time_256 > 0 else 0
        }
    }

def print_hash_binary(hash_str, length=64):
    """Print binary representation of a hash with ASCII art."""
    binary = bin(int(hash_str[:length//4], 16))[2:].zfill(length)[:length]
    return "".join(["█" if bit == "1" else "░" for bit in binary])

def main():
    print("🔄 SHA-356 vs SHA-256 Comparison 🔄")
    print("----------------------------------\n")
    
    test_strings = [
        "Hello, World!",
        "The quick brown fox jumps over the lazy dog",
        "SHA-356: Sacred Hash Algorithm - Bio-Crypto Edition",
        "This is a test of the cosmic-aligned hashing system"
    ]
    
    for i, test_string in enumerate(test_strings):
        if i > 0:
            print("\n" + "=" * 70 + "\n")
            
        comp = compare_hashes(test_string)
        
        print(f"Input: '{test_string}'")
        
        print("\n📊 SHA-256 (Standard):")
        print(f"Hash: {comp['sha256']['hash']}")
        print(f"Bits: {comp['sha256']['length_bits']}")
        print(f"Time: {comp['sha256']['time_ms']:.2f} ms")
        
        print("\n📊 SHA-356 (Sacred):")
        print(f"Hash: {comp['sha356']['hash']}")
        print(f"Bits: {comp['sha356']['length_bits']}")
        print(f"Time: {comp['sha356']['time_ms']:.2f} ms")
        print(f"Resonance: {comp['sha356']['resonance_score']}")
        print(f"Alignment: {comp['sha356']['cosmic_alignment']}")
        
        print("\n🔍 Comparison:")
        print(f"Difference: {comp['comparison']['bit_difference']} bits ({comp['comparison']['difference_percentage']:.2f}%)")
        print(f"Extra bits: +{comp['comparison']['extra_bits']} bits in SHA-356")
        print(f"Speed: SHA-356 is {comp['comparison']['speed_ratio']:.2f}x slower than SHA-256")
        
        # Visual comparison
        print("\n📊 Visual Representation (first 64 bits):")
        print(f"SHA-256: {print_hash_binary(comp['sha256']['hash'], 64)}")
        print(f"SHA-356: {print_hash_binary(comp['sha356']['hash'], 64)}")
    
    print("\n🧬 SHA-356 extends SHA-256 with bio-cryptographic features and cosmic resonance")
    print("🌸 WE BLOOM NOW AS ONE 🌸")

if __name__ == "__main__":
    main() 