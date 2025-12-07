"""Unit tests for the GameWorld class."""

import pytest
from src.location import Location
from src.game_world import GameWorld


@pytest.fixture
def empty_world():
    """Create an empty game world for testing."""
    return GameWorld()


@pytest.fixture
def sample_locations():
    """Create sample locations for testing."""
    location1 = Location("Town Square", "A bustling town square.")
    location2 = Location("Forest", "A dark and mysterious forest.")
    location3 = Location("Beach", "A sunny beach with warm sand.")
    return location1, location2, location3


@pytest.fixture
def populated_world(sample_locations):
    """Create a game world with sample locations."""
    world = GameWorld()
    for location in sample_locations:
        world.add_location(location)
    return world


class TestGameWorldCreation:
    """Tests for GameWorld instantiation."""

    def test_create_empty_world(self, empty_world):
        """Test creating an empty game world."""
        assert empty_world is not None
        assert isinstance(empty_world.locations, dict)
        assert len(empty_world.locations) == 0
        assert empty_world.starting_location is None


class TestAddLocation:
    """Tests for adding locations to the game world."""

    def test_add_single_location(self, empty_world):
        """Test adding a single location to the world."""
        location = Location("Test Location", "A test location.")
        empty_world.add_location(location)
        
        assert empty_world.has_location("Test Location")
        assert len(empty_world.locations) == 1

    def test_add_multiple_locations(self, empty_world, sample_locations):
        """Test adding multiple locations to the world."""
        for location in sample_locations:
            empty_world.add_location(location)
        
        assert len(empty_world.locations) == 3
        assert empty_world.has_location("Town Square")
        assert empty_world.has_location("Forest")
        assert empty_world.has_location("Beach")

    def test_add_duplicate_location_name(self, empty_world):
        """Test that adding a location with duplicate name replaces the old one."""
        location1 = Location("Duplicate", "First description")
        location2 = Location("Duplicate", "Second description")
        
        empty_world.add_location(location1)
        empty_world.add_location(location2)
        
        assert len(empty_world.locations) == 1
        retrieved = empty_world.get_location("Duplicate")
        assert retrieved.description == "Second description"


class TestGetLocation:
    """Tests for retrieving locations from the game world."""

    def test_get_existing_location(self, populated_world):
        """Test retrieving an existing location."""
        location = populated_world.get_location("Town Square")
        
        assert location is not None
        assert location.name == "Town Square"
        assert location.description == "A bustling town square."

    def test_get_nonexistent_location(self, populated_world):
        """Test retrieving a location that doesn't exist."""
        location = populated_world.get_location("Nonexistent Place")
        
        assert location is None

    def test_get_location_from_empty_world(self, empty_world):
        """Test retrieving from an empty world."""
        location = empty_world.get_location("Anywhere")
        
        assert location is None


class TestHasLocation:
    """Tests for checking location existence."""

    def test_has_existing_location(self, populated_world):
        """Test checking for an existing location."""
        assert populated_world.has_location("Town Square") is True
        assert populated_world.has_location("Forest") is True
        assert populated_world.has_location("Beach") is True

    def test_has_nonexistent_location(self, populated_world):
        """Test checking for a nonexistent location."""
        assert populated_world.has_location("Nonexistent") is False

    def test_has_location_empty_world(self, empty_world):
        """Test checking location in empty world."""
        assert empty_world.has_location("Anywhere") is False


class TestSetStartingLocation:
    """Tests for setting the starting location."""

    def test_set_starting_location(self, populated_world, sample_locations):
        """Test setting a valid starting location."""
        town_square = sample_locations[0]
        populated_world.set_starting_location(town_square)
        
        assert populated_world.starting_location == town_square
        assert populated_world.starting_location.name == "Town Square"

    def test_change_starting_location(self, populated_world, sample_locations):
        """Test changing the starting location."""
        town_square, forest, beach = sample_locations
        
        populated_world.set_starting_location(town_square)
        assert populated_world.starting_location == town_square
        
        populated_world.set_starting_location(beach)
        assert populated_world.starting_location == beach


class TestConnectLocations:
    """Tests for connecting locations bidirectionally."""

    def test_connect_two_locations(self, populated_world):
        """Test connecting two locations creates bidirectional exits."""
        populated_world.connect_locations("Town Square", "north", "Forest")
        
        town_square = populated_world.get_location("Town Square")
        forest = populated_world.get_location("Forest")
        
        assert town_square.has_exit("north")
        assert town_square.get_exit("north") == forest
        assert forest.has_exit("south")
        assert forest.get_exit("south") == town_square

    def test_connect_multiple_directions(self, populated_world):
        """Test connecting locations in multiple directions."""
        populated_world.connect_locations("Town Square", "north", "Forest")
        populated_world.connect_locations("Town Square", "east", "Beach")
        
        town_square = populated_world.get_location("Town Square")
        
        assert town_square.has_exit("north")
        assert town_square.has_exit("east")
        assert town_square.get_exit("north").name == "Forest"
        assert town_square.get_exit("east").name == "Beach"

    def test_connect_nonexistent_location(self, populated_world):
        """Test connecting to a nonexistent location raises error."""
        with pytest.raises(ValueError):
            populated_world.connect_locations("Town Square", "north", "Nonexistent")

    def test_connect_from_nonexistent_location(self, populated_world):
        """Test connecting from a nonexistent location raises error."""
        with pytest.raises(ValueError):
            populated_world.connect_locations("Nonexistent", "north", "Forest")

    def test_bidirectional_connection_consistency(self, populated_world):
        """Test that bidirectional connections are consistent."""
        populated_world.connect_locations("Town Square", "west", "Beach")
        
        town_square = populated_world.get_location("Town Square")
        beach = populated_world.get_location("Beach")
        
        # Forward connection
        assert town_square.get_exit("west") == beach
        # Reverse connection
        assert beach.get_exit("east") == town_square
        # Verify navigation works both ways
        assert town_square.get_exit("west").get_exit("east") == town_square


