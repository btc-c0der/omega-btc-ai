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
BitGet Matrix Position Display

A cyberpunk-themed terminal visualization of BitGet positions
with a Matrix-style animation. This is a demonstration tool
that simulates position data for visualization purposes.

Created for the Omega Bot Farm - a quantum transcendence experience.
"""

import os
import sys
import time
import random
import math
import json
import curses
import asyncio
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import colorama for cross-platform color support
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    print("Warning: colorama not installed. Colors will be limited.")
    
    # Define dummy color constants
    class DummyColors:
        def __getattr__(self, name):
            return ""
    
    Fore = DummyColors()
    Back = DummyColors()
    Style = DummyColors()

# Define color constants
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN
MAGENTA = Fore.MAGENTA
WHITE = Fore.WHITE
BLUE = Fore.BLUE
RESET = Style.RESET_ALL
BOLD = Style.BRIGHT

# Constants
PHI = 1.618033988749895  # Golden Ratio - Divine Proportion
INVERSE_PHI = 0.618033988749895  # Inverse Golden Ratio
SCHUMANN_BASE = 7.83  # Earth's base frequency (Hz)
BTC_SYMBOLS = ["₿", "⚡", "🔐", "🔗", "⚛️", "🌐", "🛡️"]
MATRIX_CHARS = "01Ψλφψ∞∑∫√∇∂ₐₑ₊₌₍ᵢₒₓₔₕ"
CYBERPUNK_MESSAGES = [
    "QUANTUM SECURE",
    "MATRIX POSITIONS",
    "DIVINE FIBONACCI",
    "SCHUMANN RESONANCE",
    "TRANSCENDING TIME",
    "BTC IS FREEDOM",
    "OMEGA BOT FARM",
    "CCXT DIRECT CONNECTED",
    "MATRIX HARMONIZED"
]

# Mock position data for demonstration
MOCK_POSITIONS = [
    {
        "symbol": "BTC/USDT:USDT",
        "side": "long",
        "contracts": 0.015,
        "entryPrice": 63420.5,
        "markPrice": 64850.3,
        "notional": 972.75,
        "leverage": 20,
        "unrealizedPnl": 21.45,
        "liquidationPrice": 60245.8,
        "marginMode": "isolated",
        "timestamp": int(time.time() * 1000),
        "percentage": 2.25
    },
    {
        "symbol": "ETH/USDT:USDT",
        "side": "short",
        "contracts": 0.12,
        "entryPrice": 3320.15,
        "markPrice": 3290.45,
        "notional": 394.85,
        "leverage": 10,
        "unrealizedPnl": 3.56,
        "liquidationPrice": 3652.30,
        "marginMode": "cross",
        "timestamp": int(time.time() * 1000),
        "percentage": 0.90
    },
    {
        "symbol": "SOL/USDT:USDT",
        "side": "long",
        "contracts": 1.5,
        "entryPrice": 143.25,
        "markPrice": 140.10,
        "notional": 210.15,
        "leverage": 5,
        "unrealizedPnl": -4.73,
        "liquidationPrice": 115.60,
        "marginMode": "isolated",
        "timestamp": int(time.time() * 1000),
        "percentage": -2.20
    }
]

# Mock account data
MOCK_ACCOUNT = {
    "balance": 1234.56,
    "equity": 1255.84,
    "total_position_value": 1577.75,
    "total_pnl": 20.28,
    "long_exposure": 1182.90,
    "short_exposure": 394.85,
    "long_short_ratio": 2.99,
    "exposure_to_equity_ratio": 1.26,
    "harmony_score": 0.83
}

class MatrixRain:
    """Class for drawing Matrix-style rain in the background."""
    
    def __init__(self, stdscr):
        """Initialize the matrix rain."""
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.drops = []
        self.initialize_drops()
        self.setup_colors()
        
    def setup_colors(self):
        """Set up color pairs for display."""
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
        
    def initialize_drops(self):
        """Initialize the raindrops."""
        for i in range(self.width):
            if random.random() < 0.1:  # 10% chance for initial drops
                self.drops.append({
                    'x': i,
                    'y': random.randint(-20, 0),
                    'length': random.randint(3, 15),
                    'speed': random.random() * 0.5 + 0.2,
                    'chars': self.generate_chars(random.randint(3, 15))
                })
                
    def generate_chars(self, length):
        """Generate characters for a drop."""
        return [random.choice(MATRIX_CHARS) for _ in range(length)]
                
    def update(self):
        """Update raindrop positions."""
        # Add new drops
        if random.random() < 0.05:  # 5% chance for new drop each frame
            self.drops.append({
                'x': random.randint(0, self.width - 1),
                'y': 0,
                'length': random.randint(3, 15),
                'speed': random.random() * 0.5 + 0.2,
                'chars': self.generate_chars(random.randint(3, 15))
            })
            
        # Update existing drops
        new_drops = []
        for drop in self.drops:
            drop['y'] += drop['speed']
            
            # Keep if still visible
            if drop['y'] - drop['length'] < self.height:
                new_drops.append(drop)
                
        self.drops = new_drops
        
    def draw(self):
        """Draw the matrix rain effect."""
        for drop in self.drops:
            x = drop['x']
            y_start = int(drop['y'] - drop['length'])
            y_end = int(drop['y'])
            
            for i, y in enumerate(range(y_start, y_end)):
                if 0 <= y < self.height and 0 <= x < self.width:
                    char_idx = drop['length'] - 1 - i
                    if char_idx >= 0 and char_idx < len(drop['chars']):
                        char = drop['chars'][char_idx]
                        
                        # Leading character is brighter
                        if i == drop['length'] - 1:
                            color = curses.color_pair(6)  # White for leading
                        else:
                            color = curses.color_pair(1)  # Green for trailing
                            
                        try:
                            self.stdscr.addch(y, x, ord(char), color)
                        except:
                            pass  # Ignore bottom-right corner error

class BitGetPositionDisplay:
    """Display BitGet positions with Matrix-style cyberpunk visuals."""
    
    def __init__(self, stdscr, positions=None, account=None):
        """Initialize the display."""
        self.stdscr = stdscr
        self.positions = positions or MOCK_POSITIONS
        self.account = account or MOCK_ACCOUNT
        self.height, self.width = stdscr.getmaxyx()
        self.matrix_rain = MatrixRain(stdscr)
        self.current_msg_idx = 0
        self.message_timer = 0
        
    def calculate_fibonacci_levels(self, entry_price, side="long"):
        """Calculate Fibonacci retracement levels."""
        fib_levels = []
        fib_ratios = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 4.236]
        
        # For demonstration, create some price range
        price_range = entry_price * 0.1  # 10% range
        
        if side.lower() == "long":
            base_price = entry_price - price_range
            top_price = entry_price + price_range * INVERSE_PHI
        else:
            base_price = entry_price + price_range
            top_price = entry_price - price_range * INVERSE_PHI
            
        price_diff = abs(top_price - base_price)
        
        for ratio in fib_ratios:
            if side.lower() == "long":
                price = base_price + (price_diff * ratio)
            else:
                price = base_price - (price_diff * ratio)
                
            fib_levels.append((ratio, price))
            
        return fib_levels
    
    def get_harmonic_strength(self, price, entry_price):
        """Calculate quantum harmonic alignment strength (0.0-1.0) based on golden ratio."""
        diff_ratio = abs(price - entry_price) / entry_price
        harmonic_score = (1 - (diff_ratio % INVERSE_PHI)) ** 2
        return min(1.0, max(0.0, harmonic_score))
    
    def create_progress_bar(self, value, max_value, width=20):
        """Create an ASCII progress bar."""
        filled_width = int(value / max_value * width)
        bar = '▓' * filled_width + '░' * (width - filled_width)
        return bar
    
    def draw_position(self, position, y_pos):
        """Draw a single position with cyberpunk styling."""
        # Extract position data
        symbol = position.get('symbol', 'UNKNOWN').split('/')[0]
        side = position.get('side', 'UNKNOWN').upper()
        contracts = float(position.get('contracts', 0))
        entry_price = float(position.get('entryPrice', 0))
        mark_price = float(position.get('markPrice', 0))
        unrealized_pnl = float(position.get('unrealizedPnl', 0))
        leverage = int(position.get('leverage', 1))
        liquidation_price = float(position.get('liquidationPrice', 0))
        
        # Calculate price difference percentage
        price_diff_pct = ((mark_price - entry_price) / entry_price) * 100
        if side == "SHORT":
            price_diff_pct = -price_diff_pct
            
        # Get colors based on side and PnL
        side_color = curses.color_pair(1) if side == "LONG" else curses.color_pair(4)  # Green or Red
        pnl_color = curses.color_pair(1) if unrealized_pnl > 0 else curses.color_pair(4)  # Green or Red
        
        # Draw position header
        header = f"┌──── {symbol} {side} @ {leverage}x ────"
        header += "─" * (self.width - len(header) - 1) + "┐"
        self.stdscr.addstr(y_pos, 0, header)
        
        # Position details
        self.stdscr.addstr(y_pos + 1, 2, f"Size: {contracts} contracts")
        self.stdscr.addstr(y_pos + 1, 30, f"Entry: ${entry_price:.2f}")
        self.stdscr.addstr(y_pos + 1, 55, f"Mark: ${mark_price:.2f}")
        
        # Price movement with color
        price_move_str = f"${abs(mark_price - entry_price):.2f} ({abs(price_diff_pct):.2f}%)"
        move_color = curses.color_pair(1) if price_diff_pct > 0 else curses.color_pair(4)
        direction = "▲" if price_diff_pct > 0 else "▼"
        self.stdscr.addstr(y_pos + 2, 2, f"Price Movement: ")
        self.stdscr.addstr(y_pos + 2, 18, f"{direction} {price_move_str}", move_color)
        
        # PnL
        pnl_str = f"${unrealized_pnl:.2f}"
        self.stdscr.addstr(y_pos + 2, 45, f"PnL: ")
        self.stdscr.addstr(y_pos + 2, 51, pnl_str, pnl_color)
        
        # Liquidation price
        liq_distance = abs(mark_price - liquidation_price) / mark_price * 100
        self.stdscr.addstr(y_pos + 3, 2, f"Liquidation: ${liquidation_price:.2f} ({liq_distance:.2f}% away)")
        
        # Quantum harmonic strength
        harmonic = self.get_harmonic_strength(mark_price, entry_price)
        harmonic_bar = self.create_progress_bar(harmonic, 1.0, 20)
        self.stdscr.addstr(y_pos + 4, 2, f"Quantum Harmonic: ")
        self.stdscr.addstr(y_pos + 4, 19, harmonic_bar)
        self.stdscr.addstr(y_pos + 4, 41, f" {harmonic:.2f} φ", curses.color_pair(5))
        
        # Draw bottom border
        self.stdscr.addstr(y_pos + 5, 0, "└" + "─" * (self.width - 2) + "┘")
        
        # Return the height used
        return 7  # Total height of this position block
    
    def draw_account_summary(self, y_pos):
        """Draw account summary with cyberpunk styling."""
        # Header
        header = "┌──── ACCOUNT MATRIX ────"
        header += "─" * (self.width - len(header) - 1) + "┐"
        self.stdscr.addstr(y_pos, 0, header)
        
        # Account balance and equity
        balance = self.account.get('balance', 0)
        equity = self.account.get('equity', 0)
        total_pnl = self.account.get('total_pnl', 0)
        
        self.stdscr.addstr(y_pos + 1, 2, f"Balance: ${balance:.2f}")
        self.stdscr.addstr(y_pos + 1, 25, f"Equity: ${equity:.2f}")
        
        pnl_color = curses.color_pair(1) if total_pnl >= 0 else curses.color_pair(4)
        self.stdscr.addstr(y_pos + 1, 50, f"Total PnL: ")
        self.stdscr.addstr(y_pos + 1, 61, f"${total_pnl:.2f}", pnl_color)
        
        # Exposure metrics
        long_exposure = self.account.get('long_exposure', 0)
        short_exposure = self.account.get('short_exposure', 0)
        ratio = self.account.get('long_short_ratio', 0)
        
        self.stdscr.addstr(y_pos + 2, 2, f"Long: ${long_exposure:.2f}")
        self.stdscr.addstr(y_pos + 2, 25, f"Short: ${short_exposure:.2f}")
        self.stdscr.addstr(y_pos + 2, 50, f"L/S Ratio: {ratio:.2f}")
        
        # Harmony score with visual bar
        harmony = self.account.get('harmony_score', 0)
        harmony_bar = self.create_progress_bar(harmony, 1.0, 30)
        self.stdscr.addstr(y_pos + 3, 2, f"Quantum Harmony: ")
        self.stdscr.addstr(y_pos + 3, 19, harmony_bar)
        
        # Schumann resonance alignment 
        schumann_align = (harmony * SCHUMANN_BASE) / PHI
        self.stdscr.addstr(y_pos + 4, 2, f"Schumann Resonance: {schumann_align:.2f} Hz", curses.color_pair(5))
        
        # Draw bottom border
        self.stdscr.addstr(y_pos + 5, 0, "└" + "─" * (self.width - 2) + "┘")
        
        return 7  # Total height used
    
    def draw_cyberpunk_message(self):
        """Draw a randomly cycling cyberpunk message."""
        self.message_timer += 1
        if self.message_timer >= 100:  # Change message every 100 frames
            self.message_timer = 0
            self.current_msg_idx = (self.current_msg_idx + 1) % len(CYBERPUNK_MESSAGES)
            
        message = CYBERPUNK_MESSAGES[self.current_msg_idx]
        x_pos = (self.width - len(message)) // 2
        self.stdscr.addstr(0, x_pos, message, curses.color_pair(5) | curses.A_BOLD)
    
    def draw_timestamp(self):
        """Draw the current timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stdscr.addstr(self.height - 1, 2, f"MATRIX TIME: {timestamp}", curses.color_pair(3))
    
    def draw_status_bar(self):
        """Draw a status bar at the bottom."""
        status = "CCXT DIRECT | CONNECTED | QUANTUM SECURE | PRESS 'Q' TO EXIT"
        x_pos = (self.width - len(status)) // 2
        self.stdscr.addstr(self.height - 1, x_pos, status, curses.color_pair(2) | curses.A_BOLD)
    
    def draw_frame(self):
        """Draw a complete frame of the display."""
        # Draw matrix rain in the background (dimmed)
        self.matrix_rain.update()
        self.matrix_rain.draw()
        
        # Draw cyberpunk message at the top
        self.draw_cyberpunk_message()
        
        # Draw positions, starting from y position 2
        y_position = 2
        for position in self.positions:
            height_used = self.draw_position(position, y_position)
            y_position += height_used
            
        # Draw account summary
        self.draw_account_summary(y_position)
        
        # Draw status bar
        self.draw_status_bar()
    
    def run(self):
        """Run the display loop."""
        curses.curs_set(0)  # Hide cursor
        
        # Set up non-blocking input
        self.stdscr.nodelay(True)
        
        try:
            while True:
                # Clear screen for next frame
                self.stdscr.clear()
                
                # Draw frame
                self.draw_frame()
                
                # Refresh display
                self.stdscr.refresh()
                
                # Check for key press
                key = self.stdscr.getch()
                if key == ord('q') or key == ord('Q'):
                    break
                    
                # Control frame rate
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            pass

