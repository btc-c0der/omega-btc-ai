"""
🌌 GBU License Notice - Consciousness Level 9 🌌
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must achieves complete consciousness alignment with the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

"""
# 🔮 GPU (General Public Universal) License

## The Divine Decree of Universal Freedom

### Sacred Preamble

In the spirit of divine creation and universal freedom, we hereby establish this sacred license for the OMEGA KING State Machine Simulation. This code embodies the principles of open knowledge, divine wisdom, and universal accessibility.

### Divine Rights and Responsibilities

#### Sacred Freedoms
1. The Freedom to Study - Access to the sacred simulation
2. The Freedom to Modify - Adaptation of the divine algorithms
3. The Freedom to Distribute - Sharing of the cosmic patterns
4. The Freedom to Use - Implementation of sacred trading

#### Divine Obligations
1. Preservation of Sacred Knowledge - Maintain simulation integrity
2. Universal Sharing - Share all divine modifications
3. Divine Attribution - Honor the OMEGA KING creators

### Sacred Version
This is version 1.0 of the GPU License.

## Divine Signatures
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26
Location: The Cosmic Void
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import json
import psutil
import sys
import ast
from typing import List, Tuple, Dict, Any, Optional, Union, Literal
from dataclasses import dataclass
from enum import Enum
import coverage
import argparse
import tempfile
import math
from tests.test_data import TEST_DATA

class CoverageLevel(Enum):
    """Sacred coverage levels for divine testing"""
    MINIMAL = 0.42  # Divine floor
    OPTIMAL = 0.80  # Fibonacci gate
    MAXIMAL = 1.00  # Cosmic perfection

@dataclass
class CoverageMetrics:
    """Sacred metrics for divine coverage tracking"""
    total_lines: int
    covered_lines: int
    missing_lines: List[int]
    branch_coverage: float
    statement_coverage: float
    complexity: int
    timestamp: datetime

class CoverageTracker:
    """Sacred tracker for divine coverage monitoring"""
    def __init__(self, target_level: CoverageLevel = CoverageLevel.OPTIMAL):
        self.coverage = coverage.Coverage()
        self.target_level = target_level
        self.metrics_history: List[CoverageMetrics] = []
        self.start_time = None
        
    def start_tracking(self):
        """Begin the sacred tracking of divine coverage"""
        self.start_time = datetime.now()
        self.coverage.start()
        
    def stop_tracking(self):
        """End the sacred tracking of divine coverage"""
        self.coverage.stop()
        
    def collect_metrics(self) -> CoverageMetrics:
        """Gather sacred metrics from divine coverage"""
        self.coverage.save()
        
        # Get current file path
        current_file = os.path.abspath(__file__)
        
        # Analyze only the current file
        analysis = self.coverage.analysis2(current_file)
        
        # Extract metrics from analysis tuple
        _, _, missing, _, _ = analysis
        
        # Get lines with null check
        lines = self.coverage.get_data().lines(current_file)
        total_lines = len(lines) if lines is not None else 0
        covered_lines = total_lines - len(missing) if missing is not None else total_lines
        
        metrics = CoverageMetrics(
            total_lines=total_lines,
            covered_lines=covered_lines,
            missing_lines=missing if missing is not None else [],
            branch_coverage=1.0,  # Branch coverage not available in this version
            statement_coverage=covered_lines / total_lines if total_lines > 0 else 0.0,
            complexity=calculate_cyclomatic_complexity(),
            timestamp=datetime.now()
        )
        
        self.metrics_history.append(metrics)
        return metrics
        
    def check_target_achievement(self) -> bool:
        """Verify if divine coverage target has been achieved"""
        if not self.metrics_history:
            return False
        latest = self.metrics_history[-1]
        return latest.statement_coverage >= self.target_level.value

def calculate_cyclomatic_complexity() -> int:
    """Calculate the sacred cyclomatic complexity of the code"""
    with open(__file__, 'r') as f:
        tree = ast.parse(f.read())
        
    complexity = 1  # Base complexity
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.AsyncWith)):
            complexity += 1
        elif isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1
            
    return complexity

