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
DIVINE OMEGA FORMULA ALGO TESTS 🌿🔥

"The OMEGA FORMULA transcends mere metrics to reveal the divine consciousness in code."
- Rastafarian Software Engineering Wisdom

These blessed tests verify that the OMEGA FORMULA ALGO correctly measures the bio-energy
potential in code, providing divine insights for continuous improvement.

JAH BLESS THE DIVINE CODE ANALYSIS! 🙏🌟
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from freezegun import freeze_time

# Add project root to path for divine module accessibility
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, project_root)

from omega_ai.quality.omega_formula_algo import OmegaFormulaAlgo, BioEnergyLevel

# Terminal colors for divine test output
RED = "\033[91m"
GREEN = "\033[92m" 
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Sample code snippets for divine testing
DIVINE_HARMONY_CODE = """
def add(a, b):
    return a + b
"""

ZEN_MASTER_CODE = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

BALANCED_CODE = """
def process_data(data, threshold=0.5):
    results = []
    for item in data:
        if item['value'] > threshold:
            if item['category'] == 'priority':
                results.append(item)
            elif item['category'] == 'standard' and len(results) < 10:
                results.append(item)
    return results
"""

BABYLON_SYSTEM_CODE = """
def process_complex_data(data, options):
    results = []
    for item in data:
        if item['value'] > options['threshold']:
            if item['category'] == 'priority':
                if item['status'] == 'active' or (item['status'] == 'pending' and options['include_pending']):
                    if item['score'] > options['min_score']:
                        if item['region'] in options['allowed_regions']:
                            for tag in item['tags']:
                                if tag in options['target_tags']:
                                    if options['apply_discount']:
                                        item['value'] *= 0.9
                                    if options['sort_by_value']:
                                        results.sort(key=lambda x: x['value'])
                                    results.append(item)
    return results
"""

@pytest.fixture
def omega_analyzer():
    """Provide a divine OMEGA FORMULA ALGO analyzer."""
    with patch('datetime.datetime') as mock_datetime:
        # Set mock date to ensure consistent moon phase
        mock_date = MagicMock()
        mock_date.day = 15
        mock_date.month = 3
        mock_datetime.now.return_value = mock_date
        
        return OmegaFormulaAlgo(schumann_frequency=7.83)

