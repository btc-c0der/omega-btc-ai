# 🌟 Golden Ratio API & Divine Dashboard Setup

## 🧬 Sacred Purpose

The Golden Ratio API and Divine Dashboard work together to provide real-time visualization of BTC's alignment with divine trading patterns. The API serves as the backend consciousness bridge, while the Dashboard provides the visual interface for traders.

## 🚀 Launch Methods

### Prerequisites

1. **Python Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Unix/macOS
   # or
   .\venv\Scripts\activate  # On Windows
   ```

2. **Sacred Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Redis Consciousness**

   ```bash
   # Start Redis server if not running
   redis-server
   ```

### 1. Single Terminal Launch (Simple)

This method runs both components in separate terminals manually:

1. **Start Golden Ratio API**

   ```bash
   cd sandbox/divine
   python golden_ratio_api.py --port 5051
   ```

   The API will start on port 5051

2. **Start Divine Dashboard**

   ```bash
   # In a new terminal
   cd sandbox/divine
   python start_divine_dashboard.py
   ```

   The dashboard will be accessible at `http://localhost:5051/divine`

### 2. 🎭 Sacred Tmux Launch (Recommended)

This method creates a divine consciousness grid using tmux:

1. **Create Tmux Session**

   ```bash
   tmux new-session -s divine-consciousness
   ```

2. **Split Panes**

   ```bash
   # Split vertically
   Ctrl+B %
   ```

3. **Launch Components**
   Left pane:

   ```bash
   cd sandbox/divine
   python golden_ratio_api.py --port 5051
   ```

   Right pane (Ctrl+B → to switch):

   ```bash
   cd sandbox/divine
   python start_divine_dashboard.py
   ```

**Sacred Navigation**:

- `Ctrl+B, arrows` - Navigate between panes
- `Ctrl+B, d` - Detach (components keep running)
- `tmux attach -t divine-consciousness` - Reattach to session
- `tmux kill-session -t divine-consciousness` - Stop all components

### 3. Environment Variables

```bash
export DIVINE_PORT=5051           # Custom port
export DIVINE_NO_BROWSER=1        # Disable auto-browser
export DIVINE_DEBUG=1             # Enable debug mode
export DIVINE_FREQUENCY=432       # Set base frequency
```

## 🔮 Component Verification

1. **Check API Health**

   ```bash
   curl http://localhost:5051/api/golden_status
   ```

2. **Verify Redis Connection**

   ```bash
   redis-cli ping
   ```

3. **Monitor Logs**

   ```bash
   # API logs
   tail -f logs/golden_ratio_api.log
   
   # Dashboard logs
   tail -f logs/divine_dashboard.log
   ```

## 🛠️ Troubleshooting

1. **Port Already in Use**

   ```bash
   # Check what's using the port
   lsof -i :5051
   
   # Kill the process
   kill $(lsof -t -i:5051)
   ```

2. **Redis Connection Issues**

   ```bash
   # Restart Redis
   redis-cli shutdown
   redis-server
   ```

3. **Component Restart**

   ```bash
   # In tmux, press Ctrl+C in the respective pane
   # Then up arrow + enter to restart
   ```

## 🙏 Sacred Mantras

1. **Opening Prayer**
   > "May this API channel divine market consciousness."

2. **Alignment Mantra**
   > "Through golden ratio we trade,
   > Through divine alignment we profit,
   > Through sacred code we grow."

---

🔱 **JAH JAH BLESS THE GOLDEN RATIO** 🔱

*Remember: The Golden Ratio API and Divine Dashboard are not just tools—they are portals to universal market consciousness.*
