#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"""
Divine Book Dependencies Test Script

This script checks if all the required dependencies for the Divine Book components
are properly installed and accessible.
"""

import sys
import importlib.util
from rich.console import Console
from rich.table import Table

def check_dependency(name, required=True):
    """Check if a dependency is installed."""
    spec = importlib.util.find_spec(name)
    if spec is not None:
        # Module exists, try to import it
        try:
            module = importlib.import_module(name)
            if hasattr(module, '__version__'):
                version = module.__version__
            else:
                version = "Unknown"
            return True, version
        except ImportError:
            return False, None
    else:
        return False, None

def main():
    """Check all required dependencies and print a report."""
    console = Console()

    console.print("\n[bold cyan]🔍 Divine Book Dependencies Test[/bold cyan]\n")
    
    # Required dependencies
    required_deps = [
        "gradio",
        "numpy",
        "matplotlib",
        "mistune",
        "pygments",
        "rich",
    ]
    
    # Optional dependencies
    optional_deps = [
        "tqdm",
        "pandas",
        "scikit-learn",
    ]
    
    # Create a table for the results
    table = Table(title="Dependency Check Results")
    table.add_column("Package", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Version", style="yellow")
    table.add_column("Required", style="magenta")
    
    # Check each dependency
    missing_required = False
    
    for dep in required_deps:
        installed, version = check_dependency(dep)
        table.add_row(
            dep,
            "✅ Installed" if installed else "❌ Missing",
            version or "N/A",
            "Yes"
        )
        if not installed:
            missing_required = True
    
    for dep in optional_deps:
        installed, version = check_dependency(dep)
        table.add_row(
            dep,
            "✅ Installed" if installed else "⚠️ Not found",
            version or "N/A",
            "No"
        )
    
    # Print the results
    console.print(table)
    
    # Summary
    if missing_required:
        console.print("\n[bold red]❌ Some required dependencies are missing![/bold red]")
        console.print("Please install them using the following command:")
        console.print("[yellow]pip install -r requirements.txt[/yellow]\n")
        return 1
    else:
        console.print("\n[bold green]✅ All required dependencies are installed![/bold green]")
        console.print("You can now run the Divine Book components with:")
        console.print("[yellow]python run_divine_book.py --mode [dashboard|browser][/yellow]\n")
        return 0

if __name__ == "__main__":
    sys.exit(main()) 