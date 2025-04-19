# Divine NFT Command Line Reference

✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------

This documentation is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

🌸 WE BLOOM NOW AS ONE 🌸

## Core Commands

### NFT Generation

#### Generate Basic NFT

```bash
python -m divine_dashboard_v3.cli.nft_tools generate \
  --name "Divine Bloom #42" \
  --pattern gradient \
  --colors "#3498db,#9b59b6,#2ecc71" \
  --output-dir ./output/nfts
```

Options:

- `--name`: Name of the NFT (required)
- `--pattern`: Pattern type (gradient, circles, squares, abstract)
- `--colors`: Comma-separated hex color codes
- `--output-dir`: Output directory for NFT files
- `--size`: Image size in pixels (e.g., 1024x1024)
- `--seed`: Random seed for reproducible generation
- `--consciousness-level`: Consciousness level (1-10)

#### Generate NFT Collection

```bash
python -m divine_dashboard_v3.cli.nft_tools collection \
  --config collection_config.json \
  --count 10 \
  --output-dir ./output/collection \
  --quantum-security
```

Options:

- `--config`: Path to collection configuration file
- `--count`: Number of NFTs to generate
- `--output-dir`: Output directory for collection
- `--quantum-security`: Enable quantum security features
- `--hashchain`: Generate provenance hashchain
- `--progress`: Show progress bar

#### Batch Process Images

```bash
python -m divine_dashboard_v3.cli.nft_tools batch-process \
  --input-dir ./input_images \
  --output-dir ./output/processed \
  --filter abstract \
  --apply-divine-attributes
```

Options:

- `--input-dir`: Directory with input images
- `--output-dir`: Output directory for processed images
- `--filter`: Apply filter (abstract, quantum, divine)
- `--apply-divine-attributes`: Add divine attributes to metadata
- `--threads`: Number of processing threads

---

### Metadata Management

#### Generate Metadata

```bash
python -m divine_dashboard_v3.cli.nft_tools metadata \
  --name "Divine Bloom #42" \
  --description "A divine creation from the quantum realm" \
  --image "divine_bloom_42.png" \
  --output ./output/metadata/divine_bloom_42.json \
  --consciousness-level 8
```

Options:

- `--name`: NFT name (required)
- `--description`: NFT description
- `--image`: Image file name or path
- `--output`: Output JSON file path
- `--attributes`: JSON string or file path with attributes
- `--consciousness-level`: Consciousness level (1-10)
- `--schema`: JSON schema for validation

#### Validate Metadata

```bash
python -m divine_dashboard_v3.cli.nft_tools validate-metadata \
  --input ./output/metadata/divine_bloom_42.json \
  --schema ./schemas/nft_metadata_schema.json
```

Options:

- `--input`: Input metadata file (or directory)
- `--schema`: JSON schema for validation
- `--recursive`: Process directories recursively
- `--report`: Generate validation report

#### Enhance Metadata

```bash
python -m divine_dashboard_v3.cli.nft_tools enhance-metadata \
  --input ./output/metadata \
  --consciousness-level 8 \
  --divine-metrics "harmony,resonance,bloom" \
  --recursive
```

Options:

- `--input`: Input metadata file or directory
- `--consciousness-level`: Consciousness level (1-10)
- `--divine-metrics`: Comma-separated divine metrics to include
- `--recursive`: Process directories recursively
- `--overwrite`: Overwrite existing files

---

### Quantum Security

#### Generate Quantum Keypair

```bash
python -m divine_dashboard_v3.cli.quantum_tools generate-keys \
  --output-dir ./keys \
  --algorithm dilithium \
  --key-size 384
```

Options:

- `--output-dir`: Directory to save keys
- `--algorithm`: Signing algorithm (dilithium, falcon, sphincs)
- `--key-size`: Key size in bits
- `--secure`: Enable secure key storage

#### Sign NFT

```bash
python -m divine_dashboard_v3.cli.quantum_tools sign \
  --input ./output/metadata/divine_bloom_42.json \
  --key ./keys/private_key.pem \
  --output ./output/metadata/divine_bloom_42_signed.json
```

Options:

- `--input`: Input file to sign
- `--key`: Private key file
- `--output`: Output signed file
- `--algorithm`: Signing algorithm
- `--embed`: Embed signature in metadata

#### Verify Signature

```bash
python -m divine_dashboard_v3.cli.quantum_tools verify \
  --input ./output/metadata/divine_bloom_42_signed.json \
  --key ./keys/public_key.pem
```

Options:

- `--input`: Input file to verify
- `--key`: Public key file
- `--signature`: External signature file (if not embedded)

#### Manage Hashchain

```bash
python -m divine_dashboard_v3.cli.quantum_tools hashchain \
  --action create \
  --storage-path ./output/hashchain.json
```

