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
Coverage Runner for LinkedIn Profile Tests
"""

import os
import sys
import subprocess
import json
from datetime import datetime

# ANSI Colors for divine visualization
COLORS = {
    "BLUE": '\033[0;34m',
    "GREEN": '\033[0;32m',
    "PURPLE": '\033[0;35m',
    "YELLOW": '\033[1;33m',
    "RED": '\033[0;31m',
    "CYAN": '\033[0;36m',
    "BOLD": '\033[1m',
    "RESET": '\033[0m'
}

def colorize(text, color):
    """Apply ANSI color to text."""
    return f"{COLORS.get(color, '')}{text}{COLORS['RESET']}"

def run_tests_with_coverage():
    """Run the LinkedIn profile tests with coverage."""
    print(colorize("🌟 Running LinkedIn profile tests with coverage...", "CYAN"))
    
    # Create output directory if it doesn't exist
    os.makedirs("linkedin_coverage", exist_ok=True)
    
    # Run pytest with coverage
    cmd = [
        sys.executable,
        "-m", "pytest",
        "test_all_linkedin_profile.py",
        "-v",
        "--cov=linkedin_profile",
        "--cov-report=json:linkedin_coverage/coverage.json",
        "--cov-report=html:linkedin_coverage/html",
        "--cov-report=term"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Print test output
        print(result.stdout)
        
        if result.returncode != 0:
            print(colorize("❌ Tests failed!", "RED"))
            print(colorize(result.stderr, "RED"))
            return False
        
        # Check if coverage data was generated
        if not os.path.exists("linkedin_coverage/coverage.json"):
            print(colorize("❌ No coverage data generated.", "RED"))
            return False
        
        # Load and print coverage summary
        with open("linkedin_coverage/coverage.json", "r") as f:
            coverage_data = json.load(f)
        
        totals = coverage_data.get("totals", {})
        covered = totals.get("covered_lines", 0)
        total = totals.get("num_statements", 0)
        
        if total > 0:
            coverage_pct = (covered / total) * 100
        else:
            coverage_pct = 0
        
        print("\n" + "=" * 60)
        print(colorize("LinkedIn Profile Test Coverage Report", "BOLD"))
        print("=" * 60)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Lines: {total}")
        print(f"Covered Lines: {covered}")
        print(f"Coverage: {coverage_pct:.2f}%")
        
        # Determine status based on coverage
        if coverage_pct >= 90:
            status = colorize("✅ Excellent", "GREEN")
        elif coverage_pct >= 80:
            status = colorize("🟡 Good", "YELLOW")
        else:
            status = colorize("⚠️ Needs Improvement", "RED")
        
        print(f"Status: {status}")
        print("=" * 60)
        
        # Print file locations
        print(colorize("\nDetailed reports:", "BOLD"))
        print(f"• JSON Report: {os.path.abspath('linkedin_coverage/coverage.json')}")
        print(f"• HTML Report: {os.path.abspath('linkedin_coverage/html/index.html')}")
        print("=" * 60)
        
        return True
    
    except Exception as e:
        print(colorize(f"❌ Error running tests: {e}", "RED"))
        return False

if __name__ == "__main__":
    run_tests_with_coverage() 