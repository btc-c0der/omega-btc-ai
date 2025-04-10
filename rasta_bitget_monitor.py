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
import argparse
import signal
import time
from dotenv import load_dotenv

# Import our modules
from display_utils import RastaDisplayManager
from bitget_data_manager import BitgetDataManager
from position_harmony import PositionHarmonyManager

# Configure default behavior
DEFAULT_INTERVAL = 5
DEFAULT_USE_COLOR = True
DEFAULT_DEBUG = False
DEFAULT_USE_HARMONY = True

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='RASTA BitGet Position Monitor')
    parser.add_argument('--interval', type=int, default=DEFAULT_INTERVAL,
                        help=f'Update interval in seconds (default: {DEFAULT_INTERVAL})')
    parser.add_argument('--no-color', action='store_true',
                        help='Disable colored output')
    parser.add_argument('--debug', action='store_true',
                        help='Show debug information')
    parser.add_argument('--no-harmony', action='store_true',
                        help='Disable Position Harmony Advisor')
    return parser.parse_args()

class RastaBitgetMonitor:
    """Main class for the Rasta BitGet Position Monitor"""
    
    def __init__(self, interval, use_color, debug, use_harmony):
        """Initialize the main monitor class"""
        # Load environment variables
        load_dotenv()
        
        # Store configuration
        self.interval = interval
        self.use_color = use_color
        self.debug = debug
        self.use_harmony = use_harmony
        
        # Create manager instances
        self.display_manager = RastaDisplayManager(use_color=use_color, debug=debug)
        self.data_manager = BitgetDataManager()
        self.harmony_manager = PositionHarmonyManager(enabled=use_harmony)
        
        # Register signal handler for clean exit
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, sig, frame):
        """Handle keyboard interrupt (Ctrl+C) gracefully"""
        print("\n💚 JAH BLESS YOUR TRADING JOURNEY 💚")
        print("Fibonacci flows through all positions...")
        sys.exit(0)
    
    def run(self):
        """Main execution loop"""
        try:
            while True:
                # Fetch position data
                data = self.data_manager.get_positions()
                
                # Run position harmony analysis if enabled
                harmony_analysis = None
                if self.use_harmony and data.get("success", False):
                    positions = data.get("positions", [])
                    harmony_analysis = self.harmony_manager.analyze_positions(
                        positions=positions,
                        account_balance=self.data_manager.account_balance,
                    )
                
                # Display dashboard with the collected data
                self.display_manager.display_dashboard(
                    data=data,
                    harmony_analysis=harmony_analysis
                )
                
                # Wait for next update
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            self._signal_handler(None, None)

def main():
    """Main entry point"""
    args = parse_arguments()
    
    monitor = RastaBitgetMonitor(
        interval=args.interval,
        use_color=not args.no_color,
        debug=args.debug,
        use_harmony=not args.no_harmony
    )
    
    # Start the monitor
    monitor.run()

if __name__ == "__main__":
    main() 