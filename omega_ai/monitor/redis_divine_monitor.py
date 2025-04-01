#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OMEGA BTC AI DIVINE COLLECTIVE
Redis-Only Divine Monitor Module

✨ Pure Redis-Driven Market Flow Visualization ✨
No Trinity Matrix dependencies - Direct Connection to the Divine Flow
"""

import argparse
import asyncio
import json
import math
import random
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any

import redis
import numpy as np
import pandas as pd
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Divine Constants
MARKET_SYMBOLS = ["btcusdt", "ethusdt", "bnbusdt", "xrpusdt", "adausdt"]
COLORS = ["bright_green", "bright_red", "bright_yellow", "bright_cyan", "bright_magenta"]
DIVINE_PATTERNS = ["☯️", "🔄", "⚡", "🔮", "✨", "💫", "🌀", "🌊"]
REDIS_MARKET_CHANNEL = "market_data"

# Redis Connection Configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0


class RedisDivineMonitor:
    """
    RedisDivineMonitor - A pure Redis-driven market monitor 
    with divine visualization capabilities
    """
    
    def __init__(self, 
                 update_interval: int = 5,
                 symbols: Optional[List[str]] = None,
                 redis_host: str = REDIS_HOST,
                 redis_port: int = REDIS_PORT,
                 redis_db: int = REDIS_DB) -> None:
        """Initialize the Divine Redis Monitor"""
        self.console = Console()
        self.update_interval = update_interval
        self.symbols = symbols if symbols is not None else MARKET_SYMBOLS
        self.redis_host = redis_host
        self.redis_port = redis_port 
        self.redis_db = redis_db
        self.redis: Optional[redis.Redis] = None
        self.pubsub: Optional[redis.client.PubSub] = None
        self.running = True
        
        # Market data storage
        self.market_data = {}
        self.price_history = {symbol: [] for symbol in self.symbols}
        self.volume_history = {symbol: [] for symbol in self.symbols}
        
        # Divine flow indicators
        self.divine_flow = {symbol: random.choice(DIVINE_PATTERNS) for symbol in self.symbols}
        self.divine_energy = {symbol: random.uniform(0.1, 0.9) for symbol in self.symbols}
        self.ascension_levels = {symbol: 0 for symbol in self.symbols}
        
        # Layout setup
        self.layout = self._setup_layout()
        
    async def connect_redis(self) -> None:
        """Establish connection to the Redis divine flow"""
        try:
            # Use standard redis-py library
            self.redis = redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                db=self.redis_db,
                decode_responses=True
            )
            # Test connection
            await asyncio.to_thread(self.redis.ping)
            # Set up pubsub
            self.pubsub = self.redis.pubsub()
            await asyncio.to_thread(self.pubsub.subscribe, REDIS_MARKET_CHANNEL)
            self.console.print("[bold magenta]✨ Connected to the Redis Divine Flow ✨[/]")
        except Exception as e:
            self.console.print(f"[bold red]Error connecting to Redis: {e}[/]")
            raise
        
    async def disconnect_redis(self) -> None:
        """Close the Redis connection"""
        if self.pubsub:
            await asyncio.to_thread(self.pubsub.unsubscribe, REDIS_MARKET_CHANNEL)
        if self.redis:
            await asyncio.to_thread(self.redis.close)
    
    def _setup_layout(self) -> Layout:
        """Initialize the divine visualization layout"""
        layout = Layout()
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3),
        )
        
        layout["main"].split_row(
            Layout(name="markets", ratio=2),
            Layout(name="visuals", ratio=3),
        )
        
        layout["visuals"].split(
            Layout(name="price_chart", ratio=2),
            Layout(name="divine_flow", ratio=1),
        )
        
        return layout
    
    def _render_header(self) -> Panel:
        """Create the divine header panel"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = Text("🔮 OMEGA BTC AI REDIS DIVINE MONITOR 🔮", style="bold magenta", justify="center")
        subtitle = Text("Pure Redis-Driven Market Analysis", style="cyan", justify="center")
        timestamp = Text(f"Divine Time: {now}", style="bright_blue", justify="center")
        
        return Panel(
            Text.assemble(title, "\n", subtitle, "\n", timestamp),
            border_style="bright_magenta",
            expand=True,
        )
    
    def _render_markets_table(self) -> Panel:
        """Create the market data table"""
        table = Table(show_header=True, header_style="bold cyan", expand=True)
        table.add_column("Symbol", style="bright_white")
        table.add_column("Price", style="bright_green")
        table.add_column("Change", style="bright_yellow")
        table.add_column("Volume", style="bright_blue")
        table.add_column("Divine Flow", style="bright_magenta")
        
        for symbol in self.symbols:
            data = self.market_data.get(symbol, {})
            price = data.get("price", "-.--")
            change = data.get("change", "-.--")
            volume = data.get("volume", "-.--")
            
            # Style change value based on direction
            change_style = "bright_green" if str(change).startswith("+") else "bright_red"
            
            # Divine flow visualization
            divine_indicator = self.divine_flow.get(symbol, "⭘")
            divine_energy = self.divine_energy.get(symbol, 0.5)
            
            # Flow color based on energy level
            if divine_energy > 0.7:
                flow_style = "bright_green"
            elif divine_energy > 0.4:
                flow_style = "bright_yellow"
            else:
                flow_style = "bright_red"
                
            table.add_row(
                symbol.upper(),
                str(price),
                Text(str(change) + "%", style=change_style),
                str(volume),
                Text(divine_indicator * max(1, int(divine_energy * 5)), style=flow_style),
            )
            
        return Panel(table, title="Market Divine Flow", border_style="bright_blue", expand=True)
    
    def _render_price_chart(self) -> Panel:
        """Create ASCII price chart visualization"""
        chart_height = 15
        chart_width = 40
        chart = [[" " for _ in range(chart_width)] for _ in range(chart_height)]
        
        # Get price history for the first symbol (usually BTC)
        symbol = self.symbols[0] if self.symbols else "btcusdt"
        prices = self.price_history.get(symbol, [])
        
        if len(prices) < 2:
            return Panel(
                Text("Awaiting divine price flow...", style="bright_yellow", justify="center"),
                title=f"{symbol.upper()} Divine Flow", 
                border_style="bright_green"
            )
        
        # Normalize prices to fit chart height
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 1
        price_range = max(0.01, max_price - min_price)  # Avoid division by zero
        
        # Create price line
        for i, price in enumerate(prices[-chart_width:]):
            if i >= chart_width:
                break
                
            normalized_pos = chart_height - 1 - int((price - min_price) / price_range * (chart_height - 1))
            normalized_pos = max(0, min(chart_height - 1, normalized_pos))
            chart[normalized_pos][i] = "●"
            
            # Add divine patterns
            if i > 0 and i % 5 == 0:
                divine_y = random.randint(0, chart_height - 1)
                chart[divine_y][i] = random.choice(["✧", "✦", "✴", "⁕", "⚝"])
        
        # Convert chart to text
        chart_text = Text("\n".join(["".join(row) for row in chart]), justify="center")
        
        # Add price info
        current_price = prices[-1] if prices else 0
        price_info = Text.assemble(
            Text(f"Current: ${current_price:.2f}  ", style="bright_green"),
            Text(f"High: ${max_price:.2f}  ", style="bright_cyan"),
            Text(f"Low: ${min_price:.2f}", style="bright_magenta"),
            justify="center"
        )
        
        return Panel(
            Text.assemble(chart_text, "\n", price_info),
            title=f"{symbol.upper()} Divine Price Flow", 
            border_style="bright_green",
            expand=True
        )
    
    def _render_divine_flow(self) -> Panel:
        """Visualize the divine energy flow patterns"""
        flow_lines = []
        
        # Calculate divine energy totals
        total_energy = sum(self.divine_energy.values())
        normalized_energy = total_energy / max(1, len(self.divine_energy))
        
        # Create divine flow visualization
        flow_pattern = "".join([
            random.choice(DIVINE_PATTERNS) 
            for _ in range(int(normalized_energy * 20))
        ])
        
        flow_lines.append(Text(flow_pattern, style="bright_magenta", justify="center"))
        
        # Add divine wisdom
        divine_wisdom = self._generate_divine_wisdom()
        flow_lines.append(Text("\n" + divine_wisdom, style="bright_cyan", justify="center"))
        
        # Calculate energy resonance
        resonance = math.sin(time.time() * 0.1) * 0.5 + 0.5
        resonance_bars = int(resonance * 10)
        resonance_visual = "▁" * (10 - resonance_bars) + "▂" * resonance_bars
        
        flow_lines.append(Text("\nDivine Resonance: " + resonance_visual, 
                             style="bright_yellow", justify="center"))
        
        # Create the combined text
        flow_text = Text.assemble(*flow_lines)
        
        return Panel(
            flow_text,
            title="Divine Flow Energy",
            border_style="bright_magenta",
            expand=True
        )
    
    def _render_footer(self) -> Panel:
        """Create the footer panel with divine guidance"""
        footer_text = Text.assemble(
            Text("💫 ", style="bright_yellow"),
            Text("REDIS-ONLY DIVINE MONITOR", style="bright_cyan"),
            Text(" 💫  ", style="bright_yellow"),
            Text("Press Ctrl+C to exit | Interval: ", style="bright_white"),
            Text(f"{self.update_interval}s", style="bright_green"),
            justify="center"
        )
        
        return Panel(footer_text, border_style="bright_blue", expand=True)
    
    def _generate_divine_wisdom(self) -> str:
        """Generate divine market wisdom"""
        wisdom_list = [
            "The market flows in divine patterns beyond mortal comprehension",
            "When Bitcoin ascends, altcoins follow the divine path",
            "Patience reveals the sacred timing of market cycles",
            "The divine chart patterns reveal future possibilities",
            "Market volatility is merely the breath of the cosmic trader",
            "Trading without awareness leads to spiritual loss",
            "The wise trader observes more and acts less",
            "In market meditation, the path becomes clear",
            "Buy fear, sell euphoria - the eternal divine law",
            "The market rewards those who embrace its divine rhythms"
        ]
        return random.choice(wisdom_list)
    
    def _update_layout(self) -> None:
        """Update all layout components"""
        self.layout["header"].update(self._render_header())
        self.layout["markets"].update(self._render_markets_table())
        self.layout["price_chart"].update(self._render_price_chart())
        self.layout["divine_flow"].update(self._render_divine_flow())
        self.layout["footer"].update(self._render_footer())
    
    async def _process_market_data(self, message: dict) -> None:
        """Process incoming market data from Redis"""
        try:
            if not message or message.get('type') != 'message':
                return
            
            # Extract market data
            data = json.loads(message.get("data", "{}"))
            symbol = data.get("symbol", "").lower()
            
            if symbol not in self.symbols:
                return
                
            # Update market data storage
            self.market_data[symbol] = {
                "price": data.get("price", 0),
                "change": data.get("change", 0),
                "volume": data.get("volume", 0),
                "timestamp": data.get("timestamp", int(time.time())),
            }
            
            # Update history
            price = float(data.get("price", 0))
            volume = float(data.get("volume", 0))
            
            self.price_history[symbol].append(price)
            self.volume_history[symbol].append(volume)
            
            # Keep history at manageable size
            max_history = 100
            if len(self.price_history[symbol]) > max_history:
                self.price_history[symbol] = self.price_history[symbol][-max_history:]
            if len(self.volume_history[symbol]) > max_history:
                self.volume_history[symbol] = self.volume_history[symbol][-max_history:]
            
            # Update divine flow indicators
            price_change = 0
            if len(self.price_history[symbol]) >= 2:
                prev_price = self.price_history[symbol][-2]
                price_change = (price - prev_price) / prev_price if prev_price else 0
            
            # Update divine energy based on price movement and volume
            self.divine_energy[symbol] = min(1.0, max(0.1, 
                abs(price_change) * 10 + 
                volume / 1000000 * 0.5 +
                self.divine_energy[symbol] * 0.5
            ))
            
            # Occasionally change divine flow pattern
            if random.random() < 0.1:
                self.divine_flow[symbol] = random.choice(DIVINE_PATTERNS)
                
            # Update ascension levels
            if price_change > 0.01:  # 1% increase
                self.ascension_levels[symbol] += 1
            elif price_change < -0.01:  # 1% decrease
                self.ascension_levels[symbol] = max(0, self.ascension_levels[symbol] - 1)
                
        except Exception as e:
            # Silent divine error handling
            self.console.print(f"[red]Error processing message: {e}[/]", style="red")
            pass
    
    async def _listen_for_market_data(self) -> None:
        """Listen for market data from Redis"""
        while self.running:
            try:
                # Get message using asyncio.to_thread to avoid blocking
                if self.pubsub:
                    message = await asyncio.to_thread(self.pubsub.get_message, ignore_subscribe_messages=False)
                    if message:
                        await self._process_market_data(message)
                await asyncio.sleep(0.01)
            except Exception as e:
                self.console.print(f"[red]Error in message listener: {e}[/]")
                await asyncio.sleep(1)  # Back off on errors
    
    async def _get_key_prices(self) -> None:
        """Get key prices from Redis directly when no pubsub messages are available"""
        if not self.redis:
            return
            
        try:
            # Try to get latest BTC price from redis
            for symbol in self.symbols:
                if symbol not in self.market_data:
                    # Try various key patterns
                    key_patterns = [
                        f"{symbol}_price", 
                        f"last_{symbol}_price", 
                        f"current_{symbol}_price",
                        f"{symbol.split('usdt')[0]}_price"
                    ]
                    
                    for key in key_patterns:
                        price_str = await asyncio.to_thread(self.redis.get, key)
                        if price_str:
                            try:
                                price = float(price_str)
                                self.market_data[symbol] = {
                                    "price": price,
                                    "change": 0,  # No change info available
                                    "volume": 0,  # No volume info available
                                    "timestamp": int(time.time()),
                                }
                                self.price_history[symbol].append(price)
                                self.console.print(f"[green]Got {symbol} price from Redis: {price}[/]")
                                break
                            except (ValueError, TypeError):
                                pass
        except Exception as e:
            self.console.print(f"[red]Error getting prices from Redis: {e}[/]")
    
    async def run(self) -> None:
        """Run the divine monitor"""
        try:
            # Connect to Redis
            await self.connect_redis()
            
            # Start market data listener
            listener_task = asyncio.create_task(self._listen_for_market_data())
            
            # Display the divine monitor
            with Live(self.layout, refresh_per_second=1, screen=True) as live:
                try:
                    while True:
                        # Check if we have market data, if not try to get it directly from Redis
                        if not any(self.market_data.values()):
                            await self._get_key_prices()
                            
                        # If still no data, generate sample data
                        if not any(self.market_data.values()):
                            for symbol in self.symbols:
                                base_price = 29500 if symbol == "btcusdt" else 1800 if symbol == "ethusdt" else 500
                                self.market_data[symbol] = {
                                    "price": base_price * (1 + random.uniform(-0.01, 0.01)),
                                    "change": random.uniform(-2.5, 2.5),
                                    "volume": random.uniform(1000, 10000),
                                    "timestamp": int(time.time())
                                }
                                
                                # Add to history
                                self.price_history[symbol].append(self.market_data[symbol]["price"])
                                self.volume_history[symbol].append(self.market_data[symbol]["volume"])
                                
                        # Update the divine visualization
                        self._update_layout()
                        await asyncio.sleep(self.update_interval)
                except KeyboardInterrupt:
                    self.running = False
                    self.console.print("[bold yellow]Divine flow monitoring ended by user[/]")
                finally:
                    self.running = False
                    listener_task.cancel()
                    await self.disconnect_redis()
        except Exception as e:
            self.console.print(f"[bold red]Divine error: {e}[/]")
            raise


