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
OMEGA BTC AI - Fibonacci Trader Statistics
=========================================

A script to analyze and display statistics for the Fibonacci-based trading strategy.
Shows performance metrics, win rates, and other key statistics.

Author: OMEGA BTC AI Team
"""

import os
import sys
import json
import asyncio
import argparse
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
from tabulate import tabulate
from colorama import Fore, Style, init
from dotenv import load_dotenv

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
from omega_ai.trading.exchanges.bitget_trader import BitGetTrader
from omega_ai.trading.profiles import StrategicTrader

# Initialize colorama
init(autoreset=True)

# Load environment variables from .env file
try:
    # Try to load from project root .env
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
    env_path = os.path.join(project_root, '.env')
    
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"{Fore.GREEN}Loaded environment from {env_path}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}No .env file found at {env_path}, using system environment variables{Style.RESET_ALL}")
except Exception as e:
    print(f"{Fore.RED}Error loading .env file: {str(e)}{Style.RESET_ALL}")

class FibonacciTraderStats:
    """Analyzes and displays statistics for the Fibonacci trading strategy."""
    
    def __init__(self, 
                 symbol: str = "BTCUSDT",
                 days: int = 30):
        """
        Initialize the Fibonacci trader statistics analyzer.
        
        Args:
            symbol: Trading symbol (default: BTCUSDT)
            days: Number of days to analyze (default: 30)
        """
        self.symbol = symbol
        self.days = days
        self.debug = False
        
        # Get API credentials from environment variables (mainnet only)
        self.api_key = os.environ.get("BITGET_API_KEY", "")
        self.secret_key = os.environ.get("BITGET_SECRET_KEY", "")
        self.passphrase = os.environ.get("BITGET_PASSPHRASE", "")
        
        # Verify API credentials
        if not all([self.api_key, self.secret_key, self.passphrase]):
            print(f"{Fore.RED}Error: API credentials missing. Please set environment variables.{Style.RESET_ALL}")
            print(f"Required variables: BITGET_API_KEY, BITGET_SECRET_KEY, BITGET_PASSPHRASE")
            sys.exit(1)
        
        # Initialize strategic trader
        self.trader = BitGetTrader(
            profile_type="strategic",
            api_key=self.api_key,
            secret_key=self.secret_key,
            passphrase=self.passphrase,
            use_testnet=False,  # Always use mainnet
            api_version="v1"
        )
        
        # Get sub-account name from environment
        self.sub_account = os.environ.get("STRATEGIC_SUB_ACCOUNT_NAME", "")
        if self.sub_account:
            print(f"{Fore.GREEN}Using sub-account: {self.sub_account}{Style.RESET_ALL}")
    
    async def get_trade_history(self) -> List[Dict[str, Any]]:
        """Get trade history for the specified period."""
        trades = []
        try:
            # Calculate time range
            end_time = datetime.now(timezone.utc)
            start_time = end_time - timedelta(days=self.days)
            
            # Get trades from BitGet
            history = self.trader.get_historical_positions(
                symbol=self.symbol,
                start_time=int(start_time.timestamp() * 1000),
                end_time=int(end_time.timestamp() * 1000)
            )
            
            if history and isinstance(history, list):
                trades = history
                print(f"{Fore.GREEN}Retrieved {len(trades)} trades from the last {self.days} days{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}No trade history found for the specified period{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}Error getting trade history: {str(e)}{Style.RESET_ALL}")
            
        return trades
    
    def calculate_statistics(self, trades: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate trading statistics from trade history."""
        stats = {
            'total_trades': len(trades),
            'winning_trades': 0,
            'losing_trades': 0,
            'total_profit': 0.0,
            'max_profit': 0.0,
            'max_loss': 0.0,
            'avg_profit': 0.0,
            'profit_factor': 0.0,
            'win_rate': 0.0,
            'avg_hold_time': 0.0,
            'best_day': {'date': None, 'profit': 0.0},
            'worst_day': {'date': None, 'profit': 0.0},
            'daily_profits': {},
            'fibonacci_levels': {
                '0': {'trades': 0, 'wins': 0, 'profit': 0.0},
                '0.236': {'trades': 0, 'wins': 0, 'profit': 0.0},
                '0.382': {'trades': 0, 'wins': 0, 'profit': 0.0},
                '0.5': {'trades': 0, 'wins': 0, 'profit': 0.0},
                '0.618': {'trades': 0, 'wins': 0, 'profit': 0.0},
                '0.786': {'trades': 0, 'wins': 0, 'profit': 0.0},
                '1': {'trades': 0, 'wins': 0, 'profit': 0.0},
                '1.618': {'trades': 0, 'wins': 0, 'profit': 0.0},
                '2.618': {'trades': 0, 'wins': 0, 'profit': 0.0},
                '4.236': {'trades': 0, 'wins': 0, 'profit': 0.0}
            }
        }
        
        if not trades:
            return stats
            
        total_profit = 0.0
        total_loss = 0.0
        total_hold_time = 0.0
        
        for trade in trades:
            # Calculate profit/loss
            profit = float(trade.get('realizedPnl', 0))
            total_profit += profit
            
            # Update win/loss counts
            if profit > 0:
                stats['winning_trades'] += 1
                if profit > stats['max_profit']:
                    stats['max_profit'] = profit
            else:
                stats['losing_trades'] += 1
                if profit < stats['max_loss']:
                    stats['max_loss'] = profit
            
            # Calculate hold time
            open_time = datetime.fromtimestamp(int(trade.get('openTime', 0)) / 1000, timezone.utc)
            close_time = datetime.fromtimestamp(int(trade.get('closeTime', 0)) / 1000, timezone.utc)
            hold_time = (close_time - open_time).total_seconds() / 3600  # Convert to hours
            total_hold_time += hold_time
            
            # Update daily profits
            trade_date = close_time.date().isoformat()
            if trade_date not in stats['daily_profits']:
                stats['daily_profits'][trade_date] = 0.0
            stats['daily_profits'][trade_date] += profit
            
            # Update Fibonacci level statistics if available
            fib_level = trade.get('fibonacciLevel', 'unknown')
            if fib_level in stats['fibonacci_levels']:
                stats['fibonacci_levels'][fib_level]['trades'] += 1
                stats['fibonacci_levels'][fib_level]['profit'] += profit
                if profit > 0:
                    stats['fibonacci_levels'][fib_level]['wins'] += 1
        
        # Calculate final statistics
        stats['total_profit'] = total_profit
        stats['avg_profit'] = total_profit / len(trades) if trades else 0
        stats['win_rate'] = (stats['winning_trades'] / len(trades)) * 100 if trades else 0
        stats['avg_hold_time'] = total_hold_time / len(trades) if trades else 0
        
        # Calculate profit factor
        total_loss = abs(sum(profit for trade in trades if (profit := float(trade.get('realizedPnl', 0))) < 0))
        stats['profit_factor'] = total_profit / total_loss if total_loss > 0 else float('inf')
        
        # Find best and worst days
        if stats['daily_profits']:
            best_day = max(stats['daily_profits'].items(), key=lambda x: x[1])
            worst_day = min(stats['daily_profits'].items(), key=lambda x: x[1])
            stats['best_day'] = {'date': best_day[0], 'profit': best_day[1]}
            stats['worst_day'] = {'date': worst_day[0], 'profit': worst_day[1]}
        
        return stats
    
    def print_statistics(self, stats: Dict[str, Any]):
        """Print trading statistics in a formatted way."""
        print(f"\n{Fore.CYAN}===== FIBONACCI TRADER STATISTICS ====={Style.RESET_ALL}")
        print(f"{Fore.CYAN}Period: Last {self.days} days{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Symbol: {self.symbol}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Mode: MAINNET{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}{Style.RESET_ALL}")
        
        # Overall Performance
        print(f"\n{Fore.MAGENTA}=== OVERALL PERFORMANCE ==={Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Total Trades: {Fore.CYAN}{stats['total_trades']}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Winning Trades: {Fore.GREEN}{stats['winning_trades']}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Losing Trades: {Fore.RED}{stats['losing_trades']}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Win Rate: {Fore.CYAN}{stats['win_rate']:.2f}%{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Total Profit: {Fore.GREEN if stats['total_profit'] >= 0 else Fore.RED}{stats['total_profit']:.2f} USDT{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Average Profit: {Fore.GREEN if stats['avg_profit'] >= 0 else Fore.RED}{stats['avg_profit']:.2f} USDT{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Profit Factor: {Fore.CYAN}{stats['profit_factor']:.2f}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Average Hold Time: {Fore.CYAN}{stats['avg_hold_time']:.2f} hours{Style.RESET_ALL}")
        
        # Best/Worst Days
        print(f"\n{Fore.MAGENTA}=== BEST/WORST DAYS ==={Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Best Day: {Fore.GREEN}{stats['best_day']['date']} ({stats['best_day']['profit']:.2f} USDT){Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Worst Day: {Fore.RED}{stats['worst_day']['date']} ({stats['worst_day']['profit']:.2f} USDT){Style.RESET_ALL}")
        
        # Fibonacci Level Performance
        print(f"\n{Fore.MAGENTA}=== FIBONACCI LEVEL PERFORMANCE ==={Style.RESET_ALL}")
        fib_data = []
        for level, data in stats['fibonacci_levels'].items():
            if data['trades'] > 0:
                win_rate = (data['wins'] / data['trades']) * 100
                fib_data.append([
                    level,
                    data['trades'],
                    data['wins'],
                    f"{win_rate:.1f}%",
                    f"{data['profit']:.2f} USDT"
                ])
        
        print(tabulate(
            fib_data,
            headers=["Level", "Trades", "Wins", "Win Rate", "Profit"],
            tablefmt="grid"
        ))
        
        # Daily Performance
        print(f"\n{Fore.MAGENTA}=== DAILY PERFORMANCE ==={Style.RESET_ALL}")
        daily_data = []
        for date, profit in sorted(stats['daily_profits'].items()):
            daily_data.append([
                date,
                f"{profit:.2f} USDT"
            ])
        
        print(tabulate(
            daily_data,
            headers=["Date", "Profit"],
            tablefmt="grid"
        ))
        
        print(f"\n{Fore.CYAN}================================={Style.RESET_ALL}")

async def main():
    """Main entry point for the Fibonacci trader statistics."""
    parser = argparse.ArgumentParser(description='OMEGA BTC AI - Fibonacci Trader Statistics')
    parser.add_argument('--symbol', type=str, default='BTCUSDT',
                      help='Trading symbol (default: BTCUSDT)')
    parser.add_argument('--days', type=int, default=30,
                      help='Number of days to analyze (default: 30)')
    parser.add_argument('--debug', action='store_true',
                      help='Enable debug mode (default: False)')
    
    args = parser.parse_args()
    
    # Initialize statistics analyzer (mainnet only)
    analyzer = FibonacciTraderStats(
        symbol=args.symbol,
        days=args.days
    )
    
    # Get trade history
    trades = await analyzer.get_trade_history()
    
    # Calculate and print statistics
    stats = analyzer.calculate_statistics(trades)
    analyzer.print_statistics(stats)

if __name__ == "__main__":
    print(f"{Fore.GREEN}OMEGA BTC AI - Fibonacci Trader Statistics{Style.RESET_ALL}")
    print(f"{Fore.GREEN}=========================================={Style.RESET_ALL}")
    print(f"{Fore.GREEN}Running on MAINNET only{Style.RESET_ALL}")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}") 