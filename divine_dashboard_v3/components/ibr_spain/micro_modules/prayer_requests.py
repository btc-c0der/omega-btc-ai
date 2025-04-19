"""
Prayer Requests for IBR España

This module provides prayer request management for the IBR España dashboard.
"""

class PrayerRequests:
    """Prayer Requests for IBR España."""
    
    def __init__(self):
        """Initialize the prayer requests manager."""
        self.requests = []
    
    def add_request(self, name, request, is_private=False):
        """Add a new prayer request."""
        self.requests.append({
            "name": name,
            "request": request,
            "is_private": is_private,
            "created_at": "2023-11-12"
        })
        
    def get_recent_requests(self, limit=5, include_private=False):
        """Get recent prayer requests."""
        if include_private:
            return self.requests[:limit]
        return [r for r in self.requests if not r.get("is_private")][:limit] 