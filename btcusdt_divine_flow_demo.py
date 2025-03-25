#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Mini demo script to demonstrate the BTCUSDT Divine Flow visualization panel
from the Redis Divine Monitor
"""

import asyncio
import json
import math
import random
import time
from datetime import datetime
import argparse

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns

# Default timing parameters (in seconds)
DEFAULT_MESSAGE_CYCLE = 3
DEFAULT_STATUS_CYCLE = 5
DEFAULT_WHALE_DETECTION_CYCLE = 30

# Sample BTC price data
SAMPLE_PRICES = [
    29342.50, 29351.20, 29367.80, 29401.10, 29422.30, 
    29418.70, 29402.40, 29387.90, 29392.50, 29410.30,
    29405.60, 29398.20, 29382.70, 29375.10, 29381.90,
    29395.40, 29412.80, 29436.20, 29468.50, 29482.10
]

# Sample volume data (matching the price data length)
SAMPLE_VOLUMES = [
    420.32, 380.25, 520.17, 610.45, 580.62,
    490.38, 350.21, 380.53, 410.72, 450.18,
    520.64, 590.87, 630.42, 580.19, 490.25,
    410.38, 380.52, 420.18, 530.62, 620.45
]

# Divine wisdom messages
DIVINE_WISDOM = [
    "The market flows in divine patterns beyond mortal comprehension",
    "When Bitcoin ascends, altcoins follow the divine path",
    "Patience reveals the sacred timing of market cycles",
    "The divine chart patterns reveal future possibilities",
    "Market volatility is merely the breath of the cosmic trader",
    "In market meditation, the path becomes clear",
    "Buy fear, sell euphoria - the eternal divine law",
    "The market rewards those who embrace its divine rhythms",
    "True profit comes from alignment with cosmic market cycles",
    "The wise trader observes more and acts less"
]

# Whale protection messages
WHALE_MESSAGES = [
    "Scanning depths for whale market activity...",
    "No harmful trading patterns detected in these waters",
    "Watching for predatory market manipulation",
    "Protecting the gentle giants of the crypto ocean",
    "Monitoring market depths for benevolent whales",
    "Shielding natural market movements from disruption",
    "Deep liquidity pools showing harmonious flow",
    "Keeping watch over the sacred crypto migration paths",
    "Divine protection for the ocean's largest traders",
    "Guarding against sudden liquidity drains"
]

# Whale detection status levels
WHALE_STATUS = [
    "Calm waters. No large movements detected.",
    "Minor ripples. Small accumulation observed.",
    "Moderate activity. Watching closely.",
    "Large wallet activated. Tracking movement.",
    "ALERT: Significant whale activity detected!",
    "Whale pod formation detected. Unusual pattern."
]

# Whale sizes and corresponding ASCII art
WHALE_ASCII_ART = {
    "small": """     .-'
'--./ /     _.---.
'-,  (__..-'       \\
   \\          .     |
    ',.__.   ,__.--/
      '._/_.'___.-'""",
    
    "medium": """       .
      ":"
    ___:____     |"\\/"|
  ,'        `.    \\  /
  |  O        \\___/  |
~^~^~^~^~^~^~^~^~^~^~^~^~""",
    
    "large": """                   .
                    ":"
                  ___:____     |"\\/"|
                ,'        `.    \\  /
                |  O        \\___/  |
              /|          ,'    |
             / |   ,'`.   |     |
    (       /__|  /    \\  |     |
     \\     (_/  | /      \\|     |
      \\         |/        \\     |
       \\        ||        |\\    |
        \\       ||        | \\   |
         \\      ||        |  \\  |
          \\___//|\\_______/    \\|
              ''   `----'      '""",
    
    "mega": """                .
               ":"
             ___:____     |"\\/"|
           ,'        `.    \\  /
           |  O        \\___/  |
         /|          ,'    |
        / |   ,'`.   |     |
  (    /__|  /    \\  |     |        _______
   \\  (_/  | /      \\|     |       _/       \\_
    \\      |/        \\     |      /   \\_      \\
     \\     ||        |\\    |      |  \\_/       |
      \\    ||        | \\   |      \\/           |
       \\   ||        |  \\  |       \\__     ___/
        \\__||\\_______/    \\|           \\   /
            ''   `----'     '            \\_/"""
}

