#!/usr/bin/env python3
"""
Test Suite for BitGet Position Fibonacci Analysis
Tests the Fibonacci analysis functions with Schumann resonance integration
"""

import unittest
import math
import copy
from unittest.mock import MagicMock, patch
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the functions to test
from print_bitget_positions import (
    calculate_phi_resonance, 
    generate_fibonacci_levels,
    analyze_position
)

# Constants
PHI = 1.618033988749895  # Golden Ratio
INV_PHI = 0.618033988749895  # Inverse Golden Ratio
SCHUMANN_RESONANCE = 7.83  # Base Schumann resonance frequency


class TestFibonacciCalculations(unittest.TestCase):
    """Test Fibonacci calculation functions"""

    def test_phi_resonance_perfect_golden_ratio(self):
        """Test perfect PHI resonance with positions at golden ratio"""
        # Create positions where ratio is exactly PHI (1.618)
        long_positions = [{'contracts': 1.618}]
        short_positions = [{'contracts': 1.0}]
        
        resonance = calculate_phi_resonance(long_positions, short_positions)
        self.assertEqual(resonance, 1.0, "Perfect PHI ratio should yield 1.0 resonance")
        
    def test_phi_resonance_inverse_golden_ratio(self):
        """Test perfect PHI resonance with positions at inverse golden ratio"""
        # Create positions where ratio is exactly inverse PHI (0.618)
        long_positions = [{'contracts': 0.618}]
        short_positions = [{'contracts': 1.0}]
        
        resonance = calculate_phi_resonance(long_positions, short_positions)
        self.assertEqual(resonance, 1.0, "Perfect inverse PHI ratio should yield 1.0 resonance")
        
    def test_phi_resonance_no_positions(self):
        """Test phi resonance with no positions"""
        resonance = calculate_phi_resonance([], [])
        self.assertEqual(resonance, 0.5, "No positions should yield 0.5 resonance")
        
    def test_phi_resonance_only_long(self):
        """Test phi resonance with only long positions"""
        long_positions = [{'contracts': 1.0}]
        resonance = calculate_phi_resonance(long_positions, [])
        self.assertEqual(resonance, 0.618, "Only long positions should yield 0.618 resonance")
        
    def test_phi_resonance_only_short(self):
        """Test phi resonance with only short positions"""
        short_positions = [{'contracts': 1.0}]
        resonance = calculate_phi_resonance([], short_positions)
        self.assertEqual(resonance, 0.618, "Only short positions should yield 0.618 resonance")
        
    def test_phi_resonance_off_ratio(self):
        """Test phi resonance with off ratio"""
        long_positions = [{'contracts': 2.0}]
        short_positions = [{'contracts': 1.0}]
        
        # Calculate expected resonance 
        # 2.0/1.0 = 2.0 ratio
        # Difference from PHI: |2.0-1.618|/1.618 = 0.236... 
        # Resonance = 1 - 0.236... ≈ 0.764
        expected = round(1 - abs(2.0 - PHI) / PHI, 3)
        
        resonance = calculate_phi_resonance(long_positions, short_positions)
        self.assertEqual(resonance, expected, f"Off ratio should yield {expected} resonance")
        
    def test_phi_resonance_multiple_positions(self):
        """Test phi resonance with multiple positions"""
        long_positions = [{'contracts': 0.5}, {'contracts': 1.118}]  # Total 1.618
        short_positions = [{'contracts': 0.5}, {'contracts': 0.5}]   # Total 1.0
        
        resonance = calculate_phi_resonance(long_positions, short_positions)
        self.assertEqual(resonance, 1.0, "Multiple positions with perfect PHI ratio should yield 1.0 resonance")


