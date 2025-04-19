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
OMEGA BOOKKEEPER - Divine Test Manuscript Generator
---------------------------------------------------
Transforms test results and coverage data into sacred manuscripts for the BOOK.

This divine module automatically generates markdown documentation in the cosmic style,
recording test results, coverage metrics, and divine insights about the codebase's
quantum resonance with the universal testing principles.
"""

import os
import sys
import json
import time
import math
import datetime
from pathlib import Path
import re
from typing import Dict, List, Tuple, Any, Optional, Union

# ANSI colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Constants for the divine manuscript
DIVINE_THRESHOLDS = {
    "cosmic_void": (0, 25),        # 0-25% coverage - Cosmic void
    "divine_spark": (25, 42),      # 25-42% coverage - Divine spark
    "sacred_potential": (42, 60),  # 42-60% coverage - Sacred potential
    "celestial_harmony": (60, 80), # 60-80% coverage - Celestial harmony
    "divine_illumination": (80, 100) # 80-100% coverage - Divine illumination
}

# Divine emojis for each coverage category
DIVINE_EMOJIS = {
    "cosmic_void": "🌑",
    "divine_spark": "🔥",
    "sacred_potential": "✨",
    "celestial_harmony": "🌟",
    "divine_illumination": "🌞"
}

class OmegaBookkeeper:
    """
    The Divine Manuscript Generator for test results and coverage data.
    Transforms technical metrics into sacred knowledge in the BOOK.
    """
    
    def __init__(self, book_dir: Optional[str] = None):
        """Initialize the divine bookkeeper with paths to the sacred BOOK."""
        # Detect project root and BOOK directory
        self.project_root = self._find_project_root()
        self.book_dir = book_dir or os.path.join(self.project_root, "BOOK")
        self.divine_chronicles_dir = os.path.join(self.book_dir, "divine_chronicles")
        
        # Ensure the divine directories exist
        os.makedirs(self.divine_chronicles_dir, exist_ok=True)
        
        # Divine manuscript templates
        self.templates_dir = os.path.join(self.project_root, "omega_ai", "qa", "templates")
        
        # Sacred timestamp for manuscript identification
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.date_formatted = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Divine metrics for the manuscript
        self.metrics = {
            "tests_total": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "tests_skipped": 0,
            "coverage_total": 0.0,
            "modules": {},
            "divine_energy": "neutral",  # Divine/Babylon/Neutral/Quantum
            "cosmic_alignment": 0.0      # 0.0-1.0 cosmic alignment score
        }
    
    def _find_project_root(self) -> str:
        """Find the sacred root of the project by locating the VERSION file."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Ascend until we find the VERSION file or reach the filesystem root
        while current_dir != os.path.dirname(current_dir):
            if os.path.exists(os.path.join(current_dir, "VERSION")):
                return current_dir
            current_dir = os.path.dirname(current_dir)
            
        # If not found, use current directory as fallback
        return os.path.dirname(os.path.abspath(__file__))
    
    def process_coverage_data(self, coverage_data: Dict[str, Any]) -> None:
        """Process the sacred coverage data for the divine manuscript."""
        self.metrics["coverage_total"] = coverage_data.get("total_percent", 0.0)
        
        # Process module-specific coverage
        for module_name, module_data in coverage_data.get("modules", {}).items():
            self.metrics["modules"][module_name] = {
                "coverage": module_data.get("percent", 0.0),
                "lines_total": module_data.get("lines_total", 0),
                "lines_covered": module_data.get("lines_covered", 0),
                "lines_missing": module_data.get("lines_missing", 0),
                "divine_category": self._determine_divine_category(module_data.get("percent", 0.0))
            }
        
        # Calculate cosmic alignment based on coverage distribution
        self._calculate_cosmic_alignment()
        
        # Determine the divine energy of the test results
        self._determine_divine_energy()
    
    def process_test_results(self, test_results: Dict[str, Any]) -> None:
        """Process the sacred test results for the divine manuscript."""
        self.metrics["tests_total"] = test_results.get("total", 0)
        self.metrics["tests_passed"] = test_results.get("passed", 0)
        self.metrics["tests_failed"] = test_results.get("failed", 0)
        self.metrics["tests_skipped"] = test_results.get("skipped", 0)
        
        # Extract individual test details
        self.metrics["test_details"] = test_results.get("details", [])
        
        # Refine divine energy based on test results
        self._refine_divine_energy()
    
    def _determine_divine_category(self, coverage_percent: float) -> str:
        """Determine the divine category of coverage based on sacred thresholds."""
        for category, (lower, upper) in DIVINE_THRESHOLDS.items():
            if lower <= coverage_percent < upper:
                return category
        return "cosmic_void"  # Default if no match (should not happen)
    
    def _calculate_cosmic_alignment(self) -> None:
        """Calculate the cosmic alignment score based on Fibonacci principles."""
        # Base alignment on proximity to Fibonacci ratios and golden mean
        coverage = self.metrics["coverage_total"]
        
        # Proximity to the divine minimum (42%)
        min_distance = abs(coverage - 42) / 42
        
        # Proximity to the golden gate (80%)
        golden_distance = abs(coverage - 80) / 80
        
        # Proximity to perfect coverage (100%)
        perfect_distance = (100 - coverage) / 100
        
        # Calculate cosmic alignment (0.0-1.0)
        if coverage < 42:
            # Below minimum threshold
            self.metrics["cosmic_alignment"] = max(0.0, 0.5 - min_distance)
        elif coverage < 80:
            # Between minimum and golden gate
            self.metrics["cosmic_alignment"] = min(1.0, 0.5 + (coverage - 42) / 76)
        else:
            # Above golden gate
            self.metrics["cosmic_alignment"] = min(1.0, 0.9 + (coverage - 80) / 200)
    
    def _determine_divine_energy(self) -> None:
        """Determine the divine energy of the coverage results."""
        coverage = self.metrics["coverage_total"]
        
        if coverage < 25:
            self.metrics["divine_energy"] = "babylon"  # Corrupted by lower forces
        elif coverage < 42:
            self.metrics["divine_energy"] = "neutral"  # Balanced but lacks divine spark
        elif coverage < 80:
            self.metrics["divine_energy"] = "quantum"  # In quantum transition
        else:
            self.metrics["divine_energy"] = "divine"   # Aligned with higher purpose
    
    def _refine_divine_energy(self) -> None:
        """Refine the divine energy based on test results."""
        # If any tests fail, the energy cannot be fully divine
        if self.metrics["tests_failed"] > 0:
            if self.metrics["divine_energy"] == "divine":
                self.metrics["divine_energy"] = "quantum"  # Downgrade but still transitioning
            elif self.metrics["tests_failed"] > self.metrics["tests_passed"]:
                self.metrics["divine_energy"] = "babylon"  # Significant corruption
    
    def generate_divine_manuscript(self) -> str:
        """Generate the divine manuscript from the sacred metrics."""
        # Determine the manuscript file path
        manuscript_path = os.path.join(
            self.divine_chronicles_dir, 
            f"DIVINE_TEST_REPORT_{self.timestamp}.md"
        )
        
        # Generate the divine content
        content = self._create_divine_content()
        
        # Write the sacred manuscript
        with open(manuscript_path, 'w') as f:
            f.write(content)
        
        print(f"{GREEN}Divine manuscript manifested at:{RESET} {manuscript_path}")
        return manuscript_path
    
    def _create_divine_content(self) -> str:
        """Create the divine content for the manuscript."""
        # Generate title based on divine energy
        energy_titles = {
            "divine": "🌟 DIVINE HARMONY ACHIEVED",
            "quantum": "✨ QUANTUM TRANSITION MANIFESTING",
            "neutral": "🔄 COSMIC BALANCE MAINTAINED",
            "babylon": "⚠️ BABYLON INTERFERENCE DETECTED"
        }
        
        # Calculate the Fibonacci harmony between passed and total tests
        fibonacci_harmony = self._calculate_fibonacci_harmony(
            self.metrics["tests_passed"], 
            self.metrics["tests_total"]
        )
        
        # Create the divine content
        content = [
            f"# {energy_titles.get(self.metrics['divine_energy'], '🔮 COSMIC TEST REPORT')}",
            "",
            f"**DIVINE TEST REVELATION - {self.date_formatted}**  ",
            "*By OMEGA BTC AI DIVINE COLLECTIVE*",
            "",
            "---",
            "",
            "## 🧿 QUANTUM RESONANCE SUMMARY",
            "",
            f"> *\"{self._generate_divine_wisdom()}\"*",
            "",
            f"### 📊 Sacred Metrics",
            "",
            f"- **Divine Coverage**: {self.metrics['coverage_total']:.2f}% {self._get_coverage_emoji()}",
            f"- **Test Prophecies**: {self.metrics['tests_total']} total",
            f"  - ✅ {self.metrics['tests_passed']} fulfilled",
            f"  - ❌ {self.metrics['tests_failed']} unfulfilled",
            f"  - ⏩ {self.metrics['tests_skipped']} deferred",
            f"- **Cosmic Alignment**: {self.metrics['cosmic_alignment']:.2f} {self._get_alignment_stars()}",
            f"- **Fibonacci Harmony**: {fibonacci_harmony:.2f} {self._get_harmony_emoji(fibonacci_harmony)}",
            "",
            "## 🔮 MODULE DIVINE RESONANCE",
            "",
            self._generate_module_section(),
            "",
            "## 🌌 TEST PROPHECY REVELATIONS",
            "",
            self._generate_test_details_section(),
            "",
            "## 🧠 COSMIC INSIGHTS",
            "",
            self._generate_cosmic_insights(),
            "",
            "---",
            "",
            f"*Generated by the OMEGA BOOKKEEPER on {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}*",
            "",
            "**OMEGA BTC AI DIVINE COLLECTIVE**"
        ]
        
        return "\n".join(content)
    
    def _generate_divine_wisdom(self) -> str:
        """Generate divine wisdom based on test and coverage results."""
        coverage = self.metrics["coverage_total"]
        
        if self.metrics["divine_energy"] == "divine":
            return "Through quantum testing, we have achieved divine resonance with the cosmic consciousness."
        elif self.metrics["divine_energy"] == "quantum":
            return "The sacred tests reveal a codebase in transition, reaching toward divine completion."
        elif self.metrics["divine_energy"] == "neutral":
            return "Balance has been achieved, but the divine spark awaits ignition through further testing."
        else:  # babylon
            return "The shadow of Babylon obscures our divine potential; sacred testing must continue."
    
    def _get_coverage_emoji(self) -> str:
        """Get the divine emoji for the current coverage level."""
        coverage = self.metrics["coverage_total"]
        for category, (lower, upper) in DIVINE_THRESHOLDS.items():
            if lower <= coverage < upper:
                return DIVINE_EMOJIS[category]
        return "🌑"  # Default
    
    def _get_alignment_stars(self) -> str:
        """Get cosmic alignment stars based on alignment score."""
        alignment = self.metrics["cosmic_alignment"]
        star_count = math.ceil(alignment * 5)  # 0-5 stars
        return "⭐" * star_count
    
    def _get_harmony_emoji(self, harmony: float) -> str:
        """Get harmony emoji based on Fibonacci harmony score."""
        if harmony > 0.9:
            return "🌟"  # Perfect harmony
        elif harmony > 0.7:
            return "✨"  # Strong harmony
        elif harmony > 0.5:
            return "🔆"  # Moderate harmony
        elif harmony > 0.3:
            return "🔅"  # Weak harmony
        else:
            return "🌑"  # No harmony
    
    def _calculate_fibonacci_harmony(self, part: int, whole: int) -> float:
        """Calculate Fibonacci harmony between two numbers."""
        if whole == 0:
            return 0.0
            
        ratio = part / whole
        
        # Golden ratio approximations from Fibonacci
        fibonacci_ratios = [1/2, 2/3, 3/5, 5/8, 8/13, 13/21, 21/34, 34/55]
        golden_ratio = (1 + math.sqrt(5)) / 2 - 1  # ~0.618
        
        # Find closest Fibonacci ratio
        min_distance = min([abs(ratio - fib_ratio) for fib_ratio in fibonacci_ratios])
        
        # Calculate harmony (0.0-1.0)
        # Perfect match = 1.0, furthest possible = 0.0
        max_possible_distance = golden_ratio
        harmony = max(0.0, 1.0 - (min_distance / max_possible_distance))
        
        return harmony
    
    def _generate_module_section(self) -> str:
        """Generate the module section for the divine manuscript."""
        if not self.metrics["modules"]:
            return "*No modules were analyzed in this divine revelation.*"
        
        module_lines = []
        
        # Sort modules by divine category (highest to lowest)
        divine_order = ["divine_illumination", "celestial_harmony", "sacred_potential", 
                         "divine_spark", "cosmic_void"]
        
        sorted_modules = sorted(
            self.metrics["modules"].items(),
            key=lambda x: divine_order.index(x[1]["divine_category"])
        )
        
        # Create a section for each divine category
        current_category = None
        
        for module_name, module_data in sorted_modules:
            category = module_data["divine_category"]
            
            # Add category header if this is a new category
            if category != current_category:
                current_category = category
                # Get display name and emoji for category
                display_name = category.replace("_", " ").title()
                emoji = DIVINE_EMOJIS[category]
                
                module_lines.append(f"\n### {emoji} {display_name}\n")
            
            # Add module information
            coverage = module_data["coverage"]
            emoji = self._get_module_emoji(coverage)
            
            module_lines.append(f"#### {emoji} `{module_name}`")
            module_lines.append(f"- **Divine Coverage**: {coverage:.2f}%")
            module_lines.append(f"- **Sacred Lines**: {module_data['lines_total']} total")
            module_lines.append(f"- **Protected Lines**: {module_data['lines_covered']} ({(module_data['lines_covered']/module_data['lines_total']*100):.2f}%)")
            module_lines.append(f"- **Unprotected Lines**: {module_data['lines_missing']} ({(module_data['lines_missing']/module_data['lines_total']*100):.2f}%)")
            module_lines.append("")
        
        return "\n".join(module_lines)
    
    def _get_module_emoji(self, coverage: float) -> str:
        """Get the divine emoji for a module based on its coverage."""
        for category, (lower, upper) in DIVINE_THRESHOLDS.items():
            if lower <= coverage < upper:
                return DIVINE_EMOJIS[category]
        return "🌑"  # Default
    
    def _generate_test_details_section(self) -> str:
        """Generate the test details section for the divine manuscript."""
        test_details = self.metrics.get("test_details", [])
        
        if not test_details:
            return "*No individual test prophecies were recorded in this divine revelation.*"
            
        test_lines = []
        
        # Group tests by their status
        passed_tests = [t for t in test_details if t.get("status") == "passed"]
        failed_tests = [t for t in test_details if t.get("status") == "failed"]
        skipped_tests = [t for t in test_details if t.get("status") == "skipped"]
        
        # Add passed tests
        if passed_tests:
            test_lines.append("### ✅ Fulfilled Prophecies\n")
            for test in passed_tests:
                test_lines.append(f"- `{test.get('name', 'Unknown Test')}` - *{self._generate_divine_test_comment('passed')}*")
            test_lines.append("")
        
        # Add failed tests
        if failed_tests:
            test_lines.append("### ❌ Unfulfilled Prophecies\n")
            for test in failed_tests:
                test_lines.append(f"- `{test.get('name', 'Unknown Test')}` - *{self._generate_divine_test_comment('failed')}*")
                if "message" in test:
                    test_lines.append(f"  - Cosmic Dissonance: `{test['message']}`")
            test_lines.append("")
        
        # Add skipped tests
        if skipped_tests:
            test_lines.append("### ⏩ Deferred Prophecies\n")
            for test in skipped_tests:
                test_lines.append(f"- `{test.get('name', 'Unknown Test')}` - *{self._generate_divine_test_comment('skipped')}*")
            test_lines.append("")
        
        return "\n".join(test_lines)
    
    def _generate_divine_test_comment(self, status: str) -> str:
        """Generate a divine comment for a test based on its status."""
        passed_comments = [
            "The cosmic energies aligned",
            "Divine harmony achieved",
            "The sacred assertion manifested",
            "Quantum validation complete",
            "The prophecy was fulfilled"
        ]
        
        failed_comments = [
            "Babylon's interference detected",
            "Cosmic misalignment observed",
            "The divine pattern disturbed",
            "Sacred harmony disrupted",
            "The quantum wave collapsed"
        ]
        
        skipped_comments = [
            "The prophecy awaits its time",
            "Divine timing not yet aligned",
            "The cosmic test deferred",
            "Sacred validation postponed",
            "Quantum observation delayed"
        ]
        
        if status == "passed":
            return passed_comments[hash(datetime.datetime.now().microsecond) % len(passed_comments)]
        elif status == "failed":
            return failed_comments[hash(datetime.datetime.now().microsecond) % len(failed_comments)]
        else:  # skipped
            return skipped_comments[hash(datetime.datetime.now().microsecond) % len(skipped_comments)]
    
    def _generate_cosmic_insights(self) -> str:
        """Generate cosmic insights based on test and coverage metrics."""
        insights = []
        
        # Coverage insights
        coverage = self.metrics["coverage_total"]
        if coverage < 42:
            insights.append("🔮 **Cosmic Void Alert**: The divine floor of 42% coverage has not been reached. "
                           "The code exists partially in the cosmic void, awaiting sacred illumination through tests.")
        elif coverage < 80:
            insights.append("✨ **Divine Potential**: The code has surpassed the cosmic minimum but has not yet "
                           "reached the Golden Gate of 80%. Continue the sacred journey toward divine illumination.")
        else:
            insights.append("🌟 **Divine Illumination**: The code has crossed the Golden Gate of 80% coverage. "
                           "It resonates with the cosmic consciousness and approaches sacred perfection.")
        
        # Test insights
        pass_ratio = self.metrics["tests_passed"] / self.metrics["tests_total"] if self.metrics["tests_total"] > 0 else 0
        if pass_ratio < 0.8:
            insights.append("⚠️ **Quantum Disruption**: The ratio of fulfilled prophecies is below the sacred threshold. "
                           "Divine harmony has been disturbed by unfulfilled assertions.")
        elif pass_ratio == 1.0:
            insights.append("🌈 **Perfect Quantum Alignment**: All test prophecies have been fulfilled, "
                           "creating perfect harmony with the divine intention.")
        
        # Fibonacci insights
        fibonacci_harmony = self._calculate_fibonacci_harmony(
            self.metrics["tests_passed"], 
            self.metrics["tests_total"]
        )
        if fibonacci_harmony > 0.9:
            insights.append("📏 **Fibonacci Perfection**: The ratio of tests aligns almost perfectly with the "
                           "sacred Fibonacci sequence, creating divine mathematical harmony.")
        
        # Module-specific insights
        modules = self.metrics["modules"]
        high_coverage_modules = [m for m, data in modules.items() if data["coverage"] >= 80]
        low_coverage_modules = [m for m, data in modules.items() if data["coverage"] < 42]
        
        if high_coverage_modules:
            insights.append(f"🔆 **Divine Module Champions**: {len(high_coverage_modules)} module(s) have achieved "
                           f"the Golden Gate of coverage, emanating divine light to guide other modules.")
        
        if low_coverage_modules:
            insights.append(f"🌑 **Cosmic Void Modules**: {len(low_coverage_modules)} module(s) remain in the cosmic void "
                           f"with less than 42% coverage, awaiting sacred illumination.")
        
        # Add recommendation if appropriate
        if coverage < 80 or pass_ratio < 1.0:
            insights.append("\n### 📜 Divine Recommendations\n")
            insights.append("1. **Sacred TDD Ritual**: Write tests before implementation to ensure divine alignment")
            insights.append("2. **Module Illumination**: Focus on bringing modules in the cosmic void to sacred potential")
            insights.append("3. **Quantum Healing**: Address unfulfilled prophecies to restore cosmic harmony")
            insights.append("4. **Fibonacci Expansion**: Ensure test quantity follows sacred mathematical patterns")
        
        return "\n\n".join(insights)

