# BitGet API Test Suite

This test suite provides comprehensive testing for the BitGet API endpoints, allowing you to verify the functionality of your BitGet integration.

## Features

- Tests for all major BitGet API endpoints
- Support for both v1 and v2 API versions
- Safe by default: read-only tests that don't place orders
- Optional order tests with minimal amounts for end-to-end verification
- Detailed logging and output for debugging API interactions

## Prerequisites

- Python 3.7+
- BitGet API credentials (API Key, Secret Key, Passphrase)
- Required Python packages: `requests`, `python-dotenv`, `unittest`

## Setup

1. Create a `.env` file in the project root with your BitGet API credentials:

```
BITGET_API_KEY=your_api_key
BITGET_SECRET_KEY=your_secret_key
BITGET_PASSPHRASE=your_passphrase
```

2. Install required packages if not already installed:

```bash
pip install requests python-dotenv
```

## Running the Tests

### Basic Usage

Run all read-only tests (no orders placed) against the testnet using API v1:

```bash
python run_bitget_api_tests.py
```

### Advanced Options

```bash
# Use mainnet (be careful!)
python run_bitget_api_tests.py --mainnet

# Test API v2
python run_bitget_api_tests.py --api-version v2

# Enable order tests (will place minimal orders)
python run_bitget_api_tests.py --enable-order-tests

# Specify custom test amount
python run_bitget_api_tests.py --enable-order-tests --test-amount 0.0002

# Enable verbose logging
python run_bitget_api_tests.py --verbose

# Provide credentials directly (not recommended, use .env instead)
python run_bitget_api_tests.py --api-key YOUR_KEY --secret-key YOUR_SECRET --passphrase YOUR_PASSPHRASE
```

## Test Categories

The test suite is organized into different categories:

1. **Market Data Tests**: Tests for ticker, depth, trades, candles, etc.
2. **Account Data Tests**: Tests for account information, positions, etc.
3. **Order Tests**: Tests for placing, querying, and closing orders (only run if explicitly enabled)

## Caution

- The `--enable-order-tests` flag will place real orders on the selected environment
- Always use testnet for development and testing when possible
- When testing on mainnet, the test places orders with minimal amounts (default: 0.0001 BTC)
- Always verify your API credentials and permissions to avoid unexpected behavior

## BitGet API Documentation

For more information on the BitGet API, refer to the official documentation:

- [BitGet API Documentation](https://bitgetlimited.github.io/apidoc/en/mix)

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Verify your API credentials are correct and properly formatted in the .env file
2. **Rate Limiting**: BitGet has API rate limits. If you see 429 errors, you may need to wait before retrying
3. **Insufficient Balance**: Ensure your account has sufficient balance for order tests

### Getting Support

If you encounter issues with the API tests, please:

1. Check the detailed logs for error messages
2. Verify your API credentials and permissions
3. Refer to the BitGet API documentation for endpoint-specific requirements
4. Contact the OMEGA BTC AI team for assistance if needed
