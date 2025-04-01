"""
Trader profiles for the OmegaBTC AI trading system.

This package contains different trader personality models used in the 
trader profile simulation system.
"""

from .aggressive_trader import AggressiveTrader
from .strategic_trader import StrategicTrader
from .newbie_trader import NewbieTrader
from .scalper_trader import ScalperTrader  # Add this line

__all__ = ['AggressiveTrader', 'StrategicTrader', 'NewbieTrader', 'ScalperTrader']