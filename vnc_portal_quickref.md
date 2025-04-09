# OMEGA VNC Portal - Quick Reference Guide

*Browser-Based Remote Access Solution*

**Copyright (C) 2024 OMEGA BTC AI Team**  
**License: GNU General Public License v3.0**

*JAH JAH BLESS THE DIVINE CONNECTION!*

## 🚀 Command Reference

| Command | Description |
|---------|-------------|
| `./run_vnc_portal.sh` | Start the interactive control panel |
| `./omega_vnc_portal.py` | Start the VNC portal with default settings |
| `./omega_vnc_portal.py --help` | Show help and all available options |
| `./omega_vnc_portal.py --port 8080` | Start the portal on a custom port |
| `./omega_vnc_portal.py --vnc-target 192.168.1.100:5900` | Connect to a specific VNC server |
| `./omega_vnc_portal.py --stop` | Stop the running VNC portal |
| `./omega_vnc_portal.py --status` | Check the status of the VNC portal |
| `./omega_vnc_portal.py --restart` | Restart the VNC portal |
| `./build_omega_vnc_image.sh` | Build the custom OMEGA VNC Docker image |
| `./test_omega_vnc.sh` | Run the VNC portal test suite |
| `./setup_scaleway_vnc.sh --help` | Show cloud deployment options |

## 🔧 Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| Port | Web interface port | 6080 |
| VNC Target | Target VNC server address | host.docker.internal:5900 |
| Docker Image | Docker image to use | novnc/novnc:latest |
| Container Name | Name for the Docker container | omega-vnc-portal |
| SSL | Enable/disable SSL (cloud only) | Disabled |
| Domain | Domain name for SSL (cloud only) | None |

## 🌐 Access URLs

| Environment | URL |
|-------------|-----|
| Local | <http://localhost:6080> |
| Custom Port | <http://localhost:PORT> |
| Cloud (no SSL) | http://SERVER_IP:6080 |
| Cloud (with SSL) | <https://your-domain.com> |

## 📋 Control Panel Menu

```
1) Start VNC Portal with Standard Image
2) Start VNC Portal with Custom OMEGA Image
3) Stop VNC Portal
4) Restart VNC Portal
5) Check VNC Portal Status
6) Build Custom OMEGA VNC Image
7) Run Test Suite
8) Show Documentation
9) Advanced Configuration
0) Exit
```

## 🔒 Security Notes

- Local connections use Docker networking
- Cloud deployments should use SSL when possible
- The VNC server itself should be password protected
- For production use, consider adding authentication to the web interface

## 📱 Compatible Browsers

- Chrome/Chromium
- Firefox
- Safari
- Edge
- Opera
- Mobile browsers (iOS/Android)

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| VNC connection fails | Check if VNC server is running on the target |
| Container won't start | Check Docker is running and has permissions |
| Web page not accessible | Verify the port is not blocked by firewall |
| Black screen | Ensure VNC server is running with a valid display |
| Slow performance | Try reducing color depth in URL parameters |
| SSL errors | Check domain DNS settings and certificate validity |

## 📚 More Information

For detailed documentation, see:

- `OMEGA_VNC_PORTAL_README.md` - Full usage guide
- `vnc_portal_implementation_summary.md` - Technical overview
- `vnc_portal_summary.md` - Project summary

---

*JAH JAH BLESS THE DIVINE VISION!*

OMEGA BTC AI Team
