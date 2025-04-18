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
BitGet Data Manager for Rasta Monitor

Handles all data fetching operations for the Rasta BitGet Position Monitor
including direct CCXT integration for real-time position data.
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("bitget_data")

# Add file handler to save logs to a file
file_handler = logging.FileHandler('rasta_bitget_monitor.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

class BitgetDataManager:
    """Manages data operations for BitGet position monitoring"""
    
    # pragma: no cover
    
    def __init__(self):
        """Initialize the BitGet data manager"""
        # Load environment variables
        load_dotenv()
        
        # Initialize state tracking
        self.previous_positions = []
        self.previous_notional = 0
        self.account_balance = 0  # Will be updated with actual data
        
        # Verify environment availability
        self._check_environment()
    
    def _check_environment(self):
        """Check if required environment variables are set"""
        api_key = os.getenv("BITGET_API_KEY", "")
        secret_key = os.getenv("BITGET_SECRET_KEY", "")
        passphrase = os.getenv("BITGET_PASSPHRASE", "")
        
        if not api_key or not secret_key or not passphrase:
            logger.warning("BitGet API credentials not found in environment variables")
    
    def get_positions(self) -> Dict[str, Any]:
        """Fetch and return BitGet positions"""
        # Get API credentials from environment
        api_key = os.getenv("BITGET_API_KEY", "")
        secret_key = os.getenv("BITGET_SECRET_KEY", "")
        passphrase = os.getenv("BITGET_PASSPHRASE", "")
        
        # Verify API credentials
        if not api_key or not secret_key or not passphrase:
            logger.error("Missing BitGet API credentials in environment variables")
            return {"error": "Missing credentials"}
        
        # Create direct CCXT BitGet client
        try:
            import ccxt
            
            # Create the exchange client
            exchange = ccxt.bitget({
                'apiKey': api_key,
                'secret': secret_key,
                'password': passphrase,
                'options': {
                    'defaultType': 'swap',
                }
            })
            
            # Fetch positions
            positions = exchange.fetch_positions()
            
            # Filter out positions with zero contracts
            active_positions = [p for p in positions if float(p.get('contracts', 0)) > 0]
            
            # Fetch account balance
            account_info = exchange.fetch_balance()
            
            # Extract USDT balance for mainnet
            if 'USDT' in account_info:
                self.account_balance = float(account_info['USDT'].get('total', 0))
            else:
                # Estimate from positions if not available directly
                total_notional = sum(float(p.get('notional', 0)) for p in active_positions)
                if total_notional > 0:
                    # Assume positions are about 30% of account on average
                    self.account_balance = max(total_notional / 0.3, self.account_balance)
            
            # Return position data and API connection info
            return {
                "success": True,
                "positions": active_positions,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "connection": "CONNECTED TO BITGET MAINNET",
                "account_balance": self.account_balance
            }
            
        except ImportError:
            logger.error("ccxt module not installed")
            return {"error": "ccxt module not installed"}
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return {"error": str(e)}
    
    def detect_position_changes(self, current_positions) -> Optional[Dict[str, List]]:
        """Detect changes between current and previous positions"""
        changes = {
            "new": [],
            "closed": [],
            "changed": []
        }
        
        if not self.previous_positions:
            # First run, no changes to detect
            self.previous_positions = current_positions
            return None
        
        # Find current position symbols
        current_symbols = {p.get('symbol'): p for p in current_positions}
        prev_symbols = {p.get('symbol'): p for p in self.previous_positions}
        
        # Detect new positions
        for symbol, position in current_symbols.items():
            if symbol not in prev_symbols:
                changes["new"].append(position)
            else:
                # Check if position size or PnL changed significantly
                prev_pos = prev_symbols[symbol]
                curr_contracts = float(position.get('contracts', 0))
                prev_contracts = float(prev_pos.get('contracts', 0))
                curr_pnl = float(position.get('unrealizedPnl', 0))
                prev_pnl = float(prev_pos.get('unrealizedPnl', 0))
                
                # Detect significant changes (>5% position size or >10% PnL)
                if abs(curr_contracts - prev_contracts) / max(prev_contracts, 0.0001) > 0.05 or \
                   abs(curr_pnl - prev_pnl) > abs(prev_pnl * 0.1):
                    changes["changed"].append({
                        "position": position,
                        "prev_contracts": prev_contracts,
                        "prev_pnl": prev_pnl
                    })
        
        # Detect closed positions
        for symbol, position in prev_symbols.items():
            if symbol not in current_symbols:
                changes["closed"].append(position)
        
        # Update previous positions for next comparison
        self.previous_positions = current_positions
        
        # Return None if no changes detected
        if not changes["new"] and not changes["closed"] and not changes["changed"]:
            return None
            
        return changes 