"""
OMEGA BTC AI - BitGet Live Traders Runner
=======================================

This script runs the live traders system with proper configuration and monitoring.
It includes command-line arguments for customization and real-time monitoring.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import asyncio
import argparse
import logging
from datetime import datetime
from typing import Optional
from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders
from omega_ai.alerts.telegram_market_report import send_telegram_alert

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('live_traders.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run OMEGA BTC AI Live Traders')
    parser.add_argument(
        '--use-testnet',
        action='store_true',
        default=True,
        help='Use BitGet testnet (default: True)'
    )
    parser.add_argument(
        '--initial-capital',
        type=float,
        default=24.0,
        help='Initial capital per trader in USDT (default: 24.0)'
    )
    parser.add_argument(
        '--symbol',
        type=str,
        default='BTCUSDT',
        help='Trading pair symbol (default: BTCUSDT)'
    )
    parser.add_argument(
        '--update-interval',
        type=float,
        default=1.0,
        help='Update interval in seconds (default: 1.0)'
    )
    return parser.parse_args()

async def monitor_system(live_traders: BitGetLiveTraders):
    """Monitor system health and performance."""
    while live_traders.is_running:
        try:
            # Get system status
            status = {
                'timestamp': datetime.now().isoformat(),
                'traders': len(live_traders.traders),
                'total_pnl': sum(trader.total_pnl for trader in live_traders.traders.values()),
                'active_positions': sum(
                    len(trader.get_positions()) 
                    for trader in live_traders.traders.values()
                )
            }
            
            # Log status
            logger.info(f"System Status: {status}")
            
            # Send status update every hour
            if datetime.now().minute == 0:
                alert_msg = (
                    f"📊 OMEGA BTC AI SYSTEM STATUS\n"
                    f"Time: {status['timestamp']}\n"
                    f"Active Traders: {status['traders']}\n"
                    f"Total PnL: {status['total_pnl']:.2f} USDT\n"
                    f"Active Positions: {status['active_positions']}"
                )
                send_telegram_alert(alert_msg)
            
            await asyncio.sleep(60)  # Check every minute
            
        except Exception as e:
            logger.error(f"Error in system monitoring: {str(e)}")
            await asyncio.sleep(5)  # Wait before retrying

async def main():
    """Main entry point for the live traders system."""
    # Parse command line arguments
    args = parse_args()
    
    # Initialize live traders
    live_traders = BitGetLiveTraders(
        use_testnet=args.use_testnet,
        initial_capital=args.initial_capital,
        symbol=args.symbol
    )
    
    try:
        # Start system monitoring
        monitor_task = asyncio.create_task(monitor_system(live_traders))
        
        # Start trading
        logger.info(f"Starting OMEGA BTC AI Live Traders System")
        logger.info(f"Mode: {'TESTNET' if args.use_testnet else 'MAINNET'}")
        logger.info(f"Initial Capital: {args.initial_capital} USDT per trader")
        logger.info(f"Trading Pair: {args.symbol}")
        
        # Send startup alert
        alert_msg = (
            f"🚀 OMEGA BTC AI LIVE TRADERS STARTED\n"
            f"Mode: {'TESTNET' if args.use_testnet else 'MAINNET'}\n"
            f"Capital: {args.initial_capital} USDT per trader\n"
            f"Symbol: {args.symbol}"
        )
        send_telegram_alert(alert_msg)
        
        # Start trading
        await live_traders.start_trading()
        
        # Wait for monitoring task
        await monitor_task
        
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    except Exception as e:
        logger.error(f"System error: {str(e)}")
    finally:
        # Stop trading
        await live_traders.stop_trading()
        
        # Send shutdown alert
        alert_msg = (
            f"🛑 OMEGA BTC AI LIVE TRADERS SHUTDOWN\n"
            f"Final PnL: {sum(trader.total_pnl for trader in live_traders.traders.values()):.2f} USDT"
        )
        send_telegram_alert(alert_msg)
        
        logger.info("System shutdown complete")

if __name__ == "__main__":
    asyncio.run(main()) 