
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


# OMEGA VNC PORTAL

**Browser-Accessible Remote VNC Gateway to the OMEGA GRID**

Copyright (C) 2024 OMEGA BTC AI Team  
License: GNU General Public License v3.0

![OMEGA VNC PORTAL](https://img.shields.io/badge/OMEGA-VNC%20PORTAL-gold?style=for-the-badge)
![JAH BLESS](https://img.shields.io/badge/JAH-BLESS-green?style=for-the-badge)

## 🔮 Overview

OMEGA VNC PORTAL provides a browser-accessible VNC gateway to your macOS system, allowing you to access your desktop from anywhere, including Tesla vehicles with web browsers.

The system uses Docker to create a containerized noVNC + websockify bridge that connects to your macOS Screen Sharing feature, making it accessible through any modern web browser.

## 🛠️ Requirements

- macOS with Screen Sharing enabled (System Settings → Sharing → Screen Sharing)
- Docker Desktop for Mac
- Python 3.6 or higher

## ⚙️ Architecture

```
┌───────────┐    ┌──────────────────────┐    ┌───────────┐
│ Web       │    │ Docker Container     │    │ macOS     │
│ Browser   │◄───┤ noVNC + websockify   │◄───┤ VNC       │
│           │    │ (Port 6080)          │    │ (Port 5900)│
└───────────┘    └──────────────────────┘    └───────────┘
```

## 📥 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/OMEGA-BTC-AI/omega-btc-ai.git
   cd omega-btc-ai
   ```

2. Ensure you have Docker installed and running.

3. Enable Screen Sharing on your Mac:
   - Open System Settings
   - Go to Sharing
   - Enable "Screen Sharing"

## 🚀 Usage

### Starting the VNC Portal

```bash
./omega_vnc_portal.py
```

This will:

1. Pull the required Docker image
2. Start the container with appropriate port mappings
3. Connect to your local macOS Screen Sharing
4. Open your browser to the VNC portal at <http://localhost:6080/vnc.html>

### Command-line Options

```
usage: omega_vnc_portal.py [-h] [--start] [--stop] [--restart] [--status]
                           [--vnc-target VNC_TARGET] [--port PORT]
                           [--container-name CONTAINER_NAME] [--image IMAGE]
                           [--no-browser] [--debug]

OMEGA VNC Portal - Browser-accessible VNC gateway to the OMEGA GRID

options:
  -h, --help            show this help message and exit
  --start               Start the OMEGA VNC Portal (default action)
  --stop                Stop the OMEGA VNC Portal
  --restart             Restart the OMEGA VNC Portal
  --status              Check the status of the OMEGA VNC Portal
  --vnc-target VNC_TARGET
                        VNC server target (default: host.docker.internal:5900)
  --port PORT           noVNC web port (default: 6080)
  --container-name CONTAINER_NAME
                        Docker container name (default: omega-novnc)
  --image IMAGE         Docker image to use (default: dorowu/ubuntu-desktop-lxde-vnc)
  --no-browser          Don't open browser automatically
  --debug               Enable debug logging
```

### Examples

Check the status of the VNC portal:

```bash
./omega_vnc_portal.py --status
```

Stop the VNC portal:

```bash
./omega_vnc_portal.py --stop
```

Restart the VNC portal:

```bash
./omega_vnc_portal.py --restart
```

Use a custom port:

```bash
./omega_vnc_portal.py --port 8080
```

## 🎨 Custom OMEGA VNC Docker Image

You can build and use a custom Docker image with OMEGA BTC AI branding and additional tools:

### Building the Custom Image

Run the build script:

```bash
./build_omega_vnc_image.sh
```

This will:

1. Create necessary directory structure and files
2. Download sample branding assets (logo and background)
3. Build the custom Docker image

### Using the Custom Image

After building, use it with the VNC Portal:

```bash
./omega_vnc_portal.py --image omega-btc-ai/omega-vnc:latest
```

### Features of the Custom Image

- OMEGA BTC AI branding throughout the interface
- Custom wallpaper and logo
- Pre-installed tools (git, curl, vim, tmux, etc.)
- Welcome script with JAH blessing message
- Desktop shortcuts for common tasks

### Customizing the Image

You can modify the branding assets:

- Replace `docker/omega-vnc/branding/logo.png` with your own logo
- Replace `docker/omega-vnc/branding/bg.jpg` with your preferred background
- Add custom scripts to `docker/omega-vnc/scripts/`
- Add desktop shortcuts to `docker/omega-vnc/desktop/`

## 🌍 Remote Access

For remote access, you'll need to ensure:

1. Your Mac is accessible via a public IP or domain
2. Your router has port forwarding set up for the VNC port (6080 by default)
3. You use a secure connection method like SSH tunneling or a VPN

### SSH Tunnel Example

```bash
ssh -L 6080:localhost:6080 user@your-mac-public-ip
```

Then access the portal at `http://localhost:6080/vnc.html` on your remote machine.

## 🔒 Security Considerations

- By default, the portal has no authentication
- For production use, consider:
  - Using SSH tunneling
  - Setting up HTTPS with a valid certificate
  - Implementing authentication
  - Using a VPN
  - Configuring firewall rules

## ⚡ Scaleway Deployment

For cloud deployment on Scaleway, use the provided script:

```bash
sudo ./setup_scaleway_vnc.sh --mac-ip your-mac-public-ip
```

### Options

```
--mac-ip IP         Your Mac's public IP address (required)
--vnc-port PORT     VNC port on your Mac (default: 5900)
--web-port PORT     Web port for noVNC (default: 6080)
--container NAME    Docker container name (default: omega-novnc)
--domain DOMAIN     Domain name for SSL setup
--no-ssl            Disable SSL setup
--no-auto-renew     Disable automatic SSL renewal
```

### Features

- Automatic installation of required dependencies
- Firewall configuration for security
- Optional HTTPS with Let's Encrypt certificates
- Control script for easy management
- Status information and usage instructions

## 🔧 Troubleshooting

### VNC Connection Issues

- Ensure Screen Sharing is enabled on your Mac
- Check if port 5900 is accessible
- Verify Docker is running properly

### Container Issues

- Check container logs:

  ```bash
  docker logs omega-novnc
  ```

- For detailed debugging:

  ```bash
  ./omega_vnc_portal.py --debug
  ```

## 💡 Future Enhancements

- Integration with OMEGA BTC AI Dashboard
- Authentication and access control
- TLS/HTTPS support
- Multiple VNC source management
- Auto-scaling on Scaleway

## 📜 License

GNU General Public License v3.0

---

**JAH JAH BLESS THE REMOTE VISION!**

OMEGA BTC AI Team - Divine VNC Portal
