# IBR España Instagram Manager Installation Guide

This guide provides step-by-step instructions for installing and setting up the Instagram Manager component for the IBR España section of the Divine Dashboard v3.

## System Requirements

- Python 3.7 or higher
- 500MB disk space for data storage
- Internet connection for API integration (optional)
- Administrator/sudo privileges (for system-level installations)

## Installation Steps

### 1. Install Base Divine Dashboard v3

If you haven't already installed the base Divine Dashboard v3, follow these steps:

```bash
# Clone the repository
git clone https://github.com/omegabtc/divine-dashboard.git
cd divine-dashboard

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Install Component-Specific Dependencies

The Instagram Manager requires additional packages:

```bash
pip install requests pillow schedule
```

### 3. Configure Data Storage

By default, the Instagram Manager stores data in the user's home directory at `~/ibr_data/instagram_manager`. To use a custom location:

1. Create a configuration file at `divine_dashboard_v3/config/ibr_spain.json`:

```json
{
  "instagram_manager": {
    "data_dir": "/path/to/your/custom/data/directory",
    "account_name": "ibrespana"
  }
}
```

2. Ensure the directory exists and has proper permissions:

```bash
mkdir -p /path/to/your/custom/data/directory
chmod 755 /path/to/your/custom/data/directory
```

### 4. Initialize the Instagram Manager

After installation, the Instagram Manager needs to be initialized:

```bash
cd divine_dashboard_v3
python -c "from components.ibr_spain.micro_modules.instagram_manager import InstagramManager; InstagramManager()"
```

This will create the necessary directory structure and initial data files.

### 5. (Optional) Instagram API Integration

For actual Instagram posting and API integration:

1. Create a Facebook Developer account at <https://developers.facebook.com/>
2. Create a new app for the Instagram Graph API
3. Get your access token
4. Add the token to your configuration:

```json
{
  "instagram_manager": {
    "data_dir": "/path/to/your/custom/data/directory",
    "account_name": "ibrespana",
    "api": {
      "access_token": "YOUR_ACCESS_TOKEN",
      "client_id": "YOUR_CLIENT_ID",
      "client_secret": "YOUR_CLIENT_SECRET"
    }
  }
}
```

### 6. Launch the Dashboard

To start the Divine Dashboard with the IBR España components including the Instagram Manager:

```bash
cd divine_dashboard_v3
python main.py
```

The dashboard will be available at <http://localhost:7860> (default port).

## Verifying Installation

To verify that the Instagram Manager is installed correctly:

1. Open the Divine Dashboard in your browser
2. Navigate to the IBR España section
3. Click on the "Instagram Manager" tab
4. You should see the Instagram Manager interface with the following tabs:
   - Schedule Posts
   - Manage Comments
   - Analytics
   - Outreach
   - Livestream Monitoring

If any of these tabs are missing or the interface doesn't load, check the logs for errors.

## Troubleshooting

### Common Issues

1. **Missing dependencies error**

   ```
   ImportError: No module named 'requests'
   ```

   Solution: Install the missing package: `pip install requests`

2. **Permission denied error**

   ```
   PermissionError: [Errno 13] Permission denied: '/path/to/data/directory'
   ```

   Solution: Check the directory permissions or use a different directory

3. **Module not found error**

   ```
   ModuleNotFoundError: No module named 'components.ibr_spain.micro_modules.instagram_manager'
   ```

   Solution: Ensure you're running the command from the correct directory

4. **Instagram API errors**

   ```
   {"error":{"message":"Invalid OAuth access token.","type":"OAuthException","code":190}}
   ```

   Solution: Refresh your access token or check if it's correctly configured

### Logs and Debugging

The Instagram Manager logs activities to `ibr_spain_dashboard.log` by default. For more detailed logging:

1. Set the logging level to DEBUG in your configuration file:

   ```json
   {
     "instagram_manager": {
       "logging_level": "DEBUG"
     }
   }
   ```

2. Check the logs for detailed information:

   ```bash
   tail -f ibr_spain_dashboard.log
   ```

## Updating

To update the Instagram Manager component:

1. Pull the latest changes from the repository:

   ```bash
   git pull origin main
   ```

2. Update dependencies if needed:

   ```bash
   pip install -r requirements.txt
   ```

3. Restart the dashboard

## Uninstallation

To remove the Instagram Manager:

1. Remove the data directory (warning: this will delete all stored data):

   ```bash
   rm -rf ~/ibr_data/instagram_manager
   ```

2. Reinstall the base Divine Dashboard without the IBR España components

## Support

For additional support, contact the OMEGA BTC AI team.

---

© IBR España 2023 | Developed by OMEGA BTC AI
