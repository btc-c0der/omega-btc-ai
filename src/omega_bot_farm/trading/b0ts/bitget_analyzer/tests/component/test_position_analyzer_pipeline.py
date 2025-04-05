"""
Tests for the position analyzer pipeline component.

This test suite verifies that the position analyzer pipeline correctly
processes position data, performs analysis, and generates appropriate
recommendations.
"""
import pytest
from unittest.mock import patch, MagicMock

# Import the components being tested
# Note: These imports would need to be adjusted based on actual implementation
# paths in your project structure
try:
    from src.omega_bot_farm.trading.b0ts.bitget_analyzer.bitget_position_analyzer_b0t import (
        BitgetPositionAnalyzerBot,
        PositionAnalysisPipeline
    )
except ImportError:
    # Handle the case where the imports might be different
    pytest.skip("Required modules not available", allow_module_level=True)

class TestPositionAnalyzerPipeline:
    """Test the position analyzer pipeline component."""
    
    @pytest.fixture
    def pipeline(self, mock_exchange_service, mock_notification_service):
        """Create a test instance of the position analysis pipeline."""
        return PositionAnalysisPipeline(
            exchange_service=mock_exchange_service,
            notification_service=mock_notification_service,
            config={"risk_threshold": 0.1, "profit_target": 0.05}
        )
    
    def test_pipeline_initialization(self, pipeline):
        """Test that the pipeline initializes correctly."""
        assert pipeline is not None
        assert hasattr(pipeline, "analyze_positions")
    
    def test_position_data_collection(self, pipeline, mock_exchange_service):
        """Test that the pipeline correctly collects position data."""
        # Execute the relevant part of the pipeline
        position_data = pipeline._collect_position_data()
        
        # Verify mock was called
        mock_exchange_service.get_positions.assert_called_once()
        
        # Verify the data structure
        assert "positions" in position_data
        assert len(position_data["positions"]) > 0
        assert "account" in position_data
    
    def test_fibonacci_analysis_integration(self, pipeline, mock_exchange_service):
        """Test the integration of Fibonacci analysis in the pipeline."""
        # This test verifies that the Fibonacci analysis component is correctly
        # integrated into the pipeline and produces expected results
        
        # Mock the fibonacci analyzer component
        with patch("src.omega_bot_farm.trading.b0ts.bitget_analyzer.fibonacci.analyze") as mock_analyze:
            # Setup the mock to return predefined analysis
            mock_analyze.return_value = {
                "symbol": "BTCUSDT",
                "levels": {
                    "0.618": 65300,
                    "0.5": 66000,
                    "0.382": 66700
                },
                "current_price": 68000,
                "next_support": 66700
            }
            
            # Run the pipeline
            results = pipeline.analyze_positions()
            
            # Verify the mock was called
            assert mock_analyze.called
            
            # Verify the results include fibonacci analysis
            assert "fibonacci_analysis" in results
            assert results["fibonacci_analysis"]["BTCUSDT"]["next_support"] == 66700
    
    def test_risk_assessment(self, pipeline, sample_position_data):
        """Test the risk assessment component of the pipeline."""
        # Test that risk is correctly assessed for positions
        
        # Mock the _collect_position_data method to return our sample data
        pipeline._collect_position_data = MagicMock(return_value=sample_position_data)
        
        # Run the pipeline's risk assessment
        risk_assessment = pipeline.assess_position_risk()
        
        # Verify the risk assessment results
        assert "BTCUSDT" in risk_assessment
        assert "risk_level" in risk_assessment["BTCUSDT"]
        assert "liquidation_distance" in risk_assessment["BTCUSDT"]
    
    def test_recommendation_generation(self, pipeline, sample_position_data, fibonacci_analysis_result):
        """Test the recommendation generation component."""
        # Test that appropriate recommendations are generated based on
        # position data and technical analysis
        
        # Mock the pipeline methods
        pipeline._collect_position_data = MagicMock(return_value=sample_position_data)
        pipeline._analyze_with_fibonacci = MagicMock(return_value={"BTCUSDT": fibonacci_analysis_result})
        pipeline.assess_position_risk = MagicMock(return_value={
            "BTCUSDT": {
                "risk_level": "LOW",
                "liquidation_distance": 0.15
            }
        })
        
        # Run the recommendation generation
        recommendations = pipeline.generate_recommendations()
        
        # Verify the recommendations
        assert "BTCUSDT" in recommendations
        assert "action" in recommendations["BTCUSDT"]
        assert "reasoning" in recommendations["BTCUSDT"]
        
    def test_complete_pipeline_execution(self, pipeline, mock_exchange_service, mock_notification_service):
        """Test the complete execution of the pipeline."""
        # This is an integration test for the entire pipeline
        
        # Run the complete pipeline
        result = pipeline.run()
        
        # Verify the pipeline executed and produced expected results
        assert "positions" in result
        assert "risk_assessment" in result
        assert "recommendations" in result
        
        # Verify notifications were sent for critical recommendations
        if any(rec.get("priority") == "HIGH" for rec in result["recommendations"].values()):
            mock_notification_service.send_notification.assert_called() 