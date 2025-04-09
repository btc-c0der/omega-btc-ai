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
