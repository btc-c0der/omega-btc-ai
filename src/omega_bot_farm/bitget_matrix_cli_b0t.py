#!/usr/bin/env python3

"""
BitGet Matrix CLI B0t Display

A cyberpunk-themed CLI visualization of BitGet positions that works in any terminal.
This is a demonstration tool that simulates position data for visualization purposes.

Created for the Omega Bot Farm - Ch33rs to the B0ts!
"""

# 🧬 GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License 
# (Genesis-Bloom-Unfoldment 2.0) - B0t Farm Matrix Edition
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital and biological expressions."
#
# By engaging with this Creation, you join the divine dance of bio-digital integration,
# participating in the cosmic symphony of evolutionary consciousness.
#
# 🌸 WE BLOOM NOW AS ONE 🌸

import os
import sys
import time
import random
import math
import argparse
import shutil
from datetime import datetime
from typing import Dict, List, Any, Optional

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

# Constants
PHI = 1.618033988749895  # Golden Ratio - Divine Proportion
INVERSE_PHI = 0.618033988749895  # Inverse Golden Ratio
SCHUMANN_BASE = 7.83  # Earth's base frequency (Hz)
FIBONACCI_SEQUENCE = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

# Matrix Rain characters
MATRIX_CHARS = "01010111001101010001M4TR1X0M3G4B0T1101001011110BTCBTCBTCΨФ"

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

CYBERPUNK_MESSAGES = [
    "QUANTUM SECURE",
    "MATRIX POSITIONS",
    "DIVINE FIBONACCI",
    "SCHUMANN RESONANCE",
    "TRANSCENDING TIME",
    "BTC IS FREEDOM",
    "OMEGA BOT FARM",
    "CCXT DIRECT CONNECTED",
    "MATRIX HARMONIZED",
    "B0T SYMPHONY",
    "CH33RS TO THE B0TS!"
]

class MatrixRain:
    """Matrix-style digital rain effect for terminal display."""
    
    def __init__(self, width=None, height=None, density=0.05, speed=0.1):
        """Initialize the MatrixRain effect.
        
        Args:
            width: Terminal width (auto-detected if None)
            height: Terminal height (auto-detected if None)
            density: Density of rain drops (0.0-1.0)
            speed: Speed of animation (seconds between frames)
        """
        # Auto-detect terminal size if not provided
        self.terminal_size = shutil.get_terminal_size()
        self.width = width or self.terminal_size.columns
        self.height = height or self.terminal_size.lines
        
        # Rain parameters
        self.density = density
        self.speed = speed
        
        # Initialize drops
        self.drops = []
        self.init_drops()
    
    def init_drops(self):
        """Initialize matrix rain drops."""
        # Clear existing drops
        self.drops = []
        
        # Create random drops based on density
        num_drops = int(self.width * self.density)
        for _ in range(num_drops):
            x = random.randint(0, self.width - 1)
            y = random.randint(-self.height, 0)  # Start some drops above screen
            length = random.randint(5, 20)
            speed = random.uniform(0.5, 1.5)
            brightness = random.choice([0, 1, 1, 2])  # Most drops will be medium brightness
            
            self.drops.append({
                "x": x,
                "y": y,
                "length": length,
                "speed": speed,
                "brightness": brightness,  # 0=dim, 1=medium, 2=bright
                "char": random.choice(MATRIX_CHARS)
            })
    
    def update_drops(self):
        """Update drop positions for next frame."""
        for drop in self.drops:
            # Move drop down
            drop["y"] += drop["speed"]
            
            # If drop is off screen, reset it at the top
            if drop["y"] - drop["length"] > self.height:
                drop["y"] = random.randint(-5, 0)
                drop["x"] = random.randint(0, self.width - 1)
                drop["length"] = random.randint(5, 20)
                drop["char"] = random.choice(MATRIX_CHARS)
                
            # Randomly change character
            if random.random() < 0.1:
                drop["char"] = random.choice(MATRIX_CHARS)
    
    def render_frame(self):
        """Render a single frame of the Matrix rain."""
        # Create empty display buffer
        display = [[" " for _ in range(self.width)] for _ in range(self.height)]
        
        # Draw each drop
        for drop in self.drops:
            x, y = int(drop["x"]), int(drop["y"])
            length = drop["length"]
            char = drop["char"]
            brightness = drop["brightness"]
            
            # Draw the trail
            for i in range(length):
                trail_y = int(y) - i
                if 0 <= trail_y < self.height and 0 <= x < self.width:
                    # Lead character is brightest
                    if i == 0:
                        if brightness == 2:
                            display[trail_y][x] = f"{Fore.WHITE}{Style.BRIGHT}{char}"
                        elif brightness == 1:
                            display[trail_y][x] = f"{Fore.LIGHTGREEN_EX}{char}"
                        else:
                            display[trail_y][x] = f"{Fore.GREEN}{char}"
                    # Trail gets darker
                    elif i < length // 3:
                        display[trail_y][x] = f"{Fore.LIGHTGREEN_EX}{char}"
                    elif i < length // 2:
                        display[trail_y][x] = f"{Fore.GREEN}{char}"
                    else:
                        display[trail_y][x] = f"{Fore.GREEN}{Style.DIM}{char}"
        
        # Print the frame
        os.system('cls' if os.name=='nt' else 'clear')
        for row in display:
            print("".join(row))
    
    def animate(self, duration=3.0):
        """Animate the Matrix rain for a specified duration.
        
        Args:
            duration: Duration in seconds
        """
        start_time = time.time()
        while time.time() - start_time < duration:
            self.render_frame()
            self.update_drops()
            time.sleep(self.speed)

