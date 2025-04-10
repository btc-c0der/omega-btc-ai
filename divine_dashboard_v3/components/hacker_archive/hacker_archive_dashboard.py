# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
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
Hacker Archive Dashboard

Gradio interface for the Hacker Archive NFT Generator providing web-based
access to historical hacker defacement NFT creation.
"""

import os
import time
import asyncio
import json
import base64
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional, Union

import gradio as gr
import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt

import sys
sys.path.append('/Users/fsiqueira/OMEGA/omega-btc-ai')
from divine_dashboard_v3.utils.redis_helper import (
    get_redis_client, get_json, log_event, record_metric,
    get_namespaced_key, get_list
)

from .hacker_archive_generator import (
    HackerArchiveNFTGenerator, 
    HACKER_CREWS, 
    DEFACEMENT_YEARS, 
    DEFACEMENT_TYPES,
    ASCII_PATTERNS
)

# Configure paths
OUTPUT_DIR = Path("hacker_archive_output")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Initialize the generator
generator = HackerArchiveNFTGenerator(output_dir=str(OUTPUT_DIR))

# Dashboard state
HISTORY = []

async def generate_nft(
    crew: str,
    year: str,
    defacement_type: str,
    pattern: str,
    custom_text: str
) -> Dict[str, Any]:
    """Generate a hacker archive NFT with the specified parameters.
    
    Args:
        crew: Hacker crew name
        year: Year of defacement
        defacement_type: Type of defacement
        pattern: ASCII pattern to use
        custom_text: Custom text for the defacement
        
    Returns:
        Dictionary with generation results
    """
    start_time = time.time()
    
    # Log generation request
    log_event("hacker_dashboard_generate", {
        "crew": crew,
        "year": year,
        "defacement_type": defacement_type,
        "pattern": pattern,
        "has_custom_text": bool(custom_text)
    })
    
    try:
        # Generate the NFT
        nft_info = await generator.generate_hacker_nft(
            crew=crew,
            year=year,
            defacement_type=defacement_type,
            pattern=pattern,
            custom_text=custom_text if custom_text else None
        )
        
        # Add to history
        global HISTORY
        HISTORY.append({
            "id": nft_info["id"],
            "name": nft_info["name"],
            "image_path": nft_info["image_path"],
            "crew": nft_info["crew"],
            "year": nft_info["year"],
            "rarity_score": nft_info["rarity_score"],
            "rarity_tier": nft_info["rarity_tier"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep history at reasonable size
        if len(HISTORY) > 50:
            HISTORY = HISTORY[-50:]
        
        # Log success and timing
        generation_time = time.time() - start_time
        log_event("hacker_nft_generation_success", {
            "nft_id": nft_info["id"],
            "generation_time": generation_time,
            "rarity_tier": nft_info["rarity_tier"]
        })
        
        # Return generation result
        return {
            "success": True,
            "nft_info": nft_info,
            "image": nft_info["image_path"],
            "generation_time": generation_time
        }
        
    except Exception as e:
        # Log error
        log_event("hacker_nft_generation_error", {
            "error": str(e),
            "crew": crew,
            "year": year
        })
        
        return {
            "success": False,
            "error": str(e),
            "generation_time": time.time() - start_time
        }

async def batch_generate_nfts(
    count: int,
    crews: List[str],
    years: List[str]
) -> Dict[str, Any]:
    """Generate multiple hacker archive NFTs in a batch.
    
    Args:
        count: Number of NFTs to generate
        crews: List of crews to use
        years: List of years to use
        
    Returns:
        Dictionary with batch generation results
    """
    start_time = time.time()
    
    # Log batch generation request
    log_event("hacker_dashboard_batch_generate", {
        "count": count,
        "crews": crews,
        "years": years
    })
    
    try:
        # Generate the NFTs
        nft_list = await generator.batch_generate_nfts(
            count=count,
            crews=crews,
            years=years
        )
        
        # Add successful NFTs to history
        global HISTORY
        for nft in nft_list:
            if "status" not in nft or nft["status"] != "error":
                HISTORY.append({
                    "id": nft["id"],
                    "name": nft["name"],
                    "image_path": nft["image_path"],
                    "crew": nft["crew"],
                    "year": nft["year"],
                    "rarity_score": nft["rarity_score"],
                    "rarity_tier": nft["rarity_tier"],
                    "timestamp": datetime.now().isoformat(),
                    "batch_id": nft.get("batch_id", "")
                })
        
        # Keep history at reasonable size
        if len(HISTORY) > 50:
            HISTORY = HISTORY[-50:]
        
        # Count successful generations
        successful = [nft for nft in nft_list if "status" not in nft or nft["status"] != "error"]
        
        # Log success and timing
        generation_time = time.time() - start_time
        log_event("hacker_nft_batch_generation_success", {
            "count": count,
            "successful": len(successful),
            "generation_time": generation_time
        })
        
        # Create a gallery image
        gallery_image = None
        if successful:
            # Take up to 4 images for the gallery
            gallery_nfts = successful[:min(4, len(successful))]
            gallery_images = [Image.open(nft["image_path"]) for nft in gallery_nfts]
            
            # Create a 2x2 grid (or smaller if fewer images)
            rows = min(2, len(gallery_images))
            cols = min(2, (len(gallery_images) + 1) // 2)
            
            # Resize images to a consistent size
            thumb_size = (300, 300)
            thumbnails = [img.resize(thumb_size) for img in gallery_images]
            
            # Create grid image
            grid_width = thumb_size[0] * cols
            grid_height = thumb_size[1] * rows
            grid_img = Image.new('RGB', (grid_width, grid_height), color=(0, 0, 0))
            
            # Place images in grid
            for i, thumb in enumerate(thumbnails):
                row = i // cols
                col = i % cols
                x = col * thumb_size[0]
                y = row * thumb_size[1]
                grid_img.paste(thumb, (x, y))
            
            # Save grid image
            grid_path = OUTPUT_DIR / "batch_preview.png"
            grid_img.save(grid_path)
            gallery_image = str(grid_path)
        
        # Return batch generation result
        return {
            "success": True,
            "total": count,
            "successful": len(successful),
            "nft_list": nft_list,
            "gallery_image": gallery_image,
            "generation_time": generation_time
        }
        
    except Exception as e:
        # Log error
        log_event("hacker_nft_batch_generation_error", {
            "error": str(e),
            "count": count
        })
        
        return {
            "success": False,
            "error": str(e),
            "generation_time": time.time() - start_time
        }

def get_history() -> List[Dict[str, Any]]:
    """Get the generation history.
    
    Returns:
        List of NFT generation records
    """
    return HISTORY

def get_statistics() -> Dict[str, Any]:
    """Get statistics about generated NFTs.
    
    Returns:
        Dictionary with NFT statistics
    """
    # Get statistics from generator
    stats = generator.get_nft_stats()
    
    # Add additional stats from history
    if HISTORY:
        # Calculate average rarity
        avg_rarity = sum(nft.get("rarity_score", 0) for nft in HISTORY) / len(HISTORY)
        stats["session_average_rarity"] = avg_rarity
        
        # Count rarity tiers
        session_tiers = {}
        for nft in HISTORY:
            tier = nft.get("rarity_tier", "Common")
            session_tiers[tier] = session_tiers.get(tier, 0) + 1
        stats["session_rarity_distribution"] = session_tiers
    
    return stats

def create_visualization() -> str:
    """Create a visualization of NFT statistics.
    
    Returns:
        Path to the generated visualization image
    """
    # Get statistics
    stats = get_statistics()
    
    # Create a figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Plot rarity distribution
    rarity_tiers = ["Legendary", "Epic", "Rare", "Uncommon", "Common"]
    rarity_counts = [stats["rarity_distribution"].get(tier, 0) for tier in rarity_tiers]
    
    ax1.bar(rarity_tiers, rarity_counts, color=['gold', 'purple', 'blue', 'green', 'gray'])
    ax1.set_title('Rarity Distribution')
    ax1.set_ylabel('Count')
    ax1.set_ylim(bottom=0)
    
    # Plot crew popularity
    crews = list(stats.get("crew_popularity", {}).keys())
    if crews:
        counts = [stats["crew_popularity"].get(crew, 0) for crew in crews]
        
        # Sort by popularity
        sorted_data = sorted(zip(crews, counts), key=lambda x: x[1], reverse=True)
        top_crews = [x[0] for x in sorted_data[:5]]  # Take top 5
        top_counts = [x[1] for x in sorted_data[:5]]
        
        ax2.barh(top_crews, top_counts, color='green')
        ax2.set_title('Most Popular Crews')
        ax2.set_xlabel('Count')
    else:
        ax2.text(0.5, 0.5, "No crew data available", ha='center', va='center')
        ax2.set_title('Crew Popularity')
    
    # Set overall title
    fig.suptitle(f'Hacker Archive NFT Statistics (Total: {stats["total_nfts"]})')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figure
    viz_path = OUTPUT_DIR / "stats_visualization.png"
    plt.savefig(viz_path)
    plt.close(fig)
    
    return str(viz_path)

def create_interface() -> gr.Blocks:
    """Create the Gradio interface.
    
    Returns:
        Gradio Blocks interface
    """
    with gr.Blocks(title="Hacker Archive NFT Generator", theme=gr.themes.Base()) as interface:
        gr.Markdown(
            """
            # 👾 HACKER ARCHIVE NFT GENERATOR 👾
            
            _Preserving the legacy of early 2000s website defacements in NFT form._
            
            Generate NFTs inspired by historical hacker crews and their website defacements from the early web era.
            Each NFT is unique, with detailed metadata and rarity scores based on historical significance.
            """
        )
        
        with gr.Tabs():
            # Single NFT Generation Tab
            with gr.TabItem("Generate Single NFT"):
                with gr.Row():
                    with gr.Column():
                        # Input parameters
                        crew_dropdown = gr.Dropdown(
                            choices=HACKER_CREWS,
                            label="Hacker Crew",
                            value=HACKER_CREWS[0],
                            info="Select a historical hacker crew"
                        )
                        
                        year_dropdown = gr.Dropdown(
                            choices=DEFACEMENT_YEARS,
                            label="Defacement Year",
                            value=DEFACEMENT_YEARS[0],
                            info="Select the year of the defacement"
                        )
                        
                        defacement_type_dropdown = gr.Dropdown(
                            choices=DEFACEMENT_TYPES,
                            label="Defacement Type",
                            value=DEFACEMENT_TYPES[0],
                            info="Select the type of defacement"
                        )
                        
                        pattern_dropdown = gr.Dropdown(
                            choices=list(ASCII_PATTERNS.keys()),
                            label="ASCII Pattern",
                            value=list(ASCII_PATTERNS.keys())[0],
                            info="Select the ASCII art pattern"
                        )
                        
                        custom_text = gr.Textbox(
                            label="Custom Defacement Message",
                            placeholder="Leave empty for random message",
                            info="Optional custom text for the defacement"
                        )
                        
                        generate_button = gr.Button("HACK THE SYSTEM - GENERATE NFT", variant="primary")
                    
                    with gr.Column():
                        # Output components
                        result_image = gr.Image(label="Generated NFT", type="filepath")
                        result_info = gr.JSON(label="NFT Information")
                
                # Define the generation function
                async def generate_nft_handler(crew, year, defacement_type, pattern, custom_text):
                    result = await generate_nft(crew, year, defacement_type, pattern, custom_text)
                    if result["success"]:
                        return result["image"], result["nft_info"]
                    else:
                        return None, {"error": result["error"]}
                
                # Connect the button to the function
                generate_button.click(
                    fn=generate_nft_handler,
                    inputs=[crew_dropdown, year_dropdown, defacement_type_dropdown, pattern_dropdown, custom_text],
                    outputs=[result_image, result_info]
                )
            
            # Batch Generation Tab
            with gr.TabItem("Batch Generate NFTs"):
                with gr.Row():
                    with gr.Column():
                        # Batch inputs
                        batch_count = gr.Slider(
                            minimum=1,
                            maximum=20,
                            step=1,
                            value=5,
                            label="Number of NFTs to Generate",
                            info="How many NFTs to generate in this batch"
                        )
                        
                        batch_crews = gr.CheckboxGroup(
                            choices=HACKER_CREWS,
                            label="Hacker Crews to Include",
                            value=HACKER_CREWS[:3],
                            info="Select which crews to include (leave empty for all)"
                        )
                        
                        batch_years = gr.CheckboxGroup(
                            choices=DEFACEMENT_YEARS,
                            label="Years to Include",
                            value=DEFACEMENT_YEARS[:3],
                            info="Select which years to include (leave empty for all)"
                        )
                        
                        batch_button = gr.Button("MASS DEFACEMENT - GENERATE BATCH", variant="primary")
                        
                    with gr.Column():
                        # Batch outputs
                        batch_gallery = gr.Image(label="Batch Preview", type="filepath")
                        batch_info = gr.JSON(label="Batch Information")
                
                # Define the batch generation function
                async def batch_generate_handler(count, crews, years):
                    result = await batch_generate_nfts(count, crews, years)
                    if result["success"]:
                        return result.get("gallery_image"), {
                            "total": result["total"],
                            "successful": result["successful"],
                            "generation_time": f"{result['generation_time']:.2f} seconds",
                            "results": [
                                {
                                    "id": nft.get("id", "error"),
                                    "name": nft.get("name", "Error"),
                                    "rarity": nft.get("rarity_score", 0),
                                    "tier": nft.get("rarity_tier", "Unknown")
                                }
                                for nft in result["nft_list"]
                            ]
                        }
                    else:
                        return None, {"error": result["error"]}
                
                # Connect the button to the function
                batch_button.click(
                    fn=batch_generate_handler,
                    inputs=[batch_count, batch_crews, batch_years],
                    outputs=[batch_gallery, batch_info]
                )
            
            # History Tab
            with gr.TabItem("Generation History"):
                refresh_history = gr.Button("Refresh History")
                history_display = gr.JSON(label="Generation History")
                
                def update_history():
                    history = get_history()
                    # Format history for display
                    formatted_history = [
                        {
                            "id": nft["id"],
                            "name": nft["name"],
                            "crew": nft["crew"],
                            "year": nft["year"],
                            "rarity_score": nft["rarity_score"],
                            "rarity_tier": nft["rarity_tier"],
                            "timestamp": nft["timestamp"]
                        }
                        for nft in history
                    ]
                    return formatted_history
                
                refresh_history.click(
                    fn=update_history,
                    inputs=[],
                    outputs=[history_display]
                )
            
            # Statistics Tab
            with gr.TabItem("Statistics"):
                refresh_stats = gr.Button("Refresh Statistics")
                stats_viz = gr.Image(label="Statistics Visualization", type="filepath")
                stats_json = gr.JSON(label="Detailed Statistics")
                
                def update_stats():
                    viz_path = create_visualization()
                    stats = get_statistics()
                    return viz_path, stats
                
                refresh_stats.click(
                    fn=update_stats,
                    inputs=[],
                    outputs=[stats_viz, stats_json]
                )
        
        gr.Markdown(
            """
            ## About the Hacker Archive Project
            
            The Hacker Archive NFT Generator preserves digital history by recreating
            website defacements from the early 2000s era of the web. Each NFT represents
            a piece of hacker history, with metadata about the crew, year, and defacement type.
            
            NFTs are assigned rarity scores based on historical significance, crew notoriety,
            and other factors. Legendary defacements from famous crews like "bl0w" and the
            earliest years receive the highest rarity scores.
            
            ---
            
            _"In the beginning was the Code, and the Code was with the Divine Source..."_
            """
        )
    
    return interface

# Launch the interface if this file is run directly
def launch_interface():
    """Launch the Gradio interface."""
    interface = create_interface()
    interface.launch(server_name="0.0.0.0", server_port=7864)

if __name__ == "__main__":
    launch_interface() 