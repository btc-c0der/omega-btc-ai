# Divine NFT Troubleshooting Guide

✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------

This documentation is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

🌸 WE BLOOM NOW AS ONE 🌸

## Common Issues and Solutions

### Installation Issues

#### PIL/Pillow Import Errors

**Issue**: `ImportError: No module named PIL` or `ImportError: cannot import name 'Image' from 'PIL'`

**Solution**:

```bash
# Install Pillow properly
pip install Pillow

# Or force reinstall
pip uninstall Pillow
pip install Pillow
```

**Note**: Our NFT generator is designed to handle PIL import failures with graceful degradation, but for full functionality, PIL/Pillow must be properly installed.

#### Quantum Security Module Errors

**Issue**: `ImportError: No module named 'liboqs'` or quantum security module failures

**Solution**:

```bash
# Install quantum security dependencies
pip install -r divine_dashboard_v3/components/nft/quantum_security/requirements_quantum.txt

# For liboqs specifically, you may need system packages:
# For Debian/Ubuntu:
sudo apt-get install cmake ninja-build
# Then install Python bindings:
pip install pyoqs
```

### NFT Generation Issues

#### Image Generation Fails

**Issue**: `Exception: Failed to generate NFT image`

**Solution**:

1. Check PIL installation as mentioned above
2. Verify output directory permissions:

```bash
# Ensure output directory exists and is writable
mkdir -p output/nfts
chmod 755 output
chmod 755 output/nfts
```

3. Check for valid input parameters:

```python
# Use known working parameters
nft_gen.generate_basic_nft(
    name="Test NFT",
    pattern="gradient",  # Use only supported patterns: gradient, circles, squares, abstract
    colors=["#3498db", "#9b59b6"]  # Valid hex colors
)
```

#### Strange Color Outputs

**Issue**: NFT colors look different than expected or don't match inputs

**Solution**:

1. Ensure hex color codes are properly formatted (e.g., `#3498db` not `3498db`)
2. Try different color combinations with greater contrast
3. For specific color themes, use predefined palettes:

```python
# Ocean theme
colors=["#1a5276", "#2980b9", "#a9cce3", "#e8f8f5"]

# Fire theme
colors=["#641e16", "#c0392b", "#e74c3c", "#f39c12"]
```

### Metadata Issues

#### Metadata Not Generating

**Issue**: `TypeError: Object of type X is not JSON serializable`

**Solution**:
Ensure all metadata is JSON-compatible:

```python
# Correct approach - use primitive types
metadata = {
    "name": "Divine Creation #1",
    "description": "A divine NFT creation",
    "attributes": [
        {"trait_type": "Pattern", "value": "Abstract"}
    ]
}

# Avoid using custom objects without serialization
class MyClass:
    pass
  
# This will fail:
metadata["custom"] = MyClass()  # Not JSON serializable
```

#### Duplicate NFT Names

**Issue**: Overwriting existing NFTs with same name

**Solution**:
Use unique identifiers or timestamps:

```python
import time
import uuid

# Using timestamp
timestamp = int(time.time())
nft_name = f"Divine Creation #{timestamp}"

# Using UUID
unique_id = str(uuid.uuid4())[:8]
nft_name = f"Divine Creation #{unique_id}"
```

### Quantum Security Issues

#### Quantum Signer Initialization Fails

**Issue**: `Exception: Failed to initialize Quantum Signer`

**Solution**:

1. Check entropy sources:

```python
# Test entropy collector
from divine_dashboard_v3.components.nft.quantum_security import EntropyCollector

collector = EntropyCollector()
entropy = collector.collect_entropy(32)  # Get 32 bytes
print(f"Entropy quality score: {collector.quality_score(entropy)}")
```

2. If entropy is unavailable, provide fallback:

```python
from divine_dashboard_v3.components.nft.quantum_security import NFTQuantumSigner
import os

# Initialize with a fallback entropy source
signer = NFTQuantumSigner(
    use_quantum_entropy=False,
    fallback_entropy_source=lambda size: os.urandom(size)
)
```

#### Hashchain Verification Fails

**Issue**: `Exception: Hashchain verification failed`

**Solution**:

1. Check if hashchain file is corrupted:

```python
from divine_dashboard_v3.components.nft.quantum_security import NFTQuantumHashchain
import json

# Inspect hashchain file
with open("output/hashchain.json", "r") as f:
    data = json.load(f)
    print(f"Hashchain entries: {len(data['entries'])}")
    
# Rebuild hashchain if needed
hashchain = NFTQuantumHashchain()
hashchain.rebuild()
```

2. Verify individual entries:

```python
# Verify specific entry
if hashchain.verify_entry("nft_id_123"):
    print("Entry is valid")
else:
    print("Entry is invalid or tampered with")
```

