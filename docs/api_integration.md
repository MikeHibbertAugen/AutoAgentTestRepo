# WorldTimeAPI Integration Documentation

## Overview

This document describes the integration with WorldTimeAPI, a free public API service that provides current time information for timezones worldwide. We use this service to retrieve the current date and time for Nelson, New Zealand.

## API Service Details

- **Service Name:** WorldTimeAPI
- **Base URL:** `https://worldtimeapi.org`
- **Documentation:** http://worldtimeapi.org/
- **Authentication:** None required (public API)
- **Rate Limits:** No strict rate limits for reasonable use
- **Cost:** Free

## Endpoint Used

### Get Timezone Information

**Endpoint:** `/api/timezone/Pacific/Auckland`

**Full URL:** `https://worldtimeapi.org/api/timezone/Pacific/Auckland`

**Method:** `GET`

**Why Pacific/Auckland:** Nelson, New Zealand uses the Pacific/Auckland timezone (NZST/NZDT). WorldTimeAPI does not have a specific Nelson timezone, so we use Auckland which shares the same timezone.

## Request Details

### Example Request

```http
GET /api/timezone/Pacific/Auckland HTTP/1.1
Host: worldtimeapi.org
Accept: application/json
```

### Request Parameters

No query parameters or request body required.

### Request Headers

- `Accept: application/json` (optional, JSON is default)

## Response Format

### Successful Response (200 OK)

```json
{
  "abbreviation": "NZDT",
  "client_ip": "203.0.113.42",
  "datetime": "2024-01-15T14:30:45.123456+13:00",
  "day_of_week": 1,
  "day_of_year": 15,
  "dst": true,
  "dst_from": "2023-09-24T02:00:00+00:00",
  "dst_offset": 3600,
  "dst_until": "2024-04-07T02:00:00+00:00",
  "raw_offset": 43200,
  "timezone": "Pacific/Auckland",
  "unixtime": 1705286445,
  "utc_datetime": "2024-01-15T01:30:45.123456+00:00",
  "utc_offset": "+13:00",
  "week_number": 3
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `abbreviation` | string | Timezone abbreviation (NZST or NZDT) |
| `datetime` | string | Current datetime in ISO 8601 format with timezone offset |
| `day_of_week` | integer | Day of week (0=Sunday, 6=Saturday) |
| `day_of_year` | integer | Day number in the year (1-366) |
| `dst` | boolean | Whether daylight saving time is currently active |
| `dst_from` | string | When DST starts (if applicable) |
| `dst_offset` | integer | DST offset in seconds |
| `dst_until` | string | When DST ends (if applicable) |
| `raw_offset` | integer | Base timezone offset from UTC in seconds |
| `timezone` | string | IANA timezone identifier |
| `unixtime` | integer | Unix timestamp (seconds since epoch) |
| `utc_datetime` | string | Current UTC datetime |
| `utc_offset` | string | Current offset from UTC (including DST) |
| `week_number` | integer | ISO week number |

### Relevant Fields for Our Use Case

Our implementation primarily uses:
- `datetime` - The current local date and time with timezone information
- `timezone` - To verify we're getting the correct timezone
- `abbreviation` - For display purposes (NZST or NZDT)

## Error Responses

### HTTP Error Codes

| Status Code | Description | Cause |
|-------------|-------------|-------|
| 404 | Not Found | Invalid timezone name |
| 500 | Internal Server Error | Server-side issue |
| 503 | Service Unavailable | Service temporarily down |

### Example Error Response

```json
{
  "error": "unknown location"
}
```

## Error Handling Strategy

Our implementation handles the following error scenarios:

### 1. Network Errors
- **Cause:** No internet connection, DNS failure, network timeout
- **Handling:** Catch `requests.RequestException` and return user-friendly error message
- **User Message:** "Failed to connect to time service"

### 2. Timeout Errors
- **Cause:** API takes too long to respond (>5 seconds)
- **Handling:** Set timeout parameter in request, catch `requests.Timeout`
- **User Message:** "Time service request timed out"
- **Timeout Value:** 5 seconds (configurable via constant)

### 3. HTTP Errors
- **Cause:** API returns 4xx or 5xx status codes
- **Handling:** Check response status code, raise exception with status
- **User Message:** "Time service returned error: {status_code}"

### 4. Invalid JSON
- **Cause:** API returns malformed JSON or unexpected format
- **Handling:** Catch `json.JSONDecodeError` and validate required fields
- **User Message:** "Invalid response from time service"

### 5. Missing Required Fields
- **Cause:** API response structure changes or incomplete data
- **Handling:** Validate presence of required fields (datetime, timezone)
- **User Message:** "Incomplete response from time service"

## Implementation Notes

### Timezone Selection

Nelson, New Zealand is located in the Tasman District on the South Island. It observes:
- **NZST (New Zealand Standard Time):** UTC+12:00 (Winter)
- **NZDT (New Zealand Daylight Time):** UTC+13:00 (Summer)

These are identical to Auckland's timezone, making Pacific/Auckland the appropriate choice.

### Datetime Parsing

The API returns datetime in ISO 8601 format with timezone offset:
```
2024-01-15T14:30:45.123456+13:00
```

Our implementation parses this string and formats it for human readability.

### Caching Considerations

The current implementation does not cache API responses because:
- Time data becomes stale within seconds
- The API is fast and reliable
- No rate limiting concerns for reasonable use

If caching is needed in the future, implement with a very short TTL (e.g., 1-5 seconds).

## Testing Strategy

### Unit Tests
- Mock all API calls using `unittest.mock`
- Test with sample response data from above
- Simulate all error conditions
- Verify error messages are user-friendly

### Integration Tests (Optional)
- Can be run manually against real API
- Not included in automated test suite to avoid external dependencies
- Useful for verifying API contract hasn't changed

## Alternative APIs

If WorldTimeAPI becomes unavailable, consider these alternatives:
1. **timeapi.io** - Similar free timezone API
2. **Google Time Zone API** - Requires API key
3. **ipgeolocation.io** - Includes timezone data, requires API key

## References

- WorldTimeAPI Documentation: http://worldtimeapi.org/
- IANA Time Zone Database: https://www.iana.org/time-zones
- ISO 8601 DateTime Format: https://en.wikipedia.org/wiki/ISO_8601