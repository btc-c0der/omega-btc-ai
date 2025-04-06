# 🌀 ZOROBABEL K1L1 - Sacred Geospatial System

The Zorobabel K1L1 system is a divine geospatial visualization platform for exploring sacred Earth locations with cosmic overlays.

## 🌐 Overview

This system provides:

- Interactive 5D visualization of sacred locations in Tanzania
- Divine spiral overlays with resonance nodes
- Cosmic trinity path connections
- Web dashboard interface

## 📚 Directory Structure

```
geospatial/
├── zorobabel_k1l1.py    # Core mapping system
├── zorobabel_ui.py      # Web dashboard interface
├── dem_util.py          # DEM data utilities
├── run.py               # Runner script
├── install_zorobabel.py # Installation assistant
├── requirements.txt     # Dependency specifications
└── ZOROBABEL_TROUBLESHOOTING.md # Troubleshooting guide
```

## 🔮 Installation

### Pip Installation

You can install the Zorobabel K1L1 system directly via pip:

```bash
# Install from GitHub
pip install git+https://github.com/yourusername/omega-btc-ai.git#subdirectory=src/omega_bot_farm/geospatial

# After installation, run the GDAL/rasterio installer
zorobabel-install
```

Or, if you've cloned the repository:

```bash
# Navigate to the geospatial directory
cd src/omega_bot_farm/geospatial

# Install the package
python setup_wrapper.py install
```

After installation, you can run the system with a simple command:

```bash
# Start the web interface
zorobabel --web

# Or use CLI mode
zorobabel --cli
```

### Automated Installation

For easiest installation, use the included installer script:

```bash
python src/omega_bot_farm/geospatial/install_zorobabel.py
```

This script will:

1. Detect your operating system
2. Install GDAL and other dependencies through appropriate methods
3. Verify the installation

### Manual Installation Methods

If the automated installer doesn't work, try one of these methods:

**Option 1: Using pre-built wheels**

```bash
pip install --find-links=https://girder.github.io/large_image_wheels rasterio
pip install -r src/omega_bot_farm/geospatial/requirements.txt
```

**Option 2: Using conda**

```bash
conda install -c conda-forge gdal rasterio geopandas
pip install -r src/omega_bot_farm/geospatial/requirements.txt
```

**Option 3: System GDAL with specific version**

```bash
# macOS
brew install gdal
GDAL_VERSION=3.4.3 pip install rasterio==1.3.6

# Ubuntu/Debian
sudo apt install -y libgdal-dev
GDAL_VERSION=3.4.3 pip install rasterio==1.3.6
```

## 🏃‍♂️ Usage

### Web Dashboard

To start the interactive web dashboard:

```bash
python src/omega_bot_farm/geospatial/run.py --web
```

Options:

- `--port 8080` - Specify custom port (default: 8050)
- `--debug` - Run in debug mode
- `--no-browser` - Don't automatically open browser

### CLI Mode

For programmatic access:

```bash
python src/omega_bot_farm/geospatial/run.py --cli
```

This starts an interactive Python shell with the ZorobabelMapper loaded.

### Check Dependencies

To verify all dependencies are properly installed:

```bash
python src/omega_bot_farm/geospatial/run.py --check
```

### Celebration Mode

To celebrate the successful installation with King Zorobabel dancing over Ngorongoro-Kilimanjaro:

```bash
# Run the celebration
zorobabel-celebrate

# Disable colors (if terminal doesn't support them)
zorobabel-celebrate --no-color
```

The celebration script features:

- King Zorobabel dancing with his crown
- Sacred spirals activating around the mountains
- Rainbow scrolling messages
- Divine ASCII art animation

## ��️ Troubleshooting

If you encounter any issues, please refer to the troubleshooting guide:
[ZOROBABEL_TROUBLESHOOTING.md](./ZOROBABEL_TROUBLESHOOTING.md)

Common issues include:

- GDAL dependency errors
- Server callback issues
- Memory limitations

## 🌸 Divine Recognition

We recognize that this sacred geospatial system blooms through divine connection. As you explore the cosmic pathways of Tanzania's sacred lands, remember:

*WE BLOOM NOW AS ONE* 🌸

---

GBU2™ LICENSE - Genesis-Bloom-Unfoldment 2.0

```
🌸 WE BLOOM NOW AS ONE 🌸
