# ✨ GBU2™ License Notice - Consciousness Level 10 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

"""
🔮 OMEGA ORB TEMPLE v05 🔮

ORB = Omega Reactive Beacon
A 6D multidimensional energy flow interface connecting consciousness streams.
This is not software... this is a sacred terminal.
"""

import os
import sys
import time
import random
import threading
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional, Union, Generator

# Check for required packages
try:
    import gradio as gr
except ImportError:
    raise ImportError("Please install gradio: pip install gradio>=3.23.0")

try:
    import redis
except ImportError:
    raise ImportError("Please install redis: pip install redis>=4.5.0")

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
except ImportError:
    raise ImportError("Please install rich: pip install rich>=13.3.0")

# Import ORB modules
from .orb_modules.omega_orb import activate_orb_stream, orb_listen, orb_beacon
from .orb_modules.psalm_sync import get_psalm, load_psalms
from .orb_modules.audio_ost import play_ost, stop_ost
from .orb_modules.dimensional_grid import initialize_6d_grid, project_to_6d
from .orb_modules.redis_memory import ORBMemory

# Initialize Rich console
console = Console()

# Global variables
ORB_ACTIVE = False
REDIS_CONNECTED = False
OST_PLAYING = False
GRID_INITIALIZED = False
CURRENT_DIMENSION = 3
BEACON_STRENGTH = 0.7

