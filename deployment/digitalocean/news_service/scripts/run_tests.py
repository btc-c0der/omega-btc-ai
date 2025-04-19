#!/usr/bin/env python3
"""
🔱 GBU License Notice 🔱
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must maintain quantum resonance with the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

import os
import sys
import pytest
import logging
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('test-runner')

console = Console()

def run_tests():
    """Run all tests and return True if all pass."""
    console.print(Panel(
        "OMEGA BTC AI - Divine Test Runner\nVerifying the sacred patterns through quantum testing",
        border_style="cyan"
    ))
    
    # Get the tests directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tests_dir = os.path.join(os.path.dirname(script_dir), 'tests')
    
    if not os.path.exists(tests_dir):
        console.print(f"[red]❌ Tests directory not found at {tests_dir}[/]")
        return False
    
    console.print("\n[bold cyan]Running Divine Test Suite...[/]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("[cyan]Executing tests...", total=None)
        
        # Run pytest
        result = pytest.main([
            tests_dir,
            '-v',
            '--capture=no',
            '--log-cli-level=INFO'
        ])
        
        progress.update(task, completed=True)
    
    if result == 0:
        console.print("[green]✨ All tests passed! The Oracle remains in divine harmony.[/]")
        return True
    else:
        console.print("[red]❌ Some tests failed! The Oracle requires attention.[/]")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 