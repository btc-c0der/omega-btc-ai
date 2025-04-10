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
RASTA BitGet Position Viewer - STREAMING EDITION
Continuously monitors and displays BitGet positions with divine Rasta styling
"""

import os
import sys
import json
import time
import logging
import signal
import argparse
import random
from dotenv import load_dotenv
from datetime import datetime

# Import Position Harmony Advisor
try:
    from omega_ai.recommendations.position_harmony import PositionHarmonyAdvisor
    HARMONY_ADVISOR_AVAILABLE = True
except ImportError:
    HARMONY_ADVISOR_AVAILABLE = False
    logging.warning("PositionHarmonyAdvisor not available. Install omega-ai for full functionality.")

# Constants for Mathematical Harmony
PHI = 1.618034  # Golden Ratio - Divine Proportion
INV_PHI = 0.618034  # Inverse Golden Ratio
SCHUMANN_BASE = 7.83  # Earth's base frequency (Hz)

# ANSI Color Codes - Rasta Colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'
CYAN = '\033[96m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
WHITE = '\033[97m'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add file handler to save logs to a file
file_handler = logging.FileHandler('rasta_bitget_monitor.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Load environment variables from .env file
load_dotenv()

# ASCII frames for loading animation
LOADING_FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
RASTA_FRAMES = [f"{GREEN}♦{RESET}", f"{YELLOW}♦{RESET}", f"{RED}♦{RESET}"]

class RastaBitgetMonitor:
    """Continuously monitors and displays BitGet positions with divine styling"""
    
    def __init__(self, interval=5, use_color=True, debug=False, harmony_advisor=True):
        """Initialize the BitGet position monitor
        
        Args:
            interval: Refresh interval in seconds
            use_color: Whether to use color in output
            debug: Show debug information
            harmony_advisor: Whether to use the Position Harmony Advisor
        """
        self.interval = interval
        self.use_color = use_color
        self.debug = debug
        self.use_harmony_advisor = harmony_advisor and HARMONY_ADVISOR_AVAILABLE
        
        # Initialize Position Harmony Advisor if available
        if self.use_harmony_advisor:
            self.harmony_advisor = PositionHarmonyAdvisor(
                max_account_risk=0.0618,  # Divine 6.18% max risk
                position_phi_targets=True,
                long_short_balance=True
            )
            logger.info("Position Harmony Advisor initialized")
        else:
            self.harmony_advisor = None
            if harmony_advisor and not HARMONY_ADVISOR_AVAILABLE:
                logger.warning("Position Harmony Advisor requested but not available")
        
        # Frame counter for animations
        self.frame_counter = 0
        
        # Previous states for change detection
        self.previous_positions = []
        self.previous_notional = 0
        self.account_balance = 0  # Will be estimated from positions
        
        # Register signal handler for clean exit
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, sig, frame):
        """Handle keyboard interrupt (Ctrl+C) gracefully"""
        print(f"\n{RESET}{GREEN}💚 JAH BLESS YOUR TRADING JOURNEY 💚{RESET}")
        print(f"{YELLOW}Fibonacci flows through all positions...{RESET}")
        sys.exit(0)
    
    def display_rasta_logo(self):
        """Display the RASTA BITGET ASCII logo with frame animation"""
        # Rotate colors based on frame counter
        color_index = self.frame_counter % 3
        highlight_color = [GREEN, YELLOW, RED][color_index]
        
        print(f"\n{YELLOW}")
        print("╔═════════════════════════════════════════════════════════════════════╗")
        print("║                                                                     ║")
        print("║   ███████╗██╗██████╗  ██████╗     ██████╗ ████████╗ ██████╗        ║")
        print("║   ██╔════╝██║██╔══██╗██╔═══██╗    ██╔══██╗╚══██╔══╝██╔════╝        ║")
        print("║   █████╗  ██║██████╔╝██║   ██║    ██████╔╝   ██║   ██║             ║")
        print(f"║   ██╔══╝  ██║██╔══██╗██║   ██║    ██╔══██╗   ██║   ██║{RED}     ▄█╗   ▄█╗{YELLOW}  ║")
        print(f"║   ██║     ██║██████╔╝╚██████╔╝    ██████╔╝   ██║   ╚██████╗{RED}  ╚═╝{GREEN}╔╗{RED}╚═╝{YELLOW}  ║")
        print(f"║   ╚═╝     ╚═╝╚═════╝  ╚═════╝     ╚═════╝    ╚═╝    ╚═════╝    {GREEN}╚═╝   {YELLOW} ║")
        print("║                                                                     ║")
        print(f"║   {RED}█{YELLOW}█{GREEN}█{YELLOW} RASTA BITGET POSITIONS {CYAN}φ{YELLOW} GOLDEN RATIO HARMONY {RED}█{YELLOW}█{GREEN}█{YELLOW}   ║")
        print(f"║                                              {highlight_color}LIVE{YELLOW} {LOADING_FRAMES[self.frame_counter % len(LOADING_FRAMES)]}        ║")
        print("╚═════════════════════════════════════════════════════════════════════╝")
        print(RESET)
    
    def display_phi_circle(self):
        """Display a small PHI symbol with circular design that animates"""
        phi_frames = [
            f"{YELLOW}◯{CYAN}φ{YELLOW}◯{RESET}",
            f"{YELLOW}◉{CYAN}φ{YELLOW}◯{RESET}",
            f"{YELLOW}◯{CYAN}φ{YELLOW}◉{RESET}",
            f"{YELLOW}◉{CYAN}φ{YELLOW}◉{RESET}"
        ]
        return phi_frames[self.frame_counter % len(phi_frames)]
    
    def fibonacci_bar(self, percentage, width=50):
        """Create a Fibonacci-colored progress bar"""
        filled_width = int(width * min(abs(percentage) / 100, 1))
        empty_width = width - filled_width
        
        # Choose color based on position side
        if percentage >= 0:
            color = GREEN
        else:
            color = RED
            
        bar = f"{color}{'█' * filled_width}{RESET}{'░' * empty_width}"
        return bar
    
    def animated_fibonacci_bar(self, percentage, width=50):
        """Create an animated Fibonacci-colored progress bar"""
        filled_width = int(width * min(abs(percentage) / 100, 1))
        empty_width = width - filled_width
        
        # Choose color based on value
        if percentage >= 0:
            base_color = GREEN
        else:
            base_color = RED
        
        # Animate the last character of the filled portion
        if filled_width > 0:
            animation_chars = ['▏', '▎', '▍', '▌', '▋', '▊', '▉', '█']
            anim_index = self.frame_counter % len(animation_chars)
            
            bar = f"{base_color}{'█' * (filled_width-1)}{animation_chars[anim_index]}{RESET}{'░' * empty_width}"
        else:
            bar = f"{'░' * width}"
        
        return bar
    
    def get_positions(self):
        """Fetch and return BitGet positions"""
        # Get API credentials from environment
        api_key = os.getenv("BITGET_API_KEY", "")
        secret_key = os.getenv("BITGET_SECRET_KEY", "")
        passphrase = os.getenv("BITGET_PASSPHRASE", "")
        
        # Verify API credentials
        if not api_key or not secret_key or not passphrase:
            logger.error("Missing BitGet API credentials in environment variables")
            return {"error": "Missing credentials"}
        
        # Create direct CCXT BitGet client
        try:
            import ccxt
            
            # Create the exchange client
            exchange = ccxt.bitget({
                'apiKey': api_key,
                'secret': secret_key,
                'password': passphrase,
                'options': {
                    'defaultType': 'swap',
                }
            })
            
            # Fetch positions
            # Note: fetchPositions is a method provided by the ccxt library
            # The linter may not recognize it, but it exists in the library
            positions = exchange.fetchPositions()
            
            # Filter out positions with zero contracts
            active_positions = [p for p in positions if float(p.get('contracts', 0)) > 0]
            
            # Return position data and API connection info
            return {
                "success": True,
                "positions": active_positions,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "connection": "CONNECTED TO BITGET MAINNET"
            }
            
        except ImportError:
            logger.error("ccxt module not installed")
            return {"error": "ccxt module not installed"}
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return {"error": str(e)}
    
    def detect_position_changes(self, current_positions):
        """Detect changes between current and previous positions"""
        changes = {
            "new": [],
            "closed": [],
            "changed": []
        }
        
        if not self.previous_positions:
            # First run, no changes to detect
            self.previous_positions = current_positions
            return None
        
        # Find current position symbols
        current_symbols = {p.get('symbol'): p for p in current_positions}
        prev_symbols = {p.get('symbol'): p for p in self.previous_positions}
        
        # Detect new positions
        for symbol, position in current_symbols.items():
            if symbol not in prev_symbols:
                changes["new"].append(position)
            else:
                # Check if position size or PnL changed significantly
                prev_pos = prev_symbols[symbol]
                curr_contracts = float(position.get('contracts', 0))
                prev_contracts = float(prev_pos.get('contracts', 0))
                curr_pnl = float(position.get('unrealizedPnl', 0))
                prev_pnl = float(prev_pos.get('unrealizedPnl', 0))
                
                # Detect significant changes (>5% position size or >10% PnL)
                if abs(curr_contracts - prev_contracts) / prev_contracts > 0.05 or \
                   abs(curr_pnl - prev_pnl) > abs(prev_pnl * 0.1):
                    changes["changed"].append({
                        "position": position,
                        "prev_contracts": prev_contracts,
                        "prev_pnl": prev_pnl
                    })
        
        # Detect closed positions
        for symbol, position in prev_symbols.items():
            if symbol not in current_symbols:
                changes["closed"].append(position)
        
        # Update previous positions for next comparison
        self.previous_positions = current_positions
        
        # Return None if no changes detected
        if not changes["new"] and not changes["closed"] and not changes["changed"]:
            return None
            
        return changes
    
    def print_changes(self, changes):
        """Print position changes with Rasta styling"""
        if not changes:
            return
            
        print(f"\n{YELLOW}{'=' * 80}")
        print(f"{BOLD}{RED}🔄{YELLOW} POSITION CHANGES DETECTED {GREEN}🔄{RESET}")
        print(f"{YELLOW}{'=' * 80}{RESET}")
        
        # Print new positions
        if changes["new"]:
            print(f"\n{GREEN}🆕 NEW POSITIONS:{RESET}")
            for position in changes["new"]:
                symbol = position.get('symbol', 'UNKNOWN')
                side = position.get('side', 'UNKNOWN').upper()
                contracts = float(position.get('contracts', 0))
                
                side_color = GREEN if side == "LONG" else RED
                print(f"  {side_color}{'▲' if side == 'LONG' else '▼'} {symbol}: {contracts} contracts{RESET}")
        
        # Print closed positions
        if changes["closed"]:
            print(f"\n{RED}🚫 CLOSED POSITIONS:{RESET}")
            for position in changes["closed"]:
                symbol = position.get('symbol', 'UNKNOWN')
                side = position.get('side', 'UNKNOWN').upper()
                contracts = float(position.get('contracts', 0))
                pnl = float(position.get('unrealizedPnl', 0))
                
                pnl_color = GREEN if pnl >= 0 else RED
                print(f"  {RED}✖ {symbol} {side}: {contracts} contracts, PnL: {pnl_color}${pnl:.2f}{RESET}")
        
        # Print changed positions
        if changes["changed"]:
            print(f"\n{CYAN}📊 CHANGED POSITIONS:{RESET}")
            for change_data in changes["changed"]:
                position = change_data["position"]
                symbol = position.get('symbol', 'UNKNOWN')
                side = position.get('side', 'UNKNOWN').upper()
                contracts = float(position.get('contracts', 0))
                prev_contracts = change_data["prev_contracts"]
                curr_pnl = float(position.get('unrealizedPnl', 0))
                prev_pnl = change_data["prev_pnl"]
                
                # Calculate changes
                size_change = contracts - prev_contracts
                size_change_pct = (size_change / prev_contracts) * 100 if prev_contracts else 0
                pnl_change = curr_pnl - prev_pnl
                
                # Determine colors
                side_color = GREEN if side == "LONG" else RED
                size_color = GREEN if size_change > 0 else RED
                pnl_color = GREEN if pnl_change > 0 else RED
                
                print(f"  {side_color}{symbol} {side}:{RESET}")
                print(f"    Size: {prev_contracts} → {contracts} ({size_color}{size_change:+.4f} / {size_change_pct:+.2f}%{RESET})")
                print(f"    PnL: ${prev_pnl:.2f} → ${curr_pnl:.2f} ({pnl_color}${pnl_change:+.2f}{RESET})")
    
    def display_market_wisdom(self):
        """Display random Rasta trading wisdom quotes"""
        wisdom_quotes = [
            "Position sizing aligned with φ creates harmonic trading",
            "When positions resonate with Schumann frequency, profits flow naturally",
            "Babylon system traps fade when Golden Ratio guides your entries",
            "Trust the Fibonacci sequence in every market cycle",
            "Align with natural patterns, not market maker traps",
            "The divine proportion reveals hidden support and resistance",
            "Trade with the rhythm of the Fibonacci spiral",
            "PHI is the divine key to trading success",
            "0.618 retracement offers the perfect entry point",
            "Every position size should honor the Golden Ratio"
        ]
        
        # Select a quote based on frame counter
        quote_index = self.frame_counter % len(wisdom_quotes)
        return wisdom_quotes[quote_index]
    
    def generate_fibonacci_levels(self, base_price, side):
        """Generate Fibonacci levels based on entry price and position side"""
        levels = []
        
        if side == "LONG":
            # For long positions, generate levels above entry
            levels.append(("Entry", base_price))
            levels.append(("0.236 Fib Ext", base_price * (1 + 0.236)))
            levels.append(("0.382 Fib Ext", base_price * (1 + 0.382)))
            levels.append(("0.5 Fib Ext", base_price * (1 + 0.5)))
            levels.append(("0.618 Fib Ext", base_price * (1 + 0.618)))
            levels.append(("0.786 Fib Ext", base_price * (1 + 0.786)))
            levels.append(("1.0 Fib Ext", base_price * 2))
            levels.append(("1.618 Fib Ext", base_price * (1 + 1.618)))
        else:
            # For short positions, generate levels below entry
            levels.append(("Entry", base_price))
            levels.append(("0.236 Fib Ret", base_price * (1 - 0.236)))
            levels.append(("0.382 Fib Ret", base_price * (1 - 0.382)))
            levels.append(("0.5 Fib Ret", base_price * (1 - 0.5)))
            levels.append(("0.618 Fib Ret", base_price * (1 - 0.618)))
            levels.append(("0.786 Fib Ret", base_price * (1 - 0.786)))
            
        return levels
    
    def print_position(self, position):
        """Format and print a position with Rasta styling"""
        # Basic information
        symbol = position.get('symbol', 'UNKNOWN')
        side = position.get('side', 'UNKNOWN').upper()
        contracts = float(position.get('contracts', 0))
        notional = float(position.get('notional', 0))
        entry_price = float(position.get('entryPrice', 0))
        mark_price = float(position.get('markPrice', 0))
        unrealized_pnl = float(position.get('unrealizedPnl', 0))
        percentage = float(position.get('percentage', 0))
        leverage = float(position.get('leverage', 0))
        liquidation_price = float(position.get('liquidationPrice', 0))
        
        # Additional fields with N/A handling
        margin_mode = position.get('marginMode', 'N/A')
        collateral = position.get('collateral', 'N/A')
        timestamp = position.get('timestamp', 'N/A')
        cost = position.get('cost', 'N/A')
        initialMargin = position.get('initialMargin', 'N/A')
        maxNotional = position.get('maxNotional', 'N/A')
        margin = position.get('margin', 'N/A')
        maintenanceMargin = position.get('maintenanceMargin', 'N/A')
        
        # Choose color based on position side
        side_color = GREEN if side == "LONG" else RED
        
        # Generate Fibonacci levels
        fib_levels = self.generate_fibonacci_levels(entry_price, side)
        
        # Print position details
        print(f"\n{YELLOW}{'─' * 80}{RESET}")
        print(f"{BOLD}{side_color}{'▲' if side == 'LONG' else '▼'} POSITION: {symbol} {side}{RESET}")
        print(f"{YELLOW}{'─' * 80}{RESET}")
        
        print(f"\n{BOLD}{CYAN}📊 POSITION DETAILS:{RESET}")
        print(f"  {YELLOW}Symbol:          {symbol}{RESET}")
        print(f"  {YELLOW}Side:            {side_color}{side}{RESET}")
        print(f"  {YELLOW}Size:            {contracts} contracts (${notional:.2f}){RESET}")
        print(f"  {YELLOW}Entry Price:     ${entry_price:.2f}{RESET}")
        print(f"  {YELLOW}Current Price:   ${mark_price:.2f}{RESET}")
        
        # Calculate price movement
        price_move = ((mark_price - entry_price) / entry_price) * 100
        if side == "SHORT":
            price_move = -price_move
        
        # Create an animated progress bar for price movement
        price_bar = self.animated_fibonacci_bar(price_move)
        price_color = GREEN if price_move >= 0 else RED
        print(f"  {YELLOW}Price Movement:  {price_color}{price_move:.2f}%{RESET}")
        print(f"  {price_bar} {price_color}{price_move:.2f}%{RESET}")
        
        pnl_color = GREEN if unrealized_pnl >= 0 else RED
        print(f"  {YELLOW}Unrealized PnL:  {pnl_color}${unrealized_pnl:.2f} ({percentage:.2f}%){RESET}")
        
        # Additional position information
        print(f"\n{BOLD}{CYAN}🔍 DETAILED DATA:{RESET}")
        print(f"  {YELLOW}Margin Mode:     {margin_mode}{RESET}")
        print(f"  {YELLOW}Collateral:      {collateral}{RESET}")
        print(f"  {YELLOW}Cost:            {cost}{RESET}")
        print(f"  {YELLOW}Initial Margin:  {initialMargin}{RESET}")
        print(f"  {YELLOW}Margin:          {margin}{RESET}")
        print(f"  {YELLOW}Maint. Margin:   {maintenanceMargin}{RESET}")
        print(f"  {YELLOW}Max Notional:    {maxNotional}{RESET}")
        if timestamp != 'N/A':
            try:
                # Try to format timestamp if it's a number
                dt = datetime.fromtimestamp(int(timestamp)/1000) if isinstance(timestamp, (int, float, str)) else timestamp
                print(f"  {YELLOW}Timestamp:       {dt}{RESET}")
            except (ValueError, TypeError):
                print(f"  {YELLOW}Timestamp:       {timestamp}{RESET}")
        else:
            print(f"  {YELLOW}Timestamp:       N/A{RESET}")
        
        # Raw JSON data if in debug mode
        if self.debug:
            print(f"\n{BOLD}{MAGENTA}🔄 RAW DATA:{RESET}")
            for key, value in position.items():
                if key not in ['symbol', 'side', 'contracts', 'notional', 'entryPrice', 'markPrice', 
                              'unrealizedPnl', 'percentage', 'leverage', 'liquidationPrice', 
                              'marginMode', 'collateral', 'timestamp', 'cost', 'initialMargin',
                              'maxNotional', 'margin', 'maintenanceMargin']:
                    print(f"  {YELLOW}{key}: {value}{RESET}")
        
        # Risk metrics
        print(f"\n{BOLD}{RED}⚠️ RISK METRICS:{RESET}")
        print(f"  {YELLOW}Leverage:        {leverage}x{RESET}")
        print(f"  {YELLOW}Liquidation:     ${liquidation_price:.2f}{RESET}")
        
        if entry_price and liquidation_price:
            liq_distance = abs(liquidation_price - entry_price)
            liq_percent = (liq_distance / entry_price) * 100
            
            # Assess liquidation risk based on distance
            if liq_percent < 10:
                liq_risk_color = RED
                liq_risk_text = "HIGH RISK"
            elif liq_percent < 20:
                liq_risk_color = YELLOW
                liq_risk_text = "MEDIUM RISK"
            else:
                liq_risk_color = GREEN
                liq_risk_text = "LOW RISK"
                
            print(f"  {YELLOW}Liq. Distance:   {liq_risk_color}{liq_percent:.2f}% from entry ({liq_risk_text}){RESET}")
        
        # Display Fibonacci levels
        print(f"\n{BOLD}{CYAN}φ FIBONACCI LEVELS:{RESET}")
        
        # Check if current price is near any Fibonacci level
        closest_level = min(fib_levels, key=lambda x: abs(x[1] - mark_price))
        
        for level_name, level_price in fib_levels:
            # Highlight if this is the closest level to current price
            if level_price == closest_level[1]:
                level_indicator = f"{BOLD}{CYAN}◉ {level_name}: ${level_price:.2f} <== CURRENT PRICE ZONE{RESET}"
            else:
                distance = ((level_price - mark_price) / mark_price) * 100
                direction = "above" if level_price > mark_price else "below"
                level_indicator = f"{YELLOW}{level_name}: ${level_price:.2f} ({abs(distance):.2f}% {direction}){RESET}"
            
            print(f"  {level_indicator}")
    
    def display_harmony_status(self, harmony_analysis):
        """Display position harmony status and recommendations"""
        if not harmony_analysis:
            return
        
        # Get key metrics from analysis
        harmony_score = harmony_analysis.get('harmony_score', 0)
        harmony_state = harmony_analysis.get('harmony_state', 'UNKNOWN')
        divine_advice = harmony_analysis.get('divine_advice', '')
        recommendations = harmony_analysis.get('recommendations', [])
        
        # Choose color based on harmony score
        if harmony_score >= 0.7:
            harmony_color = GREEN
        elif harmony_score >= 0.4:
            harmony_color = YELLOW
        else:
            harmony_color = RED
        
        print(f"\n{YELLOW}{'═' * 80}{RESET}")
        print(f"{BOLD}{CYAN}φ POSITION HARMONY ANALYSIS {self.display_phi_circle()}{RESET}")
        print(f"{YELLOW}{'═' * 80}{RESET}")
        
        # Display harmony score with animated bar
        print(f"\n{BOLD}HARMONY STATUS:{RESET}")
        print(f"  {CYAN}φ Harmony Score:   {harmony_color}{harmony_score:.3f}{RESET}")
        harmony_bar = self.animated_fibonacci_bar(harmony_score * 100)
        print(f"  {harmony_bar} {harmony_color}{int(harmony_score * 100)}%{RESET}")
        print(f"  {CYAN}✨ Harmony State:   {harmony_color}{harmony_state}{RESET}")
        
        # Display divine advice
        print(f"\n{BOLD}DIVINE ADVICE:{RESET}")
        print(f"  {MAGENTA}☯ {divine_advice}{RESET}")
        
        # Display recommendations if any
        if recommendations:
            print(f"\n{BOLD}RECOMMENDATIONS:{RESET}")
            for i, rec in enumerate(recommendations, 1):
                rec_type = rec.get('type', 'unknown')
                description = rec.get('description', 'No description')
                confidence = rec.get('confidence', 0)
                
                confidence_color = GREEN if confidence > 0.7 else (YELLOW if confidence > 0.4 else RED)
                print(f"  {i}. {description}")
                
                # Show additional details based on recommendation type
                if rec_type == 'exposure':
                    current = rec.get('current', 0) * 100
                    target = rec.get('target', 0) * 100
                    print(f"     Current exposure: {current:.2f}%, Target: {target:.2f}%")
                elif rec_type == 'long_short_balance':
                    current_ratio = rec.get('current_ratio', 0)
                    target_ratio = rec.get('target_ratio', 0)
                    print(f"     Current ratio: {current_ratio:.3f}, Target ratio: {target_ratio:.3f}")
                elif rec_type == 'position_size':
                    symbol = rec.get('position_symbol', 'UNKNOWN')
                    current_pct = rec.get('current_size_pct', 0) * 100
                    target_pct = rec.get('target_size_pct', 0) * 100
                    print(f"     {symbol}: Current: {current_pct:.2f}%, Target: {target_pct:.2f}%")
        else:
            print(f"\n{GREEN}⚡ No recommendations - positions in divine harmony!{RESET}")
            
        # Display ideal position sizes
        ideal_sizes = harmony_analysis.get('ideal_position_sizes', [])
        if ideal_sizes:
            print(f"\n{BOLD}IDEAL POSITION SIZES:{RESET}")
            for i, size in enumerate(ideal_sizes[:5], 1):  # Show top 5 sizes
                size_pct = size.get('size_pct', 0) * 100
                absolute_size = size.get('absolute_size', 0)
                fib_relation = size.get('fibonacci_relation', '')
                risk = size.get('risk_category', 'unknown').upper()
                
                risk_color = GREEN if risk == "MICRO" else (YELLOW if risk == "LOW" or risk == "MODERATE" else RED)
                print(f"  {CYAN}φ {fib_relation}:{RESET} ${absolute_size:.2f} ({size_pct:.2f}% - {risk_color}{risk}{RESET})")
    
    def display_dashboard(self, data):
        """Display the BitGet positions dashboard"""
        # Clear screen - use cls for Windows, clear for Unix
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Update frame counter
        self.frame_counter += 1
        
        # Display logo
        self.display_rasta_logo()
        
        # Check for data errors
        if "error" in data:
            print(f"\n{RED}⚠️  ERROR: {data['error']}{RESET}")
            print(f"\n{YELLOW}Reconnecting in {self.interval} seconds...{RESET}")
            return
        
        # Get connection info and positions
        connection_status = data.get("connection", "UNKNOWN")
        positions = data.get("positions", [])
        timestamp = data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Print connection status
        print(f"{GREEN}✓ {BOLD}CONNECTED TO BITGET MAINNET{RESET} {self.display_phi_circle()}")
        print(f"{CYAN}Last Update: {timestamp}{RESET}")
        
        # Check if we have positions
        if not positions:
            print(f"\n{YELLOW}🔍 JAH SAYS: NO ACTIVE POSITIONS FOUND{RESET}")
            
            # Display small Rasta flag with animation
            flag_styles = [
                f"\n{GREEN}▀▀▀{YELLOW}▀▀▀{RED}▀▀▀{RESET}",
                f"\n{GREEN}▀▀▀{YELLOW}▀▀▀{RED}▀▀▀{RESET} {LOADING_FRAMES[self.frame_counter % len(LOADING_FRAMES)]}",
                f"\n{GREEN}▀▀▀{YELLOW}▀▀▀{RED}▀▀▀{RESET} {RASTA_FRAMES[self.frame_counter % len(RASTA_FRAMES)]}"
            ]
            print(flag_styles[self.frame_counter % len(flag_styles)])
            
            # Display waiting message
            print(f"\n{CYAN}Waiting for positions... Refresh in {self.interval} seconds{RESET}")
            return
        
        # Count position types for summary
        long_count = sum(1 for p in positions if p.get('side', '').upper() == 'LONG')
        short_count = sum(1 for p in positions if p.get('side', '').upper() == 'SHORT')
        
        # Calculate total notional value
        total_notional = sum(float(p.get('notional', 0)) for p in positions)
        
        # Estimate account balance if not set
        # We use a very crude estimate for demonstration purposes
        if not self.account_balance:
            # Assume total exposure is around 30% of account on average
            # This is just for demo purposes, in a real implementation
            # we would get the actual account balance from the API
            self.account_balance = max(total_notional / 0.3, 1000)
        
        # Check for notional change
        notional_change = total_notional - self.previous_notional
        notional_change_pct = (notional_change / self.previous_notional * 100) if self.previous_notional else 0
        self.previous_notional = total_notional
        
        notional_change_text = ""
        if abs(notional_change) > 0.01:
            change_color = GREEN if notional_change > 0 else RED
            notional_change_text = f" ({change_color}{notional_change:+.2f} / {notional_change_pct:+.2f}%{RESET})"
        
        # Print positions header
        print(f"\n{YELLOW}{'═' * 80}{RESET}")
        print(f"{BOLD}{RED}█{YELLOW}█{GREEN}█{RESET} {BOLD}RASTA BITGET PORTFOLIO OVERVIEW{RESET}")
        print(f"{YELLOW}{'═' * 80}{RESET}")
        
        print(f"\n{BOLD}POSITION SUMMARY:{RESET}")
        print(f"  {GREEN}◉ Long Positions:  {long_count}{RESET}")
        print(f"  {RED}◉ Short Positions: {short_count}{RESET}")
        print(f"  {CYAN}◉ Total Notional:  ${total_notional:.2f}{notional_change_text}{RESET}")
        print(f"  {CYAN}◉ Est. Account:    ${self.account_balance:.2f}{RESET}")
        
        # Calculate Phi resonance (how close position sizing is to Golden Ratio)
        if long_count > 0 and short_count > 0:
            ratio = max(long_count, short_count) / min(long_count, short_count)
            phi_resonance = 1 - abs(ratio - PHI) / PHI
            phi_resonance = max(0, min(phi_resonance, 1))  # Normalize between 0-1
            
            # Display Phi resonance with animated bar
            print(f"\n{BOLD}DIVINE METRICS:{RESET}")
            print(f"  {CYAN}φ Phi Resonance:   {phi_resonance:.3f}{RESET}")
            bar = self.animated_fibonacci_bar(phi_resonance * 100)
            print(f"  {bar} {int(phi_resonance * 100)}%")
            
            # Add Schumann resonance alignment
            # This is just for display purposes - generates a random but consistent value
            schumann_alignment = ((hash(str(positions)) % 1000) / 1000) * 0.7 + 0.3  # 0.3-1.0 range
            print(f"  {MAGENTA}⚡ Schumann:        {schumann_alignment:.3f}{RESET}")
            schumann_bar = self.animated_fibonacci_bar(schumann_alignment * 100)
            print(f"  {schumann_bar} {int(schumann_alignment * 100)}%")
        
        # Run Position Harmony Analysis if advisor is available
        harmony_analysis = None
        if self.use_harmony_advisor and positions:
            # Convert positions to format expected by PositionHarmonyAdvisor
            formatted_positions = []
            for p in positions:
                formatted_positions.append({
                    'symbol': p.get('symbol', 'UNKNOWN'),
                    'side': p.get('side', 'long').lower(),
                    'notional': float(p.get('notional', 0)),
                    'leverage': float(p.get('leverage', 1)),
                    'entry_price': float(p.get('entryPrice', 0)),
                    'mark_price': float(p.get('markPrice', 0)),
                    'unrealized_pnl': float(p.get('unrealizedPnl', 0))
                })
                
            # Get harmony analysis
            try:
                harmony_analysis = self.harmony_advisor.analyze_positions(
                    positions=formatted_positions,
                    account_balance=self.account_balance,
                    leverage=1.0  # Use 1.0 for simplicirt
                )
                
                # Display harmony analysis
                self.display_harmony_status(harmony_analysis)
            except Exception as e:
                logger.error(f"Error in harmony analysis: {e}")
                print(f"\n{RED}⚠️ Harmony analysis error: {str(e)}{RESET}")
        
        # Check and print position changes
        changes = self.detect_position_changes(positions)
        self.print_changes(changes)
        
        # Display positions
        for position in positions:
            self.print_position(position)
        
        # Display footer with wisdom
        print(f"\n{YELLOW}{'═' * 80}")
        print(f"{BOLD}RASTA TRADING WISDOM:{RESET} {BOLD}{self.display_market_wisdom()}{RESET}")
        print(f"{YELLOW}{'═' * 80}{RESET}")
        
        # Display refresh indicator
        print(f"\n{CYAN}Next update in {self.interval} seconds... {LOADING_FRAMES[self.frame_counter % len(LOADING_FRAMES)]}{RESET}")
    
    def run(self):
        """Main execution loop"""
        try:
            while True:
                # Fetch position data
                data = self.get_positions()
                
                # Display dashboard
                self.display_dashboard(data)
                
                # Wait for next update
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            self._signal_handler(None, None)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='RASTA BitGet Position Monitor')
    parser.add_argument('--interval', type=int, default=5,
                        help='Update interval in seconds (default: 5)')
    parser.add_argument('--no-color', action='store_true',
                        help='Disable colored output')
    parser.add_argument('--debug', action='store_true',
                        help='Show debug information')
    parser.add_argument('--no-harmony', action='store_true',
                        help='Disable Position Harmony Advisor')
    return parser.parse_args()

def main():
    """Main entry point"""
    args = parse_arguments()
    
    monitor = RastaBitgetMonitor(
        interval=args.interval,
        use_color=not args.no_color,
        debug=args.debug,
        harmony_advisor=not args.no_harmony
    )
    
    # Start the monitor
    monitor.run()

if __name__ == "__main__":
    main() 