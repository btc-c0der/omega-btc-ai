
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


# BitGet API Debugging Tools

This directory contains utility scripts to help debug BitGet API authentication issues.

## BitGet API Signature Test Tool

The `bitget_signature_test.py` script is designed to help troubleshoot signature generation for BitGet API authentication. It implements and compares different signature generation algorithms and tests basic API endpoints.

### Features

- Compares two different signature generation methods to ensure they match
- Tests basic API endpoints with authentication
- Provides detailed request/response information for debugging
- Allows testing with either testnet or mainnet

### Usage

```bash
# Basic usage with environment variables for credentials
python bitget_signature_test.py --testnet

# Specify credentials directly
python bitget_signature_test.py --testnet --api-key YOUR_API_KEY --secret-key YOUR_SECRET_KEY --passphrase YOUR_PASSPHRASE

# Only compare signature generation without making API calls
python bitget_signature_test.py --compare-only

# Use mainnet instead of testnet
python bitget_signature_test.py --mainnet

# Enable detailed debug output
python bitget_signature_test.py --debug

# Test with a specific sub-account
python bitget_signature_test.py --sub-account YOUR_SUB_ACCOUNT_NAME
```

### Environment Variables

The script supports using environment variables for API credentials:

- For testnet: `BITGET_TESTNET_API_KEY`, `BITGET_TESTNET_SECRET_KEY`, `BITGET_TESTNET_PASSPHRASE`
- For mainnet: `BITGET_API_KEY`, `BITGET_SECRET_KEY`, `BITGET_PASSPHRASE`
- For sub-accounts: `STRATEGIC_SUB_ACCOUNT_NAME` or `SUB_ACCOUNT_NAME`

The script automatically loads environment variables from a `.env` file in the project root. Example `.env` file:

```
BITGET_TESTNET_API_KEY=your_api_key
BITGET_TESTNET_SECRET_KEY=your_secret_key
BITGET_TESTNET_PASSPHRASE=your_passphrase
STRATEGIC_SUB_ACCOUNT_NAME=your_sub_account_name
```

## Common BitGet API Signature Issues

1. **Signature Error**: If you see `sign signature error` in API responses, it could be due to:
   - Incorrect API credentials
   - Wrong signature generation method
   - Headers not properly formatted
   - Timestamp format issues
   - Query parameter ordering issues
   - Sub-account name formatting issues

2. **Parameter Formatting**:
   - BitGet expects parameters to be sorted alphabetically by key
   - Query parameters should be formatted as `key=value&key2=value2` (no URL encoding for signature generation)
   - The signature message should include `?` before query parameters

3. **Sub-accounts**:
   - When using sub-accounts, add the `subAccountName` parameter to the appropriate requests
   - Some endpoints don't support sub-account parameters (e.g., market data endpoints)
   - Sub-account names must match exactly what's on BitGet, including case sensitivity
   - The parameter should be included in the signature generation

## Troubleshooting Steps

1. Run the signature test tool with `--compare-only` to verify signatures match
2. Check that your API credentials have the correct permissions
3. Verify the network (testnet vs. mainnet) is correctly set
4. Check for any typos in API keys or endpoints
5. Compare request parameters with the BitGet API documentation
6. Ensure timestamps are correctly formatted as milliseconds
7. Set `--debug` flag to see detailed request/response information

## Resources

- [BitGet API Documentation](https://bitgetlimited.github.io/apidoc/en/mix/)
- [BitGet API Authentication Guide](https://bitgetlimited.github.io/apidoc/en/mix/#signature)
