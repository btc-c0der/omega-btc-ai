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
    """Display the main menu"""
    print(f"\n{CYAN}{BOLD}\"OMEGA GRID PORTAL\"   \"MAIN MENU\"{RESET}\n")
    print(f"{GOLD}1. {RESET}\"LAUNCH MATRIX TERMINAL DASHBOARD\"")
    print(f"{GOLD}2. {RESET}\"LAUNCH WEB DASHBOARD\"")
    print(f"{GOLD}3. {RESET}\"LAUNCH DISCORD BOT\"")
    print(f"{GOLD}4. {RESET}\"VIEW BITGET POSITIONS\"")
    print(f"{GOLD}5. {RESET}\"SHOW SYSTEM STATUS\"")
    print(f"{GOLD}6. {RESET}\"LAUNCH CCXT STRATEGIC TRADER\"")
    print(f"{GOLD}7. {RESET}\"LAUNCH CYBERNETIC QUANTUM BLOOM\"")
    print(f"{GOLD}8. {RESET}{MAGENTA}👑 \"OPEN KING SOLOMON'S PORTAL\" 👑{RESET}")
    print(f"{GOLD}0. {RESET}\"EXIT\"")
    return input(f"\n{BOLD}\"ENTER YOUR CHOICE (0-8):\"{RESET} ")

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
    print(f"{MAGENTA}{BOLD}Launching Cybernetic Quantum Bloom...{RESET}")
    bloom_path = os.path.join(PROJECT_ROOT, "src/omega_bot_farm/cybernetic_quantum_bloom.py")
    
    if not os.path.exists(bloom_path):
        print(f"{RED}Cybernetic Quantum Bloom not found!{RESET}")
        return False
    
    try:
        subprocess.Popen([sys.executable, bloom_path])
        print(f"{GREEN}Cybernetic Quantum Bloom launched!{RESET}")
        return True
    except Exception as e:
        print(f"{RED}Error launching Cybernetic Quantum Bloom: {e}{RESET}")
        return False

def open_solomon_portal():
    """Launch King Solomon's divine portal"""
    print(f"{MAGENTA}{BOLD}Opening King Solomon's Divine Portal...{RESET}")
    portal_path = os.path.join(SCRIPT_DIR, "omega_grid_portal.py")
    
    if not os.path.exists(portal_path):
        print(f"{RED}Portal script not found!{RESET}")
        return False
    
    try:
        subprocess.call([sys.executable, portal_path, "--open-portal-salomon-k1ng"])
        print(f"{GREEN}Divine portal closed. Returning to main menu...{RESET}")
        return True
    except Exception as e:
        print(f"{RED}Error opening Solomon's portal: {e}{RESET}")
        return False

def main():
    """Main entry point for the program"""
    # Parse command-line arguments
    import argparse
    parser = argparse.ArgumentParser(description="OMEGA Grid Portal - Simple Launcher")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--matrix", action="store_true", help="Launch Matrix dashboard")
    parser.add_argument("--web", action="store_true", help="Launch Web dashboard")
    parser.add_argument("--discord", action="store_true", help="Launch Discord bot")
    parser.add_argument("--positions", action="store_true", help="View BitGet positions")
    parser.add_argument("--strategic", action="store_true", help="Launch Strategic Trader")
    parser.add_argument("--quantum", action="store_true", help="Launch Quantum Bloom")
    parser.add_argument("--solomon", action="store_true", help="Open King Solomon's portal")
    args = parser.parse_args()
    
    # Display banner
    display_banner()
    
    # Process direct commands if provided
    if args.status:
        show_system_status()
        return
    
    if args.matrix:
        launch_matrix_dashboard()
        return
        
    if args.web:
        launch_web_dashboard()
        return
        
    if args.discord:
        launch_discord_bot()
        return
        
    if args.positions:
        view_bitget_positions()
        return
        
    if args.strategic:
        launch_strategic_trader()
        return
        
    if args.quantum:
        launch_cybernetic_quantum_bloom()
        return
        
    if args.solomon:
        open_solomon_portal()
        return
    
    # If no direct commands, show loading animation and menu
    display_loading_animation()
    
    while True:
        choice = show_menu()
        
        if choice == '0':
            print(f"\n{GREEN}Exiting OMEGA Grid Portal. JAH BLESS!{RESET}")
            break
            
        elif choice == '1':
            launch_matrix_dashboard()
            
        elif choice == '2':
            launch_web_dashboard()
            
        elif choice == '3':
            launch_discord_bot()
            
        elif choice == '4':
            view_bitget_positions()
            
        elif choice == '5':
            show_system_status()
            
        elif choice == '6':
            launch_strategic_trader()
            
        elif choice == '7':
            launch_cybernetic_quantum_bloom()
            
        elif choice == '8':
            open_solomon_portal()
            
        else:
            print(f"{RED}Invalid choice. Please try again.{RESET}")
        
        print(f"\n{CYAN}Press Enter to continue...{RESET}")
        input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{GREEN}Exiting OMEGA Grid Portal. JAH BLESS!{RESET}")
        sys.exit(0) 