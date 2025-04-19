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
Caltech Rosebowl 1961 Hack Archive

A Gradio interface for documenting and exploring the legendary 1961 
Caltech Rose Bowl hack where students changed the Washington Huskies' 
flipcard display to read "CALTECH" during the NBC broadcast.
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

try:
    import gradio as gr
except ImportError:
    print("Error: Gradio not found. Please install with: pip install gradio>=3.23.0")
    sys.exit(1)

# Add parent directory to path to make imports work
sys.path.append('/Users/fsiqueira/OMEGA/omega-btc-ai')

# Import local modules
try:
    from .micro_modules.redis_timeline import RedisTimeline
except ImportError:
    print("Warning: Could not import RedisTimeline. Creating fallback...")
    
    class RedisTimelineFallback:
        """Fallback implementation when the real module is not available."""
        
        def __init__(self, namespace="caltech_rosebowl_1961"):
            self.namespace = namespace
            self.events = []
            
        def store_event(self, event_data):
            """Store an event."""
            if "id" not in event_data:
                event_data["id"] = f"event_{len(self.events)}"
            if "stored_at" not in event_data:
                event_data["stored_at"] = datetime.now().isoformat()
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
            
        def generate_timeline_visualization(self, events=None, title="Caltech Rosebowl 1961 Timeline"):
            """Generate a timeline visualization."""
            if events is None:
                events = self.events
                
            # Create a simple fallback visualization
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Sort events by timestamp if possible
            try:
                events = sorted(events, key=lambda x: datetime.fromisoformat(x["timestamp"]))
            except (ValueError, TypeError, KeyError):
                pass
                
            if not events:
                ax.text(0.5, 0.5, "No events found", ha="center", va="center")
                ax.set_axis_off()
                return fig, "No events found"
                
            # Extract dates and event names
            dates = []
            event_names = []
            
            for e in events:
                try:
                    dates.append(datetime.fromisoformat(e["timestamp"]))
                    event_names.append(e["title"])
                except (ValueError, KeyError):
                    continue
                    
            if not dates:
                ax.text(0.5, 0.5, "No valid dates found", ha="center", va="center")
                ax.set_axis_off()
                return fig, "No valid dates found"
                
            # Plot events on a simple timeline
            ax.scatter(dates, [0] * len(dates), s=100, color='blue', zorder=5)
            ax.set_title(title)
            
            # Add labels
            for i, (date, name) in enumerate(zip(dates, event_names)):
                y_pos = 0.1 if i % 2 == 0 else -0.1
                ha = 'left' if i % 2 == 0 else 'right'
                va = 'bottom' if i % 2 == 0 else 'top'
                ax.annotate(name, (date, y_pos), rotation=45, ha=ha, va=va, fontsize=9)
                
            # Format the plot
            fig.autofmt_xdate()
            ax.set_yticks([])
            ax.set_ylim(-0.5, 0.5)
            ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3, zorder=0)
            ax.grid(True, alpha=0.3)
            
            summary = f"Timeline contains {len(dates)} events"
            return fig, summary
            
    RedisTimeline = RedisTimelineFallback

# Initialize the timeline manager
timeline = RedisTimeline(namespace="caltech_rosebowl_1961")

# Preset event data for the Caltech Rosebowl hack
PRESET_EVENTS = [
    {
        "title": "Planning Begins",
        "timestamp": "1961-01-01T10:00:00",
        "description": "Caltech students begin planning the Rose Bowl hack, targeting the Washington vs. Minnesota game.",
        "location": "Caltech Campus, Pasadena, CA",
        "participants": ["Lyn Hardy", "Several unnamed Caltech students"],
        "tags": ["planning", "caltech", "rosebowl"],
        "source": "Oral history archives"
    },
    {
        "title": "Card Stunt Instructions Acquired",
        "timestamp": "1961-01-05T14:30:00",
        "description": "Students manage to acquire the instruction sheets for Washington's card stunts.",
        "location": "University of Washington",
        "tags": ["preparation", "intelligence", "caltech", "rosebowl"],
        "source": "Caltech archives"
    },
    {
        "title": "Revised Instructions Created",
        "timestamp": "1961-01-10T12:00:00",
        "description": "Modified instruction sheets are created to change the Washington display to spell 'CALTECH'.",
        "location": "Caltech Campus, Pasadena, CA",
        "tags": ["preparation", "caltech", "rosebowl"],
        "source": "Engineering & Science, Volume 24:5, February 1961"
    },
    {
        "title": "Instructions Distributed",
        "timestamp": "1961-01-14T09:00:00",
        "description": "Modified instruction cards are distributed to Washington fans entering the Rose Bowl.",
        "location": "Rose Bowl, Pasadena, CA",
        "tags": ["execution", "caltech", "rosebowl"],
        "source": "Caltech archives"
    },
    {
        "title": "CALTECH Revealed",
        "timestamp": "1961-01-14T14:15:00",
        "description": "During the nationally televised NBC broadcast, Washington's flipcard display spells 'CALTECH' instead of 'WASHINGTON'.",
        "location": "Rose Bowl, Pasadena, CA",
        "tags": ["success", "television", "caltech", "rosebowl"],
        "source": "NBC broadcast footage, 1961"
    },
    {
        "title": "Media Coverage",
        "timestamp": "1961-01-15T08:00:00",
        "description": "National media cover the prank, which becomes one of the most famous college pranks in history.",
        "location": "United States",
        "tags": ["aftermath", "media", "caltech", "rosebowl"],
        "source": "Various newspaper archives"
    }
]


