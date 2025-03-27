"""
🔮 OMEGA BTC AI - Divine Coverage Report Generator
================================================

This script generates detailed test coverage reports by module,
with divine visualization and Fibonacci-based thresholds.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Divine color scheme
COLORS = {
    'high': '#4CAF50',    # Green for coverage >= 80%
    'medium': '#FFC107',  # Amber for coverage >= 42%
    'low': '#F44336',     # Red for coverage < 42%
    'background': '#1E1E1E',
    'text': '#FFFFFF'
}

# Fibonacci-based thresholds
THRESHOLDS = {
    'divine': 80.0,  # Divine threshold (80%)
    'sacred': 42.0   # Sacred minimum (42% - Fibonacci based)
}

class DivineCoverageReporter:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.output_dir = self.project_root / 'BOOK' / 'divine_chronicles' / 'coverage'
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_tests_with_coverage(self) -> subprocess.CompletedProcess:
        """Run pytest with coverage and generate JSON report."""
        cmd = [
            'python', '-m', 'pytest',
            'omega_ai/tests/',
            '--cov=omega_ai',
            '--cov-report=json',
            '-v'
        ]
        return subprocess.run(cmd, capture_output=True, text=True)

    def load_coverage_data(self) -> Dict:
        """Load coverage data from JSON report."""
        coverage_file = self.project_root / '.coverage.json'
        if not coverage_file.exists():
            raise FileNotFoundError("Coverage data not found. Run tests first.")
        
        with open(coverage_file) as f:
            return json.load(f)

    def calculate_module_coverage(self, coverage_data: Dict) -> List[Tuple[str, float]]:
        """Calculate coverage percentage for each module."""
        module_coverage = []
        
        for file_path, data in coverage_data['files'].items():
            if not file_path.startswith('omega_ai/'):
                continue
                
            total_lines = len(data['executed_lines']) + len(data['missing_lines'])
            if total_lines == 0:
                continue
                
            coverage_pct = (len(data['executed_lines']) / total_lines) * 100
            module_name = file_path.replace('omega_ai/', '').replace('/', '.')
            module_coverage.append((module_name, coverage_pct))
        
        return sorted(module_coverage, key=lambda x: x[1], reverse=True)

    def generate_divine_visualization(self, module_coverage: List[Tuple[str, float]]):
        """Generate divine visualization of coverage data."""
        plt.style.use('dark_background')
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), gridspec_kw={'height_ratios': [2, 1]})
        
        # Bar chart
        modules, coverage = zip(*module_coverage)
        colors = [
            COLORS['high'] if cov >= THRESHOLDS['divine'] else
            COLORS['medium'] if cov >= THRESHOLDS['sacred'] else
            COLORS['low']
            for cov in coverage
        ]
        
        ax1.bar(modules, coverage, color=colors)
        ax1.set_title('Divine Module Coverage', color=COLORS['text'], pad=20)
        ax1.set_xlabel('Modules', color=COLORS['text'])
        ax1.set_ylabel('Coverage (%)', color=COLORS['text'])
        ax1.tick_params(axis='x', rotation=45, colors=COLORS['text'])
        ax1.tick_params(axis='y', colors=COLORS['text'])
        ax1.grid(True, alpha=0.2)
        
        # Add threshold lines
        ax1.axhline(y=THRESHOLDS['divine'], color='g', linestyle='--', alpha=0.5)
        ax1.axhline(y=THRESHOLDS['sacred'], color='y', linestyle='--', alpha=0.5)
        
        # Pie chart
        divine = sum(1 for _, cov in module_coverage if cov >= THRESHOLDS['divine'])
        sacred = sum(1 for _, cov in module_coverage if THRESHOLDS['sacred'] <= cov < THRESHOLDS['divine'])
        low = len(module_coverage) - divine - sacred
        
        sizes = [divine, sacred, low]
        labels = [
            f'Divine (≥{THRESHOLDS["divine"]}%)',
            f'Sacred (≥{THRESHOLDS["sacred"]}%)',
            f'Low (<{THRESHOLDS["sacred"]}%)'
        ]
        colors = [COLORS['high'], COLORS['medium'], COLORS['low']]
        
        ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        ax2.set_title('Coverage Distribution', color=COLORS['text'], pad=20)
        
        plt.tight_layout()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plt.savefig(self.output_dir / f'divine_coverage_{timestamp}.png', 
                   facecolor=COLORS['background'],
                   bbox_inches='tight',
                   dpi=300)

    def generate_markdown_report(self, module_coverage: List[Tuple[str, float]], test_output: str):
        """Generate markdown report with coverage data."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        report_path = self.output_dir / f'coverage_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        
        with open(report_path, 'w') as f:
            f.write(f"# 🔮 OMEGA BTC AI - Divine Coverage Report\n\n")
            f.write(f"Generated on: {timestamp}\n\n")
            
            # Overall statistics
            total_coverage = sum(cov for _, cov in module_coverage) / len(module_coverage)
            divine_count = sum(1 for _, cov in module_coverage if cov >= THRESHOLDS['divine'])
            sacred_count = sum(1 for _, cov in module_coverage if THRESHOLDS['sacred'] <= cov < THRESHOLDS['divine'])
            
            f.write("## 📊 Overall Statistics\n\n")
            f.write(f"- Average Coverage: {total_coverage:.2f}%\n")
            f.write(f"- Divine Modules (≥{THRESHOLDS['divine']}%): {divine_count}\n")
            f.write(f"- Sacred Modules (≥{THRESHOLDS['sacred']}%): {sacred_count}\n")
            f.write(f"- Total Modules: {len(module_coverage)}\n\n")
            
            # Module coverage table
            f.write("## 📈 Module Coverage\n\n")
            f.write("| Module | Coverage | Status |\n")
            f.write("|--------|-----------|--------|\n")
            
            for module, coverage in module_coverage:
                status = "✨ DIVINE" if coverage >= THRESHOLDS['divine'] else \
                         "🌟 SACRED" if coverage >= THRESHOLDS['sacred'] else \
                         "⚠️ LOW"
                f.write(f"| {module} | {coverage:.2f}% | {status} |\n")
            
            # Test output
            f.write("\n## 🧪 Test Output\n\n")
            f.write("```\n")
            f.write(test_output)
            f.write("\n```\n")

    def run(self):
        """Run the divine coverage report generation."""
        print("🌟 Running tests with coverage...")
        test_result = self.run_tests_with_coverage()
        
        print("📊 Loading coverage data...")
        coverage_data = self.load_coverage_data()
        
        print("🔮 Calculating module coverage...")
        module_coverage = self.calculate_module_coverage(coverage_data)
        
        print("🎨 Generating divine visualization...")
        self.generate_divine_visualization(module_coverage)
        
        print("📝 Generating markdown report...")
        self.generate_markdown_report(module_coverage, test_result.stdout)
        
        print("✨ Divine coverage report generated successfully!")

if __name__ == "__main__":
    try:
        reporter = DivineCoverageReporter()
        reporter.run()
    except Exception as e:
        print(f"❌ Error generating coverage report: {str(e)}")
        sys.exit(1) 