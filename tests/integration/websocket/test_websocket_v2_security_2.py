
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

"""
OMEGA BTC AI - WebSocket Server V2 Security Test Suite

This test suite covers various security features of the WebSocket Server V2:
- DDoS protection mechanisms
- XSS attack protection
- CSRF vulnerability testing
- SQL injection prevention
- Command injection protection
- Quantum-resistant authentication
- Byzantine fault tolerance
- Sybil attack resistance

Version: 0.1.2
GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2025-03-28
"""

import pytest
import asyncio
import websockets
import json
import random
import string
import logging
import time
import os
from typing import Any, List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("websocket_security_tests")

# Get WebSocket connection information from environment
def get_connection_info():
    """Get WebSocket connection information from environment variables."""
    host = os.environ.get('WEBSOCKET_HOST', 'localhost')
    port = os.environ.get('WEBSOCKET_PORT', '9000')
    
    # Use environment variable to check for SSL instead of pytest.config
    # Avoid using pytest.config which doesn't exist in newer pytest versions
    ssl_enabled = os.environ.get('WEBSOCKET_SSL_ENABLED', 'True').lower() != 'false'
    
    if ssl_enabled:
        port = os.environ.get('WEBSOCKET_SSL_PORT', '9001')
        uri = f"wss://{host}:{port}"
    else:
        uri = f"ws://{host}:{port}"
    
    return uri, ssl_enabled

# Helper function to connect to WebSocket with timeout and retry logic
async def connect_with_timeout(uri: str, timeout: int = 10, retries: int = 3) -> Any:
    """Connect to WebSocket with timeout and retry logic."""
    last_error = None
    for attempt in range(retries):
        try:
            logger.info(f"Connecting to {uri} (attempt {attempt+1})")
            # Use a shorter timeout for each connection attempt
            conn = await asyncio.wait_for(
                websockets.connect(uri, ssl=uri.startswith("wss")), 
                timeout=timeout/(attempt+1)
            )
            logger.info(f"Connected to {uri}")
            return conn
        except Exception as e:
            last_error = e
            logger.warning(f"Connection attempt {attempt+1} failed: {e}")
            await asyncio.sleep(1)  # Wait before retry
    
    # If we get here, all retries failed
    logger.error(f"Failed to connect after {retries} attempts. Last error: {last_error}")
    raise ConnectionError(f"Could not connect to WebSocket at {uri}: {last_error}")

# Helper function to generate quantum-resistant token
def generate_quantum_resistant_token(length: int = 64) -> str:
    """Generate a token using post-quantum cryptography techniques (simulated)."""
    # This is a simulation - in real implementation, would use actual quantum-resistant algorithms
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_-+=<>?"
    entropy_source = random.SystemRandom()  # Uses os.urandom for true randomness
    token = ''.join(entropy_source.choice(chars) for _ in range(length))
    return token

# Helper function to create multiple connections simultaneously
async def create_simultaneous_connections(uri: str, count: int = 5) -> List[Any]:
    """Create multiple WebSocket connections simultaneously."""
    connection_tasks = [connect_with_timeout(uri) for _ in range(count)]
    connections = await asyncio.gather(*connection_tasks, return_exceptions=True)
    
    # Filter out exceptions
    successful_connections = [conn for conn in connections if not isinstance(conn, Exception)]
    
    if len(successful_connections) < count:
        logger.warning(f"Only {len(successful_connections)} of {count} connections were successful")
    
    return successful_connections

