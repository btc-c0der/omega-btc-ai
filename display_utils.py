#!/usr/bin/env python3
"""
Display Utils for Rasta BitGet Monitor

Handles all terminal display and UI functionality for the Rasta BitGet Position Monitor
with colorful Rasta styling and intuitive visualizations.
"""

import os
import sys
import time
import random
from datetime import datetime
from typing import Dict, List, Any, Optional

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

# Loading animation frames
LOADING_FRAMES = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
RASTA_FRAMES = [f"{GREEN}♦{RESET}", f"{YELLOW}♦{RESET}", f"{RED}♦{RESET}"]

class RastaDisplayManager:
    """Manages display functionality for the Rasta BitGet Position Monitor"""
    
    def __init__(self, use_color=True, debug=False):
        """Initialize the display manager
        
        Args:
            use_color: Whether to use color in output
            debug: Show debug information
        """
        self.use_color = use_color
        self.debug = debug
        self.frame_counter = 0
        
        # Disable colors if not wanted
        if not use_color:
            global GREEN, YELLOW, RED, RESET, BOLD, CYAN, BLUE, MAGENTA, WHITE
            GREEN = YELLOW = RED = RESET = BOLD = CYAN = BLUE = MAGENTA = WHITE = ''
    
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
        print(f"  {YELLOW}Leverage:        {leverage}x{RESET}")
        print(f"  {YELLOW}Liquidation:     ${liquidation_price:.2f}{RESET}")
        
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
        
        # Risk metrics section
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
                
            print(f"\n{BOLD}{RED}⚠️ RISK ASSESSMENT:{RESET}")
            print(f"  {YELLOW}Liq. Distance:   {liq_risk_color}{liq_percent:.2f}% from entry ({liq_risk_text}){RESET}")
    
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
    
    def display_dashboard(self, data, harmony_analysis=None):
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
            print(f"\n{YELLOW}Reconnecting in a few seconds...{RESET}")
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
            print(f"\n{CYAN}Waiting for positions... {RESET}")
            return
        
        # Count position types for summary
        long_count = sum(1 for p in positions if p.get('side', '').upper() == 'LONG')
        short_count = sum(1 for p in positions if p.get('side', '').upper() == 'SHORT')
        
        # Calculate total notional value
        total_notional = sum(float(p.get('notional', 0)) for p in positions)
        account_balance = data.get("account_balance", 0)
        
        # Print positions header
        print(f"\n{YELLOW}{'═' * 80}{RESET}")
        print(f"{BOLD}{RED}█{YELLOW}█{GREEN}█{RESET} {BOLD}RASTA BITGET PORTFOLIO OVERVIEW{RESET}")
        print(f"{YELLOW}{'═' * 80}{RESET}")
        
        print(f"\n{BOLD}POSITION SUMMARY:{RESET}")
        print(f"  {GREEN}◉ Long Positions:  {long_count}{RESET}")
        print(f"  {RED}◉ Short Positions: {short_count}{RESET}")
        print(f"  {CYAN}◉ Total Notional:  ${total_notional:.2f}{RESET}")
        print(f"  {CYAN}◉ Account Balance: ${account_balance:.2f}{RESET}")
        
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
        
        # Position Harmony Analysis
        if harmony_analysis:
            self.display_harmony_status(harmony_analysis)
        
        # Display positions
        for position in positions:
            self.print_position(position)
        
        # Display footer with wisdom
        print(f"\n{YELLOW}{'═' * 80}")
        print(f"{BOLD}RASTA TRADING WISDOM:{RESET} {BOLD}{self.display_market_wisdom()}{RESET}")
        print(f"{YELLOW}{'═' * 80}{RESET}")
        
        # Display refresh indicator
        print(f"\n{CYAN}Refreshing data... {LOADING_FRAMES[self.frame_counter % len(LOADING_FRAMES)]}{RESET}") 