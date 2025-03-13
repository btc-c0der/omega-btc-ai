#!/usr/bin/env python3

"""
Run BTC Futures Trading with Different Trader Profiles

This script simulates trading using the same market data but with different
trader psychological profiles to compare performance. It runs continuously
until manually interrupted.
"""

import os
import sys
import argparse
import time
import datetime
import redis
import json
import logging
from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass, field

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from omega_ai.trading.profiled_futures_trader import ProfiledFuturesTrader
from omega_ai.reporting.futures_reporter import FuturesReporter
from omega_ai.trading.btc_futures_trader import TradeHistory
from omega_ai.utils.redis_connection import RedisConnectionManager
from omega_ai.trading.session_manager import TradingSessionManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Redis connection manager with retry
try:
    redis_manager = RedisConnectionManager()
    # Test connection and data retrieval
    test_data = redis_manager.get("test_key")
    if (test_data is None):
        # Set test data if it doesn't exist
        redis_manager.set("test_key", "connection_test")
    logging.info("✅ Redis connection established")
except Exception as e:
    logging.error(f"❌ Failed to initialize Redis connection: {e}")
    sys.exit(1)

# ANSI escape codes for colors
BOLD = "\033[1m"
MAGENTA = "\033[35m"
RESET = "\033[0m"

