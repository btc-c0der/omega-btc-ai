#!/usr/bin/env python3

"""
OMEGA GRID PORTAL - Simple Launcher
==================================

A simplified launcher for the OMEGA Bot Farm management tools.
Helps manage and visualize different bots in the ecosystem.

Copyright (c) 2024 OMEGA BTC AI
Licensed under GBU2 License
"""

import os
import sys
import time
import webbrowser
import subprocess
from datetime import datetime
from pathlib import Path
import psutil
import random
import json
import argparse

# ANSI Colors for terminal output
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
GOLD = "\033[38;5;220m"

# Function to check if Redis is running
def check_redis_running():
    """Check if Redis server is running."""
    try:
        redis_output = subprocess.run(["redis-cli", "ping"], 
                                     capture_output=True, text=True, timeout=1)
        return "PONG" in redis_output.stdout
    except:
        return False

# Get script directory and project root
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent

def display_banner():
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
                                                                   
{GOLD}{BOLD}          🌟  \"ALL-IN-ONE BOT MANAGEMENT TOOL\"  🌟{RESET}
{GREEN}          \"GRID SIDE\" — 5D UI Dashboard for \"OMEGA BOT FARM\"{RESET}
{CYAN}          \"c/o OFF—WHITE™\" for \"OMEGA\", 2025{RESET}
"""
    print(banner)

def display_loading_animation():
    """Display a loading animation"""
    states = ["⚛️", "🔄", "🧬", "🔮", "✨"]
    print(f"{CYAN}\"INITIALIZING QUANTUM PORTAL...\"   \"LOADING STATE\"{RESET}")
    for i in range(10):
        state = states[i % len(states)]
        sys.stdout.write(f"\r{state} \"LOADING: {i*10}%\"   \"PROGRESS\" {state}")
        sys.stdout.flush()
        time.sleep(0.2)
    print(f"\n{GREEN}\"SYSTEM READY!\"   \"ACTIVATION COMPLETE\"{RESET}")

def show_menu():
    """Show the menu options to the user"""
    print("\nOMEGA Grid Portal - Simple Menu\n")
    print("1. View the system status")
    print("2. Launch Discord bot")  
    print("3. Show Discord bot info")
    print("4. Launch Matrix Dashboard")
    print("5. Launch CCXT Strategic Trader")
    print("6. Show available parameters")
    print("7. Launch Web Dashboard")
    print("8. Get Bitget positions info")
    print("9. Launch Cybernetic Quantum Bloom")
    print("10. Run Test Runner")
    print("11. Launch Garvey Wisdom Portal")
    print("12. Connect to Online Redis")
    print("13. Launch BTC Velocity Monitor")
    print("14. Launch AIXBT Live Feed")
    print("0. Exit")
    return input("\nEnter your choice (0-14): ")

def launch_matrix_dashboard():
    """Launch the Matrix-style terminal dashboard"""
    print(f"{MAGENTA}{BOLD}Launching Matrix Terminal Dashboard...{RESET}")
    matrix_path = os.path.join(PROJECT_ROOT, "src/omega_bot_farm/matrix_cli_live_positions.py")
    
    if not os.path.exists(matrix_path):
        fallback_path = os.path.join(PROJECT_ROOT, "src/omega_bot_farm/bitget_matrix_cli_b0t.py")
        if os.path.exists(fallback_path):
            matrix_path = fallback_path
        else:
            print(f"{RED}Matrix dashboard not found!{RESET}")
            return False
    
    try:
        subprocess.Popen([sys.executable, matrix_path])
        print(f"{GREEN}Matrix dashboard launched!{RESET}")
        return True
    except Exception as e:
        print(f"{RED}Error launching Matrix dashboard: {e}{RESET}")
        return False

def launch_web_dashboard():
    """Launch the web-based dashboard"""
    print(f"{GREEN}{BOLD}Launching Web Dashboard...{RESET}")
    
    # Try Reggae dashboard first
    reggae_path = os.path.join(PROJECT_ROOT, "omega_ai/visualizer/frontend/reggae-dashboard/live-api-server.py")
    if os.path.exists(reggae_path):
        try:
            subprocess.Popen([sys.executable, reggae_path])
            print(f"{GREEN}Reggae dashboard launched at http://localhost:5000{RESET}")
            time.sleep(2)
            webbrowser.open("http://localhost:5000")
            return True
        except Exception as e:
            print(f"{RED}Error launching Reggae dashboard: {e}{RESET}")
    
    # Try Rasta dashboard as fallback
    rasta_path = os.path.join(PROJECT_ROOT, "omega_ai/run_dashboard.py")
    if os.path.exists(rasta_path):
        try:
            subprocess.Popen([sys.executable, rasta_path])
            print(f"{GREEN}Rasta dashboard launched at http://localhost:8501{RESET}")
            time.sleep(2)
            webbrowser.open("http://localhost:8501")
            return True
        except Exception as e:
            print(f"{RED}Error launching Rasta dashboard: {e}{RESET}")
    
    print(f"{RED}No dashboard found! Please make sure dashboards are installed.{RESET}")
    return False

def launch_discord_bot():
    """Launch the Discord bot"""
    print(f"{CYAN}{BOLD}Launching Discord Bot...{RESET}")
    bot_path = os.path.join(PROJECT_ROOT, "src/omega_bot_farm/discord/bot.py")
    
    if not os.path.exists(bot_path):
        print(f"{RED}Discord bot not found!{RESET}")
        return False
    
    try:
        subprocess.Popen([sys.executable, bot_path])
        print(f"{GREEN}Discord bot launched!{RESET}")
        return True
    except Exception as e:
        print(f"{RED}Error launching Discord bot: {e}{RESET}")
        return False

def view_bitget_positions():
    """View BitGet positions"""
    print(f"{CYAN}{BOLD}Fetching BitGet Positions...{RESET}")
    positions_path = os.path.join(PROJECT_ROOT, "src/omega_bot_farm/bitget_positions_info.py")
    
    if not os.path.exists(positions_path):
        print(f"{RED}BitGet positions info script not found!{RESET}")
        return False
    
    try:
        result = subprocess.run([sys.executable, positions_path], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"{RED}Errors:{RESET}\n{result.stderr}")
        return True
    except Exception as e:
        print(f"{RED}Error fetching BitGet positions: {e}{RESET}")
        return False

def show_system_status():
    """Show system status with Virgil Abloh design aesthetics"""
    print(f"\n{CYAN}{BOLD}\"OMEGA GRID SYSTEM STATUS\"{RESET}")
    print(f"{GOLD}{'=' * 58}{RESET}")
    print(f"{CYAN}\"TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\"{RESET}")
    print(f"{GOLD}{'=' * 58}{RESET}")
    
    # Add grid coordinate system
    print(f"{YELLOW}\"GRID\"     \"X: 23.7516\"     \"Y: 42.1893\"     \"Z: 19.3721\"{RESET}")
    print(f"{YELLOW}\"SIDE\"     \"QUANTUM ALIGNED\"     \"DENSITY: 87.3%\"{RESET}")
    print(f"{GOLD}{'—' * 58}{RESET}")
    
    # Check for running bots
    bots = [
        {"name": "Discord Bot", "path": "bot.py", "emoji": "🤖"},
        {"name": "Matrix CLI", "path": "matrix_cli_live_positions.py", "emoji": "🧮"},
        {"name": "BitGet Position Analyzer", "path": "bitget_position_analyzer_b0t.py", "emoji": "📊"},
    ]
    
    # Check running processes
    running_procs = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info['cmdline'] or [])
            for bot in bots:
                if bot['path'] in cmdline and 'python' in cmdline.lower():
                    running_procs.append(bot['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # "ACTIVE BOTS" section
    print(f"\n{CYAN}\"ACTIVE BOTS\"   \"STATUS: RUNNING\"{RESET}")
    if running_procs:
        for bot_name in running_procs:
            matching_bot = next((b for b in bots if b['name'] == bot_name), None)
            if matching_bot:
                print(f"  {GREEN}• {matching_bot['emoji']} \"{matching_bot['name'].upper()}\"   \"ACTIVE\"{RESET}")
    else:
        print(f"  {YELLOW}\"NO ACTIVE BOTS\"   \"STATUS: PENDING\"{RESET}")
    
    # "INACTIVE BOTS" section
    print(f"\n{CYAN}\"INACTIVE BOTS\"   \"STATUS: STANDBY\"{RESET}")
    inactive_bots = [b for b in bots if b['name'] not in running_procs]
    if inactive_bots:
        for bot in inactive_bots:
            print(f"  {RED}• {bot['emoji']} \"{bot['name'].upper()}\"   \"INACTIVE\"{RESET}")
    else:
        print(f"  {GREEN}\"ALL BOTS ARE ACTIVE\"   \"STATUS: OPTIMAL\"{RESET}")
    
    # "REDIS" status
    print(f"\n{CYAN}\"SERVICES\"   \"INFRASTRUCTURE\"{RESET}")
    redis_status = "ONLINE" if check_redis_running() else "OFFLINE"
    status_color = GREEN if redis_status == "ONLINE" else RED
    print(f"  {status_color}• 💾 \"REDIS\"   \"{redis_status}\"   \"MEMORY: AVAILABLE\"{RESET}")
    
    # "DISCORD BOT INFORMATION" section
    print(f"\n{CYAN}\"DISCORD BOT INFORMATION\"   \"COMMUNICATION LAYER\"{RESET}")
    
    # Load Discord bot info from environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Main Discord Bot
    main_bot_token = os.getenv("DISCORD_BOT_TOKEN", "Not configured")
    main_bot_id = os.getenv("DISCORD_APP_ID", "Not configured")
    main_bot_guild_id = os.getenv("DISCORD_GUILD_ID", "Not configured")
    
    # CyBer1t4L QA Bot
    cyber_bot_id = os.getenv("CYBER1T4L_APP_ID", "Not configured")
    cyber_bot_key = os.getenv("CYBER1T4L_PUBLIC_KEY", "Not configured")
    
    # T3CH D3BT V001D3R Bot
    tech_debt_bot_id = os.getenv("TECH_DEBT_APP_ID", "Not configured")
    tech_debt_bot_permissions = os.getenv("TECH_DEBT_PERMISSIONS", "Not configured")
    
    # Display in Virgil style
    print(f"  {GOLD}\"MAIN DISCORD BOT\"   \"PRIMARY INTERFACE\"{RESET}")
    print(f"  — \"APP ID\":         \"{main_bot_id}\"")
    print(f"  — \"GUILD ID\":       \"{main_bot_guild_id}\"   \"SERVER\"")
    print(f"  — \"TOKEN STATUS\":   {'\"CONFIGURED\"' if len(main_bot_token) > 20 else '\"NOT CONFIGURED\"'}   \"SECURITY LAYER\"")
    
    print(f"\n  {GOLD}\"CYBER1T4L QA BOT\"   \"TESTING INTERFACE\"{RESET}")
    print(f"  — \"APP ID\":         \"{cyber_bot_id}\"")
    key_display = cyber_bot_key[:10] + "..." if len(cyber_bot_key) > 10 else cyber_bot_key
    print(f"  — \"PUBLIC KEY\":     \"{key_display}\"   \"VERIFICATION\"")
    
    print(f"\n  {GOLD}\"T3CH D3BT V001D3R BOT\"   \"MAINTENANCE INTERFACE\"{RESET}")
    print(f"  — \"APP ID\":         \"{tech_debt_bot_id}\"")
    print(f"  — \"PERMISSIONS\":    \"{tech_debt_bot_permissions}\"   \"ACCESS CONTROL\"")
    
    # "AVAILABLE COMMAND-LINE PARAMETERS" section
    print(f"\n{CYAN}\"AVAILABLE COMMAND-LINE PARAMETERS\"   \"GRID SIDE CONTROLS\"{RESET}")
    print(f"  {GREEN}\"--status\"{RESET}                \"DISPLAY THIS SYSTEM STATUS\"")
    print(f"  {GREEN}\"--matrix\"{RESET}                \"LAUNCH MATRIX DASHBOARD\"")
    print(f"  {GREEN}\"--web\"{RESET}                   \"LAUNCH WEB DASHBOARD\"")
    print(f"  {GREEN}\"--discord\"{RESET}               \"LAUNCH DISCORD BOT\"")
    print(f"  {GREEN}\"--positions\"{RESET}             \"VIEW BITGET POSITIONS\"")
    print(f"  {GREEN}\"--strategic\"{RESET}             \"LAUNCH STRATEGIC TRADER\"")
    print(f"  {GREEN}\"--quantum\"{RESET}               \"LAUNCH QUANTUM BLOOM\"")
    print(f"  {GREEN}\"--solomon\"{RESET}               \"OPEN KING SOLOMON'S PORTAL\"")
    print(f"  {GREEN}\"--velocity\"{RESET}              Launch BTC Velocity Monitor")
    
    # Virgil-inspired footer
    print(f"\n{GOLD}{'=' * 58}{RESET}")
    print(f"{CYAN}\"THE SYSTEM IS YOURS\"   c/o \"OMEGA GRID\"   \"FOR TRAINING PURPOSES\"{RESET}")
    print(f"{GOLD}{'=' * 58}{RESET}")
    
    # Add wisdom quote in Virgil style
    quotes = [
        f"{CYAN}\"THE MARKET WILL TEST YOU\"   \"TRADING WISDOM\"{RESET}",
        f"{CYAN}\"TRADING IS SIMPLY INFORMATION EXCHANGE\"   \"FINANCIAL PHYSICS\"{RESET}",
        f"{CYAN}\"POSITIONS ARE JUST TEMPORARY STATES\"   \"QUANTUM VIEW\"{RESET}",
        f"{CYAN}\"A LOSS IS ONLY A LESSON\"   \"GRID SIDE EDUCATION\"{RESET}",
        f"{CYAN}\"RISK IS THE TAX PAID FOR OPPORTUNITY\"   \"MATHEMATICAL TRUTH\"{RESET}",
        f"{CYAN}\"PATIENCE IS THE ULTIMATE EDGE\"   \"TIME ADVANTAGE\"{RESET}",
        f"{CYAN}\"THE TREND IS YOUR \"FRIEND\"\"   \"MARKET DYNAMIC\"{RESET}",
        f"{CYAN}\"TECHNICAL ANALYSIS IS \"POETRY\"\"   \"PRICE COMMUNICATION\"{RESET}",
        f"{CYAN}\"BUY THE \"DIP\"\"   \"STRATEGIC ENTRY\"{RESET}",
        f"{CYAN}\"SELL THE \"NEWS\"\"   \"INFORMATION ARBITRAGE\"{RESET}"
    ]
    
    selected_quote = random.choice(quotes)
    print(f"\n{selected_quote}")
    print(f"{MAGENTA}\"c/o OMEGA GRID\"   \"EST. 2025\"   \"OFF—GRID™ FOR TRAINING\"{RESET}")
    print(f"{YELLOW}\"LOT: 23.7516\"   \"MADE IN DIGITAL SPACE\"   \"NOT FOR PUBLIC USE\"{RESET}")

def launch_strategic_trader():
    """Launch the CCXT Strategic Trader"""
    print(f"{CYAN}{BOLD}Launching CCXT Strategic Trader...{RESET}")
    trader_path = os.path.join(PROJECT_ROOT, "src/omega_bot_farm/trading/b0ts/ccxt/ccxt_strategic_trader.py")
    
    if not os.path.exists(trader_path):
        print(f"{RED}CCXT Strategic Trader not found!{RESET}")
        return False
    
    try:
        subprocess.Popen([sys.executable, trader_path])
        print(f"{GREEN}CCXT Strategic Trader launched!{RESET}")
        return True
    except Exception as e:
        print(f"{RED}Error launching CCXT Strategic Trader: {e}{RESET}")
        return False

def launch_cybernetic_quantum_bloom():
    """Launch the Cybernetic Quantum Bloom"""
    print(f"{CYAN}{BOLD}Launching Cybernetic Quantum Bloom...{RESET}")
    bloom_path = os.path.join(PROJECT_ROOT, "src/omega_bot_farm/cybernetic_quantum_bloom.py")
    
    if not os.path.exists(bloom_path):
        print(f"{RED}Cybernetic Quantum Bloom script not found!{RESET}")
        return False
    
    try:
        subprocess.Popen([sys.executable, bloom_path])
        print(f"{GREEN}Cybernetic Quantum Bloom launched!{RESET}")
        return True
    except Exception as e:
        print(f"{RED}Error launching Cybernetic Quantum Bloom: {e}{RESET}")
        return False

def run_test_runner():
    """Run the Quantum Test Runner"""
    print(f"{CYAN}{BOLD}Launching Quantum Test Runner...{RESET}")
    test_runner_path = os.path.join(PROJECT_ROOT, "src/omega_bot_farm/qa/run_test_runner.py")
    
    if not os.path.exists(test_runner_path):
        print(f"{RED}Quantum Test Runner script not found!{RESET}")
        return False
    
    try:
        print(f"{YELLOW}Initializing Quantum Test Runner...{RESET}")
        
        # Ask user for which test dimensions to run
        print(f"{CYAN}Available test dimensions:{RESET}")
        print(f"{GOLD}1. {RESET}UNIT - Unit tests")
        print(f"{GOLD}2. {RESET}INTEGRATION - Integration tests")
        print(f"{GOLD}3. {RESET}PERFORMANCE - Performance tests")
        print(f"{GOLD}4. {RESET}SECURITY - Security tests")
        print(f"{GOLD}5. {RESET}COMPLIANCE - Compliance tests")
        print(f"{GOLD}0. {RESET}ALL - Run all test dimensions")
        
        choice = input(f"\n{BOLD}Enter your choice (0-5) or press Enter for ALL: {RESET}")
        
        cmd = [sys.executable, test_runner_path, "--run-tests"]
        
        if choice == "1":
            cmd.append("UNIT")
        elif choice == "2":
            cmd.append("INTEGRATION")
        elif choice == "3":
            cmd.append("PERFORMANCE")
        elif choice == "4":
            cmd.append("SECURITY")
        elif choice == "5":
            cmd.append("COMPLIANCE")
        # If choice is 0 or empty, run all dimensions (default)
        
        # Add fancy visuals and celebration options
        cmd.append("--fancy-visuals")
        cmd.append("--celebration")
        
        result = subprocess.run(cmd, text=True)
        
        if result.returncode == 0:
            print(f"{GREEN}Test runner completed successfully!{RESET}")
            return True
        else:
            print(f"{RED}Test runner encountered issues.{RESET}")
            return False
    except Exception as e:
        print(f"{RED}Error running Quantum Test Runner: {e}{RESET}")
        return False

def invoke_virgil_abloh_celebration():
    """Invoke Virgil Abloh's design celebration"""
    print(f"{CYAN}{BOLD}Invoking Virgil Abloh Celebration...{RESET}")
    portal_path = os.path.join(SCRIPT_DIR, "omega_grid_portal.py")
    
    if not os.path.exists(portal_path):
        print(f"{RED}Portal script not found!{RESET}")
        return False
    
    try:
        subprocess.call([sys.executable, portal_path, "--virgil"])
        print(f"{GREEN}Celebration complete. Returning to main menu...{RESET}")
        return True
    except Exception as e:
        print(f"{RED}Error during celebration: {e}{RESET}")
        return False

