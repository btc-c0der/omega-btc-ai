#!/usr/bin/env python3

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