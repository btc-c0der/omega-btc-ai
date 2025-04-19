#!/usr/bin/env python3
"""
0M3G4 B0TS QA AUT0 TEST SUITES RuNn3R 5D - Demo Script
------------------------------------------------------

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

This script demonstrates the capabilities of the Quantum Test Runner.
It showcases various features like running tests, license checking,
git integration, and Matrix K8s surveillance.
"""

import os
import sys
import time
import argparse
import datetime
from typing import Dict, List, Any

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the quantum runner components
try:
    from quantum_runner import (
        QuantumTestService, TestDimension, TestState, Colors,
        K8sMatrixSurveillance, GBU2LicenseChecker, GitManager
    )
except ImportError:
    print("Error: Could not import the quantum_runner module.")
    print("Make sure you've installed it or are running from the correct directory.")
    sys.exit(1)

def print_header(text):
    """Print a formatted header."""
    print(f"\n{Colors.CYAN}╔{'═' * 78}╗{Colors.ENDC}")
    print(f"{Colors.CYAN}║ {Colors.BOLD}{text}{Colors.ENDC}{Colors.CYAN}{' ' * (77 - len(text))}║{Colors.ENDC}")
    print(f"{Colors.CYAN}╚{'═' * 78}╝{Colors.ENDC}\n")

def print_step(text):
    """Print a step in the demonstration."""
    print(f"{Colors.BLUE}➤ {text}{Colors.ENDC}")

def print_result(text):
    """Print a result."""
    print(f"{Colors.GREEN}  ✓ {text}{Colors.ENDC}")

def pause(seconds=1, message=None):
    """Pause for dramatic effect."""
    if message:
        print(f"{Colors.YELLOW}{message}{Colors.ENDC}")
    time.sleep(seconds)

