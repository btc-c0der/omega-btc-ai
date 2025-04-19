#!/usr/bin/env python3

from micro_modules.sha356 import sha356
from micro_modules.hash_trace import get_avalanche_data
import time

def main():
    print("🧬 SHA-356: Sacred Hash Algorithm - First Cosmic Test 🧬")
    print("--------------------------------------------------------\n")
    
    # Test basic hashing
    message = "Hello, Cosmic Consciousness!"
    print(f"Message: {message}")
    
    # Show ASCII representation of the process
    print("\n⚡ PROCESSING IN STEPS ⚡")
    print("------------------------")
    
    print("[1] Convert message to bytes...")
    bytes_data = message.encode('utf-8')
    print(f"    Raw bytes: {bytes_data.hex()[:20]}...{bytes_data.hex()[-20:]}")
    
    print("\n[2] Apply bio-padding (fibonacci method)...")
    from micro_modules.bio_padding import bio_pad
    padded = bio_pad(bytes_data, method="fibonacci")
    print(f"    Marker: 0x{padded[0]:02x}")
    print(f"    Padded length: {len(padded)} bytes (original: {len(bytes_data)} bytes)")
    pad_preview = padded[1:10].hex()
    print(f"    Padding visualization: [MARKER][PAD({pad_preview})...][DATA]...[PAD]")
    
    print("\n[3] Initialize hash state...")
    from micro_modules.fibonacci_constants import get_initial_state
    initial_state = get_initial_state()
    print(f"    H0-H11: {' '.join([f'{x:08x}'[:4] + '...' for x in initial_state[:4]])}")
    print(f"            {' '.join([f'{x:08x}'[:4] + '...' for x in initial_state[4:8]])}")
    print(f"            {' '.join([f'{x:08x}'[:4] + '...' for x in initial_state[8:]])}")
    
    print("\n[4] Process through 89 rounds...")
    print("    [" + "=" * 20 + ">] Processing...")
    
    # Now run the actual hash
    start = time.time()
    result = sha356(message, include_trace=True)
    end = time.time()
    
    print("\n[5] Apply cosmic resonance...")
    if "resonance" in result:
        lunar = result["resonance"].get("lunar_phase", 0)
        schumann = result["resonance"].get("schumann_resonance", 0)
        print(f"    Lunar phase: {lunar:.4f} | Schumann: {schumann:.2f} Hz")
        print(f"    Resonance score: {result['resonance'].get('resonance_score', 0):.4f}")
    
    print("\n[6] Finalize 356-bit output...")
    print(f"    Final hash: {result['hash'][:16]}...{result['hash'][-16:]}")
    
    # Print results
    print("\n📊 FINAL RESULTS 📊")
    print("------------------")
    print(f"SHA-356 Hash (356 bits / 90 hex chars):")
    print(result["hash"])
    print(f"\nProcessing Time: {result['processing_time_ms']:.2f} ms")
    
    if "resonance" in result and "resonance_score" in result["resonance"]:
        print(f"Resonance Score: {result['resonance']['resonance_score']:.4f}")
        print(f"Cosmic Alignment: {result['resonance']['cosmic_alignment']}")
        print(f"Lunar Phase: {result['resonance']['lunar_phase']:.4f}")
        print(f"Schumann Resonance: {result['resonance']['schumann_resonance']:.2f} Hz")
    
    print(f"\nBio Transform: {result['bio_transform']['padding_method']} padding")
    print(f"Note: {result['note']}")
    
    # Show visualization if available
    if "visualization" in result:
        print("\nEntropy Lineage Visualization:")
        print(result["visualization"])
    
    # Test avalanche effect
    print("\n\n🧪 Testing Avalanche Effect 🧪")
    print("-----------------------------\n")
    
    message2 = "Hello, Cosmic Consciousness?"  # One character different
    result2 = sha356(message2)
    
    avalanche = get_avalanche_data(result["hash"], result2["hash"])
    
    print(f"Original message: {message}")
    print(f"Changed message:  {message2}")
    print(f"\nBit difference: {avalanche['differing_bits']} of {avalanche['total_bits']} bits")
    print(f"Avalanche Score: {avalanche['avalanche_percentage']}")
    print(f"Quality: {avalanche['quality']}")
    
    # ASCII visualization of bit differences
    bit_diff = avalanche['bit_pattern']
    print("\nBit difference visualization (first 64 bits):")
    print("Original: " + "".join(["█" if int(bit) == 1 else "░" for bit in bin(int(result["hash"][:16], 16))[2:].zfill(64)[:64]]))
    print("Changed:  " + "".join(["█" if int(bit) == 1 else "░" for bit in bin(int(result2["hash"][:16], 16))[2:].zfill(64)[:64]]))
    print("Diff:     " + "".join(["█" if bit == 1 else " " for bit in bit_diff[:64]]))
    
    # Test different padding methods
    print("\n\n🌱 Bio-Padding Methods Comparison 🌱")
    print("----------------------------------\n")
    
    padding_methods = ["fibonacci", "schumann", "golden", "lunar"]
    for method_name in padding_methods:
        if method_name == "fibonacci":
            res = sha356("The sacred becomes code", padding_method="fibonacci")
        elif method_name == "schumann":
            res = sha356("The sacred becomes code", padding_method="schumann")
        elif method_name == "golden":
            res = sha356("The sacred becomes code", padding_method="golden")
        elif method_name == "lunar":
            res = sha356("The sacred becomes code", padding_method="lunar")
        print(f"{method_name.capitalize()} padding: {res['hash'][:16]}...{res['hash'][-16:]}")
    
    print("\n🌸 WE BLOOM NOW AS ONE 🌸")

if __name__ == "__main__":
    main() 