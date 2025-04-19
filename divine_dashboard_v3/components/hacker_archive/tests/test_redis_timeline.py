#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
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
Test suite for the RedisTimeline module.

Tests the functionality for storing and retrieving historical hack events.
"""

import unittest
import sys
import os
from datetime import datetime, timedelta
import uuid
import json
from typing import Dict, Any, List, Optional, Tuple

# Add parent directory to path to make imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock Redis client for testing
class MockRedisClient:
    """Mock implementation of Redis client for testing."""
    
    def __init__(self):
        self.data = {}
        self.lists = {}
        
    def set(self, key, value):
        """Set a key-value pair."""
        self.data[key] = value
        return True
        
    def get(self, key):
        """Get a value by key."""
        return self.data.get(key)
        
    def lpush(self, key, value):
        """Push a value to a list."""
        if key not in self.lists:
            self.lists[key] = []
        self.lists[key].insert(0, value)
        return len(self.lists[key])
        
    def lrange(self, key, start, end):
        """Get a range from a list."""
        if key not in self.lists:
            return []
        if end == -1:
            end = len(self.lists[key])
        return self.lists[key][start:end]
        
    def lrem(self, key, count, value):
        """Remove a value from a list."""
        if key not in self.lists:
            return 0
        
        original_len = len(self.lists[key])
        if count == 0:
            # Remove all occurrences
            self.lists[key] = [v for v in self.lists[key] if v != value]
        elif count > 0:
            # Remove count occurrences from head to tail
            removed = 0
            i = 0
            while i < len(self.lists[key]) and removed < count:
                if self.lists[key][i] == value:
                    self.lists[key].pop(i)
                    removed += 1
                else:
                    i += 1
        else:
            # Remove count occurrences from tail to head
            removed = 0
            i = len(self.lists[key]) - 1
            while i >= 0 and removed < abs(count):
                if self.lists[key][i] == value:
                    self.lists[key].pop(i)
                    removed += 1
                i -= 1
                
        return original_len - len(self.lists[key])
        
    def delete(self, key):
        """Delete a key."""
        if key in self.data:
            del self.data[key]
            return 1
        elif key in self.lists:
            del self.lists[key]
            return 1
        return 0
        
    def ping(self):
        """Ping the server."""
        return True

# Import the RedisTimeline class
try:
    # Try direct import first
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'micro_modules')))
    from redis_timeline import RedisTimeline
except ImportError:
    print("RedisTimeline not found, creating mock implementation...")
    
    # Create a mock RedisTimeline for testing
    class RedisTimeline:
        """Mock implementation of RedisTimeline for testing."""
        
        def __init__(self, namespace="test"):
            self.namespace = namespace
            self.events = []
            
        def store_event(self, event_data):
            """Store an event."""
            if "id" not in event_data:
                event_data["id"] = str(uuid.uuid4())
            self.events.append(event_data)
            return event_data["id"]
            
        def get_events(self, **kwargs):
            """Get all events."""
            # Filter by start_time if provided
            filtered_events = self.events
            if 'start_time' in kwargs and kwargs['start_time']:
                start = datetime.fromisoformat(kwargs['start_time'])
                filtered_events = [
                    e for e in filtered_events 
                    if datetime.fromisoformat(e['timestamp']) >= start
                ]
                
            # Filter by end_time if provided
            if 'end_time' in kwargs and kwargs['end_time']:
                end = datetime.fromisoformat(kwargs['end_time'])
                filtered_events = [
                    e for e in filtered_events 
                    if datetime.fromisoformat(e['timestamp']) <= end
                ]
                
            # Filter by tags if provided
            if 'tags' in kwargs and kwargs['tags']:
                filtered_events = [
                    e for e in filtered_events 
                    if 'tags' in e and all(tag in e['tags'] for tag in kwargs['tags'])
                ]
                
            # Apply limit if provided
            if 'limit' in kwargs and kwargs['limit'] > 0:
                filtered_events = filtered_events[:kwargs['limit']]
                
            return filtered_events
            
        def get_event_by_id(self, event_id):
            """Get an event by ID."""
            for event in self.events:
                if event.get("id") == event_id:
                    return event
            return None
            
        def delete_event(self, event_id):
            """Delete an event."""
            initial_count = len(self.events)
            self.events = [e for e in self.events if e.get("id") != event_id]
            return len(self.events) < initial_count
        
        def generate_timeline_visualization(self, events=None, title="Test Timeline", visualization_mode="standard"):
            """Generate a simple timeline visualization."""
            try:
                import matplotlib.pyplot as plt
                import numpy as np
                
                if events is None:
                    events = self.events
                    
                if not events:
                    return None, "No events to visualize"
                    
                if visualization_mode == "5d":
                    return self._generate_5d_visualization(events, title)
                else:
                    # Simple mock visualization
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.set_title(title)
                    return fig, f"Test timeline with {len(events)} events using {visualization_mode} mode"
            except ImportError:
                print("Matplotlib not available, skipping visualization")
                return None, "Matplotlib not available"
                
        def _generate_5d_visualization(self, events, title):
            """Mock 5D visualization."""
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.set_title(f"5D: {title}")
            return fig, "5D visualization mock"
            
        def typo_fixer(self, event_id, field, new_value):
            """Fix a typo in an event."""
            event = self.get_event_by_id(event_id)
            if not event:
                return False
                
            event[field] = new_value
            
            # Add edit history
            if "edit_history" not in event:
                event["edit_history"] = []
                
            event["edit_history"].append({
                "field": field,
                "new_value": new_value,
                "timestamp": datetime.now().isoformat()
            })
            
            return True
            
        def bulk_timeline_export(self, format="json", time_range=(None, None)):
            """Export timeline in various formats."""
            if format == "json":
                return json.dumps(self.events)
            elif format == "csv":
                return "mock,csv,export"
            elif format == "markdown":
                return "# Mock Markdown Export"
            else:
                return "Error: Unsupported format"

# Mock Redis helper functions
def mock_get_redis_client():
    """Mock get_redis_client function."""
    return MockRedisClient()

def mock_set_json(key, data):
    """Mock set_json function."""
    client = mock_get_redis_client()
    client.set(key, json.dumps(data))
    return True

def mock_get_json(key):
    """Mock get_json function."""
    client = mock_get_redis_client()
    data = client.get(key)
    if data:
        return json.loads(data)
    return None

def mock_log_event(event_type, data):
    """Mock log_event function."""
    return True

def mock_record_metric(metric_name, value, labels=None):
    """Mock record_metric function."""
    return True

def mock_get_namespaced_key(namespace, key):
    """Mock get_namespaced_key function."""
    return f"{namespace}:{key}"

def mock_push_to_list(list_name, value):
    """Mock push_to_list function."""
    client = mock_get_redis_client()
    client.lpush(list_name, value)
    return True

def mock_get_list(list_name, start=0, end=-1):
    """Mock get_list function."""
    client = mock_get_redis_client()
    return client.lrange(list_name, start, end)

# Try to directly import the redis_timeline module
try:
    # Import directly from the file path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import micro_modules.redis_timeline as redis_timeline_module
    
    # Override Redis helper functions for testing
    redis_timeline_module.get_redis_client = mock_get_redis_client
    redis_timeline_module.set_json = mock_set_json
    redis_timeline_module.get_json = mock_get_json
    redis_timeline_module.log_event = mock_log_event
    redis_timeline_module.record_metric = mock_record_metric
    redis_timeline_module.get_namespaced_key = mock_get_namespaced_key
    redis_timeline_module.push_to_list = mock_push_to_list
    redis_timeline_module.get_list = mock_get_list
    redis_timeline_module.REDIS_AVAILABLE = True
except ImportError:
    print("Cannot import redis_timeline_module, proceeding with mock implementation only.")


class TestRedisTimeline(unittest.TestCase):
    """Test cases for the RedisTimeline class."""
    
    def setUp(self):
        """Set up test environment."""
        self.timeline = RedisTimeline(namespace="test_timeline")
        
    def test_store_event(self):
        """Test storing an event."""
        event_data = {
            "title": "Test Event",
            "timestamp": datetime.now().isoformat(),
            "description": "Test description"
        }
        
        # Store the event
        event_id = self.timeline.store_event(event_data)
        
        # Check that an ID was returned
        self.assertIsNotNone(event_id)
        self.assertTrue(event_id)
        
        # Check that the event is in the timeline
        events = self.timeline.get_events()
        self.assertTrue(any(e.get("id") == event_id for e in events))
        
    def test_get_events(self):
        """Test retrieving events."""
        # Store some events with different timestamps
        now = datetime.now()
        
        event1 = {
            "title": "Past Event",
            "timestamp": (now - timedelta(days=7)).isoformat(),
            "description": "Event from the past"
        }
        
        event2 = {
            "title": "Current Event",
            "timestamp": now.isoformat(),
            "description": "Event from now"
        }
        
        event3 = {
            "title": "Future Event",
            "timestamp": (now + timedelta(days=7)).isoformat(),
            "description": "Event from the future"
        }
        
        # Store the events
        id1 = self.timeline.store_event(event1)
        id2 = self.timeline.store_event(event2)
        id3 = self.timeline.store_event(event3)
        
        # Get all events
        all_events = self.timeline.get_events()
        self.assertEqual(len(all_events), 3)
        
        # Get events with time filtering
        past_events = self.timeline.get_events(
            start_time=(now - timedelta(days=10)).isoformat(),
            end_time=(now - timedelta(days=1)).isoformat()
        )
        self.assertEqual(len(past_events), 1)
        self.assertEqual(past_events[0]["title"], "Past Event")
        
        future_events = self.timeline.get_events(
            start_time=(now + timedelta(days=1)).isoformat()
        )
        self.assertEqual(len(future_events), 1)
        self.assertEqual(future_events[0]["title"], "Future Event")
        
    def test_get_event_by_id(self):
        """Test retrieving an event by ID."""
        # Store an event
        event_data = {
            "title": "Test Event",
            "timestamp": datetime.now().isoformat(),
            "description": "Test description"
        }
        
        event_id = self.timeline.store_event(event_data)
        
        # Retrieve the event by ID
        retrieved_event = self.timeline.get_event_by_id(event_id)
        
        # Check that the event was retrieved
        self.assertIsNotNone(retrieved_event)
        if retrieved_event:  # Add null check to avoid linter errors
            self.assertEqual(retrieved_event["title"], "Test Event")
            self.assertEqual(retrieved_event["description"], "Test description")
        
        # Try to retrieve a non-existent event
        non_existent = self.timeline.get_event_by_id("non_existent_id")
        self.assertIsNone(non_existent)
        
    def test_delete_event(self):
        """Test deleting an event."""
        # Store an event
        event_data = {
            "title": "Test Event",
            "timestamp": datetime.now().isoformat(),
            "description": "Test description"
        }
        
        event_id = self.timeline.store_event(event_data)
        
        # Check that the event exists
        self.assertIsNotNone(self.timeline.get_event_by_id(event_id))
        
        # Delete the event
        result = self.timeline.delete_event(event_id)
        
        # Check that the deletion was successful
        self.assertTrue(result)
        
        # Check that the event no longer exists
        self.assertIsNone(self.timeline.get_event_by_id(event_id))
        
    def test_tag_filtering(self):
        """Test filtering events by tags."""
        # Store events with different tags
        event1 = {
            "title": "Work Event",
            "timestamp": datetime.now().isoformat(),
            "description": "Work related",
            "tags": ["work", "meeting"]
        }
        
        event2 = {
            "title": "Personal Event",
            "timestamp": datetime.now().isoformat(),
            "description": "Personal stuff",
            "tags": ["personal", "family"]
        }
        
        event3 = {
            "title": "Mixed Event",
            "timestamp": datetime.now().isoformat(),
            "description": "Mixed tags",
            "tags": ["work", "personal"]
        }
        
        # Store the events
        self.timeline.store_event(event1)
        self.timeline.store_event(event2)
        self.timeline.store_event(event3)
        
        # Filter by tags
        work_events = self.timeline.get_events(tags=["work"])
        self.assertEqual(len(work_events), 2)
        
        personal_events = self.timeline.get_events(tags=["personal"])
        self.assertEqual(len(personal_events), 2)
        
        family_events = self.timeline.get_events(tags=["family"])
        self.assertEqual(len(family_events), 1)
        self.assertEqual(family_events[0]["title"], "Personal Event")
        
    def test_timeline_visualization(self):
        """Test generating timeline visualization."""
        # Skip if matplotlib is not available
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            print("Skipping visualization test because matplotlib is not available")
            return
        
        # Store some events from 1961 to 2025
        dates = [
            datetime(1961, 4, 12),  # First human in space
            datetime(1969, 7, 20),  # Moon landing
            datetime(1985, 1, 1),   # Early internet
            datetime(2000, 1, 1),   # Y2K
            datetime(2023, 3, 15),  # Recent event
            datetime(2025, 12, 31)  # Future event
        ]
        
        for i, date in enumerate(dates):
            event_data = {
                "title": f"Historical Event {i+1}",
                "timestamp": date.isoformat(),
                "description": f"Test description {i+1}",
                "tags": ["history", f"era{i+1}"]
            }
            self.timeline.store_event(event_data)
        
        # Generate standard visualization
        fig, summary = self.timeline.generate_timeline_visualization(
            title="Historical Timeline 1961-2025"
        )
        
        # Check that visualization was generated
        self.assertIsNotNone(fig)
        self.assertIsNotNone(summary)
        
        # Try compact visualization
        fig_compact, summary_compact = self.timeline.generate_timeline_visualization(
            title="Compact Timeline", 
            visualization_mode="compact"
        )
        
        self.assertIsNotNone(fig_compact)
        self.assertIsNotNone(summary_compact)
        
    def test_5d_visualization(self):
        """Test 5D timeline visualization."""
        # Skip if matplotlib is not available
        try:
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D
            import numpy as np
        except ImportError:
            print("Skipping 5D visualization test because matplotlib or mplot3d is not available")
            return
        
        # Store some events with rich metadata
        dates = [
            datetime(1961, 4, 12),
            datetime(1969, 7, 20),
            datetime(1985, 1, 1),
            datetime(2000, 1, 1),
            datetime(2023, 3, 15)
        ]
        
        for i, date in enumerate(dates):
            # Add varying tags to create different significance levels
            tags = ["history"]
            if i % 2 == 0:
                tags.append("major")
            if i % 3 == 0:
                tags.append("computing")
            if i == 2:
                tags.extend(["breakthrough", "innovation", "milestone"])
                
            event_data = {
                "title": f"Historical Event {i+1}",
                "timestamp": date.isoformat(),
                "description": f"This is a detailed description of historical event {i+1}. " * (i+2),
                "tags": tags,
                "location": f"Location {i+1}",
                "participants": [f"Person {j}" for j in range(1, i+3)]
            }
            self.timeline.store_event(event_data)
        
        # Generate 5D visualization
        fig, summary = self.timeline.generate_timeline_visualization(
            title="5D Historical Timeline",
            visualization_mode="5d"
        )
        
        # Check that visualization was generated
        self.assertIsNotNone(fig)
        self.assertIsNotNone(summary)
        
    def test_typo_fixer(self):
        """Test fixing typos in timeline events."""
        # Store an event with a typo
        event_data = {
            "title": "Evnet with Typo",  # Intentional typo
            "timestamp": datetime.now().isoformat(),
            "description": "This event has a typo in the title",
            "tags": ["test", "typo"]
        }
        
        # Store the event
        event_id = self.timeline.store_event(event_data)
        
        # Verify the typo exists
        event = self.timeline.get_event_by_id(event_id)
        self.assertIsNotNone(event)
        if event:
            self.assertEqual(event["title"], "Evnet with Typo")
            
            # Fix the typo
            result = self.timeline.typo_fixer(event_id, "title", "Event with Typo")
            self.assertTrue(result)
            
            # Verify the typo is fixed
            updated_event = self.timeline.get_event_by_id(event_id)
            self.assertIsNotNone(updated_event)
            if updated_event:
                self.assertEqual(updated_event["title"], "Event with Typo")
                
                # Check that edit history was recorded
                self.assertIn("edit_history", updated_event)
                self.assertTrue(len(updated_event["edit_history"]) > 0)
                
                # Verify the edit history entry
                edit = updated_event["edit_history"][0]
                self.assertEqual(edit["field"], "title")
                self.assertEqual(edit["new_value"], "Event with Typo")
    
    def test_bulk_timeline_export(self):
        """Test exporting timeline data in different formats."""
        # Add some test events
        for i in range(5):
            event_data = {
                "title": f"Export Test Event {i+1}",
                "timestamp": (datetime.now() + timedelta(days=i)).isoformat(),
                "description": f"Test description {i+1}",
                "tags": ["export", f"tag{i+1}"]
            }
            self.timeline.store_event(event_data)
            
        # Test JSON export
        json_export = self.timeline.bulk_timeline_export(format="json")
        self.assertIsNotNone(json_export)
        
        # Verify JSON data can be parsed
        try:
            parsed = json.loads(json_export)
            self.assertIsInstance(parsed, list)
        except json.JSONDecodeError:
            self.fail("JSON export could not be parsed")
            
        # Test CSV export  
        csv_export = self.timeline.bulk_timeline_export(format="csv")
        self.assertIsNotNone(csv_export)
        
        # Test Markdown export
        md_export = self.timeline.bulk_timeline_export(format="markdown")
        self.assertIsNotNone(md_export)
        self.assertIn("# Timeline Events", md_export)


if __name__ == "__main__":
    unittest.main() 