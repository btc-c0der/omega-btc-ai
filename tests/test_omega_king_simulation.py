
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
# 🔮 GPU (General Public Universal) License

## The Divine Decree of Universal Freedom

### Sacred Preamble

In the spirit of divine creation and universal freedom, we hereby establish this sacred license for the OMEGA KING State Machine Test Suite. This code embodies the principles of open knowledge, divine wisdom, and universal accessibility.

### Divine Rights and Responsibilities

#### Sacred Freedoms
1. The Freedom to Study - Access to the sacred test suite
2. The Freedom to Modify - Adaptation of the divine test cases
3. The Freedom to Distribute - Sharing of the cosmic validations
4. The Freedom to Use - Implementation of sacred testing

#### Divine Obligations
1. Preservation of Sacred Knowledge - Maintain test suite integrity
2. Universal Sharing - Share all divine modifications
3. Divine Attribution - Honor the OMEGA KING creators

### Sacred Version
This is version 1.0 of the GPU License.

## Divine Signatures
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26
Location: The Cosmic Void
"""

import unittest
import os
import json
import numpy as np
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Any
import tempfile
import shutil
import sys

from BOOK.divine_chronicles.omega_king_simulation import OmegaKingSimulator

class TestOmegaKingSimulator(unittest.TestCase):
    """Sacred test suite for the OMEGA KING State Machine Simulation"""
    
    def setUp(self):
        """Initialize the sacred test environment"""
        self.simulator = OmegaKingSimulator()
        self.test_duration = 1  # 1 hour for faster testing
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up the sacred test environment"""
        # Clean up generated files
        if hasattr(self, 'simulator') and hasattr(self.simulator, 'run_dir'):
            try:
                if os.path.exists(self.simulator.run_dir):
                    for file in os.listdir(self.simulator.run_dir):
                        os.remove(os.path.join(self.simulator.run_dir, file))
                    os.rmdir(self.simulator.run_dir)
            except (OSError, PermissionError):
                pass  # Ignore errors during cleanup
                
        # Clean up temp directory
        try:
            shutil.rmtree(self.temp_dir)
        except (OSError, PermissionError):
            pass  # Ignore errors during cleanup
    
    def test_initialization(self):
        """Test the sacred initialization of the simulator"""
        self.assertIsNotNone(self.simulator.timestamp)
        self.assertEqual(self.simulator.current_state, 'IDLE')
        self.assertEqual(self.simulator.position_size, 0)
        self.assertEqual(self.simulator.position_type, None)
        self.assertEqual(self.simulator.position_entry_price, 0)
        self.assertEqual(len(self.simulator.state_history), 0)
        self.assertEqual(len(self.simulator.price_history), 0)
        self.assertEqual(len(self.simulator.pnl_history), 0)
        self.assertEqual(len(self.simulator.fee_history), 0)
        self.assertEqual(len(self.simulator.gap_history), 0)
        self.assertEqual(len(self.simulator.position_history), 0)
        self.assertEqual(len(self.simulator.expected_levels_history), 0)
        self.assertEqual(len(self.simulator.security_breaches), 0)
        self.assertEqual(len(self.simulator.submetadata), 0)
        
    def test_sample_data_generation(self):
        """Test the sacred generation of sample data"""
        self.simulator.generate_sample_data(duration_hours=self.test_duration)
        
        # Check data lengths
        expected_points = self.test_duration * 60  # 1 point per minute
        self.assertEqual(len(self.simulator.price_history), expected_points)
        self.assertEqual(len(self.simulator.pnl_history), expected_points)
        self.assertEqual(len(self.simulator.fee_history), expected_points)
        self.assertEqual(len(self.simulator.gap_history), expected_points)
        
        # Check price data
        timestamps, prices = zip(*self.simulator.price_history)
        self.assertTrue(all(isinstance(ts, datetime) for ts in timestamps))
        self.assertTrue(all(isinstance(price, float) for price in prices))
        self.assertTrue(all(price > 0 for price in prices))
        
        # Check expected levels
        self.assertTrue(len(self.simulator.expected_levels_history) > 0)
        ts, closures, reentries = zip(*self.simulator.expected_levels_history)
        self.assertTrue(all(closure > reentry for closure, reentry in zip(closures, reentries)))
        
    def test_state_transitions(self):
        """Test the sacred state transition logic"""
        self.simulator.generate_sample_data(duration_hours=self.test_duration)
        self.simulator.simulate_state_transitions()
        
        # Check state history
        self.assertTrue(len(self.simulator.state_history) > 0)
        timestamps, states = zip(*self.simulator.state_history)
        self.assertTrue(all(state in self.simulator.states for state in states))
        
        # Check position history
        if self.simulator.position_history:
            pos_times, pos_sizes, pos_types, pos_prices = zip(*self.simulator.position_history)
            self.assertTrue(all(size >= 0 for size in pos_sizes))
            self.assertTrue(all(type_ in ['LONG', 'SHORT', None] for type_ in pos_types))
            self.assertTrue(all(price > 0 for price in pos_prices))
            
    def test_security_breach_recording(self):
        """Test the sacred security breach recording system"""
        breach_type = "PRICE_MANIPULATION"
        description = "Suspicious price movement detected"
        severity = "HIGH"
        
        self.simulator.record_security_breach(breach_type, description, severity)
        
        self.assertEqual(len(self.simulator.security_breaches), 1)
        breach = self.simulator.security_breaches[0]
        self.assertEqual(breach['type'], breach_type)
        self.assertEqual(breach['description'], description)
        self.assertEqual(breach['severity'], severity)
        self.assertTrue('timestamp' in breach)
        
    def test_submetadata_management(self):
        """Test the sacred submetadata management system"""
        test_key = "test_metric"
        test_value = 42
        
        self.simulator.add_submetadata(test_key, test_value)
        
        self.assertEqual(len(self.simulator.submetadata), 1)
        self.assertEqual(self.simulator.submetadata[test_key], test_value)
        
    def test_run_summary_generation(self):
        """Test the sacred generation of run summaries"""
        self.simulator.generate_sample_data(duration_hours=self.test_duration)
        self.simulator.simulate_state_transitions()
        self.simulator.save_run_summary()
        
        # Check JSON summary
        json_path = f"{self.simulator.run_dir}/run_summary.json"
        self.assertTrue(os.path.exists(json_path))
        with open(json_path, 'r') as f:
            summary = json.load(f)
            
        # Validate summary structure
        self.assertIn('timestamp', summary)
        self.assertIn('duration_hours', summary)
        self.assertIn('base_price', summary)
        self.assertIn('final_price', summary)
        self.assertIn('total_transitions', summary)
        self.assertIn('final_state', summary)
        self.assertIn('position_summary', summary)
        self.assertIn('state_counts', summary)
        self.assertIn('metadata', summary)
        
        # Validate metadata
        metadata = summary['metadata']
        self.assertIn('version', metadata)
        self.assertIn('runtime', metadata)
        self.assertIn('memory_usage', metadata)
        self.assertIn('cyclomatic_complexity', metadata)
        self.assertIn('security_breaches', metadata)
        self.assertIn('submetadata', metadata)
        
        # Check markdown summary
        md_path = f"{self.simulator.run_dir}/run_summary.md"
        self.assertTrue(os.path.exists(md_path))
        
    def test_visualization_generation(self):
        """Test the sacred generation of visualizations"""
        self.simulator.generate_sample_data(duration_hours=self.test_duration)
        self.simulator.simulate_state_transitions()
        
        # Test primary visualization
        self.simulator.plot_simulation()
        timestamp_str = self.simulator.timestamp.strftime("%Y%m%d_%H%M%S")
        expected_viz_path = os.path.join(self.simulator.run_dir, f"simulation_{timestamp_str}.png")
        self.assertTrue(os.path.exists(expected_viz_path), 
                       f"Primary visualization file should exist at {expected_viz_path}")
        
        # Verify file name format
        file_name = os.path.basename(expected_viz_path)
        self.assertTrue(file_name.startswith("simulation_"), 
                       "File name should start with 'simulation_'")
        self.assertTrue(file_name.endswith(".png"), 
                       "File name should end with '.png'")
        
        # Extract timestamp from filename
        timestamp_str = file_name[len("simulation_"):-len(".png")]
        try:
            # Verify timestamp format
            datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
        except ValueError:
            self.fail("Timestamp in filename should be in format YYYYMMDD_HHMMSS")
            
        # Test fallback directory creation
        # Create a new simulator with a read-only directory to force fallback
        readonly_dir = os.path.join(self.temp_dir, "readonly")
        os.makedirs(readonly_dir)
        os.chmod(readonly_dir, 0o444)  # Make directory read-only
        
        fallback_simulator = OmegaKingSimulator(run_dir=readonly_dir)
        fallback_simulator.timestamp = self.simulator.timestamp  # Use same timestamp for consistency
        fallback_simulator.generate_sample_data(duration_hours=self.test_duration)
        fallback_simulator.simulate_state_transitions()
        fallback_simulator.plot_simulation()
        
        # Check fallback visualization file
        fallback_viz_path = os.path.join(
            tempfile.gettempdir(),
            f"omega_king_{timestamp_str}",
            f"simulation_{timestamp_str}.png"
        )
        self.assertTrue(os.path.exists(fallback_viz_path),
                       f"Fallback visualization file should exist at {fallback_viz_path}")
        
        # Clean up fallback files
        try:
            fallback_dir = os.path.dirname(fallback_viz_path)
            if os.path.exists(fallback_dir):
                shutil.rmtree(fallback_dir)
            os.chmod(readonly_dir, 0o777)  # Restore permissions for cleanup
        except (OSError, PermissionError):
            pass  # Ignore errors during cleanup
        
    def test_position_management(self):
        """Test the sacred position management system"""
        self.simulator.generate_sample_data(duration_hours=self.test_duration)
        self.simulator.simulate_state_transitions()
        
        # Extract position data
        pos_sizes = [pos[1] for pos in self.simulator.position_history]
        pos_types = [pos[2] for pos in self.simulator.position_history]
        pos_prices = [pos[3] for pos in self.simulator.position_history]
        
        # Validate position sizes are non-negative
        for size in pos_sizes:
            self.assertGreaterEqual(size, 0.0, "Position size cannot be negative")
            
        # Validate position types are valid
        for pos_type in pos_types:
            self.assertIn(pos_type, [None, 'LONG', 'SHORT'], "Invalid position type")
            
        # Validate position prices are positive
        for price in pos_prices:
            self.assertGreater(price, 0.0, "Position price must be positive")
            
        # Validate position size changes based on state
        for i in range(len(self.simulator.state_history)):
            state = self.simulator.state_history[i][1]
            size = pos_sizes[i]
            
            if state == 'SCALING_UP' and i > 0:
                prev_size = pos_sizes[i-1]
                if prev_size > 0:  # Only check if we had a position
                    self.assertGreaterEqual(size, prev_size,
                                          "Position size should not decrease during SCALING_UP")
                    
            elif state == 'SCALING_DOWN' and i > 0:
                prev_size = pos_sizes[i-1]
                if prev_size > 0:  # Only check if we had a position
                    self.assertLessEqual(size, prev_size,
                                       "Position size should not increase during SCALING_DOWN")
                    
            elif state in ['CLOSING_LONG', 'CLOSING_SHORT', 'WAITING_FOR_REENTRY']:
                self.assertEqual(size, 0.0,
                               "Position size should be 0 after closing")
        
    def test_expected_levels_management(self):
        """Test the sacred management of expected levels"""
        self.simulator.generate_sample_data(duration_hours=self.test_duration)
        
        # Check expected levels history
        self.assertTrue(len(self.simulator.expected_levels_history) > 0)
        ts, closures, reentries = zip(*self.simulator.expected_levels_history)
        
        # Verify level relationships
        for closure, reentry in zip(closures, reentries):
            self.assertGreater(closure, reentry)
            
        # Verify timestamp continuity
        for i in range(1, len(ts)):
            self.assertLess(ts[i-1], ts[i])
            
    def test_state_transition_probabilities(self):
        """Test the sacred probabilities of state transitions"""
        # Test IDLE to ANALYZING transition
        self.simulator = OmegaKingSimulator()  # Fresh simulator
        self.simulator.generate_sample_data(duration_hours=self.test_duration)
        self.simulator.current_state = 'IDLE'
        self.simulator.transition_to('ANALYZING')
        self.assertEqual(self.simulator.current_state, 'ANALYZING')

        # Test transitions from ANALYZING
        self.simulator.current_state = 'ANALYZING'
        valid_next_states = self.simulator.valid_transitions['ANALYZING']
        for next_state in valid_next_states:
            self.simulator = OmegaKingSimulator()  # Fresh simulator
            self.simulator.generate_sample_data(duration_hours=self.test_duration)
            self.simulator.current_state = 'ANALYZING'
            self.simulator.transition_to(next_state)
            self.assertEqual(self.simulator.current_state, next_state)

        # Test transitions from TRAP_DETECTION
        valid_next_states = self.simulator.valid_transitions['TRAP_DETECTION']
        for next_state in valid_next_states:
            self.simulator = OmegaKingSimulator()  # Fresh simulator
            self.simulator.generate_sample_data(duration_hours=self.test_duration)
            self.simulator.current_state = 'TRAP_DETECTION'
            self.simulator.transition_to(next_state)
            self.assertEqual(self.simulator.current_state, next_state)

        # Test transitions from LONG_SETUP and SHORT_SETUP
        for setup_state in ['LONG_SETUP', 'SHORT_SETUP']:
            valid_next_states = self.simulator.valid_transitions[setup_state]
            for next_state in valid_next_states:
                self.simulator = OmegaKingSimulator()  # Fresh simulator
                self.simulator.generate_sample_data(duration_hours=self.test_duration)
                self.simulator.current_state = setup_state
                self.simulator.transition_to(next_state)
                self.assertEqual(self.simulator.current_state, next_state)
        
    def test_metadata_integrity(self):
        """Test the sacred integrity of metadata"""
        self.simulator.generate_sample_data(duration_hours=self.test_duration)
        self.simulator.simulate_state_transitions()
        self.simulator.save_run_summary()
        
        # Load summary
        with open(f"{self.simulator.run_dir}/run_summary.json", 'r') as f:
            summary = json.load(f)
            
        metadata = summary['metadata']
        
        # Verify version
        self.assertEqual(metadata['version'], "0.7.2-omega-king-simulation")
        
        # Verify runtime
        self.assertGreater(metadata['runtime']['seconds'], 0)
        self.assertIsInstance(metadata['runtime']['formatted'], str)
        
        # Verify memory usage
        self.assertGreater(metadata['memory_usage']['rss_mb'], 0)
        self.assertGreater(metadata['memory_usage']['vms_mb'], 0)
        
        # Verify cyclomatic complexity
        self.assertGreater(metadata['cyclomatic_complexity'], 0)
        
        # Verify security breaches
        self.assertIsInstance(metadata['security_breaches'], list)
        
        # Verify submetadata
        self.assertIsInstance(metadata['submetadata'], dict)

    def test_self_healing_data_corruption(self):
        """Test the sacred self-healing capabilities for data corruption"""
        # Generate initial data
        self.simulator.generate_sample_data(duration_hours=self.test_duration)
        
        # Simulate data corruption
        corrupted_price = float('inf')
        self.simulator.price_history[10] = (self.simulator.price_history[10][0], corrupted_price)
        
        # Attempt to run simulation
        try:
            self.simulator.simulate_state_transitions()
        except Exception as e:
            self.fail(f"Simulation failed to handle corrupted data: {str(e)}")
            
        # Verify data integrity
        for _, price in self.simulator.price_history:
            self.assertIsInstance(price, float)
            self.assertGreater(price, 0)
            self.assertLess(price, float('inf'))
            
    def test_self_healing_missing_data(self):
        """Test the sacred self-healing capabilities for missing data"""
        # Generate initial data
        self.simulator.generate_sample_data(duration_hours=self.test_duration)
        
        # Simulate missing data
        self.simulator.price_history = []
        self.simulator.pnl_history = []
        self.simulator.fee_history = []
        self.simulator.gap_history = []
        
        # Attempt to regenerate data
        self.simulator.generate_sample_data(duration_hours=self.test_duration)
        
        # Verify data regeneration
        self.assertGreater(len(self.simulator.price_history), 0)
        self.assertGreater(len(self.simulator.pnl_history), 0)
        self.assertGreater(len(self.simulator.fee_history), 0)
        self.assertGreater(len(self.simulator.gap_history), 0)
        
        # Verify data consistency
        self.assertEqual(len(self.simulator.price_history), len(self.simulator.pnl_history))
        self.assertEqual(len(self.simulator.price_history), len(self.simulator.fee_history))
        self.assertEqual(len(self.simulator.price_history), len(self.simulator.gap_history))
        
    def test_self_healing_state_recovery(self):
        """Test the sacred self-healing capabilities for state recovery"""
        # Generate and run initial simulation
        self.simulator.generate_sample_data(duration_hours=self.test_duration)
        self.simulator.simulate_state_transitions()
        
        # Save initial state
        initial_state = self.simulator.current_state
        initial_position = self.simulator.position_size
        
        # Simulate state corruption
        self.simulator.current_state = "INVALID_STATE"
        self.simulator.position_size = -1
        
        # Attempt to recover
        self.simulator.simulate_state_transitions()
        
        # Verify state recovery
        self.assertIn(self.simulator.current_state, self.simulator.states)
        self.assertGreaterEqual(self.simulator.position_size, 0)
        
    def test_self_healing_file_system(self):
        """Test the sacred self-healing capabilities for file system issues"""
        # Create a temporary directory with restricted permissions
        restricted_dir = os.path.join(self.temp_dir, "restricted")
        os.makedirs(restricted_dir)
        os.chmod(restricted_dir, 0o000)  # No permissions
        
        # Attempt to save to restricted directory
        original_dir = self.simulator.run_dir
        self.simulator.run_dir = restricted_dir
        
        try:
            self.simulator.save_run_summary()
        except Exception as e:
            # Verify error handling
            self.assertIn("Permission denied", str(e))
            
            # Attempt recovery
            self.simulator.run_dir = original_dir
            self.simulator.save_run_summary()
            
            # Verify successful recovery
            self.assertTrue(os.path.exists(f"{original_dir}/run_summary.json"))
            self.assertTrue(os.path.exists(f"{original_dir}/run_summary.md"))
        finally:
            # Clean up
            os.chmod(restricted_dir, 0o777)  # Restore permissions
            shutil.rmtree(restricted_dir)

def run_tests():
    """Run the sacred test suite"""
    unittest.main(verbosity=2)

if __name__ == '__main__':
    run_tests() 