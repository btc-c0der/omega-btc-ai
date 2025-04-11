#!/usr/bin/env python3
"""
Tests for the InstagramManager module.
"""

import unittest
from datetime import datetime, timedelta
import json
import os
import sys
from pathlib import Path
import shutil
import tempfile

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from micro_modules.instagram_manager import (
    InstagramManager,
    Post,
    Comment,
    AnalyticsReport,
    OutreachCampaign
)

class TestInstagramManager(unittest.TestCase):
    """Test cases for InstagramManager class."""

    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.manager = InstagramManager(
            data_dir=self.test_dir,
            account_name="ibrespana"
        )

    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary directory
        shutil.rmtree(self.test_dir)

    def test_schedule_post(self):
        """Test scheduling a post."""
        # Schedule a post for tomorrow
        tomorrow = datetime.now() + timedelta(days=1)
        scheduled_time = tomorrow.strftime("%Y-%m-%d %H:%M:%S")
        
        post = self.manager.schedule_post(
            image_path="test_image.jpg",
            caption="Test post for IBR España #iglesia #fe",
            scheduled_time=scheduled_time,
            first_comment="Más hashtags: #cristo #biblia #madrid"
        )
        
        # Verify post was scheduled
        self.assertIsNotNone(post.id)
        self.assertEqual(post.caption, "Test post for IBR España #iglesia #fe")
        self.assertEqual(post.scheduled_time, scheduled_time)
        self.assertEqual(post.first_comment, "Más hashtags: #cristo #biblia #madrid")
        
        # Check if post is in scheduled posts list
        scheduled_posts = self.manager.get_scheduled_posts()
        self.assertEqual(len(scheduled_posts), 1)
        self.assertEqual(scheduled_posts[0].id, post.id)

    def test_edit_scheduled_post(self):
        """Test editing a scheduled post."""
        # Schedule a post
        post = self.manager.schedule_post(
            image_path="test_image.jpg",
            caption="Original caption",
            scheduled_time=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Edit the post
        updated_post = self.manager.edit_scheduled_post(
            post_id=post.id,
            caption="Updated caption",
            first_comment="New comment"
        )
        
        # Verify post was updated
        self.assertEqual(updated_post.caption, "Updated caption")
        self.assertEqual(updated_post.first_comment, "New comment")

    def test_delete_scheduled_post(self):
        """Test deleting a scheduled post."""
        # Schedule a post
        post = self.manager.schedule_post(
            image_path="test_image.jpg",
            caption="Test caption",
            scheduled_time=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Delete the post
        result = self.manager.delete_scheduled_post(post.id)
        
        # Verify post was deleted
        self.assertTrue(result)
        scheduled_posts = self.manager.get_scheduled_posts()
        self.assertEqual(len(scheduled_posts), 0)

    def test_manage_comments(self):
        """Test comment management functionality."""
        # Add a comment
        comment = self.manager.add_comment(
            post_id="test_post_id",
            username="user123",
            text="Great message! God bless.",
            comment_id="comment1"
        )
        
        # Hide a comment
        self.manager.hide_comment(comment.id)
        
        # Verify comment is hidden
        comments = self.manager.get_comments("test_post_id")
        self.assertTrue(comments[0].is_hidden)
        
        # Reply to a comment
        reply = self.manager.reply_to_comment(
            comment_id=comment.id,
            reply_text="Thank you for your support! Blessings."
        )
        
        # Verify reply was added
        self.assertEqual(reply.text, "Thank you for your support! Blessings.")
        self.assertEqual(reply.parent_id, comment.id)

    def test_auto_comment_replies(self):
        """Test automatic comment reply functionality."""
        # Set up auto-reply rules
        self.manager.add_auto_reply_rule(
            keywords=["prayer", "oración"],
            reply_template="Thank you for your prayer request. Our team will pray for you."
        )
        
        # Add a comment with matching keyword
        comment = self.manager.add_comment(
            post_id="test_post_id",
            username="user456",
            text="Please pray for my family.",
            comment_id="comment2"
        )
        
        # Process auto-replies
        self.manager.process_auto_replies()
        
        # Verify auto-reply was created
        replies = self.manager.get_comment_replies(comment.id)
        self.assertEqual(len(replies), 1)
        self.assertIn("pray for you", replies[0].text)

    def test_analytics_report(self):
        """Test analytics report generation."""
        # Generate a report
        report = self.manager.generate_analytics_report(
            start_date=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
            end_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        # Verify report was created
        self.assertIsNotNone(report.id)
        self.assertIsNotNone(report.generated_at)
        self.assertIn("engagement_rate", report.metrics)
        
        # Schedule a report
        scheduled_report = self.manager.schedule_analytics_report(
            frequency="weekly",
            recipients=["pastor@ibrespana.org"]
        )
        
        # Verify report was scheduled
        self.assertIsNotNone(scheduled_report.id)
        self.assertEqual(scheduled_report.frequency, "weekly")
        self.assertEqual(scheduled_report.recipients, ["pastor@ibrespana.org"])

    def test_outreach_campaign(self):
        """Test outreach campaign functionality."""
        # Create a campaign
        campaign = self.manager.create_outreach_campaign(
            name="Easter Outreach",
            target_audience="Christian youth in Madrid",
            message_template="Join us for Easter celebration at IBR España! {custom_message}"
        )
        
        # Add leads to campaign
        self.manager.add_outreach_lead(
            campaign_id=campaign.id,
            username="youth_ministry",
            custom_message="We have special youth activities."
        )
        
        # Verify lead was added
        leads = self.manager.get_outreach_leads(campaign.id)
        self.assertEqual(len(leads), 1)
        self.assertEqual(leads[0].username, "youth_ministry")

    def test_livestream_monitoring(self):
        """Test livestream monitoring functionality."""
        # Start monitoring a livestream
        stream = self.manager.start_livestream_monitoring(
            stream_id="easter_service_2023",
            notification_email="tech@ibrespana.org"
        )
        
        # Verify monitoring was started
        self.assertTrue(stream.is_monitoring)
        
        # Add a comment to the livestream
        comment = self.manager.add_livestream_comment(
            stream_id=stream.id,
            username="viewer123",
            text="The audio is cutting out.",
            comment_id="live_comment1"
        )
        
        # Verify comment was added and flagged as technical issue
        self.assertTrue(self.manager.is_technical_issue(comment.text))
        
        # Stop monitoring
        self.manager.stop_livestream_monitoring(stream.id)
        
        # Verify monitoring was stopped
        updated_stream = self.manager.get_livestream(stream.id)
        self.assertFalse(updated_stream.is_monitoring)

if __name__ == "__main__":
    unittest.main() 