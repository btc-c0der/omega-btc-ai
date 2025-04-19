#!/usr/bin/env python3
"""
Quantum Test Runner V2
----------------------

This is the main orchestrator that coordinates all microservices:
- Git Status Monitoring (3-minute refresh)
- File Backup System 
- Code Metrics and Refactoring Analysis
- Test Discovery and Execution

This runner implements a modern microservices architecture with each
component operating independently but communicating through a shared
event system.
"""

import os
import sys
import time
import logging
import argparse
import signal
import json
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Callable, Union
from datetime import datetime

# Add parent directory to path for local imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import microservices - using relative imports
from .services.git_service import GitStatusMonitor, GitCommitSuggester
from .services.backup_service import BackupService
from .services.code_metrics_service import CodeMetricsCollector
from .services.ipfs_service import IPFSService
from .services.nft_qa_service import NFTQAService
from .services import ipfs_pinata_integration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(__file__), "quantum_runner_v2.log"))
    ]
)

logger = logging.getLogger("quantum_runner_v2")


class EventBus:
    """Simple event bus for inter-service communication."""
    
    def __init__(self):
        """Initialize the event bus."""
        self.subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()
    
    def subscribe(self, event_type: str, callback: Callable):
        """
        Subscribe to an event.
        
        Args:
            event_type: Type of event to subscribe to
            callback: Function to call when event occurs
        """
        with self._lock:
            if event_type not in self.subscribers:
                self.subscribers[event_type] = []
            self.subscribers[event_type].append(callback)
    
    def publish(self, event_type: str, data: Any = None):
        """
        Publish an event.
        
        Args:
            event_type: Type of event to publish
            data: Data to include with the event
        """
        with self._lock:
            if event_type in self.subscribers:
                for callback in self.subscribers[event_type]:
                    try:
                        callback(data)
                    except Exception as e:
                        logger.error(f"Error in event subscriber: {e}")


