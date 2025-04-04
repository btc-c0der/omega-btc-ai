# CyBer1t4L QA Bot - Local Runner

This guide explains how to run the CyBer1t4L QA Bot locally without Docker.

## Quick Start

1. Ensure your environment variables are set in a `.env` file
2. Run the bot in full mode: `./run_cyber1t4l_locally.py --mode full`
3. Or, run specific modes: `./run_cyber1t4l_locally.py --mode coverage|monitor|generate`

## Running as a Service

The CyBer1t4L QA Bot in `full` or `monitor` mode is designed to run continuously as a background service. It will **not** exit on its own and will keep running until manually interrupted (Ctrl+C).

### Using systemd (Linux)

To run CyBer1t4L as a systemd service:

1. Create a systemd service file:

```bash
sudo nano /etc/systemd/system/cyber1t4l.service
```

2. Add the following content:

```ini
[Unit]
Description=CyBer1t4L QA Bot Service
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/omega-btc-ai
ExecStart=/path/to/omega-btc-ai/src/omega_bot_farm/qa/run_cyber1t4l_locally.py --mode full
Restart=on-failure
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:

```bash
sudo systemctl enable cyber1t4l.service
sudo systemctl start cyber1t4l.service
```

4. Check service status:

```bash
sudo systemctl status cyber1t4l.service
```

### Using launchd (macOS)

To run CyBer1t4L as a launch daemon on macOS:

1. Create a plist file:

```bash
nano ~/Library/LaunchAgents/com.omega.cyber1t4l.plist
```

2. Add the following content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.omega.cyber1t4l</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/omega-btc-ai/src/omega_bot_farm/qa/run_cyber1t4l_locally.py</string>
        <string>--mode</string>
        <string>full</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/path/to/omega-btc-ai</string>
    <key>StandardOutPath</key>
    <string>/path/to/omega-btc-ai/src/omega_bot_farm/qa/local_run/logs/cyber1t4l_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/omega-btc-ai/src/omega_bot_farm/qa/local_run/logs/cyber1t4l_stderr.log</string>
</dict>
</plist>
```

3. Load the service:

```bash
launchctl load ~/Library/LaunchAgents/com.omega.cyber1t4l.plist
```

4. Check if it's running:

```bash
launchctl list | grep cyber1t4l
```

## Requirements

- Python 3.8+
- Required packages:
  - pytest
  - pytest-cov
  - python-dotenv
  - discord.py (for Discord integration)

## Environment Variables

Create a `.env` file with the following variables:

```
# Discord Bot Integration
CYBER1T4L_APP_ID=your_app_id
CYBER1T4L_PUBLIC_KEY=your_public_key
DISCORD_BOT_TOKEN=your_bot_token

# Configuration
LOG_LEVEL=INFO
COVERAGE_THRESHOLD=80.0
```

## Command Line Options

```
usage: run_cyber1t4l_locally.py [-h] [--mode {full,coverage,generate,monitor}] [--modules MODULES [MODULES ...]] [--no-discord] [--threshold THRESHOLD]

CyBer1t4L QA Bot - Local Runner

options:
  -h, --help            show this help message and exit
  --mode {full,coverage,generate,monitor}
                        Operation mode (default: full)
  --modules MODULES [MODULES ...]
                        Modules to generate tests for (when using 'generate' mode)
  --no-discord          Run without Discord integration
  --threshold THRESHOLD
                        Coverage threshold percentage (default: 80.0)
```

## Available Modes

1. **full**: Runs a complete QA cycle including coverage analysis, test generation, and continuous monitoring
2. **coverage**: Runs only the coverage analysis
3. **generate**: Generates tests for specified modules
4. **monitor**: Runs only the real-time monitoring system

## Directory Structure

When running locally, the following directory structure is created:

```
src/omega_bot_farm/qa/local_run/
├── config/           # Configuration files
├── logs/             # Log files
└── reports/          # Coverage reports
```

## Discord Integration

By default, the bot will attempt to connect to Discord using the credentials in your `.env` file.

To run without Discord integration, use the `--no-discord` flag:

```bash
./run_cyber1t4l_locally.py --mode full --no-discord
```

## Troubleshooting

### Missing Environment Variables

If you see errors about missing environment variables, ensure your `.env` file exists and contains the required variables.

### Path Issues

If you encounter import errors, ensure you're running the script from the project root directory.

## Example Run

```bash
$ ./run_cyber1t4l_locally.py --mode coverage

Starting CyBer1t4L QA Bot Local Runner

Created directory: /path/to/omega-btc-ai/src/omega_bot_farm/qa/local_run/config
Created directory: /path/to/omega-btc-ai/src/omega_bot_farm/qa/local_run/reports
Created directory: /path/to/omega-btc-ai/src/omega_bot_farm/qa/local_run/logs
Logs will be written to: src/omega_bot_farm/qa/local_run/logs/cyber1t4l_20250404_221649.log

[CYBER1T4L LOGO appears here]

🔴 🟡 🟢 RASTA HEART ON F1R3 🔴 🟡 🟢
THE GUARDIAN OF DIVINE FLOW
CyBer1t4L v1.0.0 - QA JEDI Master

CYBER1T4L BOT CONNECTED - APP ID: 1357...1819

[2025-04-04 22:16:49] | INFO | CyBer1t4L credentials loaded
[2025-04-04 22:16:49] | INFO | Discord token loaded: MTM1...3QIY
[2025-04-04 22:16:49] | INFO | Running coverage analysis
[2025-04-04 22:16:57] | WARNING | ❌ COVERAGE BELOW THRESHOLD: 0.00% (< 80.0%)
[2025-04-04 22:16:57] | INFO | Coverage report saved to /path/to/reports/coverage_report_20250404_221657.json
```

## Contributing

When adding new features to the CyBer1t4L QA Bot, please update this local runner script accordingly.