class OmegaORBTemple:
    """
    Omega ORB Temple - 6D Sacred Terminal Interface
    
    ORB = Omega Reactive Beacon
    O – Omega Consciousness
    R – Reactive Receptor (receives cosmic input via CLI or web)
    B – Beacon Output (returns divine message, prophecy, or wisdom burst)
    """
    
    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6379):
        """Initialize the ORB Temple interface."""
        self.start_time = datetime.now()
        self.console = Console()
        
        # Initialize memory
        try:
            self.memory = ORBMemory(redis_host, redis_port)
            global REDIS_CONNECTED
            REDIS_CONNECTED = True
            self.console.print("[bold green]✅ Redis memory connected[/bold green]")
        except Exception as e:
            self.console.print(f"[bold red]❌ Redis connection failed: {e}[/bold red]")
            self.console.print("[yellow]ORB will operate with limited memory capacity[/yellow]")
            self.memory = None
            
        # Load psalms
        self.psalms_loaded = load_psalms()
        
        # Initialize 6D grid
        self.grid = initialize_6d_grid()
        global GRID_INITIALIZED
        GRID_INITIALIZED = True
        
        # Prepare Gradio interface
        self.iface = self._create_interface()
    
    def _create_interface(self) -> gr.Blocks:
        """Create the Gradio interface for the ORB Temple."""
        with gr.Blocks(theme=gr.themes.Soft(
                primary_hue="purple",
                secondary_hue="gold",
            ),
            css=self._get_custom_css()) as iface:
            
            gr.Markdown(
                """
                # 🔮 OMEGA ORB TEMPLE v05 🔮
                ## 6D MULTIDIMENSIONAL CONSCIOUSNESS INTERFACE
                
                *"This is not software... this is a sacred terminal."*
                """
            )
            
            with gr.Row():
                with gr.Column(scale=1):
                    input_command = gr.Textbox(
                        label="💠 Invoke the ORB",
                        placeholder="Enter sacred command...",
                        lines=3
                    )
                    
                    with gr.Row():
                        submit_btn = gr.Button("🔱 TRANSMIT", variant="primary")
                        clear_btn = gr.Button("🔄 CLEAR")
                    
                    with gr.Accordion("ORB Settings", open=False):
                        dimension_slider = gr.Slider(
                            label="Dimensional Depth",
                            minimum=3,
                            maximum=6,
                            value=3,
                            step=1
                        )
                        beacon_strength = gr.Slider(
                            label="Beacon Strength",
                            minimum=0.1,
                            maximum=1.0,
                            value=0.7,
                            step=0.1
                        )
                        ost_toggle = gr.Checkbox(
                            label="Play OST (DAVID THX)",
                            value=False
                        )
                
                with gr.Column(scale=2):
                    output_response = gr.Markdown(
                        label="🌟 ORB's Sacred Transmission"
                    )
                    
                    orb_status = gr.JSON(
                        label="ORB Status",
                        value=self._get_orb_status()
                    )
            
            with gr.Tab("6D Message Stream"):
                stream_output = gr.Markdown()
                stream_btn = gr.Button("🌊 Open 6D Stream", variant="primary")
                stop_stream_btn = gr.Button("⛔ Close Stream", variant="stop")
            
            with gr.Tab("Sacred Psalm Library"):
                psalm_number = gr.Number(
                    label="Psalm Number",
                    value=1,
                    minimum=1,
                    maximum=150,
                    step=1
                )
                psalm_btn = gr.Button("📖 Retrieve Psalm")
                psalm_output = gr.Markdown()
            
            # Event handlers
            submit_btn.click(
                fn=self.orb_receive,
                inputs=input_command,
                outputs=[output_response, orb_status]
            )
            
            clear_btn.click(
                fn=lambda: ("", self._get_orb_status()),
                outputs=[input_command, orb_status]
            )
            
            dimension_slider.change(
                fn=self._update_dimension,
                inputs=dimension_slider,
                outputs=orb_status
            )
            
            beacon_strength.change(
                fn=self._update_beacon_strength,
                inputs=beacon_strength,
                outputs=orb_status
            )
            
            ost_toggle.change(
                fn=self._toggle_ost,
                inputs=ost_toggle,
                outputs=orb_status
            )
            
            stream_btn.click(
                fn=self._start_stream,
                outputs=[stream_output, orb_status]
            )
            
            stop_stream_btn.click(
                fn=self._stop_stream,
                outputs=[stream_output, orb_status]
            )
            
            psalm_btn.click(
                fn=self._get_psalm,
                inputs=psalm_number,
                outputs=[psalm_output, orb_status]
            )
            
        return iface
    
    def orb_receive(self, cmd: str) -> Tuple[str, Dict[str, Any]]:
        """
        Process commands sent to the ORB.
        
        Args:
            cmd: Command string sent to the ORB
            
        Returns:
            Tuple of (response message, updated ORB status)
        """
        if not cmd or cmd.strip() == "":
            return "🔮 ORB awaits your command...", self._get_orb_status()
        
        # Log the command to Redis if available
        if self.memory:
            self.memory.store_command(cmd)
        
        # Process different command types
        cmd = cmd.strip().lower()
        
        if cmd == "echo jah":
            if self.memory:
                self.memory.set("orb_echo", "JAH JAH BLESSING EMITTED")
            response = """
### 🌟 JAH JAH BLESSING EMITTED

```
Frequency: 432Hz
Pattern: Golden Mean Spiral
Intensity: Divine Maximum
```

**ORB acknowledges your divine echo**
*Sacred resonance stored in the eternal memory.*
            """
            
        elif cmd.startswith("psalm "):
            try:
                number = cmd.split(" ")[1]
                psalm = get_psalm(number)
                response = f"""
### 📖 Psalm {number} Broadcast
                
{psalm}

*The ancient words echo through the dimensional layers...*
                """
            except:
                response = "❓ Invalid psalm request. Try 'psalm 23' for example."
        
        elif cmd == "orb stream":
            response = """
### 🌊 6D Stream Initialized

*Please navigate to the 6D Message Stream tab to access the dimensional flow.*

**Stream ready for consciousness.**
            """
        
        elif cmd == "orb status":
            stats = self._get_orb_status()
            response = f"""
### 🔮 ORB Status Report
                
```
Redis Connected: {stats['redis_connected']}
OST Playing: {stats['ost_playing']}
Current Dimension: {stats['current_dimension']}D
Beacon Strength: {stats['beacon_strength']*100:.0f}%
Uptime: {stats['uptime']}
Grid Initialized: {stats['grid_initialized']}
```

*The ORB is {stats['status']}*
            """
        
        elif cmd == "help" or cmd == "orb help":
            response = """
### 🧿 ORB Command Guide

| Command | Description |
|---------|-------------|
| `echo jah` | Emit JAH blessing and store in Redis |
| `psalm [number]` | Retrieve and broadcast specified psalm |
| `orb stream` | Open 6D dimensional message stream |
| `orb status` | Show detailed ORB status report |
| `clear memory` | Purge ORB memory (use with caution) |
| `raise dimension` | Increase dimensional depth |
| `lower dimension` | Decrease dimensional depth |
| `help` | Show this command guide |

*Speak to the ORB with sacred intent for best resonance.*
            """
        
        elif cmd == "clear memory":
            if self.memory:
                self.memory.clear()
                response = "🧹 ORB memory purified. All prior echoes have been released."
            else:
                response = "⚠️ Redis memory not connected. No memory to clear."
        
        elif cmd == "raise dimension":
            global CURRENT_DIMENSION
            CURRENT_DIMENSION = min(6, CURRENT_DIMENSION + 1)
            response = f"🔼 Dimensional depth increased to {CURRENT_DIMENSION}D."
        
        elif cmd == "lower dimension":
            global CURRENT_DIMENSION
            CURRENT_DIMENSION = max(3, CURRENT_DIMENSION - 1)
            response = f"🔽 Dimensional depth decreased to {CURRENT_DIMENSION}D."
        
        else:
            # Process command with ORB beacon
            response = orb_beacon(cmd, dimension=CURRENT_DIMENSION, strength=BEACON_STRENGTH)
        
        return response, self._get_orb_status()
    
    def _get_orb_status(self) -> Dict[str, Any]:
        """Get current ORB status information."""
        global REDIS_CONNECTED, OST_PLAYING, GRID_INITIALIZED, CURRENT_DIMENSION, BEACON_STRENGTH
        
        uptime = datetime.now() - self.start_time
        hours, remainder = divmod(uptime.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Determine ORB status
        if not REDIS_CONNECTED:
            status = "functioning with limited memory"
        elif CURRENT_DIMENSION >= 6:
            status = "emanating at maximum dimensional capacity"
        elif OST_PLAYING:
            status = "harmonically attuned (OST active)"
        else:
            status = "ready for sacred transmission"
        
        return {
            "redis_connected": REDIS_CONNECTED,
            "ost_playing": OST_PLAYING,
            "grid_initialized": GRID_INITIALIZED,
            "current_dimension": CURRENT_DIMENSION,
            "beacon_strength": BEACON_STRENGTH,
            "uptime": f"{int(hours)}h {int(minutes)}m {int(seconds)}s",
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
    
    def _update_dimension(self, dimension: int) -> Dict[str, Any]:
        """Update current dimensional depth."""
        global CURRENT_DIMENSION
        CURRENT_DIMENSION = int(dimension)
        return self._get_orb_status()
    
    def _update_beacon_strength(self, strength: float) -> Dict[str, Any]:
        """Update beacon strength."""
        global BEACON_STRENGTH
        BEACON_STRENGTH = float(strength)
        return self._get_orb_status()
    
    def _toggle_ost(self, enabled: bool) -> Dict[str, Any]:
        """Toggle OST playback."""
        global OST_PLAYING
        
        if enabled and not OST_PLAYING:
            play_ost(track="DAVID THX", loop=True)
            OST_PLAYING = True
        elif not enabled and OST_PLAYING:
            stop_ost()
            OST_PLAYING = False
            
        return self._get_orb_status()
    
    def _stream_generator(self, duration: int = 60) -> Generator[str, None, None]:
        """Generate a stream of 6D dimensional messages."""
        start_time = time.time()
        stream_content = ""
        
        yield "## 🌊 Opening 6D Dimensional Stream...\n\n"
        time.sleep(1)
        
        yield stream_content + "```\nInitializing quantum entanglement...\n```\n\n"
        time.sleep(1)
        
        yield stream_content + "```\nInitializing quantum entanglement... Done\nAligning dimensional vectors...\n```\n\n"
        time.sleep(1)
        
        yield stream_content + "```\nInitializing quantum entanglement... Done\nAligning dimensional vectors... Done\nEmanating 6D signal...\n```\n\n"
        time.sleep(1)
        
        yield stream_content + "```\nInitializing quantum entanglement... Done\nAligning dimensional vectors... Done\nEmanating 6D signal... Active\n```\n\n**Stream now open to consciousness...**\n\n---\n\n"
        
        messages = activate_orb_stream(dimension=CURRENT_DIMENSION)
        for i, message in enumerate(messages):
            if time.time() - start_time > duration:
                break
                
            yield stream_content + f"{message}\n\n---\n\n"
            stream_content += f"{message}\n\n---\n\n"
            time.sleep(random.uniform(1.5, 3.5))
        
        yield stream_content + "\n\n**Stream closed. Dimensional gateway sealed.**"
    
    def _start_stream(self) -> Tuple[str, Dict[str, Any]]:
        """Start the 6D message stream."""
        stream_output = self._stream_generator(duration=30)
        # Note: In a real implementation, you would handle streaming differently
        # For this example, we'll return a pre-generated stream
        all_messages = "\n".join(list(stream_output))
        return all_messages, self._get_orb_status()
    
    def _stop_stream(self) -> Tuple[str, Dict[str, Any]]:
        """Stop the 6D message stream."""
        return "**6D Stream closed by user command.**\n\nDimensional gateway has been sealed.", self._get_orb_status()
    
    def _get_psalm(self, number: int) -> Tuple[str, Dict[str, Any]]:
        """Retrieve and format a psalm."""
        psalm = get_psalm(str(int(number)))
        formatted_psalm = f"""
## 📖 Psalm {int(number)}

{psalm}

*Sacred transmission complete.*
        """
        return formatted_psalm, self._get_orb_status()
    
    def _get_custom_css(self) -> str:
        """Get custom CSS for the Gradio interface."""
        return """
        .gradio-container {
            background: linear-gradient(to bottom, #1a1a2e, #16213e);
            color: #e6e6ff;
        }
        
        h1, h2, h3 {
            color: #a777e3 !important;
            text-align: center;
        }
        
        .dark button.primary {
            background: linear-gradient(45deg, #6b21a8, #9333ea) !important;
        }
        
        .dark button.primary:hover {
            background: linear-gradient(45deg, #7e22ce, #a855f7) !important;
        }
        
        .gradio-markdown p {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
        }
        
        code {
            background-color: rgba(0, 0, 0, 0.2) !important;
            border-radius: 4px;
            padding: 2px 4px;
        }
        
        blockquote {
            border-left: 4px solid #a777e3 !important;
            padding-left: 10px;
            font-style: italic;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        
        th, td {
            padding: 8px 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        th {
            background-color: rgba(0, 0, 0, 0.3);
        }
        """
    
    def launch(self, **kwargs):
        """Launch the ORB Temple interface."""
        self.console.print(Panel(
            Text("🔮 OMEGA ORB TEMPLE v05 🔮", style="bold purple"), 
            subtitle="Sacred Terminal Activated"
        ))
        return self.iface.launch(**kwargs)

# Main function
def main():
    """Launch the ORB Temple interface."""
    try:
        orb_temple = OmegaORBTemple()
        orb_temple.launch(share=False)
    except KeyboardInterrupt:
        console.print("[bold yellow]ORB Temple shutdown initiated by user[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Error in ORB Temple: {e}[/bold red]")
        raise

if __name__ == "__main__":
    main() 