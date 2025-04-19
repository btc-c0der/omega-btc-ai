#!/usr/bin/env python3
"""
Network Connectivity Test for CyBer1t4L QA Bot
----------------------------------------------

This script tests network connectivity and ping response times to various
important services including Discord API, Bitget API, and general internet.
It will help diagnose issues with the Discord bot ping command not responding.
"""
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


import os
import pytest
import sys
import time
import json
import socket
import logging
import asyncio
import platform
import subprocess
import datetime
import argparse
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

# Configure colored logging
RESET = "\033[0m"
GREEN = "\033[38;5;82m"
RED = "\033[38;5;196m"
YELLOW = "\033[38;5;226m"
CYAN = "\033[38;5;51m"
BLUE = "\033[38;5;39m"
PURPLE = "\033[38;5;141m"

logging.basicConfig(
    level=logging.INFO,
    format=f"{PURPLE}[%(asctime)s]{RESET} {CYAN}%(levelname)s{RESET} - {GREEN}%(message)s{RESET}",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("NetworkConnectivityTest")

class NetworkTester:
    """Test network connectivity and latency."""
    
    def __init__(self):
        self.results = {
            "internet": {},
            "dns": {},
            "discord": {},
            "bitget": {},
            "system_info": self._get_system_info(),
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def _get_system_info(self) -> Dict[str, str]:
        """Get system information."""
        return {
            "os": platform.platform(),
            "python": platform.python_version(),
            "hostname": socket.gethostname(),
            "ip_address": self._get_ip_address()
        }
    
    def _get_ip_address(self) -> str:
        """Get the machine's IP address."""
        try:
            # Create a socket to determine the IP address used to connect to the internet
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.5)
            # Using a well-known DNS server IP but we don't actually send data
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            logger.error(f"Error getting IP address: {str(e)}")
            return "Unknown"
    
    def test_internet_connectivity(self) -> None:
        """Test basic internet connectivity."""
        targets = [
            "8.8.8.8",     # Google DNS
            "1.1.1.1",     # Cloudflare DNS
            "208.67.222.222"  # OpenDNS
        ]
        
        logger.info(f"{CYAN}Testing internet connectivity...{RESET}")
        self.results["internet"] = {}
        
        for target in targets:
            logger.info(f"Pinging {target}...")
            start_time = time.time()
            try:
                # Use the ping command to test connectivity
                ping_process = subprocess.run(
                    ["ping", "-c", "4", "-W", "2", target],
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                # Parse the ping results
                if ping_process.returncode == 0:
                    # Extract average ping time
                    output = ping_process.stdout
                    avg_line = [line for line in output.split("\n") if "avg" in line]
                    if avg_line:
                        # Format varies by OS, but typically contains "min/avg/max"
                        avg_ms = float(avg_line[0].split("=")[1].split("/")[1].strip())
                    else:
                        avg_ms = (time.time() - start_time) * 1000  # fallback
                    
                    self.results["internet"][target] = {
                        "status": "success",
                        "latency_ms": avg_ms,
                        "raw_output": ping_process.stdout[:500]  # Limit output size
                    }
                    logger.info(f"{GREEN}Connection to {target} successful: {avg_ms:.2f}ms{RESET}")
                else:
                    self.results["internet"][target] = {
                        "status": "failed",
                        "error": ping_process.stderr,
                        "raw_output": ping_process.stdout[:500]  # Limit output size
                    }
                    logger.error(f"{RED}Connection to {target} failed.{RESET}")
            except Exception as e:
                self.results["internet"][target] = {
                    "status": "error",
                    "error": str(e)
                }
                logger.error(f"{RED}Error testing connection to {target}: {str(e)}{RESET}")
    
    def test_dns_resolution(self) -> None:
        """Test DNS resolution for critical services."""
        domains = [
            "discord.com",
            "gateway.discord.gg",
            "api.bitget.com",
            "google.com",
            "api.openai.com"
        ]
        
        logger.info(f"{CYAN}Testing DNS resolution...{RESET}")
        self.results["dns"] = {}
        
        for domain in domains:
            logger.info(f"Resolving {domain}...")
            start_time = time.time()
            try:
                ip_address = socket.gethostbyname(domain)
                resolution_time = (time.time() - start_time) * 1000  # ms
                
                self.results["dns"][domain] = {
                    "status": "success",
                    "ip_address": ip_address,
                    "resolution_time_ms": resolution_time
                }
                logger.info(f"{GREEN}DNS resolution for {domain}: {ip_address} ({resolution_time:.2f}ms){RESET}")
            except socket.gaierror as e:
                self.results["dns"][domain] = {
                    "status": "failed",
                    "error": str(e)
                }
                logger.error(f"{RED}DNS resolution for {domain} failed: {str(e)}{RESET}")
            except Exception as e:
                self.results["dns"][domain] = {
                    "status": "error",
                    "error": str(e)
                }
                logger.error(f"{RED}Error resolving {domain}: {str(e)}{RESET}")
    
@pytest.mark.asyncio
    async def test_discord_api(self) -> None:
        """Test connectivity to Discord API endpoints."""
        import aiohttp
        
        endpoints = [
            ("gateway", "https://discord.com/api/v10/gateway"),
            ("api", "https://discord.com/api/v10"),
            ("cdn", "https://cdn.discordapp.com"),
            ("media", "https://media.discordapp.net")
        ]
        
        logger.info(f"{CYAN}Testing Discord API connectivity...{RESET}")
        self.results["discord"] = {}
        
        async with aiohttp.ClientSession() as session:
            for name, url in endpoints:
                logger.info(f"Testing Discord {name} endpoint ({url})...")
                start_time = time.time()
                try:
                    async with session.get(url, timeout=5) as response:
                        response_time = (time.time() - start_time) * 1000  # ms
                        
                        self.results["discord"][name] = {
                            "status": "success" if response.status < 400 else "error",
                            "http_status": response.status,
                            "response_time_ms": response_time
                        }
                        
                        if response.status < 400:
                            logger.info(f"{GREEN}Discord {name} endpoint: HTTP {response.status} ({response_time:.2f}ms){RESET}")
                        else:
                            logger.warning(f"{YELLOW}Discord {name} endpoint: HTTP {response.status} ({response_time:.2f}ms){RESET}")
                            
                        # If it's the gateway endpoint, check the returned URL
                        if name == "gateway" and response.status == 200:
                            data = await response.json()
                            if "url" in data:
                                self.results["discord"][name]["gateway_url"] = data["url"]
                                logger.info(f"{GREEN}Discord gateway URL: {data['url']}{RESET}")
                except aiohttp.ClientError as e:
                    self.results["discord"][name] = {
                        "status": "failed",
                        "error": str(e)
                    }
                    logger.error(f"{RED}Discord {name} endpoint test failed: {str(e)}{RESET}")
                except Exception as e:
                    self.results["discord"][name] = {
                        "status": "error",
                        "error": str(e)
                    }
                    logger.error(f"{RED}Error testing Discord {name} endpoint: {str(e)}{RESET}")
    
@pytest.mark.asyncio
    async def test_bitget_api(self) -> None:
        """Test connectivity to Bitget API endpoints."""
        import aiohttp
        
        endpoints = [
            ("api_time", "https://api.bitget.com/api/v2/public/time"),
            ("api_server", "https://api.bitget.com/api/v2/public/server"),
            ("ws_public", "wss://ws.bitget.com/spot/v1/stream")
        ]
        
        logger.info(f"{CYAN}Testing Bitget API connectivity...{RESET}")
        self.results["bitget"] = {}
        
        async with aiohttp.ClientSession() as session:
            for name, url in endpoints:
                if not url.startswith("wss"):
                    # HTTP endpoint
                    logger.info(f"Testing Bitget {name} endpoint ({url})...")
                    start_time = time.time()
                    try:
                        async with session.get(url, timeout=5) as response:
                            response_time = (time.time() - start_time) * 1000  # ms
                            
                            response_text = await response.text()
                            try:
                                response_json = await response.json()
                                response_status = response_json.get("code", "unknown")
                            except:
                                response_json = {}
                                response_status = "parse_error"
                            
                            self.results["bitget"][name] = {
                                "status": "success" if response.status < 400 else "error",
                                "http_status": response.status,
                                "api_status": response_status,
                                "response_time_ms": response_time,
                                "response": response_json if response_json else response_text[:200]  # Limit output size
                            }
                            
                            if response.status < 400:
                                logger.info(f"{GREEN}Bitget {name} endpoint: HTTP {response.status} ({response_time:.2f}ms){RESET}")
                            else:
                                logger.warning(f"{YELLOW}Bitget {name} endpoint: HTTP {response.status} ({response_time:.2f}ms){RESET}")
                    except aiohttp.ClientError as e:
                        self.results["bitget"][name] = {
                            "status": "failed",
                            "error": str(e)
                        }
                        logger.error(f"{RED}Bitget {name} endpoint test failed: {str(e)}{RESET}")
                    except Exception as e:
                        self.results["bitget"][name] = {
                            "status": "error",
                            "error": str(e)
                        }
                        logger.error(f"{RED}Error testing Bitget {name} endpoint: {str(e)}{RESET}")
                else:
                    # WebSocket endpoint - just check if we can establish a connection
                    logger.info(f"Testing Bitget WebSocket endpoint ({url})...")
                    try:
                        import websockets
                        start_time = time.time()
                        try:
                            async with websockets.connect(url) as websocket:
                                connection_time = (time.time() - start_time) * 1000  # ms
                                self.results["bitget"][name] = {
                                    "status": "success",
                                    "connection_time_ms": connection_time
                                }
                                logger.info(f"{GREEN}Bitget WebSocket connection successful ({connection_time:.2f}ms){RESET}")
                        except websockets.exceptions.WebSocketException as e:
                            self.results["bitget"][name] = {
                                "status": "failed",
                                "error": str(e)
                            }
                            logger.error(f"{RED}Bitget WebSocket connection failed: {str(e)}{RESET}")
                    except ImportError:
                        self.results["bitget"][name] = {
                            "status": "skipped",
                            "error": "websockets library not installed"
                        }
                        logger.warning(f"{YELLOW}Skipping WebSocket test - websockets library not installed{RESET}")
    
    def test_discord_bot_token_validity(self) -> None:
        """Test if the Discord bot token is valid."""
        try:
            # Check if .env file exists and load Discord token
            import dotenv
            env_path = Path(os.path.join(os.path.dirname(__file__), '../../.env'))
            if env_path.exists():
                dotenv.load_dotenv(env_path)
            
            token = os.environ.get("DISCORD_BOT_TOKEN")
            if not token:
                logger.warning(f"{YELLOW}Discord bot token not found in environment variables{RESET}")
                self.results["discord"]["token_validity"] = {
                    "status": "unknown",
                    "error": "Token not found in environment variables"
                }
                return
            
            # Perform a simple API request to verify the token
            import requests
            url = "https://discord.com/api/v10/users/@me"
            headers = {"Authorization": f"Bot {token}"}
            
            logger.info(f"{CYAN}Testing Discord bot token validity...{RESET}")
            start_time = time.time()
            response = requests.get(url, headers=headers, timeout=5)
            response_time = (time.time() - start_time) * 1000  # ms
            
            if response.status_code == 200:
                bot_data = response.json()
                self.results["discord"]["token_validity"] = {
                    "status": "valid",
                    "bot_id": bot_data.get("id"),
                    "bot_username": bot_data.get("username"),
                    "response_time_ms": response_time
                }
                logger.info(f"{GREEN}Discord bot token is valid for bot: {bot_data.get('username')}#{bot_data.get('discriminator', '0000')}{RESET}")
            else:
                self.results["discord"]["token_validity"] = {
                    "status": "invalid",
                    "http_status": response.status_code,
                    "error": response.text[:200]  # Limit output size
                }
                logger.error(f"{RED}Discord bot token is invalid. HTTP Status: {response.status_code}{RESET}")
        except ImportError as e:
            logger.warning(f"{YELLOW}Missing required library: {str(e)}{RESET}")
            self.results["discord"]["token_validity"] = {
                "status": "error",
                "error": f"Missing required library: {str(e)}"
            }
        except Exception as e:
            logger.error(f"{RED}Error testing Discord bot token: {str(e)}{RESET}")
            self.results["discord"]["token_validity"] = {
                "status": "error",
                "error": str(e)
            }
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all network connectivity tests."""
        logger.info(f"{CYAN}Starting network connectivity tests...{RESET}")
        
        # Run tests that don't require async
        self.test_internet_connectivity()
        self.test_dns_resolution()
        self.test_discord_bot_token_validity()
        
        # Run async tests
        try:
            await self.test_discord_api()
            await self.test_bitget_api()
        except ImportError as e:
            logger.warning(f"{YELLOW}Missing required library for API tests: {str(e)}{RESET}")
        except Exception as e:
            logger.error(f"{RED}Error running API tests: {str(e)}{RESET}")
        
        # Update timestamp
        self.results["timestamp"] = datetime.datetime.now().isoformat()
        
        logger.info(f"{GREEN}Network connectivity tests completed.{RESET}")
        return self.results
    
    def save_results(self, filepath: str) -> None:
        """Save test results to a JSON file."""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(self.results, f, indent=2)
            logger.info(f"{GREEN}Results saved to {filepath}{RESET}")
        except Exception as e:
            logger.error(f"{RED}Error saving results: {str(e)}{RESET}")
    
    def generate_report(self) -> str:
        """Generate a human-readable report of the test results."""
        report = []
        report.append("# Network Connectivity Test Report")
        report.append(f"Generated on: {self.results['timestamp']}")
        report.append(f"System: {self.results['system_info']['os']}")
        report.append(f"IP Address: {self.results['system_info']['ip_address']}")
        report.append("")
        
        # Internet connectivity
        report.append("## Internet Connectivity")
        for target, data in self.results.get("internet", {}).items():
            status_icon = "✅" if data.get("status") == "success" else "❌"
            latency = data.get("latency_ms", "N/A")
            latency_str = f"{latency:.2f}ms" if isinstance(latency, (int, float)) else latency
            report.append(f"{status_icon} {target}: {data.get('status', 'unknown')} - Latency: {latency_str}")
        report.append("")
        
        # DNS resolution
        report.append("## DNS Resolution")
        for domain, data in self.results.get("dns", {}).items():
            status_icon = "✅" if data.get("status") == "success" else "❌"
            ip = data.get("ip_address", "Not resolved")
            time = data.get("resolution_time_ms", "N/A")
            time_str = f"{time:.2f}ms" if isinstance(time, (int, float)) else time
            report.append(f"{status_icon} {domain}: {ip} - Time: {time_str}")
        report.append("")
        
        # Discord API
        report.append("## Discord API")
        for endpoint, data in self.results.get("discord", {}).items():
            if endpoint == "token_validity":
                status_icon = "✅" if data.get("status") == "valid" else "❌"
                report.append(f"{status_icon} Bot Token: {data.get('status', 'unknown')}")
                if data.get("status") == "valid":
                    report.append(f"  Bot: {data.get('bot_username', 'Unknown')} (ID: {data.get('bot_id', 'Unknown')})")
            else:
                status_icon = "✅" if data.get("status") == "success" else "❌"
                http_status = data.get("http_status", "N/A")
                time = data.get("response_time_ms", "N/A")
                time_str = f"{time:.2f}ms" if isinstance(time, (int, float)) else time
                report.append(f"{status_icon} {endpoint}: HTTP {http_status} - Time: {time_str}")
        report.append("")
        
        # Bitget API
        report.append("## Bitget API")
        for endpoint, data in self.results.get("bitget", {}).items():
            status_icon = "✅" if data.get("status") == "success" else "❌"
            if "http_status" in data:
                http_status = data.get("http_status", "N/A")
                time = data.get("response_time_ms", "N/A")
                time_str = f"{time:.2f}ms" if isinstance(time, (int, float)) else time
                report.append(f"{status_icon} {endpoint}: HTTP {http_status} - Time: {time_str}")
            else:
                time = data.get("connection_time_ms", "N/A")
                time_str = f"{time:.2f}ms" if isinstance(time, (int, float)) else time
                report.append(f"{status_icon} {endpoint}: {data.get('status', 'unknown')} - Time: {time_str}")
        report.append("")
        
        # Overall recommendation
        report.append("## Recommendation")
        
        # Check if all major systems are working
        internet_ok = all(data.get("status") == "success" for data in self.results.get("internet", {}).values())
        dns_ok = all(data.get("status") == "success" for data in self.results.get("dns", {}).values())
        discord_api_ok = all(data.get("status") == "success" for key, data in self.results.get("discord", {}).items() 
                            if key != "token_validity")
        token_valid = self.results.get("discord", {}).get("token_validity", {}).get("status") == "valid"
        
        if internet_ok and dns_ok and discord_api_ok and token_valid:
            report.append("✅ All systems are operational. The Discord bot should work correctly.")
            report.append("If the ping command is still not responding, check the following:")
            report.append("1. The command is properly registered and synced to Discord")
            report.append("2. The bot has proper permissions in the Discord server")
            report.append("3. The bot's code is handling the command interaction correctly")
        else:
            report.append("❌ There are connectivity issues that may be affecting the Discord bot.")
            if not internet_ok:
                report.append("- Internet connectivity issues detected. Check your network connection.")
            if not dns_ok:
                report.append("- DNS resolution issues detected. This may be affecting API connectivity.")
            if not discord_api_ok:
                report.append("- Discord API connectivity issues detected. The bot may be unable to communicate with Discord.")
            if not token_valid:
                report.append("- Discord bot token appears to be invalid. Check the token in your .env file.")
        
        return "\n".join(report)


async def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Network Connectivity Test for CyBer1t4L QA Bot")
    parser.add_argument("--save", type=str, help="Save results to this file path")
    parser.add_argument("--report", action="store_true", help="Generate and display a human-readable report")
    args = parser.parse_args()
    
    tester = NetworkTester()
    await tester.run_all_tests()
    
    if args.save:
        tester.save_results(args.save)
    
    if args.report:
        report = tester.generate_report()
        print("\n" + report)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info(f"{YELLOW}Test cancelled by user.{RESET}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"{RED}Unexpected error: {str(e)}{RESET}")
        sys.exit(1)