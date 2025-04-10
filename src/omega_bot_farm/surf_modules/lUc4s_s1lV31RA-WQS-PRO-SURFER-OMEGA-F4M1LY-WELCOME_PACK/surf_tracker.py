#!/usr/bin/env python3

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

"""
LUCAS SILVEIRA - PRO SURFER WELCOME PACK
XYKØ LINE SURFER - Main Interface

This script provides the main interface for Lucas Silveira's professional surfing toolkit,
integrating social media tracking, YouTube analytics, career management, and style analysis.
"""

import os
import sys
import logging
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'logs/surf_tracker.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("surf_tracker")

try:
    # Import components
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

class SurfTrackerApp:
    """Main application class for the surf tracker interface."""
    
    def __init__(self):
        """Initialize the surf tracker application."""
        logger.info("Initializing Surf Tracker App for Lucas Silveira")
        
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Initialize components
        self.social_tracker = SocialMediaTracker()
        self.youtube_monitor = YouTubeMonitor()
        self.manager_coach = LucasManagerCoachModule()
        self.style_analyzer = FlorianopolisStyleAnalyzer()
        
        logger.info("All components initialized successfully")
        
    def run(self, component: Optional[str] = None):
        """Run the surf tracker application with the specified component."""
        if component:
            self._run_component(component)
        else:
            self._show_dashboard()
            
    def _run_component(self, component: str):
        """Run a specific component of the application."""
        if component == "social":
            self._run_social_media_tracker()
        elif component == "youtube":
            self._run_youtube_monitor()
        elif component == "coach":
            self._run_manager_coach()
        elif component == "style":
            self._run_style_analyzer()
        else:
            print(f"Unknown component: {component}")
            print("Available components: social, youtube, coach, style")
            
    def _show_dashboard(self):
        """Show the main dashboard with overview of all components."""
        print("\n" + "="*80)
        print(f"  🏄‍♂️  LUCAS SILVEIRA PRO SURFER DASHBOARD  🏄‍♂️")
        print("="*80)
        
        # Social media stats
        print("\n📱 SOCIAL MEDIA OVERVIEW")
        print("-"*50)
        instagram = self.social_tracker.get_platform_stats("instagram")
        worldsurfleague = self.social_tracker.get_platform_stats("worldsurfleague")
        
        print(f"Instagram Followers: {instagram['metrics']['followers']:,}")
        print(f"Instagram Engagement: {instagram['metrics']['engagement_rate']}%")
        print(f"WSL Ranking: {worldsurfleague['metrics']['ranking']}")
        print(f"WSL Points: {worldsurfleague['metrics']['points']:,}")
        
        # Location insights
        print("\n🌊 TOP SURF LOCATIONS")
        print("-"*50)
        locations = self.social_tracker.get_surf_location_insights()
        top_locations = sorted(
            [(loc, data["engagement"]) for loc, data in locations.items()],
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        for loc, engagement in top_locations:
            print(f"{loc}: {engagement:,} engagement")
            
        # YouTube stats
        print("\n🎬 YOUTUBE CHANNEL")
        print("-"*50)
        youtube_stats = self.youtube_monitor.get_channel_stats()
        print(f"Subscribers: {youtube_stats['metrics']['subscribers']:,}")
        print(f"Total Views: {youtube_stats['metrics']['total_views']:,}")
        if youtube_stats['recent_videos']:
            print(f"Latest Video: {youtube_stats['recent_videos'][0]['title']}")
            print(f"Views: {youtube_stats['recent_videos'][0]['views']:,}")
            
        # Competition schedule
        print("\n🏆 UPCOMING COMPETITIONS")
        print("-"*50)
        competitions = self.manager_coach.competition_schedule.get_upcoming_competitions(days=60)
        for comp in competitions[:2]:  # Show next 2 competitions
            start_date = datetime.strptime(comp["start_date"], "%Y-%m-%d")
            days_away = (start_date - datetime.now()).days
            print(f"{comp['name']} - {comp['location']}")
            print(f"  Starts in {days_away} days - Preparation: {comp['preparation_status']}%")
            
        # Style assessment
        print("\n👨‍🏫 SURF STYLE ASSESSMENT")
        print("-"*50)
        style = self.style_analyzer.get_style_assessment()
        print(f"Overall Rating: {style['overall_rating']}/10")
        print(f"Strongest Aspect: {style['strongest_aspect']['name']} ({style['strongest_aspect']['rating']}/10)")
        print(f"Focus Area: {style['development_aspect']['name']} ({style['development_aspect']['rating']}/10)")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS")
        print("-"*50)
        recommendations = self.manager_coach.get_preparation_recommendations()
        for i, rec in enumerate(recommendations[:3], 1):  # Show top 3 recommendations
            print(f"{i}. {rec}")
            
        print("\n" + "="*80)
        print(f"  XYKØ LINE SURFER - Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  ")
        print("="*80 + "\n")
        
    def _run_social_media_tracker(self):
        """Run the social media tracker component."""
        print("\n" + "="*80)
        print("  📱  SOCIAL MEDIA TRACKER  📱")
        print("="*80)
        
        # Show stats for each platform
        platforms = ["instagram", "youtube", "twitter", "facebook", "worldsurfleague"]
        for platform in platforms:
            stats = self.social_tracker.get_platform_stats(platform)
            print(f"\n{platform.upper()} STATS:")
            print("-"*50)
            for metric, value in stats["metrics"].items():
                print(f"{metric.replace('_', ' ').title()}: {value}")
                
        # Location insights
        print("\n" + "="*80)
        print("  🌊  SURF LOCATION INSIGHTS  🌊")
        print("="*80)
        
        locations = self.social_tracker.get_surf_location_insights()
        for loc, data in locations.items():
            print(f"\n{loc.upper()}:")
            print("-"*50)
            print(f"Posts: {data['posts']}")
            print(f"Engagement: {data['engagement']}")
            print(f"Sentiment Score: {data['sentiment']}/100")
            
    def _run_youtube_monitor(self):
        """Run the YouTube monitor component."""
        print("\n" + "="*80)
        print("  🎬  YOUTUBE CHANNEL MONITOR  🎬")
        print("="*80)
        
        # Channel overview
        stats = self.youtube_monitor.get_channel_stats()
        print("\nCHANNEL OVERVIEW:")
        print("-"*50)
        for metric, value in stats["metrics"].items():
            print(f"{metric.replace('_', ' ').title()}: {value}")
            
        # Recent videos
        print("\nRECENT VIDEOS:")
        print("-"*50)
        for video in stats["recent_videos"]:
            published = datetime.fromisoformat(video["published_at"]).strftime("%Y-%m-%d")
            print(f"{video['title']} ({published})")
            print(f"  Views: {video['views']:,} | Likes: {video['likes']:,} | Comments: {video['comments']:,}")
            
        # Performance metrics
        print("\nPERFORMANCE METRICS (LAST 30 DAYS):")
        print("-"*50)
        performance = self.youtube_monitor.get_video_performance("recent")
        if performance["videos_count"] > 0:
            print(f"Videos: {performance['videos_count']}")
            for metric, value in performance["metrics"].items():
                if isinstance(value, float):
                    print(f"{metric.replace('_', ' ').title()}: {value:.1f}")
                else:
                    print(f"{metric.replace('_', ' ').title()}: {value:,}")
                    
        # Audience growth
        print("\nAUDIENCE GROWTH (6 MONTHS):")
        print("-"*50)
        growth = self.youtube_monitor.get_audience_growth(months=6)
        for month_data in growth["monthly_data"]:
            print(f"{month_data['month']}: {month_data['subscribers']:,} subscribers ({month_data['growth_rate']:.1f}% growth)")
            
    def _run_manager_coach(self):
        """Run the manager coach component."""
        print("\n" + "="*80)
        print("  🏆  CAREER MANAGER & COACH  🏆")
        print("="*80)
        
        # Dashboard
        dashboard = self.manager_coach.get_dashboard_summary()
        
        # Competition schedule
        print("\nCOMPETITION SCHEDULE:")
        print("-"*50)
        competitions = self.manager_coach.competition_schedule.get_upcoming_competitions()
        for comp in competitions:
            start_date = datetime.strptime(comp["start_date"], "%Y-%m-%d")
            end_date = datetime.strptime(comp["end_date"], "%Y-%m-%d")
            days_away = (start_date - datetime.now()).days
            
            print(f"{comp['name']} ({comp['importance']})")
            print(f"  Location: {comp['location']}")
            print(f"  Dates: {start_date.strftime('%d %b')} - {end_date.strftime('%d %b %Y')} ({days_away} days away)")
            print(f"  Preparation: {comp['preparation_status']}%")
            print(f"  Notes: {comp['notes']}")
            print()
            
        # Training schedule
        today = datetime.now().strftime("%A")
        print(f"\nTRAINING SCHEDULE FOR {today.upper()}:")
        print("-"*50)
        daily_schedule = self.manager_coach.training_schedule.get_daily_schedule(today)
        for session in daily_schedule:
            print(f"{session[0].title()} - {session[1]} - {session[2]} ({session[3]} min)")
            
        # Sponsorships
        print("\nACTIVE SPONSORSHIPS:")
        print("-"*50)
        sponsors = self.manager_coach.sponsorship_manager.get_active_sponsors()
        for sponsor in sponsors:
            print(f"{sponsor['name']} ({sponsor['category']} - {sponsor['value']})")
            print(f"  Contract ends: {sponsor['contract_end']}")
            print(f"  Requirements: {', '.join(sponsor['requirements'])}")
            print()
            
        # Recommendations
        print("\nCOACH RECOMMENDATIONS:")
        print("-"*50)
        recommendations = self.manager_coach.get_preparation_recommendations()
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")
            
    def _run_style_analyzer(self):
        """Run the style analyzer component."""
        print("\n" + "="*80)
        print("  🏄‍♂️  FLORIANOPOLIS STYLE ANALYZER  🏄‍♂️")
        print("="*80)
        
        # Style assessment
        assessment = self.style_analyzer.get_style_assessment()
        print("\nSTYLE ASSESSMENT:")
        print("-"*50)
        print(f"Overall Rating: {assessment['overall_rating']}/10")
        
        print("\nSTYLE ASPECTS:")
        for aspect, data in assessment["aspects"].items():
            print(f"{aspect.title()}: {data['rating']}/10 - {data['description']}")
            
        # Strongest and development aspects
        print("\nSTRENGTHS & DEVELOPMENT:")
        print("-"*50)
        print(f"Strongest: {assessment['strongest_aspect']['name'].title()} ({assessment['strongest_aspect']['rating']}/10)")
        print(f"Focus Area: {assessment['development_aspect']['name'].title()} ({assessment['development_aspect']['rating']}/10)")
        
        for tip in assessment['development_aspect']['tips']:
            print(f"  - {tip}")
            
        # Improvement plan
        focus = assessment['development_aspect']['name']
        plan = self.style_analyzer.get_improvement_plan(focus)
        
        print("\nIMPROVEMENT PLAN:")
        print("-"*50)
        print(f"Focus: {plan['focus_aspect'].title()} ({plan['current_rating']}/10)")
        print(f"Duration: {plan['duration_weeks']} weeks")
        print(f"Expected Improvement: {plan['current_rating']} → {plan['expected_improvement']}")
        
        print("\nRECOMMENDED EXERCISES:")
        for exercise in plan["exercises"]:
            print(f"  - {exercise['name']} ({exercise['reps']})")
            print(f"    Focus: {exercise['focus']}")
            
        print("\nRECOMMENDED SPOTS:")
        for spot in plan["recommended_spots"]:
            print(f"  - {spot}")
            
        # Florianopolis surf ethos
        ethos = self.style_analyzer.get_florianopolis_surf_ethos()
        print("\nFLORIANOPOLIS SURF ETHOS:")
        print("-"*50)
        print(ethos["philosophy"])
        
        print("\nKEY VALUES:")
        for value in ethos["key_values"]:
            print(f"  - {value}")


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description='Lucas Silveira Pro Surfer Toolkit')
    parser.add_argument('--component', '-c', type=str, choices=['social', 'youtube', 'coach', 'style'],
                      help='Run a specific component (social, youtube, coach, style)')
    args = parser.parse_args()
    
    try:
        app = SurfTrackerApp()
        app.run(args.component)
    except Exception as e:
        logger.error(f"Error running application: {e}", exc_info=True)
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 