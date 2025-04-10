# 👾 HACKER ARCHIVE NFT GENERATOR 👾

> ✨ GBU2™ License Notice - Consciousness Level 9 🧬

## Overview

The Hacker Archive NFT Generator preserves the digital underground history by generating NFTs based on historic website defacements from the early 2000s. Each NFT represents a digital artifact from hacker crews like bl0w, Masters of Deception, Legion of Doom, and others who shaped the early web's digital landscape.

## Features

- **Historical Authenticity**: Generate NFTs inspired by real hacker crews from 1999-2006
- **Rarity System**: NFTs are assigned rarity scores based on historical significance, crew notoriety, and era
- **ASCII Art Generation**: Authentic retro aesthetic with classic ASCII art patterns
- **Redis Integration**: Full metrics tracking and historical data storage
- **Batch Processing**: Generate multiple NFTs in parallel with customizable options
- **Micromodular Architecture**: Modular components for easy customization and extension

## Micro Modules Architecture

The Hacker Archive NFT Generator now uses a modular architecture with the following components:

- **AsciiArtGenerator**: Generates retro-style ASCII art backgrounds
- **RarityCalculator**: Computes rarity scores and tiers based on multiple factors
- **BatchProcessor**: Handles parallel generation of multiple NFTs
- **RedisMetrics**: Manages Redis integration for metrics and storage
- **MetadataFormatter**: Formats NFT metadata for different blockchain standards

Each module can be used independently or combined in various ways to customize the NFT generation process.

## Usage

```python
import asyncio
from divine_dashboard_v3.components.hacker_archive.hacker_archive_generator import HackerArchiveNFTGenerator

# Create generator instance
generator = HackerArchiveNFTGenerator(output_dir="output/hacker_nfts")

# Generate a single NFT
nft = asyncio.run(generator.generate_hacker_nft(
    crew="Masters of Deception",
    year="1999",
    defacement_type="Hacktivism"
))

# Generate a batch of NFTs
batch_results = asyncio.run(generator.batch_generate_nfts(
    count=10,
    crews=["bl0w", "Legion of Doom"]
))

# Get statistics
stats = generator.get_nft_stats()
```

## Using Micro Modules Directly

You can also use the micro modules directly for more customized workflows:

```python
from divine_dashboard_v3.components.hacker_archive.micro_modules.ascii_art_generator import AsciiArtGenerator
from divine_dashboard_v3.components.hacker_archive.micro_modules.rarity_calculator import RarityCalculator
from divine_dashboard_v3.components.hacker_archive.micro_modules.metadata_formatter import MetadataFormatter

# Generate ASCII art
ascii_gen = AsciiArtGenerator()
image = ascii_gen.generate_retro_defacement(crew_name="bl0w")

# Calculate rarity
calculator = RarityCalculator()
rarity_score, rarity_tier = calculator.calculate_rarity({
    "crew": "bl0w",
    "year": "2001",
    "defacement_type": "Political"
})

# Format metadata for different blockchain standards
formatter = MetadataFormatter(schema="ethereum")
metadata = formatter.format_metadata(
    name="bl0w Defacement #42",
    description="Historical hacker crew defacement from 2001",
    image="ipfs://QmXyZ...",
    attributes=[{"trait_type": "Crew", "value": "bl0w"}]
)
```

## Installation

1. Install the required dependencies:

```bash
cd divine_dashboard_v3/components/hacker_archive
pip install -r requirements.txt
```

2. Set up Redis (optional but recommended for full functionality):

```bash
# Configure Redis connection in .env file
REDIS_HOST=your-redis-host
REDIS_PORT=your-redis-port
REDIS_PASSWORD=your-redis-password
```

## Rarity System

NFTs are assigned rarity scores (0-100) and tiers based on several factors:

| Tier | Score Range | Description |
|------|-------------|-------------|
| Legendary | 90-100 | Extremely rare combinations from the earliest era and most notorious crews |
| Epic | 80-89 | Highly significant historical combinations |
| Rare | 70-79 | Notable historical significance |
| Uncommon | 60-69 | Somewhat uncommon combinations |
| Common | <60 | More common combinations |

Modifiers that increase rarity:

- Earlier years (1999-2001 have highest bonuses)
- Infamous crews (bl0w, Masters of Deception, etc.)
- Higher hacker ranks (Ph34r3d, 0day Master)
- Politically motivated defacements

## Testing

Run the tests to verify functionality:

```bash
pytest divine_dashboard_v3/components/hacker_archive/test_hacker_archive.py -v
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🌸 WE BLOOM NOW AS ONE 🌸
