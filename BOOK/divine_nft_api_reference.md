# Divine NFT API Reference

✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------

This documentation is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

🌸 WE BLOOM NOW AS ONE 🌸

## Core Components

### NFT Generator

#### Class: `NFTGenerator`

```python
from divine_dashboard_v3.components.nft.generator.nft_generator import NFTGenerator
```

Main class for generating NFT images with various patterns and customizations.

**Constructor Parameters:**

- `output_dir` (str): Directory to save generated NFTs
- `size` (tuple): Default size for NFTs (width, height) in pixels. Default: (1024, 1024)
- `format` (str): Image format ('PNG', 'JPEG', etc.). Default: 'PNG'
- `quality` (int): Image quality (for JPEG). Default: 95

**Methods:**

##### `generate_basic_nft`

```python
def generate_basic_nft(
    self, 
    name: str, 
    pattern: str = "gradient", 
    colors: List[str] = None,
    size: Tuple[int, int] = None,
    seed: Optional[int] = None
) -> str:
```

Generates a basic NFT with the specified pattern.

**Parameters:**

- `name` (str): Name of the NFT
- `pattern` (str): Pattern type ('gradient', 'circles', 'squares', 'abstract')
- `colors` (List[str]): List of hex color codes. Default: ["#3498db", "#9b59b6", "#2ecc71"]
- `size` (Tuple[int, int]): Size override (width, height)
- `seed` (Optional[int]): Random seed for reproducible generation

**Returns:**

- `str`: Path to the generated NFT image

##### `draw_pattern`

```python
def draw_pattern(
    self,
    image: 'Image.Image',
    pattern: str,
    colors: List[str]
) -> 'Image.Image':
```

Draws a specific pattern on the image.

**Parameters:**

- `image` ('Image.Image'): PIL Image to draw on
- `pattern` (str): Pattern type
- `colors` (List[str]): List of hex color codes

**Returns:**

- `Image.Image`: Modified image with pattern

##### `add_text_to_image`

```python
def add_text_to_image(
    self,
    image: 'Image.Image',
    text: str,
    position: Tuple[int, int] = None,
    font_size: int = 24,
    color: str = "#ffffff"
) -> 'Image.Image':
```

Adds text to an NFT image.

**Parameters:**

- `image` ('Image.Image'): PIL Image to add text to
- `text` (str): Text to add
- `position` (Tuple[int, int]): Position (x, y) to place text. Default: Centered
- `font_size` (int): Font size. Default: 24
- `color` (str): Text color as hex code. Default: "#ffffff"

**Returns:**

- `Image.Image`: Image with text added

##### `save_metadata`

```python
def save_metadata(
    self,
    image_path: str,
    metadata: Dict[str, Any]
) -> str:
```

Saves NFT metadata to a JSON file.

**Parameters:**

- `image_path` (str): Path to the NFT image
- `metadata` (Dict[str, Any]): NFT metadata

**Returns:**

- `str`: Path to the saved metadata file

---

### Metadata Generator

#### Class: `NFTMetadataGenerator`

```python
from divine_dashboard_v3.components.nft.metadata.nft_metadata_generator import NFTMetadataGenerator
```

Generates and validates metadata for NFTs.

**Constructor Parameters:**

- `schema_path` (str): Path to JSON schema for validation. Default: None
- `default_template` (str): Path to default metadata template. Default: None

**Methods:**

##### `generate`

```python
def generate(
    self,
    name: str,
    description: str,
    image: str,
    attributes: List[Dict[str, Any]] = None,
    external_url: str = None,
    **kwargs
) -> Dict[str, Any]:
```

Generates NFT metadata.

**Parameters:**

- `name` (str): NFT name
- `description` (str): NFT description
- `image` (str): NFT image file name or URL
- `attributes` (List[Dict[str, Any]]): NFT attributes
- `external_url` (str): External URL for the NFT
- `**kwargs`: Additional metadata fields