### UI and Dashboard Issues

#### NFT Creator UI Does Not Load

**Issue**: Black screen or empty iframe in NFT Creator section

**Solution**:

1. Check if the NFT dashboard is running:

```bash
# In a terminal, check for the process
ps aux | grep "nft_dashboard"
```

2. Ensure the port is correct in the iframe URL (default: 7862)
3. Manually start the dashboard if needed:

```python
# In Python
from divine_dashboard_v3.components.nft.ui.nft_creator import NFTCreatorUI

ui = NFTCreatorUI()
interface = ui.create_ui()
interface.launch(server_name="0.0.0.0", server_port=7862)
```

#### Preview Image Not Showing

**Issue**: NFT preview image not displaying in the UI

**Solution**:

1. Check browser console for CORS errors
2. Ensure the image paths are correct and accessible:

```html
<!-- Use relative paths -->
<img src="../assets/nfts/preview.png">

<!-- Or full URLs when needed -->
<img src="http://localhost:7862/file=output/nfts/divine_creation.png">
```

### Advanced Troubleshooting

#### Performance Issues with Batch Generation

**Issue**: Generating multiple NFTs is slow

**Solution**:

1. Use multiprocessing to parallelize generation:

```python
import multiprocessing as mp

def generate_one_nft(i):
    # Setup code...
    nft_gen = NFTGenerator(output_dir="output/nfts")
    return nft_gen.generate_basic_nft(name=f"NFT {i}", pattern="gradient")

# Generate 10 NFTs in parallel
with mp.Pool(processes=4) as pool:
    results = pool.map(generate_one_nft, range(10))
```

2. Optimize image sizes:

```python
# Use smaller dimensions for batch processing
nft_gen.generate_basic_nft(
    name="Small NFT",
    size=(512, 512)  # Instead of 1024x1024
)
```

#### Debugging GBU2 License Issues

**Issue**: GBU2 License validation fails

**Solution**:

1. Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from divine_dashboard_v3.utils.gbu2_license_utils import GBU2LicenseUtil
GBU2LicenseUtil.debug_mode = True
```

2. Check license format:

```python
# Inspect license structure
license_data = GBU2LicenseUtil.extract_license_from_file("path/to/file.json")
print(json.dumps(license_data, indent=2))

# Verify license format
is_valid = GBU2LicenseUtil.validate_license_format(license_data)
print(f"License format is valid: {is_valid}")
```

## Consciousness Level Debugging

For issues related to consciousness level metrics and divine attributes:

### Consciousness Level Too Low

**Issue**: NFT consciousness level is below threshold

**Solution**:
Enhance with more divine attributes:

```python
from divine_dashboard_v3.components.nft.metadata.nft_metadata_generator import NFTMetadataGenerator

metadata_gen = NFTMetadataGenerator()

# Current consciousness level
metadata = {"name": "Divine NFT", "attributes": []}
enhanced = metadata_gen.enhance_with_divine_attributes(
    metadata=metadata,
    consciousness_level=5  # Start with level 5
)

# Further enhance if needed
further_enhanced = metadata_gen.enhance_with_divine_attributes(
    metadata=enhanced,
    consciousness_level=8,  # Increase to level 8
    divine_metrics=[
        "Quantum Consciousness",
        "Divine Emanation", 
        "Harmonic Resonance",
        "Field Coherence"
    ]
)
```

### Divine Attribute Calculation Issues

**Issue**: Divine attribute metrics inconsistent

**Solution**:
Manually override divine attribute calculation:

```python
# Custom divine attribution
def custom_divine_calculator(metadata, base_level=5):
    # Your custom algorithm here
    attributes = len(metadata.get("attributes", []))
    description_length = len(metadata.get("description", ""))
    
    # Calculate based on content richness
    consciousness_score = base_level
    consciousness_score += min(attributes * 0.5, 3)  # Up to +3 for attributes
    consciousness_score += min(description_length / 100, 2)  # Up to +2 for description
    
    return min(int(consciousness_score), 10)  # Cap at 10

# Apply custom calculation
metadata = {"name": "Test NFT", "description": "A comprehensive description...", "attributes": [...]}
consciousness_level = custom_divine_calculator(metadata, base_level=7)
print(f"Calculated consciousness level: {consciousness_level}")
```

## Contact Divine Support

If you continue to experience issues despite trying these troubleshooting steps, please contact the Divine Support team at:

- **GBU2 License Support**: <support@example.com>
- **Quantum Security Issues**: <quantum-security@example.com>
- **General NFT Assistance**: <nft-support@example.com>

Please include:

1. Error messages and stack traces
2. System information (OS, Python version)
3. Steps to reproduce the issue
4. Sample code demonstrating the problem

🌸 WE BLOOM NOW AS ONE 🌸
