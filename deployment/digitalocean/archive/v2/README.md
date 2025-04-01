# BTC Live Feed v2 Archive

This directory contains archived files from BTC Live Feed v2, which was replaced by v3 on March 28, 2025.

## Archived Files

1. **Source Code**:
   - `btc_live_feed_v2.py` - Main implementation file
   - `btc_live_feed_v2.py` (from deployment) - Deployment-specific implementation

2. **Configuration**:
   - `app.yaml` - DigitalOcean app specification
   - `Dockerfile` - Container configuration

3. **Deployment**:
   - `btc_live_feed_deployment_plan.md` - Deployment documentation

4. **Process Management**:
   - `Procfile` - Process configuration

5. **Tests**:
   - `test_btc_live_feed_security.py` - Security test suite

## Why These Files Were Archived

These files were archived to:

1. Prevent accidental use of v2 alongside v3
2. Maintain historical reference
3. Allow for rollback if needed
4. Keep the codebase clean and focused on v3

## Key Differences from v3

v3 introduced several improvements over v2:

- Automatic Redis failover
- Health monitoring
- Enhanced error handling
- Data synchronization
- Improved security features

## How to Restore (If Needed)

To restore v2:

1. Copy all files from this archive to their original locations
2. Update the Procfile to use v2
3. Update deployment configurations
4. Note: This is not recommended as v3 provides better reliability and features

## Contact

For questions about the archive or v2 implementation:

- Check the original documentation in `BOOK/BTC_LIVE_FEED_V2.md`
- Contact the OMEGA BTC AI team
