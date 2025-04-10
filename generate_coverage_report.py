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
Coverage report generator for LinkedIn Profile module.
This script generates coverage reports in various formats without requiring the tests to pass.
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

def generate_coverage_report():
    """Generate coverage reports for linkedin_profile.py."""
    print(colorize("\n🧪 Generating coverage report for linkedin_profile.py...\n", "CYAN"))
    
    # Create output directory
    output_dir = "linkedin_coverage"
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Run coverage directly
    subprocess.run([
        sys.executable, 
        "-m", "coverage", 
        "run", 
        "--source=linkedin_profile", 
        "linkedin_profile.py"
    ], check=False)
    
    # Step 2: Generate coverage report in multiple formats
    print(colorize("\n📊 Generating coverage reports in multiple formats...\n", "PURPLE"))
    
    # Generate HTML report
    subprocess.run([
        sys.executable, 
        "-m", "coverage", 
        "html", 
        "-d", f"{output_dir}/html"
    ], check=False)
    
    # Generate JSON report
    subprocess.run([
        sys.executable, 
        "-m", "coverage", 
        "json", 
        "-o", f"{output_dir}/coverage.json"
    ], check=False)
    
    # Generate XML report (for CI tools)
    subprocess.run([
        sys.executable, 
        "-m", "coverage", 
        "xml", 
        "-o", f"{output_dir}/coverage.xml"
    ], check=False)
    
    # Generate text report
    result = subprocess.run([
        sys.executable, 
        "-m", "coverage", 
        "report"
    ], capture_output=True, text=True, check=False)
    
    print(result.stdout)
    
    # Save text report to file
    with open(f"{output_dir}/coverage.txt", "w") as f:
        f.write(result.stdout)
    
    # Parse coverage data from JSON
    try:
        if os.path.exists(f"{output_dir}/coverage.json"):
            with open(f"{output_dir}/coverage.json", "r") as f:
                coverage_data = json.load(f)
            
            # Extract coverage percentage
            if "files" in coverage_data and "linkedin_profile.py" in coverage_data["files"]:
                file_data = coverage_data["files"]["linkedin_profile.py"]
                
                # Generate readable markdown report
                generate_markdown_report(output_dir, coverage_data)
            else:
                print(colorize("⚠️ No coverage data found for linkedin_profile.py", "YELLOW"))
        else:
            print(colorize("⚠️ Coverage JSON data file not found", "YELLOW"))
    except Exception as e:
        print(colorize(f"❌ Error parsing coverage data: {e}", "RED"))
    
    print(colorize(f"\n✅ Coverage reports generated in: {os.path.abspath(output_dir)}\n", "GREEN"))
    
    # Print report locations
    print(colorize("\nReport Locations:", "BOLD"))
    print(f"• HTML Report: {os.path.abspath(f'{output_dir}/html/index.html')}")
    print(f"• JSON Report: {os.path.abspath(f'{output_dir}/coverage.json')}")
    print(f"• XML Report: {os.path.abspath(f'{output_dir}/coverage.xml')}")
    print(f"• Text Report: {os.path.abspath(f'{output_dir}/coverage.txt')}")
    print(f"• Markdown Report: {os.path.abspath(f'{output_dir}/report.md')}")

