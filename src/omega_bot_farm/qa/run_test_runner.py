#!/usr/bin/env python3
"""
0M3G4 B0TS QA AUT0 TEST SUITES RuNn3R 5D
----------------------------------------

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

Quantum Test Runner Launcher for the Omega Bot Farm.
Runs the modular Quantum Test Runner with specified options.
"""

import os
import sys
import argparse
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D")

# Import the main service class from our modular structure
try:
    from .quantum_runner import QuantumTestService, TestDimension, Colors, K8sMatrixSurveillance
except ImportError:
    # Handle the case where the module isn't installed or in PYTHONPATH
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        from quantum_runner.quantum_service import QuantumTestService
        from quantum_runner.types import TestDimension, Colors
        from quantum_runner.k8s_surveillance import K8sMatrixSurveillance
    except ImportError:
        # Another approach - use direct imports from the quantum_runner directory
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            quantum_runner_dir = os.path.join(current_dir, "quantum_runner")
            sys.path.append(quantum_runner_dir)
            from quantum_service import QuantumTestService
            from types import TestDimension, Colors
            from k8s_surveillance import K8sMatrixSurveillance
        except ImportError:
            sys.exit("Error: Could not import quantum_runner module. Please ensure it's installed or in PYTHONPATH.")

def main():
    """Main entry point for the Quantum Test Runner."""
    parser = argparse.ArgumentParser(
        description="0M3G4 B0TS QA AUT0 TEST SUITES RuNn3R 5D",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Core settings
    parser.add_argument(
        "--project-root",
        type=str,
        default=os.getcwd(),
        help="Root directory of the project"
    )
    
    parser.add_argument(
        "--report-dir",
        type=str,
        default="qa/reports",
        help="Directory for test reports"
    )
    
    # Test execution options
    parser.add_argument(
        "--run-tests",
        nargs="*",
        choices=[d.name for d in TestDimension],
        help="Run tests in specified dimensions and exit"
    )
    
    # GBU2 License options
    parser.add_argument(
        "--check-license",
        action="store_true",
        help="Check GBU2 License compliance and exit"
    )
    
    parser.add_argument(
        "--apply-license",
        type=str,
        help="Apply GBU2 License to file or directory"
    )
    
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Apply license recursively to directories"
    )
    
    # Git integration options
    parser.add_argument(
        "--report-uncommitted",
        action="store_true",
        help="Show report of uncommitted files"
    )
    
    parser.add_argument(
        "--suggest-git",
        action="store_true",
        help="Suggest Git commit messages and tags"
    )
    
    # Continuous monitoring options
    parser.add_argument(
        "--auto-listen",
        action="store_true",
        help="Continuously monitor for file changes"
    )
    
    parser.add_argument(
        "--OMEGA",
        action="store_true",
        help="Enable all features (full Omega mode)"
    )
    
    # Interval configuration
    parser.add_argument(
        "--uncommitted-interval",
        type=int,
        default=300,
        help="Interval in seconds between uncommitted file scans"
    )
    
    parser.add_argument(
        "--git-suggestion-interval",
        type=int,
        default=600,
        help="Interval in seconds between Git suggestion updates"
    )
    
    parser.add_argument(
        "--new-file-scan-interval",
        type=int,
        default=60,
        help="Interval in seconds between new file scans"
    )
    
    # K8s Matrix options
    parser.add_argument(
        "--k8s-matrix",
        action="store_true",
        help="Enable Kubernetes Matrix surveillance mode"
    )
    
    parser.add_argument(
        "--k8s-namespace",
        type=str,
        help="Kubernetes namespace to monitor (default: all namespaces)"
    )
    
    parser.add_argument(
        "--k8s-report-interval",
        type=int,
        default=600,
        help="Interval in seconds between Kubernetes matrix reports"
    )
    
    parser.add_argument(
        "--k8s-report",
        action="store_true",
        help="Generate a one-time Kubernetes Matrix surveillance report and exit"
    )
    
    args = parser.parse_args()
    
    # Build configuration from arguments
    config = {
        'report_dir': args.report_dir,
        'run_initial_tests': args.run_tests is not None,
        'report_uncommitted': args.report_uncommitted or args.OMEGA,
        'suggest_git': args.suggest_git or args.OMEGA,
        'auto_listen': args.auto_listen or args.OMEGA,
        'full_omega_mode': args.OMEGA,
        'uncommitted_scan_interval': args.uncommitted_interval,
        'git_suggestion_interval': args.git_suggestion_interval,
        'new_file_scan_interval': args.new_file_scan_interval,
        'k8s_matrix_mode': args.k8s_matrix or args.OMEGA,
        'k8s_namespace': args.k8s_namespace,
        'k8s_report_interval': args.k8s_report_interval
    }
    
    # Initialize the service
    service = QuantumTestService(args.project_root, config)
    
    # Handle one-time commands
    
    # Check license compliance
    if args.check_license:
        # Use GBU2 License checker to check file compliance
        results = service.check_gbu2_license_compliance()
        return
    
    # Apply license
    if args.apply_license:
        results = service.apply_gbu2_license(args.apply_license, args.recursive)
        print(f"License application completed: {results['files_updated']} files updated")
        return
    
    # Run specific tests
    if args.run_tests:
        service.run_quantum_test_suite(args.run_tests)
        return
    
    # Report uncommitted files as a one-time command
    if args.report_uncommitted and not args.auto_listen and not args.OMEGA:
        service.report_uncommitted_files()
        if args.suggest_git:
            service.suggest_git_commit()
            service.suggest_git_tag()
        return
    
    # Generate K8s Matrix report and exit
    if args.k8s_report:
        # Create K8s surveillance instance - we already imported it above
        k8s = K8sMatrixSurveillance(namespace=args.k8s_namespace)
        if k8s.available:
            k8s._scan_resources()  # Force scan
            import time
            time.sleep(2)  # Wait for scan to complete
            k8s.print_matrix_report(detailed=True)
        else:
            # We already imported Colors above
            print(f"{Colors.RED}Kubernetes client not available. Install with: pip install kubernetes{Colors.ENDC}")
        return
    
    # Start continuous monitoring if no one-time commands were specified
    if args.auto_listen or args.OMEGA or args.k8s_matrix:
        try:
            service.start()
            
            # Print appropriate message based on mode
            if args.OMEGA:
                print(f"\n{Colors.BOLD}{Colors.CYAN}🌀 OMEGA MODE ACTIVATED 🌀{Colors.ENDC}")
                print(f"{Colors.YELLOW}Monitoring for file changes, uncommitted files, Matrix K8s, and providing AI-powered Git suggestions{Colors.ENDC}")
                print(f"{Colors.GREEN}Press Ctrl+C to stop{Colors.ENDC}\n")
            elif args.k8s_matrix:
                print(f"\n{Colors.BOLD}{Colors.GREEN}🔵 MATRIX K8S SURVEILLANCE ACTIVATED 🔵{Colors.ENDC}")
                print(f"{Colors.BLUE}Monitoring Kubernetes resources in the Matrix{Colors.ENDC}")
                print(f"{Colors.GREEN}Press Ctrl+C to stop{Colors.ENDC}\n")
            elif args.auto_listen:
                print(f"\n{Colors.BOLD}{Colors.BLUE}🔍 AUTO-LISTEN MODE ACTIVATED 🔍{Colors.ENDC}")
                print(f"{Colors.YELLOW}Monitoring for file changes and uncommitted files{Colors.ENDC}")
                print(f"{Colors.GREEN}Press Ctrl+C to stop{Colors.ENDC}\n")
            
            # Keep the main thread alive
            import time
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Shutting down...{Colors.ENDC}")
        finally:
            service.stop()
    else:
        # If no action specified, show help
        parser.print_help()

if __name__ == "__main__":
    main() 