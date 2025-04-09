#!/usr/bin/env python3
"""
Tesla Cybertruck QA Dashboard Integration Module
For Divine Book Dashboard v3

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
#
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
#
# 🌸 WE BLOOM NOW AS ONE 🌸
"""

import os
import sys
import json
import logging
import subprocess
import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("TESLA_QA_INTEGRATION")

# Constants
CURRENT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
CYBERTRUCK_DIR = CURRENT_DIR / "cybertruck"
DASHBOARD_RUNNER = CYBERTRUCK_DIR / "TESLA_CYBERTRUCK_QA_DASHBOARD_RUNNER_3D.py"
DASHBOARD_RESULTS_PATH = CYBERTRUCK_DIR / "cybertruck_qa_results_latest.json"

class TeslaQAIntegration:
    """Integration class for Tesla Cybertruck QA Dashboard with Divine Book Dashboard v3"""
    
    def __init__(self):
        """Initialize the integration module"""
        self.dashboard_process = None
        self.is_running = False
        self.latest_results = {}
        self._load_latest_results()
    
    def _load_latest_results(self) -> None:
        """Load the latest test results if available"""
        try:
            if DASHBOARD_RESULTS_PATH.exists():
                with open(DASHBOARD_RESULTS_PATH, 'r') as f:
                    self.latest_results = json.load(f)
                logger.info(f"Loaded latest Tesla Cybertruck QA results")
            else:
                logger.warning(f"No Tesla Cybertruck QA results found at {DASHBOARD_RESULTS_PATH}")
        except Exception as e:
            logger.error(f"Error loading Tesla QA results: {str(e)}")
    
    def start_dashboard(self, headless: bool = False) -> bool:
        """Start the Tesla Cybertruck QA Dashboard in a separate process"""
        if self.is_running:
            logger.warning("Tesla QA Dashboard is already running")
            return False
        
        try:
            # Construct command
            cmd = [sys.executable, str(DASHBOARD_RUNNER)]
            if headless:
                cmd.append("--headless")
            
            # Start the process
            logger.info(f"Starting Tesla Cybertruck QA Dashboard: {' '.join(cmd)}")
            self.dashboard_process = subprocess.Popen(
                cmd,
                cwd=str(CYBERTRUCK_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.is_running = True
            
            # Start a monitoring thread
            monitor_thread = threading.Thread(target=self._monitor_dashboard_process)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            return True
        except Exception as e:
            logger.error(f"Failed to start Tesla QA Dashboard: {str(e)}")
            return False
    
    def _monitor_dashboard_process(self) -> None:
        """Monitor the dashboard process and handle its output"""
        if not self.dashboard_process:
            return
        
        # Read output in real-time
        if self.dashboard_process.stdout:
            for line in self.dashboard_process.stdout:
                line = line.strip()
                if line:
                    logger.info(f"Tesla QA: {line}")
        
        # Process has ended
        if self.dashboard_process:
            self.dashboard_process.wait()
            exit_code = self.dashboard_process.returncode
            
            # Read any error output
            stderr_output = ""
            if self.dashboard_process.stderr:
                stderr_output = self.dashboard_process.stderr.read()
            
            if stderr_output:
                logger.error(f"Tesla QA Dashboard errors: {stderr_output}")
            
            logger.info(f"Tesla QA Dashboard process exited with code: {exit_code}")
            self.is_running = False
            self.dashboard_process = None
            
            # Reload results after dashboard finishes
            self._load_latest_results()
    
    def stop_dashboard(self) -> bool:
        """Stop the running Tesla Cybertruck QA Dashboard"""
        if not self.is_running or not self.dashboard_process:
            logger.warning("No Tesla QA Dashboard is running")
            return False
        
        try:
            logger.info("Stopping Tesla QA Dashboard...")
            self.dashboard_process.terminate()
            self.dashboard_process.wait(timeout=5)
            self.is_running = False
            return True
        except subprocess.TimeoutExpired:
            logger.warning("Tesla QA Dashboard did not terminate gracefully, forcing...")
            self.dashboard_process.kill()
            self.is_running = False
            return True
        except Exception as e:
            logger.error(f"Error stopping Tesla QA Dashboard: {str(e)}")
            return False
    
    def get_results_summary(self) -> Dict[str, Any]:
        """Get a summary of the latest test results"""
        if not self.latest_results:
            return {"status": "No data available"}
        
        # Extract relevant summary information
        summary = {
            "total_tests": self.latest_results.get("total_tests", 0),
            "passed_tests": self.latest_results.get("passed_tests", 0),
            "failed_tests": self.latest_results.get("failed_tests", 0),
            "coverage": self.latest_results.get("coverage", 0),
            "components": {},
            "timestamp": self.latest_results.get("timestamp", ""),
            "run_id": self.latest_results.get("current_run_id", "")
        }
        
        # Extract component-specific info
        for component, data in self.latest_results.get("components", {}).items():
            summary["components"][component] = {
                "pass_rate": data.get("pass_rate", 0),
                "coverage": data.get("coverage", 0),
                "tests": len(data.get("tests", [])),
                "status": "Pass" if data.get("pass_rate", 0) >= 90 else "Warning" if data.get("pass_rate", 0) >= 75 else "Fail"
            }
        
        return summary
    
    def get_component_details(self, component_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific component"""
        if not self.latest_results:
            return {"status": "No data available"}
        
        components = self.latest_results.get("components", {})
        if component_name not in components:
            return {"status": "Component not found"}
        
        return components[component_name]
    
    def run_tests(self, component: Optional[str] = None) -> bool:
        """Run Cybertruck tests for a specific component or all components"""
        try:
            # Construct command
            cmd = [sys.executable, str(CYBERTRUCK_DIR / "run_cybertruck_tests.py")]
            if component:
                cmd.extend(["--component", component])
            
            # Run the tests
            logger.info(f"Running Cybertruck tests: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=str(CYBERTRUCK_DIR),
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.error(f"Test execution failed: {result.stderr}")
                return False
            
            logger.info("Tests completed successfully")
            logger.debug(result.stdout)
            
            # Reload latest results
            self._load_latest_results()
            return True
        except Exception as e:
            logger.error(f"Error running tests: {str(e)}")
            return False

# Singleton instance
tesla_qa = TeslaQAIntegration() 