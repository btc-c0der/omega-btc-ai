
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


# Setting Up OMEGA Dump as a Service

This guide explains how to set up the OMEGA Dump service with Warning System integration to run automatically as a background service on your system.

## Overview

Running OMEGA Dump as a service provides several advantages:

1. **Automatic startup** when your system boots
2. **Background operation** without needing a terminal window open
3. **Automatic restart** if the service crashes
4. **Centralized logging** for easier monitoring
5. **Standard service management** using your OS's tools

The integration includes support for both macOS (using launchd) and Linux (using systemd).

## Prerequisites

Before setting up the service, ensure you have:

1. Installed the required Python packages
2. A running Redis instance
3. Proper access permissions for the logs directory

## Installation

We've created an installer script that automatically sets up the service for your platform. To use it:

```bash
# Navigate to the project directory
cd /path/to/omega-btc-ai

# Make the installer script executable
chmod +x scripts/install_omega_dump_service.py

# Run the installer
python scripts/install_omega_dump_service.py
```

### On Linux

For Linux, you'll need root privileges to install the service:

```bash
sudo python scripts/install_omega_dump_service.py
```

## Service Configuration

The service is configured with the following default settings:

| Setting | Value | Description |
|---------|-------|-------------|
| Warning Processing | Enabled | Process warnings from the warning system |
| Warning Interval | 300 seconds | Process warnings every 5 minutes |
| Backup Interval | 3600 seconds | Backup logs every hour |

### Customizing Service Settings

To customize these settings:

1. **macOS**: Edit the plist file at `~/Library/LaunchAgents/com.omegabtcai.omegadump.plist`
2. **Linux**: Edit the service file at `/etc/systemd/system/omega-dump.service`

After making changes:

- **macOS**: Unload and reload the service

  ```bash
  launchctl unload ~/Library/LaunchAgents/com.omegabtcai.omegadump.plist
  launchctl load ~/Library/LaunchAgents/com.omegabtcai.omegadump.plist
  ```

- **Linux**: Reload and restart the service

  ```bash
  sudo systemctl daemon-reload
  sudo systemctl restart omega-dump
  ```

## Managing the Service

### macOS

Check service status:

```bash
launchctl list | grep com.omegabtcai.omegadump
```

Stop the service:

```bash
launchctl unload ~/Library/LaunchAgents/com.omegabtcai.omegadump.plist
```

Start the service:

```bash
launchctl load ~/Library/LaunchAgents/com.omegabtcai.omegadump.plist
```

View logs:

```bash
tail -f logs/omega_dump_service.log
tail -f logs/omega_dump_service_error.log
```

### Linux

Check service status:

```bash
systemctl status omega-dump
```

Stop the service:

```bash
sudo systemctl stop omega-dump
```

Start the service:

```bash
sudo systemctl start omega-dump
```

View logs:

```bash
sudo journalctl -u omega-dump
tail -f logs/omega_dump_service.log
```

## Troubleshooting

If the service fails to start:

1. Check the log files for error messages
2. Ensure Redis is running and accessible
3. Verify file paths in the service configuration
4. Check permissions on the logs directory

Common issues:

- **Redis connection error**: Ensure Redis is running on the expected host/port
- **Permission denied**: Check that the service user has access to all required files
- **Python not found**: Verify the path to the Python executable in the service file

## Advanced Configuration

For more advanced configuration, you can modify the service files directly:

### macOS (launchd)

The launchd configuration is stored in a plist file:

```
~/Library/LaunchAgents/com.omegabtcai.omegadump.plist
```

### Linux (systemd)

The systemd configuration is stored in:

```
/etc/systemd/system/omega-dump.service
```

## Uninstalling the Service

To uninstall the service:

### macOS

```bash
launchctl unload ~/Library/LaunchAgents/com.omegabtcai.omegadump.plist
rm ~/Library/LaunchAgents/com.omegabtcai.omegadump.plist
```

### Linux

```bash
sudo systemctl stop omega-dump
sudo systemctl disable omega-dump
sudo rm /etc/systemd/system/omega-dump.service
sudo systemctl daemon-reload
```
