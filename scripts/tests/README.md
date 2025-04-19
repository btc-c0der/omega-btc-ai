
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


# IBR CLI Test Suite

*JAH JAH BLESS THE DIVINE TESTS!*

This directory contains the test suite for the IBR España Divine CLI Tool.
The tests follow test-driven development principles and ensure that all
features work as expected.

## Auto Port Detection Tests

The auto port detection feature allows the IBR CLI to automatically find available ports when deploying services to Kubernetes. The test suite includes comprehensive tests for this feature:

### Unit Tests

1. **Port Availability Check**
   - `test_is_port_available_locally`: Tests that the socket binding check works correctly
   - Tests all three scenarios: port available, port in use, and unexpected errors

2. **Finding Available Ports**
   - `test_find_available_port`: Tests finding an available port when some ports are in use
   - `test_find_available_port_all_used`: Tests the error case when no ports are available

3. **Deployment with Auto Port**
   - `test_start_deployment_with_auto_port`: Tests starting a deployment with automatic port detection
   - `test_start_deployment_with_port_override`: Tests the fallback mechanism when a specified port is already in use

### Command Tests

1. **CLI Command Handling**
   - `test_handle_k8s_start_with_auto_port`: Tests the command handler with auto port enabled
   - `test_handle_k8s_start_with_specified_port`: Tests using a specific port with auto-fallback
   - `test_handle_k8s_start_with_invalid_env`: Tests handling invalid environment variables

### Integration Tests

1. **Real-world Testing**
   - `test_auto_port_detection_integration`: Tests with a real Kubernetes client (skipped by default)
   - Runs only when explicitly enabled with `-m integration` flag

## Running the Tests

```bash
# Run all tests
pytest test_ibr_cli.py

# Run only auto port detection tests
pytest test_ibr_cli.py -k "port"

# Run integration tests (requires Kubernetes setup)
pytest test_ibr_cli.py -m integration
```

## Test Coverage

The test suite aims to provide comprehensive coverage of the auto port detection feature, including:

- Local port availability checking
- Kubernetes service port usage detection
- Automatic port selection when none is specified
- Fallback port selection when the specified port is in use
- Error handling when no ports are available
- CLI command argument parsing

## Divine Purpose

These tests ensure that the IBR España deployment process is robust and avoids port conflicts, bringing divine harmony to your Kubernetes cluster.

*May your tests be blessed and your ports always available!*