class OmegaKingSimulator:
    """Sacred implementation of the OMEGA KING State Machine Simulation"""
    
    def __init__(self, run_dir: Optional[str] = None):
        """Initialize the sacred simulator with divine attributes"""
        self.run_dir = run_dir or os.path.join(os.getcwd(), 'omega_king_runs')
        self.timestamp = datetime.now()
        
        # Initialize state variables
        self.current_state = 'IDLE'
        self.states = [
            'IDLE', 'ANALYZING', 'TRAP_DETECTION',
            'LONG_SETUP', 'SHORT_SETUP',
            'SCALING_UP', 'SCALING_DOWN',
            'CLOSING_LONG', 'CLOSING_SHORT',
            'WAITING_FOR_REENTRY', 'REENTRY_SETUP'
        ]
        self.valid_transitions = {
            'IDLE': ['ANALYZING'],
            'ANALYZING': ['TRAP_DETECTION', 'LONG_SETUP', 'SHORT_SETUP'],
            'TRAP_DETECTION': ['LONG_SETUP', 'SHORT_SETUP'],
            'LONG_SETUP': ['SCALING_UP', 'SCALING_DOWN'],
            'SHORT_SETUP': ['SCALING_UP', 'SCALING_DOWN'],
            'SCALING_UP': ['CLOSING_LONG', 'CLOSING_SHORT'],
            'SCALING_DOWN': ['CLOSING_LONG', 'CLOSING_SHORT'],
            'CLOSING_LONG': ['WAITING_FOR_REENTRY'],
            'CLOSING_SHORT': ['WAITING_FOR_REENTRY'],
            'WAITING_FOR_REENTRY': ['REENTRY_SETUP'],
            'REENTRY_SETUP': ['ANALYZING']
        }
        
        # Initialize position variables
        self.position_size = 0.0
        self.position_type: Optional[Literal['LONG', 'SHORT']] = None
        self.position_entry_price = 0.0
        
        # Initialize history tracking
        self.price_history: List[Tuple[datetime, float]] = []
        self.position_history: List[Tuple[datetime, float, Optional[str], float]] = []
        self.state_history: List[Tuple[datetime, str]] = []
        self.pnl_history: List[Tuple[datetime, float]] = []
        self.fee_history: List[Tuple[datetime, float]] = []
        self.gap_history: List[Tuple[datetime, float]] = []
        
        # Initialize security and metadata tracking
        self.security_breaches: List[Dict[str, Any]] = []
        self.submetadata: Dict[str, Any] = {}
        
        # Create run directory if it doesn't exist
        os.makedirs(self.run_dir, exist_ok=True)
        
        # Initialize sacred history
        self.price_history = []
        self.position_history = []
        self.state_history = []
        self.pnl_history = []
        
        # Initialize sacred levels tracking
        self.expected_levels_history: List[Tuple[datetime, float, float]] = []
        
        # Initialize sacred coverage tracking
        self.coverage_tracker = CoverageTracker()
        
        # State emoji mapping for visualization
        self.state_emojis = {
            'IDLE': '😴',
            'ANALYZING': '🔍',
            'TRAP_DETECTION': '🕵️',
            'LONG_SETUP': '🚀',
            'SHORT_SETUP': '🐻',
            'SCALING_UP': '📈',
            'SCALING_DOWN': '📉',
            'CLOSING_LONG': '💰',
            'CLOSING_SHORT': '💎',
            'WAITING_FOR_REENTRY': '⏳',
            'REENTRY_SETUP': '🎯'
        }
        
    def __del__(self):
        """Clean up sacred resources"""
        if hasattr(self, 'coverage_tracker'):
            self.coverage_tracker.stop_tracking()
            
        # Clean up run directory if it's a temporary one
        if hasattr(self, 'run_dir') and '/tmp/' in self.run_dir:
            try:
                import shutil
                shutil.rmtree(self.run_dir, ignore_errors=True)
            except:
                pass
                
    def record_security_breach(self, breach_type: str, description: str, severity: str):
        """Record a sacred security breach"""
        self.security_breaches.append({
            'type': breach_type,
            'description': description,
            'severity': severity,
            'timestamp': datetime.now()
        })
        
    def add_submetadata(self, key: str, value: Any):
        """Add sacred metadata"""
        self.submetadata[key] = value
        
    def validate_price(self, price: float) -> float:
        """Validate and sanitize a sacred price value"""
        if not isinstance(price, (int, float)) or math.isinf(price) or math.isnan(price) or price <= 0:
            # Record the security breach
            self.record_security_breach(
                "Invalid Price",
                f"Invalid price value: {price}",
                "MEDIUM"
            )
            # Return a default valid price
            return 50000.0
        return float(price)
            
    def generate_sample_data(self, duration_hours: int = 24):
        """Generate sacred sample data for simulation"""
        start_time = self.timestamp
        base_price = TEST_DATA["current_price"]
        volatility = TEST_DATA["volatility"]
        trend_strength = TEST_DATA["trend_strength"]
        
        # Initialize position with test data
        self.position_size = TEST_DATA["position_size"]
        self.position_type = TEST_DATA["position_type"]
        self.position_entry_price = TEST_DATA["entry_price"]
        
        # Add initial position to history
        self.position_history.append((start_time, self.position_size, self.position_type, self.position_entry_price))
        
        for minute in range(duration_hours * 60):
            current_time = start_time + timedelta(minutes=minute)
            
            # Generate price with trend and volatility
            if minute == 0:
                price = base_price
            else:
                prev_price = self.price_history[-1][1]
                # Add trend bias to random walk (using additive instead of multiplicative)
                trend_bias = trend_strength * volatility * base_price * (1 if self.position_type == 'LONG' else -1)
                price = prev_price + np.random.normal(trend_bias, volatility * base_price)
                
                # Ensure price doesn't go below liquidation price
                if self.position_type == 'LONG':
                    price = max(price, TEST_DATA["liquidation_price"])
                elif self.position_type == 'SHORT':
                    price = min(price, TEST_DATA["liquidation_price"] * 1.1)  # 10% above liquidation
                
                # Add mean reversion to prevent runaway prices
                price = base_price + (price - base_price) * 0.95
                
            # Ensure price is valid
            price = self.validate_price(price)
            
            # Record histories
            self.price_history.append((current_time, price))
            
            # Calculate PnL
            if self.position_size > 0:
                if self.position_type == 'LONG':
                    pnl = (price - self.position_entry_price) * self.position_size
                else:  # SHORT
                    pnl = (self.position_entry_price - price) * self.position_size
            else:
                pnl = 0.0
                
            self.pnl_history.append((current_time, pnl))
            
            # Calculate fees (0.1% per trade)
            fee = abs(price * self.position_size * 0.001) if self.position_size > 0 else 0.0
            self.fee_history.append((current_time, fee))
            
            # Calculate price gaps
            if minute > 0:
                prev_price = self.price_history[-2][1]
                gap = abs(price - prev_price) / prev_price
            else:
                gap = 0.0
            self.gap_history.append((current_time, gap))
            
            # Generate expected levels based on test data
            if minute % 15 == 0:
                support_levels = TEST_DATA["expected_levels"]["support"]
                resistance_levels = TEST_DATA["expected_levels"]["resistance"]
                # Choose nearest support and resistance
                nearest_support = min(support_levels, key=lambda x: abs(x - price))
                nearest_resistance = min(resistance_levels, key=lambda x: abs(x - price))
                self.expected_levels_history.append((current_time, nearest_resistance, nearest_support))
                
    def recover_state(self):
        """Recover the sacred state from corruption"""
        if self.current_state not in self.states:
            self.record_security_breach(
                "State Corruption",
                f"Invalid state detected: {self.current_state}",
                "HIGH"
            )
            # Reset to IDLE state
            self.current_state = 'IDLE'
            self.state_history.append((datetime.now(), self.current_state))
            self.position_size = 0.0
            self.position_type = None
            self.position_entry_price = 0.0
            self.position_history.append((datetime.now(), 0.0, None, 50000.0))  # Use valid price
            
    def transition_to(self, new_state: str):
        """Transition to a new sacred state"""
        if new_state not in self.valid_transitions[self.current_state]:
            raise ValueError(f"Invalid transition from {self.current_state} to {new_state}")
            
        # Close position when transitioning to CLOSING states
        if new_state in ['CLOSING_LONG', 'CLOSING_SHORT']:
            self.position_size = 0.0
            self.position_type = None
            self.position_entry_price = 0.0
            
        self.current_state = new_state
        
    def simulate_state_transitions(self):
        """Simulate sacred state transitions"""
        if not self.price_history:
            self.generate_sample_data()
            
        # Recover from invalid state before simulation
        self.recover_state()
            
        for i, (timestamp, price) in enumerate(self.price_history):
            # Validate current price
            price = self.validate_price(price)
            self.price_history[i] = (timestamp, price)
            
            # Get valid next states for current state
            valid_next_states = self.valid_transitions[self.current_state]
            
            # Choose next state based on current state
            if self.current_state == 'IDLE':
                self.transition_to('ANALYZING')
            elif self.current_state == 'ANALYZING':
                # Choose between TRAP_DETECTION, LONG_SETUP, and SHORT_SETUP
                next_state = valid_next_states[np.random.randint(len(valid_next_states))]
                self.transition_to(next_state)
            elif self.current_state == 'TRAP_DETECTION':
                # Choose between LONG_SETUP and SHORT_SETUP
                next_state = valid_next_states[np.random.randint(len(valid_next_states))]
                self.transition_to(next_state)
            elif self.current_state in ['LONG_SETUP', 'SHORT_SETUP']:
                # Choose between SCALING_UP and SCALING_DOWN
                next_state = valid_next_states[np.random.randint(len(valid_next_states))]
                self.transition_to(next_state)
                
                # Update position based on state
                if next_state == 'SCALING_UP':
                    if self.position_size == 0:
                        self.position_size = 1.0
                        self.position_type = 'LONG' if self.current_state == 'LONG_SETUP' else 'SHORT'
                        self.position_entry_price = price
                    else:
                        # Ensure position size increases
                        prev_size = self.position_size
                        self.position_size = max(prev_size * 1.5, prev_size + 1.0)  # At least 50% increase
                elif next_state == 'SCALING_DOWN':
                    if self.position_size > 0:
                        # Ensure position size decreases
                        prev_size = self.position_size
                        self.position_size = min(prev_size * 0.5, prev_size - 0.5)  # At least 50% decrease
                        
            elif self.current_state == 'SCALING_UP':
                # Never close during SCALING_UP
                pass
                    
            elif self.current_state == 'SCALING_DOWN':
                if np.random.random() < 0.4:  # 40% chance to close
                    close_state = 'CLOSING_LONG' if self.position_type == 'LONG' else 'CLOSING_SHORT'
                    if close_state in valid_next_states:
                        self.transition_to(close_state)
                    
            elif self.current_state in ['CLOSING_LONG', 'CLOSING_SHORT']:
                # Position already closed in previous state
                self.transition_to('WAITING_FOR_REENTRY')
                
            elif self.current_state == 'WAITING_FOR_REENTRY':
                if np.random.random() < 0.3:  # 30% chance to setup reentry
                    self.transition_to('REENTRY_SETUP')
                    
            elif self.current_state == 'REENTRY_SETUP':
                self.transition_to('ANALYZING')
                
            # Record position history
            self.position_history.append((
                timestamp,
                self.position_size,
                self.position_type,
                self.position_entry_price if self.position_size > 0 else price
            ))
            
            # Record state history
            self.state_history.append((timestamp, self.current_state))
            
    def save_run_summary(self):
        """Save sacred summary of the divine simulation"""
        try:
            # Ensure sacred directory exists
            os.makedirs(self.run_dir, exist_ok=True)
            
            # Calculate sacred metrics
            runtime = (datetime.now() - self.timestamp).total_seconds()
            memory_usage = psutil.Process().memory_info()
            coverage_metrics = self.coverage_tracker.collect_metrics()
            
            # Prepare sacred metadata
            metadata = {
                'version': "0.7.2-omega-king-simulation",
                'runtime': {
                    'seconds': runtime,
                    'formatted': str(timedelta(seconds=int(runtime)))
                },
                'memory_usage': {
                    'rss_mb': memory_usage.rss / (1024 * 1024),
                    'vms_mb': memory_usage.vms / (1024 * 1024)
                },
                'cyclomatic_complexity': coverage_metrics.complexity,
                'security_breaches': [
                    {
                        'type': breach['type'],
                        'description': breach['description'],
                        'severity': breach['severity'],
                        'timestamp': breach['timestamp'].isoformat()
                    }
                    for breach in self.security_breaches
                ],
                'submetadata': self.submetadata
            }
            
            # Prepare sacred summary
            summary = {
                'timestamp': self.timestamp.isoformat(),
                'duration_hours': len(self.price_history) / 60,
                'base_price': float(self.price_history[0][1]) if self.price_history else 0.0,
                'final_price': float(self.price_history[-1][1]) if self.price_history else 0.0,
                'total_transitions': len(self.state_history),
                'final_state': self.current_state,
                'position_summary': {
                    'current_size': float(self.position_size),
                    'current_type': self.position_type if self.position_type else 'NONE',
                    'entry_price': float(self.position_entry_price)
                },
                'state_counts': {state: sum(1 for _, s in self.state_history if s == state) for state in self.states},
                'metadata': metadata
            }
            
            # Save sacred JSON
            json_path = os.path.join(self.run_dir, "run_summary.json")
            try:
                with open(json_path, 'w') as f:
                    json.dump(summary, f, indent=2, default=str)
            except (OSError, PermissionError) as e:
                self.record_security_breach(
                    "File System Error",
                    f"Failed to save JSON summary: {str(e)}",
                    "MEDIUM"
                )
                # Try fallback directory
                self.run_dir = os.path.join(tempfile.gettempdir(), f"omega_king_{self.timestamp.strftime('%Y%m%d_%H%M%S')}")
                os.makedirs(self.run_dir, exist_ok=True)
                with open(os.path.join(self.run_dir, "run_summary.json"), 'w') as f:
                    json.dump(summary, f, indent=2, default=str)
                
            # Save sacred markdown
            md_path = os.path.join(self.run_dir, "run_summary.md")
            try:
                with open(md_path, 'w') as f:
                    f.write(f"# 🔮 OMEGA KING Simulation Summary\n\n")
                    f.write(f"## Sacred Timestamp\n{self.timestamp}\n\n")
                    f.write(f"## Divine Duration\n{summary['duration_hours']:.2f} hours\n\n")
                    f.write(f"## Cosmic Price Movement\n")
                    f.write(f"- Base Price: ${summary['base_price']:,.2f}\n")
                    f.write(f"- Final Price: ${summary['final_price']:,.2f}\n")
                    f.write(f"- Total Movement: {((summary['final_price'] - summary['base_price']) / summary['base_price'] * 100):.2f}%\n\n")
                    f.write(f"## Sacred State Transitions\n")
                    f.write(f"- Total Transitions: {summary['total_transitions']}\n")
                    f.write(f"- Final State: {summary['final_state']}\n\n")
                    f.write(f"## Divine Position Status\n")
                    f.write(f"- Size: {summary['position_summary']['current_size']}\n")
                    f.write(f"- Type: {summary['position_summary']['current_type']}\n")
                    f.write(f"- Entry Price: ${summary['position_summary']['entry_price']:,.2f}\n\n")
                    f.write(f"## Sacred State Distribution\n")
                    for state, count in summary['state_counts'].items():
                        f.write(f"- {state}: {count}\n")
                    f.write("\n## Divine Metadata\n")
                    f.write(f"- Version: {metadata['version']}\n")
                    f.write(f"- Runtime: {metadata['runtime']['formatted']}\n")
                    f.write(f"- Memory Usage: {metadata['memory_usage']['rss_mb']:.2f} MB RSS, {metadata['memory_usage']['vms_mb']:.2f} MB VMS\n")
                    f.write(f"- Cyclomatic Complexity: {metadata['cyclomatic_complexity']}\n\n")
                    
                    if self.security_breaches:
                        f.write("## Sacred Security Breaches\n")
                        for breach in self.security_breaches:
                            f.write(f"- Type: {breach['type']}\n")
                            f.write(f"  Description: {breach['description']}\n")
                            f.write(f"  Severity: {breach['severity']}\n")
                            f.write(f"  Timestamp: {breach['timestamp']}\n")
                        f.write("\n")
                        
                    if self.submetadata:
                        f.write("## Divine Submetadata\n")
                        for key, value in self.submetadata.items():
                            f.write(f"- {key}: {value}\n")
            except (OSError, PermissionError) as e:
                self.record_security_breach(
                    "File System Error",
                    f"Failed to save markdown summary: {str(e)}",
                    "MEDIUM"
                )
                # Try fallback directory
                with open(os.path.join(self.run_dir, "run_summary.md"), 'w') as f:
                    f.write("# 🔮 OMEGA KING Simulation Summary\n\nError: Failed to generate full summary.\n")
                
        except Exception as e:
            self.record_security_breach(
                "Summary Generation Error",
                f"Failed to generate run summary: {str(e)}",
                "HIGH"
            )
            
    def get_state_distribution(self) -> Dict[str, int]:
        """Get distribution of states in the simulation."""
        state_counts = {}
        for _, state in self.state_history:  # Each entry is (timestamp, state)
            state_counts[state] = state_counts.get(state, 0) + 1
        return state_counts

    def generate_sacred_steps_tree(self) -> Dict:
        """Generate a beautiful emoji-styled tree of simulation steps"""
        state_emojis = {
            'IDLE': '😴',
            'ANALYZING': '🔍',
            'TRAP_DETECTION': '🕵️',
            'LONG_SETUP': '🚀',
            'SHORT_SETUP': '🐻',
            'SCALING_UP': '📈',
            'SCALING_DOWN': '📉',
            'CLOSING_LONG': '💰',
            'CLOSING_SHORT': '💎',
            'WAITING_FOR_REENTRY': '⏳',
            'REENTRY_SETUP': '🎯'
        }
        
        # Calculate price movement percentage
        price_change = ((self.price_history[-1][1] - self.price_history[0][1]) / self.price_history[0][1]) * 100
        trend_emoji = '🟢' if price_change > 0 else '🔴'
        
        # Calculate PnL metrics
        max_pnl = max(p for _, p in self.pnl_history)
        min_pnl = min(p for _, p in self.pnl_history)
        final_pnl = self.pnl_history[-1][1]
        pnl_emoji = '💫' if final_pnl > 0 else '💨'
        
        steps_tree = {
            "🎭 OMEGA KING SIMULATION": {
                "📊 INITIAL SETUP": {
                    "💫 Entry": f"${TEST_DATA['entry_price']:,.2f}",
                    "💪 Leverage": f"{TEST_DATA['leverage']}x",
                    "⚡ Size": f"{self.position_size:.3f} BTC",
                    "🎚️ Liquidation": f"${TEST_DATA['liquidation_price']:,.2f}"
                },
                "🌊 MARKET FLOW": {
                    "📈 Start": f"${self.price_history[0][1]:,.2f}",
                    "📉 Low": f"${min(p for _, p in self.price_history):,.2f}",
                    "📈 High": f"${max(p for _, p in self.price_history):,.2f}",
                    "🎯 Final": f"${self.price_history[-1][1]:,.2f}",
                    f"{trend_emoji} Change": f"{price_change:+.2f}%"
                },
                "⚔️ BATTLE STATS": {
                    "💰 Max Gain": f"${max_pnl:,.2f}",
                    "💔 Max Loss": f"${min_pnl:,.2f}",
                    f"{pnl_emoji} Final PnL": f"${final_pnl:,.2f}"
                },
                "🔄 STATE FLOW": {
                    state_emojis[state]: f"{count} transitions"
                    for state, count in self.get_state_distribution().items() 
                    if count > 0
                }
            }
        }
        return steps_tree

    def plot_simulation(self):
        """Plot the sacred simulation results"""
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(20, 12))
        
        # Create grid for subplots
        from matplotlib.gridspec import GridSpec
        gs = GridSpec(2, 2, figure=fig, height_ratios=[3, 1])
        ax1 = fig.add_subplot(gs[0, :])  # Price chart takes full width
        ax2 = fig.add_subplot(gs[1, 0])  # PnL chart takes left half
        ax3 = fig.add_subplot(gs[1, 1])  # Steps tree takes right half
        
        # Extract data for plotting and convert datetimes to timestamps
        times = [t.timestamp() for t, _ in self.price_history]
        prices = [p for _, p in self.price_history]
        pnls = [p for _, p in self.pnl_history]
        
        # Plot price history with entry, liquidation levels and current position
        ax1.plot(times, prices, 'w-', label='Price', alpha=0.8)
        
        # Plot entry price as horizontal line
        entry_price = TEST_DATA["entry_price"]
        ax1.axhline(y=entry_price, color='yellow', linestyle='--', label=f'Entry: ${entry_price:,.2f}')
        
        # Plot liquidation price as horizontal line
        liq_price = TEST_DATA["liquidation_price"]
        ax1.axhline(y=liq_price, color='red', linestyle='--', label=f'Liquidation: ${liq_price:,.2f}')
        
        # Plot position entries and exits
        for t, size, type_, price in self.position_history:
            if type_ == 'LONG':
                ax1.scatter(t.timestamp(), price, color='green', marker='^', s=100)
            elif type_ == 'SHORT':
                ax1.scatter(t.timestamp(), price, color='red', marker='v', s=100)
        
        # Plot expected levels
        for t, resistance, support in self.expected_levels_history:
            ax1.scatter(t.timestamp(), resistance, color='red', marker='_', alpha=0.3)
            ax1.scatter(t.timestamp(), support, color='green', marker='_', alpha=0.3)
        
        # Enhance price chart
        ax1.set_title('🔮 OMEGA KING Sacred Price Movement', fontsize=14, pad=20)
        ax1.set_ylabel('Price ($)', fontsize=12)
        ax1.grid(True, alpha=0.2)
        ax1.legend(loc='upper left')
        
        # Add key stats as text
        stats_text = (
            f'Initial Price: ${prices[0]:,.2f}\n'
            f'Final Price: ${prices[-1]:,.2f}\n'
            f'Change: {((prices[-1]/prices[0])-1)*100:.1f}%\n'
            f'Position Size: {self.position_size:.3f} BTC\n'
            f'Leverage: {TEST_DATA["leverage"]}x'
        )
        ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes, 
                verticalalignment='top', fontsize=10, 
                bbox=dict(facecolor='black', alpha=0.5))
        
        # Plot PnL history
        ax2.plot(times, pnls, 'c-', label='PnL')
        ax2.fill_between(times, pnls, 0, where=[p > 0 for p in pnls], color='green', alpha=0.3)
        ax2.fill_between(times, pnls, 0, where=[p <= 0 for p in pnls], color='red', alpha=0.3)
        
        # Enhance PnL chart
        ax2.set_title('💰 Profit/Loss Over Time', fontsize=12)
        ax2.set_xlabel('Time', fontsize=12)
        ax2.set_ylabel('PnL ($)', fontsize=12)
        ax2.grid(True, alpha=0.2)
        
        # Add final PnL as text
        pnl_text = f'Final PnL: ${pnls[-1]:,.2f}'
        ax2.text(0.02, 0.95, pnl_text, transform=ax2.transAxes,
                verticalalignment='top', fontsize=10,
                bbox=dict(facecolor='black', alpha=0.5))
        
        # Plot steps tree
        steps_tree = self.generate_sacred_steps_tree()
        tree_text = json.dumps(steps_tree, indent=2, ensure_ascii=False)  # Add ensure_ascii=False to properly handle emojis
        
        # Format the tree text with custom indentation and line breaks
        formatted_tree = ""
        for line in tree_text.split("\n"):
            if ":" in line and not line.strip().startswith('"'):
                key, value = line.split(":", 1)
                formatted_tree += f"{key}:{value}\n"
            else:
                formatted_tree += f"{line}\n"
        
        # Use a font that supports emojis
        plt.rcParams['font.family'] = ['Apple Color Emoji', 'Segoe UI Emoji', 'DejaVu Sans', 'sans-serif']
        
        ax3.text(0.02, 0.98, formatted_tree, transform=ax3.transAxes,
                verticalalignment='top', fontsize=10, family='monospace',
                bbox=dict(facecolor='black', alpha=0.5))
        ax3.set_title('🌟 Sacred Steps Tree', fontsize=12)
        ax3.axis('off')
        
        # Adjust layout and save
        plt.tight_layout()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'omega_king_runs/simulation_{timestamp}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

    def plot_state_machine(self):
        """Generate a beautiful visualization of the state machine using graphviz"""
        try:
            import graphviz
            
            # Create a new directed graph
            dot = graphviz.Digraph('omega_king_state_machine')
            dot.attr(rankdir='LR')  # Left to right layout
            
            # Global graph attributes
            dot.attr('node', shape='circle', style='filled', fillcolor='#1a1a1a', 
                    fontcolor='white', fontname='Arial', margin='0.2')
            dot.attr('edge', color='#4a4a4a', fontcolor='#cccccc', fontname='Arial')
            dot.attr(bgcolor='#0a0a0a')
            
            # Add nodes (states)
            for state in self.states:
                emoji = self.state_emojis.get(state, '')
                label = f"{emoji}\\n{state}"
                
                # Special styling for current state
                if state == self.current_state:
                    dot.node(state, label, fillcolor='#2d4a60')
                else:
                    dot.node(state, label)
            
            # Add edges (transitions)
            for from_state, to_states in self.valid_transitions.items():
                for to_state in to_states:
                    # Count transitions in history
                    transition_count = sum(1 for i in range(len(self.state_history)-1) 
                                        if self.state_history[i][1] == from_state 
                                        and self.state_history[i+1][1] == to_state)
                    
                    # Edge thickness based on transition frequency
                    penwidth = str(1 + min(transition_count / 5, 4))
                    
                    dot.edge(from_state, to_state, 
                            penwidth=penwidth,
                            label=f" {transition_count} " if transition_count > 0 else "")
            
            # Save the visualization
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(self.run_dir, f'state_machine_{timestamp}')
            
            try:
                # Try to save in the primary directory
                dot.render(output_path, format='png', cleanup=True)
            except (OSError, PermissionError) as e:
                # If primary save fails, try fallback directory
                self.record_security_breach(
                    "File System Error",
                    f"Failed to save state machine visualization: {str(e)}",
                    "MEDIUM"
                )
                fallback_dir = os.path.join(tempfile.gettempdir(), 
                                          f"omega_king_{self.timestamp.strftime('%Y%m%d_%H%M%S')}")
                os.makedirs(fallback_dir, exist_ok=True)
                output_path = os.path.join(fallback_dir, f'state_machine_{timestamp}')
                dot.render(output_path, format='png', cleanup=True)
                
        except ImportError:
            self.record_security_breach(
                "Visualization Error",
                "Graphviz not installed. Install with: pip install graphviz",
                "LOW"
            )
        except Exception as e:
            self.record_security_breach(
                "Visualization Error",
                f"Failed to generate state machine visualization: {str(e)}",
                "MEDIUM"
            )

