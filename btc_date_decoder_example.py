#!/usr/bin/env python3
"""
OMEGA BTC AI - BTC Date Decoder Example
======================================

This script demonstrates the Bitcoin date decoder functionality
by analyzing October 29, 2023 and displaying the results.

Copyright (C) 2024 OMEGA BTC AI Team
License: GNU General Public License v3.0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

Author: OMEGA BTC AI Team
Version: 1.0
"""

import sys
import json
from datetime import datetime
import pytz
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from omega_ai.utils.btc_date_decoder import analyze_date, analyze_october_29_2023

# Initialize Rich console
console = Console()

def format_fibonacci_level(level):
    """Format Fibonacci level for display."""
    if not level or level == "Unknown":
        return "[dim]Unknown[/dim]"
    return level

def display_header():
    """Display script header."""
    console.print(Panel(
        "[bold yellow]OMEGA BTC AI[/bold yellow] - [bold cyan]BTC Date Decoder[/bold cyan]",
        subtitle="[italic]JAH BLESS the eternal flow of time and markets[/italic]",
        box=box.DOUBLE,
        expand=False
    ))

def display_btc_age(age_data):
    """Display Bitcoin age information."""
    console.print(Panel(
        f"[bold green]Bitcoin Age:[/bold green] {age_data['years']} years, {age_data['months']} months, {age_data['days']} days\n"
        f"[bold green]Total Days:[/bold green] {age_data['total_days']} days since genesis block",
        title="[bold]BTC AGE[/bold]",
        border_style="green",
        box=box.ROUNDED
    ))

def display_halving_phase(halving_data):
    """Display halving phase information."""
    if halving_data.get("start_date") and halving_data.get("end_date"):
        start = halving_data["start_date"].strftime("%Y-%m-%d")
        end = halving_data["end_date"].strftime("%Y-%m-%d")
        days_passed = halving_data["days_passed"]
        days_remaining = halving_data["days_remaining"]
        percentage = halving_data["percentage_complete"]
        
        progress_bar = create_progress_bar(percentage)
        
        console.print(Panel(
            f"[bold magenta]Cycle:[/bold magenta] {halving_data['cycle_name']}\n"
            f"[bold magenta]Period:[/bold magenta] {start} to {end}\n"
            f"[bold magenta]Progress:[/bold magenta] {progress_bar} {percentage:.1f}%\n"
            f"[bold magenta]Days passed:[/bold magenta] {days_passed} | [bold magenta]Days remaining:[/bold magenta] {days_remaining}\n"
            f"[bold magenta]Fibonacci Phase:[/bold magenta] {format_fibonacci_level(halving_data['fibonacci_level'])}",
            title="[bold]HALVING CYCLE[/bold]",
            border_style="magenta",
            box=box.ROUNDED
        ))

def create_progress_bar(percentage, width=20):
    """Create a visual progress bar."""
    filled = int(width * percentage / 100)
    bar = f"[{'█' * filled}{' ' * (width - filled)}]"
    if percentage < 33:
        return f"[red]{bar}[/red]"
    elif percentage < 66:
        return f"[yellow]{bar}[/yellow]"
    else:
        return f"[green]{bar}[/green]"

def display_market_cycles(cycles_data):
    """Display market cycles information."""
    table = Table(title="[bold]MARKET CYCLES[/bold]", box=box.ROUNDED)
    table.add_column("Cycle Type", style="cyan")
    table.add_column("Length", style="blue")
    table.add_column("Phase", style="magenta")
    table.add_column("Days In/Out", style="green")
    table.add_column("Description", style="yellow")
    
    for cycle_name, data in cycles_data.items():
        phase_percentage = data["phase_percentage"]
        progress = create_progress_bar(phase_percentage, width=10)
        
        table.add_row(
            cycle_name.capitalize(),
            f"{data['cycle_length_days']} days",
            f"{progress} {phase_percentage:.1f}%",
            f"{data['days_into_cycle']}/{data['days_remaining']}",
            data["phase_description"]
        )
    
    console.print(table)

def display_time_alignment(alignment_data):
    """Display temporal alignment information."""
    harmony = alignment_data["overall_temporal_harmony"] * 100
    harmony_color = "red" if harmony < 33 else "yellow" if harmony < 66 else "green"
    
    table = Table(title="[bold]TEMPORAL GOLDEN RATIO ALIGNMENT[/bold]", box=box.ROUNDED)
    table.add_column("Time Scale", style="cyan")
    table.add_column("Phase", style="blue")
    table.add_column("Alignment", style="green")
    
    table.add_row(
        "Day",
        f"{alignment_data['day_cycle_phase']:.3f}",
        f"{create_progress_bar(alignment_data['day_golden_ratio_alignment']*100, width=10)} {alignment_data['day_golden_ratio_alignment']*100:.1f}%"
    )
    
    table.add_row(
        "Week",
        f"{alignment_data['week_cycle_phase']:.3f}",
        f"{create_progress_bar(alignment_data['week_golden_ratio_alignment']*100, width=10)} {alignment_data['week_golden_ratio_alignment']*100:.1f}%"
    )
    
    table.add_row(
        "Month",
        f"{alignment_data['month_phase']:.3f}",
        f"{create_progress_bar(alignment_data['month_golden_ratio_alignment']*100, width=10)} {alignment_data['month_golden_ratio_alignment']*100:.1f}%"
    )
    
    table.add_row(
        "Year",
        f"{alignment_data['year_phase']:.3f}",
        f"{create_progress_bar(alignment_data['year_golden_ratio_alignment']*100, width=10)} {alignment_data['year_golden_ratio_alignment']*100:.1f}%"
    )
    
    console.print(table)
    
    console.print(Panel(
        f"[bold {harmony_color}]Overall Harmony:[/bold {harmony_color}] {create_progress_bar(harmony, width=20)} {harmony:.1f}%\n"
        f"[bold {harmony_color}]Description:[/bold {harmony_color}] {alignment_data['harmony_description']}",
        border_style=harmony_color,
        box=box.ROUNDED
    ))

