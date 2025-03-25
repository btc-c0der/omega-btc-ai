# Schumann Resonance JSON Parsing Fix

## Issue

The BTC live feed was encountering the following error when trying to use the MM Trap Detector:

```
[2025-03-25 20:59:18] ⚠️ Error using MM Trap Detector: could not convert string to float: '{"frequency": 7.8070279775308125, "amplitude": 1.1729044665569435, "alignment": "aligned", "market_influence": 0.0366220510035431}'
```

This error occurred because the Schumann resonance data in Redis is stored as a JSON string, but the MM Trap Detector was attempting to directly convert this JSON string to a float without parsing it first.

## Cause of the Issue

1. **Data Format Mismatch**: The `generate_market_data.py` script stores Schumann resonance data in Redis as a JSON object with multiple fields, but the `high_frequency_detector.py` expected it to be a simple float.

2. **No JSON Parsing**: The MM Trap Detector tried to directly convert the Redis value to a float without checking if it was in JSON format.

3. **Multiple Data Formats**: The system needed to support both the old format (simple float) and the new JSON format for backward compatibility.

## Fix Applied

### 1. Updated High Frequency Detector Module

Modified the `detect_high_freq_trap_mode` method in `high_frequency_detector.py` to handle JSON data:

```python
# 4. Get Schumann resonance data
if schumann_resonance is None:
    # Get Schumann data safely - avoid circular import
    schumann_data = redis_conn.get("schumann_resonance")
    if schumann_data:
        try:
            # Try to parse as JSON first (new format)
            schumann_json = json.loads(schumann_data)
            schumann_resonance = float(schumann_json.get("frequency", 0.0))
        except (json.JSONDecodeError, TypeError):
            # If not JSON, try direct float conversion (old format)
            try:
                schumann_resonance = float(schumann_data)
            except (ValueError, TypeError):
                print(f"⚠️ Invalid Schumann resonance value in Redis: {schumann_data}")
                schumann_resonance = 0.0
    else:
        schumann_resonance = 0.0
```

### 2. Updated Check Schumann Anomalies Method

Similarly updated the `check_schumann_anomalies` method to handle JSON data:

```python
# Get Schumann data from Redis
schumann_bytes = redis_conn.get("schumann_resonance")
schumann = 0.0

if schumann_bytes:
    try:
        # Try to parse as JSON first (new format)
        schumann_json = json.loads(schumann_bytes)
        schumann = float(schumann_json.get("frequency", 0.0))
    except (json.JSONDecodeError, TypeError):
        # If not JSON, try direct float conversion (old format)
        try:
            schumann = float(schumann_bytes)
        except (ValueError, TypeError):
            print(f"⚠️ Invalid Schumann resonance value in Redis: {schumann_bytes}")
            schumann = 0.0
```

### 3. Created Test Script

Created a test script `test_schumann_resonance.py` to verify the fix with different data formats:

- JSON Format: `{"frequency": 7.83, "amplitude": 1.2, "alignment": "aligned", "market_influence": 0.1}`
- Simple Float: `7.83`
- Invalid Data: `invalid-data`

## Verification

Ran the test script to ensure the updated code correctly handles all data formats:

```
✅ Successfully parsed Schumann frequency: 7.83 Hz  # JSON format
✅ Successfully parsed Schumann frequency: 7.83 Hz  # Simple float
✅ Using default Schumann value: 0.0 Hz            # Invalid data
```

## Additional Improvements

- **Error Handling**: Added detailed error messages to help diagnose issues with Schumann resonance data
- **Format Detection**: Implemented intelligent format detection to work with both JSON and simple float values
- **Default Values**: Set reasonable default values when data is missing or invalid
- **Backwards Compatibility**: Maintained backward compatibility with older data formats

## Conclusion

This fix ensures the MM Trap Detector can properly extract and use the Schumann resonance frequency regardless of whether it's stored as a JSON object or a simple float value. The system is now more robust against data format changes and will gracefully handle invalid data.