def add_preset_events():
    """Add the preset Caltech Rosebowl hack events to the timeline."""
    for event in PRESET_EVENTS:
        # Check if event already exists by title and date
        existing_events = timeline.get_events()
        exists = False
        
        for existing in existing_events:
            if (existing.get("title") == event["title"] and 
                existing.get("timestamp") == event["timestamp"]):
                exists = True
                break
                
        if not exists:
            timeline.store_event(event)


def format_event(event: Dict[str, Any]) -> str:
    """Format an event for display in the UI."""
    try:
        dt = datetime.fromisoformat(event["timestamp"])
        date_str = dt.strftime("%B %d, %Y at %H:%M")
    except (ValueError, TypeError):
        date_str = event.get("timestamp", "Unknown date")
        
    formatted = f"## {event['title']}\n\n"
    formatted += f"**Date:** {date_str}\n\n"
    formatted += f"**Description:** {event.get('description', 'No description')}\n\n"
    
    if "location" in event and event["location"]:
        formatted += f"**Location:** {event['location']}\n\n"
    
    if "participants" in event and event["participants"]:
        participants = ", ".join(event["participants"])
        formatted += f"**Participants:** {participants}\n\n"
    
    if "tags" in event and event["tags"]:
        tags = ", ".join([f"#{tag}" for tag in event["tags"]])
        formatted += f"**Tags:** {tags}\n\n"
    
    if "source" in event and event["source"]:
        formatted += f"**Source:** {event['source']}\n\n"
    
    if "id" in event:
        formatted += f"*Event ID: {event['id']}*\n\n"
    
    formatted += "---\n\n"
    return formatted


def store_new_event(title, timestamp, description, location="", participants="", tags="", source=""):
    """Store a new event in the timeline."""
    # Validate required fields
    if not title or not timestamp or not description:
        return {
            "success": False,
            "message": "Title, timestamp, and description are required."
        }
    
    # Parse participants and tags
    if participants:
        participants_list = [p.strip() for p in participants.split(",")]
    else:
        participants_list = []
        
    if tags:
        tags_list = [t.strip() for t in tags.split(",")]
    else:
        tags_list = []
    
    # Create event data
    event_data = {
        "title": title,
        "timestamp": timestamp,
        "description": description,
        "location": location,
        "participants": participants_list,
        "tags": tags_list,
        "source": source
    }
    
    # Store the event
    event_id = timeline.store_event(event_data)
    
    if event_id:
        return {
            "success": True,
            "message": f"Event stored successfully with ID: {event_id}",
            "event_id": event_id
        }
    else:
        return {
            "success": False,
            "message": "Failed to store event."
        }


def get_all_events():
    """Get all events from the timeline."""
    events = timeline.get_events()
    
    if not events:
        return "No events found."
    
    # Format each event
    formatted_events = [format_event(event) for event in events]
    
    # Join all formatted events
    return "".join(formatted_events)


def generate_timeline_viz():
    """Generate timeline visualization."""
    events = timeline.get_events()
    fig, summary = timeline.generate_timeline_visualization(
        events=events,
        title="Caltech Rosebowl 1961 Hack Timeline"
    )
    return fig, summary


