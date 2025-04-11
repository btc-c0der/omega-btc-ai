"""
VIRGIL GRID UI - Example App
----------------------------
Simple example application demonstrating the VIRGIL GRID UI design system with Gradio.

To run:
    python virgil_example_app.py
"""

import os
import sys
import random
import time
import gradio as gr

# Add parent directory to path to import components
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from components.virgil_gradio_components import (
    create_virgil_layout,
    virgil_terminal,
    virgil_card,
    virgil_progress,
    virgil_badge
)

# Example terminal commands and outputs
TERMINAL_COMMANDS = [
    (
        'echo "THE GRID IS SACRED"',
        'THE GRID IS SACRED'
    ),
    (
        'cd /OMEGA/GRID/sacred_modules',
        ''
    ),
    (
        'ls -la',
        'total 8\ndrwxr-xr-x  6 divine divine  192 May 21 13:34 .\ndrwxr-xr-x 14 divine divine  448 May 21 13:34 ..\n-rw-r--r--  1 divine divine 2195 May 21 13:34 quantum_engine.js\ndrwxr-xr-x  4 divine divine  128 May 21 13:34 tesla_modules'
    ),
    (
        'cat quantum_engine.js | head -3',
        '/**\n * Quantum Engine - Core module for quantum calculations\n * OMEGA GRID - Sacred Implementation'
    ),
    (
        'run_transformation --level=3',
        'Starting transformation level 3 (∆∆∆)\nQuantum entanglement initialized\nCalculating probability waves...\nTransformation complete.'
    )
]


def update_terminal(terminal_box):
    """Add a random command to the terminal output."""
    command, output = random.choice(TERMINAL_COMMANDS)
    current_content = terminal_box or ""
    
    # Add command with prompt
    new_content = current_content + f"\n$ {command}"
    
    # Add output if it exists
    if output:
        new_content += f"\n{output}"
    
    return new_content


def update_system_stats():
    """Generate random system statistics."""
    return {
        'cpu': random.randint(10, 90),
        'memory': random.randint(20, 85),
        'network': random.randint(5, 60),
        'quantum': random.randint(30, 99),
    }


