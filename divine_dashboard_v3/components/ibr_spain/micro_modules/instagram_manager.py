#!/usr/bin/env python3

"""
IBR España - Instagram Manager Micro Module

This module provides comprehensive Instagram account management for @ibrespana.
Features include post scheduling, comment management, analytics reporting,
outreach campaigns, and livestream monitoring.
"""

import os
import json
import logging
import uuid
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any, Tuple

from .instagram_api import InstagramAPI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("instagram_manager")

class Post:
    """Instagram post data structure"""
    
    def __init__(
        self,
        image_path: str,
        caption: str,
        post_id: Optional[str] = None,
        scheduled_time: Optional[str] = None,
        first_comment: Optional[str] = None,
        status: str = "scheduled",
        posted_at: Optional[str] = None,
        likes: int = 0,
        comments_count: int = 0,
        media_type: str = "image"
    ):
        self.id = post_id or str(uuid.uuid4())
        self.image_path = image_path
        self.caption = caption
        self.scheduled_time = scheduled_time
        self.first_comment = first_comment
        self.status = status  # "scheduled", "posted", "failed"
        self.posted_at = posted_at
        self.likes = likes
        self.comments_count = comments_count
        self.media_type = media_type
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "id": self.id,
            "image_path": self.image_path,
            "caption": self.caption,
            "scheduled_time": self.scheduled_time,
            "first_comment": self.first_comment,
            "status": self.status,
            "posted_at": self.posted_at,
            "likes": self.likes,
            "comments_count": self.comments_count,
            "media_type": self.media_type
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Post':
        """Create from dictionary representation"""
        return cls(
            post_id=data.get("id"),
            image_path=data.get("image_path", ""),
            caption=data.get("caption", ""),
            scheduled_time=data.get("scheduled_time"),
            first_comment=data.get("first_comment"),
            status=data.get("status", "scheduled"),
            posted_at=data.get("posted_at"),
            likes=data.get("likes", 0),
            comments_count=data.get("comments_count", 0),
            media_type=data.get("media_type", "image")
        )

class Comment:
    """Instagram comment data structure"""
    
    def __init__(
        self,
        post_id: str,
        username: str,
        text: str,
        comment_id: Optional[str] = None,
        created_at: Optional[str] = None,
        is_hidden: bool = False,
        parent_id: Optional[str] = None
    ):
        self.id = comment_id or str(uuid.uuid4())
        self.post_id = post_id
        self.username = username
        self.text = text
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_hidden = is_hidden
        self.parent_id = parent_id  # For replies
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "id": self.id,
            "post_id": self.post_id,
            "username": self.username,
            "text": self.text,
            "created_at": self.created_at,
            "is_hidden": self.is_hidden,
            "parent_id": self.parent_id
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Comment':
        """Create from dictionary representation"""
        return cls(
            comment_id=data.get("id"),
            post_id=data.get("post_id", ""),
            username=data.get("username", ""),
            text=data.get("text", ""),
            created_at=data.get("created_at"),
            is_hidden=data.get("is_hidden", False),
            parent_id=data.get("parent_id")
        )

class AnalyticsReport:
    """Instagram analytics report data structure"""
    
    def __init__(
        self,
        start_date: str,
        end_date: str,
        metrics: Dict[str, Any],
        report_id: Optional[str] = None,
        generated_at: Optional[str] = None,
        frequency: Optional[str] = None,
        recipients: Optional[List[str]] = None
    ):
        self.id = report_id or str(uuid.uuid4())
        self.start_date = start_date
        self.end_date = end_date
        self.metrics = metrics
        self.generated_at = generated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.frequency = frequency  # "daily", "weekly", "monthly"
        self.recipients = recipients or []
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "id": self.id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "metrics": self.metrics,
            "generated_at": self.generated_at,
            "frequency": self.frequency,
            "recipients": self.recipients
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AnalyticsReport':
        """Create from dictionary representation"""
        return cls(
            report_id=data.get("id"),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date", ""),
            metrics=data.get("metrics", {}),
            generated_at=data.get("generated_at"),
            frequency=data.get("frequency"),
            recipients=data.get("recipients", [])
        )