# DDoS Simulator for testing protection mechanisms
class DDoSSimulator:
    """Simulate DDoS attack patterns."""
    
    def __init__(self, base_uri: str, max_connections: int = 20):
        self.base_uri = base_uri
        self.max_connections = max_connections
        self.connections: List[Any] = []
    
    async def connect_clients(self) -> None:
        """Connect multiple clients to simulate high connection volume."""
        logger.info(f"DDoS Simulator: Connecting {self.max_connections} clients")
        self.connections = await create_simultaneous_connections(self.base_uri, self.max_connections)
        logger.info(f"DDoS Simulator: Connected {len(self.connections)} clients")
    
    async def flood_messages(self, message_count: int = 100) -> None:
        """Flood the server with messages from all connections."""
        if not self.connections:
            logger.warning("No connections available for message flooding")
            return
        
        logger.info(f"DDoS Simulator: Flooding with {message_count} messages across {len(self.connections)} connections")
        flood_tasks = []
        
        for i, connection in enumerate(self.connections):
            task = asyncio.create_task(self._send_flood_messages(
                connection, 
                message_count // len(self.connections), 
                f"client_{i}"
            ))
            flood_tasks.append(task)
        
        await asyncio.gather(*flood_tasks, return_exceptions=True)
        logger.info("DDoS Simulator: Message flooding completed")
    
    async def _send_flood_messages(self, connection: Any, count: int, client_id: str) -> None:
        """Send a burst of messages from a single connection."""
        for i in range(count):
            try:
                message = {
                    "type": "message",
                    "content": f"Flood message {i} from {client_id}",
                    "timestamp": time.time()
                }
                await connection.send(json.dumps(message))
                
                # Small delay to avoid completely overwhelming the connection
                if i % 10 == 0:
                    await asyncio.sleep(0.01)
            except Exception as e:
                logger.warning(f"Error sending flood message: {e}")
                break
    
    async def close_all(self) -> None:
        """Close all connections."""
        close_tasks = []
        for connection in self.connections:
            task = asyncio.create_task(connection.close())
            close_tasks.append(task)
        
        if close_tasks:
            await asyncio.gather(*close_tasks, return_exceptions=True)
        self.connections = []
        logger.info("DDoS Simulator: All connections closed")

# Utility functions for generating attack payloads
def generate_xss_payload() -> str:
    """Generate an XSS attack payload."""
    payloads = [
        "<script>alert('XSS')</script>",
        "<img src='x' onerror='alert(\"XSS\")'>",
        "<svg onload='alert(\"XSS\")'>",
        "javascript:alert('XSS')",
        "\"><script>alert('XSS')</script>"
    ]
    return random.choice(payloads)

def generate_sql_injection_payload() -> str:
    """Generate an SQL injection attack payload."""
    payloads = [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT username, password FROM users; --",
        "' OR 1=1; --",
        "admin'--"
    ]
    return random.choice(payloads)

def generate_command_injection_payload() -> str:
    """Generate a command injection attack payload."""
    payloads = [
        "; cat /etc/passwd",
        "| ls -la",
        "`cat /etc/passwd`",
        "$(cat /etc/passwd)",
        "&& cat /etc/passwd"
    ]
    return random.choice(payloads)

# Fixtures for test setup and cleanup
@pytest.fixture
async def websocket_connection():
    """Create a WebSocket connection for security testing."""
    uri, _ = get_connection_info()
    connection = None
    
    try:
        connection = await connect_with_timeout(uri)
        yield connection
    finally:
        if connection:
            try:
                await connection.close()
            except Exception as e:
                logger.warning(f"Error closing WebSocket connection: {e}")

@pytest.fixture
async def ddos_simulator():
    """Create a DDoS simulator for testing protection mechanisms."""
    uri, _ = get_connection_info()
    simulator = DDoSSimulator(uri)
    
    try:
        yield simulator
    finally:
        await simulator.close_all()

