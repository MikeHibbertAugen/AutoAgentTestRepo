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
    """Fixture providing a basic location with name only."""
    return Location("Test Room")


@pytest.fixture
def detailed_location():
    """Fixture providing a location with name and description."""
    return Location(
        "Detailed Room",
        "A richly detailed room with ornate decorations."
    )


@pytest.fixture
def connected_locations():
    """Fixture providing multiple connected locations."""
    entrance = Location("Entrance Hall", "A grand entrance with marble floors.")
    kitchen = Location("Kitchen", "A cozy kitchen with modern appliances.")
    garden = Location("Garden", "A beautiful garden with native plants.")
    
    entrance.add_exit("north", kitchen)
    entrance.add_exit("west", garden)
    kitchen.add_exit("south", entrance)
    
    return {
        "entrance": entrance,
        "kitchen": kitchen,
        "garden": garden
    }


class TestLocationCreation:
    """Test suite for Location initialization."""
    
    def test_create_location_with_name_only(self):
        """Test creating a location with just a name."""
        location = Location("Test Room")
        assert location.name == "Test Room"
        assert location.description == ""
    
    def test_create_location_with_name_and_description(self):
        """Test creating a location with name and description."""
        location = Location(
            "Test Room",
            "A simple test room for unit testing."
        )
        assert location.name == "Test Room"
        assert location.description == "A simple test room for unit testing."
    
    def test_location_name_property(self, simple_location):
        """Test that location name is accessible via property."""
        assert simple_location.name == "Test Room"
    
    def test_location_description_property(self, detailed_location):
        """Test that location description is accessible via property."""
        assert detailed_location.description == "A richly detailed room with ornate decorations."
    
    def test_default_empty_description(self, simple_location):
        """Test that description defaults to empty string when not provided."""
        assert simple_location.description == ""
        assert isinstance(simple_location.description, str)


class TestExitManagement:
    """Test suite for adding and managing exits."""
    
    def test_add_single_exit(self, simple_location):
        """Test adding a single exit to a location."""
        destination = Location("Destination Room")
        simple_location.add_exit("north", destination)
        
        assert simple_location.get_exit("north") == destination
    
    def test_add_multiple_exits(self, simple_location):
        """Test adding multiple exits in different directions."""
        north_room = Location("North Room")
        south_room = Location("South Room")
        east_room = Location("East Room")
        
        simple_location.add_exit("north", north_room)
        simple_location.add_exit("south", south_room)
        simple_location.add_exit("east", east_room)
        
        assert simple_location.get_exit("north") == north_room
        assert simple_location.get_exit("south") == south_room
        assert simple_location.get_exit("east") == east_room
    
    def test_overwrite_existing_exit(self, simple_location):
        """Test that adding an exit with same direction overwrites previous one."""
        first_destination = Location("First Room")
        second_destination = Location("Second Room")
        
        simple_location.add_exit("north", first_destination)
        simple_location.add_exit("north", second_destination)
        
        assert simple_location.get_exit("north") == second_destination
        assert simple_location.get_exit("north") != first_destination
    
    def test_add_exit_with_various_directions(self, simple_location):
        """Test adding exits with various direction names."""
        directions = ["north", "south", "east", "west", "up", "down", "northwest"]
        destinations = [Location(f"Room {i}") for i in range(len(directions))]
        
        for direction, destination in zip(directions, destinations):
            simple_location.add_exit(direction, destination)
        
        for direction, destination in zip(directions, destinations):
            assert simple_location.get_exit(direction) == destination


class TestExitRetrieval:
    """Test suite for retrieving exits."""
    
    def test_get_existing_exit(self, connected_locations):
        """Test retrieving an exit that exists."""
        entrance = connected_locations["entrance"]
        kitchen = connected_locations["kitchen"]
        
        assert entrance.get_exit("north") == kitchen
    
    def test_get_nonexistent_exit(self, simple_location):
        """Test retrieving an exit that doesn't exist returns None."""
        assert simple_location.get_exit("north") is None
        assert simple_location.get_exit("invalid") is None
    
    def test_get_exit_case_sensitive(self, simple_location):
        """Test that exit retrieval is case-sensitive."""
        destination = Location("Destination")
        simple_location.add_exit("north", destination)
        
        assert simple_location.get_exit("north") == destination
        assert simple_location.get_exit("North") is None
        assert simple_location.get_exit("NORTH") is None