# Global timing parameters
whale_message_cycle_seconds = DEFAULT_MESSAGE_CYCLE
whale_status_cycle_seconds = DEFAULT_STATUS_CYCLE
whale_detection_cycle_seconds = DEFAULT_WHALE_DETECTION_CYCLE

def set_whale_sonar_timing(message_cycle_seconds=None, status_cycle_seconds=None, detection_cycle_seconds=None):
    """Set the timing parameters for the whale sonar"""
    global whale_message_cycle_seconds, whale_status_cycle_seconds, whale_detection_cycle_seconds
    
    if message_cycle_seconds is not None:
        whale_message_cycle_seconds = max(1, message_cycle_seconds)  # Minimum 1 second
        
    if status_cycle_seconds is not None:
        whale_status_cycle_seconds = max(1, status_cycle_seconds)    # Minimum 1 second
        
    if detection_cycle_seconds is not None:
        whale_detection_cycle_seconds = max(5, detection_cycle_seconds)  # Minimum 5 seconds

def _render_whale_visualization(whale_size, direction, depth, impact):
    """
    Render an ASCII whale visualization with metadata
    
    Args:
        whale_size: Size of the whale in BTC
        direction: Direction of movement (→, ←, ↑, ↓)
        depth: Market depth in meters
        impact: Impact level (Low, Medium, High)
    
    Returns:
        Panel containing the whale visualization
    """
    # Determine whale category based on size
    if whale_size <= 250:
        whale_category = "small"
        border_style = "bright_blue"
    elif whale_size <= 500:
        whale_category = "medium"
        border_style = "bright_cyan"
    elif whale_size <= 1000:
        whale_category = "large" 
        border_style = "bright_yellow"
    else:
        whale_category = "mega"
        border_style = "bright_red"
    
    # Get corresponding ASCII art
    whale_art = WHALE_ASCII_ART[whale_category]
    
    # Create detection time and last seen
    now = datetime.now()
    detection_time = now.strftime("%H:%M:%S")
    last_seen_minutes = random.randint(0, 5)
    
    # Determine movement type
    movements = ["Accumulation Phase", "Distribution Phase", "HODLing", "Position Building", "Taking Profit"]
    movement = random.choice(movements)
    
    # Build the visualization with metadata
    content = Text()
    
    # Add the whale ASCII art with whale body in bright_white
    content.append(whale_art, style="bright_white")
    
    # Add metadata below the whale
    content.append("\n\n")
    content.append(f"ø01-Size: {whale_size} BTC | ", style="bright_green")
    content.append(f"ø02-Depth: {depth}m | ", style="bright_blue")
    content.append(f"ø03-Direction: {direction}", style="bright_yellow")
    
    content.append("\n")
    content.append(f"ø04-Impact: {impact} | ", style="bright_magenta")
    content.append(f"ø05-Movement: {movement}", style="bright_cyan")
    
    content.append("\n")
    content.append(f"ø06-Detected at: {detection_time} | ", style="dim")
    content.append(f"ø07-Last seen: {last_seen_minutes}min ago", style="dim")
    
    # Center all content
    content.justify = "center"
    
    # Create and return the panel
    return Panel(
        content,
        title="ø00-WHALE DETECTION FRAME",
        border_style=border_style,
        expand=False
    )

