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
QA STATUS VISUALIZATION 📊🧪

"Visualize the divine quality of thy codebase, for what is not measured cannot be improved."
- Rastafarian Software Engineering Proverbs

This sacred tool visualizes the quality assurance status of the OMEGA BTC AI project,
showing test coverage, passing tests, and other divine metrics that guide development.

JAH BLESS THE METRICS! 🙏📈
"""

import os
import sys
import json
import subprocess
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import datetime
from pathlib import Path
import coverage

# Add project root to path for divine module accessibility
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# Terminal colors for divine output
RED = "\033[91m"
GREEN = "\033[92m" 
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Define Rastafarian colors
RASTA_COLORS = {
    "green": "#058137",  # Vibrant Rasta Green
    "yellow": "#F9D00F", # Bright Rasta Yellow
    "red": "#E42518",    # Rasta Red
    "gold": "#FCBF13",   # Spiritual Golden Aura
    "black": "#000000"   # For contrast and Afrocentric essence
}

# Define paths
QA_OUTPUT_DIR = os.path.join(project_root, "qa_reports")
COVERAGE_FILE = os.path.join(QA_OUTPUT_DIR, "coverage.json")
TEST_RESULTS_FILE = os.path.join(QA_OUTPUT_DIR, "test_results.json")
QA_VISUALIZATION_FILE = os.path.join(QA_OUTPUT_DIR, "qa_visualization.png")

def ensure_output_dir():
    """Create QA output directory if it doesn't exist."""
    os.makedirs(QA_OUTPUT_DIR, exist_ok=True)


