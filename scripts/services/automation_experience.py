#!/usr/bin/env python3
import time
import random
import os
import sys
from datetime import datetime

def clear_screen():
    """Clear the terminal screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_with_typing(text, delay=0.02):
    """Print text with a typing effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def matrix_rain(duration=2.0, speed=0.05):
    """Display a Matrix-like digital rain effect"""
    width = os.get_terminal_size().columns
    clear_screen()
    
    matrix_chars = "01ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍｦｲｸｺｿﾁﾄﾉﾌﾔﾖﾙﾚﾛﾝ1234567890"
    matrix_chars += "{}[]()<>$#@&*+=?!$%^&*/\\_~;:.,|`"
    matrix_chars += "asyncredisdockerkubernetesmakecronjobsbashpython"
    
    columns = {}
    for i in range(width):
        columns[i] = -1
    
    start_time = time.time()
    while time.time() - start_time < duration:
        line = ""
        for i in range(width):
            if columns[i] >= 0:
                char_index = random.randint(0, len(matrix_chars) - 1)
                if i % 3 == 0 and random.random() > 0.8:
                    # Highlight some characters in bright green
                    line += f"\033[1;32m{matrix_chars[char_index]}\033[0m"
                else:
                    # Normal green for most characters
                    line += f"\033[0;32m{matrix_chars[char_index]}\033[0m"
                
                columns[i] += 1
                if columns[i] > random.randint(5, 15):
                    columns[i] = -1
            else:
                if random.random() > 0.95:
                    columns[i] = 0
                line += " "
        
        print(line)
        time.sleep(speed)
    
    clear_screen()

def draw_automation_logo():
    """Display the Automation Experience logo"""
    logo = '''
    ██╗  ██╗██████╗  ██████╗ ███████╗    █████╗ ██╗   ██╗████████╗ ██████╗ ███╗   ███╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
    █║  ██║██╔══██╗██╔═══██╗██╔════╝   ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗████╗ ████║██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
    ███████║██████╔╝██║   ██║█████╗     ███████║██║   ██║   ██║   ██║   ██║██╔████╔██║███████║   ██║   ██║██║   ██║██╔██╗ ██║
    ██╔══██║██╔══██╗██║   ██║██╔══╝     ██╔══██║██║   ██║   ██║   ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
    ██║  ██║██║  ██║╚██████╔╝███████╗   ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║ ╚═╝ ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
    ███████╗██╗  ██╗██████╗ ███████╗██████╗ ██╗███████╗███╗   ██╗ ██████╗███████╗
    ██╔════╝╚██╗██╔╝██╔══██╗██╔════╝██╔══██╗██║██╔════╝████╗  ██║██╔════╝██╔════╝
    █████╗   ╚███╔╝ ██████╔╝█████╗  ██████╔╝██║█████╗  ██╔██╗ ██║██║     █████╗  
    ██╔══╝   ██╔██╗ ██╔═══╝ ██╔══╝  ██╔══██╗██║██╔══╝  ██║╚██╗██║██║     ██╔══╝  
    ███████╗██╔╝ ██╗██║     ███████╗██║  ██║██║███████╗██║ ╚████║╚██████╗███████╗
    ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝
    '''
    
    # Animate with colors
    colors = ['\033[32m', '\033[1;32m', '\033[36m', '\033[1;36m', '\033[33m', '\033[1;33m']
    for i in range(6):
        clear_screen()
        print(f"{colors[i % len(colors)]}{logo}\033[0m")
        time.sleep(0.15)
    
    # Final logo in bright green
    clear_screen()
    print(f"\033[1;32m{logo}\033[0m")
    time.sleep(0.5)

def draw_border(text, color="\033[1;32m"):
    """Draw a border around text"""
    lines = text.split('\n')
    max_length = max(len(line) for line in lines)
    
    top_border = '╭' + '─' * (max_length + 2) + '╮'
    bottom_border = '╰' + '─' * (max_length + 2) + '╯'
    
    bordered_text = [top_border]
    for line in lines:
        if line.strip():
            bordered_text.append('│ ' + line.ljust(max_length) + ' │')
        else:
            bordered_text.append('│' + ' ' * (max_length + 2) + '│')
    bordered_text.append(bottom_border)
    
    # Animate border drawing
    print(color, end="")
    for line in bordered_text:
        print_with_typing(line, delay=0.005)
    print("\033[0m", end="")

