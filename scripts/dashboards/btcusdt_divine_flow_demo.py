#!/usr/bin/env python

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

def _render_whale_sonar(is_streaming=False, custom_text=None):
    """Render the whale sonar section of the panel
    
    Args:
        is_streaming: Whether data is streaming or in awaiting state
        custom_text: Optional custom text to override default rendering
    
    Returns:
        Text: The formatted whale sonar text
    """
    if custom_text is not None:
        return custom_text
        
    # Default rendering if no custom text is provided
    whale_sonar_text = Text()
    
    # Only show whale sonar in streaming mode
    if is_streaming:
        # Animation frames for sonar - use all 4 frames for a more dynamic animation
        frames = ["◟   ◞", "◜   ◝", "◠───◠", "◡───◡"]
        frame_index = int(time.time() * 2) % len(frames)  # Faster animation speed
        frame = frames[frame_index]
        
        status_options = [
            "Minor ripples. Small accumulation observed.",
            "Calm waters. No large movements detected.", 
            "Moderate activity. Watching closely.",
            "Significant volume detected. Alert raised."
        ]
        
        msg_options = [
            "Divine protection for the ocean's largest traders",
            "Monitoring market depths for benevolent whales",
            "No harmful trading patterns detected in these waters",
            "Whale sanctuary established in these market depths"
        ]
        
        # Choose messages based on time
        status_idx = int(time.time() / whale_status_cycle_seconds) % len(status_options)
        msg_idx = int(time.time() / whale_message_cycle_seconds) % len(msg_options)
        
        current_status = status_options[status_idx]
        current_msg = msg_options[msg_idx]
        
        # Add the whale sonar components
        whale_sonar_text.append("\nø11-SEA SHEPHERD CLI Ω MODULE\n", style="bright_cyan bold")
        whale_sonar_text.append(f"ø12-WHALE SONAR: [ACTIVE] {frame}\n", style="bright_green")
        whale_sonar_text.append(f"ø13-{current_msg}\n", style="bright_yellow")
        whale_sonar_text.append(f"ø14-STATUS: {current_status}\n", style="bright_white")
        whale_sonar_text.append(f"ø15-[MSG: {whale_message_cycle_seconds}s | STATUS: {whale_status_cycle_seconds}s]\n", style="bright_yellow")
        
        # Add whale detection if time is right
        detection_phase = (time.time() % whale_detection_cycle_seconds) / whale_detection_cycle_seconds
        if detection_phase < 0.3:  # Show detection 30% of the time
            whale_size = random.randint(250, 750)
            depth = random.randint(300, 600)
            whale_sonar_text.append(f"\nø16-[WHALE DETECTED] Depth: {depth}m | Size: {whale_size} BTC\n", style="bright_red")
    else:
        # Awaiting data stream
        whale_sonar_text.append("\nWhale Sonar: STANDBY (awaiting data stream)\n", style="dim_grey")
        whale_sonar_text.append("Connect to Redis for advanced whale detection\n", style="dim_grey")
    
    return whale_sonar_text

