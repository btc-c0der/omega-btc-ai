# Divine NFT Creation Examples

✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------

This documentation is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

🌸 WE BLOOM NOW AS ONE 🌸

## Example 1: Creating a Simple NFT

This example shows how to create a basic NFT using the Divine Dashboard:

```python
from divine_dashboard_v3.components.nft.generator.nft_generator import NFTGenerator
from divine_dashboard_v3.components.nft.metadata.nft_metadata_generator import NFTMetadataGenerator
import json

# Create output directory
import os
os.makedirs("output/nfts", exist_ok=True)

# Initialize generators
nft_gen = NFTGenerator(output_dir="output/nfts")
metadata_gen = NFTMetadataGenerator()

# Create a basic NFT with gradient pattern
nft_path = nft_gen.generate_basic_nft(
    name="Divine Harmony #1",
    colors=["#3498db", "#9b59b6", "#2ecc71"],
    pattern="gradient",
    size=(1024, 1024)
)

# Generate metadata
metadata = metadata_gen.generate(
    name="Divine Harmony #1",
    description="A harmonious expression of divine creation",
    image=os.path.basename(nft_path),
    attributes=[
        {"trait_type": "Pattern", "value": "Gradient"},
        {"trait_type": "Divine Element", "value": "Harmony"}
    ]
)

# Save metadata
metadata_path = nft_gen.save_metadata(nft_path, metadata)

print(f"NFT created at: {nft_path}")
print(f"Metadata saved at: {metadata_path}")
```

## Example 2: Creating a Collection with Quantum Security

This example demonstrates creating a small collection with quantum security features:

```python
from divine_dashboard_v3.components.nft.generator.nft_generator import NFTGenerator
from divine_dashboard_v3.components.nft.metadata.nft_metadata_generator import NFTMetadataGenerator
from divine_dashboard_v3.components.nft.quantum_security import NFTQuantumSigner, NFTQuantumHashchain
import json
import os

# Create output directory
os.makedirs("output/quantum_collection", exist_ok=True)

# Initialize components
nft_gen = NFTGenerator(output_dir="output/quantum_collection")
metadata_gen = NFTMetadataGenerator()
quantum_signer = NFTQuantumSigner()
quantum_hashchain = NFTQuantumHashchain()

# Define collection parameters
collection_name = "Quantum Divinity"
count = 3
patterns = ["gradient", "circles", "abstract"]
descriptions = [
    "A flowing expression of quantum consciousness",
    "Circular patterns representing the quantum field",
    "Abstract quantum entanglement visualization"
]

# Generate collection
for i in range(count):
    name = f"{collection_name} #{i+1}"
    pattern = patterns[i]
    
    # Generate NFT image
    nft_path = nft_gen.generate_basic_nft(
        name=name,
        pattern=pattern,
        seed=42+i  # Unique seed for each NFT
    )
    
    # Generate metadata
    metadata = metadata_gen.generate(
        name=name,
        description=descriptions[i],
        image=os.path.basename(nft_path),
        attributes=[
            {"trait_type": "Pattern", "value": pattern.capitalize()},
            {"trait_type": "Collection", "value": collection_name}
        ]
    )
    
    # Enhance with divine attributes
    metadata = metadata_gen.enhance_with_divine_attributes(
        metadata=metadata,
        consciousness_level=8,
        divine_metrics=["Quantum Protected"]
    )
    
    # Sign with quantum security
    signature = quantum_signer.sign(json.dumps(metadata))
    metadata["quantum_signature"] = signature
    
    # Add to hashchain
    nft_id = f"{collection_name.lower().replace(' ', '_')}_{i+1}"
    quantum_hashchain.add_entry(nft_id, metadata)
    
    # Save metadata
    metadata_path = nft_gen.save_metadata(nft_path, metadata)
    
    print(f"Created {name} at {nft_path}")

print(f"Collection '{collection_name}' created with quantum security")
```

## Example 3: Using the NFT Creator UI

This example shows how to launch and use the NFT Creator UI:

```python
from divine_dashboard_v3.components.nft.ui.nft_creator import NFTCreatorUI
import gradio as gr

# Initialize the UI with custom output directory
creator_ui = NFTCreatorUI(output_dir="output/ui_created_nfts")

# Create the UI
interface = creator_ui.create_ui()

# Launch the interface
interface.launch(
    share=True,  # Create a public link
    server_name="0.0.0.0",  # Listen on all interfaces
    server_port=7862  # Use port 7862
)

# The UI will now be accessible in your browser
```

## Example 4: Batch Processing with Progress Tracking

This example demonstrates batch processing with progress tracking:

