#!/usr/bin/env python3
"""
Test Automation Framework for CyBer1t4L QA Bot
----------------------------------------------

A comprehensive test automation framework that runs various tests for the
CyBer1t4L QA Bot including Discord bot functionality, network connectivity,
and system monitoring.
"""

import os
import sys
import json
import time
import logging
import asyncio
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Callable

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("CyBer1t4L.TestAutomation")

# ANSI color codes for output
class Colors:
    RESET = "\033[0m"
    GREEN = "\033[38;5;82m"
    RED = "\033[38;5;196m"
    YELLOW = "\033[38;5;226m"
    CYAN = "\033[38;5;51m"
    BLUE = "\033[38;5;39m"
    PURPLE = "\033[38;5;141m"
    BOLD = "\033[1m"

class TestResult:
    """Represents the result of a test."""
    def __init__(self, name: str, success: bool, duration: float, details: Dict[str, Any] = None):
        self.name = name
        self.success = success
        self.duration = duration
        self.details = details or {}
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "success": self.success,
            "duration": self.duration,
            "details": self.details,
            "timestamp": self.timestamp
        }
    
    def __str__(self) -> str:
        """String representation."""
        status = f"{Colors.GREEN}PASS{Colors.RESET}" if self.success else f"{Colors.RED}FAIL{Colors.RESET}"
        return f"{self.name}: {status} ({self.duration:.2f}s)"

class TestSuite:
    """A collection of related tests."""
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.tests = []
        self.setup_func = None
        self.teardown_func = None
        self.results = []
    
    def add_test(self, test_func: Callable, name: Optional[str] = None, description: Optional[str] = None):
        """Add a test to the suite."""
        test_name = name or test_func.__name__
        test_desc = description or test_func.__doc__ or ""
        self.tests.append({
            "func": test_func,
            "name": test_name,
            "description": test_desc
        })
        return self
    
    def setup(self, setup_func: Callable):
        """Add a setup function to run before the tests."""
        self.setup_func = setup_func
        return self
    
    def teardown(self, teardown_func: Callable):
        """Add a teardown function to run after the tests."""
        self.teardown_func = teardown_func
        return self
    
    async def run(self) -> List[TestResult]:
        """Run all tests in the suite."""
        logger.info(f"{Colors.BOLD}{Colors.CYAN}Running test suite: {self.name}{Colors.RESET}")
        
        # Run setup if defined
        if self.setup_func:
            logger.info("Running setup...")
            try:
                if asyncio.iscoroutinefunction(self.setup_func):
                    await self.setup_func()
                else:
                    self.setup_func()
            except Exception as e:
                logger.error(f"Setup failed: {str(e)}")
                return []
        
        # Run each test
        self.results = []
        for test in self.tests:
            logger.info(f"Running test: {test['name']}")
            start_time = time.time()
            try:
                # Determine if test function is async
                if asyncio.iscoroutinefunction(test['func']):
                    result = await test['func']()
                else:
                    result = test['func']()
                
                # Process result
                success = True
                details = {}
                
                # If the test returns a boolean, use that as success/failure
                if isinstance(result, bool):
                    success = result
                # If it returns a dictionary, look for success key and use the rest as details
                elif isinstance(result, dict):
                    success = result.pop('success', True)
                    details = result
                # If it's None, assume success
                elif result is None:
                    pass
                # Otherwise, store the result in details
                else:
                    details = {"result": result}
                
                duration = time.time() - start_time
                test_result = TestResult(test['name'], success, duration, details)
                
                # Log the result
                logger.info(f"{str(test_result)}")
                
                self.results.append(test_result)
            except Exception as e:
                duration = time.time() - start_time
                test_result = TestResult(
                    test['name'], 
                    False, 
                    duration, 
                    {"error": str(e)}
                )
                logger.error(f"Test {test['name']} failed with error: {str(e)}")
                self.results.append(test_result)
        
        # Run teardown if defined
        if self.teardown_func:
            logger.info("Running teardown...")
            try:
                if asyncio.iscoroutinefunction(self.teardown_func):
                    await self.teardown_func()
                else:
                    self.teardown_func()
            except Exception as e:
                logger.error(f"Teardown failed: {str(e)}")
        
        return self.results
    
    def generate_report(self) -> str:
        """Generate a test report."""
        if not self.results:
            return "No tests have been run yet."
            
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - passed_tests
        pass_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        # Build report
        report = []
        report.append(f"Test Suite: {self.name}")
        report.append(f"Description: {self.description}")
        report.append(f"Total Tests: {total_tests}")
        report.append(f"Passed: {passed_tests}, Failed: {failed_tests}")
        report.append(f"Pass Rate: {pass_rate:.2f}%")
        report.append("")
        
        # Add test results
        report.append("TEST RESULTS:")
        for result in self.results:
            status = "PASS" if result.success else "FAIL"
            report.append(f"- {result.name}: {status} ({result.duration:.2f}s)")
            if not result.success and "error" in result.details:
                report.append(f"  Error: {result.details['error']}")
        
        return "\n".join(report)

