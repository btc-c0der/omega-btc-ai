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
Simple BitGet Position Test
Tests the BitGet position monitoring functionality with test data
"""

import os
import sys
import json
import argparse
from datetime import datetime

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
        'leverage': '10',
        'liquidationPrice': '20000',
        'marginMode': 'cross',
        'collateral': '4000',
        'timestamp': str(int(datetime.now().timestamp() * 1000)),
        'cost': '30000',
        'initialMargin': '3000',
        'maxNotional': '150000',
        'margin': '3000',
        'maintenanceMargin': '300',
        'percentage': '6.67'
    },
    {
        'symbol': 'ETH/USDT:USDT',
        'side': 'short',
        'contracts': str(SCHUMANN_BASE),  # Schumann base frequency
        'notional': str(SCHUMANN_BASE * 2000),
        'entryPrice': '2000',
        'markPrice': '1900',
        'unrealizedPnl': '800',
        'leverage': '10',
        'liquidationPrice': '2500',
        'marginMode': 'isolated',
        'collateral': '1566',
        'timestamp': str(int(datetime.now().timestamp() * 1000)),
        'cost': '15660',
        'initialMargin': '1566',
        'maxNotional': '50000',
        'margin': '1566',
        'maintenanceMargin': '156.6',
        'percentage': '5.11'
    }
]

# Add complete comprehensive test data (Missing some fields for testing N/A handling)
COMPREHENSIVE_TEST_POSITIONS = [
    {
        'symbol': 'BTC/USDT:USDT',
        'side': 'long',
        'contracts': str(PHI),
        'notional': str(PHI * 30000),
        'entryPrice': '30000',
        'markPrice': '32000',
        'unrealizedPnl': '2000',
        'leverage': '10',
        # Missing liquidationPrice intentionally to test N/A handling
        'marginMode': 'cross',
        'collateral': '4000',
        # Missing timestamp intentionally
        'percentage': '6.67'
    },
    {
        'symbol': 'SOL/USDT:USDT',
        'side': 'short',
        'contracts': '21',  # Random number to test non-Fibonacci
        'notional': '2100',
        'entryPrice': '100',
        'markPrice': '95',
        'unrealizedPnl': '105',
        'leverage': '5',
        'liquidationPrice': '125',
        # Missing marginMode intentionally
        # Other fields intentionally missing to test N/A handling
    }
]

class BasicAnimationTest:
    """Tests basic animation components for BitGet monitoring"""
    
    def __init__(self):
        self.spinner_idx = 0
        self.wisdom_idx = 0
        self.phi_animation_state = 0
        
    def test_spinner_animation(self):
        """Test spinner animation frames"""
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        print("Testing spinner animation:")
        for i in range(len(frames)):
            frame = frames[self.spinner_idx]
            self.spinner_idx = (self.spinner_idx + 1) % len(frames)
            print(f"  Frame {i+1}: {frame}")
        return True
        
    def test_phi_symbol_animation(self):
        """Test phi symbol animation"""
        states = ['◯φ◯', '◉φ◯', '◯φ◉', '◉φ◉']
        print("\nTesting phi symbol animation:")
        for i in range(len(states)):
            symbol = states[self.phi_animation_state]
            self.phi_animation_state = (self.phi_animation_state + 1) % len(states)
            print(f"  State {i+1}: {symbol}")
        return True
        
    def test_wisdom_quotes(self):
        """Test RASTA wisdom quotes"""
        quotes = [
            "Position sizing aligned with φ creates harmonic trading",
            "When price meets Fibonacci, the universe reveals its plan",
            "Trade with the rhythm of Schumann, profit with the pattern of φ"
        ]
        print("\nTesting wisdom quotes:")
        for i in range(len(quotes)):
            quote = quotes[self.wisdom_idx]
            self.wisdom_idx = (self.wisdom_idx + 1) % len(quotes)
            print(f"  Quote {i+1}: \"{quote}\"")
        return True
        
    def test_progress_bar(self):
        """Test progress bar animation"""
        print("\nTesting progress bars:")
        values = [0, 0.25, 0.5, 0.75, 1.0]
        for val in values:
            fill_count = int(20 * min(val, 1.0))
            empty_count = 20 - fill_count
            bar = '█' * fill_count + '░' * empty_count
            print(f"  {val:.2f}: {bar} {int(val * 100)}%")
        return True
        
    def test_fibonacci_levels(self):
        """Test Fibonacci level generation"""
        print("\nTesting Fibonacci levels:")
        entry_price = 40000
        
        # Long position levels
        print("  Long position levels (entry $40000):")
        levels = {
            '0': entry_price,
            '0.236': entry_price * 1.0236,
            '0.382': entry_price * 1.0382,
            '0.5': entry_price * 1.05,
            '0.618': entry_price * 1.0618,
            '0.786': entry_price * 1.0786,
            '1.0': entry_price * 2.0,
            '1.618': entry_price * 2.618
        }
        for level, price in levels.items():
            print(f"    {level}: ${price:.2f}")
            
        # Short position levels
        print("\n  Short position levels (entry $40000):")
        levels = {
            '0': entry_price,
            '0.236': entry_price * 0.9764,
            '0.382': entry_price * 0.9618,
            '0.5': entry_price * 0.95,
            '0.618': entry_price * 0.9382,
            '0.786': entry_price * 0.9214,
            '1.0': entry_price * 0.5
        }
        for level, price in levels.items():
            print(f"    {level}: ${price:.2f}")
            
        return True
        
    def test_position_display(self):
        """Test position display formatting"""
        print("\nTesting position display:")
        
        position = TEST_POSITIONS[0]
        
        print(f"\n{'='*72}")
        print(f"POSITION: {position['symbol']} {position['side'].upper()}")
        print(f"{'='*72}")
        
        print(f"\n📊 POSITION DETAILS:")
        print(f"  Symbol:          {position['symbol']}")
        print(f"  Side:            {position['side'].upper()}")
        print(f"  Size:            {position['contracts']} contracts (${float(position['notional']):.2f})")
        print(f"  Entry Price:     ${float(position['entryPrice']):.2f}")
        print(f"  Current Price:   ${float(position['markPrice']):.2f}")
        
        # Calculate price movement
        price_diff = (float(position['markPrice']) - float(position['entryPrice'])) / float(position['entryPrice']) * 100
        print(f"  Price Movement:  {price_diff:.2f}%")
        
        # Simple progress bar for price movement
        bar_width = 20
        normalized_movement = min(max((price_diff + 5) / 10, 0), 1)  # -5% to +5% range
        fill_count = int(bar_width * normalized_movement)
        empty_count = bar_width - fill_count
        bar = '█' * fill_count + '░' * empty_count
        print(f"  {bar} {price_diff:.2f}%")
        
        print(f"  Unrealized PnL:  ${float(position['unrealizedPnl']):.2f}")
        
        print(f"\n⚠️ RISK METRICS:")
        print(f"  Leverage:        {position['leverage']}x")
        
        print(f"\nφ FIBONACCI LEVELS:")
        entry = float(position['entryPrice'])
        is_long = position['side'].lower() == 'long'
        
        # Display a few Fibonacci levels
        print(f"  ◉ Entry: ${entry:.2f}")
        if is_long:
            print(f"  0.618 Fib Ext: ${entry * 1.0618:.2f} (6.18% above)")
            print(f"  1.0 Fib Ext: ${entry * 2.0:.2f} (100.00% above)")
            print(f"  1.618 Fib Ext: ${entry * 2.618:.2f} (161.80% above)")
        else:
            print(f"  0.618 Fib Ret: ${entry * 0.9382:.2f} (6.18% below)")
            print(f"  0.786 Fib Ret: ${entry * 0.9214:.2f} (7.86% below)")
            print(f"  1.0 Fib Ret: ${entry * 0.5:.2f} (50.00% below)")
            
        return True
        
    def run_all_tests(self):
        """Run all component tests"""
        print("🧪 RASTA BitGet Monitor Component Tests\n")
        tests = [
            self.test_spinner_animation,
            self.test_phi_symbol_animation,
            self.test_wisdom_quotes,
            self.test_progress_bar,
            self.test_fibonacci_levels,
            self.test_position_display
        ]
        
        success = True
        for test in tests:
            try:
                result = test()
                if not result:
                    print(f"❌ Test failed: {test.__name__}")
                    success = False
            except Exception as e:
                print(f"❌ Test error in {test.__name__}: {str(e)}")
                success = False
                
        if success:
            print("\n✅ All component tests passed successfully!")
        else:
            print("\n❌ Some component tests failed")
            
        return success

class FullPositionTest(BasicAnimationTest):
    """Tests full position display with JSON field parsing"""
    
    def __init__(self, debug=False):
        super().__init__()
        self.debug = debug
        
    def test_position_parsing_complete(self):
        """Test parsing of all JSON fields for positions"""
        print("\nTesting complete position JSON parsing:")
        
        position = TEST_POSITIONS[0]
        
        print(f"\n{'='*72}")
        print(f"COMPLETE POSITION: {position['symbol']} {position['side'].upper()}")
        print(f"{'='*72}")
        
        # Standard fields
        print(f"\n📊 POSITION DETAILS:")
        print(f"  Symbol:          {position['symbol']}")
        print(f"  Side:            {position['side'].upper()}")
        print(f"  Size:            {position['contracts']} contracts (${float(position['notional']):.2f})")
        print(f"  Entry Price:     ${float(position['entryPrice']):.2f}")
        print(f"  Current Price:   ${float(position['markPrice']):.2f}")
        
        # Price movement
        price_diff = (float(position['markPrice']) - float(position['entryPrice'])) / float(position['entryPrice']) * 100
        print(f"  Price Movement:  {price_diff:.2f}%")
        
        print(f"  Unrealized PnL:  ${float(position['unrealizedPnl']):.2f}")
        
        # Extended JSON fields
        print(f"\n🔍 DETAILED DATA:")
        print(f"  Margin Mode:     {position.get('marginMode', 'N/A')}")
        print(f"  Collateral:      {position.get('collateral', 'N/A')}")
        print(f"  Timestamp:       {position.get('timestamp', 'N/A')}")
        print(f"  Cost:            {position.get('cost', 'N/A')}")
        print(f"  Initial Margin:  {position.get('initialMargin', 'N/A')}")
        print(f"  Margin:          {position.get('margin', 'N/A')}")
        print(f"  Maint. Margin:   {position.get('maintenanceMargin', 'N/A')}")
        print(f"  Max Notional:    {position.get('maxNotional', 'N/A')}")
        
        # Risk metrics
        print(f"\n⚠️ RISK METRICS:")
        print(f"  Leverage:        {position.get('leverage', 'N/A')}x")
        print(f"  Liquidation:     ${float(position.get('liquidationPrice', 0)):.2f}")
        
        return True
        
    def test_position_parsing_missing(self):
        """Test parsing of position with missing fields (N/A handling)"""
        print("\nTesting position JSON parsing with missing fields:")
        
        position = COMPREHENSIVE_TEST_POSITIONS[1]
        
        print(f"\n{'='*72}")
        print(f"PARTIAL POSITION: {position['symbol']} {position['side'].upper()}")
        print(f"{'='*72}")
        
        # Standard fields
        print(f"\n📊 POSITION DETAILS:")
        print(f"  Symbol:          {position['symbol']}")
        print(f"  Side:            {position['side'].upper()}")
        print(f"  Size:            {position['contracts']} contracts (${float(position['notional']):.2f})")
        print(f"  Entry Price:     ${float(position['entryPrice']):.2f}")
        print(f"  Current Price:   ${float(position['markPrice']):.2f}")
        
        # Extended JSON fields with N/A handling
        print(f"\n🔍 DETAILED DATA:")
        print(f"  Margin Mode:     {position.get('marginMode', 'N/A')}")
        print(f"  Collateral:      {position.get('collateral', 'N/A')}")
        print(f"  Timestamp:       {position.get('timestamp', 'N/A')}")
        print(f"  Cost:            {position.get('cost', 'N/A')}")
        print(f"  Initial Margin:  {position.get('initialMargin', 'N/A')}")
        print(f"  Margin:          {position.get('margin', 'N/A')}")
        print(f"  Maint. Margin:   {position.get('maintenanceMargin', 'N/A')}")
        print(f"  Max Notional:    {position.get('maxNotional', 'N/A')}")
        
        return True
        
    def test_field_coverage(self):
        """Test field coverage by comparing against expected fields"""
        print("\nTesting field coverage against expected API fields:")
        
        # List of expected fields from BitGet API
        expected_fields = [
            'symbol', 'side', 'contracts', 'notional', 
            'entryPrice', 'markPrice', 'unrealizedPnl', 
            'leverage', 'liquidationPrice', 'marginMode', 
            'collateral', 'timestamp', 'cost', 'initialMargin',
            'maxNotional', 'margin', 'maintenanceMargin', 'percentage'
        ]
        
        # Check coverage in our test positions
        present_fields = set()
        for position in TEST_POSITIONS:
            for field in position.keys():
                present_fields.add(field)
        
        # Report coverage
        print("Field coverage in test data:")
        for field in expected_fields:
            if field in present_fields:
                print(f"  ✅ {field}")
            else:
                print(f"  ❌ {field}")
                
        # Check for any fields in test data not in expected list
        for field in present_fields:
            if field not in expected_fields:
                print(f"  ⚠️ Extra field in test data: {field}")
                
        coverage_pct = len(present_fields) / len(expected_fields) * 100
        print(f"\nCoverage: {coverage_pct:.1f}% of expected fields")
        
        return True

    def run_all_tests(self):
        """Run all JSON field coverage tests"""
        print("🧪 RASTA BitGet Position JSON Field Tests\n")
        tests = [
            self.test_position_parsing_complete,
            self.test_position_parsing_missing,
            self.test_field_coverage
        ]
        
        success = True
        for test in tests:
            try:
                result = test()
                if not result:
                    print(f"❌ Test failed: {test.__name__}")
                    success = False
            except Exception as e:
                print(f"❌ Test error in {test.__name__}: {str(e)}")
                success = False
                
        if success:
            print("\n✅ All JSON field coverage tests passed successfully!")
        else:
            print("\n❌ Some JSON field coverage tests failed")
            
        return success

def test_position_change_detection():
    """Test position change detection functionality"""
    print("\n🧪 Testing Position Change Detection\n")
    
    # Initial positions
    previous_positions = {
        f"{p['symbol']}:{p['side']}": p for p in TEST_POSITIONS
    }
    
    # Modified positions for next update
    modified_positions = [
        {
            'symbol': 'BTC/USDT:USDT',
            'side': 'long',
            'contracts': str(float(TEST_POSITIONS[0]['contracts']) * 1.1),  # Increased size
            'notional': str(float(TEST_POSITIONS[0]['notional']) * 1.1),
            'entryPrice': TEST_POSITIONS[0]['entryPrice'],
            'markPrice': str(float(TEST_POSITIONS[0]['markPrice']) * 1.05),  # Price increased
            'unrealizedPnl': str(float(TEST_POSITIONS[0]['unrealizedPnl']) * 1.2),  # More profit
            'leverage': TEST_POSITIONS[0]['leverage']
        },
        # ETH position removed (closed)
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
        }
    ]
    
    # Convert to dictionary for comparison
    current_positions = {
        f"{p['symbol']}:{p['side']}": p for p in modified_positions
    }
    
    # Detect changes
    new_positions = []
    closed_positions = []
    changed_positions = []
    
    # Find new and modified positions
    for key, position in current_positions.items():
        if key not in previous_positions:
            new_positions.append(position)
        else:
            prev_position = previous_positions[key]
            # Check for significant changes
            if float(position['contracts']) != float(prev_position['contracts']):
                changed_positions.append((prev_position, position))
    
    # Find closed positions
    for key, position in previous_positions.items():
        if key not in current_positions:
            closed_positions.append(position)
    
    # Display the detected changes
    if new_positions:
        print("🟢 NEW POSITIONS:")
        for position in new_positions:
            print(f"  {position['symbol']} {position['side'].upper()}:")
            print(f"    Size: {position['contracts']}")
            print(f"    Entry: ${float(position['entryPrice']):.2f}")
            print()
    
    if closed_positions:
        print("🟥 CLOSED POSITIONS:")
        for position in closed_positions:
            print(f"  {position['symbol']} {position['side'].upper()}:")
            print(f"    Size: {position['contracts']}")
            print(f"    Entry: ${float(position['entryPrice']):.2f}")
            print()
    
    if changed_positions:
        print("📊 CHANGED POSITIONS:")
        for prev, curr in changed_positions:
            print(f"  {curr['symbol']} {curr['side'].upper()}:")
            
            # Size change
            prev_size = float(prev['contracts'])
            curr_size = float(curr['contracts'])
            size_diff = curr_size - prev_size
            size_pct = (size_diff / prev_size * 100) if prev_size > 0 else 0
            size_sign = "+" if size_diff >= 0 else ""
            print(f"    Size: {prev_size} → {curr_size} ({size_sign}{size_diff:.4f} / {size_sign}{size_pct:.2f}%)")
            
            # PnL change
            prev_pnl = float(prev['unrealizedPnl'])
            curr_pnl = float(curr['unrealizedPnl'])
            pnl_diff = curr_pnl - prev_pnl
            pnl_sign = "+" if pnl_diff >= 0 else ""
            print(f"    PnL: ${prev_pnl:.2f} → ${curr_pnl:.2f} ({pnl_sign}${pnl_diff:.2f})")
            print()
            
    # Validate the change detection
    success = True
    if len(new_positions) != 1:
        print(f"❌ Expected 1 new position, found {len(new_positions)}")
        success = False
    if len(closed_positions) != 1:
        print(f"❌ Expected 1 closed position, found {len(closed_positions)}")
        success = False
    if len(changed_positions) != 1:
        print(f"❌ Expected 1 changed position, found {len(changed_positions)}")
        success = False
        
    if success:
        print("✅ Position change detection test passed!")
    else:
        print("❌ Position change detection test failed")
        
    return success

def main():
    """Main function to run test script"""
    parser = argparse.ArgumentParser(description='Simple BitGet Position Test')
    parser.add_argument('--component', action='store_true', help='Run component tests')
    parser.add_argument('--changes', action='store_true', help='Run position change detection test')
    parser.add_argument('--json', action='store_true', help='Run JSON field coverage tests')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--debug', action='store_true', help='Show debug info')
    
    args = parser.parse_args()
    
    # Default to all tests if no specific test is requested
    run_all = args.all or not (args.component or args.changes or args.json)
    
    success = True
    
    if run_all or args.component:
        animation_test = BasicAnimationTest()
        component_success = animation_test.run_all_tests()
        success = success and component_success
        
    if run_all or args.changes:
        change_success = test_position_change_detection()
        success = success and change_success

    if run_all or args.json:
        json_test = FullPositionTest(debug=args.debug)
        json_success = json_test.run_all_tests()
        success = success and json_success
        
    # Exit with status code
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 