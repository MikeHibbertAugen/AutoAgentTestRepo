"""
Unit tests for the Location class.

This module contains comprehensive unit tests for the Location model,
ensuring all functionality works correctly including location creation,
exit management, and querying operations.
"""

import pytest
from src.location import Location


@pytest.fixture
def simple_location():
    """Fixture providing a basic location with name and description."""
    return Location("Test Room", "A simple test room.")


@pytest.fixture
def detailed_location():
    """Fixture providing a location with name and description."""
    return Location(
        "Detailed Room",
        "A richly detailed room with ornate decorations."
    )


@pytest.fixture
def location_with_exits():
    """Fixture providing a location with multiple exits."""
    location = Location("Room with Exits", "A room with several exits.")
    exits = {
        "north": "North Room",
        "south": "South Room",
        "east": "East Room"
    }
    return Location("Room with Exits", "A room with several exits.", exits)


@pytest.fixture
def location_without_exits():
    """Fixture providing a location with no exits."""
    return Location("Isolated Room", "A room with no exits.")


class TestLocationCreation:
    """Test suite for Location initialization."""
    
    def test_create_location_with_name_and_description(self):
        """Test creating a location with name and description."""
        location = Location("Test Room", "A simple test room for unit testing.")
        assert location.name == "Test Room"
        assert location.description == "A simple test room for unit testing."
    
    def test_create_location_with_exits(self):
        """Test creating a location with exits dictionary."""
        exits = {"north": "North Room", "south": "South Room"}
        location = Location("Test Room", "A test room.", exits)
        assert location.name == "Test Room"
        assert location.description == "A test room."
        assert location.get_exits() == ["north", "south"]
    
    def test_create_location_without_exits(self):
        """Test creating a location without exits (defaults to empty dict)."""
        location = Location("Test Room", "A test room.")
        assert location.get_exits() == []
    
    def test_location_name_property(self, simple_location):
        """Test that location name is accessible via property."""
        assert simple_location.name == "Test Room"
    
    def test_location_description_property(self, detailed_location):
        """Test that location description is accessible via property."""
        assert detailed_location.description == "A richly detailed room with ornate decorations."


class TestGetExits:
    """Test suite for getting available exits."""
    
    def test_get_exits_returns_list_of_directions(self, location_with_exits):
        """Test that get_exits returns list of available direction strings."""
        exits = location_with_exits.get_exits()
        assert isinstance(exits, list)
        assert len(exits) == 3
        assert "north" in exits
        assert "south" in exits
        assert "east" in exits
    
    def test_get_exits_empty_list_when_no_exits(self, location_without_exits):
        """Test that get_exits returns empty list when no exits exist."""
        exits = location_without_exits.get_exits()
        assert exits == []
        assert isinstance(exits, list)
    
    def test_get_exits_single_exit(self):
        """Test get_exits with a single exit."""
        location = Location("Room", "A room.", {"north": "North Room"})
        exits = location.get_exits()
        assert exits == ["north"]


class TestHasExits:
    """Test suite for checking if location has exits."""
    
    def test_has_exits_true_when_exits_exist(self, location_with_exits):
        """Test has_exits returns True when location has exits."""
        assert location_with_exits.has_exits() is True
    
    def test_has_exits_false_when_no_exits(self, location_without_exits):
        """Test has_exits returns False when location has no exits."""
        assert location_without_exits.has_exits() is False
    
    def test_has_exits_true_with_single_exit(self):
        """Test has_exits returns True with just one exit."""
        location = Location("Room", "A room.", {"north": "North Room"})
        assert location.has_exits() is True


class TestGetExitDestination:
    """Test suite for getting exit destination by direction."""
    
    def test_get_exit_destination_returns_correct_destination(self, location_with_exits):
        """Test that get_exit_destination returns the correct destination name."""
        assert location_with_exits.get_exit_destination("north") == "North Room"
        assert location_with_exits.get_exit_destination("south") == "South Room"
        assert location_with_exits.get_exit_destination("east") == "East Room"
    
    def test_get_exit_destination_returns_none_for_invalid_direction(self, location_with_exits):
        """Test that get_exit_destination returns None for non-existent direction."""
        assert location_with_exits.get_exit_destination("west") is None
        assert location_with_exits.get_exit_destination("invalid") is None
    
    def test_get_exit_destination_returns_none_when_no_exits(self, location_without_exits):
        """Test that get_exit_destination returns None when location has no exits."""
        assert location_without_exits.get_exit_destination("north") is None


class TestLocationWithVariousExitConfigurations:
    """Test suite for various exit configurations."""
    
    def test_location_with_all_cardinal_directions(self):
        """Test location with north, south, east, west exits."""
        exits = {
            "north": "North Room",
            "south": "South Room",
            "east": "East Room",
            "west": "West Room"
        }
        location = Location("Central Room", "A room in the center.", exits)
        assert len(location.get_exits()) == 4
        assert location.has_exits() is True
        assert location.get_exit_destination("north") == "North Room"
        assert location.get_exit_destination("west") == "West Room"
    
    def test_location_with_unconventional_directions(self):
        """Test location with unconventional direction names."""
        exits = {
            "up": "Upper Room",
            "down": "Lower Room",
            "northwest": "Northwest Room"
        }
        location = Location("Multi-level Room", "A room with various exits.", exits)
        assert "up" in location.get_exits()
        assert "down" in location.get_exits()
        assert "northwest" in location.get_exits()
        assert location.get_exit_destination("up") == "Upper Room"
    
    def test_exits_are_case_sensitive(self):
        """Test that exit directions are case-sensitive."""
        exits = {"north": "North Room"}
        location = Location("Room", "A room.", exits)
        assert location.get_exit_destination("north") == "North Room"
        assert location.get_exit_destination("North") is None
        assert location.get_exit_destination("NORTH") is None


class TestEdgeCases:
    """Test suite for edge cases and special scenarios."""
    
    def test_empty_exits_dictionary(self):
        """Test location with explicitly empty exits dictionary."""
        location = Location("Room", "A room.", {})
        assert location.has_exits() is False
        assert location.get_exits() == []
    
    def test_location_with_empty_strings(self):
        """Test location can handle empty description."""
        location = Location("Room", "")
        assert location.name == "Room"
        assert location.description == ""
    
    def test_exits_with_same_destination(self):
        """Test that multiple exits can lead to the same destination."""
        exits = {
            "north": "Same Room",
            "east": "Same Room"
        }
        location = Location("Room", "A room.", exits)
        assert location.get_exit_destination("north") == "Same Room"
        assert location.get_exit_destination("east") == "Same Room"