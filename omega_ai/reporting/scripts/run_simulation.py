#!/usr/bin/env python3

"""
OmegaBTC AI Trading Simulation Runner

This script runs a simulation of different trading profiles:
- Aggressive Trader (high risk, short timeframes)
- Strategic Trader (calculated risk, longer timeframes)
- Newbie Trader (inexperienced, emotional decisions)

Results are logged and can be visualized in Grafana.
"""

import os
import sys
import json
import datetime
import argparse

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from omega_ai.reporting.futures_reporter import FuturesReporter
from omega_ai.simulation.market_simulator import MarketSimulator

# Import all trader profiles
from omega_ai.trading.profiles.aggressive_trader import AggressiveTrader
from omega_ai.trading.profiles.strategic_trader import StrategicTrader
from omega_ai.trading.profiles.newbie_trader import NewbieTrader
from omega_ai.trading.profiles.scalper_trader import ScalperTrader

# Registry of available trader types
TRADER_PROFILES = {
    "aggressive": AggressiveTrader,
    "strategic": StrategicTrader,
    "newbie": NewbieTrader,
    "scalper": ScalperTrader
}

def load_config(config_path):
    """Load configuration from a JSON file."""
    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description='Run OmegaBTC AI Trading Simulation')
    parser.add_argument('--config', default='config/config.json', help='Path to configuration file')
    parser.add_argument('--log-dir', default='logs', help='Directory for logs')
    parser.add_argument('--dashboard-output', default='dashboards/trading_dashboard.json', 
                       help='Output file for Grafana dashboard')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--days', type=int, default=30, help='Days to simulate')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    args = parser.parse_args()
    
    # Create directories if they don't exist
    os.makedirs(args.log_dir, exist_ok=True)
    os.makedirs(os.path.dirname(args.dashboard_output), exist_ok=True)
    
    # Initialize reporter
    reporter = FuturesReporter(
        log_dir=args.log_dir,
        debug_mode=args.debug
    )
    
    print(f"Starting simulation with session ID: {reporter.session_id}")
    
    # Create and register traders
    initial_capital = 10000.0
    aggressive = AggressiveTrader(initial_capital=initial_capital)
    strategic = StrategicTrader(initial_capital=initial_capital)
    newbie = NewbieTrader(initial_capital=initial_capital)
    scalper = ScalperTrader(initial_capital=initial_capital)
    
    reporter.register_trader("Aggressive_Trader", "aggressive", aggressive)
    reporter.register_trader("Strategic_Trader", "strategic", strategic)
    reporter.register_trader("Newbie_Trader", "newbie", newbie)
    reporter.register_trader("Scalper_1", "scalper", scalper)
    
    # Start metrics reporting in background
    reporter.schedule_metrics_reporting(interval_seconds=300)
    
    # Initialize market simulator
    simulator = MarketSimulator(seed=args.seed)
    
    # Run simulation for specified days
    print(f"Running {args.days} days of trading simulation...")
    day_count = args.days
    bars_per_day = 24  # For hourly bars
    
    for day in range(day_count):
        print(f"Day {day+1}/{day_count}")
        
        # Generate market data for the day
        market_data = simulator.generate_day_data(bars=bars_per_day)
        
        # Simulate trading for each trader
        for bar in range(bars_per_day):
            current_price = market_data[bar]
            
            # Aggressive trader decisions
            agg_decision = aggressive.make_decision(current_price, bar)
            if agg_decision['action'] == 'ENTER':
                trade_id = reporter.record_trade_entry(
                    trader_name="Aggressive_Trader",
                    direction=agg_decision['direction'],
                    entry_price=current_price,
                    position_size=agg_decision['size'],
                    leverage=agg_decision['leverage'],
                    stop_loss=agg_decision['stop_loss'],
                    take_profits=agg_decision['take_profits'],
                    entry_reason=agg_decision['reason']
                )
            elif agg_decision['action'] == 'EXIT' and agg_decision['trade_id']:
                reporter.record_trade_exit(
                    trade_id=agg_decision['trade_id'],
                    exit_price=current_price,
                    exit_type=agg_decision['exit_type'],
                    pnl=agg_decision['pnl'],
                    exit_reason=agg_decision['reason'],
                    exit_bar=bar
                )
            
            # Repeat for other traders...
            # Strategic trader decisions
            # Newbie trader decisions
    
    # Generate summary report
    report = reporter.generate_performance_report()
    report_file = os.path.join(args.log_dir, f"performance_report_{reporter.session_id}.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
        
    print(f"Performance report saved to: {report_file}")
    
    # Export Grafana dashboard
    if reporter.export_grafana_dashboard(args.dashboard_output):
        print(f"Grafana dashboard exported to: {args.dashboard_output}")
    else:
        print("Failed to export Grafana dashboard")
    
    # Print summary statistics
    print("\n===== SIMULATION SUMMARY =====")
    for trader_name, stats in report['traders'].items():
        print(f"\n{trader_name} ({stats['trader_type']})")
        print(f"  Initial: ${stats['initial_capital']:.2f}")
        print(f"  Final:   ${stats['current_capital']:.2f}")
        print(f"  Return:  {stats['return_percentage']:.2f}%")
        print(f"  Win Rate: {stats['win_rate']:.2f}%")
        print(f"  Trades:   {stats['total_trades']} ({stats['winning_trades']} wins, {stats['losing_trades']} losses)")
    
    print("\nSimulation complete.")

if __name__ == "__main__":
    main()