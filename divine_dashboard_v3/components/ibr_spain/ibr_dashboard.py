#!/usr/bin/env python3

"""
IBR España Dashboard - Main Interface

This module integrates all IBR España micro modules into a unified
Gradio interface for the Divine Dashboard v3.
"""

import os
import gradio as gr
import json
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ibr_spain_dashboard.log")
    ]
)
logger = logging.getLogger("ibr_spain_dashboard")

# Ensure micro_modules directory exists before importing
current_dir = Path(__file__).parent
micro_modules_dir = current_dir / "micro_modules"
if not micro_modules_dir.exists():
    micro_modules_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created micro_modules directory at {micro_modules_dir}")

# Dynamically import micro modules
try:
    from .micro_modules.sermon_library import SermonLibrary, render_sermon_card
    from .micro_modules.prayer_requests import PrayerRequests, render_prayer_request
    from .micro_modules.church_events import ChurchEvents, render_event_card
    from .micro_modules.devotionals import Devotionals, render_devotional_card
    from .micro_modules.instagram_integration import InstagramIntegration, render_instagram_feed
    from .micro_modules.instagram_manager import InstagramManager, Post, Comment, AnalyticsReport, OutreachCampaign
    logger.info("Successfully imported all IBR España micro modules")
except ImportError as e:
    logger.error(f"Error importing micro modules: {str(e)}")
    # Create placeholder functions if imports fail
    def render_sermon_card(sermon: Dict[str, Any]) -> str:
        return f"<div class='sermon-card'>Sermon: {sermon.get('title', 'Unknown')}</div>"
    
    def render_prayer_request(prayer: Dict[str, Any]) -> str:
        return f"<div class='prayer-card'>Prayer: {prayer.get('title', 'Unknown')}</div>"
    
    def render_event_card(event: Dict[str, Any]) -> str:
        return f"<div class='event-card'>Event: {event.get('title', 'Unknown')}</div>"
    
    def render_devotional_card(devotional: Dict[str, Any]) -> str:
        return f"<div class='devotional-card'>Devotional: {devotional.get('title', 'Unknown')}</div>"
    
    def render_instagram_feed(posts: List[Dict[str, Any]]) -> str:
        return "<div class='instagram-feed'>Instagram feed placeholder</div>"

# Language support
LANGUAGES = {
    "es": "Español",
    "ca": "Català",
    "en": "English"
}

def get_sample_sermons() -> List[Dict[str, Any]]:
    """Get sample sermon data (in production, would fetch from API)"""
    return [
        {
            "id": "sermon001",
            "title": "La Gracia de Dios en Tiempos Difíciles",
            "preacher": "Pastor Juan Martínez",
            "date": "2023-10-22",
            "duration": "45:30",
            "scripture": "Romanos 8:18-39",
            "language": "es",
            "audio_url": "https://ibr-espana.org/sermons/sermon001.mp3",
            "thumbnail": "https://ibr-espana.org/thumbnails/sermon001.jpg"
        },
        {
            "id": "sermon002",
            "title": "La Soberanía de Dios",
            "preacher": "Pastor Miguel Rodríguez",
            "date": "2023-10-15",
            "duration": "38:22",
            "scripture": "Job 38:1-41",
            "language": "es",
            "audio_url": "https://ibr-espana.org/sermons/sermon002.mp3",
            "thumbnail": "https://ibr-espana.org/thumbnails/sermon002.jpg"
        },
        {
            "id": "sermon003",
            "title": "God's Sovereignty in Our Lives",
            "preacher": "Pastor David Wilson",
            "date": "2023-10-08",
            "duration": "41:05",
            "scripture": "Psalm 139:1-24",
            "language": "en",
            "audio_url": "https://ibr-espana.org/sermons/sermon003.mp3",
            "thumbnail": "https://ibr-espana.org/thumbnails/sermon003.jpg"
        }
    ]

