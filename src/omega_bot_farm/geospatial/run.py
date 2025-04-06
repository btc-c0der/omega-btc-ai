#!/usr/bin/env python3
"""
ZOROBABEL K1L1 - 5D Geospatial Visualization System - Runner Script
------------------------------------------------------------------
This script provides an easy way to launch the Zorobabel K1L1 visualization
system either in command-line mode or with the web interface.

🌀 MODULE: Runner Script
🧭 CONSCIOUSNESS LEVEL: 4 - Awareness
"""

import os
import sys
import argparse
from pathlib import Path

# Ensure the parent directory is in the path so we can import the geospatial package
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

try:
    from src.omega_bot_farm.geospatial import (
        ZorobabelMapper, 
        ensure_dem_available,
        run_web_interface
    )
except ImportError as e:
    print(f"⚠️ Error importing Zorobabel K1L1 system: {e}")
    print("⚠️ Please ensure all dependencies are installed:")
    print("⚠️ pip install -r requirements.txt")
    sys.exit(1)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="ZOROBABEL K1L1 - 5D Geospatial Visualization System",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--web", 
        action="store_true",
        help="Launch the web interface"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8050,
        help="Port for the web interface (will auto-find if occupied)"
    )
    
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Don't automatically open a browser when starting web interface"
    )
    
    parser.add_argument(
        "--region", 
        type=str, 
        default="ngorongoro",
        choices=["ngorongoro", "olduvai", "kilimanjaro"],
        help="Sacred region to visualize"
    )
    
    parser.add_argument(
        "--revolutions", 
        type=int, 
        default=4,
        help="Number of spiral revolutions"
    )
    
    parser.add_argument(
        "--nodes", 
        type=int, 
        default=7,
        help="Number of resonance nodes"
    )
    
    parser.add_argument(
        "--output", 
        type=str,
        default=os.path.expanduser("~/omega_maze/visualizations/zorobabel_map.png"),
        help="Output path for the visualization image"
    )
    
    parser.add_argument(
        "--no-display", 
        action="store_true",
        help="Don't display the visualization (only save to file)"
    )
    
    return parser.parse_args()


def run_cli_mode(args):
    """Run in command-line mode with direct visualization."""
    print("🌀 ZOROBABEL K1L1 - Sacred Geospatial System 🌀")
    print("-----------------------------------------------")
    
    try:
        # Ensure DEM data is available
        print(f"🌐 Preparing DEM data for Tanzania region...")
        dem_path = ensure_dem_available("tanzania")
        print(f"✅ DEM data ready: {dem_path}")
        
        # Create the mapper
        print(f"🔱 Creating sacred visualization for {args.region}...")
        mapper = ZorobabelMapper(dem_path)
        mapper.load_dem()
        
        # Create visualization with sacred overlays
        title = f"ZOROBABEL K1L1 - {args.region.capitalize()} Sacred Map"
        mapper.create_visualization(title=title)
        
        # Add sacred locations
        print("✨ Adding sacred locations...")
        location_coords = mapper.add_all_sacred_locations()
        
        # Add the Zorobabel spiral
        print(f"🌀 Generating divine spiral with {args.revolutions} revolutions...")
        spiral_x, spiral_y = mapper.add_zorobabel_spiral(
            center_key=args.region,
            revolutions=args.revolutions
        )
        
        # Add resonance nodes
        print(f"💫 Adding {args.nodes} resonance nodes...")
        mapper.add_resonance_nodes(spiral_x, spiral_y, num_nodes=args.nodes)
        
        # Add cosmic paths
        print("🧭 Connecting sacred trinity paths...")
        mapper.add_cosmic_paths(location_coords)
        
        # Save the visualization
        print(f"💾 Saving sacred map to: {args.output}")
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        mapper.save_visualization(args.output)
        
        # Display if requested
        if not args.no_display:
            print("🔮 Displaying sacred map...")
            mapper.display()
        
        print("\n🌸 WE BLOOM NOW AS ONE 🌸")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


def main():
    """Main entry point."""
    args = parse_arguments()
    
    if args.web:
        print("🌐 Launching ZOROBABEL K1L1 web interface...")
        # Pass port and browser preferences to the web interface
        from src.omega_bot_farm.geospatial.zorobabel_ui import main as run_ui
        run_ui(default_port=args.port, auto_open_browser=not args.no_browser)
    else:
        return run_cli_mode(args)


if __name__ == "__main__":
    sys.exit(main()) 