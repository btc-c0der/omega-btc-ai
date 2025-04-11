#!/usr/bin/env python3
"""
Test suite for IBR Spain Routes

This module tests the Flask routes for the IBR Spain component,
including the event management functionality.
"""

import os
import json
import pytest
import tempfile
import sys
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from pathlib import Path

from flask import Flask, url_for

# Add the parent directory to the Python path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

# Now we can import our modules
from routes.ibr_spain_routes import ibr_spain_bp, events_manager
from components.ibr_spain.micro_modules.events_manager import EventsManager

# Test data
SAMPLE_EVENT = {
    "title": "Test Event",
    "date": datetime.now().strftime("%Y-%m-%d"),
    "time": "19:00",
    "location": "Test Location",
    "description": "Test Description",
    "type": "worship",
    "recurring": False
}

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-key'
    app.config['SERVER_NAME'] = 'test.local'
    
    # Register the blueprint
    app.register_blueprint(ibr_spain_bp)
    
    # Create a temporary directory for test data
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test events manager with the temporary directory
        test_events_manager = EventsManager(data_dir=temp_dir)
        
        # Replace the events manager in the routes with our test instance
        events_manager = test_events_manager
        
        # Add app context
        with app.app_context():
            yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def mock_events_manager():
    """Create a mocked events manager for unit tests."""
    with patch('routes.ibr_spain_routes.events_manager') as mock_manager:
        mock_manager.get_upcoming_events.return_value = [
            {
                "id": "event001",
                "title": "Test Event 1",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": "19:00",
                "location": "Test Location 1",
                "description": "Test Description 1",
                "type": "worship",
                "recurring": False
            },
            {
                "id": "event002",
                "title": "Test Event 2",
                "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                "time": "20:00",
                "location": "Test Location 2",
                "description": "Test Description 2",
                "type": "prayer",
                "recurring": True,
                "recurrence_pattern": "weekly"
            }
        ]
        yield mock_manager

# Unit Tests

def test_index_route(client, mock_events_manager):
    """Test the index route."""
    response = client.get('/ibr-spain/')
    assert response.status_code == 200
    mock_events_manager.get_upcoming_events.assert_called_once()

def test_events_page_route(client, mock_events_manager):
    """Test the events page route."""
    # Mock the get_all_events method
    mock_events_manager.get_all_events.return_value = mock_events_manager.get_upcoming_events.return_value
    
    response = client.get('/ibr-spain/events')
    assert response.status_code == 200
    mock_events_manager.get_all_events.assert_called_once()

def test_events_page_with_filters(client, mock_events_manager):
    """Test the events page route with filters."""
    # Mock the filtered methods
    mock_events_manager.get_events_by_type.return_value = [mock_events_manager.get_upcoming_events.return_value[0]]
    mock_events_manager.get_events_by_date_range.return_value = mock_events_manager.get_upcoming_events.return_value
    
    # Test type filter
    response = client.get('/ibr-spain/events?type=worship')
    assert response.status_code == 200
    mock_events_manager.get_events_by_type.assert_called_with('worship')
    
    # Test date range filter
    today = datetime.now().strftime("%Y-%m-%d")
    next_week = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    response = client.get(f'/ibr-spain/events?start_date={today}&end_date={next_week}')
    assert response.status_code == 200
    mock_events_manager.get_events_by_date_range.assert_called_with(today, next_week)

def test_create_event_get(client):
    """Test the create event page (GET)."""
    response = client.get('/ibr-spain/events/create')
    assert response.status_code == 200

