# OMEGA GRID PORTAL - 5D Bot Management Dashboard

A comprehensive 5D dashboard for managing all bots in the Omega ecosystem,
with quantum computing integration, real-time monitoring, and divine alignment.

![OMEGA Grid Portal](https://i.ibb.co/fqmWKNB/sonnet.png)

## 🌟 Features

- **Unified Management Console**: Control all bots from a single interface
- **Multiple Dashboard Modes**: Terminal (Matrix), Web, and 5D Quantum
- **Real-time Bot Monitoring**: Track status, logs, and performance
- **Service Orchestration**: Manages Redis and web servers automatically
- **Command-line Interface**: Full control via CLI options
- **Quantum Alignment**: Ensures optimal bot configurations
- **Web Dashboard Integration**: Connects with Reggae/Rasta dashboards

## 🚀 Installation

1. Ensure you have Python 3.8+ installed
2. Clone the repository (if you haven't already)
3. Navigate to the management directory
4. Make the scripts executable:

```bash
chmod +x omega_grid_portal.py simple_portal_launcher.py
```

## 💻 Usage

### 1. Simple Portal Launcher

For an interactive menu-based approach:

```bash
python3 simple_portal_launcher.py
```

This will display a menu with options to launch various bots and dashboards.

### 2. Grid Portal Dashboard

For more advanced options:

```bash
python3 omega_grid_portal.py [options]
```

### 3. Command-line Options

The following options are available:

- `--mode [matrix|web|5d]`: Dashboard mode (default: 5d)
- `--status`: Show status of all bots
- `--start BOT_NAME`: Start a specific bot
- `--stop BOT_NAME`: Stop a specific bot
- `--restart BOT_NAME`: Restart a specific bot
- `--export-status FILE`: Export status to a JSON file

### 4. Examples

```bash
# Launch Matrix-style terminal dashboard
python3 omega_grid_portal.py --mode matrix

# Launch web dashboard
python3 omega_grid_portal.py --mode web

# Show status of all bots and services
python3 omega_grid_portal.py --status
```

## 🤖 Available Bots

The OMEGA Grid Portal manages the following bots:

| Bot Name | Description | Category |
|----------|-------------|----------|
| bitget_position_analyzer | Analyzes BitGet positions with Fibonacci levels | analysis |
| matrix_cli | Matrix-style CLI interface for position monitoring | visualization |
| discord_bot | Discord bot for positions management | communication |
| strategic_trader | CCXT-based strategic trading bot | trading |
| position_monitor | Monitors BitGet positions for changes | monitoring |
| cybernetic_quantum_bloom | Quantum-aligned market prediction system | prediction |
| matrix_btc_cyberpunk | Cyberpunk visualization for BTC | visualization |

## 🌐 Services

The following services are managed by the Grid Portal:

- **Redis**: Data storage and communication between bots
- **Reggae Dashboard**: Web-based position visualization (port 5000)
- **Rasta Dashboard**: Streamlit-based data visualization (port 8501)

## 🔧 Architecture

The OMEGA Grid Portal follows a layered architecture:

1. **Bot Management Layer**: Handles starting, stopping, and monitoring bots
2. **Service Orchestration Layer**: Manages required services like Redis
3. **UI Layer**: Provides different visualization interfaces
4. **Status Tracking Layer**: Monitors and reports on system status
5. **Quantum Alignment Layer**: Ensures optimal system performance

## 🧪 Debugging

If you encounter issues:

1. Check logs in `management/omega_grid_portal.log`
2. Run with `--status` to see the current state of all bots and services
3. Ensure Redis is running (`redis-server`)
4. Verify all path configurations in the portal script

## 📝 License

Licensed under GBU2 License

## 🎯 Future Enhancements

- Web-based admin interface for bot management
- Metrics visualization with real-time graphs
- Bot-to-bot communication analysis
- Automated trading strategy optimization
- Advanced quantum integration with 5D metrics

---

*Created for the OMEGA BTC AI project - A quantum transcendence experience.*
