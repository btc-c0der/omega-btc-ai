# Divine Dashboard v3

A powerful dashboard interface for the OMEGA GRID system.

## 🎨 Design System

The `VIRGIL GRID UI` is a minimalist symbolic interface inspired by Virgil Abloh and sacred design traditions. It follows a disciplined approach:

- Typography is voice
- Space is silence
- Symbols are truth

📁 Explore `/design_guide/` for full documentation.

### Design Philosophy

VIRGIL GRID UI embodies:

- **Sacred Calm**: Interfaces that provide breathing room and focused attention
- **Symbolic Minimalism**: Using the least to say the most
- **Technical Reverence**: Honoring the code beneath the surface
- **Divine Clarity**: Communication without unnecessary complexity
- **Informed Contrast**: Sharp distinctions between elements, honoring the off-white tradition

### Implementation

The design system is implemented through:

```html
<!-- HTML integration -->
<link rel="stylesheet" href="/static/css/virgil.css">
<script src="/static/js/virgil-ui.js"></script>
```

```python
# Gradio integration
import gradio as gr
from components.virgil_gradio_components import create_virgil_layout

with create_virgil_layout("DASHBOARD TITLE") as demo:
    # Your Gradio components here
    pass
```

## 🚀 Features

- Modern, responsive dashboard interface
- Real-time monitoring and visualizations
- Crypto and hash components
- Quantum systems integration
- Creator tools
- Performance metrics
- Task management

## 📋 Requirements

See `requirements.txt` for dependencies.

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/example/divine-dashboard.git

# Navigate to the project directory
cd divine-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
python launch_dashboard.py
```

## 📚 Documentation

- `/design_guide/README.md` - Design system overview
- `/design_guide/virgil_style_guide.md` - Typography, color, spacing and layout
- `/design_guide/components.md` - UI components
- `/design_guide/symbolic_language.md` - Meaning behind typographic choices and symbols

## 💻 Usage

### Basic Dashboard

```python
from divine_dashboard_v3.components.virgil_gradio_components import create_virgil_layout, virgil_card, virgil_terminal

def create_app():
    blocks = create_virgil_layout("MY DASHBOARD")
    
    with blocks:
        with gr.Row():
            with gr.Column():
                gr.HTML(virgil_card(
                    "SYSTEM STATUS",
                    "System status information goes here."
                ))
            
            with gr.Column():
                gr.HTML(virgil_terminal("$ echo 'Hello World'"))
    
    return blocks

app = create_app()
app.launch()
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the terms of the GBU2™ License (Genesis-Bloom-Unfoldment 2.0).

🌸 WE BLOOM NOW AS ONE 🌸

## Components

The Divine Book Dashboard v3 includes the following major components:

1. **Core Dashboard**: The main interface for exploring the Divine Book
2. **Divine Server**: Backend server handling data processing and API endpoints
3. **Visualization Components**: Interactive charts and data visualizations
4. **Tesla Cybertruck QA Dashboard**: Advanced testing framework for Tesla Cybertruck components

## Running the Dashboard

### Main Dashboard

```bash
./run_server.sh
```

### Tesla Cybertruck QA Dashboard

```bash
./run_tesla_qa_dashboard.sh
```

# Divine Dashboard v3 - GitHub to Hugging Face Deployment

## Connecting GitHub Repository to Hugging Face Spaces

### Step 1: Create a Hugging Face Space

1. Go to [Hugging Face](https://huggingface.co/) and sign in to your account
2. Navigate to your profile and click on "Spaces"
3. Click "Create new Space"
4. Fill in the following details:
   - **Space name**: `divine-dashboard-v3` (or any unique name you prefer)
   - **License**: Choose appropriate license (MIT is common)
   - **SDK**: Select "Gradio" for the DNA Portal and dashboards
   - **Space hardware**: Choose "CPU" (free tier) to start

### Step 2: Link GitHub Repository

1. Instead of creating an empty Space, choose "Import from GitHub"
2. Enter your GitHub repo URL: `https://github.com/btc-c0der/omega-btc-ai`
3. Choose the correct branch: `divine-book-dashboard-v3`
4. You can specify a subdirectory: `divine_dashboard_v3` if needed

### Step 3: Configure for Deployment

For Gradio apps to deploy correctly, ensure you have:

1. A `requirements.txt` file in your directory with all dependencies:

   ```
   gradio>=3.32.0
   fastapi>=0.95.2
   uvicorn>=0.22.0
   numpy>=1.24.3
   matplotlib>=3.7.1
   pillow>=10.0.0
   python-multipart>=0.0.6
   schedule>=1.2.0
   ```

2. A `.huggingface` file to customize the Space (already created)

3. An `app.py` file that Hugging Face will run automatically. Create this file to point to your main application.

### Step 4: Create an app.py File

Create a simple `app.py` file that will be the entry point for your Space:

```python
#!/usr/bin/env python3
import gradio as gr
import os
import sys

# Determine which component to launch
COMPONENT = os.environ.get("HF_COMPONENT", "DNA_PORTAL")

if COMPONENT == "DNA_PORTAL":
    # Import and run DNA Portal
    from dna_pcr_quantum_portal import iface
    # The iface object is already defined in the imported file
elif COMPONENT == "DASHBOARD":
    # Import and run main dashboard
    from divine_server import create_gradio_interface
    iface = create_gradio_interface()
else:
    # Default to DNA Portal
    from dna_pcr_quantum_portal import iface

# Launch with Hugging Face Spaces configuration
if __name__ == "__main__":
    iface.launch()
```

### Step 5: Enable GitHub Actions (Optional)

You can set up GitHub Actions for automated deployment:

1. Create a `.github/workflows/hf-sync.yml` file
2. Use Hugging Face's GitHub Action to automatically sync your repo

### Step 6: Deploy with a Direct Link from Hugging Face

Once set up, you can deploy directly from the command line using your Hugging Face token:

```bash
huggingface-cli login
huggingface-cli repo create space btc-c0der/divine-dashboard-v3 --repo-type space --space-sdk gradio
git remote add space https://huggingface.co/spaces/btc-c0der/divine-dashboard-v3
git push --force space divine-book-dashboard-v3:main
```

Replace `btc-c0der` with your actual Hugging Face username.

## Multiple Component Deployment

You can create separate Spaces for each component:

- DNA Portal: `btc-c0der/dna-quantum-portal`
- Main Dashboard: `btc-c0der/divine-dashboard-v3`
- NFT Dashboard: `btc-c0der/divine-nft-dashboard`
