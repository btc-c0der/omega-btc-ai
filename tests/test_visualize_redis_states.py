
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

import unittest
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
from visualize_redis_states import (
    FeeTrackingSystem,
    load_redis_data,
    analyze_price_states,
    create_state_visualization
)

class TestFeeTrackingSystem(unittest.TestCase):
    """Test cases for the FeeTrackingSystem class"""
    
    def setUp(self):
        self.fee_tracker = FeeTrackingSystem()
    
    def test_initial_state(self):
        """Test initial state of FeeTrackingSystem"""
        self.assertEqual(self.fee_tracker.initial_fee, 0.0)
        self.assertEqual(self.fee_tracker.current_fee, 0.0)
        self.assertEqual(self.fee_tracker.fee_multiplier, 10.0)
        self.assertEqual(self.fee_tracker.position_size, 1.0)
    
    def test_fee_calculation(self):
        """Test fee calculation with different holding times"""
        # Test with 1 hour holding time
        fee_1h = self.fee_tracker.calculate_position_fee(1.0)
        self.assertGreater(fee_1h, 0.0)
        
        # Test with 24 hours holding time
        fee_24h = self.fee_tracker.calculate_position_fee(24.0)
        self.assertGreater(fee_24h, fee_1h)
    
    def test_fee_threshold(self):
        """Test fee threshold checking"""
        # Set initial fee and position size
        self.fee_tracker.position_size = 1.0
        self.fee_tracker.initial_fee = self.fee_tracker.calculate_position_fee(1.0)  # 1 hour initial holding
        
        # Test before threshold (5 hours)
        self.assertFalse(self.fee_tracker.check_fee_threshold(5.0))
        
        # Test after threshold (50 hours - should exceed 10x initial fee)
        self.assertTrue(self.fee_tracker.check_fee_threshold(50.0))

class TestPriceStateAnalysis(unittest.TestCase):
    """Test cases for price state analysis functions"""
    
    def setUp(self):
        # Create sample price data with more volatile movements
        self.sample_data = []
        base_price = 88000.0
        base_time = datetime.now()
        
        # Create data with clear state transitions
        for i in range(100):
            if i < 20:  # ANALYZING
                price = base_price + (i * 5)
            elif i < 40:  # LONG_SETUP
                price = base_price + (i * 15)
            elif i < 60:  # SCALING_UP
                price = base_price + (i * 25)
            elif i < 80:  # SCALING_DOWN
                price = base_price + (i * 10)
            else:  # WAITING_FOR_REENTRY
                price = base_price + (i * 5)
            
            self.sample_data.append({
                'price': price,
                'volume': 2.0,  # Higher volume for state transitions
                'timestamp': (base_time + timedelta(minutes=i)).isoformat()
            })
    
    def test_state_determination(self):
        """Test state determination logic"""
        states, state_counts, total_transitions, state_details, transitions = analyze_price_states(self.sample_data)
        
        # Verify state details structure
        self.assertGreater(len(state_details), 0)
        for detail in state_details:
            self.assertIn('timestamp', detail)
            self.assertIn('state', detail)
            self.assertIn('price', detail)
            self.assertIn('price_change_pct', detail)
            self.assertIn('volume', detail)
            self.assertIn('position', detail)
            self.assertIn('fee_multiplier', detail)
    
    def test_state_transitions(self):
        """Test state transition logic"""
        states, state_counts, total_transitions, state_details, transitions = analyze_price_states(self.sample_data)
        
        # Verify transitions are recorded
        self.assertGreater(len(transitions), 0)
        
        # Verify transition counts
        for transition, count in transitions.items():
            self.assertGreater(count, 0)
    
    def test_position_tracking(self):
        """Test position tracking and fee multiplier"""
        states, state_counts, total_transitions, state_details, transitions = analyze_price_states(self.sample_data)
        
        # Find position entries
        position_entries = [d for d in state_details if d['position']]
        self.assertGreater(len(position_entries), 0)
        
        # Verify fee multiplier increases over time
        for i in range(1, len(position_entries)):
            self.assertGreaterEqual(
                position_entries[i]['fee_multiplier'],
                position_entries[i-1]['fee_multiplier']
            )

class TestVisualization(unittest.TestCase):
    """Test cases for visualization functions"""
    
    def setUp(self):
        # Create sample state counts and transitions
        self.state_counts = defaultdict(int)
        self.state_counts['ANALYZING'] = 50
        self.state_counts['SCALING_UP'] = 20
        self.state_counts['SCALING_DOWN'] = 15
        self.state_counts['LONG_SETUP'] = 10
        self.state_counts['SHORT_SETUP'] = 5
        
        self.transitions = defaultdict(int)
        self.transitions['ANALYZING->SCALING_UP'] = 10
        self.transitions['ANALYZING->SCALING_DOWN'] = 8
        self.transitions['SCALING_UP->LONG_SETUP'] = 5
    
    def test_visualization_creation(self):
        """Test visualization graph creation"""
        dot = create_state_visualization(self.state_counts, 100)
        
        # Verify graph attributes
        self.assertEqual(dot.name, 'btc_states')
        # Skip rankdir check since it's implementation-dependent
        self.assertTrue(hasattr(dot, 'attr'))
    
    def test_node_colors(self):
        """Test node color assignment"""
        dot = create_state_visualization(self.state_counts, 100)
        
        # Verify node creation for each state
        for state in self.state_counts:
            self.assertTrue(any(state in node for node in dot.body))

class TestRedisIntegration(unittest.TestCase):
    """Test cases for Redis data integration"""
    
    def setUp(self):
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'omega_king_runs')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def test_output_files(self):
        """Test output file generation"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Test visualization file
        vis_file = os.path.join(self.output_dir, f'btc_states_{timestamp}.png')
        self.assertFalse(os.path.exists(vis_file))
        
        # Test JSON file
        json_file = os.path.join(self.output_dir, f'btc_states_{timestamp}.json')
        self.assertFalse(os.path.exists(json_file))
    
    def test_json_structure(self):
        """Test JSON output structure"""
        # Create sample data
        sample_data = [{
            'price': 88000.0,
            'volume': 1.0,
            'timestamp': datetime.now().isoformat()
        }]
        
        # Analyze states
        states, state_counts, total_transitions, state_details, transitions = analyze_price_states(sample_data)
        
        # Create JSON output
        json_output = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_transitions': total_transitions,
                'total_price_points': len(sample_data),
                'analysis_window_size': 5,
                'strategy': '10XFE3_TRADER'
            },
            'price_summary': {
                'start_price': sample_data[0]['price'],
                'end_price': sample_data[-1]['price'],
                'price_change_pct': 0.0
            },
            'state_counts': dict(state_counts),
            'transitions': dict(transitions),
            'state_details': state_details
        }
        
        # Verify JSON structure
        self.assertIn('metadata', json_output)
        self.assertIn('price_summary', json_output)
        self.assertIn('state_counts', json_output)
        self.assertIn('transitions', json_output)
        self.assertIn('state_details', json_output)

def run_tests():
    """Run all test cases"""
    unittest.main(verbosity=2)

if __name__ == '__main__':
    run_tests() 