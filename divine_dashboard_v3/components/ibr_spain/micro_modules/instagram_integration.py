#!/usr/bin/env python3

"""
IBR España - Instagram Integration Micro Module

This module provides Instagram social media integration for the IBR España dashboard.
"""

import os
import json
import logging
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("instagram_integration")

class InstagramIntegration:
    """Instagram integration for IBR España"""
    
    def __init__(self, 
                 data_dir: Optional[str] = None, 
                 account_name: str = "ibrespana",
                 refresh_interval: int = 900):
        """Initialize the Instagram integration
        
        Args:
            data_dir: Directory to store Instagram data (optional)
            account_name: Instagram account name to follow
            refresh_interval: Time in seconds between refreshes
        """
        self.data_dir = Path(data_dir) if data_dir else Path.home() / "ibr_data" / "instagram"
        self.account_name = account_name
        self.refresh_interval = refresh_interval
        
        # Create data directory if it doesn't exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize posts cache
        self.posts_file = self.data_dir / "instagram_posts.json"
        self.last_refresh_file = self.data_dir / "last_refresh.txt"
        self.posts = self.load_posts()
        
        logger.info(f"Instagram integration initialized for account: {account_name}")
    
    def load_posts(self) -> List[Dict[str, Any]]:
        """Load posts from cache or get new ones if cache is expired"""
        # Check if we need to refresh
        if self.should_refresh():
            try:
                logger.info("Refreshing Instagram posts")
                self.refresh_posts()
            except Exception as e:
                logger.error(f"Error refreshing posts: {e}")
        
        # Return cached posts
        if self.posts_file.exists():
            try:
                with open(self.posts_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading posts from cache: {e}")
        
        # Return sample data if no cached posts exist
        return self._get_sample_posts()
    
    def should_refresh(self) -> bool:
        """Check if we should refresh the posts data"""
        if not self.last_refresh_file.exists():
            return True
            
        try:
            with open(self.last_refresh_file, "r") as f:
                last_refresh = datetime.fromisoformat(f.read().strip())
                
            # Refresh if it's been longer than refresh_interval
            now = datetime.now()
            return (now - last_refresh).total_seconds() > self.refresh_interval
            
        except Exception as e:
            logger.error(f"Error checking refresh time: {e}")
            return True
    
    def refresh_posts(self) -> bool:
        """Refresh Instagram posts from the API
        
        In a real implementation, this would use the Instagram API
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # In a real implementation, this would make an API request
            # For demonstration, we'll just use sample data
            posts = self._get_sample_posts()
            
            # Save posts to cache
            with open(self.posts_file, "w", encoding="utf-8") as f:
                json.dump(posts, f, ensure_ascii=False, indent=2)
                
            # Update last refresh time
            with open(self.last_refresh_file, "w") as f:
                f.write(datetime.now().isoformat())
                
            self.posts = posts
            return True
            
        except Exception as e:
            logger.error(f"Error refreshing posts: {e}")
            return False
    
    def get_recent_posts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the most recent Instagram posts
        
        Args:
            limit: Maximum number of posts to return
            
        Returns:
            List: Recent Instagram posts
        """
        # Ensure posts are loaded
        if not self.posts:
            self.posts = self.load_posts()
            
        # Sort by date (most recent first) and limit
        sorted_posts = sorted(
            self.posts, 
            key=lambda x: datetime.strptime(x.get("date", "2000-01-01"), "%Y-%m-%d"),
            reverse=True
        )
        
        return sorted_posts[:limit]
    
    def categorize_post(self, post: Dict[str, Any]) -> str:
        """Categorize an Instagram post based on its content
        
        Args:
            post: Instagram post data
            
        Returns:
            str: Category label
        """
        caption = post.get("caption", "").lower()
        
        # Define categories and their keywords
        categories = {
            "sermon": ["sermon", "sermón", "predicación", "prédica", "mensaje"],
            "worship": ["worship", "adoración", "alabanza", "música", "canto"],
            "event": ["event", "evento", "actividad", "reunión", "meeting"],
            "youth": ["youth", "jóvenes", "adolescentes", "teenagers"],
            "prayer": ["prayer", "oración", "intercesión", "plegaria"],
            "fellowship": ["fellowship", "comunión", "hermandad", "fraternidad"]
        }
        
        # Check for keywords in caption
        for category, keywords in categories.items():
            if any(keyword in caption for keyword in keywords):
                return category
                
        # Use the type field if available
        if "type" in post:
            return post["type"]
            
        # Default category
        return "general"
    
    def get_posts_by_category(self, category: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get Instagram posts filtered by category
        
        Args:
            category: Category to filter by
            limit: Maximum number of posts to return
            
        Returns:
            List: Filtered Instagram posts
        """
        # Get all posts
        all_posts = self.get_recent_posts(limit=100)  # Get a larger set to filter from
        
        # Filter by category
        filtered = []
        for post in all_posts:
            post_category = self.categorize_post(post)
            if post_category == category:
                filtered.append(post)
                
        # Limit results
        return filtered[:limit]
    
    def _get_sample_posts(self) -> List[Dict[str, Any]]:
        """Get sample Instagram posts"""
        return [
            {
                "id": "post001",
                "image_url": "https://ibr-espana.org/instagram/post001.jpg",
                "caption": "Servicio dominical - ¡Gloria a Dios por Su fidelidad!",
                "likes": 45,
                "date": "2023-11-12",
                "type": "service"
            },
            {
                "id": "post002",
                "image_url": "https://ibr-espana.org/instagram/post002.jpg",
                "caption": "Estudio bíblico del miércoles - profundizando en la Palabra",
                "likes": 36,
                "date": "2023-11-08",
                "type": "study"
            },
            {
                "id": "post003",
                "image_url": "https://ibr-espana.org/instagram/post003.jpg",
                "caption": "Youth group fellowship night - fun and learning!",
                "likes": 52,
                "date": "2023-11-04",
                "type": "youth"
            },
            {
                "id": "post004",
                "image_url": "https://ibr-espana.org/instagram/post004.jpg",
                "caption": "Reunión de oración - buscando el rostro de Dios juntos",
                "likes": 41,
                "date": "2023-11-01",
                "type": "prayer"
            },
            {
                "id": "post005",
                "image_url": "https://ibr-espana.org/instagram/post005.jpg",
                "caption": "Hoy tuvimos un hermoso tiempo de adoración. ¡Gloria a Dios!",
                "likes": 63,
                "date": "2023-10-29",
                "type": "worship"
            },
            {
                "id": "post006",
                "image_url": "https://ibr-espana.org/instagram/post006.jpg",
                "caption": "Sermón sobre la importancia de la fe en tiempos difíciles",
                "likes": 58,
                "date": "2023-10-22",
                "type": "sermon"
            }
        ]


def render_instagram_feed(posts: List[Dict[str, Any]]) -> str:
    """
    Render Instagram posts as HTML
    
    Args:
        posts: List of Instagram post data
    
    Returns:
        str: HTML representation of the Instagram feed
    """
    if not posts:
        return "<div class='instagram-feed-empty'>No hay publicaciones recientes / No recent posts</div>"
    
    html = ""
    for post in posts:
        # Format the date
        date_formatted = post.get("date", "")
        try:
            date_obj = datetime.strptime(date_formatted, "%Y-%m-%d")
            date_formatted = date_obj.strftime("%d %b %Y")
        except:
            pass
        
        # Get post category/type
        post_type = post.get("type", "general").capitalize()
        
        # Create HTML for the post
        html += f"""
        <div class="instagram-post">
            <div class="instagram-post-image">
                <img src="{post.get('image_url', '')}" alt="{post.get('caption', 'Instagram post')}" />
            </div>
            <div class="instagram-post-caption">
                {post.get('caption', '')}
            </div>
            <div class="instagram-post-meta">
                <span class="instagram-post-date">{date_formatted}</span>
                <span class="instagram-post-likes">❤️ {post.get('likes', 0)}</span>
                <span class="instagram-post-type">{post_type}</span>
            </div>
        </div>
        """
    
    return html


# For testing purposes
if __name__ == "__main__":
    instagram = InstagramIntegration()
    recent_posts = instagram.get_recent_posts(3)
    print(f"Found {len(recent_posts)} recent posts")
    
    # Test categorization
    for post in recent_posts:
        category = instagram.categorize_post(post)
        print(f"Post '{post.get('id')}' categorized as '{category}'")
    
    # Test rendering
    html = render_instagram_feed(recent_posts)
    print(html) 