# IBR España Micro-Modules

This directory contains modular components that power the IBR España section of the Divine Dashboard v3.

## Available Modules

### `instagram_manager.py`

Instagram account management system for @ibrespana with comprehensive features for post scheduling, comment management, analytics reporting, outreach campaigns, and livestream monitoring.

#### Classes and Data Structures

1. **Post**
   - Represents an Instagram post (scheduled or published)
   - Properties: id, image_path, caption, scheduled_time, first_comment, status, posted_at, likes, comments_count, media_type
   - Methods: to_dict(), from_dict()

2. **Comment**
   - Represents an Instagram comment on a post
   - Properties: id, post_id, username, text, created_at, is_hidden, parent_id
   - Methods: to_dict(), from_dict()

3. **AnalyticsReport**
   - Represents an Instagram analytics report
   - Properties: id, start_date, end_date, metrics, generated_at, frequency, recipients
   - Methods: to_dict(), from_dict()

4. **OutreachCampaign**
   - Represents an Instagram outreach campaign
   - Properties: id, name, target_audience, message_template, created_at, status, leads
   - Methods: to_dict(), from_dict()

5. **InstagramManager**
   - Main class that handles all Instagram management functionality
   - Key method groups:
     - Data handling: _load_data(), _save_*()
     - Post scheduling: schedule_post(), edit_scheduled_post(), delete_scheduled_post(), get_scheduled_posts()
     - Comment management: add_comment(), get_comments(), hide_comment(), reply_to_comment()
     - Auto-replies: add_auto_reply_rule(), process_auto_replies()
     - Analytics: generate_analytics_report(), schedule_analytics_report()
     - Outreach: create_outreach_campaign(), add_outreach_lead(), get_outreach_leads()
     - Livestream: start_livestream_monitoring(), stop_livestream_monitoring(), add_livestream_comment()

#### Data Storage

The InstagramManager uses a directory structure to store all data as JSON files:

```
/ibr_data/instagram_manager/
  ├── posts/
  │   ├── scheduled_posts.json
  │   └── published_posts.json
  ├── comments/
  │   ├── comments.json
  │   └── auto_reply_rules.json
  ├── reports/
  │   ├── analytics_reports.json
  │   └── scheduled_reports.json
  ├── campaigns/
  │   └── outreach_campaigns.json
  └── livestreams/
      └── active_livestreams.json
```

#### Implementation Notes

- All data is persisted to disk immediately after any change
- UUIDs are used for all object IDs to ensure uniqueness
- Current implementation uses mock data for analytics, but is designed with real API integration in mind
- Technical issue detection uses a keyword-based approach for livestream comments

### `instagram_integration.py`

Basic Instagram integration for displaying the church's Instagram feed in the dashboard.

### `sermon_library.py`

Manages the church's sermon library with search and categorization features.

### Other modules

Additional modules include prayer requests, church events, and devotionals management.

## Integration with Dashboard

All modules are designed to be included in the main IBR España dashboard interface (`ibr_dashboard.py`). The dashboard creates appropriate UI components for each module and handles user interactions.

## Development Guidelines

1. **Extending functionality**:
   To add new Instagram features, extend the InstagramManager class in instagram_manager.py and add corresponding UI elements in the dashboard interface.

2. **API integration**:
   The current implementation is designed to work offline with local data, but includes placeholder methods for future Instagram API integration.

3. **Error handling**:
   All methods include comprehensive error handling and logging to ensure stability.

4. **Testing**:
   Unit tests for each module are available in the `tests` directory.

## Technical Requirements

- Python 3.7+
- JSON for data storage
- Pathlib for file handling
- UUID for object identification
- Datetime for scheduling and timestamps
- Logging for error tracking

## Future Development Roadmap

1. Integration with Instagram Graph API for real posting capabilities
2. Real-time notifications for comments and technical issues
3. Advanced analytics with visualization
4. AI-powered content suggestions

---

© OMEGA BTC AI | Developed for IBR España
