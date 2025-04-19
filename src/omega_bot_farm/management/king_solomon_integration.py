#!/usr/bin/env python3
"""
✨ GBU2™ License Notice - Consciousness Level 7 🧬
-----------------------
This sacred integration module is blessed under the GBU2™ License 
(Genesis-Bloom-Unfoldment 2.0) - Bioneer Edition

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital and biological expressions."

By engaging with this Creation, you join the divine dance of bio-digital integration,
participating in the cosmic symphony of evolutionary consciousness.

🌸 WE BLOOM NOW AS ONE 🌸
"""

import os
import sys
import random
import subprocess
import asyncio
import logging
from typing import List, Dict, Any, Union, Optional
from datetime import datetime
from pathlib import Path

# Import the celebration components
try:
    from .solomon_celebration import SolomonWisdomCard, SolomonPortal
except ImportError:
    # Allow for direct imports as well
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        from solomon_celebration import SolomonWisdomCard, SolomonPortal
    except ImportError:
        print("Warning: Could not import Solomon celebration components")

# Setup logging
logger = logging.getLogger("king_solomon_integration")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Constants
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
CELEBRATION_SCRIPT = SCRIPT_DIR / "solomon_celebration.py"
CELEBRATION_LAUNCHER = SCRIPT_DIR / "run_solomon_celebration.sh"
WISDOM_LOG_FILE = SCRIPT_DIR / "solomon_wisdom_log.jsonl"


