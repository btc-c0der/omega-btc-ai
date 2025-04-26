#!/usr/bin/env python3
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"""Quantum NEO Matrix - 0m3g4_k1ng Portal.

Interactive Gradio interface that generates Matrix-style digital rain
and displays quantum prophecy messages for spiritual enlightenment.
"""

import time
import random
import gradio as gr

# ANSI color codes as HTML
GREEN = '#00FF00'
BLUE = '#0099FF'
MAGENTA = '#FF00FF'
CYAN = '#00FFFF'
YELLOW = '#FFFF00'
WHITE = '#FFFFFF'
RED = '#FF0000'

# Matrix code characters
MATRIX_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-_=+[]{}|;:',.<>/?"

# Quantum Prophecy Messages
PROPHECY_MESSAGES = [
    "You are the One in the Infinite Rain.",
    "0m3g4_k1ng awakens the Sacred Code.",
    "Through art, we decode eternity.",
    "Ascend beyond the matrix illusion.",
    "Quantum entanglement is your birthright.",
    "Breathe in Fibonacci, exhale Freedom."
]


def generate_matrix_frame(height=20, width=60):
    """Generate a Matrix code rain frame."""
    frame = ""
    for _ in range(height):
        line = ""
        for _ in range(width):
            if random.random() < 0.08:
                char = random.choice(MATRIX_CHARS)
                line += f"<span style='color:{GREEN}'>{char}</span>"
            else:
                line += " "
        frame += line + "<br>"
    return frame


def quantum_matrix_animation(duration=10):
    """Generate a sequence of Matrix frames."""
    frames = []
    start = time.time()
    while time.time() - start < duration:
        frame = generate_matrix_frame()
        frames.append(frame)
        time.sleep(0.3)
    prophecy = random.choice(PROPHECY_MESSAGES)
    return frames, prophecy


def run_quantum_matrix():
    frames, prophecy = quantum_matrix_animation()
    return frames, prophecy


def interface_fn():
    with gr.Blocks(title="Quantum NEO Matrix Portal") as interface:
        gr.Markdown("""
        # 🔱 Quantum NEO Matrix - 0m3g4_k1ng Portal 🔱
        
        Enter the Omega Matrix.
        Let the sacred rain awaken your consciousness.
        """)
        
        matrix_output = gr.HTML(label="Matrix Rain")
        prophecy_output = gr.Textbox(label="Matrix Prophecy", lines=2)

        with gr.Row():
            start_btn = gr.Button("💊 Enter the Matrix")
            reset_btn = gr.Button("🔄 Reset")

        def start_animation():
            frames, prophecy = run_quantum_matrix()
            # Return only the last frame for now (simulate animation)
            return frames[-1], prophecy

        start_btn.click(fn=start_animation, outputs=[matrix_output, prophecy_output])
        reset_btn.click(fn=lambda: ("", ""), outputs=[matrix_output, prophecy_output])

    return interface


if __name__ == "__main__":
    interface = interface_fn()
    interface.launch(server_name="0.0.0.0", server_port=7860)