def get_sample_events() -> List[Dict[str, Any]]:
    """Get sample church events (in production, would fetch from API)"""
    return [
        {
            "id": "event001",
            "title": "Estudio Bíblico Semanal",
            "date": "2023-11-15",
            "time": "19:00",
            "location": "Sala Principal",
            "description": "Estudio del libro de Romanos, capítulos 5-8",
            "language": "es"
        },
        {
            "id": "event002",
            "title": "Reunión de Oración",
            "date": "2023-11-17",
            "time": "20:00",
            "location": "Sala 2",
            "description": "Tiempo dedicado a la oración comunitaria",
            "language": "es"
        },
        {
            "id": "event003",
            "title": "Youth Fellowship",
            "date": "2023-11-18",
            "time": "18:00",
            "location": "Youth Room",
            "description": "Bible study and games for teenagers",
            "language": "en"
        }
    ]

def get_sample_devotionals() -> List[Dict[str, Any]]:
    """Get sample devotionals (in production, would fetch from API)"""
    return [
        {
            "id": "dev001",
            "title": "El Poder de la Oración",
            "date": "2023-11-13",
            "scripture": "Santiago 5:13-18",
            "content": "La oración del justo es poderosa y eficaz...",
            "author": "Pastor Juan Martínez",
            "language": "es"
        },
        {
            "id": "dev002",
            "title": "La Fe que Mueve Montañas",
            "date": "2023-11-12",
            "scripture": "Mateo 17:20",
            "content": "Si tuvierais fe como un grano de mostaza...",
            "author": "Hermana Ana García",
            "language": "es"
        },
        {
            "id": "dev003",
            "title": "Walking by Faith",
            "date": "2023-11-11",
            "scripture": "2 Corinthians 5:7",
            "content": "For we walk by faith, not by sight...",
            "author": "Pastor David Wilson",
            "language": "en"
        }
    ]

def get_sample_instagram_posts() -> List[Dict[str, Any]]:
    """Get sample Instagram posts (in production, would fetch from API)"""
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
        }
    ]

def filter_content_by_language(content_list: List[Dict[str, Any]], language: str) -> List[Dict[str, Any]]:
    """Filter content by language"""
    if language == "all":
        return content_list
    return [item for item in content_list if item.get("language", "es") == language]

