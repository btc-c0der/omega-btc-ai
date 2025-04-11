# IBR España Instagram Manager

## Overview

The IBR España Instagram Manager is a comprehensive tool for managing the church's Instagram account (@ibrespana). This module integrates directly with the Divine Dashboard v3 and provides a complete suite of Instagram management features.

## 🔄 Recent Updates

- **April 11, 2025**: Fixed indentation error in Instagram data fetching code
- **April 11, 2025**: Reorganized component files into a more maintainable structure
- **April 11, 2025**: Enhanced follower count extraction from meta description

See [REORGANIZATION.md](./docs/REORGANIZATION.md) for details on the directory structure changes.
See [BUG_FIX_LOG_IBR_SPAIN.md](./docs/BUG_FIX_LOG_IBR_SPAIN.md) for details on the bug fixes.

## Component Structure

```
ibr_spain/
├── docs/                   # Documentation files
├── standalone/             # Standalone version
├── tests/                  # Test files
├── micro_modules/          # Smaller feature modules
├── ibr_dashboard.py        # Main component implementation
├── __init__.py             # Package initialization
└── README.md               # This file
```

## Running the Component

### Standalone Mode

To run the IBR España component as a standalone dashboard:

```bash
cd divine_dashboard_v3/components/ibr_spain/standalone
./run_ibr_standalone.sh
```

The dashboard will be available at <http://localhost:7863> (or the next available port).

### Integrated with Divine Server

To run the IBR España component integrated with the main Divine Server:

```bash
cd divine_dashboard_v3/components/ibr_spain/standalone
./run_ibr_with_server.sh
```

### Running Tests

To run the tests for the IBR España component:

```bash
cd divine_dashboard_v3/components/ibr_spain/tests
./run_ibr_tests.sh
```

## Features

### Post Scheduling

- Schedule Instagram posts with images, captions, and first comments
- Edit or delete scheduled posts
- View all upcoming scheduled content
- Support for automatically posting first comments (ideal for hashtags)

### Comment Management

- Monitor and manage all post comments
- Hide inappropriate or spam comments
- Reply to comments directly from the dashboard
- Set up automatic responses based on keywords

### Analytics Reporting

- Generate detailed analytics reports for any date range
- View key metrics including followers, engagement rate, reach, and impressions
- Schedule recurring reports (daily, weekly, monthly)
- Email reports to multiple team members automatically

### Outreach Campaigns

- Create targeted outreach campaigns
- Define custom message templates
- Add leads to campaigns with personalized messages
- Track campaign performance and lead status

### Livestream Monitoring

- Monitor Instagram Live streams in real-time
- Detect and flag technical issues
- View all livestream comments in one place
- Receive notifications for important issues

## Technical Details

### Configuration

Create a JSON file at `divine_dashboard_v3/config/ibr_spain.json`:

```json
{
  "instagram_manager": {
    "data_dir": "/path/to/data",
    "account_name": "ibrespana",
    "api_credentials": {
      "access_token": "your_access_token",
      "client_id": "your_client_id",
      "client_secret": "your_client_secret",
      "page_id": "your_page_id",
      "instagram_account_id": "your_instagram_account_id"
    }
  }
}
```

### Dependencies

- Python 3.7+
- Gradio (for UI components)
- BeautifulSoup4 (for Instagram data extraction)
- Requests (for API communication)
- Standard Python libraries: json, pathlib, datetime, logging, uuid

## Data Modes

The component can operate in two modes:

1. **Sample Data Mode**: When API credentials are not provided, the component uses sample data
2. **Real Data Mode**: When API credentials are provided, the component fetches real data from Instagram

## Support

For questions or issues regarding the Instagram Manager, please contact the OMEGA BTC AI team.

## Credits

Developed by OMEGA BTC AI for IBR España as part of the Divine Dashboard v3 project.

## License

This software is licensed for the exclusive use of IBR España.

---

© IBR España 2025 | Desarrollado con ❤️ por OMEGA BTC AI
