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
Test Runner for RASTA Discord Bot

Runs tests with coverage reporting to ensure we meet the 80% threshold.
"""

import os
import subprocess
import sys

def run_tests_with_coverage():
    """Run tests with coverage and generate a report."""
    print("🔴🟡🟢 Running RASTA Discord Bot tests with coverage 🔴🟡🟢")
    
    # Run pytest with coverage
    cmd = [
        "python", "-m", "pytest",
        "tests/",
        "-v",
        "--cov=.",
        "--cov-report=term",
        "--cov-report=html:coverage_html",
        "--cov-config=.coveragerc"
    ]
    
    try:
        # Create a basic .coveragerc file if it doesn't exist
        if not os.path.exists(".coveragerc"):
            with open(".coveragerc", "w") as f:
                f.write("""[run]
source = .
omit = 
    tests/*
    run_tests.py
    */site-packages/*
    
[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
    pass
    raise ImportError
""")
            print("Created .coveragerc configuration file")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        # Extract coverage percentage
        for line in reversed(result.stdout.split('\n')):
            if "TOTAL" in line:
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        coverage = float(parts[3].strip('%'))
                        print(f"\n🔍 Overall coverage: {coverage:.1f}%")
                        
                        if coverage >= 80:
                            print("✅ Coverage meets or exceeds 80% threshold!")
                        else:
                            print(f"❌ Coverage is below 80% threshold by {80 - coverage:.1f}%")
                            print("Additional tests are needed to reach 80% coverage.")
                    except ValueError:
                        print("Could not parse coverage percentage")
                break
        
        print("\nDetailed coverage report has been generated in the coverage_html directory")
        return result.returncode
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests_with_coverage()) 