def supports_color():
    """
    Returns True if the running system's terminal supports color,
    and False otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty

# If color is not supported, set color codes to empty strings
if not supports_color():
    BOLD = MAGENTA = RESET = ""

class RedisKeys:
    """Redis key constants to avoid typos and maintain consistency"""
    MOVEMENTS_PREFIX = "btc_movements_"
    START_TRADING = "omega:start_trading"
    LIVE_TRADER_DATA = "omega:live_trader_data"
    LIVE_BATTLE_STATE = "omega:live_battle_state"
    TEST_KEY = "test_key"

def store_trader_data_in_redis(traders: Dict, day_counter: int, 
                             session_counter: int, start_time: datetime.datetime, 
                             price_history: List[float]) -> None:
    """Store trader data in Redis for the dashboard."""
    try:
        trader_data = {}
        for profile, trader in traders.items():
            trader_data[profile] = {
                "name": getattr(trader.profile, 'name', f"{profile.capitalize()} Trader"),
                "capital": trader.initial_capital,
                "pnl": sum(position.unrealized_pnl for position in trader.positions) if hasattr(trader, 'positions') else 0,
                "win_rate": getattr(trader, 'win_rate', 0),
                "trades": getattr(trader, 'total_trades', 0),
                "winning_trades": getattr(trader, 'winning_trades', 0),
                "losing_trades": getattr(trader, 'losing_trades', 0),
                "emotional_state": trader.state.get("emotional_state", "neutral") if hasattr(trader, 'state') else "neutral",
                "confidence": trader.state.get("confidence", 0.5) if hasattr(trader, 'state') else 0.5,
                "risk_level": getattr(trader, 'risk_per_trade', 0.5),
                "positions": get_positions_data(trader),
                "trade_history": get_trade_history(trader),
                "achievements": []
            }
        
        redis_manager.set(RedisKeys.LIVE_TRADER_DATA, trader_data)
        
        battle_state = {
            "day": day_counter,
            "session": session_counter % 4 if session_counter % 4 != 0 else 4,
            "btc_price": getattr(list(traders.values())[0], 'current_price', 0),
            "btc_history": price_history[-100:] if price_history else [],
            "battle_active": True,
            "start_time": start_time.isoformat(),
            "timeline_events": []
        }
        redis_manager.set(RedisKeys.LIVE_BATTLE_STATE, battle_state)
        
        logging.info("Successfully updated Redis with trader data and battle state")
    except Exception as e:
        logging.error(f"An unexpected error occurred while updating Redis: {e}")

def get_positions_data(trader):
    """Extract positions data in the format expected by the dashboard."""
    positions = []
    if hasattr(trader, 'positions'):
        for pos in trader.positions:
            positions.append({
                "direction": pos.direction if hasattr(pos, 'direction') else "LONG",
                "entry_price": pos.entry_price if hasattr(pos, 'entry_price') else 0,
                "size": pos.size if hasattr(pos, 'size') else 0,
                "leverage": pos.leverage if hasattr(pos, 'leverage') else 1,
                "entry_time": pos.entry_time.isoformat() if hasattr(pos, 'entry_time') else datetime.datetime.now().isoformat(),
                "stop_loss": pos.stop_loss if hasattr(pos, 'stop_loss') else None,
                "take_profit": pos.take_profit[0]["price"] if hasattr(pos, 'take_profit') and pos.take_profit else None
            })
    return positions

def get_trade_history(trader):
    """Extract trade history in the format expected by the dashboard."""
    history = []
    if hasattr(trader, 'trade_history'):
        try:
            if isinstance(trader.trade_history, TradeHistory):
                trades = trader.trade_history.trades[:20]
            elif isinstance(trader.trade_history, list):
                trades = trader.trade_history[:20]
            else:
                logging.warning(f"Unexpected trade_history type: {type(trader.trade_history)}")
                return history
            
            for trade in trades:
                try:
                    trade_data = {
                        "direction": trade.direction,
                        "entry_price": trade.entry_price,
                        "exit_price": trade.exit_price,
                        "size": trade.size,
                        "leverage": trade.leverage,
                        "pnl": trade.realized_pnl,
                        "pnl_pct": (trade.realized_pnl / (trade.entry_price * trade.size)) * 100 if trade.entry_price and trade.size else 0,
                        "exit_reason": trade.exit_reason,
                        "entry_time": trade.entry_time.isoformat() if trade.entry_time else "",
                        "exit_time": trade.exit_time.isoformat() if trade.exit_time else ""
                    }
                    history.append(trade_data)
                except AttributeError as e:
                    logging.error(f"Error processing trade in history: {e}")
        except Exception as e:
            logging.error(f"Error accessing trade history: {e}")
    else:
        logging.warning(f"Trader {trader.profile_type} has no trade_history attribute")
    return history

def get_movements_data(timeframe: int) -> List[Dict]:
    """Get price movements data for a specific timeframe."""
    try:
        movements_key = f"{RedisKeys.MOVEMENTS_PREFIX}{timeframe}min"
        movements_data = redis_manager.get(movements_key)
        
        if movements_data:
            try:
                return json.loads(movements_data)
            except json.JSONDecodeError:
                logging.error(f"Invalid JSON data for timeframe {timeframe}min")
                return []
        else:
            logging.warning(f"No movements data found for {timeframe}min timeframe")
            return []
            
    except Exception as e:
        logging.error(f"Error fetching movements for {timeframe}min: {e}")
        return []

def analyze_fibonacci_levels(timeframe: int) -> Dict[str, Any]:
    """Analyze Fibonacci levels for a specific timeframe."""
    try:
        movements = get_movements_data(timeframe)
        
        if not movements:
            logging.info(f"Insufficient data for {timeframe}min")
            return {}
        
        # Calculate Fibonacci levels from movements
        prices = [m["price"] for m in movements if "price" in m]
        if not prices:
            return {}
            
        high, low = max(prices), min(prices)
        range_size = high - low
        
        # Calculate actual Fibonacci levels
        fib_236 = high - (range_size * 0.236)
        fib_382 = high - (range_size * 0.382)
        fib_500 = high - (range_size * 0.500)
        fib_618 = high - (range_size * 0.618)
        fib_786 = high - (range_size * 0.786)
        
        return {
            "timeframe": timeframe,
            "movements": len(movements),
            "levels": {
                "0.236": fib_236,
                "0.382": fib_382,
                "0.500": fib_500,
                "0.618": fib_618,
                "0.786": fib_786
            }
        }
        
    except Exception as e:
        logging.error(f"Error analyzing {timeframe}min timeframe: {e}")
        return {}

def run_fibonacci_analysis():
    """Run Fibonacci analysis across all timeframes."""
    timeframes = [1, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1440]
    
    print("\n════════════════════ FIBONACCI MULTI-TIMEFRAME ANALYSIS ════════════════════")
    
    for timeframe in timeframes:
        print(f"\nAnalyzing {timeframe}min timeframe:")
        movements = get_movements_data(timeframe)
        print(f"Retrieved {len(movements)} movements")
        
        analysis = analyze_fibonacci_levels(timeframe)
        if analysis:
            # Print analysis results
            for level, value in analysis["levels"].items():
                print(f"Fibonacci {level}: {value}")

@dataclass
class TraderState:
    day_counter: int = 1
    session_counter: int = 0
    price_history: List[float] = field(default_factory=list)
    start_time: datetime.datetime = field(default_factory=lambda: datetime.datetime.now())

def main():
    parser = argparse.ArgumentParser(description='Run BTC Futures Trading with Different Trader Profiles')
    parser.add_argument('--profiles', nargs='+', default=['strategic', 'aggressive', 'newbie', 'scalper'],
                      help='Trader profiles to simulate')
    parser.add_argument('--capital', type=float, default=10000.0, help='Initial capital')
    parser.add_argument('--log-dir', default='logs', help='Directory for logs')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--report-interval', type=int, default=4, 
                       help='Number of sessions between full performance reports')
    args = parser.parse_args()
    
    # Create log directory if it doesn't exist
    os.makedirs(args.log_dir, exist_ok=True)
    
    # Initialize reporter
    reporter = FuturesReporter(log_dir=args.log_dir, debug_mode=args.debug)
    
    # Initialize one trader per profile
    traders = {}
    for profile in args.profiles:
        trader = ProfiledFuturesTrader(
            profile_type=profile,
            initial_capital=args.capital
        )
        traders[profile] = trader
        reporter.register_trader(f"{profile.capitalize()}_Trader", profile, trader)
    
    # Run simulation with all profiles in parallel (infinite loop)
    try:
        print(f"Waiting for start signal...")
        
        while True:
            start_signal = redis_manager.get("omega:start_trading")
            if start_signal != "1":
                time.sleep(1)  # Wait for 1 second before checking again
                continue
            
            print(f"Start signal received. Beginning trading simulation with {len(traders)} trader profiles")
            print(f"Press Ctrl+C to stop the simulation")
            
            # Run Fibonacci analysis before starting trading
            run_fibonacci_analysis()
            
            # Track simulation metrics
            start_time = datetime.datetime.now()
            day_counter = 1
            session_counter = 0
            
            # Initialize price history
            price_history = []
            
            # Run while start signal is active
            while redis_manager.get("omega:start_trading") == "1":
                current_time = datetime.datetime.now()
                runtime = current_time - start_time
                
                print(f"\n{BOLD}Day {day_counter} | Runtime: {runtime}{RESET}")
                
                # Each day has multiple trading sessions
                for session in range(4):  # 4 sessions per day
                    session_counter += 1
                    print(f"  Trading session {(session_counter-1)%4+1}/4 | Total sessions: {session_counter}")
                    
                    # Each session has multiple price updates
                    for i in range(15):  # 15 price updates per session
                        # Check if we should stop
                        if redis_manager.get("omega:start_trading") != "1":
                            break
                        
                        # Get latest market data (shared across all trader profiles)
                        current_price = traders['strategic'].update_current_price()
                        price_history.append(current_price)
                        
                        # Each trader processes the same market conditions
                        for profile, trader in traders.items():
                            try:
                                trader.current_price = current_price
                                trader.manage_open_positions()
                                
                                if i % 3 == 0:
                                    should_open, reason, leverage = trader.should_open_position()
                                    if should_open and "LONG" in reason:
                                        trader.open_position("LONG", reason, leverage)
                                    elif should_open and "SHORT" in reason:
                                        trader.open_position("SHORT", reason, leverage)
                            except Exception as e:
                                logging.error(f"Error updating trader {profile}: {e}")
                        
                        store_trader_data_in_redis(
                            traders, 
                            day_counter,
                            session_counter,
                            start_time,
                            price_history
                        )
                        
                        time.sleep(2)
                    
                    if redis_manager.get("omega:start_trading") != "1":
                        break
                    
                    print("\n===== Trader Profile Performance =====")
                    for profile, trader in traders.items():
                        print(f"\n----- {profile.upper()} TRADER -----")
                        trader.print_position_status()
                    print("\n=====================================")
                    
                    if session_counter % args.report_interval == 0:
                        print(f"\n{MAGENTA}══════ DETAILED PERFORMANCE REPORT ══════{RESET}")
                        for profile, trader in traders.items():
                            print(f"\n{BOLD}{profile.upper()} TRADER PERFORMANCE SUMMARY{RESET}")
                            trader.print_performance_summary()
                        print(f"\n{MAGENTA}══════════════════════════════════════{RESET}")
                        
                        for trader in traders.values():
                            trader.save_state(f"trader_state_{trader.profile_type}.json")
                    
                    time.sleep(5)
                
                if redis_manager.get("omega:start_trading") != "1":
                    break
                
                day_counter += 1
                time.sleep(5)
                price_history = price_history[-1000:]
            
            print("\nStop signal received. Ending simulation.")
            
            print("\n===== FINAL PERFORMANCE COMPARISON =====")
            for profile, trader in traders.items():
                print(f"\n----- {profile.UPPER()} TRADER -----")
                trader.print_performance_summary()
            
            for trader in traders.values():
                trader.save_state(f"trader_state_{trader.profile_type}.json")
            
            end_time = datetime.datetime.now()
            total_runtime = end_time - start_time
            print(f"\nTotal simulation runtime: {total_runtime}")
            print(f"Total trading days simulated: {day_counter}")
            print(f"Total trading sessions: {session_counter}")
            
            print("\nWaiting for next start signal...")
    
    except KeyboardInterrupt:
        print("\nScript stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()