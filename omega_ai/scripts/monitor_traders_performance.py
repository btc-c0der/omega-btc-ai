#!/usr/bin/env python3
"""
OMEGA BTC AI - Live Traders Performance Monitor
===============================================

This script provides a CLI interface to monitor the real-time performance
of the BitGet traders implemented in the system.

Author: OMEGA BTC AI Team
"""

import os
import sys
import time
import asyncio
import argparse
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import curses
from curses import wrapper
import signal
import random

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
from omega_ai.trading.exchanges.bitget_trader import BitGetTrader
from omega_ai.trading.profiles import (
    StrategicTrader,
    AggressiveTrader,
    NewbieTrader,
    ScalperTrader
)
from omega_ai.alerts.telegram_market_report import send_telegram_alert

# Terminal colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# Define Curses color pairs
COLOR_NORMAL = 1
COLOR_GREEN = 2
COLOR_RED = 3
COLOR_YELLOW = 4
COLOR_BLUE = 5
COLOR_CYAN = 6
COLOR_MAGENTA = 7

# Reggae Patois messages
PATOIS_MESSAGES = [
    "JAH bless di trading, mon! We watchin' di markets.",
    "BOOM! Di market movin' like a rockin' riddim.",
    "Irie trades, mon! We keepin' it steady.",
    "One love to all traders, we stayin' positive on di charts.",
    "Hold tight! Market going up like smoke to di sky.",
    "Feel di vibes of di market, it speaks to us!",
    "Di traders dem doing work, respect every time!",
    "We jammin' with di numbers, tradah mon!",
    "Rasta never sleeps when di market a move.",
    "Price dipping? No problem. Every little ting gonna be alright.",
    "We staring at di charts till we eyes dem red!",
    "Big up to all di traders making profits today!",
    "We no want no bear market, only bull vibrations.",
    "Mi tell you, patience is di key to di profits.",
    "HODL strong! Crypto is di future currency.",
]

