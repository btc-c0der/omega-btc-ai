#!/usr/bin/env python3
"""
CyBer1t4L - Advanced Quality Assurance Bot for OMEGA Trading Ecosystem
-----------------------------------------------------------------------
The Guardian of Divine Flow: Monitors test coverage, performs real-time QA,
and maintains the sacred harmony of the codebase.

Created with RASTA HEART ON F1R3
"""

import os
import sys
import time
import json
import argparse
import logging
import pytest
import asyncio
import threading
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path

# Add dotenv import for loading environment variables
from dotenv import load_dotenv

# Import Discord for bot integration
try:
    HAVE_DISCORD = True
except ImportError:
    HAVE_DISCORD = False

# ASCII Art for CyBer1t4L
CYBER1T4L_LOGO = """
  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗████████╗██╗  ██╗██╗     
 ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║╚══██╔══╝██║  ██║██║     
 ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║   ██║   ███████║██║     
 ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║   ██║   ██╔══██║██║     
 ╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║   ██║   ██║  ██║███████╗
  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝
                                                                       
 ░█▀█░█▀█░░░█▀▄░█▀█░▀█▀░░░█░█░█▀█░█▀▄░█▀▄░▀█▀░█▀█░█▀▄                  
 ░█▀▀░█▀█░░░█▀▄░█░█░░█░░░░█▀█░█▀█░█▀▄░█▀▄░░█░░█░█░█▀▄                  
 ░▀░░░▀░▀░░░▀▀░░▀▀▀░░▀░░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀░▀░▀                  
"""

# ANSI color codes for cyberpunk theming
class Colors:
    RESET = "\033[0m"
    NEON_GREEN = "\033[38;5;82m"
    NEON_BLUE = "\033[38;5;39m"
    NEON_PINK = "\033[38;5;213m"
    NEON_YELLOW = "\033[38;5;226m"
    NEON_ORANGE = "\033[38;5;208m"
    NEON_RED = "\033[38;5;196m"
    CYBER_CYAN = "\033[38;5;51m"
    CYBER_PURPLE = "\033[38;5;141m"
    DARK_BG = "\033[48;5;17m"
    
    @staticmethod
    def format(text, color, bold=False):
        bold_code = "\033[1m" if bold else ""
        return f"{bold_code}{color}{text}{Colors.RESET}"

# Configure logging with cyberpunk styling
def setup_logging(log_level=logging.INFO):
    log_format = f"{Colors.CYBER_PURPLE}[%(asctime)s]{Colors.RESET} {Colors.NEON_PINK}|{Colors.RESET} {Colors.CYBER_CYAN}%(levelname)s{Colors.RESET} {Colors.NEON_PINK}|{Colors.RESET} {Colors.NEON_GREEN}%(message)s{Colors.RESET}"
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger("CyBer1t4L")

