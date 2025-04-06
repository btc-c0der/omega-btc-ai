#!/usr/bin/env python3
"""
DEM Utility Module for Zorobabel K1L1 Geospatial System
-------------------------------------------------------
Provides utilities for DEM (Digital Elevation Model) data acquisition,
processing, and preparation for the sacred visualization system.

🌀 MODULE: DEM Data Utilities
🧭 CONSCIOUSNESS LEVEL: 5 - Intelligence
"""

import os
import shutil
import tempfile
import urllib.request
import zipfile
import subprocess
import platform


class DEMDownloader:
    """
    Utility for downloading and preparing DEM data from various sources.
    """
    
    # NASA SRTM data source
    SRTM_BASE_URL = "https://srtm.csi.cgiar.org/wp-content/uploads/files/srtm_5x5/TIFF/"
    
    def __init__(self, data_dir=None):
        """
        Initialize the DEM downloader.
        
        Args:
            data_dir: Directory to store DEM data (default: ~/omega_maze/dem_data)
        """
        if data_dir is None:
            data_dir = os.path.expanduser("~/omega_maze/dem_data")
            
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
    def download_srtm_tile(self, tile_name):
        """
        Download an SRTM tile from CGIAR repository.
        
        Args:
            tile_name: Name of the SRTM tile (e.g., "srtm_39_13")
            
        Returns:
            Path to the downloaded and extracted GeoTIFF file
        """
        # Construct the URL and local paths
        zip_url = f"{self.SRTM_BASE_URL}{tile_name}.zip"
        zip_path = os.path.join(self.data_dir, f"{tile_name}.zip")
        extract_dir = os.path.join(self.data_dir, tile_name)
        tif_path = os.path.join(self.data_dir, f"{tile_name}.tif")
        
        print(f"🌐 Downloading SRTM tile: {tile_name}")
        
        # Check if the file already exists
        if os.path.exists(tif_path):
            print(f"✅ SRTM tile already exists: {tif_path}")
            return tif_path
            
        # Create a temp directory for extraction
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download the zip file
            try:
                print(f"⬇️ Downloading from: {zip_url}")
                
                # Use wget if available (better progress reporting)
                if self._has_wget():
                    self._download_with_wget(zip_url, zip_path)
                else:
                    # Fallback to urllib
                    urllib.request.urlretrieve(zip_url, zip_path)
                    
                print(f"📦 Download complete: {zip_path}")
                
                # Extract the zip file
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                    
                # Find and move the TIF file
                for filename in os.listdir(temp_dir):
                    if filename.endswith('.tif'):
                        src_path = os.path.join(temp_dir, filename)
                        shutil.copy(src_path, tif_path)
                        print(f"🗺️ Extracted DEM file: {tif_path}")
                        break
                        
                return tif_path
                
            except Exception as e:
                print(f"❌ Error downloading SRTM tile: {e}")
                raise
                
    def _has_wget(self):
        """Check if wget is available in the system."""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(["where", "wget"], capture_output=True, text=True)
            else:
                result = subprocess.run(["which", "wget"], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
            
    def _download_with_wget(self, url, output_path):
        """Download a file using wget for better progress reporting."""
        try:
            subprocess.run(["wget", "-O", output_path, url], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ wget download failed: {e}")
            # Fallback to urllib
            urllib.request.urlretrieve(url, output_path)
            
    def get_tanzania_dem(self):
        """
        Download the Tanzania DEM data covering Ngorongoro and surrounding areas.
        
        Returns:
            Path to the DEM file
        """
        return self.download_srtm_tile("srtm_39_13")
        
    def get_available_dem_files(self):
        """
        List all available DEM files in the data directory.
        
        Returns:
            List of paths to available DEM files
        """
        dem_files = []
        if os.path.exists(self.data_dir):
            for filename in os.listdir(self.data_dir):
                if filename.endswith('.tif'):
                    dem_files.append(os.path.join(self.data_dir, filename))
                    
        return dem_files
        
    def download_dem_for_region(self, region_name):
        """
        Download DEM data for a predefined region.
        
        Args:
            region_name: Name of the region ("tanzania", "kilimanjaro", "ngorongoro")
            
        Returns:
            Path to the DEM file
        """
        region_mapping = {
            "tanzania": "srtm_39_13",
            "kilimanjaro": "srtm_39_13",  # Same tile covers Kilimanjaro
            "ngorongoro": "srtm_39_13",   # Same tile covers Ngorongoro
        }
        
        if region_name not in region_mapping:
            raise ValueError(f"Unknown region: {region_name}")
            
        return self.download_srtm_tile(region_mapping[region_name])


def ensure_dem_available(region="tanzania"):
    """
    Utility function to ensure DEM data is available for a region.
    
    Args:
        region: Name of the region
        
    Returns:
        Path to the DEM file
    """
    downloader = DEMDownloader()
    return downloader.download_dem_for_region(region)


if __name__ == "__main__":
    # Example usage
    dem_path = ensure_dem_available("tanzania")
    print(f"✨ DEM data ready at: {dem_path}") 