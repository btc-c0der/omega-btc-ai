"""
Church Events for IBR España

This module provides church event management for the IBR España dashboard.
"""

class ChurchEvents:
    """Church Events for IBR España."""
    
    def __init__(self):
        """Initialize the church events manager."""
        self.events = [
            {
                "id": "event001",
                "title": "Servicio Dominical",
                "location": "REUS",
                "date": "2023-11-12",
                "time": "19:00",
                "description": "Servicio dominical con alabanza y predicación"
            },
            {
                "id": "event002",
                "title": "Estudio Bíblico",
                "location": "CUNIT",
                "date": "2023-11-15",
                "time": "20:00",
                "description": "Estudio bíblico semanal"
            }
        ]
    
    def get_upcoming_events(self, limit=5):
        """Get upcoming church events."""
        return self.events[:limit]
        
    def get_events_by_location(self, location):
        """Get events filtered by location."""
        return [e for e in self.events if e.get("location") == location] 