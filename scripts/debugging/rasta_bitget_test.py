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
RASTA BitGet Monitor Test Script
Runs the BitGet monitoring functionality in test mode with mock data
"""

import os
import sys
import json
import argparse
from datetime import datetime
import time

# Constants
PHI = 1.618034  # Golden Ratio
INV_PHI = 0.618034  # Inverse Golden Ratio
SCHUMANN_BASE = 7.83  # Earth's base frequency (Hz)
SCHUMANN_HARMONICS = [14.3, 20.8, 27.3, 33.8]  # Higher harmonics (Hz)

# Test data - positions that align with Fibonacci and Schumann
TEST_POSITIONS = [
    {
        'symbol': 'BTC/USDT:USDT',
        'side': 'long',
        'contracts': str(PHI),  # Golden Ratio size
        'notional': str(PHI * 30000),
        'entryPrice': '30000',
        'markPrice': '32000',
        'unrealizedPnl': '2000',
        'leverage': '10'
    },
    {
        'symbol': 'ETH/USDT:USDT',
        'side': 'short',
        'contracts': str(SCHUMANN_BASE),  # Schumann base frequency
        'notional': str(SCHUMANN_BASE * 2000),
        'entryPrice': '2000',
        'markPrice': '1900',
        'unrealizedPnl': '800',
        'leverage': '10'
    },
    {
        'symbol': 'SOL/USDT:USDT',
        'side': 'long',
        'contracts': '0.000000001',  # Quantum position
        'notional': '0.0001',
        'entryPrice': '100',
        'markPrice': '101',
        'unrealizedPnl': '0.000000001',
        'leverage': '21'
    }
]

# Modified position data to test change detection
MODIFIED_POSITIONS = [
    {
        'symbol': 'BTC/USDT:USDT',
        'side': 'long',
        'contracts': str(PHI * 1.1),  # Increased size
        'notional': str(PHI * 1.1 * 30000),
        'entryPrice': '30000',
        'markPrice': '33000',  # Price increased
        'unrealizedPnl': '3000',  # More profit
        'leverage': '10'
    },
    # ETH position closed (removed)
    # New position added
    {
        'symbol': 'LINK/USDT:USDT',
        'side': 'long',
        'contracts': '13',  # Fibonacci number
        'notional': '13000',
        'entryPrice': '10',
        'markPrice': '10.8',
        'unrealizedPnl': '10.4',
        'leverage': '5'
    },
    {
        'symbol': 'SOL/USDT:USDT',
        'side': 'long',
        'contracts': '0.000000001',  # Unchanged
        'notional': '0.0001',
        'entryPrice': '100',
        'markPrice': '101',
        'unrealizedPnl': '0.000000001',
        'leverage': '21'
    }
]

class TestingError(Exception):
    """Custom exception for test-specific errors"""
    pass

try:
    # Try to import the actual monitor
    from simple_bitget_positions import RastaBitgetMonitor
except ImportError:
    # Create a stub if import fails
    class RastaBitgetMonitor:
        def __init__(self, *args, **kwargs):
            self.debug = kwargs.get('debug', False)
            self.spinner_idx = 0
            self.wisdom_idx = 0
            self.phi_animation_state = 0
            
        def run(self, *args, **kwargs):
            print("Error: Cannot import RastaBitgetMonitor from simple_bitget_positions")
            print("This test script requires simple_bitget_positions.py to be present")
            
        def get_spinner_frame(self):
            """Stub spinner animation"""
            frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
            self.spinner_idx = (self.spinner_idx + 1) % len(frames)
            return frames[self.spinner_idx]
            
        def animate_phi_symbol(self):
            """Stub phi symbol animation"""
            states = ['◯φ◯', '◉φ◯', '◯φ◉', '◉φ◉']
            self.phi_animation_state = (self.phi_animation_state + 1) % len(states)
            return states[self.phi_animation_state]
            
        def get_wisdom_quote(self):
            """Stub wisdom quotes"""
            quotes = [
                "Position sizing aligned with φ creates harmonic trading",
                "When price meets Fibonacci, the universe reveals its plan",
                "Trade with the rhythm of Schumann, profit with the pattern of φ"
            ]
            self.wisdom_idx = (self.wisdom_idx + 1) % len(quotes)
            return quotes[self.wisdom_idx]
            
        def animate_progress_bar(self, value, max_value=1.0, width=50):
            """Stub progress bar animation"""
            fill_count = int(width * min(value / max_value, 1.0))
            empty_count = width - fill_count
            bar = '█' * fill_count + '░' * empty_count
            return f"{bar} {int(value * 100)}%"
            
        def generate_fibonacci_levels(self, entry_price, is_long=True):
            """Stub Fibonacci level generation"""
            levels = {}
            if is_long:
                levels['0'] = entry_price
                levels['0.236'] = entry_price * 1.0236
                levels['0.382'] = entry_price * 1.0382
                levels['0.5'] = entry_price * 1.05
                levels['0.618'] = entry_price * 1.0618
                levels['0.786'] = entry_price * 1.0786
                levels['1.0'] = entry_price * 2.0
                levels['1.618'] = entry_price * 2.618
            else:
                levels['0'] = entry_price
                levels['0.236'] = entry_price * 0.9764
                levels['0.382'] = entry_price * 0.9618
                levels['0.5'] = entry_price * 0.95
                levels['0.618'] = entry_price * 0.9382
                levels['0.786'] = entry_price * 0.9214
                levels['1.0'] = entry_price * 0.5
            return levels

def run_test(test_mode, change_test=False, anim_test=False, show_output=True):
    """Run tests on the RASTA BitGet Monitor using mock data"""
    
    # Create a custom monitor class for testing
    class TestRastaBitgetMonitor(RastaBitgetMonitor):
        def __init__(self, test_mode=True, mock_data=None, *args, **kwargs):
            super().__init__(debug=True, *args, **kwargs)
            self.test_mode = test_mode
            self.mock_data = mock_data or TEST_POSITIONS
            self.test_iteration = 0
            self.test_max_iterations = 3 if change_test else 1
            
        def connect(self):
            """Mock connection in test mode"""
            if self.test_mode:
                print("✅ TEST MODE: Connected to BitGet Test Environment")
                return True
            return super().connect()
            
        def get_positions(self):
            """Return mock position data in test mode"""
            if not self.test_mode:
                return super().get_positions()
                
            if change_test and self.test_iteration == 1:
                # Return modified positions on second iteration to test change detection
                return MODIFIED_POSITIONS
                
            # Default test positions
            return self.mock_data
            
        def run(self, interval=5):
            """Run once or multiple times in test mode"""
            if not self.test_mode:
                return super().run(interval)
                
            print(f"🧪 Running in TEST MODE with {'change detection' if change_test else 'standard'} test")
            
            try:
                for i in range(self.test_max_iterations):
                    self.test_iteration = i
                    if i > 0:
                        print(f"\n\n{'='*80}\nTEST ITERATION {i+1}\n{'='*80}\n")
                    positions = self.run_once()
                    
                    if i < self.test_max_iterations - 1:
                        print(f"\n⏳ Waiting {interval} seconds before next test iteration...")
                        time.sleep(interval)
                        
                print("\n✅ TEST COMPLETED SUCCESSFULLY")
                return True
                
            except Exception as e:
                print(f"\n❌ TEST FAILED: {str(e)}")
                import traceback
                traceback.print_exc()
                return False
            
        def run_component_tests(self):
            """Run specific component tests"""
            print("\n🧪 COMPONENT TEST MODE\n")
            
            # Test spinner animation
            print("Testing spinner animation:")
            for _ in range(5):
                print(f"  {self.get_spinner_frame()}", end=" ")
            print("\n")
            
            # Test phi symbol animation
            print("Testing phi symbol animation:")
            for _ in range(4):
                print(f"  {self.animate_phi_symbol()}", end=" ")
            print("\n")
            
            # Test wisdom quotes
            print("Testing wisdom quotes:")
            for _ in range(3):
                print(f"  \"{self.get_wisdom_quote()}\"")
            print()
            
            # Test progress bars
            print("Testing progress bars:")
            values = [0.1, 0.5, 0.8, 1.0]
            for val in values:
                print(f"  {val:.1f}: {self.animate_progress_bar(val)}")
            print()
            
            # Test Fibonacci calculations
            print("Testing Fibonacci calculations:")
            entry = 40000
            current = 42000
            print(f"  Entry: ${entry}, Current: ${current}")
            print("  Fibonacci levels (long):")
            levels = self.generate_fibonacci_levels(entry, True)
            for level, price in levels.items():
                print(f"    {level}: ${price:.2f}")
            print()
            
            return True
    
    # Create and run the test monitor
    test_args = {
        'test_mode': test_mode
    }
    
    monitor = TestRastaBitgetMonitor(**test_args)
    
    if anim_test:
        return monitor.run_component_tests()
    else:
        return monitor.run(interval=2)

def main():
    """Main function to run test script"""
    parser = argparse.ArgumentParser(description='RASTA BitGet Monitor Test Script')
    parser.add_argument('--test', action='store_true', help='Run in test mode with mock data')
    parser.add_argument('--change', action='store_true', help='Test position change detection')
    parser.add_argument('--anim', action='store_true', help='Test animation components')
    parser.add_argument('--real', action='store_true', help='Run with real BitGet API')
    parser.add_argument('--interval', type=int, default=2, help='Refresh interval in seconds')
    
    args = parser.parse_args()
    
    # Default to test mode if no specific mode is requested
    test_mode = not args.real if args.real else True
    
    # Run tests
    success = run_test(
        test_mode=test_mode,
        change_test=args.change,
        anim_test=args.anim
    )
    
    # Exit with status code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 