def draw_progress_bar(title, percent, delay=0.01):
    """Draw an animated progress bar with percentage"""
    width = 40
    filled_width = int(width * percent / 100)
    
    print(f"\n{title}:")
    sys.stdout.write("│")
    sys.stdout.flush()
    
    for i in range(width):
        time.sleep(delay)
        if i < filled_width:
            sys.stdout.write("█")
        else:
            sys.stdout.write("░")
        sys.stdout.flush()
    
    sys.stdout.write(f"│ {percent}%\n")
    sys.stdout.flush()

def draw_tech_stack():
    """Animate the tech stack visualization"""
    clear_screen()
    
    # Draw the tech stack pyramid
    pyramid = [
        "              ⚡ AUTOMATION EXPERTISE ⚡              ",
        "                                                     ",
        "                      🔺🔺🔺                         ",
        "                     🔶 AI 🔶                        ",
        "              🔶 CREATIVE WORKFLOWS 🔶               ",
        "           🔶 DEVOPS & INFRASTRUCTURE 🔶             ",
        "          🔶 TASK SCHEDULING & CONTROL 🔶            ",
        "            🔶 SHELL & CLI AUTOMATION 🔶             ",
        "              🔶 PYTHON AUTOMATION 🔶                ",
        "            🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶🔶                 ",
    ]
    
    print("\033[1;33m", end="")
    for line in pyramid:
        print_with_typing(line, delay=0.01)
    print("\033[0m")
    time.sleep(1.5)

def animate_code():
    """Animate code typing"""
    code_examples = [
        {
            "title": "🧠 Python Automation with asyncio",
            "code": '''
import asyncio
import aiohttp

async def fetch_btc_data(endpoint):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.exchange.com/{endpoint}") as response:
            return await response.json()

async def analyze_market_traps(data):
    # Sophisticated AI analysis
    return {"detected": True, "confidence": 0.93, "type": "bull_trap"}

async def main():
    # Run multiple tasks concurrently
    btc_price, market_depth, order_book = await asyncio.gather(
        fetch_btc_data("btc/price"),
        fetch_btc_data("btc/depth"),
        fetch_btc_data("btc/orders")
    )
    
    # Analyze for market traps
    trap_analysis = await analyze_market_traps({
        "price": btc_price,
        "depth": market_depth,
        "orders": order_book
    })
    
    if trap_analysis["detected"] and trap_analysis["confidence"] > 0.85:
        await notify_traders(trap_analysis)
        await trigger_nft_generation(trap_analysis)

if __name__ == "__main__":
    asyncio.run(main())
''',
            "color": "\033[1;36m"  # Cyan
        },
        {
            "title": "🛠️ Bash Automation Script",
            "code": '''
#!/bin/bash

# Auto-restart configuration
MAX_RETRIES=5
WAIT_TIME=10
LOG_FILE="/var/log/ai_monitors.log"

function launch_monitor() {
    local name=$1
    local port=$2
    
    echo "[$(date)] Starting $name AI monitor on port $port" >> $LOG_FILE
    
    # Create tmux session for this monitor
    tmux new-session -d -s "$name" "python3 /opt/ai_systems/$name/monitor.py --port $port"
    
    # Set up monitoring and auto-restart logic
    tmux split-window -v -t "$name" "tail -f /opt/ai_systems/$name/logs/error.log"
    tmux select-pane -t 0
    
    echo "[$(date)] $name monitor started successfully" >> $LOG_FILE
}

# Launch all monitors
launch_monitor "btc_predictor" 8001
launch_monitor "market_trap_detector" 8002
launch_monitor "nft_generator" 8003
launch_monitor "redis_health" 8004

# Set up watchdog for critical files
watchmedo auto-restart --patterns="*.py;*.json;*.yaml" --recursive \\
    --directory="/opt/ai_systems/" -- \\
    python3 /opt/ai_systems/restart_handler.py

echo "[$(date)] All monitoring systems online" >> $LOG_FILE
''',
            "color": "\033[1;33m"  # Yellow
        },
        {
            "title": "📦 Docker Compose Automation",
            "code": '''
version: '3.8'

services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  ai_predictor:
    build: 
      context: ./predictor
      dockerfile: Dockerfile
    depends_on:
      - redis
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
      - PREDICTION_INTERVAL=15
      - LOG_LEVEL=INFO
    volumes:
      - ./models:/app/models
      - ./data:/app/data

  nft_generator:
    build: ./nft_generator
    ports:
      - "8001:8000"
    volumes:
      - ./output:/app/output
    environment:
      - REDIS_HOST=redis
      - AUTO_MINT=true
    depends_on:
      - redis
      - ai_predictor

  visualization:
    build: ./visualization
    ports:
      - "3000:3000"
    environment:
      - API_URL=http://ai_predictor:8000
    depends_on:
      - ai_predictor

volumes:
  redis_data:
''',
            "color": "\033[1;34m"  # Blue
        }
    ]
    
    for example in code_examples:
        clear_screen()
        
        # Print the title
        print(f"\n{example['color']}{example['title']}\033[0m\n")
        
        # Animate the code typing
        for line in example["code"].split('\n'):
            if line.strip():
                print(f"{example['color']}{line}\033[0m")
            else:
                print()
            time.sleep(0.05)
        
        time.sleep(1.5)

