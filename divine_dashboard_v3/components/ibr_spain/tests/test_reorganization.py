#!/usr/bin/env python3

"""
Reorganization Test for IBR España Component

This script verifies that all components are properly importable
after the directory reorganization.
"""

import os
import sys
import unittest

# Add the parent directory to the path so we can import the component
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
sys.path.append(os.path.dirname(parent_dir))  # For components

# Try importing from the standalone package
try:
    from standalone.ibr_standalone import InstagramManager, create_ibr_interface
    print("✅ Successfully imported from standalone package")
except ImportError as e:
    print(f"❌ Failed to import from standalone package: {e}")

# Try importing from the micro_modules package
try:
    from micro_modules.instagram_integration import InstagramIntegration
    from micro_modules.sermon_library import SermonLibrary
    from micro_modules.prayer_requests import PrayerRequests
    from micro_modules.church_events import ChurchEvents
    from micro_modules.devotionals import Devotionals
    print("✅ Successfully imported from micro_modules package")
except ImportError as e:
    print(f"❌ Failed to import from micro_modules package: {e}")

# Test that the main component interface can be imported
try:
    from ibr_dashboard import create_ibr_interface
    print("✅ Successfully imported main component interface")
except ImportError as e:
    print(f"❌ Failed to import main component interface: {e}")

class TestReorganization(unittest.TestCase):
    """Test that the reorganized components are working properly."""
    
    def test_instagram_integration(self):
        """Test the Instagram integration."""
        try:
            integration = InstagramIntegration()
            stats = integration.get_instagram_stats()
            self.assertIsNotNone(stats)
            self.assertIn("followers", stats)
            self.assertIn("posts", stats)
            print("✅ Instagram integration is working properly")
        except Exception as e:
            self.fail(f"Instagram integration test failed: {e}")
            
    def test_sermon_library(self):
        """Test the sermon library."""
        try:
            library = SermonLibrary()
            sermons = library.get_recent_sermons()
            self.assertIsNotNone(sermons)
            self.assertTrue(isinstance(sermons, list))
            print("✅ Sermon library is working properly")
        except Exception as e:
            self.fail(f"Sermon library test failed: {e}")
            
    def test_prayer_requests(self):
        """Test the prayer requests module."""
        try:
            prayers = PrayerRequests()
            prayers.add_request("Test User", "Please pray for me")
            requests = prayers.get_recent_requests()
            self.assertIsNotNone(requests)
            self.assertTrue(isinstance(requests, list))
            print("✅ Prayer requests module is working properly")
        except Exception as e:
            self.fail(f"Prayer requests test failed: {e}")
            
    def test_church_events(self):
        """Test the church events module."""
        try:
            events = ChurchEvents()
            upcoming = events.get_upcoming_events()
            self.assertIsNotNone(upcoming)
            self.assertTrue(isinstance(upcoming, list))
            print("✅ Church events module is working properly")
        except Exception as e:
            self.fail(f"Church events test failed: {e}")
            
    def test_devotionals(self):
        """Test the devotionals module."""
        try:
            devos = Devotionals()
            daily = devos.get_daily_devotional()
            self.assertIsNotNone(daily)
            self.assertTrue(isinstance(daily, dict))
            print("✅ Devotionals module is working properly")
        except Exception as e:
            self.fail(f"Devotionals test failed: {e}")

if __name__ == "__main__":
    print("Running reorganization tests...")
    unittest.main() 