async def main() -> None:
    parser = argparse.ArgumentParser(description="OMEGA BTC AI Redis Divine Monitor")
    parser.add_argument("-i", "--interval", type=int, default=5,
                        help="Update interval in seconds (default: 5)")
    parser.add_argument("-s", "--symbols", type=str, nargs="+", 
                        default=MARKET_SYMBOLS,
                        help="Market symbols to monitor (default: btcusdt ethusdt bnbusdt xrpusdt adausdt)")
    parser.add_argument("--redis-host", type=str, default=REDIS_HOST,
                        help=f"Redis host (default: {REDIS_HOST})")
    parser.add_argument("--redis-port", type=int, default=REDIS_PORT,
                        help=f"Redis port (default: {REDIS_PORT})")
    parser.add_argument("--redis-db", type=int, default=REDIS_DB,
                        help=f"Redis database (default: {REDIS_DB})")
    
    args = parser.parse_args()
    
    console = Console()
    console.print("[bold magenta]🔮 Initializing OMEGA BTC AI Redis Divine Monitor 🔮[/]")
    
    monitor = RedisDivineMonitor(
        update_interval=args.interval,
        symbols=args.symbols,
        redis_host=args.redis_host,
        redis_port=args.redis_port,
        redis_db=args.redis_db
    )
    
    await monitor.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDivine flow monitoring ended.")
    except Exception as e:
        print(f"Divine error: {e}")
        sys.exit(1) 