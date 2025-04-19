#!/usr/bin/env python3
"""
Tests for the Instagram API integration with the InstagramManager.
This test suite uses mocks to simulate the Instagram API responses.
"""

import unittest
from unittest import mock
import json
import os
import sys
from pathlib import Path
import shutil
import tempfile
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from micro_modules.instagram_manager import InstagramManager
from micro_modules.instagram_api import InstagramAPI

# Mock API responses
MOCK_API_CONFIG = {
    "access_token": "mock_access_token",
    "user_id": "17841123456789",
    "username": "ibrespana",
    "app_id": "1234567890",
    "app_secret": "mock_app_secret",
    "redirect_uri": "https://ibrespana.org/instagram-auth",
    "token_expiration": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
}

MOCK_API_STATUS = {
    "status": "success",
    "user_id": "17841123456789",
    "username": "ibrespana",
    "account_type": "BUSINESS",
    "media_count": 42
}

MOCK_POSTS = [
    {
        "id": "17891234567891234",
        "caption": "Servicio dominical en IBR España #iglesia #fe",
        "media_url": "https://instagram.com/p/mock_image1.jpg",
        "permalink": "https://instagram.com/p/abc123",
        "timestamp": "2023-04-25T10:00:00+0000",
        "like_count": 45,
        "comments_count": 8,
        "media_type": "IMAGE"
    },
    {
        "id": "17891234567891235",
        "caption": "Grupo de jóvenes #juventud #cristo",
        "media_url": "https://instagram.com/p/mock_image2.jpg",
        "permalink": "https://instagram.com/p/def456",
        "timestamp": "2023-04-20T18:30:00+0000",
        "like_count": 72,
        "comments_count": 12,
        "media_type": "CAROUSEL_ALBUM"
    }
]

MOCK_COMMENTS = [
    {
        "id": "17891234567000001",
        "text": "¡Amén! Excelente mensaje.",
        "username": "usuario_fiel",
        "timestamp": "2023-04-25T11:05:00+0000",
        "replies": {
            "data": [
                {
                    "id": "17891234567000002",
                    "text": "Gracias por acompañarnos!",
                    "username": "ibrespana",
                    "timestamp": "2023-04-25T11:30:00+0000"
                }
            ]
        }
    },
    {
        "id": "17891234567000003",
        "text": "¿A qué hora es el servicio de oración?",
        "username": "nuevo_miembro",
        "timestamp": "2023-04-25T12:15:00+0000"
    }
]

MOCK_INSIGHTS = {
    "insights": [
        {
            "name": "impressions",
            "period": "day",
            "values": [
                {
                    "value": 1250,
                    "end_time": "2023-04-25T07:00:00+0000"
                }
            ]
        },
        {
            "name": "reach",
            "period": "day",
            "values": [
                {
                    "value": 980,
                    "end_time": "2023-04-25T07:00:00+0000"
                }
            ]
        },
        {
            "name": "follower_count",
            "period": "lifetime",
            "values": [
                {
                    "value": 1500,
                    "end_time": "2023-04-25T07:00:00+0000"
                }
            ]
        }
    ]
}

class MockResponse:
    """Mock response object for requests"""
    def __init__(self, data, status_code=200):
        self.data = data
        self.status_code = status_code
        
    def json(self):
        return self.data