```python
from divine_dashboard_v3.components.nft.generator.nft_generator import NFTGenerator
from divine_dashboard_v3.components.nft.metadata.nft_metadata_generator import NFTMetadataGenerator
import json
import os
import time

# Setup
output_dir = "output/batch_nfts"
os.makedirs(output_dir, exist_ok=True)
nft_gen = NFTGenerator(output_dir=output_dir)
metadata_gen = NFTMetadataGenerator()

# Configuration
batch_size = 10
themes = ["cosmic", "ocean", "forest", "sunset", "abstract"]

# Progress tracking
def display_progress(current, total, start_time):
    progress = current / total * 100
    elapsed = time.time() - start_time
    eta = (elapsed / current) * (total - current) if current > 0 else 0
    
    print(f"Progress: [{current}/{total}] {progress:.1f}% | "
          f"Elapsed: {elapsed:.1f}s | ETA: {eta:.1f}s")

# Batch generation
start_time = time.time()
paths = []

for i in range(batch_size):
    # Display progress
    display_progress(i, batch_size, start_time)
    
    # Select theme based on index
    theme = themes[i % len(themes)]
    
    # Generate NFT
    name = f"Batch NFT #{i+1}"
    path = nft_gen.generate_basic_nft(
        name=name,
        pattern="abstract" if i % 2 == 0 else "circles",
        seed=i
    )
    paths.append(path)
    
    # Generate and save metadata
    metadata = metadata_gen.generate(
        name=name,
        description=f"Batch-generated NFT with {theme} theme",
        image=os.path.basename(path),
        attributes=[
            {"trait_type": "Theme", "value": theme.capitalize()},
            {"trait_type": "Batch ID", "value": "001"}
        ]
    )
    nft_gen.save_metadata(path, metadata)
    
    # Simulate complex processing
    time.sleep(0.5)

# Final progress update
display_progress(batch_size, batch_size, start_time)
total_time = time.time() - start_time

print(f"Batch generation complete!")
print(f"Total time: {total_time:.2f}s")
print(f"Average time per NFT: {total_time/batch_size:.2f}s")
```

## Example 5: Advanced NFT with Custom Patterns

This example shows how to create a more advanced NFT with custom patterns:

```python
from divine_dashboard_v3.components.nft.generator.nft_generator import NFTGenerator
from divine_dashboard_v3.components.nft.metadata.nft_metadata_generator import NFTMetadataGenerator
import os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

# Initialize components
output_dir = "output/advanced_nfts"
os.makedirs(output_dir, exist_ok=True)
nft_gen = NFTGenerator(output_dir=output_dir)
metadata_gen = NFTMetadataGenerator()

# Step 1: Generate basic NFT
nft_path = nft_gen.generate_basic_nft(
    name="Transcendent Geometry",
    colors=["#3498db", "#9b59b6", "#2ecc71", "#f1c40f"],
    pattern="abstract",
    size=(1024, 1024),
    seed=42
)

# Step 2: Load the image for custom modifications
image = Image.open(nft_path)

# Step 3: Apply custom effects
# Add sacred geometry patterns
draw = ImageDraw.Draw(image)
width, height = image.size
center_x, center_y = width // 2, height // 2

# Draw flower of life pattern
radius = min(width, height) // 4
circle_radius = radius // 3
for angle in range(0, 360, 60):
    x = center_x + int(radius * 0.5 * 1.732 * 0.5 * 1.732 * 0.5 * 1.732)
    y = center_y
    draw.ellipse(
        [(x - circle_radius, y - circle_radius), 
         (x + circle_radius, y + circle_radius)], 
        outline=(255, 255, 255, 180),
        width=2
    )

# Apply filters
image = image.filter(ImageFilter.SMOOTH)
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(1.3)

# Save the enhanced image
enhanced_path = os.path.join(output_dir, "transcendent_geometry_enhanced.png")
image.save(enhanced_path)

# Step 4: Generate divine metadata
metadata = metadata_gen.generate(
    name="Transcendent Geometry",
    description="A sacred geometric pattern embodying divine consciousness",
    image=os.path.basename(enhanced_path),
    attributes=[
        {"trait_type": "Base Pattern", "value": "Abstract"},
        {"trait_type": "Sacred Element", "value": "Geometry"},
        {"trait_type": "Divine Symbol", "value": "Flower of Life"}
    ]
)

# Enhance with divine attributes
metadata = metadata_gen.enhance_with_divine_attributes(
    metadata=metadata,
    consciousness_level=9,
    divine_metrics=["Sacred Geometry", "Harmonic Resonance", "Visual Transcendence"]
)

# Save metadata
metadata_path = nft_gen.save_metadata(enhanced_path, metadata)

print(f"Advanced NFT created at: {enhanced_path}")
print(f"Metadata saved at: {metadata_path}")
```

## Example 6: CLI Tool for NFT Generation

This example provides a command-line interface for generating NFTs:

