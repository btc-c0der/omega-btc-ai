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
OmegaBTC AI Trading System Runner

This script connects the BtcFuturesTrader with the FuturesReporter
to track trading performance and visualize results.
"""

import os
import sys
import argparse
import time
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from omega_ai.trading.btc_futures_trader import BtcFuturesTrader
from omega_ai.reporting.futures_reporter import FuturesReporter

def main():
    parser = argparse.ArgumentParser(description='Run OmegaBTC AI Trading System')
    parser.add_argument('--mode', choices=['live', 'simulation'], default='simulation', 
                      help='Trading mode (live or simulation)')
    parser.add_argument('--capital', type=float, default=10000.0, help='Initial capital')
    parser.add_argument('--max-leverage', type=int, default=5, help='Maximum leverage')
    parser.add_argument('--risk', type=float, default=0.02, help='Risk per trade (decimal)')
    parser.add_argument('--log-dir', default='logs', help='Directory for logs')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    # Create log directory if it doesn't exist
    os.makedirs(args.log_dir, exist_ok=True)
    
    # Initialize futures reporter
    reporter = FuturesReporter(log_dir=args.log_dir, debug_mode=args.debug)
    
    # Initialize trader
    trader = BtcFuturesTrader(
        initial_capital=args.capital,
        max_leverage=args.max_leverage,
        risk_per_trade=args.risk,
        max_positions=3
    )
    
    # Load previous state if available
    trader.load_state()
    
    # Register trader with reporter
    reporter.register_trader(
        trader_name="BTC_Futures_Omega",
        trader_type="strategic",  # You can change this based on your trader's characteristics
        trader_instance=trader
    )
    
    # Start the metrics reporting in background
    reporter.schedule_metrics_reporting(interval_seconds=300)  # Report every 5 minutes
    
    print(f"Starting OmegaBTC AI Trading in {args.mode.upper()} mode")
    print(f"Session ID: {reporter.session_id}")
    print(f"Initial capital: ${args.capital:.2f}")
    
    try:
        # Helper function to integrate trader with reporter
        def handle_position_events():
            # Check for new positions opened since last check
            for position in trader.open_positions:
                if position.id not in reported_positions:
                    # Record entry in reporter
                    trade_id = reporter.record_trade_entry(
                        trader_name="BTC_Futures_Omega",
                        direction=position.direction,
                        entry_price=position.entry_price,
                        position_size=position.size,
                        leverage=position.leverage,
                        stop_loss=position.stop_loss or 0.0,
                        take_profits=[{
                            "price": tp["price"], 
                            "percentage": tp["percentage"]
                        } for tp in position.take_profits],
                        entry_reason=position.entry_reason
                    )
                    
                    # Map trader's position ID to reporter's trade ID
                    position_mapping[position.id] = trade_id
                    reported_positions.add(position.id)
            
            # Check for closed positions
            closed_positions = []
            for pos_id in list(reported_positions):
                position = next((p for p in trader.trade_history.trades 
                               if p.id == pos_id and p.status == "CLOSED"), None)
                               
                if position:
                    # Record exit in reporter
                    reporter.record_trade_exit(
                        trade_id=position_mapping[pos_id],
                        exit_price=position.exit_price,
                        exit_type="take_profit" if position.realized_pnl > 0 else "stop_loss",
                        pnl=position.realized_pnl,
                        exit_reason=position.exit_reason or "Position closed"
                    )
                    
                    # Remove from tracking
                    reported_positions.remove(pos_id)
                    closed_positions.append(pos_id)
            
            # Remove closed positions from mapping
            for pos_id in closed_positions:
                if pos_id in position_mapping:
                    del position_mapping[pos_id]
        
        # Track which positions have been reported
        reported_positions = set()
        position_mapping = {}  # Maps trader's position IDs to reporter's trade IDs
        
        # Main loop
        if args.mode == 'live':
            # Live trading mode with real data
            try:
                while True:
                    # Let trader update with new price and manage positions
                    trader.update_current_price()
                    trader.manage_open_positions()
                    
                    # Check for new trading opportunities
                    should_open, reason, leverage = trader.should_open_position()
                    if should_open:
                        direction = "LONG" if "LONG" in reason else "SHORT"
                        trader.open_position(direction, reason, leverage)
                    
                    # Update reporter with position changes
                    handle_position_events()
                    
                    # Sleep to avoid excessive CPU usage
                    time.sleep(5)
                    
            except KeyboardInterrupt:
                print("\nTrading stopped by user.")
                
        else:
            # Simulation mode 
            trader.run_live_trading_simulation(update_interval=1.0)
            
            # Final update to reporter
            handle_position_events()
        
        # Generate final report
        report = reporter.generate_performance_report()
        report_file = os.path.join(args.log_dir, f"performance_{reporter.session_id}.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Export Grafana dashboard if requested
        dashboard_file = os.path.join(args.log_dir, "trader_dashboard.json")
        reporter.export_grafana_dashboard(dashboard_file)
        
        print(f"Performance report saved to: {report_file}")
        print(f"Grafana dashboard exported to: {dashboard_file}")
        
    finally:
        # Save trader state
        trader.save_state()
        print("Trading session complete.")

if __name__ == "__main__":
    main()