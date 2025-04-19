"""
Devotionals for IBR España

This module provides devotional content for the IBR España dashboard.
"""

class Devotionals:
    """Devotionals for IBR España."""
    
    def __init__(self):
        """Initialize the devotionals manager."""
        self.devotionals = [
            {
                "id": "dev001",
                "title": "La fidelidad de Dios",
                "scripture": "Lamentaciones 3:22-23",
                "content": "Las misericordias de Jehová nunca terminan, nuevas son cada mañana; grande es tu fidelidad.",
                "date": "2023-11-12"
            },
            {
                "id": "dev002",
                "title": "La paz de Dios",
                "scripture": "Filipenses 4:7",
                "content": "Y la paz de Dios, que sobrepasa todo entendimiento, guardará vuestros corazones y vuestros pensamientos en Cristo Jesús.",
                "date": "2023-11-11"
            }
        ]
    
    def get_daily_devotional(self):
        """Get the daily devotional."""
        if self.devotionals:
            return self.devotionals[0]
        return None
        
    def get_recent_devotionals(self, limit=5):
        """Get recent devotionals."""
        return self.devotionals[:limit] 