class TestFibonacciLevels(unittest.TestCase):
    """Test Fibonacci level generation"""
    
    def test_fibonacci_levels_long(self):
        """Test Fibonacci levels for long position"""
        entry_price = 80000.0
        levels = generate_fibonacci_levels(entry_price, is_long=True)
        
        # Check key Fibonacci levels
        self.assertAlmostEqual(float(levels['0']), 72000.0, places=1) # 0% level (10% below entry)
        self.assertAlmostEqual(float(levels['0.382']), 75273.6, places=1) # 38.2% retracement
        self.assertAlmostEqual(float(levels['0.618']), 77454.4, places=1) # 61.8% retracement
        self.assertAlmostEqual(float(levels['1.0']), 80000.0, places=1) # 100% level (entry price)
        self.assertAlmostEqual(float(levels['1.618']), 84000.0, places=1) # 161.8% extension
        
    def test_fibonacci_levels_short(self):
        """Test Fibonacci levels for short position"""
        entry_price = 80000.0
        levels = generate_fibonacci_levels(entry_price, is_long=False)
        
        # For shorts, the levels are the same but interpreted differently
        self.assertAlmostEqual(float(levels['0']), 72000.0, places=1) # 0% level
        self.assertAlmostEqual(float(levels['0.382']), 75273.6, places=1) # 38.2% level
        self.assertAlmostEqual(float(levels['0.618']), 77454.4, places=1) # 61.8% level
        self.assertAlmostEqual(float(levels['1.0']), 80000.0, places=1) # 100% level (entry price)
        self.assertAlmostEqual(float(levels['1.618']), 84000.0, places=1) # 161.8% level
        
    def test_schumann_alignment_fibonacci(self):
        """Test Schumann resonance alignment with Fibonacci levels"""
        # Schumann resonance as multiplier (7.83) from base BTC price 
        base_price = 10000.0  # Base price
        schumann_price = base_price * SCHUMANN_RESONANCE  # 78,300
        
        # Generate levels from a price point that should have Schumann resonance at 0.618 level
        # Need to find entry price where 61.8% retracement = schumann_price
        
        # Calculation:
        # If 0.618 level = 78300
        # And 0 level = 72000 (10% below entry)
        # And 1.0 level = 80000 (entry price)
        # Then entry ~= 80000
        
        entry_price = 80000.0
        levels = generate_fibonacci_levels(entry_price, is_long=True)
        
        # Check if the Schumann price is close to the 0.618 Fibonacci level
        schumann_level_diff = abs(float(levels['0.618']) - schumann_price)
        self.assertLess(schumann_level_diff / schumann_price, 0.05, 
                         "Schumann resonance should be close to 0.618 Fibonacci level")


