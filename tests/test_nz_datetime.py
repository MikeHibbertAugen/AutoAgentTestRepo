import pytest
from unittest.mock import patch, Mock
from requests.exceptions import RequestException, Timeout, ConnectionError
import json

from src.nz_datetime import get_nz_datetime, format_nz_datetime


@pytest.fixture
def mock_api_response():
    """Fixture providing a valid API response"""
    return {
        "abbreviation": "NZDT",
        "client_ip": "203.0.113.1",
        "datetime": "2024-01-15T14:30:45.123456+13:00",
        "day_of_week": 1,
        "day_of_year": 15,
        "dst": True,
        "dst_from": "2023-09-24T14:00:00+00:00",
        "dst_offset": 3600,
        "dst_until": "2024-04-07T14:00:00+00:00",
        "raw_offset": 43200,
        "timezone": "Pacific/Auckland",
        "unixtime": 1705285845,
        "utc_datetime": "2024-01-15T01:30:45.123456+00:00",
        "utc_offset": "+13:00",
        "week_number": 3
    }


@pytest.fixture
def mock_formatted_response():
    """Fixture providing expected formatted response"""
    return {
        "timezone": "Pacific/Auckland",
        "datetime": "2024-01-15T14:30:45.123456+13:00",
        "utc_offset": "+13:00",
        "utc_datetime": "2024-01-15T01:30:45.123456+00:00",
        "abbreviation": "NZDT",
        "unixtime": 1705285845,
        "day_of_week": 1,
        "week_number": 3
    }


class TestGetNzDatetime:
    """Tests for the get_nz_datetime function"""

    @patch('src.nz_datetime.requests.get')
    def test_successful_api_call(self, mock_get, mock_api_response, mock_formatted_response):
        """Test successful API call and proper data formatting"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_api_response
        mock_get.return_value = mock_response

        result = get_nz_datetime()

        assert result is not None
        assert result["timezone"] == "Pacific/Auckland"
        assert result["datetime"] == "2024-01-15T14:30:45.123456+13:00"
        assert result["utc_offset"] == "+13:00"
        assert "error" not in result
        mock_get.assert_called_once_with(
            "http://worldtimeapi.org/api/timezone/Pacific/Auckland",
            timeout=10
        )

    @patch('src.nz_datetime.requests.get')
    def test_network_connection_error(self, mock_get):
        """Test handling of network connection errors"""
        mock_get.side_effect = ConnectionError("Failed to establish connection")

        result = get_nz_datetime()

        assert result is not None
        assert "error" in result
        assert "Connection error" in result["error"]

    @patch('src.nz_datetime.requests.get')
    def test_timeout_error(self, mock_get):
        """Test handling of timeout errors"""
        mock_get.side_effect = Timeout("Request timed out")

        result = get_nz_datetime()

        assert result is not None
        assert "error" in result
        assert "Request timed out" in result["error"]

    @patch('src.nz_datetime.requests.get')
    def test_general_request_exception(self, mock_get):
        """Test handling of general request exceptions"""
        mock_get.side_effect = RequestException("General request error")

        result = get_nz_datetime()

        assert result is not None
        assert "error" in result
        assert "Request failed" in result["error"]

    @patch('src.nz_datetime.requests.get')
    def test_invalid_json_response(self, mock_get):
        """Test handling of invalid JSON response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_get.return_value = mock_response

        result = get_nz_datetime()

        assert result is not None
        assert "error" in result
        assert "Invalid JSON" in result["error"]

    @patch('src.nz_datetime.requests.get')
    def test_404_error_response(self, mock_get):
        """Test handling of 404 HTTP error"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = RequestException("404 Not Found")
        mock_get.return_value = mock_response

        result = get_nz_datetime()

        assert result is not None
        assert "error" in result

    @patch('src.nz_datetime.requests.get')
    def test_500_error_response(self, mock_get):
        """Test handling of 500 HTTP error"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = RequestException("500 Internal Server Error")
        mock_get.return_value = mock_response

        result = get_nz_datetime()

        assert result is not None
        assert "error" in result

    @patch('src.nz_datetime.requests.get')
    def test_unexpected_exception(self, mock_get):
        """Test handling of unexpected exceptions"""
        mock_get.side_effect = Exception("Unexpected error")

        result = get_nz_datetime()

        assert result is not None
        assert "error" in result
        assert "Unexpected error" in result["error"]


class TestFormatNzDatetime:
    """Tests for the format_nz_datetime helper function"""

    def test_format_with_complete_data(self, mock_api_response):
        """Test formatting with complete API response data"""
        result = format_nz_datetime(mock_api_response)

        assert result["timezone"] == "Pacific/Auckland"
        assert result["datetime"] == "2024-01-15T14:30:45.123456+13:00"
        assert result["utc_offset"] == "+13:00"
        assert result["utc_datetime"] == "2024-01-15T01:30:45.123456+00:00"
        assert result["abbreviation"] == "NZDT"
        assert result["unixtime"] == 1705285845
        assert result["day_of_week"] == 1
        assert result["week_number"] == 3

    def test_format_with_missing_optional_fields(self):
        """Test formatting with minimal required fields"""
        minimal_data = {
            "timezone": "Pacific/Auckland",
            "datetime": "2024-01-15T14:30:45.123456+13:00",
            "utc_offset": "+13:00"
        }

        result = format_nz_datetime(minimal_data)

        assert result["timezone"] == "Pacific/Auckland"
        assert result["datetime"] == "2024-01-15T14:30:45.123456+13:00"
        assert result["utc_offset"] == "+13:00"
        assert result.get("utc_datetime") is None
        assert result.get("abbreviation") is None

    def test_format_with_partial_data(self):
        """Test formatting with some fields present"""
        partial_data = {
            "timezone": "Pacific/Auckland",
            "datetime": "2024-01-15T14:30:45.123456+13:00",
            "utc_offset": "+13:00",
            "abbreviation": "NZDT",
            "unixtime": 1705285845
        }

        result = format_nz_datetime(partial_data)

        assert result["timezone"] == "Pacific/Auckland"
        assert result["datetime"] == "2024-01-15T14:30:45.123456+13:00"
        assert result["utc_offset"] == "+13:00"
        assert result["abbreviation"] == "NZDT"
        assert result["unixtime"] == 1705285845
        assert result.get("day_of_week") is None
        assert result.get("week_number") is None

    def test_format_preserves_data_types(self, mock_api_response):
        """Test that formatting preserves correct data types"""
        result = format_nz_datetime(mock_api_response)

        assert isinstance(result["timezone"], str)
        assert isinstance(result["datetime"], str)
        assert isinstance(result["utc_offset"], str)
        assert isinstance(result["unixtime"], int)
        assert isinstance(result["day_of_week"], int)
        assert isinstance(result["week_number"], int)