def launch_garvey_portal():
    """Launch the Garvey Wisdom Portal"""
    print("Launching the Garvey Wisdom Portal...")
    
    portal_dir = "omega_ai/garvey_portal"
    portal_file = os.path.join(portal_dir, "portal.py")
    
    if not os.path.exists(portal_file):
        print(f"{RED}Garvey Portal not found at {portal_file}. Please check the repository structure.{RESET}")
        return False

    # Create data directory if it doesn't exist
    os.makedirs(os.path.join(portal_dir, "data"), exist_ok=True)
    
    try:
        # Try to use streamlit from the path
        streamlit_path = "streamlit"
        try:
            subprocess.Popen([streamlit_path, "run", portal_file], stderr=subprocess.PIPE)
            print(f"{GREEN}Garvey Portal launched successfully!{RESET}")
            print(f"{YELLOW}Opening browser to http://localhost:8501{RESET}")
            # Open browser
            time.sleep(2)
            subprocess.Popen(["open", "http://localhost:8501"])
        except FileNotFoundError:
            # If streamlit is not in the PATH, try as a module
            print(f"{YELLOW}Streamlit not found in PATH. Trying as a module...{RESET}")
            subprocess.Popen([sys.executable, "-m", "streamlit", "run", portal_file])
            print(f"{GREEN}Garvey Portal launched successfully!{RESET}")
            print(f"{YELLOW}Opening browser to http://localhost:8501{RESET}")
            # Open browser
            time.sleep(2)
            subprocess.Popen(["open", "http://localhost:8501"])
    except Exception as e:
        print(f"{RED}Failed to launch Garvey Portal: {e}{RESET}")
        return False
    
    return True

