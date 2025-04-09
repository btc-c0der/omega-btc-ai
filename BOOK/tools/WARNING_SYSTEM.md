# OMEGA BTC AI Warning System

## Overview

The OMEGA BTC AI Warning System is a robust monitoring and diagnostics tool that stores system warnings and errors in Redis rather than simply logging them to the console. This approach provides several advantages:

1. **Reduced Console Noise**: Keeps the console output clean by minimizing warning messages
2. **Historical Analysis**: Maintains a searchable history of warnings for post-mortem analysis
3. **Pattern Detection**: Allows tracking of warning frequency and patterns over time
4. **Categorization**: Organizes warnings by type and source for better troubleshooting

## Warning Types

The system categorizes warnings into various types:

| Warning Type | Description |
|--------------|-------------|
| `NO_TREND_DATA` | No trend data available for a particular timeframe |
| `FALLBACK_USED` | Successfully used a fallback data source |
| `FALLBACK_FAILED` | Attempted to use fallback data but failed |
| `NO_FALLBACK_DATA` | No fallback data sources available |
| `FALLBACK_ERROR` | Error encountered while using fallback mechanisms |
| `SYSTEM_STARTUP` | System initialization events |

## Checking Warnings

The `check_warnings.py` tool provides a simple command-line interface to view and manage warnings stored in Redis:

```bash
# Show latest 10 warnings
python check_warnings.py

# Show all warnings
python check_warnings.py --all

# Show warnings of a specific type
python check_warnings.py --type NO_TREND_DATA

# Show warning counts by type
python check_warnings.py --count

# Clear all warnings (keeps counts)
python check_warnings.py --clear

# Reset warning counters
python check_warnings.py --reset
```

## Redis Storage Structure

Warnings are stored in Redis using the following keys:

- `system:warnings` - A list of all warnings (JSON format), newest first
- `system:warnings:{TYPE}` - Lists of warnings by type
- `system:warning_counts` - Hash of warning counts by type

## Implementation

The warning system is implemented in the `monitor_market_trends_fixed.py` module, with the following key components:

1. `store_warning_in_redis()` - Stores warnings in Redis
2. `check_system_warnings()` - Retrieves and summarizes warnings
3. Modified logging - Uses DEBUG level for regular warnings to reduce console output

## Example Output

When checking warnings:

```
SYSTEM WARNINGS of type NO_TREND_DATA (showing latest 10, total: 24)
Timestamp           Type           Source                 Message
------------------  -------------  ---------------------  -------------------------------------------------
2023-03-24 22:15:43  NO_TREND_DATA  trap_detector_15min    No trend data available for timeframe 15min. Attempting fallback.
2023-03-24 22:15:43  NO_TREND_DATA  trap_detector_30min    No trend data available for timeframe 30min. Attempting fallback.
2023-03-24 22:15:43  NO_TREND_DATA  trap_detector_60min    No trend data available for timeframe 60min. Attempting fallback.
```

## Extending the Warning System

To add a new warning type:

1. Call `store_warning_in_redis()` with appropriate parameters
2. Use a consistent naming convention for warning types (ALL_CAPS_WITH_UNDERSCORES)
3. Include meaningful source identification to trace the warning origin

## Integration with Monitoring Tools

The warning system can be integrated with monitoring tools by:

1. Creating a monitoring endpoint that calls `check_system_warnings()`
2. Setting up alerts based on warning counts or specific warning types
3. Visualizing warning patterns through time-series dashboards
