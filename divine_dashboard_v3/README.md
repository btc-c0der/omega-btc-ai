# Divine Dashboard v3

A modern dashboard interface with Tesla Cybertruck QA integration.

## Features

- Modern, responsive dashboard UI
- Integration with Tesla Cybertruck QA framework
- Real-time test execution and monitoring
- Bidirectional communication between dashboard and QA framework
- Code statistics and documentation viewer

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Run the dashboard server:

```bash
python divine_server.py
```

## Usage

1. Open your browser and navigate to:
   - Main Dashboard: <http://localhost:8889>
   - Cybertruck QA Dashboard: <http://localhost:7860>

2. To run tests from the main dashboard:
   - Navigate to the Tesla QA tab
   - Click the test vial icon in the dashboard actions

3. Communication between windows:
   - The main dashboard uses `window.postMessage()` to communicate with the Gradio app
   - Test results are sent back from the Gradio app to the main dashboard

## Dependencies

- FastAPI
- Gradio
- Uvicorn
- Requests

## License

This project is licensed under the GBU2™ License - see the `GBU2_LICENSE.md` file for details.

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