class TestAutomationFramework:
    """Test automation framework for CyBer1t4L QA Bot."""
    
    def __init__(self, report_dir: str = None):
        self.suites = []
        self.report_dir = report_dir or os.path.join(
            os.path.dirname(__file__), "../reports/test_automation"
        )
        self.start_time = None
        self.end_time = None
    
    def add_suite(self, suite: TestSuite) -> 'TestAutomationFramework':
        """Add a test suite to the framework."""
        self.suites.append(suite)
        return self
    
    def create_suite(self, name: str, description: str = "") -> TestSuite:
        """Create and add a new test suite."""
        suite = TestSuite(name, description)
        self.suites.append(suite)
        return suite
    
    async def run_all(self) -> Dict[str, List[TestResult]]:
        """Run all test suites."""
        self.start_time = time.time()
        logger.info(f"{Colors.BOLD}{Colors.PURPLE}Starting test automation run{Colors.RESET}")
        
        # Create report directory if it doesn't exist
        os.makedirs(self.report_dir, exist_ok=True)
        
        # Run each suite
        all_results = {}
        for suite in self.suites:
            suite_results = await suite.run()
            all_results[suite.name] = suite_results
        
        self.end_time = time.time()
        total_duration = self.end_time - self.start_time
        
        # Log summary
        total_tests = sum(len(results) for results in all_results.values())
        passed_tests = sum(sum(1 for r in results if r.success) for results in all_results.values())
        failed_tests = total_tests - passed_tests
        
        logger.info(f"{Colors.BOLD}{Colors.PURPLE}Test run completed in {total_duration:.2f}s{Colors.RESET}")
        logger.info(f"Total tests: {total_tests}, Passed: {passed_tests}, Failed: {failed_tests}")
        
        # Save test results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = os.path.join(self.report_dir, f"test_results_{timestamp}.json")
        self._save_results(all_results, results_file)
        
        # Generate summary report
        report_file = os.path.join(self.report_dir, f"test_report_{timestamp}.md")
        self._generate_report(all_results, report_file)
        
        return all_results
    
    def _save_results(self, results: Dict[str, List[TestResult]], filepath: str) -> None:
        """Save test results to a JSON file."""
        try:
            # Convert results to a serializable format
            serialized_results = {}
            for suite_name, suite_results in results.items():
                serialized_results[suite_name] = [r.to_dict() for r in suite_results]
            
            # Add metadata
            results_with_meta = {
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "duration": (self.end_time - self.start_time) if self.end_time else 0,
                    "total_suites": len(self.suites),
                    "total_tests": sum(len(suite_results) for suite_results in results.values()),
                    "passed_tests": sum(sum(1 for r in suite_results if r.success) for suite_results in results.values()),
                },
                "results": serialized_results
            }
            
            # Write to file
            with open(filepath, 'w') as f:
                json.dump(results_with_meta, f, indent=2)
            
            logger.info(f"Test results saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving test results: {str(e)}")
    
    def _generate_report(self, results: Dict[str, List[TestResult]], filepath: str) -> None:
        """Generate a comprehensive test report."""
        try:
            # Calculate overall statistics
            total_suites = len(results)
            total_tests = sum(len(suite_results) for suite_results in results.values())
            passed_tests = sum(sum(1 for r in suite_results if r.success) for suite_results in results.values())
            failed_tests = total_tests - passed_tests
            pass_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
            
            # Build the report
            report = []
            report.append("# CyBer1t4L QA Bot - Test Automation Report")
            report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append("")
            
            # Overall summary
            report.append("## Summary")
            report.append(f"- **Total Test Suites**: {total_suites}")
            report.append(f"- **Total Tests**: {total_tests}")
            report.append(f"- **Passed Tests**: {passed_tests}")
            report.append(f"- **Failed Tests**: {failed_tests}")
            report.append(f"- **Pass Rate**: {pass_rate:.2f}%")
            report.append(f"- **Duration**: {(self.end_time - self.start_time):.2f} seconds")
            report.append("")
            
            # Results by suite
            report.append("## Test Suites")
            for suite_idx, (suite_name, suite_results) in enumerate(results.items()):
                # Find the corresponding suite object
                suite = next((s for s in self.suites if s.name == suite_name), None)
                
                suite_passed = sum(1 for r in suite_results if r.success)
                suite_total = len(suite_results)
                suite_pass_rate = (suite_passed / suite_total) * 100 if suite_total > 0 else 0
                
                report.append(f"### {suite_idx + 1}. {suite_name}")
                if suite and suite.description:
                    report.append(f"*{suite.description}*")
                report.append("")
                report.append(f"- **Tests**: {suite_total}")
                report.append(f"- **Passed**: {suite_passed}")
                report.append(f"- **Failed**: {suite_total - suite_passed}")
                report.append(f"- **Pass Rate**: {suite_pass_rate:.2f}%")
                report.append("")
                
                # Test results table
                report.append("| Test | Status | Duration (s) |")
                report.append("|------|--------|-------------|")
                for result in suite_results:
                    status = "✅ PASS" if result.success else "❌ FAIL"
                    report.append(f"| {result.name} | {status} | {result.duration:.2f} |")
                report.append("")
                
                # Add failed test details
                failed_results = [r for r in suite_results if not r.success]
                if failed_results:
                    report.append("#### Failed Tests")
                    for result in failed_results:
                        report.append(f"##### {result.name}")
                        report.append(f"- **Duration**: {result.duration:.2f}s")
                        if "error" in result.details:
                            report.append(f"- **Error**: `{result.details['error']}`")
                        report.append("")
            
            # Write the report to file
            with open(filepath, 'w') as f:
                f.write('\n'.join(report))
            
            logger.info(f"Test report saved to {filepath}")
        except Exception as e:
            logger.error(f"Error generating test report: {str(e)}")