Options:

- `--action`: Action (create, add, verify, export)
- `--storage-path`: Path to hashchain file
- `--nft-id`: NFT ID for add/verify actions
- `--metadata`: Path to NFT metadata for add action
- `--export-format`: Format for export action (json, txt)

#### Collect Entropy

```bash
python -m divine_dashboard_v3.cli.quantum_tools entropy \
  --size 64 \
  --sources "quantum,system,timing,network" \
  --output ./entropy.bin \
  --analyze
```

Options:

- `--size`: Entropy size in bytes
- `--sources`: Comma-separated entropy sources
- `--output`: Output file for entropy
- `--analyze`: Analyze entropy quality
- `--visualize`: Generate entropy visualization

---

### Blockchain Integration

#### Mint NFT

```bash
python -m divine_dashboard_v3.cli.blockchain_tools mint \
  --image ./output/nfts/divine_bloom_42.png \
  --metadata ./output/metadata/divine_bloom_42.json \
  --recipient 0x123456789abcdef... \
  --chain ethereum \
  --testnet
```

Options:

- `--image`: Path to NFT image
- `--metadata`: Path to NFT metadata
- `--recipient`: Recipient wallet address
- `--chain`: Blockchain (ethereum, polygon, solana)
- `--testnet`: Use testnet instead of mainnet
- `--gas-limit`: Gas limit for transaction
- `--private-key`: Private key file

#### Transfer NFT

```bash
python -m divine_dashboard_v3.cli.blockchain_tools transfer \
  --token-id 42 \
  --from 0x123456789abcdef... \
  --to 0xabcdef123456789... \
  --chain ethereum \
  --testnet
```

Options:

- `--token-id`: NFT token ID
- `--from`: Current owner address
- `--to`: New owner address
- `--chain`: Blockchain
- `--testnet`: Use testnet
- `--private-key`: Private key file

#### Get NFT Data

```bash
python -m divine_dashboard_v3.cli.blockchain_tools get-data \
  --token-id 42 \
  --chain ethereum \
  --testnet \
  --output ./nft_data.json
```

Options:

- `--token-id`: NFT token ID
- `--chain`: Blockchain
- `--testnet`: Use testnet
- `--output`: Output file for NFT data

---

### UI Tools

#### Launch NFT Creator UI

```bash
python -m divine_dashboard_v3.cli.ui_tools nft-creator \
  --output-dir ./output/nfts \
  --title "Divine NFT Creator" \
  --theme dark \
  --port 7862
```

Options:

- `--output-dir`: Directory to save NFTs
- `--title`: UI title
- `--theme`: UI theme (default, dark, light)
- `--port`: Port for web UI
- `--share`: Create shareable link

#### Launch Divine Dashboard

```bash
python -m divine_dashboard_v3.cli.ui_tools dashboard \
  --config ./config/dashboard.json \
  --port 7861
```

Options:

- `--config`: Dashboard configuration file
- `--port`: Port for dashboard
- `--open-browser`: Open browser automatically
- `--debug`: Enable debug mode

---

### Test and Coverage

#### Run Tests

```bash
python -m divine_dashboard_v3.cli.test_tools run \
  --component nft-generator \
  --verbose
```

Options:

- `--component`: Component to test (all, nft-generator, metadata, quantum, blockchain)
- `--verbose`: Verbose output
- `--junit-xml`: Generate JUnit XML report
- `--coverage`: Generate coverage report

#### Generate Coverage Report

```bash
python -m divine_dashboard_v3.cli.test_tools coverage \
  --input ./coverage.json \
  --format markdown \
  --output ./coverage_report.md \
  --target 90.0
```

Options:

- `--input`: Coverage data file
- `--format`: Report format (markdown, html, json)
- `--output`: Output report file
- `--target`: Target coverage percentage
- `--include-recommendations`: Include improvement recommendations

---

### License Tools

#### Apply GBU2 License

```bash
python -m divine_dashboard_v3.cli.license_tools apply \
  --target ./components \
  --recursive \
  --file-types ".py,.md,.html,.js" \
  --consciousness-level 8
```

Options:

- `--target`: Target file or directory
- `--recursive`: Process directories recursively
- `--file-types`: Comma-separated file extensions
- `--consciousness-level`: Consciousness level (1-10)
- `--dry-run`: Show changes without applying

#### Validate License

```bash
python -m divine_dashboard_v3.cli.license_tools validate \
  --target ./components \
  --recursive \
  --report ./license_report.md
```

Options:

- `--target`: Target file or directory
- `--recursive`: Process directories recursively
- `--report`: Generate validation report
- `--fail-on-missing`: Exit with error if license missing

🌸 WE BLOOM NOW AS ONE 🌸
