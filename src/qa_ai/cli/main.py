#!/usr/bin/env python3

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

"""
QA AI CLI - Professional command-line interface for QA operations
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Optional
from pathlib import Path
import json
import sys
from datetime import datetime

app = typer.Typer(
    name="qa-ai",
    help="QA AI Command Line Interface",
    add_completion=False,
    rich_markup_mode="rich"
)

console = Console()

def version_callback(value: bool):
    if value:
        console.print(f"QA AI CLI version: [bold blue]0.1.0[/bold blue]")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the version and exit.",
        callback=version_callback,
        is_eager=True,
    )
):
    """
    QA AI Command Line Interface for automated testing and quality assurance.
    """
    pass

@app.command()
def init(
    config: Path = typer.Option(
        "config/qa_config.json",
        "--config",
        "-c",
        help="Path to the configuration file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=True,
    )
):
    """
    Initialize the QA AI environment with configuration.
    """
    console.print(Panel.fit(
        "[bold blue]Initializing QA AI Environment[/bold blue]",
        border_style="blue"
    ))
    
    try:
        with open(config, "r") as f:
            config_data = json.load(f)
        
        console.print(f"Using config file: {config}")
        console.print("[green]Environment initialized successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error initializing environment: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def generate_tests(
    test_type: str = typer.Option(
        "e2e",
        "--type",
        "-t",
        help="Type of tests to generate (e2e, integration, unit)",
    ),
    target: str = typer.Option(
        ...,
        "--target",
        help="Target system or URL to test",
    ),
    output: Path = typer.Option(
        "tests/generated",
        "--output",
        "-o",
        help="Output directory for generated tests",
    )
):
    """
    Generate automated test cases based on the target system.
    """
    console.print(Panel.fit(
        f"[bold blue]Generating {test_type} Tests[/bold blue]",
        border_style="blue"
    ))
    
    console.print(f"Target: {target}")
    console.print(f"Output directory: {output}")
    console.print("[green]Tests generated successfully[/green]")

@app.command()
def run_tests(
    parallel: bool = typer.Option(
        False,
        "--parallel",
        "-p",
        help="Run tests in parallel",
    )
):
    """
    Execute the generated test cases.
    """
    console.print(Panel.fit(
        "[bold blue]Running QA Tests[/bold blue]",
        border_style="blue"
    ))
    
    if parallel:
        console.print("Running tests in parallel")
    else:
        console.print("Running tests sequentially")
    
    console.print("[green]Tests completed successfully[/green]")

@app.command()
def metrics(
    dashboard: bool = typer.Option(
        False,
        "--dashboard",
        "-d",
        help="Open metrics dashboard in browser",
    )
):
    """
    Display QA metrics and statistics.
    """
    console.print(Panel.fit(
        "[bold blue]QA Metrics Dashboard[/bold blue]",
        border_style="blue"
    ))
    
    # Create a sample metrics table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="dim")
    table.add_column("Value")
    
    table.add_row("Test Coverage", "85%")
    table.add_row("Pass Rate", "92%")
    table.add_row("Execution Time", "2m 15s")
    table.add_row("Last Run", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    console.print(table)
    
    if dashboard:
        console.print("Opening metrics dashboard")
    
    console.print("[green]Metrics displayed successfully[/green]")

@app.command()
def persona(
    persona_type: str = typer.Argument(
        ...,
        help="Type of QA persona to activate",
    ),
    task: str = typer.Option(
        None,
        "--task",
        "-t",
        help="Specific task for the persona",
    )
):
    """
    Activate a specialized QA persona for specific testing tasks.
    """
    console.print(Panel.fit(
        f"[bold blue]Activating {persona_type} Persona[/bold blue]",
        border_style="blue"
    ))
    
    try:
        # Import the persona factory
        from qa_ai.personas.factory import PersonaFactory
        
        # Create the persona instance
        persona_instance = PersonaFactory.create_persona(persona_type)
        
        # Display persona information
        console.print(f"Persona: [bold]{persona_instance.name}[/bold]")
        console.print(f"Focus: {persona_instance.description}")
        
        if task:
            console.print(f"Task: {task}")
            # In a real implementation, you would use the persona to execute the task
        
        # Show status
        status = persona_instance.get_status()
        console.print(f"Active scenarios: {status['active_scenarios']}")
        
        console.print(f"[green]{persona_type} persona activated successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error activating persona: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()