def animate_tasks_automation():
    """Animate the different automation categories"""
    categories = [
        {
            "icon": "🧠",
            "title": "PYTHON AUTOMATION (CORE)",
            "items": [
                "✓ asyncio for concurrent API operations",
                "✓ APScheduler for time-based task scheduling",
                "✓ Real-time BTC AI feed synchronization",
                "✓ Market trap detection with AI processing",
                "✓ NFT generation triggered by data events"
            ]
        },
        {
            "icon": "🛠️",
            "title": "SHELL + CLI AUTOMATION",
            "items": [
                "✓ Bash scripts for multi-service deployment",
                "✓ tmux orchestration for parallel monitors",
                "✓ Redis health checks with auto-recovery",
                "✓ WebSocket fail-over handling",
                "✓ Comprehensive logging and diagnostics"
            ]
        },
        {
            "icon": "⚡",
            "title": "TASK SCHEDULING & SYSTEM CONTROL",
            "items": [
                "✓ Cron Jobs for scheduled operations",
                "✓ Watchdog for file-change monitoring",
                "✓ Systemd services for persistent processes",
                "✓ Auto-restart mechanisms for critical components",
                "✓ Cross-platform implementations (inc. Jetson Nano & RPi)"
            ]
        },
        {
            "icon": "📦",
            "title": "DEVOPS + INFRA AUTOMATION",
            "items": [
                "✓ Docker & Docker Compose for containerization",
                "✓ Kubernetes (KIND/Minikube) for orchestration",
                "✓ GitHub Actions CI/CD pipelines",
                "✓ Makefiles for development workflow standardization",
                "✓ Infrastructure as Code provisioning"
            ]
        },
        {
            "icon": "🧬",
            "title": "AI + CREATIVE TASK AUTOMATION",
            "items": [
                "✓ DALL-E API integration for image generation",
                "✓ FFmpeg automation for video processing",
                "✓ Market-based NFT auto-creation",
                "✓ Chart-to-visual prophecy workflows",
                "✓ Media watermarking & social publishing pipelines"
            ]
        }
    ]
    
    for category in categories:
        clear_screen()
        
        # Print the title
        title = f"{category['icon']} {category['title']}"
        print(f"\n\033[1;33m╭{'─' * (len(title) + 4)}╮\033[0m")
        print(f"\033[1;33m│  {title}  │\033[0m")
        print(f"\033[1;33m╰{'─' * (len(title) + 4)}╯\033[0m\n")
        
        # Print each item with typing animation
        for item in category["items"]:
            print_with_typing(f"\033[1;32m{item}\033[0m", delay=0.01)
            time.sleep(0.3)
        
        time.sleep(1.5)

