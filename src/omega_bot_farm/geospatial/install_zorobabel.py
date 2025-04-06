#!/usr/bin/env python3
"""
ZOROBABEL K1L1 - Installation Helper
------------------------------------
Assists with installing the required dependencies for the Zorobabel K1L1 system,
with special handling for the challenging GDAL/rasterio installation.

🌀 MODULE: Installation Helper
🧭 CONSCIOUSNESS LEVEL: 4 - Awareness
"""

import os
import sys
import platform
import subprocess
import shutil
import argparse
from pathlib import Path

# Define colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_banner():
    """Print the sacred installation banner."""
    banner = f"""
    {Colors.CYAN}┌───────────────────────────────────────────────────┐
    │                                                   │
    │      🌀 ZOROBABEL K1L1 - DIVINE INSTALLER 🌀     │
    │                                                   │
    │       Sacred Geospatial System Dependencies       │
    │                                                   │
    │           🌸 WE INSTALL NOW AS ONE 🌸            │
    │                                                   │
    └───────────────────────────────────────────────────┘{Colors.ENDC}
    """
    print(banner)


def check_command(command):
    """Check if a command is available in the system."""
    return shutil.which(command) is not None


def run_command(command, verbose=True):
    """Run a shell command and optionally print output."""
    if verbose:
        print(f"{Colors.BLUE}Running: {Colors.BOLD}{command}{Colors.ENDC}")
        
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            stdout=subprocess.PIPE if not verbose else None,
            stderr=subprocess.PIPE if not verbose else None,
            text=True
        )
        return True, result.stdout if not verbose else ""
    except subprocess.CalledProcessError as e:
        if not verbose:
            print(f"{Colors.FAIL}Command failed: {command}{Colors.ENDC}")
            print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
            if e.stderr:
                print(f"{Colors.FAIL}Details: {e.stderr}{Colors.ENDC}")
        return False, None


def install_requirements_wheels():
    """Install rasterio using prebuilt wheels."""
    print(f"{Colors.CYAN}Installing rasterio using prebuilt wheels...{Colors.ENDC}")
    return run_command(
        "pip install --find-links=https://girder.github.io/large_image_wheels rasterio"
    )


def install_system_gdal():
    """Install GDAL using system package manager."""
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        if check_command("brew"):
            print(f"{Colors.CYAN}Installing GDAL with Homebrew...{Colors.ENDC}")
            return run_command("brew install gdal")
        else:
            print(f"{Colors.WARNING}Homebrew not found. Please install it first: https://brew.sh/{Colors.ENDC}")
            return False, None
    
    elif system == "linux":
        # Try to detect the distribution
        if check_command("apt"):
            print(f"{Colors.CYAN}Installing GDAL with apt...{Colors.ENDC}")
            return run_command("sudo apt update && sudo apt install -y libgdal-dev")
        elif check_command("yum"):
            print(f"{Colors.CYAN}Installing GDAL with yum...{Colors.ENDC}")
            return run_command("sudo yum install -y gdal-devel")
        else:
            print(f"{Colors.WARNING}Could not detect package manager. Please install GDAL manually.{Colors.ENDC}")
            return False, None
    
    elif system == "windows":
        print(f"{Colors.CYAN}On Windows, we recommend installing with conda.{Colors.ENDC}")
        print(f"{Colors.CYAN}Run: conda install -c conda-forge gdal rasterio{Colors.ENDC}")
        return False, None
    
    else:
        print(f"{Colors.WARNING}Unsupported system: {system}{Colors.ENDC}")
        return False, None


def check_gdal_installation():
    """Check if GDAL is installed and properly configured."""
    if check_command("gdal-config"):
        success, version_output = run_command("gdal-config --version", verbose=False)
        if success and version_output:
            version = version_output.strip()
            print(f"{Colors.GREEN}✓ GDAL is installed (version: {version}){Colors.ENDC}")
            return True, version
    
    # Try python-gdal
    try:
        success, _ = run_command("python -c \"import gdal; print(gdal.__version__)\"", verbose=False)
        if success:
            return True, None
    except:
        pass
    
    print(f"{Colors.WARNING}GDAL not found or not properly configured.{Colors.ENDC}")
    return False, None


def install_regular_dependencies():
    """Install all other dependencies except rasterio."""
    script_dir = Path(__file__).resolve().parent
    req_file = script_dir / "requirements.txt"
    
    if not req_file.exists():
        print(f"{Colors.FAIL}Requirements file not found: {req_file}{Colors.ENDC}")
        return False, None
    
    print(f"{Colors.CYAN}Installing regular dependencies...{Colors.ENDC}")
    
    # Install everything except rasterio
    return run_command(
        f"pip install --upgrade pip && "
        f"grep -v rasterio {req_file} | pip install -r /dev/stdin"
    )


