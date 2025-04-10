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


import asyncio
import os
from datetime import datetime


async def main():
    try:
        print(f"Testing BitGet Position Analyzer at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Get environment variables
        api_key = os.environ.get("BITGET_API_KEY", "")
        api_secret = os.environ.get("BITGET_SECRET_KEY", "")
        api_passphrase = os.environ.get("BITGET_PASSPHRASE", "")
        
        print(f"API Key available: {'Yes' if api_key else 'No'}")
        print(f"API Secret available: {'Yes' if api_secret else 'No'}")
        print(f"API Passphrase available: {'Yes' if api_passphrase else 'No'}")
        
        from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import BitgetPositionAnalyzerB0t
        
        # Initialize analyzer
        analyzer = BitgetPositionAnalyzerB0t()
        print("BitgetPositionAnalyzerB0t initialized")
        
        # Get positions
        positions = await analyzer.get_positions()
        print("\nPositions:")
        print(positions)
        
        # Analyze positions
        analysis = analyzer.analyze_all_positions()
        print("\nAnalysis:")
        print(analysis)
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 