class TestExitExistence:
    """Test suite for checking exit existence."""
    
    def test_has_exit_true(self, simple_location):
        """Test has_exit returns True for existing exit."""
        destination = Location("Destination")
        simple_location.add_exit("north", destination)
        
        assert simple_location.has_exit("north") is True
    
    def test_has_exit_false(self, simple_location):
        """Test has_exit returns False for non-existent exit."""
        assert simple_location.has_exit("north") is False
        assert simple_location.has_exit("invalid") is False
    
    def test_has_exit_multiple_exits(self, connected_locations):
        """Test has_exit with multiple exits."""
        entrance = connected_locations["entrance"]
        
        assert entrance.has_exit("north") is True
        assert entrance.has_exit("west") is True
        assert entrance.has_exit("south") is False
        assert entrance.has_exit("east") is False
    
    def test_has_exit_case_sensitive(self, simple_location):
        """Test that has_exit is case-sensitive."""
        destination = Location("Destination")
        simple_location.add_exit("north", destination)
        
        assert simple_location.has_exit("north") is True
        assert simple_location.has_exit("North") is False
        assert simple_location.has_exit("NORTH") is False


class TestAvailableExits:
    """Test suite for querying available exits."""
    
    def test_get_available_exits_empty(self, simple_location):
        """Test getting available exits when none exist."""
        exits = simple_location.get_available_exits()
        assert exits == []
        assert isinstance(exits, list)
    
    def test_get_available_exits_single(self, simple_location):
        """Test getting available exits with one exit."""
        destination = Location("Destination")
        simple_location.add_exit("north", destination)
        
        exits = simple_location.get_available_exits()
        assert len(exits) == 1
        assert "north" in exits
    
    def test_get_available_exits_multiple(self, connected_locations):
        """Test getting available exits with multiple exits."""
        entrance = connected_locations["entrance"]
        exits = entrance.get_available_exits()
        
        assert len(exits) == 2
        assert "north" in exits
        assert "west" in exits
    
    def test_get_available_exits_order(self, simple_location):
        """Test that available exits are returned as a list."""
        simple_location.add_exit("east", Location("East Room"))
        simple_location.add_exit("west", Location("West Room"))
        simple_location.add_exit("north", Location("North Room"))
        
        exits = simple_location.get_available_exits()
        assert isinstance(exits, list)
        assert len(exits) == 3
        assert set(exits) == {"east", "west", "north"}


class TestLocationConnectivity:
    """Test suite for complex location connections."""
    
    def test_bidirectional_connection(self):
        """Test creating bidirectional connections between locations."""
        room_a = Location("Room A")
        room_b = Location("Room B")
        
        room_a.add_exit("north", room_b)
        room_b.add_exit("south", room_a)
        
        assert room_a.get_exit("north") == room_b
        assert room_b.get_exit("south") == room_a
    
    def test_circular_connections(self):
        """Test that locations can form circular connections."""
        room1 = Location("Room 1")
        room2 = Location("Room 2")
        room3 = Location("Room 3")
        
        room1.add_exit("north", room2)
        room2.add_exit("north", room3)
        room3.add_exit("north", room1)
        
        assert room1.get_exit("north") == room2
        assert room2.get_exit("north") == room3
        assert room3.get_exit("north") == room1
    
    def test_self_referential_exit(self, simple_location):
        """Test that a location can have an exit leading to itself."""
        simple_location.add_exit("loop", simple_location)
        assert simple_location.get_exit("loop") == simple_location


class TestExitsDictionary:
    """Test suite for verifying exits dictionary is properly maintained."""
    
    def test_exits_dictionary_empty_initially(self, simple_location):
        """Test that exits dictionary is empty when no exits added."""
        exits = simple_location.get_available_exits()
        assert len(exits) == 0
    
    def test_exits_dictionary_updated_on_add(self, simple_location):
        """Test that exits dictionary is updated when exits are added."""
        dest1 = Location("Dest1")
        dest2 = Location("Dest2")
        
        simple_location.add_exit("north", dest1)
        assert len(simple_location.get_available_exits()) == 1
        
        simple_location.add_exit("south", dest2)
        assert len(simple_location.get_available_exits()) == 2
    
    def test_exits_dictionary_maintains_references(self, simple_location):
        """Test that exits dictionary maintains correct location references."""
        destinations = {
            "north": Location("North Room"),
            "south": Location("South Room"),
            "east": Location("East Room")
        }
        
        for direction, dest in destinations.items():
            simple_location.add_exit(direction, dest)
        
        for direction, dest in destinations.items():
            assert simple_location.get_exit(direction) == dest