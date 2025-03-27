"""
OMEGA BTC AI Consolidated Runner

Main entry point for the OMEGA BTC AI system, using the ServiceManager for orchestration.
"""

import asyncio
import argparse
import logging
import sys
from typing import List, Optional

from omega_ai.orchestrator.service_manager import ServiceManager
from omega_ai.db_manager.database import setup_database
from omega_ai.data_feed.schumann_monitor import start_schumann_monitor, stop_schumann_monitor
from omega_ai.data_feed.btc_live_feed import start_btc_websocket, stop_btc_websocket
from omega_ai.mm_trap_detector.mm_trap_detector import MMTrapDetector
from omega_ai.monitor.monitor_market_trends import monitor_market_trends, stop_market_monitor
from omega_ai.visualization.omega_dashboard import start_dashboard, stop_dashboard
from omega_ai.trading.exchanges.bitget_live_traders import BitGetLiveTraders

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('omega_runner.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('OmegaRunner')

def display_banner():
    """Display the OMEGA BTC AI banner."""
    print("""
  ___  __  __ _____ ____    _      ____ _____ ____      _    ___ 
 / _ \|  \/  | ____/ ___|  / \    | __ )_   _/ ___|    / \  |_ _|
| | | | |\/| |  _|| |  _  / _ \   |  _ \ | || |       / _ \  | | 
| |_| | |  | | |__| |_| |/ ___ \  | |_) || || |___   / ___ \ | | 
 \___/|_|  |_|_____\____/_/   \_\ |____/ |_| \____| /_/   \_\___|
                                                                         
    """)

async def setup_services(service_manager: ServiceManager) -> None:
    """Register all services with the service manager."""
    # Database setup
    service_manager.register_service(
        name="database",
        start_func=setup_database,
        stop_func=lambda: None,  # No-op as database doesn't need cleanup
        dependencies=set()
    )
    
    # Schumann Monitor
    service_manager.register_service(
        name="schumann_monitor",
        start_func=start_schumann_monitor,
        stop_func=stop_schumann_monitor,
        dependencies={"database"}
    )
    
    # BTC Price Feed
    service_manager.register_service(
        name="btc_feed",
        start_func=start_btc_websocket,
        stop_func=stop_btc_websocket,
        dependencies={"database"}
    )
    
    # Market Trend Monitor
    service_manager.register_service(
        name="market_monitor",
        start_func=monitor_market_trends,
        stop_func=stop_market_monitor,
        dependencies={"database", "btc_feed"}
    )
    
    # MM Trap Detector
    service_manager.register_service(
        name="mm_trap_detector",
        start_func=lambda: MMTrapDetector().run(),
        stop_func=lambda: None,  # No explicit stop needed, will stop when event loop stops
        dependencies={"database", "btc_feed", "market_monitor"}
    )
    
    # Dashboard
    service_manager.register_service(
        name="dashboard",
        start_func=start_dashboard,
        stop_func=stop_dashboard,
        dependencies={"database", "btc_feed", "market_monitor", "mm_trap_detector"}
    )
    
    # Trading System
    service_manager.register_service(
        name="trading",
        start_func=lambda: BitGetLiveTraders(
            use_testnet=False,  # Use mainnet
            initial_capital=100.0,  # Initial capital per trader
            symbol="BTCUSDT",
            strategic_only=True,  # Only use strategic trader
            leverage=11,
            enable_pnl_alerts=True,
            pnl_alert_interval=1
        ).start_trading(),
        stop_func=lambda: None,  # Stop will be handled by the trader's shutdown
        dependencies={"database", "btc_feed", "market_monitor", "mm_trap_detector"}
    )

async def main():
    """Main entry point for the OMEGA BTC AI system."""
    parser = argparse.ArgumentParser(description="OMEGA BTC AI System Runner")
    parser.add_argument(
        "--mode",
        choices=["full", "trading", "monitoring", "dashboard"],
        default="full",
        help="Operation mode"
    )
    parser.add_argument(
        "--services",
        nargs="*",
        help="Specific services to start"
    )
    parser.add_argument(
        "--testnet",
        action="store_true",
        help="Use testnet instead of mainnet"
    )
    args = parser.parse_args()
    
    # Display banner
    display_banner()
    
    # Initialize service manager
    service_manager = ServiceManager()
    service_manager.setup_signal_handlers()
    
    # Setup services
    await setup_services(service_manager)
    
    # Determine which services to start based on mode
    services_to_start: List[str] = []
    if args.services:
        services_to_start = args.services
    else:
        if args.mode == "full":
            services_to_start = list(service_manager.services.keys())
        elif args.mode == "trading":
            services_to_start = ["database", "btc_feed", "market_monitor", "mm_trap_detector", "trading"]
        elif args.mode == "monitoring":
            services_to_start = ["database", "btc_feed", "market_monitor", "mm_trap_detector"]
        elif args.mode == "dashboard":
            services_to_start = ["database", "dashboard"]
    
    # Start health check task
    service_manager._health_check_task = asyncio.create_task(service_manager.health_check())
    
    try:
        # Start requested services
        for service in services_to_start:
            if not await service_manager.start_service(service):
                logger.error(f"Failed to start service {service}")
                await service_manager.shutdown()
                return
        
        # Keep the main task alive
        while not service_manager._shutdown_event.is_set():
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        await service_manager.shutdown()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        await service_manager.shutdown()
        raise

if __name__ == "__main__":
    asyncio.run(main()) 