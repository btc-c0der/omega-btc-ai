"""
End-to-end test for the full position analysis workflow.

This test verifies that the entire position analysis pipeline works
correctly from start to finish, including data fetching, analysis,
visualization, and notification.
"""
import os
import pytest
import logging
from pathlib import Path

logger = logging.getLogger('e2e_tests.full_workflow')

@pytest.mark.e2e
def test_full_analysis_execution(position_analyzer_bot, e2e_config):
    """
    Test the full position analysis workflow.
    
    This test simulates a complete run of the position analyzer bot,
    verifying that all components work together as expected.
    """
    # Skip if we couldn't create the bot
    if position_analyzer_bot is None:
        pytest.skip("Position analyzer bot not available")
    
    # Run the complete analysis pipeline
    logger.info("Starting full analysis workflow test")
    results = position_analyzer_bot.run_analysis()
    
    # Verify the results structure
    assert results is not None, "Analysis results should not be None"
    assert "positions" in results, "Results should include position data"
    assert "risk_assessment" in results, "Results should include risk assessment"
    assert "recommendations" in results, "Results should include recommendations"
    assert "harmony_analysis" in results, "Results should include harmony analysis"
    
    # Check that we have analysis for each test symbol
    for symbol in e2e_config["test_symbols"]:
        if symbol in results["positions"]:
            assert symbol in results["risk_assessment"], f"Missing risk assessment for {symbol}"
            assert symbol in results["recommendations"], f"Missing recommendation for {symbol}"
            assert symbol in results["harmony_analysis"], f"Missing harmony analysis for {symbol}"
    
    # Verify that visualization files were created
    output_path = Path(e2e_config["output_path"])
    
    # Check for at least one chart file per position
    chart_files = list(output_path.glob("*.png"))
    assert len(chart_files) > 0, "No chart files were generated"
    
    # Verify that at least one report file was created
    report_files = list(output_path.glob("*_report.json"))
    assert len(report_files) > 0, "No report files were generated"
    
    logger.info(f"Analysis workflow test completed successfully")
    return results

@pytest.mark.e2e
def test_risk_detection_workflow(position_analyzer_bot, exchange_service, notification_service, e2e_config):
    """
    Test the risk detection and notification workflow.
    
    This test verifies that high-risk positions are properly 
    identified and notifications are sent.
    """
    # Skip if we couldn't create the bot
    if position_analyzer_bot is None:
        pytest.skip("Position analyzer bot not available")
    
    # Configure a high-risk position
    if hasattr(exchange_service, "set_mock_position"):
        # Set up a risky position (close to liquidation price)
        exchange_service.set_mock_position({
            "symbol": "BTCUSDT",
            "side": "long",
            "contracts": 1.0,
            "entryPrice": 65000,
            "markPrice": 61000,  # Price is dropping towards liquidation
            "leverage": 20,      # High leverage
            "liquidationPrice": 60000,
            "marginType": "isolated"
        })
    
    # Run the analysis
    logger.info("Starting risk detection workflow test")
    results = position_analyzer_bot.run_analysis()
    
    # Verify risk was detected correctly
    assert "BTCUSDT" in results["risk_assessment"], "Should have risk assessment for BTCUSDT"
    btc_risk = results["risk_assessment"]["BTCUSDT"]
    assert btc_risk["risk_level"] in ["HIGH", "EXTREME"], f"Risk level should be HIGH or EXTREME, got {btc_risk['risk_level']}"
    
    # Verify notification was sent for the high risk
    assert len(notification_service.notifications) > 0, "No notifications were sent"
    
    # Find notification related to high risk
    risk_notifications = [
        n for n in notification_service.notifications 
        if "risk" in str(n).lower() or "liquidation" in str(n).lower()
    ]
    assert len(risk_notifications) > 0, "No risk-related notifications were sent"
    
    logger.info("Risk detection workflow test completed successfully")
    return results

@pytest.mark.e2e
def test_multiple_timeframe_analysis(position_analyzer_bot, e2e_config):
    """
    Test analysis across multiple timeframes.
    
    This test verifies that the position analyzer correctly
    analyzes positions across different timeframes.
    """
    # Skip if we couldn't create the bot
    if position_analyzer_bot is None:
        pytest.skip("Position analyzer bot not available")
    
    # Run the analysis
    logger.info("Starting multiple timeframe analysis test")
    
    # Get a reference to the analysis pipeline
    pipeline = position_analyzer_bot.analysis_pipeline
    
    # Analyze for each timeframe
    timeframe_results = {}
    for timeframe in e2e_config["test_timeframes"]:
        logger.info(f"Analyzing timeframe {timeframe}")
        results = pipeline.analyze_timeframe("BTCUSDT", timeframe)
        timeframe_results[timeframe] = results
        
        # Verify timeframe-specific results
        assert results is not None, f"Analysis for timeframe {timeframe} returned None"
        assert "fibonacci_levels" in results, f"Missing Fibonacci levels for {timeframe}"
        assert "trend" in results, f"Missing trend for {timeframe}"
    
    # Verify differences between timeframes
    # Different timeframes should have at least some variation in results
    trends = [results["trend"] for results in timeframe_results.values()]
    assert len(set(trends)) > 1, "All timeframes have identical trends, expected some variation"
    
    # Verify that overall analysis was performed
    overall_results = position_analyzer_bot.analyze_position("BTCUSDT")
    assert "timeframe_analysis" in overall_results, "Missing timeframe analysis in overall results"
    assert len(overall_results["timeframe_analysis"]) > 1, "Expected analysis for multiple timeframes"
    
    logger.info("Multiple timeframe analysis test completed successfully")
    return timeframe_results

@pytest.mark.e2e
def test_harmony_threshold_impact(position_analyzer_bot, e2e_config):
    """
    Test how different harmony thresholds impact recommendations.
    
    This test verifies that changing harmony thresholds appropriately
    affects the analysis results and recommendations.
    """
    # Skip if we couldn't create the bot
    if position_analyzer_bot is None:
        pytest.skip("Position analyzer bot not available")
    
    # Run analysis with different harmony thresholds
    logger.info("Starting harmony threshold impact test")
    
    threshold_results = {}
    for threshold in e2e_config["test_harmony_thresholds"]:
        logger.info(f"Testing harmony threshold {threshold}")
        
        # Temporarily set the harmony threshold
        original_threshold = position_analyzer_bot.config.get("harmony_threshold")
        position_analyzer_bot.config["harmony_threshold"] = threshold
        
        # Run analysis
        results = position_analyzer_bot.analyze_position("BTCUSDT")
        threshold_results[threshold] = results
        
        # Restore original threshold
        if original_threshold is not None:
            position_analyzer_bot.config["harmony_threshold"] = original_threshold
        
        # Verify threshold-specific results
        assert results is not None, f"Analysis with threshold {threshold} returned None"
        assert "harmony_score" in results, f"Missing harmony score with threshold {threshold}"
        assert "recommendation" in results, f"Missing recommendation with threshold {threshold}"
    
    # Verify that different thresholds produce different recommendations
    # Higher thresholds should result in more conservative recommendations
    recommendations = [results["recommendation"]["action"] for results in threshold_results.values()]
    assert len(set(recommendations)) > 1, "All thresholds produced identical recommendations"
    
    # Verify that harmony scores are consistent
    harmony_scores = [results["harmony_score"] for results in threshold_results.values()]
    assert all(0 <= score <= 1 for score in harmony_scores), "Harmony scores should be between 0 and 1"
    
    logger.info("Harmony threshold impact test completed successfully")
    return threshold_results 