#!/usr/bin/env python3
"""
CYBERTRUCK TEST RUNNER
---------------------

This script demonstrates the complete test-first methodology workflow:
1. Define test cases for a component
2. Implement the component to satisfy the tests
3. Run tests to verify the implementation
4. Generate test reports

Usage:
    python run_cybertruck_tests.py [--component COMPONENT]

Example:
    python run_cybertruck_tests.py --component exoskeleton

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
"""

import os
import sys
import argparse
import logging
import subprocess
import time
import importlib
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the test framework
from cybertruck_test_framework import (
    ComponentCategory,
    TestPriority,
    TestStage,
    TestCase,
    TestFirstFramework,
    Colors
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("CYBERTRUCK_TEST_RUNNER")

# Component mappings
COMPONENT_MAP = {
    "exoskeleton": {
        "category": ComponentCategory.EXOSKELETON,
        "test_file": "cybertruck_components/exoskeleton_test.py",
        "impl_file": "cybertruck_components/exoskeleton.py",
        "name": "Cybertruck Exoskeleton",
        "description": "Exterior armor panels providing structural integrity and protection"
    },
    "powertrain": {
        "category": ComponentCategory.POWERTRAIN,
        "test_file": "cybertruck_components/powertrain_test.py",
        "impl_file": "cybertruck_components/powertrain.py",
        "name": "Cybertruck Powertrain",
        "description": "Motors, battery, and electronic systems for vehicle propulsion"
    },
    "suspension": {
        "category": ComponentCategory.SUSPENSION,
        "test_file": "cybertruck_components/suspension_test.py",
        "impl_file": "cybertruck_components/suspension.py",
        "name": "Cybertruck Suspension",
        "description": "Adaptive air suspension system for variable ride height"
    },
    "autopilot": {
        "category": ComponentCategory.AUTOPILOT,
        "test_file": "cybertruck_components/autopilot_test.py",
        "impl_file": "cybertruck_components/autopilot.py",
        "name": "Cybertruck Autopilot",
        "description": "Self-driving capabilities and driver assistance features"
    }
}

def print_title(title: str, color=Colors.CYAN):
    """Print a formatted title."""
    print(f"\n{color}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{color}{Colors.BOLD}{title.center(80)}{Colors.ENDC}")
    print(f"{color}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def print_step(step: str, color=Colors.YELLOW):
    """Print a formatted step."""
    print(f"\n{color}{Colors.BOLD}[STEP] {step}{Colors.ENDC}")
    print(f"{color}{'-' * (7 + len(step))}{Colors.ENDC}\n")

def run_command(command: List[str], cwd: Optional[str] = None) -> Tuple[int, str]:
    """Run a command and return exit code and output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=cwd or os.path.dirname(os.path.abspath(__file__))
        )
        return result.returncode, result.stdout + "\n" + result.stderr
    except Exception as e:
        return 1, str(e)

def check_file_exists(filepath: str) -> bool:
    """Check if a file exists."""
    return os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath))

def demonstrate_test_first_workflow(component_key: str):
    """Demonstrate the test-first workflow for a component."""
    if component_key not in COMPONENT_MAP:
        logger.error(f"Component '{component_key}' not found. Available components: {', '.join(COMPONENT_MAP.keys())}")
        return
    
    component_info = COMPONENT_MAP[component_key]
    
    print_title(f"TEST-FIRST METHODOLOGY DEMONSTRATION: {component_info['name']}")
    
    # Initialize the test framework
    framework = TestFirstFramework(
        project_root=os.path.dirname(os.path.abspath(__file__)),
        report_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    )
    
    # STEP 1: Define test cases
    print_step("1. Define Test Cases (Tests First!)")
    
    # Check if test file exists
    test_file_exists = check_file_exists(component_info['test_file'])
    if test_file_exists:
        print(f"Test file already exists: {component_info['test_file']}")
        print(f"Loading existing test definitions...")
    else:
        print(f"Test file does not exist. In a real scenario, you would create it first.")
        print(f"For this demo, we'll use existing test files.")
    
    # Find or create module
    module = next((m for m in framework.modules.values() 
                  if m.category == component_info['category'] and component_key in m.name.lower()),
                 None)
    
    if not module:
        module = framework.create_module(
            name=component_info['name'],
            category=component_info['category'],
            description=component_info['description']
        )
        print(f"{Colors.GREEN}Created new module: {module.id} - {module.name}{Colors.ENDC}")
    else:
        print(f"{Colors.BLUE}Using existing module: {module.id} - {module.name}{Colors.ENDC}")
    
    # Show test cases
    if module.test_cases:
        print(f"\n{Colors.BOLD}Defined Test Cases:{Colors.ENDC}")
        for i, (test_id, test_case) in enumerate(module.test_cases.items(), 1):
            print(f"{i}. {Colors.BOLD}{test_case.name}{Colors.ENDC} ({test_case.priority.name})")
            print(f"   {test_case.description}")
            print(f"   Expected Results:")
            for j, result in enumerate(test_case.expected_results, 1):
                print(f"   {j}. {result}")
            print()
    else:
        print(f"\n{Colors.YELLOW}No test cases defined yet. Let's import them from the test file.{Colors.ENDC}")
    
    # Update module with test and implementation paths
    module.test_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        component_info['test_file']
    ))
    
    module.implementation_path = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        component_info['impl_file']
    ))
    
    # Save changes
    framework._save_modules()
    
    # STEP 2: Check Implementation
    print_step("2. Check Component Implementation")
    
    impl_file_exists = check_file_exists(component_info['impl_file'])
    if impl_file_exists:
        print(f"{Colors.GREEN}Implementation file exists: {component_info['impl_file']}{Colors.ENDC}")
        
        # Check LOC compliance
        loc_compliant = module.check_loc_compliance()
        loc_color = Colors.GREEN if loc_compliant else Colors.RED
        print(f"LOC Compliance: {loc_color}{module.loc}/{module.max_loc} lines{Colors.ENDC}")
    else:
        print(f"{Colors.YELLOW}Implementation file does not exist: {component_info['impl_file']}{Colors.ENDC}")
        print(f"In a test-first scenario, the implementation would be created after test definition.")
        print(f"For this demo, we'll assume the implementation exists.")
    
    # STEP 3: Import and Register Tests
    print_step("3. Import and Register Tests")
    
    if test_file_exists:
        print(f"Importing tests from: {component_info['test_file']}")
        
        # Use importlib to dynamically import the test module
        try:
            # Format the module path for import
            module_path = component_info['test_file'].replace('/', '.').replace('.py', '')
            test_module = importlib.import_module(module_path)
            
            if hasattr(test_module, 'register_exoskeleton_tests'):
                test_module.register_exoskeleton_tests()
                print(f"{Colors.GREEN}Successfully registered tests{Colors.ENDC}")
            else:
                print(f"{Colors.YELLOW}No test registration function found in module{Colors.ENDC}")
        except ImportError as e:
            print(f"{Colors.RED}Error importing test module: {e}{Colors.ENDC}")
            print(f"For this demo, we'll proceed anyway.")
    
    # STEP 4: Run Tests
    print_step("4. Run Tests Against Implementation")
    
    if test_file_exists and impl_file_exists:
        print(f"Running tests for: {component_info['name']}")
        
        # Run pytest on the test file
        returncode, output = run_command(
            [sys.executable, "-m", "pytest", component_info['test_file'], "-v"]
        )
        
        if returncode == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}✅ All tests passed!{Colors.ENDC}")
        else:
            print(f"{Colors.RED}{Colors.BOLD}❌ Some tests failed!{Colors.ENDC}")
        
        # Extract and display test results
        print(f"\nTest Results Summary:")
        print(f"{'-' * 30}")
        
        # Simple parsing of pytest output
        test_lines = [line for line in output.splitlines() if " PASSED " in line or " FAILED " in line]
        for line in test_lines:
            if " PASSED " in line:
                print(f"{Colors.GREEN}{line.strip()}{Colors.ENDC}")
            else:
                print(f"{Colors.RED}{line.strip()}{Colors.ENDC}")
    else:
        print(f"{Colors.YELLOW}Cannot run tests: Test file or implementation file missing{Colors.ENDC}")
    
    # STEP 5: Calculate Coverage
    print_step("5. Calculate Test Coverage")
    
    if test_file_exists and impl_file_exists:
        print(f"Calculating coverage for: {component_info['name']}")
        
        # Calculate coverage
        coverage = framework.calculate_coverage(module.id)
        
        if coverage.get("line_coverage", 0) > 0:
            coverage_color = Colors.GREEN if coverage["line_coverage"] >= 80 else (Colors.YELLOW if coverage["line_coverage"] >= 50 else Colors.RED)
            print(f"Line Coverage: {coverage_color}{coverage['line_coverage']:.1f}%{Colors.ENDC}")
            print(f"Branch Coverage: {coverage_color}{coverage['branch_coverage']:.1f}%{Colors.ENDC}")
            print(f"Mutation Coverage: {coverage_color}{coverage['mutation_coverage']:.1f}%{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}Coverage calculation failed or returned 0%{Colors.ENDC}")
    
    # STEP 6: Generate Report
    print_step("6. Generate Test Report")
    
    report = framework.generate_report(module.id)
    
    print(f"{Colors.GREEN}Report generated:{Colors.ENDC}")
    print(f"- Total Tests: {report['total_tests']}")
    print(f"- Passed Tests: {report['passed_tests']}")
    print(f"- Failed Tests: {report['failed_tests']}")
    
    if report.get("modules"):
        module_report = report["modules"][0]
        metrics = module_report.get("metrics", {})
        
        if metrics:
            print(f"\nModule Metrics:")
            print(f"- Pass Rate: {metrics.get('pass_rate', 0):.1f}%")
            print(f"- Line Coverage: {metrics.get('line_coverage', 0):.1f}%")
            print(f"- LOC Compliance: {'Yes' if metrics.get('loc_compliance', False) else 'No'}")
    
    # Final Summary
    print_title("TEST-FIRST METHODOLOGY WORKFLOW COMPLETED", color=Colors.GREEN)
    
    # Show full status
    framework.print_status(module.id)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run Cybertruck test-first methodology demonstration")
    parser.add_argument("--component", type=str, default="exoskeleton",
                        help=f"Component to test: {', '.join(COMPONENT_MAP.keys())}")
    args = parser.parse_args()
    
    demonstrate_test_first_workflow(args.component)

if __name__ == "__main__":
    main() 