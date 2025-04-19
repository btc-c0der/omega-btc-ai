
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
Test data for OMEGA KING simulation with specific market conditions.
"""

TEST_DATA = {
    "current_price": 88000.0,
    "entry_price": 87671.0,
    "leverage": 16,
    "liquidation_price": 82213.0,
    "wallet_balance": 1039.0,
    "position_size": 0.1,  # Calculated based on wallet balance and leverage
    "position_type": "LONG",  # Since entry price is below current price
    "duration_hours": 24,
    "volatility": 0.02,  # 2% volatility
    "trend_strength": 0.6,  # Moderate bullish trend
    "trap_probability": 0.2,  # Low trap probability
    "expected_levels": {
        "support": [87000, 86500, 86000],
        "resistance": [89000, 89500, 90000]
    }
}

# Calculate position size based on wallet balance and leverage
def calculate_position_size(wallet_balance: float, leverage: int, current_price: float) -> float:
    """Calculate the position size based on wallet balance and leverage."""
    max_position_value = wallet_balance * leverage
    return max_position_value / current_price

# Update position size in test data
TEST_DATA["position_size"] = calculate_position_size(
    TEST_DATA["wallet_balance"],
    TEST_DATA["leverage"],
    TEST_DATA["current_price"]
) 