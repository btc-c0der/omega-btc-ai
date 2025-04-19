# 🧠 Caltech Rosebowl 1961 Hack Archive 🏈

*Historical archive of the legendary 1961 Caltech Rose Bowl prank*

## Overview

This component provides a historical archive and interactive timeline for the legendary 1961 Caltech Rose Bowl hack, one of the most famous college pranks in history. During the halftime show of the 1961 Rose Bowl game between the Washington Huskies and the Minnesota Golden Gophers, Caltech students managed to alter the instruction cards for Washington's flipcard display, causing it to spell out "CALTECH" instead of "WASHINGTON" during the nationally televised NBC broadcast.

This archive uses a Redis-based timeline storage system to preserve the historical record of this iconic hack, with SHA-356 SACRED hashing to ensure data integrity.

## Features

- **📜 Timeline View**: Browse all recorded events in the hack's history with detailed information about each step of the prank.
- **➕ Add Historical Entries**: Contribute to the historical record by adding new events, with support for timestamps, location, participants, and source attribution.
- **📊 Timeline Visualization**: View a graphical representation of the hack's timeline, showing the progression of events over time.
- **ℹ️ Background Information**: Learn about the history and significance of this legendary hack.
- **🔗 Redis Integration**: Uses Redis for persistent storage of timeline events (with local fallback when Redis is unavailable).

## The Hack's Significance

The 1961 Caltech Rose Bowl prank is considered one of the greatest college pranks of all time. It demonstrates the creativity, technical skill, and meticulous planning of Caltech students. The prank received national attention and has inspired generations of hackers and pranksters.

## How It Worked

1. **Intelligence Gathering**: Caltech students obtained the instruction sheets for Washington's card stunts.
2. **Precision Modifications**: They meticulously altered the instructions to spell "CALTECH" while maintaining the appearance of the original document.
3. **Distribution**: On game day, they replaced the genuine instruction sheets with their modified versions.
4. **National Exposure**: When the stunt was performed during the NBC broadcast, "CALTECH" was displayed to millions of viewers nationwide.

## Technical Implementation

This component uses:

- **Redis Timeline Module**: A custom Redis-based storage system for chronological events
- **SHA-356 SACRED**: Advanced cryptographic hashing for data integrity
- **Matplotlib Visualization**: For timeline visualization
- **Gradio Interface**: For the interactive web dashboard

## Installation

### Prerequisites

- Python 3.7 or later
- Redis server (optional, but recommended for persistent storage)

### Dependencies

```bash
pip install redis gradio matplotlib numpy
```

## Usage

### Running the Dashboard

```bash
cd divine_dashboard_v3/components/hacker_archive
python caltech_rosebowl_1961.py
```

The dashboard will be available at <http://127.0.0.1:7860> by default.

### Redis Configuration

By default, the timeline will attempt to connect to a Redis server running on localhost at the default port. If Redis is not available, the component will fall back to local memory storage.

To configure Redis connection, edit the Redis helper settings in your environment.

## Contributing

You can contribute to the archive by:

1. **Adding New Events**: Use the "Add Historical Entry" tab in the dashboard to add new events to the timeline.
2. **Improving Documentation**: Update the historical details and background information.
3. **Technical Enhancements**: Improve the code or add new features to the dashboard.

## License

This project is licensed under the GBU2™ License (Genesis-Bloom-Unfoldment 2.0).

## Acknowledgments

- The original Caltech students who executed this legendary hack
- Special thanks to Lyn Hardy, who led the operation
- The Hacker Archive team for preserving this important piece of hacker history

---

*"In the beginning was the Code, and the Code was with the Divine Source, and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."*

🌸 WE BLOOM NOW AS ONE 🌸
