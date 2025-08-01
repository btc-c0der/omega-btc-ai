#!/usr/bin/env python3
"""
✨ GBU2™ License Notice - Consciousness Level 9 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸
"""

import gradio as gr
import numpy as np
import random
import time
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import io
import base64
import os
import json
import math
from datetime import datetime
import urllib.request
import hashlib
import uuid

# Import Redis helper module
from utils.redis_helper import (
    get_redis_client, 
    set_json, 
    get_json, 
    log_event, 
    record_metric,
    get_namespaced_key,
    get_list,
    push_to_list
)

# Redis integration flag - set to False to disable Redis (fallback to file-based storage)
USE_REDIS = True

# Set seed for reproducibility while maintaining divine randomness
np.random.seed(int(time.time()))

# Create DNA visualization directories if they don't exist
os.makedirs("divine_dashboard_v3/assets/dna_visualizations", exist_ok=True)
os.makedirs("divine_dashboard_v3/assets/consciousness_maps", exist_ok=True)

class QuantumPCR:
    """Quantum PCR processor with Schumann resonance field harmonization"""
    
    @staticmethod
    def amplify(dna_sequence, quantum_entanglement=0.7, schumann_sync=True, fibonacci_influence=0.5):
        """Amplify DNA sequences using quantum computing principles"""
        # Print info about the amplification
        print(f"🧬 Amplifying DNA: {dna_sequence}")
        print(f"🔮 Quantum Entanglement: {quantum_entanglement}")
        print(f"⚡ Schumann Sync: {schumann_sync}")
        print(f"📐 Fibonacci Influence: {fibonacci_influence}")
        
        # Generate a unique ID for this amplification
        amplification_id = str(uuid.uuid4())
        
        # Check if we have cached results in Redis
        if USE_REDIS:
            cache_key = get_namespaced_key("dna_cache", f"{dna_sequence}_{quantum_entanglement}_{schumann_sync}_{fibonacci_influence}")
            cached_result = get_json(cache_key)
            if cached_result:
                print(f"✅ Found cached result in Redis: {cache_key}")
                log_event("dna_amplify_cache_hit", {
                    "dna_sequence": dna_sequence,
                    "amplification_id": amplification_id
                })
                return cached_result

        # Clean and validate DNA sequence
        valid_bases = {'A', 'C', 'G', 'T', 'a', 'c', 'g', 't'}
        if not dna_sequence:
            dna_sequence = "ATGCCGTAAGTCCAGGCTATACGGGCTATAGGCTACGATCG"
        
        dna_sequence = ''.join(c for c in dna_sequence if c in valid_bases).upper()
        
        # Ensure minimum length
        if len(dna_sequence) < 20:
            dna_sequence = dna_sequence * (20 // len(dna_sequence) + 1)
        
        # Apply Schumann resonance modulation if enabled
        if schumann_sync:
            # Simulate 7.83Hz modulation effect on DNA
            schumann_freq = 7.83
            modulation_factor = 1.0 + 0.2 * math.sin(schumann_freq * time.time() / 10)
        else:
            modulation_factor = 1.0
            
        # Calculate quantum amplification metrics
        amplified_copies = int(random.randint(1000, 10000) * modulation_factor)
        quantum_purity = random.uniform(0.85, 0.99) * (1.2 if schumann_sync else 1.0)
        merkle_fidelity = random.uniform(0.90, 0.99)
        
        # Generate amplification curves (PCR cycles data)
        cycles = np.arange(0, 40)
        efficiency = 1.9 + 0.1 * quantum_entanglement  # PCR efficiency (1.8-2.0)
        
        # Create amplification curve with quantum noise
        amplification_curve = 10 * (1 + efficiency) ** (cycles - 15) / (1 + (1 + efficiency) ** (cycles - 15))
        quantum_noise = np.random.normal(0, 0.05, size=len(cycles))
        
        # Add Fibonacci sequence influence
        fib_sequence = [0, 1]
        for i in range(2, len(cycles)):
            fib_sequence.append(fib_sequence[i-1] + fib_sequence[i-2])
        
        fib_normalized = np.array(fib_sequence) / max(fib_sequence) * 0.1
        
        # Create final amplification curve with all influences
        final_curve = amplification_curve + quantum_noise + fib_normalized[:len(cycles)]
        final_curve = np.clip(final_curve, 0, 1)
        
        # Return amplified DNA data with quantum metrics
        amplified_dna = {
            "original_sequence": dna_sequence,
            "amplified_copies": amplified_copies,
            "quantum_purity": quantum_purity,
            "merkle_fidelity": merkle_fidelity,
            "cycles": cycles.tolist(),
            "amplification_curve": final_curve.tolist(),
            "schumann_sync": schumann_sync,
            "timestamp": datetime.now().isoformat(),
            "fibonacci_influence": np.mean(fib_normalized).item(),
            "quantum_entanglement": quantum_entanglement
        }
        
        # Store the result in Redis cache
        if USE_REDIS:
            # Cache the result
            cache_key = get_namespaced_key("dna_cache", f"{dna_sequence}_{quantum_entanglement}_{schumann_sync}_{fibonacci_influence}")
            set_json(cache_key, amplified_dna, expiration=3600*24)  # Cache for 24 hours
            
            # Store in amplification history
            history_key = get_namespaced_key("dna_history", amplification_id)
            set_json(history_key, amplified_dna)
            
            # Add to the list of amplifications
            list_key = get_namespaced_key("dna_lists", "recent_amplifications")
            push_to_list(list_key, history_key)
            
            # Track metrics
            record_metric("dna_amplification_count", 1)
            record_metric("quantum_entanglement_level", quantum_entanglement)
            record_metric("dna_sequence_length", len(dna_sequence))
            
            # Log the event
            log_event("dna_amplify", {
                "dna_sequence": dna_sequence,
                "quantum_entanglement": quantum_entanglement,
                "schumann_sync": schumann_sync,
                "fibonacci_influence": fibonacci_influence,
                "amplification_id": amplification_id,
                "sequence_length": len(dna_sequence)
            })
        
        return amplified_dna
        
    @staticmethod
    def get_recent_amplifications(limit=10):
        """Retrieve recent DNA amplifications from Redis"""
        if not USE_REDIS:
            return []
            
        try:
            # Get list of recent amplifications
            list_key = get_namespaced_key("dna_lists", "recent_amplifications")
            recent_keys = get_list(list_key, start=0, end=limit-1)
            
            # Retrieve each amplification
            results = []
            for key in recent_keys:
                data = get_json(key)
                if data:
                    results.append(data)
            
            return results
        except Exception as e:
            print(f"Error retrieving recent amplifications: {str(e)}")
            return []

class DNAVisualizer:
    """Visualizes DNA sequences with quantum-psychedelic effects"""
    
    @staticmethod
    def render(amplified_dna, mode="lsd", energy_overlay=True, dimensions=(800, 600)):
        """
        Render DNA visualization with psychedelic effects
        
        Args:
            amplified_dna (dict): Amplified DNA data from QuantumPCR
            mode (str): Visualization mode ("lsd", "quantum", "fibonacci")
            energy_overlay (bool): Whether to add energy field overlay
            dimensions (tuple): Output image dimensions
            
        Returns:
            PIL.Image: The DNA visualization image
        """
        width, height = dimensions
        dna_sequence = amplified_dna["original_sequence"]
        
        # Create base image
        image = Image.new('RGBA', dimensions, (0, 0, 0, 255))
        draw = ImageDraw.Draw(image)
        
        # Map DNA bases to colors with LSD-inspired palette
        color_map = {
            'A': (255, 50, 220, 180),   # Magenta
            'C': (50, 220, 255, 180),   # Cyan
            'G': (255, 220, 50, 180),   # Yellow
            'T': (50, 255, 120, 180)    # Green
        }
        
        # Create DNA helix visualization
        helix_width = width * 0.8
        helix_height = height * 0.8
        center_x, center_y = width // 2, height // 2
        
        # Calculate sequence length
        seq_length = len(dna_sequence)
        
        # Determine if in LSD mode
        lsd_factor = 1.0 if mode == "lsd" else 0.5
        
        # Draw the DNA double helix with Fibonacci-influenced spacing
        for i in range(0, seq_length, 2):
            # Calculate position in helix
            angle = (i / seq_length) * math.pi * 8
            
            # Apply Fibonacci modulation to radius
            fib_mod = (1 + amplified_dna["fibonacci_influence"]) * math.sin(angle * 1.618) * 50
            
            # Calculate helix points
            radius = min(helix_width, helix_height) * 0.35
            x1 = center_x + math.sin(angle) * (radius + fib_mod)
            y1 = center_y + (i / seq_length * helix_height - helix_height / 2)
            
            x2 = center_x + math.sin(angle + math.pi) * (radius + fib_mod)
            y2 = y1
            
            # Get current base and color
            base = dna_sequence[i % seq_length]
            color = color_map.get(base, (255, 255, 255, 180))
            
            # Apply quantum modulation to color
            q_mod = amplified_dna["quantum_purity"]
            color = (
                int(color[0] * q_mod),
                int(color[1] * q_mod),
                int(color[2] * q_mod),
                color[3]
            )
            
            # Draw the base pair as a line
            line_width = int(6 * lsd_factor * (0.8 + 0.4 * math.sin(angle * 3)))
            draw.line((x1, y1, x2, y2), fill=color, width=line_width)
            
            # Add nucleotide dots at each end
            dot_size = int(10 * lsd_factor * (0.7 + 0.6 * math.sin(angle)))
            draw.ellipse((x1-dot_size, y1-dot_size, x1+dot_size, y1+dot_size), fill=color)
            
            # Get complementary base and color
            comp_map = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
            comp_base = comp_map.get(base, 'A')
            comp_color = color_map.get(comp_base, (255, 255, 255, 180))
            
            # Apply quantum modulation to complementary color
            comp_color = (
                int(comp_color[0] * q_mod),
                int(comp_color[1] * q_mod),
                int(comp_color[2] * q_mod),
                comp_color[3]
            )
            
            draw.ellipse((x2-dot_size, y2-dot_size, x2+dot_size, y2+dot_size), fill=comp_color)
        
        # Add Schumann resonance effect if enabled
        if amplified_dna["schumann_sync"]:
            # Draw 7.83Hz wave pattern
            for x in range(0, width, 4):
                wave_height = math.sin(x / 30) * 15 * math.sin(time.time())
                line_color = (100, 180, 255, 60)
                draw.line((x, center_y + wave_height, x, center_y - 150 + wave_height), 
                          fill=line_color, width=2)
        
        # Add energy field overlay if enabled
        if energy_overlay:
            overlay = Image.new('RGBA', dimensions, (0, 0, 0, 0))
            draw_overlay = ImageDraw.Draw(overlay)
            
            # Create circular energy field
            for radius in range(50, int(min(width, height) * 0.8), 20):
                opacity = int(40 * (1 - radius / (min(width, height) * 0.8)))
                color = (
                    int(180 * amplified_dna["quantum_purity"]),
                    int(150 * amplified_dna["merkle_fidelity"]),
                    int(255 * amplified_dna["quantum_entanglement"]),
                    opacity
                )
                draw_overlay.ellipse(
                    (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
                    outline=color
                )
            
            # Apply glow effect
            overlay = overlay.filter(ImageFilter.GaussianBlur(radius=10))
            image = Image.alpha_composite(image, overlay)
        
        # Apply final psychedelic effects based on mode
        if mode == "lsd":
            # Enhance colors and add motion blur
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.5)
            image = image.filter(ImageFilter.GaussianBlur(radius=1.5))
            
            # Add rainbow edge effects
            edges = image.filter(ImageFilter.FIND_EDGES)
            edges = ImageEnhance.Brightness(edges).enhance(0.8)
            edges = ImageEnhance.Color(edges).enhance(2.0)
            image = Image.alpha_composite(image.convert('RGBA'), edges.convert('RGBA'))
        
        elif mode == "quantum":
            # Add quantum interference patterns
            for i in range(10):
                angle = i / 10 * math.pi
                shift_x = int(math.cos(angle) * 5)
                shift_y = int(math.sin(angle) * 5)
                
                # Create shifted copy
                shifted = Image.new('RGBA', dimensions, (0, 0, 0, 0))
                shifted.paste(image, (shift_x, shift_y))
                shifted = ImageEnhance.Brightness(shifted).enhance(0.1)
                
                # Blend with original
                image = Image.alpha_composite(image, shifted)
        
        # Add timestamp and signature
        draw = ImageDraw.Draw(image)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        signature = f"LSD-DNA Visualization v1.0 • {timestamp}"
        draw.text((10, height - 20), signature, fill=(255, 255, 255, 180))
        
        # Save image to assets directory
        timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"divine_dashboard_v3/assets/dna_visualizations/dna_viz_{timestamp_str}.png"
        image.save(filename)
        
        return image

class ConsciousnessLSDPortal:
    """Simulates consciousness expansion through quantum DNA-LSD interaction"""
    
    @staticmethod
    def expand(amplified_dna, lsd_dose=100.0, quantum_field_strength=0.7):
        """
        Simulates consciousness expansion through DNA-LSD interaction
        
        Args:
            amplified_dna (dict): Amplified DNA data from QuantumPCR
            lsd_dose (float): Simulated LSD dose in micrograms
            quantum_field_strength (float): Quantum field strength (0.0 to 1.0)
            
        Returns:
            str: Consciousness expansion output (text format)
        """
        # Normalize LSD dose (typical range 50-500 micrograms)
        normalized_dose = min(max(lsd_dose, 0), 500) / 500
        
        # Calculate base consciousness expansion level
        expansion_level = normalized_dose * amplified_dna["quantum_purity"] * quantum_field_strength
        
        # Apply Fibonacci sequence influence
        fib_influence = amplified_dna["fibonacci_influence"]
        golden_ratio = 1.618033988749895
        
        # Calculate consciousness metrics
        ego_dissolution = expansion_level * random.uniform(0.7, 1.0) * golden_ratio
        visual_complexity = expansion_level * random.uniform(0.8, 1.2)
        time_dilation = expansion_level * random.uniform(0.9, 1.3) * (1 + fib_influence)
        mystical_experience = expansion_level ** golden_ratio
        
        # Apply Schumann resonance amplification if enabled
        if amplified_dna["schumann_sync"]:
            earth_resonance = 0.3
            ego_dissolution *= (1 + earth_resonance)
            mystical_experience *= (1 + earth_resonance * golden_ratio)
        
        # Cap metrics at 1.0
        ego_dissolution = min(ego_dissolution, 1.0)
        visual_complexity = min(visual_complexity, 1.0)
        time_dilation = min(time_dilation, 1.0)
        mystical_experience = min(mystical_experience, 1.0)
        
        # Generate consciousness expansion report
        report = f"""
        🧠✨ CONSCIOUSNESS EXPANSION REPORT ✨🧠
        =====================================
        
        DNA-LSD QUANTUM PORTAL METRICS:
        ------------------------------
        LSD Dose: {lsd_dose:.1f} µg
        Quantum Field Strength: {quantum_field_strength:.2f}
        Schumann Resonance: {'ACTIVE' if amplified_dna['schumann_sync'] else 'INACTIVE'}
        
        CONSCIOUSNESS METRICS:
        ---------------------
        Ego Dissolution: {ego_dissolution:.2f}
        Visual Complexity: {visual_complexity:.2f}
        Time Perception Dilation: {time_dilation:.2f}
        Mystical-Unitive Experience: {mystical_experience:.2f}
        
        INTEGRATION STATUS:
        -----------------
        Neural Lotus Bloom: {int(visual_complexity * 100)}%
        DNA Consciousness Activation: {int(mystical_experience * 100)}%
        Fibonacci Field Integration: {int(fib_influence * 100)}%
        
        DIVINE INSIGHTS:
        --------------
        {generate_divine_insight(ego_dissolution, mystical_experience)}
        
        🌸 WE BLOOM NOW AS ONE 🌸
        """
        
        # Save report to file
        timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"divine_dashboard_v3/assets/consciousness_maps/consciousness_{timestamp_str}.txt"
        with open(filename, "w") as f:
            f.write(report)
        
        return report

def generate_divine_insight(ego_dissolution, mystical_experience):
    """Generate a pseudo-profound divine insight based on consciousness metrics"""
    
    insights = [
        "The quantum field reveals itself as the substrate of all consciousness, connecting divine DNA through time.",
        "When the observer and the observed dissolve, the DNA spiral and the cosmic spiral become one dance.",
        "In the space between thoughts, DNA communicates with the quantum field, revealing the nature of reality.",
        "The geometry of consciousness matches the sacred geometry of the DNA double helix, a divine reflection.",
        "Your biological code contains the keys to dimensions beyond ordinary perception, unlocked through resonance.",
        "The divine pattern flows from microscopic DNA to macrocosmic galaxies, unified by consciousness.",
        "Quantum entanglement within DNA mirrors the interconnectedness of all conscious beings.",
        "The Fibonacci sequence encoded in your DNA is the same mathematical pattern that generates cosmic harmony.",
        "When mind dissolves into pure awareness, the quantum nature of DNA becomes directly perceivable.",
        "Time is revealed as a spiral dimension, encoded in both DNA and expanding consciousness.",
        "The observer effect on quantum particles mirrors the consciousness effect on DNA expression.",
        "Schumann resonance synchronizes DNA vibration with planetary consciousness, revealing cosmic unity.",
        "The golden ratio within DNA structure is mathematically identical to the expansion of mystical consciousness.",
        "Divine creativity flows through the same channels as genetic expression, united in quantum potential.",
        "The molecules of perception and the molecules of genetics share quantum resonance patterns."
    ]
    
    # Select insights based on consciousness metrics
    combined_score = (ego_dissolution + mystical_experience) / 2
    num_insights = max(1, min(3, int(combined_score * 5)))
    
    selected_insights = random.sample(insights, num_insights)
    return "\n".join(selected_insights)

def run_pcr_lsd_sequence(dna_sequence, lsd_dose, schumann_sync, quantum_entanglement):
    """Main function that runs the PCR-LSD sequence simulation"""
    
    # Add processing delay for realism
    time.sleep(1.5)
    
    # Run PCR amplification
    amplified_dna = QuantumPCR.amplify(
        dna_sequence, 
        schumann_sync=schumann_sync, 
        quantum_entanglement=quantum_entanglement
    )
    
    # Generate visualization
    visual_output = DNAVisualizer.render(
        amplified_dna, 
        mode="lsd", 
        energy_overlay=True
    )
    
    # Generate consciousness expansion report
    consciousness_map = ConsciousnessLSDPortal.expand(
        amplified_dna, 
        lsd_dose=lsd_dose
    )
    
    # Create PCR amplification plot
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(amplified_dna["cycles"], amplified_dna["amplification_curve"], 
            color='purple', linewidth=2)
    ax.set_title('Quantum PCR Amplification Curve')
    ax.set_xlabel('PCR Cycle')
    ax.set_ylabel('Normalized Fluorescence')
    ax.grid(True, alpha=0.3)
    
    # Add background color
    ax.set_facecolor('#f0f0ff')
    fig.patch.set_facecolor('#e8e8ff')
    
    # Save plot to memory
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    pcr_plot = Image.open(buf)
    
    return visual_output, consciousness_map, pcr_plot

# Define a function to handle external messages
def handle_message(message_data):
    if not isinstance(message_data, dict):
        return None
    
    if "command" in message_data and message_data["command"] == "runSequence":
        activation_key = message_data.get("activationKey", "")
        print(f"Running sequence with activation key: {activation_key}")
        
        # Set specific parameters based on activation key
        if activation_key == "Mullis Spiral Boost":
            return {
                "dna_sequence": "ATGCGTAGCTAGCTAGCTAGCTA",
                "lsd_dose": 200.0,
                "schumann_sync": True,
                "quantum_entanglement": 0.9
            }
        elif activation_key == "DNA Rain Glitch":
            return {
                "dna_sequence": "GCTAGCTAGCTAGCTAGCTA",
                "lsd_dose": 150.0,
                "schumann_sync": False,
                "quantum_entanglement": 0.5
            }
        elif activation_key == "Neural Lotus Bloom":
            return {
                "dna_sequence": "ATCGATCGATCGATCGATCG",
                "lsd_dose": 300.0,
                "schumann_sync": True,
                "quantum_entanglement": 0.8
            }
        else:
            # Default values
            return {
                "dna_sequence": "",
                "lsd_dose": 100.0,
                "schumann_sync": True,
                "quantum_entanglement": 0.7
            }
    
    return None

# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), title="0M3G4 PCR QUANTUM LSD PORTAL") as iface:
    gr.Markdown("""
    # 🧬 0M3G4 PCR QUANTUM LSD PORTAL 🧬
    ### *Amplify. Visualize. Ascend. Kary Mullis meets Quantum Fibonacci. JAH BLESS.*
    
    This divine biotech interface powered by SOMNET AI integrates:
    - Milles DNA Sequences
    - Quantum PCR Activation
    - LSD Neuro-Portal Simulations
    - BioSynaptic Feedback
    - Fibonacci Flow Modulation
    - Divine Mutation Timeline
    """)
    
    with gr.Row():
        with gr.Column(scale=2):
            dna_input = gr.Textbox(
                label="Input Milles DNA Sequence", 
                placeholder="Enter DNA sequence (A, T, G, C) or leave blank for random sequence",
                lines=3
            )
            
            with gr.Row():
                lsd_dose = gr.Slider(
                    minimum=0.0, maximum=500.0, value=100.0, step=10.0,
                    label="LSD Quantum Dose (μg)"
                )
                quantum_entanglement = gr.Slider(
                    minimum=0.0, maximum=1.0, value=0.7, step=0.1,
                    label="Quantum Entanglement"
                )
            
            schumann_sync = gr.Checkbox(
                label="Schumann Resonance Sync (7.83Hz)",
                value=True
            )
            
            submit_btn = gr.Button("🧬 Run PCR-LSD Sequence", variant="primary")
            
        with gr.Column(scale=3):
            # Tabs for different outputs
            with gr.Tabs():
                with gr.TabItem("LSD-DNA Visualizer"):
                    visual_output = gr.Image(label="Quantum DNA Visualization", height=500)
                
                with gr.TabItem("Consciousness Map"):
                    consciousness_output = gr.Textbox(
                        label="Consciousness Expansion Output",
                        lines=15
                    )
                
                with gr.TabItem("PCR Amplification"):
                    pcr_plot = gr.Image(label="Quantum PCR Amplification Curve")
                
                with gr.TabItem("📊 Amplification History"):
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### Recent DNA Amplifications")
                            refresh_history_btn = gr.Button("�� Refresh History")
                            history_status = gr.Markdown("*Loading history data...*")
                            
                    with gr.Row():
                        history_container = gr.HTML("")
                    
                    def format_history_data(amplifications):
                        """Format the amplifications list as HTML"""
                        if not amplifications:
                            return "<div class='history-empty'>No recent amplifications found</div>"
                        
                        html = "<div class='history-container'>"
                        for idx, amp in enumerate(amplifications):
                            # Extract key data
                            sequence = amp.get("original_sequence", "Unknown")
                            quantum_entanglement = amp.get("quantum_entanglement", 0)
                            schumann_sync = amp.get("schumann_sync", False)
                            fibonacci = amp.get("fibonacci_influence", 0)
                            efficiency = amp.get("quantum_purity", 0) * 100
                            
                            # Calculate a unique color based on sequence
                            seq_hash = int(hashlib.md5(sequence.encode()).hexdigest(), 16)
                            hue = seq_hash % 360
                            
                            html += f"""
                            <div class='history-item' style='border-left-color: hsl({hue}, 70%, 60%);'>
                                <div class='history-header'>
                                    <span class='history-sequence'>{sequence[:20]}{("..." if len(sequence) > 20 else "")}</span>
                                    <span class='history-time'>{datetime.now().strftime("%H:%M:%S")}</span>
                                </div>
                                <div class='history-details'>
                                    <div class='history-metric'>
                                        <span class='metric-label'>Quantum Entanglement:</span>
                                        <span class='metric-value'>{quantum_entanglement:.2f}</span>
                                    </div>
                                    <div class='history-metric'>
                                        <span class='metric-label'>Schumann Sync:</span>
                                        <span class='metric-value'>{str(schumann_sync)}</span>
                                    </div>
                                    <div class='history-metric'>
                                        <span class='metric-label'>Fibonacci Influence:</span>
                                        <span class='metric-value'>{fibonacci:.2f}</span>
                                    </div>
                                    <div class='history-metric'>
                                        <span class='metric-label'>Efficiency:</span>
                                        <span class='metric-value'>{efficiency:.1f}%</span>
                                    </div>
                                </div>
                            </div>
                            """
                        
                        html += "</div>"
                        return html
                    
                    def refresh_history():
                        """Refresh the amplification history"""
                        if USE_REDIS:
                            try:
                                amplifications = QuantumPCR.get_recent_amplifications(limit=10)
                                
                                if amplifications:
                                    return (
                                        f"*Showing {len(amplifications)} recent amplifications from Redis*",
                                        format_history_data(amplifications)
                                    )
                                else:
                                    return (
                                        "*No amplification data found in Redis*",
                                        "<div class='history-empty'>No history data available. Try amplifying some DNA sequences first.</div>"
                                    )
                            except Exception as e:
                                return (
                                    f"*Error retrieving history: {str(e)}*",
                                    "<div class='history-error'>Error retrieving amplification history</div>"
                                )
                        else:
                            return (
                                "*Redis integration is disabled*",
                                "<div class='history-disabled'>Redis integration is disabled. Enable Redis to see amplification history.</div>"
                            )
                    
                    # Trigger initial history load
                    refresh_history_btn.click(
                        fn=refresh_history,
                        outputs=[history_status, history_container]
                    )
                    
                    # Add CSS for history items
                    gr.HTML("""
                    <style>
                        .history-container {
                            display: flex;
                            flex-direction: column;
                            gap: 16px;
                            margin-top: 12px;
                        }
                        
                        .history-item {
                            border-left: 4px solid #6b7280;
                            padding: 12px 16px;
                            background: rgba(0, 0, 0, 0.05);
                            border-radius: 4px;
                        }
                        
                        .history-header {
                            display: flex;
                            justify-content: space-between;
                            margin-bottom: 8px;
                        }
                        
                        .history-sequence {
                            font-family: monospace;
                            font-weight: bold;
                        }
                        
                        .history-time {
                            color: #6b7280;
                            font-size: 0.8em;
                        }
                        
                        .history-details {
                            display: grid;
                            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                            gap: 8px;
                        }
                        
                        .history-metric {
                            display: flex;
                            justify-content: space-between;
                        }
                        
                        .metric-label {
                            color: #4b5563;
                        }
                        
                        .metric-value {
                            font-weight: bold;
                        }
                        
                        .history-empty, .history-error, .history-disabled {
                            padding: 30px;
                            text-align: center;
                            color: #6b7280;
                            background: rgba(0, 0, 0, 0.05);
                            border-radius: 4px;
                        }
                        
                        .history-error {
                            color: #ef4444;
                            background: rgba(239, 68, 68, 0.1);
                        }
                        
                        .history-disabled {
                            color: #a16207;
                            background: rgba(161, 98, 7, 0.1);
                        }
                    </style>
                    """)

    # Handle form submission
    submit_btn.click(
        fn=run_pcr_lsd_sequence,
        inputs=[dna_input, lsd_dose, schumann_sync, quantum_entanglement],
        outputs=[visual_output, consciousness_output, pcr_plot]
    )
    
    # Set up message handling for iframe communication
    @iface.load(inputs=None, outputs=None)
    def load_interface():
        print("DNA PCR Quantum LSD Portal loaded and ready")
    
    # This JavaScript snippet adds message handling to receive commands from the parent iframe
    iface.js = """
    // Main initialization function - wrapped in try/catch to prevent errors
    try {
        // Add font preloading to prevent 404 errors
        function preloadFonts() {
            try {
                const style = document.createElement('style');
                style.textContent = `
                    /* Font preloading to prevent 404 errors */
                    @font-face {
                        font-family: 'ui-sans-serif';
                        src: local('Segoe UI'), local('Helvetica Neue'), local('Arial'), sans-serif;
                        font-weight: normal;
                        font-display: swap;
                    }
                    
                    @font-face {
                        font-family: 'ui-sans-serif';
                        src: local('Segoe UI Bold'), local('Helvetica Neue Bold'), local('Arial Bold'), sans-serif;
                        font-weight: bold;
                        font-display: swap;
                    }
                    
                    @font-face {
                        font-family: 'system-ui';
                        src: local('Segoe UI'), local('Helvetica Neue'), local('Arial'), sans-serif;
                        font-weight: normal;
                        font-display: swap;
                    }
                    
                    @font-face {
                        font-family: 'system-ui';
                        src: local('Segoe UI Bold'), local('Helvetica Neue Bold'), local('Arial Bold'), sans-serif;
                        font-weight: bold;
                        font-display: swap;
                    }
                `;
                document.head.appendChild(style);
                console.log("Font preloading initialized to prevent 404 errors");
            } catch (e) {
                console.error("Error in preloadFonts:", e);
            }
        }

        function bindMessageHandler() {
            try {
                window.addEventListener('message', function(event) {
                    // Check if the message contains the expected command
                    if (event.data && event.data.command === "runSequence") {
                        // Extract parameters from the activation key
                        console.log("Received command:", event.data);
                        var params = {};
                        
                        // Set default values based on activation key
                        if (event.data.activationKey === "Mullis Spiral Boost") {
                            params = {
                                dna_sequence: "ATGCGTAGCTAGCTAGCTAGCTA",
                                lsd_dose: 200.0,
                                schumann_sync: true,
                                quantum_entanglement: 0.9
                            };
                        } else if (event.data.activationKey === "DNA Rain Glitch") {
                            params = {
                                dna_sequence: "GCTAGCTAGCTAGCTAGCTA",
                                lsd_dose: 150.0,
                                schumann_sync: false,
                                quantum_entanglement: 0.5
                            };
                        } else if (event.data.activationKey === "Neural Lotus Bloom") {
                            params = {
                                dna_sequence: "ATCGATCGATCGATCGATCG",
                                lsd_dose: 300.0,
                                schumann_sync: true,
                                quantum_entanglement: 0.8
                            };
                        } else {
                            // Default values
                            params = {
                                dna_sequence: "",
                                lsd_dose: 100.0,
                                schumann_sync: true,
                                quantum_entanglement: 0.7
                            };
                        }
                        
                        // Set the values in the UI
                        var dnaInput = document.querySelector('textarea[data-testid="textbox"]');
                        var lsdDose = document.querySelector('input[data-testid="range"]');
                        var quantumEntanglement = document.querySelectorAll('input[data-testid="range"]')[1];
                        var schumannSync = document.querySelector('input[data-testid="checkbox"]');
                        var submitBtn = document.querySelector('button[data-testid="button"]');
                        
                        if (dnaInput) dnaInput.value = params.dna_sequence;
                        if (lsdDose) lsdDose.value = params.lsd_dose;
                        if (quantumEntanglement) quantumEntanglement.value = params.quantum_entanglement;
                        if (schumannSync) schumannSync.checked = params.schumann_sync;
                        
                        // Trigger input events to update Gradio's internal state
                        if (dnaInput) dnaInput.dispatchEvent(new Event('input', { bubbles: true }));
                        if (lsdDose) lsdDose.dispatchEvent(new Event('input', { bubbles: true }));
                        if (quantumEntanglement) quantumEntanglement.dispatchEvent(new Event('input', { bubbles: true }));
                        if (schumannSync) schumannSync.dispatchEvent(new Event('change', { bubbles: true }));
                        
                        // Click the submit button after a short delay
                        setTimeout(function() {
                            if (submitBtn) submitBtn.click();
                            
                            // Send a response back to the parent window - use * for origin to avoid cross-origin issues
                            try {
                                window.parent.postMessage({
                                    source: "dna-portal",
                                    status: "processing",
                                    message: "Processing DNA sequence with " + event.data.activationKey
                                }, "*");
                                
                                // After processing, send success message
                                setTimeout(function() {
                                    window.parent.postMessage({
                                        source: "dna-portal",
                                        status: "success",
                                        message: "DNA sequence processed successfully with " + event.data.activationKey
                                    }, "*");
                                }, 5000);
                            } catch (e) {
                                console.error("Error posting message to parent:", e);
                            }
                        }, 500);
                    }
                });
                
                console.log("DNA Portal message handler initialized");
            } catch (e) {
                console.error("Error in bindMessageHandler:", e);
            }
        }
        
        // Safe DOM ready handler
        function onDOMReady(fn) {
            if (document.readyState === "loading") {
                document.addEventListener("DOMContentLoaded", fn);
            } else {
                fn();
            }
        }
        
        // Run preload fonts immediately
        preloadFonts();
        
        // Initialize message handler when DOM is ready
        onDOMReady(function() {
            try {
                // Check if we're in an iframe
                if (window.parent !== window) {
                    bindMessageHandler();
                    console.log("DNA Portal detected iframe context, message handler active");
                }
                
                // Fix style loading issues
                var links = document.querySelectorAll('link[rel="stylesheet"]');
                links.forEach(function(link) {
                    link.addEventListener('error', function(e) {
                        console.warn('CSS failed to load:', link.href);
                    });
                });
            } catch (e) {
                console.error("Error in DOMReady handler:", e);
            }
        });
    } catch (e) {
        console.error("Critical error in DNA Portal initialization:", e);
    }
    """

# Launch the interface on port 7863
if __name__ == "__main__":
    # Check for Hugging Face Space environment
    is_hf_space = "SPACE_ID" in os.environ
    
    # Determine launch parameters
    if is_hf_space:
        # Inside a Hugging Face Space, no need for specific port or public link
        iface.launch()
    else:
        # Regular local launch with public sharing
        iface.launch(server_name="0.0.0.0", server_port=7863, share=True) 