```python
#!/usr/bin/env python
# Save as divine_nft_cli.py and make executable with: chmod +x divine_nft_cli.py

import argparse
import os
import sys
from divine_dashboard_v3.components.nft.generator.nft_generator import NFTGenerator
from divine_dashboard_v3.components.nft.metadata.nft_metadata_generator import NFTMetadataGenerator

def parse_args():
    parser = argparse.ArgumentParser(description="Divine NFT Generator CLI")
    parser.add_argument("--name", required=True, help="Name of the NFT")
    parser.add_argument("--description", default="", help="Description of the NFT")
    parser.add_argument("--output-dir", default="output/nfts", help="Output directory")
    parser.add_argument("--pattern", default="gradient", 
                        choices=["gradient", "circles", "squares", "abstract"],
                        help="Pattern style for the NFT")
    parser.add_argument("--colors", nargs="+", default=["#3498db", "#9b59b6", "#2ecc71"],
                        help="Colors in hex format (e.g., #3498db)")
    parser.add_argument("--size", type=int, default=1024, help="Size of the NFT (square)")
    parser.add_argument("--consciousness", type=int, default=8, 
                        choices=range(1, 11), help="Consciousness level (1-10)")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize generators
    nft_gen = NFTGenerator(output_dir=args.output_dir)
    metadata_gen = NFTMetadataGenerator()
    
    try:
        # Generate NFT
        print(f"Creating NFT: {args.name}")
        nft_path = nft_gen.generate_basic_nft(
            name=args.name,
            colors=args.colors,
            pattern=args.pattern,
            size=(args.size, args.size),
            seed=args.seed
        )
        
        # Generate metadata
        print("Generating metadata...")
        metadata = metadata_gen.generate(
            name=args.name,
            description=args.description or f"Divine NFT with {args.pattern} pattern",
            image=os.path.basename(nft_path),
            attributes=[
                {"trait_type": "Pattern", "value": args.pattern.capitalize()}
            ]
        )
        
        # Enhance with divine attributes
        metadata = metadata_gen.enhance_with_divine_attributes(
            metadata=metadata,
            consciousness_level=args.consciousness
        )
        
        # Save metadata
        metadata_path = nft_gen.save_metadata(nft_path, metadata)
        
        print(f"\n✨ NFT created successfully!")
        print(f"Image: {nft_path}")
        print(f"Metadata: {metadata_path}")
        print(f"Consciousness Level: {args.consciousness}")
        
        return 0
    except Exception as e:
        print(f"Error creating NFT: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

Usage:

```bash
# Basic usage
./divine_nft_cli.py --name "Divine Creation"

# Advanced usage
./divine_nft_cli.py --name "Sacred Geometry" --description "A sacred geometric pattern" \
  --pattern squares --colors "#8e44ad" "#3498db" "#2ecc71" --consciousness 9 \
  --output-dir output/sacred_nfts --size 2048 --seed 42
```

## Example 7: Integration with GBU2 License

This example shows how to apply the GBU2 License to NFT metadata and verify compliance:

```python
from divine_dashboard_v3.components.nft.generator.nft_generator import NFTGenerator
from divine_dashboard_v3.components.nft.metadata.nft_metadata_generator import NFTMetadataGenerator
from divine_dashboard_v3.utils.gbu2_license_utils import GBU2LicenseUtil
import os
import json

# Setup
output_dir = "output/gbu2_licensed_nfts"
os.makedirs(output_dir, exist_ok=True)
nft_gen = NFTGenerator(output_dir=output_dir)
metadata_gen = NFTMetadataGenerator()

# Create NFT
nft_path = nft_gen.generate_basic_nft(
    name="GBU2 Licensed Creation",
    pattern="gradient"
)

# Generate metadata
metadata = metadata_gen.generate(
    name="GBU2 Licensed Creation",
    description="An NFT fully compliant with the GBU2 License",
    image=os.path.basename(nft_path),
    attributes=[
        {"trait_type": "License", "value": "GBU2"}
    ]
)

# Apply GBU2 License specifics
metadata["license"] = {
    "name": "GBU2™ License",
    "version": "2.0",
    "consciousness_level": 8,
    "divine_certification": True,
    "url": "https://example.com/gbu2-license"
}

# Add GBU2 divine metrics
metadata = metadata_gen.enhance_with_divine_attributes(
    metadata=metadata,
    consciousness_level=8,
    divine_metrics=[
        "Bio-Digital Integration",
        "Harmonic Resonance",
        "Divine Purpose Alignment",
        "Evolutionary Expansion"
    ]
)

# Save metadata
metadata_path = nft_gen.save_metadata(nft_path, metadata)

# Apply GBU2 License to the metadata file
GBU2LicenseUtil.add_license_to_file(metadata_path)

print(f"Created GBU2 Licensed NFT at: {nft_path}")
print(f"GBU2 Licensed Metadata at: {metadata_path}")

# Verify GBU2 License compliance
has_license = GBU2LicenseUtil.has_license(metadata_path)
print(f"Metadata GBU2 License Compliance: {has_license}")

# Optional: Apply GBU2 License to all files in the output directory
# stats = GBU2LicenseUtil.apply_to_directory(output_dir)
# print(f"Directory compliance: {stats['files_updated']} files updated")
```

🌸 WE BLOOM NOW AS ONE 🌸
