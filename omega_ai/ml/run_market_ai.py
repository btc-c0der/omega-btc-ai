#!/usr/bin/env python3

import os
import sys
import time
import logging
import argparse
from datetime import datetime, timezone

# Add parent directory to path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from omega_ai.ml.generate_dummy_data import run_generator
from omega_ai.ml.market_trends_model import run_model

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# ANSI Colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run the Market Trends AI Model')
    
    parser.add_argument('--generate-data', action='store_true',
                        help='Generate dummy data for training')
    parser.add_argument('--days', type=int, default=30,
                        help='Number of days of data to generate (default: 30)')
    parser.add_argument('--train', action='store_true', 
                        help='Train the model on historical data')
    parser.add_argument('--predict', action='store_true',
                        help='Generate predictions based on current data')
    parser.add_argument('--monitor', action='store_true',
                        help='Run in continuous monitoring mode')
    parser.add_argument('--interval', type=int, default=60,
                        help='Prediction interval in seconds (default: 60)')
    
    args = parser.parse_args()
    
    # If no specific action is selected, default to prediction only
    if not (args.generate_data or args.train or args.predict or args.monitor):
        args.predict = True
    
    return args

def print_header():
    """Print the application header."""
    print(f"\n{MAGENTA}{BOLD}╔══════════════════════════════════════════════════════════╗{RESET}")
    print(f"{MAGENTA}{BOLD}║             OMEGA MARKET TRENDS AI MODEL                  ║{RESET}")
    print(f"{MAGENTA}{BOLD}║      🧠 DIVINE FIBONACCI LEARNING ALGORITHM 🧠           ║{RESET}")
    print(f"{MAGENTA}{BOLD}╚══════════════════════════════════════════════════════════╝{RESET}")
    print(f"{YELLOW}Version 1.0.0 | {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}{RESET}")
    print(f"{CYAN}Enhanced with Fibonacci Sacred Mathematics{RESET}")
    print()

def main():
    """Main entry point for the Market Trends AI Model."""
    args = parse_arguments()
    
    print_header()
    
    # Connect to Redis
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    print(f"{BLUE}Redis connection: {redis_host}:{redis_port}{RESET}")
    
    try:
        # Generate dummy data if requested
        if args.generate_data:
            print(f"{CYAN}Generating {args.days} days of historical market data...{RESET}")
            current_price = run_generator(days=args.days)
            print(f"{GREEN}{BOLD}Data generation complete!{RESET}")
        
        # Train and/or predict
        if args.train or args.predict:
            if args.monitor:
                print(f"{YELLOW}{BOLD}Starting continuous monitoring mode...{RESET}")
                print(f"{BLUE}Prediction interval: {args.interval} seconds{RESET}")
                print(f"{YELLOW}Press Ctrl+C to exit{RESET}")
                
                # Run in continuous mode
                while True:
                    try:
                        # Train or update model if needed
                        if args.train:
                            print(f"\n{CYAN}Training model on historical data...{RESET}")
                        
                        # Run model with training if requested
                        model = run_model(days_back=args.days, train=args.train)
                        
                        # Sleep until next prediction
                        time.sleep(args.interval)
                        
                    except KeyboardInterrupt:
                        print(f"\n{YELLOW}Monitoring stopped by user.{RESET}")
                        break
                    except Exception as e:
                        logger.error(f"Error in monitoring loop: {e}")
                        print(f"{RED}Error: {e}{RESET}")
                        print(f"{YELLOW}Retrying in 10 seconds...{RESET}")
                        time.sleep(10)
            else:
                # Run once
                if args.train:
                    print(f"{CYAN}Training model on historical data...{RESET}")
                
                # Run model with training if requested
                model = run_model(days_back=args.days, train=args.train)
                print(f"{GREEN}{BOLD}Model execution complete!{RESET}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        print(f"{RED}Error: {e}{RESET}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 