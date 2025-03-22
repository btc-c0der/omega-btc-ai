#!/usr/bin/env python3
"""
OMEGA BTC AI - Stdout to WebSocket Bridge
==========================================

This script captures the stdout from bitget_live_traders.py and forwards it
to the MM WebSocket server for visualization on the dashboard.

Usage:
    python stdout_to_ws_bridge.py --cmd "python -m omega_ai.trading.exchanges.bitget_live_traders"
"""

import asyncio
import json
import re
import websockets
import argparse
import subprocess
import sys
import time
from datetime import datetime, timezone
import os
import signal

# Terminal colors for output
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
RESET = "\033[0m"

# WebSocket connection info
WS_HOST = "localhost"
WS_PORT = 8765
WS_PATH = "/ws"
WS_URL = f"ws://{WS_HOST}:{WS_PORT}{WS_PATH}"

# Global variables
ws_client = None
process = None
last_price = 84000.0  # Default BTC price as fallback
stop_event = asyncio.Event()

# Output patterns to extract trading data
PATTERNS = {
    "new_order": r"Placing new (buy|sell) order for (\w+) trader",
    "price": r"Current price for [^:]+: ([0-9.]+)",
    "position_close": r"Closing position for (\w+) trader",
    "pnl": r"Total PnL: ([+-]?[0-9.]+) USDT",
    "active_positions": r"Active Positions: ([0-9]+)",
    "error": r"ERROR.*?(?::\s+)?(.+)",
    "trader_performance": r"(\w+) Performance:.*?Symbol: ([^\\n]+).*?Total PnL: ([+-]?[0-9.]+).*?Active Positions: ([0-9]+)",
    "position_details": r"(long|short|LONG|SHORT): ([0-9.]+) @ ([0-9.]+) USD \| Unreal: ([+-]?[0-9.]+) \| Real: ([+-]?[0-9.]+)",
    # Add new pattern for detailed position data
    "detailed_position": r"\"symbol\": \"([^\"]+)\",\s*\"notional\": ([0-9.]+),.*?\"liquidationPrice\": ([0-9.]+),\s*\"entryPrice\": ([0-9.]+),\s*\"unrealizedPnl\": ([+-]?[0-9.]+),.*?\"percentage\": ([0-9.]+),\s*\"contracts\": ([0-9.]+),.*?\"side\": \"([^\"]+)\",.*?\"leverage\": ([0-9.]+)"
}

async def connect_websocket():
    """Connect to the MM WebSocket server."""
    global ws_client
    
    print(f"{CYAN}Connecting to WebSocket server at {WS_URL}...{RESET}")
    try:
        ws_client = await websockets.connect(WS_URL)
        print(f"{GREEN}Connected to WebSocket server{RESET}")
        return True
    except Exception as e:
        print(f"{RED}Failed to connect to WebSocket server: {str(e)}{RESET}")
        return False

async def send_to_websocket(data):
    """Send data to the WebSocket server."""
    global ws_client
    
    if not ws_client:
        success = await connect_websocket()
        if not success:
            print(f"{YELLOW}Cannot send data, WebSocket not connected{RESET}")
            return False
    
    try:
        if ws_client:
            await ws_client.send(json.dumps(data))
            return True
        return False
    except websockets.exceptions.ConnectionClosed:
        print(f"{YELLOW}WebSocket connection closed, attempting to reconnect...{RESET}")
        ws_client = None
        return await send_to_websocket(data)
    except Exception as e:
        print(f"{RED}Error sending data to WebSocket: {str(e)}{RESET}")
        return False

