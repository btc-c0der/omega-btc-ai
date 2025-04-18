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
OMEGA GENESIS BLOCK CREATOR
---------------------------
Creates the sacred first block of the OMEGA Blockchain with market trends data
and a divine message to Satoshi Nakamoto.
"""

import sys
import json
import time
import hashlib
import logging
import redis
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ANSI colors for terminal output
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

# Genesis block constants
GENESIS_TIMESTAMP = int(time.time())
GENESIS_PREV_HASH = "0" * 64  # Genesis block has no previous block
GENESIS_DIFFICULTY = 4  # Number of leading zeros in hash
GENESIS_SATOSHI_MESSAGE = (
    "From OMEGA BTC AI to Satoshi Nakamoto: Your innovation has changed the world. "
    "We honor your vision by extending the blockchain beyond prices to embody the patterns "
    "of market consciousness. May this genesis block bridge your creation with the quantum "
    "future of blockchain. JAH BLESS."
)
GENESIS_SPECIAL_MESSAGE = "0m3g4_k1ng JAH BLESS THE OMEGA BL0CKCHAIN"
GENESIS_VERSION = "0.6.2-enhanced-market-trends"

def get_market_trends_data() -> Dict[str, Any]:
    """
    Retrieve market trends data from Redis to include in the genesis block
    """
    try:
        # Connect to Redis
        redis_conn = redis.Redis(host="localhost", port=6379, db=0)
        logger.info(f"{BLUE}Connected to Redis{RESET}")

        # Get current BTC price
        btc_price_json = redis_conn.get("btc_price")
        btc_price_data = json.loads(btc_price_json) if btc_price_json else {"price": 50000.0}
        
        # Get trend data for different timeframes
        timeframes = [1, 5, 15, 30, 60, 240, 720, 1440]
        trend_data = {}
        
        for tf in timeframes:
            trend_key = f"btc_trend_{tf}min"
            trend_json = redis_conn.get(trend_key)
            if trend_json:
                trend_data[f"{tf}min"] = json.loads(trend_json)
            else:
                trend_data[f"{tf}min"] = {"trend": "Bullish", "change_pct": 0.5}
        
        # Get Fibonacci levels
        fib_json = redis_conn.get("fibonacci_levels")
        fib_data = json.loads(fib_json) if fib_json else {
            "high": 104713.26,
            "low": 69808.84,
            "fib_0": 69808.84,
            "fib_0.236": 78002.40,
            "fib_0.382": 83132.05,
            "fib_0.5": 87261.05,
            "fib_0.618": 91389.93,
            "fib_0.786": 97126.47,
            "fib_1": 104713.26
        }
        
        # Get volatility
        volatility_json = redis_conn.get("btc_volatility")
        volatility_data = json.loads(volatility_json) if volatility_json else {"volatility": 0.0102}
        
        # Get 24h volume
        volume_json = redis_conn.get("btc_24h_volume")
        volume_data = json.loads(volume_json) if volume_json else {"volume": 19426.05}
        
        # Get Schumann resonance data
        schumann_json = redis_conn.get("schumann_resonance")
        schumann_data = json.loads(schumann_json) if schumann_json else {"frequency": 7.83}
        
        # Return market data
        return {
            "btc_price": btc_price_data,
            "trend_data": trend_data,
            "fibonacci_levels": fib_data,
            "volatility_data": volatility_data,
            "volume_data": volume_data,
            "schumann_data": schumann_data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error retrieving market data: {e}")
        # Return fallback data for genesis block
        return {
            "btc_price": {"price": 87261.05, "timestamp": datetime.now(timezone.utc).isoformat()},
            "trend_data": {
                "1min": {"trend": "Bullish", "change_pct": 0.5},
                "5min": {"trend": "Bullish", "change_pct": 0.8},
                "15min": {"trend": "Bullish", "change_pct": 1.2},
                "30min": {"trend": "Bullish", "change_pct": 1.5},
                "60min": {"trend": "Bullish", "change_pct": 2.1},
                "240min": {"trend": "Strongly Bullish", "change_pct": 3.2},
                "720min": {"trend": "Strongly Bullish", "change_pct": 4.5},
                "1440min": {"trend": "Strongly Bullish", "change_pct": 5.1}
            },
            "fibonacci_levels": {
                "high": 104713.26,
                "low": 69808.84,
                "fib_0": 69808.84,
                "fib_0.236": 78002.40,
                "fib_0.382": 83132.05,
                "fib_0.5": 87261.05,
                "fib_0.618": 91389.93,
                "fib_0.786": 97126.47,
                "fib_1": 104713.26
            },
            "volatility_data": {"volatility": 0.0102, "timestamp": datetime.now(timezone.utc).isoformat()},
            "volume_data": {"volume": 19426.05, "timestamp": datetime.now(timezone.utc).isoformat()},
            "schumann_data": {"frequency": 7.83, "timestamp": datetime.now(timezone.utc).isoformat()},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

def create_genesis_block() -> Dict[str, Any]:
    """
    Create the OMEGA Genesis Block with market trends data and special messages
    """
    logger.info(f"{YELLOW}Creating OMEGA Genesis Block...{RESET}")
    
    # Get market trends data
    market_data = get_market_trends_data()
    
    # Create genesis block data
    genesis_block = {
        "header": {
            "version": GENESIS_VERSION,
            "prev_block_hash": GENESIS_PREV_HASH,
            "timestamp": GENESIS_TIMESTAMP,
            "difficulty": GENESIS_DIFFICULTY,
        },
        "messages": {
            "to_satoshi": GENESIS_SATOSHI_MESSAGE,
            "special": GENESIS_SPECIAL_MESSAGE
        },
        "market_data": market_data,
        "nonce": 0
    }
    
    # Mine the genesis block (find a valid hash)
    genesis_block = mine_genesis_block(genesis_block)
    
    logger.info(f"{GREEN}OMEGA Genesis Block successfully created!{RESET}")
    return genesis_block

def calculate_block_hash(block: Dict[str, Any]) -> str:
    """
    Calculate the SHA-256 hash of a block
    """
    # Create a copy of the block to avoid modifying the original
    block_for_hashing = block.copy()
    
    # Remove the hash if it exists (we're calculating it now)
    if "hash" in block_for_hashing:
        del block_for_hashing["hash"]
    
    # Convert the block to a JSON string
    block_string = json.dumps(block_for_hashing, sort_keys=True)
    
    # Calculate the SHA-256 hash
    return hashlib.sha256(block_string.encode()).hexdigest()

def mine_genesis_block(block: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mine the genesis block by finding a nonce that produces a hash with the required number of leading zeros
    """
    difficulty = block["header"]["difficulty"]
    target_prefix = "0" * difficulty
    
    logger.info(f"{YELLOW}Mining Genesis Block with difficulty {difficulty}...{RESET}")
    
    nonce = 0
    while True:
        block["nonce"] = nonce
        block_hash = calculate_block_hash(block)
        
        if block_hash.startswith(target_prefix):
            block["hash"] = block_hash
            logger.info(f"{GREEN}Genesis Block mined with hash: {block_hash}{RESET}")
            return block
        
        nonce += 1
        if nonce % 1000 == 0:
            logger.info(f"Tried {nonce} nonces...")

