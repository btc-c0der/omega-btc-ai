"""
LUCAS SILVEIRA PORTAL - SENEGAL SK8 DONATION MODULE
===================================================

This module implements a quantum matrix Rubik's cube inspired 80/20 donation flow
for the SENEGAL SURFER ONG AND SK8 THAT VIRGIL ABLOH BUILT.

JAH BLESS! "YOU ARE ALIVE ON OUR HEART(S)"
"""

__version__ = "0.8.2"
__author__ = "OMEGA BTC AI Team"
__license__ = "GBU2™ License - Genesis-Bloom-Unfoldment 2.0"

from .donation_flow import DonationFlow
from .ascii_banner import display_banner, SHAKA_BANNER
from .crypto_wallet import CryptoWallet

# Display banner on import
display_banner() 