def create_app():
    """Create the example Virgil UI Gradio app."""
    # Initialize with a divine title
    blocks = create_virgil_layout("OMEGA GRID SACRED INTERFACE")
    
    # State variables
    stats = update_system_stats()
    
    with blocks:
        # Header section
        with gr.Row():
            with gr.Column():
                gr.HTML(f"""
                <div class="virgil-state-indicator processing">"LIVE"</div>
                <div class="virgil-mt-m">
                    <div class="symbol-sequence level-4">
                        <span class="sacred-symbol delta">∆</span>
                        <span class="sacred-symbol delta">∆</span>
                        <span class="sacred-symbol delta">∆</span>
                        <span class="sacred-symbol delta">∆</span>
                    </div>
                </div>
                """)

        # Main content
        with gr.Row():
            # Left column - System stats
            with gr.Column():
                system_card = gr.HTML(virgil_card(
                    "SYSTEM STATUS",
                    f"""
                    <div>{virgil_badge("ACTIVE", "success")}</div>
                    <div class="virgil-mt-m">{virgil_progress("CPU LOAD", stats['cpu'])}</div>
                    <div>{virgil_progress("MEMORY", stats['memory'])}</div>
                    <div>{virgil_progress("NETWORK", stats['network'])}</div>
                    <div>{virgil_progress("QUANTUM FLUX", stats['quantum'])}</div>
                    """
                ))
            
            # Right column - Terminal
            with gr.Column():
                terminal_content = """$ echo "INITIALIZING VIRGIL GRID UI"
INITIALIZING VIRGIL GRID UI

$ echo "THE GRID IS SACRED"
THE GRID IS SACRED"""
                
                terminal_output = gr.HTML(virgil_terminal(terminal_content))
        
        # Controls 
        with gr.Row():
            with gr.Column():
                gr.HTML("""
                <div class="virgil-card">
                    <div class="virgil-card-header">
                        <h3 class="virgil-card-title">"CONTROLS"</h3>
                    </div>
                    <div class="virgil-card-content">
                        <div style="display: flex; gap: 10px;">
                            <button class="virgil-btn virgil-btn-primary" id="update-btn">"UPDATE"</button>
                            <button class="virgil-btn virgil-btn-secondary" id="reset-btn">"RESET"</button>
                            <button class="virgil-btn virgil-btn-sacred" id="ascend-btn">"ASCEND"</button>
                        </div>
                    </div>
                </div>
                """)
        
        # Add interactive functionality with JavaScript
        gr.HTML("""
        <script>
            // Helper function to update system card
            function updateSystemCard(stats) {
                // Update system stats on button click
                const updateBtn = document.getElementById('update-btn');
                const resetBtn = document.getElementById('reset-btn');
                const ascendBtn = document.getElementById('ascend-btn');
                
                if (updateBtn) {
                    updateBtn.addEventListener('click', function() {
                        // Send message to Python backend
                        if (window.gradio_client) {
                            window.gradio_client.dispatch('update_stats');
                        }
                    });
                }
                
                if (resetBtn) {
                    resetBtn.addEventListener('click', function() {
                        // Create and show notification
                        const notification = document.createElement('div');
                        notification.className = 'virgil-notification';
                        notification.innerHTML = '<div class="virgil-notification-content">"SYSTEM RESET INITIATED"</div>';
                        document.body.appendChild(notification);
                        
                        // Remove after 3 seconds
                        setTimeout(function() {
                            notification.remove();
                        }, 3000);
                    });
                }
                
                if (ascendBtn) {
                    ascendBtn.addEventListener('click', function() {
                        // Create sacred symbols animation
                        const symbolContainer = document.createElement('div');
                        symbolContainer.className = 'sacred-symbol-animation';
                        
                        for (let i = 0; i < 10; i++) {
                            const symbol = document.createElement('div');
                            symbol.className = 'floating-symbol';
                            symbol.textContent = '∆';
                            symbol.style.left = Math.random() * 100 + 'vw';
                            symbol.style.animationDuration = (3 + Math.random() * 4) + 's';
                            symbol.style.animationDelay = Math.random() * 2 + 's';
                            symbolContainer.appendChild(symbol);
                        }
                        
                        document.body.appendChild(symbolContainer);
                        
                        // Remove after animation completes
                        setTimeout(function() {
                            symbolContainer.remove();
                        }, 7000);
                    });
                }
            }
            
            // Initialize on page load
            document.addEventListener('DOMContentLoaded', function() {
                updateSystemCard();
                
                // Add custom styles for notifications and animations
                const styleElement = document.createElement('style');
                styleElement.textContent = `
                    .virgil-notification {
                        position: fixed;
                        top: 20px;
                        right: 20px;
                        background: linear-gradient(135deg, var(--color-divine-blue) 0%, var(--color-sacred-gold) 100%);
                        color: white;
                        padding: 15px 25px;
                        border-radius: 4px;
                        z-index: 1000;
                        animation: slide-in 0.3s ease-out forwards;
                    }
                    
                    @keyframes slide-in {
                        from { transform: translateX(100%); opacity: 0; }
                        to { transform: translateX(0); opacity: 1; }
                    }
                    
                    .sacred-symbol-animation {
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100vw;
                        height: 100vh;
                        pointer-events: none;
                        z-index: 999;
                    }
                    
                    .floating-symbol {
                        position: absolute;
                        font-size: 24px;
                        color: var(--color-divine-blue);
                        animation: float-up 5s ease-in-out forwards;
                        opacity: 0;
                    }
                    
                    @keyframes float-up {
                        0% { transform: translateY(100vh); opacity: 0; }
                        10% { opacity: 1; }
                        90% { opacity: 1; }
                        100% { transform: translateY(-100px); opacity: 0; }
                    }
                `;
                document.head.appendChild(styleElement);
            });
        </script>
        """)
        
        # Add event handlers
        def update_ui():
            """Update the UI with new stats."""
            new_stats = update_system_stats()
            new_terminal = update_terminal(terminal_content)
            
            # Update system card HTML
            new_system_card = virgil_card(
                "SYSTEM STATUS",
                f"""
                <div>{virgil_badge("ACTIVE", "success")}</div>
                <div class="virgil-mt-m">{virgil_progress("CPU LOAD", new_stats['cpu'])}</div>
                <div>{virgil_progress("MEMORY", new_stats['memory'])}</div>
                <div>{virgil_progress("NETWORK", new_stats['network'])}</div>
                <div>{virgil_progress("QUANTUM FLUX", new_stats['quantum'])}</div>
                """
            )
            
            # Update terminal
            new_terminal_output = virgil_terminal(new_terminal)
            
            return new_system_card, new_terminal_output
        
        # Register event handler for the "update_stats" event
        blocks.load(lambda: None, None, None, _js="() => {window.gradio_client.on('update_stats', () => {gradio_client.dispatch('update_ui')})}") 
        blocks.load(update_ui, None, [system_card, terminal_output], _js="() => {window.gradio_client.on('update_ui', () => {})}")
    
    return blocks


if __name__ == "__main__":
    app = create_app()
    app.launch() 