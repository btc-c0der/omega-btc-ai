# IBR España Instagram Manager

## Overview

The IBR España Instagram Manager is a comprehensive tool for managing the church's Instagram account (@ibrespana). This module integrates directly with the Divine Dashboard v3 and provides a complete suite of Instagram management features.

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

### Installation

This module is part of the Divine Dashboard v3 and is automatically included when installing the IBR España component.

### Configuration

No additional configuration is needed beyond the standard IBR España dashboard setup.

### Dependencies

- Python 3.7+
- Gradio (for UI components)
- Standard Python libraries: json, pathlib, datetime, logging, uuid

### Data Storage

All data is stored locally in JSON format in the following structure:

- `posts/`: Contains scheduled and published posts
- `comments/`: Contains comments and auto-reply rules
- `reports/`: Contains analytics reports and scheduled report configurations
- `campaigns/`: Contains outreach campaign data and leads
- `livestreams/`: Contains active livestream data and comments

## Usage Guide

### Accessing the Manager

The Instagram Manager is available as a tab in the IBR España dashboard interface. Navigate to "Instagram Manager" to access all features.

### Scheduling Posts

1. Go to the "Schedule Posts" tab
2. Fill in the image path, caption, and scheduled time
3. Optionally add a first comment for hashtags
4. Click "Schedule Post"

### Managing Comments

1. Go to the "Manage Comments" tab
2. Set up auto-reply rules by defining keywords and reply templates
3. Click "Process Auto-Replies" to apply rules to existing comments

### Generating Reports

1. Go to the "Analytics" tab
2. Set the start and end dates for your report
3. Click "Generate Report" to view metrics
4. To schedule recurring reports, select frequency and add recipient emails

### Creating Outreach Campaigns

1. Go to the "Outreach" tab
2. Create a new campaign with a name, target audience, and message template
3. Add leads to the campaign with custom messages

### Monitoring Livestreams

1. Go to the "Livestream Monitoring" tab
2. Enter the stream ID and start monitoring
3. View comments and technical issues in real-time
4. Stop monitoring when the livestream ends

## Support

For questions or issues regarding the Instagram Manager, please contact the OMEGA BTC AI team.

## Credits

Developed by OMEGA BTC AI for IBR España as part of the Divine Dashboard v3 project.

## License

This software is licensed for the exclusive use of IBR España.

---

© IBR España 2023 | Desarrollado con �� por OMEGA BTC AI
