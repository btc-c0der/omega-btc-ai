#!/usr/bin/env python3
"""
EventsManager module for IBR España component.
Handles church event management functionality.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import uuid
import random

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventsManager:
    """
    EventsManager is responsible for managing church events for the IBR España component.
    Provides functionality for adding, updating, deleting, and retrieving events.
    """

    def __init__(self, data_dir: str = "data/ibr_spain/events"):
        """
        Initialize the EventsManager with the path to store events data.
        
        Args:
            data_dir: Directory path where events data will be stored
        """
        self.data_dir = Path(data_dir)
        self.events_file = self.data_dir / "events.json"
        self.events = []
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Load existing events data
        self.load_events()

    def load_events(self) -> None:
        """Load events from the JSON file if it exists."""
        try:
            if self.events_file.exists():
                with open(self.events_file, 'r', encoding='utf-8') as f:
                    self.events = json.load(f)
                logger.info(f"Loaded {len(self.events)} events from {self.events_file}")
            else:
                logger.info(f"No events file found at {self.events_file}. Starting with empty events list.")
                self.events = []
        except Exception as e:
            logger.error(f"Error loading events: {str(e)}")
            self.events = []

    def save_events(self) -> None:
        """Save events to the JSON file."""
        try:
            with open(self.events_file, 'w', encoding='utf-8') as f:
                json.dump(self.events, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(self.events)} events to {self.events_file}")
        except Exception as e:
            logger.error(f"Error saving events: {str(e)}")

    def add_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new event to the collection.
        
        Args:
            event_data: Dictionary containing event information
            
        Returns:
            The newly added event with generated ID
        """
        # Generate a unique ID for the event
        event_id = self._generate_event_id()
        
        # Add required fields if missing
        event = {
            "id": event_id,
            "title": event_data.get("title", "Untitled Event"),
            "date": event_data.get("date", datetime.now().strftime("%Y-%m-%d")),
            "time": event_data.get("time", "00:00"),
            "end_time": event_data.get("end_time", ""),
            "location": event_data.get("location", ""),
            "description": event_data.get("description", ""),
            "type": event_data.get("type", "general"),
            "recurring": event_data.get("recurring", False),
            "recurrence_pattern": event_data.get("recurrence_pattern", ""),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add the event to the collection
        self.events.append(event)
        
        # Save changes to file
        self.save_events()
        
        return event

    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """
        Get an event by its ID.
        
        Args:
            event_id: The ID of the event to retrieve
            
        Returns:
            The event dictionary if found, None otherwise
        """
        for event in self.events:
            if event["id"] == event_id:
                return event
        return None

    def update_event(self, event_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing event.
        
        Args:
            event_id: ID of the event to update
            update_data: Dictionary with fields to update
            
        Returns:
            The updated event if found, None otherwise
        """
        for i, event in enumerate(self.events):
            if event["id"] == event_id:
                # Update fields
                for key, value in update_data.items():
                    if key != "id":  # Prevent overwriting the ID
                        event[key] = value
                
                # Add updated_at timestamp
                event["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Update in the collection
                self.events[i] = event
                
                # Save changes
                self.save_events()
                
                return event
        
        logger.warning(f"Event with ID {event_id} not found for update")
        return None

    def delete_event(self, event_id: str) -> bool:
        """
        Delete an event by its ID.
        
        Args:
            event_id: ID of the event to delete
            
        Returns:
            True if the event was deleted, False otherwise
        """
        for i, event in enumerate(self.events):
            if event["id"] == event_id:
                # Remove the event
                del self.events[i]
                
                # Save changes
                self.save_events()
                
                logger.info(f"Deleted event with ID {event_id}")
                return True
        
        logger.warning(f"Event with ID {event_id} not found for deletion")
        return False

    def get_all_events(self) -> List[Dict[str, Any]]:
        """
        Get all events.
        
        Returns:
            List of all event dictionaries
        """
        return self.events

    def get_upcoming_events(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get upcoming events for the next specified number of days.
        
        Args:
            days: Number of days to look ahead
            
        Returns:
            List of upcoming event dictionaries
        """
        upcoming = []
        today = datetime.now().date()
        end_date = today + timedelta(days=days)
        
        for event in self.events:
            try:
                event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
                
                # Check if event date is within range
                if today <= event_date <= end_date:
                    upcoming.append(event)
            except (ValueError, KeyError) as e:
                logger.warning(f"Error processing event date for event {event.get('id', 'unknown')}: {str(e)}")
        
        # Sort by date
        upcoming.sort(key=lambda x: x["date"])
        
        return upcoming

    def get_events_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        """
        Get events filtered by type.
        
        Args:
            event_type: Type of events to filter
            
        Returns:
            List of event dictionaries of the specified type
        """
        return [event for event in self.events if event.get("type") == event_type]

    def get_events_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Get events within a date range.
        
        Args:
            start_date: Start date in format 'YYYY-MM-DD'
            end_date: End date in format 'YYYY-MM-DD'
            
        Returns:
            List of event dictionaries within the date range
        """
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            
            filtered_events = []
            for event in self.events:
                try:
                    event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
                    if start <= event_date <= end:
                        filtered_events.append(event)
                except (ValueError, KeyError):
                    pass  # Skip events with invalid dates
            
            return filtered_events
        except ValueError as e:
            logger.error(f"Error parsing date range: {str(e)}")
            return []

    def _generate_event_id(self) -> str:
        """
        Generate a unique ID for a new event.
        
        Returns:
            A unique string ID
        """
        return f"event_{uuid.uuid4().hex[:8]}"
        
    def generate_sample_events(self, count: int = 5) -> None:
        """
        Generate sample events for testing purposes.
        
        Args:
            count: Number of sample events to generate
        """
        event_types = ["worship", "prayer", "bible_study", "conference", "community", "youth", "other"]
        locations = ["Main Hall", "Room 1", "Room 2", "Youth Room", "Garden", "Online"]
        
        today = datetime.now()
        
        for i in range(count):
            # Generate a random date within the next 60 days
            random_days = random.randint(0, 60)
            event_date = today + timedelta(days=random_days)
            
            # Create the event
            event_data = {
                "title": f"Sample Event {i+1}",
                "date": event_date.strftime("%Y-%m-%d"),
                "time": f"{random.randint(8, 20):02d}:00",
                "location": random.choice(locations),
                "description": f"This is a sample event generated for testing purposes. Event #{i+1}.",
                "type": random.choice(event_types),
                "recurring": random.random() > 0.7  # 30% chance of being recurring
            }
            
            # If recurring, add recurrence pattern
            if event_data["recurring"]:
                event_data["recurrence_pattern"] = random.choice(["weekly", "biweekly", "monthly"])
            
            # Add the event
            self.add_event(event_data)
        
        logger.info(f"Generated {count} sample events")


def render_event_card(event: Dict[str, Any]) -> str:
    """
    Render an event card HTML for display in the dashboard.
    
    Args:
        event: Event dictionary to render
        
    Returns:
        HTML string representing the event card
    """
    # Format the date for display
    try:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d")
        formatted_date = event_date.strftime("%B %d, %Y")
    except (ValueError, KeyError):
        formatted_date = event.get("date", "Unknown date")
    
    # Get event type CSS class
    event_type = event.get("type", "other")
    type_class = f"event-type-{event_type}"
    
    # Build the HTML
    html = f"""
    <div class="event-card {type_class}" id="event-{event['id']}">
        <div class="event-date">{formatted_date}</div>
        <div class="event-time">{event.get('time', '')}</div>
        <h3 class="event-title">{event.get('title', 'Untitled Event')}</h3>
        <div class="event-location">
            <i class="fas fa-map-marker-alt"></i> {event.get('location', '')}
        </div>
        <div class="event-description">{event.get('description', '')}</div>
        <div class="event-footer">
            <span class="event-type-badge">{event_type.upper()}</span>
            <div class="event-actions">
                <a href="/ibr-spain/events/{event['id']}" class="view-btn">View</a>
                <a href="/ibr-spain/events/{event['id']}/edit" class="edit-btn">Edit</a>
            </div>
        </div>
    </div>
    """
    
    return html


def render_events_calendar(events: List[Dict[str, Any]], view: str = "list") -> str:
    """
    Render events in a calendar view.
    
    Args:
        events: List of event dictionaries to render
        view: View type ('list', 'grid', or 'calendar')
        
    Returns:
        HTML string representing the events in the specified view
    """
    if view not in ["list", "grid", "calendar"]:
        view = "list"  # Default to list view
    
    if view == "list":
        html = '<div class="events-list">'
        for event in events:
            html += render_event_card(event)
        html += '</div>'
        
    elif view == "grid":
        html = '<div class="events-grid">'
        for event in events:
            html += render_event_card(event)
        html += '</div>'
        
    else:  # calendar view
        # This is a simplified calendar view
        html = '<div class="events-calendar">'
        html += '<div class="calendar-header">Calendar View (Simplified)</div>'
        
        # Group events by date
        events_by_date = {}
        for event in events:
            date = event.get("date", "Unknown")
            if date not in events_by_date:
                events_by_date[date] = []
            events_by_date[date].append(event)
        
        # Render events by date
        for date, date_events in sorted(events_by_date.items()):
            try:
                event_date = datetime.strptime(date, "%Y-%m-%d")
                formatted_date = event_date.strftime("%A, %B %d, %Y")
            except ValueError:
                formatted_date = date
                
            html += f'<div class="calendar-date">{formatted_date}</div>'
            html += '<div class="calendar-events">'
            for event in date_events:
                html += f"""
                <div class="calendar-event">
                    <span class="event-time">{event.get('time', '')}</span>
                    <span class="event-title">{event.get('title', 'Untitled Event')}</span>
                    <span class="event-location">{event.get('location', '')}</span>
                    <a href="/ibr-spain/events/{event['id']}" class="view-link">View</a>
                </div>
                """
            html += '</div>'
        
        html += '</div>'
    
    return html 