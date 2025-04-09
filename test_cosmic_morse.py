#!/usr/bin/env python3
"""
OMEGA BTC AI - Cosmic Morse Code Converter
==========================================

This script provides a cosmic Morse code converter for encoding,
transmitting, and decoding messages through cosmic wavelengths.
Includes time-delayed delivery and quantum entanglement features.

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the GPU License
"""

import os
import sys
import time
import argparse
import json
import random
import base64
import binascii
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from scipy import signal
import pandas as pd

# Ensure the package is in the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'deployment/digitalocean/btc_live_feed_v3/src')
sys.path.insert(0, src_path)

# Parse command line arguments
parser = argparse.ArgumentParser(description="Cosmic Morse Code Converter")
parser.add_argument("--nodatabase", action="store_true", help="Run without database connection")
parser.add_argument("--message", type=str, help="Message to encode/decode")
parser.add_argument("--encode", action="store_true", help="Encode a message to Morse code")
parser.add_argument("--decode", action="store_true", help="Decode a Morse code message")
parser.add_argument("--transmit", action="store_true", help="Transmit encoded message via cosmic channels")
parser.add_argument("--receive", action="store_true", help="Receive messages from cosmic channels")
parser.add_argument("--delay", type=int, default=0, help="Delay delivery by N cosmic cycles (hours)")
parser.add_argument("--visualize", action="store_true", help="Visualize the Morse code waveform")
parser.add_argument("--quantum-entangle", action="store_true", help="Use quantum entanglement for secure transmission")
parser.add_argument("--cosmic-drift", type=float, default=0.0, help="Apply cosmic drift correction factor (0.0-1.0)")
parser.add_argument("--force-receive", action="store_true", help="Force receive messages regardless of delivery time")
args = parser.parse_args()

console = Console()

