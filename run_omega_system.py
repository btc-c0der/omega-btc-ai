#!/usr/bin/env python3
"""
OMEGA BTC AI - Complete System Launcher
======================================

This script launches all components of the OMEGA BTC AI system in a coordinated manner.
It handles process management, monitoring, and graceful shutdown of all components.

Components managed:
- WebSocket server for real-time data communication
- Trap detection consumer for market manipulation detection
- BTC live price feed for real-time market data
- Market trends monitor for trend analysis
- Trap probability meter for risk assessment
- Reggae Dashboard UI for visualization
- Enhanced Market Trend Analyzer for multi-timeframe analysis
- Fibonacci Dashboard Connector for visualization

Usage:
    ./run_omega_system.py [options]

Options:
    --no-reggae      Don't start the Reggae Dashboard UI
    --no-backend     Don't start the Reggae Backend Server
    --no-cleanup     Don't kill existing processes
    --no-fibonacci   Don't start the Fibonacci Dashboard Connector
    --no-market-analyzer  Don't start the Enhanced Market Trend Analyzer
    --no-live-api    Don't start the Live API Server
    --background     Run components in background mode
    --foreground     Run components in foreground mode (default)
    --auto-heal      Enable auto-healing for system components
    --ui-first       Start UI components first, then add other components

Examples:
    # Run all components with auto-cleanup
    ./run_omega_system.py
    
    # Run without the Reggae Dashboard
    ./run_omega_system.py --no-reggae
    
    # Run with auto-healing enabled in background mode
    ./run_omega_system.py --auto-heal --background

Author: OMEGA BTC AI Team
"""

import os
import sys
import time
import signal
import argparse
import subprocess
import logging
import psutil
import atexit
from pathlib import Path
import threading
import redis
import json
import socket
from datetime import datetime
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("omega_system")

# Process tracking
processes = []
running = True

# Project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()

# Log directory
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Auto-healing settings
MAX_RESTART_ATTEMPTS = 5
RESTART_COOLDOWN = 60  # seconds
HEALTH_CHECK_INTERVAL = 10  # seconds
AUTO_HEAL_ENABLED = False

# Redis connection
redis_client = None