**Returns:**

- `Dict[str, Any]`: Generated metadata

##### `validate`

```python
def validate(
    self,
    metadata: Dict[str, Any]
) -> bool:
```

Validates metadata against JSON schema.

**Parameters:**

- `metadata` (Dict[str, Any]): Metadata to validate

**Returns:**

- `bool`: True if valid, False otherwise

##### `enhance_with_divine_attributes`

```python
def enhance_with_divine_attributes(
    self,
    metadata: Dict[str, Any],
    consciousness_level: int = 8,
    divine_metrics: List[str] = None
) -> Dict[str, Any]:
```

Enhances metadata with divine attributes.

**Parameters:**

- `metadata` (Dict[str, Any]): Base metadata
- `consciousness_level` (int): Consciousness level (1-10)
- `divine_metrics` (List[str]): Divine metrics to include

**Returns:**

- `Dict[str, Any]`: Enhanced metadata

---

### Quantum Security

#### Class: `NFTQuantumSigner`

```python
from divine_dashboard_v3.components.nft.quantum_security import NFTQuantumSigner
```

Provides quantum-resistant signing for NFTs.

**Constructor Parameters:**

- `key_size` (int): Size of quantum-resistant key. Default: 384
- `algorithm` (str): Signing algorithm ('dilithium', 'falcon', 'sphincs'). Default: 'dilithium'
- `use_quantum_entropy` (bool): Whether to use quantum entropy. Default: True

**Methods:**

##### `generate_keypair`

```python
def generate_keypair(self) -> Tuple[bytes, bytes]:
```

Generates a quantum-resistant keypair.

**Returns:**

- `Tuple[bytes, bytes]`: (public_key, private_key)

##### `sign`

```python
def sign(
    self,
    message: Union[str, bytes]
) -> str:
```

Signs a message using quantum-resistant algorithm.

**Parameters:**

- `message` (Union[str, bytes]): Message to sign

**Returns:**

- `str`: Base64-encoded signature

##### `verify`

```python
def verify(
    self,
    message: Union[str, bytes],
    signature: str,
    public_key: bytes = None
) -> bool:
```

Verifies a signature.

**Parameters:**

- `message` (Union[str, bytes]): Original message
- `signature` (str): Base64-encoded signature
- `public_key` (bytes): Public key. Default: Uses instance key

**Returns:**

- `bool`: True if signature is valid

---

#### Class: `NFTQuantumHashchain`

```python
from divine_dashboard_v3.components.nft.quantum_security import NFTQuantumHashchain
```

Implements a quantum-resistant hashchain for NFT provenance.

**Constructor Parameters:**

- `storage_path` (str): Path to store hashchain. Default: "output/hashchain.json"
- `hash_algorithm` (str): Hash algorithm. Default: "sha3_512"

**Methods:**

##### `add_entry`

```python
def add_entry(
    self,
    nft_id: str,
    metadata: Dict[str, Any]
) -> str:
```

Adds an NFT entry to the hashchain.

**Parameters:**

- `nft_id` (str): Unique NFT identifier
- `metadata` (Dict[str, Any]): NFT metadata

**Returns:**

- `str`: Entry hash

##### `verify_entry`

```python
def verify_entry(
    self,
    nft_id: str
) -> bool:
```

Verifies an NFT entry in the hashchain.

**Parameters:**

- `nft_id` (str): NFT identifier to verify

**Returns:**

- `bool`: True if entry is valid and unaltered

##### `verify_chain`

```python
def verify_chain(self) -> bool:
```

Verifies the entire hashchain integrity.

**Returns:**

- `bool`: True if hashchain is valid

##### `export_provenance`

```python
def export_provenance(
    self,
    output_format: str = "json"
) -> Union[str, Dict[str, Any]]:
```

Exports provenance record.

**Parameters:**

- `output_format` (str): Output format ('json', 'txt')