def _render_whale_sonar(is_streaming=False):
    """Create the WHALE SONAR visualization for the SEA SHEPHERD module"""
    if not is_streaming:
        # Grey out when not streaming
        sonar_text = Text("ø10-WHALE SONAR: OFFLINE (awaiting data stream)", style="dim")
        sonar_text.justify = "center"
        return sonar_text
    
    # Create a sonar visualization that "scans" by changing with time
    timestamp = time.time()
    scan_phase = (timestamp % 4)  # 0-3 for different phases of the scan
    
    # Create the sonar animation frames based on scan phase
    if scan_phase < 1:
        sonar_frame = "◜   ◝"
    elif scan_phase < 2:
        sonar_frame = "◠───◠"
    elif scan_phase < 3:
        sonar_frame = "◟   ◞"
    else:
        sonar_frame = "◡───◡"
    
    # Random status message changing based on the configured cycle
    message_index = int(timestamp / whale_message_cycle_seconds) % len(WHALE_MESSAGES)
    whale_message = WHALE_MESSAGES[message_index]
    
    # Status changes based on configured cycle
    status_seed = int(timestamp / whale_status_cycle_seconds)
    random.seed(status_seed)  # Use time-based seed for consistent randomness within the same cycle
    
    # Randomly choose a status level, weighted toward calmer states
    status_weight = random.random()
    if status_weight < 0.6:  # 60% chance of lowest two levels
        status_index = random.randint(0, 1)
    elif status_weight < 0.85:  # 25% chance of middle two levels
        status_index = random.randint(2, 3)
    else:  # 15% chance of highest two levels
        status_index = random.randint(4, 5)
    
    random.seed()  # Reset the random seed
    
    status = WHALE_STATUS[status_index]
    
    # Choose status color based on level
    if status_index <= 1:
        status_color = "bright_green"
    elif status_index <= 3:
        status_color = "bright_yellow"
    else:
        status_color = "bright_red"
    
    # Combine everything into the sonar display
    sonar_text = Text()
    sonar_text.append("\n\nø11-SEA SHEPHERD CLI Ω MODULE", style="bright_blue")
    sonar_text.append("\nø12-WHALE SONAR: [ACTIVE] ", style="bright_cyan")
    sonar_text.append(sonar_frame, style="bright_white")
    sonar_text.append(f"\nø13-{whale_message}", style="cyan")
    sonar_text.append(f"\nø14-STATUS: ", style="white")
    sonar_text.append(status, style=status_color)
    
    # Timing info display
    sonar_text.append(f"\nø15-[MSG: {whale_message_cycle_seconds}s | STATUS: {whale_status_cycle_seconds}s]", style="dim")
    
    # Whale detection based on configured cycle
    detected_whale = False
    whale_size = 0
    depth = 0
    
    if int(timestamp / whale_detection_cycle_seconds) % 2 == 1 and random.random() < 0.3:
        depth = random.randint(100, 1000)
        whale_size = random.randint(100, 900)
        sonar_text.append(f"\nø16-[WHALE DETECTED] Depth: {depth}m | Size: {whale_size} BTC", style="bright_magenta")
        detected_whale = True
    
    sonar_text.justify = "center"
    
    # Add whale visualization if a whale was detected
    if detected_whale:
        directions = ["→", "←", "↑", "↓", "↗", "↘", "↙", "↖"]
        impacts = ["Low", "Medium", "High"]
        
        # Render the whale visualization panel
        whale_panel = _render_whale_visualization(
            whale_size=whale_size,
            direction=random.choice(directions),
            depth=depth,
            impact=random.choice(impacts)
        )
        
        # Create a column with sonar and whale visualization
        sonar_column = Columns([sonar_text, whale_panel], expand=True)
        return sonar_column
    
    return sonar_text