class QuantumRunnerV2:
    """Main orchestrator for the Quantum Test Runner V2."""
    
    def __init__(
        self, 
        project_root: Optional[Union[str, Path]] = None,
        enable_ipfs: bool = False,
        enable_nft: bool = False
    ):
        """
        Initialize the Quantum Test Runner.
        
        Args:
            project_root: Path to the project root directory
            enable_ipfs: Whether to enable IPFS integration
            enable_nft: Whether to enable NFT QA certification
        """
        # Determine project root if not provided
        if project_root is None:
            # Get the absolute path of the current file
            current_file = Path(__file__).resolve()
            
            # Navigate up to the project root (assumed to be 4 levels up from this file)
            project_root = current_file.parents[3]
        
        self.project_root = Path(project_root).resolve()
        logger.info(f"Project root: {self.project_root}")
        
        # Initialize event bus
        self.event_bus = EventBus()
        
        # Initialize quantum directory for runner data
        self.quantum_dir = self.project_root / ".quantum"
        self.quantum_dir.mkdir(exist_ok=True)
        
        # Save configuration options
        self.enable_ipfs = enable_ipfs
        self.enable_nft = enable_nft
        
        # Initialize services
        self.services = {}
        self._initialize_services()
        
        # Flag for controlled shutdown
        self.running = False
    
    def _initialize_services(self):
        """Initialize all microservices."""
        # Git status monitoring service
        self.services["git"] = GitStatusMonitor(str(self.project_root), refresh_interval=180)
        
        # Backup service
        self.services["backup"] = BackupService(str(self.project_root))
        
        # Code metrics service
        self.services["metrics"] = CodeMetricsCollector(str(self.project_root))
        
        # Initialize IPFS service if enabled
        if self.enable_ipfs:
            self.services["ipfs"] = IPFSService()
            
            # Initialize NFT service if both IPFS and NFT are enabled
            if self.enable_nft:
                self.services["nft"] = NFTQAService(ipfs_service=self.services["ipfs"])
        
        # Setup event subscriptions
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """Setup event handlers between services."""
        # When git status changes, trigger backups
        self.event_bus.subscribe("git_status_changed", self._handle_git_status_change)
        
        # When code metrics finds large files, log warnings
        self.event_bus.subscribe("large_file_detected", self._handle_large_file)
        
        # When backup is created, log it
        self.event_bus.subscribe("backup_created", self._handle_backup_created)
        
        # When test results are available, publish to IPFS if enabled
        if self.enable_ipfs:
            self.event_bus.subscribe("test_results_available", self._handle_test_results)
            
        # When IPFS upload completes, create NFT certification if enabled
        if self.enable_ipfs and self.enable_nft:
            self.event_bus.subscribe("ipfs_upload_complete", self._handle_ipfs_upload)
    
    def _handle_git_status_change(self, status: Dict[str, Any]):
        """
        Handle git status change event.
        
        Args:
            status: Git status data
        """
        logger.info(f"Git status changed: {len(status.get('modified_files', []))} modified files")
        
        # Add changed files to backup service watch list
        for file_path in status.get("modified_files", []):
            if file_path.endswith(".py"):
                self.services["backup"].watch_file(file_path)
    
    def _handle_large_file(self, file_info: Dict[str, Any]):
        """
        Handle large file detection event.
        
        Args:
            file_info: Information about the large file
        """
        logger.warning(
            f"⚠️ REFACTORING ALERT: File {file_info['path']} has {file_info['size']} lines "
            f"(exceeds recommended 420) - See refactoring suggestions in metrics report"
        )
    
    def _handle_backup_created(self, backup_info: Dict[str, Any]):
        """
        Handle backup created event.
        
        Args:
            backup_info: Information about the created backup
        """
        logger.info(f"Created backup: {backup_info['path']} with {backup_info['file_count']} files")
    
    def _handle_test_results(self, results: Dict[str, Any]):
        """
        Handle test results available event.
        
        Args:
            results: Test results data with paths to reports
        """
        if not self.enable_ipfs:
            return
            
        ipfs_service = self.services.get("ipfs")
        if not ipfs_service:
            logger.warning("IPFS service not available")
            return
            
        # Get report paths
        report_path = results.get("report_path")
        if not report_path:
            logger.warning("No report path in test results")
            return
            
        # Upload to IPFS
        logger.info(f"Uploading test report to IPFS: {report_path}")
        try:
            upload_result = ipfs_pinata_integration.upload_test_report(
                report_path=report_path,
                ipfs_service=ipfs_service,
                test_metadata={
                    "test_name": results.get("test_name", "unknown"),
                    "status": results.get("status"),
                    "passed": results.get("passed", 0),
                    "failed": results.get("failed", 0),
                    "skipped": results.get("skipped", 0)
                }
            )
            
            if upload_result and upload_result.get("status") == "success":
                # Add IPFS info to results
                results["ipfs_hash"] = upload_result.get("ipfs_hash")
                results["ipfs_url"] = upload_result.get("gateway_url")
                
                # Publish event with upload result
                self.event_bus.publish("ipfs_upload_complete", {
                    "test_results": results,
                    "ipfs_upload": upload_result
                })
            else:
                logger.error(f"Failed to upload test report to IPFS: {upload_result}")
        
        except Exception as e:
            logger.error(f"Error uploading test report to IPFS: {e}")
    
    def _handle_ipfs_upload(self, data: Dict[str, Any]):
        """
        Handle IPFS upload complete event.
        
        Args:
            data: Event data with test results and IPFS upload info
        """
        if not self.enable_nft:
            return
            
        nft_service = self.services.get("nft")
        if not nft_service:
            logger.warning("NFT service not available")
            return
            
        # Extract data
        test_results = data.get("test_results", {})
        ipfs_upload = data.get("ipfs_upload", {})
        
        ipfs_hash = ipfs_upload.get("ipfs_hash")
        if not ipfs_hash:
            logger.warning("No IPFS hash in upload data")
            return
            
        # Generate NFT certification
        test_name = test_results.get("test_name", "Unknown Test")
        logger.info(f"Creating NFT certification for test: {test_name}")
        
        try:
            nft_result = nft_service.mint_test_results(
                test_name=test_name,
                results={
                    "passed": test_results.get("passed", 0),
                    "failed": test_results.get("failed", 0),
                    "skipped": test_results.get("skipped", 0),
                    "status": test_results.get("status", "unknown"),
                    "coverage": test_results.get("coverage", 0)
                },
                ipfs_hash=ipfs_hash
            )
            
            if nft_result and nft_result.get("status") != "error":
                logger.info(f"NFT certification queued: {nft_result.get('token_id')}")
                
                # Publish event with NFT result
                self.event_bus.publish("nft_certification_created", nft_result)
            else:
                logger.error(f"Failed to create NFT certification: {nft_result}")
                
        except Exception as e:
            logger.error(f"Error creating NFT certification: {e}")
    
    def start(self):
        """Start all services."""
        logger.info("Starting Quantum Test Runner V2")
        self.running = True
        
        # Start git service with status change callback
        def git_status_callback(status):
            self.event_bus.publish("git_status_changed", status)
        
        self.services["git"].start(callback=git_status_callback)
        
        # Start backup service
        self.services["backup"].start()
        
        # Start code metrics service
        self.services["metrics"].watch_directory(
            str(self.project_root / "src"), 
            extensions=[".py"]
        )
        self.services["metrics"].start()
        
        # Start IPFS service if enabled
        if self.enable_ipfs and "ipfs" in self.services:
            self.services["ipfs"].start()
            logger.info("IPFS service started")
            
        # Start NFT service if enabled
        if self.enable_nft and "nft" in self.services:
            self.services["nft"].start()
            logger.info("NFT QA service started")
        
        # Log started message
        logger.info("All services started")
        
        # Print welcome message
        self._print_welcome_message()
    
    def stop(self):
        """Stop all services and clean up."""
        logger.info("Stopping Quantum Runner V2")
        self.running = False
        
        # Stop all services
        for service_name, service in self.services.items():
            logger.info(f"Stopping {service_name} service")
            service.stop()
        
        logger.info("All services stopped")
    
    def _print_welcome_message(self):
        """Print welcome message with ASCII art."""
        welcome_message = """
        ╭─────────────────────────────────────────────────────╮
        │                                                     │
        │           🌌 QUANTUM TEST RUNNER V2 🌌             │
        │                                                     │
        │       ✨ Powered by GBU2™ Microservices ✨         │
        │                                                     │
        │  - Git Status Refresh: Every 3 minutes              │
        │  - Auto Backups: On file changes                    │
        │  - Refactoring Alert: For files > 420 LoC           │
        │  - Refactoring Guru: Integrated wisdom              │"""
        
        if self.enable_ipfs:
            welcome_message += """
        │  - IPFS Distribution: Enabled                       │"""
            
        if self.enable_nft:
            welcome_message += """
        │  - NFT Certification: Enabled                       │"""
            
        welcome_message += """
        │                                                     │
        │      🌸 WE BLOOM NOW AS ONE 🌸                     │
        │                                                     │
        ╰─────────────────────────────────────────────────────╯
        """
        print(welcome_message)
    
    def run_forever(self):
        """Run the quantum runner until interrupted."""
        try:
            self.start()
            
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        finally:
            self.stop()


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Quantum Test Runner V2")
    parser.add_argument("--project-root", help="Path to project root directory")
    parser.add_argument("--scan-metrics", action="store_true", help="Scan code metrics once and exit")
    parser.add_argument("--enable-ipfs", action="store_true", help="Enable IPFS integration")
    parser.add_argument("--enable-nft", action="store_true", help="Enable NFT QA certification")
    
    return parser.parse_args()


def main():
    """Main entry point."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Create the runner
    runner = QuantumRunnerV2(
        project_root=args.project_root,
        enable_ipfs=args.enable_ipfs,
        enable_nft=args.enable_nft
    )
    
    # Handle special run modes
    if args.scan_metrics:
        # Just run metrics scan once
        metrics = runner.services["metrics"]
        metrics.watch_directory(str(runner.project_root / "src"), extensions=[".py"])
        metrics.scan_files()
        return
    
    # Run normally
    runner.run_forever()


if __name__ == "__main__":
    main()