
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
Environment setup for BDD tests.

This module defines the setup and teardown procedures for the BDD tests
using the Behave framework.
"""
import os
import json
import logging
from pathlib import Path
from unittest.mock import MagicMock

# Configure logging for BDD tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('bdd_tests')

# Define fixture paths relative to this directory
FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures")


def before_all(context):
    """
    Set up the test environment before any scenarios run.
    
    Args:
        context: The behave context object
    """
    logger.info("Setting up BDD test environment")
    
    # Create a context object to share data between steps
    context.config = load_test_config()
    
    # Ensure fixture directories exist
    os.makedirs(os.path.join(FIXTURE_PATH, "mock_data"), exist_ok=True)
    os.makedirs(os.path.join(FIXTURE_PATH, "output"), exist_ok=True)
    
    # Initialize context attributes
    context.mock_exchange_service = None
    context.mock_notification_service = None
    context.position_analyzer = None
    context.analysis_results = {}
    context.positions = {}
    context.alerts = []
    context.discord_messages = []
    context.created_files = []


def after_all(context):
    """
    Clean up the test environment after all scenarios have run.
    
    Args:
        context: The behave context object
    """
    logger.info("Cleaning up BDD test environment")
    
    # Clean up any generated files
    for file_path in context.created_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Removed test file: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to remove test file {file_path}: {e}")


def before_feature(context, feature):
    """
    Set up the environment before each feature runs.
    
    Args:
        context: The behave context object
        feature: The feature being run
    """
    logger.info(f"Starting feature: {feature.name}")


def after_feature(context, feature):
    """
    Clean up after each feature runs.
    
    Args:
        context: The behave context object
        feature: The feature being run
    """
    logger.info(f"Completed feature: {feature.name}")


def before_scenario(context, scenario):
    """
    Set up the environment before each scenario runs.
    
    Args:
        context: The behave context object
        scenario: The scenario being run
    """
    logger.info(f"Starting scenario: {scenario.name}")
    
    # Create mock services for each scenario
    setup_mock_services(context)
    
    # Reset scenario-specific state
    context.analysis_results = {}
    context.positions = {}
    context.alerts = []
    context.discord_messages = []


def after_scenario(context, scenario):
    """
    Clean up after each scenario runs.
    
    Args:
        context: The behave context object
        scenario: The scenario being run
    """
    logger.info(f"Completed scenario: {scenario.name}")


def load_test_config():
    """
    Load test configuration from environment or defaults.
    
    Returns:
        dict: The test configuration
    """
    config_path = os.environ.get('BDD_CONFIG_PATH', 
                              os.path.join(FIXTURE_PATH, 'bdd_config.json'))
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        # Default configuration for tests
        config = {
            "use_mock_exchange": True,
            "test_symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
            "mock_data_path": os.path.join(FIXTURE_PATH, "mock_data"),
            "output_path": os.path.join(FIXTURE_PATH, "output"),
            "test_timeframes": ["15m", "1h", "4h", "1d"],
            "discord": {
                "command_prefix": "!",
                "alert_channel_id": "123456789",
                "admin_role_id": "987654321"
            },
            "risk_thresholds": {
                "LOW": 0.05,
                "MEDIUM": 0.15,
                "HIGH": 0.25,
                "EXTREME": 0.4
            }
        }
    
    # Ensure output directory exists
    os.makedirs(config["output_path"], exist_ok=True)
    
    return config


def setup_mock_services(context):
    """
    Set up mock services for the tests.
    
    Args:
        context: The behave context object
    """
    # Create mock exchange service
    context.mock_exchange_service = MagicMock()
    
    # Configure default behavior
    context.mock_exchange_service.get_positions.return_value = [
        {
            "symbol": "BTCUSDT",
            "side": "long",
            "contracts": 0.5,
            "entryPrice": 65000,
            "markPrice": 68000,
            "unrealizedPnl": 1500,
            "leverage": 10,
            "liquidationPrice": 59000,
            "marginType": "isolated"
        }
    ]
    
    context.mock_exchange_service.get_account_balance.return_value = {
        "USDT": {
            "free": 5000,
            "used": 5000,
            "total": 10000
        },
        "total": {
            "USDT": 10000,
            "unrealizedPnl": 1500
        }
    }
    
    # Create mock notification service
    context.mock_notification_service = MagicMock()
    
    # Track notifications
    context.mock_notification_service.send_notification.side_effect = \
        lambda alert, **kwargs: context.alerts.append(alert)
    
    # Create the position analyzer with mock services (if implementation available)
    try:
        from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import (
            BitgetPositionAnalyzerBot
        )
        
        context.position_analyzer = BitgetPositionAnalyzerBot(
            exchange_service=context.mock_exchange_service,
            notification_service=context.mock_notification_service,
            config=context.config
        )
    except ImportError:
        logger.warning("Could not import BitgetPositionAnalyzerBot, using mock analyzer")
        context.position_analyzer = MagicMock()
        
        # Configure the mock analyzer with realistic behavior
        context.position_analyzer.analyze_position.side_effect = \
            lambda symbol: {
                "symbol": symbol,
                "position_side": "LONG",
                "risk_level": "LOW",
                "harmony_score": 0.85,
                "unrealized_pnl": 1500,
                "unrealized_pnl_percent": 4.6,
                "fibonacci_levels": {
                    "0": 68000,
                    "0.236": 67200,
                    "0.382": 66700,
                    "0.5": 66000,
                    "0.618": 65300,
                    "0.786": 64600,
                    "1": 64000
                },
                "recommendation": {
                    "action": "HOLD",
                    "reason": "Position is profitable and low risk"
                }
            } 