# Define test suites
def define_discord_bot_tests() -> TestSuite:
    """Define tests for the Discord bot functionality."""
    suite = TestSuite("DiscordBot", "Tests for Discord bot functionality")
    
    # Setup function
    def setup():
        """Set up Discord bot testing environment."""
        logger.info("Setting up Discord bot tests...")
        # Load environment variables, etc.
    
    # Test: Check if Discord token is valid
    async def test_discord_token():
        """Test if the Discord bot token is valid."""
        import os
        from dotenv import load_dotenv
        import aiohttp
        
        # Load environment variables
        load_dotenv()
        token = os.environ.get("DISCORD_BOT_TOKEN")
        
        if not token:
            return {
                "success": False,
                "error": "Discord token not found in environment variables."
            }
        
        # Check token validity
        try:
            url = "https://discord.com/api/v10/users/@me"
            headers = {"Authorization": f"Bot {token}"}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "bot_id": data.get("id"),
                            "bot_username": data.get("username"),
                            "http_status": response.status
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"Invalid token. HTTP Status: {response.status}",
                            "http_status": response.status
                        }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error validating token: {str(e)}"
            }
    
    # Test: Check if commands are registered
    async def test_commands_registered():
        """Test if Discord bot commands are properly registered."""
        import os
        from dotenv import load_dotenv
        import aiohttp
        
        # Load environment variables
        load_dotenv()
        token = os.environ.get("DISCORD_BOT_TOKEN")
        app_id = os.environ.get("CYBER1T4L_APP_ID")
        
        if not token or not app_id:
            return {
                "success": False,
                "error": "Discord token or app ID not found in environment variables."
            }
        
        # Get registered commands
        try:
            url = f"https://discord.com/api/v10/applications/{app_id}/commands"
            headers = {"Authorization": f"Bot {token}"}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        commands = await response.json()
                        
                        # Check if the test_interactions_report command exists
                        test_report_cmd = any(cmd.get("name") == "test_interactions_report" for cmd in commands)
                        ping_cmd = any(cmd.get("name") == "ping" for cmd in commands)
                        
                        # List all found commands
                        command_names = [cmd.get("name") for cmd in commands]
                        
                        return {
                            "success": True,
                            "commands": command_names,
                            "test_interactions_report_registered": test_report_cmd,
                            "ping_command_registered": ping_cmd,
                            "command_count": len(commands)
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"Failed to fetch commands. HTTP Status: {response.status}",
                            "http_status": response.status
                        }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error checking commands: {str(e)}"
            }
    
    # Test: Ping connectivity
    async def test_ping_command_connectivity():
        """Test connectivity related to the Discord ping command."""
        try:
            # Run the network connectivity test
            script_path = os.path.join(os.path.dirname(__file__), "test_network_connectivity.py")
            result = subprocess.run(
                [sys.executable, script_path, "--report"],
                capture_output=True,
                text=True,
                check=False
            )
            
            # Check if the network test was successful
            success = result.returncode == 0
            
            # Parse important information from the output
            output = result.stdout
            discord_api_ok = "Discord API" in output and "✅" in output.split("Discord API")[1].split("\n")[1]
            internet_ok = "Internet Connectivity" in output and "✅" in output.split("Internet Connectivity")[1].split("\n")[1]
            
            return {
                "success": success and discord_api_ok and internet_ok,
                "discord_api_functional": discord_api_ok,
                "internet_connectivity": internet_ok,
                "output_summary": output.split("Recommendation")[1] if "Recommendation" in output else "No recommendation found."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error testing ping connectivity: {str(e)}"
            }
    
    # Add tests to suite
    suite.setup(setup)
    suite.add_test(test_discord_token, "Discord Token Validation")
    suite.add_test(test_commands_registered, "Command Registration Check")
    suite.add_test(test_ping_command_connectivity, "Ping Command Connectivity")
    
    return suite