def parse_output(line):
    """Parse the output line and extract trading data."""
    global last_price
    
    data = {}
    
    # Check for price updates
    price_match = re.search(PATTERNS["price"], line)
    if price_match:
        last_price = float(price_match.group(1))
        data["btc_price"] = last_price
    
    # Check for new orders
    order_match = re.search(PATTERNS["new_order"], line)
    if order_match:
        side = order_match.group(1)
        trader_type = order_match.group(2)
        data["new_order"] = {
            "side": side,
            "trader": trader_type,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    # Check for position closures
    close_match = re.search(PATTERNS["position_close"], line)
    if close_match:
        trader_type = close_match.group(1)
        data["close_position"] = {
            "trader": trader_type,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    # Check for trader performance
    performance_match = re.search(PATTERNS["trader_performance"], line, re.DOTALL)
    if performance_match:
        trader_type = performance_match.group(1)
        symbol = performance_match.group(2)
        pnl = float(performance_match.group(3))
        positions = int(performance_match.group(4))
        
        data["trader_update"] = {
            "trader": trader_type,
            "symbol": symbol,
            "pnl": pnl,
            "active_positions": positions,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    # Check for position details
    position_match = re.search(PATTERNS["position_details"], line)
    if position_match:
        side = position_match.group(1).lower()
        size = float(position_match.group(2))
        price = float(position_match.group(3))
        unrealized_pnl = float(position_match.group(4))
        realized_pnl = float(position_match.group(5))
        
        data["position_update"] = {
            "side": side,
            "size": size,
            "entry_price": price,
            "unrealized_pnl": unrealized_pnl,
            "realized_pnl": realized_pnl,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    # Check for detailed position data
    detailed_position_match = re.search(PATTERNS["detailed_position"], line)
    if detailed_position_match:
        symbol = detailed_position_match.group(1)
        notional = float(detailed_position_match.group(2))
        liquidation_price = float(detailed_position_match.group(3))
        entry_price = float(detailed_position_match.group(4))
        unrealized_pnl = float(detailed_position_match.group(5))
        percentage = float(detailed_position_match.group(6))
        contracts = float(detailed_position_match.group(7))
        side = detailed_position_match.group(8)
        leverage = float(detailed_position_match.group(9))
        
        # Extract trader type from context (previous lines)
        trader_type = "strategic"  # Default to strategic if not found
        if "strategic trader" in line.lower():
            trader_type = "strategic"
        elif "aggressive trader" in line.lower():
            trader_type = "aggressive"
        elif "scalping trader" in line.lower():
            trader_type = "scalping"
        
        data["detailed_position"] = {
            "trader": trader_type,
            "symbol": symbol,
            "notional": notional,
            "liquidation_price": liquidation_price,
            "entry_price": entry_price,
            "unrealized_pnl": unrealized_pnl,
            "percentage": percentage,
            "contracts": contracts,
            "side": side,
            "leverage": leverage,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    # Check for full ticker data
    if "Full ticker data: {" in line:
        try:
            # Extract JSON between "Full ticker data: " and end of line
            ticker_data_start = line.find("Full ticker data: ") + len("Full ticker data: ")
            ticker_json = line[ticker_data_start:].strip()
            
            # Parse the JSON data
            ticker_data = json.loads(ticker_json)
            
            # Create a clean version for the dashboard
            data["ticker_data"] = {
                "symbol": ticker_data.get("symbol", "BTC/USDT"),
                "last": ticker_data.get("last", last_price),
                "bid": ticker_data.get("bid", 0),
                "ask": ticker_data.get("ask", 0),
                "high": ticker_data.get("high", 0),
                "low": ticker_data.get("low", 0),
                "change": ticker_data.get("change", 0),
                "percentage": ticker_data.get("percentage", 0),
                "volume": ticker_data.get("baseVolume", 0),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "btc_price": last_price,
                "funding_rate": ticker_data.get("info", {}).get("fundingRate", "0")
            }
        except Exception as e:
            print(f"{RED}Error parsing ticker data: {str(e)}{RESET}")
    
    # Check for errors
    error_match = re.search(PATTERNS["error"], line)
    if error_match:
        data["error"] = {
            "message": error_match.group(1),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    # Always include current BTC price in any message
    if data and "btc_price" not in data:
        data["btc_price"] = last_price
    
    # If we don't have any data but the line has meaningful content, 
    # send it as a generic log message
    if not data and len(line.strip()) > 10:
        data = {
            "log": {
                "message": line.strip(),
                "timestamp": datetime.now(timezone.utc).isoformat()
            },
            "btc_price": last_price
        }
    
    return data

async def process_output():
    """Process the output from the command and send it to the WebSocket server."""
    global process, stop_event
    
    # Send initial system status
    await send_to_websocket({
        "system_status": "STARTING",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "btc_price": last_price
    })
    
    while not stop_event.is_set():
        try:
            if process and process.stdout:
                line = await process.stdout.readline()
                if not line:
                    if process and process.returncode is not None:
                        print(f"{YELLOW}Process exited with code {process.returncode}{RESET}")
                        break
                    await asyncio.sleep(0.1)
                    continue
                
                line_str = line.decode('utf-8').strip()
                print(line_str)  # Echo to console
                
                data = parse_output(line_str)
                if data:
                    await send_to_websocket(data)
            else:
                await asyncio.sleep(0.1)
        except Exception as e:
            print(f"{RED}Error processing output: {str(e)}{RESET}")
            await asyncio.sleep(0.1)
    
    # Send final system status
    await send_to_websocket({
        "system_status": "STOPPED",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "btc_price": last_price
    })

async def send_heartbeat():
    """Send heartbeat messages to the WebSocket server."""
    global stop_event
    
    while not stop_event.is_set():
        await send_to_websocket({
            "heartbeat": True,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "btc_price": last_price
        })
        
        # Send heartbeat every 5 seconds
        await asyncio.sleep(5)

async def run_command(cmd):
    """Run the command and capture its output."""
    global process, stop_event
    
    print(f"{CYAN}Running command: {cmd}{RESET}")
    
    try:
        # Start the process
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        
        # Start tasks to process output and send heartbeats
        output_task = asyncio.create_task(process_output())
        heartbeat_task = asyncio.create_task(send_heartbeat())
        
        # Wait for the process to complete
        await process.wait()
        
        # Signal tasks to stop
        stop_event.set()
        
        # Wait for tasks to complete
        await asyncio.gather(output_task, heartbeat_task)
        
        print(f"{GREEN}Command completed with exit code {process.returncode}{RESET}")
        
    except Exception as e:
        print(f"{RED}Error running command: {str(e)}{RESET}")
        stop_event.set()

async def shutdown(signal=None):
    """Handle shutdown signal."""
    global process, stop_event, ws_client
    
    if signal:
        print(f"{YELLOW}Received signal {signal.name}, shutting down...{RESET}")
    
    # Set stop event
    stop_event.set()
    
    # Close WebSocket connection
    if ws_client:
        try:
            await ws_client.close()
        except:
            pass
    
    # Terminate process if running
    if process and process.returncode is None:
        try:
            process.terminate()
            # Wait briefly for process to terminate
            try:
                await asyncio.wait_for(process.wait(), timeout=2.0)
            except asyncio.TimeoutError:
                print(f"{YELLOW}Process did not terminate, killing...{RESET}")
                process.kill()
        except:
            pass

async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Capture stdout from a command and forward to WebSocket server")
    parser.add_argument("--cmd", type=str, required=True, help="Command to run and capture output from")
    parser.add_argument("--ws-host", type=str, default=WS_HOST, help=f"WebSocket server host (default: {WS_HOST})")
    parser.add_argument("--ws-port", type=int, default=WS_PORT, help=f"WebSocket server port (default: {WS_PORT})")
    parser.add_argument("--ws-path", type=str, default=WS_PATH, help=f"WebSocket server path (default: {WS_PATH})")
    
    args = parser.parse_args()
    
    # Update global WebSocket URL
    global WS_URL
    WS_URL = f"ws://{args.ws_host}:{args.ws_port}{args.ws_path}"
    
    # Register signal handlers
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(shutdown(s)))
    
    # Connect to WebSocket server
    connected = await connect_websocket()
    if not connected:
        print(f"{YELLOW}Will retry connection when data is available{RESET}")
    
    try:
        # Run the command
        await run_command(args.cmd)
    except KeyboardInterrupt:
        print(f"{YELLOW}Interrupted by user{RESET}")
    finally:
        # Ensure cleanup
        await shutdown()

if __name__ == "__main__":
    asyncio.run(main()) 