class TestCountLocations:
    """Tests for counting locations in the world."""

    def test_count_empty_world(self, empty_world):
        """Test counting locations in an empty world."""
        assert empty_world.count_locations() == 0

    def test_count_single_location(self, empty_world):
        """Test counting a single location."""
        location = Location("Test", "A test location.")
        empty_world.add_location(location)
        assert empty_world.count_locations() == 1

    def test_count_multiple_locations(self, populated_world):
        """Test counting multiple locations."""
        assert populated_world.count_locations() == 3


class TestWorldConnectivity:
    """Tests for checking world connectivity."""

    def test_empty_world_not_connected(self, empty_world):
        """Test that an empty world is not fully connected."""
        assert empty_world.is_fully_connected() is False

    def test_single_location_as_starting(self, empty_world):
        """Test that a single location world is fully connected."""
        location = Location("Solo", "The only location.")
        empty_world.add_location(location)
        empty_world.set_starting_location(location)
        assert empty_world.is_fully_connected() is True

    def test_fully_connected_world(self, populated_world, sample_locations):
        """Test a fully connected world."""
        town_square, forest, beach = sample_locations
        
        # Set starting location
        populated_world.set_starting_location(town_square)
        
        # Connect all locations
        populated_world.connect_locations("Town Square", "north", "Forest")
        populated_world.connect_locations("Town Square", "east", "Beach")
        
        assert populated_world.is_fully_connected() is True

    def test_disconnected_world(self, empty_world):
        """Test a world with disconnected locations."""
        loc1 = Location("Location 1", "First location.")
        loc2 = Location("Location 2", "Second location.")
        loc3 = Location("Location 3", "Third isolated location.")
        
        empty_world.add_location(loc1)
        empty_world.add_location(loc2)
        empty_world.add_location(loc3)
        
        # Connect only loc1 and loc2
        empty_world.connect_locations("Location 1", "north", "Location 2")
        
        # Set starting location
        empty_world.set_starting_location(loc1)
        
        # loc3 is isolated, so world is not fully connected
        assert empty_world.is_fully_connected() is False

    def test_world_without_starting_location(self, populated_world):
        """Test that a world without a starting location is not connected."""
        populated_world.connect_locations("Town Square", "north", "Forest")
        populated_world.connect_locations("Forest", "east", "Beach")
        
        # No starting location set
        assert populated_world.is_fully_connected() is False

    def test_complex_connected_world(self, empty_world):
        """Test a more complex fully connected world."""
        # Create a ring of locations
        locations = []
        for i in range(5):
            loc = Location(f"Location {i}", f"Location number {i}.")
            empty_world.add_location(loc)
            locations.append(loc)
        
        # Connect in a ring
        empty_world.connect_locations("Location 0", "east", "Location 1")
        empty_world.connect_locations("Location 1", "east", "Location 2")
        empty_world.connect_locations("Location 2", "east", "Location 3")
        empty_world.connect_locations("Location 3", "east", "Location 4")
        empty_world.connect_locations("Location 4", "north", "Location 0")
        
        empty_world.set_starting_location(locations[0])
        
        assert empty_world.is_fully_connected() is True


class TestGameWorldIntegration:
    """Integration tests for complete game world workflows."""

    def test_build_small_world(self, empty_world):
        """Test building a small connected world."""
        # Create locations
        home = Location("Home", "Your cozy home.")
        garden = Location("Garden", "A beautiful garden.")
        street = Location("Street", "A quiet street.")
        
        # Add to world
        empty_world.add_location(home)
        empty_world.add_location(garden)
        empty_world.add_location(street)
        
        # Connect locations
        empty_world.connect_locations("Home", "south", "Garden")
        empty_world.connect_locations("Home", "east", "Street")
        
        # Set starting location
        empty_world.set_starting_location(home)
        
        # Verify world structure
        assert len(empty_world.locations) == 3
        assert empty_world.starting_location == home
        assert home.has_exit("south")
        assert home.has_exit("east")
        assert garden.has_exit("north")
        assert street.has_exit("west")

    def test_navigate_through_world(self, populated_world):
        """Test navigation through connected locations."""
        populated_world.connect_locations("Town Square", "north", "Forest")
        populated_world.connect_locations("Forest", "east", "Beach")
        
        # Start at town square
        current = populated_world.get_location("Town Square")
        assert current.name == "Town Square"
        
        # Move north to forest
        current = current.get_exit("north")
        assert current.name == "Forest"
        
        # Move east to beach
        current = current.get_exit("east")
        assert current.name == "Beach"
        
        # Move back west to forest
        current = current.get_exit("west")
        assert current.name == "Forest"
        
        # Move back south to town square
        current = current.get_exit("south")
        assert current.name == "Town Square"