class OutreachCampaign:
    """Instagram outreach campaign data structure"""
    
    def __init__(
        self,
        name: str,
        target_audience: str,
        message_template: str,
        campaign_id: Optional[str] = None,
        created_at: Optional[str] = None,
        status: str = "active",
        leads: Optional[List[Dict[str, Any]]] = None
    ):
        self.id = campaign_id or str(uuid.uuid4())
        self.name = name
        self.target_audience = target_audience
        self.message_template = message_template
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = status  # "active", "paused", "completed"
        self.leads = leads or []
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            "id": self.id,
            "name": self.name,
            "target_audience": self.target_audience,
            "message_template": self.message_template,
            "created_at": self.created_at,
            "status": self.status,
            "leads": self.leads
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OutreachCampaign':
        """Create from dictionary representation"""
        return cls(
            campaign_id=data.get("id"),
            name=data.get("name", ""),
            target_audience=data.get("target_audience", ""),
            message_template=data.get("message_template", ""),
            created_at=data.get("created_at"),
            status=data.get("status", "active"),
            leads=data.get("leads", [])
        )

class InstagramManager:
    """Instagram account manager for IBR España"""
    
    def __init__(self, 
                 data_dir: Optional[str] = None, 
                 account_name: str = "ibrespana",
                 use_api: bool = True):
        """Initialize the Instagram manager
        
        Args:
            data_dir: Directory to store Instagram data (optional)
            account_name: Instagram account name to manage
            use_api: Whether to use the Instagram API (if configured)
        """
        self.data_dir = Path(data_dir) if data_dir else Path.home() / "ibr_data" / "instagram_manager"
        self.account_name = account_name
        self.use_api = use_api
        
        # Initialize API connection if requested
        self.api = None
        if self.use_api:
            try:
                self.api = InstagramAPI()
                self.api_status = self.api.check_api_connection()
                if self.api_status["status"] == "success":
                    logger.info(f"Connected to Instagram API for account: @{self.api_status['username']}")
                else:
                    logger.warning(f"Instagram API connection failed: {self.api_status.get('message', 'Unknown error')}")
            except Exception as e:
                logger.error(f"Error initializing Instagram API: {e}")
                self.api = None
        
        # Create data directories
        self.posts_dir = self.data_dir / "posts"
        self.comments_dir = self.data_dir / "comments"
        self.reports_dir = self.data_dir / "reports"
        self.campaigns_dir = self.data_dir / "campaigns"
        self.livestreams_dir = self.data_dir / "livestreams"
        
        for directory in [self.posts_dir, self.comments_dir, self.reports_dir, 
                         self.campaigns_dir, self.livestreams_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize data files
        self.scheduled_posts_file = self.posts_dir / "scheduled_posts.json"
        self.published_posts_file = self.posts_dir / "published_posts.json"
        self.comments_file = self.comments_dir / "comments.json"
        self.auto_reply_rules_file = self.comments_dir / "auto_reply_rules.json"
        self.reports_file = self.reports_dir / "analytics_reports.json"
        self.scheduled_reports_file = self.reports_dir / "scheduled_reports.json"
        self.campaigns_file = self.campaigns_dir / "outreach_campaigns.json"
        self.livestreams_file = self.livestreams_dir / "active_livestreams.json"
        
        # Load data
        self._load_data()
        
        logger.info(f"Instagram manager initialized for account: {account_name}")
    
    def _load_data(self):
        """Load data from storage files"""
        # Initialize empty collections
        self.scheduled_posts = []
        self.published_posts = []
        self.comments = []
        self.auto_reply_rules = []
        self.analytics_reports = []
        self.scheduled_reports = []
        self.outreach_campaigns = []
        self.active_livestreams = []
        
        # Load scheduled posts
        if self.scheduled_posts_file.exists():
            try:
                with open(self.scheduled_posts_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.scheduled_posts = [Post.from_dict(post_data) for post_data in data]
            except Exception as e:
                logger.error(f"Error loading scheduled posts: {e}")
        
        # Load published posts
        if self.published_posts_file.exists():
            try:
                with open(self.published_posts_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.published_posts = [Post.from_dict(post_data) for post_data in data]
            except Exception as e:
                logger.error(f"Error loading published posts: {e}")
        
        # Load comments
        if self.comments_file.exists():
            try:
                with open(self.comments_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.comments = [Comment.from_dict(comment_data) for comment_data in data]
            except Exception as e:
                logger.error(f"Error loading comments: {e}")
        
        # Load auto-reply rules
        if self.auto_reply_rules_file.exists():
            try:
                with open(self.auto_reply_rules_file, "r", encoding="utf-8") as f:
                    self.auto_reply_rules = json.load(f)
            except Exception as e:
                logger.error(f"Error loading auto-reply rules: {e}")
        
        # Load analytics reports
        if self.reports_file.exists():
            try:
                with open(self.reports_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.analytics_reports = [AnalyticsReport.from_dict(report_data) for report_data in data]
            except Exception as e:
                logger.error(f"Error loading analytics reports: {e}")
        
        # Load scheduled reports
        if self.scheduled_reports_file.exists():
            try:
                with open(self.scheduled_reports_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.scheduled_reports = [AnalyticsReport.from_dict(report_data) for report_data in data]
            except Exception as e:
                logger.error(f"Error loading scheduled reports: {e}")
        
        # Load outreach campaigns
        if self.campaigns_file.exists():
            try:
                with open(self.campaigns_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.outreach_campaigns = [OutreachCampaign.from_dict(campaign_data) for campaign_data in data]
            except Exception as e:
                logger.error(f"Error loading outreach campaigns: {e}")
        
        # Load active livestreams
        if self.livestreams_file.exists():
            try:
                with open(self.livestreams_file, "r", encoding="utf-8") as f:
                    self.active_livestreams = json.load(f)
            except Exception as e:
                logger.error(f"Error loading active livestreams: {e}")
    
    def _save_scheduled_posts(self):
        """Save scheduled posts to file"""
        try:
            data = [post.to_dict() for post in self.scheduled_posts]
            with open(self.scheduled_posts_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving scheduled posts: {e}")
    
    def _save_published_posts(self):
        """Save published posts to file"""
        try:
            data = [post.to_dict() for post in self.published_posts]
            with open(self.published_posts_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving published posts: {e}")
    
    def _save_comments(self):
        """Save comments to file"""
        try:
            data = [comment.to_dict() for comment in self.comments]
            with open(self.comments_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving comments: {e}")
    
    def _save_auto_reply_rules(self):
        """Save auto-reply rules to file"""
        try:
            with open(self.auto_reply_rules_file, "w", encoding="utf-8") as f:
                json.dump(self.auto_reply_rules, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving auto-reply rules: {e}")
    
    def _save_reports(self):
        """Save analytics reports to file"""
        try:
            data = [report.to_dict() for report in self.analytics_reports]
            with open(self.reports_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving analytics reports: {e}")
    
    def _save_scheduled_reports(self):
        """Save scheduled reports to file"""
        try:
            data = [report.to_dict() for report in self.scheduled_reports]
            with open(self.scheduled_reports_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving scheduled reports: {e}")
    
    def _save_campaigns(self):
        """Save outreach campaigns to file"""
        try:
            data = [campaign.to_dict() for campaign in self.outreach_campaigns]
            with open(self.campaigns_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving outreach campaigns: {e}")
    
    def _save_livestreams(self):
        """Save active livestreams to file"""
        try:
            with open(self.livestreams_file, "w", encoding="utf-8") as f:
                json.dump(self.active_livestreams, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving active livestreams: {e}")

    # Post scheduling methods with API integration
    def schedule_post(self, 
                      image_path: str, 
                      caption: str, 
                      scheduled_time: str,
                      first_comment: Optional[str] = None,
                      publish_immediately: bool = False) -> Post:
        """Schedule a new Instagram post
        
        Args:
            image_path: Path to the image file
            caption: Post caption text
            scheduled_time: Scheduled posting time (YYYY-MM-DD HH:MM:SS)
            first_comment: Optional first comment (typically for hashtags)
            publish_immediately: Whether to publish the post immediately (if API is available)
            
        Returns:
            Post: The scheduled post object
        """
        post = Post(
            image_path=image_path,
            caption=caption,
            scheduled_time=scheduled_time,
            first_comment=first_comment
        )
        
        # Try to publish immediately if requested
        if publish_immediately and self.api:
            try:
                # Validate the image path (could be URL or local path)
                image_url = image_path
                if not image_path.startswith(('http://', 'https://')):
                    # In a real implementation, would upload the local image and get a URL
                    logger.warning("Direct publishing from local files not implemented")
                    # For now, we'll just schedule the post
                    publish_immediately = False
                
                if publish_immediately:
                    result = self.api.publish_post(image_url, caption)
                    if result["status"] == "success":
                        post.status = "posted"
                        post.posted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Add first comment if provided
                        if first_comment and "post_id" in result:
                            comment_result = self.api.create_comment(result["post_id"], first_comment)
                            if comment_result["status"] != "success":
                                logger.warning(f"Failed to add first comment: {comment_result.get('message')}")
                        
                        logger.info("Post published successfully through API")
                    else:
                        logger.warning(f"Failed to publish post: {result.get('message')}")
                        # Still schedule the post for later
            except Exception as e:
                logger.error(f"Error publishing post: {e}")
                # Still schedule the post for later
        
        # Add to scheduled posts
        if post.status == "scheduled":
            self.scheduled_posts.append(post)
            self._save_scheduled_posts()
            logger.info(f"Post scheduled for {scheduled_time}")
        elif post.status == "posted":
            self.published_posts.append(post)
            self._save_published_posts()
            logger.info(f"Post published immediately")
        
        return post
    
    def process_scheduled_posts(self) -> int:
        """Process posts that are scheduled to be published now
        
        Returns:
            int: Number of posts published
        """
        if not self.api:
            logger.warning("API not available, skipping post processing")
            return 0
        
        count = 0
        current_time = datetime.now()
        
        # Find posts scheduled for now or in the past
        posts_to_publish = []
        remaining_posts = []
        
        for post in self.scheduled_posts:
            try:
                if post.scheduled_time is None:
                    logger.warning(f"Post {post.id} has no scheduled time, skipping")
                    remaining_posts.append(post)
                    continue
                    
                scheduled_time = datetime.strptime(post.scheduled_time, "%Y-%m-%d %H:%M:%S")
                if scheduled_time <= current_time:
                    posts_to_publish.append(post)
                else:
                    remaining_posts.append(post)
            except Exception as e:
                logger.error(f"Error parsing scheduled time: {e}")
                remaining_posts.append(post)
        
        # Update scheduled posts list
        self.scheduled_posts = remaining_posts
        self._save_scheduled_posts()
        
        # Publish each post
        for post in posts_to_publish:
            try:
                # Check if image is URL or local path
                image_url = post.image_path
                if not post.image_path.startswith(('http://', 'https://')):
                    # In a real implementation, would upload the local image and get a URL
                    logger.warning("Direct publishing from local files not implemented")
                    # Skip this post for now
                    continue
                
                # Publish the post
                result = self.api.publish_post(image_url, post.caption)
                if result["status"] == "success":
                    post.status = "posted"
                    post.posted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Add first comment if provided
                    if post.first_comment and "post_id" in result:
                        comment_result = self.api.create_comment(result["post_id"], post.first_comment)
                        if comment_result["status"] != "success":
                            logger.warning(f"Failed to add first comment: {comment_result.get('message')}")
                    
                    # Add to published posts
                    self.published_posts.append(post)
                    count += 1
                    logger.info(f"Post {post.id} published successfully")
                else:
                    logger.error(f"Failed to publish post {post.id}: {result.get('message')}")
                    # Return the post to scheduled posts with failed status
                    post.status = "failed"
                    self.scheduled_posts.append(post)
            except Exception as e:
                logger.error(f"Error publishing post {post.id}: {e}")
                # Return the post to scheduled posts with failed status
                post.status = "failed"
                self.scheduled_posts.append(post)
        
        # Save changes
        self._save_scheduled_posts()
        self._save_published_posts()
        
        return count

    # Fetch real data from API methods
    def fetch_recent_posts(self, limit: int = 10) -> List[Post]:
        """Fetch recent posts from the Instagram API
        
        Args:
            limit: Maximum number of posts to fetch
            
        Returns:
            List[Post]: List of recent posts
        """
        if not self.api:
            logger.warning("API not available, returning sample data")
            return []
        
        try:
            api_posts = self.api.get_recent_posts(limit)
            posts = []
            
            for api_post in api_posts:
                try:
                    post = Post(
                        post_id=api_post.get("id"),
                        image_path=api_post.get("media_url", ""),
                        caption=api_post.get("caption", ""),
                        status="posted",
                        posted_at=api_post.get("timestamp"),
                        likes=api_post.get("like_count", 0),
                        comments_count=api_post.get("comments_count", 0),
                        media_type=api_post.get("media_type", "image")
                    )
                    posts.append(post)
                except Exception as e:
                    logger.error(f"Error processing API post: {e}")
            
            return posts
        except Exception as e:
            logger.error(f"Error fetching recent posts: {e}")
            return []
    
    def fetch_post_comments(self, post_id: str, limit: int = 50) -> List[Comment]:
        """Fetch comments for a post from the Instagram API
        
        Args:
            post_id: ID of the post
            limit: Maximum number of comments to fetch
            
        Returns:
            List[Comment]: List of comments
        """
        if not self.api:
            logger.warning("API not available, returning empty comments list")
            return []
        
        try:
            api_comments = self.api.get_post_comments(post_id, limit)
            comments = []
            
            for api_comment in api_comments:
                try:
                    comment = Comment(
                        post_id=post_id,
                        username=api_comment.get("username", ""),
                        text=api_comment.get("text", ""),
                        comment_id=api_comment.get("id"),
                        created_at=api_comment.get("timestamp")
                    )
                    comments.append(comment)
                    
                    # Also add any replies
                    replies_data = api_comment.get("replies", {}).get("data", [])
                    for reply in replies_data:
                        reply_comment = Comment(
                            post_id=post_id,
                            username=reply.get("username", ""),
                            text=reply.get("text", ""),
                            comment_id=reply.get("id"),
                            created_at=reply.get("timestamp"),
                            parent_id=api_comment.get("id")
                        )
                        comments.append(reply_comment)
                except Exception as e:
                    logger.error(f"Error processing API comment: {e}")
            
            return comments
        except Exception as e:
            logger.error(f"Error fetching post comments: {e}")
            return []
    
    def add_comment_to_api(self, post_id: str, comment_text: str) -> Dict[str, Any]:
        """Add a comment to a post using the Instagram API
        
        Args:
            post_id: ID of the post
            comment_text: Text of the comment
            
        Returns:
            Dict: Result of the operation
        """
        if not self.api:
            return {"status": "error", "message": "API not available"}
        
        try:
            return self.api.create_comment(post_id, comment_text)
        except Exception as e:
            logger.error(f"Error adding comment through API: {e}")
            return {"status": "error", "message": str(e)}
    
    def hide_comment_via_api(self, comment_id: str, hide: bool = True) -> Dict[str, Any]:
        """Hide or unhide a comment using the Instagram API
        
        Args:
            comment_id: ID of the comment
            hide: Whether to hide or unhide the comment
            
        Returns:
            Dict: Result of the operation
        """
        if not self.api:
            return {"status": "error", "message": "API not available"}
        
        try:
            return self.api.hide_comment(comment_id, hide)
        except Exception as e:
            logger.error(f"Error {'hiding' if hide else 'unhiding'} comment through API: {e}")
            return {"status": "error", "message": str(e)}
    
    # Enhance analytics with real data
    def generate_analytics_report(self, start_date: str, end_date: str) -> AnalyticsReport:
        """Generate an analytics report with real data if available
        
        Args:
            start_date: Start date for the report (YYYY-MM-DD)
            end_date: End date for the report (YYYY-MM-DD)
            
        Returns:
            AnalyticsReport: The generated report
        """
        # Start with mock metrics
        metrics = {
            "followers_count": 1250,
            "followers_growth": 75,
            "posts_count": 12,
            "total_likes": 3420,
            "total_comments": 520,
            "engagement_rate": 4.8,
            "reach": 15600,
            "impressions": 22400,
            "top_posts": [
                {"id": "post001", "likes": 345, "comments": 42},
                {"id": "post002", "likes": 287, "comments": 38}
            ]
        }
        
        # Try to enhance with real data if API is available
        if self.api:
            try:
                # Get account insights
                account_insights = self.api.get_insights(period="day")
                if account_insights["status"] == "success":
                    insights_data = account_insights["insights"]
                    
                    # Parse and integrate insights data
                    for metric in insights_data:
                        metric_name = metric.get("name")
                        if metric_name == "impressions":
                            metrics["impressions"] = metric.get("values", [{}])[0].get("value", metrics["impressions"])
                        elif metric_name == "reach":
                            metrics["reach"] = metric.get("values", [{}])[0].get("value", metrics["reach"])
                        elif metric_name == "profile_views":
                            metrics["profile_views"] = metric.get("values", [{}])[0].get("value", 0)
                        elif metric_name == "follower_count":
                            metrics["followers_count"] = metric.get("values", [{}])[0].get("value", metrics["followers_count"])
                
                # Get media insights for top posts
                try:
                    posts = self.fetch_recent_posts(limit=5)
                    if posts:
                        metrics["posts_count"] = len(posts)
                        top_posts = []
                        
                        for post in posts:
                            top_posts.append({
                                "id": post.id,
                                "likes": post.likes,
                                "comments": post.comments_count
                            })
                        
                        # Sort by engagement (likes + comments)
                        top_posts.sort(key=lambda x: x["likes"] + x["comments"], reverse=True)
                        metrics["top_posts"] = top_posts[:3]  # Top 3 posts
                        
                        # Calculate total engagement
                        total_likes = sum(post.likes for post in posts)
                        total_comments = sum(post.comments_count for post in posts)
                        metrics["total_likes"] = total_likes
                        metrics["total_comments"] = total_comments
                        
                        # Calculate engagement rate
                        if metrics["followers_count"] > 0:
                            metrics["engagement_rate"] = round(((total_likes + total_comments) / metrics["followers_count"]) * 100, 2)
                except Exception as e:
                    logger.error(f"Error enhancing report with posts data: {e}")
            except Exception as e:
                logger.error(f"Error enhancing report with API data: {e}")
        
        # Create and return the report
        report = AnalyticsReport(
            start_date=start_date,
            end_date=end_date,
            metrics=metrics
        )
        
        self.analytics_reports.append(report)
        self._save_reports()
        
        logger.info(f"Analytics report generated for period {start_date} to {end_date}")
        return report

    # New methods for API integration
    def get_api_status(self) -> Dict[str, Any]:
        """Get the current API connection status
        
        Returns:
            Dict: API status information
        """
        if not self.api:
            return {"status": "error", "message": "API not initialized"}
        
        return self.api.check_api_connection()
    
    def reconnect_api(self) -> Dict[str, Any]:
        """Attempt to reconnect to the Instagram API
        
        Returns:
            Dict: Result of the reconnection attempt
        """
        try:
            self.api = InstagramAPI()
            status = self.api.check_api_connection()
            if status["status"] == "success":
                logger.info(f"Reconnected to Instagram API for account: @{status['username']}")
            else:
                logger.warning(f"Instagram API reconnection failed: {status.get('message', 'Unknown error')}")
            return status
        except Exception as e:
            logger.error(f"Error reconnecting to Instagram API: {e}")
            return {"status": "error", "message": str(e)}

    # Post scheduling methods
    def edit_scheduled_post(self,
                           post_id: str,
                           caption: Optional[str] = None,
                           scheduled_time: Optional[str] = None,
                           first_comment: Optional[str] = None,
                           image_path: Optional[str] = None) -> Optional[Post]:
        """Edit a scheduled Instagram post
        
        Args:
            post_id: ID of the post to edit
            caption: Updated caption text (optional)
            scheduled_time: Updated scheduled time (optional)
            first_comment: Updated first comment (optional)
            image_path: Updated image path (optional)
            
        Returns:
            Post: The updated post object, or None if not found
        """
        for post in self.scheduled_posts:
            if post.id == post_id:
                if caption is not None:
                    post.caption = caption
                if scheduled_time is not None:
                    post.scheduled_time = scheduled_time
                if first_comment is not None:
                    post.first_comment = first_comment
                if image_path is not None:
                    post.image_path = image_path
                
                self._save_scheduled_posts()
                logger.info(f"Post {post_id} updated")
                return post
        
        logger.warning(f"Post {post_id} not found")
        return None
    
    def delete_scheduled_post(self, post_id: str) -> bool:
        """Delete a scheduled Instagram post
        
        Args:
            post_id: ID of the post to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        for i, post in enumerate(self.scheduled_posts):
            if post.id == post_id:
                del self.scheduled_posts[i]
                self._save_scheduled_posts()
                logger.info(f"Post {post_id} deleted")
                return True
        
        logger.warning(f"Post {post_id} not found")
        return False
    
    def get_scheduled_posts(self) -> List[Post]:
        """Get all scheduled posts
        
        Returns:
            List[Post]: List of scheduled posts
        """
        return self.scheduled_posts

    # Comment management methods
    def add_comment(self,
                   post_id: str,
                   username: str,
                   text: str,
                   comment_id: Optional[str] = None) -> Comment:
        """Add a comment to a post
        
        Args:
            post_id: ID of the post
            username: Username of the commenter
            text: Comment text
            comment_id: Optional comment ID
            
        Returns:
            Comment: The created comment object
        """
        comment = Comment(
            post_id=post_id,
            username=username,
            text=text,
            comment_id=comment_id
        )
        
        self.comments.append(comment)
        self._save_comments()
        
        logger.info(f"Comment added to post {post_id}")
        return comment
    
    def get_comments(self, post_id: str) -> List[Comment]:
        """Get all comments for a post
        
        Args:
            post_id: ID of the post
            
        Returns:
            List[Comment]: List of comments for the post
        """
        return [comment for comment in self.comments 
                if comment.post_id == post_id and comment.parent_id is None]
    
    def get_comment_replies(self, comment_id: str) -> List[Comment]:
        """Get all replies to a comment
        
        Args:
            comment_id: ID of the parent comment
            
        Returns:
            List[Comment]: List of reply comments
        """
        return [comment for comment in self.comments if comment.parent_id == comment_id]
    
    def hide_comment(self, comment_id: str) -> bool:
        """Hide a comment
        
        Args:
            comment_id: ID of the comment to hide
            
        Returns:
            bool: True if hidden, False if not found
        """
        for comment in self.comments:
            if comment.id == comment_id:
                comment.is_hidden = True
                self._save_comments()
                logger.info(f"Comment {comment_id} hidden")
                return True
        
        logger.warning(f"Comment {comment_id} not found")
        return False
    
    def reply_to_comment(self, comment_id: str, reply_text: str) -> Optional[Comment]:
        """Reply to a comment
        
        Args:
            comment_id: ID of the comment to reply to
            reply_text: Reply text
            
        Returns:
            Comment: The reply comment object, or None if parent not found
        """
        parent_comment = None
        for comment in self.comments:
            if comment.id == comment_id:
                parent_comment = comment
                break
        
        if parent_comment:
            reply = Comment(
                post_id=parent_comment.post_id,
                username=self.account_name,
                text=reply_text,
                parent_id=comment_id
            )
            
            self.comments.append(reply)
            self._save_comments()
            
            logger.info(f"Replied to comment {comment_id}")
            return reply
        
        logger.warning(f"Parent comment {comment_id} not found")
        return None

    # Auto-reply functionality
    def add_auto_reply_rule(self, keywords: List[str], reply_template: str) -> Dict[str, Any]:
        """Add an auto-reply rule
        
        Args:
            keywords: List of keywords to trigger the rule
            reply_template: Template for the auto-reply
            
        Returns:
            Dict: The created rule
        """
        rule = {
            "id": str(uuid.uuid4()),
            "keywords": keywords,
            "reply_template": reply_template,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.auto_reply_rules.append(rule)
        self._save_auto_reply_rules()
        
        logger.info(f"Auto-reply rule added for keywords: {', '.join(keywords)}")
        return rule
    
    def process_auto_replies(self) -> int:
        """Process auto-replies for all comments
        
        Returns:
            int: Number of auto-replies generated
        """
        count = 0
        
        # Get comments without replies
        for comment in self.comments:
            # Skip comments that already have replies
            if any(reply.parent_id == comment.id for reply in self.comments):
                continue
            
            # Check each rule
            for rule in self.auto_reply_rules:
                keywords = rule["keywords"]
                reply_template = rule["reply_template"]
                
                # Check if any keyword is in the comment
                if any(keyword.lower() in comment.text.lower() for keyword in keywords):
                    # Generate reply
                    reply = self.reply_to_comment(comment.id, reply_template)
                    if reply:
                        count += 1
                    break  # Only apply the first matching rule
        
        logger.info(f"Generated {count} auto-replies")
        return count

    # Analytics reporting
    def schedule_analytics_report(self, 
                                 frequency: str, 
                                 recipients: List[str],
                                 start_date: Optional[str] = None) -> AnalyticsReport:
        """Schedule recurring analytics reports
        
        Args:
            frequency: Report frequency ("daily", "weekly", "monthly")
            recipients: List of email recipients
            start_date: Optional start date (defaults to today)
            
        Returns:
            AnalyticsReport: The scheduled report template
        """
        if start_date is None:
            start_date = datetime.now().strftime("%Y-%m-%d")
        
        # Create a template report
        report = AnalyticsReport(
            start_date=start_date,
            end_date="recurring",
            metrics={},
            frequency=frequency,
            recipients=recipients
        )
        
        self.scheduled_reports.append(report)
        self._save_scheduled_reports()
        
        logger.info(f"Analytics report scheduled with {frequency} frequency")
        return report

    # Outreach campaign functionality
    def create_outreach_campaign(self,
                                name: str,
                                target_audience: str,
                                message_template: str) -> OutreachCampaign:
        """Create a new outreach campaign
        
        Args:
            name: Campaign name
            target_audience: Description of target audience
            message_template: Template for outreach messages
            
        Returns:
            OutreachCampaign: The created campaign
        """
        campaign = OutreachCampaign(
            name=name,
            target_audience=target_audience,
            message_template=message_template
        )
        
        self.outreach_campaigns.append(campaign)
        self._save_campaigns()
        
        logger.info(f"Outreach campaign created: {name}")
        return campaign
    
    def add_outreach_lead(self,
                         campaign_id: str,
                         username: str,
                         custom_message: Optional[str] = None) -> bool:
        """Add a lead to an outreach campaign
        
        Args:
            campaign_id: ID of the campaign
            username: Instagram username of the lead
            custom_message: Custom message for this lead (optional)
            
        Returns:
            bool: True if added, False if campaign not found
        """
        for campaign in self.outreach_campaigns:
            if campaign.id == campaign_id:
                lead = {
                    "id": str(uuid.uuid4()),
                    "username": username,
                    "custom_message": custom_message,
                    "status": "pending",  # "pending", "contacted", "responded", "converted"
                    "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                campaign.leads.append(lead)
                self._save_campaigns()
                
                logger.info(f"Lead {username} added to campaign {campaign_id}")
                return True
        
        logger.warning(f"Campaign {campaign_id} not found")
        return False
    
    def get_outreach_leads(self, campaign_id: str) -> List[Dict[str, Any]]:
        """Get all leads for a campaign
        
        Args:
            campaign_id: ID of the campaign
            
        Returns:
            List[Dict]: List of campaign leads
        """
        for campaign in self.outreach_campaigns:
            if campaign.id == campaign_id:
                return campaign.leads
        
        return []

    # Livestream monitoring
    def start_livestream_monitoring(self,
                                  stream_id: str,
                                  notification_email: Optional[str] = None) -> Dict[str, Any]:
        """Start monitoring a livestream
        
        Args:
            stream_id: ID of the livestream
            notification_email: Email for notifications (optional)
            
        Returns:
            Dict: Livestream data
        """
        stream = {
            "id": stream_id,
            "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "is_monitoring": True,
            "notification_email": notification_email,
            "technical_issues": [],
            "comments": []
        }
        
        self.active_livestreams.append(stream)
        self._save_livestreams()
        
        logger.info(f"Started monitoring livestream {stream_id}")
        return stream
    
    def stop_livestream_monitoring(self, stream_id: str) -> bool:
        """Stop monitoring a livestream
        
        Args:
            stream_id: ID of the livestream
            
        Returns:
            bool: True if stopped, False if not found
        """
        for stream in self.active_livestreams:
            if stream["id"] == stream_id:
                stream["is_monitoring"] = False
                stream["ended_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_livestreams()
                
                logger.info(f"Stopped monitoring livestream {stream_id}")
                return True
        
        logger.warning(f"Livestream {stream_id} not found")
        return False
    
    def get_livestream(self, stream_id: str) -> Optional[Dict[str, Any]]:
        """Get livestream data
        
        Args:
            stream_id: ID of the livestream
            
        Returns:
            Dict: Livestream data, or None if not found
        """
        for stream in self.active_livestreams:
            if stream["id"] == stream_id:
                return stream
        
        return None
    
    def add_livestream_comment(self,
                              stream_id: str,
                              username: str,
                              text: str,
                              comment_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Add a comment to a livestream
        
        Args:
            stream_id: ID of the livestream
            username: Username of the commenter
            text: Comment text
            comment_id: Optional comment ID
            
        Returns:
            Dict: Comment data, or None if stream not found
        """
        for stream in self.active_livestreams:
            if stream["id"] == stream_id:
                comment = {
                    "id": comment_id or str(uuid.uuid4()),
                    "username": username,
                    "text": text,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "is_technical_issue": self.is_technical_issue(text)
                }
                
                stream["comments"].append(comment)
                
                # Add to technical issues if applicable
                if comment["is_technical_issue"]:
                    stream["technical_issues"].append({
                        "comment_id": comment["id"],
                        "issue": text,
                        "reported_at": comment["created_at"]
                    })
                
                self._save_livestreams()
                
                logger.info(f"Comment added to livestream {stream_id}")
                return comment
        
        logger.warning(f"Livestream {stream_id} not found")
        return None
    
    def is_technical_issue(self, text: str) -> bool:
        """Check if a comment indicates a technical issue
        
        Args:
            text: Comment text
            
        Returns:
            bool: True if it's a technical issue
        """
        technical_keywords = [
            "audio", "sound", "video", "quality", "cutting out", "buffering",
            "lag", "frozen", "stuck", "can't hear", "can't see", "blurry"
        ]
        
        return any(keyword.lower() in text.lower() for keyword in technical_keywords)


# For testing purposes
if __name__ == "__main__":
    manager = InstagramManager()
    
    # Test post scheduling
    post = manager.schedule_post(
        image_path="test_image.jpg",
        caption="Test post for IBR España #iglesia #fe",
        scheduled_time=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
        first_comment="Más hashtags: #cristo #biblia #madrid"
    )
    
    print(f"Scheduled post: {post.id}")
    
    # Test auto-replies
    rule = manager.add_auto_reply_rule(
        keywords=["prayer", "oración"],
        reply_template="Thank you for your prayer request. Our team will pray for you."
    )
    
    print(f"Added auto-reply rule: {rule['id']}") 