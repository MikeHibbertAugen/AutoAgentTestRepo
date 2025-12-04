"""
Module for retrieving current date and time in New Zealand timezone.

This module uses the free WorldTimeAPI to fetch the current datetime
for the Pacific/Auckland timezone (New Zealand).
"""

import requests
from typing import Dict, Optional, Any


API_URL = "http://worldtimeapi.org/api/timezone/Pacific/Auckland"
REQUEST_TIMEOUT = 10


def get_nz_datetime() -> Dict[str, Any]:
    """
    Retrieve the current date and time for New Zealand (Pacific/Auckland timezone).
    
    Makes an HTTP GET request to the WorldTimeAPI and returns formatted
    datetime information for New Zealand.
    
    Returns:
        dict: A dictionary containing:
            - success (bool): Whether the request was successful
            - datetime (str): ISO 8601 formatted datetime string (if successful)
            - timezone (str): Timezone name (if successful)
            - utc_offset (str): UTC offset (if successful)
            - date (str): Date in YYYY-MM-DD format (if successful)
            - time (str): Time in HH:MM:SS format (if successful)
            - error (str): Error message (if not successful)
    
    Example:
        >>> result = get_nz_datetime()
        >>> if result['success']:
        ...     print(f"NZ Time: {result['datetime']}")
        ... else:
        ...     print(f"Error: {result['error']}")
    """
    try:
        response = requests.get(API_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        return format_nz_datetime(data)
        
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Request timed out while fetching NZ datetime'
        }
    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'error': 'Failed to connect to WorldTimeAPI'
        }
    except requests.exceptions.HTTPError as e:
        return {
            'success': False,
            'error': f'HTTP error occurred: {e.response.status_code}'
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'Request failed: {str(e)}'
        }
    except (ValueError, KeyError) as e:
        return {
            'success': False,
            'error': f'Failed to parse API response: {str(e)}'
        }


def format_nz_datetime(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format raw API response data into a structured dictionary.
    
    Args:
        raw_data (dict): Raw JSON response from WorldTimeAPI
    
    Returns:
        dict: Formatted dictionary containing:
            - success (bool): Always True for successful formatting
            - datetime (str): ISO 8601 formatted datetime string
            - timezone (str): Timezone name
            - utc_offset (str): UTC offset
            - date (str): Date in YYYY-MM-DD format
            - time (str): Time in HH:MM:SS format
    
    Raises:
        KeyError: If required fields are missing from raw_data
        ValueError: If datetime format is invalid
    """
    datetime_str = raw_data['datetime']
    
    # Split datetime into date and time components
    # Expected format: 2024-01-15T14:30:45.123456+13:00
    if 'T' in datetime_str:
        date_part = datetime_str.split('T')[0]
        time_with_offset = datetime_str.split('T')[1]
        # Remove timezone offset and microseconds for cleaner time display
        time_part = time_with_offset.split('+')[0].split('-')[0].split('.')[0]
    else:
        raise ValueError("Invalid datetime format in API response")
    
    return {
        'success': True,
        'datetime': datetime_str,
        'timezone': raw_data['timezone'],
        'utc_offset': raw_data['utc_offset'],
        'date': date_part,
        'time': time_part
    }