def test_create_event_post(client, mock_events_manager):
    """Test creating an event (POST)."""
    # Mock the add_event method
    mock_events_manager.add_event.return_value = {
        "id": "new_event_id",
        **SAMPLE_EVENT,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    response = client.post('/ibr-spain/events/create', data=SAMPLE_EVENT, follow_redirects=True)
    assert response.status_code == 200
    mock_events_manager.add_event.assert_called_once()

def test_view_event(client, mock_events_manager):
    """Test viewing a single event."""
    event_id = "event001"
    
    # Mock the get_event method
    mock_events_manager.get_event.return_value = {
        "id": event_id,
        **SAMPLE_EVENT
    }
    
    response = client.get(f'/ibr-spain/events/{event_id}')
    assert response.status_code == 200
    mock_events_manager.get_event.assert_called_with(event_id)

def test_view_nonexistent_event(client, mock_events_manager):
    """Test viewing a non-existent event."""
    event_id = "nonexistent"
    
    # Mock the get_event method to return None
    mock_events_manager.get_event.return_value = None
    
    response = client.get(f'/ibr-spain/events/{event_id}', follow_redirects=True)
    assert response.status_code == 200  # Redirected to events page
    mock_events_manager.get_event.assert_called_with(event_id)

def test_edit_event_get(client, mock_events_manager):
    """Test the edit event page (GET)."""
    event_id = "event001"
    
    # Mock the get_event method
    mock_events_manager.get_event.return_value = {
        "id": event_id,
        **SAMPLE_EVENT
    }
    
    response = client.get(f'/ibr-spain/events/{event_id}/edit')
    assert response.status_code == 200
    mock_events_manager.get_event.assert_called_with(event_id)

def test_edit_event_post(client, mock_events_manager):
    """Test editing an event (POST)."""
    event_id = "event001"
    
    # Mock the get_event and update_event methods
    mock_events_manager.get_event.return_value = {
        "id": event_id,
        **SAMPLE_EVENT
    }
    
    updated_event = {
        "id": event_id,
        **SAMPLE_EVENT,
        "title": "Updated Title",
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    mock_events_manager.update_event.return_value = updated_event
    
    data = {**SAMPLE_EVENT, "title": "Updated Title"}
    response = client.post(f'/ibr-spain/events/{event_id}/edit', data=data, follow_redirects=True)
    assert response.status_code == 200
    mock_events_manager.update_event.assert_called_once()

def test_delete_event(client, mock_events_manager):
    """Test deleting an event."""
    event_id = "event001"
    
    # Mock the delete_event method
    mock_events_manager.delete_event.return_value = True
    
    response = client.post(f'/ibr-spain/events/{event_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    mock_events_manager.delete_event.assert_called_with(event_id)

# API Tests

def test_api_get_events(client, mock_events_manager):
    """Test the API endpoint to get events."""
    # Mock the methods
    mock_events_manager.get_upcoming_events.return_value = [
        {"id": "event001", "title": "Test Event 1"}, 
        {"id": "event002", "title": "Test Event 2"}
    ]
    
    response = client.get('/ibr-spain/api/events')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]["id"] == "event001"
    mock_events_manager.get_upcoming_events.assert_called_once()
    
    # Test with type filter
    mock_events_manager.get_events_by_type.return_value = [{"id": "event001", "title": "Test Event 1"}]
    response = client.get('/ibr-spain/api/events?type=worship')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    mock_events_manager.get_events_by_type.assert_called_with("worship")

def test_api_get_event(client, mock_events_manager):
    """Test the API endpoint to get a single event."""
    event_id = "event001"
    
    # Mock the get_event method
    mock_events_manager.get_event.return_value = {
        "id": event_id,
        "title": "Test Event 1"
    }
    
    response = client.get(f'/ibr-spain/api/events/{event_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == event_id
    mock_events_manager.get_event.assert_called_with(event_id)
    
    # Test with non-existent event
    mock_events_manager.get_event.return_value = None
    response = client.get('/ibr-spain/api/events/nonexistent')
    assert response.status_code == 404

def test_api_create_event(client, mock_events_manager):
    """Test the API endpoint to create an event."""
    # Mock the add_event method
    new_event = {
        "id": "new_event_id",
        **SAMPLE_EVENT,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    mock_events_manager.add_event.return_value = new_event
    
    response = client.post(
        '/ibr-spain/api/events',
        data=json.dumps(SAMPLE_EVENT),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["id"] == "new_event_id"
    mock_events_manager.add_event.assert_called_once()

def test_api_update_event(client, mock_events_manager):
    """Test the API endpoint to update an event."""
    event_id = "event001"
    
    # Mock the update_event method
    updated_event = {
        "id": event_id,
        **SAMPLE_EVENT,
        "title": "Updated Title",
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    mock_events_manager.update_event.return_value = updated_event
    
    update_data = {"title": "Updated Title"}
    response = client.put(
        f'/ibr-spain/api/events/{event_id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["title"] == "Updated Title"
    mock_events_manager.update_event.assert_called_once()
    
    # Test with non-existent event
    mock_events_manager.update_event.return_value = None
    response = client.put(
        '/ibr-spain/api/events/nonexistent',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert response.status_code == 404

def test_api_delete_event(client, mock_events_manager):
    """Test the API endpoint to delete an event."""
    event_id = "event001"
    
    # Mock the delete_event method
    mock_events_manager.delete_event.return_value = True
    
    response = client.delete(f'/ibr-spain/api/events/{event_id}')
    assert response.status_code == 200
    mock_events_manager.delete_event.assert_called_with(event_id)
    
    # Test with non-existent event
    mock_events_manager.delete_event.return_value = False
    response = client.delete('/ibr-spain/api/events/nonexistent')
    assert response.status_code == 404

def test_generate_sample_events(client, mock_events_manager):
    """Test generating sample events."""
    # Mock the generate_sample_events method
    mock_events_manager.generate_sample_events.return_value = None
    
    response = client.post('/ibr-spain/generate-sample-events', data={"count": 5}, follow_redirects=True)
    assert response.status_code == 200
    mock_events_manager.generate_sample_events.assert_called_with(5)

# Integration Tests

class TestIntegration:
    """Integration tests that use a real EventsManager instance."""
    
    @pytest.fixture
    def integration_client(self):
        """A test client for integration tests with a real EventsManager."""
        app = Flask(__name__, 
                    template_folder='templates',
                    static_folder='static')
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-key'
        
        # Create a temporary directory for test data
        temp_dir = tempfile.mkdtemp()
        
        # Create a real events manager with the temporary directory
        real_events_manager = EventsManager(data_dir=temp_dir)
        
        # Replace the blueprint's events_manager with our real instance
        # This is a bit of a hack but needed for integration testing
        import routes.ibr_spain_routes
        routes.ibr_spain_routes.events_manager = real_events_manager
        
        # Register the blueprint
        app.register_blueprint(ibr_spain_bp)
        
        # Add app context
        with app.app_context():
            client = app.test_client()
            yield client
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_event_lifecycle(self, integration_client):
        """Test the complete lifecycle of an event: create, view, edit, delete."""
        # Create an event
        response = integration_client.post(
            '/ibr-spain/events/create',
            data=SAMPLE_EVENT,
            follow_redirects=True
        )
        assert response.status_code == 200
        
        # Get the ID from the response
        # Note: In a real test, you'd parse the HTML to get this
        # For this example, we'll get all events and use the first one
        response = integration_client.get('/ibr-spain/api/events')
        assert response.status_code == 200
        events = json.loads(response.data)
        assert len(events) > 0
        event_id = events[0]["id"]
        
        # View the event
        response = integration_client.get(f'/ibr-spain/events/{event_id}')
        assert response.status_code == 200
        
        # Edit the event
        edit_data = {**SAMPLE_EVENT, "title": "Updated Integration Test Event"}
        response = integration_client.post(
            f'/ibr-spain/events/{event_id}/edit',
            data=edit_data,
            follow_redirects=True
        )
        assert response.status_code == 200
        
        # Verify the edit worked
        response = integration_client.get(f'/ibr-spain/api/events/{event_id}')
        assert response.status_code == 200
        updated_event = json.loads(response.data)
        assert updated_event["title"] == "Updated Integration Test Event"
        
        # Delete the event
        response = integration_client.post(
            f'/ibr-spain/events/{event_id}/delete',
            follow_redirects=True
        )
        assert response.status_code == 200
        
        # Verify the delete worked
        response = integration_client.get(f'/ibr-spain/api/events/{event_id}')
        assert response.status_code == 404

if __name__ == "__main__":
    pytest.main(["-xvs"]) 