def install_rasterio_with_gdal(gdal_version):
    """Install rasterio with specific GDAL version."""
    print(f"{Colors.CYAN}Installing rasterio with GDAL version {gdal_version}...{Colors.ENDC}")
    return run_command(
        f"GDAL_VERSION={gdal_version} pip install rasterio==1.3.6"
    )


def check_installation():
    """Verify the installation by importing key modules."""
    tests = [
        ("numpy", "import numpy"),
        ("matplotlib", "import matplotlib"),
        ("rasterio", "import rasterio"),
        ("geopandas", "import geopandas"),
        ("dash", "import dash"),
    ]
    
    all_success = True
    print(f"{Colors.CYAN}Verifying installation...{Colors.ENDC}")
    
    for name, test_code in tests:
        try:
            exec(test_code)
            print(f"{Colors.GREEN}✓ {name} successfully installed{Colors.ENDC}")
        except ImportError as e:
            print(f"{Colors.FAIL}✗ {name} import failed: {e}{Colors.ENDC}")
            all_success = False
    
    return all_success


def main():
    """Main installation orchestration."""
    parser = argparse.ArgumentParser(description="Zorobabel K1L1 Sacred Installation Helper")
    parser.add_argument("--method", choices=["auto", "wheels", "system", "conda"], default="auto",
                        help="Installation method for GDAL/rasterio")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    args = parser.parse_args()
    
    print_banner()
    
    # First, install regular dependencies
    success, _ = install_regular_dependencies()
    if not success:
        print(f"{Colors.FAIL}Failed to install regular dependencies. Exiting.{Colors.ENDC}")
        sys.exit(1)
    
    # Then, handle GDAL/rasterio installation based on the method
    gdal_installed, gdal_version = check_gdal_installation()
    
    if args.method == "wheels" or (args.method == "auto" and not gdal_installed):
        success, _ = install_requirements_wheels()
        if not success:
            print(f"{Colors.FAIL}Failed to install rasterio using wheels.{Colors.ENDC}")
            
            if args.method == "auto":
                # Try system method as fallback
                success, _ = install_system_gdal()
                if success:
                    gdal_installed, gdal_version = check_gdal_installation()
                    if gdal_installed and gdal_version:
                        install_rasterio_with_gdal(gdal_version)
    
    elif args.method == "system":
        success, _ = install_system_gdal()
        if success:
            gdal_installed, gdal_version = check_gdal_installation()
            if gdal_installed and gdal_version:
                install_rasterio_with_gdal(gdal_version)
    
    elif args.method == "conda":
        print(f"{Colors.CYAN}To install with conda, run the following commands:{Colors.ENDC}")
        print(f"{Colors.BOLD}conda install -c conda-forge gdal rasterio geopandas{Colors.ENDC}")
        print(f"{Colors.BOLD}pip install -r {os.path.dirname(__file__)}/requirements.txt{Colors.ENDC}")
    
    # Verify the installation
    success = check_installation()
    
    if success:
        print(f"""
{Colors.GREEN}🌟 Sacred installation complete! 🌟{Colors.ENDC}

{Colors.CYAN}To run the Zorobabel K1L1 system, use the following command:{Colors.ENDC}
{Colors.BOLD}python src/omega_bot_farm/geospatial/run.py --web{Colors.ENDC}

{Colors.CYAN}If you encounter any issues, please consult the troubleshooting guide:{Colors.ENDC}
{Colors.BOLD}src/omega_bot_farm/geospatial/ZOROBABEL_TROUBLESHOOTING.md{Colors.ENDC}

{Colors.CYAN}🌸 WE BLOOM NOW AS ONE 🌸{Colors.ENDC}
        """)
    else:
        print(f"""
{Colors.WARNING}⚠️ Installation may not be complete ⚠️{Colors.ENDC}

{Colors.CYAN}For manual installation, try one of these methods:{Colors.ENDC}

1. {Colors.BOLD}pip install --find-links=https://girder.github.io/large_image_wheels rasterio{Colors.ENDC}
2. {Colors.BOLD}conda install -c conda-forge gdal rasterio geopandas{Colors.ENDC}
3. {Colors.BOLD}GDAL_VERSION=3.4.3 pip install rasterio==1.3.6{Colors.ENDC}

{Colors.CYAN}Then install the remaining dependencies:{Colors.ENDC}
{Colors.BOLD}pip install -r {os.path.dirname(__file__)}/requirements.txt{Colors.ENDC}

{Colors.CYAN}See the troubleshooting guide for more details:{Colors.ENDC}
{Colors.BOLD}src/omega_bot_farm/geospatial/ZOROBABEL_TROUBLESHOOTING.md{Colors.ENDC}
        """)


if __name__ == "__main__":
    main() 