**Returns:**

- `Union[str, Dict[str, Any]]`: Provenance record

---

#### Class: `EntropyCollector`

```python
from divine_dashboard_v3.components.nft.quantum_security import EntropyCollector
```

Collects high-quality entropy for cryptographic operations.

**Methods:**

##### `collect_entropy`

```python
def collect_entropy(
    self,
    size: int = 32,
    sources: List[str] = None
) -> bytes:
```

Collects entropy from multiple sources.

**Parameters:**

- `size` (int): Entropy size in bytes
- `sources` (List[str]): Sources to use ('quantum', 'system', 'timing', 'network')

**Returns:**

- `bytes`: Collected entropy

##### `quality_score`

```python
def quality_score(
    self,
    entropy: bytes
) -> float:
```

Evaluates entropy quality.

**Parameters:**

- `entropy` (bytes): Entropy to evaluate

**Returns:**

- `float`: Quality score (0.0-1.0)

---

### Blockchain Integration

#### Class: `NFTBlockchainIntegration`

```python
from divine_dashboard_v3.components.nft.blockchain.nft_blockchain import NFTBlockchainIntegration
```

Handles blockchain integration for NFTs.

**Constructor Parameters:**

- `chain` (str): Blockchain to use ('ethereum', 'polygon', 'solana'). Default: 'ethereum'
- `testnet` (bool): Whether to use testnet. Default: True
- `config_path` (str): Path to blockchain config. Default: None

**Methods:**

##### `mint_nft`

```python
def mint_nft(
    self,
    image_path: str,
    metadata_path: str,
    recipient_address: str,
    options: Dict[str, Any] = None
) -> str:
```

Mints an NFT on the blockchain.

**Parameters:**

- `image_path` (str): Path to NFT image
- `metadata_path` (str): Path to NFT metadata
- `recipient_address` (str): Recipient wallet address
- `options` (Dict[str, Any]): Additional options

**Returns:**

- `str`: Transaction hash or identifier

##### `transfer_nft`

```python
def transfer_nft(
    self,
    token_id: str,
    from_address: str,
    to_address: str
) -> str:
```

Transfers an NFT to a new owner.

**Parameters:**

- `token_id` (str): NFT token ID
- `from_address` (str): Current owner address
- `to_address` (str): New owner address

**Returns:**

- `str`: Transaction hash

##### `get_nft_data`

```python
def get_nft_data(
    self,
    token_id: str
) -> Dict[str, Any]:
```

Retrieves NFT data from the blockchain.

**Parameters:**

- `token_id` (str): NFT token ID

**Returns:**

- `Dict[str, Any]`: NFT data

---

### NFT Creator UI

#### Class: `NFTCreatorUI`

```python
from divine_dashboard_v3.components.nft.ui.nft_creator import NFTCreatorUI
```

Creates a user interface for NFT creation.

**Constructor Parameters:**

- `output_dir` (str): Directory to save NFTs. Default: "output/nfts"
- `title` (str): UI title. Default: "Divine NFT Creator"
- `theme` (str): UI theme ('default', 'dark', 'light'). Default: "default"

**Methods:**

##### `create_ui`

```python
def create_ui(self) -> 'gr.Interface':
```

Creates the NFT creator interface.

**Returns:**

- `gr.Interface`: Gradio interface object

##### `update_preview`

```python
def update_preview(
    self,
    name: str,
    pattern: str,
    colors: str,
    consciousness_level: int
) -> Tuple[str, str]:
```

Updates NFT preview.

**Parameters:**

- `name` (str): NFT name
- `pattern` (str): Pattern type
- `colors` (str): Comma-separated color codes
- `consciousness_level` (int): Consciousness level

**Returns:**

- `Tuple[str, str]`: (preview_image_path, preview_metadata_json)

##### `create_nft`