def _render_price_chart(price_history, volume_history=None, height=10, width=40, is_streaming=False, use_omega=False):
    """Create ASCII price chart visualization similar to the Redis Divine Monitor
    
    Args:
        price_history: List of price data points
        volume_history: List of volume data points
        height: Height of the chart
        width: Width of the chart
        is_streaming: Whether data is streaming or in mockup mode
        use_omega: Whether to use the Omega symbol (Ω) instead of dot (●)
    """
    chart_height = height
    chart_width = width
    
    # Choose the character for price dots
    dot_char = "Ω" if use_omega else "●"
    
    if len(price_history) < 2:
        return Panel(
            Text("Awaiting divine price flow...", style="bright_yellow", justify="center"),
            title="BTCUSDT Divine Flow" + (" (Ω)" if use_omega else ""), 
            border_style="bright_green"
        )
    
    # Use provided volume history or generate random if not provided
    if volume_history is None or len(volume_history) != len(price_history):
        volume_history = [random.uniform(300, 700) for _ in range(len(price_history))]
    
    # Normalize prices to fit chart height
    min_price = min(price_history)
    max_price = max(price_history)
    current_price = price_history[-1]
    price_range = max(0.01, max_price - min_price)  # Avoid division by zero
    
    # Normalize volumes
    min_volume = min(volume_history)
    max_volume = max(volume_history)
    current_volume = volume_history[-1]
    volume_range = max(0.01, max_volume - min_volume)  # Avoid division by zero
    
    # Create a text representation of the chart with colored dots
    chart_lines = []
    for y in range(chart_height):
        line = Text()
        for x in range(chart_width):
            if x < len(price_history[-chart_width:]):
                price = price_history[-chart_width:][x]
                normalized_pos = chart_height - 1 - int((price - min_price) / price_range * (chart_height - 1))
                
                if y == normalized_pos:
                    # Determine dot color based on price
                    if abs(price - max_price) < 0.01:
                        dot = Text(dot_char, style="bright_cyan")  # High price
                    elif abs(price - min_price) < 0.01:
                        dot = Text(dot_char, style="bright_magenta")  # Low price
                    elif abs(price - current_price) < 0.01:
                        dot = Text(dot_char, style="bright_green")  # Current price
                    elif price > (min_price + price_range * 0.7):
                        dot = Text(dot_char, style="cyan")  # Upper range
                    elif price > (min_price + price_range * 0.4):
                        dot = Text(dot_char, style="green")  # Middle range
                    else:
                        dot = Text(dot_char, style="magenta")  # Lower range
                    
                    line = line + dot
                    
                    # Add divine pattern
                    if x > 0 and x % 5 == 0 and random.random() < 0.8 and y != normalized_pos:
                        divine_symbol = random.choice(["✧", "✦", "✴", "⁕", "⚝"])
                        divine_style = random.choice(["bright_yellow", "bright_white", "gold1"])
                        y_random = random.randint(0, chart_height - 1)
                        chart_lines[y_random] = chart_lines[y_random] + Text(divine_symbol, style=divine_style)
                else:
                    line = line + " "
            else:
                line = line + " "
        chart_lines.append(line)
    
    # Combine all lines into a single text object
    chart_text = Text("\n").join(chart_lines)
    
    # Create price info text
    price_info = Text()
    price_info.append(f"Current: ${current_price:.2f}  ", style="bright_green")
    price_info.append(f"High: ${max_price:.2f}  ", style="bright_cyan")
    price_info.append(f"Low: ${min_price:.2f}", style="bright_magenta")
    price_info.justify = "center"
    
    # Choose a random divine wisdom or use default
    divine_index = random.randint(0, len(DIVINE_WISDOM) - 1)
    divine_wisdom = Text(f'"{DIVINE_WISDOM[divine_index]}"', style="bright_cyan")
    divine_wisdom.justify = "center"
    
    # Create divine resonance visualization (▁▂▃▄▅▆▇█)
    # Use resonance formula for random-but-sensible values
    resonance_seed = sum([ord(c) for c in str(current_price)])
    random.seed(resonance_seed)
    resonance = random.uniform(0.1, 0.9)
    random.seed()  # Reset seed
    
    resonance_bars = int(resonance * 10)
    resonance_visual = "▁" * (10 - resonance_bars) + "▂" * resonance_bars
    
    divine_resonance = Text("Divine Resonance: " + resonance_visual, style="bright_yellow")
    divine_resonance.justify = "center"
    
    # Add volume resonance if streaming
    volume_text = Text()
    if is_streaming:
        volume_normalized = (current_volume - min_volume) / volume_range
        volume_bars = int(volume_normalized * 10)
        volume_bars = max(1, min(10, volume_bars))  # Ensure between 1-10
        
        volume_visual = "▁" * (10 - volume_bars) + "▂" * volume_bars
        volume_text = Text(f"Volume Resonance: {volume_visual} ({current_volume:.2f})", style="bright_blue")
        volume_text.justify = "center"
    
    # Combine all elements
    combined_text = Text()
    combined_text = combined_text + chart_text + "\n"
    combined_text = combined_text + price_info + "\n\n"
    combined_text = combined_text + divine_wisdom + "\n\n"
    combined_text = combined_text + divine_resonance
    
    if is_streaming and len(volume_text) > 0:
        combined_text = combined_text + "\n\n" + volume_text
    
    # Add whale sonar if streaming
    if is_streaming:
        whale_sonar_text = _render_whale_sonar(is_streaming=True)
        
        # Handle both Text and Columns return types from _render_whale_sonar
        if isinstance(whale_sonar_text, Text):
            # For standard sonar display (Text object)
            combined_text = combined_text + "\n\n" + whale_sonar_text
        else:
            # For whale detection display (Columns object)
            # Create a new panel with just the chart content
            chart_panel = Panel(
                combined_text,
                title="BTCUSDT Divine Flow" + (" (Ω)" if use_omega else ""),
                border_style="bright_green" if not use_omega else "bright_magenta",
                expand=True
            )
            
            # Return a columns layout with the chart panel and whale display
            return Columns([chart_panel, whale_sonar_text], expand=True)
    
    # Create the final panel
    panel = Panel(
        combined_text,
        title="BTCUSDT Divine Flow" + (" (Ω)" if use_omega else ""),
        border_style="bright_green" if not use_omega else "bright_magenta",
        expand=True
    )
    
    return panel

