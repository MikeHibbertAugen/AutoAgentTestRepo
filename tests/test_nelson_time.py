"""
Unit tests for nelson_time module.

Tests the NelsonTimeService class and get_current_time function
with mocked API responses to avoid external dependencies.
"""

import json
from unittest.mock import Mock, patch

import pytest
import requests

from src.nelson_time import (
    API_TIMEOUT,
    API_URL,
    NelsonTimeService,
    get_current_time,
)


@pytest.fixture
def mock_api_response():
    """Fixture providing a valid WorldTimeAPI response."""
    return {
        "abbreviation": "NZDT",
        "client_ip": "123.45.67.89",
        "datetime": "2024-01-15T14:30:45.123456+13:00",
        "day_of_week": 1,
        "day_of_year": 15,
        "dst": True,
        "dst_from": "2023-09-24T14:00:00+00:00",
        "dst_offset": 3600,
        "dst_until": "2024-04-07T14:00:00+00:00",
        "raw_offset": 43200,
        "timezone": "Pacific/Auckland",
        "unixtime": 1705281045,
        "utc_datetime": "2024-01-15T01:30:45.123456+00:00",
        "utc_offset": "+13:00",
        "week_number": 3
    }


@pytest.fixture
def service():
    """Fixture providing a NelsonTimeService instance."""
    return NelsonTimeService()


class TestNelsonTimeService:
    """Test suite for NelsonTimeService class."""

    def test_successful_api_call(self, service, mock_api_response):
        """Test successful API call returns formatted datetime."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_api_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            result = service.fetch_nelson_time()

            assert isinstance(result, dict)
            assert "datetime" in result
            assert "timezone" in result
            assert result["timezone"] == "Pacific/Auckland"
            assert result["datetime"] == "2024-01-15T14:30:45.123456+13:00"
            mock_get.assert_called_once_with(API_URL, timeout=API_TIMEOUT)

    def test_network_error_handling(self, service):
        """Test handling of network connection errors."""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

            with pytest.raises(RuntimeError) as exc_info:
                service.fetch_nelson_time()

            assert "Failed to connect to WorldTimeAPI" in str(exc_info.value)

    def test_timeout_handling(self, service):
        """Test handling of request timeout."""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

            with pytest.raises(RuntimeError) as exc_info:
                service.fetch_nelson_time()

            assert "Request to WorldTimeAPI timed out" in str(exc_info.value)

    def test_http_error_404(self, service):
        """Test handling of HTTP 404 error."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
                "404 Client Error: Not Found"
            )
            mock_get.return_value = mock_response

            with pytest.raises(RuntimeError) as exc_info:
                service.fetch_nelson_time()

            assert "HTTP error occurred" in str(exc_info.value)

    def test_http_error_500(self, service):
        """Test handling of HTTP 500 error."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
                "500 Server Error: Internal Server Error"
            )
            mock_get.return_value = mock_response

            with pytest.raises(RuntimeError) as exc_info:
                service.fetch_nelson_time()

            assert "HTTP error occurred" in str(exc_info.value)

    def test_invalid_json_response(self, service):
        """Test handling of invalid JSON in response."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.side_effect = json.JSONDecodeError(
                "Invalid JSON", "", 0
            )
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            with pytest.raises(RuntimeError) as exc_info:
                service.fetch_nelson_time()

            assert "Failed to parse API response" in str(exc_info.value)

    def test_missing_datetime_field(self, service):
        """Test handling of response missing datetime field."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {"timezone": "Pacific/Auckland"}
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            with pytest.raises(RuntimeError) as exc_info:
                service.fetch_nelson_time()

            assert "Invalid API response format" in str(exc_info.value)

    def test_missing_timezone_field(self, service):
        """Test handling of response missing timezone field."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "datetime": "2024-01-15T14:30:45.123456+13:00"
            }
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            with pytest.raises(RuntimeError) as exc_info:
                service.fetch_nelson_time()

            assert "Invalid API response format" in str(exc_info.value)

    def test_request_exception_handling(self, service):
        """Test handling of generic request exceptions."""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException(
                "Generic error"
            )

            with pytest.raises(RuntimeError) as exc_info:
                service.fetch_nelson_time()

            assert "An error occurred while fetching time data" in str(exc_info.value)


class TestGetCurrentTime:
    """Test suite for get_current_time convenience function."""

    def test_get_current_time_success(self, mock_api_response):
        """Test get_current_time returns formatted string."""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_api_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            result = get_current_time()

            assert isinstance(result, str)
            assert "2024-01-15" in result
            assert "14:30:45" in result
            assert "Pacific/Auckland" in result

    def test_get_current_time_propagates_errors(self):
        """Test get_current_time propagates errors from service."""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

            with pytest.raises(RuntimeError) as exc_info:
                get_current_time()

            assert "Failed to connect to WorldTimeAPI" in str(exc_info.value)


class TestConstants:
    """Test suite for module constants."""

    def test_api_url_constant(self):
        """Test API_URL constant is correctly defined."""
        assert API_URL == "https://worldtimeapi.org/api/timezone/Pacific/Auckland"
        assert isinstance(API_URL, str)

    def test_api_timeout_constant(self):
        """Test API_TIMEOUT constant is correctly defined."""
        assert API_TIMEOUT == 5
        assert isinstance(API_TIMEOUT, int)