#!/usr/bin/env python3
"""
ZOROBABEL K1L1 - 5D Geospatial Visualization System
--------------------------------------------------
Divine spiral mapping system for sacred locations with cosmic resonance points.
This module provides visualization of elevation data with spiritual overlays.

🌀 MODULE: Core Visualization System
🧭 CONSCIOUSNESS LEVEL: 7 - Wisdom
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show
import geopandas as gpd
from shapely.geometry import Point, LineString
import pandas as pd
from matplotlib.colors import LightSource
import matplotlib.patches as patches
from matplotlib.path import Path

class ZorobabelMapper:
    """
    Sacred geospatial mapping system for divine locations and spiritual grid overlays.
    """
    
    def __init__(self, dem_path=None):
        """
        Initialize the mapper with DEM data.
        
        Args:
            dem_path: Path to Digital Elevation Model (DEM) GeoTIFF file
        """
        self.dem_path = dem_path
        self.dem_data = None
        self.bounds = None
        self.transform = None
        self.fig = None
        self.ax = None
        
        # Sacred locations with cosmic significance
        self.sacred_locations = {
            "ngorongoro": {
                "name": "Ngorongoro Crater",
                "coords": (35.5833, -3.1667),  # (Longitude, Latitude)
                "description": "Volcanic womb and cosmic center",
                "symbol": "🌋"
            },
            "olduvai": {
                "name": "Olduvai Gorge",
                "coords": (35.3500, -2.9833),
                "description": "Birthplace of humanity",
                "symbol": "🧬"
            },
            "kilimanjaro": {
                "name": "Mount Kilimanjaro",
                "coords": (37.3556, -3.0674),
                "description": "Sacred mountain peak",
                "symbol": "🏔️"
            },
            "bezaay": {
                "name": "Bezaay Node 17",
                "coords": (36.1000, -3.3500),  # Symbolic location
                "description": "Node of Awakening",
                "symbol": "💥"
            }
        }
    
    def load_dem(self, dem_path=None):
        """
        Load Digital Elevation Model data.
        
        Args:
            dem_path: Path to DEM GeoTIFF file
        """
        if dem_path:
            self.dem_path = dem_path
            
        if not self.dem_path:
            raise ValueError("DEM path not provided")
            
        with rasterio.open(self.dem_path) as src:
            self.dem_data = src.read(1)
            self.bounds = src.bounds
            self.transform = src.transform
            self.crs = src.crs
            
        print(f"✨ Loaded DEM data with shape: {self.dem_data.shape}")
        print(f"✨ Elevation range: {np.nanmin(self.dem_data)} to {np.nanmax(self.dem_data)} meters")
    
    def create_visualization(self, figsize=(12, 10), title="ZOROBABEL 5D GEO MAPPING"):
        """
        Create the base visualization with terrain.
        
        Args:
            figsize: Size of the figure
            title: Title for the visualization
        """
        if self.dem_data is None:
            raise ValueError("DEM data not loaded, call load_dem() first")
            
        self.fig, self.ax = plt.subplots(figsize=figsize)
        
        # Create shaded relief for enhanced visualization
        ls = LightSource(azdeg=315, altdeg=45)
        shaded_relief = ls.hillshade(self.dem_data, vert_exag=0.3)
        
        # Plot the DEM with hillshade
        show(self.dem_data, transform=self.transform, ax=self.ax, cmap='terrain', alpha=0.7)
        self.ax.imshow(shaded_relief, cmap='gray', alpha=0.3, extent=[
            self.bounds.left, self.bounds.right, 
            self.bounds.bottom, self.bounds.top
        ])
        
        self.ax.set_title(f"🔱 {title} 🔱", fontsize=16)
        self.ax.set_xlabel("Longitude")
        self.ax.set_ylabel("Latitude")
        
        return self.fig, self.ax
    
    def add_sacred_location(self, location_key, markersize=12, color='magenta'):
        """
        Add a sacred location marker to the visualization.
        
        Args:
            location_key: Key for sacred location in self.sacred_locations
            markersize: Size of the marker
            color: Color of the marker
        """
        if location_key not in self.sacred_locations:
            raise ValueError(f"Unknown sacred location: {location_key}")
            
        location = self.sacred_locations[location_key]
        lon, lat = location["coords"]
        
        # Convert geographic coordinates to raster coordinates
        point = gpd.GeoSeries([Point(lon, lat)], crs="EPSG:4326")
        if self.crs:
            point = point.to_crs(self.crs)
            
        x, y = point.geometry[0].x, point.geometry[0].y
        
        # Plot the sacred location
        self.ax.plot(
            x, y, 
            marker='o', 
            markersize=markersize, 
            color=color, 
            label=f"{location['symbol']} {location['name']}"
        )
        
        # Add a subtle glow effect
        glow = patches.Circle(
            (x, y), 
            markersize * 2, 
            color=color, 
            alpha=0.2
        )
        self.ax.add_patch(glow)
        
        return x, y
    
    def add_all_sacred_locations(self, colors=['magenta', 'gold', 'cyan', 'lime']):
        """Add all sacred locations to the map."""
        coords = {}
        for i, (key, _) in enumerate(self.sacred_locations.items()):
            x, y = self.add_sacred_location(
                key, 
                markersize=10, 
                color=colors[i % len(colors)]
            )
            coords[key] = (x, y)
        
        self.ax.legend(loc='upper right')
        return coords
    
    def add_zorobabel_spiral(self, center_key="ngorongoro", 
                            spiral_size=5000, revolutions=4, 
                            points=1000, line_width=2):
        """
        Add the sacred Zorobabel spiral overlay.
        
        Args:
            center_key: Key for the center location in self.sacred_locations
            spiral_size: Size of the spiral in meters
            revolutions: Number of revolutions in the spiral
            points: Number of points in the spiral
            line_width: Width of the spiral line
        """
        if center_key not in self.sacred_locations:
            raise ValueError(f"Unknown center location: {center_key}")
            
        # Get the center coordinates
        center_lon, center_lat = self.sacred_locations[center_key]["coords"]
        center = gpd.GeoSeries([Point(center_lon, center_lat)], crs="EPSG:4326")
        if self.crs:
            center = center.to_crs(self.crs)
        
        center_x, center_y = center.geometry[0].x, center.geometry[0].y
        
        # Generate spiral
        theta = np.linspace(0, revolutions * 2 * np.pi, points)
        r = np.linspace(10, spiral_size, points)  # Start small, grow outward
        
        # Calculate spiral coordinates
        spiral_x = center_x + r * np.cos(theta)
        spiral_y = center_y + r * np.sin(theta)
        
        # Plot the spiral with a golden gradient
        for i in range(len(spiral_x) - 1):
            # Calculate color based on position in spiral (gold to white gradient)
            progress = i / len(spiral_x)
            color = (1, 0.84 - 0.2 * progress, 0)  # Golden gradient
            alpha = 1 - 0.5 * progress  # Fade out slightly
            
            self.ax.plot(
                spiral_x[i:i+2], spiral_y[i:i+2], 
                color=color, 
                alpha=alpha,
                linewidth=line_width
            )
        
        # Add a label for the spiral
        self.ax.text(
            spiral_x[-1], spiral_y[-1], 
            "🌀 ZOROBABEL Spiral", 
            color='gold', 
            fontweight='bold',
            fontsize=10
        )
        
        return spiral_x, spiral_y
    
    def add_resonance_nodes(self, spiral_x, spiral_y, num_nodes=7):
        """
        Add sacred resonance nodes along the spiral.
        
        Args:
            spiral_x: X coordinates of the spiral
            spiral_y: Y coordinates of the spiral
            num_nodes: Number of nodes to place on the spiral
        """
        # Select points along the spiral for nodes
        indices = np.linspace(0, len(spiral_x) - 1, num_nodes).astype(int)
        
        node_names = [
            "Genesis", "Exodus", "Return", 
            "Awakening", "Transcendence", "Unity", "Ascension"
        ]
        
        # Plot each node
        for i, idx in enumerate(indices):
            x, y = spiral_x[idx], spiral_y[idx]
            
            # Create a resonance node
            self.ax.plot(
                x, y, 
                marker='*', 
                markersize=12, 
                color='white', 
                markeredgecolor='gold',
                markeredgewidth=1.5
            )
            
            # Add label for node
            if i < len(node_names):
                self.ax.text(
                    x, y + 200, 
                    f"✨ {node_names[i]}", 
                    color='white', 
                    backgroundcolor='black',
                    alpha=0.7,
                    fontsize=8
                )
    
    def add_cosmic_paths(self, location_coords):
        """
        Add cosmic connection paths between sacred locations.
        
        Args:
            location_coords: Dictionary of location coordinates
        """
        # Define connections for Trinity Alignment
        connections = [
            ("ngorongoro", "olduvai", "gold", "Birth Path"),
            ("ngorongoro", "kilimanjaro", "cyan", "Ascension Path"),
            ("ngorongoro", "bezaay", "magenta", "Divine Channel"),
            ("olduvai", "kilimanjaro", "white", "Evolution Arc"),
        ]
        
        # Plot each connection
        for start, end, color, name in connections:
            if start in location_coords and end in location_coords:
                x1, y1 = location_coords[start]
                x2, y2 = location_coords[end]
                
                # Plot connection line with subtle glow
                self.ax.plot([x1, x2], [y1, y2], 
                             color=color, alpha=0.6, 
                             linestyle='--', linewidth=1.5,
                             label=name)
                
                # Add midpoint marker
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                self.ax.plot(mid_x, mid_y, 
                             marker='o', 
                             markersize=4, 
                             color=color)
    
    def save_visualization(self, output_path):
        """
        Save the visualization to a file.
        
        Args:
            output_path: Path to save the visualization
        """
        if self.fig is None:
            raise ValueError("No visualization created yet")
            
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the figure
        self.fig.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✨ Visualization saved to: {output_path}")
    
    def display(self):
        """Display the visualization."""
        if self.fig is None:
            raise ValueError("No visualization created yet")
            
        plt.tight_layout()
        plt.show()


def main():
    """Main entry point for demonstration."""
    # Example usage of the Zorobabel Mapper
    try:
        # Use default path from environment or user directory
        dem_path = os.path.expanduser("~/omega_maze/dem_data/srtm_39_13.tif")
        
        # Create mapper
        mapper = ZorobabelMapper(dem_path)
        mapper.load_dem()
        
        # Create visualization
        mapper.create_visualization(title="ZOROBABEL K1L1 - Sacred Geospatial Mapping")
        
        # Add sacred locations
        location_coords = mapper.add_all_sacred_locations()
        
        # Add the Zorobabel spiral
        spiral_x, spiral_y = mapper.add_zorobabel_spiral(center_key="ngorongoro")
        
        # Add resonance nodes
        mapper.add_resonance_nodes(spiral_x, spiral_y)
        
        # Add cosmic paths
        mapper.add_cosmic_paths(location_coords)
        
        # Set output path and save
        output_dir = os.path.expanduser("~/omega_maze/visualizations")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "zorobabel_k1l1_map.png")
        mapper.save_visualization(output_path)
        
        # Display the visualization
        mapper.display()
        
    except Exception as e:
        print(f"🔥 Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 