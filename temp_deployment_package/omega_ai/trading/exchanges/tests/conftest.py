"""
Pytest configuration for CCXT Strategic Fibonacci Trader tests.
"""

def pytest_addoption(parser):
    """Add command line options for pytest."""
    parser.addoption(
        "--mainnet",
        action="store_true",
        default=False,
        help="Run tests on mainnet instead of testnet"
    ) 