#!/usr/bin/env python3

"""
IBR España - Sermon Library Micro Module

This module provides sermon management functionality for the IBR España dashboard.
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
    """Sermon library manager for IBR España"""
    
    def __init__(self, data_dir: Optional[str] = None):
        """Initialize the sermon library
        
        Args:
            data_dir: Directory to store sermon data (optional)
        """
        self.data_dir = Path(data_dir) if data_dir else Path.home() / "ibr_data" / "sermons"
        
        # Create data directory if it doesn't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize sermon database
        self.sermons_file = self.data_dir / "sermons.json"
        self.sermons = self.load_sermons()
        
        logger.info(f"Sermon library initialized with {len(self.sermons)} sermons")
    
    def load_sermons(self) -> List[Dict[str, Any]]:
        """Load sermons from storage"""
        if not self.sermons_file.exists():
            # Return sample data if no file exists yet
            return self._get_sample_sermons()
            
        try:
            with open(self.sermons_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading sermons: {e}")
            return self._get_sample_sermons()
    
    def save_sermons(self) -> bool:
        """Save sermons to storage
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.sermons_file, "w", encoding="utf-8") as f:
                json.dump(self.sermons, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving sermons: {e}")
            return False
    
    def add_sermon(self, sermon: Dict[str, Any]) -> bool:
        """Add a new sermon to the library
        
        Args:
            sermon: Sermon data dictionary
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Validate sermon data
        required_fields = ["title", "preacher", "date", "scripture", "language"]
        for field in required_fields:
            if field not in sermon:
                logger.error(f"Missing required field in sermon: {field}")
                return False
        
        # Generate ID if not provided
        if "id" not in sermon:
            sermon["id"] = f"sermon_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Add sermon to library
        self.sermons.append(sermon)
        return self.save_sermons()
    
    def get_sermon(self, sermon_id: str) -> Optional[Dict[str, Any]]:
        """Get a sermon by ID
        
        Args:
            sermon_id: ID of sermon to retrieve
            
        Returns:
            Dict or None: Sermon data if found, None otherwise
        """
        for sermon in self.sermons:
            if sermon.get("id") == sermon_id:
                return sermon
        return None
    
    def update_sermon(self, sermon_id: str, updated_data: Dict[str, Any]) -> bool:
        """Update a sermon's data
        
        Args:
            sermon_id: ID of sermon to update
            updated_data: New sermon data (partial updates supported)
            
        Returns:
            bool: True if successful, False otherwise
        """
        for i, sermon in enumerate(self.sermons):
            if sermon.get("id") == sermon_id:
                # Update only the provided fields
                self.sermons[i] = {**sermon, **updated_data}
                return self.save_sermons()
        
        logger.error(f"Sermon not found for update: {sermon_id}")
        return False
    
    def delete_sermon(self, sermon_id: str) -> bool:
        """Delete a sermon from the library
        
        Args:
            sermon_id: ID of sermon to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        for i, sermon in enumerate(self.sermons):
            if sermon.get("id") == sermon_id:
                del self.sermons[i]
                return self.save_sermons()
        
        logger.error(f"Sermon not found for deletion: {sermon_id}")
        return False
    
    def search_sermons(self, query: str = "", language: str = None) -> List[Dict[str, Any]]:
        """Search sermons by query and/or language
        
        Args:
            query: Search query (searches title, preacher, and scripture)
            language: Language filter (e.g., 'es', 'en')
            
        Returns:
            List: Matching sermons
        """
        results = self.sermons.copy()
        
        # Filter by language
        if language:
            results = [s for s in results if s.get("language") == language]
        
        # Filter by query
        if query:
            query = query.lower()
            results = [
                s for s in results if (
                    query in s.get("title", "").lower() or
                    query in s.get("preacher", "").lower() or
                    query in s.get("scripture", "").lower()
                )
            ]
        
        return results
    
    def _get_sample_sermons(self) -> List[Dict[str, Any]]:
        """Get sample sermon data"""
        return [
            {
                "id": "sermon001",
                "title": "La Gracia de Dios en Tiempos Difíciles",
                "preacher": "Pastor Juan Martínez",
                "date": "2023-10-22",
                "duration": "45:30",
                "scripture": "Romanos 8:18-39",
                "language": "es",
                "audio_url": "https://ibr-espana.org/sermons/sermon001.mp3",
                "thumbnail": "https://ibr-espana.org/thumbnails/sermon001.jpg"
            },
            {
                "id": "sermon002",
                "title": "La Soberanía de Dios",
                "preacher": "Pastor Miguel Rodríguez",
                "date": "2023-10-15",
                "duration": "38:22",
                "scripture": "Job 38:1-41",
                "language": "es",
                "audio_url": "https://ibr-espana.org/sermons/sermon002.mp3",
                "thumbnail": "https://ibr-espana.org/thumbnails/sermon002.jpg"
            },
            {
                "id": "sermon003",
                "title": "God's Sovereignty in Our Lives",
                "preacher": "Pastor David Wilson",
                "date": "2023-10-08",
                "duration": "41:05",
                "scripture": "Psalm 139:1-24",
                "language": "en",
                "audio_url": "https://ibr-espana.org/sermons/sermon003.mp3",
                "thumbnail": "https://ibr-espana.org/thumbnails/sermon003.jpg"
            }
        ]


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