def _render_price_chart(price_history, volume_history=None, height=10, width=40, is_streaming=False, use_omega=False, whale_sonar_text=None):
    """Render a price chart with colored dots based on price levels
    
    Args:
        price_history: List of price points
        volume_history: List of volume points (optional)
        height: Height of the chart
        width: Width of the chart
        is_streaming: Whether data is streaming or in awaiting state
        use_omega: Whether to use Omega symbols instead of dots
        whale_sonar_text: Optional custom whale sonar text
    
    Returns:
        Panel: Rich panel containing the price chart
    """
    if len(price_history) < 2:
        return Panel("Insufficient data for visualization")
        
    # Extract the prices we'll use for the chart
    prices_to_plot = price_history[-width:]
    
    # Calculate min/max for Y-axis scale
    max_price = max(prices_to_plot)
    min_price = min(prices_to_plot)
    price_range = max_price - min_price
    
    # Make sure there is a range to avoid division by zero
    if price_range == 0:
        price_range = 1
    
    # Current price is the most recent price
    current_price = prices_to_plot[-1]
    
    # Create a list of chart rows using Text objects
    chart_rows = []
    for i in range(height):
        # Calculate the price at this row
        row_price = max_price - (i / (height - 1)) * price_range
        
        # Create a new row as a Text object
        row = Text()
        for j, price in enumerate(prices_to_plot):
            # Only plot if we have enough prices
            if j < len(prices_to_plot):
                # Determine if this price should be plotted at this height
                # We need price to be within 1/height of the row price
                price_step = price_range / height
                if abs(price - row_price) < price_step / 2:
                    # Use Omega symbol if requested
                    symbol = "Ω" if use_omega else "●"
                    
                    # Determine color based on price value
                    if abs(price - current_price) < price_step / 2:
                        color = "bright_green"  # Current price
                    elif price >= (max_price - price_range * 0.2):
                        color = "bright_cyan"   # High prices (top 20%)
                    elif price <= (min_price + price_range * 0.2):
                        color = "bright_magenta"  # Low prices (bottom 20%)
                    else:
                        # Create a gradient color for prices in between
                        # Higher values closer to cyan, lower values closer to magenta
                        normalized = (price - min_price) / price_range
                        if normalized > 0.5:
                            # Upper half - blend from green to cyan
                            blend = (normalized - 0.5) * 2  # 0 to 1
                            color = "bright_green" if blend < 0.5 else "bright_cyan"
                        else:
                            # Lower half - blend from magenta to green
                            blend = normalized * 2  # 0 to 1
                            color = "bright_magenta" if blend < 0.5 else "bright_green"
                    
                    # Add the symbol with color using Text object methods
                    row.append(symbol, style=color)
                else:
                    row.append(" ")
            else:
                row.append(" ")
        
        # Add the row to the chart
        chart_rows.append(row)
    
    # Create the chart text by joining the rows
    chart_text = Text()
    for i, row in enumerate(chart_rows):
        chart_text.append(row)
        if i < len(chart_rows) - 1:
            chart_text.append("\n")
    
    # Add price metrics
    price_info = Text(f"\nCurrent: ${current_price:.2f}  High: ${max_price:.2f}  Low: ${min_price:.2f}\n\n")
    price_info.stylize("bright_green", 0, 8)  # Style "Current:"
    price_info.stylize("bright_green", 9, 9 + len(f"${current_price:.2f}"))
    price_info.stylize("bright_cyan", 9 + len(f"${current_price:.2f}") + 2, 9 + len(f"${current_price:.2f}") + 2 + 5)  # Style "High:"
    price_info.stylize("bright_cyan", 9 + len(f"${current_price:.2f}") + 2 + 6, 9 + len(f"${current_price:.2f}") + 2 + 6 + len(f"${max_price:.2f}"))
    price_info.stylize("bright_magenta", 9 + len(f"${current_price:.2f}") + 2 + 6 + len(f"${max_price:.2f}") + 2, 9 + len(f"${current_price:.2f}") + 2 + 6 + len(f"${max_price:.2f}") + 2 + 4)  # Style "Low:"
    price_info.stylize("bright_magenta", 9 + len(f"${current_price:.2f}") + 2 + 6 + len(f"${max_price:.2f}") + 2 + 5, 9 + len(f"${current_price:.2f}") + 2 + 6 + len(f"${max_price:.2f}") + 2 + 5 + len(f"${min_price:.2f}"))
    
    # Get divine wisdom
    divine_wisdom = _generate_divine_wisdom()
    wisdom_text = Text(f'"{divine_wisdom}"\n\n')
    wisdom_text.stylize("bright_cyan")
    
    # Create divine resonance
    if is_streaming:
        resonance = Text("Divine Resonance: ")
        # Generate a resonance bar with 10 segments
        resonance_level = random.randint(1, 10)
        for i in range(10):
            if i < resonance_level:
                segment = "▂"
            else:
                segment = "▁"
            resonance.append(segment, style="bright_yellow")
    else:
        resonance = Text("Divine Resonance: ▁▁▁▁▁▁▁▁▁▁ (awaiting data stream)")
        resonance.stylize("dim_grey")
    
    # Add volume resonance if volume history is provided
    if volume_history and len(volume_history) > 0:
        # Get the last volume for display
        last_volume = volume_history[-1]
        
        resonance.append("\n\n")  # Add spacing
        
        if is_streaming:
            volume_text = Text("Volume Resonance: ")
            # Generate a volume bar with 10 segments
            volume_level = random.randint(1, 10)
            for i in range(10):
                if i < volume_level:
                    segment = "▂"
                else:
                    segment = "▁"
                volume_text.append(segment, style="bright_blue")
            volume_text.append(f" ({last_volume:.2f})", style="bright_blue")
        else:
            volume_text = Text("Volume Resonance: ▁▁▁▁▁▁▁▁▁▁ (awaiting data stream)")
            volume_text.stylize("dim_grey")
        
        resonance.append(volume_text)
    
    # Combine all elements
    combined_text = Text()
    combined_text.append(chart_text)
    combined_text.append(price_info)
    combined_text.append(wisdom_text)
    combined_text.append(resonance)
    combined_text.append("\n\n")
    
    # Add the whale sonar if we're in streaming mode
    if is_streaming:
        # Use custom whale sonar text if provided, otherwise generate default
        whale_sonar_text = whale_sonar_text if whale_sonar_text else _render_whale_sonar(is_streaming=True)
        
        # Handle both Text and string types
        if isinstance(whale_sonar_text, Text):
            combined_text.append(whale_sonar_text)
        else:
            combined_text.append(whale_sonar_text)
    
    # Create the panel with the appropriate title and styling
    title = "BTCUSDT Divine Flow (Ω)" if use_omega else "BTCUSDT Divine Flow"
    style = "bright_magenta" if use_omega else "bright_blue"
    
    panel = Panel(
        combined_text,
        title=title,
        border_style=style,
        width=width+30
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
    """Demonstrate the expected panel with live updates"""
    console = Console(width=120)  # Set wider console for better visualization
    console.print(f"[bright_magenta]Demonstrating live panel...[/]")
    console.print("[bright_yellow]Press Ctrl+C to exit[/]")
    
    # Use our sample price data as a starting point
    prices = SAMPLE_PRICES.copy()
    volumes = SAMPLE_VOLUMES.copy()
    
    # Track update timing for components
    update_counter = 0
    chart_update_frequency = 2  # More frequent chart updates for better flow
    
    # Animation state for the scanning dots
    scanning_dots_state = 0
    scanning_dots = [".", "..", "..."]
    
    # Sonar animation frames - restore the full 4-frame animation
    sonar_frames = ["◟   ◞", "◜   ◝", "◠───◠", "◡───◡"]
    
    # Create a collection of sonar messages for ø13
    sonar_messages = [
        "Divine protection for the ocean's largest traders",
        "Monitoring market depths for benevolent whales",
        "No harmful trading patterns detected in these waters",
        "Watching for predatory market manipulation",
        "Scanning market depths for significant movements",
        "The divine sonar detects ripples in the cosmic ocean",
        "Protecting gentle giants from market predators",
        "Whale sanctuary established in these market depths"
    ]
    
    # Initialize status messages for ø14
    status_messages = [
        "STATUS: Calm waters. No large movements detected.",
        "STATUS: Minor ripples. Small accumulation observed.",
        "STATUS: Moderate activity. Watching closely.",
        "STATUS: Increased activity detected. Alert level raised.",
        "STATUS: Large movements detected. Divine protection activated."
    ]
    
    # Initialize message and status
    current_message = random.choice(sonar_messages)
    current_status = random.choice(status_messages)
    
    try:
        while True:
            # Update data every iteration
            last_price = prices[-1]
            price_change = random.uniform(-0.5, 0.5)
            
            # Occasionally make a larger move (15% chance)
            if random.random() < 0.15:
                price_change = random.uniform(-2.0, 2.0)
                
            # Ensure price stays realistic
            new_price = max(10, last_price + price_change)
            prices.append(new_price)
            
            # Keep dataset at manageable size
            if len(prices) > 100:
                prices = prices[-100:]
                
            # Update volume data
            last_volume = volumes[-1]
            volume_change = random.uniform(-50, 50)
            new_volume = max(50, last_volume + volume_change)
            volumes.append(new_volume)
            
            if len(volumes) > 100:
                volumes = volumes[-100:]
            
            # Update panel more frequently for a better flow
            should_update_panel = (update_counter % chart_update_frequency) == 0
            
            if should_update_panel or update_counter == 0:
                # Update animation elements
                
                # Update scanning dots animation (ø13)
                scanning_dots_state = (scanning_dots_state + 1) % len(scanning_dots)
                scanning_suffix = scanning_dots[scanning_dots_state]
                
                # Change sonar message every 6 updates (ø13)
                if update_counter % 6 == 0:
                    current_message = random.choice(sonar_messages)
                
                # Change status message every 10 updates (ø14)
                if update_counter % 10 == 0:
                    current_status = random.choice(status_messages)
                
                # Create custom whale sonar section with styled components
                whale_sonar_text = Text()
                
                # ø11 - Static title with title styling
                whale_sonar_text.append("\nø11-SEA SHEPHERD CLI Ω MODULE\n", style="bright_cyan bold")
                
                # ø12 - Active subtitle with full 4-frame animation
                # Use the full animation sequence instead of just alternating between two frames
                sonar_frame = sonar_frames[update_counter % len(sonar_frames)]
                whale_sonar_text.append(f"ø12-WHALE SONAR: [ACTIVE] {sonar_frame}\n", style="bright_green")
                
                # ø13 - Scanning with dots progress bar
                whale_sonar_text.append(f"ø13-{current_message}{scanning_suffix}\n", style="bright_yellow")
                
                # ø14 - Status refreshes as per sonar reading
                whale_sonar_text.append(f"ø14-{current_status}\n", style="bright_white")
                
                # ø15 - Current timing info
                whale_sonar_text.append("ø15-[MSG: 3s | STATUS: 5s]\n", style="bright_yellow")
                
                # Render the Omega panel with full functionality and custom whale sonar
                panel = _render_price_chart(
                    prices, volumes, 
                    height=12,  # Taller chart for better visualization
                    width=50,   # Wider chart for more detail
                    is_streaming=True, 
                    use_omega=True,
                    whale_sonar_text=whale_sonar_text  # Pass custom whale sonar text
                )
                
                # Display the panel
                console.print(panel)
            
            # Increment counter
            update_counter += 1
            
            # Sleep for a shorter time for smoother animation
            await asyncio.sleep(random.uniform(0.2, 0.6))
            
    except KeyboardInterrupt:
        console.print("[bright_yellow]Demonstration ended.[/]")
        return

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
    parser.add_argument("--msg-cycle", type=int, default=DEFAULT_MESSAGE_CYCLE,
                        help=f"Whale message cycle in seconds (default: {DEFAULT_MESSAGE_CYCLE})")
    parser.add_argument("--status-cycle", type=int, default=DEFAULT_STATUS_CYCLE,
                        help=f"Whale status cycle in seconds (default: {DEFAULT_STATUS_CYCLE})")
    parser.add_argument("--detection-cycle", type=int, default=DEFAULT_WHALE_DETECTION_CYCLE,
                        help=f"Whale detection cycle in seconds (default: {DEFAULT_WHALE_DETECTION_CYCLE})")
    parser.add_argument("--comparison", action="store_true",
                        help="Show side-by-side comparison of regular and Omega panels")
    return parser.parse_args()

async def main():
    """Run the btcusdt_divine_flow_demo.py script"""
    # Parse command line arguments
    args = parse_args()
    
    # Set timing parameters for whale sonar
    set_whale_sonar_timing(
        message_cycle_seconds=args.msg_cycle,
        status_cycle_seconds=args.status_cycle,
        detection_cycle_seconds=args.detection_cycle
    )
    
    # Print settings
    print(f"🔮 BTCUSDT Divine Flow Panel Demo 🔮".center(80))
    print(f"Whale Sonar Settings: Message Cycle: {args.msg_cycle}s | Status Cycle: {args.status_cycle}s | Detection Cycle: {args.detection_cycle}s\n")
    
    # Show expected panel mockup
    print(f"Expected BTCUSDT Divine Flow Panel:")
    show_expected_mockup(use_comparison=False)  # Always use single panel mode
    
    # Prompt user if they want to see live demonstration
    user_input = input("\nDo you want to see a live demonstration? (y/n): ")
    if user_input.lower() in ['y', 'yes']:
        await demonstrate_expected_panel(use_comparison=False)  # Always use single panel mode
    
    # Show instructions for running actual monitor
    print("\nTo run the actual Redis Divine Monitor:")
    show_actual_execution()

def _generate_divine_wisdom():
    """Generate a random piece of divine wisdom for the chart"""
    wisdom_quotes = [
        "The wise trader observes more and acts less",
        "Buy fear, sell euphoria - the eternal divine law",
        "The market flows in divine patterns beyond mortal comprehension",
        "True profit comes from alignment with cosmic market cycles",
        "When Bitcoin ascends, altcoins follow the divine path",
        "Market volatility is merely the breath of the cosmic trader",
        "The patient accumulator receives the greatest divine rewards",
        "Alignment with cosmic cycles brings trader enlightenment",
        "The divine pattern reveals itself to those who wait",
        "In market turbulence, find the eye of the divine storm",
        "Zoom out to see the divine pattern, zoom in to find entry",
        "Greed and fear are the clouds that obscure divine vision",
        "The cosmic trader waits for confluence of multiple timeframes",
        "Divine patience is the greatest trading strategy",
        "Ride the cosmic wave, do not fight its flow"
    ]
    return random.choice(wisdom_quotes)

if __name__ == "__main__":
    asyncio.run(main()) 