def create_ibr_interface():
    """Create the IBR España interface for Divine Dashboard v3"""
    with gr.Blocks(css="""
        .sermon-card {
            border: 2px solid #0F0F0F;
            padding: 16px;
            margin-bottom: 16px;
            background-color: white;
            position: relative;
        }
        .sermon-card h3 {
            text-transform: uppercase;
            font-weight: 700;
        }
        .event-card {
            border: 2px solid #0F0F0F;
            margin-bottom: 16px;
            position: relative;
            overflow: hidden;
            background-color: white;
            padding: 16px;
        }
        .devotional-card {
            border: 2px solid #0F0F0F;
            padding: 16px;
            margin-bottom: 16px;
            background-color: white;
            position: relative;
        }
        .prayer-form {
            border: 2px solid #0F0F0F;
            padding: 20px;
            background-color: white;
        }
        .instagram-feed {
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
        }
        .instagram-post {
            width: calc(33.333% - 16px);
            border: 2px solid #0F0F0F;
            padding: 8px;
            background-color: white;
            position: relative;
        }
        /* Instagram Manager Styles */
        .scheduled-post {
            border: 2px solid #0F0F0F;
            padding: 16px;
            margin-bottom: 16px;
            background-color: white;
            border-radius: 8px;
        }
        .analytics-report {
            padding: 16px;
        }
        .metrics-card {
            border: 2px solid #0F0F0F;
            padding: 16px;
            margin-bottom: 16px;
            background-color: white;
            border-radius: 8px;
        }
        .livestream-info {
            padding: 16px;
        }
        .comments-list {
            max-height: 300px;
            overflow-y: auto;
            margin-bottom: 16px;
        }
        .comment {
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 8px;
            background-color: #f8f8f8;
        }
        .comment-meta {
            font-size: 0.8em;
            color: #666;
        }
        .issues-list {
            max-height: 200px;
            overflow-y: auto;
        }
        .issue {
            border: 1px solid #ffdddd;
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 8px;
            background-color: #fff8f8;
        }
        .issue-meta {
            font-size: 0.8em;
            color: #966;
        }
        .technical-issue {
            border: 2px solid #ff6b6b;
            background-color: #fff0f0;
        }
    """) as iface:
        # Header
        gr.Markdown("# 🔱 IBR ESPAÑA PORTAL DIVINO 🔱")
        gr.Markdown("Portal digital para la Iglesia Bautista Reformada de España")
        
        # Language selector
        with gr.Row():
            language = gr.Radio(
                choices=["es", "ca", "en", "all"],
                value="es",
                label="Idioma / Language",
                info="Seleccione su idioma preferido / Select your preferred language"
            )
        
        # Main content tabs
        with gr.Tabs():
            # Sermons tab
            with gr.TabItem("Sermones / Sermons"):
                sermon_search = gr.Textbox(label="Buscar sermones / Search sermons")
                sermon_output = gr.HTML()
                
                def update_sermons(search_term, lang):
                    """Update sermon list based on search and language filter"""
                    sermons = get_sample_sermons()
                    if lang != "all":
                        sermons = [s for s in sermons if s.get("language", "es") == lang]
                    if search_term:
                        sermons = [s for s in sermons if search_term.lower() in s.get("title", "").lower() 
                                   or search_term.lower() in s.get("preacher", "").lower()
                                   or search_term.lower() in s.get("scripture", "").lower()]
                    
                    html_output = "<div class='sermon-container'>"
                    for sermon in sermons:
                        html_output += render_sermon_card(sermon)
                    html_output += "</div>"
                    return html_output
                
                sermon_search.change(update_sermons, [sermon_search, language], sermon_output)
                language.change(update_sermons, [sermon_search, language], sermon_output)
                # Initialize sermons
                sermon_output.update(value=update_sermons("", "es"))
            
            # Events tab
            with gr.TabItem("Eventos / Events"):
                event_output = gr.HTML()
                
                def update_events(lang):
                    """Update events list based on language filter"""
                    events = get_sample_events()
                    if lang != "all":
                        events = [e for e in events if e.get("language", "es") == lang]
                    
                    html_output = "<div class='event-container'>"
                    for event in events:
                        html_output += render_event_card(event)
                    html_output += "</div>"
                    return html_output
                
                language.change(update_events, [language], event_output)
                # Initialize events
                event_output.update(value=update_events("es"))
            
            # Devotionals tab
            with gr.TabItem("Devocionales / Devotionals"):
                devotional_output = gr.HTML()
                
                def update_devotionals(lang):
                    """Update devotionals list based on language filter"""
                    devotionals = get_sample_devotionals()
                    if lang != "all":
                        devotionals = [d for d in devotionals if d.get("language", "es") == lang]
                    
                    html_output = "<div class='devotional-container'>"
                    for devotional in devotionals:
                        html_output += render_devotional_card(devotional)
                    html_output += "</div>"
                    return html_output
                
                language.change(update_devotionals, [language], devotional_output)
                # Initialize devotionals
                devotional_output.update(value=update_devotionals("es"))
            
            # Prayer requests tab
            with gr.TabItem("Peticiones de Oración / Prayer Requests"):
                with gr.Box(elem_classes=["prayer-form"]):
                    gr.Markdown("### Enviar Petición de Oración / Submit Prayer Request")
                    name = gr.Textbox(label="Nombre / Name")
                    email = gr.Textbox(label="Email")
                    request_text = gr.Textbox(label="Petición / Request", lines=5)
                    is_private = gr.Checkbox(label="Petición Privada / Private Request")
                    submit_btn = gr.Button("Enviar / Submit")
                    
                prayer_output = gr.HTML()
                
                def submit_prayer_request(name, email, request_text, is_private):
                    """Submit a prayer request"""
                    if not name or not email or not request_text:
                        return "<div class='error'>Por favor complete todos los campos / Please fill all fields</div>"
                    
                    # In production, would save to database/API
                    prayer = {
                        "id": f"prayer{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "name": name,
                        "email": email,
                        "request": request_text,
                        "is_private": is_private,
                        "date": datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    return "<div class='success'>¡Petición recibida! Su petición ha sido recibida y será atendida por nuestro equipo de oración. / Prayer request received! Your request has been received and will be attended to by our prayer team.</div>"
                
                submit_btn.click(submit_prayer_request, [name, email, request_text, is_private], prayer_output)
            
            # Instagram feed tab
            with gr.TabItem("Instagram"):
                instagram_output = gr.HTML()
                
                def update_instagram():
                    """Update Instagram feed"""
                    posts = get_sample_instagram_posts()
                    
                    html_output = "<div class='instagram-feed'>"
                    for post in posts:
                        html_output += render_instagram_feed([post])
                    html_output += "</div>"
                    return html_output
                
                # Initialize Instagram feed
                instagram_output.update(value=update_instagram())
            
            # Instagram Manager tab
            with gr.TabItem("Instagram Manager"):
                gr.Markdown("## Instagram Account Manager for @ibrespana")
                
                with gr.Tabs():
                    # Post Scheduling tab
                    with gr.TabItem("Schedule Posts"):
                        with gr.Row():
                            with gr.Column():
                                gr.Markdown("### Schedule a New Post")
                                image_path = gr.Textbox(label="Image Path", placeholder="path/to/image.jpg")
                                caption = gr.Textbox(label="Caption", lines=3, placeholder="Your post caption...")
                                first_comment = gr.Textbox(label="First Comment (optional)", lines=2, placeholder="Additional hashtags...")
                                scheduled_time = gr.Textbox(label="Scheduled Time (YYYY-MM-DD HH:MM:SS)", placeholder="2023-12-31 12:00:00")
                                schedule_btn = gr.Button("Schedule Post", variant="primary")
                            
                            with gr.Column():
                                gr.Markdown("### Scheduled Posts")
                                scheduled_posts_output = gr.HTML()
                                refresh_scheduled_btn = gr.Button("Refresh")
                        
                        schedule_status = gr.Markdown("")
                        
                        def schedule_new_post(image, caption, comment, time):
                            try:
                                if not image or not caption or not time:
                                    return "⚠️ Please fill in all required fields"
                                
                                manager = InstagramManager()
                                post = manager.schedule_post(
                                    image_path=image,
                                    caption=caption,
                                    scheduled_time=time,
                                    first_comment=comment if comment else None
                                )
                                
                                return f"✅ Post scheduled successfully for {time}"
                            except Exception as e:
                                return f"❌ Error: {str(e)}"
                        
                        def get_scheduled_posts():
                            try:
                                manager = InstagramManager()
                                posts = manager.get_scheduled_posts()
                                
                                if not posts:
                                    return "<p>No scheduled posts</p>"
                                
                                html = "<div class='scheduled-posts'>"
                                for post in posts:
                                    html += f"""
                                    <div class='scheduled-post'>
                                        <h4>Post ID: {post.id}</h4>
                                        <p><strong>Scheduled for:</strong> {post.scheduled_time}</p>
                                        <p><strong>Caption:</strong> {post.caption}</p>
                                        <p><strong>Image:</strong> {post.image_path}</p>
                                        <p><strong>First Comment:</strong> {post.first_comment or "None"}</p>
                                        <hr>
                                    </div>
                                    """
                                html += "</div>"
                                return html
                            except Exception as e:
                                return f"<p>Error loading scheduled posts: {str(e)}</p>"
                        
                        schedule_btn.click(schedule_new_post, 
                                          [image_path, caption, first_comment, scheduled_time], 
                                          schedule_status)
                        refresh_scheduled_btn.click(get_scheduled_posts, [], scheduled_posts_output)
                        # Initialize scheduled posts
                        scheduled_posts_output.update(value=get_scheduled_posts())
                    
                    # Comment Management tab
                    with gr.TabItem("Manage Comments"):
                        with gr.Row():
                            with gr.Column():
                                gr.Markdown("### Auto-Reply Rules")
                                keywords = gr.Textbox(label="Keywords (comma separated)", placeholder="prayer, oración, ayuda")
                                reply_template = gr.Textbox(label="Reply Template", lines=3, 
                                                          placeholder="Thank you for your message. Our team will respond shortly.")
                                add_rule_btn = gr.Button("Add Rule")
                                
                                rule_status = gr.Markdown("")
                                
                                def add_auto_reply_rule(keywords_text, template):
                                    try:
                                        if not keywords_text or not template:
                                            return "⚠️ Please fill in all fields"
                                        
                                        keywords_list = [k.strip() for k in keywords_text.split(",")]
                                        
                                        manager = InstagramManager()
                                        rule = manager.add_auto_reply_rule(keywords_list, template)
                                        
                                        return f"✅ Auto-reply rule added for keywords: {', '.join(keywords_list)}"
                                    except Exception as e:
                                        return f"❌ Error: {str(e)}"
                                
                                add_rule_btn.click(add_auto_reply_rule, [keywords, reply_template], rule_status)
                            
                            with gr.Column():
                                gr.Markdown("### Process Comments")
                                process_btn = gr.Button("Process Auto-Replies")
                                process_status = gr.Markdown("")
                                
                                def process_auto_replies():
                                    try:
                                        manager = InstagramManager()
                                        count = manager.process_auto_replies()
                                        
                                        return f"✅ Processed comments and generated {count} auto-replies"
                                    except Exception as e:
                                        return f"❌ Error: {str(e)}"
                                
                                process_btn.click(process_auto_replies, [], process_status)
                    
                    # Analytics tab
                    with gr.TabItem("Analytics"):
                        with gr.Row():
                            with gr.Column():
                                gr.Markdown("### Generate Report")
                                start_date = gr.Textbox(label="Start Date (YYYY-MM-DD)", 
                                                      value=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
                                end_date = gr.Textbox(label="End Date (YYYY-MM-DD)", 
                                                    value=datetime.now().strftime("%Y-%m-%d"))
                                generate_report_btn = gr.Button("Generate Report")
                                
                                report_output = gr.HTML()
                                
                                def generate_analytics_report(start, end):
                                    try:
                                        manager = InstagramManager()
                                        report = manager.generate_analytics_report(start, end)
                                        
                                        metrics = report.metrics
                                        
                                        html = f"""
                                        <div class='analytics-report'>
                                            <h3>Analytics Report: {start} to {end}</h3>
                                            <p><strong>Generated at:</strong> {report.generated_at}</p>
                                            
                                            <div class='metrics-card'>
                                                <h4>Account Metrics</h4>
                                                <p>Followers: {metrics.get('followers_count', 0)} (Growth: +{metrics.get('followers_growth', 0)})</p>
                                                <p>Posts: {metrics.get('posts_count', 0)}</p>
                                                <p>Engagement Rate: {metrics.get('engagement_rate', 0)}%</p>
                                            </div>
                                            
                                            <div class='metrics-card'>
                                                <h4>Engagement</h4>
                                                <p>Total Likes: {metrics.get('total_likes', 0)}</p>
                                                <p>Total Comments: {metrics.get('total_comments', 0)}</p>
                                                <p>Reach: {metrics.get('reach', 0)}</p>
                                                <p>Impressions: {metrics.get('impressions', 0)}</p>
                                            </div>
                                            
                                            <div class='metrics-card'>
                                                <h4>Top Posts</h4>
                                                <ul>
                                        """
                                        
                                        for post in metrics.get('top_posts', []):
                                            html += f"<li>Post {post.get('id')}: {post.get('likes')} likes, {post.get('comments')} comments</li>"
                                        
                                        html += """
                                                </ul>
                                            </div>
                                        </div>
                                        """
                                        
                                        return html
                                    except Exception as e:
                                        return f"<p>Error generating report: {str(e)}</p>"
                                
                                generate_report_btn.click(generate_analytics_report, [start_date, end_date], report_output)
                            
                            with gr.Column():
                                gr.Markdown("### Schedule Reports")
                                freq = gr.Radio(choices=["daily", "weekly", "monthly"], value="weekly", label="Frequency")
                                recipients = gr.Textbox(label="Recipients (comma separated emails)", 
                                                     placeholder="pastor@ibrespana.org, admin@ibrespana.org")
                                schedule_report_btn = gr.Button("Schedule Report")
                                
                                schedule_report_status = gr.Markdown("")
                                
                                def schedule_report(frequency, emails):
                                    try:
                                        if not emails:
                                            return "⚠️ Please enter at least one recipient email"
                                        
                                        email_list = [e.strip() for e in emails.split(",")]
                                        
                                        manager = InstagramManager()
                                        report = manager.schedule_analytics_report(frequency, email_list)
                                        
                                        return f"✅ Analytics report scheduled with {frequency} frequency for {len(email_list)} recipients"
                                    except Exception as e:
                                        return f"❌ Error: {str(e)}"
                                
                                schedule_report_btn.click(schedule_report, [freq, recipients], schedule_report_status)
                    
                    # Outreach tab
                    with gr.TabItem("Outreach"):
                        with gr.Row():
                            with gr.Column():
                                gr.Markdown("### Create Campaign")
                                campaign_name = gr.Textbox(label="Campaign Name", placeholder="Easter Outreach 2024")
                                target_audience = gr.Textbox(label="Target Audience", placeholder="Christian youth in Madrid")
                                message_template = gr.Textbox(label="Message Template", lines=3,
                                                           placeholder="Join us for our Easter celebration! {custom_message}")
                                create_campaign_btn = gr.Button("Create Campaign")
                                
                                campaign_status = gr.Markdown("")
                                
                                def create_campaign(name, audience, template):
                                    try:
                                        if not name or not audience or not template:
                                            return "⚠️ Please fill in all fields"
                                        
                                        manager = InstagramManager()
                                        campaign = manager.create_outreach_campaign(name, audience, template)
                                        
                                        return f"✅ Campaign '{name}' created with ID: {campaign.id}"
                                    except Exception as e:
                                        return f"❌ Error: {str(e)}"
                                
                                create_campaign_btn.click(create_campaign, 
                                                        [campaign_name, target_audience, message_template], 
                                                        campaign_status)
                            
                            with gr.Column():
                                gr.Markdown("### Add Lead")
                                campaign_id = gr.Textbox(label="Campaign ID", placeholder="Enter campaign ID")
                                lead_username = gr.Textbox(label="Instagram Username", placeholder="@username")
                                custom_message = gr.Textbox(label="Custom Message (optional)", 
                                                         placeholder="Looking forward to seeing you!")
                                add_lead_btn = gr.Button("Add Lead")
                                
                                lead_status = gr.Markdown("")
                                
                                def add_lead(campaign_id, username, message):
                                    try:
                                        if not campaign_id or not username:
                                            return "⚠️ Please enter campaign ID and username"
                                        
                                        # Remove @ if present
                                        if username.startswith("@"):
                                            username = username[1:]
                                        
                                        manager = InstagramManager()
                                        result = manager.add_outreach_lead(
                                            campaign_id=campaign_id,
                                            username=username,
                                            custom_message=message if message else None
                                        )
                                        
                                        if result:
                                            return f"✅ Lead '{username}' added to campaign"
                                        else:
                                            return "⚠️ Campaign not found"
                                    except Exception as e:
                                        return f"❌ Error: {str(e)}"
                                
                                add_lead_btn.click(add_lead, [campaign_id, lead_username, custom_message], lead_status)
                    
                    # Livestream tab
                    with gr.TabItem("Livestream Monitoring"):
                        with gr.Row():
                            with gr.Column():
                                gr.Markdown("### Monitor Livestream")
                                stream_id = gr.Textbox(label="Stream ID", placeholder="easter_service_2024")
                                notification_email = gr.Textbox(label="Notification Email", 
                                                             placeholder="tech@ibrespana.org")
                                start_monitor_btn = gr.Button("Start Monitoring")
                                stop_monitor_btn = gr.Button("Stop Monitoring")
                                
                                stream_status = gr.Markdown("")
                                
                                def start_monitoring(stream_id, email):
                                    try:
                                        if not stream_id:
                                            return "⚠️ Please enter a stream ID"
                                        
                                        manager = InstagramManager()
                                        stream = manager.start_livestream_monitoring(
                                            stream_id=stream_id,
                                            notification_email=email if email else None
                                        )
                                        
                                        return f"✅ Started monitoring livestream: {stream_id}"
                                    except Exception as e:
                                        return f"❌ Error: {str(e)}"
                                
                                def stop_monitoring(stream_id):
                                    try:
                                        if not stream_id:
                                            return "⚠️ Please enter a stream ID"
                                        
                                        manager = InstagramManager()
                                        result = manager.stop_livestream_monitoring(stream_id)
                                        
                                        if result:
                                            return f"✅ Stopped monitoring livestream: {stream_id}"
                                        else:
                                            return "⚠️ Livestream not found"
                                    except Exception as e:
                                        return f"❌ Error: {str(e)}"
                                
                                start_monitor_btn.click(start_monitoring, [stream_id, notification_email], stream_status)
                                stop_monitor_btn.click(stop_monitoring, [stream_id], stream_status)
                            
                            with gr.Column():
                                gr.Markdown("### Livestream Comments")
                                active_stream_id = gr.Textbox(label="Active Stream ID", placeholder="Enter stream ID to view")
                                view_stream_btn = gr.Button("View Stream Info")
                                
                                stream_info = gr.HTML()
                                
                                def view_stream_info(stream_id):
                                    try:
                                        if not stream_id:
                                            return "<p>Please enter a stream ID</p>"
                                        
                                        manager = InstagramManager()
                                        stream = manager.get_livestream(stream_id)
                                        
                                        if not stream:
                                            return "<p>Livestream not found</p>"
                                        
                                        html = f"""
                                        <div class='livestream-info'>
                                            <h3>Livestream: {stream_id}</h3>
                                            <p><strong>Started:</strong> {stream.get('started_at', 'Unknown')}</p>
                                            <p><strong>Status:</strong> {'Active' if stream.get('is_monitoring', False) else 'Inactive'}</p>
                                            
                                            <h4>Comments:</h4>
                                            <div class='comments-list'>
                                        """
                                        
                                        comments = stream.get('comments', [])
                                        if not comments:
                                            html += "<p>No comments yet</p>"
                                        else:
                                            for comment in comments:
                                                issue_class = "technical-issue" if comment.get('is_technical_issue', False) else ""
                                                html += f"""
                                                <div class='comment {issue_class}'>
                                                    <p><strong>{comment.get('username')}:</strong> {comment.get('text')}</p>
                                                    <p class='comment-meta'>{comment.get('created_at', '')}</p>
                                                </div>
                                                """
                                        
                                        html += """
                                            </div>
                                            
                                            <h4>Technical Issues:</h4>
                                            <div class='issues-list'>
                                        """
                                        
                                        issues = stream.get('technical_issues', [])
                                        if not issues:
                                            html += "<p>No technical issues reported</p>"
                                        else:
                                            for issue in issues:
                                                html += f"""
                                                <div class='issue'>
                                                    <p><strong>Issue:</strong> {issue.get('issue', '')}</p>
                                                    <p class='issue-meta'>Reported at: {issue.get('reported_at', '')}</p>
                                                </div>
                                                """
                                        
                                        html += """
                                            </div>
                                        </div>
                                        """
                                        
                                        return html
                                    except Exception as e:
                                        return f"<p>Error loading stream info: {str(e)}</p>"
                                
                                view_stream_btn.click(view_stream_info, [active_stream_id], stream_info)
        
        # Footer
        gr.Markdown("---")
        gr.Markdown("© IBR España 2023 | Desarrollado con 💙 por OMEGA BTC AI")
    
    return iface

# For testing purposes
if __name__ == "__main__":
    iface = create_ibr_interface()
    iface.launch() 