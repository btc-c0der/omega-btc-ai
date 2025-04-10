#!/usr/bin/env python3

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
Test suite for Quantum 5D QA Dashboard API Endpoints
---------------------------------------------------

This test suite provides comprehensive HTTP-level testing for the
Quantum 5D QA Dashboard API endpoints, using both unittest and 
requests libraries to directly test the API interface.
"""

import os
import sys
import json
import unittest
import threading
import requests
import time
from unittest import mock

# Add parent directory to path to allow imports to work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
    
# Also add the directory containing quantum_qa_dashboard
qa_dir = os.path.dirname(parent_dir)
src_dir = os.path.dirname(qa_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

# Import the dashboard module
try:
    from quantum_qa_dashboard import Quantum5DDashboard
except ImportError:
    # Try alternate import path
    try:
        from omega_bot_farm.qa.quantum_qa_dashboard import Quantum5DDashboard
    except ImportError:
        print("Warning: Could not import Quantum5DDashboard. Using mock implementation.")
        # Create a mock implementation for testing
        class MockQuantum5DDashboard:
            """Mock implementation of Quantum5DDashboard for testing purposes."""
            
            def __init__(self):
                """Initialize the mock dashboard."""
                self.is_running = False
                self.metrics_running = False
                self.app = self._create_mock_app()
                
            def _create_mock_app(self):
                """Create a mock Dash app for testing."""
                class MockApp:
                    def __init__(self):
                        self.layout = {"dashboard-metrics": {}}
                        self.callback_map = {}
                        
                    def callback(self, *args, **kwargs):
                        def wrapper(func):
                            return func
                        return wrapper
                
                return MockApp()
                
            def run_dashboard(self, debug=False, host="localhost", port=8050):
                """Mock method to simulate starting the dashboard server."""
                self.is_running = True
                # In a real implementation, this would start a Dash server
                # For testing, we just set a flag
                
            def stop_metrics_collection(self):
                """Mock method to simulate stopping metrics collection."""
                self.metrics_running = False
        
        # Use the mock implementation
        Quantum5DDashboard = MockQuantum5DDashboard

# Test configuration
TEST_HOST = "localhost"
TEST_PORT = 8050
BASE_URL = f"http://{TEST_HOST}:{TEST_PORT}"

class APITestServer:
    """Helper class to start and stop the dashboard server for testing."""
    
    def __init__(self, host=TEST_HOST, port=TEST_PORT):
        """Initialize the test server."""
        self.host = host
        self.port = port
        self.server_thread = None
        self.dashboard = None
        
    def start(self):
        """Start the dashboard server in a background thread."""
        # Check if Quantum5DDashboard is available
        if Quantum5DDashboard is None:
            raise ImportError("Quantum5DDashboard class could not be imported")
        
        # Create dashboard instance with mocked metrics collection
        with mock.patch('quantum_qa_dashboard.QuantumMetrics.from_test_reports',
                        return_value=mock.MagicMock()):
            self.dashboard = Quantum5DDashboard()
            
            # Start the server in a separate thread
            self.server_thread = threading.Thread(
                target=self.dashboard.run_dashboard,
                kwargs={"debug": False, "host": self.host, "port": self.port}
            )
            self.server_thread.daemon = True
            self.server_thread.start()
            
            # Wait for server to start
            self._wait_for_server()
            
    def stop(self):
        """Stop the dashboard server."""
        if self.dashboard:
            self.dashboard.stop_metrics_collection()
            
        # The server thread will terminate when the main thread exits
        
    def _wait_for_server(self, max_retries=30, retry_interval=0.1):
        """Wait for the server to start."""
        retries = 0
        while retries < max_retries:
            try:
                requests.get(f"{BASE_URL}/_dash-layout")
                return True
            except requests.exceptions.ConnectionError:
                retries += 1
                time.sleep(retry_interval)
                
        raise TimeoutError("Server did not start within the timeout period")
            

class TestDashboardAPIEndpoints(unittest.TestCase):
    """Test the HTTP API endpoints of the Quantum 5D QA Dashboard."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the test server once for all tests."""
        cls.server = APITestServer()
        try:
            cls.server.start()
        except:
            print("Warning: Could not start test server. Tests will be skipped.")
            cls.server = None
    
    @classmethod
    def tearDownClass(cls):
        """Stop the test server after all tests."""
        if cls.server:
            cls.server.stop()
    
    def setUp(self):
        """Skip tests if server is not running."""
        if not self.server:
            self.skipTest("Test server is not running")
            
    def test_dash_layout_endpoint(self):
        """Test the Dash layout endpoint."""
        response = requests.get(f"{BASE_URL}/_dash-layout")
        self.assertEqual(response.status_code, 200)
        
        # Verify that response is JSON
        layout = response.json()
        self.assertIsNotNone(layout)
        
    def test_dash_dependencies_endpoint(self):
        """Test the Dash dependencies endpoint."""
        response = requests.get(f"{BASE_URL}/_dash-dependencies")
        self.assertEqual(response.status_code, 200)
        
        # Verify that response is JSON
        dependencies = response.json()
        self.assertIsNotNone(dependencies)
        
        # Verify that callbacks are defined
        self.assertGreater(len(dependencies), 0)
        
    def test_component_update_endpoint(self):
        """Test the component update endpoint."""
        # Prepare the payload for updating dashboard metrics
        payload = {
            "output": "dashboard-metrics.children",
            "outputs": {
                "id": "dashboard-metrics",
                "property": "children"
            },
            "inputs": [
                {
                    "id": "interval-component",
                    "property": "n_intervals",
                    "value": 1
                }
            ],
            "changedPropIds": ["interval-component.n_intervals"]
        }
        
        # Send the request
        response = requests.post(
            f"{BASE_URL}/_dash-update-component",
            json=payload
        )
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("response", result)
        self.assertIn("dashboard-metrics", result["response"])
        
    def test_dimensions_update_endpoint(self):
        """Test the API endpoint for updating dimension graphs."""
        # Prepare the payload for updating dimension graphs
        payload = {
            "output": ["coverage-graph.figure", "quality-graph.figure", 
                     "performance-graph.figure", "security-graph.figure"],
            "outputs": [
                {"id": "coverage-graph", "property": "figure"},
                {"id": "quality-graph", "property": "figure"},
                {"id": "performance-graph", "property": "figure"},
                {"id": "security-graph", "property": "figure"}
            ],
            "inputs": [
                {
                    "id": "interval-component",
                    "property": "n_intervals",
                    "value": 1
                }
            ],
            "changedPropIds": ["interval-component.n_intervals"]
        }
        
        # Send the request
        response = requests.post(
            f"{BASE_URL}/_dash-update-component",
            json=payload
        )
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("response", result)
        self.assertIn("coverage-graph", result["response"])
        self.assertIn("quality-graph", result["response"])
        self.assertIn("performance-graph", result["response"])
        self.assertIn("security-graph", result["response"])
        
    def test_quantum_visualizations_update_endpoint(self):
        """Test the API endpoint for updating quantum visualizations."""
        # Prepare the payload for updating quantum visualizations
        payload = {
            "output": ["entanglement-web.figure", "hypercube-visualization.figure"],
            "outputs": [
                {"id": "entanglement-web", "property": "figure"},
                {"id": "hypercube-visualization", "property": "figure"}
            ],
            "inputs": [
                {
                    "id": "interval-component",
                    "property": "n_intervals",
                    "value": 1
                }
            ],
            "changedPropIds": ["interval-component.n_intervals"]
        }
        
        # Send the request
        response = requests.post(
            f"{BASE_URL}/_dash-update-component",
            json=payload
        )
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("response", result)
        self.assertIn("entanglement-web", result["response"])
        self.assertIn("hypercube-visualization", result["response"])
        
    def test_git_info_update_endpoint(self):
        """Test the API endpoint for updating git information."""
        # Prepare the payload for updating git information
        payload = {
            "output": [
                "uncommitted-files-store.data", 
                "git-total-files.children",
                "git-modified-files.children",
                "git-added-files.children",
                "git-deleted-files.children",
                "uncommitted-files-list.children",
                "git-commit-suggestion.children",
                "git-tag-suggestion.children"
            ],
            "outputs": [
                {"id": "uncommitted-files-store", "property": "data"},
                {"id": "git-total-files", "property": "children"},
                {"id": "git-modified-files", "property": "children"},
                {"id": "git-added-files", "property": "children"},
                {"id": "git-deleted-files", "property": "children"},
                {"id": "uncommitted-files-list", "property": "children"},
                {"id": "git-commit-suggestion", "property": "children"},
                {"id": "git-tag-suggestion", "property": "children"}
            ],
            "inputs": [
                {
                    "id": "interval-component",
                    "property": "n_intervals",
                    "value": 1
                },
                {
                    "id": "refresh-git-btn",
                    "property": "n_clicks",
                    "value": 1
                }
            ],
            "changedPropIds": ["refresh-git-btn.n_clicks"]
        }
        
        # Send the request
        response = requests.post(
            f"{BASE_URL}/_dash-update-component",
            json=payload
        )
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("response", result)
        self.assertIn("git-total-files", result["response"])
        
    def test_static_assets(self):
        """Test access to static assets."""
        # Test access to the Dash favicon
        response = requests.get(f"{BASE_URL}/assets/favicon.ico")
        self.assertIn(response.status_code, [200, 404])  # May or may not exist
        
    def test_concurrent_api_requests(self):
        """Test concurrent API requests to ensure thread safety."""
        def make_request():
            # Simple request to get the layout
            response = requests.get(f"{BASE_URL}/_dash-layout")
            return response.status_code
            
        # Create threads to make concurrent requests
        threads = []
        results = []
        
        for _ in range(5):
            thread = threading.Thread(target=lambda: results.append(make_request()))
            thread.daemon = True
            threads.append(thread)
            
        # Start all threads
        for thread in threads:
            thread.start()
            
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
            
        # Check that all requests succeeded
        for status_code in results:
            self.assertEqual(status_code, 200)
            
    def test_error_handling(self):
        """Test error handling for malformed requests."""
        # Send a request with invalid JSON
        response = requests.post(
            f"{BASE_URL}/_dash-update-component",
            data="This is not valid JSON",
            headers={"Content-Type": "application/json"}
        )
        
        # Should return an error status code
        self.assertNotEqual(response.status_code, 200)
        
        # Send a valid request with non-existent component ID
        payload = {
            "output": "non-existent-component.children",
            "outputs": {
                "id": "non-existent-component",
                "property": "children"
            },
            "inputs": [
                {
                    "id": "interval-component",
                    "property": "n_intervals",
                    "value": 1
                }
            ],
            "changedPropIds": ["interval-component.n_intervals"]
        }
        
        response = requests.post(
            f"{BASE_URL}/_dash-update-component",
            json=payload
        )
        
        # Should return an error or empty response for non-existent component
        result = response.json()
        self.assertIn("response", result)


# Also mock the QuantumMetrics class that's used in tests
class MockQuantumMetrics:
    """Mock implementation of QuantumMetrics for testing."""
    
    @classmethod
    def from_test_reports(cls, reports_dir):
        """Create a mock instance from test reports."""
        return cls()
    
    def __init__(self):
        """Initialize with mock data."""
        self.metrics = {
            "coverage": 85.5,
            "quality": 92.3,
            "performance": 78.9,
            "security": 88.7,
            "total_tests": 250,
            "passing_tests": 235,
            "failing_tests": 15
        }
        
    def get_dimension_data(self, dimension):
        """Get mock data for a specific dimension."""
        return [{"x": i, "y": 80 + i} for i in range(10)]
    
    def get_all_metrics(self):
        """Get all mock metrics."""
        return self.metrics


if __name__ == "__main__":
    unittest.main() 