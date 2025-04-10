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
from typing import Dict, Any, List, Optional

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
    from micro_modules.redis_timeline import RedisTimeline
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
            return self.events
            
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

# Override Redis helper functions for testing
import micro_modules.redis_timeline as redis_timeline_module
redis_timeline_module.get_redis_client = mock_get_redis_client
redis_timeline_module.set_json = mock_set_json
redis_timeline_module.get_json = mock_get_json
redis_timeline_module.log_event = mock_log_event
redis_timeline_module.record_metric = mock_record_metric
redis_timeline_module.get_namespaced_key = mock_get_namespaced_key
redis_timeline_module.push_to_list = mock_push_to_list
redis_timeline_module.get_list = mock_get_list
redis_timeline_module.REDIS_AVAILABLE = True


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
        # Store some events
        for i in range(5):
            event_data = {
                "title": f"Test Event {i+1}",
                "timestamp": (datetime.now() + timedelta(days=i)).isoformat(),
                "description": f"Test description {i+1}"
            }
            self.timeline.store_event(event_data)
        
        # Generate visualization
        fig, summary = self.timeline.generate_timeline_visualization()
        
        # Check that visualization was generated
        self.assertIsNotNone(fig)
        self.assertIsNotNone(summary)
        self.assertTrue("Timeline contains" in summary)
        self.assertTrue("5 events" in summary)


if __name__ == "__main__":
    unittest.main() 