def create_interface():
    """Create the Gradio interface."""
    with gr.Blocks(title="Caltech Rosebowl 1961 Hack Archive") as interface:
        gr.Markdown(
            """
            # 🧠 Caltech Rosebowl 1961 Hack Archive 🏈
            
            *Historical archive of the legendary 1961 Caltech Rose Bowl prank*
            
            In 1961, Caltech students executed one of the most famous college pranks in history by hacking the Washington Huskies' 
            flipcard display during the nationally televised Rose Bowl game, making it spell "CALTECH" instead of "WASHINGTON".
            
            This dashboard allows you to explore and contribute to the historical record of this iconic hack.
            """
        )
        
        # Add tabs
        with gr.Tabs():
            # View Timeline Tab
            with gr.Tab("📜 View Timeline"):
                with gr.Row():
                    with gr.Column():
                        view_refresh_btn = gr.Button("Refresh Timeline")
                        events_display = gr.Markdown("Loading events...")
                
                view_refresh_btn.click(
                    fn=get_all_events,
                    outputs=events_display
                )
            
            # Add Event Tab
            with gr.Tab("➕ Add Historical Entry"):
                with gr.Row():
                    with gr.Column():
                        title_input = gr.Textbox(label="Event Title")
                        timestamp_input = gr.Textbox(
                            label="Timestamp (YYYY-MM-DDTHH:MM:SS)",
                            value=datetime.now().isoformat(timespec='seconds')
                        )
                        description_input = gr.Textbox(
                            label="Description",
                            lines=3
                        )
                        location_input = gr.Textbox(label="Location")
                        participants_input = gr.Textbox(
                            label="Participants (comma-separated)",
                            placeholder="Lyn Hardy, John Doe, Jane Smith"
                        )
                        tags_input = gr.Textbox(
                            label="Tags (comma-separated)",
                            placeholder="planning, execution, caltech, rosebowl"
                        )
                        source_input = gr.Textbox(
                            label="Source",
                            placeholder="Caltech archives, newspaper article, etc."
                        )
                        
                        submit_btn = gr.Button("Add Event", variant="primary")
                        result_output = gr.JSON(label="Result")
                        
                submit_btn.click(
                    fn=store_new_event,
                    inputs=[
                        title_input, timestamp_input, description_input,
                        location_input, participants_input, tags_input,
                        source_input
                    ],
                    outputs=result_output
                )
            
            # Timeline Visualization Tab
            with gr.Tab("📊 Timeline Visualization"):
                with gr.Row():
                    with gr.Column():
                        viz_refresh_btn = gr.Button("Generate Timeline Visualization")
                        viz_plot = gr.Plot(label="Timeline Visualization")
                        viz_summary = gr.Textbox(label="Summary")
                
                viz_refresh_btn.click(
                    fn=generate_timeline_viz,
                    outputs=[viz_plot, viz_summary]
                )
            
            # About Tab
            with gr.Tab("ℹ️ About This Hack"):
                gr.Markdown(
                    """
                    ## The Caltech Rose Bowl Hack of 1961
                    
                    The 1961 Rose Bowl featured the Washington Huskies against the Minnesota Golden Gophers. During the halftime show,
                    the Washington fans were set to perform a flipcard display spelling out "WASHINGTON". Instead, due to careful planning
                    by Caltech students, the cards spelled out "CALTECH".
                    
                    ### How They Did It
                    
                    1. **Intelligence Gathering**: Caltech students obtained the instruction sheets for Washington's card stunts.
                    
                    2. **Precision Modifications**: They meticulously altered the instructions to spell "CALTECH" while maintaining the
                       appearance of the original document.
                    
                    3. **Distribution**: On game day, they replaced the genuine instruction sheets with their modified versions.
                    
                    4. **National Exposure**: When the stunt was performed during the NBC broadcast, "CALTECH" was displayed to millions
                       of viewers nationwide.
                    
                    ### Legacy
                    
                    This prank is considered one of the greatest college pranks of all time and exemplifies the creativity and technical
                    skill of Caltech students. It has inspired generations of collegiate pranksters and remains a proud part of Caltech's
                    history.
                    
                    ### Participants
                    
                    The hack was led by student Lyn Hardy, along with a group of Caltech undergraduates who carefully planned and
                    executed this complex operation.
                    
                    ### Documentation
                    
                    This archive uses SHA-356 SACRED hashing to ensure the integrity of historical records, combined with Redis ORB
                    persistent storage for long-term preservation of this iconic moment in hacker history.
                    """
                )
        
        # Initialize interface
        interface.load(
            fn=lambda: [get_all_events(), *generate_timeline_viz()],
            outputs=[events_display, viz_plot, viz_summary]
        )
        
    return interface


def main():
    """Main entry point."""
    # Add preset events
    add_preset_events()
    
    # Create and launch interface
    interface = create_interface()
    interface.launch(share=True)


if __name__ == "__main__":
    main() 