class TestPositionAnalysis(unittest.TestCase):
    """Test position analysis functions"""
    
    def setUp(self):
        """Set up test data"""
        # Sample long position
        self.long_position = {
            'side': 'long',
            'entryPrice': 80000.0,
            'markPrice': 82000.0,
            'contracts': 0.618,
            'notional': 49440.0,  # 0.618 * 80000
            'unrealizedPnl': 1236.0,
            'percentage': 2.5,
            'leverage': 20.0,
            'liquidationPrice': 40000.0,
            'symbol': 'BTC/USDT:USDT'
        }
        
        # Sample short position
        self.short_position = {
            'side': 'short',
            'entryPrice': 80000.0,
            'markPrice': 78300.0,  # Schumann resonance price (7.83 * 10000)
            'contracts': 1.0,
            'notional': 80000.0,
            'unrealizedPnl': 1700.0,
            'percentage': 2.125,
            'leverage': 20.0,
            'liquidationPrice': 160000.0,
            'symbol': 'BTC/USDT:USDT'
        }
        
        # Golden ratio position pair 
        self.phi_long = copy.deepcopy(self.long_position)
        self.phi_long['contracts'] = 1.618
        self.phi_long['notional'] = 1.618 * 80000.0
        
        self.phi_short = copy.deepcopy(self.short_position)
        self.phi_short['contracts'] = 1.0
        self.phi_short['notional'] = 80000.0
    
    def test_analyze_long_position(self):
        """Test analyzing long position"""
        analysis = analyze_position(self.long_position)
        
        self.assertEqual(analysis['side'], 'long')
        self.assertEqual(analysis['contracts'], 0.618)
        self.assertEqual(analysis['entry_price'], 80000.0)
        self.assertEqual(analysis['mark_price'], 82000.0)
        self.assertEqual(analysis['price_move_percent'], 2.5)
        
        # Check Fibonacci levels
        fib_levels = analysis['fibonacci_levels']
        self.assertAlmostEqual(float(fib_levels['0']), 72000.0, places=1)
        self.assertAlmostEqual(float(fib_levels['0.618']), 77454.4, places=1)
        self.assertAlmostEqual(float(fib_levels['1.0']), 80000.0, places=1)
        
        # Check closest Fibonacci level
        # 82000 is closest to 84000 (1.618 level)
        self.assertEqual(analysis['closest_fibonacci_level'], '1.618')
    
    def test_analyze_short_position(self):
        """Test analyzing short position"""
        analysis = analyze_position(self.short_position)
        
        self.assertEqual(analysis['side'], 'short')
        self.assertEqual(analysis['contracts'], 1.0)
        self.assertEqual(analysis['entry_price'], 80000.0)
        self.assertEqual(analysis['mark_price'], 78300.0)
        self.assertEqual(analysis['price_move_percent'], 2.13)  # Rounded to 2 decimal places
        
        # Check closest Fibonacci level
        # 78300 is closest to 77454.4 (0.618 level)
        self.assertEqual(analysis['closest_fibonacci_level'], '0.618')
        
    def test_schumann_resonance_alignment(self):
        """Test position alignment with Schumann resonance"""
        # The short position is at 78300 which is the Schumann price
        analysis = analyze_position(self.short_position)
        
        # Check if closest level is 0.618, which has special significance
        # 78300 should be closest to 0.618 level (77454.4)
        self.assertEqual(analysis['closest_fibonacci_level'], '0.618')
        
        # Calculate distance to Schumann price
        schumann_price = 10000.0 * SCHUMANN_RESONANCE  # 78,300
        distance_to_schumann = abs(analysis['mark_price'] - schumann_price)
        
        # Should be very close to Schumann resonance
        self.assertLess(distance_to_schumann, 1.0, "Price should be at Schumann resonance")
        
    def test_golden_ratio_positions(self):
        """Test position sizes at Golden Ratio"""
        # Calculate phi resonance for the perfectly balanced positions
        resonance = calculate_phi_resonance([self.phi_long], [self.phi_short])
        
        # Should be exactly 1.0 (perfect alignment)
        self.assertEqual(resonance, 1.0, "Positions at Golden Ratio should have 1.0 resonance")


class TestSchumannIntegration(unittest.TestCase):
    """Test Schumann resonance integration with Fibonacci analysis"""
    
    def test_schumann_harmonic_series(self):
        """Test Schumann harmonic series alignment with Fibonacci sequence"""
        # Base Schumann resonance: 7.83 Hz
        # Schumann harmonics: 7.83, 14.3, 20.8, 27.3, 33.8 Hz
        
        # Convert to normalized series
        base = 7.83
        schumann_harmonics = [7.83, 14.3, 20.8, 27.3, 33.8]
        normalized_harmonics = [h/base for h in schumann_harmonics]
        
        # Compare with Fibonacci sequence ratios
        fibonacci_sequence = [1, 1, 2, 3, 5, 8, 13, 21]
        fibonacci_ratios = [fibonacci_sequence[i+1]/fibonacci_sequence[i] for i in range(len(fibonacci_sequence)-1)]
        
        # The first harmonics should approach PHI
        self.assertAlmostEqual(normalized_harmonics[1], 1.826, places=3) 
        
        # Calculate alignment between each harmonic and closest Fibonacci ratio
        alignments = []
        for harmonic in normalized_harmonics:
            closest_alignment = min(abs(harmonic - ratio) for ratio in fibonacci_ratios)
            alignments.append(closest_alignment)
            
        # Average alignment should be less than 0.5 (indicating correlation)
        avg_alignment = sum(alignments) / len(alignments)
        self.assertLess(avg_alignment, 0.5, "Schumann harmonics should correlate with Fibonacci ratios")


if __name__ == '__main__':
    unittest.main() 