class CosmicMorseConverter:
    """Converts between text and cosmic Morse code."""
    
    # Standard Morse code dictionary
    MORSE_CODE_DICT = { 
        'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 
        'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 
        'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 
        'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-', 
        'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 
        'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', 
        '3':'...--', '4':'....-', '5':'.....', '6':'-....', 
        '7':'--...', '8':'---..', '9':'----.', '0':'-----', 
        '.':'.-.-.-', ',':'--..--', '?':'..--..', '/':'-..-.', 
        '-':'-....-', '(':'-.--.', ')':'-.--.-', ' ':' '
    }
    
    # Reversed dictionary for decoding
    MORSE_CODE_REVERSE = {v: k for k, v in MORSE_CODE_DICT.items()}
    
    # Cosmic frequency bands (Hz)
    COSMIC_FREQUENCIES = {
        "alpha": 432.0,    # Alpha cosmic frequency
        "theta": 369.0,    # Theta cosmic frequency
        "gamma": 528.0,    # Gamma cosmic frequency
        "delta": 216.0,    # Delta cosmic frequency
        "epsilon": 144.0,  # Epsilon cosmic frequency
    }
    
    # Transmission parameters
    DOT_DURATION = 0.1   # seconds
    DASH_DURATION = 0.3  # seconds
    SYMBOL_PAUSE = 0.1   # seconds
    LETTER_PAUSE = 0.3   # seconds
    WORD_PAUSE = 0.7     # seconds
    
    # Cosmic cycle parameters
    COSMIC_CYCLE_DURATION = 3600  # 1 hour in seconds
    
    def __init__(self, data_dir="./data", use_redis=True, cosmic_drift=0.0):
        """Initialize the cosmic Morse code converter."""
        self.data_dir = data_dir
        self.use_redis = use_redis
        self.cosmic_drift = cosmic_drift
        self.redis_client = None
        self.message_buffer = []
        self.quantum_keys = {}
        
        # Ensure data directory exists
        os.makedirs(os.path.join(data_dir, "cosmic_morse"), exist_ok=True)
        
        # Initialize Redis if needed
        if use_redis:
            self._init_redis()
    
    def _init_redis(self):
        """Initialize Redis connection if available."""
        try:
            import redis
            # Skip BtcNewsFeed import and connection since it's causing errors
            # Just log that we're using local storage instead
            console.print("[yellow]⚠️ Using local storage for message storage (Redis connection skipped)[/]")
            
        except (ImportError, Exception) as e:
            console.print(f"[yellow]⚠️ Redis not available: {e}[/]")
    
    def encode_message(self, message):
        """Encode a text message to Morse code."""
        if not message:
            return ""
            
        # Convert to uppercase for Morse code conversion
        message = message.upper()
        
        # Encode to Morse code
        morse_words = []
        words = message.split()
        
        for word in words:
            morse_letters = []
            for char in word:
                if char in self.MORSE_CODE_DICT:
                    morse_letters.append(self.MORSE_CODE_DICT[char])
                else:
                    # For characters not in the dictionary, keep them as is
                    morse_letters.append(char)
            
            # Join letters with spaces
            morse_words.append(" ".join(morse_letters))
        
        # Join words with " / "
        morse_text = " / ".join(morse_words)
        
        return morse_text
    
    def decode_message(self, morse_code):
        """Decode a Morse code message to text."""
        if not morse_code:
            return ""
            
        # Split into words (separated by " / ")
        words = morse_code.split(" / ")
        decoded_message = []
        
        for word in words:
            # Split into letters (separated by spaces)
            letters = word.split(" ")
            decoded_word = ""
            
            for letter in letters:
                if letter in self.MORSE_CODE_REVERSE:
                    decoded_word += self.MORSE_CODE_REVERSE[letter]
                elif letter == "":
                    # Skip empty strings
                    continue
                else:
                    # For symbols not in the dictionary, keep them as is
                    decoded_word += f"[{letter}]"
            
            decoded_message.append(decoded_word)
        
        # Join words with spaces
        return " ".join(decoded_message)
    
    def _apply_cosmic_drift(self, data):
        """Apply cosmic drift correction to data."""
        if self.cosmic_drift == 0:
            return data
            
        # Apply a sinusoidal drift pattern
        t = np.linspace(0, len(data), len(data))
        drift = np.sin(t * 0.01) * self.cosmic_drift
        return data * (1 + drift)
    
    def _apply_quantum_entanglement(self, data):
        """Apply quantum entanglement encryption to data."""
        # Generate a quantum key (simplified simulation)
        quantum_key = np.random.random(len(data))
        
        # Store the key for decryption
        key_id = binascii.hexlify(os.urandom(8)).decode()
        self.quantum_keys[key_id] = quantum_key
        
        # Apply the key to the data (XOR-like operation in continuous space)
        entangled_data = data * (0.5 + 0.5 * quantum_key)
        
        return entangled_data, key_id
    
    def _decode_quantum_entanglement(self, data, key_id):
        """Decode quantum entangled data using the stored key."""
        if key_id not in self.quantum_keys:
            console.print(f"[red]Error: Quantum key {key_id} not found[/]")
            return data
            
        quantum_key = self.quantum_keys[key_id]
        
        # Apply the inverse operation
        return data / (0.5 + 0.5 * quantum_key)
    
    def generate_waveform(self, morse_code, carrier_freq="alpha", quantum_entangle=False):
        """Convert Morse code to an audio waveform."""
        # Define sampling parameters
        sample_rate = 44100  # Hz
        carrier_frequency = self.COSMIC_FREQUENCIES[carrier_freq]
        
        # Convert Morse code to timing sequence
        timing_sequence = []
        
        for char in morse_code:
            if char == '.':
                timing_sequence.append((1, self.DOT_DURATION))
            elif char == '-':
                timing_sequence.append((1, self.DASH_DURATION))
            elif char == ' ':
                timing_sequence.append((0, self.LETTER_PAUSE))
            elif char == '/':
                timing_sequence.append((0, self.WORD_PAUSE))
            else:
                # Skip characters we don't recognize
                continue
                
            # Add pause between symbols (except for spaces and slashes)
            if char not in [' ', '/']:
                timing_sequence.append((0, self.SYMBOL_PAUSE))
        
        # Calculate total duration
        total_duration = sum(duration for _, duration in timing_sequence)
        total_samples = int(total_duration * sample_rate)
        
        # Generate the waveform
        waveform = np.zeros(total_samples)
        current_sample = 0
        
        for amplitude, duration in timing_sequence:
            num_samples = int(duration * sample_rate)
            t = np.linspace(0, duration, num_samples, False)
            
            if amplitude > 0:
                # Generate a carrier wave with an envelope
                carrier = np.sin(2 * np.pi * carrier_frequency * t)
                # Apply an envelope to avoid clicking
                envelope = np.ones_like(carrier)
                if num_samples > 100:
                    fade_len = 50
                    envelope[:fade_len] = np.linspace(0, 1, fade_len)
                    envelope[-fade_len:] = np.linspace(1, 0, fade_len)
                
                segment = amplitude * carrier * envelope
            else:
                # Silent pause
                segment = np.zeros(num_samples)
            
            # Add to the waveform
            end_sample = current_sample + num_samples
            if end_sample <= total_samples:
                waveform[current_sample:end_sample] = segment
            else:
                # Handle potential overflow
                waveform[current_sample:] = segment[:total_samples-current_sample]
            
            current_sample = end_sample
        
        # Apply cosmic drift correction
        waveform = self._apply_cosmic_drift(waveform)
        
        # Apply quantum entanglement if requested
        key_id = None
        if quantum_entangle:
            waveform, key_id = self._apply_quantum_entanglement(waveform)
        
        return waveform, key_id, sample_rate
    
    def visualize_waveform(self, waveform, sample_rate, morse_code):
        """Generate a visualization of the Morse code waveform."""
        # Create output directory
        output_dir = os.path.join(self.data_dir, "cosmic_morse")
        os.makedirs(output_dir, exist_ok=True)
        
        # Create a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Plot the waveform
        duration = len(waveform) / sample_rate
        time_axis = np.linspace(0, duration, len(waveform))
        
        plt.figure(figsize=(12, 8))
        
        # Plot full waveform
        plt.subplot(211)
        plt.plot(time_axis, waveform, 'b-')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude')
        plt.title('Cosmic Morse Code Waveform')
        plt.grid(True)
        
        # Plot spectrogram
        plt.subplot(212)
        plt.specgram(waveform, Fs=sample_rate, scale='dB')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Spectrogram of Morse Code Signal')
        plt.colorbar(label='Intensity (dB)')
        
        # Add the Morse code as text
        plt.figtext(0.5, 0.01, f"Morse Code: {morse_code}", ha='center', fontsize=10)
        
        # Save the figure
        filename = os.path.join(output_dir, f"morse_waveform_{timestamp}.png")
        plt.savefig(filename)
        plt.close()
        
        console.print(f"[green]✅ Waveform visualization saved to {filename}[/]")
        return filename
    
    def transmit_message(self, morse_code, delay=0, quantum_entangle=False):
        """Transmit a Morse code message via cosmic channels."""
        # Generate waveform
        waveform, key_id, sample_rate = self.generate_waveform(
            morse_code, 
            carrier_freq="alpha", 
            quantum_entangle=quantum_entangle
        )
        
        # Calculate transmission metadata
        timestamp = datetime.now()
        delivery_time = timestamp + timedelta(hours=delay)
        
        # Create message payload
        message_data = {
            "morse_code": morse_code,
            "timestamp": timestamp.isoformat(),
            "delivery_time": delivery_time.isoformat(),
            "quantum_key_id": key_id,
            "carrier_frequency": self.COSMIC_FREQUENCIES["alpha"],
            "cosmic_drift": self.cosmic_drift,
            "sample_rate": sample_rate,
            "waveform_length": len(waveform)
        }
        
        # Convert waveform to compact format for storage
        # Use base64 encoding to store the numpy array
        waveform_bytes = base64.b64encode(waveform.tobytes()).decode('ascii')
        message_data["waveform"] = waveform_bytes
        
        # Store in Redis or local file
        message_id = f"cosmic:morse:{timestamp.strftime('%Y%m%d%H%M%S')}"
        
        if self.redis_client and self.use_redis:
            try:
                # Store the message data
                self.redis_client.set(message_id, json.dumps(message_data))
                
                # Add to the scheduled delivery queue
                if delay > 0:
                    scheduled_key = f"cosmic:morse:scheduled:{delivery_time.strftime('%Y%m%d%H')}"
                    self.redis_client.sadd(scheduled_key, message_id)
                    console.print(f"[green]✅ Message scheduled for cosmic delivery at {delivery_time}[/]")
                else:
                    # Immediate delivery - add to the outgoing queue
                    self.redis_client.sadd("cosmic:morse:outgoing", message_id)
                    console.print("[green]✅ Message queued for immediate cosmic transmission[/]")
                
                return message_id
            except Exception as e:
                console.print(f"[yellow]⚠️ Redis transmission failed: {e}, falling back to local storage[/]")
        
        # Local file storage fallback
        output_dir = os.path.join(self.data_dir, "cosmic_morse")
        filename = os.path.join(output_dir, f"{message_id.replace(':', '_')}.json")
        
        with open(filename, 'w') as f:
            json.dump(message_data, f)
        
        console.print(f"[green]✅ Message saved to {filename}[/]")
        return message_id
    
    def receive_messages(self, max_messages=5, force_receive=False):
        """Receive messages from cosmic channels."""
        received_messages = []
        
        if self.redis_client and self.use_redis:
            try:
                # Check for incoming messages
                incoming_ids = self.redis_client.smembers("cosmic:morse:incoming")
                
                if not incoming_ids:
                    # Also check scheduled messages that are due for delivery
                    current_hour = datetime.now().strftime('%Y%m%d%H')
                    scheduled_key = f"cosmic:morse:scheduled:{current_hour}"
                    incoming_ids = self.redis_client.smembers(scheduled_key)
                
                # Limit the number of messages to process
                message_ids = list(incoming_ids)[:max_messages]
                
                for message_id in message_ids:
                    # Get the message data
                    message_data_str = self.redis_client.get(message_id)
                    if not message_data_str:
                        continue
                        
                    message_data = json.loads(message_data_str)
                    
                    # Process and add to received messages
                    received_messages.append(self._process_received_message(message_data))
                    
                    # Remove from the incoming queue
                    self.redis_client.srem("cosmic:morse:incoming", message_id)
                    
                    # Also check scheduled queues
                    delivery_time = datetime.fromisoformat(message_data["delivery_time"])
                    scheduled_key = f"cosmic:morse:scheduled:{delivery_time.strftime('%Y%m%d%H')}"
                    self.redis_client.srem(scheduled_key, message_id)
            
            except Exception as e:
                console.print(f"[yellow]⚠️ Redis reception failed: {e}, checking local storage[/]")
        
        # Check local storage if Redis failed or no messages were found
        if not received_messages:
            output_dir = os.path.join(self.data_dir, "cosmic_morse")
            message_files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
            
            # Sort by timestamp (newest first)
            message_files.sort(reverse=True)
            
            # Process each file
            for filename in message_files[:max_messages]:
                filepath = os.path.join(output_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        message_data = json.loads(f.read())
                    
                    # Check if it's due for delivery
                    delivery_time = datetime.fromisoformat(message_data["delivery_time"])
                    if force_receive or delivery_time <= datetime.now():
                        received_messages.append(self._process_received_message(message_data))
                except Exception as e:
                    console.print(f"[red]Error processing {filename}: {e}[/]")
        
        return received_messages
    
    def _process_received_message(self, message_data):
        """Process a received message and return its contents."""
        morse_code = message_data["morse_code"]
        
        # Decode the waveform if present
        if "waveform" in message_data:
            try:
                waveform_bytes = base64.b64decode(message_data["waveform"])
                waveform = np.frombuffer(waveform_bytes, dtype=np.float64)
                
                # Apply quantum decoding if needed
                if message_data.get("quantum_key_id"):
                    waveform = self._decode_quantum_entanglement(
                        waveform, 
                        message_data["quantum_key_id"]
                    )
                
                # Reverse cosmic drift if applied
                if message_data.get("cosmic_drift", 0) > 0:
                    # Set the drift value to reverse it
                    self.cosmic_drift = -message_data["cosmic_drift"]
                    waveform = self._apply_cosmic_drift(waveform)
                    self.cosmic_drift = message_data["cosmic_drift"]
            except Exception as e:
                console.print(f"[yellow]⚠️ Warning: Could not decode waveform: {e}[/]")
        
        # Decode the Morse code to text
        decoded_text = self.decode_message(morse_code)
        
        return {
            "morse_code": morse_code,
            "text": decoded_text,
            "received_at": datetime.now().isoformat(),
            "sent_at": message_data["timestamp"],
            "delivery_time": message_data["delivery_time"],
            "carrier_frequency": message_data.get("carrier_frequency", self.COSMIC_FREQUENCIES["alpha"]),
            "quantum_encrypted": message_data.get("quantum_key_id") is not None
        }
    
    def display_message(self, message):
        """Display a cosmic Morse code message with fancy formatting."""
        received_at = datetime.fromisoformat(message["received_at"])
        sent_at = datetime.fromisoformat(message["sent_at"])
        delivery_time = datetime.fromisoformat(message["delivery_time"])
        
        transit_time = received_at - sent_at
        
        # Determine the security level based on quantum encryption
        security_level = "Quantum-Secured" if message["quantum_encrypted"] else "Standard"
        security_color = "bright_magenta" if message["quantum_encrypted"] else "green"
        
        message_panel = Panel(
            f"[bold cyan]Message:[/] [yellow]{message['text']}[/]\n\n"
            f"[cyan]Morse Code:[/] {message['morse_code']}\n\n"
            f"[cyan]Sent at:[/] {sent_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"[cyan]Scheduled Delivery:[/] {delivery_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"[cyan]Received at:[/] {received_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"[cyan]Cosmic Transit Time:[/] {transit_time}\n"
            f"[cyan]Carrier Frequency:[/] {message['carrier_frequency']} Hz\n"
            f"[cyan]Security Level:[/] [{security_color}]{security_level}[/]",
            title="🌌 Cosmic Morse Transmission",
            border_style="magenta"
        )
        
        console.print(message_panel)

def run_cosmic_morse():
    """Run the Cosmic Morse Code Converter."""
    try:
        # Display banner
        console.print(Panel(
            "[bold cyan]OMEGA BTC AI - Cosmic Morse Code Converter[/]\n"
            "[yellow]Transmitting messages through cosmic wavelengths and quantum entanglement[/]",
            border_style="magenta"
        ))
        
        # Create converter instance
        cosmic_morse = CosmicMorseConverter(
            data_dir="./data", 
            use_redis=not args.nodatabase,
            cosmic_drift=args.cosmic_drift
        )
        
        # Process command based on arguments
        if args.encode and args.message:
            morse_code = cosmic_morse.encode_message(args.message)
            console.print(Panel(
                f"[cyan]Original Message:[/] {args.message}\n"
                f"[cyan]Morse Code:[/] [yellow]{morse_code}[/]",
                title="📝 Encoded Message",
                border_style="blue"
            ))
            
            # Generate and visualize waveform if requested
            if args.visualize:
                waveform, key_id, sample_rate = cosmic_morse.generate_waveform(
                    morse_code,
                    quantum_entangle=args.quantum_entangle
                )
                cosmic_morse.visualize_waveform(waveform, sample_rate, morse_code)
            
            # Transmit if requested
            if args.transmit:
                message_id = cosmic_morse.transmit_message(
                    morse_code,
                    delay=args.delay,
                    quantum_entangle=args.quantum_entangle
                )
                
                security_level = "QUANTUM-SECURED" if args.quantum_entangle else "STANDARD"
                
                console.print(Panel(
                    f"[cyan]Message ID:[/] [bright_magenta]{message_id}[/]\n"
                    f"[cyan]Security Level:[/] [bright_cyan]{security_level}[/]\n"
                    f"[cyan]Cosmic Cycles Delay:[/] {args.delay} hours\n"
                    f"[cyan]Expected Delivery:[/] {(datetime.now() + timedelta(hours=args.delay)).strftime('%Y-%m-%d %H:%M:%S')}",
                    title="📡 Transmission Details",
                    border_style="green"
                ))
        
        elif args.decode and args.message:
            # Decode Morse code to text
            decoded_text = cosmic_morse.decode_message(args.message)
            console.print(Panel(
                f"[cyan]Morse Code:[/] {args.message}\n"
                f"[cyan]Decoded Message:[/] [yellow]{decoded_text}[/]",
                title="🔍 Decoded Message",
                border_style="blue"
            ))
            
        elif args.receive:
            # Receive cosmic transmissions
            console.print("[bold cyan]Listening for cosmic transmissions...[/]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task("[cyan]Scanning cosmic frequencies...", total=None)
                time.sleep(2)  # Simulate scanning time
            
            messages = cosmic_morse.receive_messages(force_receive=args.force_receive)
            
            if messages:
                console.print(f"[green]✅ Received {len(messages)} cosmic transmission(s)[/]")
                for message in messages:
                    cosmic_morse.display_message(message)
            else:
                console.print("[yellow]No cosmic transmissions detected at this time[/]")
                
                # Cosmic advice when no messages are found
                cosmic_advice = [
                    "The cosmic silence speaks volumes. Mercury might be in retrograde.",
                    "No messages found. Try adjusting your quantum receiver.",
                    "The stars are contemplating your request. Try again later.",
                    "Cosmic channels are clear, but no messages are present.",
                    "Your quantum entanglement may need realignment with the lunar cycle."
                ]
                console.print(f"[cyan]{random.choice(cosmic_advice)}[/]")
        
        else:
            # Display help if no valid commands
            console.print(Markdown("""
            # Cosmic Morse Code Usage:
            
            ## Encode & Transmit:
            ```
            python test_cosmic_morse.py --encode --message "YOUR MESSAGE" --transmit
            ```
            
            ## Receive Messages:
            ```
            python test_cosmic_morse.py --receive
            ```
            
            ## Decode Morse Code:
            ```
            python test_cosmic_morse.py --decode --message ".... . .-.. .-.. ---"
            ```
            
            ## Advanced Options:
            - Add `--visualize` to see the waveform
            - Add `--quantum-entangle` for secure transmission
            - Add `--delay 24` to delay delivery by 24 cosmic cycles (hours)
            - Add `--cosmic-drift 0.05` to apply cosmic drift correction
            """))
    
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/]")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_cosmic_morse() 