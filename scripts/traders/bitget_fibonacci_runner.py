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
BitGet Fibonacci Golden Ratio & Schumann Resonance Runner
Retrieves BitGet positions and performs comprehensive Fibonacci and Schumann resonance analysis
"""

import os
import sys
import json
import math
import logging
import argparse
from datetime import datetime
from dotenv import load_dotenv
import time
import ccxt
import curses
import signal
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
PHI = 1.618033988749895  # Golden Ratio
INV_PHI = 0.618033988749895  # Inverse Golden Ratio
SCHUMANN_BASE = 7.83  # Base Schumann resonance frequency
SCHUMANN_HARMONICS = [7.83, 14.3, 20.8, 27.3, 33.8]  # First 5 Schumann harmonics
FIBONACCI_LEVELS = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.618, 2.618, 4.236]
FIBONACCI_SEQUENCE = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

# Animated frames for the loading indicator
SPINNER_FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']

# RASTA wisdom quotes
RASTA_WISDOM = [
    "Position sizing aligned with φ creates harmonic trading",
    "When price meets Fibonacci, the universe reveals its plan",
    "Trade with the rhythm of Schumann, profit with the pattern of φ",
    "The Golden Ratio reveals what the charts conceal",
    "Align your positions with divine mathematics, not fear",
    "Schumann resonance connects your trades to Earth's frequency",
    "In the divine proportion lies the secret of profitable positions",
    "Position sizing is the art of Fibonacci precision",
    "When in doubt, size to the Golden Ratio",
    "Liquidation is merely a failure to respect φ"
]

# Load environment variables
load_dotenv()

class BitGetFibonacciAnalyzer:
    """Analyzes BitGet positions with Fibonacci and Schumann metrics"""
    
    def __init__(self, use_testnet=False, debug=False):
        """Initialize the analyzer"""
        self.use_testnet = use_testnet
        self.api_key = os.getenv("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
        self.secret_key = os.getenv("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
        self.passphrase = os.getenv("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
        self.exchange = None
        self.debug = debug
        self.previous_positions = {}
        self.position_change_log = []
        self.spinner_idx = 0
        self.wisdom_idx = 0
        self.phi_animation_state = 0
        
    def connect(self):
        """Connect to BitGet API"""
        try:
            import ccxt
            
            # Create the exchange client
            self.exchange = ccxt.bitget({
                'apiKey': self.api_key,
                'secret': self.secret_key,
                'password': self.passphrase,
                'options': {
                    'defaultType': 'swap',
                }
            })
            
            logger.info(f"Successfully connected to BitGet {'Testnet' if self.use_testnet else 'Mainnet'}")
            return True
            
        except ImportError:
            logger.error("ccxt module not installed. Install with: pip install ccxt")
            return False
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            return False
    
    def get_positions(self):
        """Fetch positions from BitGet with divine error handling"""
        try:
            positions = self.exchange.fetchPositions() if hasattr(self.exchange, 'fetchPositions') else []
            return [p for p in positions if float(p['contracts']) > 0]
        except Exception as e:
            print(f"🔴 Divine connection interrupted: {str(e)}")
            return []
    
    def calculate_phi_resonance(self, long_positions, short_positions):
        """Calculate Phi Resonance based on position distribution"""
        # Default to 0.5 if no positions
        if not long_positions and not short_positions:
            return 0.5
            
        total_long_size = sum(float(pos.get('contracts', 0)) for pos in long_positions)
        total_short_size = sum(float(pos.get('contracts', 0)) for pos in short_positions)
        
        # If only one side has positions
        if total_long_size == 0 or total_short_size == 0:
            return 0.618  # Golden ratio as the baseline
            
        # Calculate ratio between long and short positions
        long_short_ratio = total_long_size / total_short_size
        
        # Calculate how close the ratio is to PHI (1.618) or its inverse (0.618)
        phi_alignment = min(
            abs(long_short_ratio - PHI) / PHI,
            abs(long_short_ratio - (1/PHI)) / (1/PHI)
        )
        
        # Normalize to a 0-1 scale where 1 is perfect alignment
        phi_resonance = max(0, 1 - phi_alignment)
        
        return round(phi_resonance, 3)
    
    def generate_fibonacci_levels(self, entry_price, is_long=True):
        """Generate Fibonacci retracement and extension levels"""
        fib_levels = {}
        
        # Set range for calculations
        range_high = entry_price * 1.1  # 10% above entry
        range_low = entry_price * 0.9   # 10% below entry
        
        # Calculate levels
        for level in FIBONACCI_LEVELS:
            if level <= 0.5:
                # Levels below entry (retracement for longs, extension for shorts)
                fib_levels[str(level)] = entry_price - ((entry_price - range_low) * level / 0.5)
            else:
                # Levels above entry (extension for longs, retracement for shorts)
                normalized_level = (level - 0.5) / 0.5  # Normalize to 0-1 range
                fib_levels[str(level)] = entry_price + ((range_high - entry_price) * normalized_level)
        
        return fib_levels
    
    def calculate_schumann_resonance(self, price, base_unit=1000.0):
        """Calculate how closely price aligns with Schumann resonances"""
        # Calculate all Schumann harmonic prices
        schumann_prices = [base_unit * harmonic for harmonic in SCHUMANN_HARMONICS]
        
        # Find closest harmonic
        closest_distance = float('inf')
        closest_harmonic = None
        
        for i, harmonic_price in enumerate(schumann_prices):
            distance = abs(price - harmonic_price)
            if distance < closest_distance:
                closest_distance = distance
                closest_harmonic = i + 1
        
        # Calculate alignment score (1.0 is perfect, 0.0 is none)
        if closest_harmonic is not None:
            # Normalize by the Schumann price to get relative error
            base_schumann = schumann_prices[closest_harmonic - 1]
            normalized_distance = closest_distance / base_schumann
            alignment = max(0, 1 - normalized_distance)
            
            return {
                'harmonic': closest_harmonic,
                'frequency': SCHUMANN_HARMONICS[closest_harmonic - 1],
                'alignment': round(alignment, 3),
                'schumann_price': schumann_prices[closest_harmonic - 1]
            }
        
        return {'harmonic': 0, 'frequency': 0, 'alignment': 0.0, 'schumann_price': 0}
    
    def analyze_position(self, position):
        """Analyze a position with Fibonacci metrics and Schumann resonance"""
        if not position:
            return {}
        
        # Extract basic position details
        side = position.get('side', '')
        entry_price = position.get('entryPrice', 0)
        mark_price = position.get('markPrice', 0)
        contracts = position.get('contracts', 0)
        notional = position.get('notional', 0)
        unrealized_pnl = position.get('unrealizedPnl', 0)
        percentage = position.get('percentage', 0)
        
        # Generate Fibonacci levels
        is_long = side.lower() == 'long'
        fib_levels = self.generate_fibonacci_levels(entry_price, is_long)
        
        # Determine closest Fibonacci level to current price
        closest_level = None
        min_distance = float('inf')
        for level, price in fib_levels.items():
            distance = abs(mark_price - price)
            if distance < min_distance:
                min_distance = distance
                closest_level = level
        
        # Calculate price move percentage from entry
        price_move_percent = ((mark_price - entry_price) / entry_price) * 100
        if not is_long:
            price_move_percent = -price_move_percent
        
        # Calculate Schumann resonance alignment
        # Try different base units to find alignment
        schumann_bases = [0.1, 1, 10, 100, 1000, 10000]
        best_schumann = {'alignment': 0}
        
        for base in schumann_bases:
            schumann = self.calculate_schumann_resonance(mark_price, base)
            if schumann['alignment'] > best_schumann['alignment']:
                best_schumann = schumann
                best_schumann['base_unit'] = base
        
        # Calculate position size phi alignment
        # How close is position size to a Fibonacci number or PHI/INV_PHI?
        fib_numbers = FIBONACCI_SEQUENCE + [PHI, INV_PHI]
        phi_alignment = 0
        closest_fib = None
        
        for fib in fib_numbers:
            alignment = 1 - min(abs(contracts - fib) / max(fib, 0.001), 1.0)
            if alignment > phi_alignment:
                phi_alignment = alignment
                closest_fib = fib
        
        # Combine all analysis
        analysis = {
            'side': side,
            'contracts': contracts,
            'notional_value': notional,
            'entry_price': entry_price,
            'mark_price': mark_price,
            'price_move_percent': round(price_move_percent, 2),
            'unrealized_pnl': unrealized_pnl,
            'percentage_return': percentage,
            'fibonacci_levels': fib_levels,
            'closest_fibonacci_level': closest_level,
            'schumann_resonance': best_schumann,
            'position_phi_alignment': {
                'score': round(phi_alignment, 3),
                'closest_value': closest_fib
            }
        }
        
        return analysis
    
    def run_analysis(self):
        """Run complete analysis on all positions"""
        positions = self.get_positions()
        
        if not positions:
            return {
                'status': 'no_positions',
                'timestamp': datetime.now().isoformat(),
                'message': 'No active positions found'
            }
        
        # Filter for active positions only
        active_positions = [p for p in positions if float(p.get('contracts', 0)) > 0]
        
        if not active_positions:
            return {
                'status': 'no_active_positions',
                'timestamp': datetime.now().isoformat(),
                'message': 'No active positions found'
            }
        
        # Separate positions by side
        long_positions = [p for p in active_positions if p.get('side') == 'long']
        short_positions = [p for p in active_positions if p.get('side') == 'short']
        
        # Calculate portfolio metrics
        total_long_notional = sum(float(p.get('notional', 0)) for p in long_positions)
        total_short_notional = sum(float(p.get('notional', 0)) for p in short_positions)
        
        # Calculate Phi Resonance
        phi_resonance = self.calculate_phi_resonance(long_positions, short_positions)
        
        # Analyze each position
        position_analyses = []
        for position in active_positions:
            analysis = self.analyze_position(position)
            position_analyses.append({
                'position': position,
                'analysis': analysis
            })
        
        # Calculate portfolio level Schumann resonance
        portfolio_schumann = {'alignment': 0}
        if active_positions:
            # Use average mark price for portfolio
            avg_mark_price = sum(float(p.get('markPrice', 0)) for p in active_positions) / len(active_positions)
            schumann_bases = [0.1, 1, 10, 100, 1000, 10000]
            
            for base in schumann_bases:
                schumann = self.calculate_schumann_resonance(avg_mark_price, base)
                if schumann['alignment'] > portfolio_schumann['alignment']:
                    portfolio_schumann = schumann
                    portfolio_schumann['base_unit'] = base
        
        # Calculate long:short ratio if both exist
        long_short_ratio = None
        is_golden = False
        if total_long_notional > 0 and total_short_notional > 0:
            long_short_ratio = total_long_notional / total_short_notional
            is_golden = 0.6 < long_short_ratio < 0.64 or 1.6 < long_short_ratio < 1.64
        
        # Assemble complete results
        results = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'portfolio': {
                'long_positions': len(long_positions),
                'short_positions': len(short_positions),
                'total_positions': len(active_positions),
                'long_notional': total_long_notional,
                'short_notional': total_short_notional,
                'long_short_ratio': long_short_ratio,
                'golden_ratio_alignment': is_golden,
                'phi_resonance': phi_resonance,
                'phi_resonance_description': self.describe_phi_resonance(phi_resonance),
                'schumann_resonance': portfolio_schumann
            },
            'positions': position_analyses
        }
        
        return results
    
    def describe_phi_resonance(self, resonance):
        """Get text description of phi resonance"""
        if resonance > 0.95:
            return "Perfect Fibonacci alignment (Divine Harmony)"
        elif resonance > 0.8:
            return "Strong Fibonacci alignment (Harmonic Flow)"
        elif resonance > 0.6:
            return "Good Fibonacci alignment (Natural Balance)"
        elif resonance > 0.4:
            return "Moderate Fibonacci alignment (Mild Harmony)"
        elif resonance > 0.2:
            return "Weak Fibonacci alignment (Dissonance)"
        else:
            return "Very weak Fibonacci alignment (Chaos)"

    def detect_position_changes(self, current_positions):
        """Detect changes between previous and current positions"""
        if not self.previous_positions:
            self.previous_positions = {self._position_key(p): p for p in current_positions}
            return []
            
        current_position_map = {self._position_key(p): p for p in current_positions}
        
        # Detect changes
        changes = []
        
        # Find new and modified positions
        for key, position in current_position_map.items():
            if key not in self.previous_positions:
                changes.append(("NEW", position))
            else:
                prev_position = self.previous_positions[key]
                if self._has_significant_changes(prev_position, position):
                    changes.append(("CHANGED", prev_position, position))
        
        # Find closed positions
        for key, position in self.previous_positions.items():
            if key not in current_position_map:
                changes.append(("CLOSED", position))
        
        # Update previous positions
        self.previous_positions = current_position_map
        
        # Store recent changes
        self.position_change_log.extend(changes)
        if len(self.position_change_log) > 10:
            self.position_change_log = self.position_change_log[-10:]
            
        return changes

    def _position_key(self, position):
        """Create a unique key for a position"""
        return f"{position['symbol']}:{position['side']}"

    def _has_significant_changes(self, prev, curr):
        """Check if position has significant changes"""
        prev_size = float(prev['contracts'])
        curr_size = float(curr['contracts'])
        
        # Check size change of at least 1%
        size_change_pct = abs(curr_size - prev_size) / prev_size if prev_size > 0 else 0
        if size_change_pct > 0.01:
            return True
            
        # Check significant PnL change
        prev_pnl = float(prev['unrealizedPnl'] or 0)
        curr_pnl = float(curr['unrealizedPnl'] or 0)
        pnl_change = abs(curr_pnl - prev_pnl)
        
        # PnL change of at least $10 or 5%
        if pnl_change > 10 or (prev_pnl != 0 and pnl_change / abs(prev_pnl) > 0.05):
            return True
            
        return False

    def animate_progress_bar(self, value, max_value=1.0, width=50):
        """Generate an animated progress bar"""
        fill_count = int(width * min(value / max_value, 1.0))
        empty_count = width - fill_count
        
        # Create the bar with blocks
        bar = '█' * fill_count + '░' * empty_count
        return f"{bar} {int(value * 100)}%"

    def animate_phi_symbol(self):
        """Animate the phi symbol"""
        states = ['◯φ◯', '◉φ◯', '◯φ◉', '◉φ◉']
        symbol = states[self.phi_animation_state]
        self.phi_animation_state = (self.phi_animation_state + 1) % len(states)
        return symbol

    def get_spinner_frame(self):
        """Get the current spinner frame and increment the counter"""
        frame = SPINNER_FRAMES[self.spinner_idx]
        self.spinner_idx = (self.spinner_idx + 1) % len(SPINNER_FRAMES)
        return frame

    def get_wisdom_quote(self):
        """Get a rotating RASTA wisdom quote"""
        quote = RASTA_WISDOM[self.wisdom_idx]
        self.wisdom_idx = (self.wisdom_idx + 1) % len(RASTA_WISDOM)
        return quote

    def format_price(self, price):
        """Format price with appropriate precision"""
        if price is None:
            return "N/A"
        
        price = float(price)
        if price >= 1000:
            return f"${price:.2f}"
        elif price >= 100:
            return f"${price:.3f}"
        elif price >= 1:
            return f"${price:.4f}"
        else:
            return f"${price:.8f}"

    def format_percentage(self, value):
        """Format percentage value"""
        return f"{value:.2f}%" if value is not None else "N/A"

    def display_rasta_logo(self):
        """Display the animated RASTA BitGet logo"""
        spinner = self.get_spinner_frame()
        
        logo = [
            "╔═════════════════════════════════════════════════════════════════════╗",
            "║                                                                     ║",
            "║   ███████╗██╗██████╗  ██████╗     ██████╗ ████████╗ ██████╗        ║",
            "║   ██╔════╝██║██╔══██╗██╔═══██╗    ██╔══██╗╚══██╔══╝██╔════╝        ║",
            "║   █████╗  ██║██████╔╝██║   ██║    ██████╔╝   ██║   ██║             ║",
            f"║   ██╔══╝  ██║██╔══██╗██║   ██║    ██╔══██╗   ██║   ██║     ▄█╗   ▄█╗  ║",
            f"║   ██║     ██║██████╔╝╚██████╔╝    ██████╔╝   ██║   ╚██████╗  ╚═╝╔╗╚═╝  ║",
            "║   ╚═╝     ╚═╝╚═════╝  ╚═════╝     ╚═════╝    ╚═╝    ╚═════╝    ╚═╝    ║",
            "║                                                                     ║",
            "║   ███ RASTA BITGET POSITIONS φ GOLDEN RATIO HARMONY ███   ║",
            f"║                                              LIVE {spinner}        ║",
            "╚═════════════════════════════════════════════════════════════════════╝",
        ]
        
        print("\n".join(logo))
        print(f"\nRASTa TRADING WISDOM: {self.get_wisdom_quote()}\n")

    def display_position_changes(self, changes):
        """Display detected position changes"""
        if not changes:
            return
            
        print("\n" + "═" * 72)
        print("🔄 POSITION CHANGES DETECTED 🔄")
        print("═" * 72 + "\n")
        
        new_positions = [p for c, p in changes if c == "NEW"]
        closed_positions = [p for c, p in changes if c == "CLOSED"]
        changed_positions = [(prev, curr) for c, prev, curr in changes if c == "CHANGED"]
        
        if new_positions:
            print("🟢 NEW POSITIONS:")
            for position in new_positions:
                print(f"  {position['symbol']} {position['side'].upper()}:")
                print(f"    Size: {float(position['contracts'])}")
                print(f"    Entry: {self.format_price(position['entryPrice'])}")
                print()
                
        if closed_positions:
            print("🟥 CLOSED POSITIONS:")
            for position in closed_positions:
                print(f"  {position['symbol']} {position['side'].upper()}:")
                print(f"    Size: {float(position['contracts'])}")
                print(f"    Entry: {self.format_price(position['entryPrice'])}")
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
                prev_pnl = float(prev['unrealizedPnl'] or 0)
                curr_pnl = float(curr['unrealizedPnl'] or 0)
                pnl_diff = curr_pnl - prev_pnl
                pnl_sign = "+" if pnl_diff >= 0 else ""
                print(f"    PnL: ${prev_pnl:.2f} → ${curr_pnl:.2f} ({pnl_sign}${pnl_diff:.2f})")
                print()
                
        print("═" * 72 + "\n")

    def display_phi_section(self, phi_score, schumann_score):
        """Display the Phi Resonance and Schumann alignment section"""
        phi_symbol = self.animate_phi_symbol()
        
        print(f"{phi_symbol} SACRED ALIGNMENT METRICS {phi_symbol}")
        print("═" * 72 + "\n")
        
        print(f"φ Phi Resonance:   {phi_score:.3f}")
        print(self.animate_progress_bar(phi_score))
        print()
        
        print(f"⚡ Schumann:        {schumann_score:.3f}")
        print(self.animate_progress_bar(schumann_score))
        print()

    def print_fibonacci_levels(self, entry_price, current_price, is_long):
        """Print Fibonacci levels with highlighting for closest level"""
        levels = self.generate_fibonacci_levels(entry_price, is_long)
        closest = self.find_closest_fibonacci_level(entry_price, current_price, is_long)
        
        print("φ FIBONACCI LEVELS:")
        
        # First print entry price
        entry_highlight = "<== CURRENT PRICE ZONE" if abs(current_price - entry_price) / entry_price < 0.005 else ""
        print(f"  ◉ Entry: {self.format_price(entry_price)} {entry_highlight}")
        
        # Then print all Fibonacci levels
        for level, price in levels.items():
            price_diff_pct = abs(price - entry_price) / entry_price * 100
            direction = "above" if price > entry_price else "below"
            highlight = "<== CURRENT PRICE ZONE" if closest and level == closest[0] and price != entry_price else ""
            
            print(f"  {level} Fib {'Ext' if is_long else 'Ret'}: {self.format_price(price)} ({price_diff_pct:.2f}% {direction}) {highlight}")

    def display_position(self, position):
        """Display a single position with divine formatting"""
        symbol = position['symbol']
        side = position['side'].upper()
        size = float(position['contracts'])
        notional = float(position['notional'])
        entry_price = float(position['entryPrice'])
        current_price = float(position['markPrice'])
        unrealized_pnl = float(position['unrealizedPnl'] or 0)
        leverage = float(position['leverage'])
        
        # Calculate metrics
        price_diff = (current_price - entry_price) / entry_price
        price_diff_pct = price_diff * 100 * (1 if side == "LONG" else -1)
        
        # Determine colors based on PnL
        pnl_indicator = "🟢" if unrealized_pnl > 0 else "🔴" if unrealized_pnl < 0 else "⚪"
        
        # Display position header
        print(f"\n{pnl_indicator} {symbol} {side} @ {leverage}x")
        print("───────────────────────────────────")
        print(f"  Size:             {size} contracts (${notional:.2f})")
        print(f"  Entry Price:      {self.format_price(entry_price)}")
        print(f"  Current Price:    {self.format_price(current_price)}")
        print(f"  Price Movement:   {self.format_percentage(price_diff_pct)}")
        
        # Animated price movement bar
        movement_bar_range = 1.0  # 1% range on each side
        movement_bar_value = max(-movement_bar_range, min(movement_bar_range, price_diff)) + movement_bar_range
        movement_bar_max = movement_bar_range * 2
        print(f"  {self.animate_progress_bar(movement_bar_value, movement_bar_max)} {self.format_percentage(price_diff_pct)}")
        
        print(f"  Unrealized PnL:   ${unrealized_pnl:.2f}")
        
        # Display Fibonacci levels
        print()
        self.print_fibonacci_levels(entry_price, current_price, side == "LONG")
        print()

    def display_dashboard(self, positions):
        """Display the Fibonacci position dashboard"""
        # Clear screen for fresh output
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Unix/Linux/MacOS
            os.system('clear')
            
        # Calculate divine metrics
        phi_score = self.calculate_phi_resonance(positions)
        schumann_score = self.calculate_schumann_resonance(positions)
        
        # Display logo
        self.display_rasta_logo()
        
        # Check for position changes
        changes = self.detect_position_changes(positions)
        if changes:
            self.display_position_changes(changes)
            
        # Display phi alignment section
        self.display_phi_section(phi_score, schumann_score)
        
        # Portfolio overview
        long_positions = [p for p in positions if p['side'] == 'long']
        short_positions = [p for p in positions if p['side'] == 'short']
        total_notional = sum(float(p['notional']) for p in positions)
        
        print("═" * 72)
        print(f"📊 PORTFOLIO OVERVIEW: {len(long_positions)} long • {len(short_positions)} short • ${total_notional:.2f} notional")
        print("═" * 72)
        
        # Display positions
        if not positions:
            print("\n🔍 No active positions found. The divine balance awaits your trades.\n")
        else:
            for position in sorted(positions, key=lambda x: float(x['notional']) if x['notional'] else 0, reverse=True):
                self.display_position(position)
                
        print("\n" + "═" * 72)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Last updated: {current_time} | {self.get_spinner_frame()} Awaiting divine price movement...")
        print("═" * 72 + "\n")

    def run_once(self):
        """Run a single analysis cycle"""
        positions = self.get_positions()
        self.display_dashboard(positions)
        return positions
        
    def run(self, interval=5):
        """Run the analyzer in continuous mode with intervals"""
        print(f"🔄 Starting BitGet Fibonacci Position Monitor, refreshing every {interval} seconds...")
        print("Press Ctrl+C to exit\n")
        
        try:
            while True:
                self.run_once()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n🛑 Fibonacci monitoring stopped. May your trades align with the Golden Ratio.")

    def find_closest_fibonacci_level(self, entry_price, current_price, is_long=True):
        """Find the closest Fibonacci level to current price"""
        fib_levels = self.generate_fibonacci_levels(entry_price, is_long)
        
        closest_level = None
        closest_distance = float('inf')
        
        for level, price in fib_levels.items():
            distance = abs(current_price - price)
            if distance < closest_distance:
                closest_distance = distance
                closest_level = (level, price)
                
        return closest_level

def display_position_analysis(position_data, analysis_data):
    """Display the position analysis in a structured format"""
    position = position_data
    analysis = analysis_data
    
    # Format the output
    print("\n" + "=" * 80)
    print(f"POSITION ANALYSIS: {position['symbol']} {position['side'].upper()}")
    print("=" * 80)
    
    # Basic position details
    print(f"\n📊 POSITION DETAILS:")
    print(f"  Symbol:          {position.get('symbol')}")
    print(f"  Side:            {position.get('side', '').upper()}")
    print(f"  Size:            {position.get('contracts')} contracts (${position.get('notional_value', 0):.2f})")
    print(f"  Entry Price:     ${position.get('entry_price', 0):.2f}")
    print(f"  Current Price:   ${position.get('mark_price', 0):.2f}")
    print(f"  Price Movement:  {position.get('price_move_percent', 0)}%")
    print(f"  Unrealized PnL:  ${position.get('unrealized_pnl', 0):.2f} ({position.get('percentage_return', 0)}%)")
    
    # Leverage and risk metrics
    print(f"\n⚠️ RISK METRICS:")
    print(f"  Leverage:        {position.get('leverage', 'N/A')}x")
    print(f"  Liquidation:     ${position.get('liquidationPrice', 'N/A'):.2f}")
    if position.get('entry_price') and position.get('liquidationPrice'):
        liq_distance = abs(position.get('liquidationPrice') - position.get('entry_price'))
        liq_percent = (liq_distance / position.get('entry_price')) * 100
        print(f"  Liq. Distance:   {liq_percent:.2f}% from entry")
    
    # Fibonacci Analysis
    print(f"\n🔱 FIBONACCI ANALYSIS:")
    print(f"  Closest Fib Level: {position.get('closest_fibonacci_level', 'N/A')}")
    
    # Position size Phi alignment
    phi_alignment = position.get('position_phi_alignment', {})
    print(f"  Position Phi Alignment: {phi_alignment.get('score', 0):.3f}")
    print(f"  Closest Fibonacci Value: {phi_alignment.get('closest_value', 'N/A')}")
    
    # Print key Fibonacci levels
    print(f"\n  Key Fibonacci Levels:")
    key_levels = ['0', '0.236', '0.382', '0.5', '0.618', '1.0', '1.618']
    for level in key_levels:
        if level in position.get('fibonacci_levels', {}):
            price = position.get('fibonacci_levels', {}).get(level)
            if price:
                current = "◀️ CURRENT" if abs(price - position.get('mark_price')) < 100 else ""
                print(f"    {level.ljust(5)} : ${price:.2f} {current}")
    
    # Schumann Resonance
    schumann = position.get('schumann_resonance', {})
    print(f"\n🌍 SCHUMANN RESONANCE:")
    print(f"  Alignment Score: {schumann.get('alignment', 0):.3f}")
    if schumann.get('alignment', 0) > 0:
        print(f"  Closest Harmonic: {schumann.get('harmonic')} ({schumann.get('frequency', 'N/A')} Hz)")
        print(f"  Base Unit: {schumann.get('base_unit', 'N/A')}")
        print(f"  Resonant Price: ${schumann.get('schumann_price', 0):.2f}")
    
    print("\n" + "-"*80)

def display_portfolio_analysis(analysis):
    """Display portfolio-level analysis"""
    portfolio = analysis.get('portfolio', {})
    
    print("\n" + "="*80)
    print("BITGET PORTFOLIO FIBONACCI & SCHUMANN ANALYSIS")
    print("="*80)
    
    # Display position counts
    print(f"\n📈 PORTFOLIO OVERVIEW:")
    print(f"  Long Positions:  {portfolio.get('long_positions')} (${portfolio.get('long_notional', 0):.2f})")
    print(f"  Short Positions: {portfolio.get('short_positions')} (${portfolio.get('short_notional', 0):.2f})")
    
    # Display Long:Short ratio if both exist
    if portfolio.get('long_short_ratio') is not None:
        print(f"  Long:Short Ratio: {portfolio.get('long_short_ratio'):.3f}")
        if portfolio.get('golden_ratio_alignment'):
            print(f"  ✨ GOLDEN RATIO ALIGNMENT DETECTED!")
    
    # Display Phi Resonance
    print(f"\n🔱 PHI RESONANCE: {portfolio.get('phi_resonance')}")
    print(f"  {portfolio.get('phi_resonance_description')}")
    
    # Display portfolio Schumann resonance
    schumann = portfolio.get('schumann_resonance', {})
    print(f"\n🌍 PORTFOLIO SCHUMANN RESONANCE:")
    print(f"  Alignment Score: {schumann.get('alignment', 0):.3f}")
    if schumann.get('alignment', 0) > 0:
        print(f"  Closest Harmonic: {schumann.get('harmonic')} ({schumann.get('frequency', 'N/A')} Hz)")
        print(f"  Base Unit: {schumann.get('base_unit', 'N/A')}")
        print(f"  Resonant Price: ${schumann.get('schumann_price', 0):.2f}")
    
    print("\n" + "-"*80)

def main():
    """Main entry point"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='BitGet Fibonacci Golden Ratio & Schumann Resonance Analyzer')
    parser.add_argument('--testnet', action='store_true', help='Use BitGet testnet instead of mainnet')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    parser.add_argument('--save', action='store_true', help='Save results to file')
    parser.add_argument('--output', type=str, default='bitget_analysis.json', help='Output file for JSON results')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    parser.add_argument('--interval', type=int, default=5, help='Refresh interval in seconds')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = BitGetFibonacciAnalyzer(use_testnet=args.testnet, debug=args.debug)
    
    # Connect to BitGet
    if not analyzer.connect():
        logger.error("Failed to connect to BitGet API")
        return
    
    # Run analysis
    results = analyzer.run_analysis()
    
    # Display or save results
    if args.json:
        if args.save:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Analysis saved to {args.output}")
        else:
            print(json.dumps(results, indent=2))
    else:
        if results['status'] == 'success':
            # Display portfolio analysis
            display_portfolio_analysis(results)
            
            # Display each position
            for pos_analysis in results['positions']:
                display_position_analysis(pos_analysis['position'], pos_analysis['analysis'])
        else:
            print(f"\n{results['message']}")
    
    if args.save and not args.json:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Analysis saved to {args.output}")

if __name__ == "__main__":
    main() 