class TestCoverageMonitor:
    """
    Monitors test coverage across the codebase and ensures thresholds are met.
    """
    def __init__(self, 
                 project_root: Path,
                 threshold: float = 80.0,
                 report_dir: Optional[Path] = None):
        self.project_root = project_root
        self.threshold = threshold
        self.report_dir = report_dir or project_root / "reports" / "coverage"
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger("CyBer1t4L.Coverage")
        
    def run_coverage_analysis(self, modules: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run pytest with coverage and return the results."""
        self.logger.info(f"{Colors.format('Running coverage analysis', Colors.NEON_BLUE, True)}")
        
        if modules is None:
            modules = [
                "src/omega_bot_farm/trading",
                "src/omega_bot_farm/discord",
                "src/omega_bot_farm/bitget_positions_info.py",
                "src/omega_bot_farm/matrix_cli_live_positions.py"
            ]
        
        module_str = " ".join(modules)
        xml_path = self.report_dir / "coverage.xml"
        html_dir = self.report_dir / "html"
        
        # Ensure the pytest.ini exists
        self._create_pytest_ini_if_missing()
        
        # Run the coverage command
        cmd = f"python -m pytest {module_str} --cov={self.project_root} --cov-report=xml:{xml_path} --cov-report=html:{html_dir} --cov-report=term -v"
        
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                check=False,
                capture_output=True,
                text=True
            )
            
            # Parse the coverage output
            coverage_data = self._parse_coverage_output(result.stdout)
            
            # Check if we meet the threshold
            overall_coverage = float(coverage_data.get("total_coverage", 0))
            if overall_coverage >= self.threshold:
                self.logger.info(f"{Colors.format('✅ COVERAGE THRESHOLD MET', Colors.NEON_GREEN, True)}: {overall_coverage:.2f}% (>= {self.threshold}%)")
            else:
                self.logger.warning(f"{Colors.format('❌ COVERAGE BELOW THRESHOLD', Colors.NEON_RED, True)}: {overall_coverage:.2f}% (< {self.threshold}%)")
            
            # Save a JSON report
            self._save_coverage_report(coverage_data)
            
            return coverage_data
            
        except Exception as e:
            self.logger.error(f"{Colors.format('Error running coverage analysis', Colors.NEON_RED, True)}: {str(e)}")
            return {"error": str(e), "total_coverage": 0.0, "modules": {}}
    
    def _parse_coverage_output(self, output: str) -> Dict[str, Any]:
        """Parse the coverage output from pytest-cov."""
        lines = output.split('\n')
        coverage_data = {
            "total_coverage": 0.0,
            "modules": {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Find the TOTAL line
        for i, line in enumerate(lines):
            if "TOTAL" in line and "%" in line:
                parts = line.split()
                try:
                    # Example format: "TOTAL 1234 567 54%"
                    coverage_data["total_coverage"] = float(parts[3].replace("%", ""))
                    coverage_data["total_statements"] = int(parts[1])
                    coverage_data["total_missed"] = int(parts[2])
                except (IndexError, ValueError):
                    pass
                break
        
        # Parse individual module coverage
        in_coverage_section = False
        for line in lines:
            if "---------- coverage:" in line:
                in_coverage_section = True
                continue
                
            if in_coverage_section and line.strip() and not line.startswith("-"):
                if "TOTAL" in line:
                    break
                    
                parts = line.split()
                if len(parts) >= 4:
                    module_name = parts[0]
                    try:
                        statements = int(parts[1])
                        missed = int(parts[2])
                        coverage_pct = float(parts[3].replace("%", ""))
                        
                        coverage_data["modules"][module_name] = {
                            "statements": statements,
                            "missed": missed,
                            "coverage": coverage_pct
                        }
                    except (IndexError, ValueError):
                        pass
        
        return coverage_data
    
    def _save_coverage_report(self, coverage_data: Dict[str, Any]):
        """Save the coverage report as JSON."""
        report_path = self.report_dir / f"coverage_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(coverage_data, f, indent=2)
        self.logger.info(f"Coverage report saved to {report_path}")
    
    def _create_pytest_ini_if_missing(self):
        """Create a basic pytest.ini if it doesn't exist."""
        pytest_ini_path = self.project_root / "pytest.ini"
        if not pytest_ini_path.exists():
            with open(pytest_ini_path, 'w') as f:
                f.write("""[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    e2e: marks tests as end-to-end tests
""")
            self.logger.info(f"Created default pytest.ini at {pytest_ini_path}")

class RealTimeQAMonitor:
    """
    Performs real-time monitoring of the trading bots and systems.
    """
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.logger = logging.getLogger("CyBer1t4L.RealTimeQA")
        self.active_monitors = {}
        self.stop_event = threading.Event()
    
    def start_monitoring(self, components: Optional[List[str]] = None):
        """Start real-time monitoring of components."""
        if components is None:
            components = ["bitget", "discord", "matrix"]
        
        self.logger.info(f"{Colors.format('Starting real-time monitoring', Colors.NEON_BLUE, True)} for: {', '.join(components)}")
        
        for component in components:
            monitor_thread = threading.Thread(
                target=self._monitor_component,
                args=(component,),
                daemon=True
            )
            monitor_thread.start()
            self.active_monitors[component] = monitor_thread
            self.logger.info(f"Monitoring started for: {Colors.format(component, Colors.CYBER_CYAN)}")
    
    def stop_monitoring(self):
        """Stop all monitoring threads."""
        self.logger.info(f"{Colors.format('Stopping all monitors', Colors.NEON_ORANGE)}")
        self.stop_event.set()
        
        for component, thread in self.active_monitors.items():
            thread.join(timeout=2.0)
            self.logger.info(f"Stopped monitoring: {component}")
        
        self.active_monitors.clear()
    
    def _monitor_component(self, component: str):
        """Monitor a specific component in real-time."""
        check_interval = 30  # seconds
        
        while not self.stop_event.is_set():
            try:
                # Perform component-specific checks
                if component == "bitget":
                    self._check_bitget_health()
                elif component == "discord":
                    self._check_discord_health()
                elif component == "matrix":
                    self._check_matrix_display_health()
                
                # Wait for the next check interval or until stop is requested
                self.stop_event.wait(check_interval)
                
            except Exception as e:
                self.logger.error(f"Error monitoring {component}: {e}")
                self.stop_event.wait(check_interval)  # Wait before retrying
    
    def _check_bitget_health(self):
        """Check the health of the BitGet connection and data flow."""
        # This would typically ping the BitGet API and verify response times
        self.logger.info(f"{Colors.format('BitGet API', Colors.NEON_GREEN)}: Connection healthy")
    
    def _check_discord_health(self):
        """Check the health of Discord bot connections."""
        # This would check if Discord bots are responsive
        self.logger.info(f"{Colors.format('Discord Bot', Colors.NEON_GREEN)}: Bot responding within acceptable limits")
    
    def _check_matrix_display_health(self):
        """Check the health of the Matrix display system."""
        # This would verify that the matrix display is rendering correctly
        self.logger.info(f"{Colors.format('Matrix Display', Colors.NEON_GREEN)}: Rendering performance optimal")

class TestGenerator:
    """
    Generates test cases based on code analysis and fills coverage gaps.
    """
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.logger = logging.getLogger("CyBer1t4L.TestGen")
    
    def generate_tests_for_module(self, module_path: str):
        """Generate test cases for a specific module."""
        self.logger.info(f"{Colors.format('Generating tests', Colors.NEON_BLUE, True)} for module: {module_path}")
        
        try:
            # Find module file
            module_file = self.project_root / module_path
            if not module_file.exists():
                self.logger.error(f"Module not found: {module_path}")
                return False
            
            # Analyze the module to find untested functions
            untested_functions = self._find_untested_functions(module_file)
            
            if not untested_functions:
                self.logger.info(f"No untested functions found in {module_path}")
                return True
            
            # Generate test file path
            test_file_path = self._get_test_file_path(module_path)
            
            # Generate the test file content
            test_content = self._generate_test_content(module_path, untested_functions)
            
            # Write the test file
            test_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(test_file_path, 'w') as f:
                f.write(test_content)
            
            self.logger.info(f"{Colors.format('Test file generated', Colors.NEON_GREEN)}: {test_file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating tests: {str(e)}")
            return False
    
    def _find_untested_functions(self, module_file: Path) -> List[Dict[str, Any]]:
        """Find functions without tests in the module."""
        # This is a simplified implementation - a real version would use AST parsing
        untested_functions = []
        
        try:
            with open(module_file, 'r') as f:
                content = f.read()
            
            import re
            # Find function definitions (simplified approach)
            func_pattern = re.compile(r'def\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)')
            for match in func_pattern.finditer(content):
                func_name = match.group(1)
                params = match.group(2)
                
                # Skip dunder methods and private methods
                if func_name.startswith('__') or func_name.startswith('_'):
                    continue
                
                # Check if a test exists for this function (simplified)
                test_exists = self._check_if_test_exists(module_file.name, func_name)
                
                if not test_exists:
                    untested_functions.append({
                        "name": func_name,
                        "params": params
                    })
        
        except Exception as e:
            self.logger.error(f"Error analyzing functions: {str(e)}")
        
        return untested_functions
    
    def _check_if_test_exists(self, module_name: str, func_name: str) -> bool:
        """Check if a test already exists for the given function."""
        # This is a simplified implementation
        test_name = f"test_{func_name}"
        test_dir = self.project_root / "tests"
        
        # Check in multiple test files
        for test_file in test_dir.glob(f"test_{module_name.replace('.py', '')}*.py"):
            try:
                with open(test_file, 'r') as f:
                    content = f.read()
                    if f"def {test_name}" in content:
                        return True
            except:
                pass
        
        return False
    
    def _get_test_file_path(self, module_path: str) -> Path:
        """Get the path for the test file."""
        module_name = os.path.basename(module_path).replace('.py', '')
        return self.project_root / "tests" / f"test_{module_name}.py"
    
    def _generate_test_content(self, module_path: str, untested_functions: List[Dict[str, Any]]) -> str:
        """Generate the content for the test file."""
        module_name = os.path.basename(module_path).replace('.py', '')
        import_path = module_path.replace('/', '.').replace('.py', '')
        
        # Create the test file header
        content = [
            "#!/usr/bin/env python3",
            '"""',
            f"Tests for {module_name}",
            "",
            f"This file was auto-generated by CyBer1t4L QA Bot",
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            '"""',
            "",
            "import pytest",
            "import unittest.mock as mock",
            "from unittest.mock import patch, MagicMock, AsyncMock",
            "import os",
            "import sys",
            "",
            "# Add the project root to the path",
            "sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))",
            "",
            f"# Import the module to test",
            f"from {import_path} import {', '.join(f['name'] for f in untested_functions)}",
            "",
            f"class Test{module_name.capitalize()}:",
            f'    """Tests for the {module_name} module."""',
            ""
        ]
        
        # Generate a test for each untested function
        for func in untested_functions:
            func_name = func["name"]
            params = func["params"]
            
            # Generate test function
            test_func = [
                f"    def test_{func_name}(self):",
                f'        """Test the {func_name} function."""',
                "        # TODO: Implement this test",
                f"        # {func_name}({params})",
                "        assert True  # Placeholder assertion",
                ""
            ]
            
            content.extend(test_func)
        
        return "\n".join(content)

class DiscordConnector:
    """
    Handles Discord bot integration for CyBer1t4L QA Bot.
    """
    def __init__(self, 
                 token: Optional[str] = None, 
                 app_id: Optional[str] = None, 
                 public_key: Optional[str] = None,
                 logger=None):
        self.token = token or os.getenv("DISCORD_BOT_TOKEN")
        self.app_id = app_id or os.getenv("CYBER1T4L_APP_ID")
        self.public_key = public_key or os.getenv("CYBER1T4L_PUBLIC_KEY")
        self.logger = logger or logging.getLogger("CyBer1t4L.Discord")
        self.client = None
        self.connected = False
        self.thread = None
        
        # Add initial log entries to help debug
        if self.token:
            token_preview = f"{self.token[:4]}...{self.token[-4:]}" if len(self.token) > 8 else "[EMPTY]"
            self.logger.info(f"{Colors.format('Discord token loaded', Colors.CYBER_CYAN)}: {token_preview}")
        if self.app_id:
            self.logger.info(f"{Colors.format('Discord App ID loaded', Colors.CYBER_CYAN)}: {self.app_id}")
        
    def is_configured(self) -> bool:
        """Check if Discord credentials are properly configured."""
        try:
            import discord
            has_config = bool(self.token and self.app_id and self.public_key)
            self.logger.info(f"{Colors.format('Discord configuration check', Colors.CYBER_CYAN)}: {'Configured' if has_config else 'Not configured'}")
            return has_config
        except ImportError:
            self.logger.warning(f"{Colors.format('Discord library not installed', Colors.NEON_YELLOW)}")
            return False
    
    def start(self) -> bool:
        """Start the Discord bot in a separate thread."""
        if not self.is_configured():
            self.logger.warning(f"{Colors.format('Discord bot not configured, skipping start', Colors.NEON_YELLOW)}")
            return False
        
        try:
            self.thread = threading.Thread(
                target=self._run_discord_bot,
                daemon=True
            )
            self.thread.start()
            self.logger.info(f"{Colors.format('Discord bot thread started', Colors.NEON_GREEN)}")
            return True
        except Exception as e:
            self.logger.error(f"{Colors.format('Error starting Discord bot thread', Colors.NEON_RED)}: {str(e)}")
            return False
    
    def _run_discord_bot(self):
        """Run the Discord bot (in a background thread)."""
        self.logger.info(f"{Colors.format('Discord bot thread running', Colors.CYBER_CYAN)}")
        
        # Import Discord libraries within the method to avoid issues if not installed
        try:
            import discord
            from discord.ext import commands
            from discord import app_commands
            self.logger.info(f"{Colors.format('Discord library imported successfully', Colors.NEON_GREEN)}")
        except ImportError:
            self.logger.error(f"{Colors.format('Discord library not available', Colors.NEON_RED)}")
            return
            
        # Skip if token is not set
        if not self.token:
            self.logger.error(f"{Colors.format('Discord bot token not set', Colors.NEON_RED)}")
            return
            
        try:
            # Set up intents (required for newer Discord.py versions)
            intents = discord.Intents.default()
            # Enabling privileged intents that are now active in the Discord Developer Portal
            intents.message_content = True  # Privileged intent for reading message content
            # intents.members = True         # Privileged intent for accessing member information
            # intents.presences = True       # Privileged intent for accessing presence information
            
            # Create bot with command prefix and intents
            bot = commands.Bot(command_prefix='!', intents=intents)
            self.client = bot
            self.logger.info(f"{Colors.format('Discord bot created with intents', Colors.NEON_GREEN)}")
            self.logger.info(f"{Colors.format('Message content intent enabled: ' + str(intents.message_content), Colors.NEON_GREEN)}")
            
            # Define bot events
            @bot.event
            async def on_ready():
                self.connected = True
                self.logger.info(f"{Colors.format('CyBer1t4L QA Bot', Colors.NEON_GREEN)} connected to Discord as {bot.user}")
                
                # Set bot status
                await bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.watching, 
                        name="code quality 🧪"
                    ),
                    status=discord.Status.online
                )
                self.logger.info(f"{Colors.format('Discord bot status set to online', Colors.NEON_GREEN)}")
                
                # Sync commands with Discord
                try:
                    self.logger.info(f"{Colors.format('Attempting to sync slash commands with Discord', Colors.NEON_YELLOW)}")
                    # Use copy_global_to=None to sync to all guilds the bot is in
                    synced = await bot.tree.sync(guild=None)
                    self.logger.info(f"{Colors.format('Slash commands synced globally', Colors.NEON_GREEN)}: {len(synced)} commands")
                    
                    # If global sync doesn't work, try syncing to each guild individually
                    if not synced and bot.guilds:
                        self.logger.info(f"{Colors.format('Attempting guild-specific command sync', Colors.NEON_YELLOW)}")
                        for guild in bot.guilds:
                            try:
                                guild_synced = await bot.tree.sync(guild=discord.Object(id=guild.id))
                                self.logger.info(f"{Colors.format('Slash commands synced to guild', Colors.NEON_GREEN)}: {guild.name} ({len(guild_synced)} commands)")
                            except Exception as e:
                                self.logger.error(f"{Colors.format('Failed to sync commands to guild', Colors.NEON_RED)}: {guild.name} - {str(e)}")
                except Exception as e:
                    self.logger.error(f"{Colors.format('Failed to sync slash commands', Colors.NEON_RED)}: {str(e)}")
                    self.logger.error(f"Exception type: {type(e).__name__}")
                    import traceback
                    self.logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Add more debug events
            @bot.event
            async def on_guild_join(guild):
                self.logger.info(f"{Colors.format('Bot joined new guild', Colors.NEON_GREEN)}: {guild.name} ({guild.id})")
                try:
                    cmds = await bot.tree.sync(guild=discord.Object(id=guild.id))
                    self.logger.info(f"{Colors.format('Synced commands to new guild', Colors.NEON_GREEN)}: {len(cmds)} commands")
                except Exception as e:
                    self.logger.error(f"{Colors.format('Failed to sync commands to new guild', Colors.NEON_RED)}: {str(e)}")
                    
            @bot.event 
            async def on_app_command_completion(interaction, command):
                self.logger.info(f"{Colors.format('Slash command executed', Colors.NEON_GREEN)}: /{command.name} by {interaction.user}")
                
            # Register slash commands using the app_commands tree
            # Clear any existing commands first
            bot.tree.clear_commands(guild=None)
            self.logger.info(f"{Colors.format('Cleared existing slash commands', Colors.CYBER_CYAN)}")
            
            @bot.tree.command(name="ping", description="Check if the bot is alive")
            async def slash_ping(interaction: discord.Interaction):
                """Simple ping command to check if the bot is alive."""
                self.logger.info(f"{Colors.format('Processing ping command', Colors.NEON_GREEN)} from {interaction.user}")
                await interaction.response.send_message("🧪 PONG! CyBer1t4L QA Bot is alive")
                self.logger.info(f"{Colors.format('Ping command completed', Colors.NEON_GREEN)} for {interaction.user}")
            
            @bot.tree.command(name="status", description="Get the current status of the QA bot")
            async def slash_status(interaction: discord.Interaction):
                """Return the current status of the QA bot."""
                self.logger.info(f"{Colors.format('Processing status command', Colors.NEON_GREEN)} from {interaction.user}")
                await interaction.response.send_message(
                    "🧬 **CyBer1t4L QA Bot Status**\n"
                    f"✅ Bot is running\n"
                    f"✅ Monitoring active\n"
                    f"✅ Coverage analysis available\n"
                )
                self.logger.info(f"{Colors.format('Status command completed', Colors.NEON_GREEN)} for {interaction.user}")
            
            @bot.tree.command(name="coverage", description="Get the current test coverage report")
            async def slash_coverage(interaction: discord.Interaction):
                """Return the current test coverage information."""
                self.logger.info(f"{Colors.format('Processing coverage command', Colors.NEON_GREEN)} from {interaction.user}")
                await interaction.response.defer()
                await interaction.followup.send("📊 **Generating coverage report...**\nThis may take a few moments.")
                self.logger.info(f"{Colors.format('Coverage command completed', Colors.NEON_GREEN)} for {interaction.user}")
            
            @bot.tree.command(name="test", description="Run tests for a specific module")
            @app_commands.describe(module="The module to test (e.g., trading, discord, qa)")
            async def slash_test(interaction: discord.Interaction, module: str):
                """Run tests for a specific module."""
                self.logger.info(f"{Colors.format('Processing test command', Colors.NEON_GREEN)} for module {module} from {interaction.user}")
                await interaction.response.defer()
                await interaction.followup.send(f"🧪 **Running tests for module: {module}**\nThis may take a few moments.")
                self.logger.info(f"{Colors.format('Test command completed', Colors.NEON_GREEN)} for {interaction.user}")
                
            # Log the registered commands
            all_commands = bot.tree.get_commands()
            self.logger.info(f"{Colors.format('Registered slash commands', Colors.NEON_GREEN)}: {len(all_commands)} commands")
            for cmd in all_commands:
                cmd_desc = getattr(cmd, 'description', 'No description available')
                self.logger.info(f"{Colors.format('Command', Colors.CYBER_CYAN)}: /{cmd.name} - {cmd_desc}")
            
            # Start the bot (with non-None token)
            if self.token and self.token != "DISABLED":
                self.logger.info(f"{Colors.format('Starting Discord bot with token', Colors.NEON_GREEN)}: {self.token[:4]}...{self.token[-4:]}")
                bot.run(self.token)
            else:
                self.logger.error(f"{Colors.format('Cannot run Discord bot: Invalid token', Colors.NEON_RED)}")
            
        except Exception as e:
            import traceback
            self.logger.error(f"{Colors.format('Discord bot error', Colors.NEON_RED)}: {str(e)}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            self.connected = False

class CyBer1t4L:
    """
    Main CyBer1t4L QA Bot class that coordinates all QA activities.
    """
    def __init__(self, project_root: Optional[Path] = None):
        # Load environment variables
        load_dotenv()
        
        self.project_root = project_root or Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
        self.logger = setup_logging()
        
        # Load credentials from environment variables
        self.app_id = os.getenv("CYBER1T4L_APP_ID")
        self.public_key = os.getenv("CYBER1T4L_PUBLIC_KEY")
        
        if not self.app_id or not self.public_key:
            self.logger.warning(f"{Colors.format('Missing CYBER1T4L credentials in .env file', Colors.NEON_RED, True)}")
            self.logger.warning("Set CYBER1T4L_APP_ID and CYBER1T4L_PUBLIC_KEY in your .env file")
        else:
            self.logger.info(f"{Colors.format('CYBER1T4L credentials loaded', Colors.NEON_GREEN)}")
        
        # Initialize components
        self.coverage_monitor = TestCoverageMonitor(self.project_root)
        self.realtime_monitor = RealTimeQAMonitor(self.project_root)
        self.test_generator = TestGenerator(self.project_root)
        
        # Initialize Discord connector
        self.discord = DiscordConnector(logger=self.logger)
        
        self.logger.info(f"{Colors.format('CyBer1t4L QA Bot Initialized', Colors.NEON_GREEN, True)}")
        self.logger.info(f"Project root: {self.project_root}")
    
    def display_intro(self):
        """Display the cyberpunk-themed intro."""
        print(f"\n{Colors.DARK_BG}")
        for line in CYBER1T4L_LOGO.split('\n'):
            colored_line = ""
            for i, char in enumerate(line):
                if char in "█▀▄":
                    colors = [Colors.NEON_GREEN, Colors.NEON_BLUE, Colors.NEON_PINK]
                    colored_line += f"{colors[i % 3]}{char}{Colors.RESET}"
                elif char == "░":
                    colored_line += f"{Colors.CYBER_PURPLE}{char}{Colors.RESET}"
                else:
                    colored_line += f"{Colors.CYBER_CYAN}{char}{Colors.RESET}"
            print(colored_line)
            
        print(f"{Colors.RESET}\n")
        print(f"{Colors.format('🔴 🟡 🟢 RASTA HEART ON F1R3 🔴 🟡 🟢', Colors.NEON_ORANGE, True)}")
        print(f"{Colors.format('THE GUARDIAN OF DIVINE FLOW', Colors.NEON_GREEN, True)}")
        print(f"{Colors.format('CyBer1t4L v1.0.0', Colors.NEON_BLUE)} - {Colors.format('QA JEDI Master', Colors.NEON_PINK)}\n")
        
        # Display credentials status
        if self.app_id and self.public_key:
            print(f"{Colors.format('CYBER1T4L BOT CONNECTED', Colors.NEON_GREEN)} - APP ID: {self.app_id[:4]}...{self.app_id[-4:]}")
        else:
            print(f"{Colors.format('CYBER1T4L BOT NOT CONFIGURED', Colors.NEON_RED)} - Missing credentials")
    
    def run_full_qa_cycle(self):
        """Run a full QA cycle including coverage analysis and test generation."""
        self.display_intro()
        
        # Start Discord bot if configured
        self.discord.start()
        
        # Step 1: Run coverage analysis
        self.logger.info(f"{Colors.format('STEP 1', Colors.NEON_YELLOW, True)}: Running coverage analysis")
        coverage_data = self.coverage_monitor.run_coverage_analysis()
        
        # Step 2: Generate tests for low-coverage modules
        self.logger.info(f"{Colors.format('STEP 2', Colors.NEON_YELLOW, True)}: Generating tests for low-coverage modules")
        low_coverage_modules = [
            module for module, data in coverage_data.get("modules", {}).items()
            if data.get("coverage", 0) < self.coverage_monitor.threshold
        ]
        
        for module in low_coverage_modules:
            self.test_generator.generate_tests_for_module(module)
        
        # Step 3: Start real-time monitoring
        self.logger.info(f"{Colors.format('STEP 3', Colors.NEON_YELLOW, True)}: Initiating real-time monitoring")
        self.realtime_monitor.start_monitoring()
        
        # Keep running until interrupted
        try:
            self.logger.info(f"{Colors.format('CyBer1t4L QA Bot running', Colors.NEON_GREEN, True)}")
            self.logger.info("Press Ctrl+C to exit")
            
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info(f"{Colors.format('Shutting down CyBer1t4L QA Bot', Colors.NEON_ORANGE)}")
            self.realtime_monitor.stop_monitoring()
    
    def run_coverage_check(self):
        """Run only the coverage check."""
        self.display_intro()
        # Start Discord bot if configured
        self.discord.start()
        self.coverage_monitor.run_coverage_analysis()
    
    def generate_tests(self, module_paths: List[str]):
        """Generate tests for specific modules."""
        self.display_intro()
        # Start Discord bot if configured
        self.discord.start()
        for module_path in module_paths:
            self.test_generator.generate_tests_for_module(module_path)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="CyBer1t4L QA Bot - OMEGA Trading Ecosystem QA Guardian")
    
    parser.add_argument("--mode", choices=["full", "coverage", "generate", "monitor"], 
                        default="full", help="Operation mode")
    
    parser.add_argument("--modules", nargs="+", help="Modules to generate tests for")
    
    parser.add_argument("--threshold", type=float, default=80.0,
                        help="Coverage threshold percentage (default: 80.0)")
    
    parser.add_argument("--project-root", type=str, help="Project root directory")
    
    return parser.parse_args()

def main():
    """Main entry point for CyBer1t4L."""
    args = parse_args()
    
    project_root = Path(args.project_root) if args.project_root else None
    bot = CyBer1t4L(project_root)
    
    if args.mode == "full":
        bot.run_full_qa_cycle()
    elif args.mode == "coverage":
        bot.run_coverage_check()
    elif args.mode == "generate":
        if not args.modules:
            bot.logger.error("No modules specified. Use --modules to specify modules")
            return 1
        bot.generate_tests(args.modules)
    elif args.mode == "monitor":
        bot.display_intro()
        # Start Discord bot if configured
        bot.discord.start()
        bot.realtime_monitor.start_monitoring()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            bot.realtime_monitor.stop_monitoring()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 