class TraderMonitor:
    """CLI-based monitor for real-time trader performance."""
    
    def __init__(self, 
                 use_testnet: bool = False,
                 symbol: str = "BTCUSDT",
                 api_key: str = "",
                 secret_key: str = "",
                 passphrase: str = "",
                 refresh_rate: float = 1.0):
        """
        Initialize the trader monitor.
        
        Args:
            use_testnet: Whether to use testnet (default: False)
            symbol: Trading symbol (default: BTCUSDT)
            api_key: BitGet API key
            secret_key: BitGet secret key
            passphrase: BitGet API passphrase
            refresh_rate: Data refresh rate in seconds (default: 1.0)
        """
        self.use_testnet = use_testnet
        self.symbol = symbol
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.refresh_rate = refresh_rate
        self.traders_data = {}
        self.market_data = {}
        self.running = False
        self.stdscr = None
        self.use_mock_data = False
        self.api_success = False
        self.mock_price = 61500.0  # Starting BTC price for mock data
        self.mock_start_time = datetime.now(timezone.utc)
        self.message_idx = 0
        self.message_change_time = time.time()
        
        # Look for API credentials in environment variables if not provided
        if not self.api_key:
            self.api_key = os.environ.get("BITGET_TESTNET_API_KEY" if use_testnet else "BITGET_API_KEY", "")
        if not self.secret_key:
            self.secret_key = os.environ.get("BITGET_TESTNET_SECRET_KEY" if use_testnet else "BITGET_SECRET_KEY", "")
        if not self.passphrase:
            self.passphrase = os.environ.get("BITGET_TESTNET_PASSPHRASE" if use_testnet else "BITGET_PASSPHRASE", "")
        
        # Create live traders instance
        self.live_traders = BitGetLiveTraders(
            use_testnet=self.use_testnet,
            symbol=self.symbol,
            api_key=self.api_key,
            secret_key=self.secret_key,
            passphrase=self.passphrase
        )
        
    async def initialize(self):
        """Initialize the monitor and traders."""
        print(f"{CYAN}Initializing trader performance monitor... JAH guide us!{RESET}")
        
        # Notify via Telegram that this is only a monitoring bot
        monitor_alert_msg = (
            f"🔍 MONITOR BOT STARTED (NOT TRADING)\n"
            f"Symbol: {self.symbol}\n"
            f"Mode: {'TESTNET' if self.use_testnet else 'MAINNET'}\n"
            f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            f"Message: Monitor bot just watching, no worry mon! No trades will be made."
        )
        await send_telegram_alert(monitor_alert_msg)
        
        # Override the send_telegram_alert function in BitGetLiveTraders to prevent duplicate alerts
        original_initialize = self.live_traders._initialize_traders
        
        async def silent_initialize():
            """Modified initialization that doesn't send alerts"""
            profiles = {
                "strategic": StrategicTrader,
                "aggressive": AggressiveTrader,
                "newbie": NewbieTrader,
                "scalper": ScalperTrader
            }
            
            # API version to use - v1 is more stable and has different endpoints
            api_version = "v1"
            print(f"{YELLOW}Initializing traders with API version {api_version} - just for monitoring, no trading, mon!{RESET}")
            
            for profile_name, profile_class in profiles.items():
                try:
                    trader = BitGetTrader(
                        profile_type=profile_name,
                        api_key=self.live_traders.api_key,
                        secret_key=self.live_traders.secret_key,
                        passphrase=self.live_traders.passphrase,
                        use_testnet=self.live_traders.use_testnet,
                        initial_capital=self.live_traders.initial_capital,
                        api_client=self.live_traders.api_client,
                        api_version=api_version
                    )
                    
                    trader.symbol = self.live_traders.symbol
                    self.live_traders.traders[profile_name] = trader
                    print(f"{GREEN}Initialized {profile_name} trader mon for monitoring only! Respect!{RESET}")
                    
                except Exception as e:
                    print(f"{RED}Failed to initialize {profile_name} trader: {str(e)} - Babylon system!{RESET}")
        
        # Replace the initialize method with our silent version
        self.live_traders._initialize_traders = silent_initialize
        
        # Now initialize
        await self.live_traders.initialize()
        print(f"{GREEN}Trader performance monitor initialized - Ready to watch di market, mon!{RESET}")
        
    def _get_patois_message(self):
        """Get a reggae patois message, changing it every 10 seconds"""
        current_time = time.time()
        if current_time - self.message_change_time > 10:
            self.message_idx = (self.message_idx + 1) % len(PATOIS_MESSAGES)
            self.message_change_time = current_time
            
        return PATOIS_MESSAGES[self.message_idx]
        
    async def start(self, stdscr):
        """Start the monitor in curses mode."""
        self.stdscr = stdscr
        self.running = True
        
        # Set up curses
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(COLOR_NORMAL, curses.COLOR_WHITE, -1)
        curses.init_pair(COLOR_GREEN, curses.COLOR_GREEN, -1)
        curses.init_pair(COLOR_RED, curses.COLOR_RED, -1)
        curses.init_pair(COLOR_YELLOW, curses.COLOR_YELLOW, -1)
        curses.init_pair(COLOR_BLUE, curses.COLOR_BLUE, -1)
        curses.init_pair(COLOR_CYAN, curses.COLOR_CYAN, -1)
        curses.init_pair(COLOR_MAGENTA, curses.COLOR_MAGENTA, -1)
        
        stdscr.clear()
        stdscr.nodelay(True)
        stdscr.timeout(100)  # 100ms timeout for getch()
        
        try:
            while self.running:
                # Check for keyboard input
                key = stdscr.getch()
                if key == ord('q'):
                    self.running = False
                    break
                
                # Update data
                await self._update_data()
                
                # Refresh the display
                self._draw_interface(stdscr)
                
                # Wait before next update
                await asyncio.sleep(self.refresh_rate)
        except KeyboardInterrupt:
            self.running = False
        finally:
            await self.stop()
         
    async def stop(self):
        """Stop the monitor."""
        self.running = False
        print(f"{YELLOW}Stopping trader performance monitor... One love!{RESET}")
        
        # Send closing message
        stop_msg = (
            f"🛑 MONITOR BOT SHUTDOWN (NO TRADING AFFECTED)\n"
            f"Symbol: {self.symbol}\n"
            f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            f"Message: Monitor bot going to sleep now, but traders still running. Respect!"
        )
        await send_telegram_alert(stop_msg)
        
    async def _update_data(self):
        """Update trader and market data."""
        # First try to get real data
        if not self.use_mock_data:
            try:
                # Update market data
                if not self.live_traders.traders:
                    print(f"{YELLOW}No traders initialized yet, waiting... Patience, mon!{RESET}")
                    return
                    
                for profile_name, trader in self.live_traders.traders.items():
                    try:
                        # Get market ticker
                        ticker = trader.get_market_ticker(trader.symbol)
                        if ticker and 'last' in ticker:
                            current_price = float(ticker['last'])
                            
                            # Update market data
                            self.market_data = {
                                "symbol": trader.symbol,
                                "price": current_price,
                                "timestamp": datetime.now(timezone.utc)
                            }
                            
                            # Update positions
                            try:
                                positions = trader.get_positions(trader.symbol)
                            except Exception as pos_error:
                                print(f"{RED}Error getting positions for {profile_name}: {str(pos_error)} - Babylon confusion!{RESET}")
                                positions = []
                            
                            # Get total PnL 
                            try:
                                total_pnl = trader.get_total_pnl()
                            except Exception as pnl_error:
                                print(f"{RED}Error getting PnL for {profile_name}: {str(pnl_error)} - Downpression!{RESET}")
                                total_pnl = 0
                                
                            # Get account balance
                            try:
                                balance = trader.get_account_balance()
                            except Exception as bal_error:
                                print(f"{RED}Error getting balance for {profile_name}: {str(bal_error)} - Where's di money gone?{RESET}")
                                balance = None
                            
                            # Update trader data
                            self.traders_data[profile_name] = {
                                "total_pnl": total_pnl,
                                "positions": positions if positions else [],
                                "balance": balance,
                                "trades_count": len(trader.trade_history) if hasattr(trader, 'trade_history') else 0,
                                "last_trade": trader.trade_history[-1] if hasattr(trader, 'trade_history') and trader.trade_history else None
                            }
                            
                            # If we got here, API is working
                            self.api_success = True
                            
                        else:
                            print(f"{YELLOW}Warning: Invalid ticker data for {trader.symbol} ({profile_name} trader) - Di market confused, mon!{RESET}")
                            if ticker:
                                print(f"{YELLOW}Ticker: {ticker}{RESET}")
                            
                    except Exception as trader_error:
                        print(f"{RED}Error updating {profile_name} trader: {str(trader_error)} - Babylon system!{RESET}")
                        continue
                        
                    # We only need to get market data once, from the first working trader
                    break
                    
            except Exception as e:
                print(f"{RED}Error updating data: {str(e)} - Wi need some digital healing!{RESET}")
                if not self.api_success:
                    print(f"{YELLOW}Switching to mock data mode after API failure - No worry, every little ting gonna be alright!{RESET}")
                    self.use_mock_data = True
        
        # If API failed or mock data is enabled, use simulated data
        if self.use_mock_data:
            await self._update_mock_data()
            
    async def _update_mock_data(self):
        """Update with simulated mock data when API is unavailable."""
        # Generate a random price movement (+/- 0.5%)
        price_change = random.uniform(-0.005, 0.005)
        self.mock_price = self.mock_price * (1 + price_change)
        
        # Update market data with mock price
        self.market_data = {
            "symbol": self.symbol,
            "price": self.mock_price,
            "timestamp": datetime.now(timezone.utc)
        }
        
        # Create mock traders if they don't exist
        profiles = ["strategic", "aggressive", "newbie", "scalper"]
        
        for profile in profiles:
            if profile not in self.traders_data:
                # Initialize mock data for this profile
                initial_pnl = random.uniform(-2.0, 5.0)
                
                # Random number of positions (0-2)
                position_count = random.randint(0, 2)
                positions = []
                
                for i in range(position_count):
                    # Random position data
                    side = "LONG" if random.random() > 0.5 else "SHORT"
                    size = random.uniform(0.001, 0.01)
                    entry_price = self.mock_price * (1 + random.uniform(-0.02, 0.02))
                    pos_pnl = random.uniform(-1.0, 2.0)
                    
                    positions.append({
                        "side": side,
                        "size": size,
                        "entry_price": entry_price,
                        "unrealized_pnl": pos_pnl,
                        "status": "OPEN"
                    })
                
                # Create mock trader data
                self.traders_data[profile] = {
                    "total_pnl": initial_pnl,
                    "positions": positions,
                    "balance": {"available": 24.0 + initial_pnl},
                    "trades_count": random.randint(3, 15),
                    "last_trade": None
                }
            else:
                # Update existing mock data
                data = self.traders_data[profile]
                
                # Update PnL with small random changes
                pnl_change = random.uniform(-0.2, 0.3)
                data["total_pnl"] += pnl_change
                
                # Update balance
                if isinstance(data["balance"], dict):
                    data["balance"]["available"] = 24.0 + data["total_pnl"]
                else:
                    data["balance"] = {"available": 24.0 + data["total_pnl"]}
                
                # Random chance to add/remove positions
                if random.random() < 0.05:  # 5% chance to change positions
                    if data["positions"] and random.random() < 0.5:
                        # Close a position
                        data["positions"].pop()
                    else:
                        # Add a position
                        side = "LONG" if random.random() > 0.5 else "SHORT"
                        size = random.uniform(0.001, 0.01)
                        entry_price = self.mock_price * (1 + random.uniform(-0.02, 0.02))
                        pos_pnl = random.uniform(-1.0, 2.0)
                        
                        data["positions"].append({
                            "side": side,
                            "size": size,
                            "entry_price": entry_price,
                            "unrealized_pnl": pos_pnl,
                            "status": "OPEN"
                        })
                
                # Update existing positions
                for pos in data["positions"]:
                    # Update PnL for the position
                    pnl_change = random.uniform(-0.1, 0.15)
                    pos["unrealized_pnl"] += pnl_change
                    
                    # Small chance to flip trend
                    if random.random() < 0.1:
                        pnl_change *= -1.5
                        
                    # Update with new values
                    self.traders_data[profile] = data
                        
    def _draw_interface(self, stdscr):
        """Draw the monitoring interface."""
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        # Draw header
        header = f" 🔍 OMEGA BTC AI - MONITOR BOT (NO TRADING) 🔍 "
        stdscr.addstr(0, (max_x - len(header)) // 2, header, curses.color_pair(COLOR_CYAN) | curses.A_BOLD)
        
        # Draw market data
        market_str = f" Symbol: {self.market_data.get('symbol', 'N/A')} | Price: {self.market_data.get('price', 0):.2f} | Time: {self.market_data.get('timestamp', datetime.now()).strftime('%H:%M:%S')} "
        stdscr.addstr(1, (max_x - len(market_str)) // 2, market_str, curses.color_pair(COLOR_YELLOW))
        
        # Draw mode info and mock data warning if necessary
        if self.use_mock_data:
            mode_str = f" {'TESTNET' if self.use_testnet else 'MAINNET'} MODE - MOCK DATA (API UNAVAILABLE) "
            stdscr.addstr(2, (max_x - len(mode_str)) // 2, mode_str, curses.color_pair(COLOR_MAGENTA))
        else:
            mode_str = f" {'TESTNET' if self.use_testnet else 'MAINNET'} MODE "
            stdscr.addstr(2, (max_x - len(mode_str)) // 2, mode_str, 
                          curses.color_pair(COLOR_MAGENTA) if self.use_testnet else curses.color_pair(COLOR_GREEN))
                          
        # Draw reggae message
        patois_msg = f" {self._get_patois_message()} "
        stdscr.addstr(3, (max_x - len(patois_msg)) // 2, patois_msg, curses.color_pair(COLOR_GREEN))
        
        # Draw trader information
        row = 5
        for profile_name, data in self.traders_data.items():
            if row >= max_y - 3:
                break
                
            # Draw profile header
            profile_header = f" {profile_name.upper()} TRADER MON "
            stdscr.addstr(row, 2, profile_header, curses.color_pair(COLOR_BLUE) | curses.A_BOLD)
            row += 1
            
            # Draw PnL
            pnl = data.get('total_pnl', 0)
            pnl_color = COLOR_GREEN if pnl >= 0 else COLOR_RED
            pnl_desc = "IRIE PROFITS!" if pnl >= 0 else "BABYLON LOSSES!"
            stdscr.addstr(row, 4, f"PnL: {pnl:.2f} USDT - {pnl_desc}", curses.color_pair(pnl_color))
            row += 1
            
            # Draw balance - Fix to handle None safely
            balance_data = data.get('balance') or {}
            balance = balance_data.get('available', 0) if isinstance(balance_data, dict) else 0
            stdscr.addstr(row, 4, f"Balance: {balance:.2f} USDT - DI MONEY POT!", curses.color_pair(COLOR_NORMAL))
            row += 1
            
            # Draw positions
            positions = data.get('positions', [])
            position_count = len(positions)
            position_txt = f"HODLIN' {position_count} POSITIONS" if position_count else "NO POSITIONS, JUST CHILLIN'"
            stdscr.addstr(row, 4, f"Positions: {position_count} - {position_txt}", curses.color_pair(COLOR_NORMAL))
            row += 1
            
            # Draw position details if available
            for i, pos in enumerate(positions[:2]):  # Show max 2 positions
                if row >= max_y - 3:
                    break
                    
                side = pos.get('side', 'UNKNOWN')
                size = pos.get('size', 0)
                entry_price = pos.get('entry_price', 0)
                pnl = pos.get('unrealized_pnl', 0)
                
                side_color = COLOR_GREEN if side == 'LONG' else COLOR_RED
                pnl_color = COLOR_GREEN if pnl >= 0 else COLOR_RED
                
                side_txt = f"{side} - TO DI MOON!" if side == 'LONG' else f"{side} - GOING DOWN!"
                pos_str = f"  #{i+1}: {side} {size:.4f} @ {entry_price:.2f} (PnL: {pnl:.2f})"
                stdscr.addstr(row, 4, pos_str, curses.color_pair(COLOR_NORMAL))
                # Highlight side and PnL with appropriate colors
                pos_idx = pos_str.find(side)
                stdscr.addstr(row, 4 + pos_idx, side, curses.color_pair(side_color))
                pnl_idx = pos_str.find("PnL: ")
                stdscr.addstr(row, 4 + pnl_idx + 5, f"{pnl:.2f}", curses.color_pair(pnl_color))
                row += 1
            
            row += 1  # Add space between traders
            
        # Draw footer
        footer = " Press 'q' to quit - ONE LOVE! "
        stdscr.addstr(max_y - 1, (max_x - len(footer)) // 2, footer, curses.color_pair(COLOR_YELLOW))
        
        # Refresh the screen
        stdscr.refresh()

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='OMEGA BTC AI - Trader Performance Monitor')
    parser.add_argument('--symbol', type=str, default='BTCUSDT',
                      help='Trading symbol (default: BTCUSDT)')
    parser.add_argument('--testnet', action='store_true',
                      help='Use testnet (default: False)')
    parser.add_argument('--mainnet', action='store_true',
                      help='Use mainnet (default: True)')
    parser.add_argument('--api-key', type=str, default='',
                      help='BitGet API key')
    parser.add_argument('--secret-key', type=str, default='',
                      help='BitGet secret key')
    parser.add_argument('--passphrase', type=str, default='',
                      help='BitGet API passphrase')
    parser.add_argument('--refresh', type=float, default=1.0,
                      help='Refresh rate in seconds (default: 1.0)')
    parser.add_argument('--mock', action='store_true',
                      help='Use mock data instead of API (for testing)')
    
    return parser.parse_args()

async def main():
    """Main entry point for the trader monitor."""
    args = parse_args()
    
    # Determine if we should use testnet
    use_testnet = args.testnet or not args.mainnet
    
    # Initialize the monitor
    monitor = TraderMonitor(
        use_testnet=use_testnet,
        symbol=args.symbol,
        api_key=args.api_key,
        secret_key=args.secret_key,
        passphrase=args.passphrase,
        refresh_rate=args.refresh
    )
    
    # Use mock data if requested
    if args.mock:
        monitor.use_mock_data = True
    
    try:
        # Initialize traders if not using mock data
        if not monitor.use_mock_data:
            await monitor.initialize()
        else:
            print(f"{YELLOW}Using mock data mode - No API connection needed, mon! Just vibes!{RESET}")
        
        # Start the monitor (curses interface)
        await wrapper(monitor.start)
    except KeyboardInterrupt:
        print(f"{YELLOW}Received shutdown signal - Respect, mon!{RESET}")
    finally:
        await monitor.stop()

if __name__ == "__main__":
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, lambda sig, frame: None)
    
    print(f"{GREEN}Starting OMEGA BTC AI Monitor Bot - JAH bless di trading! One love!{RESET}")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Exiting... Respect and blessings, mon!{RESET}") 