def generate_markdown_report(output_dir, coverage_data):
    """Generate readable markdown report."""
    if "files" not in coverage_data or "linkedin_profile.py" not in coverage_data["files"]:
        return
    
    file_data = coverage_data["files"]["linkedin_profile.py"]
    summary = file_data["summary"]
    
    # Extract coverage metrics
    total_lines = summary["num_statements"]
    covered_lines = summary["covered_lines"]
    missing_lines = summary["missing_lines"]
    coverage_pct = summary["percent_covered"]
    
    # Get missing lines
    missing_lines_list = file_data.get("missing_lines", [])
    
    # Format missing lines ranges
    missing_ranges = []
    current_range = []
    
    if missing_lines_list:
        sorted_missing = sorted(missing_lines_list)
        
        for line in sorted_missing:
            if not current_range or line == current_range[-1] + 1:
                current_range.append(line)
            else:
                missing_ranges.append(current_range)
                current_range = [line]
        
        if current_range:
            missing_ranges.append(current_range)
    
    formatted_ranges = []
    for range_list in missing_ranges:
        if len(range_list) == 1:
            formatted_ranges.append(str(range_list[0]))
        else:
            formatted_ranges.append(f"{range_list[0]}-{range_list[-1]}")
    
    # Determine status
    if coverage_pct >= 90:
        status = "✅ Excellent"
        status_color = "GREEN"
    elif coverage_pct >= 80:
        status = "🟡 Good"
        status_color = "YELLOW"
    else:
        status = "⚠️ Needs Improvement"
        status_color = "RED"
    
    # Create markdown report
    report = f"""# LinkedIn Profile Module Coverage Report
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary
- **Total Lines**: {total_lines}
- **Covered Lines**: {covered_lines}
- **Missing Lines**: {missing_lines}
- **Coverage**: {coverage_pct:.2f}%
- **Status**: {status}

## File Details
- **Filename**: linkedin_profile.py
- **Total Branches**: {summary.get("num_branches", 0)}
- **Covered Branches**: {summary.get("covered_branches", 0)}
- **Branch Coverage**: {coverage_pct:.2f}%

## Missing Lines
```
{", ".join(formatted_ranges) if formatted_ranges else "None"}
```

## Functions
"""
    
    # Add function-level coverage if available
    if "functions" in file_data:
        functions = file_data["functions"]
        report += "\n| Function | Statements | Coverage | Missing Lines |\n"
        report += "|----------|------------|----------|---------------|\n"
        
        for func_name, func_data in functions.items():
            # Skip the empty function name (module-level code)
            if not func_name:
                continue
                
            func_summary = func_data["summary"]
            func_missing = func_data.get("missing_lines", [])
            
            func_statements = func_summary["num_statements"]
            func_coverage = func_summary["percent_covered"]
            
            report += f"| `{func_name}` | {func_statements} | {func_coverage:.1f}% | {', '.join(map(str, func_missing)) if func_missing else 'None'} |\n"
    
    # Add recommendations
    report += "\n## Recommendations\n"
    if coverage_pct < 100:
        report += "To improve coverage, focus on testing these areas:\n\n"
        
        # Group missing lines by functions if possible
        missing_in_functions = {}
        
        if "functions" in file_data:
            for func_name, func_data in file_data["functions"].items():
                if func_data.get("missing_lines"):
                    if func_name:
                        missing_in_functions[func_name] = func_data["missing_lines"]
        
        if missing_in_functions:
            report += "Functions with missing coverage:\n"
            for func_name, missing in missing_in_functions.items():
                report += f"- `{func_name}`: lines {', '.join(map(str, missing))}\n"
        
        report += "\nGeneral recommendations:\n"
        report += "- Implement tests for error handling paths\n"
        report += "- Ensure all conditional branches are tested\n"
        report += "- Add explicit tests for boundary conditions\n"
    else:
        report += "Perfect coverage! Maintain the quality by ensuring tests for new features.\n"
    
    # Add machine-readable data for CI
    report += "\n## Machine-Readable Data\n```json\n"
    report += json.dumps({
        "coverage": coverage_pct,
        "status": status,
        "total_lines": total_lines,
        "covered_lines": covered_lines,
        "missing_lines": missing_lines,
        "missing_line_numbers": missing_lines_list
    }, indent=2)
    report += "\n```\n"
    
    # Write to file
    with open(f"{output_dir}/report.md", "w") as f:
        f.write(report)
    
    # Print status
    print(colorize(f"\nCoverage: {coverage_pct:.2f}% - {status}", status_color))

if __name__ == "__main__":
    generate_coverage_report() 