
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
Tests for the position visualization component.

This test suite verifies that the position visualization component correctly
generates charts and visual representations of position data and analysis.
"""
import pytest
import os
import io
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing

from unittest.mock import patch, MagicMock

class TestVisualizationComponent:
    """Tests for the position visualization component."""
    
    @pytest.fixture
    def visualization_service(self, mock_exchange_service):
        """Creates a visualization service instance."""
        # Try importing the actual service, skip if not available
        viz_service = pytest.importorskip(
            "src.omega_bot_farm.trading.b0ts.bitget_analyzer.visualization"
        ).VisualizationService
        
        # Create the service
        return viz_service(exchange_service=mock_exchange_service)
    
    @pytest.fixture
    def sample_position_analysis(self):
        """Provides sample position analysis data for visualization testing."""
        return {
            "symbol": "BTCUSDT",
            "position_side": "LONG",
            "entry_price": 65000,
            "current_price": 68000,
            "unrealized_pnl": 1500,
            "unrealized_pnl_percent": 4.6,
            "leverage": 10,
            "liquidation_price": 59000,
            "risk_level": "LOW",
            "fibonacci_levels": {
                "0": 68000,
                "0.236": 67200,
                "0.382": 66700,
                "0.5": 66000,
                "0.618": 65300,
                "0.786": 64600,
                "1": 64000
            },
            "harmony_score": 0.85
        }
    
    def test_position_chart_generation(self, visualization_service, sample_position_analysis):
        """Test generation of position charts."""
        # Generate a position chart
        chart_buffer = visualization_service.generate_position_chart(sample_position_analysis)
        
        # Verify the chart was generated
        assert chart_buffer is not None
        assert isinstance(chart_buffer, io.BytesIO)
        assert chart_buffer.getbuffer().nbytes > 0
    
    def test_fibonacci_visualization(self, visualization_service, sample_position_analysis):
        """Test visualization of Fibonacci levels."""
        # Generate a Fibonacci levels chart
        fib_chart = visualization_service.generate_fibonacci_chart(
            symbol="BTCUSDT",
            fibonacci_levels=sample_position_analysis["fibonacci_levels"],
            current_price=sample_position_analysis["current_price"],
            entry_price=sample_position_analysis["entry_price"]
        )
        
        # Verify the chart
        assert fib_chart is not None
        assert isinstance(fib_chart, io.BytesIO)
        assert fib_chart.getbuffer().nbytes > 0
    
    def test_risk_gauge_visualization(self, visualization_service, sample_position_analysis):
        """Test generation of risk gauge visualizations."""
        # Generate a risk gauge
        risk_gauge = visualization_service.generate_risk_gauge(
            risk_level=sample_position_analysis["risk_level"],
            liquidation_distance_percent=10.0  # 10% from liquidation
        )
        
        # Verify the gauge
        assert risk_gauge is not None
        assert isinstance(risk_gauge, io.BytesIO)
        assert risk_gauge.getbuffer().nbytes > 0
    
    def test_harmony_chart_generation(self, visualization_service, sample_position_analysis):
        """Test generation of harmony score charts."""
        # Generate a harmony chart
        harmony_chart = visualization_service.generate_harmony_chart(
            harmony_score=sample_position_analysis["harmony_score"],
            symbol=sample_position_analysis["symbol"]
        )
        
        # Verify the chart
        assert harmony_chart is not None
        assert isinstance(harmony_chart, io.BytesIO)
        assert harmony_chart.getbuffer().nbytes > 0
    
    def test_portfolio_distribution_chart(self, visualization_service, mock_exchange_service):
        """Test generation of portfolio distribution charts."""
        # Mock the position data
        mock_exchange_service.get_positions.return_value = [
            {
                "symbol": "BTCUSDT",
                "positionSide": "LONG",
                "position": 0.5,
                "entryPrice": 65000,
                "markPrice": 68000,
                "unrealizedProfit": 1500,
                "margin": 3250
            },
            {
                "symbol": "ETHUSDT",
                "positionSide": "SHORT",
                "position": 2.0,
                "entryPrice": 3500,
                "markPrice": 3400,
                "unrealizedProfit": 200,
                "margin": 1400
            },
            {
                "symbol": "SOLUSDT",
                "positionSide": "LONG",
                "position": 10.0,
                "entryPrice": 150,
                "markPrice": 160,
                "unrealizedProfit": 100,
                "margin": 300
            }
        ]
        
        # Generate a portfolio distribution chart
        portfolio_chart = visualization_service.generate_portfolio_distribution_chart()
        
        # Verify the chart
        assert portfolio_chart is not None
        assert isinstance(portfolio_chart, io.BytesIO)
        assert portfolio_chart.getbuffer().nbytes > 0
    
    def test_combined_analysis_dashboard(self, visualization_service, sample_position_analysis, mock_exchange_service):
        """Test generation of a combined analysis dashboard."""
        # Mock harmony data
        harmony_data = {
            "overall_harmony": 0.85,
            "price_volume_harmony": 0.82,
            "fibonacci_retracement_harmony": 0.88,
            "market_alignment": "ALIGNED"
        }
        
        # Generate a dashboard with multiple charts
        dashboard = visualization_service.generate_analysis_dashboard(
            position_analysis=sample_position_analysis,
            harmony_data=harmony_data
        )
        
        # Verify the dashboard
        assert dashboard is not None
        assert isinstance(dashboard, io.BytesIO)
        assert dashboard.getbuffer().nbytes > 0
    
    def test_chart_save_functionality(self, visualization_service, sample_position_analysis, tmp_path):
        """Test saving charts to disk."""
        # Generate a chart
        chart = visualization_service.generate_position_chart(sample_position_analysis)
        
        # Define a temp file path
        chart_path = os.path.join(tmp_path, "test_chart.png")
        
        # Save the chart
        saved = visualization_service.save_chart(chart, chart_path)
        
        # Verify the chart was saved
        assert saved
        assert os.path.exists(chart_path)
        assert os.path.getsize(chart_path) > 0 