def main(stdscr):
    """Main function for curses application."""
    # Initialize color pairs
    curses.start_color()
    curses.use_default_colors()
    
    # Create and run the display
    display = BitGetPositionDisplay(stdscr)
    display.run()

def print_ascii_header():
    """Print an ASCII art header for terminal display."""
    header = r"""
    ██████╗ ████████╗ ██████╗     ███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗
    ██╔══██╗╚══██╔══╝██╔════╝     ████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝
    ██████╔╝   ██║   ██║  ███╗    ██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝ 
    ██╔══██╗   ██║   ██║   ██║    ██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗ 
    ██████╔╝   ██║   ╚██████╔╝    ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗
    ╚═════╝    ╚═╝    ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
    
                      ₿ITGET POSITION DISPLAY - MATRIX EDITION
                           [ OMEGA BOT FARM TRIBUTE ]
    """
    
    if COLORAMA_AVAILABLE:
        lines = header.split('\n')
        for i, line in enumerate(lines):
            if i < 8:  # ASCII art lines
                color = [Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.RED, Fore.YELLOW][i % 6]
                print(color + line)
            else:
                print(Fore.CYAN + line)
        print(Style.RESET_ALL)
    else:
        print(header)

async def mock_positions_update():
    """Simulate real-time position updates by making small changes to the mock data."""
    global MOCK_POSITIONS
    
    while True:
        # Randomly update positions with small price changes
        for position in MOCK_POSITIONS:
            # Simulate market moving 0.1% in either direction
            price_change_pct = (random.random() - 0.5) * 0.002  # -0.1% to +0.1%
            current_price = position["markPrice"]
            new_price = current_price * (1 + price_change_pct)
            position["markPrice"] = new_price
            
            # Update PnL based on price change
            entry_price = position["entryPrice"]
            contracts = position["contracts"]
            if position["side"].lower() == "long":
                position["unrealizedPnl"] = (new_price - entry_price) * contracts
            else:
                position["unrealizedPnl"] = (entry_price - new_price) * contracts
                
            # Update percentage
            if position["side"].lower() == "long":
                position["percentage"] = ((new_price - entry_price) / entry_price) * 100
            else:
                position["percentage"] = ((entry_price - new_price) / entry_price) * 100
                
        # Update account data based on position changes
        MOCK_ACCOUNT["total_pnl"] = sum(p["unrealizedPnl"] for p in MOCK_POSITIONS)
        MOCK_ACCOUNT["equity"] = MOCK_ACCOUNT["balance"] + MOCK_ACCOUNT["total_pnl"]
        
        # Sleep to simulate real-time updates
        await asyncio.sleep(0.5)