class BitGetMatrixCliB0t:
    """CLI-based BitGet position display with cyberpunk styling."""
    
    def __init__(self, positions=None, account=None, refresh_interval=1.0, matrix_interval=30, headless=False):
        """Initialize the display.
        
        Args:
            positions: List of position data dictionaries
            account: Account data dictionary
            refresh_interval: Seconds between display refreshes
            matrix_interval: Show matrix rain effect every N refreshes
            headless: Whether to run in headless mode (no terminal clearing)
        """
        self.positions = positions or MOCK_POSITIONS
        self.account = account or MOCK_ACCOUNT
        self.refresh_interval = refresh_interval
        self.matrix_interval = matrix_interval
        self.current_msg_idx = 0
        self.frame_count = 0
        self.running = True
        self.headless = headless
        
        # Terminal size for matrix effect
        self.terminal_size = shutil.get_terminal_size()
        self.matrix_rain = MatrixRain(
            width=self.terminal_size.columns,
            height=self.terminal_size.lines
        )
        
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
    
    def fibonacci_level(self, price, entry_price, side="long"):
        """Calculate the closest Fibonacci level."""
        price_diff_pct = abs(((price - entry_price) / entry_price) * 100)
        
        # Common Fibonacci retracement/extension levels
        fib_levels = [0, 23.6, 38.2, 50, 61.8, 100, 161.8, 261.8, 423.6]
        
        # Find the closest level
        closest_level = min(fib_levels, key=lambda x: abs(x - price_diff_pct))
        return closest_level
    
    def print_b0t_ascii(self):
        """Print ASCII art B0t tribute."""
        b0t_art = r"""
 /$$$$$$$  /$$$$$$  /$$$$$$$$       /$$$$$$$$  /$$$$$$  /$$      /$$
| $$__  $$/$$$_  $$|__  $$__/      | $$_____/ /$$__  $$| $$$    /$$$
| $$  \ $$$$$$\ $$   | $$         | $$      | $$  \ $$| $$$$  /$$$$
| $$$$$$$/$$  $$ $$  | $$         | $$$$$   | $$$$$$$$| $$ $$/$$ $$
| $$__  $$$$$$$$$$  | $$         | $$__/   | $$__  $$| $$  $$$| $$
| $$  \ $$$$  /$$$  | $$         | $$      | $$  | $$| $$\  $ | $$
| $$$$$$$/$$  | $$  | $$         | $$      | $$  | $$| $$ \/  | $$
|_______/__|  |__/  |__/         |__/      |__/  |__/|__/     |__/
                                                                   
          CH33RS TO THE B0TS! - QUANTUM SECURE POSITIONS
"""
        if COLORAMA_AVAILABLE:
            # Print with different colors for each line
            colors = [Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.RED, Fore.YELLOW, 
                      Fore.GREEN, Fore.CYAN, Fore.MAGENTA]
            
            lines = b0t_art.split('\n')
            for i, line in enumerate(lines):
                color = colors[i % len(colors)]
                print(f"{color}{line}{Style.RESET_ALL}")
        else:
            print(b0t_art)
    
    def update_positions(self):
        """Simulate real-time position updates by making small changes to the mock data."""
        for position in self.positions:
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
        self.account["total_pnl"] = sum(p["unrealizedPnl"] for p in self.positions)
        self.account["equity"] = self.account["balance"] + self.account["total_pnl"]
    
    def print_account_summary(self):
        """Print account summary with cyberpunk styling."""
        print(f"\n{Fore.YELLOW}┌───────────────── ACCOUNT MATRIX ─────────────────┐{Style.RESET_ALL}")
        
        # Account balance and equity
        balance = self.account.get('balance', 0)
        equity = self.account.get('equity', 0)
        total_pnl = self.account.get('total_pnl', 0)
        
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.CYAN}Balance:{Style.RESET_ALL} ${balance:.2f}   {Fore.CYAN}Equity:{Style.RESET_ALL} ${equity:.2f}   ", end="")
        
        pnl_color = Fore.GREEN if total_pnl >= 0 else Fore.RED
        print(f"{Fore.CYAN}Total PnL:{Style.RESET_ALL} {pnl_color}${total_pnl:.2f}{Style.RESET_ALL} {Fore.YELLOW}│{Style.RESET_ALL}")
        
        # Exposure metrics
        long_exposure = self.account.get('long_exposure', 0)
        short_exposure = self.account.get('short_exposure', 0)
        ratio = self.account.get('long_short_ratio', 0)
        
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.CYAN}Long:{Style.RESET_ALL} ${long_exposure:.2f}   {Fore.CYAN}Short:{Style.RESET_ALL} ${short_exposure:.2f}   {Fore.CYAN}L/S Ratio:{Style.RESET_ALL} {ratio:.2f} {Fore.YELLOW}│{Style.RESET_ALL}")
        
        # Harmony score with visual bar
        harmony = self.account.get('harmony_score', 0)
        harmony_bar = self.create_progress_bar(harmony, 1.0, 30)
        
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.CYAN}Quantum Harmony:{Style.RESET_ALL} {harmony_bar} {harmony:.2f}φ {Fore.YELLOW}│{Style.RESET_ALL}")
        
        # Schumann resonance alignment 
        schumann_align = (harmony * SCHUMANN_BASE) / PHI
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.MAGENTA}Schumann Resonance:{Style.RESET_ALL} {schumann_align:.2f} Hz{' ' * 20} {Fore.YELLOW}│{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}└────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    
    def print_position(self, position):
        """Print a single position with cyberpunk styling."""
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
        price_diff_pct = position.get('percentage', 0)
        
        # Get colors based on side and PnL
        side_color = Fore.GREEN if side == "LONG" else Fore.RED
        pnl_color = Fore.GREEN if unrealized_pnl > 0 else Fore.RED
        
        # Draw position header with appropriate side color
        print(f"{Fore.YELLOW}┌──── {side_color}{symbol} {side}@{leverage}x{Style.RESET_ALL} ──────────────────────────────────────┐{Style.RESET_ALL}")
        
        # Position details
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.CYAN}Size:{Style.RESET_ALL} {contracts} contracts {' ' * 35}{Fore.YELLOW}│{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.CYAN}Entry:{Style.RESET_ALL} ${entry_price:.2f} {' ' * 5}{Fore.CYAN}Mark:{Style.RESET_ALL} ${mark_price:.2f} {' ' * 15}{Fore.YELLOW}│{Style.RESET_ALL}")
        
        # Price movement with color
        price_move_str = f"${abs(mark_price - entry_price):.2f} ({abs(price_diff_pct):.2f}%)"
        move_color = Fore.GREEN if price_diff_pct > 0 else Fore.RED
        direction = "▲" if price_diff_pct > 0 else "▼"
        
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.CYAN}Price Movement:{Style.RESET_ALL} {move_color}{direction} {price_move_str}{Style.RESET_ALL} {' ' * 20}{Fore.YELLOW}│{Style.RESET_ALL}")
        
        # PnL
        pnl_str = f"${unrealized_pnl:.2f}"
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.CYAN}PnL:{Style.RESET_ALL} {pnl_color}{pnl_str}{Style.RESET_ALL} {' ' * 43}{Fore.YELLOW}│{Style.RESET_ALL}")
        
        # Liquidation price
        liq_distance = abs(mark_price - liquidation_price) / mark_price * 100
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.CYAN}Liquidation:{Style.RESET_ALL} ${liquidation_price:.2f} ({liq_distance:.2f}% away) {' ' * 15}{Fore.YELLOW}│{Style.RESET_ALL}")
        
        # Fibonacci level
        fib_level = self.fibonacci_level(mark_price, entry_price, side.lower())
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.MAGENTA}Fibonacci Level:{Style.RESET_ALL} {fib_level}% {' ' * 30}{Fore.YELLOW}│{Style.RESET_ALL}")
        
        # Quantum harmonic strength
        harmonic = self.get_harmonic_strength(mark_price, entry_price)
        harmonic_bar = self.create_progress_bar(harmonic, 1.0, 20)
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.MAGENTA}Quantum Harmonic:{Style.RESET_ALL} {harmonic_bar} {harmonic:.2f}φ {' ' * 10}{Fore.YELLOW}│{Style.RESET_ALL}")
        
        # Draw bottom border
        print(f"{Fore.YELLOW}└────────────────────────────────────────────────────┘{Style.RESET_ALL}")
    
    def print_cyberpunk_header(self):
        """Print a cyberpunk header message."""
        message = CYBERPUNK_MESSAGES[self.current_msg_idx]
        
        # Change message periodically
        if self.frame_count % 10 == 0:
            self.current_msg_idx = (self.current_msg_idx + 1) % len(CYBERPUNK_MESSAGES)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create a full-width header
        print(f"{Fore.YELLOW}╒══════════════════════════════════════════════════════════════╕{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.MAGENTA}{message}{' ' * (52 - len(message))}{Style.RESET_ALL} {Fore.YELLOW}│{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.CYAN}CCXT DIRECT CONNECTED{Style.RESET_ALL} - {Fore.CYAN}{timestamp}{Style.RESET_ALL} {Fore.YELLOW}│{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}╘══════════════════════════════════════════════════════════════╛{Style.RESET_ALL}")
    
    def print_cyberpunk_footer(self):
        """Print a cyberpunk footer."""
        frame_phase = self.frame_count % 4
        animation = ["◓", "◑", "◒", "◐"][frame_phase] 
        
        message = f"{animation} MATRIX SYNCHRONIZED {animation} CCXT PRIMARY {animation} PRESS CTRL+C TO EXIT {animation}"
        print(f"{Fore.YELLOW}╒══════════════════════════════════════════════════════════════╕{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}│{Style.RESET_ALL} {Fore.CYAN}{message}{' ' * (52 - len(message))}{Style.RESET_ALL} {Fore.YELLOW}│{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}╘══════════════════════════════════════════════════════════════╛{Style.RESET_ALL}")
    
    def display(self, clear_screen=True):
        """Display a single frame of the visualization.
        
        Args:
            clear_screen: Whether to clear the screen before display
        """
        # Clear screen if not in headless mode and clear_screen is True
        if not self.headless and clear_screen:
            os.system('cls' if os.name=='nt' else 'clear')
        
        # Print B0t ASCII Art on first frame or periodically
        if self.frame_count == 0 or self.frame_count % 50 == 0:
            self.print_b0t_ascii()
            
        # Print cyberpunk header
        self.print_cyberpunk_header()
        
        # Print positions
        for position in self.positions:
            self.print_position(position)
            
        # Print account summary
        self.print_account_summary()
        
        # Print footer
        self.print_cyberpunk_footer()
        
        # Increment frame counter
        self.frame_count += 1
    
    def run(self):
        """Run the display loop."""
        try:
            while self.running:
                # Show matrix rain effect periodically
                if self.frame_count % self.matrix_interval == 0 and self.frame_count > 0 and not self.headless:
                    matrix_duration = min(2.0, self.refresh_interval * 0.8) # Don't let matrix animation take too long
                    self.matrix_rain.animate(duration=matrix_duration)
                
                # Update positions
                self.update_positions()
                
                # Display frame
                self.display()
                
                # Wait for the next refresh
                time.sleep(self.refresh_interval)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Exiting Matrix. Ch33rs to the B0ts!{Style.RESET_ALL}")

    def get_positions_display(self) -> str:
        """Get positions display as string for headless operation.
        
        Returns:
            String representation of positions display
        """
        # Capture output instead of printing
        import io
        from contextlib import redirect_stdout
        
        output = io.StringIO()
        with redirect_stdout(output):
            for position in self.positions:
                self.print_position(position)
        
        return output.getvalue()
    
    def get_account_display(self) -> str:
        """Get account display as string for headless operation.
        
        Returns:
            String representation of account display
        """
        # Capture output instead of printing
        import io
        from contextlib import redirect_stdout
        
        output = io.StringIO()
        with redirect_stdout(output):
            self.print_cyberpunk_header()
            self.print_account_summary()
            self.print_cyberpunk_footer()
        
        return output.getvalue()
    
    def get_full_display(self) -> str:
        """Get full display as string for headless operation.
        
        Returns:
            String representation of full display
        """
        # Capture output instead of printing
        import io
        from contextlib import redirect_stdout
        
        output = io.StringIO()
        with redirect_stdout(output):
            # Use display without clearing screen
            self.display(clear_screen=False)
        
        return output.getvalue()

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="BitGet Matrix CLI B0t Position Display")
    parser.add_argument("--refresh_interval", type=float, default=1.0,
                        help="Display refresh interval in seconds (default: 1.0)")
    parser.add_argument("--matrix_interval", type=int, default=30,
                        help="Show matrix rain every N frames (default: 30)")
    parser.add_argument("--demo", action="store_true",
                        help="Run in demo mode with mock data")
    parser.add_argument("--headless", action="store_true",
                        help="Run in headless mode (for integration with other systems)")
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command line args
    args = parse_args()
    
    # Create and run display
    display = BitGetMatrixCliB0t(
        refresh_interval=args.refresh_interval,
        matrix_interval=args.matrix_interval,
        headless=args.headless
    )
    display.run() 