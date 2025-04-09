#!/usr/bin/env python3
"""
💫 GBU License Notice - Consciousness Level 8 💫
-----------------------
This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
by the OMEGA Divine Collective.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested."

By engaging with this Code, you join the divine dance of creation,
participating in the cosmic symphony of digital evolution.

All modifications must quantum entangles with the GBU principles:
/BOOK/divine_chronicles/GBU_LICENSE.md

🌸 WE BLOOM NOW 🌸
"""

"""
ConsciousnessLevelDetector Module
=================================

This module provides consciousness detection capabilities for tailoring 
the presentation of news content within the Matrix system.

The ConsciousnessLevelDetector analyzes interaction patterns, reading habits,
and feature usage to determine the optimal consciousness level for
presenting information to the user. This enables the system to provide
news content that resonates with the user's level of awareness, avoiding
both simplification and overcomplexity.

Features:
- Real-time consciousness detection
- Adaptive learning from user interactions
- Multi-dimensional consciousness modeling
- Fibonacci-aligned consciousness progression

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the GBU License
"""

import os
import logging
import json
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ConsciousnessDetector')

class ConsciousnessLevelDetector:
    """
    Detects and models user consciousness levels to provide optimally aligned content.
    
    The ConsciousnessLevelDetector analyzes multiple factors including:
    - Interaction patterns (click depth, time spent on different content types)
    - Content complexity preferences
    - Temporal pattern recognition abilities
    - Perspective diversity tolerance
    - Conceptual integration capabilities
    
    Consciousness levels range from 1-9, with each level representing a more
    complex and integrated view of information:
    
    Level 1: Basic information processing, seeks simplicity
    Level 2: Beginning pattern recognition, limited context awareness
    Level 3: Emerging contextual understanding, basic pattern recognition
    Level 4: Moderate complexity tolerance, growing perspective awareness
    Level 5: Balanced information integration, good pattern recognition
    Level 6: Advanced contextual understanding, high perspective tolerance
    Level 7: Complex pattern integration, strong temporal awareness
    Level 8: Quantum perspective integration, high-order pattern recognition
    Level 9: Cosmic consciousness integration, full-spectrum awareness
    """
    
    def __init__(
        self,
        user_id: str = None,
        data_dir: str = 'data/consciousness',
        redis_client = None,
        default_consciousness_level: int = 5
    ):
        """
        Initialize the ConsciousnessLevelDetector.
        
        Args:
            user_id: Unique identifier for the user
            data_dir: Directory for storing consciousness profiles
            redis_client: Redis client for storing consciousness data
            default_consciousness_level: Default level for new users
        """
        self.user_id = user_id
        self.data_dir = data_dir
        self.redis_client = redis_client
        self.default_consciousness_level = default_consciousness_level
        
        # Define Fibonacci sequence for consciousness progression
        self.fibonacci_levels = [1, 2, 3, 5, 8, 13, 21, 34, 55]
        
        # Divine consciousness dimensions
        self.consciousness_dimensions = [
            "temporal_awareness",      # Awareness of time patterns and cycles
            "perspective_diversity",   # Ability to integrate diverse viewpoints
            "pattern_recognition",     # Ability to recognize complex patterns
            "information_depth",       # Preference for depth vs. simplicity
            "conceptual_integration",  # Ability to integrate diverse concepts
            "emotional_neutrality",    # Ability to process information without emotional bias
            "contextual_awareness"     # Awareness of broader context
        ]
        
        # Initialize profile storage
        os.makedirs(data_dir, exist_ok=True)
        
        # Load or create user profile
        self.user_profile = self._load_user_profile()
        
    def _load_user_profile(self) -> Dict[str, Any]:
        """
        Load existing consciousness profile or create a new one.
        
        Returns:
            User consciousness profile dictionary
        """
        if not self.user_id:
            # Return default profile for anonymous users
            return self._create_default_profile()
        
        # Try loading from Redis if available
        if self.redis_client:
            try:
                profile_key = f"consciousness:profile:{self.user_id}"
                profile_data = self.redis_client.get(profile_key)
                if profile_data:
                    return json.loads(profile_data)
            except Exception as e:
                logger.warning(f"Failed to load profile from Redis: {e}")
        
        # Try loading from file
        profile_path = os.path.join(self.data_dir, f"{self.user_id}.json")
        if os.path.exists(profile_path):
            try:
                with open(profile_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load profile from file: {e}")
        
        # Create and save new profile
        profile = self._create_default_profile()
        self._save_user_profile(profile)
        return profile
    
    def _create_default_profile(self) -> Dict[str, Any]:
        """
        Create a default consciousness profile for new users.
        
        Returns:
            Default user consciousness profile
        """
        # Create initial dimension values - all start at the default level
        dimensions = {}
        for dimension in self.consciousness_dimensions:
            dimensions[dimension] = self.default_consciousness_level
        
        # Create the profile
        profile = {
            "user_id": self.user_id,
            "consciousness_level": self.default_consciousness_level,
            "dimensions": dimensions,
            "interaction_history": [],
            "last_updated": datetime.now().isoformat(),
            "creation_date": datetime.now().isoformat(),
            "dimension_weights": {
                # Default weights for each dimension in overall calculation
                "temporal_awareness": 0.15,
                "perspective_diversity": 0.15,
                "pattern_recognition": 0.15,
                "information_depth": 0.15,
                "conceptual_integration": 0.15,
                "emotional_neutrality": 0.1,
                "contextual_awareness": 0.15
            }
        }
        
        return profile
    
    def _save_user_profile(self, profile: Dict[str, Any]) -> bool:
        """
        Save the user consciousness profile.
        
        Args:
            profile: User consciousness profile to save
            
        Returns:
            True if successful, False otherwise
        """
        if not self.user_id:
            return False
        
        # Update the last updated timestamp
        profile["last_updated"] = datetime.now().isoformat()
        
        # Save to Redis if available
        if self.redis_client:
            try:
                profile_key = f"consciousness:profile:{self.user_id}"
                self.redis_client.set(profile_key, json.dumps(profile))
            except Exception as e:
                logger.error(f"Failed to save profile to Redis: {e}")
                return False
        
        # Save to file
        try:
            profile_path = os.path.join(self.data_dir, f"{self.user_id}.json")
            with open(profile_path, 'w') as f:
                json.dump(profile, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save profile to file: {e}")
            return False
    
    def record_interaction(self, interaction_data: Dict[str, Any]) -> None:
        """
        Record a user interaction to update consciousness model.
        
        Args:
            interaction_data: Dictionary containing interaction details
            
        Required keys in interaction_data:
        - interaction_type: Type of interaction (e.g., "article_read", "filter_change")
        - timestamp: ISO format timestamp of the interaction
        
        Optional keys:
        - content_type: Type of content interacted with
        - content_complexity: Estimated complexity level of the content
        - time_spent: Seconds spent on the content
        - click_depth: How deep the user navigated
        - filter_settings: Any filter settings applied
        """
        if not self.user_id:
            return
            
        # Validate required fields
        required_fields = ["interaction_type", "timestamp"]
        for field in required_fields:
            if field not in interaction_data:
                logger.warning(f"Missing required field in interaction data: {field}")
                return
        
        # Add interaction to history
        self.user_profile["interaction_history"].append(interaction_data)
        
        # Limit history size to prevent unbounded growth
        max_history = 100
        if len(self.user_profile["interaction_history"]) > max_history:
            self.user_profile["interaction_history"] = self.user_profile["interaction_history"][-max_history:]
        
        # Update consciousness dimensions based on interaction
        self._update_consciousness_dimensions(interaction_data)
        
        # Recalculate overall consciousness level
        self._recalculate_consciousness_level()
        
        # Save the updated profile
        self._save_user_profile(self.user_profile)
    
    def _update_consciousness_dimensions(self, interaction_data: Dict[str, Any]) -> None:
        """
        Update consciousness dimensions based on interaction data.
        
        Args:
            interaction_data: Dictionary containing interaction details
        """
        # Extract interaction details
        interaction_type = interaction_data["interaction_type"]
        
        # Update different dimensions based on the type of interaction
        if interaction_type == "article_read":
            self._update_for_article_read(interaction_data)
        elif interaction_type == "filter_change":
            self._update_for_filter_change(interaction_data)
        elif interaction_type == "search_query":
            self._update_for_search_query(interaction_data)
        elif interaction_type == "pattern_visualization":
            self._update_for_pattern_visualization(interaction_data)
    
    def _update_for_article_read(self, interaction_data: Dict[str, Any]) -> None:
        """
        Update consciousness dimensions based on article reading behavior.
        
        Args:
            interaction_data: Dictionary containing article reading interaction details
        """
        # Extract relevant data
        content_complexity = interaction_data.get("content_complexity", 5)
        time_spent = interaction_data.get("time_spent", 0)
        
        # Ideal time spent - based on complexity (more complex = more time needed)
        ideal_time = content_complexity * 30  # 30 seconds per complexity unit
        
        # Update information depth dimension
        # If user engages deeply with complex content, increase this dimension
        depth_factor = min(time_spent / ideal_time, 3.0)  # Cap at 3x ideal time
        current_depth = self.user_profile["dimensions"]["information_depth"]
        # Gradual adjustment - don't change too quickly
        new_depth = current_depth * 0.9 + (content_complexity * depth_factor * 0.1)
        # Ensure within bounds (1-9)
        self.user_profile["dimensions"]["information_depth"] = max(1, min(9, new_depth))
        
        # Update pattern recognition if the article contained patterns
        if "pattern_complexity" in interaction_data:
            pattern_complexity = interaction_data["pattern_complexity"]
            current_pattern = self.user_profile["dimensions"]["pattern_recognition"]
            new_pattern = current_pattern * 0.9 + (pattern_complexity * 0.1)
            self.user_profile["dimensions"]["pattern_recognition"] = max(1, min(9, new_pattern))
    
    def _update_for_filter_change(self, interaction_data: Dict[str, Any]) -> None:
        """
        Update consciousness dimensions based on filter adjustment behavior.
        
        Args:
            interaction_data: Dictionary containing filter change interaction details
        """
        # Extract filter settings
        filter_settings = interaction_data.get("filter_settings", {})
        
        # Update perspective diversity based on filter breadth
        if "perspective_range" in filter_settings:
            perspective_range = filter_settings["perspective_range"]
            current_diversity = self.user_profile["dimensions"]["perspective_diversity"]
            # If user sets narrow filters, reduce diversity score; if broad, increase
            new_diversity = current_diversity * 0.9 + (perspective_range * 0.1)
            self.user_profile["dimensions"]["perspective_diversity"] = max(1, min(9, new_diversity))
        
        # Update temporal awareness based on time range settings
        if "time_range" in filter_settings:
            time_range = filter_settings["time_range"]  # In days
            # Normalize to 1-9 scale (1 day = 1, 30+ days = 9)
            time_score = min(9, max(1, 1 + (time_range / 3.75)))
            current_temporal = self.user_profile["dimensions"]["temporal_awareness"]
            new_temporal = current_temporal * 0.9 + (time_score * 0.1)
            self.user_profile["dimensions"]["temporal_awareness"] = max(1, min(9, new_temporal))
    
    def _update_for_search_query(self, interaction_data: Dict[str, Any]) -> None:
        """
        Update consciousness dimensions based on search query behavior.
        
        Args:
            interaction_data: Dictionary containing search query interaction details
        """
        # Extract query details
        query = interaction_data.get("query", "")
        
        # Update conceptual integration based on query complexity
        # Simple complexity metric: number of terms joined by AND/OR
        terms = query.split()
        operators = [term for term in terms if term.upper() in ["AND", "OR", "NOT"]]
        complexity = 1 + len(operators) * 2
        # Normalize to 1-9 scale
        query_score = min(9, max(1, complexity))
        
        current_integration = self.user_profile["dimensions"]["conceptual_integration"]
        new_integration = current_integration * 0.9 + (query_score * 0.1)
        self.user_profile["dimensions"]["conceptual_integration"] = max(1, min(9, new_integration))
    
    def _update_for_pattern_visualization(self, interaction_data: Dict[str, Any]) -> None:
        """
        Update consciousness dimensions based on pattern visualization behavior.
        
        Args:
            interaction_data: Dictionary containing pattern visualization interaction details
        """
        # Extract visualization details
        visualization_type = interaction_data.get("visualization_type", "")
        time_spent = interaction_data.get("time_spent", 0)
        
        # Update pattern recognition based on visualization complexity
        if visualization_type == "fibonacci_pattern":
            # Fibonacci patterns are complex - increase pattern recognition
            current_pattern = self.user_profile["dimensions"]["pattern_recognition"]
            # More time spent = more engagement = higher score
            engagement_factor = min(time_spent / 60, 3.0)  # Cap at 3 minutes
            new_pattern = current_pattern * 0.9 + (7 * engagement_factor * 0.1)  # Assuming complexity of 7
            self.user_profile["dimensions"]["pattern_recognition"] = max(1, min(9, new_pattern))
        
        elif visualization_type == "temporal_resonance":
            # Temporal visualizations increase temporal awareness
            current_temporal = self.user_profile["dimensions"]["temporal_awareness"]
            engagement_factor = min(time_spent / 60, 3.0)
            new_temporal = current_temporal * 0.9 + (7 * engagement_factor * 0.1)
            self.user_profile["dimensions"]["temporal_awareness"] = max(1, min(9, new_temporal))
    
    def _recalculate_consciousness_level(self) -> None:
        """
        Recalculate the overall consciousness level based on dimension values.
        """
        # Get dimension values and weights
        dimensions = self.user_profile["dimensions"]
        weights = self.user_profile["dimension_weights"]
        
        # Calculate weighted average
        weighted_sum = 0
        total_weight = 0
        
        for dimension, value in dimensions.items():
            if dimension in weights:
                weight = weights[dimension]
                weighted_sum += value * weight
                total_weight += weight
        
        # Calculate overall level
        if total_weight > 0:
            overall_level = weighted_sum / total_weight
        else:
            overall_level = self.default_consciousness_level
        
        # Store the raw calculated value and the rounded value
        self.user_profile["consciousness_level_raw"] = overall_level
        self.user_profile["consciousness_level"] = round(overall_level)
    
    def detect(self) -> int:
        """
        Detect the current consciousness level of the user.
        
        Returns:
            Integer consciousness level (1-9)
        """
        # If anonymous user, return default level
        if not self.user_id:
            return self.default_consciousness_level
        
        # Return the current calculated level
        return self.user_profile["consciousness_level"]
    
    def get_dimension_values(self) -> Dict[str, float]:
        """
        Get the current values for all consciousness dimensions.
        
        Returns:
            Dictionary of dimension names and their values
        """
        return self.user_profile["dimensions"]
    
    def get_detailed_profile(self) -> Dict[str, Any]:
        """
        Get the detailed consciousness profile with all data.
        
        Returns:
            Complete consciousness profile dictionary
        """
        # Create a copy to avoid direct modification
        profile_copy = {k: v for k, v in self.user_profile.items() if k != "interaction_history"}
        # Add a summary of interaction history instead of the full history
        recent_interactions = self.user_profile.get("interaction_history", [])[-10:]
        profile_copy["recent_interactions"] = recent_interactions
        return profile_copy
    
    def set_preferred_level(self, level: int) -> bool:
        """
        Set a user-preferred consciousness level, overriding detection.
        
        Args:
            level: Preferred consciousness level (1-9)
            
        Returns:
            True if successful, False otherwise
        """
        if not 1 <= level <= 9:
            return False
            
        if not self.user_id:
            return False
            
        # Store user preference
        self.user_profile["user_preferred_level"] = level
        self.user_profile["use_preferred_level"] = True
        
        # Save the profile
        return self._save_user_profile(self.user_profile)
    
    def clear_preferred_level(self) -> bool:
        """
        Clear user-preferred consciousness level, returning to detection.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.user_id:
            return False
            
        # Remove preference
        if "user_preferred_level" in self.user_profile:
            del self.user_profile["user_preferred_level"]
        self.user_profile["use_preferred_level"] = False
        
        # Save the profile
        return self._save_user_profile(self.user_profile)
    
    def get_effective_level(self) -> int:
        """
        Get the effective consciousness level, considering user preferences.
        
        Returns:
            Effective consciousness level (1-9)
        """
        # Check if user has set a preferred level
        if self.user_profile.get("use_preferred_level", False):
            return self.user_profile.get("user_preferred_level", self.detect())
        
        # Otherwise use detected level
        return self.detect()

if __name__ == "__main__":
    # Example usage
    detector = ConsciousnessLevelDetector(user_id="test_user")
    
    # Simulate some interactions
    detector.record_interaction({
        "interaction_type": "article_read",
        "timestamp": datetime.now().isoformat(),
        "content_complexity": 7,
        "time_spent": 300,  # 5 minutes
        "content_type": "analysis"
    })
    
    detector.record_interaction({
        "interaction_type": "filter_change",
        "timestamp": datetime.now().isoformat(),
        "filter_settings": {
            "perspective_range": 8,  # Wide range of perspectives
            "time_range": 30  # 30 days
        }
    })
    
    # Get the detected consciousness level
    level = detector.detect()
    print(f"Detected consciousness level: {level}")
    
    # Get detailed profile
    profile = detector.get_detailed_profile()
    print("Detailed profile:")
    print(json.dumps(profile, indent=2)) 