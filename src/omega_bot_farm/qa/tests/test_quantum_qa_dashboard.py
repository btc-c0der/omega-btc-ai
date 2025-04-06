#!/usr/bin/env python3
"""
Test suite for Quantum 5D QA Dashboard
--------------------------------------

This test suite provides comprehensive coverage for the Quantum 5D QA Dashboard,
focusing on the API endpoints, metrics calculation, and visualization functions.
"""

import os
import sys
import json
import unittest
import datetime
import tempfile
import time
import pandas as pd
import numpy as np
from unittest import mock
from pathlib import Path

# Add parent directory to path to allow imports to work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import the dashboard module
from quantum_qa_dashboard import (
    QuantumMetrics, 
    Quantum5DDashboard, 
    QUANTUM_DIMENSIONS,
    quantum_theme,
    DASHBOARD_CONFIG
)

# Testing configuration
TEST_DATA_DIR = os.path.join(current_dir, "test_data")
os.makedirs(TEST_DATA_DIR, exist_ok=True)


class TestQuantumMetrics(unittest.TestCase):
    """Test the QuantumMetrics class and its calculation methods."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create test reports directory
        self.test_reports_dir = os.path.join(TEST_DATA_DIR, "reports")
        os.makedirs(self.test_reports_dir, exist_ok=True)
        
        # Create test JSON reports
        self.latest_report_path = os.path.join(self.test_reports_dir, "latest.json")
        self.quantum_report_path = os.path.join(self.test_reports_dir, "quantum_test_report_20250405_085546.json")
        
        # Create a sample latest.json
        self.latest_report = {
            "id": "20250405_095428",
            "timestamp": "2025-04-05T09:54:28.761114",
            "trigger": "file_change",
            "source_files": [
                "/test/path/quantum_qa_dashboard.py"
            ],
            "results": {
                "UNIT": {
                    "dimension": "UNIT",
                    "state": "PASSED",
                    "duration": 1.021,
                    "timestamp": "2025-04-05T09:54:29.783093",
                    "details": {
                        "output": "coverage: 87.5%",
                        "error": "",
                        "returncode": 0,
                        "command": "pytest test_file.py",
                        "reports": {}
                    },
                    "entangled_dimensions": []
                },
                "INTEGRATION": {
                    "dimension": "INTEGRATION",
                    "state": "PASSED",
                    "duration": 0.845,
                    "timestamp": "2025-04-05T09:54:30.021",
                    "details": {
                        "output": "All integration tests passed",
                        "error": "",
                        "returncode": 0,
                        "command": "pytest integration_tests.py",
                        "reports": {}
                    },
                    "entangled_dimensions": []
                }
            },
            "state": "PASSED",
            "total_duration": 1.866
        }
        
        # Create a sample quantum report
        self.quantum_report = {
            "timestamp": "2025-04-05T08:55:47.352952",
            "total_tests": 30,
            "passed_tests": 27,
            "failed_tests": 3,
            "total_execution_time": 1.17,
            "results": {
                "unit": {
                    "success": True,
                    "output": "Unit tests passed: 24/27",
                    "error_output": "",
                    "execution_time": 0.337,
                    "returncode": 0
                },
                "integration": {
                    "success": False,
                    "output": "Integration tests failed: 2 failures\nAPI Error: connection refused",
                    "error_output": "",
                    "execution_time": 0.198,
                    "returncode": 1
                },
                "performance": {
                    "success": False,
                    "output": "Performance tests failed: 1 error\nCPU Usage: 32%\nMemory: 45%",
                    "error_output": "",
                    "execution_time": 0.635,
                    "returncode": 1
                }
            }
        }
        
        # Write the test reports to files
        with open(self.latest_report_path, 'w') as f:
            json.dump(self.latest_report, f)
            
        with open(self.quantum_report_path, 'w') as f:
            json.dump(self.quantum_report, f)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up test files
        if os.path.exists(self.latest_report_path):
            os.remove(self.latest_report_path)
            
        if os.path.exists(self.quantum_report_path):
            os.remove(self.quantum_report_path)
            
    def test_quantum_metrics_init(self):
        """Test initialization of QuantumMetrics."""
        metrics = QuantumMetrics()
        
        # Check default values
        self.assertEqual(metrics.coverage_score, 0.0)
        self.assertEqual(metrics.success_score, 0.0)
        self.assertEqual(metrics.performance_score, 0.0)
        self.assertEqual(metrics.security_score, 0.0)
        self.assertEqual(metrics.api_score, 0.0)
        
        # Check 5D dimensions
        self.assertEqual(len(metrics.hyperspatial_trend), 5)
        
    def test_calculate_quantum_dimensions(self):
        """Test calculation of quantum dimensions."""
        metrics = QuantumMetrics()
        
        # Set some values
        metrics.coverage_score = 85.0
        metrics.success_score = 90.0
        metrics.performance_score = 75.0
        metrics.security_score = 95.0
        metrics.api_score = 88.0
        
        # Calculate dimensions
        metrics._calculate_quantum_dimensions()
        
        # Check dimension positions
        self.assertEqual(metrics.coverage_position, 85.0)
        self.assertEqual(metrics.quality_position, 90.0 * 0.7 + 88.0 * 0.3)
        self.assertEqual(metrics.performance_position, 75.0)
        self.assertEqual(metrics.security_position, 95.0)
        
        # Check quantum metrics
        self.assertGreater(metrics.dimensional_stability, 0)
        self.assertLessEqual(metrics.dimensional_stability, 100)
        self.assertGreaterEqual(metrics.entanglement_factor, 0)
        self.assertLessEqual(metrics.entanglement_factor, 1)
        
    def test_from_qa_metrics(self):
        """Test creation of QuantumMetrics from QAMetrics."""
        # Create a mock QAMetrics instance
        qa_metrics = mock.MagicMock()
        qa_metrics.coverage.total_coverage = 80.0
        qa_metrics.tests.total_tests = 100
        qa_metrics.tests.passed = 95
        qa_metrics.performance.cpu_percent = 30.0
        qa_metrics.performance.memory_usage = 40.0
        qa_metrics.performance.disk_usage = 25.0
        qa_metrics.security.firewall_active = True
        qa_metrics.security.discord_token_secure = True
        qa_metrics.security.api_keys_secure = True
        qa_metrics.security.ssl_certificates = {"site_cert": {"verified": True}}
        qa_metrics.api.availability = {"main_api": 98.0, "backup_api": 99.0}
        
        # Create metrics from QAMetrics
        metrics = QuantumMetrics.from_qa_metrics(qa_metrics)
        
        # Check values
        self.assertEqual(metrics.coverage_score, 80.0)
        self.assertEqual(metrics.success_score, 95.0)
        self.assertAlmostEqual(metrics.performance_score, (70.0 + 60.0 + 75.0) / 3, places=1)
        self.assertEqual(metrics.security_score, 100.0)
        self.assertEqual(metrics.api_score, 98.5)
        
    def test_from_test_reports(self):
        """Test creation of QuantumMetrics from test reports."""
        # Mock the current_dir in quantum_qa_dashboard to use our test directory
        with mock.patch('quantum_qa_dashboard.current_dir', self.test_reports_dir):
            metrics = QuantumMetrics.from_test_reports()
            
            # Check that metrics were extracted correctly
            self.assertGreater(metrics.success_score, 0)
            self.assertLessEqual(metrics.success_score, 100)
            self.assertGreater(metrics.coverage_score, 0)
            self.assertLessEqual(metrics.coverage_score, 100)
            
            # Since we're using controlled test data:
            self.assertEqual(metrics.security_score, 95.0)  # Default for passing security tests
            
    def test_missing_test_reports(self):
        """Test fallback when test reports aren't found."""
        # Create a temp directory with no reports
        with tempfile.TemporaryDirectory() as temp_dir:
            # Mock the current_dir to use our empty temp directory
            with mock.patch('quantum_qa_dashboard.current_dir', temp_dir):
                metrics = QuantumMetrics.from_test_reports()
                
                # Should use fallback values
                self.assertEqual(metrics.coverage_score, 75.0)
                self.assertEqual(metrics.success_score, 80.0)
                
    def test_to_dict(self):
        """Test conversion of QuantumMetrics to dictionary."""
        metrics = QuantumMetrics()
        metrics_dict = metrics.to_dict()
        
        # Check dictionary keys
        self.assertIn('coverage_score', metrics_dict)
        self.assertIn('success_score', metrics_dict)
        self.assertIn('performance_score', metrics_dict)
        self.assertIn('security_score', metrics_dict)
        self.assertIn('api_score', metrics_dict)
        self.assertIn('dimensional_stability', metrics_dict)
        self.assertIn('hyperspatial_trend', metrics_dict)