def create_side_by_side_panels(price_history, volume_history=None, height=8, width=30, is_streaming=False):
    """Create side-by-side comparison of dot and omega panels"""
    # Create the two panels
    dot_panel = _render_price_chart(price_history, volume_history, height, width, is_streaming, use_omega=False)
    omega_panel = _render_price_chart(price_history, volume_history, height, width, is_streaming, use_omega=True)
    
    # Return as a Columns object to display side by side
    return Columns([dot_panel, omega_panel])

def create_compact_mockup():
    """Create a compact static mockup of the panel"""
    # Create a static representation with sample data
    prices = SAMPLE_PRICES[-15:]  # Use fewer prices for compact display
    volumes = SAMPLE_VOLUMES[-15:]  # Use matching volumes
    chart_panel = _render_price_chart(prices, volumes, height=8, width=30, is_streaming=False)
    return chart_panel

def create_comparison_mockup():
    """Create a comparison mockup with both dot and omega panels"""
    prices = SAMPLE_PRICES[-15:]  # Use fewer prices for compact display
    volumes = SAMPLE_VOLUMES[-15:]  # Use matching volumes
    return create_side_by_side_panels(prices, volumes, height=8, width=25, is_streaming=False)

async def demonstrate_expected_panel(use_comparison=False):
    """Show how the BTCUSDT Divine Flow panel should look in a continuous loop"""
    console = Console(width=120)  # Set console width for better display
    
    # Using sample price data to simulate the price history
    prices = SAMPLE_PRICES.copy()
    volumes = SAMPLE_VOLUMES.copy()
    
    # Display control instructions
    console.print("[bold magenta]🔮 Divine Flow Demo - Press Ctrl+C to stop 🔮[/]", justify="center")
    console.print("")
    legend = Text()
    legend.append("Price Colors: ")
    if use_comparison:
        legend.append("●", style="bright_green")
        legend.append("/")
        legend.append("Ω", style="bright_green")
    else:
        legend.append("●", style="bright_green")
    legend.append(" Current  ")
    if use_comparison:
        legend.append("●", style="bright_cyan")
        legend.append("/")
        legend.append("Ω", style="bright_cyan")
    else:
        legend.append("●", style="bright_cyan")
    legend.append(" High  ")
    if use_comparison:
        legend.append("●", style="bright_magenta")
        legend.append("/")
        legend.append("Ω", style="bright_magenta")
    else:
        legend.append("●", style="bright_magenta")
    legend.append(" Low")
    console.print(legend, justify="center")
    console.print("\n[bold yellow]Starting with 'awaiting data stream' mode for 5 seconds...[/]")
    
    try:
        # Run indefinitely until user interrupts
        with Live(refresh_per_second=2, console=console) as live:  # Increased refresh rate
            iteration = 0
            
            # First show a "not streaming" version for 5 seconds
            start_time = time.time()
            while time.time() - start_time < 5:
                if use_comparison:
                    panel = create_side_by_side_panels(prices, volumes, height=8, width=25, is_streaming=False)
                else:
                    panel = _render_price_chart(prices, volumes, height=8, width=30, is_streaming=False)
                live.update(panel)
                await asyncio.sleep(1)
            
            # Then show "now streaming" message and switch to streaming mode
            console.print("[bold green]Connection established - Data now streaming...[/]")
            await asyncio.sleep(1)
            
            # Continue with normal streaming demo
            while True:
                # Add some randomness to the prices to simulate movement
                if iteration > 0:
                    # More dynamic price changes with occasional larger jumps
                    if random.random() < 0.15:  # 15% chance of a bigger move
                        change = random.uniform(-60, 60)
                        # Volume tends to increase with larger price moves
                        volume_change = random.uniform(50, 150) * (1 if change > 0 else -0.5)
                    else:
                        change = random.uniform(-20, 20)
                        # Normal volume changes
                        volume_change = random.uniform(-30, 30)
                    
                    # Ensure volume doesn't go below a minimum
                    new_volume = max(250, volumes[-1] + volume_change)
                    
                    prices.append(prices[-1] + change)
                    volumes.append(new_volume)
                    prices.pop(0)
                    volumes.pop(0)
                
                # Render the price chart panel
                if use_comparison:
                    panel = create_side_by_side_panels(prices, volumes, height=8, width=25, is_streaming=True)
                else:
                    panel = _render_price_chart(prices, volumes, height=8, width=30, is_streaming=True)
                live.update(panel)
                
                # Change update frequency randomly between 0.3-0.7 seconds for more responsive animation
                await asyncio.sleep(random.uniform(0.3, 0.7))
                iteration += 1
    
    except KeyboardInterrupt:
        console.print("\n[bold magenta]Divine flow visualization ended by user[/]")