class TestInstagramAPIIntegration(unittest.TestCase):
    """Test cases for Instagram API integration with InstagramManager."""

    def setUp(self):
        """Set up test environment with mocked API."""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        
        # Create mock API config file
        self.config_dir = Path(self.test_dir) / "instagram_manager"
        self.config_dir.mkdir(exist_ok=True, parents=True)
        self.config_file = self.config_dir / "api_config.json"
        with open(self.config_file, "w") as f:
            json.dump(MOCK_API_CONFIG, f)
        
        # Set up patches
        self.api_patch = mock.patch('micro_modules.instagram_api.InstagramAPI')
        self.mock_api = self.api_patch.start()
        
        # Create instance with mocked API
        self.manager = InstagramManager(data_dir=self.test_dir, account_name="ibrespana")
        
        # Set up the mock API on the manager
        self.mock_api_instance = mock.MagicMock()
        self.manager.api = self.mock_api_instance
        
        # Set up common mock responses
        self.mock_api_instance.check_api_connection.return_value = MOCK_API_STATUS
        self.mock_api_instance.get_recent_posts.return_value = MOCK_POSTS
        self.mock_api_instance.get_post_comments.return_value = MOCK_COMMENTS
        self.mock_api_instance.get_insights.return_value = {"status": "success", "insights": MOCK_INSIGHTS["insights"]}

    def tearDown(self):
        """Clean up test environment."""
        # Stop patching
        self.api_patch.stop()
        
        # Remove temporary directory
        shutil.rmtree(self.test_dir)

    def test_api_initialization(self):
        """Test API initialization."""
        # Create a new manager to test initialization
        with mock.patch('micro_modules.instagram_manager.InstagramAPI') as mock_api_class:
            mock_api_instance = mock.MagicMock()
            mock_api_class.return_value = mock_api_instance
            mock_api_instance.check_api_connection.return_value = MOCK_API_STATUS
            
            manager = InstagramManager(data_dir=self.test_dir, account_name="ibrespana")
            
            # Verify API was initialized
            mock_api_class.assert_called_once()
            mock_api_instance.check_api_connection.assert_called_once()
            self.assertEqual(manager.account_name, "ibrespana")

    def test_fetch_recent_posts(self):
        """Test fetching recent posts from API."""
        posts = self.manager.fetch_recent_posts(limit=5)
        
        # Verify API was called correctly
        self.mock_api_instance.get_recent_posts.assert_called_once_with(5)
        
        # Verify posts were parsed correctly
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0].caption, "Servicio dominical en IBR España #iglesia #fe")
        self.assertEqual(posts[0].likes, 45)
        self.assertEqual(posts[0].comments_count, 8)
        self.assertEqual(posts[1].media_type, "CAROUSEL_ALBUM")

    def test_fetch_post_comments(self):
        """Test fetching comments from API."""
        comments = self.manager.fetch_post_comments(post_id="17891234567891234", limit=10)
        
        # Verify API was called correctly
        self.mock_api_instance.get_post_comments.assert_called_once_with("17891234567891234", 10)
        
        # Verify comments were parsed correctly
        self.assertEqual(len(comments), 3)  # 2 top-level comments + 1 reply
        self.assertEqual(comments[0].username, "usuario_fiel")
        self.assertEqual(comments[0].text, "¡Amén! Excelente mensaje.")
        
        # Verify reply was parsed correctly
        reply = next((c for c in comments if c.parent_id is not None), None)
        self.assertIsNotNone(reply)
        self.assertEqual(reply.username, "ibrespana")
        self.assertEqual(reply.text, "Gracias por acompañarnos!")

    def test_add_comment_to_api(self):
        """Test adding a comment via API."""
        self.mock_api_instance.create_comment.return_value = {
            "status": "success", 
            "comment_id": "17891234567000004"
        }
        
        result = self.manager.add_comment_to_api(
            post_id="17891234567891234",
            comment_text="Gracias por tu comentario!"
        )
        
        # Verify API was called correctly
        self.mock_api_instance.create_comment.assert_called_once_with(
            "17891234567891234",
            "Gracias por tu comentario!"
        )
        
        # Verify result was handled correctly
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["comment_id"], "17891234567000004")

    def test_hide_comment_via_api(self):
        """Test hiding a comment via API."""
        self.mock_api_instance.hide_comment.return_value = {"status": "success"}
        
        result = self.manager.hide_comment_via_api(
            comment_id="17891234567000003",
            hide=True
        )
        
        # Verify API was called correctly
        self.mock_api_instance.hide_comment.assert_called_once_with(
            "17891234567000003",
            True
        )
        
        # Verify result was handled correctly
        self.assertEqual(result["status"], "success")

    def test_publish_post_immediately(self):
        """Test publishing a post immediately via API."""
        self.mock_api_instance.publish_post.return_value = {
            "status": "success",
            "post_id": "17891234567891236",
            "permalink": "https://instagram.com/p/ghi789"
        }
        
        self.mock_api_instance.create_comment.return_value = {
            "status": "success",
            "comment_id": "17891234567000005"
        }
        
        post = self.manager.schedule_post(
            image_path="https://example.com/test_image.jpg",
            caption="Test post via API",
            scheduled_time=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
            first_comment="#testing #api #integration",
            publish_immediately=True
        )
        
        # Verify API was called correctly
        self.mock_api_instance.publish_post.assert_called_once_with(
            "https://example.com/test_image.jpg",
            "Test post via API"
        )
        
        # Verify post status was updated
        self.assertEqual(post.status, "posted")
        self.assertIsNotNone(post.posted_at)
        
        # Verify first comment was added
        self.mock_api_instance.create_comment.assert_called_once()
        args, _ = self.mock_api_instance.create_comment.call_args
        self.assertEqual(args[0], "17891234567891236")
        self.assertEqual(args[1], "#testing #api #integration")

    def test_process_scheduled_posts(self):
        """Test processing scheduled posts via API."""
        # Set up responses for publishing
        self.mock_api_instance.publish_post.return_value = {
            "status": "success",
            "post_id": "17891234567891237",
            "permalink": "https://instagram.com/p/jkl012"
        }
        
        # Schedule a post in the past
        yesterday = datetime.now() - timedelta(days=1)
        self.manager.schedule_post(
            image_path="https://example.com/past_image.jpg",
            caption="Past scheduled post",
            scheduled_time=yesterday.strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Process scheduled posts
        count = self.manager.process_scheduled_posts()
        
        # Verify API was called correctly
        self.mock_api_instance.publish_post.assert_called_once_with(
            "https://example.com/past_image.jpg",
            "Past scheduled post"
        )
        
        # Verify count of published posts
        self.assertEqual(count, 1)
        
        # Verify scheduled posts list is empty
        self.assertEqual(len(self.manager.scheduled_posts), 0)
        
        # Verify post was moved to published posts
        self.assertEqual(len(self.manager.published_posts), 1)
        self.assertEqual(self.manager.published_posts[0].caption, "Past scheduled post")
        self.assertEqual(self.manager.published_posts[0].status, "posted")

    def test_enhanced_analytics_report(self):
        """Test analytics report enhanced with API data."""
        # Generate a report
        report = self.manager.generate_analytics_report(
            start_date=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
            end_date=datetime.now().strftime("%Y-%m-%d")
        )
        
        # Verify API was called correctly
        self.mock_api_instance.get_insights.assert_called_once()
        
        # Verify metrics were enhanced with API data
        self.assertEqual(report.metrics["followers_count"], 1500)
        self.assertEqual(report.metrics["impressions"], 1250)
        self.assertEqual(report.metrics["reach"], 980)

    def test_api_error_handling(self):
        """Test error handling in API integration."""
        # Make API methods raise exceptions
        self.mock_api_instance.get_recent_posts.side_effect = Exception("API timeout")
        
        # Verify error handling in fetch_recent_posts
        posts = self.manager.fetch_recent_posts()
        self.assertEqual(len(posts), 0)  # Should return empty list on error
        
        # Test API error in publishing
        self.mock_api_instance.publish_post.side_effect = Exception("Publishing failed")
        
        # Schedule and attempt to publish immediately
        post = self.manager.schedule_post(
            image_path="https://example.com/error_image.jpg",
            caption="Post with error",
            scheduled_time=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
            publish_immediately=True
        )
        
        # Verify post was scheduled despite API error
        self.assertEqual(post.status, "scheduled")
        self.assertEqual(len(self.manager.scheduled_posts), 1)

    def test_api_reconnection(self):
        """Test API reconnection functionality."""
        # Set up reconnection mock
        self.mock_api_instance.check_api_connection.return_value = {
            "status": "success", 
            "username": "ibrespana_reconnected"
        }
        
        # Test reconnection
        result = self.manager.reconnect_api()
        
        # Verify result
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["username"], "ibrespana_reconnected")

if __name__ == "__main__":
    unittest.main() 