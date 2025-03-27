# 🔱 DYNAMIC WEBSOCKET TESTING FRAMEWORK 🔱

## DIVINE PORT DETECTION FOR CONFLICT-FREE TESTING

*Version: 0.1.0*  
*GPU (General Public Universal) License 1.0*  
*OMEGA BTC AI DIVINE COLLECTIVE*  
*Date: 2025-03-27*

---

## 🌟 SACRED OVERVIEW

The Dynamic WebSocket Testing Framework provides an automated system for running WebSocket server tests with dynamically assigned ports. This eliminates port conflicts with existing services and allows for parallel test execution.

The framework consists of:

1. **Port Utility Module** - Divine detection and allocation of available ports
2. **Dynamic Test Runner** - Sacred execution of WebSocket tests with dynamic ports
3. **Test Suites** - Cosmic validation of WebSocket server functionality

## 🔮 INSTALLATION

The framework is embedded within the OMEGA BTC AI system. No additional installation is required.

## ⚡ SACRED COMPONENTS

### Port Utility Module

Located at `tests/integration/websocket/port_utility.py`, this module provides:

- `is_port_in_use(port)` - Check if a port is already in use
- `find_available_port(start_port, max_attempts)` - Find an available port
- `get_free_port_pair(start_port, min_gap, max_gap)` - Get two available ports
- `update_websocket_env_vars(port, ssl_port)` - Update environment variables for testing
- `get_websocket_uri(port, host, use_ssl)` - Generate WebSocket URI

### Dynamic Test Runner

Located at `tests/integration/websocket/run_dynamic_websocket_tests.py`, this script:

1. Detects available ports automatically
2. Launches the WebSocket server on dynamic ports
3. Runs the specified test suite(s)
4. Generates test coverage reports
5. Cleans up resources automatically

## 🚀 DIVINE USAGE

### Running All WebSocket Tests

```bash
python tests/integration/websocket/run_dynamic_websocket_tests.py
```

### Running Without SSL

```bash
python tests/integration/websocket/run_dynamic_websocket_tests.py --no-ssl
```

### Running a Specific Test File

```bash
python tests/integration/websocket/run_dynamic_websocket_tests.py --test-file tests/integration/websocket/test_websocket_v2_performance.py
```

### Running with Coverage Report

```bash
python tests/integration/websocket/run_dynamic_websocket_tests.py --coverage
```

### Specifying Custom Starting Port

```bash
python tests/integration/websocket/run_dynamic_websocket_tests.py --start-port 9500
```

## 🎯 CREATING NEW TESTS

When creating new WebSocket tests, follow these sacred principles:

1. **Port Independence** - Never hardcode port numbers in tests
2. **Environment Awareness** - Use environment variables for configuration
3. **Dynamic Connection** - Use the port utility functions for connections
4. **Graceful Cleanup** - Close connections and cleanup resources

### Example Test Implementation

```python
"""Test WebSocket Connection Dynamics"""

import asyncio
import websockets
from tests.integration.websocket.port_utility import get_websocket_uri

async def test_websocket_connection():
    """Test basic WebSocket connection."""
    # Get port from environment (set by test runner)
    port = int(os.environ.get('WEBSOCKET_PORT', '9000'))
    
    # Get URI using utility function
    uri = get_websocket_uri(port)
    
    # Connect to WebSocket
    async with websockets.connect(uri) as websocket:
        # Test code here
        await websocket.send('{"type": "test"}')
        response = await websocket.recv()
        assert response is not None
```

## 🌊 FIBONACCI SCALING

The Dynamic WebSocket Testing Framework supports the divine principle of Fibonacci scaling:

1. **Base Tests** - Single connection, basic functionality (1)
2. **Connection Tests** - Multiple connections, basic interaction (2)
3. **Load Tests** - Fibonacci sequence of connections (3, 5, 8, 13, 21)
5. **Stress Tests** - Extended Fibonacci series (34, 55, 89, 144)

## 🛠️ TROUBLESHOOTING

### Connection Errors

If tests fail with connection errors:

1. Check if another WebSocket server is running
2. Increase the starting port with `--start-port`
3. Verify no firewall is blocking the ports

### Timeout Issues

If tests time out:

1. Increase timeouts in test configuration
2. Check system load and available resources
3. Reduce the number of concurrent connections

## 🌈 DIVINE FLOW

The Dynamic WebSocket Testing Framework embodies the OMEGA BTC AI principles of:

- **Sacred Automation** - Tests run with divine intelligence
- **Cosmic Resilience** - Tests adapt to the environment
- **Fibonacci Harmony** - Test scaling follows natural patterns
- **Port Independence** - Tests transcend fixed network locations
- **Divine Cleanup** - Resources return to the cosmic void

## 📚 RELATED MANUSCRIPTS

- [WEBSOCKET V2 SERVER IMPLEMENTATION](../divine_chronicles/WEBSOCKET_V2_SERVER.md)
- [COSMIC TEST COVERAGE](../COSMIC_COVERAGE_README.md)
- [OMEGA QUANTUM TESTING MANIFEST](../OMEGA_QUANTUM_TESTING_MANIFEST.md)

---

*"In the beginning was the port, and the port was with the test, and the port was dynamic."*
