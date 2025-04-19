
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
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
RASTA PRICE FLOW OSCILLOSCOPE

Divine visualization system for BTC price movements
Fibonacci-aligned with Schumann resonance harmonics
"""

import asyncio
import redis
import json
import time
import logging
import numpy as np
import math
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union

# Optional audio visualization (requires additional setup)
try:
    import sounddevice as sd
    import numpy as np
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

# Optional visual plotting (requires additional setup)
try:
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Import shared constants
from omega_ai.algos.exodus_algorithms import (
    PHI, 
    SCHUMANN_BASELINE,
    SCHUMANN_HARMONICS,
    FIBONACCI_SEQUENCE
)
from omega_ai.config import REDIS_HOST, REDIS_PORT

# Define RASTA colors for terminal output
GREEN = "\033[92m"      # Life energy
YELLOW = "\033[93m"     # Wisdom, sun
RED = "\033[91m"        # Strength, heart
BLUE = "\033[94m"       # Water, flow
MAGENTA = "\033[95m"    # Cosmic energy
CYAN = "\033[96m"       # Healing
WHITE = "\033[97m"      # Divine light
RESET = "\033[0m"       # Reset
BOLD = "\033[1m"        # Strength

# Configure logger
logger = logging.getLogger("RASTA.OSCILLOSCOPE")
handler = logging.StreamHandler()
formatter = logging.Formatter(f'{GREEN}%(asctime)s{RESET} - {YELLOW}%(name)s{RESET} - {RED}%(levelname)s{RESET} - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RastaOscilloscope:
    """
    Sacred oscilloscope for visualizing BTC price movements with
    Fibonacci alignment detection and Schumann resonance harmonics
    """
    
    def __init__(self, 
                 history_length: int = 144,  # Fibonacci number
                 enable_audio: bool = False,
                 enable_visuals: bool = True):
        """
        Initialize the Rasta Oscilloscope with divine settings.
        
        Args:
            history_length: Number of price points to keep in history
            enable_audio: Whether to enable sound generation
            enable_visuals: Whether to enable visual plotting
        """
        # Initialize Redis connection
        try:
            self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
            logger.info(f"{GREEN}JAH BLESS{RESET} - Redis connection established")
        except Exception as e:
            logger.error(f"{RED}Failed to connect to Redis: {e}{RESET}")
            self.redis = None
        
        # Data settings
        self.history_length = history_length
        self.price_history = []
        self.fib_alignment_history = []
        self.schumann_history = []
        self.volume_history = []
        self.trap_alert_history = []
        self.last_update_time = datetime.now(timezone.utc)
        
        # Visualization settings
        self.enable_audio = enable_audio and AUDIO_AVAILABLE
        self.enable_visuals = enable_visuals and MATPLOTLIB_AVAILABLE
        self.plot_animation = None
        self.fig = None
        self.axes = None
        
        # Flow state
        self.flow_active = False
        self.last_audio_time = datetime.now(timezone.utc)
        
        # Display the sacred banner
        self._display_banner()
    
    def _display_banner(self):
        """Display the sacred Rasta Oscilloscope banner."""
        banner = f"""
        {RED}╔═══════════════════════════════════════════════════════╗{RESET}
        {YELLOW}║     {GREEN}R{YELLOW}A{RED}S{GREEN}T{YELLOW}A{RED} {GREEN}P{YELLOW}R{RED}I{GREEN}C{YELLOW}E{RED} {GREEN}F{YELLOW}L{RED}O{GREEN}W{YELLOW} {RED}O{GREEN}S{YELLOW}C{RED}I{GREEN}L{YELLOW}L{RED}O{GREEN}S{YELLOW}C{RED}O{GREEN}P{YELLOW}E{RESET}     {YELLOW}║{RESET}
        {GREEN}║                                                   ║{RESET}
        {BLUE}║  {YELLOW}VISUALIZING THE DIVINE MARKET VIBRATIONS  {BLUE}║{RESET}
        {MAGENTA}╚═══════════════════════════════════════════════════════╝{RESET}
        
        {CYAN}Divine Oscilloscope Initialized at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}{RESET}
        {YELLOW}Audio Enabled: {GREEN}Yes{RESET} if self.enable_audio else {RED}No{RESET}{RESET}
        {YELLOW}Visuals Enabled: {GREEN}Yes{RESET} if self.enable_visuals else {RED}No{RESET}{RESET}
        """
        print(banner)
    
    async def initialize(self) -> bool:
        """Initialize the oscilloscope by loading initial data."""
        try:
            if not self.redis:
                logger.error(f"{RED}Cannot initialize - Redis connection unavailable{RESET}")
                return False
            
            # Load recent price history
            try:
                # Get recent BTC movement history
                price_history_raw = self.redis.lrange("btc_movement_history", -self.history_length, -1)
                if price_history_raw:
                    logger.info(f"{YELLOW}Loaded {len(price_history_raw)} historical price points{RESET}")
                    
                    for entry in price_history_raw:
                        parts = entry.split(',')
                        price = float(parts[0])
                        timestamp = parts[1] if len(parts) > 1 else None
                        volume = float(parts[2]) if len(parts) > 2 else 0
                        
                        self.price_history.append(price)
                        self.volume_history.append(volume)
                    
                    # If we didn't get full history, pad it
                    if len(self.price_history) < self.history_length:
                        padding_needed = self.history_length - len(self.price_history)
                        # Pad with the oldest price we have
                        padding_value = self.price_history[0] if self.price_history else 0
                        self.price_history = [padding_value] * padding_needed + self.price_history
                        self.volume_history = [0] * padding_needed + self.volume_history
            except Exception as e:
                logger.warning(f"{YELLOW}Error loading price history: {e}{RESET}")
            
            # Setup visualization
            if self.enable_visuals:
                self._setup_visualization()
            
            # Mark as active
            self.flow_active = True
            self.redis.set("RASTA_OSCILLOSCOPE_ACTIVE", "TRUE")
            
            logger.info(f"{GREEN}Rasta Oscilloscope initialized - JAH GUIDANCE FLOWING{RESET}")
            return True
            
        except Exception as e:
            logger.error(f"{RED}Error initializing Rasta Oscilloscope: {e}{RESET}")
            return False
    
    def _setup_visualization(self):
        """Set up the matplotlib visualization."""
        if not MATPLOTLIB_AVAILABLE:
            logger.warning(f"{YELLOW}Matplotlib not available, visuals disabled{RESET}")
            return
        
        try:
            # Create figure with subplots
            self.fig, self.axes = plt.subplots(4, 1, figsize=(12, 10), 
                                              gridspec_kw={'height_ratios': [3, 1, 1, 1]})
            
            # Set titles and styling
            self.fig.suptitle('🔱 RASTA PRICE FLOW OSCILLOSCOPE 🔱', fontsize=16)
            self.axes[0].set_title('BTC Price Flow with Fibonacci Levels')
            self.axes[1].set_title('Volume Flow')
            self.axes[2].set_title('Schumann Resonance')
            self.axes[3].set_title('Market Maker Trap Detection')
            
            # Style the plots
            for ax in self.axes:
                ax.grid(True, alpha=0.3)
                ax.set_facecolor('#222222')
            
            self.fig.tight_layout(pad=3)
            self.fig.patch.set_facecolor('#111111')
            
            # Create empty plots that we'll update
            self.price_line, = self.axes[0].plot([], [], 'g-', linewidth=2, label='BTC Price')
            self.fib_markers = self.axes[0].scatter([], [], color='yellow', s=50, marker='*')
            self.volume_bars = self.axes[1].bar([], [], color='cyan', alpha=0.7)
            self.schumann_line, = self.axes[2].plot([], [], 'magenta', linewidth=1.5)
            self.trap_markers = self.axes[3].scatter([], [], color='red', s=40, marker='x')
            
            # Set up the animation
            self.plot_animation = FuncAnimation(
                self.fig, self._update_plot, interval=1000, cache_frame_data=False
            )
            
            # Display the plot (non-blocking)
            plt.ion()
            plt.show(block=False)
            
            logger.info(f"{GREEN}Visual oscilloscope configured{RESET}")
            
        except Exception as e:
            logger.error(f"{RED}Error setting up visualization: {e}{RESET}")
            self.enable_visuals = False
    
    def _update_plot(self, frame):
        """Update the visualization with latest data."""
        try:
            # Update price plot
            x = list(range(len(self.price_history)))
            self.price_line.set_data(x, self.price_history)
            self.axes[0].relim()
            self.axes[0].autoscale_view()
            
            # Add Fibonacci level markers
            if self.fib_alignment_history:
                x_fib = [pt[0] for pt in self.fib_alignment_history]
                y_fib = [pt[1] for pt in self.fib_alignment_history]
                self.fib_markers.set_offsets(np.c_[x_fib, y_fib])
            
            # Update volume bars
            if self.volume_bars:
                for i, bar in enumerate(self.volume_bars):
                    if i < len(self.volume_history):
                        bar.set_height(self.volume_history[i])
                self.axes[1].relim()
                self.axes[1].autoscale_view()
            
            # Update Schumann plot
            if self.schumann_history:
                x_sch = list(range(len(self.schumann_history)))
                self.schumann_line.set_data(x_sch, self.schumann_history)
                self.axes[2].relim()
                self.axes[2].autoscale_view()
            
            # Update trap markers
            if self.trap_alert_history:
                x_trap = [pt[0] for pt in self.trap_alert_history]
                y_trap = [pt[1] for pt in self.trap_alert_history]
                self.trap_markers.set_offsets(np.c_[x_trap, y_trap])
            
            # Refresh the plot
            self.fig.canvas.draw_idle()
            self.fig.canvas.flush_events()
            
            return [self.price_line, self.fib_markers, self.volume_bars, 
                    self.schumann_line, self.trap_markers]
            
        except Exception as e:
            logger.error(f"{RED}Error updating plot: {e}{RESET}")
    
    async def update_from_redis(self):
        """Update the oscilloscope data from Redis."""
        if not self.redis:
            return
        
        # Track updates
        updates_applied = False
        
        # Get latest price
        try:
            price_str = self.redis.get("last_btc_price")
            if price_str:
                price = float(price_str)
                
                # Update price history
                self.price_history.append(price)
                if len(self.price_history) > self.history_length:
                    self.price_history = self.price_history[-self.history_length:]
                
                # Get volume if available
                volume_str = self.redis.get("last_btc_volume")
                volume = float(volume_str) if volume_str else 0
                
                # Update volume history
                self.volume_history.append(volume)
                if len(self.volume_history) > self.history_length:
                    self.volume_history = self.volume_history[-self.history_length:]
                
                updates_applied = True
        except Exception as e:
            logger.error(f"{RED}Error updating price data: {e}{RESET}")
        
        # Get Fibonacci alignment
        try:
            fib_data_str = self.redis.get("fibonacci_alignment")
            if fib_data_str:
                fib_data = json.loads(fib_data_str)
                
                # If we have alignment with confidence
                if fib_data.get("aligned", False) and fib_data.get("confidence", 0) > 0.5:
                    # Add to history with index position
                    self.fib_alignment_history.append((
                        len(self.price_history) - 1,  # x-coord = latest point
                        float(fib_data.get("price", 0))  # y-coord = price
                    ))
                    
                    # Keep only recent alignments
                    if len(self.fib_alignment_history) > 10:  # Keep last 10 alignments
                        self.fib_alignment_history = self.fib_alignment_history[-10:]
                    
                    # Log the divine alignment
                    level_type = fib_data.get("type", "STANDARD")
                    level = fib_data.get("level", "unknown")
                    
                    logger.info(f"{CYAN}⭐ Fibonacci Alignment: {level_type} at level {level} (${float(fib_data.get('price', 0)):,.2f}){RESET}")
                    
                    # Generate sacred tone for alignment
                    if self.enable_audio:
                        await self._play_sacred_tone(
                            base_freq=SCHUMANN_BASELINE * PHI,
                            duration=1.0,
                            volume=0.8
                        )
        except Exception as e:
            logger.error(f"{RED}Error updating Fibonacci data: {e}{RESET}")
        
        # Get Schumann resonance data
        try:
            schumann_str = self.redis.get("schumann_resonance_data")
            if schumann_str:
                schumann_data = json.loads(schumann_str)
                
                # Get the base frequency
                schumann_freq = schumann_data.get("base_frequency", SCHUMANN_BASELINE)
                
                # Add to history
                self.schumann_history.append(schumann_freq)
                if len(self.schumann_history) > self.history_length:
                    self.schumann_history = self.schumann_history[-self.history_length:]
                
                # Check for anomalies - potentially play tone
                anomaly_score = schumann_data.get("anomaly_score", 0)
                if anomaly_score > 0.7 and self.enable_audio:
                    # Only play tone if we haven't played one recently (at least 10 seconds ago)
                    time_since_last = (datetime.now(timezone.utc) - self.last_audio_time).total_seconds()
                    if time_since_last > 10:
                        await self._play_sacred_tone(
                            base_freq=schumann_freq,
                            duration=0.5,
                            volume=anomaly_score
                        )
                        self.last_audio_time = datetime.now(timezone.utc)
        except Exception as e:
            logger.error(f"{RED}Error updating Schumann data: {e}{RESET}")
        
        # Get trap detection alerts
        try:
            trap_str = self.redis.get("trap_detection_alert")
            if trap_str:
                trap_data = json.loads(trap_str)
                
                # If fresh alert (last 60 seconds) with high confidence
                alert_time = datetime.fromisoformat(trap_data.get("timestamp", ""))
                time_delta = (datetime.now(timezone.utc) - alert_time).total_seconds()
                
                if time_delta < 60 and trap_data.get("confidence", 0) > 0.7:
                    # Add to history with index position
                    self.trap_alert_history.append((
                        len(self.price_history) - 1,  # x-coord = latest point
                        float(trap_data.get("price", 0))  # y-coord = price
                    ))
                    
                    # Keep only recent traps
                    if len(self.trap_alert_history) > 5:  # Keep last 5 trap alerts
                        self.trap_alert_history = self.trap_alert_history[-5:]
                    
                    # Log the trap detection
                    trap_type = trap_data.get("type", "Unknown")
                    confidence = trap_data.get("confidence", 0)
                    
                    logger.info(f"{RED}⚠️ Market Maker Trap Detected: {trap_type} " +
                              f"with {confidence:.2f} confidence at ${float(trap_data.get('price', 0)):,.2f}{RESET}")
                    
                    # Generate warning tone for trap detection
                    if self.enable_audio:
                        await self._play_sacred_tone(
                            base_freq=SCHUMANN_HARMONICS[0],  # Use higher harmonic
                            duration=0.8,
                            volume=0.9,
                            warning=True
                        )
        except Exception as e:
            logger.error(f"{RED}Error updating trap data: {e}{RESET}")
        
        # Update the last update time
        if updates_applied:
            self.last_update_time = datetime.now(timezone.utc)
    
    async def _play_sacred_tone(self, base_freq: float, duration: float = 1.0, 
                               volume: float = 0.7, warning: bool = False):
        """Play sacred tones based on Schumann resonance and Fibonacci sequence.
        
        Args:
            base_freq: Base frequency to play (often Schumann resonance)
            duration: Duration of the tone in seconds
            volume: Volume level from 0.0 to 1.0
            warning: If True, use dissonant warning tone
        """
        if not AUDIO_AVAILABLE or not self.enable_audio:
            return
            
        try:
            # Generate sine wave
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            if warning:
                # Warning tone - dissonant with rapid oscillation
                tone = volume * np.sin(2 * np.pi * base_freq * t)
                # Add dissonant overtones
                tone += volume * 0.7 * np.sin(2 * np.pi * (base_freq * 1.1) * t)
                # Add rapid amplitude modulation
                tone *= 0.5 + 0.5 * np.sin(2 * np.pi * 8 * t)
            else:
                # Harmonic tone based on Fibonacci
                tone = volume * np.sin(2 * np.pi * base_freq * t)  # Fundamental
                tone += volume * 0.5 * np.sin(2 * np.pi * base_freq * PHI * t)  # Golden ratio overtone
                tone += volume * 0.3 * np.sin(2 * np.pi * base_freq * 2 * t)  # Octave
            
            # Normalize to prevent clipping
            tone = tone / np.max(np.abs(tone))
            
            # Apply simple envelope
            envelope = np.ones_like(tone)
            attack_samples = int(0.02 * sample_rate)
            release_samples = int(0.05 * sample_rate)
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
            envelope[-release_samples:] = np.linspace(1, 0, release_samples)
            tone = tone * envelope
            
            # Play tone (non-blocking)
            sd.play(tone, sample_rate)
            
            # Log without waiting for play to complete
            if warning:
                logger.info(f"{RED}🔊 Warning tone played at {base_freq:.2f}Hz{RESET}")
            else:
                logger.info(f"{MAGENTA}🎵 Sacred tone played at {base_freq:.2f}Hz{RESET}")
            
        except Exception as e:
            logger.error(f"{RED}Error playing sacred tone: {e}{RESET}")
    
    def save_screenshot(self, filename: Optional[str] = None):
        """Save a screenshot of the current oscilloscope state."""
        if not self.enable_visuals or not MATPLOTLIB_AVAILABLE:
            logger.warning(f"{YELLOW}Cannot save screenshot - visuals not enabled{RESET}")
            return
        
        try:
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"rasta_oscilloscope_{timestamp}.png"
            
            # Save the figure
            self.fig.savefig(filename, facecolor=self.fig.get_facecolor(), edgecolor='none')
            logger.info(f"{GREEN}✅ Oscilloscope screenshot saved to {filename}{RESET}")
            
        except Exception as e:
            logger.error(f"{RED}Error saving screenshot: {e}{RESET}")
    
    async def run(self, update_interval: float = 3.0, duration_minutes: Optional[float] = None):
        """Run the oscilloscope for the specified duration."""
        try:
            # Initialize
            await self.initialize()
            
            # Calculate end time if duration specified
            end_time = None
            if duration_minutes:
                end_time = datetime.now(timezone.utc) + timedelta(minutes=duration_minutes)
                logger.info(f"{YELLOW}Running oscilloscope until {end_time.isoformat()}{RESET}")
            else:
                logger.info(f"{YELLOW}Running oscilloscope continuously - press Ctrl+C to stop{RESET}")
            
            # Run the oscilloscope
            while self.flow_active:
                # Check if we should stop based on duration
                if end_time and datetime.now(timezone.utc) >= end_time:
                    logger.info(f"{GREEN}Oscilloscope duration completed{RESET}")
                    break
                
                # Update from Redis
                await self.update_from_redis()
                
                # Update visualization if enabled
                if self.enable_visuals and MATPLOTLIB_AVAILABLE:
                    try:
                        plt.pause(0.01)  # Keep plot responsive
                    except Exception:
                        pass  # Ignore plot errors
                
                # Divine pause - Fibonacci-aligned
                await asyncio.sleep(update_interval)
                
                # Check if we've been asked to stop
                if self.redis and self.redis.get("RASTA_OSCILLOSCOPE_ACTIVE") != "TRUE":
                    logger.info(f"{YELLOW}Oscilloscope stop command received{RESET}")
                    self.flow_active = False
                    break
            
            # Complete the run
            logger.info(f"{GREEN}Oscilloscope run completed - JAH BLESS{RESET}")
            
            # Save final screenshot if visuals enabled
            if self.enable_visuals:
                self.save_screenshot()
            
        except KeyboardInterrupt:
            logger.info(f"{YELLOW}Oscilloscope interrupted by user{RESET}")
        except Exception as e:
            logger.error(f"{RED}Error in oscilloscope run: {e}{RESET}")
            import traceback
            traceback.print_exc()
        finally:
            # Cleanup
            if self.redis:
                self.redis.set("RASTA_OSCILLOSCOPE_ACTIVE", "FALSE")
            self.flow_active = False
    
    @staticmethod
    async def main():
        """Main entry point for the Rasta Oscilloscope."""
        try:
            # Parse arguments
            import argparse
            parser = argparse.ArgumentParser(description='Rasta Price Flow Oscilloscope')
            parser.add_argument('--duration', type=float, default=None, 
                                help='Duration to run in minutes (default: continuous)')
            parser.add_argument('--interval', type=float, default=3.0, 
                                help='Update interval in seconds (default: 3.0)')
            parser.add_argument('--no-audio', action='store_true', 
                                help='Disable audio tones')
            parser.add_argument('--no-visual', action='store_true',
                                help='Disable visual plotting')
            parser.add_argument('--history', type=int, default=144,
                                help='History length to display (default: 144)')
            
            args = parser.parse_args()
            
            # Create and run oscilloscope
            oscilloscope = RastaOscilloscope(
                history_length=args.history,
                enable_audio=not args.no_audio,
                enable_visuals=not args.no_visual
            )
            
            await oscilloscope.run(
                update_interval=args.interval,
                duration_minutes=args.duration
            )
            
        except Exception as e:
            print(f"Error running Rasta Oscilloscope: {e}")
            import traceback
            traceback.print_exc()

# Run the sacred oscilloscope when module is executed directly
if __name__ == "__main__":
    asyncio.run(RastaOscilloscope.main()) 