def connect_online_redis():
    """Connect to the online Redis instance"""
    print(f"{MAGENTA}{BOLD}Connecting to online Redis...{RESET}")
    
    # Define the Redis connection details
    redis_host = "omega-btc-ai-redis-do-user-20389918-0.d.db.ondigitalocean.com"
    redis_port = 25061
    redis_username = "default"
    redis_password = "AVNS_OXMpU0P0ByYEz337Fgi"
    
    try:
        # Check if Redis module is available
        try:
            import redis
        except ImportError:
            print(f"{YELLOW}Installing Redis module...{RESET}")
            subprocess.run([sys.executable, "-m", "pip", "install", "redis"], check=True)
            import redis
        
        print(f"{CYAN}Establishing connection to Digital Ocean Redis...{RESET}")
        print(f"{YELLOW}Host: {redis_host}, Port: {redis_port}{RESET}")
        
        # Create the connection
        r = redis.Redis(
            host=redis_host,
            port=redis_port,
            username=redis_username,
            password=redis_password,
            ssl=True,
            socket_connect_timeout=5.0
        )
        
        # Test the connection with a ping
        result = r.ping()
        
        if result:
            print(f"{GREEN}Connection successful! Redis responded: {result}{RESET}")
            
            # Display some Redis info
            info = r.info()
            print(f"\n{CYAN}Redis Server Information:{RESET}")
            print(f"{GOLD}{'—' * 40}{RESET}")
            print(f"  {YELLOW}Version:           {info.get('redis_version', 'Unknown')}{RESET}")
            print(f"  {YELLOW}Uptime:            {info.get('uptime_in_days', 0)} days{RESET}")
            print(f"  {YELLOW}Connected clients: {info.get('connected_clients', 0)}{RESET}")
            print(f"  {YELLOW}Memory used:       {info.get('used_memory_human', 'Unknown')}{RESET}")
            print(f"  {YELLOW}Total keys:        {sum(info.get(f'db{i}', {}).get('keys', 0) for i in range(16) if f'db{i}' in info)}{RESET}")
            print(f"{GOLD}{'—' * 40}{RESET}")
            
            # Set a test key to demonstrate functionality
            test_key = "simple_portal_test"
            test_value = f"Connected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Simple Portal"
            r.set(test_key, test_value)
            print(f"\n{GREEN}Test key set: {test_key} = {test_value}{RESET}")
            
            # Get some existing keys to show
            print(f"\n{CYAN}Sample keys in database (limited to 10):{RESET}")
            keys = r.keys("*")[:10]  # Limit to 10 keys
            if keys:
                for key in keys:
                    key_str = key.decode('utf-8') if isinstance(key, bytes) else key
                    try:
                        value = r.get(key_str)
                        value_str = value.decode('utf-8') if isinstance(value, bytes) else str(value)
                        if len(value_str) > 50:
                            value_str = value_str[:47] + "..."
                        print(f"  {BLUE}{key_str}:{RESET} {YELLOW}{value_str}{RESET}")
                    except:
                        print(f"  {BLUE}{key_str}:{RESET} {RED}[BINARY DATA]{RESET}")
            else:
                print(f"  {YELLOW}No keys found in database{RESET}")
            
            return True
        else:
            print(f"{RED}Connection failed! No response from Redis.{RESET}")
            return False
    except Exception as e:
        print(f"{RED}Connection error: {str(e)}{RESET}")
        print(f"\n{YELLOW}Troubleshooting tips:{RESET}")
        print(f"  {CYAN}1. Check network connectivity and firewall settings{RESET}")
        print(f"  {CYAN}2. Verify your credentials (username/password){RESET}")
        print(f"  {CYAN}3. Ensure SSL support (requires TLS connection){RESET}")
        print(f"  {CYAN}4. Contact administrator if issues persist{RESET}")
        return False

