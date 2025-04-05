#!/usr/bin/env python3
"""
0M3G4 B0TS QA AUT0 TEST SUITES RuNn3R 5D - Quantum Test Service
--------------------------------------------------------------

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

This module provides the main service class for the Quantum Test Runner.
"""

import os
import sys
import time
import logging
import queue
from typing import Dict, List, Any, Optional, Set

from .types import TestDimension, Colors
from .test_runner import TestRunner
from .test_scheduler import TestScheduler
from .file_monitor import FileChangeHandler
from .git_manager import GitManager
from .gbu2_license import GBU2LicenseChecker
from .k8s_surveillance import K8sMatrixSurveillance
from .utils import log_with_formatting, print_section_header, print_enhanced_header

logger = logging.getLogger(__name__)

class QuantumTestService:
    """
    Main service class for the Quantum Test Runner.
    Orchestrates test running, file monitoring, git integration, and more.
    """
    
    def __init__(self, project_root: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Quantum Test Service.
        
        Args:
            project_root: The root directory of the project
            config: Optional configuration dictionary
        """
        self.project_root = os.path.abspath(project_root)
        self.config = config or {}
        
        # Initialize report directory
        self.report_dir = os.path.join(
            self.project_root, 
            self.config.get('report_dir', 'qa/reports')
        )
        os.makedirs(self.report_dir, exist_ok=True)
        
        # Initialize components
        self.test_runner = TestRunner(self.project_root, self.report_dir)
        
        # Create a queue for scheduling events
        self.event_queue = queue.Queue()
        
        # Default schedule - run tests at different intervals
        self.schedule = {
            'unit': 3600,         # Every hour
            'integration': 7200,  # Every 2 hours
            'performance': 14400, # Every 4 hours
            'security': 86400,    # Daily
            'full': 604800        # Weekly
        }
        
        # Override schedule from config if provided
        if 'test_schedule' in self.config:
            self.schedule.update(self.config.get('test_schedule', {}))
        
        # Initialize test scheduler
        self.test_scheduler = TestScheduler(self.event_queue, self.schedule)
        
        # Set up file monitoring
        self.watched_extensions = {'.py', '.js', '.ts', '.sh', '.yaml', '.yml', '.md'}
        self.ignored_dirs = {'.git', 'venv', '__pycache__', 'node_modules', '.pytest_cache'}
        self.test_map = {
            'test_': [TestDimension.UNIT],
            'integration': [TestDimension.INTEGRATION],
            'performance': [TestDimension.PERFORMANCE],
            'security': [TestDimension.SECURITY],
            'benchmark': [TestDimension.PERFORMANCE],
            'docker': [TestDimension.INTEGRATION, TestDimension.COMPLIANCE],
            'k8s': [TestDimension.COMPLIANCE]
        }
        
        # Initialize file monitor
        self.file_change_handler = FileChangeHandler(
            self.event_queue, 
            self.watched_extensions,
            self.ignored_dirs,
            self.test_map
        )
        
        # Other components
        self.git_manager = GitManager(self.project_root)
        self.license_checker = GBU2LicenseChecker(self.project_root)
        
        # Initialize K8s surveillance if enabled
        self.k8s_surveillance = None
        if self.config.get('k8s_matrix_mode', False):
            self.k8s_surveillance = K8sMatrixSurveillance(
                namespace=self.config.get('k8s_namespace')
            )
        
        # Print initialization message
        self._print_initialization_message()
    
    def _print_initialization_message(self):
        """Print an initialization message."""
        full_mode = self.config.get('full_omega_mode', False)
        mode_text = "FULL OMEGA MODE" if full_mode else "STANDARD MODE"
        
        print_enhanced_header(f"0M3G4 B0TS QA AUT0 TEST SUITES RuNn3R 5D", mode_text)
        log_with_formatting(f"Initialized on project root: {self.project_root}", logging.INFO, Colors.BLUE)
        log_with_formatting(f"Reports will be saved to: {self.report_dir}", logging.INFO, Colors.BLUE)
    
    def start(self):
        """Start the service with continuous monitoring."""
        try:
            # Run initial tests if configured
            if self.config.get('run_initial_tests', False):
                self.run_quantum_test_suite(None)  # Run all dimensions
            
            # Set up monitoring intervals
            uncommitted_interval = self.config.get('uncommitted_scan_interval', 300)
            git_suggestion_interval = self.config.get('git_suggestion_interval', 600)
            file_scan_interval = self.config.get('new_file_scan_interval', 60)
            k8s_report_interval = self.config.get('k8s_report_interval', 600)
            
            # Start the scheduler
            self.test_scheduler.start()
            
            # Start file monitoring if enabled
            if self.config.get('auto_listen', False):
                from watchdog.observers import Observer
                self.observer = Observer()
                self.observer.schedule(self.file_change_handler, self.project_root, recursive=True)
                self.observer.start()
                log_with_formatting("File monitoring started", logging.INFO, Colors.GREEN)
                
                # Show what we're watching
                extensions_str = ", ".join(sorted(self.watched_extensions))
                log_with_formatting(f"Watching file types: {extensions_str}", logging.INFO, Colors.CYAN)
                log_with_formatting(f"Monitoring directory: {self.project_root}", logging.INFO, Colors.CYAN)
                log_with_formatting(f"Ignoring directories: {', '.join(sorted(self.ignored_dirs))}", logging.INFO, Colors.YELLOW)
                
                # Force-print the initial status
                self._last_status_print = 0
            
            # Main service loop
            last_uncommitted_check = 0
            last_git_suggestion = 0
            last_k8s_report = 0
            
            print_enhanced_header("QUANTUM SERVICE RUNNING", "PRESS CTRL+C TO EXIT")
            
            while True:
                now = time.time()
                
                # Process any events in the queue (with non-blocking get)
                try:
                    # Try to get an event with a short timeout
                    event = self.event_queue.get(block=True, timeout=0.1)
                    # Process the event
                    self._process_event(event)
                    # Mark task as done
                    self.event_queue.task_done()
                except queue.Empty:
                    # No events to process, continue with other tasks
                    pass
                
                # Check for uncommitted files
                if (self.config.get('report_uncommitted', False) and 
                        now - last_uncommitted_check >= uncommitted_interval):
                    self.report_uncommitted_files()
                    last_uncommitted_check = now
                
                # Generate git suggestions
                if (self.config.get('suggest_git', False) and 
                        now - last_git_suggestion >= git_suggestion_interval):
                    self.suggest_git_commit()
                    self.suggest_git_tag()
                    last_git_suggestion = now
                
                # Generate K8s matrix report with timeout
                if (self.k8s_surveillance and self.k8s_surveillance.available and
                        now - last_k8s_report >= k8s_report_interval):
                    # Use a timeout for the K8s report to prevent it from blocking
                    try:
                        import threading
                        
                        def run_k8s_report():
                            if self.k8s_surveillance:  # Add null check
                                self.k8s_surveillance.print_matrix_report()
                        
                        k8s_thread = threading.Thread(target=run_k8s_report)
                        k8s_thread.daemon = True
                        k8s_thread.start()
                        
                        # Wait with a timeout
                        k8s_thread.join(timeout=15)
                        
                        # If the thread is still alive after timeout, log a warning
                        if k8s_thread.is_alive():
                            log_with_formatting("K8s Matrix report timed out - continuing operation", logging.WARNING)
                    except Exception as e:
                        log_with_formatting(f"Error generating K8s Matrix report: {e}", logging.ERROR)
                    
                    last_k8s_report = now
                
                # Print monitoring status
                self._print_monitoring_status()
                
                # Sleep to prevent CPU overuse
                time.sleep(1)
                
        except KeyboardInterrupt:
            # Handle graceful shutdown using the stop method
            self.stop()
    
    def run_quantum_test_suite(self, dimensions: Optional[List[str]] = None):
        """
        Run tests in the specified dimensions.
        
        Args:
            dimensions: List of test dimensions to run. If None, run all dimensions.
        """
        if dimensions is None:
            # Run all dimensions
            dimensions = [d.name for d in TestDimension]
        
        print_enhanced_header(f"RUNNING TESTS IN DIMENSIONS", f"{', '.join(dimensions)}")
        
        for dimension in dimensions:
            try:
                test_dim = TestDimension[dimension]
                self.test_runner.run_tests([test_dim])
            except KeyError:
                log_with_formatting(f"Invalid test dimension: {dimension}", logging.ERROR, Colors.RED)
    
    def report_uncommitted_files(self):
        """Report uncommitted files in the repository."""
        report = self.git_manager.get_uncommitted_report()
        
        if report['total_count'] == 0:
            log_with_formatting("No uncommitted files found", logging.INFO, Colors.GREEN)
            return
        
        print_enhanced_header("UNCOMMITTED FILES REPORT", None)
        log_with_formatting(f"Found {report['total_count']} uncommitted files", logging.WARNING, Colors.YELLOW)
        
        # Print details by category using the 'categories' field from the report
        categories = {
            'modified': ('MODIFIED', Colors.BLUE),
            'added': ('ADDED', Colors.GREEN),
            'deleted': ('DELETED', Colors.RED),
            'untracked': ('UNTRACKED', Colors.YELLOW)
        }
        
        for status, (label, color) in categories.items():
            count = report['categories'][status]
            if count > 0:
                log_with_formatting(f"{label}: {count} files", logging.INFO, color)
                
                # Get files with this status
                files_with_status = [f['path'] for f in report['files'] if f['status'] == status][:5]
                for file_path in files_with_status:
                    print(f"  - {color}{file_path}{Colors.ENDC}")
                if len(files_with_status) > 5:
                    print(f"  ... and {len(files_with_status) - 5} more")
    
    def suggest_git_commit(self):
        """Suggest a Git commit message based on uncommitted changes."""
        message = self.git_manager.get_enhanced_commit_analysis()
        if message:
            print_enhanced_header("SUGGESTED GIT COMMIT", None)
            log_with_formatting(f"Suggested commit message:", logging.INFO, Colors.CYAN)
            print(f"\n{Colors.GREEN}{message}{Colors.ENDC}\n")
    
    def suggest_git_tag(self):
        """Suggest a Git tag based on the current state."""
        tag = self.git_manager.suggest_git_tag()
        if tag:
            log_with_formatting(f"Suggested Git tag: {tag}", logging.INFO, Colors.YELLOW)
    
    def check_gbu2_license_compliance(self):
        """Check GBU2 License compliance for the project."""
        print_enhanced_header("GBU2 LICENSE COMPLIANCE CHECK", None)
        
        report = self.license_checker.check_directory(self.project_root, recursive=True)
        compliance_rate = report["compliance_rate"] * 100
        
        log_with_formatting(f"Project compliance rate: {compliance_rate:.1f}%", logging.INFO, Colors.CYAN)
        log_with_formatting(f"Files checked: {report['files_checked']}", logging.INFO, Colors.BLUE)
        log_with_formatting(f"Files with license: {report['files_with_license']}", logging.INFO, Colors.GREEN)
        
        return report
    
    def apply_gbu2_license(self, target_path: str, recursive: bool = False):
        """
        Apply GBU2 License to a file or directory.
        
        Args:
            target_path: Path to the file or directory
            recursive: Whether to apply recursively to directories
            
        Returns:
            Dict containing results of the operation
        """
        print_enhanced_header(f"APPLYING GBU2 LICENSE", f"TARGET: {target_path}")
        
        abs_path = os.path.join(self.project_root, target_path)
        if not os.path.exists(abs_path):
            log_with_formatting(f"Path does not exist: {abs_path}", logging.ERROR, Colors.RED)
            return {"error": "Path does not exist", "files_updated": 0}
        
        if os.path.isfile(abs_path):
            # Apply to a single file
            success = self.license_checker.apply_license_to_file(abs_path)
            files_updated = 1 if success else 0
            return {"files_updated": files_updated}
        elif os.path.isdir(abs_path):
            # Apply to a directory
            results = self.license_checker.apply_license_to_dir(abs_path, recursive)
            log_with_formatting(f"Updated {results['files_updated']} files", logging.INFO, Colors.GREEN)
            return results
        else:
            log_with_formatting(f"Unknown path type: {abs_path}", logging.ERROR, Colors.RED)
            return {"error": "Unknown path type", "files_updated": 0}

    def stop(self):
        """Stop the service and clean up resources."""
        print_enhanced_header("SHUTTING DOWN QUANTUM SERVICE", None)
        
        # Stop scheduler
        if hasattr(self, 'test_scheduler'):
            self.test_scheduler.stop()
        
        # Stop file monitoring
        if hasattr(self, 'observer') and self.observer.is_alive():
            self.observer.stop()
            self.observer.join()
            log_with_formatting("File monitoring stopped", logging.INFO, Colors.YELLOW)
        
        log_with_formatting("Quantum Test Service has been stopped", logging.INFO, Colors.CYAN)

    def _process_event(self, event):
        """Process an event from the queue.
        
        Events can be:
          - (file_path, [dimensions]) - Run tests in specified dimensions due to file change
          - ("scan", path) - Scan a path for files
          - Other events from the scheduler
        
        Args:
            event: The event to process
        """
        try:
            if not event:
                return
                
            # Unpack the event
            if isinstance(event, tuple) and len(event) == 2:
                source, data = event
                
                # Case 1: File change event
                if isinstance(source, str) and isinstance(data, list):
                    if os.path.exists(source):
                        # This is a file change event
                        # Convert TestDimension enum instances to strings
                        dimension_names = [dim.name for dim in data]
                        
                        print_enhanced_header("FILE CHANGE DETECTED", os.path.basename(source))
                        log_with_formatting(f"Path: {source}", logging.INFO, Colors.CYAN)
                        log_with_formatting(f"Running tests: {', '.join(dimension_names)}", 
                                        logging.INFO, Colors.GREEN)
                        
                        # Run the tests
                        self.run_quantum_test_suite(dimension_names)
                elif source is None and isinstance(data, list):
                    # This is a scheduled test
                    dimension_names = [dim.name for dim in data]
                    print_enhanced_header("SCHEDULED TEST", ", ".join(dimension_names))
                    self.run_quantum_test_suite(dimension_names)
                else:
                    log_with_formatting(f"Unknown event type: {event}", logging.WARNING, Colors.YELLOW)
            else:
                log_with_formatting(f"Malformed event: {event}", logging.WARNING, Colors.YELLOW)
        except Exception as e:
            log_with_formatting(f"Error processing event: {e}", logging.ERROR, Colors.RED)

    def _print_monitoring_status(self, force=False):
        """Periodically print monitoring status to show the system is active.
        
        Args:
            force: If True, print status regardless of interval
        """
        now = time.time()
        
        # Only print status every 1 minute by default
        if not hasattr(self, '_last_status_print'):
            self._last_status_print = 0
            
        if force or now - self._last_status_print >= 60:  # 1 minute
            print_enhanced_header("QUANTUM MONITORING STATUS", "ACTIVE")
            
            monitoring_details = []
            
            if hasattr(self, 'observer') and self.observer.is_alive():
                monitoring_details.append(f"{Colors.CYAN}🔍 File monitoring: {Colors.GREEN}ACTIVE{Colors.ENDC}")
                monitoring_details.append(f"   {Colors.CYAN}Watching {len(self.watched_extensions)} file types across {self.project_root}{Colors.ENDC}")
            else:
                monitoring_details.append(f"{Colors.CYAN}🔍 File monitoring: {Colors.RED}INACTIVE{Colors.ENDC}")
                
            if self.test_scheduler.running:
                monitoring_details.append(f"{Colors.YELLOW}⏱ Test scheduler: {Colors.GREEN}ACTIVE{Colors.ENDC}")
                # Show next scheduled tests
                for test_type, interval in self.schedule.items():
                    next_run = self.test_scheduler.last_run.get(test_type, 0) + interval
                    time_left = max(0, next_run - now)
                    monitoring_details.append(f"   {Colors.YELLOW}{test_type.upper()} tests: {Colors.GREEN}next in {int(time_left)} seconds{Colors.ENDC}")
            else:
                monitoring_details.append(f"{Colors.YELLOW}⏱ Test scheduler: {Colors.RED}INACTIVE{Colors.ENDC}")
                
            if self.k8s_surveillance and self.k8s_surveillance.available:
                monitoring_details.append(f"{Colors.BLUE}🔷 K8s Matrix: {Colors.GREEN}ACTIVE{Colors.ENDC}")
            elif self.k8s_surveillance:
                monitoring_details.append(f"{Colors.BLUE}🔷 K8s Matrix: {Colors.RED}NOT AVAILABLE{Colors.ENDC}")
                
            # Print all details
            for detail in monitoring_details:
                print(detail)
                
            self._last_status_print = now 