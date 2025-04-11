#!/usr/bin/env python3

"""
Instagram Graph API Integration Module

This module provides a comprehensive interface for interacting with the Instagram Graph API,
including functionality for managing posts, comments, insights, and authentication.

Features:
- Robust configuration management using Pydantic
- Automatic token refresh handling
- Rate limiting and request throttling
- Comprehensive error handling and logging
- Type hints and data validation
- Metrics collection and insights retrieval
"""

import os
import time
import json
import logging
from typing import Dict, List, Optional, Union, Any, cast, Protocol, TypeVar, Mapping, Type, TypedDict
from datetime import datetime, timedelta
from pathlib import Path
from logging import Logger
from functools import wraps
from dataclasses import dataclass
from collections.abc import Sized
from abc import ABC, abstractmethod

import requests
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential
from pythonjsonlogger import jsonlogger

# Configure logging
logger = logging.getLogger(__name__)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Base classes and type definitions
class BaseConfig(ABC):
    """Abstract base configuration class."""
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        pass

    @abstractmethod
    def __getitem__(self, key: str) -> Any:
        pass

# Type definitions
ConfigDict = Dict[str, Any]

@dataclass
class DictConfig:
    """Wrapper class for configuration dictionary with safe access methods."""
    _config: ConfigDict

    def __init__(self, config_dict: Optional[ConfigDict] = None) -> None:
        """Initialize with a configuration dictionary."""
        self._config = config_dict if config_dict is not None else {}

    def get(self, key: str, default: Any = None) -> Any:
        """Safely get a value from the config dictionary."""
        return self._config.get(key, default)

    def get_dict(self) -> ConfigDict:
        """Return the underlying configuration dictionary."""
        return self._config

    def __getitem__(self, key: str) -> Any:
        """Allow dictionary-style access to configuration."""
        return self._config.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Allow dictionary-style setting of configuration values."""
        self._config[key] = value

    def __contains__(self, key: str) -> bool:
        """Support 'in' operator for checking key existence."""
        return key in self._config

@dataclass
class InstagramAPIConfig:
    """Configuration class for Instagram API."""
    access_token: str
    client_id: str
    client_secret: str
    page_id: str
    instagram_account_id: str
    api_version: str = "v18.0"
    base_url: str = "https://graph.facebook.com"
    token_refresh_threshold: int = Field(default=3600, description="Seconds before token expiry to trigger refresh")
    rate_limit_calls: int = Field(default=200, description="Maximum API calls per hour")
    rate_limit_window: int = Field(default=3600, description="Time window for rate limiting in seconds")
    retry_attempts: int = Field(default=3, description="Number of retry attempts for failed requests")
    retry_backoff_factor: float = Field(default=2.0, description="Exponential backoff factor for retries")

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

class RateLimiter:
    """Rate limiter implementation using token bucket algorithm."""
    def __init__(self, calls: int, window: int):
        self.calls = calls
        self.window = window
        self.tokens = calls
        self.last_update = time.time()

    def acquire(self) -> bool:
        now = time.time()
        time_passed = now - self.last_update
        self.tokens = min(self.calls, self.tokens + time_passed * (self.calls / self.window))
        self.last_update = now

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

class InsightData(BaseModel):
    """Model for Instagram insights data."""
    metric: str
    value: Union[int, float]
    end_time: Optional[datetime]
    period: Optional[str]

class HasLength(Protocol):
    def __len__(self) -> int: ...

T = TypeVar('T')

@dataclass
class APIResponse:
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def __len__(self) -> int:
        return len(self.data) if self.data else 0

    def __getitem__(self, key: str) -> Any:
        if self.data is None:
            raise KeyError(f"No data available to access key {key}")
        return self.data[key]

def rate_limit_decorator(func):
    """Decorator to implement rate limiting for API calls."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.rate_limiter.acquire():
            wait_time = self.config.rate_limit_window / self.config.rate_limit_calls
            logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds.")
            time.sleep(wait_time)
        return func(self, *args, **kwargs)
    return wrapper

# Define type variables
ConfigType = TypeVar('ConfigType', bound='BaseConfig')

