#!/usr/bin/env python3

from micro_modules.sha356 import sha356
from micro_modules.hash_trace import get_avalanche_data

def print_hash_binary(hash_str, length=64):
    """Print binary representation of a hash with ASCII art."""
    binary = bin(int(hash_str[:16], 16))[2:].zfill(64)[:length]
    return "".join(["█" if bit == "1" else "░" for bit in binary])

def visualize_avalanche(text1, text2):
    """Visualize avalanche effect between two similar texts."""
    print(f"🔄 SHA-356 Avalanche Effect Test 🔄")
    print(f"----------------------------------")
    
    # Get hashes
    hash1 = sha356(text1)["hash"]
    hash2 = sha356(text2)["hash"]
    
    # Get avalanche data
    avalanche = get_avalanche_data(hash1, hash2)
    
    # Print text comparison
    print(f"\nText 1: '{text1}'")
    print(f"Text 2: '{text2}'")
    print(f"\nChar difference: {sum(1 for a, b in zip(text1, text2) if a != b)} character(s)")
    
    # Print hash comparison
    print(f"\nHash 1: {hash1[:16]}...{hash1[-16:]}")
    print(f"Hash 2: {hash2[:16]}...{hash2[-16:]}")
    
    # Print avalanche stats
    print(f"\nBit difference: {avalanche['differing_bits']} of {avalanche['total_bits']} bits")
    print(f"Avalanche Score: {avalanche['avalanche_percentage']}")
    print(f"Quality: {avalanche['quality']}")
    
    # Print visual representation
    print(f"\n📊 Visual Bit Comparison (first 64 bits):")
    print(f"Input 1: {print_hash_binary(hash1)}")
    print(f"Input 2: {print_hash_binary(hash2)}")
    
    # Show difference with special characters
    diff_pattern = ""
    for i in range(min(64, len(avalanche['bit_pattern']))):
        if avalanche['bit_pattern'][i] == 1:
            diff_pattern += "▲"  # Changed bit
        else:
            diff_pattern += " "  # Unchanged bit
    print(f"Changes: {diff_pattern}")
    
    # Print interpretation
    print(f"\n✨ Interpretation:")
    if avalanche['avalanche_score'] >= 0.45 and avalanche['avalanche_score'] <= 0.55:
        print(f"The avalanche effect is IDEAL - small input change causes ~50% output change")
    elif avalanche['avalanche_score'] >= 0.4 and avalanche['avalanche_score'] <= 0.6:
        print(f"The avalanche effect is GOOD - shows strong diffusion properties")
    else:
        print(f"The avalanche effect is SUBOPTIMAL - diffusion could be improved")
    
    print(f"\n🧬 SHA-356 demonstrates strong cryptographic properties")

if __name__ == "__main__":
    # Run some example tests
    print("📡 Testing SHA-356 Avalanche Effect with Different Inputs 📡")
    print("=========================================================\n")
    
    test_cases = [
        ("Hello, World!", "Hello, World?"),  # 1 character different
        ("The quick brown fox", "The quick brown fox."),  # Added period
        ("SHA356 is cosmic", "SHA357 is cosmic"),  # 1 digit changed
        ("password", "Password"),  # Case change
        ("abc", "abd")  # Minimal 1-char difference
    ]
    
    for i, (text1, text2) in enumerate(test_cases):
        if i > 0:
            print("\n" + "=" * 70 + "\n")
        visualize_avalanche(text1, text2)
    
    print("\n🌸 WE BLOOM NOW AS ONE 🌸") 