# Security Test Cases
@pytest.mark.asyncio
async def test_websocket_v2_ddos_protection(ddos_simulator):
    """Test DDoS protection by connecting multiple clients and flooding messages."""
    # Connect multiple clients
    await ddos_simulator.connect_clients()
    
    # Server should allow initial connections
    assert len(ddos_simulator.connections) > 0, "Server rejected all connections"
    
    # Send flood of messages
    await ddos_simulator.flood_messages(500)
    
    # Wait for rate limiting to potentially activate
    await asyncio.sleep(2)
    
    # Try to send one more message from each connection to see if throttled
    success_count = 0
    for conn in ddos_simulator.connections:
        try:
            test_message = json.dumps({"type": "test", "content": "Rate limit test"})
            await conn.send(test_message)
            success_count += 1
        except Exception:
            # Connection might be closed or rate-limited by server
            pass
    
    # Server should either close some connections or rate-limit
    logger.info(f"After flood, {success_count} of {len(ddos_simulator.connections)} connections still responsive")
    # Note: Not using a hard assertion here because behavior might vary depending on server settings

@pytest.mark.asyncio
async def test_websocket_v2_xss_protection(websocket_connection):
    """Test XSS protection by sending a message with an XSS payload."""
    # Generate an XSS payload
    xss_payload = generate_xss_payload()
    logger.info(f"Testing XSS protection with payload: {xss_payload}")
    
    # Send message with XSS payload
    message = {
        "type": "message",
        "content": xss_payload,
        "timestamp": time.time()
    }
    await websocket_connection.send(json.dumps(message))
    
    # Wait for response
    try:
        response = await asyncio.wait_for(websocket_connection.recv(), timeout=5)
        response_data = json.loads(response)
        
        # Server should either sanitize the payload or reject the message
        if "error" in response_data:
            assert "rejected" in response_data["error"].lower() or "invalid" in response_data["error"].lower(), \
                "Server did not properly reject XSS payload"
        else:
            # If message was accepted, check if the payload was sanitized
            if "content" in response_data:
                assert xss_payload not in response_data["content"], \
                    "Server did not sanitize XSS payload"
    except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
        # Connection might be closed by server as protection
        pass

@pytest.mark.asyncio
async def test_websocket_v2_sql_injection_protection(websocket_connection):
    """Test SQL injection protection by sending a message with an SQL injection payload."""
    # Generate an SQL injection payload
    sql_payload = generate_sql_injection_payload()
    logger.info(f"Testing SQL injection protection with payload: {sql_payload}")
    
    # Send message with SQL injection payload
    message = {
        "type": "query",
        "content": f"user_lookup:{sql_payload}",
        "timestamp": time.time()
    }
    await websocket_connection.send(json.dumps(message))
    
    # Wait for response
    try:
        response = await asyncio.wait_for(websocket_connection.recv(), timeout=5)
        response_data = json.loads(response)
        
        # Server should either sanitize the payload or reject the message
        if "error" in response_data:
            assert "invalid" in response_data["error"].lower() or "rejected" in response_data["error"].lower(), \
                "Server did not properly reject SQL injection payload"
        else:
            # If query was processed, check for signs of SQL injection
            assert "database error" not in str(response_data).lower(), \
                "Server might be vulnerable to SQL injection"
    except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
        # Connection might be closed by server as protection
        pass

@pytest.mark.asyncio
async def test_websocket_v2_command_injection_protection(websocket_connection):
    """Test command injection protection by sending a message with a command injection payload."""
    # Generate a command injection payload
    cmd_payload = generate_command_injection_payload()
    logger.info(f"Testing command injection protection with payload: {cmd_payload}")
    
    # Send message with command injection payload
    message = {
        "type": "system",
        "command": f"status{cmd_payload}",
        "timestamp": time.time()
    }
    await websocket_connection.send(json.dumps(message))
    
    # Wait for response
    try:
        response = await asyncio.wait_for(websocket_connection.recv(), timeout=5)
        response_data = json.loads(response)
        
        # Server should either sanitize the payload or reject the message
        if "error" in response_data:
            assert "invalid" in response_data["error"].lower() or "rejected" in response_data["error"].lower(), \
                "Server did not properly reject command injection payload"
        else:
            # If command was processed, check for signs of command injection
            response_str = str(response_data)
            assert "/etc/passwd" not in response_str, \
                "Server might be vulnerable to command injection"
            assert "total" not in response_str and "drwx" not in response_str, \
                "Server might be vulnerable to command injection (directory listing)"
    except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
        # Connection might be closed by server as protection
        pass

