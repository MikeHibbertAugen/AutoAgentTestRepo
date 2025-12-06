"""
Unit tests for the LocationDisplay class.

Tests the formatting of location information including names, descriptions,
and exits for display in the text-based adventure game.
"""

import pytest
from src.location import Location
from src.location_display import LocationDisplay


class TestLocationDisplay:
    """Test suite for LocationDisplay class."""

    @pytest.fixture
    def display(self):
        """Create a LocationDisplay instance for testing."""
        return LocationDisplay()

    @pytest.fixture
    def location_with_exits(self):
        """Create a location with multiple exits."""
        return Location(
            name="Town Square",
            description="A bustling town square with a fountain in the center.",
            exits={"north": "Castle Gate", "south": "Market", "east": "Temple"}
        )

    @pytest.fixture
    def location_without_exits(self):
        """Create a location with no exits."""
        return Location(
            name="Dead End",
            description="A narrow corridor that ends abruptly.",
            exits={}
        )

    @pytest.fixture
    def location_with_one_exit(self):
        """Create a location with a single exit."""
        return Location(
            name="Hallway",
            description="A long hallway.",
            exits={"west": "Main Room"}
        )

    def test_format_name(self, display, location_with_exits):
        """Test formatting of location name."""
        result = display.format_name(location_with_exits)
        assert result == "Town Square"

    def test_format_description(self, display, location_with_exits):
        """Test formatting of location description."""
        result = display.format_description(location_with_exits)
        assert result == "A bustling town square with a fountain in the center."

    def test_format_exits_with_multiple_exits(self, display, location_with_exits):
        """Test formatting exits list with multiple exits."""
        result = display.format_exits(location_with_exits)
        # Should contain all directions
        assert "north" in result
        assert "south" in result
        assert "east" in result

    def test_format_exits_with_no_exits(self, display, location_without_exits):
        """Test formatting exits when location has no exits."""
        result = display.format_exits(location_without_exits)
        assert result == "There are no obvious exits."

    def test_format_exits_with_one_exit(self, display, location_with_one_exit):
        """Test formatting exits list with a single exit."""
        result = display.format_exits(location_with_one_exit)
        assert "west" in result

    def test_format_location_info_complete(self, display, location_with_exits):
        """Test complete location info formatting with all components."""
        result = display.format_location_info(location_with_exits)
        
        # Should contain name
        assert "Town Square" in result
        
        # Should contain description
        assert "A bustling town square with a fountain in the center." in result
        
        # Should contain exits
        assert "north" in result
        assert "south" in result
        assert "east" in result

    def test_format_location_info_no_exits(self, display, location_without_exits):
        """Test complete location info formatting for location with no exits."""
        result = display.format_location_info(location_without_exits)
        
        # Should contain name
        assert "Dead End" in result
        
        # Should contain description
        assert "A narrow corridor that ends abruptly." in result
        
        # Should contain no exits message
        assert "no obvious exits" in result.lower()

    def test_format_location_info_structure(self, display, location_with_exits):
        """Test that location info has proper structure with all sections."""
        result = display.format_location_info(location_with_exits)
        
        # Result should be a non-empty string
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Should contain all three main components
        lines = result.split('\n')
        assert len(lines) >= 3  # At minimum: name, description, exits

    def test_format_exits_returns_string(self, display, location_with_exits):
        """Test that format_exits returns a string."""
        result = display.format_exits(location_with_exits)
        assert isinstance(result, str)

    def test_format_name_returns_string(self, display, location_with_exits):
        """Test that format_name returns a string."""
        result = display.format_name(location_with_exits)
        assert isinstance(result, str)

    def test_format_description_returns_string(self, display, location_with_exits):
        """Test that format_description returns a string."""
        result = display.format_description(location_with_exits)
        assert isinstance(result, str)

    def test_format_location_info_returns_string(self, display, location_with_exits):
        """Test that format_location_info returns a string."""
        result = display.format_location_info(location_with_exits)
        assert isinstance(result, str)