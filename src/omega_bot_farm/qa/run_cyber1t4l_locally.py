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
Local Runner for CyBer1t4L QA Bot
---------------------------------
This script enables running the CyBer1t4L QA Bot locally without Docker.
It sets up the necessary environment and directories before starting the bot.
"""

import os
import sys
import argparse
import shutil
import logging
import time
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Add the project root to the Python path to ensure imports work correctly
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
project_root = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
sys.path.insert(0, str(project_root))

# Import the CyBer1t4L QA Bot
from src.omega_bot_farm.qa.cyber1t4l_qa_bot import CyBer1t4L, Colors

def setup_local_directories():
    """
    Creates necessary directories for running CyBer1t4L locally.
    """
    # Define directories
    config_dir = script_dir / "local_run" / "config"
    reports_dir = script_dir / "local_run" / "reports"
    logs_dir = script_dir / "local_run" / "logs"
    
    # Create directories
    for directory in [config_dir, reports_dir, logs_dir]:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create a basic config file if it doesn't exist
    config_file = config_dir / "config.yaml"
    if not config_file.exists():
        with open(config_file, 'w') as f:
            f.write("""bot:
  name: CyBer1t4L
  description: Advanced Quality Assurance Bot for OMEGA Trading Ecosystem
  version: 1.0.0

testing:
  coverage_threshold: 80.0
  monitor_components:
    - trading
    - discord
    - matrix
  critical_modules:
    - src/omega_bot_farm/trading/b0ts/ccxt/ccxt_strategic_trader.py
    - src/omega_bot_farm/bitget_positions_info.py
    - src/omega_bot_farm/matrix_cli_live_positions.py
  report_directory: reports
  run_interval_minutes: 60

discord:
  enabled: true
  command_prefix: "!"
  status_message: "Monitoring QA | /qa_status"

monitoring:
  enabled: true
  interval_minutes: 60
  realtime_monitoring: true
  
reporting:
  html_reports: true
  json_reports: true
  console_reports: true
  max_report_age_days: 30
  report_format: "cyberpunk"
""")
        print(f"Created default config file: {config_file}")
    
    return {
        'config_dir': config_dir,
        'reports_dir': reports_dir,
        'logs_dir': logs_dir
    }

def setup_environment():
    """
    Sets up the environment variables needed by the CyBer1t4L QA Bot.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Check for required environment variables
    required_vars = [
        "CYBER1T4L_APP_ID",
        "CYBER1T4L_PUBLIC_KEY",
        "DISCORD_BOT_TOKEN"
    ]
    
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"{Colors.NEON_RED}ERROR: The following required environment variables are missing:{Colors.RESET}")
        for var in missing_vars:
            print(f"  - {var}")
        print(f"\nPlease ensure these are set in your .env file or environment.")
        return False
        
    # Set default environment variables if not already set
    if not os.environ.get("LOG_LEVEL"):
        os.environ["LOG_LEVEL"] = "INFO"
    
    if not os.environ.get("COVERAGE_THRESHOLD"):
        os.environ["COVERAGE_THRESHOLD"] = "80.0"
    
    return True

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="CyBer1t4L QA Bot - Local Runner"
    )
    
    parser.add_argument(
        "--mode", 
        choices=["full", "coverage", "generate", "monitor"],
        default="full", 
        help="Operation mode (default: full)"
    )
    
    parser.add_argument(
        "--modules", 
        nargs="+", 
        help="Modules to generate tests for (when using 'generate' mode)"
    )
    
    parser.add_argument(
        "--no-discord", 
        action="store_true",
        help="Run without Discord integration"
    )
    
    parser.add_argument(
        "--threshold", 
        type=float, 
        default=80.0,
        help="Coverage threshold percentage (default: 80.0)"
    )
    
    parser.add_argument(
        "--stop-if-running",
        action="store_true",
        help="Stop any currently running instance before starting"
    )
    
    return parser.parse_args()

def stop_running_instance():
    """Stop any currently running instance of CyBer1t4L."""
    print(f"\n{Colors.NEON_YELLOW}Checking for running CyBer1t4L instances...{Colors.RESET}")
    
    # Look for process running the module
    try:
        import psutil
        current_pid = os.getpid()
        count = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.pid == current_pid:
                continue
                
            cmdline = proc.info.get('cmdline', [])
            if cmdline and 'python' in cmdline[0].lower() and 'cyber1t4l' in ' '.join(cmdline).lower():
                print(f"{Colors.NEON_RED}Found running instance: PID {proc.pid}{Colors.RESET}")
                try:
                    proc.terminate()
                    print(f"{Colors.NEON_GREEN}Successfully terminated process {proc.pid}{Colors.RESET}")
                    count += 1
                except Exception as e:
                    print(f"{Colors.NEON_RED}Failed to terminate process {proc.pid}: {e}{Colors.RESET}")
        
        if count == 0:
            print(f"{Colors.NEON_GREEN}No running instances found.{Colors.RESET}")
        else:
            print(f"{Colors.NEON_GREEN}Terminated {count} running instances.{Colors.RESET}")
            # Give processes time to shut down
            time.sleep(2)
            
    except ImportError:
        print(f"{Colors.NEON_YELLOW}psutil not installed. Cannot check for running instances.{Colors.RESET}")
        print(f"{Colors.NEON_YELLOW}Install with: pip install psutil{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.NEON_RED}Error checking for running instances: {e}{Colors.RESET}")

def main():
    """Main function to run the CyBer1t4L QA Bot locally."""
    print(f"\n{Colors.NEON_GREEN}Starting CyBer1t4L QA Bot Local Runner{Colors.RESET}\n")
    
    args = parse_args()
    
    if args.stop_if_running:
        stop_running_instance()
    
    setup_local_directories()
    setup_environment()
    
    # Set up logging
    log_dir = Path("src/omega_bot_farm/qa/local_run/logs")
    log_file = log_dir / f"cyber1t4l_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Map string log levels to logging constants
    log_level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    
    # Get log level from environment variable, default to INFO
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    level = log_level_map.get(log_level, logging.INFO)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=str(log_file),
        filemode='a'
    )
    
    print(f"Logs will be written to: {log_file}")
    
    # Handle Discord integration
    if args.no_discord:
        print(f"{Colors.NEON_YELLOW}Running without Discord integration{Colors.RESET}\n")
        # Set placeholder values for required Discord environment variables
        os.environ["DISCORD_BOT_TOKEN"] = "DISABLED"
        os.environ["CYBER1T4L_APP_ID"] = "DISABLED"
        os.environ["CYBER1T4L_PUBLIC_KEY"] = "DISABLED"
    
    # Create and run CyBer1t4L instance
    cyber1t4l = CyBer1t4L(project_root=Path(os.getcwd()))
    
    # Display the CyBer1t4L logo
    cyber1t4l.display_intro()
    
    # Run in the specified mode
    if args.mode == "full":
        cyber1t4l.run_full_qa_cycle()
    elif args.mode == "coverage":
        cyber1t4l.run_coverage_check()
    elif args.mode == "generate":
        if not args.modules:
            print(f"{Colors.NEON_RED}No modules specified. Use --modules to specify modules{Colors.RESET}")
            return 1
        cyber1t4l.generate_tests(args.modules)
    elif args.mode == "monitor":
        cyber1t4l.realtime_monitor.start_monitoring()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            cyber1t4l.realtime_monitor.stop_monitoring()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 