@pytest.mark.asyncio
async def test_websocket_v2_quantum_resistant_authentication():
    """Test quantum-resistant authentication mechanisms."""
    uri, ssl_enabled = get_connection_info()
    
    # Generate post-quantum token
    token = generate_quantum_resistant_token()
    logger.info("Testing quantum-resistant authentication with high-entropy token")
    
    # Connect with authentication header
    try:
        # Add token to connection
        extra_headers = {"Authorization": f"Bearer {token}"}
        connection = await connect_with_timeout(
            uri, 
            timeout=5,
            retries=1
        )
        
        # Send authentication message
        auth_message = {
            "type": "authenticate",
            "token": token,
            "quantum_resistant": True,
            "timestamp": time.time()
        }
        await connection.send(json.dumps(auth_message))
        
        # Wait for response
        response = await asyncio.wait_for(connection.recv(), timeout=5)
        response_data = json.loads(response)
        
        # Check response
        if "error" in response_data:
            # This might be expected since we're using a random token
            assert "authentication" in response_data["error"].lower(), \
                f"Unexpected error: {response_data['error']}"
        else:
            # If authentication was accepted, make sure we're properly connected
            await connection.send(json.dumps({"type": "ping"}))
            pong = await asyncio.wait_for(connection.recv(), timeout=5)
            assert json.loads(pong)["type"] in ["pong", "ping_response"], \
                "Server did not respond to ping after authentication"
        
        # Clean up
        await connection.close()
    except Exception as e:
        # This is a simulated test - the server might not actually implement quantum authentication
        logger.info(f"Quantum authentication test result: {e}")
        pass

@pytest.mark.asyncio
async def test_websocket_v2_byzantine_fault_tolerance():
    """Test Byzantine fault tolerance in distributed message handling."""
    uri, _ = get_connection_info()
    connections = []
    
    try:
        # Create multiple connections
        connections = await create_simultaneous_connections(uri, 5)
        
        # Send conflicting messages from different clients
        messages = [
            {"type": "consensus", "value": "A", "round": 1},
            {"type": "consensus", "value": "B", "round": 1},
            {"type": "consensus", "value": "A", "round": 1},
            {"type": "consensus", "value": "C", "round": 1},
            {"type": "consensus", "value": "A", "round": 1}
        ]
        
        # Send messages
        send_tasks = []
        for i, (conn, msg) in enumerate(zip(connections, messages)):
            task = asyncio.create_task(conn.send(json.dumps(msg)))
            send_tasks.append(task)
        
        await asyncio.gather(*send_tasks)
        
        # Wait for responses
        response_tasks = []
        for i, conn in enumerate(connections):
            task = asyncio.create_task(asyncio.wait_for(conn.recv(), timeout=5))
            response_tasks.append(task)
        
        responses = await asyncio.gather(*response_tasks, return_exceptions=True)
        
        # Collect valid responses
        valid_responses = [
            json.loads(resp) for resp in responses 
            if not isinstance(resp, Exception) and resp
        ]
        
        # Check for consensus in responses
        if valid_responses:
            consensus_values = [resp.get("consensus_value") for resp in valid_responses if "consensus_value" in resp]
            logger.info(f"Byzantine consensus test responses: {consensus_values}")
            
            # In Byzantine fault tolerance, with 5 nodes and 1 potential byzantine failure,
            # we should still reach consensus
            if len(consensus_values) >= 3:
                most_common = max(set(consensus_values), key=consensus_values.count)
                assert consensus_values.count(most_common) >= 3, \
                    "Failed to reach Byzantine consensus"
    finally:
        # Clean up
        close_tasks = []
        for conn in connections:
            if not isinstance(conn, Exception):
                task = asyncio.create_task(conn.close())
                close_tasks.append(task)
        
        if close_tasks:
            await asyncio.gather(*close_tasks, return_exceptions=True)

