#!/usr/bin/env python3

"""
OMEGA GRID PORTAL - 5D UI Dashboard for Bot Management
=====================================================

A comprehensive 5D dashboard for managing all bots in the Omega ecosystem,
with quantum computing integration, real-time monitoring, and divine alignment.

Copyright (c) 2024 OMEGA BTC AI
Licensed under GBU2 License
"""

import os
import sys
import argparse
import asyncio
import logging
import time
import json
import subprocess
import threading
import webbrowser
from pathlib import Path
from datetime import datetime

# Add parent directories to path
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

# ANSI Colors for terminal output
GREEN = "\033[92m"
GOLD = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(current_dir, "omega_grid_portal.log"))
    ]
)
logger = logging.getLogger("omega_grid_portal")

class OmegaBot:
    """Representation of a single bot in the OMEGA ecosystem"""
    
    def __init__(self, name, path, description, category, config=None):
        self.name = name
        self.path = path
        self.description = description
        self.category = category
        self.status = "inactive"
        self.process = None
        self.last_start = None
        self.last_stop = None
        self.config = config or {}
        self.logs = []
        self.metrics = {
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
            "uptime": 0
        }
        
    def start(self):
        """Start the bot"""
        if self.status == "active":
            logger.warning(f"Bot {self.name} is already running")
            return False
            
        logger.info(f"Starting bot: {self.name}")
        try:
            env = os.environ.copy()
            # Add any bot-specific environment variables
            for key, value in self.config.get("env", {}).items():
                env[key] = str(value)
                
            full_path = os.path.join(project_root, self.path)
            self.process = subprocess.Popen(
                [sys.executable, full_path],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            self.status = "active"
            self.last_start = datetime.now()
            
            # Start a thread to capture logs
            threading.Thread(target=self._capture_logs, daemon=True).start()
            return True
        except Exception as e:
            logger.error(f"Error starting bot {self.name}: {e}")
            self.status = "error"
            return False
            
    def _capture_logs(self):
        """Capture logs from bot process"""
        while self.process and self.process.poll() is None:
            if self.process.stdout:
                line = self.process.stdout.readline().strip()
                if line:
                    self.logs.append({"timestamp": datetime.now().isoformat(), "message": line})
                    # Keep only the last 100 log entries
                    if len(self.logs) > 100:
                        self.logs.pop(0)
            else:
                # If stdout is None, sleep a bit to avoid CPU spinning
                time.sleep(0.1)
        
        # Process ended
        if self.process and self.process.poll() is not None:
            self.status = "inactive"
            
    def stop(self):
        """Stop the bot"""
        if self.status != "active" or not self.process:
            logger.warning(f"Bot {self.name} is not running")
            return False
            
        logger.info(f"Stopping bot: {self.name}")
        try:
            self.process.terminate()
            # Give it some time to terminate gracefully
            for _ in range(5):
                if self.process.poll() is not None:
                    break
                time.sleep(1)
                
            # Force kill if still running
            if self.process.poll() is None:
                self.process.kill()
                
            self.status = "inactive"
            self.last_stop = datetime.now()
            return True
        except Exception as e:
            logger.error(f"Error stopping bot {self.name}: {e}")
            return False
            
    def restart(self):
        """Restart the bot"""
        self.stop()
        time.sleep(2)  # Wait a bit
        return self.start()
        
    def get_status(self):
        """Get the current status of the bot"""
        if self.process:
            # Check if process is still running
            if self.process.poll() is not None:
                self.status = "inactive"
                
        return {
            "name": self.name,
            "status": self.status,
            "category": self.category,
            "description": self.description,
            "last_start": self.last_start.isoformat() if self.last_start else None,
            "last_stop": self.last_stop.isoformat() if self.last_stop else None,
            "metrics": self.metrics,
            "logs": self.logs[-5:]  # Last 5 log entries
        }

class OmegaGridPortal:
    """Main management class for the OMEGA Grid Portal"""
    
    def __init__(self):
        """Initialize the manager"""
        self.bots = {}
        self.services = {}
        self.redis_status = False
        self.webserver_status = False
        self._load_bots()
        self._load_services()
        
    def _load_bots(self):
        """Load all bots in the farm"""
        bot_configs = {
            "bitget_position_analyzer": {
                "path": "src/omega_bot_farm/trading/b0ts/bitget_analyzer/bitget_position_analyzer_b0t.py",
                "description": "Analyzes BitGet positions with Fibonacci levels",
                "category": "analysis",
                "config": {
                    "env": {
                        "LOG_LEVEL": "INFO"
                    }
                }
            },
            "matrix_cli": {
                "path": "src/omega_bot_farm/bitget_matrix_cli_b0t.py",
                "description": "Matrix-style CLI interface for position monitoring",
                "category": "visualization",
                "config": {}
            },
            "discord_bot": {
                "path": "src/omega_bot_farm/discord/bot.py",
                "description": "Discord bot for positions management",
                "category": "communication",
                "config": {
                    "env": {
                        "LOG_LEVEL": "INFO"
                    }
                }
            },
            "strategic_trader": {
                "path": "src/omega_bot_farm/trading/b0ts/ccxt/ccxt_strategic_trader.py",
                "description": "CCXT-based strategic trading bot",
                "category": "trading",
                "config": {}
            },
            "position_monitor": {
                "path": "omega_ai/trading/exchanges/bitget_position_monitor.py",
                "description": "Monitors BitGet positions for changes",
                "category": "monitoring",
                "config": {}
            },
            "cybernetic_quantum_bloom": {
                "path": "src/omega_bot_farm/cybernetic_quantum_bloom.py",
                "description": "Quantum-aligned market prediction system",
                "category": "prediction",
                "config": {}
            },
            "matrix_btc_cyberpunk": {
                "path": "src/omega_bot_farm/matrix_btc_cyberpunk.py",
                "description": "Cyberpunk visualization for BTC",
                "category": "visualization",
                "config": {}
            }
        }
        
        # Create bot objects
        for name, config in bot_configs.items():
            self.bots[name] = OmegaBot(
                name=name,
                path=config["path"],
                description=config["description"],
                category=config["category"],
                config=config.get("config", {})
            )
            
        logger.info(f"Loaded {len(self.bots)} bots")
        
    def _load_services(self):
        """Load all services required by the farm"""
        service_configs = {
            "redis": {
                "description": "Redis server for data exchange",
                "start_cmd": "redis-server",
                "check_cmd": "redis-cli ping",
                "success_output": "PONG",
                "required": True
            },
            "reggie_dashboard": {
                "description": "Web-based position visualization",
                "start_cmd": f"{sys.executable} {os.path.join(project_root, 'omega_ai/visualizer/frontend/reggae-dashboard/live-api-server.py')}",
                "check_cmd": "curl -s http://localhost:5000/api/health",
                "success_output": "healthy",
                "required": False
            },
            "rasta_dashboard": {
                "description": "Streamlit dashboard for OMEGA",
                "start_cmd": f"{sys.executable} {os.path.join(project_root, 'omega_ai/run_dashboard.py')}",
                "check_cmd": "curl -s http://localhost:8501",
                "success_output": "Streamlit",
                "required": False
            }
        }
        
        # Create service objects
        for name, config in service_configs.items():
            self.services[name] = {
                "name": name,
                "description": config["description"],
                "start_cmd": config["start_cmd"],
                "check_cmd": config["check_cmd"],
                "success_output": config["success_output"],
                "required": config["required"],
                "status": "inactive",
                "process": None
            }
            
        logger.info(f"Loaded {len(self.services)} services")
        
    def check_service(self, service_name):
        """Check if a service is running"""
        if service_name not in self.services:
            return False
            
        service = self.services[service_name]
        try:
            result = subprocess.run(
                service["check_cmd"].split(),
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if service["success_output"] in result.stdout:
                service["status"] = "active"
                return True
            else:
                service["status"] = "inactive"
                return False
        except Exception as e:
            logger.error(f"Error checking service {service_name}: {e}")
            service["status"] = "error"
            return False
            
    def start_service(self, service_name):
        """Start a required service"""
        if service_name not in self.services:
            return False
            
        service = self.services[service_name]
        if self.check_service(service_name):
            logger.info(f"Service {service_name} is already running")
            return True
            
        logger.info(f"Starting service: {service_name}")
        try:
            process = subprocess.Popen(
                service["start_cmd"].split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            service["process"] = process
            service["status"] = "starting"
            
            # Give it some time to start
            time.sleep(3)
            
            # Check if it's running
            if self.check_service(service_name):
                logger.info(f"Service {service_name} started successfully")
                return True
            else:
                logger.error(f"Service {service_name} failed to start")
                return False
        except Exception as e:
            logger.error(f"Error starting service {service_name}: {e}")
            service["status"] = "error"
            return False
            
    def start_required_services(self):
        """Start all required services"""
        success = True
        for name, service in self.services.items():
            if service["required"] and not self.check_service(name):
                if not self.start_service(name):
                    success = False
                    
        return success
        
    def start_bot(self, bot_name):
        """Start a specific bot"""
        if bot_name not in self.bots:
            logger.error(f"Bot {bot_name} not found")
            return False
            
        # Make sure required services are running
        self.start_required_services()
        
        # Start the bot
        return self.bots[bot_name].start()
            
    def stop_bot(self, bot_name):
        """Stop a specific bot"""
        if bot_name not in self.bots:
            logger.error(f"Bot {bot_name} not found")
            return False
            
        return self.bots[bot_name].stop()
        
    def restart_bot(self, bot_name):
        """Restart a specific bot"""
        if bot_name not in self.bots:
            logger.error(f"Bot {bot_name} not found")
            return False
            
        return self.bots[bot_name].restart()
        
    def start_all_bots(self):
        """Start all bots in the farm"""
        # Make sure required services are running
        self.start_required_services()
        
        success_count = 0
        for bot_name in self.bots:
            if self.start_bot(bot_name):
                success_count += 1
        
        logger.info(f"Started {success_count}/{len(self.bots)} bots")
        return success_count
        
    def stop_all_bots(self):
        """Stop all running bots"""
        success_count = 0
        for bot_name, bot in self.bots.items():
            if bot.status == "active" and self.stop_bot(bot_name):
                success_count += 1
        
        logger.info(f"Stopped {success_count} bots")
        return success_count
        
    def get_status(self):
        """Get the status of all bots and services"""
        bot_status = {name: bot.get_status() for name, bot in self.bots.items()}
        
        # Update service status
        for name in self.services:
            self.check_service(name)
            
        service_status = {name: service for name, service in self.services.items()}
        
        return {
            "bots": bot_status,
            "services": service_status,
            "timestamp": datetime.now().isoformat(),
            "grid_status": "active" if any(bot.status == "active" for bot in self.bots.values()) else "inactive"
        }
        
    def export_status(self, file_path=None):
        """Export the current status to a JSON file"""
        status = self.get_status()
        
        if not file_path:
            file_path = os.path.join(current_dir, "omega_grid_status.json")
            
        with open(file_path, "w") as f:
            json.dump(status, f, indent=2)
            
        logger.info(f"Status exported to {file_path}")
        return file_path
        
    def launch_matrix_dashboard(self):
        """Launch the Matrix terminal dashboard"""
        print(f"{MAGENTA}{BOLD}Launching Matrix Terminal Dashboard...{RESET}")
        matrix_path = os.path.join(project_root, "src/omega_bot_farm/tmp/bitget_matrix_position_display.py")
        
        if not os.path.exists(matrix_path):
            logger.error(f"Matrix dashboard not found at {matrix_path}")
            return False
            
        try:
            subprocess.Popen([sys.executable, matrix_path])
            logger.info("Matrix dashboard launched")
            return True
        except Exception as e:
            logger.error(f"Error launching Matrix dashboard: {e}")
            return False
            
    def launch_web_dashboard(self):
        """Launch the web-based dashboard"""
        print(f"{GREEN}{BOLD}Launching Web Dashboard...{RESET}")
        
        # Try to start the Reggae dashboard service
        if self.start_service("reggie_dashboard"):
            # Open the dashboard in a web browser
            webbrowser.open("http://localhost:5000")
            logger.info("Reggae dashboard launched at http://localhost:5000")
            return True
        else:
            # Fall back to Rasta dashboard
            if self.start_service("rasta_dashboard"):
                webbrowser.open("http://localhost:8501")
                logger.info("Rasta dashboard launched at http://localhost:8501")
                return True
                
        logger.error("Failed to launch web dashboard")
        return False
        
    def display_quantum_loading(self):
        """Display a quantum loading animation"""
        quantum_states = ["⚛️", "🔄", "🧬", "🔮", "✨", "🌠", "💫", "🌌"]
        print(f"{CYAN}Quantum alignment in progress...{RESET}")
        for i in range(10):
            state = quantum_states[i % len(quantum_states)]
            sys.stdout.write(f"\r{state} Quantum state: {i*10}% aligned {state}")
            sys.stdout.flush()
            time.sleep(0.2)
        print(f"\n{GREEN}Quantum alignment complete!{RESET}")
        
    def launch_5d_dashboard(self):
        """Launch the 5D comprehensive dashboard"""
        print(f"{CYAN}{BOLD}LAUNCHING 5D QUANTUM DASHBOARD...{RESET}")
        print(f"{GOLD}Initializing quantum computing alignment...{RESET}")
        
        # Display quantum loading animation
        self.display_quantum_loading()
        
        # Start required services
        self.start_required_services()
        
        # Start web dashboard
        self.launch_web_dashboard()
        
        print(f"\n{GREEN}5D Grid Portal activated!{RESET}")
        print(f"{CYAN}Monitoring {len(self.bots)} bots across the OMEGA ecosystem{RESET}")
        return True

def display_ascii_banner():
    """Display an ASCII art banner"""
    banner = f"""
{CYAN}{BOLD}    ██████╗ ███╗   ███╗███████╗ ██████╗  █████╗{RESET}     {GREEN}{BOLD} ██████╗ ██████╗ ██╗██████╗ {RESET}
{CYAN}{BOLD}   ██╔═══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗{RESET}    {GREEN}{BOLD}██╔════╝ ██╔══██╗██║██╔══██╗{RESET}
{CYAN}{BOLD}   ██║   ██║██╔████╔██║█████╗  ██║  ███╗███████║{RESET}    {GREEN}{BOLD}██║  ███╗██████╔╝██║██║  ██║{RESET}
{CYAN}{BOLD}   ██║   ██║██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║{RESET}    {GREEN}{BOLD}██║   ██║██╔══██╗██║██║  ██║{RESET}
{CYAN}{BOLD}   ╚██████╔╝██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║{RESET}    {GREEN}{BOLD}╚██████╔╝██║  ██║██║██████╔╝{RESET}
{CYAN}{BOLD}    ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝{RESET}    {GREEN}{BOLD} ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝ {RESET}
                                                                             
{MAGENTA}{BOLD}    ██████╗  ██████╗ ██████╗ ████████╗ █████╗ ██╗      {RESET}
{MAGENTA}{BOLD}    ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔══██╗██║      {RESET}
{MAGENTA}{BOLD}    ██████╔╝██║   ██║██████╔╝   ██║   ███████║██║      {RESET}
{MAGENTA}{BOLD}    ██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══██║██║      {RESET}
{MAGENTA}{BOLD}    ██║     ╚██████╔╝██║  ██║   ██║   ██║  ██║███████╗ {RESET}
{MAGENTA}{BOLD}    ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝ {RESET}
                                                                  
{GOLD}{BOLD}          🌟  QUANTUM COMPUTING PORTAL - RELEASE Φ1.618  🌟{RESET}
{GREEN}          5D UI Dashboard for Omega Bot Farm Management{RESET}
"""
    print(banner)

def main():
    """Main entry point for the OMEGA Grid Portal"""
    parser = argparse.ArgumentParser(description="OMEGA Grid Portal - 5D Bot Management Dashboard")
    parser.add_argument("--mode", choices=["matrix", "web", "5d"], default="5d",
                      help="Dashboard mode (matrix=terminal, web=browser, 5d=quantum)")
    parser.add_argument("--start-all", action="store_true", 
                      help="Start all bots automatically")
    parser.add_argument("--start", type=str, help="Start a specific bot")
    parser.add_argument("--stop", type=str, help="Stop a specific bot")
    parser.add_argument("--restart", type=str, help="Restart a specific bot")
    parser.add_argument("--status", action="store_true", help="Show status of all bots")
    parser.add_argument("--export-status", type=str, help="Export status to a file")
    args = parser.parse_args()
    
    # Display ASCII banner
    display_ascii_banner()
    
    # Initialize the grid portal
    portal = OmegaGridPortal()
    
    # Handle commands
    if args.start:
        portal.start_bot(args.start)
        
    if args.stop:
        portal.stop_bot(args.stop)
        
    if args.restart:
        portal.restart_bot(args.restart)
        
    if args.start_all:
        portal.start_all_bots()
        
    if args.status:
        status = portal.get_status()
        print(f"\n{CYAN}OMEGA GRID STATUS:{RESET}")
        print(f"Grid Status: {GREEN if status['grid_status'] == 'active' else RED}{status['grid_status'].upper()}{RESET}")
        print(f"\n{CYAN}Active Bots:{RESET}")
        active_count = 0
        for name, bot in status["bots"].items():
            if bot["status"] == "active":
                active_count += 1
                print(f"  • {GREEN}{name}{RESET} - {bot['description']}")
        
        if active_count == 0:
            print(f"  {RED}No active bots{RESET}")
            
        print(f"\n{CYAN}Services:{RESET}")
        for name, service in status["services"].items():
            status_color = GREEN if service["status"] == "active" else RED
            print(f"  • {name}: {status_color}{service['status']}{RESET} - {service['description']}")
            
    if args.export_status:
        portal.export_status(args.export_status)
        
    # Launch dashboard based on mode
    if args.mode == "matrix":
        portal.launch_matrix_dashboard()
    elif args.mode == "web":
        portal.launch_web_dashboard()
    elif args.mode == "5d":
        portal.launch_5d_dashboard()
        
    # Keep the script running
    try:
        print(f"\n{GREEN}OMEGA Grid Portal is running. Press Ctrl+C to exit.{RESET}")
        print(f"{CYAN}Use the dashboard to monitor and control your bots.{RESET}")
        
        # Update status periodically
        while True:
            status = portal.get_status()
            # Log active bots
            active_bots = [name for name, bot in status["bots"].items() if bot["status"] == "active"]
            if active_bots:
                logger.info(f"Active bots: {', '.join(active_bots)}")
            time.sleep(60)  # Update every minute
    except KeyboardInterrupt:
        print(f"\n{GOLD}Shutting down OMEGA Grid Portal...{RESET}")
        portal.stop_all_bots()
        print(f"{GREEN}All systems safely shutdown. JAH BLESS!{RESET}")

if __name__ == "__main__":
    main() 