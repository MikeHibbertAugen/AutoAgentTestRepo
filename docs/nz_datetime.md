# New Zealand DateTime Module Documentation

## Overview

The `nz_datetime` module provides a simple interface to retrieve the current date and time in New Zealand's timezone (Pacific/Auckland) using the free WorldTimeAPI service. This module handles all API communication, error handling, and data formatting automatically.

## Features

- Retrieves accurate New Zealand datetime from WorldTimeAPI
- Handles network failures and timeouts gracefully
- Returns structured, easy-to-use datetime information
- No authentication or API keys required
- Comprehensive error handling

## Installation

Ensure the required dependencies are installed:

```bash
pip install requests
```

## Usage

### Basic Example

```python
from src.nz_datetime import get_nz_datetime

# Get current NZ datetime
result = get_nz_datetime()

if result['success']:
    print(f"Current NZ Time: {result['datetime']}")
    print(f"Timezone: {result['timezone']}")
    print(f"UTC Offset: {result['utc_offset']}")
else:
    print(f"Error: {result['error']}")
```

### Example Output

```python
{
    'success': True,
    'datetime': '2024-01-15T14:30:45.123456+13:00',
    'timezone': 'Pacific/Auckland',
    'utc_offset': '+13:00',
    'day_of_week': 1,
    'day_of_year': 15,
    'week_number': 3
}
```

## API Reference

### `get_nz_datetime(timeout: int = 10) -> dict`

Retrieves the current date and time for New Zealand timezone from WorldTimeAPI.

**Parameters:**
- `timeout` (int, optional): Request timeout in seconds. Default is 10.

**Returns:**
- `dict`: A dictionary containing the datetime information or error details.

**Success Response:**
```python
{
    'success': True,
    'datetime': str,        # ISO 8601 formatted datetime string
    'timezone': str,        # Timezone name (Pacific/Auckland)
    'utc_offset': str,      # UTC offset (e.g., '+13:00')
    'day_of_week': int,     # Day of week (0=Sunday, 6=Saturday)
    'day_of_year': int,     # Day number in the year
    'week_number': int      # ISO week number
}
```

**Error Response:**
```python
{
    'success': False,
    'error': str,           # Error message describing what went wrong
    'error_type': str       # Type of error (network, timeout, invalid_response, http_error)
}
```

### `format_nz_datetime(raw_data: dict) -> dict`

Helper function to format raw API response data into a clean, structured dictionary.

**Parameters:**
- `raw_data` (dict): Raw JSON response from WorldTimeAPI

**Returns:**
- `dict`: Formatted datetime information

**Raises:**
- `KeyError`: If required fields are missing from the raw data
- `ValueError`: If data format is invalid

## Error Handling

The module handles various error scenarios:

### Network Errors
Occurs when the API cannot be reached due to connectivity issues.

```python
{
    'success': False,
    'error': 'Network error: Connection refused',
    'error_type': 'network'
}
```

### Timeout Errors
Occurs when the API doesn't respond within the specified timeout period.

```python
{
    'success': False,
    'error': 'Request timeout: API did not respond in time',
    'error_type': 'timeout'
}
```

### Invalid Response
Occurs when the API returns malformed or unexpected data.

```python
{
    'success': False,
    'error': 'Invalid API response: missing required field',
    'error_type': 'invalid_response'
}
```

### HTTP Errors
Occurs when the API returns an error status code (4xx, 5xx).

```python
{
    'success': False,
    'error': 'HTTP error: 404 Not Found',
    'error_type': 'http_error'
}
```

## Dependencies

- **requests** (>=2.31.0): HTTP library for making API requests

## API Endpoint

The module uses the following free public API:
- **URL:** http://worldtimeapi.org/api/timezone/Pacific/Auckland
- **Method:** GET
- **Authentication:** None required
- **Rate Limits:** None for reasonable use

## Best Practices

1. **Error Handling:** Always check the `success` field before using the datetime data
2. **Timeout Configuration:** Adjust the timeout parameter based on your network conditions
3. **Caching:** Consider caching results for a few seconds if making frequent calls
4. **Logging:** Log errors appropriately for debugging purposes

## Examples

### With Custom Timeout

```python
from src.nz_datetime import get_nz_datetime

# Use a shorter timeout for faster failure detection
result = get_nz_datetime(timeout=5)
```

### Error Handling Pattern

```python
from src.nz_datetime import get_nz_datetime
import logging

result = get_nz_datetime()

if not result['success']:
    logging.error(f"Failed to get NZ datetime: {result['error']}")
    # Fallback logic here
    return None

return result['datetime']
```

## Troubleshooting

**Problem:** Module returns timeout errors frequently
- **Solution:** Increase the timeout parameter or check network connectivity

**Problem:** Module returns invalid response errors
- **Solution:** Verify the WorldTimeAPI service is operational at http://worldtimeapi.org

**Problem:** Import errors for requests library
- **Solution:** Install dependencies with `pip install -r requirements-dev.txt`

## Future Enhancements

Potential improvements for future versions:
- Response caching to reduce API calls
- Support for multiple timezone queries
- Offline fallback using system time
- Retry logic with exponential backoff

## License

This module follows the same license as the parent project.