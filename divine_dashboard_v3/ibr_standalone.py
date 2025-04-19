import os
import sys
import json
import gradio as gr
import logging
import requests
import re
import time
import socket
import asyncio
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from fastapi import FastAPI, APIRouter, Request, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ibr_standalone')

def find_available_port(start_port=7863, max_port=7873):
    """Find an available port to use for the server, starting from start_port"""
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                logger.info(f"Found available port: {port}")
                return port
            except OSError:
                logger.info(f"Port {port} is already in use, trying next port")
                continue
    
    # If we got here, no ports were available
    logger.error(f"No available ports found in range {start_port}-{max_port}")
    return None

# Create a basic manifest.json to avoid 404 errors
def create_manifest_json():
    """Create a basic manifest.json to avoid 404 errors"""
    manifest = {
        "name": "IBR España Instagram Manager",
        "short_name": "IBR España",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#4a90e2",
        "icons": []
    }
    
    static_dir = Path("static")
    static_dir.mkdir(exist_ok=True)
    
    with open(static_dir / "manifest.json", "w") as f:
        json.dump(manifest, f)
    
    logger.info("Created manifest.json")

def get_instagram_data(username):
    """
    Attempt to fetch Instagram data for a given username.
    Handles anti-scraping measures by returning structured error.
    
    Returns:
        dict: {
            'success': bool,
            'followers': int or None,
            'posts': int or None,
            'error': str or None
        }
    """
    result = {
        'success': False,
        'followers': None,
        'posts': None,
        'error': None
    }
    
    try:
        # Enhanced headers to appear more like a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        # Make the request
        response = requests.get(f"https://www.instagram.com/{username}/", headers=headers, timeout=10)
        response.raise_for_status()
        
        # Try multiple methods to extract data
        
        # Method 1: Use BeautifulSoup to parse meta tags
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_tag = soup.find("meta", property="og:description")
            if meta_tag and meta_tag.get("content"):
                content = meta_tag["content"]
                # Try to parse followers from meta description
                # Format may be like "1,234 Followers, 567 Following, 89 Posts"
                parts = content.split(" ")
                if len(parts) >= 2 and "followers" in parts[1].lower():
                    try:
                        # Extract the number part from "1,234 Followers"
                        followers_str = parts[0].replace(',', '')
                        result['followers'] = int(followers_str)
                    except ValueError:
                        logger.warning(f"Could not parse followers count from: {parts[0]}")
                
                # Look for post count
                posts_match = re.search(r'"edge_owner_to_timeline_media":{"count":(\d+)', response.text)
                if posts_match:
                    result['posts'] = int(posts_match.group(1))
                
                # Calculate an approximate engagement rate based on recent posts
                # This is a simplified calculation
                result['engagement_rate'] = round((result['posts'] / max(1, result['followers'])) * 100, 2)
                
                result['success'] = True
            else:
                result['error'] = "Meta description not found"
        except Exception as e:
            result['error'] = f"Error parsing meta tags: {e}"
        
        if result['success']:
            result['last_update'] = datetime.now().isoformat()
            result['followers'] = result['followers'] or 0
            result['posts'] = result['posts'] or 0
            result['engagement_rate'] = result['engagement_rate'] or 0
            
            # Save to cache
            cache_data = {
                'followers': result['followers'],
                'posts': result['posts'],
                'engagement_rate': result['engagement_rate'],
                'timestamp': result['last_update']
            }
            
            cache_file = os.path.join('cache', f"{username}_instagram_data.json")
            os.makedirs(os.path.dirname(cache_file), exist_ok=True)
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
            logger.info("Saved Instagram data to cache")
        else:
            logger.warning("Failed to fetch Instagram data")
        
        return result
    except Exception as e:
        logger.error(f"Error fetching Instagram data: {e}")
        return {
            'success': False,
            'followers': None,
            'posts': None,
            'error': str(e)
        }

