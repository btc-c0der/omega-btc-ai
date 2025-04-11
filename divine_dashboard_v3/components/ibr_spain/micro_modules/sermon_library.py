#!/usr/bin/env python3

"""
Sermon Library for IBR España

This module provides a sermon library for the IBR España dashboard.
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Union, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sermon_library")

class SermonLibrary:
    """Sermon Library for IBR España."""
    
    def __init__(self):
        """Initialize the sermon library."""
        self.sermons = [
            {
                "id": "sermon001",
                "title": "El amor de Dios",
                "speaker": "Pastor Thiago Rodriguez",
                "date": "2023-11-12",
                "duration": 45,
                "description": "Un mensaje sobre el amor incondicional de Dios",
                "audio_url": "/sermons/sermon001.mp3"
            },
            {
                "id": "sermon002",
                "title": "La fe en tiempos difíciles",
                "speaker": "Pastor Thiago Rodriguez",
                "date": "2023-11-05",
                "duration": 38,
                "description": "Cómo mantener nuestra fe durante los tiempos difíciles",
                "audio_url": "/sermons/sermon002.mp3"
            }
        ]
        
    def get_recent_sermons(self, limit=5):
        """Get the most recent sermons."""
        return self.sermons[:limit]


def render_sermon_card(sermon: Dict[str, Any]) -> str:
    """
    Render a sermon card in HTML
    
    Args:
        sermon: Sermon data dictionary
        
    Returns:
        str: HTML representation of the sermon card
    """
    # Format date
    date_formatted = sermon.get("date", "")
    try:
        date_obj = datetime.strptime(date_formatted, "%Y-%m-%d")
        date_formatted = date_obj.strftime("%d %b %Y")
    except:
        pass
    
    # Set language badge
    language_code = sermon.get("language", "es")
    language_name = {"es": "Español", "ca": "Català", "en": "English"}.get(language_code, "")
    
    # Create HTML card
    html = f"""
    <div class="sermon-card">
        <div class="sermon-language-badge">{language_name}</div>
        <h3>{sermon.get('title', 'Untitled Sermon')}</h3>
        <div class="sermon-preacher">{sermon.get('preacher', '')}</div>
        <div class="sermon-date-duration">
            <span class="sermon-date">{date_formatted}</span>
            <span class="sermon-duration">{sermon.get('duration', '')}</span>
        </div>
        <div class="sermon-scripture">
            <strong>Scripture:</strong> {sermon.get('scripture', '')}
        </div>
        <div class="sermon-audio">
            <audio controls>
                <source src="{sermon.get('audio_url', '')}" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
        </div>
    </div>
    """
    
    return html


# For testing purposes
if __name__ == "__main__":
    # Create a test sermon library
    library = SermonLibrary()
    
    # Test search functionality
    results = library.search_sermons(query="soberanía")
    print(f"Found {len(results)} sermons matching 'soberanía'")
    
    # Test rendering
    for sermon in results:
        print(render_sermon_card(sermon)) 