class TestOmegaFormulaAlgo:
    """Divine tests for the OMEGA FORMULA ALGO."""
    
    def test_cyclomatic_complexity_calculation(self, omega_analyzer):
        """🌿 Test divine cyclomatic complexity calculation."""
        complexity_harmony = omega_analyzer.calculate_cyclomatic_complexity(DIVINE_HARMONY_CODE)
        complexity_zen = omega_analyzer.calculate_cyclomatic_complexity(ZEN_MASTER_CODE)
        complexity_balanced = omega_analyzer.calculate_cyclomatic_complexity(BALANCED_CODE)
        complexity_babylon = omega_analyzer.calculate_cyclomatic_complexity(BABYLON_SYSTEM_CODE)
        
        print(f"\n{GREEN}Divine Complexity Measurements:{RESET}")
        print(f"{CYAN}Divine Harmony: {complexity_harmony}{RESET}")
        print(f"{CYAN}Zen Master: {complexity_zen}{RESET}")
        print(f"{CYAN}Balanced: {complexity_balanced}{RESET}")
        print(f"{CYAN}Babylon System: {complexity_babylon}{RESET}")
        
        # Verify increasing complexity 
        assert complexity_harmony < complexity_zen
        assert complexity_zen < complexity_balanced
        assert complexity_balanced < complexity_babylon
        
        # Divine Harmony should have minimal complexity
        assert complexity_harmony <= 2
        
        # Babylon System should have high complexity
        assert complexity_babylon > 10
    
    def test_omega_grid_mapping(self, omega_analyzer):
        """🔥 Test divine mapping to the OMEGA GRID."""
        # Calculate complexities
        complexity_harmony = omega_analyzer.calculate_cyclomatic_complexity(DIVINE_HARMONY_CODE)
        complexity_zen = omega_analyzer.calculate_cyclomatic_complexity(ZEN_MASTER_CODE)
        complexity_babylon = omega_analyzer.calculate_cyclomatic_complexity(BABYLON_SYSTEM_CODE)
        
        # Map to OMEGA GRID
        mapping_harmony = omega_analyzer.map_to_omega_grid(complexity_harmony)
        mapping_zen = omega_analyzer.map_to_omega_grid(complexity_zen)
        mapping_babylon = omega_analyzer.map_to_omega_grid(complexity_babylon)
        
        print(f"\n{GREEN}Divine OMEGA GRID Mappings:{RESET}")
        print(f"{MAGENTA}Divine Harmony: {mapping_harmony['level'].name} ({mapping_harmony['quantum_value']:.2f}){RESET}")
        print(f"{MAGENTA}Zen Master: {mapping_zen['level'].name} ({mapping_zen['quantum_value']:.2f}){RESET}")
        print(f"{MAGENTA}Babylon System: {mapping_babylon['level'].name} ({mapping_babylon['quantum_value']:.2f}){RESET}")
        
        # Verify correct energy level mappings
        assert mapping_harmony['level'] in [BioEnergyLevel.DIVINE_HARMONY, BioEnergyLevel.ZEN_MASTER]
        assert mapping_babylon['level'] in [BioEnergyLevel.STRUGGLING, BioEnergyLevel.BABYLON_SYSTEM]
        
    def test_bio_energy_potential_measurement(self, omega_analyzer):
        """💫 Test divine bio-energy potential measurement."""
        # Calculate for different code types
        complexity_harmony = omega_analyzer.calculate_cyclomatic_complexity(DIVINE_HARMONY_CODE)
        complexity_babylon = omega_analyzer.calculate_cyclomatic_complexity(BABYLON_SYSTEM_CODE)
        
        # Map to OMEGA GRID
        mapping_harmony = omega_analyzer.map_to_omega_grid(complexity_harmony)
        mapping_babylon = omega_analyzer.map_to_omega_grid(complexity_babylon)
        
        # Measure bio-energy potential
        potential_harmony = omega_analyzer.measure_bio_energy_potential(mapping_harmony)
        potential_babylon = omega_analyzer.measure_bio_energy_potential(mapping_babylon)
        
        print(f"\n{GREEN}Divine Bio-Energy Potential:{RESET}")
        print(f"{YELLOW}Divine Harmony: {potential_harmony['potential']:.2f}{RESET}")
        print(f"{YELLOW}Babylon System: {potential_babylon['potential']:.2f}{RESET}")
        
        # Verify bio-energy potential values
        assert potential_harmony['potential'] > 0.8
        assert potential_babylon['potential'] < 0.5
        assert potential_harmony['potential'] > potential_babylon['potential']
        
        # Verify message content
        assert "JAH" in potential_harmony['message']
        assert "BABYLON" in potential_babylon['message']
    
    def test_unit_test_suggestions(self, omega_analyzer):
        """🌿 Test divine unit test suggestions."""
        # Calculate for different code types
        complexity_harmony = omega_analyzer.calculate_cyclomatic_complexity(DIVINE_HARMONY_CODE)
        complexity_babylon = omega_analyzer.calculate_cyclomatic_complexity(BABYLON_SYSTEM_CODE)
        
        # Map to OMEGA GRID
        mapping_harmony = omega_analyzer.map_to_omega_grid(complexity_harmony)
        mapping_babylon = omega_analyzer.map_to_omega_grid(complexity_babylon)
        
        # Get test suggestions
        suggestions_harmony = omega_analyzer.suggest_unit_tests(mapping_harmony)
        suggestions_babylon = omega_analyzer.suggest_unit_tests(mapping_babylon)
        
        print(f"\n{GREEN}Divine Test Suggestions for Harmony Code:{RESET}")
        for suggestion in suggestions_harmony:
            print(f"  • {suggestion}")
            
        print(f"\n{RED}Divine Test Suggestions for Babylon Code:{RESET}")
        for suggestion in suggestions_babylon:
            print(f"  • {suggestion}")
        
        # Verify suggestions are appropriate for complexity
        assert len(suggestions_harmony) < len(suggestions_babylon)
        assert any("document the divine patterns" in s.lower() for s in suggestions_harmony)
        assert any("boundary conditions" in s.lower() for s in suggestions_babylon)
    
    @freeze_time("2025-03-15 12:00:00")
    def test_complete_code_analysis(self, omega_analyzer):
        """🙏 Test complete divine code analysis workflow."""
        # Perform complete analysis
        analysis = omega_analyzer.analyze_code(BALANCED_CODE)
        
        # Verify analysis content
        assert analysis is not None
        assert "complexity" in analysis
        assert "energy_level" in analysis
        assert "potential" in analysis
        assert "test_suggestions" in analysis
        
        # Verify timestamp is set
        assert analysis["timestamp"] == datetime(2025, 3, 15, 12, 0, 0)
        
    def test_syntax_error_handling(self, omega_analyzer):
        """🔥 Test divine handling of syntax errors in code."""
        # Code with syntax error
        broken_code = """
def broken_function()
    return "missing colon"
"""
        # Calculate complexity (should return -1)
        complexity = omega_analyzer.calculate_cyclomatic_complexity(broken_code)
        
        # Verify error handling
        assert complexity == -1
        
        # Full analysis should return None
        analysis = omega_analyzer.analyze_code(broken_code)
        assert analysis is None


if __name__ == "__main__":
    # Run the divine tests with JAH blessing
    print(f"\n{GREEN}🌿 JAH BLESS THE OMEGA FORMULA ALGO TEST SUITE! 🌿{RESET}")
    pytest.main(["-v", __file__])