class OmegaComponent:
    """
    Base class for OMEGA BTC AI system components.
    
    This class provides a unified interface for managing system components,
    including starting, stopping, monitoring, and automatic restart functionality.
    
    Attributes:
        name (str): Component display name
        command (str): Shell command to start the component
        process (subprocess.Popen): Process handle when running
        cwd (Path): Working directory for the component
        env (dict): Environment variables for the component
        restart_count (int): Number of times this component has been restarted
        max_restarts (int): Maximum number of automatic restarts
        is_optional (bool): Whether the component is optional for system operation
        log_file (str): Path to the component's log file
        status (str): Current component status ('starting', 'running', 'stopped', 'failed')
        last_restart (float): Timestamp of the last restart
        health_check_file (str): File to check for health validation
        health_check_method (function): Custom health check function
        run_in_background (bool): Whether to run in background mode
        startup_validation_timeout (float): Timeout for startup validation
        validation_complete (bool): Flag indicating if startup validation is complete
    """
    
    def __init__(self, name, command, log_file=None):
        """
        Initialize an OMEGA BTC AI system component.
        
        Args:
            name (str): Name of the component
            command (str): Command to start the component
            log_file (str, optional): Path to log file. If None, logs to console only.
        """
        self.name = name
        self.command = command
        self.process = None
        self.log_file = log_file
        self.log_fd = None
        self.cwd = PROJECT_ROOT
        self.env = os.environ.copy()
        self.restart_count = 0
        self.max_restarts = MAX_RESTART_ATTEMPTS
        self.is_optional = False
        self.status = 'stopped'
        self.last_restart = 0
        self.health_check_file = None
        self.health_check_method = None
        self.health_check_string = None
        self.health_check_port = None
        self.run_in_background = False
        self.startup_validation_timeout = 30  # seconds
        self.validation_complete = False

    def set_health_check(self, method=None, file=None, string=None, port=None):
        """
        Set health check parameters for this component.
        
        Args:
            method (function, optional): Custom health check function
            file (str, optional): File to check for existence
            string (str, optional): String to look for in the log file
            port (int, optional): Port to check for availability
        """
        self.health_check_method = method
        self.health_check_file = file
        self.health_check_string = string
        self.health_check_port = port
        
    def set_background_mode(self, background=False):
        """
        Set whether this component should run in background mode.
        
        Args:
            background (bool): True to run in background, False for foreground
        """
        self.run_in_background = background

    def start(self):
        """
        Start the component as a subprocess.
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        logger.info(f"Starting {self.name}...")
        self.status = 'starting'
        
        try:
            if self.log_file:
                # Create log directory if it doesn't exist
                log_dir = os.path.dirname(self.log_file)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                    
                # Open log file
                self.log_fd = open(self.log_file, 'w')
                
                if self.run_in_background:
                    # Run in background mode with output to log file
                    self.process = subprocess.Popen(
                        self.command,
                        cwd=self.cwd,
                        env=self.env,
                        shell=True,
                        stdout=self.log_fd,
                        stderr=self.log_fd,
                        text=True
                    )
                else:
                    # Run in foreground mode with output to both console and log file
                    self.process = subprocess.Popen(
                        self.command,
                        cwd=self.cwd,
                        env=self.env,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True
                    )
                    
                    # Start a thread to read output and write to both console and log file
                    def log_output():
                        if self.process and self.process.stdout:
                            for line in self.process.stdout:
                                sys.stdout.write(f"[{self.name}] {line}")
                                if self.log_fd:
                                    self.log_fd.write(line)
                                    self.log_fd.flush()
                    
                    threading.Thread(target=log_output, daemon=True).start()
            else:
                # No log file specified, output to console
                self.process = subprocess.Popen(
                    self.command,
                    cwd=self.cwd,
                    env=self.env,
                    shell=True,
                    text=True
                )
                
            logger.info(f"Started {self.name} (PID: {self.process.pid})")
            self.last_restart = time.time()
            self.status = 'running'
            
            # Start validation thread
            threading.Thread(target=self.validate_startup, daemon=True).start()
            
            return True
        except Exception as e:
            logger.error(f"Failed to start {self.name}: {str(e)}")
            self.status = 'failed'
            return False

    def validate_startup(self):
        """
        Validate that the component started successfully.
        
        This method runs in a separate thread and checks various indicators
        that the component is running correctly, based on the configured
        health check parameters.
        """
        start_time = time.time()
        
        while time.time() - start_time < self.startup_validation_timeout:
            # Check if process is still running
            if not self.is_running():
                logger.error(f"{self.name} failed to start - process terminated")
                self.status = 'failed'
                return False
            
            # Check health indicators
            health_status = self.check_health()
            
            if health_status:
                logger.info(f"{self.name} successfully validated")
                self.validation_complete = True
                self.status = 'running'
                return True
                
            time.sleep(1)
            
        logger.warning(f"{self.name} validation timed out after {self.startup_validation_timeout}s")
        # We don't mark as failed here, give it a chance to recover
        return False

    def check_health(self):
        """
        Check the health of the component.
        
        Returns:
            bool: True if the component is healthy, False otherwise
        """
        # Check if process is running
        if not self.is_running():
            return False
            
        # Call custom health check method if provided
        if self.health_check_method and not self.health_check_method(self):
            return False
            
        # Check if health check file exists
        if self.health_check_file and not os.path.exists(self.health_check_file):
            return False
            
        # Check if health check string is in log file
        if self.health_check_string and self.log_file:
            try:
                with open(self.log_file, 'r') as f:
                    if self.health_check_string not in f.read():
                        return False
            except Exception:
                return False
                
        # Check if port is available
        if self.health_check_port:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('127.0.0.1', self.health_check_port))
                sock.close()
                if result != 0:  # Port is not open
                    return False
            except Exception:
                return False
                
        return True

    def stop(self):
        """
        Stop the component process gracefully.
        
        Attempts to terminate the process gracefully with SIGTERM first,
        then forces termination with SIGKILL if necessary.
        """
        if self.process:
            try:
                logger.info(f"Stopping {self.name} (PID {self.process.pid})...")
                
                # First try SIGTERM
                self.process.terminate()
                
                # Give it 5 seconds to terminate gracefully
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if it didn't terminate
                    logger.warning(f"{self.name} did not terminate gracefully, forcing...")
                    self.process.kill()
                
                logger.info(f"{self.name} stopped")
                self.status = 'stopped'
            except Exception as e:
                logger.error(f"Error stopping {self.name}: {e}")
                
            # Close log file if open
            if self.log_fd:
                try:
                    self.log_fd.close()
                except Exception:
                    pass
                self.log_fd = None
                
            self.process = None
            self.validation_complete = False

    def is_running(self):
        """
        Check if the component process is still running.
        
        Returns:
            bool: True if the process is running, False otherwise
        """
        if not self.process:
            return False
            
        # Check if process is still running
        return self.process.poll() is None

    def monitor(self):
        """
        Monitor the component and restart it if it has crashed.
        
        Checks if the process is running and attempts to restart it if it has
        stopped unexpectedly, up to the maximum number of restart attempts.
        
        Returns:
            bool: True if a restart was attempted, False otherwise
        """
        if not self.is_running():
            if self.status == 'running':
                logger.warning(f"{self.name} is not running but status is 'running', updating status...")
                self.status = 'stopped'
                
            # Check if we should restart
            if self.restart_count < self.max_restarts:
                # Check if enough time has passed since last restart
                current_time = time.time()
                if current_time - self.last_restart >= RESTART_COOLDOWN:
                    logger.warning(f"{self.name} is not running, restarting... (attempt {self.restart_count + 1})")
                    self.restart_count += 1
                    self.start()
                    return True
                else:
                    logger.info(f"Waiting for cooldown before restarting {self.name}...")
            else:
                if self.status != 'failed':
                    logger.error(f"{self.name} has failed too many times, not restarting")
                    self.status = 'failed'
        else:
            # Component is running, check health
            if not self.check_health():
                logger.warning(f"{self.name} is running but not healthy, restarting...")
                self.stop()
                if self.restart_count < self.max_restarts:
                    self.restart_count += 1
                    self.start()
                    return True
                    
        return False

    def log_tail(self, lines=10):
        """
        Get the last N lines from the component's log file.
        
        Args:
            lines (int): Number of lines to return
            
        Returns:
            str: Last N lines from the log file
        """
        if not self.log_file or not os.path.exists(self.log_file):
            return "No log file available"
            
        try:
            with open(self.log_file, 'r') as f:
                # Use deque for efficiency when getting last N lines
                from collections import deque
                return "".join(deque(f, lines))
        except Exception as e:
            return f"Error reading log file: {str(e)}"

def init_components(args, running_processes=None):
    """
    Initialize the system components.
    
    Args:
        args: Command line arguments
        running_processes: Dictionary of processes that are already running
        
    Returns:
        List of OmegaComponent objects representing each component to start
    """
    # Paths defined in the configuration
    # Default list of components
    components = []
    
    # If running_processes is None, initialize it as an empty dict
    if running_processes is None:
        running_processes = {}
    
    # Helper function to check if a component is already running
    def is_component_running(keyword):
        for k in running_processes.keys():
            if keyword in k:
                return True
        return False
    
    # Add market trend analyzer if not disabled
    if not args.no_market_analyzer and not is_component_running("monitor_market_trends"):
        components.append(
            OmegaComponent(
                "Market Trends Monitor",
                "python -m omega_ai.monitor.monitor_market_trends",
                "logs/market_trend_analyzer.log"
            )
        )
    
    # Add Fibonacci dashboard connector if not disabled
    if not args.no_fibonacci and not is_component_running("fibonacci_dashboard_connector"):
        components.append(
            OmegaComponent(
                "Fibonacci Dashboard Connector",
                "python -m omega_ai.visualizer.backend.fibonacci_dashboard_connector",
                "logs/fibonacci_dashboard_connector.log"
            )
        )
    
    # Add live-api-server if not disabled
    if not args.no_live_api and not is_component_running("live-api-server"):
        components.append(
            OmegaComponent(
                "Live API Server",
                "cd omega_ai/visualizer/backend && python live-api-server.py",
                "logs/live_api_server.log"
            )
        )
    
    # Live feed for BTC price data
    if not is_component_running("live_btc_feed") and not is_component_running("btc_live_feed"):
        components.append(
            OmegaComponent(
                "BTC Live Feed",
                "python -m omega_ai.live_btc_feed",
                "logs/live_feed.log"
            )
        )
    
    # WebSocket server for real-time market data
    if not is_component_running("mm_websocket_server"):
        components.append(
            OmegaComponent(
                "WebSocket Server",
                "python -m omega_ai.mm_websocket_server",
                "logs/websocket_server.log"
            )
        )
    
    # Market maker trap event consumer
    if not is_component_running("mm_trap_consumer"):
        components.append(
            OmegaComponent(
                "MM Trap Consumer",
                "python -m omega_ai.mm_trap_consumer",
                "logs/trap_consumer.log"
            )
        )
    
    # Reggae Backend Dashboard Server
    if not args.no_backend and not is_component_running("reggae_dashboard_server"):
        components.append(
            OmegaComponent(
                "Reggae Backend Dashboard Server",
                "cd omega_ai/visualizer/backend && python -m reggae_dashboard_server",
                "logs/reggae_backend.log"
            )
        )
    
    # Reggae Dashboard UI
    if not args.no_reggae and not is_component_running("npm"):
        components.append(
            OmegaComponent(
                "Reggae Dashboard UI",
                "cd omega_ai/visualizer/frontend/reggae-dashboard && npm run dev",
                "logs/reggae_ui.log"
            )
        )
    
    return components

def cleanup_processes():
    """
    Clean up all processes on exit.
    
    Stops all running components in reverse order to ensure dependent
    components are stopped after their dependencies.
    """
    global running
    running = False
    
    logger.info("Shutting down OMEGA BTC AI system...")
    
    # Stop all components in reverse order
    for component in reversed(processes):
        component.stop()
    
    logger.info("All components stopped. Goodbye!")

def signal_handler(sig, frame):
    """
    Handle termination signals.
    
    Ensures clean shutdown when receiving signals like SIGINT (Ctrl+C)
    or SIGTERM (kill command).
    
    Args:
        sig: Signal number
        frame: Current stack frame
    """
    logger.info(f"Received signal {sig}, shutting down...")
    cleanup_processes()
    sys.exit(0)

def monitor_components():
    """
    Monitor all components and restart if needed.
    
    Runs in a background thread, periodically checking each component's
    status and restarting any that have stopped unexpectedly.
    """
    global running, AUTO_HEAL_ENABLED
    
    check_count = 0
    
    while running:
        all_healthy = True
        status_report = []
        
        for component in processes:
            # Check if component needs monitoring
            component_healthy = component.is_running() and component.check_health()
            
            # Auto-healing based on component health
            if not component_healthy:
                all_healthy = False
                if AUTO_HEAL_ENABLED:
                    logger.warning(f"{component.name} is unhealthy, attempting auto-healing...")
                    if component.monitor():
                        status_report.append(f"{component.name}: Restarted (attempt {component.restart_count})")
                    else:
                        status_report.append(f"{component.name}: Unhealthy - {component.status}")
                else:
                    # Just run the regular monitor method if auto-healing is not enabled
                    component.monitor()
                    status_report.append(f"{component.name}: {component.status}")
            else:
                status_report.append(f"{component.name}: Healthy")
        
        # Print periodic health status (every 6 checks = 30 seconds with 5 second interval)
        check_count += 1
        if check_count >= 6:
            check_count = 0
            
            logger.info("System Health Status:")
            for status in status_report:
                logger.info(f"  {status}")
            
            if all_healthy:
                logger.info("All components are healthy")
            else:
                if AUTO_HEAL_ENABLED:
                    logger.warning("Some components are unhealthy, auto-healing is active")
                else:
                    logger.warning("Some components are unhealthy")
        
        time.sleep(5)  # Check every 5 seconds

def kill_existing_processes(args):
    """
    Kill any existing OMEGA processes before starting.
    
    Scans the system for processes matching known OMEGA component names
    and terminates them to prevent conflicts.
    
    Args:
        args: Command line arguments with no_cleanup option
        
    Returns:
        int or dict: Number of processes killed or dictionary of running processes
    """
    logger.info("Checking for existing OMEGA processes...")
    
    # Keywords to identify OMEGA processes
    keywords = [
        "mm_websocket_server",
        "mm_trap_consumer", 
        "btc_live_feed",
        "live_btc_feed",
        "market_trends_monitor",
        "monitor_market_trends",
        "fibonacci_dashboard_connector",
        "trap_probability_meter",
        "live-api-server.py",
        "reggae_dashboard_server"
    ]
    
    killed = 0
    running_processes = {}
    
    # Iterate through all processes
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = " ".join(proc.info['cmdline'] if proc.info['cmdline'] else [])
            
            # Check if this is one of our processes
            for keyword in keywords:
                if keyword in cmdline:
                    # Don't kill ourselves
                    if proc.info['pid'] != os.getpid():
                        if args.no_cleanup:
                            # If no cleanup, just log the running process
                            logger.info(f"Found existing process: {proc.info['pid']} - {cmdline[:60]}")
                            # Store info about the running process
                            running_processes[keyword] = {
                                'pid': proc.info['pid'],
                                'cmdline': cmdline
                            }
                        else:
                            # Kill the process if cleanup is enabled
                            logger.info(f"Killing existing process: {proc.info['pid']} - {cmdline[:60]}...")
                            proc.kill()
                            killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if args.no_cleanup:
        logger.info(f"Found {len(running_processes)} existing processes (not killing due to --no-cleanup)")
        return running_processes
    
    if killed > 0:
        logger.info(f"Killed {killed} existing processes")
    else:
        logger.info("No existing processes found")
    
    # Give everything a moment to fully terminate
    time.sleep(2)
    
    return killed

def init_redis_client():
    """
    Initialize the Redis client connection.
    
    Attempts to connect to the Redis server with default settings.
    
    Returns:
        redis.Redis: Connected Redis client or None if connection failed
    """
    global redis_client
    
    try:
        # Check for .env.local file and load settings from it
        env_local_path = PROJECT_ROOT / '.env.local'
        if env_local_path.exists():
            # Parse .env.local file for Redis settings
            with open(env_local_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            # Set environment variables
                            os.environ[key.strip()] = value.strip()
            logger.info("Loaded Redis configuration from .env.local")
        
        # Get Redis connection parameters from environment variables
        redis_host = os.environ.get('REDIS_HOST', 'localhost')
        redis_port = int(os.environ.get('REDIS_PORT', 6379))
        redis_password = os.environ.get('REDIS_PASSWORD', '')
        
        # Only use password if it's not empty
        if redis_password:
            redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                decode_responses=True,
                socket_connect_timeout=5
            )
        else:
            redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                decode_responses=True,
                socket_connect_timeout=5
            )
        
        # Test connection
        redis_client.ping()
        logger.info(f"Connected to Redis at {redis_host}:{redis_port}")
        return redis_client
    except redis.RedisError as e:
        logger.error(f"Failed to connect to Redis: {str(e)}")
        redis_client = None
        return None

def check_redis_health():
    """
    Check if Redis connection is healthy.
    
    Returns:
        bool: True if Redis is connected and responding, False otherwise
    """
    global redis_client
    
    if not redis_client:
        return False
        
    try:
        # Try to ping Redis
        redis_client.ping()
        return True
    except redis.RedisError:
        return False

def heal_redis_connection():
    """
    Attempt to heal the Redis connection.
    
    Returns:
        bool: True if healing was successful, False otherwise
    """
    global redis_client
    
    logger.info("Attempting to heal Redis connection...")
    
    try:
        # Close existing connection if any
        if redis_client:
            try:
                redis_client.close()
            except Exception:
                pass
                
        # Try to reconnect
        return init_redis_client() is not None
    except Exception as e:
        logger.error(f"Failed to heal Redis connection: {str(e)}")
        return False
        
def check_and_heal_redis_data():
    """
    Check for common Redis data issues and fix them.
    
    This function checks for missing or corrupted keys and tries to repair them.
    
    Returns:
        bool: True if checks passed or issues were fixed, False otherwise
    """
    global redis_client
    
    if not check_redis_health():
        if not heal_redis_connection():
            logger.error("Failed to heal Redis connection")
            return False
    
    # If redis_client is still None after healing attempt, return False
    if redis_client is None:
        return False
    
    try:
        # Check for essential keys
        essential_keys = [
            'btc_price:last_btc_price',
            'current_position'
        ]
        
        for key in essential_keys:
            if not redis_client.exists(key):
                logger.warning(f"Essential Redis key missing: {key}")
                
                # Handle specific cases
                if key == 'btc_price:last_btc_price':
                    # Try to get price from a secondary source
                    try:
                        # Placeholder for actual price fetch logic
                        price = 50000.0  # Default placeholder
                        redis_client.set(key, str(price))
                        logger.info(f"Restored key {key} with value {price}")
                    except Exception as e:
                        logger.error(f"Failed to restore {key}: {str(e)}")
                        
                elif key == 'current_position':
                    # Create empty position data
                    default_position = {
                        "has_position": False,
                        "position_side": "none",
                        "entry_price": 0,
                        "current_price": 0,
                        "position_size": 0,
                        "pnl_percent": 0,
                        "pnl_usd": 0,
                        "timestamp": datetime.now().isoformat(),
                        "source": "system_recovery"
                    }
                    redis_client.set(key, json.dumps(default_position))
                    logger.info(f"Restored key {key} with default position data")
        
        return True
    except Exception as e:
        logger.error(f"Error checking/healing Redis data: {str(e)}")
        return False

def backup_logs():
    """
    Backup log files before starting the system.
    
    Creates timestamped backups of previous log files.
    """
    try:
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = LOG_DIR / f"backup_{timestamp}"
        
        # Only create backup if there are existing log files
        log_files = list(LOG_DIR.glob("*.log"))
        if log_files:
            os.makedirs(backup_dir, exist_ok=True)
            
            for log_file in log_files:
                if os.path.isfile(log_file):
                    shutil.copy2(log_file, backup_dir / log_file.name)
                    
            logger.info(f"Backed up {len(log_files)} log files to {backup_dir}")
    except Exception as e:
        logger.error(f"Failed to backup logs: {str(e)}")

def health_check_background():
    """
    Background thread for continuous health checking.
    
    This function runs in a background thread and periodically checks
    the health of all components and Redis, attempting to heal them if needed.
    """
    global running, processes
    
    logger.info("Starting health check background thread")
    
    while running:
        # Check Redis health
        if not check_redis_health():
            logger.warning("Redis connection unhealthy, attempting to heal...")
            heal_redis_connection()
        
        # Periodic Redis data validation
        if redis_client is not None:
            check_and_heal_redis_data()
            
        # Sleep for the health check interval
        time.sleep(HEALTH_CHECK_INTERVAL)
    
    logger.info("Health check background thread stopped")

def main():
    """
    Main entry point for the OMEGA BTC AI system.
    
    Parses command-line arguments, initializes components, and
    starts the system. Handles graceful shutdown on keyboard interrupt.
    
    Command-line arguments:
        --no-reggae: Don't start the Reggae Dashboard UI
        --no-backend: Don't start the Reggae Backend Dashboard Server
        --no-cleanup: Don't kill existing processes
        --no-fibonacci: Don't start the Fibonacci Dashboard Connector
        --no-market-analyzer: Don't start the Enhanced Market Trend Analyzer
        --no-live-api: Don't start the Live API Server
        --background: Run components in background mode
        --foreground: Run components in foreground mode (default)
        --auto-heal: Enable auto-healing for system components
        --ui-first: Start UI components first, then add other components
        
    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    global processes, running, AUTO_HEAL_ENABLED
    
    parser = argparse.ArgumentParser(description="OMEGA BTC AI System Launcher")
    parser.add_argument("--no-reggae", action="store_true", help="Don't start Reggae UI")
    parser.add_argument("--no-backend", action="store_true", help="Don't start Reggae Backend Server")
    parser.add_argument("--no-cleanup", action="store_true", help="Don't kill existing processes")
    parser.add_argument("--no-fibonacci", action="store_true", help="Don't start the Fibonacci Dashboard Connector")
    parser.add_argument("--no-market-analyzer", action="store_true", help="Don't start the Enhanced Market Trend Analyzer")
    parser.add_argument("--no-live-api", action="store_true", help="Don't start the Live API Server")
    parser.add_argument("--background", action="store_true", help="Run components in background mode")
    parser.add_argument("--foreground", action="store_true", help="Run components in foreground mode (default)")
    parser.add_argument("--auto-heal", action="store_true", help="Enable auto-healing for system components")
    parser.add_argument("--ui-first", action="store_true", help="Start UI components first, then add other components")
    args = parser.parse_args()
    
    # Display banner
    print("\n" + "=" * 80)
    print("                     OMEGA BTC AI SYSTEM LAUNCHER                      ")
    print("=" * 80 + "\n")
    
    # Set background mode
    run_in_background = args.background and not args.foreground
    
    # Set auto-healing mode
    AUTO_HEAL_ENABLED = args.auto_heal
    if AUTO_HEAL_ENABLED:
        logger.info("Auto-healing mode enabled")
    
    # Register signal handlers and cleanup
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    atexit.register(cleanup_processes)
    
    # Backup existing logs
    logger.info("Backing up existing log files...")
    backup_logs()
    
    # Kill existing processes or identify running ones
    running_processes = {}
    if not args.no_cleanup:
        kill_existing_processes(args)
    else:
        running_processes = kill_existing_processes(args)
    
    # Initialize Redis connection
    logger.info("Initializing Redis connection...")
    if init_redis_client():
        logger.info("Redis connection established")
        if AUTO_HEAL_ENABLED:
            # Run initial Redis data check and healing
            if check_and_heal_redis_data():
                logger.info("Redis data validated and healed if needed")
            else:
                logger.warning("Redis data validation failed")
    else:
        logger.warning("Failed to connect to Redis - some features may not work correctly")
    
    # Initialize components
    logger.info("Initializing system components...")
    processes = init_components(args, running_processes)
    
    # Set background mode for all components
    for component in processes:
        component.set_background_mode(run_in_background)
        
        # Set health checks based on component type
        if component.name == "WebSocket Server":
            component.set_health_check(port=8765, string="WebSocket server started")
        elif component.name == "Reggae Backend Dashboard Server":
            component.set_health_check(port=8000, string="Uvicorn running")
        elif component.name == "Reggae Dashboard UI":
            component.set_health_check(port=5001, string="Compiled successfully")
    
    # Start components in the right order based on ui-first flag
    ui_components = [c for c in processes if "UI" in c.name or "Dashboard" in c.name]
    non_ui_components = [c for c in processes if c not in ui_components]
    
    components_to_start = ui_components + non_ui_components if args.ui_first else processes
    
    # Start all components
    logger.info("Starting system components...")
    for component in components_to_start:
        success = component.start()
        if not success and not component.is_optional:
            logger.error(f"Failed to start {component.name}, aborting startup")
            cleanup_processes()
            sys.exit(1)
        time.sleep(1)  # Small delay between component starts
    
    logger.info("All components started successfully!")
    print("\n" + "=" * 80)
    print("               OMEGA BTC AI SYSTEM RUNNING                ")
    print("=" * 80 + "\n")
    
    # Print access instructions
    print("Access Points:")
    print("  Reggae Frontend Dashboard: http://localhost:5001/")
    print("  Reggae Backend Dashboard: http://localhost:8000/")
    print("  WebSocket Server: ws://localhost:8765/")
    print("  Enhanced Market Analyzer: Check logs/market_trend_analyzer.log")
    print("  Fibonacci Dashboard: Check logs/fibonacci_dashboard_connector.log")
    print("\n" + "=" * 80)
    
    # Start health check thread if auto-healing is enabled
    if AUTO_HEAL_ENABLED:
        logger.info("Starting auto-healing health check thread...")
        health_thread = threading.Thread(target=health_check_background, daemon=True)
        health_thread.start()
    
    # Monitor components in a separate thread
    logger.info("Starting component monitor thread...")
    monitor_thread = threading.Thread(target=monitor_components)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # Keep the main thread alive
    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down...")
        cleanup_processes()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 