def show_expected_mockup(use_comparison=False):
    """Show a static mockup of how the panel should look"""
    console = Console(width=120)  # Set console width for better display
    console.print("\n[bold cyan]Expected BTCUSDT Divine Flow Panel:[/]\n")
    
    legend = Text()
    legend.append("Price Colors: ")
    if use_comparison:
        legend.append("●", style="bright_green")
        legend.append("/")
        legend.append("Ω", style="bright_green")
    else:
        legend.append("●", style="bright_green")
    legend.append(" Current  ")
    if use_comparison:
        legend.append("●", style="bright_cyan")
        legend.append("/")
        legend.append("Ω", style="bright_cyan")
    else:
        legend.append("●", style="bright_cyan")
    legend.append(" High  ")
    if use_comparison:
        legend.append("●", style="bright_magenta")
        legend.append("/")
        legend.append("Ω", style="bright_magenta")
    else:
        legend.append("●", style="bright_magenta")
    legend.append(" Low")
    console.print(legend, justify="center")
    console.print("")
    
    # Create a static representation
    if use_comparison:
        panel = create_comparison_mockup()
    else:
        panel = create_compact_mockup()
    console.print(panel)

def show_actual_execution():
    """Provide instructions to run the actual Redis Divine Monitor"""
    console = Console()
    console.print("\n[bold cyan]To see the actual panel in the Redis Divine Monitor:[/]\n")
    console.print("Run the following command:")
    console.print("[bold green]python -m omega_ai.monitor.redis_divine_monitor --symbols btcusdt[/]")
    console.print("\nThis will show the full Redis Divine Monitor with the BTCUSDT Divine Flow panel.")

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="BTCUSDT Divine Flow Demo")
    parser.add_argument('--msg-cycle', type=int, default=DEFAULT_MESSAGE_CYCLE,
                       help=f'Whale message cycle in seconds (default: {DEFAULT_MESSAGE_CYCLE})')
    parser.add_argument('--status-cycle', type=int, default=DEFAULT_STATUS_CYCLE,
                       help=f'Whale status cycle in seconds (default: {DEFAULT_STATUS_CYCLE})')
    parser.add_argument('--detection-cycle', type=int, default=DEFAULT_WHALE_DETECTION_CYCLE,
                       help=f'Whale detection cycle in seconds (default: {DEFAULT_WHALE_DETECTION_CYCLE})')
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_args()
    
    # Set whale sonar timing parameters
    set_whale_sonar_timing(
        message_cycle_seconds=args.msg_cycle,
        status_cycle_seconds=args.status_cycle,
        detection_cycle_seconds=args.detection_cycle
    )
    
    console = Console(width=120)  # Wider console for side-by-side display
    console.print("[bold magenta]🔮 BTCUSDT Divine Flow Panel Demo 🔮[/]", justify="center")
    
    # Display whale sonar timing settings
    console.print(f"[cyan]Whale Sonar Settings: Message Cycle: {whale_message_cycle_seconds}s | " +
                 f"Status Cycle: {whale_status_cycle_seconds}s | " +
                 f"Detection Cycle: {whale_detection_cycle_seconds}s[/]")
    
    # Show side-by-side comparison mockup
    show_expected_mockup(use_comparison=True)
    
    # Provide instructions for running the actual monitor
    show_actual_execution()
    
    # Ask if user wants to see the live demo
    console.print("\n[bold cyan]Do you want to see a continuous live demonstration? (y/n)[/]")
    console.print("[bold yellow]Note: Press Ctrl+C to stop the demo when running[/]")
    response = input()
    
    if response.lower() in ['y', 'yes']:
        try:
            # Run the demo with side-by-side comparison
            asyncio.run(demonstrate_expected_panel(use_comparison=True))
        except KeyboardInterrupt:
            console.print("\n[bold magenta]Demo ended.[/]")
    else:
        console.print("\n[bold magenta]Demo ended.[/]") 