def run_demo():
    """Run the Quantum Test Runner demonstration."""
    # Get the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    
    print_header("0M3G4 B0TS QA AUT0 TEST SUITES RuNn3R 5D - QUANTUM DEMONSTRATION")
    
    print(f"{Colors.BOLD}Welcome to the Quantum Test Runner demonstration!{Colors.ENDC}")
    print("This script will showcase the various capabilities of the test framework.")
    print("We'll run through several examples to highlight its features.\n")
    
    pause(2, "Initializing quantum systems...")
    
    # DEMO 1: Initialize the service
    print_step("Initializing the Quantum Test Service")
    service = QuantumTestService(project_root, config={
        'report_dir': 'qa/reports/demo',
        'full_omega_mode': True
    })
    print_result("Service initialized successfully")
    
    pause()
    
    # DEMO 2: Run a simple unit test
    print_step("Running a unit test in the UNIT dimension")
    service.run_quantum_test_suite(['UNIT'])
    print_result("Unit test completed")
    
    pause()
    
    # DEMO 3: Check GBU2 License compliance
    print_step("Checking GBU2 License compliance")
    license_checker = GBU2LicenseChecker(project_root)
    
    # Check the demo file itself
    demo_file = os.path.abspath(__file__)
    has_license, level = license_checker.check_file(demo_file)
    
    if has_license:
        print_result(f"This demo file has a GBU2 License with Consciousness Level {level}")
    else:
        print(f"{Colors.RED}  ✗ This demo file does not have a GBU2 License{Colors.ENDC}")
    
    # Check a directory
    qa_dir = os.path.dirname(demo_file)
    print_step(f"Checking GBU2 License compliance for the QA directory")
    report = license_checker.check_directory(qa_dir, recursive=False)
    compliance_rate = report["compliance_rate"] * 100
    
    print_result(f"Directory compliance rate: {compliance_rate:.1f}%")
    print(f"  - Files checked: {report['files_checked']}")
    print(f"  - Files with license: {report['files_with_license']}")
    
    pause()
    
    # DEMO 4: Git integration
    print_step("Demonstrating Git integration")
    git_manager = GitManager(project_root)
    
    # Show uncommitted files
    uncommitted = git_manager.get_uncommitted_report()
    if uncommitted['total_count'] > 0:
        print_result(f"Found {uncommitted['total_count']} uncommitted files")
        
        # Suggest a commit message
        message = git_manager.suggest_commit_message()
        print_result(f"Suggested commit message: {Colors.GREEN}{message}{Colors.ENDC}")
        
        # Suggest a Git tag
        tag = git_manager.suggest_git_tag()
        print_result(f"Suggested Git tag: {Colors.GREEN}{tag}{Colors.ENDC}")
    else:
        print_result("No uncommitted files found")
    
    pause()
    
    # DEMO 5: K8s Matrix surveillance
    print_step("Demonstrating K8s Matrix surveillance")
    
    # Check if Kubernetes client is available
    k8s = K8sMatrixSurveillance()
    if k8s.available:
        print_result("Kubernetes client is available")
        print_step("Generating Matrix surveillance report")
        
        # Scan resources first
        k8s._scan_resources()
        time.sleep(1)  # Wait for scan to complete
        
        # Print the report
        k8s.print_matrix_report(detailed=True)
    else:
        print(f"{Colors.YELLOW}  ⚠ Kubernetes client not available{Colors.ENDC}")
        print(f"{Colors.YELLOW}  Installing the client would enable Matrix K8s surveillance{Colors.ENDC}")
        
        # Show a simulated Matrix report
        print_step("Simulating Matrix report (for demonstration)")
        
        matrix_header = f"""
{Colors.GREEN}╔═════════════════════════════════════════════════════════════╗
║                                                             ║
║  𝕋𝕙𝕖 𝕄𝕒𝕥𝕣𝕚𝕩 𝕂𝟠𝕤 𝔾𝕣𝕚𝕕: 𝕊𝕠𝕟𝕟𝕖𝕥 𝔹𝕝𝕦𝕖 ℙ𝕚𝕝𝕝 𝔼𝕕𝕚𝕥𝕚𝕠𝕟            ║
║                                                             ║
╚═════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
        print(matrix_header)
        
        # Matrix time
        matrix_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.CYAN}Time in the Matrix: {matrix_time}{Colors.ENDC}")
        
        # Summary section
        print(f"\n{Colors.BOLD}{Colors.GREEN}🧬 MATRIX RESOURCE SUMMARY (SIMULATED){Colors.ENDC}")
        print(f"{Colors.GREEN}───────────────────────────{Colors.ENDC}")
        print(f"  📦 Pods:        23")
        print(f"  🚀 Deployments:  8")
        print(f"  🔌 Services:     12")
        
        # Footer
        print(f"\n{Colors.GREEN}═════════════════════════════════════════════════════════════{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.GREEN}                  FOLLOW THE WHITE RABBIT                  {Colors.ENDC}")
        print(f"{Colors.GREEN}═════════════════════════════════════════════════════════════{Colors.ENDC}\n")
    
    pause()
    
    # DEMO 6: Run tests in multiple dimensions
    print_step("Running tests in multiple dimensions")
    dimensions = ['UNIT', 'INTEGRATION', 'PERFORMANCE']
    print(f"Running tests in dimensions: {', '.join(dimensions)}")
    
    service.run_quantum_test_suite(dimensions)
    print_result("Multiple dimension tests completed")
    
    pause()
    
    # DEMO 7: Full OMEGA mode
    print_header("ACTIVATING FULL OMEGA MODE")
    print(f"{Colors.PURPLE}In full OMEGA mode, the Quantum Test Runner activates all features:{Colors.ENDC}")
    print(f" ⚡ Continuous file monitoring")
    print(f" ⚡ Periodic test runs")
    print(f" ⚡ Git integration with smart commit suggestions")
    print(f" ⚡ GBU2 License compliance checking")
    print(f" ⚡ K8s Matrix surveillance")
    print(f" ⚡ Quantum entanglement detection")
    
    print(f"\n{Colors.YELLOW}To activate OMEGA mode in practice, run:{Colors.ENDC}")
    print(f"{Colors.CYAN}python run_test_runner.py --OMEGA{Colors.ENDC}")
    
    # Final message
    print_header("DEMONSTRATION COMPLETE")
    print(f"{Colors.BOLD}Thank you for witnessing the power of the Quantum Test Runner!{Colors.ENDC}")
    print(f"To learn more, check out the documentation in src/omega_bot_farm/qa/quantum_runner/README.md")

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description="Quantum Test Runner Demo")
    parser.add_argument("--auto-run", action="store_true", help="Run the demo automatically")
    args = parser.parse_args()
    
    if args.auto_run:
        # Set shorter pauses for automated runs
        def pause(seconds=0.5, message=None):
            if message:
                print(f"{Colors.YELLOW}{message}{Colors.ENDC}")
            time.sleep(seconds)
    
    try:
        run_demo()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}Demo interrupted by user.{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n{Colors.RED}Error during demo: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 