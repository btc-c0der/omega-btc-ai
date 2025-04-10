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
Redis Timeline Module

Provides functionality for storing and retrieving historical hack event timelines
using Redis as a backing store. Optimized for storing chronological events with
timestamps, metadata, and optional media attachments.
"""

import json
import time
import logging
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime
import sys
import uuid

# Configure logging
logger = logging.getLogger(__name__)

# Define fallback functions for when Redis is not available
def fallback_store_event(namespace, event_data):
    """Fallback function for storing event when Redis is not available."""
    logger.warning(f"Redis not available, can't store event in {namespace}")
    return False

def fallback_get_events(namespace, start_time=None, end_time=None):
    """Fallback function for retrieving events when Redis is not available."""
    logger.warning(f"Redis not available, can't retrieve events from {namespace}")
    return []

def fallback_get_event_by_id(namespace, event_id):
    """Fallback function for retrieving an event by ID when Redis is not available."""
    logger.warning(f"Redis not available, can't retrieve event {event_id} from {namespace}")
    return None

def fallback_generate_timeline_viz(events):
    """Fallback function for generating timeline visualization."""
    logger.warning("Redis not available, can't generate timeline visualization")
    return None

# Try to import Redis helper
try:
    sys.path.append('/Users/fsiqueira/OMEGA/omega-btc-ai')
    from divine_dashboard_v3.utils.redis_helper import (
        get_redis_client, set_json, get_json, log_event, 
        record_metric, get_namespaced_key, push_to_list, 
        increment, get_list
    )
    REDIS_AVAILABLE = True
except ImportError:
    logger.warning("Redis helper not found, timeline events will be stored locally")
    REDIS_AVAILABLE = False
    # Set fallback functions
    store_event = fallback_store_event
    get_events = fallback_get_events
    get_event_by_id = fallback_get_event_by_id
    generate_timeline_viz = fallback_generate_timeline_viz

class RedisTimeline:
    """Handles Redis-based storage and retrieval of historical hack event timelines."""
    
    def __init__(self, namespace: str = "hack_history"):
        """
        Initialize the Redis timeline manager.
        
        Args:
            namespace: Redis namespace for keys (default: hack_history)
        """
        self.namespace = namespace
        self.use_redis = REDIS_AVAILABLE
        self.redis_client = None
        
        # Local storage fallback
        self.local_events: List[Dict[str, Any]] = []
        
        # Initialize Redis connection if available
        if self.use_redis:
            try:
                self.redis_client = get_redis_client()
                logger.info(f"Redis connection successful for timeline: {namespace}")
                
                # Test Redis connection with a ping
                if self.redis_client is not None:
                    self.redis_client.ping()
                else:
                    raise Exception("Redis client is None")
            except Exception as e:
                logger.error(f"Redis connection error: {e}")
                self.use_redis = False
    
    def store_event(self, event_data: Dict[str, Any]) -> str:
        """
        Store a historical hack event in the timeline.
        
        Args:
            event_data: Event data dictionary containing at minimum:
                - title: Event title
                - timestamp: Event timestamp (ISO format or Unix timestamp)
                - description: Event description
                Optional fields:
                - location: Where the event occurred
                - participants: List of participants
                - media_urls: List of media URLs
                - tags: List of tags
                - source: Source of the information
                
        Returns:
            Event ID if successful, empty string otherwise
        """
        # Validate required fields
        required_fields = ["title", "timestamp", "description"]
        for field in required_fields:
            if field not in event_data:
                logger.error(f"Missing required field: {field}")
                return ""
        
        # Generate event ID if not provided
        if "id" not in event_data:
            event_id = str(uuid.uuid4())
            event_data["id"] = event_id
        else:
            event_id = event_data["id"]
        
        # Add storage timestamp if not present
        if "stored_at" not in event_data:
            event_data["stored_at"] = datetime.now().isoformat()
        
        # Normalize timestamp format
        if isinstance(event_data["timestamp"], (int, float)):
            # Convert Unix timestamp to ISO format
            event_data["timestamp"] = datetime.fromtimestamp(event_data["timestamp"]).isoformat()
            
        # Store the event
        if self.use_redis:
            try:
                # Store event data as JSON
                event_key = get_namespaced_key(self.namespace, f"event:{event_id}")
                set_json(event_key, event_data)
                
                # Add to chronological index
                timeline_key = get_namespaced_key(self.namespace, "timeline")
                push_to_list(timeline_key, event_id)
                
                # Add to year-based index for faster retrieval
                if "timestamp" in event_data:
                    try:
                        dt = datetime.fromisoformat(event_data["timestamp"])
                        year_key = get_namespaced_key(self.namespace, f"year:{dt.year}")
                        push_to_list(year_key, event_id)
                    except (ValueError, TypeError):
                        logger.warning(f"Invalid timestamp format: {event_data['timestamp']}")
                
                # Log the storage
                log_event("timeline_event_stored", {
                    "namespace": self.namespace,
                    "event_id": event_id,
                    "title": event_data["title"]
                })
                
                return event_id
            
            except Exception as e:
                logger.error(f"Redis error storing event: {e}")
                # Fall back to local storage
                self.local_events.append(event_data)
                return event_id
        else:
            # Store locally
            self.local_events.append(event_data)
            return event_id
    
    def get_events(self, 
                  start_time: Optional[str] = None, 
                  end_time: Optional[str] = None,
                  tags: Optional[List[str]] = None,
                  limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve historical hack events from the timeline.
        
        Args:
            start_time: Start time in ISO format (optional)
            end_time: End time in ISO format (optional)
            tags: Filter by tags (optional)
            limit: Maximum number of events to return (default: 100)
            
        Returns:
            List of event data dictionaries
        """
        # If Redis isn't available, return local events
        if not self.use_redis:
            filtered_events = self.local_events
            
            # Apply time filtering
            if start_time:
                try:
                    start_dt = datetime.fromisoformat(start_time)
                    filtered_events = [e for e in filtered_events 
                                    if datetime.fromisoformat(e["timestamp"]) >= start_dt]
                except (ValueError, TypeError):
                    logger.warning(f"Invalid start_time format: {start_time}")
            
            if end_time:
                try:
                    end_dt = datetime.fromisoformat(end_time)
                    filtered_events = [e for e in filtered_events 
                                    if datetime.fromisoformat(e["timestamp"]) <= end_dt]
                except (ValueError, TypeError):
                    logger.warning(f"Invalid end_time format: {end_time}")
            
            # Apply tag filtering
            if tags:
                filtered_events = [e for e in filtered_events 
                                if "tags" in e and any(tag in e["tags"] for tag in tags)]
            
            # Apply limit
            return filtered_events[:limit]
        
        # Redis is available
        try:
            # Get timeline list
            timeline_key = get_namespaced_key(self.namespace, "timeline")
            event_ids = get_list(timeline_key, 0, -1)
            
            events = []
            for event_id in event_ids:
                # Get event data
                event_key = get_namespaced_key(self.namespace, f"event:{event_id}")
                event_data = get_json(event_key)
                
                if not event_data:
                    continue
                
                # Apply time filtering
                if start_time:
                    try:
                        if datetime.fromisoformat(event_data["timestamp"]) < datetime.fromisoformat(start_time):
                            continue
                    except (ValueError, TypeError):
                        logger.warning(f"Invalid timestamp comparison: {event_data['timestamp']} vs {start_time}")
                
                if end_time:
                    try:
                        if datetime.fromisoformat(event_data["timestamp"]) > datetime.fromisoformat(end_time):
                            continue
                    except (ValueError, TypeError):
                        logger.warning(f"Invalid timestamp comparison: {event_data['timestamp']} vs {end_time}")
                
                # Apply tag filtering
                if tags:
                    if "tags" not in event_data or not any(tag in event_data["tags"] for tag in tags):
                        continue
                
                events.append(event_data)
                
                # Check limit
                if len(events) >= limit:
                    break
            
            return events
        
        except Exception as e:
            logger.error(f"Redis error retrieving events: {e}")
            return self.local_events[:limit]
    
    def get_event_by_id(self, event_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific event by ID.
        
        Args:
            event_id: Event ID
            
        Returns:
            Event data dictionary or None if not found
        """
        # If Redis isn't available, search in local events
        if not self.use_redis:
            for event in self.local_events:
                if event.get("id") == event_id:
                    return event
            return None
        
        # Redis is available
        try:
            event_key = get_namespaced_key(self.namespace, f"event:{event_id}")
            return get_json(event_key)
        except Exception as e:
            logger.error(f"Redis error retrieving event {event_id}: {e}")
            
            # Fall back to local search
            for event in self.local_events:
                if event.get("id") == event_id:
                    return event
            
            return None
    
    def delete_event(self, event_id: str) -> bool:
        """
        Delete an event from the timeline.
        
        Args:
            event_id: Event ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        # If Redis isn't available, remove from local events
        if not self.use_redis:
            initial_count = len(self.local_events)
            self.local_events = [e for e in self.local_events if e.get("id") != event_id]
            return len(self.local_events) < initial_count
        
        # Redis is available
        try:
            # Remove from timeline list
            timeline_key = get_namespaced_key(self.namespace, "timeline")
            try:
                self.redis_client.lrem(timeline_key, 0, event_id)
            except Exception as e:
                logger.warning(f"Error removing event ID from timeline list: {e}")
            
            # Delete the event data
            event_key = get_namespaced_key(self.namespace, f"event:{event_id}")
            return self.redis_client.delete(event_key) > 0
        
        except Exception as e:
            logger.error(f"Redis error deleting event {event_id}: {e}")
            return False
    
    def generate_timeline_visualization(self, 
                                      events: Optional[List[Dict[str, Any]]] = None,
                                      title: str = "Historical Hack Timeline") -> Tuple[Any, str]:
        """
        Generate a timeline visualization using matplotlib.
        
        Args:
            events: List of events (if None, all events will be retrieved)
            title: Title for the visualization
            
        Returns:
            Tuple of (matplotlib figure, events summary)
        """
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from matplotlib.figure import Figure
        import io
        import base64
        
        # Get events if not provided
        if events is None:
            events = self.get_events(limit=50)
        
        if not events:
            fig, ax = plt.subplots(figsize=(10, 2))
            ax.text(0.5, 0.5, "No events found", ha="center", va="center")
            ax.set_axis_off()
            return fig, "No events found"
        
        # Sort events by timestamp
        try:
            events = sorted(events, key=lambda x: datetime.fromisoformat(x["timestamp"]))
        except (ValueError, TypeError) as e:
            logger.warning(f"Error sorting events by timestamp: {e}")
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Extract dates and event names
        dates = [datetime.fromisoformat(e["timestamp"]) for e in events]
        event_names = [e["title"] for e in events]
        
        # Create y positions (all at y=0)
        y_positions = [0] * len(dates)
        
        # Plot the timeline
        ax.scatter(dates, y_positions, s=100, color='blue', zorder=5)
        
        # Add event labels
        for i, (date, name) in enumerate(zip(dates, event_names)):
            # Alternate label positions above and below the timeline
            if i % 2 == 0:
                ax.annotate(name, (date, 0.1), rotation=45, 
                         ha='left', va='bottom', fontsize=9)
            else:
                ax.annotate(name, (date, -0.1), rotation=45, 
                         ha='right', va='top', fontsize=9)
        
        # Format the x-axis to show dates nicely
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        fig.autofmt_xdate()
        
        # Remove y-axis ticks and labels
        ax.set_yticks([])
        ax.set_ylim(-0.5, 0.5)
        
        # Add a horizontal line for the timeline
        ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3, zorder=0)
        
        # Add title and grid
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        # Create a summary of the events
        summary = f"Timeline contains {len(events)} events from "
        if dates:
            summary += f"{dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')}"
        
        return fig, summary 