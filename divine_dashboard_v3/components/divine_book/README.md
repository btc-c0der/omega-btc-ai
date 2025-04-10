# Divine Book Components

This directory contains the Divine Book components for the Omega BTC AI project.

## Overview

The Divine Book components provide interfaces for analyzing sacred texts and detecting quantum resonance patterns. The components include:

- `divine_book_dashboard.py`: A simplified dashboard for analyzing text resonance patterns
- `divine_book_browser.py`: An advanced browser with additional visualization features
- `run_divine_book.py`: A script to run the Divine Book components
- `test_dependencies.py`: A utility to verify required dependencies are installed
- `common/`: Shared utilities used by both components

Both the dashboard and browser components now scan and load Markdown files from the entire repository, providing a consistent experience.

## Features Comparison

| Feature | Dashboard | Browser |
|---------|-----------|---------|
| Repository Document Scanning | ✅ | ✅ |
| Sample Texts | ✅ | ✅ |
| Resonance Analysis | ✅ | ✅ |
| Resonance Visualizations | ✅ | ✅ |
| Markdown Rendering | ❌ | ✅ |
| Repository File Tree | ❌ | ✅ |
| Advanced Pattern Visualization | ❌ | ✅ |

## Prerequisites

Before running the Divine Book components, ensure you have the following dependencies installed:

```bash
pip install -r requirements.txt
```

You can verify your dependencies are properly installed by running:

```bash
python test_dependencies.py
```

This will display a table showing all required and optional dependencies and their status.

## Running the Components

### Divine Book Dashboard

To run the simplified Divine Book Dashboard:

```bash
cd divine_dashboard_v3
python components/divine_book/divine_book_dashboard.py
```

This will launch a Gradio interface that allows you to:

- Load and browse various sacred texts
- Analyze text passages for resonance patterns
- Visualize resonance scores and alignments

### Divine Book Browser

To run the advanced Divine Book Browser:

```bash
cd divine_dashboard_v3
python components/divine_book/divine_book_browser.py
```

The browser provides additional features:

- Explore Markdown files from the repository
- Rendered preview of Markdown documents
- Advanced resonance analysis with customizable weights
- Visual pattern distribution via bar and radar charts

### Using the Run Script

Alternatively, you can use the run script which supports both components:

```bash
cd divine_dashboard_v3
python components/divine_book/run_divine_book.py --mode [dashboard|browser]
```

Options:

- `--mode dashboard`: Run the simplified dashboard (default)
- `--mode browser`: Run the advanced browser
- `--share`: Share the Gradio interface through a public URL
- `--port PORT`: Specify a custom port (default: 7860)

## Environment Variables

You can also configure the components using environment variables:

- `GRADIO_SHARE`: Set to "true" to enable sharing (public URL)
- `GRADIO_PORT`: Set a custom port number
- `DIVINE_MODE`: Set to "dashboard" or "browser"

Example:

```bash
GRADIO_SHARE=true DIVINE_MODE=browser python components/divine_book/run_divine_book.py
