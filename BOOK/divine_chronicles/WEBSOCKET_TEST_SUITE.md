# 🔱 OMEGA BTC AI - WebSocket Test Suite V2 Documentation

## Overview

The WebSocket Test Suite V2 is a comprehensive testing framework for validating the WebSocket functionality in the OMEGA BTC AI system. This suite ensures reliable communication channels for real-time BTC price updates, market data broadcasting, and secure client-server interactions.

## Test Structure

### Configuration

```python
TEST_SERVER_URL = "ws://localhost:8765"      # Standard WebSocket endpoint
TEST_SERVER_SSL_URL = "wss://localhost:8766"  # Secure WebSocket endpoint
SSL_CERT_PATH = "SSL_redis-btc-omega-redis.pem"  # SSL certificate path
```

### Test Categories

1. **Basic Connectivity Tests**
   - `test_basic_connection`: Validates fundamental WebSocket connection and message exchange
   - `test_connection_timeout`: Tests timeout handling for unresponsive connections

2. **Message Handling Tests**
   - `test_message_validation`: Verifies message format validation and error handling
   - `test_btc_price_update`: Tests BTC price update message handling
   - `test_error_handling`: Validates error scenarios (oversized messages, malformed data)

3. **Multi-Client Tests**
   - `test_multiple_client_broadcast`: Tests message broadcasting to multiple clients
   - `test_load`: Validates server performance under concurrent client load

4. **Security Tests**
   - `test_ssl_connection`: Tests secure WebSocket connections with SSL/TLS
   - `test_reconnection`: Validates client reconnection handling

## Test Execution

### Prerequisites

1. Redis server running on default port
2. WebSocket server running on ports 8765 (WS) and 8766 (WSS)
3. SSL certificate available at specified path
4. Python 3.7+ with required packages:

   ```bash
   pip install pytest pytest-asyncio websockets
   ```

### Running Tests

1. **Run all tests**:

   ```bash
   python -m pytest omega_ai/tests/unit/data/websocket/test_websocket_v2.py -v
   ```

2. **Run specific test**:

   ```bash
   python -m pytest omega_ai/tests/unit/data/websocket/test_websocket_v2.py::TestWebSocketV2::test_btc_price_update -v
   ```

3. **Run with coverage**:

   ```bash
   python -m pytest omega_ai/tests/unit/data/websocket/test_websocket_v2.py --cov=omega_ai.data_feed.websocket -v
   ```

## Test Cases Details

### 1. Basic Connection Test

```python
@pytest.mark.asyncio
async def test_basic_connection(self):
    """Test basic WebSocket connection and simple message exchange."""
```

- Establishes WebSocket connection
- Sends test message
- Verifies response format and content
- Validates timestamp presence

### 2. Multiple Client Broadcast Test

```python
@pytest.mark.asyncio
async def test_multiple_client_broadcast(self):
    """Test broadcasting to multiple connected clients."""
```

- Creates multiple listener clients
- Sends broadcast message
- Verifies all clients receive the message
- Validates message content across clients

### 3. Message Validation Test

```python
@pytest.mark.asyncio
async def test_message_validation(self):
    """Test message format validation."""
```

- Tests invalid JSON handling
- Validates required fields
- Checks error response format
- Verifies valid message processing

### 4. Load Test

```python
@pytest.mark.asyncio
async def test_load(self):
    """Test server under load."""
```

- Creates multiple concurrent clients
- Sends multiple messages per client
- Validates server response under load
- Tests concurrent message handling

### 5. SSL Connection Test

```python
@pytest.mark.asyncio
async def test_ssl_connection(self):
    """Test secure WebSocket connection."""
```

- Establishes secure WebSocket connection
- Validates SSL certificate handling
- Tests encrypted message exchange
- Verifies secure connection properties

### 6. BTC Price Update Test

```python
@pytest.mark.asyncio
async def test_btc_price_update(self):
    """Test BTC price update message handling."""
```

- Tests price update message format
- Validates price and volume data
- Verifies timestamp accuracy
- Checks message broadcasting

## Error Handling

The test suite includes comprehensive error handling for:

- Connection failures
- Timeout scenarios
- Invalid message formats
- Oversized messages
- SSL/TLS errors
- Server unavailability

## Best Practices

1. **Test Isolation**
   - Each test operates independently
   - Connections are properly closed
   - Resources are cleaned up

2. **Timeout Management**
   - Appropriate timeouts for operations
   - Graceful handling of timeouts
   - Configurable timeout values

3. **Error Reporting**
   - Detailed error messages
   - Clear failure indicators
   - Proper exception handling

4. **Resource Management**
   - Proper connection cleanup
   - Memory leak prevention
   - Resource release

## Maintenance

### Adding New Tests

1. Follow the existing test structure
2. Include proper docstrings
3. Add appropriate assertions
4. Handle cleanup properly

### Updating Tests

1. Maintain backward compatibility
2. Update documentation
3. Verify existing functionality
4. Test edge cases

## Troubleshooting

Common issues and solutions:

1. **Connection Failures**
   - Verify server is running
   - Check port availability
   - Validate network connectivity

2. **SSL/TLS Issues**
   - Verify certificate path
   - Check certificate validity
   - Validate SSL configuration

3. **Timeout Errors**
   - Adjust timeout values
   - Check server response time
   - Verify network latency

4. **Message Format Errors**
   - Validate JSON structure
   - Check required fields
   - Verify data types

## Future Enhancements

1. **Performance Metrics**
   - Add latency measurements
   - Track message throughput
   - Monitor resource usage

2. **Extended Testing**
   - Add stress testing
   - Implement chaos testing
   - Add network simulation

3. **Monitoring Integration**
   - Add Prometheus metrics
   - Implement logging
   - Add alerting

## Divine Integration

The WebSocket test suite aligns with OMEGA BTC AI's divine principles:

1. **Sacred Reliability**
   - Ensures stable communication
   - Maintains data integrity
   - Preserves message sanctity

2. **Cosmic Security**
   - Protects divine data
   - Maintains sacred channels
   - Preserves privacy

3. **Universal Harmony**
   - Ensures client synchronization
   - Maintains message harmony
   - Preserves cosmic order