class InstagramAPI:
    """
    Instagram Graph API client implementation with advanced features.
    
    Features:
    - Automatic token refresh
    - Rate limiting
    - Request retry logic
    - Comprehensive error handling
    - Metrics collection
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None, logger: Optional[Logger] = None) -> None:
        """
        Initialize the Instagram API client.
        
        Args:
            config: Configuration dictionary containing API settings
            logger: Custom logger instance
        """
        self.config = config or {}
        self.logger = logger or logging.getLogger(__name__)
        self.session = requests.Session()
        self._access_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None
        self._base_url = f"{self.config.get('base_url', 'https://graph.facebook.com')}/{self.config.get('api_version', 'v18.0')}"
        
        # Initialize rate limiter with defaults if not provided
        rate_limit_calls = int(self.config.get('rate_limit_calls', 200))
        rate_limit_window = int(self.config.get('rate_limit_window', 3600))
        self.rate_limiter = RateLimiter(rate_limit_calls, rate_limit_window)
        
        self._setup_session()
        self._check_token()

    def _setup_session(self):
        """Configure the requests session with default headers and timeout."""
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "Instagram-Python-Client/1.0"
        })
        # Set timeout using a tuple (connect timeout, read timeout)
        setattr(self.session, 'timeout', (5, 30))

    def _check_token(self) -> bool:
        """Check if access token exists and is valid."""
        if not self.config:
            self.logger.error("No configuration provided")
            return False
            
        if 'access_token' not in self.config:
            self.logger.error("No access token found in configuration")
            return False
            
        return True

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """Make a request to the Instagram API."""
        if not self._check_token():
            return APIResponse(success=False, error="No valid access token")

        url = f"{self._base_url}/{endpoint}"
        request_params = {'access_token': self._access_token}
        if params:
            request_params.update(params)

        try:
            response = self.session.request(
                method,
                url,
                params=request_params,
                json=data,
                files=files
            )
            response.raise_for_status()
            return APIResponse(success=True, data=response.json())
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            return APIResponse(success=False, error=str(e))

    def _check_token_expiry(self) -> None:
        """
        Check if the access token is about to expire and refresh it if needed.
        """
        if not self._token_expiry:
            self.refresh_token()
            return

        time_until_expiry = self._token_expiry - datetime.now()
        if time_until_expiry.days < 7:  # Refresh token if less than 7 days until expiry
            self.refresh_token()

    def refresh_token(self) -> APIResponse:
        """Refresh the long-lived access token before it expires."""
        if not self._check_token():
            return APIResponse(success=False, error="No valid access token")
            
        try:
            response = self._make_request(
                "GET",
                "oauth/access_token",
                params={
                    "grant_type": "fb_exchange_token",
                    "client_id": self.config.get('page_id', ''),
                    "client_secret": self.config.get('access_token', ''),
                    "fb_exchange_token": self.config.get('access_token', '')
                }
            )
            
            if response.success and isinstance(response.data, dict) and "access_token" in response.data:
                self.config['access_token'] = response.data["access_token"]
                # Set token expiry to 60 days from now
                self._token_expiry = datetime.now() + timedelta(days=60)
                return APIResponse(success=True, data={"message": "Token refreshed successfully"})
            
            return APIResponse(
                success=False,
                error="Failed to refresh token: Invalid response"
            )
        except Exception as e:
            error_msg = f"Failed to refresh token: {str(e)}"
            self.logger.error(error_msg)
            return APIResponse(success=False, error=error_msg)

    def get_recent_posts(self, limit: int = 10) -> APIResponse:
        """
        Retrieve recent Instagram posts.
        
        Args:
            limit: Maximum number of posts to retrieve
            
        Returns:
            APIResponse containing list of recent posts
        """
        return self._make_request(
            "GET",
            f"{self.config['instagram_account_id']}/media",
            params={"limit": limit, "fields": "id,caption,media_type,media_url,permalink,timestamp"}
        )

    def publish_post(
        self,
        media_type: str,
        media_url: str,
        caption: Optional[str] = None,
        location_id: Optional[str] = None
    ) -> APIResponse:
        """
        Publish a new post to Instagram.
        
        Args:
            media_type: Type of media (IMAGE, VIDEO, CAROUSEL)
            media_url: URL of the media to post
            caption: Post caption
            location_id: Instagram location ID
            
        Returns:
            APIResponse containing the published post data
        """
        data = {
            "media_type": media_type,
            "image_url" if media_type == "IMAGE" else "video_url": media_url
        }
        
        if caption:
            data["caption"] = caption
        if location_id:
            data["location_id"] = location_id
            
        return self._make_request(
            "POST",
            f"{self.config['instagram_account_id']}/media",
            data=data
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @rate_limit_decorator
    def get_insights(
        self,
        metrics: Optional[List[str]] = None,
        period: str = "day",
        since: Optional[datetime] = None,
        until: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get insights data for the Instagram Business Account.
        
        Args:
            metrics: List of metrics to retrieve. Defaults to ["engagement", "impressions", "reach"]
            period: Time period for metrics (day, week, month)
            since: Start date for metrics
            until: End date for metrics
            
        Returns:
            Dictionary containing insights data
        """
        if not self._check_token():
            return {"status": "error", "message": "No valid access token"}

        if metrics is None:
            metrics = ["engagement", "impressions", "reach"]
            
        params: Dict[str, str] = {
            "metric": ",".join(metrics),
            "period": period
        }
        
        if since:
            params["since"] = str(int(since.timestamp()))
        if until:
            params["until"] = str(int(until.timestamp()))
            
        endpoint = f"{self.config['instagram_account_id']}/insights"
        response = self._make_request("GET", endpoint, params=params)
        
        if not response.success or not response.data:
            self.logger.error("Failed to retrieve insights", extra={"error": response.error})
            return {"status": "error", "message": response.error or "Failed to retrieve insights"}
            
        return {"status": "success", "data": response.data}

    def manage_comments(
        self,
        media_id: str,
        action: str,
        comment_id: Optional[str] = None,
        message: Optional[str] = None
    ) -> APIResponse:
        """
        Manage comments on a post (create, reply, hide, delete).
        
        Args:
            media_id: ID of the media
            action: Action to perform (create, reply, hide, delete)
            comment_id: ID of the comment (for reply, hide, delete)
            message: Comment message (for create, reply)
            
        Returns:
            APIResponse containing the result of the comment operation
        """
        if action == "create":
            return self._make_request(
                "POST",
                f"{media_id}/comments",
                data={"message": message}
            )
        elif action == "reply" and comment_id and message:
            return self._make_request(
                "POST",
                f"{comment_id}/replies",
                data={"message": message}
            )
        elif action == "hide" and comment_id:
            return self._make_request(
                "POST",
                f"{comment_id}",
                data={"hide": True}
            )
        elif action == "delete" and comment_id:
            return self._make_request(
                "DELETE",
                f"{comment_id}"
            )
        else:
            return APIResponse(success=False, error="Invalid comment management parameters")

    def schedule_post(
        self,
        media_id: str,
        publish_time: datetime
    ) -> APIResponse:
        """
        Schedule a post for future publication.
        
        Args:
            media_id: ID of the media to schedule
            publish_time: Datetime when the post should be published
            
        Returns:
            APIResponse containing the scheduling result
        """
        return self._make_request(
            "POST",
            f"{self.config['instagram_account_id']}/media_publish",
            data={
                "creation_id": media_id,
                "publish_time": int(publish_time.timestamp())
            }
        )

    def get_media_insights(self, media_id: str, metrics: Optional[List[str]] = None) -> APIResponse:
        """
        Get insights for a specific media post.
        
        Args:
            media_id: The ID of the media to get insights for
            metrics: List of metrics to retrieve. Defaults to ["engagement", "impressions", "reach"]
        """
        if metrics is None:
            metrics = ["engagement", "impressions", "reach"]
            
        try:
            response = self._make_request(
                "GET",
                f"{media_id}/insights",
                params={
                    "metric": ",".join(metrics),
                    "period": "lifetime"
                }
            )
            return response
        except Exception as e:
            error_msg = f"Failed to get media insights: {str(e)}"
            self.logger.error(error_msg)
            return APIResponse(success=False, error=error_msg)

    def __del__(self):
        """Cleanup method to close the session."""
        if hasattr(self, 'session'):
            self.session.close()

    def check_api_connection(self) -> APIResponse:
        """Check if the API connection is working."""
        if not self._check_token():
            return APIResponse(success=False, error="No valid access token")
            
        try:
            response = self._make_request(
                "GET",
                f"{self.config['instagram_account_id']}",
                params={"fields": "id,username"}
            )
            if response.success:
                return APIResponse(success=True, data={"message": "API connection successful"})
            return APIResponse(success=False, error="Failed to connect to Instagram API")
        except Exception as e:
            error_msg = f"API connection check failed: {str(e)}"
            self.logger.error(error_msg)
            return APIResponse(success=False, error=error_msg)

    def get_post_insights(self, post_id: str, metrics: Optional[List[str]] = None) -> APIResponse:
        """Get insights for a specific post."""
        if not metrics:
            metrics = ["engagement", "impressions", "reach"]
        
        if not self._check_token():
            return APIResponse(success=False, error="No valid access token")
        
        try:
            response = self._make_request(
                "GET",
                f"{post_id}/insights",
                params={"metric": ",".join(metrics)},
                config=self.config
            )
            if isinstance(response, dict):
                return APIResponse(success=True, data=response)
            return response
        except Exception as e:
            error_msg = f"Failed to get post insights: {str(e)}"
            self.logger.error(error_msg)
            return APIResponse(success=False, error=error_msg)

# For testing purposes
if __name__ == "__main__":
    api = InstagramAPI()
    connection_status = api.check_api_connection()
    print(f"API Connection: {connection_status['status']}")
    
    if connection_status["status"] == "success":
        print(f"Connected to Instagram account: @{connection_status['username']}")
        
        # Test getting recent posts
        posts = api.get_recent_posts(limit=3)
        print(f"Retrieved {len(posts)} recent posts")
        
        # Test getting insights
        insights = api.get_insights()
        print(f"Account insights: {insights['status']}") 