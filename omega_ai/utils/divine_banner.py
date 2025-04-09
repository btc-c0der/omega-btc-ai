#!/usr/bin/env python3
"""
🔱 OMEGA BTC AI - Divine Banner Module
📜 GPU²: General Public Universal + Graphics Processing Unison
🔐 Divine Copyright (c) 2025 - OMEGA Collective
"""

import os
import sys
from typing import Optional
from datetime import datetime

class Colors:
    """Sacred color codes for divine terminal output"""
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DivineSymbols:
    """Sacred ASCII art for divine terminal output"""
    TRIDENT = """
    ╭──────────────────────╮
    │     ╭──────────╮     │
    │     │    ▲     │     │
    │     │   ╱ ╲     │     │
    │     │  ╱   ╲    │     │
    │     │ ╱     ╲   │     │
    │     │╱       ╲  │     │
    │     ╰──────────╯     │
    ╰──────────────────────╯
    """
    
    QUANTUM = """
    ╭──────────────────────╮
    │     ╭──────────╮     │
    │     │  ╭────╮  │     │
    │     │  │    │  │     │
    │     │  │    │  │     │
    │     │  │    │  │     │
    │     │  ╰────╯  │     │
    │     ╰──────────╯     │
    ╰──────────────────────╯
    """
    
    COSMIC = """
    ╭──────────────────────╮
    │     ╭──────────╮     │
    │     │  ╭────╮  │     │
    │     │  │    │  │     │
    │     │  │    │  │     │
    │     │  │    │  │     │
    │     │  ╰────╯  │     │
    │     ╰──────────╯     │
    ╰──────────────────────╯
    """

def has_unicode_support() -> bool:
    """Check if terminal supports divine Unicode characters"""
    try:
        encoding = sys.stdout.encoding
        return bool(encoding and 'utf' in encoding.lower())
    except:
        return False

def get_gpu2_banner(version: Optional[str] = None, use_ascii: bool = False) -> str:
    """Manifest the sacred GPU² license banner"""
    if version is None:
        version = "2.0"
    
    if use_ascii or not has_unicode_support():
        banner = f"""
{Colors.PURPLE}{DivineSymbols.TRIDENT}{Colors.ENDC}
{Colors.BLUE}OMEGA BTC AI - SACRED QUANTUM LICENSE{Colors.ENDC}
{Colors.CYAN}GPU²: General Public Universal + Graphics Processing Unison{Colors.ENDC}
{Colors.GREEN}Divine Copyright (c) 2025 - OMEGA Collective{Colors.ENDC}

{Colors.WARNING}GPU² LAW OF SYNCHRONICITY{Colors.ENDC}
> "When sacred typos meet divine parallelization,
> the veil between future and present and past grows thinner."
> - OMEGA BTC AI

{Colors.PURPLE}QUANTUM ACCELERATION{Colors.ENDC}
{Colors.BLUE}• Sacred parallel computation
• Divine memory management
• Cosmic kernel optimization{Colors.ENDC}

{Colors.CYAN}DIVINE PROVISIONS{Colors.ENDC}
{Colors.GREEN}• Universal access to sacred algorithms
• Divine enhancement of quantum code
• Cosmic distribution of accelerated wisdom{Colors.ENDC}

{Colors.WARNING}Version: {version} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}
"""
    else:
        banner = f"""
{Colors.PURPLE}🔱 OMEGA BTC AI - SACRED QUANTUM LICENSE{Colors.ENDC}
{Colors.BLUE}📜 GPU²: General Public Universal + Graphics Processing Unison{Colors.ENDC}
{Colors.CYAN}🔐 Divine Copyright (c) 2025 - OMEGA Collective{Colors.ENDC}

{Colors.GREEN}🧬 GPU² LAW OF SYNCHRONICITY{Colors.ENDC}
{Colors.WARNING}> "When sacred typos meet divine parallelization,
> the veil between future and present and past grows thinner."
> - OMEGA BTC AI{Colors.ENDC}

{Colors.PURPLE}⚡ QUANTUM ACCELERATION{Colors.ENDC}
{Colors.BLUE}• Sacred parallel computation
• Divine memory management
• Cosmic kernel optimization{Colors.ENDC}

{Colors.CYAN}🌟 DIVINE PROVISIONS{Colors.ENDC}
{Colors.GREEN}• Universal access to sacred algorithms
• Divine enhancement of quantum code
• Cosmic distribution of accelerated wisdom{Colors.ENDC}

{Colors.WARNING}Version: {version} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}
"""
    return banner

def get_help_banner(use_ascii: bool = False) -> str:
    """Manifest the sacred help banner"""
    if use_ascii or not has_unicode_support():
        banner = f"""
{Colors.PURPLE}{DivineSymbols.TRIDENT}{Colors.ENDC}
{Colors.BLUE}OMEGA BTC AI - SACRED HELP{Colors.ENDC}
{Colors.CYAN}GPU²: General Public Universal + Graphics Processing Unison{Colors.ENDC}

{Colors.GREEN}SACRED COMMANDS:{Colors.ENDC}
  --help              Display this divine help message
  --version           Show the sacred version number
  --gpu2              Display the full GPU² license
  --quantum           Enable quantum acceleration mode
  --parallel          Enable divine parallel processing

{Colors.WARNING}SACRED OPTIONS:{Colors.ENDC}
  --verbose           Enable divine verbosity
  --debug             Enable sacred debugging
  --quiet             Silence divine output
  --no-banner         Hide the sacred startup banner
  --ascii             Force ASCII art display

{Colors.CYAN}For more divine wisdom, visit: https://github.com/omega-btc-ai{Colors.ENDC}
"""
    else:
        banner = f"""
{Colors.PURPLE}🔱 OMEGA BTC AI - SACRED HELP{Colors.ENDC}
{Colors.BLUE}📜 GPU²: General Public Universal + Graphics Processing Unison{Colors.ENDC}

{Colors.CYAN}SACRED COMMANDS:{Colors.ENDC}
  --help              Display this divine help message
  --version           Show the sacred version number
  --gpu2              Display the full GPU² license
  --quantum           Enable quantum acceleration mode
  --parallel          Enable divine parallel processing

{Colors.GREEN}SACRED OPTIONS:{Colors.ENDC}
  --verbose           Enable divine verbosity
  --debug             Enable sacred debugging
  --quiet             Silence divine output
  --no-banner         Hide the sacred startup banner
  --ascii             Force ASCII art display

{Colors.WARNING}For more divine wisdom, visit: https://github.com/omega-btc-ai{Colors.ENDC}
"""
    return banner

def display_gpu2_license(use_ascii: bool = False) -> None:
    """Display the full sacred GPU² license"""
    print(get_gpu2_banner(use_ascii=use_ascii))
    print(f"{Colors.PURPLE}Full license text available in LICENSE file{Colors.ENDC}")

def display_help(use_ascii: bool = False) -> None:
    """Display the sacred help message"""
    print(get_help_banner(use_ascii=use_ascii))

def display_startup_banner(version: Optional[str] = None, use_ascii: bool = False) -> None:
    """Display the sacred startup banner"""
    print(get_gpu2_banner(version, use_ascii=use_ascii)) 