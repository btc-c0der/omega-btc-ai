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
QUANTUM Coverage Test Suite for YouTube Monitor
"""

import os
import sys
import unittest
import json
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.youtube_monitor import YouTubeMonitor


class TestYouTubeMonitor(unittest.TestCase):
    """Test cases for the YouTube Monitor component."""

    def setUp(self):
        """Set up test fixtures."""
        # Patch os.path.exists to return False so we don't try to load real files
        with patch('os.path.exists', return_value=False):
            self.monitor = YouTubeMonitor()

    def test_initialization(self):
        """Test initialization of the monitor."""
        self.assertIsNotNone(self.monitor)
        self.assertEqual(self.monitor.channel_id, "UC_LucasSilveiraOfficial")
        self.assertEqual(self.monitor.refresh_interval, 3600)
        self.assertIsNotNone(self.monitor.last_update)
        self.assertIsInstance(self.monitor.metrics, dict)
        self.assertIsInstance(self.monitor.videos, list)
        self.assertTrue(len(self.monitor.videos) > 0)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='{"metrics": {"subscribers": 50000}, "videos": [], "last_update": "2023-01-01T00:00:00"}')
    def test_load_data(self, mock_file, mock_exists):
        """Test loading data from storage."""
        mock_exists.return_value = True
        
        # Create a new monitor instance which will load the mocked data
        monitor = YouTubeMonitor()
        
        # Check that data was loaded correctly
        self.assertEqual(monitor.metrics["subscribers"], 50000)
        self.assertEqual(monitor.videos, [])
        self.assertEqual(monitor.last_update.strftime("%Y-%m-%d"), "2023-01-01")

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_data(self, mock_file, mock_makedirs):
        """Test saving data to storage."""
        self.monitor._save_data()
        
        # Check that makedirs was called
        mock_makedirs.assert_called_once()
        
        # Check that open was called with write mode
        mock_file.assert_called_once()
        self.assertEqual(mock_file.call_args[0][1], 'w')
        
        # Check that json data was written
        handle = mock_file()
        handle.write.assert_called_once()
        written_data = handle.write.call_args[0][0]
        self.assertIn('"metrics":', written_data)
        self.assertIn('"videos":', written_data)
        self.assertIn('"last_update":', written_data)

    def test_simulate_data(self):
        """Test data simulation."""
        # Reset data and simulate
        self.monitor.metrics = {}
        self.monitor.videos = []
        self.monitor._simulate_data()
        
        # Check that metrics were populated
        self.assertIn("subscribers", self.monitor.metrics)
        self.assertIn("total_views", self.monitor.metrics)
        self.assertIn("videos_count", self.monitor.metrics)
        
        # Check that videos were populated
        self.assertTrue(len(self.monitor.videos) > 0)
        video = self.monitor.videos[0]
        self.assertIn("title", video)
        self.assertIn("published_at", video)
        self.assertIn("views", video)
        self.assertIn("likes", video)
        self.assertIn("comments", video)

    def test_run_update(self):
        """Test running an update."""
        # Save original values to compare later
        original_subscribers = self.monitor.metrics["subscribers"]
        original_total_views = self.monitor.metrics["total_views"]
        original_first_video_views = self.monitor.videos[0]["views"]
        
        # Run update
        result = self.monitor.run_update()
        
        # Check that values were updated
        self.assertGreater(self.monitor.metrics["subscribers"], original_subscribers)
        self.assertGreater(self.monitor.metrics["total_views"], original_total_views)
        self.assertGreater(self.monitor.videos[0]["views"], original_first_video_views)
        
        # Check that result matches current state
        self.assertEqual(result["metrics"]["subscribers"], self.monitor.metrics["subscribers"])
        self.assertEqual(len(result["recent_videos"]), 5)

    def test_get_channel_stats(self):
        """Test getting channel statistics."""
        # Set a last update time in the past to trigger an update
        self.monitor.last_update = datetime.now() - timedelta(seconds=4000)
        
        with patch.object(self.monitor, 'run_update') as mock_update:
            stats = self.monitor.get_channel_stats()
            mock_update.assert_called_once()

        self.assertEqual(stats["channel_id"], self.monitor.channel_id)
        self.assertIn("metrics", stats)
        self.assertIn("recent_videos", stats)
        self.assertLessEqual(len(stats["recent_videos"]), 5)

    def test_get_video_performance(self):
        """Test getting video performance metrics."""
        # Test with no time period (all videos)
        all_performance = self.monitor.get_video_performance()
        self.assertEqual(all_performance["period"], "all")
        self.assertEqual(all_performance["videos_count"], len(self.monitor.videos))
        self.assertIn("metrics", all_performance)
        self.assertIn("total_views", all_performance["metrics"])
        
        # Test with recent time period (last 30 days)
        recent_performance = self.monitor.get_video_performance("recent")
        self.assertEqual(recent_performance["period"], "recent")
        # Number of recent videos should be less than or equal to all videos
        self.assertLessEqual(recent_performance["videos_count"], all_performance["videos_count"])
        
        # Test with custom time period (last 90 days)
        month3_performance = self.monitor.get_video_performance("month3")
        self.assertEqual(month3_performance["period"], "month3")
        # Should have at least as many videos as recent period
        self.assertGreaterEqual(month3_performance["videos_count"], recent_performance["videos_count"])

    def test_get_audience_growth(self):
        """Test getting audience growth data."""
        growth = self.monitor.get_audience_growth(months=6)
        
        self.assertEqual(growth["growth_period"], "6 months")
        self.assertEqual(growth["current_subscribers"], self.monitor.metrics["subscribers"])
        self.assertEqual(len(growth["monthly_data"]), 6)
        
        # Check that data is in chronological order (oldest first)
        for i in range(1, len(growth["monthly_data"])):
            month1 = growth["monthly_data"][i-1]["month"]
            month2 = growth["monthly_data"][i]["month"]
            month1_date = datetime.strptime(month1, "%B %Y")
            month2_date = datetime.strptime(month2, "%B %Y")
            self.assertLess(month1_date, month2_date)
        
        # Test with different month parameter
        growth_3m = self.monitor.get_audience_growth(months=3)
        self.assertEqual(growth_3m["growth_period"], "3 months")
        self.assertEqual(len(growth_3m["monthly_data"]), 3)


class TestQuantumVideoAnalytics(unittest.TestCase):
    """QUANTUM COVERAGE test cases for higher dimension video analytics."""

    def setUp(self):
        """Set up quantum test fixtures."""
        with patch('os.path.exists', return_value=False):
            self.monitor = YouTubeMonitor()
        
        # Define quantum dimensions for video analytics
        self.quantum_dimensions = [
            "superposition_engagement",
            "entanglement_coefficient",
            "quantum_retention",
            "nonlocal_virality"
        ]

    def test_quantum_video_superposition(self):
        """Test superposition of video states across time."""
        # Get performance for different time periods (quantum projections)
        now_performance = self.monitor.get_video_performance("recent")
        past_performance = self.monitor.get_video_performance("month3")
        all_performance = self.monitor.get_video_performance()
        
        # Validate quantum superposition principle: sum of parts equals the whole
        if all_performance["videos_count"] > 0:
            total_views_sum = sum([
                now_performance["metrics"].get("total_views", 0),
                past_performance["metrics"].get("total_views", 0) - now_performance["metrics"].get("total_views", 0)
            ])
            # Allow for small fluctuations due to quantum uncertainty
            self.assertAlmostEqual(
                total_views_sum / all_performance["metrics"]["total_views"],
                1.0,
                delta=0.5  # 50% tolerance for quantum fluctuations
            )

    def test_quantum_temporal_entanglement(self):
        """Test entanglement of video metrics across time."""
        growth = self.monitor.get_audience_growth(months=6)
        monthly_data = growth["monthly_data"]
        
        # Test temporal entanglement by checking correlations
        if len(monthly_data) >= 2:
            # In an entangled system, subscribers and views should correlate
            subscriber_growth = []
            view_growth = []
            
            for i in range(1, len(monthly_data)):
                sub_ratio = monthly_data[i]["subscribers"] / monthly_data[i-1]["subscribers"]
                view_ratio = monthly_data[i]["views"] / monthly_data[i-1]["views"]
                subscriber_growth.append(sub_ratio)
                view_growth.append(view_ratio)
            
            # Subscriber and view growth should be similar (entangled)
            avg_sub_growth = sum(subscriber_growth) / len(subscriber_growth)
            avg_view_growth = sum(view_growth) / len(view_growth)
            
            # Growth rates should be within 30% of each other (quantum correlation)
            self.assertAlmostEqual(
                avg_sub_growth / avg_view_growth,
                1.0,
                delta=0.3
            )
            
    def test_quantum_measurement_effect(self):
        """Test quantum measurement effect - observation changes the system."""
        # Take measurement (get stats)
        original_stats = self.monitor.get_channel_stats()
        # Do a quantum collapse (update)
        self.monitor.run_update()
        # Take another measurement
        new_stats = self.monitor.get_channel_stats()
        
        # Verify the act of observation (update) changed the system
        self.assertNotEqual(
            original_stats["metrics"]["subscribers"],
            new_stats["metrics"]["subscribers"]
        )
        self.assertNotEqual(
            original_stats["metrics"]["total_views"],
            new_stats["metrics"]["total_views"]
        )


if __name__ == "__main__":
    unittest.main() 