# Instagram Manager for IBR Spain
class InstagramManager:
    def __init__(self):
        # Default values in case fetching fails
        self.followers = 1245
        self.posts = 87
        self.engagement_rate = 3.7
        self.last_update = "Never"
        self.account_name = "ibrespana"
        
        # Config file and data directory setup
        self.config_file = os.path.join('config', 'ibr_spain.json')
        self.data_dir = os.path.expanduser("~/ibr_data/instagram_manager")
        self.account_data_file = os.path.join(self.data_dir, "account_data.json")
        
        # Load config if exists
        self.load_config()
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Try to fetch real data
        self.fetch_instagram_data()
        
    def load_config(self):
        """Load configuration file with account settings"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    if 'instagram_manager' in config:
                        img_config = config['instagram_manager']
                        if 'data_dir' in img_config:
                            self.data_dir = img_config['data_dir']
                        if 'account_name' in img_config:
                            self.account_name = img_config['account_name']
            except Exception as e:
                logger.error(f"Error loading config: {e}")
    
    def fetch_instagram_data(self):
        """Fetch Instagram data using web scraping approach"""
        try:
            # First, check if we have cached data and it's recent (less than 1 hour old)
            if os.path.exists(self.account_data_file):
                try:
                    with open(self.account_data_file, 'r') as f:
                        cached_data = json.load(f)
                        
                    # Check if data is recent
                    cached_time = datetime.fromisoformat(cached_data.get('timestamp', '2000-01-01T00:00:00'))
                    now = datetime.now()
                    
                    # If cached data is less than 1 hour old, use it
                    if (now - cached_time).total_seconds() < 3600:
                        self.followers = cached_data.get('followers', self.followers)
                        self.posts = cached_data.get('posts', self.posts)
                        self.engagement_rate = cached_data.get('engagement_rate', self.engagement_rate)
                        self.last_update = cached_data.get('timestamp', self.last_update)
                        logger.info(f"Using cached Instagram data (updated {self.last_update})")
                        return
                except Exception as e:
                    logger.error(f"Error reading cached data: {e}")
            
            # If we got here, we need to fetch fresh data
            result = get_instagram_data(self.account_name)
            
            if result['success']:
                self.followers = result['followers']
                self.posts = result['posts']
                self.engagement_rate = result['engagement_rate']
                self.last_update = result['last_update']
                
                # Save to account data file
                account_data = {
                    'followers': self.followers,
                    'posts': self.posts,
                    'engagement_rate': self.engagement_rate,
                    'timestamp': self.last_update
                }
                
                with open(self.account_data_file, 'w') as f:
                    json.dump(account_data, f)
                logger.info(f"Fetched fresh Instagram data for @{self.account_name}")
            else:
                logger.warning(f"Failed to fetch Instagram data: {result['error']}")
                self.load_fallback_data()
        except Exception as e:
            logger.error(f"Error in fetch_instagram_data: {e}")
            self.load_fallback_data()
    
    def load_fallback_data(self):
        """Load fallback data if fetching fails"""
        try:
            if os.path.exists(self.account_data_file):
                with open(self.account_data_file, 'r') as f:
                    cached_data = json.load(f)
                self.followers = cached_data.get('followers', self.followers)
                self.posts = cached_data.get('posts', self.posts)
                self.engagement_rate = cached_data.get('engagement_rate', self.engagement_rate)
                self.last_update = cached_data.get('timestamp', self.last_update)
                logger.info(f"Using fallback Instagram data (last updated {self.last_update})")
            else:
                logger.warning("No fallback data available, using default values")
        except Exception as e:
            logger.error(f"Error loading fallback data: {e}")
    
    def get_stats(self):
        """Get Instagram account statistics"""
        return {
            "followers": self.followers,
            "posts": self.posts,
            "engagement_rate": self.engagement_rate,
            "last_update": self.last_update,
            "account_name": self.account_name
        }
    
    def create_post(self, caption, hashtags):
        """Create a new Instagram post"""
        # This is a simulation only
        return {
            "success": True,
            "message": f"Post created with caption: {caption[:20]}... and {len(hashtags.split())} hashtags"
        }
    
    def analyze_account(self):
        """Analyze the Instagram account"""
        stats = self.get_stats()
        return {
            "success": True,
            "analysis": f"""
            ## IBR España Instagram Analysis (@{stats['account_name']})
            
            ### Account Metrics
            - Followers: {stats['followers']}
            - Posts: {stats['posts']}
            - Engagement Rate: {stats['engagement_rate']}%
            - Last Updated: {stats['last_update']}
            """
        }
    
    def refresh_data(self):
        """Refresh Instagram data"""
        self.fetch_instagram_data()
        return self.get_stats()

# Define Pydantic models for API
class PostRequest(BaseModel):
    caption: str = Field(..., description="Caption for the Instagram post")
    hashtags: str = Field(..., description="Hashtags for the post")

class PostResponse(BaseModel):
    success: bool
    message: str = ""
    error: str = ""

# Create FastAPI app
app = FastAPI(title="IBR España Dashboard API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create API router
router = APIRouter(prefix="/api/instagram", tags=["instagram"])

# Define endpoints
@router.get("/stats", response_model=Dict[str, Any])
async def get_stats():
    """Get Instagram account statistics"""
    manager = InstagramManager()
    return manager.get_stats()

@router.get("/feed", response_model=List[Dict[str, Any]])
async def get_feed():
    """Get Instagram feed"""
    return [
        {
            "id": "post1",
            "image_url": "https://ibr-espana.org/instagram/post1.jpg",
            "caption": "Servicio dominical - ¡Gloria a Dios por Su fidelidad!",
            "likes": 45,
            "date": "2023-11-12",
            "category": "service"
        },
        {
            "id": "post2",
            "image_url": "https://ibr-espana.org/instagram/post2.jpg", 
            "caption": "Estudio bíblico del miércoles - profundizando en la Palabra",
            "likes": 36,
            "date": "2023-11-08",
            "category": "bible_study"
        }
    ]

@router.post("/post", response_model=PostResponse)
async def create_post(request: PostRequest):
    """Create a new Instagram post"""
    try:
        manager = InstagramManager()
        result = manager.create_post(request.caption, request.hashtags)
        
        if isinstance(result, dict) and "error" in result and result["error"]:
            return PostResponse(success=False, error=result["error"])
        elif isinstance(result, dict) and "message" in result:
            return PostResponse(success=True, message=result["message"])
        elif isinstance(result, str):
            return PostResponse(success=True, message=result)
        else:
            return PostResponse(success=True, message="Post created successfully")
    except Exception as e:
        return PostResponse(success=False, error=str(e))

@router.get("/analysis", response_model=Dict[str, Any])
async def get_analysis():
    """Get Instagram account analysis"""
    manager = InstagramManager()
    return manager.analyze_account()

# Include router
app.include_router(router)

def create_ibr_interface():
    """Create the IBR España Gradio interface"""
    manager = InstagramManager()
    
    with gr.Blocks(title="IBR España Instagram Manager") as demo:
        with gr.Column():
            gr.Markdown("# IBR España Instagram Manager")
            gr.Markdown("### Gestión de Instagram para IBR España")
            
            with gr.Tab("Dashboard"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.Markdown("## Estadísticas de la cuenta")
                        stats_md = gr.Markdown(f"""
                        ### @{manager.account_name}
                        
                        - **Seguidores:** {manager.followers}
                        - **Publicaciones:** {manager.posts}
                        - **Tasa de interacción:** {manager.engagement_rate}%
                        - **Última actualización:** {manager.last_update}
                        """)
                        
                        refresh_btn = gr.Button("Actualizar datos")
                    
                    with gr.Column(scale=3):
                        gr.Markdown("## Publicaciones recientes")
                        posts_html = gr.HTML("""
                        <div class="instagram-feed">
                            <div class="instagram-post">
                                <img src="https://ibr-espana.org/instagram/post1.jpg" alt="Instagram post">
                                <p class="caption">Servicio dominical - ¡Gloria a Dios por Su fidelidad!</p>
                                <p class="likes">❤️ 45 likes</p>
                                <p class="date">2023-11-12</p>
                            </div>
                            <div class="instagram-post">
                                <img src="https://ibr-espana.org/instagram/post2.jpg" alt="Instagram post">
                                <p class="caption">Estudio bíblico del miércoles - profundizando en la Palabra</p>
                                <p class="likes">❤️ 36 likes</p>
                                <p class="date">2023-11-08</p>
                            </div>
                        </div>
                        """)
            
            with gr.Tab("Crear publicación"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("## Crear nueva publicación")
                        caption_input = gr.Textbox(label="Texto de la publicación", lines=5)
                        hashtags_input = gr.Textbox(label="Hashtags", lines=2)
                        post_btn = gr.Button("Publicar")
                        post_result = gr.Markdown("")
            
            with gr.Tab("Análisis"):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("## Análisis de la cuenta")
                        analysis_md = gr.Markdown(f"""
                        ## IBR España Instagram Analysis (@{manager.account_name})
                        
                        ### Account Metrics
                        - Followers: {manager.followers}
                        - Posts: {manager.posts}
                        - Engagement Rate: {manager.engagement_rate}%
                        - Last Updated: {manager.last_update}
                        """)
                        
                        analyze_btn = gr.Button("Analizar cuenta")
        
        # Define functions to handle button clicks
        def on_refresh():
            manager.refresh_data()
            stats = manager.get_stats()
            return f"""
            ### @{stats['account_name']}
            
            - **Seguidores:** {stats['followers']}
            - **Publicaciones:** {stats['posts']}
            - **Tasa de interacción:** {stats['engagement_rate']}%
            - **Última actualización:** {stats['last_update']}
            """
        
        def on_post(caption, hashtags):
            result = manager.create_post(caption, hashtags)
            if isinstance(result, dict) and result.get("success", False):
                return f"✅ **Éxito:** {result.get('message', 'Publicación creada')}"
            elif isinstance(result, dict) and "error" in result:
                return f"❌ **Error:** {result['error']}"
            else:
                return f"✅ **Éxito:** {result}"
        
        def on_analyze():
            result = manager.analyze_account()
            if isinstance(result, dict) and "analysis" in result:
                return result["analysis"]
            elif isinstance(result, dict) and "error" in result:
                return f"❌ **Error:** {result['error']}"
            else:
                return result
        
        # Connect functions to buttons
        refresh_btn.click(on_refresh, inputs=[], outputs=[stats_md])
        post_btn.click(on_post, inputs=[caption_input, hashtags_input], outputs=[post_result])
        analyze_btn.click(on_analyze, inputs=[], outputs=[analysis_md])
        
        # Add CSS for Instagram feed styling
        gr.HTML("""
        <style>
        .instagram-feed {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }
        .instagram-post {
            border: 1px solid #dbdbdb;
            border-radius: 4px;
            padding: 10px;
            background: white;
        }
        .instagram-post img {
            width: 100%;
            max-height: 250px;
            object-fit: cover;
            border-radius: 2px;
        }
        .instagram-post .caption {
            padding: 10px 0;
            font-size: 14px;
        }
        .instagram-post .likes {
            font-size: 12px;
            color: #555;
        }
        .instagram-post .date {
            font-size: 11px;
            color: #888;
        }
        </style>
        """)
    
    return demo

async def run_api_server():
    """Run the FastAPI server on the same port as the Gradio interface."""
    config = uvicorn.Config(app, host="0.0.0.0", port=7863)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    # Create manifest.json to fix 404 errors
    create_manifest_json()
    
    # Create the Gradio interface
    ibr_interface = create_ibr_interface()
    
    # Explicitly disable queue to avoid the pydantic error
    ibr_interface.queue(api_open=False)
    
    # Launch the interface
    ibr_interface.launch(
        server_name="0.0.0.0",
        server_port=7863,
        share=True,
        prevent_thread_lock=True
    )