class TestQuantum5DDashboard(unittest.TestCase):
    """Test the Quantum5DDashboard class and its visualization functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock dashboard initialization to avoid starting threads
        with mock.patch('quantum_qa_dashboard.Quantum5DDashboard.start_metrics_collection'):
            self.dashboard = Quantum5DDashboard()
            
        # Create sample metrics for testing
        self.sample_metrics = QuantumMetrics()
        self.sample_metrics.coverage_score = 85.0
        self.sample_metrics.success_score = 90.0
        self.sample_metrics.performance_score = 75.0
        self.sample_metrics.security_score = 95.0
        self.sample_metrics.api_score = 88.0
        self.sample_metrics._calculate_quantum_dimensions()
        
    def tearDown(self):
        """Clean up test fixtures."""
        # Stop metrics collection thread if running
        self.dashboard.stop_metrics_collection()
        
    def test_dashboard_initialization(self):
        """Test dashboard initialization."""
        self.assertIsNotNone(self.dashboard.app)
        self.assertIsNotNone(self.dashboard.git_manager)
        self.assertIsNone(self.dashboard.current_metrics)
        self.assertEqual(len(self.dashboard.metrics_history), 0)
        
    def test_collect_metrics(self):
        """Test metrics collection."""
        # Mock the from_test_reports method
        with mock.patch('quantum_qa_dashboard.QuantumMetrics.from_test_reports', 
                        return_value=self.sample_metrics):
            metrics = self.dashboard.collect_metrics()
            
            self.assertEqual(metrics.coverage_score, 85.0)
            self.assertEqual(metrics.success_score, 90.0)
            self.assertEqual(metrics.performance_score, 75.0)
            
    def test_fallback_metrics_collection(self):
        """Test fallback metrics collection."""
        # Mock from_test_reports to raise exception and collect_and_save_metrics to succeed
        with mock.patch('quantum_qa_dashboard.QuantumMetrics.from_test_reports', 
                        side_effect=Exception("Test error")):
            with mock.patch('quantum_qa_dashboard.collect_and_save_metrics', 
                            return_value=mock.MagicMock()):
                metrics = self.dashboard.collect_metrics()
                
                # Should have default values from fallback
                self.assertGreater(metrics.coverage_score, 0)
                
    def test_metrics_collection_loop(self):
        """Test the metrics collection background loop."""
        # Mock collect_metrics to count calls
        self.dashboard.collect_metrics = mock.MagicMock(return_value=self.sample_metrics)
        
        # Start metrics collection
        self.dashboard.start_metrics_collection()
        
        # Wait a bit for the thread to run
        time.sleep(0.1)
        
        # Stop the thread
        self.dashboard.stop_metrics_collection()
        
        # Check that collect_metrics was called
        self.dashboard.collect_metrics.assert_called()
        
    def test_create_dimension_graph(self):
        """Test creation of dimension graphs."""
        # Test each dimension
        for dimension in ["quality", "coverage", "performance", "security"]:
            # Create dimension data
            metrics_history = []
            for i in range(10):
                metrics = QuantumMetrics()
                setattr(metrics, f"{dimension}_score", 75.0 + i)
                metrics.timestamp = (datetime.datetime.now() - 
                                     datetime.timedelta(minutes=i)).isoformat()
                metrics_history.append(metrics)
                
            # Create graph
            fig = self.dashboard._create_dimension_graph(metrics_history, dimension)
            
            # Check that figure was created
            self.assertIsNotNone(fig)
            
    def test_create_dashboard_metrics(self):
        """Test creation of dashboard metrics."""
        # Set current metrics
        self.dashboard.current_metrics = self.sample_metrics
        
        # Get metrics display
        metrics_display = self.dashboard._create_dashboard_metrics()
        
        # Check that metrics were created
        self.assertIsNotNone(metrics_display)
        self.assertIn("coverage_score", metrics_display)
        self.assertIn("success_score", metrics_display)
        self.assertIn("performance_score", metrics_display)
        self.assertIn("security_score", metrics_display)
        
    def test_create_entanglement_web(self):
        """Test creation of entanglement web visualization."""
        # Create web
        fig = self.dashboard._create_entanglement_web(
            self.sample_metrics.to_dict(),
            {"frame": 0}
        )
        
        # Check that figure was created
        self.assertIsNotNone(fig)
        
    def test_create_hypercube_visualization(self):
        """Test creation of hypercube visualization."""
        # Create visualization
        fig = self.dashboard._create_hypercube_visualization(
            self.sample_metrics.to_dict(),
            {"frame": 0}
        )
        
        # Check that figure was created
        self.assertIsNotNone(fig)
        
    def test_format_git_data_for_display(self):
        """Test formatting git data for display."""
        # Create sample git report
        git_report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'file_counts': {
                'total': 5,
                'modified': 2,
                'added': 1,
                'deleted': 1,
                'untracked': 1
            },
            'by_extension': {},
            'by_directory': {},
            'files': {
                'modified': ['file1.py', 'file2.py'],
                'added': ['file3.py'],
                'deleted': ['file4.py'],
                'untracked': ['file5.py']
            },
            'suggestions': {
                'commit_message': "Test commit message",
                'tag': "v1.0.0-test"
            }
        }
        
        # Format data
        result = self.dashboard._format_git_data_for_display(git_report)
        
        # Check result
        self.assertEqual(result[0], git_report)  # Store data
        self.assertEqual(result[1], "5")  # Total files
        self.assertEqual(result[2], "2")  # Modified files
        self.assertEqual(result[3], "2")  # Added files
        self.assertEqual(result[4], "1")  # Deleted files
        self.assertIsInstance(result[5], list)  # Files list
        self.assertEqual(len(result[5]), 5)  # 5 files in list


class TestDashboardAPIEndpoints(unittest.TestCase):
    """Test the dashboard API endpoints and callbacks."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock dashboard initialization to avoid starting threads
        with mock.patch('quantum_qa_dashboard.Quantum5DDashboard.start_metrics_collection'):
            self.dashboard = Quantum5DDashboard()
            
        # Create sample metrics for testing
        self.sample_metrics = QuantumMetrics()
        self.sample_metrics.coverage_score = 85.0
        self.sample_metrics.success_score = 90.0
        self.sample_metrics.performance_score = 75.0
        self.sample_metrics.security_score = 95.0
        self.sample_metrics.api_score = 88.0
        self.sample_metrics._calculate_quantum_dimensions()
        
        # Set current metrics
        self.dashboard.current_metrics = self.sample_metrics
        self.dashboard.metrics_history = [self.sample_metrics]
        self.dashboard.last_metrics_update = datetime.datetime.now()
        
    def test_update_dimensional_metrics_callback(self):
        """Test callback for updating dimensional metrics."""
        # Get the callback function
        update_callback = None
        for callback in self.dashboard.app.callback_map.values():
            if 'coverage-graph' in str(callback.outputs):
                update_callback = callback.callback
                break
        
        self.assertIsNotNone(update_callback)
        
        # This would normally be tested with dash.testing, but for simplicity
        # we'll call the callback function directly with dummy input
        n_intervals = 1
        with mock.patch('dash.callback_context') as mock_ctx:
            mock_ctx.triggered_id = 'interval-component'
            
            # Call the callback
            coverage_fig, quality_fig, performance_fig, security_fig = update_callback(n_intervals)
            
            # Check that figures were created
            self.assertIsNotNone(coverage_fig)
            self.assertIsNotNone(quality_fig)
            self.assertIsNotNone(performance_fig)
            self.assertIsNotNone(security_fig)
    
    def test_update_dashboard_metrics_callback(self):
        """Test callback for updating dashboard metrics."""
        # Get the callback function
        update_callback = None
        for callback in self.dashboard.app.callback_map.values():
            if 'dashboard-metrics' in str(callback.outputs):
                update_callback = callback.callback
                break
        
        self.assertIsNotNone(update_callback)
        
        # Call the callback
        n_intervals = 1
        with mock.patch('dash.callback_context') as mock_ctx:
            mock_ctx.triggered_id = 'interval-component'
            
            # Call the callback
            metrics = update_callback(n_intervals)
            
            # Check metrics
            self.assertIsNotNone(metrics)
            self.assertIn("coverage_score", metrics)
            self.assertEqual(metrics["coverage_score"]["value"], "85.0%")
    
    def test_update_quantum_visualizations_callback(self):
        """Test callback for updating quantum visualizations."""
        # Get the callback function
        update_callback = None
        for callback in self.dashboard.app.callback_map.values():
            if 'entanglement-web' in str(callback.outputs):
                update_callback = callback.callback
                break
        
        self.assertIsNotNone(update_callback)
        
        # Call the callback
        n_intervals = 1
        with mock.patch('dash.callback_context') as mock_ctx:
            mock_ctx.triggered_id = 'interval-component'
            
            # Call the callback
            web_fig, hypercube_fig = update_callback(n_intervals)
            
            # Check figures
            self.assertIsNotNone(web_fig)
            self.assertIsNotNone(hypercube_fig)
    
    def test_update_git_info_callback(self):
        """Test callback for updating git information."""
        # Mock git manager
        self.dashboard.git_manager.get_uncommitted_report = mock.MagicMock(
            return_value={
                'timestamp': datetime.datetime.now().isoformat(),
                'file_counts': {
                    'total': 3,
                    'modified': 1,
                    'added': 1,
                    'deleted': 1,
                    'untracked': 0
                },
                'by_extension': {},
                'by_directory': {},
                'files': {
                    'modified': ['file1.py'],
                    'added': ['file2.py'],
                    'deleted': ['file3.py'],
                    'untracked': []
                },
                'suggestions': {
                    'commit_message': "Test commit message",
                    'tag': "v1.0.0-test"
                }
            }
        )
        
        # Get the callback function
        update_callback = None
        for callback in self.dashboard.app.callback_map.values():
            if 'git-total-files' in str(callback.outputs):
                update_callback = callback.callback
                break
        
        self.assertIsNotNone(update_callback)
        
        # Call the callback
        n_intervals = 1
        btn_clicks = 1
        with mock.patch('dash.callback_context') as mock_ctx:
            mock_ctx.triggered_id = 'refresh-git-btn'
            
            # Call the callback
            result = update_callback(n_intervals, btn_clicks)
            
            # Check result
            self.assertIsNotNone(result[0])  # Store data
            self.assertEqual(result[1], "3")  # Total files
            self.assertEqual(result[2], "1")  # Modified files
            self.assertEqual(result[3], "1")  # Added files
            self.assertEqual(result[4], "1")  # Deleted files
            self.assertIsInstance(result[5], list)  # Files list


if __name__ == "__main__":
    unittest.main() 