def save_genesis_block(block: Dict[str, Any]) -> None:
    """
    Save the genesis block to a file
    """
    genesis_file = "OMEGA_GENESIS_BLOCK.json"
    with open(genesis_file, "w") as f:
        json.dump(block, f, indent=2)
    
    logger.info(f"{GREEN}Genesis Block saved to {genesis_file}{RESET}")
    
    # Also save to blockchain directory if it exists
    try:
        omega_blockchain_dir = "omega_blockchain/data"
        if not os.path.exists(omega_blockchain_dir):
            os.makedirs(omega_blockchain_dir)
        
        with open(f"{omega_blockchain_dir}/block_0.json", "w") as f:
            json.dump(block, f, indent=2)
        
        logger.info(f"{GREEN}Genesis Block saved to blockchain directory{RESET}")
    except Exception as e:
        logger.warning(f"Could not save to blockchain directory: {e}")

def display_genesis_block(block: Dict[str, Any]) -> None:
    """
    Display the genesis block in a formatted way
    """
    print("\n" + "=" * 80)
    print(f"{MAGENTA}OMEGA GENESIS BLOCK{RESET}".center(80))
    print("=" * 80)
    
    print(f"\n{CYAN}Block Hash:{RESET} {block['hash']}")
    print(f"{CYAN}Timestamp:{RESET} {datetime.fromtimestamp(block['header']['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{CYAN}Version:{RESET} {block['header']['version']}")
    print(f"{CYAN}Difficulty:{RESET} {block['header']['difficulty']}")
    print(f"{CYAN}Nonce:{RESET} {block['nonce']}")
    
    print(f"\n{YELLOW}MESSAGE TO SATOSHI:{RESET}")
    print(f"{block['messages']['to_satoshi']}")
    
    print(f"\n{YELLOW}SPECIAL MESSAGE:{RESET}")
    print(f"{block['messages']['special']}")
    
    print(f"\n{YELLOW}MARKET DATA AT GENESIS:{RESET}")
    market_data = block['market_data']
    
    # Display BTC price
    btc_price = market_data['btc_price'].get('price', 0)
    print(f"\n{CYAN}BTC Price:{RESET} ${btc_price:,.2f}")
    
    # Display trend data
    print(f"\n{CYAN}Market Trends:{RESET}")
    for timeframe, data in market_data['trend_data'].items():
        trend = data.get('trend', 'Neutral')
        change = data.get('change_pct', 0.0)
        print(f"  {timeframe}: {trend} ({change:+.2f}%)")
    
    # Display Fibonacci levels
    if market_data.get('fibonacci_levels'):
        fib = market_data['fibonacci_levels']
        print(f"\n{CYAN}Fibonacci Levels:{RESET}")
        print(f"  High: ${fib.get('high', 0):,.2f}")
        print(f"  0.786: ${fib.get('fib_0.786', 0):,.2f}")
        print(f"  0.618: ${fib.get('fib_0.618', 0):,.2f}")
        print(f"  0.5: ${fib.get('fib_0.5', 0):,.2f}")
        print(f"  0.382: ${fib.get('fib_0.382', 0):,.2f}")
        print(f"  0.236: ${fib.get('fib_0.236', 0):,.2f}")
        print(f"  Low: ${fib.get('low', 0):,.2f}")
    
    # Display additional data
    print(f"\n{CYAN}Additional Market Data:{RESET}")
    
    # Handle volatility data
    volatility_data = market_data.get('volatility_data', {})
    if isinstance(volatility_data, dict):
        volatility = volatility_data.get('volatility', 0) * 100
        print(f"  Volatility: {volatility:.2f}%")
    else:
        print(f"  Volatility: 1.02%")  # Default
    
    # Handle volume data
    volume_data = market_data.get('volume_data', {})
    if isinstance(volume_data, dict):
        volume = volume_data.get('volume', 0)
        print(f"  24h Volume: {volume:,.2f} BTC")
    else:
        print(f"  24h Volume: 19,426.05 BTC")  # Default
    
    # Handle Schumann resonance data
    schumann_data = market_data.get('schumann_data', {})
    if isinstance(schumann_data, dict):
        schumann = schumann_data.get('frequency', 7.83)
        print(f"  Schumann Resonance: {schumann:.2f} Hz")
    else:
        print(f"  Schumann Resonance: 7.83 Hz")  # Default
    
    print("\n" + "=" * 80)
    print(f"{GREEN}OMEGA BLOCKCHAIN HAS BEEN INITIALIZED{RESET}".center(80))
    print("=" * 80 + "\n")

def connect_to_blockchain() -> bool:
    """
    Attempt to connect the genesis block to the OMEGA blockchain
    """
    logger.warning("OMEGA Blockchain module integration pending")
    return False

if __name__ == "__main__":
    try:
        print(f"\n{MAGENTA}OMEGA GENESIS BLOCK CREATOR{RESET}")
        print(f"{BLUE}Creating the first block of the OMEGA Blockchain{RESET}\n")
        
        # Create the genesis block
        genesis_block = create_genesis_block()
        
        # Save the genesis block to file
        save_genesis_block(genesis_block)
        
        # Display the genesis block
        display_genesis_block(genesis_block)
        
        # Try to connect to the blockchain
        blockchain_connected = connect_to_blockchain()
        
        if blockchain_connected:
            print(f"{GREEN}Genesis block successfully connected to OMEGA Blockchain!{RESET}")
        else:
            print(f"{YELLOW}Genesis block created but not connected to blockchain infrastructure.{RESET}")
            print(f"{YELLOW}Run omega_blockchain.py to initialize the full blockchain.{RESET}")
        
    except Exception as e:
        logger.error(f"Error creating genesis block: {e}")
        sys.exit(1) 