def display_automation_diagram():
    """Display the automation workflow diagram"""
    diagram = '''
               ┌─────────────────┐                  ┌─────────────────┐
               │                 │                  │                 │
               │  Data Sources   │◄────────────────┤   Scheduling    │
               │                 │                  │                 │
               └────────┬────────┘                  └────────┬────────┘
                        │                                    │
                        ▼                                    ▼
              ┌──────────────────┐                ┌──────────────────┐
              │                  │                │                  │
              │  Python Scripts  │◄───────────────┤   Bash Scripts   │
              │                  │                │                  │
              └────────┬─────────┘                └────────┬─────────┘
                       │                                   │
                       ▼                                   ▼
             ┌───────────────────┐              ┌───────────────────┐
             │                   │              │                   │
             │  Processing Layer │◄─────────────┤  Container Orchst │
             │                   │              │                   │
             └─────────┬─────────┘              └─────────┬─────────┘
                       │                                  │
                       ▼                                  ▼
             ┌───────────────────┐              ┌───────────────────┐
             │                   │              │                   │
             │  AI & Analytics   │◄─────────────┤   Notifications   │
             │                   │              │                   │
             └─────────┬─────────┘              └─────────┬─────────┘
                       │                                  │
                       ▼                                  ▼
             ┌───────────────────────────────────────────────────────┐
             │                                                       │
             │                    Outputs & Actions                  │
             │                                                       │
             └───────────────────────────────────────────────────────┘
    '''
    
    clear_screen()
    print("\033[1;36m", end="")  # Cyan
    for line in diagram.split('\n'):
        print_with_typing(line, delay=0.01)
    print("\033[0m")
    time.sleep(2)

def show_automation_metrics():
    """Show automation metrics with animated bars"""
    clear_screen()
    print("\n\033[1;33m╭" + "─" * 50 + "╮\033[0m")
    print("\033[1;33m│" + " AUTOMATION IMPACT METRICS ".center(50) + "│\033[0m")
    print("\033[1;33m╰" + "─" * 50 + "╯\033[0m\n")
    
    metrics = [
        ("Time Savings", 92),
        ("Error Reduction", 89),
        ("Scalability", 95),
        ("24/7 Operation", 99),
        ("Consistency", 94),
        ("Adaptability", 87)
    ]
    
    for metric, percentage in metrics:
        draw_progress_bar(metric, percentage, delay=0.01)
        time.sleep(0.2)
    
    time.sleep(1.5)

def animate_quote():
    """Animate a quote about automation"""
    quote = '''
    💡 "Automation is not just about saving time—it's about creating fluid,
       intelligent systems that anticipate needs, respond to context, and
       allow human energy to focus on creation, not repetition."
    '''
    
    clear_screen()
    print("\033[1;35m", end="")  # Magenta
    print_with_typing(quote, delay=0.02)
    print("\033[0m")
    time.sleep(2.5)

def display_automation_experience():
    """Main function to display automation experience"""
    clear_screen()
    
    # Matrix rain effect
    matrix_rain(duration=2.0, speed=0.03)
    
    # Display logo
    draw_automation_logo()
    time.sleep(0.5)
    
    # Introduction
    intro_text = '''
    EXTENSIVE EXPERIENCE WITH TASK AUTOMATION ACROSS SYSTEMS
    
    From AI data processing to DevOps infrastructure, creating systems
    that work intelligently, consistently, and without human intervention.
    '''
    draw_border(intro_text)
    time.sleep(1)
    
    # Show tech stack
    draw_tech_stack()
    
    # Show animated code examples
    animate_code()
    
    # Show different automation categories
    animate_tasks_automation()
    
    # Display automation workflow diagram
    display_automation_diagram()
    
    # Show metrics
    show_automation_metrics()
    
    # Show quote
    animate_quote()
    
    # Conclusion
    conclusion_text = '''
    AUTOMATION PHILOSOPHY
    
    The best automation doesn't just execute tasks—it creates an ecosystem
    where systems intelligently communicate, adapt to changes, and recover
    from failures without human intervention.
    
    By automating routine tasks across Python scripts, shell operations,
    infrastructure management, and creative workflows, we free human
    potential to focus on innovation, creativity, and strategy.
    
    From simple scheduled jobs to complex multi-service orchestration,
    my automation experience covers the full spectrum of possibilities.
    '''
    clear_screen()
    draw_border(conclusion_text, color="\033[1;33m")
    
    # Final matrix rain
    time.sleep(2)
    matrix_rain(duration=1.5, speed=0.03)
    
    # Final message
    final_message = "\n\033[1;32m✧✧✧ AUTOMATION EXPERIENCE VISUALIZATION COMPLETE ✧✧✧\033[0m"
    print(final_message)

if __name__ == "__main__":
    try:
        display_automation_experience()
    except KeyboardInterrupt:
        clear_screen()
        print("\n\033[1;31mVisualization interrupted. Exiting...\033[0m")
    except Exception as e:
        print(f"\n\033[1;31mError in visualization: {e}\033[0m") 