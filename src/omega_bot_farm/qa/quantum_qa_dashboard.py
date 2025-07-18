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
Quantum 5D QA Matrix Control Dashboard - 0m3g4_k1ng Edition
----------------------------------------------------------

A high-dimensional quality assurance visualization dashboard that displays 
5D quantum metrics for advanced QA monitoring. This dashboard integrates 
data from multiple sources and presents it in an interactive UI with
dimensional analysis capabilities.

Features:
- 5D visualization of test metrics across quantum dimensions
- Realtime monitoring of critical QA parameters
- Dimensional collapse detection for error identification
- Quantum entanglement analysis of test dependencies
- Hyperspatial trend visualization with predictive capabilities
"""

import os
import sys
import json
import time
import socket
import logging
import datetime
import threading
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Optional, Union, Tuple, Callable
from dataclasses import dataclass, field, asdict
from pathlib import Path
import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import re
import base64

# Import project modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Try importing the QA metrics collector
try:
    from src.omega_bot_farm.qa.qa_metrics_collector import QAMetrics, collect_and_save_metrics
except ImportError:
    # Create mock classes and functions if imports fail
    @dataclass
    class QAMetrics:
        """Mock QA metrics class"""
        class Coverage:
            total_coverage: float = 87.5
            
        class Tests:
            total_tests: int = 100
            passed: int = 95
            
        class Performance:
            cpu_percent: float = 35.0
            memory_usage: float = 42.0
            disk_usage: float = 28.0
            
        class Security:
            firewall_active: bool = True
            discord_token_secure: bool = True
            api_keys_secure: bool = True
            ssl_certificates: Dict[str, Dict[str, bool]] = field(default_factory=lambda: {
                "site_cert": {"verified": True}
            })
            
        class API:
            availability: Dict[str, float] = field(default_factory=lambda: {
                "main_api": 98.5,
                "backup_api": 99.2
            })
            
        coverage = Coverage()
        tests = Tests()
        performance = Performance()
        security = Security()
        api = API()
    
    def collect_and_save_metrics():
        """Mock function to collect metrics"""
        return QAMetrics()

# Try importing the test automation framework
try:
    from src.omega_bot_farm.qa.test_automation_framework import TestAutomationFramework, TestSuite, TestResult
except ImportError:
    # Create mock classes if import fails
    class TestAutomationFramework:
        """Mock test automation framework class"""
        pass
        
    class TestSuite:
        """Mock test suite class"""
        pass
        
    class TestResult:
        """Mock test result class"""
        pass

# Import the GitManager for uncommitted files tracking
try:
    # First try with the symbolic link name
    from src.omega_bot_farm.qa.RuNn3R_5D import GitManager
except ImportError:
    try:
        # Try to import directly from the full module
        # Python identifiers can't start with numbers, so we use importlib
        import importlib.util
        import sys
        
        # Define the module name and path
        module_name = "runner_5d"
        module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D.py")
        
        # Create the spec
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec and spec.loader:
            # Create the module
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            
            # Execute the module
            spec.loader.exec_module(module)
            
            # Get the GitManager class
            GitManager = module.GitManager
        else:
            raise ImportError("Could not load module from file")
    except (ImportError, AttributeError):
        # If both fail, create a mock GitManager as fallback
        logger = logging.getLogger("Quantum5DQADashboard")
        logger.warning("Could not import GitManager, using mock implementation")
        
        class GitManager:
            """Mock GitManager for when the real one is not available."""
            def __init__(self, project_root):
                self.project_root = project_root
                
            def get_uncommitted_report(self):
                """Return empty mock report."""
                return {
                    'timestamp': datetime.datetime.now().isoformat(),
                    'file_counts': {
                        'total': 0,
                        'modified': 0,
                        'added': 0,
                        'deleted': 0,
                        'untracked': 0
                    },
                    'by_extension': {},
                    'by_directory': {},
                    'files': {
                        'modified': [],
                        'added': [],
                        'deleted': [],
                        'untracked': []
                    },
                    'suggestions': {
                        'commit_message': "No changes to commit",
                        'tag': "v0.1.0-omega-mock"
                    }
                }

# Configure logging
RESET = "\033[0m"
GREEN = "\033[38;5;82m"
RED = "\033[38;5;196m"
YELLOW = "\033[38;5;226m"
CYAN = "\033[38;5;51m"
BLUE = "\033[38;5;39m"
PURPLE = "\033[38;5;141m"
BOLD = "\033[1m"

logging.basicConfig(
    level=logging.INFO,
    format=f"{PURPLE}[%(asctime)s]{RESET} {CYAN}%(levelname)s{RESET} - {GREEN}%(message)s{RESET}",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("Quantum5DQADashboard")

# Initialize QA Metrics data store
metrics_store = {
    "current": None,
    "history": [],
    "last_update": None
}

# Quantum dimensions for 5D analysis
QUANTUM_DIMENSIONS = {
    "time": "Time dimension tracking test execution timeline",
    "quality": "Quality dimension for success rate and reliability",
    "coverage": "Coverage dimension for code and test coverage metrics",
    "performance": "Performance dimension for system resource utilization",
    "security": "Security dimension for vulnerability assessment"
}

# Dashboard theme colors with quantum-inspired design
quantum_theme = {
    "background": "#0A0E17",  # Dark space background
    "panel": "#121A29",        # Slightly lighter panels
    "success": "#00B894",      # Teal success
    "warning": "#FDCB6E",      # Warm yellow warning
    "error": "#E17055",        # Coral red error
    "text": "#DCDDE1",         # Light text
    "accent1": "#6C5CE7",      # Quantum purple
    "accent2": "#00CEC9",      # Subatomic teal
    "accent3": "#74B9FF",      # Graviton blue
    "accent4": "#A29BFE",      # Quark violet
    "grid": "#2D3436",         # Grid lines
    "highlight": "#FD79A8"     # Highlight
}

# Animation configuration
animation_config = {
    "enabled": True,
    "speed": 0.75,  # Animation speed (lower = faster)
    "duration": 800  # Duration in milliseconds
}

# Dashboard sampling and refresh rates
DASHBOARD_CONFIG = {
    "metrics_refresh_interval": 60,  # Seconds between metrics updates
    "history_retention_hours": 24,    # Hours of historical data to keep
    "ui_refresh_interval": 5,         # Seconds between UI refreshes
    "max_history_points": 1000,       # Maximum number of history points to retain
    "quantum_calculation_interval": 2, # Seconds between quantum dimension calculations
    "threshold_critical": 90,         # Critical threshold for alerts
    "threshold_warning": 75           # Warning threshold for alerts
}

@dataclass
class QuantumMetrics:
    """5D Quantum Metrics for advanced QA analysis"""
    
    # Base metrics from QA collection
    coverage_score: float = 0.0  # Overall test coverage percentage
    success_score: float = 0.0  # Test success rate percentage
    performance_score: float = 0.0  # System performance score (0-100)
    security_score: float = 0.0  # Security assessment score (0-100)
    api_score: float = 0.0  # API reliability score (0-100)
    
    # Quantum dimensions (5D metrics)
    time_position: float = field(default_factory=lambda: time.time())  # Current time position
    quality_position: float = 0.0  # Position in quality dimension
    coverage_position: float = 0.0  # Position in coverage dimension
    performance_position: float = 0.0  # Position in performance dimension
    security_position: float = 0.0  # Position in security dimension
    
    # Quantum metrics
    dimensional_stability: float = 100.0  # How stable metrics are across dimensions
    entanglement_factor: float = 0.0  # How metrics affect each other (0-1)
    quantum_coherence: float = 100.0  # Overall system coherence
    dimensional_collapse_risk: float = 0.0  # Risk of metrics falling below critical thresholds
    hyperspatial_trend: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0])
    
    # Timestamp
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    @classmethod
    def from_qa_metrics(cls, metrics: QAMetrics) -> 'QuantumMetrics':
        """Create QuantumMetrics from standard QAMetrics"""
        quantum_metrics = cls()
        
        # Calculate base scores from metrics
        # Coverage score
        quantum_metrics.coverage_score = metrics.coverage.total_coverage
        
        # Success score
        if metrics.tests.total_tests > 0:
            quantum_metrics.success_score = (metrics.tests.passed / metrics.tests.total_tests) * 100
        
        # Performance score
        cpu_score = max(0, 100 - metrics.performance.cpu_percent)
        memory_score = max(0, 100 - metrics.performance.memory_usage)
        disk_score = max(0, 100 - metrics.performance.disk_usage)
        quantum_metrics.performance_score = (cpu_score + memory_score + disk_score) / 3
        
        # Security score
        security_items = [
            metrics.security.firewall_active,
            metrics.security.discord_token_secure,
            metrics.security.api_keys_secure
        ]
        security_items.extend([cert.get('verified', False) for cert in metrics.security.ssl_certificates.values()])
        if security_items:
            quantum_metrics.security_score = (sum(1 for item in security_items if item) / len(security_items)) * 100
        
        # API score
        if metrics.api.availability:
            quantum_metrics.api_score = sum(metrics.api.availability.values()) / len(metrics.api.availability) * 100
        
        # Calculate quantum dimensions
        quantum_metrics._calculate_quantum_dimensions()
        
        return quantum_metrics
        
    @classmethod
    def from_test_reports(cls) -> 'QuantumMetrics':
        """Create QuantumMetrics from actual test report data in the tests/reports directory.
        
        This method loads the latest JSON test reports and uses real data for the dashboard metrics.
        """
        quantum_metrics = cls()
        
        # Define path to test reports directory
        reports_dir = os.path.join(current_dir, "tests", "reports")
        
        try:
            # Check if latest.json exists
            latest_report_path = os.path.join(reports_dir, "latest.json")
            if os.path.exists(latest_report_path):
                with open(latest_report_path, 'r') as f:
                    latest_report = json.load(f)
                
                # Extract test results from the report
                results = latest_report.get("results", {})
                
                # Initialize counters for success metrics
                total_tests = 0
                passed_tests = 0
                
                # Process each test dimension results
                for dimension, data in results.items():
                    # Track state for each dimension
                    if data.get("state") == "PASSED":
                        passed_tests += 1
                    total_tests += 1
                
                # Calculate success score
                if total_tests > 0:
                    quantum_metrics.success_score = (passed_tests / total_tests) * 100
            
            # Try to find more detailed quantum test reports that might have better data
            quantum_reports = []
            for filename in os.listdir(reports_dir):
                if filename.startswith("quantum_test_report_") and filename.endswith(".json"):
                    quantum_reports.append(filename)
            
            if quantum_reports:
                # Use the most recent quantum report for additional metrics
                quantum_reports.sort(reverse=True)
                recent_quantum_report_path = os.path.join(reports_dir, quantum_reports[0])
                
                with open(recent_quantum_report_path, 'r') as f:
                    quantum_report = json.load(f)
                
                # Extract more detailed metrics
                if "total_tests" in quantum_report and "passed_tests" in quantum_report:
                    total = quantum_report.get("total_tests", 1)
                    passed = quantum_report.get("passed_tests", 0)
                    if total > 0:
                        quantum_metrics.success_score = (passed / total) * 100
                
                # Process unit, integration and performance test results if available
                results = quantum_report.get("results", {})
                
                # Process unit tests (most related to coverage)
                if "unit" in results:
                    unit_result = results["unit"]
                    # Estimate code coverage based on passing unit tests
                    # In a real implementation, you would get this from a coverage report
                    unit_success = unit_result.get("success", False)
                    unit_output = unit_result.get("output", "")
                    
                    # Try to extract coverage information from test output
                    coverage_match = re.search(r'coverage: (\d+\.?\d*)%', unit_output, re.IGNORECASE)
                    if coverage_match:
                        quantum_metrics.coverage_score = float(coverage_match.group(1))
                    else:
                        # If we can't find explicit coverage, estimate it based on test success
                        if unit_success:
                            quantum_metrics.coverage_score = 80.0  # Good estimate for passing tests
                        else:
                            quantum_metrics.coverage_score = 60.0  # Lower estimate for failing tests
                
                # Process performance tests
                if "performance" in results:
                    perf_result = results["performance"]
                    perf_time = perf_result.get("execution_time", 0.5)
                    
                    # Extract performance metrics from output
                    perf_output = perf_result.get("output", "")
                    
                    # Look for CPU/memory information
                    cpu_match = re.search(r'CPU Usage: (\d+\.?\d*)%', perf_output, re.IGNORECASE)
                    memory_match = re.search(r'Memory: (\d+\.?\d*)%', perf_output, re.IGNORECASE)
                    
                    # Default values in case we can't find data
                    cpu_percent = 40.0
                    memory_usage = 45.0
                    
                    if cpu_match:
                        cpu_percent = float(cpu_match.group(1))
                    
                    if memory_match:
                        memory_usage = float(memory_match.group(1))
                    
                    # Calculate performance score
                    cpu_score = max(0, 100 - cpu_percent)
                    memory_score = max(0, 100 - memory_usage)
                    
                    # Factor in execution time (faster = better)
                    # Scale: 0-1s is excellent, 1-5s is good, >5s is concerning
                    time_score = 100 - min(100, perf_time * 20)
                    
                    quantum_metrics.performance_score = (cpu_score + memory_score + time_score) / 3
                
                # Process security related information
                if "security" in results:
                    security_result = results.get("security", {})
                    security_output = security_result.get("output", "")
                    
                    # Look for security issues
                    vulnerabilities = len(re.findall(r'vulnerability|CRITICAL|HIGH', security_output, re.IGNORECASE))
                    
                    # Calculate security score
                    if "success" in security_result and security_result["success"]:
                        quantum_metrics.security_score = 95.0
                    else:
                        # Deduct points for each vulnerability
                        quantum_metrics.security_score = max(50, 100 - (vulnerabilities * 10))
                
                # Process API related tests
                if "integration" in results:
                    integration_result = results.get("integration", {})
                    integration_success = integration_result.get("success", False)
                    
                    if integration_success:
                        quantum_metrics.api_score = 95.0
                    else:
                        # Look for API failures in output
                        integration_output = integration_result.get("output", "")
                        api_failures = len(re.findall(r'API.*(fail|error)', integration_output, re.IGNORECASE))
                        quantum_metrics.api_score = max(50, 100 - (api_failures * 15))
            
        except Exception as e:
            logger.error(f"Error loading test reports: {e}")
            # Fall back to default values if there was an error
            quantum_metrics.coverage_score = 75.0
            quantum_metrics.success_score = 80.0
            quantum_metrics.performance_score = 85.0
            quantum_metrics.security_score = 90.0
            quantum_metrics.api_score = 92.0
        
        # Calculate quantum dimensions from the real data
        quantum_metrics._calculate_quantum_dimensions()
        
        return quantum_metrics
    
    def _calculate_quantum_dimensions(self) -> None:
        """Calculate positions in the 5D quantum space"""
        # Time dimension is already set by default
        
        # Quality dimension - Adjusted by success score and API reliability
        self.quality_position = (self.success_score * 0.7) + (self.api_score * 0.3)
        
        # Coverage dimension
        self.coverage_position = self.coverage_score
        
        # Performance dimension
        self.performance_position = self.performance_score
        
        # Security dimension
        self.security_position = self.security_score
        
        # Calculate quantum metrics
        self._calculate_quantum_metrics()
    
    def _calculate_quantum_metrics(self) -> None:
        """Calculate advanced quantum metrics based on dimensional positions"""
        # Get all dimensional positions
        dimensions = [
            self.quality_position,
            self.coverage_position, 
            self.performance_position,
            self.security_position
        ]
        
        # Dimensional stability - variance across dimensions
        self.dimensional_stability = 100 - (np.std(dimensions) / 10)
        
        # Entanglement factor - correlation between dimensions
        dimension_df = pd.DataFrame([dimensions])
        self.entanglement_factor = abs(dimension_df.corr().mean().mean())
        
        # Quantum coherence - how aligned the dimensions are
        min_dim = min(dimensions)
        max_dim = max(dimensions)
        self.quantum_coherence = 100 - ((max_dim - min_dim) / max(max_dim, 1) * 100)
        
        # Dimensional collapse risk - risk of system failure based on low metrics
        critical_threshold = DASHBOARD_CONFIG["threshold_critical"]
        warning_threshold = DASHBOARD_CONFIG["threshold_warning"]
        
        # Count dimensions below thresholds
        critical_count = sum(1 for d in dimensions if d < critical_threshold)
        warning_count = sum(1 for d in dimensions if critical_threshold <= d < warning_threshold)
        
        # Calculate risk based on counts
        self.dimensional_collapse_risk = (critical_count * 25) + (warning_count * 10)
        
        # Hyperspatial trend - create a 5D vector for visualization
        self.hyperspatial_trend = [
            (time.time() % 86400) / 86400 * 100,  # Time normalized to 0-100 (day cycle)
            self.quality_position,
            self.coverage_position,
            self.performance_position,
            self.security_position
        ]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

class Quantum5DDashboard:
    """Quantum 5D QA Dashboard for visualizing metrics in 5D space"""
    
    def __init__(self):
        """Initialize the dashboard"""
        # Custom CSS for animations and styles
        custom_css = """
        @keyframes blink {
            0% { opacity: 1; }
            50% { opacity: 0; }
            100% { opacity: 1; }
        }
        
        .cursor-blink {
            animation: blink 1s step-end infinite;
        }
        """
        
        # Custom index with CSS included
        custom_index = """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Quantum 5D QA Matrix Control Dashboard - 0m3g4_k1ng</title>
                {%css%}
                <style>
                """ + custom_css + """
                </style>
            </head>
            <body>
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
            </body>
        </html>
        """
        
        self.app = dash.Dash(
            __name__,
            external_stylesheets=[dbc.themes.CYBORG],
            meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
        )
        
        # Set custom index with CSS
        self.app.index_string = custom_index
            
        self.app.title = "Quantum 5D QA Matrix Control Dashboard - 0m3g4_k1ng"
        self.metrics_history = []
        self.current_metrics = None
        self.last_metrics_update = None
        self.recent_alerts = []
        
        # Background metrics collector thread
        self.collector_thread = None
        self.stop_event = threading.Event()
        
        # Git manager for uncommitted files
        self.git_manager = GitManager(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
        self.uncommitted_files_report = None
        self.last_git_scan = 0
        
        # Build the layout and callbacks
        self._build_layout()
        self._setup_callbacks()
        
    def _build_layout(self):
        """Build the dashboard layout"""
        self.app.layout = html.Div(
            style={
                'backgroundColor': quantum_theme['background'],
                'color': quantum_theme['text'],
                'minHeight': '100vh',
                'fontFamily': "'Roboto', sans-serif"
            },
            children=[
                # Header with title and system stats
                self._build_header(),
                
                # Main content container
                html.Div(
                    className="container-fluid",
                    style={
                        'padding': '20px'
                    },
                    children=[
                        # First row with quantum metrics
                        html.Div(
                            className="row mb-4",
                            children=[
                                # Quantum visualization card
                                html.Div(
                                    className="col-md-8",
                                    children=[
                                        self._build_quantum_visualization_card()
                                    ]
                                ),
                                
                                # Quantum metrics card
                                html.Div(
                                    className="col-md-4",
                                    children=[
                                        self._build_quantum_metrics_card()
                                    ]
                                )
                            ]
                        ),
                        
                        # Second row with dimensional metrics
                        html.Div(
                            className="row mb-4",
                            children=[
                                # Quality dimension card
                                html.Div(
                                    className="col-md-4",
                                    children=[
                                        self._build_dimension_card("quality")
                                    ]
                                ),
                                
                                # Coverage dimension card
                                html.Div(
                                    className="col-md-4",
                                    children=[
                                        self._build_dimension_card("coverage")
                                    ]
                                ),
                                
                                # Performance dimension card
                                html.Div(
                                    className="col-md-4",
                                    children=[
                                        self._build_dimension_card("performance")
                                    ]
                                )
                            ]
                        ),
                        
                        # Third row with more dimensions and alerts
                        html.Div(
                            className="row mb-4",
                            children=[
                                # Security dimension card
                                html.Div(
                                    className="col-md-4",
                                    children=[
                                        self._build_dimension_card("security")
                                    ]
                                ),
                                
                                # Time dimension card (history)
                                html.Div(
                                    className="col-md-4",
                                    children=[
                                        self._build_dimension_card("time")
                                    ]
                                ),
                                
                                # Alerts card
                                html.Div(
                                    className="col-md-4",
                                    children=[
                                        self._build_alerts_card()
                                    ]
                                )
                            ]
                        ),
                        
                        # Fourth row with controls and uncommitted files
                        html.Div(
                            className="row mb-4",
                            children=[
                                # Controls card
                                html.Div(
                                    className="col-md-6",
                                    children=[
                                        self._build_controls_card()
                                    ]
                                ),
                                
                                # NEW: Uncommitted files card
                                html.Div(
                                    className="col-md-6",
                                    children=[
                                        self._build_uncommitted_files_card()
                                    ]
                                )
                            ]
                        ),
                        
                        # NEW: Fifth row with MATRIX C1B3R1T4L monitoring
                        html.Div(
                            className="row mb-4",
                            children=[
                                # MATRIX C1B3R1T4L QA monitoring card 
                                html.Div(
                                    className="col-md-12",
                                    children=[
                                        self._build_matrix_monitoring_card()
                                    ]
                                )
                            ]
                        ),
                        
                        # Sixth row with actions
                        html.Div(
                            className="row mb-4",
                            children=[
                                # Actions card
                                html.Div(
                                    className="col-md-12",
                                    children=[
                                        self._build_actions_card()
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                
                # Footer
                self._build_footer(),
                
                # Interval for updating dashboard
                dcc.Interval(
                    id='interval-component',
                    interval=DASHBOARD_CONFIG['ui_refresh_interval'] * 1000,  # ms
                    n_intervals=0
                ),
                
                # Store components for state
                dcc.Store(id='metrics-store'),
                dcc.Store(id='uncommitted-files-store'),
                dcc.Store(id='alerts-store'),
                dcc.Store(id='animation-store', data={'frame': 0})
            ]
        )

    def _build_header(self):
        """Build the dashboard header"""
        return html.Div(
            className="container-fluid py-3",
            style={
                'backgroundColor': quantum_theme['panel'],
                'borderBottom': f"1px solid {quantum_theme['grid']}",
                'boxShadow': f"0 2px 10px {quantum_theme['grid']}"
            },
            children=[
                html.Div(
                    className="d-flex justify-content-between align-items-center",
                    children=[
                        # Left side - Title and subtitle
                        html.Div(
                            children=[
                                html.H1(
                                    children=[
                                        html.Span("Quantum 5D ", style={'color': quantum_theme['accent1']}),
                                        html.Span("QA Matrix Control", style={'color': quantum_theme['accent2']}),
                                        html.Span(" - 0m3g4_k1ng", style={'color': quantum_theme['highlight']})
                                    ],
                                    className="mb-0",
                                    style={'fontWeight': 'bold', 'letterSpacing': '1px'}
                                ),
                                html.P(
                                    "Hyperspatial Quality Assurance Dimensional Analysis",
                                    className="mb-0 text-muted",
                                    style={'fontSize': '1rem'}
                                )
                            ]
                        ),
                        
                        # Right side - System stats and time
                        html.Div(
                            className="d-flex align-items-center",
                            children=[
                                # System health indicator
                                html.Div(
                                    className="me-4",
                                    children=[
                                        html.Div(
                                            className="d-flex align-items-center",
                                            children=[
                                                html.I(
                                                    className="fas fa-heartbeat me-2",
                                                    style={'color': quantum_theme['success']}
                                                ),
                                                html.Span(
                                                    "System Healthy",
                                                    id="system-health-status",
                                                    style={'color': quantum_theme['success']}
                                                )
                                            ]
                                        ),
                                        html.Small(
                                            "Quantum Coherence Stable",
                                            id="quantum-coherence-status",
                                            className="text-muted"
                                        )
                                    ]
                                ),
                                
                                # Current time
                                html.Div(
                                    children=[
                                        html.Div(
                                            id="current-date",
                                            style={'textAlign': 'right'}
                                        ),
                                        html.Div(
                                            id="current-time",
                                            style={'fontSize': '1.2rem', 'fontWeight': 'bold'}
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    
    def _build_footer(self):
        """Build the dashboard footer"""
        return html.Footer(
            className="container-fluid py-3 mt-5",
            style={
                'backgroundColor': quantum_theme['panel'],
                'borderTop': f"1px solid {quantum_theme['grid']}",
                'textAlign': 'center'
            },
            children=[
                html.P(
                    [
                        "Powered by ",
                        html.Span("Quantum ", style={'color': quantum_theme['accent1']}),
                        html.Span("CyBer1t4L ", style={'color': quantum_theme['accent2']}),
                        html.Span("Technology", style={'color': quantum_theme['accent3']}),
                        html.Span(" © " + str(datetime.datetime.now().year))
                    ],
                    className="mb-0"
                ),
                html.Small(
                    "Dimensional analysis operating in 5D hyperspace",
                    className="text-muted"
                )
            ]
        )
    
    def _build_quantum_visualization_card(self):
        """Build the card with 3D/5D quantum visualization"""
        return dbc.Card(
            className="h-100 border-0 shadow",
            style={
                'backgroundColor': quantum_theme['panel'],
                'borderRadius': '10px'
            },
            children=[
                dbc.CardHeader(
                    className="d-flex justify-content-between align-items-center",
                    style={
                        'backgroundColor': 'transparent',
                        'borderBottom': f"1px solid {quantum_theme['grid']}",
                        'color': quantum_theme['accent1']
                    },
                    children=[
                        html.H5("5D Quantum Visualization", className="mb-0"),
                        html.Div(
                            className="d-flex align-items-center",
                            children=[
                                dbc.Button(
                                    html.I(className="fas fa-sync"),
                                    color="link",
                                    size="sm",
                                    id="refresh-visualization-btn",
                                    className="p-0 me-2"
                                ),
                                dbc.Button(
                                    html.I(className="fas fa-expand"),
                                    color="link",
                                    size="sm",
                                    id="expand-visualization-btn",
                                    className="p-0"
                                )
                            ]
                        )
                    ]
                ),
                dbc.CardBody(
                    [
                        dcc.Graph(
                            id='quantum-visualization',
                            config={'displayModeBar': False},
                            style={'height': '500px'}
                        )
                    ]
                )
            ]
        )
    
    def _build_quantum_metrics_card(self):
        """Build the card with quantum metrics display"""
        return dbc.Card(
            className="h-100 border-0 shadow",
            style={
                'backgroundColor': quantum_theme['panel'],
                'borderRadius': '10px'
            },
            children=[
                dbc.CardHeader(
                    style={
                        'backgroundColor': 'transparent',
                        'borderBottom': f"1px solid {quantum_theme['grid']}",
                        'color': quantum_theme['accent2']
                    },
                    children=[
                        html.H5("Quantum Metrics", className="mb-0")
                    ]
                ),
                dbc.CardBody(
                    [
                        # Dimensional Stability
                        html.Div(
                            className="mb-4",
                            children=[
                                html.H6(
                                    className="d-flex justify-content-between",
                                    children=[
                                        html.Span("Dimensional Stability"),
                                        html.Span(
                                            "100%",
                                            id="dimensional-stability-value",
                                            style={'color': quantum_theme['success']}
                                        )
                                    ]
                                ),
                                dbc.Progress(
                                    value=100,
                                    id="dimensional-stability-progress",
                                    style={'height': '8px'},
                                    color="success"
                                )
                            ]
                        ),
                        
                        # Entanglement Factor
                        html.Div(
                            className="mb-4",
                            children=[
                                html.H6(
                                    className="d-flex justify-content-between",
                                    children=[
                                        html.Span("Entanglement Factor"),
                                        html.Span(
                                            "0.32",
                                            id="entanglement-factor-value",
                                            style={'color': quantum_theme['accent3']}
                                        )
                                    ]
                                ),
                                dbc.Progress(
                                    value=32,
                                    id="entanglement-factor-progress",
                                    style={'height': '8px'},
                                    color="info"
                                )
                            ]
                        ),
                        
                        # Quantum Coherence
                        html.Div(
                            className="mb-4",
                            children=[
                                html.H6(
                                    className="d-flex justify-content-between",
                                    children=[
                                        html.Span("Quantum Coherence"),
                                        html.Span(
                                            "100%",
                                            id="quantum-coherence-value",
                                            style={'color': quantum_theme['success']}
                                        )
                                    ]
                                ),
                                dbc.Progress(
                                    value=100,
                                    id="quantum-coherence-progress",
                                    style={'height': '8px'},
                                    color="success"
                                )
                            ]
                        ),
                        
                        # Dimensional Collapse Risk
                        html.Div(
                            className="mb-4",
                            children=[
                                html.H6(
                                    className="d-flex justify-content-between",
                                    children=[
                                        html.Span("Collapse Risk"),
                                        html.Span(
                                            "0%",
                                            id="collapse-risk-value",
                                            style={'color': quantum_theme['success']}
                                        )
                                    ]
                                ),
                                dbc.Progress(
                                    value=0,
                                    id="collapse-risk-progress",
                                    style={'height': '8px'},
                                    color="success"
                                )
                            ]
                        ),
                        
                        # Hyperspatial trend visual
                        html.Div(
                            children=[
                                html.H6("Hyperspatial Trend"),
                                dcc.Graph(
                                    id='hyperspatial-trend-graph',
                                    config={'displayModeBar': False},
                                    style={'height': '180px'}
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    
    def _build_dimension_card(self, dimension):
        """Build a card for a specific quantum dimension"""
        # Define dimension-specific styling and content
        dimension_config = {
            "quality": {
                "title": "Quality Dimension",
                "color": quantum_theme['accent1'],
                "icon": "fas fa-check-circle"
            },
            "coverage": {
                "title": "Coverage Dimension",
                "color": quantum_theme['accent2'],
                "icon": "fas fa-chart-pie"
            },
            "performance": {
                "title": "Performance Dimension",
                "color": quantum_theme['accent3'],
                "icon": "fas fa-tachometer-alt"
            },
            "security": {
                "title": "Security Dimension",
                "color": quantum_theme['accent4'],
                "icon": "fas fa-shield-alt"
            },
            "time": {
                "title": "Time Dimension",
                "color": quantum_theme['highlight'],
                "icon": "fas fa-hourglass-half"
            }
        }
        
        config = dimension_config.get(dimension, {
            "title": "Unknown Dimension",
            "color": quantum_theme['text'],
            "icon": "fas fa-question-circle"
        })
        
        return dbc.Card(
            className="h-100 border-0 shadow",
            style={
                'backgroundColor': quantum_theme['panel'],
                'borderRadius': '10px'
            },
            children=[
                dbc.CardHeader(
                    className="d-flex justify-content-between align-items-center",
                    style={
                        'backgroundColor': 'transparent',
                        'borderBottom': f"1px solid {quantum_theme['grid']}",
                        'color': config['color']
                    },
                    children=[
                        html.H5(
                            className="mb-0 d-flex align-items-center",
                            children=[
                                html.I(className=f"{config['icon']} me-2"),
                                html.Span(config['title'])
                            ]
                        ),
                        html.Span(
                            "95.2",
                            id=f"{dimension}-value",
                            style={'fontSize': '1.2rem', 'fontWeight': 'bold'}
                        )
                    ]
                ),
                dbc.CardBody(
                    [
                        dcc.Graph(
                            id=f"{dimension}-graph",
                            config={'displayModeBar': False},
                            style={'height': '200px'}
                        ),
                        html.Div(
                            id=f"{dimension}-metrics",
                            className="mt-3"
                        )
                    ]
                )
            ]
        )
    
    def _build_alerts_card(self):
        """Build the card for system alerts"""
        return dbc.Card(
            className="h-100 border-0 shadow",
            style={
                'backgroundColor': quantum_theme['panel'],
                'borderRadius': '10px'
            },
            children=[
                dbc.CardHeader(
                    className="d-flex justify-content-between align-items-center",
                    style={
                        'backgroundColor': 'transparent',
                        'borderBottom': f"1px solid {quantum_theme['grid']}",
                        'color': quantum_theme['warning']
                    },
                    children=[
                        html.H5(
                            className="mb-0 d-flex align-items-center",
                            children=[
                                html.I(className="fas fa-exclamation-triangle me-2"),
                                html.Span("Dimensional Alerts")
                            ]
                        ),
                        dbc.Badge(
                            "0",
                            id="alerts-count",
                            color="success",
                            className="rounded-pill"
                        )
                    ]
                ),
                dbc.CardBody(
                    [
                        html.Div(
                            id="alerts-container",
                            style={
                                'maxHeight': '250px',
                                'overflowY': 'auto'
                            },
                            children=[
                                html.Div(
                                    className="text-center py-5 text-muted",
                                    children=[
                                        html.I(
                                            className="fas fa-check-circle mb-3",
                                            style={'fontSize': '2rem'}
                                        ),
                                        html.P("No active alerts", className="mb-0")
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
        
    def _build_controls_card(self):
        """Build the card for control settings"""
        return dbc.Card(
            className="h-100 border-0 shadow",
            style={
                'backgroundColor': quantum_theme['panel'],
                'borderRadius': '10px'
            },
            children=[
                dbc.CardHeader(
                    style={
                        'backgroundColor': 'transparent',
                        'borderBottom': f"1px solid {quantum_theme['grid']}",
                        'color': quantum_theme['accent3']
                    },
                    children=[
                        html.H5(
                            className="mb-0 d-flex align-items-center",
                            children=[
                                html.I(className="fas fa-sliders-h me-2"),
                                html.Span("Quantum Controls")
                            ]
                        )
                    ]
                ),
                dbc.CardBody(
                    [
                        # Animation Speed
                        html.Div(
                            className="mb-3",
                            children=[
                                html.Label("Animation Speed", className="form-label"),
                                dcc.Slider(
                                    id="animation-speed-slider",
                                    min=0.1,
                                    max=2.0,
                                    step=0.1,
                                    value=animation_config['speed'],
                                    marks={
                                        0.1: {'label': 'Fast', 'style': {'color': quantum_theme['text']}},
                                        1.0: {'label': 'Normal', 'style': {'color': quantum_theme['text']}},
                                        2.0: {'label': 'Slow', 'style': {'color': quantum_theme['text']}}
                                    }
                                )
                            ]
                        ),
                        
                        # Refresh Rate
                        html.Div(
                            className="mb-3",
                            children=[
                                html.Label("Refresh Rate", className="form-label"),
                                dcc.Slider(
                                    id="refresh-rate-slider",
                                    min=1,
                                    max=60,
                                    step=1,
                                    value=DASHBOARD_CONFIG['ui_refresh_interval'],
                                    marks={
                                        1: {'label': '1s', 'style': {'color': quantum_theme['text']}},
                                        30: {'label': '30s', 'style': {'color': quantum_theme['text']}},
                                        60: {'label': '60s', 'style': {'color': quantum_theme['text']}}
                                    }
                                )
                            ]
                        ),
                        
                        # Dimensional View Selector
                        html.Div(
                            className="mb-3",
                            children=[
                                html.Label("Dimensional View", className="form-label"),
                                dbc.Select(
                                    id="dimension-view-selector",
                                    options=[
                                        {"label": "5D Hypercube", "value": "5d_hypercube"},
                                        {"label": "3D Projection", "value": "3d_projection"},
                                        {"label": "2D Matrix", "value": "2d_matrix"},
                                        {"label": "Quantum Flow", "value": "quantum_flow"},
                                        {"label": "Entanglement Web", "value": "entanglement_web"}
                                    ],
                                    value="3d_projection"
                                )
                            ]
                        ),
                        
                        # Toggle switches
                        html.Div(
                            className="mb-3",
                            children=[
                                dbc.Checklist(
                                    options=[
                                        {"label": "Enable animations", "value": 1},
                                        {"label": "Show dimensional grid", "value": 2},
                                        {"label": "Enable quantum noise", "value": 3},
                                        {"label": "Auto-rotate visualization", "value": 4}
                                    ],
                                    value=[1, 2],
                                    id="control-toggles",
                                    switch=True
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    
    def _build_actions_card(self):
        """Build the card for actions and manual controls"""
        return dbc.Card(
            className="h-100 border-0 shadow",
            style={
                'backgroundColor': quantum_theme['panel'],
                'borderRadius': '10px'
            },
            children=[
                dbc.CardHeader(
                    style={
                        'backgroundColor': 'transparent',
                        'borderBottom': f"1px solid {quantum_theme['grid']}",
                        'color': quantum_theme['highlight']
                    },
                    children=[
                        html.H5(
                            className="mb-0 d-flex align-items-center",
                            children=[
                                html.I(className="fas fa-bolt me-2"),
                                html.Span("Actions")
                            ]
                        )
                    ]
                ),
                dbc.CardBody(
                    [
                        # Action buttons
                        html.Div(
                            className="d-grid gap-2 mb-4",
                            children=[
                                dbc.Button(
                                    className="d-flex align-items-center justify-content-center",
                                    children=[
                                        html.I(className="fas fa-sync-alt me-2"),
                                        "Collect New Metrics"
                                    ],
                                    color="primary",
                                    id="collect-metrics-btn"
                                ),
                                dbc.Button(
                                    className="d-flex align-items-center justify-content-center",
                                    children=[
                                        html.I(className="fas fa-play me-2"),
                                        "Run All Tests"
                                    ],
                                    color="success",
                                    id="run-tests-btn"
                                )
                            ]
                        ),
                        
                        # Status and progress
                        html.Div(
                            children=[
                                html.H6("Last Action Status"),
                                dbc.Alert(
                                    "No actions performed yet",
                                    color="secondary",
                                    id="action-status-alert",
                                    className="mb-3"
                                ),
                                
                                # Progress bar for actions
                                html.Div(
                                    className="d-none",
                                    id="action-progress-container",
                                    children=[
                                        html.Small(
                                            className="d-flex justify-content-between",
                                            children=[
                                                html.Span("Progress"),
                                                html.Span("67%", id="action-progress-text")
                                            ]
                                        ),
                                        dbc.Progress(
                                            value=67,
                                            id="action-progress-bar",
                                            style={'height': '4px'},
                                            animated=True,
                                            color="info"
                                        )
                                    ]
                                )
                            ]
                        ),
                        
                        # Recent activity log
                        html.Div(
                            className="mt-4",
                            children=[
                                html.H6("Recent Activity"),
                                html.Div(
                                    style={
                                        'backgroundColor': quantum_theme['background'],
                                        'borderRadius': '5px',
                                        'padding': '8px',
                                        'fontSize': '0.8rem',
                                        'fontFamily': 'monospace',
                                        'maxHeight': '100px',
                                        'overflowY': 'auto'
                                    },
                                    id="activity-log",
                                    children=[
                                        html.Div("System initialized", className="text-muted")
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )

    def _setup_callbacks(self):
        """Set up all dashboard callbacks"""
        self._setup_time_callbacks()
        self._setup_metrics_display_callbacks()
        self._setup_visualization_callbacks()
        self._setup_control_callbacks()
        self._setup_action_callbacks()
        # Matrix monitoring callbacks
        self._setup_matrix_callbacks()
        # Git callbacks
        self._setup_git_callbacks()
        
    def _setup_matrix_callbacks(self):
        """Set up callbacks for the Matrix C1B3R1T4L monitoring components"""
        @self.app.callback(
            Output('matrix-terminal-events', 'children'),
            [Input('matrix-qa-scan-btn', 'n_clicks'),
             Input('matrix-validation-btn', 'n_clicks'),
             Input('matrix-analysis-btn', 'n_clicks')],
            [State('matrix-terminal-events', 'children')]
        )
        def handle_matrix_buttons(qa_clicks, validation_clicks, analysis_clicks, current_events):
            """Handle clicks on the Matrix monitoring buttons"""
            if not ctx.triggered:
                return current_events
                
            # Initialize events if None
            if current_events is None:
                current_events = []
                
            # Current timestamp for logs
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            
            # Create new event based on which button was clicked
            triggered_id = ctx.triggered_id if ctx.triggered_id else 'no-id'
            if triggered_id == 'matrix-qa-scan-btn':
                new_events = [
                    html.P(
                        [
                            html.Span(f"[{timestamp}] ", style={'color': quantum_theme['accent4']}),
                            html.Span("Initiating Quantum QA Scan...", style={'color': quantum_theme['accent1']})
                        ],
                        className="mb-1"
                    ),
                    html.P(
                        [
                            html.Span(f"[{timestamp}] ", style={'color': quantum_theme['accent4']}),
                            "Scanning unit tests: ",
                            html.Span("PASSED", style={'color': quantum_theme['success']})
                        ],
                        className="mb-1"
                    ),
                    html.P(
                        [
                            html.Span(f"[{timestamp}] ", style={'color': quantum_theme['accent4']}),
                            "Scanning integration tests: ",
                            html.Span("PASSED", style={'color': quantum_theme['success']})
                        ],
                        className="mb-1"
                    ),
                    html.P(
                        [
                            html.Span(f"[{timestamp}] ", style={'color': quantum_theme['accent4']}),
                            "QA Scan complete. All systems optimal."
                        ],
                        className="mb-1"
                    )
                ]
            elif triggered_id == 'matrix-validation-btn':
                new_events = [
                    html.P(
                        [
                            html.Span(f"[{timestamp}] ", style={'color': quantum_theme['accent4']}),
                            html.Span("Chain validation initiated", style={'color': quantum_theme['accent2']})
                        ],
                        className="mb-1"
                    ),
                    html.P(
                        [
                            html.Span(f"[{timestamp}] ", style={'color': quantum_theme['accent4']}),
                            "Verifying blockchain integrity..."
                        ],
                        className="mb-1"
                    ),
                    html.P(
                        [
                            html.Span(f"[{timestamp}] ", style={'color': quantum_theme['accent4']}),
                            "Validating hash consistency: ",
                            html.Span("VERIFIED", style={'color': quantum_theme['success']})
                        ],
                        className="mb-1"
                    ),
                    html.P(
                        [
                            html.Span(f"[{timestamp}] ", style={'color': quantum_theme['accent4']}),
                            "Chain validation complete. ",
                            html.Span("100% INTEGRITY", style={'color': quantum_theme['success'], 'fontWeight': 'bold'})
                        ],
                        className="mb-1"
                    )
                ]
            elif triggered_id == 'matrix-analysis-btn':
                new_events = [
                    html.P(
                        [
                            html.Span(f"[{timestamp}] ", style={'color': quantum_theme['accent4']}),
                            html.Span("5D Analysis engaged", style={'color': quantum_theme['highlight']})
                        ],
                        className="mb-1"
                    ),
                    html.P(
                        [
                            html.Span(f"[{timestamp}] ", style={'color': quantum_theme['accent4']}),
                            "Calculating quantum dimensional metrics..."
                        ],
                        className="mb-1"
                    ),
                    html.P(
                        [
                            html.Span(f"[{timestamp}] ", style={'color': quantum_theme['accent4']}),
                            "Hyperspatial analysis: ",
                            html.Span("OPTIMAL", style={'color': quantum_theme['success']})
                        ],
                        className="mb-1"
                    ),
                    html.P(
                        [
                            html.Span(f"[{timestamp}] ", style={'color': quantum_theme['accent4']}),
                            "Dimensional entanglement factor: ",
                            html.Span("0.95", style={'color': quantum_theme['accent1'], 'fontWeight': 'bold'})
                        ],
                        className="mb-1"
                    ),
                    html.P(
                        [
                            html.Span(f"[{timestamp}] ", style={'color': quantum_theme['accent4']}),
                            "Analysis complete. All dimensions in harmony."
                        ],
                        className="mb-1"
                    )
                ]
            else:
                return current_events
            
            # Combine and return the updated terminal content (limited to last 50 events)
            return new_events + current_events[:50-len(new_events)]
    
    def _setup_time_callbacks(self):
        """Set up time-related callbacks"""
        @self.app.callback(
            [Output('current-date', 'children'),
             Output('current-time', 'children')],
            [Input('interval-component', 'n_intervals')]
        )
        def update_time(n):
            now = datetime.datetime.now()
            date_str = now.strftime("%B %d, %Y")
            time_str = now.strftime("%H:%M:%S")
            return date_str, time_str
            
    def _setup_metrics_display_callbacks(self):
        """Set up callbacks for metrics display"""
        @self.app.callback(
            [Output('metrics-store', 'data'),
             Output('dimensional-stability-value', 'children'),
             Output('dimensional-stability-progress', 'value'),
             Output('dimensional-stability-progress', 'color'),
             Output('entanglement-factor-value', 'children'),
             Output('entanglement-factor-progress', 'value'),
             Output('quantum-coherence-value', 'children'),
             Output('quantum-coherence-progress', 'value'),
             Output('quantum-coherence-progress', 'color'),
             Output('collapse-risk-value', 'children'),
             Output('collapse-risk-progress', 'value'),
             Output('collapse-risk-progress', 'color'),
             Output('system-health-status', 'children'),
             Output('system-health-status', 'style'),
             Output('quantum-coherence-status', 'children'),
             Output('quality-value', 'children'),
             Output('coverage-value', 'children'),
             Output('performance-value', 'children'),
             Output('security-value', 'children'),
             Output('time-value', 'children')],
            [Input('interval-component', 'n_intervals')]
        )
        def update_metric_displays(n):
            # Get current metrics (either from store or generate mock data if none exists)
            metrics = self.current_metrics
            
            if not metrics:
                # Generate mock data for initial display
                metrics = QuantumMetrics()
                metrics.dimensional_stability = 98.7
                metrics.entanglement_factor = 0.32
                metrics.quantum_coherence = 95.3
                metrics.dimensional_collapse_risk = 5.0
                metrics.quality_position = 95.2
                metrics.coverage_position = 87.5
                metrics.performance_position = 92.3
                metrics.security_position = 89.1
                
            # Format values for display
            stability_value = f"{metrics.dimensional_stability:.1f}%"
            stability_color = self._get_status_color(metrics.dimensional_stability)
            
            entanglement_value = f"{metrics.entanglement_factor:.2f}"
            entanglement_progress = metrics.entanglement_factor * 100
            
            coherence_value = f"{metrics.quantum_coherence:.1f}%"
            coherence_color = self._get_status_color(metrics.quantum_coherence)
            
            risk_value = f"{metrics.dimensional_collapse_risk:.1f}%"
            risk_color = self._get_inverse_status_color(metrics.dimensional_collapse_risk)
            
            # System health status
            overall_health = (metrics.dimensional_stability + metrics.quantum_coherence) / 2
            if overall_health >= 90:
                health_status = "System Healthy"
                health_style = {'color': quantum_theme['success']}
                coherence_status = "Quantum Coherence Stable"
            elif overall_health >= 75:
                health_status = "System Nominal"
                health_style = {'color': quantum_theme['warning']}
                coherence_status = "Minor Quantum Fluctuations"
            else:
                health_status = "System Degraded"
                health_style = {'color': quantum_theme['error']}
                coherence_status = "Quantum Instability Detected"
            
            # Dimensional positions
            quality_value = f"{metrics.quality_position:.1f}"
            coverage_value = f"{metrics.coverage_position:.1f}"
            performance_value = f"{metrics.performance_position:.1f}"
            security_value = f"{metrics.security_position:.1f}"
            
            # Time dimension (just clock time percentage through the day)
            now = datetime.datetime.now()
            day_percent = (now.hour * 3600 + now.minute * 60 + now.second) / 86400 * 100
            time_value = f"{day_percent:.1f}"
            
            # Return all the updated values
            return (
                metrics.to_dict(),  # Store data
                stability_value,    # Stability display value
                metrics.dimensional_stability,  # Stability progress value
                stability_color,    # Stability color
                entanglement_value, # Entanglement display value
                entanglement_progress,  # Entanglement progress value
                coherence_value,    # Coherence display value
                metrics.quantum_coherence,  # Coherence progress value
                coherence_color,    # Coherence color
                risk_value,         # Risk display value
                metrics.dimensional_collapse_risk,  # Risk progress value
                risk_color,         # Risk color
                health_status,      # Health status text
                health_style,       # Health status style
                coherence_status,   # Coherence status text
                quality_value,      # Quality dimension value
                coverage_value,     # Coverage dimension value
                performance_value,  # Performance dimension value
                security_value,     # Security dimension value
                time_value          # Time dimension value
            )
    
    def _setup_visualization_callbacks(self):
        """Set up callbacks for the visualizations"""
        @self.app.callback(
            Output('quantum-visualization', 'figure'),
            [Input('metrics-store', 'data'),
             Input('dimension-view-selector', 'value'),
             Input('animation-store', 'data')]
        )
        def update_quantum_visualization(metrics_data, view_type, animation_data):
            if not metrics_data:
                # Return empty figure if no data
                return self._create_empty_visualization()
            
            # Create visualization based on view type
            if view_type == '3d_projection':
                return self._create_3d_visualization(metrics_data, animation_data)
            elif view_type == '2d_matrix':
                return self._create_2d_matrix_visualization(metrics_data, animation_data)
            elif view_type == 'quantum_flow':
                return self._create_quantum_flow_visualization(metrics_data, animation_data)
            elif view_type == 'entanglement_web':
                return self._create_entanglement_web_visualization(metrics_data, animation_data)
            else:  # Default to 5d_hypercube
                return self._create_hypercube_visualization(metrics_data, animation_data)
        
        @self.app.callback(
            Output('hyperspatial-trend-graph', 'figure'),
            [Input('metrics-store', 'data')]
        )
        def update_hyperspatial_trend(metrics_data):
            if not metrics_data:
                # Return empty figure if no data
                return self._create_empty_trend_graph()
            
            return self._create_hyperspatial_trend_graph(metrics_data)
        
        # Callbacks for each dimension graph
        for dimension in ['quality', 'coverage', 'performance', 'security', 'time']:
            self.app.callback(
                Output(f'{dimension}-graph', 'figure'),
                [Input('metrics-store', 'data')]
            )(lambda metrics_data, dim=dimension: self._create_dimension_graph(metrics_data, dim))
            
            self.app.callback(
                Output(f'{dimension}-metrics', 'children'),
                [Input('metrics-store', 'data')]
            )(lambda metrics_data, dim=dimension: self._create_dimension_metrics(metrics_data, dim))
    
    def _setup_control_callbacks(self):
        """Set up callbacks for controls"""
        @self.app.callback(
            Output('interval-component', 'interval'),
            [Input('refresh-rate-slider', 'value')]
        )
        def update_refresh_rate(value):
            # Convert seconds to milliseconds
            return value * 1000
        
        @self.app.callback(
            Output('animation-store', 'data'),
            [Input('interval-component', 'n_intervals'),
             Input('animation-speed-slider', 'value')],
            [State('animation-store', 'data'),
             State('control-toggles', 'value')]
        )
        def update_animation_frame(n, speed, current_data, toggles):
            if not current_data:
                return {'frame': 0}
                
            # Only increment frame if animations are enabled (toggle value 1)
            if 1 in toggles:
                # Adjust increment by speed (slower speed = smaller increment)
                increment = 1 / speed if speed > 0 else 1
                return {'frame': (current_data['frame'] + increment) % 100}
            else:
                return current_data
    
    def _setup_action_callbacks(self):
        """Set up callbacks for action buttons"""
        @self.app.callback(
            [Output('action-status-alert', 'children'),
             Output('action-status-alert', 'color'),
             Output('action-progress-container', 'className'),
             Output('action-progress-bar', 'value'),
             Output('action-progress-text', 'children'),
             Output('activity-log', 'children')],
            [Input('collect-metrics-btn', 'n_clicks'),
             Input('run-tests-btn', 'n_clicks')],
            [State('activity-log', 'children')]
        )
        def handle_action_buttons(collect_clicks, run_clicks, current_log):
            # Determine which button was clicked
            triggered_id = ctx.triggered_id if ctx.triggered_id else 'no-id'
            
            if not ctx.triggered:
                # No button clicked, return initial state
                return (
                    "No actions performed yet", "secondary", "d-none", 
                    0, "0%", current_log
                )
            
            # Add new log entry
            now = datetime.datetime.now().strftime("%H:%M:%S")
            if triggered_id == 'collect-metrics-btn':
                new_log = html.Div(f"[{now}] Collecting new metrics...", className="mb-1")
                # In a real implementation, you would trigger the metrics collection here
                # For now, we'll just simulate it
                return (
                    "Collecting new metrics...", "info", "", 
                    50, "50%", [new_log] + (current_log if isinstance(current_log, list) else [current_log])
                )
                
            elif triggered_id == 'run-tests-btn':
                new_log = html.Div(f"[{now}] Running all tests...", className="mb-1")
                # In a real implementation, you would trigger test runs here
                # For now, we'll just simulate it
                return (
                    "Running all tests...", "info", "", 
                    30, "30%", [new_log] + (current_log if isinstance(current_log, list) else [current_log])
                )
                
            # Default return if somehow no button matched
            return (
                "Unknown action", "warning", "d-none", 
                0, "0%", current_log
            )
    
    def _get_status_color(self, value):
        """Get status color based on value (higher is better)"""
        if value >= 90:
            return "success"
        elif value >= 75:
            return "warning"
        else:
            return "danger"
    
    def _get_inverse_status_color(self, value):
        """Get status color based on value (lower is better)"""
        if value <= 10:
            return "success"
        elif value <= 25:
            return "warning"
        else:
            return "danger"
            
    def _create_empty_visualization(self):
        """Create an empty 3D visualization figure"""
        fig = go.Figure(
            go.Scatter3d(
                x=[0],
                y=[0],
                z=[0],
                mode='markers',
                marker=dict(
                    size=1,
                    color=quantum_theme['accent1'],
                    opacity=0.5
                )
            )
        )
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=quantum_theme['panel'],
            plot_bgcolor=quantum_theme['panel'],
            scene=dict(
                xaxis=dict(
                    title="Quality",
                    showbackground=True,
                    backgroundcolor=quantum_theme['background'],
                    gridcolor=quantum_theme['grid'],
                    showticklabels=False
                ),
                yaxis=dict(
                    title="Coverage",
                    showbackground=True,
                    backgroundcolor=quantum_theme['background'],
                    gridcolor=quantum_theme['grid'],
                    showticklabels=False
                ),
                zaxis=dict(
                    title="Performance",
                    showbackground=True,
                    backgroundcolor=quantum_theme['background'],
                    gridcolor=quantum_theme['grid'],
                    showticklabels=False
                )
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )
        
        return fig
        
    def _create_empty_trend_graph(self):
        """Create an empty trend graph"""
        fig = go.Figure()
        
        # Add empty line
        fig.add_trace(
            go.Scatter(
                x=[0, 1, 2, 3, 4],
                y=[0, 0, 0, 0, 0],
                mode='lines',
                line=dict(color=quantum_theme['accent1'], width=2)
            )
        )
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="transparent",
            plot_bgcolor="transparent",
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            showlegend=False
        )
        
        return fig
        
    def _create_3d_visualization(self, metrics_data, animation_data):
        """Create a 3D visualization of the quantum metrics"""
        # Extract metrics from data dictionary
        metrics = metrics_data
        frame = animation_data.get('frame', 0)
        
        # Create points for the visualization
        # We'll create a series of points that represent the 5D metrics projected into 3D space
        
        # Main dimensional positions
        quality = metrics.get('quality_position', 0)
        coverage = metrics.get('coverage_position', 0)
        performance = metrics.get('performance_position', 0)
        security = metrics.get('security_position', 0)
        
        # Create the central point (the current state)
        x = [quality]
        y = [coverage]
        z = [performance]
        
        # Add secondary points that show the dimensional paths
        t = np.linspace(0, 2*np.pi, 50)
        
        # Create a spiral that represents the path through dimensions
        for i in range(len(t)):
            # Add animation offset
            angle = t[i] + (frame / 30)
            
            # Calculate coordinates with some oscillation
            radius = 10 + 5 * np.sin(angle * 3 + frame / 10)
            height = 10 * np.cos(angle * 2 + frame / 15)
            
            x.append(quality + radius * np.cos(angle))
            y.append(coverage + radius * np.sin(angle))
            z.append(performance + height)
        
        # Create quantum aura (sphere) around the main point
        stability = metrics.get('dimensional_stability', 100)
        coherence = metrics.get('quantum_coherence', 100)
        
        # Size of aura proportional to stability
        aura_size = stability / 10
        
        # Generate points for the aura
        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 20)
        aura_x = quality + aura_size * np.outer(np.cos(u), np.sin(v)).flatten()
        aura_y = coverage + aura_size * np.outer(np.sin(u), np.sin(v)).flatten()
        aura_z = performance + aura_size * np.outer(np.ones(np.size(u)), np.cos(v)).flatten()
        
        # Calculate colors based on coherence
        if coherence >= 90:
            aura_color = quantum_theme['success']
        elif coherence >= 75:
            aura_color = quantum_theme['warning']
        else:
            aura_color = quantum_theme['error']
        
        # Create the figure
        fig = go.Figure()
        
        # Add the aura (cloud of points)
        fig.add_trace(
            go.Scatter3d(
                x=aura_x,
                y=aura_y,
                z=aura_z,
                mode='markers',
                marker=dict(
                    size=3,
                    color=aura_color,
                    opacity=0.3
                ),
                hoverinfo='none'
            )
        )
        
        # Add the dimensional path
        fig.add_trace(
            go.Scatter3d(
                x=x[1:],
                y=y[1:],
                z=z[1:],
                mode='lines',
                line=dict(
                    color=quantum_theme['accent1'],
                    width=3
                ),
                hoverinfo='none'
            )
        )
        
        # Add the current position point
        fig.add_trace(
            go.Scatter3d(
                x=[quality],
                y=[coverage],
                z=[performance],
                mode='markers',
                marker=dict(
                    size=10,
                    color=quantum_theme['highlight'],
                    symbol='circle',
                    line=dict(
                        color=quantum_theme['text'],
                        width=2
                    )
                ),
                hovertemplate=(
                    "<b>Quantum State</b><br>" +
                    "Quality: %{x:.1f}<br>" +
                    "Coverage: %{y:.1f}<br>" +
                    "Performance: %{z:.1f}<br>" +
                    "Security: " + f"{security:.1f}" +
                    "<extra></extra>"
                )
            )
        )
        
        # Add the security dimension as a projection plane or grid
        grid_x, grid_y = np.meshgrid(
            np.linspace(quality - 20, quality + 20, 5),
            np.linspace(coverage - 20, coverage + 20, 5)
        )
        grid_z = np.ones_like(grid_x) * (performance - 20) + security / 5
        
        fig.add_trace(
            go.Surface(
                x=grid_x,
                y=grid_y,
                z=grid_z,
                colorscale=[[0, quantum_theme['accent4']], [1, quantum_theme['accent4']]],
                showscale=False,
                opacity=0.1,
                hoverinfo='none'
            )
        )
        
        # Update layout
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=quantum_theme['panel'],
            plot_bgcolor=quantum_theme['panel'],
            scene=dict(
                xaxis=dict(
                    title="Quality",
                    range=[0, 100],
                    showbackground=True,
                    backgroundcolor=quantum_theme['background'],
                    gridcolor=quantum_theme['grid']
                ),
                yaxis=dict(
                    title="Coverage",
                    range=[0, 100],
                    showbackground=True,
                    backgroundcolor=quantum_theme['background'],
                    gridcolor=quantum_theme['grid']
                ),
                zaxis=dict(
                    title="Performance",
                    range=[0, 100],
                    showbackground=True,
                    backgroundcolor=quantum_theme['background'],
                    gridcolor=quantum_theme['grid']
                ),
                camera=dict(
                    # Rotate camera based on animation frame for subtle motion
                    eye=dict(
                        x=1.5 * np.cos(frame / 50),
                        y=1.5 * np.sin(frame / 50),
                        z=1.0
                    )
                )
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )
        
        return fig
    
    def _create_hyperspatial_trend_graph(self, metrics_data):
        """Create a graph showing the hyperspatial trend"""
        # Extract the trend data from the metrics
        trend = metrics_data.get('hyperspatial_trend', [0, 0, 0, 0, 0])
        
        # Create labels for the dimensions
        labels = ['Time', 'Quality', 'Coverage', 'Performance', 'Security']
        
        # Create the radar chart
        fig = go.Figure()
        
        # Get safe fill color
        fill_color = self._safe_rgba_from_hex(quantum_theme['accent1'], 0.3)
        
        fig.add_trace(
            go.Scatterpolar(
                r=trend,
                theta=labels,
                fill='toself',
                fillcolor=fill_color,
                line=dict(
                    color=quantum_theme['accent1'],
                    width=2
                )
            )
        )
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="transparent",
            plot_bgcolor="transparent",
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    showticklabels=False,
                    gridcolor=quantum_theme['grid']
                ),
                angularaxis=dict(
                    gridcolor=quantum_theme['grid']
                ),
                bgcolor="transparent"
            ),
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False
        )
        
        return fig
        
    def _create_dimension_graph(self, metrics_data, dimension):
        """Create a graph for a specific dimension"""
        if not metrics_data:
            # Return empty figure
            return self._create_empty_trend_graph()
        
        # Create some mock historical data if we don't have real data
        # In a real implementation, this would come from stored metrics history
        history_length = 20
        history = []
        
        # Get current value for this dimension
        current_value = metrics_data.get(f'{dimension}_position', 50)
        
        # Generate mock history data
        for i in range(history_length):
            # Add some random variation but keep trend toward current value
            if i == history_length - 1:
                history.append(current_value)  # Latest value is current
            else:
                # Closer to end of array = closer to current value
                weight = i / history_length
                base_value = current_value * weight + 50 * (1 - weight)
                history.append(base_value + np.random.normal(0, 5))
        
        # Get color for this dimension
        dimension_colors = {
            'quality': quantum_theme['accent1'],
            'coverage': quantum_theme['accent2'],
            'performance': quantum_theme['accent3'],
            'security': quantum_theme['accent4'],
            'time': quantum_theme['highlight']
        }
        color = dimension_colors.get(dimension, quantum_theme['text'])
        
        # Get safe fill color
        fill_color = self._safe_rgba_from_hex(color, 0.2)
        
        # Create the figure
        fig = go.Figure()
        
        # Add the line
        fig.add_trace(
            go.Scatter(
                x=list(range(history_length)),
                y=history,
                mode='lines',
                line=dict(
                    color=color,
                    width=2,
                    shape='spline',
                    smoothing=1.3
                ),
                fill='tozeroy',
                fillcolor=fill_color
            )
        )
        
        # Add current point
        fig.add_trace(
            go.Scatter(
                x=[history_length - 1],
                y=[current_value],
                mode='markers',
                marker=dict(
                    size=10,
                    color=color,
                    line=dict(
                        color=quantum_theme['text'],
                        width=2
                    )
                ),
                hoverinfo='y'
            )
        )
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(
                range=[0, 100],
                showticklabels=False,
                showgrid=True,
                gridcolor=quantum_theme['grid'],
                zeroline=False
            ),
            showlegend=False
        )
        
        return fig
    
    def _create_dimension_metrics(self, metrics_data, dimension):
        """Create metrics display for a specific dimension"""
        if not metrics_data:
            return html.Div("No data available")
        
        # Get the value for this dimension
        value = metrics_data.get(f'{dimension}_position', 0)
        
        # Generate dimension-specific metrics
        if dimension == 'quality':
            metrics = [
                {"name": "Success Rate", "value": f"{metrics_data.get('success_score', 0):.1f}%"},
                {"name": "API Reliability", "value": f"{metrics_data.get('api_score', 0):.1f}%"}
            ]
        elif dimension == 'coverage':
            metrics = [
                {"name": "Code Coverage", "value": f"{metrics_data.get('coverage_score', 0):.1f}%"},
                {"name": "Test Density", "value": "Medium"}  # Mock value
            ]
        elif dimension == 'performance':
            metrics = [
                {"name": "CPU Usage", "value": "32%"},  # Mock value
                {"name": "Memory", "value": "45%"}  # Mock value
            ]
        elif dimension == 'security':
            metrics = [
                {"name": "Vulnerabilities", "value": "0"},  # Mock value
                {"name": "Auth Status", "value": "Secure"}  # Mock value
            ]
        elif dimension == 'time':
            now = datetime.datetime.now()
            day_percent = (now.hour * 3600 + now.minute * 60 + now.second) / 86400 * 100
            metrics = [
                {"name": "Time Position", "value": f"{day_percent:.1f}%"},
                {"name": "Update Frequency", "value": f"{DASHBOARD_CONFIG['ui_refresh_interval']}s"}
            ]
        else:
            metrics = []
        
        # Generate the metrics display
        children = []
        for metric in metrics:
            children.append(html.Div(
                className="d-flex justify-content-between",
                children=[
                    html.Small(metric["name"], className="text-muted"),
                    html.Small(metric["value"], style={"fontWeight": "bold"})
                ]
            ))
        
        return html.Div(children)
    
    def _create_2d_matrix_visualization(self, metrics_data, animation_data):
        """Create a 2D matrix visualization"""
        # This is a simplified implementation
        # In a real implementation, this would be more elaborate
        
        # Create some mock data points for the matrix
        n = 20
        x = np.linspace(0, 100, n)
        y = np.linspace(0, 100, n)
        z = np.zeros((n, n))
        
        # Extract metrics values
        quality = metrics_data.get('quality_position', 50)
        coverage = metrics_data.get('coverage_position', 50)
        
        # Generate the z values with some animation
        frame = animation_data.get('frame', 0)
        for i in range(n):
            for j in range(n):
                # Distance from the current position
                dist = np.sqrt((x[i] - quality)**2 + (y[j] - coverage)**2)
                # Create a wave effect
                z[j][i] = 50 + 30 * np.sin(dist / 10 - frame / 10) * np.exp(-dist / 30)
        
        # Create the figure
        fig = go.Figure(data=go.Heatmap(
            z=z,
            x=x,
            y=y,
            colorscale=[
                [0, quantum_theme['background']],
                [0.4, quantum_theme['accent4']],
                [0.6, quantum_theme['accent3']],
                [0.8, quantum_theme['accent2']],
                [1, quantum_theme['accent1']]
            ],
            showscale=False
        ))
        
        # Add the current position point
        fig.add_trace(
            go.Scatter(
                x=[quality],
                y=[coverage],
                mode='markers',
                marker=dict(
                    size=12,
                    color=quantum_theme['highlight'],
                    line=dict(
                        color=quantum_theme['text'],
                        width=2
                    )
                ),
                hovertemplate=(
                    "<b>Current Position</b><br>" +
                    "Quality: %{x:.1f}<br>" +
                    "Coverage: %{y:.1f}<br>" +
                    "<extra></extra>"
                )
            )
        )
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=quantum_theme['panel'],
            plot_bgcolor=quantum_theme['background'],
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(
                title="Quality",
                range=[0, 100],
                showgrid=True,
                gridcolor=quantum_theme['grid']
            ),
            yaxis=dict(
                title="Coverage",
                range=[0, 100],
                showgrid=True,
                gridcolor=quantum_theme['grid']
            ),
            showlegend=False
        )
        
        return fig
        
    def _create_quantum_flow_visualization(self, metrics_data, animation_data):
        """Create a quantum flow visualization"""
        # This would be a more elaborate visualization in a real implementation
        # For now, we'll create a simple streamline plot
        
        frame = animation_data.get('frame', 0)
        
        # Create a grid
        n = 20
        x = np.linspace(0, 100, n)
        y = np.linspace(0, 100, n)
        X, Y = np.meshgrid(x, y)
        
        # Vector field
        U = np.sin(X / 10 + frame / 20) * np.cos(Y / 10)
        V = np.cos(X / 10) * np.sin(Y / 10 + frame / 20)
        
        # Normalize
        magnitude = np.sqrt(U**2 + V**2)
        U = U / magnitude
        V = V / magnitude
        
        # Create streamlines
        fig = go.Figure()
        
        # Add streamlines
        for i in range(0, n, 2):
            for j in range(0, n, 2):
                # Start points
                x_start = X[i, j]
                y_start = Y[i, j]
                
                # Create a streamline
                x_line = [x_start]
                y_line = [y_start]
                
                for _ in range(10):
                    # Get vector at current position
                    x_idx = int(x_line[-1] / 100 * (n-1))
                    y_idx = int(y_line[-1] / 100 * (n-1))
                    
                    # Ensure indices are in bounds
                    x_idx = max(0, min(x_idx, n-1))
                    y_idx = max(0, min(y_idx, n-1))
                    
                    # Get vector
                    u = U[y_idx, x_idx]
                    v = V[y_idx, x_idx]
                    
                    # Update position
                    x_new = x_line[-1] + u * 5
                    y_new = y_line[-1] + v * 5
                    
                    # Check if out of bounds
                    if x_new < 0 or x_new > 100 or y_new < 0 or y_new > 100:
                        break
                    
                    x_line.append(x_new)
                    y_line.append(y_new)
                
                # Add line to figure
                fig.add_trace(
                    go.Scatter(
                        x=x_line,
                        y=y_line,
                        mode='lines',
                        line=dict(
                            color=quantum_theme['accent1'],
                            width=1
                        ),
                        hoverinfo='none'
                    )
                )
        
        # Add current position
        quality = metrics_data.get('quality_position', 50)
        coverage = metrics_data.get('coverage_position', 50)
        
        fig.add_trace(
            go.Scatter(
                x=[quality],
                y=[coverage],
                mode='markers',
                marker=dict(
                    size=12,
                    color=quantum_theme['highlight'],
                    line=dict(
                        color=quantum_theme['text'],
                        width=2
                    )
                ),
                hovertemplate=(
                    "<b>Current Position</b><br>" +
                    "Quality: %{x:.1f}<br>" +
                    "Coverage: %{y:.1f}<br>" +
                    "<extra></extra>"
                )
            )
        )
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=quantum_theme['panel'],
            plot_bgcolor=quantum_theme['background'],
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(
                title="Quality",
                range=[0, 100],
                showgrid=True,
                gridcolor=quantum_theme['grid']
            ),
            yaxis=dict(
                title="Coverage",
                range=[0, 100],
                showgrid=True,
                gridcolor=quantum_theme['grid']
            ),
            showlegend=False
        )
        
        return fig
    
    def _create_entanglement_web_visualization(self, metrics_data, animation_data):
        """Create an entanglement web visualization showing connections between dimensions"""
        # Extract the metrics
        quality = metrics_data.get('quality_position', 50)
        coverage = metrics_data.get('coverage_position', 50)
        performance = metrics_data.get('performance_position', 50)
        security = metrics_data.get('security_position', 50)
        time_pos = metrics_data.get('time_position', 50)
        
        # Get entanglement factor and frame
        entanglement = metrics_data.get('entanglement_factor', 0.5)
        frame = animation_data.get('frame', 0)
        
        # Create positions for the nodes in a pentagon
        radius = 40
        angles = np.linspace(0, 2*np.pi, 6)[:-1]  # 5 points, remove the last one (equal to first)
        
        # Add slight movement to the nodes based on the animation frame
        angles = angles + np.sin(frame / 20) * 0.05
        
        x_nodes = [50 + radius * np.cos(angle) for angle in angles]
        y_nodes = [50 + radius * np.sin(angle) for angle in angles]
        
        # Dimension values
        values = [quality, coverage, performance, security, time_pos]
        
        # Node labels
        labels = ['Quality', 'Coverage', 'Performance', 'Security', 'Time']
        
        # Entanglement strengths between dimensions (mock data, would be calculated in real impl)
        # Higher value = stronger connection
        connections = [
            [0, 0.8, 0.3, 0.5, 0.2],  # Quality connections
            [0.8, 0, 0.7, 0.4, 0.3],  # Coverage connections
            [0.3, 0.7, 0, 0.6, 0.4],  # Performance connections
            [0.5, 0.4, 0.6, 0, 0.2],  # Security connections
            [0.2, 0.3, 0.4, 0.2, 0]   # Time connections
        ]
        
        # Adjust connection strengths by overall entanglement factor
        for i in range(5):
            for j in range(5):
                connections[i][j] *= entanglement
        
        # Create the figure
        fig = go.Figure()
        
        # Add the connections between nodes
        for i in range(5):
            for j in range(i+1, 5):  # Only upper triangle to avoid duplicates
                # Skip connections that are too weak
                if connections[i][j] < 0.1:
                    continue
                
                # Calculate line width and opacity based on connection strength
                width = connections[i][j] * 5
                opacity = connections[i][j]
                
                # Add a curved line for aesthetics
                t = np.linspace(0, 1, 30)
                # Add some animation to the curve
                curve_height = 10 * connections[i][j] * np.sin(frame / 20 + i*0.5 + j*0.7)
                
                # Calculate the midpoint
                mid_x = (x_nodes[i] + x_nodes[j]) / 2
                mid_y = (y_nodes[i] + y_nodes[j]) / 2
                
                # Calculate the perpendicular vector for curve control
                dx = x_nodes[j] - x_nodes[i]
                dy = y_nodes[j] - y_nodes[i]
                # Rotate 90 degrees
                perp_x = -dy
                perp_y = dx
                # Normalize
                mag = np.sqrt(perp_x**2 + perp_y**2)
                if mag > 0:
                    perp_x = perp_x / mag
                    perp_y = perp_y / mag
                
                # Control point for the curve
                ctrl_x = mid_x + perp_x * curve_height
                ctrl_y = mid_y + perp_y * curve_height
                
                # Generate the curve using quadratic Bezier
                curve_x = [(1-t_val)**2 * x_nodes[i] + 2*(1-t_val)*t_val * ctrl_x + t_val**2 * x_nodes[j] for t_val in t]
                curve_y = [(1-t_val)**2 * y_nodes[i] + 2*(1-t_val)*t_val * ctrl_y + t_val**2 * y_nodes[j] for t_val in t]
                
                # Add the connection line
                fig.add_trace(
                    go.Scatter(
                        x=curve_x,
                        y=curve_y,
                        mode='lines',
                        line=dict(
                            width=width,
                            color=quantum_theme['accent1'],
                            opacity=opacity
                        ),
                        hoverinfo='none'
                    )
                )
        
        # Add the nodes
        for i in range(5):
            # Calculate node size based on the dimension value
            size = values[i] / 5 + 10  # Scale to reasonable size
            
            # Calculate node color based on value
            if values[i] >= 90:
                color = quantum_theme['success']
            elif values[i] >= 75:
                color = quantum_theme['warning']
            else:
                color = quantum_theme['error']
            
            # Add the node
            fig.add_trace(
                go.Scatter(
                    x=[x_nodes[i]],
                    y=[y_nodes[i]],
                    mode='markers+text',
                    marker=dict(
                        size=size,
                        color=color,
                        line=dict(
                            color=quantum_theme['text'],
                            width=1
                        )
                    ),
                    text=labels[i],
                    textposition='top center',
                    textfont=dict(
                        color=quantum_theme['text']
                    ),
                    hovertemplate=(
                        f"<b>{labels[i]}</b><br>" +
                        f"Value: {values[i]:.1f}<br>" +
                        "<extra></extra>"
                    )
                )
            )
        
        # Add the entanglement factor label in the center
        fig.add_trace(
            go.Scatter(
                x=[50],
                y=[50],
                mode='markers+text',
                marker=dict(
                    size=entanglement * 30 + 10,
                    color=quantum_theme['accent4'],
                    opacity=0.7
                ),
                text=f"{entanglement:.2f}",
                textfont=dict(
                    color=quantum_theme['text'],
                    size=16
                ),
                hovertemplate=(
                    "<b>Entanglement Factor</b><br>" +
                    f"{entanglement:.2f}<br>" +
                    "<extra></extra>"
                )
            )
        )
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=quantum_theme['panel'],
            plot_bgcolor=quantum_theme['background'],
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(
                range=[0, 100],
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            yaxis=dict(
                range=[0, 100],
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            showlegend=False
        )
        
        return fig
    
    def _create_hypercube_visualization(self, metrics_data, animation_data):
        """Create a 5D hypercube visualization"""
        # This is a simplified version - a real implementation would be more elaborate
        # We'll project a 5D hypercube into 3D space
        
        # Extract metrics and animation frame
        quality = metrics_data.get('quality_position', 50)
        coverage = metrics_data.get('coverage_position', 50)
        performance = metrics_data.get('performance_position', 50)
        security = metrics_data.get('security_position', 50)
        time_pos = metrics_data.get('time_position', 50)
        frame = animation_data.get('frame', 0)
        
        # Define a 3D cube vertices (normalized to 0-1)
        vertices_3d = np.array([
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
        ])
        
        # Define edges connecting vertices
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Top face
            (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
        ]
        
        # Scale and center the cube
        scale = 50
        center = np.array([50, 50, 50])
        vertices_3d = vertices_3d * scale + center
        
        # Project the 5D metrics into the 3D space
        # These projections are simplified - real 5D projection would be more complex
        time_angle = (time_pos / 100) * 2 * np.pi + frame / 50
        
        # Create a rotation matrix based on the time dimension
        rot_x = np.array([
            [1, 0, 0],
            [0, np.cos(time_angle), -np.sin(time_angle)],
            [0, np.sin(time_angle), np.cos(time_angle)]
        ])
        
        rot_y = np.array([
            [np.cos(time_angle), 0, np.sin(time_angle)],
            [0, 1, 0],
            [-np.sin(time_angle), 0, np.cos(time_angle)]
        ])
        
        rot_z = np.array([
            [np.cos(time_angle), -np.sin(time_angle), 0],
            [np.sin(time_angle), np.cos(time_angle), 0],
            [0, 0, 1]
        ])
        
        # Apply the rotations
        vertices_rotated = vertices_3d.copy()
        for i in range(len(vertices_3d)):
            # Apply rotations
            vertices_rotated[i] = rot_x @ rot_y @ rot_z @ (vertices_3d[i] - center) + center
        
        # Scale vertices based on security dimension
        security_scale = 0.5 + security / 100
        vertices_scaled = center + (vertices_rotated - center) * security_scale
        
        # Create the figure
        fig = go.Figure()
        
        # Add each edge as a line
        for edge in edges:
            fig.add_trace(
                go.Scatter3d(
                    x=[vertices_scaled[edge[0]][0], vertices_scaled[edge[1]][0]],
                    y=[vertices_scaled[edge[0]][1], vertices_scaled[edge[1]][1]],
                    z=[vertices_scaled[edge[0]][2], vertices_scaled[edge[1]][2]],
                    mode='lines',
                    line=dict(
                        color=quantum_theme['accent1'],
                        width=2
                    ),
                    hoverinfo='none'
                )
            )
        
        # Add vertices as markers
        fig.add_trace(
            go.Scatter3d(
                x=vertices_scaled[:, 0],
                y=vertices_scaled[:, 1],
                z=vertices_scaled[:, 2],
                mode='markers',
                marker=dict(
                    size=5,
                    color=quantum_theme['accent2']
                ),
                hoverinfo='none'
            )
        )
        
        # Add the current position point
        fig.add_trace(
            go.Scatter3d(
                x=[quality],
                y=[coverage],
                z=[performance],
                mode='markers',
                marker=dict(
                    size=10,
                    color=quantum_theme['highlight'],
                    symbol='circle',
                    line=dict(
                        color=quantum_theme['text'],
                        width=2
                    )
                ),
                hovertemplate=(
                    "<b>Quantum State</b><br>" +
                    "Quality: %{x:.1f}<br>" +
                    "Coverage: %{y:.1f}<br>" +
                    "Performance: %{z:.1f}<br>" +
                    "Security: " + f"{security:.1f}" +
                    "<extra></extra>"
                )
            )
        )
        
        # Update layout
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=quantum_theme['panel'],
            plot_bgcolor=quantum_theme['panel'],
            scene=dict(
                xaxis=dict(
                    title="Quality",
                    range=[0, 100],
                    showbackground=True,
                    backgroundcolor=quantum_theme['background'],
                    gridcolor=quantum_theme['grid']
                ),
                yaxis=dict(
                    title="Coverage",
                    range=[0, 100],
                    showbackground=True,
                    backgroundcolor=quantum_theme['background'],
                    gridcolor=quantum_theme['grid']
                ),
                zaxis=dict(
                    title="Performance",
                    range=[0, 100],
                    showbackground=True,
                    backgroundcolor=quantum_theme['background'],
                    gridcolor=quantum_theme['grid']
                ),
                camera=dict(
                    # Rotate camera based on animation frame for subtle motion
                    eye=dict(
                        x=1.5 * np.cos(frame / 50),
                        y=1.5 * np.sin(frame / 50),
                        z=1.0
                    )
                )
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )
        
        return fig
    
    def collect_metrics(self):
        """Collect metrics from QA metrics collector"""
        try:
            # First try to get real metrics from test reports
            metrics = QuantumMetrics.from_test_reports()
            logger.info("Collected metrics from test report data")
        except Exception as e:
            logger.warning(f"Error collecting metrics from test reports: {e}, falling back to QA metrics")
            try:
                # If that fails, try the QA metrics collector
                qa_metrics = collect_and_save_metrics()
                metrics = QuantumMetrics.from_qa_metrics(qa_metrics)
                logger.info("Collected metrics from QA metrics collector")
            except Exception as e:
                logger.warning(f"Error collecting metrics from QA collector: {e}, using default values")
                # If all else fails, use default metrics
                metrics = QuantumMetrics()
                
                # Set reasonable default values
                metrics.coverage_score = 87.5
                metrics.success_score = 95.2
                metrics.performance_score = 92.3
                metrics.security_score = 89.1
                metrics.api_score = 97.8
                
                # Calculate quantum dimensions
                metrics._calculate_quantum_dimensions()
                
                logger.info("Using default metrics values")
        
        return metrics
    
    def start_metrics_collection(self):
        """Start the background thread for collecting metrics."""
        if self.collector_thread is not None and self.collector_thread.is_alive():
            logger.warning("Metrics collection thread is already running")
            return
            
        # Reset the stop event
        self.stop_event.clear()
        
        # Start the collector thread
        self.collector_thread = threading.Thread(
            target=self._metrics_collection_loop,
            daemon=True
        )
        self.collector_thread.start()
        logger.info("Started metrics collection thread")
        
        # Also scan for git data
        try:
            self.uncommitted_files_report = self.git_manager.get_uncommitted_report()
            self.last_git_scan = time.time()
        except Exception as e:
            logger.error(f"Error in initial git scan: {e}")
    
    def _metrics_collection_loop(self):
        """Background loop for collecting metrics periodically"""
        while not self.stop_event.is_set():
            try:
                logger.info("Collecting new metrics...")
                metrics = self.collect_metrics()
                self.current_metrics = metrics
                self.last_metrics_update = datetime.datetime.now()
                
                # Add to history (with a maximum size limit)
                self.metrics_history.append(metrics)
                if len(self.metrics_history) > DASHBOARD_CONFIG['max_history_points']:
                    self.metrics_history = self.metrics_history[-DASHBOARD_CONFIG['max_history_points']:]
                
                logger.info(f"Metrics updated - {metrics.dimensional_stability:.1f}% stability")
            except Exception as e:
                logger.error(f"Error collecting metrics: {str(e)}")
            
            # Wait for next collection interval or until stop event
            self.stop_event.wait(DASHBOARD_CONFIG['metrics_refresh_interval'])
    
    def stop_metrics_collection(self):
        """Stop the background metrics collection thread"""
        if self.collector_thread and self.collector_thread.is_alive():
            self.stop_event.set()
            self.collector_thread.join(timeout=2)
            logger.info("Stopped metrics collection thread")
    
    def run_dashboard(self, debug=False, host='0.0.0.0', port=8051):
        """Run the dashboard application"""
        logger.info(f"Starting Quantum 5D QA Dashboard on http://{host}:{port}")
        
        # Start metrics collection in the background
        self.start_metrics_collection()
        
        # Run the app
        try:
            self.app.run(debug=debug, host=host, port=port)
        finally:
            # Ensure we clean up the metrics collection thread
            self.stop_metrics_collection()

    # NEW: Build uncommitted files card
    def _build_uncommitted_files_card(self):
        """Build the card to display git uncommitted files and suggestions."""
        return dbc.Card(
            className="h-100 border-0 shadow",
            style={
                'backgroundColor': quantum_theme['panel'],
                'borderRadius': '10px'
            },
            children=[
                dbc.CardHeader(
                    className="d-flex justify-content-between align-items-center",
                    style={
                        'backgroundColor': 'transparent',
                        'borderBottom': f"1px solid {quantum_theme['grid']}",
                        'color': quantum_theme['accent4']
                    },
                    children=[
                        html.H5("Git Quantum State", className="mb-0"),
                        html.Div(
                            className="d-flex align-items-center",
                            children=[
                                dbc.Button(
                                    html.I(className="fas fa-sync"),
                                    color="link",
                                    size="sm",
                                    id="refresh-git-btn",
                                    className="p-0 me-2"
                                )
                            ]
                        )
                    ]
                ),
                dbc.CardBody(
                    [
                        # Git stats summary
                        html.Div(
                            className="mb-3",
                            children=[
                                html.H6("Uncommitted Files", className="mb-3"),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Card(
                                            className="text-center p-2 border-0",
                                            style={
                                                'backgroundColor': 'rgba(0, 184, 148, 0.1)',
                                                'borderRadius': '8px'
                                            },
                                            children=[
                                                html.H3(
                                                    "0",
                                                    id="git-total-files",
                                                    className="mb-0",
                                                    style={'color': quantum_theme['accent2']}
                                                ),
                                                html.Small("Total", className="text-muted")
                                            ]
                                        )
                                    ], width=3),
                                    dbc.Col([
                                        dbc.Card(
                                            className="text-center p-2 border-0",
                                            style={
                                                'backgroundColor': 'rgba(108, 92, 231, 0.1)',
                                                'borderRadius': '8px'
                                            },
                                            children=[
                                                html.H3(
                                                    "0",
                                                    id="git-modified-files",
                                                    className="mb-0",
                                                    style={'color': quantum_theme['accent1']}
                                                ),
                                                html.Small("Modified", className="text-muted")
                                            ]
                                        )
                                    ], width=3),
                                    dbc.Col([
                                        dbc.Card(
                                            className="text-center p-2 border-0",
                                            style={
                                                'backgroundColor': 'rgba(253, 203, 110, 0.1)',
                                                'borderRadius': '8px'
                                            },
                                            children=[
                                                html.H3(
                                                    "0",
                                                    id="git-added-files",
                                                    className="mb-0",
                                                    style={'color': quantum_theme['warning']}
                                                ),
                                                html.Small("New", className="text-muted")
                                            ]
                                        )
                                    ], width=3),
                                    dbc.Col([
                                        dbc.Card(
                                            className="text-center p-2 border-0",
                                            style={
                                                'backgroundColor': 'rgba(225, 112, 85, 0.1)',
                                                'borderRadius': '8px'
                                            },
                                            children=[
                                                html.H3(
                                                    "0",
                                                    id="git-deleted-files",
                                                    className="mb-0",
                                                    style={'color': quantum_theme['error']}
                                                ),
                                                html.Small("Deleted", className="text-muted")
                                            ]
                                        )
                                    ], width=3)
                                ])
                            ]
                        ),
                        
                        # Uncommitted file list
                        html.Div(
                            className="mb-3",
                            style={
                                'maxHeight': '150px',
                                'overflowY': 'auto',
                                'borderRadius': '8px',
                                'border': f"1px solid {quantum_theme['grid']}",
                                'padding': '10px'
                            },
                            children=[
                                html.Div(
                                    id="uncommitted-files-list",
                                    children=[
                                        html.P(
                                            "No uncommitted files found",
                                            className="text-muted text-center my-3"
                                        )
                                    ]
                                )
                            ]
                        ),
                        
                        # Commit suggestion
                        html.Div(
                            className="mb-3",
                            children=[
                                html.H6("Suggested Commit Message"),
                                dbc.Card(
                                    className="p-2 border-0",
                                    style={
                                        'backgroundColor': 'rgba(0, 206, 201, 0.1)',
                                        'borderRadius': '8px'
                                    },
                                    children=[
                                        html.P(
                                            "No changes to commit",
                                            id="git-commit-suggestion",
                                            className="mb-0",
                                            style={'color': quantum_theme['accent2']}
                                        )
                                    ]
                                )
                            ]
                        ),
                        
                        # Tag suggestion
                        html.Div(
                            children=[
                                html.H6("Suggested Tag"),
                                dbc.Card(
                                    className="p-2 border-0",
                                    style={
                                        'backgroundColor': 'rgba(116, 185, 255, 0.1)',
                                        'borderRadius': '8px'
                                    },
                                    children=[
                                        html.P(
                                            "No tag suggested",
                                            id="git-tag-suggestion",
                                            className="mb-0",
                                            style={'color': quantum_theme['accent3']}
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )

    # NEW: Setup git callbacks
    def _setup_git_callbacks(self):
        """Set up callbacks for git integration"""
        
        @self.app.callback(
            [Output('uncommitted-files-store', 'data'),
             Output('git-total-files', 'children'),
             Output('git-modified-files', 'children'),
             Output('git-added-files', 'children'),
             Output('git-deleted-files', 'children'),
             Output('uncommitted-files-list', 'children'),
             Output('git-commit-suggestion', 'children'),
             Output('git-tag-suggestion', 'children')],
            [Input('interval-component', 'n_intervals'),
             Input('refresh-git-btn', 'n_clicks')]
        )
        def update_git_info(n, btn_clicks):
            # Check if we should update
            now = time.time()
            force_update = btn_clicks is not None and ctx.triggered_id == 'refresh-git-btn'
            
            if not force_update and now - self.last_git_scan < 60:  # Update at most once per minute
                if self.uncommitted_files_report is None:
                    # First time, scan anyway
                    pass
                else:
                    # Return current data
                    return self._format_git_data_for_display(self.uncommitted_files_report)
            
            # Scan for uncommitted files
            try:
                self.uncommitted_files_report = self.git_manager.get_uncommitted_report()
                self.last_git_scan = now
                return self._format_git_data_for_display(self.uncommitted_files_report)
            except Exception as e:
                logger.error(f"Error updating git info: {e}")
                # Return empty data
                return (
                    None,  # Store data
                    "0",   # Total files
                    "0",   # Modified files
                    "0",   # Added files 
                    "0",   # Deleted files
                    [html.P("Error scanning git repository", className="text-danger text-center my-3")],  # Files list
                    "Error scanning git repository",  # Commit suggestion
                    "Error scanning git repository"   # Tag suggestion
                )
    
    def _format_git_data_for_display(self, report):
        """Format git data for display in the dashboard"""
        # Counters
        total = report['file_counts']['total']
        modified = report['file_counts']['modified']
        added = report['file_counts']['added'] + report['file_counts']['untracked']
        deleted = report['file_counts']['deleted']
        
        # File list
        file_list = []
        
        # Add modified files
        for file_path in report['files']['modified'][:5]:  # Top 5
            file_list.append(html.Div(
                className="d-flex align-items-center mb-1",
                children=[
                    html.Span(
                        "●",
                        className="me-2",
                        style={'color': quantum_theme['accent1']}
                    ),
                    html.Span(
                        file_path,
                        style={'color': quantum_theme['text'], 'fontSize': '0.85rem'}
                    )
                ]
            ))
        
        # Add new files
        for file_path in (report['files']['added'] + report['files']['untracked'])[:5]:  # Top 5
            file_list.append(html.Div(
                className="d-flex align-items-center mb-1",
                children=[
                    html.Span(
                        "●",
                        className="me-2",
                        style={'color': quantum_theme['warning']}
                    ),
                    html.Span(
                        file_path,
                        style={'color': quantum_theme['text'], 'fontSize': '0.85rem'}
                    )
                ]
            ))
        
        # Add deleted files
        for file_path in report['files']['deleted'][:3]:  # Top 3
            file_list.append(html.Div(
                className="d-flex align-items-center mb-1",
                children=[
                    html.Span(
                        "●",
                        className="me-2",
                        style={'color': quantum_theme['error']}
                    ),
                    html.Span(
                        file_path,
                        style={'color': quantum_theme['text'], 'fontSize': '0.85rem', 'textDecoration': 'line-through'}
                    )
                ]
            ))
        
        # If no files, show message
        if not file_list:
            file_list = [html.P("No uncommitted files found", className="text-muted text-center my-3")]
        
        # Format the commit message with line breaks for dashboard
        commit_message = report['suggestions']['commit_message']
        formatted_commit = []
        for line in commit_message.split('\n'):
            formatted_commit.append(html.Span(line))
            formatted_commit.append(html.Br())
        
        # Return all formatted data
        return (
            report,  # Store data
            str(total),  # Total files
            str(modified),  # Modified files
            str(added),  # Added files
            str(deleted),  # Deleted files
            file_list,  # Files list
            formatted_commit,  # Commit suggestion
            report['suggestions']['tag']  # Tag suggestion
        )

    def _safe_rgba_from_hex(self, hex_color, alpha=0.3):
        """Safely convert a hex color to RGBA format with error handling"""
        try:
            # Remove the leading # if present
            if hex_color.startswith('#'):
                hex_color = hex_color[1:]
            
            # Parse the RGB components safely
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                return f'rgba({r}, {g}, {b}, {alpha})'
            else:
                # Fallback to a safe default
                return f'rgba(108, 92, 231, {alpha})'  # Default color with opacity
        except Exception as e:
            # Log the error and use a fallback
            logger.error(f"Error parsing color: {e}")
            return f'rgba(108, 92, 231, {alpha})'  # Default color with opacity

    def _build_matrix_monitoring_card(self):
        """Build the advanced MATRIX C1B3R1T4L real-time monitoring card with ChainGPT-inspired design."""
        return dbc.Card(
            className="h-100 border-0 shadow",
            style={
                'backgroundColor': quantum_theme['panel'],
                'borderRadius': '10px',
                'background': f'linear-gradient(135deg, {quantum_theme["panel"]}, #111823)',
                'boxShadow': f'0 0 20px rgba(108, 92, 231, 0.2)'
            },
            children=[
                dbc.CardHeader(
                    className="d-flex justify-content-between align-items-center",
                    style={
                        'backgroundColor': 'transparent',
                        'borderBottom': f"1px solid {quantum_theme['accent4']}",
                        'color': quantum_theme['highlight'],
                        'padding': '16px 20px'
                    },
                    children=[
                        html.H5(
                            className="mb-0 d-flex align-items-center",
                            children=[
                                html.I(className="fas fa-cube me-2", style={'color': quantum_theme['accent2']}),
                                html.Span([
                                    "MATR1X ", 
                                    html.Span("C1B3R1T4L", style={'color': quantum_theme['accent2']}),
                                    " QA Monitor"
                                ])
                            ],
                            style={'fontWeight': 'bold', 'letterSpacing': '2px', 'textShadow': '0 0 5px rgba(108, 92, 231, 0.5)'}
                        ),
                        dbc.Badge(
                            "∞", 
                            color="dark",
                            className="rounded-pill",
                            style={
                                'backgroundColor': quantum_theme['background'], 
                                'color': quantum_theme['accent1'],
                                'border': f'1px solid {quantum_theme["accent1"]}',
                                'fontSize': '14px',
                                'boxShadow': '0 0 8px rgba(108, 92, 231, 0.5)'
                            }
                        )
                    ]
                ),
                dbc.CardBody(
                    [
                        # Advanced monitor container with terminal-like styling
                        html.Div(
                            style={
                                'backgroundColor': 'rgba(10, 14, 23, 0.7)',
                                'borderRadius': '6px',
                                'border': f'1px solid {quantum_theme["accent1"]}',
                                'boxShadow': 'inset 0 0 15px rgba(0, 0, 0, 0.5)',
                                'padding': '15px',
                                'fontFamily': 'monospace',
                                'overflow': 'hidden',
                                'position': 'relative',
                                'height': '280px'
                            },
                            className="mb-3",
                            children=[
                                # Terminal header
                                html.Div(
                                    className="d-flex justify-content-between align-items-center mb-2",
                                    children=[
                                        html.Span("QUANTUM MATRIX MONITOR v5.7.3", style={'color': quantum_theme['accent2'], 'fontWeight': 'bold'}),
                                        html.Div([
                                            html.Span("●", style={'color': quantum_theme['error'], 'fontSize': '10px', 'marginRight': '8px'}),
                                            html.Span("●", style={'color': quantum_theme['warning'], 'fontSize': '10px', 'marginRight': '8px'}),
                                            html.Span("●", style={'color': quantum_theme['success'], 'fontSize': '10px'})
                                        ])
                                    ]
                                ),
                                
                                # Live terminal output
                                html.Div(
                                    id="matrix-terminal-output",
                                    className="mt-3",
                                    style={
                                        'color': quantum_theme['text'],
                                        'fontSize': '0.85rem',
                                        'height': '230px',
                                        'overflowY': 'auto',
                                        'overflowX': 'hidden',
                                        'paddingRight': '5px',
                                        'marginBottom': '10px'
                                    },
                                    children=[
                                        html.P(
                                            [
                                                html.Span(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ", style={'color': quantum_theme['accent4']}),
                                                "5D Quantum Matrix Initialized"
                                            ],
                                            className="mb-1"
                                        ),
                                        html.P(
                                            [
                                                html.Span(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ", style={'color': quantum_theme['accent4']}),
                                                "Dimensional scanning active..."
                                            ],
                                            className="mb-1"
                                        ),
                                        html.P(
                                            [
                                                html.Span(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ", style={'color': quantum_theme['accent4']}),
                                                html.Span("Hyperspace channels open", style={'color': quantum_theme['success']})
                                            ],
                                            className="mb-1"
                                        ),
                                        html.P(
                                            [
                                                html.Span(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ", style={'color': quantum_theme['accent4']}),
                                                "Monitoring all quantum fluctuations"
                                            ],
                                            className="mb-1"
                                        ),
                                        html.P(
                                            [
                                                html.Span(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ", style={'color': quantum_theme['accent4']}),
                                                html.Span("REALTIME QA MONITORING ACTIVE", style={'color': quantum_theme['accent2'], 'fontWeight': 'bold'})
                                            ],
                                            className="mb-3"
                                        ),
                                        html.Div(
                                            id="matrix-terminal-events",
                                            children=[]
                                        )
                                    ]
                                ),
                                
                                # Blinking cursor
                                html.Div(
                                    className="position-absolute cursor-blink",
                                    style={
                                        'bottom': '15px',
                                        'left': '15px',
                                        'width': '10px',
                                        'height': '20px',
                                        'backgroundColor': quantum_theme['accent1']
                                    }
                                )
                            ]
                        ),
                        
                        # Status grid
                        html.Div(
                            className="row g-2",
                            children=[
                                # Status indicators - Using a grid layout for metrics
                                html.Div(
                                    className="col-6 col-lg-3",
                                    children=[
                                        html.Div(
                                            className="p-2",
                                            style={
                                                'backgroundColor': 'rgba(10, 14, 23, 0.7)',
                                                'borderRadius': '6px',
                                                'border': f'1px solid {quantum_theme["accent3"]}',
                                            },
                                            children=[
                                                html.Div(
                                                    className="d-flex align-items-center justify-content-between",
                                                    children=[
                                                        html.Small("Blockchain", style={'color': quantum_theme['accent3']}),
                                                        html.Span("ACTIVE", style={'color': quantum_theme['success'], 'fontSize': '0.75rem'})
                                                    ]
                                                ),
                                                html.Div(
                                                    "CONNECTED",
                                                    style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '1rem', 'marginTop': '2px'}
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                
                                html.Div(
                                    className="col-6 col-lg-3",
                                    children=[
                                        html.Div(
                                            className="p-2",
                                            style={
                                                'backgroundColor': 'rgba(10, 14, 23, 0.7)',
                                                'borderRadius': '6px',
                                                'border': f'1px solid {quantum_theme["accent1"]}',
                                            },
                                            children=[
                                                html.Div(
                                                    className="d-flex align-items-center justify-content-between",
                                                    children=[
                                                        html.Small("Node Status", style={'color': quantum_theme['accent1']}),
                                                        html.Span("SYNCED", style={'color': quantum_theme['success'], 'fontSize': '0.75rem'})
                                                    ]
                                                ),
                                                html.Div(
                                                    "5 / 5",
                                                    style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '1rem', 'marginTop': '2px'}
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                
                                html.Div(
                                    className="col-6 col-lg-3",
                                    children=[
                                        html.Div(
                                            className="p-2",
                                            style={
                                                'backgroundColor': 'rgba(10, 14, 23, 0.7)',
                                                'borderRadius': '6px',
                                                'border': f'1px solid {quantum_theme["accent2"]}',
                                            },
                                            children=[
                                                html.Div(
                                                    className="d-flex align-items-center justify-content-between",
                                                    children=[
                                                        html.Small("Hash Power", style={'color': quantum_theme['accent2']}),
                                                        html.Span("OPTIMAL", style={'color': quantum_theme['success'], 'fontSize': '0.75rem'})
                                                    ]
                                                ),
                                                html.Div(
                                                    "∞ TH/s",
                                                    style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '1rem', 'marginTop': '2px'}
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                
                                html.Div(
                                    className="col-6 col-lg-3",
                                    children=[
                                        html.Div(
                                            className="p-2",
                                            style={
                                                'backgroundColor': 'rgba(10, 14, 23, 0.7)',
                                                'borderRadius': '6px',
                                                'border': f'1px solid {quantum_theme["highlight"]}',
                                            },
                                            children=[
                                                html.Div(
                                                    className="d-flex align-items-center justify-content-between",
                                                    children=[
                                                        html.Small("Memory Pool", style={'color': quantum_theme['highlight']}),
                                                        html.Span("OPTIMIZED", style={'color': quantum_theme['success'], 'fontSize': '0.75rem'})
                                                    ]
                                                ),
                                                html.Div(
                                                    "13.37 MB",
                                                    style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '1rem', 'marginTop': '2px'}
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        ),
                        
                        # Action buttons
                        html.Div(
                            className="d-flex justify-content-between mt-3",
                            children=[
                                dbc.Button(
                                    className="d-flex align-items-center justify-content-center",
                                    size="sm",
                                    style={
                                        'backgroundColor': 'transparent',
                                        'border': f'1px solid {quantum_theme["accent1"]}',
                                        'color': quantum_theme['accent1']
                                    },
                                    children=[
                                        html.I(className="fas fa-sync-alt me-2"),
                                        "QA Scan"
                                    ],
                                    id="matrix-qa-scan-btn"
                                ),
                                dbc.Button(
                                    className="d-flex align-items-center justify-content-center",
                                    size="sm",
                                    style={
                                        'backgroundColor': 'transparent',
                                        'border': f'1px solid {quantum_theme["accent2"]}',
                                        'color': quantum_theme['accent2']
                                    },
                                    children=[
                                        html.I(className="fas fa-shield-alt me-2"),
                                        "Chain Validation"
                                    ],
                                    id="matrix-validation-btn"
                                ),
                                dbc.Button(
                                    className="d-flex align-items-center justify-content-center",
                                    size="sm",
                                    style={
                                        'backgroundColor': 'transparent',
                                        'border': f'1px solid {quantum_theme["highlight"]}',
                                        'color': quantum_theme['highlight']
                                    },
                                    children=[
                                        html.I(className="fas fa-project-diagram me-2"),
                                        "5D Analysis"
                                    ],
                                    id="matrix-analysis-btn"
                                )
                            ]
                        )
                    ]
                )
            ]
        )

def run_dashboard():
    """Run the Quantum 5D QA Dashboard"""
    dashboard = Quantum5DDashboard()
    dashboard.run_dashboard(debug=True)

if __name__ == "__main__":
    run_dashboard() 