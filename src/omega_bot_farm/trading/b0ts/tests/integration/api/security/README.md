
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


# BitgetPositionAnalyzerB0t API Security Tests

This directory contains security test suites for the BitgetPositionAnalyzerB0t API. These tests verify that security best practices and mechanisms are correctly implemented.

## Test Categories

### Authentication Tests

Located in the `auth/` directory, these tests verify:

- API key authentication and HMAC signature verification
- Token-based authentication (JWT) generation and validation
- Session management and authentication flows
- Secure credential handling

### Rate Limiting Tests

Tests to verify rate limiting functionality:

- Request frequency restrictions enforcement
- Per-API-key rate limits
- Response headers for rate limit information
- Burst protection mechanisms
- Throttling behavior

### IP Restriction Tests  

Tests to verify IP whitelisting and restriction capabilities:

- Whitelisted IPs allowed access
- Non-whitelisted IPs blocked
- CIDR range support
- Country-based blocking

### CSRF Protection Tests

Tests to verify Cross-Site Request Forgery protection:

- Token generation and validation
- Token expiration mechanisms
- Double submission protection
- Session binding

### Data Validation Tests

Tests to ensure proper request data validation:

- Input validation for various data types
- Sanitization of user inputs
- Protection against injection attacks
- Schema validation for API requests

## Running the Tests

### Prerequisites

- Python 3.8+
- pytest
- Configured environment with access to BitgetPositionAnalyzerB0t

### Test Execution

Run all security tests:

```bash
pytest -v src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/integration/api/security/
```

Run a specific test category:

```bash
pytest -v src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/integration/api/security/auth/
```

Skip tests requiring real implementation:

```bash
pytest -v -k "not requires_real_implementation" src/omega_bot_farm/trading/b0ts/bitget_analyzer/tests/integration/api/security/
```

## Mocking Behavior

All test files include fallback mock implementations that allow tests to run even if the actual BitgetPositionAnalyzerB0t security components are not available. This enables:

1. Test-driven development before implementation
2. Consistent test execution in CI/CD pipelines
3. Verification of security concepts and behavior

The tests check for the presence of real implementations and, if not found, use the mock implementations to verify the expected behavior.

## Security Best Practices

The tests validate adherence to these key security practices:

1. **Defense in Depth**: Multiple security layers (authentication, rate limiting, IP restrictions)
2. **Secure by Default**: Rejecting requests unless explicitly authorized
3. **Least Privilege**: Verifying that scope limitations are enforced
4. **Secure Communication**: Validating token mechanisms for secure data exchange
5. **Input Validation**: Checking request parameters before processing

## Adding New Security Tests

When adding new tests:

1. Follow the established pattern of attempting to import real implementations first
2. Provide mock implementations that accurately reflect expected behavior
3. Test both positive (authorized) and negative (unauthorized) cases
4. Include timing attack mitigations in authentication tests
5. Document any new security mechanisms in this README

## Performance Considerations

Security mechanisms often involve trade-offs with performance. The test suite includes basic performance tests to ensure that:

1. Security checks don't add excessive latency
2. Rate limiting configuration is reasonable
3. Token validation is optimized

## Test Data

Test fixtures provide sample credentials, tokens, and request data. These are contained within the test files to avoid storing sensitive information in separate files.

No real API credentials should be included in tests - all keys and tokens should be test-specific values.

## Reporting Security Issues

If you discover a security vulnerability when running these tests, please report it through our secure reporting channel, not as a public issue.