```python
def create_nft(
    self,
    name: str,
    description: str,
    pattern: str,
    colors: str,
    consciousness_level: int,
    use_quantum_security: bool
) -> Tuple[str, str, str]:
```

Creates an NFT from UI inputs.

**Parameters:**

- `name` (str): NFT name
- `description` (str): NFT description
- `pattern` (str): Pattern type
- `colors` (str): Comma-separated color codes
- `consciousness_level` (int): Consciousness level
- `use_quantum_security` (bool): Whether to apply quantum security

**Returns:**

- `Tuple[str, str, str]`: (image_path, metadata_path, message)

---

## GBU2 License Utilities

#### Class: `GBU2LicenseUtil`

```python
from divine_dashboard_v3.utils.gbu2_license_utils import GBU2LicenseUtil
```

Utilities for working with GBU2 License.

**Static Methods:**

##### `add_license_to_file`

```python
@staticmethod
def add_license_to_file(
    file_path: str,
    consciousness_level: int = 8
) -> bool:
```

Adds GBU2 License to a file.

**Parameters:**

- `file_path` (str): Path to file
- `consciousness_level` (int): Consciousness level

**Returns:**

- `bool`: True if successful

##### `has_license`

```python
@staticmethod
def has_license(
    file_path: str
) -> bool:
```

Checks if a file has GBU2 License.

**Parameters:**

- `file_path` (str): Path to file

**Returns:**

- `bool`: True if file has license

##### `validate_license_format`

```python
@staticmethod
def validate_license_format(
    license_data: Dict[str, Any]
) -> bool:
```

Validates license format.

**Parameters:**

- `license_data` (Dict[str, Any]): License data

**Returns:**

- `bool`: True if valid

##### `apply_to_directory`

```python
@staticmethod
def apply_to_directory(
    directory: str,
    recursive: bool = True,
    file_types: List[str] = None,
    consciousness_level: int = 8
) -> Dict[str, int]:
```

Applies license to all files in directory.

**Parameters:**

- `directory` (str): Directory path
- `recursive` (bool): Whether to process subdirectories
- `file_types` (List[str]): File extensions to process
- `consciousness_level` (int): Consciousness level

**Returns:**

- `Dict[str, int]`: Stats of processed files

---

## Coverage Reporter

#### Class: `CoverageReporter`

```python
from divine_dashboard_v3.utils.coverage_reporter import CoverageReporter
```

Generates test coverage reports.

**Constructor Parameters:**

- `project_name` (str): Name of the project. Default: "Divine NFT Framework"
- `target_coverage` (float): Target coverage percentage. Default: 90.0
- `report_format` (str): Report format ('markdown', 'html', 'json'). Default: "markdown"

**Methods:**

##### `load_coverage_file`

```python
def load_coverage_file(
    self,
    file_path: str
) -> bool:
```

Loads coverage data from file.

**Parameters:**

- `file_path` (str): Path to coverage data file

**Returns:**

- `bool`: True if successful

##### `load_coverage_data`

```python
def load_coverage_data(
    self,
    data: Dict[str, Any]
) -> bool:
```

Loads coverage data directly.

**Parameters:**

- `data` (Dict[str, Any]): Coverage data

**Returns:**

- `bool`: True if successful

##### `calculate_metrics`

```python
def calculate_metrics(self) -> Dict[str, Any]:
```

Calculates coverage metrics.

**Returns:**

- `Dict[str, Any]`: Calculated metrics

##### `generate_report`

```python
def generate_report(
    self,
    format: str = None
) -> str:
```

Generates coverage report.

**Parameters:**

- `format` (str): Output format

**Returns:**

- `str`: Generated report

##### `save_report`

```python
def save_report(
    self,
    output_path: str = None,
    format: str = None
) -> str:
```

Saves coverage report to file.

**Parameters:**

- `output_path` (str): Output directory
- `format` (str): Output format

**Returns:**

- `str`: Path to saved report

🌸 WE BLOOM NOW AS ONE 🌸