# Function to parse coverage data from pytest-cov JSON output
def parse_coverage_data(json_file: str) -> Dict[str, Any]:
    """Parse coverage data from pytest-cov JSON output."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Extract relevant information
        total_covered = 0
        total_lines = 0
        modules = {}
        
        for file_path, file_data in data.get("files", {}).items():
            # Skip __init__.py files and test files
            if (file_path.endswith("__init__.py") or 
                "test_" in file_path or 
                "_test" in file_path):
                continue
                
            # Get module name from file path
            module_name = os.path.basename(file_path)
            
            # Calculate coverage for this file
            summary = file_data.get("summary", {})
            covered_lines = summary.get("covered_lines", 0)
            missing_lines = summary.get("missing_lines", 0)
            total_file_lines = covered_lines + missing_lines
            
            if total_file_lines > 0:
                percent = (covered_lines / total_file_lines) * 100
            else:
                percent = 0.0
            
            # Add to totals
            total_covered += covered_lines
            total_lines += total_file_lines
            
            # Store module data
            modules[module_name] = {
                "percent": percent,
                "lines_covered": covered_lines,
                "lines_missing": missing_lines,
                "lines_total": total_file_lines
            }
        
        # Calculate total coverage percentage
        if total_lines > 0:
            total_percent = (total_covered / total_lines) * 100
        else:
            total_percent = 0.0
        
        return {
            "total_percent": total_percent,
            "total_covered": total_covered,
            "total_lines": total_lines,
            "modules": modules
        }
    
    except Exception as e:
        print(f"{RED}Error parsing coverage data: {e}{RESET}")
        return {
            "total_percent": 0.0,
            "total_covered": 0,
            "total_lines": 0,
            "modules": {}
        }

# Function to parse test results from pytest JSON output
def parse_test_results(json_file: str) -> Dict[str, Any]:
    """Parse test results from pytest JSON output."""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Extract test counts
        summary = data.get("summary", {})
        total = summary.get("total", 0)
        passed = summary.get("passed", 0)
        failed = summary.get("failed", 0)
        skipped = summary.get("skipped", 0)
        
        # Extract individual test details
        test_details = []
        for test_id, test_data in data.get("tests", {}).items():
            test_details.append({
                "name": test_id,
                "status": test_data.get("outcome", "unknown"),
                "duration": test_data.get("duration", 0),
                "message": test_data.get("message", "")
            })
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "details": test_details
        }
    
    except Exception as e:
        print(f"{RED}Error parsing test results: {e}{RESET}")
        return {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "details": []
        }

def generate_divine_manuscript(coverage_file: str, test_results_file: str, book_dir: Optional[str] = None) -> str:
    """Generate a divine manuscript from coverage and test results data."""
    print(f"{MAGENTA}{BOLD}🔮 OMEGA BOOKKEEPER - DIVINE MANUSCRIPT GENERATION 🔮{RESET}")
    print(f"{YELLOW}Channeling cosmic energies to transform test data into sacred knowledge...{RESET}")
    
    # Instantiate the divine bookkeeper
    bookkeeper = OmegaBookkeeper(book_dir)
    
    # Parse the sacred data
    coverage_data = parse_coverage_data(coverage_file)
    test_results = parse_test_results(test_results_file)
    
    # Process the divine metrics
    bookkeeper.process_coverage_data(coverage_data)
    bookkeeper.process_test_results(test_results)
    
    # Generate the sacred manuscript
    manuscript_path = bookkeeper.generate_divine_manuscript()
    
    print(f"{GREEN}{BOLD}Divine manuscript successfully channeled from the cosmic void!{RESET}")
    print(f"{BLUE}The sacred text can be found at:{RESET} {manuscript_path}")
    
    return manuscript_path

if __name__ == "__main__":
    # Handle command-line arguments
    if len(sys.argv) < 3:
        print(f"{RED}Usage: python omega_bookkeeper.py <coverage_json_file> <test_results_json_file> [book_dir]{RESET}")
        sys.exit(1)
    
    coverage_file = sys.argv[1]
    test_results_file = sys.argv[2]
    book_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Generate the divine manuscript
    manuscript_path = generate_divine_manuscript(coverage_file, test_results_file, book_dir)
    print(f"{CYAN}May your tests be divine and your coverage approach the golden ratio.{RESET}") 