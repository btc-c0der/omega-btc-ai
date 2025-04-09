#!/usr/bin/env python3
"""
YouTube Channel Monitor for Lucas Silveira
Part of the XYKØ LINE SURFER package
"""

import os
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any

logger = logging.getLogger("lucas_youtube_monitor")

class YouTubeMonitor:
    """YouTube channel monitoring for Lucas Silveira."""
    
    def __init__(self, channel_id="UC_LucasSilveiraOfficial", refresh_interval=3600):
        """Initialize the YouTube monitor with channel ID and refresh interval."""
        self.channel_id = channel_id
        self.refresh_interval = refresh_interval
        self.last_update = None
        self.data_path = os.path.join(os.path.dirname(__file__), "../data/youtube_stats.json")
        self.metrics = {
            "subscribers": 0,
            "total_views": 0,
            "videos_count": 0,
            "avg_views_per_video": 0,
            "avg_likes_per_video": 0,
            "avg_comments_per_video": 0,
            "watch_time_hours": 0,
            "engagement_rate": 0.0,
            "growth_rate": 0.0
        }
        self.videos = []
        self._load_data()
        
    def _load_data(self):
        """Load data from storage if available."""
        try:
            if os.path.exists(self.data_path):
                with open(self.data_path, 'r') as f:
                    data = json.load(f)
                    self.metrics = data.get("metrics", self.metrics)
                    self.videos = data.get("videos", [])
                    self.last_update = datetime.fromisoformat(data.get("last_update", datetime.now().isoformat()))
                    logger.info(f"Loaded YouTube data from {self.data_path}")
            else:
                # Ensure directory exists
                os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
                self._simulate_data()
                self._save_data()
        except Exception as e:
            logger.error(f"Error loading YouTube data: {e}")
            self._simulate_data()
            
    def _save_data(self):
        """Save data to storage."""
        try:
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
            with open(self.data_path, 'w') as f:
                json.dump({
                    "metrics": self.metrics,
                    "videos": self.videos,
                    "last_update": datetime.now().isoformat()
                }, f, indent=2)
            logger.info(f"Saved YouTube data to {self.data_path}")
        except Exception as e:
            logger.error(f"Error saving YouTube data: {e}")
            
    def _simulate_data(self):
        """Simulate data for demonstration purposes."""
        self.metrics = {
            "subscribers": 45000,
            "total_views": 5200000,
            "videos_count": 128,
            "avg_views_per_video": 40625,
            "avg_likes_per_video": 2450,
            "avg_comments_per_video": 185,
            "watch_time_hours": 148000,
            "engagement_rate": 5.8,
            "growth_rate": 1.8
        }
        
        # Simulate video data
        surf_titles = [
            "Epic Barrels at Guarda do Embaú",
            "Surfing Massive Waves at Joaquina",
            "Lagoinha do Leste Hidden Gems",
            "Pro Surf Training Session at Saquarema",
            "Sunset Surfing at Farol de Santa Marta",
            "Aerial Tricks Tutorial",
            "My Pre-Competition Ritual",
            "Barrel Riding Techniques",
            "Surviving Giant Ubatuba Swells",
            "Equipment Review: New Surfboard Test",
            "Surf Trip: Indonesian Paradise",
            "Cross Training for Pro Surfers",
            "Recovery Tips After Heavy Sessions",
            "Meet My Surf Team",
            "Q&A: Ask Lucas Anything"
        ]
        
        self.videos = []
        for i, title in enumerate(surf_titles):
            days_ago = i * 14  # One video every two weeks
            self.videos.append({
                "title": title,
                "published_at": (datetime.now() - timedelta(days=days_ago)).isoformat(),
                "views": int(40000 * (0.85 + 0.3 * (1 / (i + 1)))),
                "likes": int(2500 * (0.85 + 0.3 * (1 / (i + 1)))),
                "comments": int(200 * (0.85 + 0.3 * (1 / (i + 1)))),
                "watch_time_hours": int(1200 * (0.85 + 0.3 * (1 / (i + 1)))),
                "thumbnail": f"https://example.com/thumbnails/{i}.jpg",
                "url": f"https://youtube.com/watch?v={i}abcdef"
            })
        
        self.last_update = datetime.now()
        
    def run_update(self):
        """Update YouTube statistics."""
        # In a real implementation, this would call the YouTube API
        # This is a placeholder that simulates data updates
        self._simulate_data_update()
        self._save_data()
        return self.get_channel_stats()
        
    def _simulate_data_update(self):
        """Simulate data update for demonstration."""
        # Simulate small changes to metrics
        growth_factor = 1.005  # Small growth
        self.metrics["subscribers"] = int(self.metrics["subscribers"] * growth_factor)
        self.metrics["total_views"] = int(self.metrics["total_views"] * growth_factor)
        
        # Update averages
        if self.metrics["videos_count"] > 0:
            self.metrics["avg_views_per_video"] = int(self.metrics["total_views"] / self.metrics["videos_count"])
            
        # Update video stats with small increments
        for video in self.videos:
            age_factor = (datetime.now() - datetime.fromisoformat(video["published_at"])).days / 30
            growth = max(0.001, 0.05 * (1 / (age_factor + 1)))  # Newer videos grow faster
            
            video["views"] = int(video["views"] * (1 + growth))
            video["likes"] = int(video["likes"] * (1 + growth * 0.8))
            video["comments"] = int(video["comments"] * (1 + growth * 0.5))
            video["watch_time_hours"] = int(video["watch_time_hours"] * (1 + growth * 0.7))
            
        self.last_update = datetime.now()
        
    def get_channel_stats(self) -> Dict[str, Any]:
        """Get current channel statistics."""
        if not self.last_update or (datetime.now() - self.last_update).total_seconds() > self.refresh_interval:
            self.run_update()
            
        return {
            "channel_id": self.channel_id,
            "last_updated": self.last_update.isoformat(),
            "metrics": self.metrics,
            "recent_videos": self.videos[:5]  # Return only 5 most recent videos
        }
        
    def get_video_performance(self, time_period: str = "all") -> Dict[str, Any]:
        """Get video performance metrics for a given time period."""
        if time_period == "recent":
            # Videos from last 30 days
            cutoff = datetime.now() - timedelta(days=30)
            filtered_videos = [v for v in self.videos 
                              if datetime.fromisoformat(v["published_at"]) >= cutoff]
        elif time_period == "month3":
            # Videos from last 90 days
            cutoff = datetime.now() - timedelta(days=90)
            filtered_videos = [v for v in self.videos 
                              if datetime.fromisoformat(v["published_at"]) >= cutoff]
        else:
            # All videos
            filtered_videos = self.videos
            
        if not filtered_videos:
            return {"period": time_period, "videos_count": 0, "metrics": {}}
            
        total_views = sum(v["views"] for v in filtered_videos)
        total_likes = sum(v["likes"] for v in filtered_videos)
        total_comments = sum(v["comments"] for v in filtered_videos)
        total_watch_time = sum(v["watch_time_hours"] for v in filtered_videos)
        
        return {
            "period": time_period,
            "videos_count": len(filtered_videos),
            "metrics": {
                "total_views": total_views,
                "total_likes": total_likes,
                "total_comments": total_comments,
                "total_watch_time_hours": total_watch_time,
                "avg_views": total_views / len(filtered_videos),
                "avg_likes": total_likes / len(filtered_videos),
                "avg_comments": total_comments / len(filtered_videos),
                "avg_watch_time": total_watch_time / len(filtered_videos),
                "engagement_rate": (total_likes + total_comments) / total_views * 100 if total_views > 0 else 0
            },
            "top_video": max(filtered_videos, key=lambda x: x["views"]) if filtered_videos else None
        }
        
    def get_audience_growth(self, months: int = 6) -> Dict[str, Any]:
        """Simulate audience growth over time."""
        today = datetime.now()
        months_data = []
        
        # Start with current values and work backwards
        current_subs = self.metrics["subscribers"]
        current_views = self.metrics["total_views"]
        
        for i in range(months):
            month_date = today.replace(day=1) - timedelta(days=30*i)
            
            # Simulate previous values (decreasing as we go back in time)
            decay_factor = 0.97 ** i
            month_subs = int(current_subs * decay_factor)
            month_views = int(current_views * decay_factor)
            
            months_data.append({
                "month": month_date.strftime("%B %Y"),
                "subscribers": month_subs,
                "views": month_views,
                "growth_rate": (current_subs / month_subs - 1) * 100 if i > 0 else 0
            })
            
        return {
            "growth_period": f"{months} months",
            "current_subscribers": self.metrics["subscribers"],
            "monthly_data": list(reversed(months_data)),
            "overall_growth_rate": (months_data[0]["subscribers"] / months_data[-1]["subscribers"] - 1) * 100 if months > 1 else 0
        }


if __name__ == "__main__":
    # Simple demonstration of the YouTube monitor
    logging.basicConfig(level=logging.INFO)
    monitor = YouTubeMonitor()
    
    # Get channel stats
    stats = monitor.get_channel_stats()
    print(f"Channel subscribers: {stats['metrics']['subscribers']}")
    print(f"Average views per video: {stats['metrics']['avg_views_per_video']}")
    
    # Get performance metrics
    performance = monitor.get_video_performance("recent")
    print(f"Recent videos count: {performance['videos_count']}")
    if performance['videos_count'] > 0:
        print(f"Top video: {performance.get('top_video', {}).get('title', 'N/A')}") 