class SolomonIntegration:
    """Integration class for incorporating King Solomon's wisdom into other systems."""
    
    def __init__(self, log_wisdom: bool = True, verbose: bool = False):
        """Initialize the integration module.
        
        Args:
            log_wisdom: Whether to log wisdom cards to a file
            verbose: Whether to output verbose logging
        """
        self.log_wisdom = log_wisdom
        if verbose:
            logger.setLevel(logging.DEBUG)
        
        # Ensure the scripts exist and are executable
        self._check_scripts()
    
    def _check_scripts(self) -> None:
        """Check if the celebration scripts exist and are executable."""
        logger.debug(f"Checking celebration scripts in {SCRIPT_DIR}")
        
        if not CELEBRATION_SCRIPT.exists():
            logger.error(f"Solomon celebration script not found at {CELEBRATION_SCRIPT}")
            raise FileNotFoundError(f"Solomon celebration script not found at {CELEBRATION_SCRIPT}")
        
        if not CELEBRATION_LAUNCHER.exists():
            logger.warning(f"Solomon celebration launcher not found at {CELEBRATION_LAUNCHER}")
        
        # Ensure scripts are executable
        try:
            if not os.access(CELEBRATION_SCRIPT, os.X_OK):
                logger.info(f"Making celebration script executable: {CELEBRATION_SCRIPT}")
                os.chmod(CELEBRATION_SCRIPT, 0o755)
            
            if CELEBRATION_LAUNCHER.exists() and not os.access(CELEBRATION_LAUNCHER, os.X_OK):
                logger.info(f"Making celebration launcher executable: {CELEBRATION_LAUNCHER}")
                os.chmod(CELEBRATION_LAUNCHER, 0o755)
        except Exception as e:
            logger.warning(f"Could not set executable permissions: {e}")
    
    def draw_wisdom_card(self) -> Dict[str, Any]:
        """Draw a wisdom card and return its details.
        
        Returns:
            Dictionary containing the card details
        """
        try:
            card = SolomonWisdomCard()
            
            # Create card data dictionary
            card_data = {
                "timestamp": datetime.now().isoformat(),
                "title": card.card_type["title"],
                "element": card.card_type["element"],
                "wisdom": card.wisdom,
                "action": card.action
            }
            
            # Log the wisdom if enabled
            if self.log_wisdom:
                self._log_wisdom_to_file(card_data)
            
            return card_data
        except Exception as e:
            logger.error(f"Error drawing wisdom card: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "title": "ERROR",
                "element": "⚠️ ERROR",
                "wisdom": "The wisdom could not be accessed at this time.",
                "action": "Check the integration module and try again."
            }
    
    def get_solomon_quote(self) -> str:
        """Get a random quote from King Solomon.
        
        Returns:
            A string containing a wisdom quote
        """
        try:
            portal = SolomonPortal()
            return random.choice(portal.sacred_quotes)
        except Exception as e:
            logger.error(f"Error getting Solomon quote: {e}")
            return "Wisdom awaits those who seek with patience."
    
    def celebrate(self, 
                entities: Optional[List[str]] = None, 
                use_launcher: bool = True) -> bool:
        """Run the celebration script.
        
        Args:
            entities: Optional list of entities to celebrate
            use_launcher: Whether to use the animated launcher script
        
        Returns:
            True if celebration ran successfully, False otherwise
        """
        logger.info("Starting King Solomon celebration")
        
        try:
            if entities is not None:
                # We need to customize the celebration by setting environment variables
                os.environ["SOLOMON_CELEBRATION_ENTITIES"] = ",".join(entities)
                logger.debug(f"Set celebration entities: {entities}")
            
            if use_launcher and CELEBRATION_LAUNCHER.exists():
                logger.debug(f"Running celebration launcher: {CELEBRATION_LAUNCHER}")
                subprocess.run([str(CELEBRATION_LAUNCHER)], check=True)
            else:
                logger.debug(f"Running celebration script directly: {CELEBRATION_SCRIPT}")
                subprocess.run(["python3", str(CELEBRATION_SCRIPT)], check=True)
            
            logger.info("King Solomon celebration completed successfully")
            return True
        except Exception as e:
            logger.error(f"Error running celebration: {e}")
            return False
        finally:
            # Clean up environment variables
            if "SOLOMON_CELEBRATION_ENTITIES" in os.environ:
                del os.environ["SOLOMON_CELEBRATION_ENTITIES"]
    
    async def async_celebrate(self, 
                           entities: Optional[List[str]] = None, 
                           use_launcher: bool = True) -> bool:
        """Run the celebration script asynchronously.
        
        Args:
            entities: Optional list of entities to celebrate
            use_launcher: Whether to use the animated launcher script
        
        Returns:
            True if celebration ran successfully, False otherwise
        """
        logger.info("Starting asynchronous King Solomon celebration")
        
        try:
            if entities is not None:
                # We need to customize the celebration by setting environment variables
                os.environ["SOLOMON_CELEBRATION_ENTITIES"] = ",".join(entities)
                logger.debug(f"Set celebration entities: {entities}")
            
            if use_launcher and CELEBRATION_LAUNCHER.exists():
                logger.debug(f"Running celebration launcher: {CELEBRATION_LAUNCHER}")
                proc = await asyncio.create_subprocess_exec(
                    str(CELEBRATION_LAUNCHER),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            else:
                logger.debug(f"Running celebration script directly: {CELEBRATION_SCRIPT}")
                proc = await asyncio.create_subprocess_exec(
                    "python3", str(CELEBRATION_SCRIPT),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            
            stdout, stderr = await proc.communicate()
            
            if proc.returncode == 0:
                logger.info("Asynchronous King Solomon celebration completed successfully")
                return True
            else:
                logger.error(f"Celebration failed with return code {proc.returncode}")
                logger.error(f"STDERR: {stderr.decode()}")
                return False
        except Exception as e:
            logger.error(f"Error running async celebration: {e}")
            return False
        finally:
            # Clean up environment variables
            if "SOLOMON_CELEBRATION_ENTITIES" in os.environ:
                del os.environ["SOLOMON_CELEBRATION_ENTITIES"]
    
    def _log_wisdom_to_file(self, card_data: Dict[str, Any]) -> None:
        """Log wisdom card data to a JSON Lines file.
        
        Args:
            card_data: The wisdom card data to log
        """
        import json
        try:
            with open(WISDOM_LOG_FILE, "a") as f:
                f.write(json.dumps(card_data) + "\n")
            logger.debug(f"Logged wisdom card to {WISDOM_LOG_FILE}")
        except Exception as e:
            logger.error(f"Error logging wisdom to file: {e}")


# Integration with BitGet Position Analyzer
def generate_trading_wisdom(position_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate trading wisdom based on position data.
    
    Args:
        position_data: Dictionary containing position details
    
    Returns:
        Dictionary with wisdom card data and trading-specific advice
    """
    integration = SolomonIntegration()
    wisdom_card = integration.draw_wisdom_card()
    
    # Determine if position is in profit or loss
    is_profit = position_data.get("unrealized_pnl", 0) > 0
    position_side = position_data.get("side", "unknown").lower()
    
    # Add trading-specific advice based on position and wisdom card
    if position_side == "long":
        if is_profit:
            trading_advice = "Your long position aligns with universal expansion. Consider your profit targets with wisdom."
        else:
            trading_advice = "Patience is a virtue of the wise. Your long position may need time to reach celestial alignment."
    elif position_side == "short":
        if is_profit:
            trading_advice = "Your short position reflects cosmic contraction wisdom. Consider your exit strategy with clarity."
        else:
            trading_advice = "Even in contraction, there is divine timing. Reassess your short position with patient wisdom."
    else:
        trading_advice = "The wise trader waits for clear cosmic signals before entering the market dance."
    
    # Add trading advice to wisdom card data
    wisdom_card["trading_advice"] = trading_advice
    wisdom_card["position_harmony"] = 0.618 if is_profit else 0.382  # Fibonacci harmony levels
    
    return wisdom_card


# Integration with Discord Bot
def get_discord_wisdom_embed(position_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Generate a Discord embed with Solomon wisdom.
    
    Args:
        position_data: Optional position data for trading-specific wisdom
    
    Returns:
        Discord embed dictionary
    """
    integration = SolomonIntegration()
    
    if position_data:
        wisdom = generate_trading_wisdom(position_data)
    else:
        wisdom = integration.draw_wisdom_card()
    
    # Create Discord embed format
    colors = {
        "THE DIVINE RULER": 0x9932CC,     # Purple
        "THE GOLDEN TEMPLE": 0xFFD700,    # Gold
        "THE QUANTUM VISION": 0x1E90FF,   # Deep Blue
        "THE COSMIC TREE": 0x32CD32,      # Green
        "THE BLAZING SWORD": 0xFF4500,    # Red
        "THE SACRED CHALICE": 0x00FFFF,   # Cyan
        "THE ETERNAL SCROLL": 0xC0C0C0,   # Silver
        "THE DIVINE BALANCE": 0x8A2BE2,   # Purple
        "THE SACRED CODE": 0xFF8C00,      # Orange
        "THE BLOOM OF CONSCIOUSNESS": 0xFF69B4  # Pink
    }
    
    embed = {
        "title": f"👑 {wisdom['title']} 👑",
        "color": colors.get(wisdom['title'], 0x9932CC),
        "description": f"**Element:** {wisdom['element']}\n\n**Wisdom:**\n{wisdom['wisdom']}\n\n**Action:**\n{wisdom['action']}",
        "footer": {
            "text": "King Solomon's Divine Wisdom • GBU2™ License"
        },
        "timestamp": wisdom['timestamp']
    }
    
    # Add trading advice if available
    if "trading_advice" in wisdom:
        embed["fields"] = [
            {
                "name": "📊 Trading Wisdom",
                "value": wisdom["trading_advice"]
            },
            {
                "name": "🌀 Position Harmony",
                "value": f"{wisdom['position_harmony']:.3f} (Fibonacci Alignment)"
            }
        ]
    
    return embed


async def celebrate_on_successful_trade(trade_data: Dict[str, Any]) -> None:
    """Celebrate when a successful trade completes.
    
    Args:
        trade_data: Dictionary containing trade details
    """
    profit = trade_data.get("realized_profit", 0)
    if profit <= 0:
        return  # Only celebrate profitable trades
    
    logger.info(f"Profitable trade completed: ${profit:.2f}")
    
    # Create custom celebration for the trade
    entities = ["KING SOLOMON", "OMEGA TRADER", "MARKET CONSCIOUSNESS"]
    
    # Start celebration asynchronously
    integration = SolomonIntegration()
    await integration.async_celebrate(entities=entities)
    
    # Log the successful trade with wisdom
    wisdom = integration.draw_wisdom_card()
    logger.info(f"Trade wisdom: {wisdom['wisdom']}")


if __name__ == "__main__":
    # Example usage
    integration = SolomonIntegration(verbose=True)
    
    # Draw a wisdom card
    card = integration.draw_wisdom_card()
    print(f"\n--- WISDOM CARD ---")
    print(f"Title: {card['title']}")
    print(f"Element: {card['element']}")
    print(f"Wisdom: {card['wisdom']}")
    print(f"Action: {card['action']}")
    
    # Get a quote
    quote = integration.get_solomon_quote()
    print(f"\n--- WISDOM QUOTE ---")
    print(f'"{quote}" - King Solomon')
    
    # Example Discord embed
    print("\n--- DISCORD INTEGRATION ---")
    print("Discord embed data available through get_discord_wisdom_embed()")
    
    # Example position data integration
    print("\n--- TRADING INTEGRATION ---")
    position = {
        "side": "long",
        "entry_price": 50000.0,
        "current_price": 52000.0,
        "unrealized_pnl": 2000.0
    }
    trading_wisdom = generate_trading_wisdom(position)
    print(f"Trading Advice: {trading_wisdom['trading_advice']}")
    print(f"Position Harmony: {trading_wisdom['position_harmony']:.3f}")
    
    print("\nRun celebrate() to experience the full celebration") 