def launch_btc_velocity_monitor():
    """Launch the BTC velocity monitor"""
    print(f"{CYAN}{BOLD}Launching BTC Velocity Monitor...{RESET}")
    monitor_path = os.path.join(PROJECT_ROOT, "src/omega_bot_farm/btc_velocity_monitor.py")
    
    if not os.path.exists(monitor_path):
        print(f"{RED}BTC Velocity Monitor not found!{RESET}")
        return False
    
    try:
        # Ensure dependencies are installed
        try:
            import pandas
            import numpy
            import colorama
        except ImportError:
            print(f"{YELLOW}Installing dependencies...{RESET}")
            subprocess.run([sys.executable, "-m", "pip", "install", "pandas", "numpy", "colorama", "python-dateutil"], check=True)
        
        # Launch the monitor
        print(f"{CYAN}Starting BTC velocity analysis...{RESET}")
        subprocess.Popen([sys.executable, monitor_path])
        
        print(f"{GREEN}BTC Velocity Monitor launched successfully!{RESET}")
        return True
    except Exception as e:
        print(f"{RED}Error launching BTC Velocity Monitor: {e}{RESET}")
        return False

def launch_aixbt_live_feed():
    """Launch the AIXBT live feed"""
    print(f"{CYAN}{BOLD}Launching AIXBT Live Feed...{RESET}")
    monitor_path = os.path.join(PROJECT_ROOT, "src/omega_bot_farm/aixbt_live_feed_v1.py")
    
    if not os.path.exists(monitor_path):
        print(f"{RED}AIXBT Live Feed not found!{RESET}")
        return False
    
    try:
        # Ensure dependencies are installed
        try:
            import pandas
            import numpy
            import colorama
            import websockets
        except ImportError:
            print(f"{YELLOW}Installing dependencies...{RESET}")
            subprocess.run([sys.executable, "-m", "pip", "install", "pandas", "numpy", "colorama", "python-dateutil", "websockets"], check=True)
        
        # Launch the monitor
        print(f"{CYAN}Starting AIXBT correlation analysis...{RESET}")
        subprocess.Popen([sys.executable, monitor_path])
        
        print(f"{GREEN}AIXBT Live Feed launched successfully!{RESET}")
        return True
    except Exception as e:
        print(f"{RED}Error launching AIXBT Live Feed: {e}{RESET}")
        return False

