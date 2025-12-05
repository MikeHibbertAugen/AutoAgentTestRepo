"""
Module for fetching current date and time in Nelson, New Zealand.

This module integrates with the WorldTimeAPI service to retrieve accurate
timezone information for Nelson, which uses the Pacific/Auckland timezone.
"""

import requests
from datetime import datetime
from typing import Dict, Any


# API Configuration
API_BASE_URL = "https://worldtimeapi.org/api/timezone/Pacific/Auckland"
REQUEST_TIMEOUT = 5  # seconds


class NelsonTimeError(Exception):
    """Base exception for Nelson time service errors."""
    pass


class NelsonTimeService:
    """Service class for fetching time data for Nelson, New Zealand."""
    
    def __init__(self, api_url: str = API_BASE_URL, timeout: int = REQUEST_TIMEOUT):
        """
        Initialize the NelsonTimeService.
        
        Args:
            api_url: The WorldTimeAPI endpoint URL (default: Pacific/Auckland)
            timeout: Request timeout in seconds (default: 5)
        """
        self.api_url = api_url
        self.timeout = timeout
    
    def fetch_time_data(self) -> Dict[str, Any]:
        """
        Fetch raw time data from WorldTimeAPI.
        
        Returns:
            Dictionary containing the API response data
            
        Raises:
            NelsonTimeError: If the API request fails for any reason
        """
        try:
            response = requests.get(self.api_url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise NelsonTimeError(
                f"Request timed out after {self.timeout} seconds"
            )
        except requests.exceptions.ConnectionError:
            raise NelsonTimeError(
                "Failed to connect to WorldTimeAPI. Please check your internet connection."
            )
        except requests.exceptions.HTTPError as e:
            raise NelsonTimeError(
                f"HTTP error occurred: {e.response.status_code} - {e.response.reason}"
            )
        except requests.exceptions.JSONDecodeError:
            raise NelsonTimeError(
                "Failed to parse API response. Invalid JSON received."
            )
        except requests.exceptions.RequestException as e:
            raise NelsonTimeError(
                f"An error occurred while fetching time data: {str(e)}"
            )
    
    def get_formatted_time(self) -> str:
        """
        Get the current date and time in Nelson formatted as a string.
        
        Returns:
            Formatted datetime string in ISO format
            
        Raises:
            NelsonTimeError: If unable to fetch or parse time data
        """
        data = self.fetch_time_data()
        
        try:
            datetime_str = data.get("datetime")
            if not datetime_str:
                raise NelsonTimeError("No datetime field in API response")
            
            # Parse ISO 8601 datetime string
            dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S %Z")
        except (ValueError, KeyError) as e:
            raise NelsonTimeError(
                f"Failed to parse datetime from API response: {str(e)}"
            )


def get_current_time() -> str:
    """
    Get the current date and time in Nelson, New Zealand.
    
    This function fetches the current time from WorldTimeAPI using the
    Pacific/Auckland timezone, which is used by Nelson.
    
    Returns:
        A formatted string containing the current date and time in Nelson
        
    Raises:
        NelsonTimeError: If unable to fetch the current time
        
    Example:
        >>> time_str = get_current_time()
        >>> print(f"Current time in Nelson: {time_str}")
        Current time in Nelson: 2024-01-15 14:30:45
    """
    service = NelsonTimeService()
    return service.get_formatted_time()