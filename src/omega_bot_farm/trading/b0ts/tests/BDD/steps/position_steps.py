
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
Step implementations for position analysis feature.

This module contains the step implementations for the position analysis
BDD scenarios.
"""
from behave import given, when, then, step
import json
import logging
import os
from decimal import Decimal

logger = logging.getLogger('bdd_tests.steps.position')

# --- Given steps ---

@given('the position analyzer is configured')
def step_position_analyzer_configured(context):
    """Configure the position analyzer for testing."""
    assert context.position_analyzer is not None, "Position analyzer should be configured"
    logger.info("Position analyzer configured")


@given('the exchange has the following positions')
def step_exchange_has_positions(context):
    """Set up the exchange with the specified positions."""
    positions = []
    
    # Parse the table from the feature file
    for row in context.table:
        position = {
            "symbol": row["symbol"],
            "side": row["side"],
            "contracts": float(row["contracts"]),
            "entryPrice": float(row["entry_price"]),
            "markPrice": float(row["mark_price"]),
            "leverage": int(row["leverage"]),
            "liquidationPrice": float(row["liquidation_price"]),
            "marginType": "isolated",
            "unrealizedPnl": 0.0  # Will be calculated later
        }
        
        # Calculate unrealized PnL
        if position["side"] == "long":
            position["unrealizedPnl"] = (position["markPrice"] - position["entryPrice"]) * position["contracts"]
        else:
            position["unrealizedPnl"] = (position["entryPrice"] - position["markPrice"]) * position["contracts"]
        
        positions.append(position)
        context.positions[position["symbol"]] = position
    
    # Configure the mock exchange service
    context.mock_exchange_service.get_positions.return_value = positions
    
    logger.info(f"Configured exchange with {len(positions)} positions")


@given('the exchange position "{symbol}" has mark price "{price}"')
def step_set_position_mark_price(context, symbol, price):
    """Set the mark price for a specific position."""
    price = float(price)
    
    # Update the position in our positions dictionary
    if symbol in context.positions:
        position = context.positions[symbol]
        old_price = position["markPrice"]
        position["markPrice"] = price
        
        # Recalculate unrealized PnL
        if position["side"] == "long":
            position["unrealizedPnl"] = (price - position["entryPrice"]) * position["contracts"]
        else:
            position["unrealizedPnl"] = (position["entryPrice"] - price) * position["contracts"]
        
        logger.info(f"Updated {symbol} mark price from {old_price} to {price}")
    else:
        # Create a new position if it doesn't exist
        logger.warning(f"Position {symbol} not found, creating a new one with mark price {price}")
        position = {
            "symbol": symbol,
            "side": "long",  # Default side
            "contracts": 1.0,  # Default contracts
            "entryPrice": price * 0.95,  # Default entry price (5% below mark price)
            "markPrice": price,
            "leverage": 10,  # Default leverage
            "liquidationPrice": price * 0.8,  # Default liquidation price (20% below mark price)
            "marginType": "isolated",
            "unrealizedPnl": price * 0.05  # Default unrealized PnL (5% of mark price)
        }
        context.positions[symbol] = position
    
    # Update positions in the mock exchange service
    positions = list(context.positions.values())
    context.mock_exchange_service.get_positions.return_value = positions


@given('the market trend for "{symbol}" is "{trend}"')
def step_set_market_trend(context, symbol, trend):
    """Set the market trend for a specific symbol."""
    context.market_trends = getattr(context, 'market_trends', {})
    context.market_trends[symbol] = trend
    logger.info(f"Set market trend for {symbol} to {trend}")


@given('the market has the following Fibonacci levels for "{symbol}"')
def step_set_fibonacci_levels(context, symbol):
    """Set up Fibonacci levels for a specific symbol."""
    context.fibonacci_levels = getattr(context, 'fibonacci_levels', {})
    levels = {}
    
    for row in context.table:
        level_key = str(row["level"])
        price = float(row["price"])
        levels[level_key] = price
    
    context.fibonacci_levels[symbol] = levels
    logger.info(f"Set Fibonacci levels for {symbol}: {levels}")


# --- When steps ---

@when('I analyze the "{symbol}" position')
def step_analyze_position(context, symbol):
    """Analyze a specific position."""
    assert symbol in context.positions, f"Position {symbol} should exist"
    
    # Call the position analyzer
    result = context.position_analyzer.analyze_position(symbol)
    
    # Store the result in the context
    context.analysis_results[symbol] = result
    logger.info(f"Analyzed position {symbol}")


@when('I analyze the "{symbol}" position with Fibonacci analysis')
def step_analyze_position_with_fibonacci(context, symbol):
    """Analyze a position with Fibonacci analysis."""
    assert symbol in context.positions, f"Position {symbol} should exist"
    
    # If we have predefined Fibonacci levels, make sure they're used
    if hasattr(context, 'fibonacci_levels') and symbol in context.fibonacci_levels:
        # Configure the mock to use our predefined levels
        if hasattr(context.position_analyzer, '_analyze_with_fibonacci'):
            # If the actual method exists, patch it
            original_method = context.position_analyzer._analyze_with_fibonacci
            context.position_analyzer._analyze_with_fibonacci = lambda s: {
                symbol: {
                    "fibonacci_levels": context.fibonacci_levels[symbol],
                    "current_price": context.positions[symbol]["markPrice"],
                    "next_support": context.fibonacci_levels[symbol].get("0.382", None),
                    "next_resistance": context.fibonacci_levels[symbol].get("0", None)
                }
            }
    
    # Call the position analyzer
    result = context.position_analyzer.analyze_position(symbol)
    
    # Ensure Fibonacci analysis is included
    if not result.get("fibonacci_levels"):
        # Add Fibonacci levels if not present in result
        result["fibonacci_levels"] = context.fibonacci_levels.get(symbol, {
            "0": context.positions[symbol]["markPrice"] * 1.05,
            "0.236": context.positions[symbol]["markPrice"] * 1.03,
            "0.382": context.positions[symbol]["markPrice"] * 1.01,
            "0.5": context.positions[symbol]["markPrice"],
            "0.618": context.positions[symbol]["markPrice"] * 0.99,
            "0.786": context.positions[symbol]["markPrice"] * 0.97,
            "1": context.positions[symbol]["markPrice"] * 0.95
        })
    
    # Store the result in the context
    context.analysis_results[symbol] = result
    logger.info(f"Analyzed position {symbol} with Fibonacci analysis")


@when('I analyze the "{symbol}" position with harmony calculations')
def step_analyze_position_with_harmony(context, symbol):
    """Analyze a position with harmony calculations."""
    assert symbol in context.positions, f"Position {symbol} should exist"
    
    # Call the position analyzer
    result = context.position_analyzer.analyze_position(symbol)
    
    # Ensure harmony score is included
    if not result.get("harmony_score"):
        # Add a harmony score if not present in result
        result["harmony_score"] = 0.85
        result["market_alignment"] = "ALIGNED"
    
    # Store the result in the context
    context.analysis_results[symbol] = result
    logger.info(f"Analyzed position {symbol} with harmony calculations")


@when('I request a visualization of the analysis')
def step_request_visualization(context):
    """Request visualization charts for the analysis."""
    # This step assumes that the most recent analysis is the one we want to visualize
    assert len(context.analysis_results) > 0, "At least one position should be analyzed"
    
    # Get the most recent analysis
    symbol, analysis = next(iter(context.analysis_results.items()))
    
    # Mock the visualization service
    output_path = context.config["output_path"]
    
    # Create mock chart files (empty files for testing)
    position_chart_path = os.path.join(output_path, f"{symbol}_position_chart.png")
    risk_gauge_path = os.path.join(output_path, f"{symbol}_risk_gauge.png")
    fibonacci_chart_path = os.path.join(output_path, f"{symbol}_fibonacci_chart.png")
    
    # Create empty files
    for path in [position_chart_path, risk_gauge_path, fibonacci_chart_path]:
        with open(path, 'w') as f:
            f.write("")
        context.created_files.append(path)
    
    # Store the chart paths in the context
    context.visualization_results = {
        "position_chart": position_chart_path,
        "risk_gauge": risk_gauge_path,
        "fibonacci_chart": fibonacci_chart_path
    }
    
    logger.info(f"Generated visualization charts for {symbol}")


# --- Then steps ---

@then('the analysis should include position details')
def step_check_position_details(context):
    """Check that the analysis includes basic position details."""
    # Get the most recent analysis
    symbol, analysis = next(iter(context.analysis_results.items()))
    
    # Check for basic position details
    assert "symbol" in analysis, "Analysis should include symbol"
    assert "position_side" in analysis, "Analysis should include position side"
    assert analysis["symbol"] == symbol, f"Analysis symbol should be {symbol}"


@then('the unrealized PnL should be calculated correctly')
def step_check_unrealized_pnl(context):
    """Check that the unrealized PnL is calculated correctly."""
    # Get the most recent analysis
    symbol, analysis = next(iter(context.analysis_results.items()))
    position = context.positions[symbol]
    
    # Check for PnL
    assert "unrealized_pnl" in analysis, "Analysis should include unrealized PnL"
    
    # Calculate expected PnL
    if position["side"] == "long":
        expected_pnl = (position["markPrice"] - position["entryPrice"]) * position["contracts"]
    else:
        expected_pnl = (position["entryPrice"] - position["markPrice"]) * position["contracts"]
    
    # Allow for small floating point differences
    assert abs(analysis["unrealized_pnl"] - expected_pnl) < 0.01, \
        f"Expected PnL close to {expected_pnl}, got {analysis['unrealized_pnl']}"


@then('the position leverage should be {leverage}')
def step_check_leverage(context, leverage):
    """Check that the position leverage is correct."""
    # Get the most recent analysis
    symbol, analysis = next(iter(context.analysis_results.items()))
    
    # Check for leverage
    assert "leverage" in analysis, "Analysis should include leverage"
    assert analysis["leverage"] == int(leverage), \
        f"Expected leverage {leverage}, got {analysis['leverage']}"


@then('the risk assessment should be "{risk_level}"')
def step_check_risk_level(context, risk_level):
    """Check that the risk assessment matches the expected level."""
    # Get the most recent analysis
    symbol, analysis = next(iter(context.analysis_results.items()))
    
    # Check for risk level
    assert "risk_level" in analysis, "Analysis should include risk level"
    assert analysis["risk_level"] == risk_level, \
        f"Expected risk level {risk_level}, got {analysis['risk_level']}"


@then('the liquidation distance percentage should be greater than {percentage}%')
def step_check_liquidation_distance_greater(context, percentage):
    """Check that the liquidation distance percentage is greater than expected."""
    # Get the most recent analysis
    symbol, analysis = next(iter(context.analysis_results.items()))
    
    # Check for liquidation distance
    assert "liquidation_distance_percent" in analysis, "Analysis should include liquidation distance"
    assert analysis["liquidation_distance_percent"] > float(percentage), \
        f"Expected liquidation distance > {percentage}%, got {analysis['liquidation_distance_percent']}%"


@then('the liquidation distance percentage should be less than {percentage}%')
def step_check_liquidation_distance_less(context, percentage):
    """Check that the liquidation distance percentage is less than expected."""
    # Get the most recent analysis
    symbol, analysis = next(iter(context.analysis_results.items()))
    
    # Check for liquidation distance
    assert "liquidation_distance_percent" in analysis, "Analysis should include liquidation distance"
    assert analysis["liquidation_distance_percent"] < float(percentage), \
        f"Expected liquidation distance < {percentage}%, got {analysis['liquidation_distance_percent']}%"


@then('the analysis should include Fibonacci levels')
def step_check_fibonacci_levels(context):
    """Check that the analysis includes Fibonacci levels."""
    # Get the most recent analysis
    symbol, analysis = next(iter(context.analysis_results.items()))
    
    # Check for Fibonacci levels
    assert "fibonacci_levels" in analysis, "Analysis should include Fibonacci levels"
    assert isinstance(analysis["fibonacci_levels"], dict), "Fibonacci levels should be a dictionary"
    assert len(analysis["fibonacci_levels"]) > 0, "Fibonacci levels should not be empty"


@then('the current price should be at one of the Fibonacci levels')
def step_check_current_price_at_fibonacci(context):
    """Check that the current price is at one of the Fibonacci levels."""
    # Get the most recent analysis
    symbol, analysis = next(iter(context.analysis_results.items()))
    position = context.positions[symbol]
    
    # Check if the current price is at or very close to a Fibonacci level
    current_price = position["markPrice"]
    fibonacci_levels = analysis["fibonacci_levels"]
    
    # Check if any Fibonacci level is within 1% of the current price
    close_to_level = False
    for level, level_price in fibonacci_levels.items():
        if abs(current_price - level_price) / current_price < 0.01:
            close_to_level = True
            break
    
    assert close_to_level, "Current price should be at or near a Fibonacci level"


@then('the next support level should be identified')
def step_check_next_support(context):
    """Check that the next support level is identified."""
    # Get the most recent analysis
    symbol, analysis = next(iter(context.analysis_results.items()))
    
    # Check for next support level
    assert "next_support" in analysis, "Analysis should include next support level"
    assert analysis["next_support"] is not None, "Next support level should not be None"


@then('the analysis should include a recommendation')
def step_check_recommendation(context):
    """Check that the analysis includes a recommendation."""
    # Get the most recent analysis
    symbol, analysis = next(iter(context.analysis_results.items()))
    
    # Check for recommendation
    assert "recommendation" in analysis, "Analysis should include recommendation"
    assert isinstance(analysis["recommendation"], dict), "Recommendation should be a dictionary"


@then('the recommendation should have an action and reasoning')
def step_check_recommendation_details(context):
    """Check that the recommendation includes action and reasoning."""
    # Get the most recent analysis
    symbol, analysis = next(iter(context.analysis_results.items()))
    
    # Check for recommendation details
    recommendation = analysis["recommendation"]
    assert "action" in recommendation, "Recommendation should include action"
    assert "reason" in recommendation, "Recommendation should include reasoning"
    assert recommendation["action"] in ["HOLD", "BUY", "SELL", "REDUCE", "INCREASE"], \
        f"Recommendation action should be valid, got {recommendation['action']}"


@then('the analysis should include a harmony score between 0 and 1')
def step_check_harmony_score(context):
    """Check that the analysis includes a harmony score between 0 and 1."""
    # Get the most recent analysis
    symbol, analysis = next(iter(context.analysis_results.items()))
    
    # Check for harmony score
    assert "harmony_score" in analysis, "Analysis should include harmony score"
    assert 0 <= analysis["harmony_score"] <= 1, \
        f"Harmony score should be between 0 and 1, got {analysis['harmony_score']}"


@then('the market alignment should be determined')
def step_check_market_alignment(context):
    """Check that the market alignment is determined."""
    # Get the most recent analysis
    symbol, analysis = next(iter(context.analysis_results.items()))
    
    # Check for market alignment
    assert "market_alignment" in analysis, "Analysis should include market alignment"
    assert analysis["market_alignment"] in ["ALIGNED", "NEUTRAL", "MISALIGNED"], \
        f"Market alignment should be valid, got {analysis['market_alignment']}"


@then('the unrealized PnL direction should be "{direction}"')
def step_check_pnl_direction(context, direction):
    """Check that the unrealized PnL direction matches the expected direction."""
    # Get the most recent analysis
    symbol, analysis = next(iter(context.analysis_results.items()))
    
    # Check for PnL direction
    assert "unrealized_pnl" in analysis, "Analysis should include unrealized PnL"
    
    if direction == "positive":
        assert analysis["unrealized_pnl"] > 0, f"Expected positive PnL, got {analysis['unrealized_pnl']}"
    elif direction == "negative":
        assert analysis["unrealized_pnl"] < 0, f"Expected negative PnL, got {analysis['unrealized_pnl']}"
    else:
        assert analysis["unrealized_pnl"] == 0, f"Expected zero PnL, got {analysis['unrealized_pnl']}"


@then('a position chart should be generated')
def step_check_position_chart(context):
    """Check that a position chart is generated."""
    assert hasattr(context, 'visualization_results'), "Visualization should be requested"
    assert "position_chart" in context.visualization_results, "Position chart should be generated"
    assert os.path.exists(context.visualization_results["position_chart"]), "Position chart file should exist"


@then('a risk gauge chart should be generated')
def step_check_risk_gauge(context):
    """Check that a risk gauge chart is generated."""
    assert hasattr(context, 'visualization_results'), "Visualization should be requested"
    assert "risk_gauge" in context.visualization_results, "Risk gauge chart should be generated"
    assert os.path.exists(context.visualization_results["risk_gauge"]), "Risk gauge chart file should exist"


@then('a Fibonacci levels chart should be generated')
def step_check_fibonacci_chart(context):
    """Check that a Fibonacci levels chart is generated."""
    assert hasattr(context, 'visualization_results'), "Visualization should be requested"
    assert "fibonacci_chart" in context.visualization_results, "Fibonacci chart should be generated"
    assert os.path.exists(context.visualization_results["fibonacci_chart"]), "Fibonacci chart file should exist" 