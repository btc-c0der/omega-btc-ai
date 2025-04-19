#!/usr/bin/env python3

"""
Instagram Integration for IBR España

This module provides integration with Instagram for the IBR España dashboard.
It's a simplified version that delegates to the InstagramManager in the standalone package.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, cast

# Define a base InstagramManager before trying to import the real one
class BaseInstagramManager:
    """Base implementation of InstagramManager."""
    def __init__(self):
        self.followers = 0
        self.posts = 0
        self.engagement_rate = 0
        self.last_update = "Never"
        
    def get_stats(self) -> Dict[str, Any]:
        """Get account statistics."""
        return {
            "followers": self.followers,
            "posts": self.posts,
            "engagement_rate": self.engagement_rate,
            "last_update": self.last_update
        }
        
    def create_post(self, caption: str, hashtags: str) -> Dict[str, Any]:
        """Create a new post."""
        return {"success": False, "error": "Not implemented in base class"}
        
    def analyze_account(self) -> Dict[str, Any]:
        """Analyze the account."""
        return {"success": False, "error": "Not implemented in base class"}

# Try to import the actual InstagramManager
try:
    # Add parent directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(current_dir))
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)
    
    # Import from standalone module
    from ibr_standalone import InstagramManager
except ImportError:
    # Use the base implementation if import fails
    InstagramManager = BaseInstagramManager

class InstagramIntegration:
    """Integration with Instagram for IBR España."""
    
    def __init__(self):
        """Initialize the Instagram integration."""
        self.manager = InstagramManager()
        
    def get_account_stats(self) -> Dict[str, Any]:
        """Get account statistics from Instagram."""
        return cast(Dict[str, Any], self.manager.get_stats())
    
    def create_instagram_post(self, caption: str, hashtags: str) -> Dict[str, Any]:
        """Create a new Instagram post."""
        result = self.manager.create_post(caption, hashtags)
        if isinstance(result, str):
            return {"success": True, "message": result}
        return result
    
    def analyze_instagram_account(self) -> Dict[str, Any]:
        """Analyze the Instagram account."""
        result = self.manager.analyze_account()
        if isinstance(result, str):
            return {"success": True, "analysis": result}
        return result
    
    def get_instagram_feed(self) -> List[Dict[str, Any]]:
        """Get recent posts from the Instagram feed."""
        # This is a placeholder implementation that returns sample data
        return [
            {
                "id": "post1",
                "image_url": "https://ibr-espana.org/instagram/post1.jpg",
                "caption": "Servicio dominical - ¡Gloria a Dios por Su fidelidad!",
                "likes": 45,
                "date": "2023-11-12",
                "category": "service"
            },
            {
                "id": "post2",
                "image_url": "https://ibr-espana.org/instagram/post2.jpg",
                "caption": "Estudio bíblico del miércoles - profundizando en la Palabra",
                "likes": 36,
                "date": "2023-11-08",
                "category": "bible_study"
            }
        ]
    
    def categorize_post(self, post: Dict[str, Any]) -> str:
        """Categorize a post based on its content."""
        caption = post.get('caption', '').lower()
        
        if 'servicio' in caption or 'domingo' in caption or 'service' in caption:
            return 'service'
        elif 'estudio' in caption or 'bible' in caption or 'study' in caption:
            return 'bible_study'
        elif 'joven' in caption or 'youth' in caption:
            return 'youth'
        elif 'oración' in caption or 'prayer' in caption:
            return 'prayer'
        else:
            return 'other'

# Helper function for rendering Instagram feed
def render_instagram_feed(posts: List[Dict[str, Any]]) -> str:
    """Render Instagram feed as HTML."""
    html = '<div class="instagram-feed">'
    for post in posts:
        html += f'''
        <div class="instagram-post">
            <img src="{post.get('image_url', '')}" alt="Instagram post">
            <p class="caption">{post.get('caption', '')}</p>
            <p class="likes">❤️ {post.get('likes', 0)} likes</p>
            <p class="date">{post.get('date', '')}</p>
        </div>
        '''
    html += '</div>'
    return html

# For testing purposes
if __name__ == "__main__":
    instagram = InstagramIntegration()
    recent_posts = instagram.get_instagram_feed()
    print(f"Found {len(recent_posts)} recent posts")
    
    # Test categorization
    for post in recent_posts:
        category = instagram.categorize_post(post)
        print(f"Post '{post.get('id')}' categorized as '{category}'")
    
    # Test rendering
    html = render_instagram_feed(recent_posts)
    print(f"Generated HTML: {len(html)} characters") 