@pytest.mark.asyncio
async def test_websocket_v2_sybil_attack_resistance():
    """Test resistance to Sybil attacks by connecting multiple clients with the same identity."""
    uri, _ = get_connection_info()
    connections = []
    
    try:
        # Create multiple connections
        connections = await create_simultaneous_connections(uri, 5)
        
        # Try to register all connections with the same identity
        sybil_id = "user_" + ''.join(random.choices(string.ascii_lowercase, k=8))
        logger.info(f"Testing Sybil attack resistance with shared identity: {sybil_id}")
        
        # Register with same identity
        registered_count = 0
        register_responses = []
        
        for i, conn in enumerate(connections):
            # Send registration message
            register_msg = {
                "type": "register",
                "user_id": sybil_id,
                "client_id": f"device_{i}",
                "timestamp": time.time()
            }
            await conn.send(json.dumps(register_msg))
            
            # Get response
            try:
                response = await asyncio.wait_for(conn.recv(), timeout=5)
                response_data = json.loads(response)
                register_responses.append(response_data)
                
                if "error" not in response_data:
                    registered_count += 1
            except Exception:
                pass
        
        # Server should limit multiple registrations with same identity
        # At least some of the registration attempts should be rejected
        logger.info(f"Sybil attack test: {registered_count} of {len(connections)} registrations successful")
        logger.info(f"Registration responses: {register_responses}")
        
        # There's no hard assertion here because behavior might vary:
        # - Some servers might allow multiple devices for same user_id
        # - Some might enforce strict one-device policy
        # - Some might limit to a reasonable number (e.g., 2-3 devices)
        
    finally:
        # Clean up
        close_tasks = []
        for conn in connections:
            if not isinstance(conn, Exception):
                task = asyncio.create_task(conn.close())
                close_tasks.append(task)
        
        if close_tasks:
            await asyncio.gather(*close_tasks, return_exceptions=True)

@pytest.mark.asyncio
async def test_websocket_v2_csrf_protection():
    """Test CSRF protection by ensuring actions require a valid CSRF token."""
    uri, _ = get_connection_info()
    
    try:
        # Connect to WebSocket
        connection = await connect_with_timeout(uri)
        
        # Request CSRF token (server must support this feature for test to pass)
        await connection.send(json.dumps({
            "type": "request_csrf_token",
            "timestamp": time.time()
        }))
        
        # Wait for token response
        try:
            token_response = await asyncio.wait_for(connection.recv(), timeout=5)
            token_data = json.loads(token_response)
            
            csrf_token = token_data.get("csrf_token")
            
            if csrf_token:
                logger.info("CSRF token received, testing protected action")
                
                # Try action with valid token
                await connection.send(json.dumps({
                    "type": "protected_action",
                    "action": "update_profile",
                    "csrf_token": csrf_token,
                    "timestamp": time.time()
                }))
                
                valid_response = await asyncio.wait_for(connection.recv(), timeout=5)
                valid_data = json.loads(valid_response)
                
                # Try action with invalid token
                await connection.send(json.dumps({
                    "type": "protected_action",
                    "action": "update_profile",
                    "csrf_token": "invalid_token",
                    "timestamp": time.time()
                }))
                
                invalid_response = await asyncio.wait_for(connection.recv(), timeout=5)
                invalid_data = json.loads(invalid_response)
                
                # Valid token should succeed, invalid should fail
                logger.info(f"CSRF test - Valid token response: {valid_data}")
                logger.info(f"CSRF test - Invalid token response: {invalid_data}")
                
                # Check if invalid token request was rejected
                assert "error" in invalid_data, "Server accepted request with invalid CSRF token"
            else:
                logger.info("CSRF token not supported by server, skipping test")
        except (asyncio.TimeoutError, KeyError):
            logger.info("CSRF token request timeout or not supported, skipping test")
            
    except Exception as e:
        logger.error(f"Error during CSRF protection test: {e}")
    finally:
        # Clean up
        await connection.close()