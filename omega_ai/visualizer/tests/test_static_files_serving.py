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
Tests for static file serving in the Reggae Dashboard server.
"""

import unittest
import requests
import os
import time
import subprocess
import signal
import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))


class TestStaticFileServing(unittest.TestCase):
    """Tests for static file serving from the Reggae Dashboard server."""
    
    server_process = None
    server_url = "http://localhost:5001"
    
    @classmethod
    def setUpClass(cls):
        """Start the server before running tests."""
        # Kill any existing server processes
        try:
            subprocess.run(["pkill", "-f", "reggae_dashboard_server.py"], check=False)
            time.sleep(1)  # Give it time to shut down
        except Exception as e:
            logger.warning(f"Error killing existing server processes: {e}")
        
        # Start the server
        server_script = project_root / "omega_ai" / "visualizer" / "backend" / "reggae_dashboard_server.py"
        cmd = [sys.executable, str(server_script), "--port", "5001"]
        
        try:
            # Start server with specific port
            cls.server_process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logger.info(f"Started server process with PID {cls.server_process.pid}")
            
            # Wait for server to start
            time.sleep(2)
            
            # Verify server is running
            try:
                response = requests.get(f"{cls.server_url}/api/health", timeout=5)
                if response.status_code != 200:
                    logger.error(f"Server health check failed with status code {response.status_code}")
                    cls.tearDownClass()
                    raise Exception("Server failed to start properly")
            except requests.RequestException as e:
                logger.error(f"Server health check failed: {e}")
                cls.tearDownClass()
                raise Exception("Server failed to start or respond to health check")
                
        except Exception as e:
            logger.error(f"Error starting server: {e}")
            if cls.server_process:
                cls.server_process.terminate()
                cls.server_process = None
            raise
    
    @classmethod
    def tearDownClass(cls):
        """Stop the server after running tests."""
        if cls.server_process:
            logger.info(f"Stopping server process with PID {cls.server_process.pid}")
            cls.server_process.terminate()
            cls.server_process.wait(timeout=5)
            cls.server_process = None
    
    def test_dashboard_route(self):
        """Test that /dashboard route exists and serves files."""
        response = requests.get(f"{self.server_url}/dashboard/")
        self.assertEqual(response.status_code, 200, "Dashboard route should return 200 OK")
    
    def test_big_brother_styles_css(self):
        """Test that the Big Brother styles CSS file is served correctly."""
        response = requests.get(f"{self.server_url}/dashboard/big_brother_styles.css")
        self.assertEqual(response.status_code, 200, "CSS file should be accessible")
        self.assertIn("text/css", response.headers.get("Content-Type", ""), 
                      "Response should be of type text/css")
        self.assertTrue(len(response.text) > 100, "CSS file should have content")
    
    def test_big_brother_panel_js(self):
        """Test that the Big Brother panel JS file is served correctly."""
        response = requests.get(f"{self.server_url}/dashboard/big_brother_panel.js")
        self.assertEqual(response.status_code, 200, "JS file should be accessible")
        self.assertIn("javascript", response.headers.get("Content-Type", ""), 
                     "Response should be of type javascript")
        self.assertTrue(len(response.text) > 100, "JS file should have content")
    
    def test_big_brother_panel_html(self):
        """Test that the Big Brother panel HTML file is served correctly."""
        response = requests.get(f"{self.server_url}/big-brother")
        self.assertEqual(response.status_code, 200, "Big Brother panel should be accessible")
        self.assertIn("text/html", response.headers.get("Content-Type", ""), 
                     "Response should be of type text/html")
        self.assertIn("<script", response.text, "HTML should contain script tag")
        self.assertIn("big-brother-panel", response.text, "HTML should contain panel elements")
    

if __name__ == "__main__":
    unittest.main() 