def run_tests_with_coverage():
    """Run all tests with coverage and save results."""
    print(f"\n{CYAN}🧪 Running tests with coverage...{RESET}")
    
    # Ensure output directory exists
    ensure_output_dir()
    
    # Create coverage object
    cov = coverage.Coverage()
    
    try:
        # Start coverage measurement
        cov.start()
        
        # Run pytest with JSON output
        result = subprocess.run(
            ["python", "-m", "pytest", "-v", os.path.join(project_root, "omega_ai"), 
             "--json-report", f"--json-report-file={TEST_RESULTS_FILE}"],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        # Stop coverage
        cov.stop()
        
        # Save coverage data
        cov.json_report(outfile=COVERAGE_FILE)
        
        # Print test output
        if result.returncode == 0:
            print(f"{GREEN}✅ All tests passed!{RESET}")
        else:
            print(f"{RED}❌ Some tests failed!{RESET}")
            print(result.stdout)
        
        return result.returncode == 0
    
    except Exception as e:
        print(f"{RED}Error running tests: {e}{RESET}")
        return False


def load_qa_data():
    """Load test results and coverage data."""
    qa_data = {
        "test_results": {},
        "coverage": {},
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    # Load test results if available
    if os.path.exists(TEST_RESULTS_FILE):
        try:
            with open(TEST_RESULTS_FILE, 'r') as f:
                qa_data["test_results"] = json.load(f)
        except Exception as e:
            print(f"{RED}Error reading test results: {e}{RESET}")
    
    # Load coverage data if available
    if os.path.exists(COVERAGE_FILE):
        try:
            with open(COVERAGE_FILE, 'r') as f:
                qa_data["coverage"] = json.load(f)
        except Exception as e:
            print(f"{RED}Error reading coverage data: {e}{RESET}")
    
    return qa_data


def visualize_qa_status(qa_data):
    """Create visualization of QA status."""
    print(f"\n{CYAN}📊 Generating QA visualization...{RESET}")
    
    # Ensure we have data to visualize
    if not qa_data["test_results"] or not qa_data["coverage"]:
        print(f"{YELLOW}⚠️ Insufficient data for visualization. Run tests first.{RESET}")
        return
    
    # Create figure with subplots
    plt.close('all')
    fig = plt.figure(figsize=(20, 12))
    fig.suptitle("OMEGA BTC AI - Divine Quality Assurance Status 🌈🧪", 
                fontsize=24, color=RASTA_COLORS["gold"], fontweight='bold')
    
    # Add timestamp
    time_str = datetime.datetime.fromisoformat(qa_data["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
    plt.figtext(0.02, 0.02, f"Generated: {time_str}", fontsize=10, color=RASTA_COLORS["yellow"])
    
    # Set background color
    fig.patch.set_facecolor('#222222')
    
    # Extract test summary
    test_summary = qa_data["test_results"]["summary"]
    total_tests = test_summary.get("total", 0)
    passed = test_summary.get("passed", 0)
    failed = test_summary.get("failed", 0)
    skipped = test_summary.get("skipped", 0)
    
    # Extract coverage data
    coverage_data = qa_data["coverage"].get("totals", {})
    overall_coverage = coverage_data.get("percent_covered", 0)
    
    # Main modules coverage
    module_coverage = {}
    for filepath, data in qa_data["coverage"].get("files", {}).items():
        # Convert Windows path to Unix-style for consistent parsing
        filepath = filepath.replace("\\", "/")
        # Skip if not in omega_ai
        if "omega_ai" not in filepath:
            continue
        
        # Extract module name (category)
        parts = filepath.split("omega_ai/")
        if len(parts) > 1:
            path_parts = parts[1].split("/")
            if len(path_parts) > 1:
                module = path_parts[0]
            else:
                module = "core"
                
            # Add to module coverage
            if module not in module_coverage:
                module_coverage[module] = {"covered_lines": 0, "num_statements": 0, "files": 0}
            
            module_coverage[module]["covered_lines"] += data.get("covered_lines", 0)
            module_coverage[module]["num_statements"] += data.get("num_statements", 0) 
            module_coverage[module]["files"] += 1
    
    # Calculate percentages
    for module in module_coverage:
        statements = module_coverage[module]["num_statements"]
        if statements > 0:
            module_coverage[module]["percent"] = (
                module_coverage[module]["covered_lines"] / statements * 100
            )
        else:
            module_coverage[module]["percent"] = 0
    
    # Create plots
    
    # 1. Test status - pie chart
    ax1 = plt.subplot2grid((2, 3), (0, 0))
    if total_tests > 0:
        test_labels = [f"Passed ({passed})", f"Failed ({failed})", f"Skipped ({skipped})"]
        test_values = [passed, failed, skipped]
        test_colors = [RASTA_COLORS["green"], RASTA_COLORS["red"], RASTA_COLORS["yellow"]]
        # Only include non-zero segments
        filtered_labels = []
        filtered_values = []
        filtered_colors = []
        for i, val in enumerate(test_values):
            if val > 0:
                filtered_labels.append(test_labels[i])
                filtered_values.append(val)
                filtered_colors.append(test_colors[i])
                
        ax1.pie(filtered_values, labels=filtered_labels, colors=filtered_colors, 
                autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.set_title("Test Status", color='white', fontsize=16)
    else:
        ax1.text(0.5, 0.5, "No test data available", 
                horizontalalignment='center', verticalalignment='center',
                fontsize=14, color=RASTA_COLORS["yellow"])
    ax1.set_facecolor('#333333')
    
    # 2. Overall coverage - gauge chart
    ax2 = plt.subplot2grid((2, 3), (0, 1))
    gauge_colors = [RASTA_COLORS["red"], RASTA_COLORS["yellow"], RASTA_COLORS["green"]]
    gauge_cmap = mcolors.LinearSegmentedColormap.from_list("GaugeMap", gauge_colors)
    
    # Create gauge
    gauge_theta = np.linspace(0, 180, 100)
    gauge_r = np.ones_like(gauge_theta)
    gauge_width = 0.3
    
    # Background gauge (gray)
    ax2.bar(0, 1, width=180, bottom=1-gauge_width, color='#444444', 
           edgecolor='gray', linewidth=1, alpha=0.8)
    
    # Colored gauge based on coverage
    cov_angle = 180 * (overall_coverage / 100)
    ax2.bar(0, 1, width=cov_angle, bottom=1-gauge_width, color=gauge_cmap(overall_coverage/100), 
           edgecolor='white', linewidth=1, alpha=0.8)
    
    # Add coverage text
    ax2.text(0, 0.5, f"{overall_coverage:.1f}%", 
            horizontalalignment='center', verticalalignment='center',
            fontsize=20, fontweight='bold', color='white')
    
    # Clean up gauge
    ax2.set_title("Overall Code Coverage", color='white', fontsize=16)
    ax2.set_ylim(0, 2)
    ax2.set_xlim(-90, 90)
    ax2.set_facecolor('#333333')
    ax2.axis('off')
    
    # 3. Module coverage - bar chart
    ax3 = plt.subplot2grid((2, 3), (0, 2), rowspan=2)
    modules = list(module_coverage.keys())
    modules.sort(key=lambda m: module_coverage[m]["percent"], reverse=True)
    
    if modules:
        module_names = []
        module_percentages = []
        module_colors = []
        
        for module in modules:
            if module_coverage[module]["num_statements"] > 0:
                module_names.append(f"{module} ({module_coverage[module]['files']} files)")
                coverage_pct = module_coverage[module]["percent"]
                module_percentages.append(coverage_pct)
                
                # Color based on coverage
                if coverage_pct < 50:
                    color = RASTA_COLORS["red"]
                elif coverage_pct < 80:
                    color = RASTA_COLORS["yellow"]
                else:
                    color = RASTA_COLORS["green"]
                module_colors.append(color)
        
        y_pos = np.arange(len(module_names))
        horizontal_bars = ax3.barh(y_pos, module_percentages, color=module_colors)
        ax3.set_yticks(y_pos)
        ax3.set_yticklabels(module_names, color='white')
        ax3.invert_yaxis()  # Labels read top-to-bottom
        ax3.set_xlabel('Coverage %', color='white')
        ax3.set_title('Coverage by Module', color='white', fontsize=16)
        ax3.xaxis.set_ticks_position('top')
        ax3.xaxis.set_label_position('top')
        
        # Add coverage text on bars
        for i, bar in enumerate(horizontal_bars):
            width = bar.get_width()
            label_x_pos = width - 5 if width > 10 else width + 5
            label_color = 'black' if width > 50 else 'white'
            ax3.text(label_x_pos, bar.get_y() + bar.get_height()/2, 
                    f'{module_percentages[i]:.1f}%',
                    va='center', color=label_color, fontweight='bold')
    else:
        ax3.text(0.5, 0.5, "No coverage data by module available", 
                horizontalalignment='center', verticalalignment='center',
                fontsize=14, color=RASTA_COLORS["yellow"])
    
    ax3.set_facecolor('#333333')
    ax3.tick_params(axis='x', colors='white')
    ax3.tick_params(axis='y', colors='white')
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['bottom'].set_visible(False)
    ax3.spines['left'].set_visible(False)
    
    # 4. Test Result Timeline - For future implementation
    ax4 = plt.subplot2grid((2, 3), (1, 0), colspan=2)
    ax4.text(0.5, 0.5, "🚧 Test Timeline Visualization Coming Soon 🚧", 
            horizontalalignment='center', verticalalignment='center',
            fontsize=14, color=RASTA_COLORS["yellow"])
    ax4.set_facecolor('#333333')
    ax4.axis('off')
    
    # Fine-tune layout
    plt.tight_layout(rect=(0, 0.03, 1, 0.95))
    
    # Save the visualization
    plt.savefig(QA_VISUALIZATION_FILE, bbox_inches='tight', dpi=150)
    print(f"{GREEN}✅ QA visualization saved to: {QA_VISUALIZATION_FILE}{RESET}")
    
    # Show metrics in the console
    print(f"\n{GREEN}=== QA METRICS SUMMARY ==={RESET}")
    print(f"{CYAN}Total Tests:{RESET} {total_tests}")
    
    # Calculate pass percentage safely
    pass_percent = (passed / total_tests * 100) if total_tests > 0 else 0
    print(f"{GREEN}Passed Tests:{RESET} {passed} ({pass_percent:.1f}%)")
    
    print(f"{RED}Failed Tests:{RESET} {failed}")
    print(f"{YELLOW}Skipped Tests:{RESET} {skipped}")
    print(f"{CYAN}Overall Coverage:{RESET} {overall_coverage:.1f}%")
    
    # Module coverage summary
    print(f"\n{CYAN}Module Coverage:{RESET}")
    for module in modules:
        if module_coverage[module]["num_statements"] > 0:
            cov_pct = module_coverage[module]["percent"]
            color = GREEN if cov_pct >= 80 else (YELLOW if cov_pct >= 50 else RED)
            print(f"{color}{module}{RESET}: {cov_pct:.1f}% " +
                 f"({module_coverage[module]['covered_lines']}/{module_coverage[module]['num_statements']} lines)")


def main():
    """Main function to run QA visualization."""
    print(f"\n{CYAN}🌈 OMEGA BTC AI - Divine QA Visualization 🌈{RESET}")
    
    # Run tests with coverage
    tests_ok = run_tests_with_coverage()
    
    # Load QA data
    qa_data = load_qa_data()
    
    # Visualize QA status
    visualize_qa_status(qa_data)
    
    # Exit code based on test results
    return 0 if tests_ok else 1


if __name__ == "__main__":
    sys.exit(main()) 