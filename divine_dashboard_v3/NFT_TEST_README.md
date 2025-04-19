# 🎨 NFT Dashboard Test Suite

This directory contains comprehensive test coverage for the Divine Dashboard v3 NFT components.

## 🧬 Test Coverage Metrics

The test suite aims for a minimum of **90% code coverage** as required by Mr. Elon's specifications. Coverage is measured across:

- NFT Metadata module
- NFT Generator functionality
- NFT Blockchain integration
- NFT Dashboard API
- Server integration with NFT components

## 🚀 Running the Tests

### Prerequisites

Before running the tests, ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Quick Start

To run all tests with coverage reports:

```bash
./run_nft_tests.sh
```

This script will:

1. Set up necessary environment variables
2. Create output directories
3. Run all tests with coverage reporting
4. Generate HTML and XML coverage reports
5. Verify if the 90% coverage target has been met

### Manual Test Execution

To run specific test modules:

```bash
# Run just the component tests
python -m pytest components/nft/test_nft_components.py -v

# Run just the API tests
python -m pytest components/nft/test_nft_api.py -v

# Run server integration tests
python -m pytest test_server_nft_integration.py -v
```

## 📊 Test Structure

### NFT Component Tests (`components/nft/test_nft_components.py`)

Tests for core NFT functionality:

- Metadata creation and manipulation
- Blockchain operations (minting, IPFS uploads)
- NFT generation from images
- Divine metrics calculation
- Integration between components

### NFT API Tests (`components/nft/test_nft_api.py`)

Tests for the NFT API endpoints:

- NFT minting API
- Error handling
- Request validation
- Response formatting

### Server Integration Tests (`test_server_nft_integration.py`)

Tests for integration with the main server:

- Server initialization with NFT components
- Thread management
- Port configuration
- API routing
- Error handling

## 🌈 Divine Metrics

The tests verify that NFTs include the required divine metrics:

- Divine Harmony
- Sacred Balance
- Golden Ratio Alignment
- Cosmic Resonance
- Ethereal Vibrance

## 🔄 Continuous Integration

For continuous integration systems, use:

```bash
python -m pytest --cov=components.nft --cov-report=xml:coverage.xml
```

## 🧪 Test Configuration

Configuration is defined in `pytest.ini` and includes:

- Path configurations
- Marker definitions (asyncio, slow)
- Coverage reporting settings
- Logging configuration

## 🛠️ Troubleshooting

If tests fail due to:

1. **Missing dependencies**: Ensure all requirements are installed
2. **Port conflicts**: Check if ports 7860-7862 are already in use
3. **Permission issues**: Verify write access to output directories

## 🌐 License

Covered under the GBU2™ License (Genesis-Bloom-Unfoldment 2.0) - Bioneer Edition
