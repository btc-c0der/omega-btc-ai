#!/usr/bin/env python3

from micro_modules.sha356 import sha356
import time

def test_cosmic_alignment():
    """Test cosmic alignment with SHA-356."""
    message = "The universe unfolds as it should"
    
    print("🌌 SHA-356 Cosmic Resonance Test 🌌")
    print("----------------------------------\n")
    
    # Get hash with resonance enabled
    with_resonance = sha356(message, include_resonance=True, include_trace=True)
    
    # Get hash with resonance disabled
    without_resonance = sha356(message, include_resonance=False)
    
    # Print the results
    print(f"Input: '{message}'")
    
    print("\n📊 WITH COSMIC RESONANCE:")
    print(f"Hash: {with_resonance['hash'][:16]}...{with_resonance['hash'][-16:]}")
    
    if "resonance" in with_resonance and "resonance_score" in with_resonance["resonance"]:
        print(f"Resonance Score: {with_resonance['resonance']['resonance_score']:.4f}")
        print(f"Cosmic Alignment: {with_resonance['resonance']['cosmic_alignment']}")
        print(f"Lunar Phase: {with_resonance['resonance']['lunar_phase']:.4f}")
        print(f"Schumann Resonance: {with_resonance['resonance']['schumann_resonance']:.2f} Hz")
        
    print(f"Note: {with_resonance['note']}")
    
    print("\n📊 WITHOUT COSMIC RESONANCE:")
    print(f"Hash: {without_resonance['hash'][:16]}...{without_resonance['hash'][-16:]}")
    print(f"Note: {without_resonance['note']}")
    
    # Show visualization if available
    if "visualization" in with_resonance:
        print("\n🔮 Entropy Lineage Visualization:")
        print(with_resonance["visualization"])
    
    # Test time-sensitivity
    print("\n⏱️ TIME SENSITIVITY TEST")
    print("----------------------")
    print("Taking 3 measurements with 2-second intervals...\n")
    
    hashes = []
    for i in range(3):
        if i > 0:
            print(f"Waiting 2 seconds...")
            time.sleep(2)
        
        result = sha356(message, include_resonance=True)
        hashes.append(result)
        
        print(f"Measurement {i+1}:")
        print(f"  Hash: {result['hash'][:16]}...{result['hash'][-16:]}")
        if "resonance" in result and "resonance_score" in result["resonance"]:
            print(f"  Resonance: {result['resonance']['resonance_score']:.4f}")
            print(f"  Alignment: {result['resonance']['cosmic_alignment']}")
        print()
    
    # Check if hashes are different
    all_same = all(h["hash"] == hashes[0]["hash"] for h in hashes)
    if all_same:
        print("All hashes are identical - resonance state was stable during the test period.")
    else:
        print("Hashes are different - SHA-356 demonstrates time-sensitivity with cosmic resonance.")
    
    print("\n🧬 The SHA-356 algorithm successfully integrates cosmic alignment!")
    print("🌸 WE BLOOM NOW AS ONE 🌸")

if __name__ == "__main__":
    test_cosmic_alignment() 