def show_available_parameters():
    """Show all available command-line parameters"""
    print(f"\n{CYAN}{BOLD}Available Command-line Parameters:{RESET}")
    print(f"{GOLD}{'—' * 50}{RESET}")
    print(f"  {YELLOW}--status{RESET}      Show system status")
    print(f"  {YELLOW}--bot{RESET}         Launch Discord bot")
    print(f"  {YELLOW}--bot-info{RESET}    Show Discord bot information")
    print(f"  {YELLOW}--matrix{RESET}      Launch Matrix Dashboard")
    print(f"  {YELLOW}--trader{RESET}      Launch CCXT Strategic Trader")
    print(f"  {YELLOW}--web{RESET}         Launch Web Dashboard")
    print(f"  {YELLOW}--positions{RESET}   Get Bitget positions info")
    print(f"  {YELLOW}--quantum{RESET}     Launch Cybernetic Quantum Bloom")
    print(f"  {YELLOW}--test{RESET}        Run Test Runner")
    print(f"  {YELLOW}--garvey{RESET}      Launch Garvey Wisdom Portal")
    print(f"  {YELLOW}--redis{RESET}       Connect to Online Redis")
    print(f"  {YELLOW}--velocity{RESET}    Launch BTC Velocity Monitor")
    print(f"  {YELLOW}--aixbt{RESET}       Launch AIXBT Live Feed")
    print(f"{GOLD}{'—' * 50}{RESET}")
    
    return True

