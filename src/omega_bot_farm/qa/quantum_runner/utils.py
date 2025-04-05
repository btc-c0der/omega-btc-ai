"""
Utility functions for the Quantum Test Runner.
"""

import logging
from .types import Colors

logger = logging.getLogger("0M3G4_B0TS_QA_AUT0_TEST_SUITES_RuNn3R_5D")

def log_with_formatting(message, level=logging.INFO, color=None):
    """Log a message with optional color formatting."""
    if color:
        formatted_message = f"{color}{message}{Colors.ENDC}"
        logger.log(level, formatted_message)
    else:
        logger.log(level, message)

def print_section_header(title, width=80):
    """Print a section header with a border."""
    border = "═" * width
    logger.info(f"{Colors.CYAN}{border}{Colors.ENDC}")
    centered_title = f"  {title}  ".center(width, "═")
    logger.info(f"{Colors.CYAN}║{Colors.BOLD}{Colors.BLUE}{centered_title}{Colors.ENDC}{Colors.CYAN}║{Colors.ENDC}")
    logger.info(f"{Colors.CYAN}{border}{Colors.ENDC}")

def print_test_result(test_type, result, duration, report_path=None):
    """Print a formatted test result."""
    if result == "PASSED":
        status_color = Colors.GREEN
        symbol = "✓"
    elif result == "FAILED":
        status_color = Colors.RED
        symbol = "✗"
    else:
        status_color = Colors.YELLOW
        symbol = "⚠"
    
    test_type_formatted = f"{Colors.BOLD}{test_type}{Colors.ENDC}"
    result_formatted = f"{status_color}{symbol} {result}{Colors.ENDC}"
    duration_formatted = f"{Colors.YELLOW}{duration:.2f}s{Colors.ENDC}"
    
    message = f"\n  {test_type_formatted} tests {result_formatted} in {duration_formatted}"
    logger.info(message)
    
    if report_path:
        logger.info(f"  {Colors.CYAN}Report saved to: {report_path}{Colors.ENDC}\n")

def print_file_action(action, file_path):
    """Print a formatted file action message."""
    logger.info(f"{Colors.BLUE}{action}:{Colors.ENDC} {file_path}") 