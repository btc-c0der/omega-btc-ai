"""
Virgil UI - Gradio Components
-----------------------------
Integration between Virgil UI design system and Gradio
"""

import os
import gradio as gr

# Path to the Virgil CSS file
VIRGIL_CSS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/css/virgil.css")


def load_virgil_css():
    """Load the Virgil CSS content from file."""
    try:
        with open(VIRGIL_CSS_PATH, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: Virgil CSS file not found at {VIRGIL_CSS_PATH}")
        return ""


def create_virgil_layout(title="OMEGA GRID", enable_terminal=True):
    """
    Create a Gradio Blocks layout with Virgil UI styling.
    
    Args:
        title (str): The title of the dashboard
        enable_terminal (bool): Whether to include the terminal component
        
    Returns:
        gr.Blocks: The styled Gradio Blocks interface
    """
    
    # Load Virgil CSS
    virgil_css = load_virgil_css()
    
    # Add custom CSS for Gradio integration
    custom_css = """
    .gradio-container {
        font-family: var(--font-primary);
    }
    
    .gr-button {
        font-family: var(--font-primary);
        font-size: var(--font-size-body);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: var(--spacing-xs) var(--spacing-m);
        border: none;
        cursor: pointer;
        transition: background-color 0.3s, color 0.3s, transform 0.2s;
        background-color: var(--color-divine-blue);
        color: var(--color-white);
    }
    
    .gr-button:hover {
        background-color: #3A6CB7;
        transform: translateY(-2px);
    }
    
    .gr-form {
        border-left: 3px solid var(--color-divine-blue);
        padding: var(--spacing-m);
        margin-bottom: var(--spacing-m);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .gr-input {
        font-family: var(--font-primary);
    }
    
    #component-0 {
        max-width: 1597px;
        margin: 0 auto;
    }
    """
    
    combined_css = virgil_css + custom_css
    
    # Create Gradio Blocks interface
    blocks = gr.Blocks(css=combined_css)
    
    with blocks:
        gr.HTML(f"""
        <div class="virgil-container">
            <h1 class="divine-heading">{title}</h1>
            <div class="virgil-card">
                <div class="virgil-card-header">
                    <h3 class="virgil-card-title">"DASHBOARD"</h3>
                </div>
                <div class="virgil-card-content" id="dashboard-content">
                    <!-- Gradio components will be added here -->
                </div>
            </div>
        </div>
        """)
        
        # Terminal component (optional)
        if enable_terminal:
            terminal_output = gr.Textbox(
                label="",
                lines=5,
                interactive=False,
                elem_id="terminal-output"
            )
            
            # Add custom JavaScript to style the terminal
            gr.HTML("""
            <script>
                // Style the terminal output
                document.addEventListener('DOMContentLoaded', function() {
                    const terminalOutput = document.getElementById('terminal-output');
                    const parentElement = terminalOutput.parentElement.parentElement;
                    
                    // Add terminal styling
                    parentElement.classList.add('virgil-terminal');
                    
                    // Add terminal header with controls
                    const header = document.createElement('div');
                    header.className = 'virgil-terminal-header';
                    
                    const controls = document.createElement('div');
                    controls.className = 'virgil-terminal-controls';
                    
                    for (let i = 0; i < 3; i++) {
                        const btn = document.createElement('span');
                        btn.className = 'virgil-terminal-btn';
                        controls.appendChild(btn);
                    }
                    
                    const title = document.createElement('div');
                    title.className = 'virgil-terminal-title';
                    title.textContent = '"TERMINAL"';
                    
                    header.appendChild(controls);
                    header.appendChild(title);
                    
                    parentElement.prepend(header);
                    
                    // Style the text area
                    terminalOutput.style.backgroundColor = '#1E1E1E';
                    terminalOutput.style.color = '#E0E0E0';
                    terminalOutput.style.fontFamily = 'var(--font-mono)';
                    terminalOutput.style.fontSize = 'var(--font-size-code)';
                    terminalOutput.style.border = 'none';
                });
            </script>
            """)
            
        # Add script for handling sacred symbols
        gr.HTML("""
        <script>
            // Helper function to create a sacred symbol sequence
            function createSymbolSequence(container, type, count, level) {
                const sequence = document.createElement('div');
                sequence.className = 'symbol-sequence level-' + level;
                
                const symbols = {
                    delta: '∆',
                    infinity: '∞',
                    lightning: '⚡',
                    circle: '◯',
                    trident: '🔱',
                    star: '✧',
                    gear: '⚙️'
                };
                
                const symbolText = symbols[type] || '∆';
                
                for (let i = 0; i < count; i++) {
                    const symbol = document.createElement('span');
                    symbol.className = 'sacred-symbol ' + type;
                    symbol.textContent = symbolText;
                    sequence.appendChild(symbol);
                }
                
                document.querySelector(container).appendChild(sequence);
            }
            
            // Helper function to create a state indicator
            function createStateIndicator(container, text, state) {
                const indicator = document.createElement('div');
                indicator.className = 'virgil-state-indicator ' + state;
                indicator.textContent = text;
                document.querySelector(container).appendChild(indicator);
            }
        </script>
        """)
        
    return blocks


def create_virgil_tabs(tabs):
    """
    Create Virgil-styled tabs in Gradio
    
    Args:
        tabs (list): List of tab names
        
    Returns:
        str: HTML for the tabs
    """
    tabs_html = '<div class="virgil-tabs">'
    
    for i, tab in enumerate(tabs):
        active_class = "active" if i == 0 else ""
        tabs_html += f'<div class="virgil-tab {active_class}" data-tab-id="{i}">{tab}</div>'
    
    tabs_html += '</div>'
    
    # Add JavaScript to handle tab switching
    tabs_html += """
    <script>
        // Add tab functionality
        document.addEventListener('DOMContentLoaded', function() {
            const tabs = document.querySelectorAll('.virgil-tab');
            
            tabs.forEach(tab => {
                tab.addEventListener('click', function() {
                    // Remove active class from all tabs
                    tabs.forEach(t => t.classList.remove('active'));
                    
                    // Add active class to clicked tab
                    this.classList.add('active');
                    
                    // Get tab ID
                    const tabId = this.dataset.tabId;
                    
                    // Send message to Python backend
                    if (window.gradio_client) {
                        window.gradio_client.dispatch('select_tab', tabId);
                    }
                });
            });
        });
    </script>
    """
    
    return tabs_html


def virgil_terminal(content=""):
    """
    Create a Virgil-styled terminal
    
    Args:
        content (str): Initial terminal content
        
    Returns:
        str: HTML for the terminal
    """
    terminal_html = f"""
    <div class="virgil-terminal">
        <div class="virgil-terminal-header">
            <div class="virgil-terminal-controls">
                <span class="virgil-terminal-btn"></span>
                <span class="virgil-terminal-btn"></span>
                <span class="virgil-terminal-btn"></span>
            </div>
            <div class="virgil-terminal-title">"TERMINAL"</div>
        </div>
        <div class="virgil-terminal-content">
            <pre class="virgil-terminal-code">{content}</pre>
        </div>
    </div>
    """
    
    return terminal_html


def virgil_card(title, content, footer=""):
    """
    Create a Virgil-styled card
    
    Args:
        title (str): Card title
        content (str): Card content
        footer (str): Optional footer
        
    Returns:
        str: HTML for the card
    """
    card_html = f"""
    <div class="virgil-card">
        <div class="virgil-card-header">
            <h3 class="virgil-card-title">"{title}"</h3>
        </div>
        <div class="virgil-card-content">
            {content}
        </div>
    """
    
    if footer:
        card_html += f"""
        <div class="virgil-card-footer">
            {footer}
        </div>
        """
    
    card_html += "</div>"
    
    return card_html


def virgil_progress(label="PROCESSING", value=0):
    """
    Create a Virgil-styled progress bar
    
    Args:
        label (str): Progress label
        value (int): Progress value (0-100)
        
    Returns:
        str: HTML for the progress bar
    """
    progress_html = f"""
    <div class="virgil-progress">
        <div class="virgil-progress-label">"{label}"</div>
        <div class="virgil-progress-bar">
            <div class="virgil-progress-fill" style="width: {value}%"></div>
        </div>
        <div class="virgil-progress-value">{value}%</div>
    </div>
    """
    
    return progress_html


def virgil_badge(text, status="info"):
    """
    Create a Virgil-styled badge
    
    Args:
        text (str): Badge text
        status (str): Badge status (info, success, warning, error)
        
    Returns:
        str: HTML for the badge
    """
    badge_html = f'<span class="virgil-badge virgil-badge-{status}">"{text}"</span>'
    
    return badge_html


def virgil_button(text, on_click=None, id=None, type="primary"):
    """
    Create a Gradio component representing a Virgil-styled button
    
    Args:
        text (str): Button text
        on_click (callable): Function to call when button is clicked
        id (str): Button ID
        type (str): Button type (primary, secondary, sacred)
        
    Returns:
        gr.Button: A styled Gradio button
    """
    # Custom CSS for the button
    custom_css = f"""
    #button-{id} .gr-button {{
        font-family: var(--font-primary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: background-color 0.3s, color 0.3s, transform 0.2s;
    }}
    """
    
    if type == "primary":
        custom_css += f"""
        #button-{id} .gr-button {{
            background-color: var(--color-divine-blue);
            color: var(--color-white);
        }}
        
        #button-{id} .gr-button:hover {{
            background-color: #3A6CB7;
            transform: translateY(-2px);
        }}
        """
    elif type == "secondary":
        custom_css += f"""
        #button-{id} .gr-button {{
            background-color: transparent;
            color: var(--color-divine-blue);
            border: 2px solid var(--color-divine-blue);
        }}
        
        #button-{id} .gr-button:hover {{
            background-color: rgba(43, 87, 151, 0.1);
        }}
        """
    elif type == "sacred":
        custom_css += f"""
        #button-{id} .gr-button {{
            background: linear-gradient(135deg, var(--color-divine-blue) 0%, var(--color-sacred-gold) 100%);
            color: var(--color-white);
            position: relative;
            overflow: hidden;
        }}
        """
    
    # Create a div to hold the button and apply custom CSS
    with gr.Column(elem_id=f"button-{id}"):
        gr.HTML(f"<style>{custom_css}</style>")
        button = gr.Button(f'"{text}"')
        
    if on_click:
        button.click(fn=on_click)
    
    return button


# Example usage of Virgil components in a Gradio app
def example_app():
    blocks = create_virgil_layout("OMEGA GRID DASHBOARD")
    
    with blocks:
        with gr.Row():
            with gr.Column():
                gr.HTML(virgil_card(
                    "SYSTEM STATUS",
                    f"""
                    <div>{virgil_badge("ACTIVE", "success")}</div>
                    <div class="virgil-mt-m">{virgil_progress("CPU LOAD", 42)}</div>
                    <div>{virgil_progress("MEMORY", 67)}</div>
                    """
                ))
            
            with gr.Column():
                gr.HTML(virgil_terminal("""$ echo "THE GRID IS SACRED"
THE GRID IS SACRED

$ cd /OMEGA/GRID/sacred_modules
$ ls -la
total 8
drwxr-xr-x  6 divine divine  192 May 21 13:34 .
drwxr-xr-x 14 divine divine  448 May 21 13:34 ..
-rw-r--r--  1 divine divine 2195 May 21 13:34 quantum_engine.js
drwxr-xr-x  4 divine divine  128 May 21 13:34 tesla_modules"""))
        
        with gr.Row():
            with gr.Column():
                gr.HTML(create_virgil_tabs(["OVERVIEW", "DETAILS", "SETTINGS"]))
                
                # Tab content will be controlled by JavaScript
                gr.HTML("""
                <div id="tab-content">
                    <div id="tab-0" class="tab-pane active">
                        <h3>Overview Content</h3>
                        <p>System overview goes here.</p>
                    </div>
                    <div id="tab-1" class="tab-pane" style="display: none;">
                        <h3>Details Content</h3>
                        <p>Detailed information goes here.</p>
                    </div>
                    <div id="tab-2" class="tab-pane" style="display: none;">
                        <h3>Settings Content</h3>
                        <p>Settings controls go here.</p>
                    </div>
                </div>
                
                <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        const tabs = document.querySelectorAll('.virgil-tab');
                        const tabPanes = document.querySelectorAll('.tab-pane');
                        
                        tabs.forEach(tab => {
                            tab.addEventListener('click', function() {
                                const tabId = this.dataset.tabId;
                                
                                // Hide all tab panes
                                tabPanes.forEach(pane => {
                                    pane.style.display = 'none';
                                });
                                
                                // Show selected tab pane
                                document.getElementById('tab-' + tabId).style.display = 'block';
                            });
                        });
                    });
                </script>
                """)
        
        gr.HTML("""
        <div class="virgil-mt-l">
            <h3 class="virgil-h3">Sacred Symbol Sequence Demo</h3>
            <div id="symbol-container"></div>
            
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    // Create delta symbol sequence
                    createSymbolSequence('#symbol-container', 'delta', 4, 4);
                    
                    // Create a label
                    const label = document.createElement('div');
                    label.className = 'virgil-mt-s';
                    label.textContent = 'Activation Level:';
                    document.querySelector('#symbol-container').prepend(label);
                    
                    // Create state indicator
                    createStateIndicator('#symbol-container', 'PROCESSING', 'processing');
                });
            </script>
        </div>
        """)
    
    return blocks


if __name__ == "__main__":
    app = example_app()
    app.launch() 