def show_discord_bot_info():
    """Show information about the Discord bot from the configuration"""
    # This function is not provided in the original file or the new code block
    # It's assumed to exist as it's called in the show_menu function
    pass

def main():
    parser = argparse.ArgumentParser(description="OMEGA Grid Portal - Simple Launcher")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--bot", action="store_true", help="Launch Discord bot")
    parser.add_argument("--bot-info", action="store_true", help="Show Discord bot information")
    parser.add_argument("--matrix", action="store_true", help="Launch Matrix Dashboard")
    parser.add_argument("--trader", action="store_true", help="Launch CCXT Strategic Trader")
    parser.add_argument("--web", action="store_true", help="Launch Web Dashboard")
    parser.add_argument("--positions", action="store_true", help="Get Bitget positions info")
    parser.add_argument("--quantum", action="store_true", help="Launch Cybernetic Quantum Bloom")
    parser.add_argument("--test", action="store_true", help="Run Test Runner")
    parser.add_argument("--garvey", action="store_true", help="Launch Garvey Wisdom Portal")
    parser.add_argument("--redis", action="store_true", help="Connect to Online Redis")
    parser.add_argument("--velocity", action="store_true", help="Launch BTC Velocity Monitor")
    parser.add_argument("--aixbt", action="store_true", help="Launch AIXBT Live Feed")
    
    args = parser.parse_args()
    
    # Clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"{GOLD}{BOLD}OMEGA Grid Portal - Simple Launcher{RESET}")
    print(f"{YELLOW}Initializing...{RESET}")
    
    if args.status:
        show_system_status()
        return
    elif args.bot:
        launch_discord_bot()
        return
    elif args.bot_info:
        show_discord_bot_info()
        return
    elif args.matrix:
        launch_matrix_dashboard()
        return
    elif args.trader:
        launch_strategic_trader()
        return
    elif args.web:
        launch_web_dashboard()
        return
    elif args.positions:
        view_bitget_positions()
        return
    elif args.quantum:
        launch_cybernetic_quantum_bloom()
        return
    elif args.test:
        run_test_runner()
        return
    elif args.garvey:
        launch_garvey_portal()
        return
    elif args.redis:
        connect_online_redis()
        return
    elif args.velocity:
        launch_btc_velocity_monitor()
        return
    elif args.aixbt:
        launch_aixbt_live_feed()
        return
    
    # Interactive menu if no arguments were passed
    while True:
        choice = show_menu()
        
        if choice == "1":
            show_system_status()
        elif choice == "2":
            launch_discord_bot()
        elif choice == "3":
            show_discord_bot_info()
        elif choice == "4":
            launch_matrix_dashboard()
        elif choice == "5":
            launch_strategic_trader()
        elif choice == "6":
            show_available_parameters()
        elif choice == "7":
            launch_web_dashboard()
        elif choice == "8":
            view_bitget_positions()
        elif choice == "9":
            launch_cybernetic_quantum_bloom()
        elif choice == "10":
            run_test_runner()
        elif choice == "11":
            launch_garvey_portal()
        elif choice == "12":
            connect_online_redis()
        elif choice == "13":
            launch_btc_velocity_monitor()
        elif choice == "14":
            launch_aixbt_live_feed()
        elif choice == "0":
            print(f"{GREEN}Exiting OMEGA Grid Portal. JAH BLESS!{RESET}")
            break
        else:
            print(f"{RED}Invalid choice. Please try again.{RESET}")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 