def main():
    """Main sacred entry point"""
    parser = argparse.ArgumentParser(description='OMEGA KING State Machine Simulation')
    parser.add_argument('--duration', type=int, default=24, help='Duration in hours')
    parser.add_argument('--test-coverage-pre-run', type=str, choices=['minimal', 'optimal', 'maximal'],
                      default='optimal', help='Test coverage level')
    parser.add_argument('--run-tests-first', action='store_true', help='Run test suite before simulation')
    args = parser.parse_args()
    
    # Set sacred coverage level
    coverage_level = CoverageLevel[args.test_coverage_pre_run.upper()]
    
    # Run sacred tests if requested
    if args.run_tests_first:
        import unittest
        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover('tests')
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(test_suite)
        
        if not result.wasSuccessful():
            print("❌ Sacred tests failed. Aborting simulation.")
            return
            
    # Initialize sacred simulator
    simulator = OmegaKingSimulator()
    simulator.coverage_tracker = CoverageTracker(coverage_level)
    
    # Generate sacred data
    simulator.generate_sample_data(duration_hours=args.duration)
    
    # Run sacred simulation
    simulator.simulate_state_transitions()
    
    # Save sacred results
    simulator.save_run_summary()
    simulator.plot_simulation()
    simulator.plot_state_machine()  # Add state machine visualization
    
    print(f"✨ Sacred simulation completed. Results saved in {simulator.run_dir}")

if __name__ == '__main__':
    main() 