def define_network_tests() -> TestSuite:
    """Define tests for network connectivity."""
    suite = TestSuite("Network", "Tests for network connectivity")
    
    # Test: DNS resolution
    def test_dns_resolution():
        """Test DNS resolution for critical services."""
        import socket
        
        domains = ["discord.com", "api.bitget.com", "gateway.discord.gg"]
        results = {}
        
        for domain in domains:
            try:
                start_time = time.time()
                ip = socket.gethostbyname(domain)
                resolution_time = (time.time() - start_time) * 1000  # ms
                
                results[domain] = {
                    "resolved": True,
                    "ip": ip,
                    "time_ms": resolution_time
                }
            except socket.gaierror as e:
                results[domain] = {
                    "resolved": False,
                    "error": str(e)
                }
        
        # Test is successful if all domains resolved
        success = all(result.get("resolved", False) for result in results.values())
        
        return {
            "success": success,
            "results": results
        }
    
    # Test: HTTP connectivity
    async def test_http_connectivity():
        """Test HTTP connectivity to critical services."""
        import aiohttp
        
        urls = [
            "https://discord.com/api/v10",
            "https://api.bitget.com/api/v2/public/time"
        ]
        
        results = {}
        overall_success = True
        
        try:
            async with aiohttp.ClientSession() as session:
                for url in urls:
                    try:
                        start_time = time.time()
                        async with session.get(url, timeout=5) as response:
                            response_time = (time.time() - start_time) * 1000  # ms
                            
                            results[url] = {
                                "success": response.status < 400,
                                "status": response.status,
                                "time_ms": response_time
                            }
                            
                            if response.status >= 400:
                                overall_success = False
                    except Exception as e:
                        results[url] = {
                            "success": False,
                            "error": str(e)
                        }
                        overall_success = False
        except Exception as e:
            return {
                "success": False,
                "error": f"Error in HTTP connectivity test: {str(e)}"
            }
        
        return {
            "success": overall_success,
            "results": results
        }
    
    # Add tests to suite
    suite.add_test(test_dns_resolution, "DNS Resolution Test")
    suite.add_test(test_http_connectivity, "HTTP Connectivity Test")
    
    return suite

