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
QA Metrics Collector for CyBer1t4L QA Bot
-----------------------------------------

This module collects and analyzes comprehensive quality metrics including:
- Test coverage metrics
- Response time measurements
- System performance stats
- API reliability metrics
- Error rate tracking
- Test success/failure statistics
- Network connectivity metrics
- Security verification
"""

import os
import sys
import json
import time
import logging
import socket
import requests
import subprocess
import datetime
import platform
import psutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("CyBer1t4L.QAMetrics")

@dataclass
class TestCoverageMetrics:
    """Test coverage metrics data."""
    total_coverage: float = 0.0
    statements: int = 0
    missing: int = 0
    modules: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    def update_from_json(self, coverage_data: Dict[str, Any]) -> None:
        """Update metrics from coverage data JSON."""
        self.total_coverage = coverage_data.get("total_coverage", 0.0)
        self.statements = coverage_data.get("total_statements", 0)
        self.missing = coverage_data.get("total_missed", 0)
        self.modules = coverage_data.get("modules", {})
        self.timestamp = coverage_data.get("timestamp", datetime.datetime.now().isoformat())

@dataclass
class PerformanceMetrics:
    """System performance metrics data."""
    cpu_percent: float = 0.0
    memory_usage: float = 0.0
    memory_available: float = 0.0
    disk_usage: float = 0.0
    process_count: int = 0
    boot_time: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    def update(self) -> None:
        """Update system performance metrics."""
        self.cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        self.memory_usage = memory.percent
        self.memory_available = memory.available / (1024 * 1024 * 1024)  # GB
        disk = psutil.disk_usage('/')
        self.disk_usage = disk.percent
        self.process_count = len(psutil.pids())
        self.boot_time = psutil.boot_time()
        self.timestamp = datetime.datetime.now().isoformat()

@dataclass
class NetworkMetrics:
    """Network connectivity and performance metrics."""
    ping_latency: Dict[str, float] = field(default_factory=dict)
    dns_lookup_time: Dict[str, float] = field(default_factory=dict)
    connectivity_status: Dict[str, bool] = field(default_factory=dict)
    http_response_times: Dict[str, float] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    def check_connectivity(self, targets: Optional[List[str]] = None) -> None:
        """Test connectivity to specified targets."""
        if targets is None:
            targets = ["8.8.8.8", "1.1.1.1", "discord.com", "api.bitget.com"]
        
        # Reset metrics
        self.ping_latency = {}
        self.dns_lookup_time = {}
        self.connectivity_status = {}
        self.http_response_times = {}
        
        # Check connectivity to each target
        for target in targets:
            # Check if target is pingable
            try:
                start_time = time.time()
                ping_result = subprocess.run(
                    ["ping", "-c", "1", "-W", "2", target],
                    capture_output=True, text=True, check=False
                )
                end_time = time.time()
                
                self.connectivity_status[target] = ping_result.returncode == 0
                if ping_result.returncode == 0:
                    self.ping_latency[target] = round((end_time - start_time) * 1000, 2)  # ms
                else:
                    self.ping_latency[target] = -1  # Error
            except Exception as e:
                logger.error(f"Error pinging {target}: {str(e)}")
                self.connectivity_status[target] = False
                self.ping_latency[target] = -1
            
            # Check DNS lookup time
            try:
                start_time = time.time()
                socket.gethostbyname(target)
                end_time = time.time()
                
                self.dns_lookup_time[target] = round((end_time - start_time) * 1000, 2)  # ms
            except Exception as e:
                logger.error(f"Error resolving DNS for {target}: {str(e)}")
                self.dns_lookup_time[target] = -1
            
            # Check HTTP response times for web services
            if target not in ["8.8.8.8", "1.1.1.1"]:
                try:
                    url = f"https://{target}"
                    start_time = time.time()
                    response = requests.get(url, timeout=5)
                    end_time = time.time()
                    
                    self.http_response_times[target] = round((end_time - start_time) * 1000, 2)  # ms
                except Exception as e:
                    logger.error(f"Error making HTTP request to {target}: {str(e)}")
                    self.http_response_times[target] = -1
        
        self.timestamp = datetime.datetime.now().isoformat()

@dataclass
class SecurityMetrics:
    """Security check metrics."""
    ssl_certificates: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    ports_open: Dict[int, bool] = field(default_factory=dict)
    firewall_active: bool = False
    discord_token_secure: bool = False
    api_keys_secure: bool = False
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    def check_security(self, 
                       domains: Optional[List[str]] = None,
                       ports: Optional[List[int]] = None) -> None:
        """Run security checks."""
        if domains is None:
            domains = ["discord.com", "api.bitget.com"]
        
        if ports is None:
            ports = [80, 443, 8080, 22]
        
        # Check SSL certificates
        for domain in domains:
            try:
                # This is a simplified check, in production you'd want to use a library like pyOpenSSL
                output = subprocess.run(
                    ["openssl", "s_client", "-connect", f"{domain}:443", "-servername", domain],
                    input=b'Q\n',  # Send 'Q' to quit after connecting
                    capture_output=True, text=True, check=False
                )
                
                # Extract certificate info
                cert_info = {}
                cert_text = output.stdout
                
                if "-----BEGIN CERTIFICATE-----" in cert_text:
                    # Parse basic certificate info
                    if "subject=" in cert_text:
                        cert_info["subject"] = cert_text.split("subject=")[1].split("\n")[0]
                    if "issuer=" in cert_text:
                        cert_info["issuer"] = cert_text.split("issuer=")[1].split("\n")[0]
                    if "Verify return code:" in cert_text:
                        verify_line = [line for line in cert_text.split("\n") if "Verify return code:" in line][0]
                        cert_info["verify_code"] = verify_line.strip()
                        cert_info["verified"] = "Verify return code: 0 (ok)" in verify_line
                else:
                    cert_info["error"] = "Could not retrieve certificate"
                    cert_info["verified"] = False
                
                self.ssl_certificates[domain] = cert_info
            except Exception as e:
                logger.error(f"Error checking SSL for {domain}: {str(e)}")
                self.ssl_certificates[domain] = {"error": str(e), "verified": False}
        
        # Check open ports (basic check)
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('127.0.0.1', port))
                self.ports_open[port] = (result == 0)
                sock.close()
            except Exception as e:
                logger.error(f"Error checking port {port}: {str(e)}")
                self.ports_open[port] = False
        
        # Check if firewall is active (basic check for macOS/Linux)
        try:
            if platform.system() == "Darwin":  # macOS
                result = subprocess.run(
                    ["defaults", "read", "/Library/Preferences/com.apple.alf", "globalstate"],
                    capture_output=True, text=True, check=False
                )
                self.firewall_active = result.stdout.strip() != "0"
            elif platform.system() == "Linux":
                result = subprocess.run(
                    ["sudo", "ufw", "status"],
                    capture_output=True, text=True, check=False
                )
                self.firewall_active = "Status: active" in result.stdout
            elif platform.system() == "Windows":
                result = subprocess.run(
                    ["netsh", "advfirewall", "show", "currentprofile"],
                    capture_output=True, text=True, check=False
                )
                self.firewall_active = "State                      ON" in result.stdout
        except Exception as e:
            logger.error(f"Error checking firewall status: {str(e)}")
            self.firewall_active = False
        
        # Check if Discord token is securely stored
        env_path = Path(os.path.join(os.path.dirname(__file__), '../../.env'))
        if env_path.exists():
            try:
                with open(env_path, 'r') as f:
                    env_content = f.read()
                    # Check if token is in .env file and not hardcoded elsewhere
                    self.discord_token_secure = "DISCORD_BOT_TOKEN" in env_content
                    # Check if API keys are in .env file and not hardcoded elsewhere
                    self.api_keys_secure = "API_KEY" in env_content or "SECRET_KEY" in env_content
            except Exception as e:
                logger.error(f"Error checking token security: {str(e)}")
                self.discord_token_secure = False
                self.api_keys_secure = False
        else:
            self.discord_token_secure = False
            self.api_keys_secure = False
        
        self.timestamp = datetime.datetime.now().isoformat()

@dataclass
class TestSuccessMetrics:
    """Test success/failure metrics."""
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    error: int = 0
    duration: float = 0.0
    tests_by_module: Dict[str, Dict[str, int]] = field(default_factory=dict)
    test_failures: List[Dict[str, Any]] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    def update_from_pytest_results(self, result_output: str) -> None:
        """Parse pytest output to extract test success metrics."""
        try:
            # Extract total tests and statuses
            total_line = [line for line in result_output.split('\n') if "collected " in line]
            if total_line:
                total_str = total_line[0]
                self.total_tests = int(total_str.split("collected ")[1].split(" ")[0])
            
            # Extract passed, failed, etc.
            summary_line = [line for line in result_output.split('\n') if " passed, " in line or " failed, " in line]
            if summary_line:
                summary = summary_line[0]
                if " passed, " in summary:
                    self.passed = int(summary.split(" passed")[0].split()[-1])
                if " failed, " in summary:
                    self.failed = int(summary.split(" failed")[0].split()[-1])
                if " skipped, " in summary:
                    self.skipped = int(summary.split(" skipped")[0].split()[-1])
                if " error" in summary:
                    self.error = int(summary.split(" error")[0].split()[-1])
            
            # Extract duration
            time_line = [line for line in result_output.split('\n') if " seconds " in line]
            if time_line:
                time_str = time_line[0]
                self.duration = float(time_str.split(" seconds")[0].split()[-1])
            
            # Extract failures
            self.test_failures = []
            failure_sections = result_output.split("=== FAILURES ===")
            if len(failure_sections) > 1:
                failures_text = failure_sections[1]
                failure_blocks = failures_text.split("___ ")[1:]  # Skip the first empty part
                
                for block in failure_blocks:
                    test_name = block.split(" ___")[0]
                    error_msg = block.split("\n")[1:] if "\n" in block else ["Unknown error"]
                    self.test_failures.append({
                        "test_name": test_name,
                        "error": "\n".join(error_msg[:5])  # First 5 lines of error
                    })
            
            # Set timestamp
            self.timestamp = datetime.datetime.now().isoformat()
        except Exception as e:
            logger.error(f"Error parsing pytest results: {str(e)}")

@dataclass 
class APIMetrics:
    """API reliability and performance metrics."""
    endpoints: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    response_times: Dict[str, List[float]] = field(default_factory=dict)
    error_rates: Dict[str, float] = field(default_factory=dict)
    availability: Dict[str, float] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    def test_api_endpoints(self, 
                          endpoints: Optional[List[Tuple[str, str, Dict[str, Any]]]] = None) -> None:
        """Test API endpoints for reliability and performance."""
        if endpoints is None:
            # Default endpoints to test - tuple of (name, url, request_params)
            endpoints = [
                ("discord_gateway", "https://discord.com/api/v10/gateway", {}),
                ("discord_api", "https://discord.com/api/v10", {}),
                ("bitget_api", "https://api.bitget.com/api/v2/public/time", {})
            ]
        
        for name, url, params in endpoints:
            if name not in self.response_times:
                self.response_times[name] = []
            
            self.endpoints[name] = {"url": url, "last_status": None}
            
            try:
                # Make request
                start_time = time.time()
                response = requests.get(url, timeout=5, **params)
                end_time = time.time()
                
                # Record response time
                response_time = (end_time - start_time) * 1000  # ms
                self.response_times[name].append(response_time)
                
                # Keep only the most recent 100 response times
                if len(self.response_times[name]) > 100:
                    self.response_times[name] = self.response_times[name][-100:]
                
                # Update metrics
                self.endpoints[name].update({
                    "last_status": response.status_code,
                    "last_response_time": response_time,
                    "last_checked": datetime.datetime.now().isoformat()
                })
                
                # Calculate error rate
                success_count = len([t for t in self.response_times[name] 
                                    if t >= 0])  # Negative times indicate errors
                self.error_rates[name] = 1 - (success_count / len(self.response_times[name])) \
                                        if self.response_times[name] else 0
                
                # Calculate availability (% of time it's responsive)
                self.availability[name] = success_count / max(1, len(self.response_times[name]))
                
            except Exception as e:
                logger.error(f"Error calling {name} API at {url}: {str(e)}")
                self.response_times[name].append(-1)  # Use -1 to indicate error
                self.endpoints[name].update({
                    "last_status": None,
                    "error": str(e),
                    "last_checked": datetime.datetime.now().isoformat()
                })
                
                # Update error rate and availability
                success_count = len([t for t in self.response_times[name] if t >= 0])
                self.error_rates[name] = 1 - (success_count / len(self.response_times[name])) \
                                        if self.response_times[name] else 1
                self.availability[name] = success_count / max(1, len(self.response_times[name]))
        
        self.timestamp = datetime.datetime.now().isoformat()

@dataclass
class QAMetrics:
    """Complete collection of QA metrics."""
    coverage: TestCoverageMetrics = field(default_factory=TestCoverageMetrics)
    performance: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    network: NetworkMetrics = field(default_factory=NetworkMetrics)
    security: SecurityMetrics = field(default_factory=SecurityMetrics)
    tests: TestSuccessMetrics = field(default_factory=TestSuccessMetrics)
    api: APIMetrics = field(default_factory=APIMetrics)
    collection_timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    system_info: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize system info."""
        self.system_info = {
            "os": platform.platform(),
            "python": platform.python_version(),
            "hostname": socket.gethostname(),
            "processor": platform.processor(),
            "cpu_count": str(psutil.cpu_count()),
            "memory_total": f"{psutil.virtual_memory().total / (1024**3):.2f} GB"
        }
    
    def collect_all_metrics(self) -> None:
        """Collect all QA metrics."""
        # Update performance metrics
        self.performance.update()
        
        # Check network connectivity
        self.network.check_connectivity()
        
        # Check security
        self.security.check_security()
        
        # Test API endpoints
        self.api.test_api_endpoints()
        
        # Update collection timestamp
        self.collection_timestamp = datetime.datetime.now().isoformat()
    
    def save_to_file(self, filepath: str) -> None:
        """Save metrics to a JSON file."""
        with open(filepath, 'w') as f:
            json.dump(asdict(self), f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'QAMetrics':
        """Load metrics from a JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        metrics = cls()
        
        # Load coverage metrics
        metrics.coverage = TestCoverageMetrics(**data.get('coverage', {}))
        
        # Load performance metrics
        metrics.performance = PerformanceMetrics(**data.get('performance', {}))
        
        # Load network metrics
        metrics.network = NetworkMetrics(**data.get('network', {}))
        
        # Load security metrics
        metrics.security = SecurityMetrics(**data.get('security', {}))
        
        # Load test success metrics
        metrics.tests = TestSuccessMetrics(**data.get('tests', {}))
        
        # Load API metrics
        metrics.api = APIMetrics(**data.get('api', {}))
        
        # Load other fields
        metrics.collection_timestamp = data.get('collection_timestamp', datetime.datetime.now().isoformat())
        metrics.system_info = data.get('system_info', {})
        
        return metrics
    
    def generate_report(self) -> str:
        """Generate a human-readable report of the metrics."""
        report = []
        report.append("# CyBer1t4L QA Metrics Report")
        report.append(f"Generated on: {self.collection_timestamp}")
        report.append(f"System: {self.system_info.get('os', 'Unknown')}")
        report.append("")
        
        # Coverage summary
        report.append("## Test Coverage")
        report.append(f"Total Coverage: {self.coverage.total_coverage:.2f}%")
        report.append(f"Statements: {self.coverage.statements}, Missing: {self.coverage.missing}")
        report.append("")
        
        # Performance summary
        report.append("## System Performance")
        report.append(f"CPU: {self.performance.cpu_percent:.1f}%")
        report.append(f"Memory: {self.performance.memory_usage:.1f}% used, {self.performance.memory_available:.2f} GB available")
        report.append(f"Disk: {self.performance.disk_usage:.1f}% used")
        report.append("")
        
        # Network summary
        report.append("## Network Connectivity")
        for target, status in self.network.connectivity_status.items():
            latency = self.network.ping_latency.get(target, -1)
            latency_str = f"{latency:.1f} ms" if latency >= 0 else "Failed"
            report.append(f"{target}: {'✅ Connected' if status else '❌ Disconnected'} - Latency: {latency_str}")
        report.append("")
        
        # Security summary
        report.append("## Security Status")
        report.append(f"Firewall: {'✅ Active' if self.security.firewall_active else '❌ Inactive'}")
        report.append(f"Credentials: {'✅ Secure' if self.security.discord_token_secure else '❌ Insecure'}")
        for domain, cert in self.security.ssl_certificates.items():
            report.append(f"SSL for {domain}: {'✅ Valid' if cert.get('verified', False) else '❌ Invalid'}")
        report.append("")
        
        # Test success summary
        report.append("## Test Results")
        report.append(f"Total Tests: {self.tests.total_tests}")
        report.append(f"Passed: {self.tests.passed}, Failed: {self.tests.failed}, Skipped: {self.tests.skipped}")
        if self.tests.test_failures:
            report.append("### Failures:")
            for failure in self.tests.test_failures:
                report.append(f"- {failure['test_name']}")
        report.append("")
        
        # API metrics summary
        report.append("## API Status")
        for name, data in self.api.endpoints.items():
            status = data.get('last_status', None)
            status_str = f"{status}" if status else "Failed"
            response_time = data.get('last_response_time', -1)
            time_str = f"{response_time:.1f} ms" if response_time >= 0 else "N/A"
            report.append(f"{name}: Status {status_str}, Response Time: {time_str}")
        report.append("")
        
        return "\n".join(report)


def collect_and_save_metrics(output_path: str = None) -> QAMetrics:
    """Collect all metrics and save to file."""
    metrics = QAMetrics()
    metrics.collect_all_metrics()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        metrics.save_to_file(output_path)
        logger.info(f"Metrics saved to {output_path}")
    
    return metrics

if __name__ == "__main__":
    # Example usage
    output_file = os.path.join(os.path.dirname(__file__), 
                             "../reports/qa_metrics_report.json")
    
    metrics = collect_and_save_metrics(output_file)
    report = metrics.generate_report()
    print(report) 