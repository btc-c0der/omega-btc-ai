#!/usr/bin/env python3
"""
LUCAS SILVEIRA - PRO SURFER WELCOME PACK
XYKØ LINE SURFER - Example Usage

This script demonstrates how to use the Lucas Silveira Pro Surfer Welcome Pack.
"""

import os
import sys
import logging

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("example_usage")

try:
    # Import the main app
    from surf_tracker import SurfTrackerApp
    
    # Import individual components
    from config.social_tracker import SocialMediaTracker
    from config.youtube_monitor import YouTubeMonitor
    from config.manager_coach_module import LucasManagerCoachModule
    from config.florian_style_analyzer import FlorianopolisStyleAnalyzer
    
    logger.info("Successfully imported all modules")
except ImportError as e:
    logger.error(f"Error importing modules: {e}")
    print(f"Error importing modules: {e}")
    print("Please make sure you have installed all required dependencies.")
    sys.exit(1)

def example_social_tracker():
    """Example of using the social media tracker."""
    print("\n" + "="*80)
    print("  SOCIAL MEDIA TRACKER EXAMPLE  ")
    print("="*80)
    
    tracker = SocialMediaTracker()
    
    # Get Instagram stats
    instagram = tracker.get_platform_stats("instagram")
    print(f"Instagram Followers: {instagram['metrics']['followers']:,}")
    print(f"Instagram Engagement Rate: {instagram['metrics']['engagement_rate']}%")
    
    # Get location insights for a specific location
    location = "Guarda do Embaú"
    insights = tracker.get_surf_location_insights(location)
    print(f"\n{location} Insights:")
    print(f"  Posts: {insights[location]['posts']}")
    print(f"  Engagement: {insights[location]['engagement']:,}")
    print(f"  Sentiment: {insights[location]['sentiment']}/100")

def example_youtube_monitor():
    """Example of using the YouTube monitor."""
    print("\n" + "="*80)
    print("  YOUTUBE MONITOR EXAMPLE  ")
    print("="*80)
    
    monitor = YouTubeMonitor()
    
    # Get basic channel stats
    stats = monitor.get_channel_stats()
    print(f"Channel: {stats['channel_id']}")
    print(f"Subscribers: {stats['metrics']['subscribers']:,}")
    print(f"Videos: {stats['metrics']['videos_count']}")
    
    # Get recent video performance
    performance = monitor.get_video_performance("recent")
    if performance['videos_count'] > 0:
        print("\nRecent Performance:")
        print(f"  Videos: {performance['videos_count']}")
        print(f"  Average Views: {performance['metrics']['avg_views']:,.0f}")
        print(f"  Top Video: {performance.get('top_video', {}).get('title', 'N/A')}")

def example_manager_coach():
    """Example of using the manager coach module."""
    print("\n" + "="*80)
    print("  MANAGER COACH MODULE EXAMPLE  ")
    print("="*80)
    
    coach = LucasManagerCoachModule()
    
    # Get basic dashboard
    dashboard = coach.get_dashboard_summary()
    
    # Show next competition
    if dashboard["next_competition"]:
        comp = dashboard["next_competition"]
        print(f"Next Competition: {comp['name']} in {dashboard['days_to_next_competition']} days")
        print(f"Location: {comp['location']}")
        print(f"Preparation: {comp['preparation_status']}%")
    
    # Show recommendations
    print("\nCoach Recommendations:")
    recommendations = coach.get_preparation_recommendations()
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"{i}. {rec}")

def example_style_analyzer():
    """Example of using the Florianopolis style analyzer."""
    print("\n" + "="*80)
    print("  FLORIANOPOLIS STYLE ANALYZER EXAMPLE  ")
    print("="*80)
    
    analyzer = FlorianopolisStyleAnalyzer()
    
    # Get style assessment
    assessment = analyzer.get_style_assessment()
    print(f"Overall Rating: {assessment['overall_rating']}/10")
    print(f"Strongest Aspect: {assessment['strongest_aspect']['name']} ({assessment['strongest_aspect']['rating']}/10)")
    
    # Get improvement plan for tube riding
    focus = "tube_riding"
    plan = analyzer.get_improvement_plan(focus)
    print(f"\nImprovement Focus: {plan['focus_aspect']}")
    print(f"Current Rating: {plan['current_rating']}/10")
    print(f"Expected after {plan['duration_weeks']} weeks: {plan['expected_improvement']}/10")
    
    # Get spot recommendations
    print("\nSpot Recommendations for Today's Conditions:")
    conditions = {
        "swell_direction": "S", 
        "wind_direction": "NW", 
        "swell_size": "4-6ft"
    }
    spots = analyzer.get_spot_recommendations(conditions)
    for i, spot in enumerate(spots[:2], 1):
        print(f"{i}. {spot['spot']} (Match Score: {spot['match_score']})")

def example_full_app():
    """Example of using the full application."""
    print("\n" + "="*80)
    print("  FULL APPLICATION EXAMPLE  ")
    print("="*80)
    
    app = SurfTrackerApp()
    
    # Show dashboard (overview of all components)
    print("Launching full dashboard...")
    print("Note: In a real terminal, this would show the complete dashboard")
    print("Run the actual surf_tracker.py script for the full experience")

def main():
    """Run all example functions."""
    print("\n🏄‍♂️ LUCAS SILVEIRA PRO SURFER WELCOME PACK - XYKØ LINE SURFER 🏄‍♂️")
    print("Example Usage Guide\n")
    
    example_social_tracker()
    example_youtube_monitor()
    example_manager_coach()
    example_style_analyzer()
    example_full_app()
    
    print("\n" + "="*80)
    print("For full functionality, run the main application:")
    print("python surf_tracker.py")
    print("")
    print("Or run a specific component:")
    print("python surf_tracker.py --component social")
    print("python surf_tracker.py --component youtube")
    print("python surf_tracker.py --component coach")
    print("python surf_tracker.py --component style")
    print("="*80 + "\n")

if __name__ == "__main__":
    main() 