def display_divine_score(score, rating):
    """Display divine date score."""
    score_percentage = score * 100
    score_color = "red" if score_percentage < 33 else "yellow" if score_percentage < 66 else "green"
    
    console.print(Panel(
        f"[bold {score_color}]Divine Date Score:[/bold {score_color}] {create_progress_bar(score_percentage, width=30)} {score_percentage:.1f}%\n"
        f"[bold {score_color}]Rating:[/bold {score_color}] {rating}",
        title="[bold]DIVINE DATE RATING[/bold]",
        border_style=score_color,
        box=box.DOUBLE
    ))

def display_specific_btc_data(btc_data):
    """Display specific BTC data for the analyzed date."""
    if not btc_data:
        return
    
    console.print(Panel(
        f"[bold yellow]Closing Price:[/bold yellow] ${btc_data['closing_price']:,.2f}\n"
        f"[bold yellow]Market Cap:[/bold yellow] ${btc_data['market_cap']/1e9:,.2f} billion\n"
        f"[bold yellow]24h Change:[/bold yellow] {'+' if btc_data['24h_change'] > 0 else ''}{btc_data['24h_change']}%\n",
        title="[bold]BTC MARKET DATA[/bold]",
        border_style="yellow",
        box=box.ROUNDED
    ))
    
    # Display significant events
    events_panel = Panel(
        "\n".join(f"• {event}" for event in btc_data['significant_events']),
        title="[bold]SIGNIFICANT EVENTS[/bold]",
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(events_panel)
    
    # Display numerological significance
    numerology_panel = Panel(
        "\n".join(f"• {item}" for item in btc_data['numerological_significance']),
        title="[bold]NUMEROLOGICAL SIGNIFICANCE[/bold]",
        border_style="magenta",
        box=box.ROUNDED
    )
    console.print(numerology_panel)
    
    # Display market cycle context
    context_panel = Panel(
        "\n".join(f"• {item}" for item in btc_data['market_cycle_context']),
        title="[bold]MARKET CYCLE CONTEXT[/bold]",
        border_style="green",
        box=box.ROUNDED
    )
    console.print(context_panel)

def display_conclusion():
    """Display conclusion message."""
    console.print(Panel(
        "[bold yellow]JAH JAH BLESS THE ETERNAL FLOW OF TIME AND MARKETS.[/bold yellow]\n"
        "[italic]May this insight illuminate the sacred patterns intertwining our temporal journey with the rhythm of Bitcoin.[/italic]",
        border_style="yellow",
        box=box.DOUBLE
    ))

def main():
    """Main function to demonstrate BTC date decoder."""
    display_header()
    
    # Analyze October 29, 2023
    console.print("\n[bold]Analyzing October 29, 2023...[/bold]\n")
    analysis = analyze_october_29_2023()
    
    console.print(f"[bold cyan]Date:[/bold cyan] {analysis['date_str']}\n")
    
    # Display components
    display_btc_age(analysis["btc_age"])
    console.print()
    
    display_halving_phase(analysis["halving_phase"])
    console.print()
    
    display_market_cycles(analysis["market_cycles"])
    console.print()
    
    display_time_alignment(analysis["time_alignment"])
    console.print()
    
    display_divine_score(analysis["divine_date_score"], analysis["divine_date_rating"])
    console.print()
    
    # Display specific BTC data for October 29, 2023
    if "specific_btc_data" in analysis:
        display_specific_btc_data(analysis["specific_btc_data"])
        console.print()
    
    display_conclusion()
    
    # Option to analyze another date
    console.print("\n[bold]Would you like to analyze another date? (y/n)[/bold]")
    response = input().lower().strip()
    
    if response == 'y':
        console.print("\n[bold]Enter a date in YYYY-MM-DD format:[/bold]")
        date_str = input().strip()
        
        try:
            new_analysis = analyze_date(date_str=date_str)
            
            console.clear()
            display_header()
            
            console.print(f"\n[bold cyan]Date:[/bold cyan] {new_analysis['date_str']}\n")
            
            display_btc_age(new_analysis["btc_age"])
            console.print()
            
            display_halving_phase(new_analysis["halving_phase"])
            console.print()
            
            display_market_cycles(new_analysis["market_cycles"])
            console.print()
            
            display_time_alignment(new_analysis["time_alignment"])
            console.print()
            
            display_divine_score(new_analysis["divine_date_score"], new_analysis["divine_date_rating"])
            console.print()
            
            display_conclusion()
            
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == "__main__":
    main() 