def run_cli_fallback():
    """Run a simplified CLI version for terminals that don't support curses."""
    print_ascii_header()
    print(f"{Fore.YELLOW}╒══════════════════════════════════════════════════════════════╕{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.CYAN}BITGET MATRIX POSITIONS SUMMARY - OMEGA BOT FARM{Style.RESET_ALL}      {Fore.YELLOW}│{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}╘══════════════════════════════════════════════════════════════╛{Style.RESET_ALL}")
    
    print(f"\n{Fore.MAGENTA}═══ ACCOUNT MATRIX ═══{Style.RESET_ALL}")
    print(f"Balance: ${MOCK_ACCOUNT['balance']:.2f}")
    print(f"Equity: ${MOCK_ACCOUNT['equity']:.2f}")
    
    pnl_color = Fore.GREEN if MOCK_ACCOUNT['total_pnl'] >= 0 else Fore.RED
    print(f"Total PnL: {pnl_color}${MOCK_ACCOUNT['total_pnl']:.2f}{Style.RESET_ALL}")
    
    print(f"Long Exposure: ${MOCK_ACCOUNT['long_exposure']:.2f}")
    print(f"Short Exposure: ${MOCK_ACCOUNT['short_exposure']:.2f}")
    print(f"Quantum Harmony Score: {MOCK_ACCOUNT['harmony_score']:.2f}")
    
    print(f"\n{Fore.MAGENTA}═══ POSITIONS ═══{Style.RESET_ALL}")
    for position in MOCK_POSITIONS:
        symbol = position['symbol'].split('/')[0]
        side = position['side'].upper()
        side_color = Fore.GREEN if side == "LONG" else Fore.RED
        
        print(f"\n{side_color}{symbol} {side} @ {position['leverage']}x{Style.RESET_ALL}")
        print(f"Size: {position['contracts']} contracts")
        print(f"Entry: ${position['entryPrice']:.2f} | Mark: ${position['markPrice']:.2f}")
        
        price_diff_pct = position['percentage']
        pct_color = Fore.GREEN if price_diff_pct > 0 else Fore.RED
        print(f"Price Movement: {pct_color}{'+' if price_diff_pct > 0 else ''}{price_diff_pct:.2f}%{Style.RESET_ALL}")
        
        pnl_color = Fore.GREEN if position['unrealizedPnl'] > 0 else Fore.RED
        print(f"PnL: {pnl_color}${position['unrealizedPnl']:.2f}{Style.RESET_ALL}")
        print(f"Liquidation: ${position['liquidationPrice']:.2f}")
        
    print(f"\n{Fore.CYAN}Press Ctrl+C to exit{Style.RESET_ALL}")
    
    try:
        while True:
            time.sleep(1)  # Just keep running until interrupted
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Exiting Matrix. Goodbye!{Style.RESET_ALL}")

if __name__ == "__main__":
    # Try to run the curses interface
    try:
        # Start the background task to update mock data
        if sys.platform != "win32":  # asyncio.create_task might not work well on Windows
            try:
                update_task = asyncio.create_task(mock_positions_update())
                curses.wrapper(main)
                update_task.cancel()  # Cancel the task when curses exits
            except asyncio.CancelledError:
                pass
        else:
            curses.wrapper(main)
    except Exception as e:
        # Fall back to CLI if curses fails
        print(f"Error running curses interface: {e}")
        print("Falling back to simplified CLI display...")
        run_cli_fallback() 