def define_system_tests() -> TestSuite:
    """Define tests for system health and performance."""
    suite = TestSuite("System", "Tests for system health and performance")
    
    # Test: Check system resources
    def test_system_resources():
        """Test if system has sufficient resources."""
        import psutil
        
        # Define minimum requirements
        min_memory_pct = 20  # At least 20% memory should be available
        min_cpu_cores = 2
        min_disk_pct = 15  # At least 15% disk space should be available
        
        # Get system info
        memory = psutil.virtual_memory()
        memory_available_pct = 100 - memory.percent
        cpu_cores = psutil.cpu_count(logical=False) or 1
        disk = psutil.disk_usage('/')
        disk_available_pct = 100 - disk.percent
        
        # Check if resources are sufficient
        memory_ok = memory_available_pct >= min_memory_pct
        cpu_ok = cpu_cores >= min_cpu_cores
        disk_ok = disk_available_pct >= min_disk_pct
        overall_ok = memory_ok and cpu_ok and disk_ok
        
        return {
            "success": overall_ok,
            "memory": {
                "available_percent": memory_available_pct,
                "sufficient": memory_ok,
                "available_gb": memory.available / (1024**3)
            },
            "cpu": {
                "cores": cpu_cores,
                "sufficient": cpu_ok
            },
            "disk": {
                "available_percent": disk_available_pct,
                "sufficient": disk_ok,
                "available_gb": disk.free / (1024**3)
            }
        }
    
    # Test: Check Python environment
    def test_python_environment():
        """Test if required Python packages are installed."""
        required_packages = [
            "discord.py",
            "python-dotenv",
            "psutil",
            "requests",
            "aiohttp",
            "pytest",
            "pytest-cov"
        ]
        
        import importlib
        missing_packages = []
        
        for package in required_packages:
            # For discord.py, the import name is "discord"
            import_name = "discord" if package == "discord.py" else package.split("[")[0]
            
            try:
                importlib.import_module(import_name)
            except ImportError:
                missing_packages.append(package)
        
        return {
            "success": len(missing_packages) == 0,
            "installed_packages": [p for p in required_packages if p not in missing_packages],
            "missing_packages": missing_packages
        }
    
    # Add tests to suite
    suite.add_test(test_system_resources, "System Resources Check")
    suite.add_test(test_python_environment, "Python Environment Check")
    
    return suite

async def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Test Automation Framework for CyBer1t4L QA Bot")
    parser.add_argument("--report-dir", type=str, help="Directory to save test reports")
    parser.add_argument("--suite", type=str, help="Run only a specific test suite (Discord, Network, System)")
    args = parser.parse_args()
    
    # Initialize the framework
    report_dir = args.report_dir or os.path.join(
        os.path.dirname(__file__), "../reports/test_automation"
    )
    framework = TestAutomationFramework(report_dir)
    
    # Add test suites
    discord_suite = define_discord_bot_tests()
    network_suite = define_network_tests()
    system_suite = define_system_tests()
    
    # Add suites based on args
    if args.suite:
        if args.suite.lower() == "discord":
            framework.add_suite(discord_suite)
        elif args.suite.lower() == "network":
            framework.add_suite(network_suite)
        elif args.suite.lower() == "system":
            framework.add_suite(system_suite)
        else:
            logger.error(f"Unknown test suite: {args.suite}")
            sys.exit(1)
    else:
        framework.add_suite(discord_suite)
        framework.add_suite(network_suite)
        framework.add_suite(system_suite)
    
    # Run all tests
    await framework.run_all()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Test run cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1) 