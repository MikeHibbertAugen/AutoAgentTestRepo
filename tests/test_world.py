"""Unit tests for world and location classes."""

import pytest
from src.world import Location, World


class TestLocation:
    """Tests for the Location class."""

    def test_location_creation(self):
        """Test creating a location with a name."""
        location = Location("Helensville")
        assert location.name == "Helensville"

    def test_location_with_no_exits(self):
        """Test a location with no exits."""
        location = Location("Helensville")
        assert not location.has_exit("north")
        assert not location.has_exit("south")
        assert location.get_destination("north") is None

    def test_location_add_single_exit(self):
        """Test adding a single exit to a location."""
        location = Location("Helensville")
        location.add_exit("south", "Parakai")
        assert location.has_exit("south")
        assert location.get_destination("south") == "Parakai"

    def test_location_add_multiple_exits(self):
        """Test adding multiple exits to a location."""
        location = Location("Helensville")
        location.add_exit("south", "Parakai")
        location.add_exit("east", "Kumeu")
        location.add_exit("west", "Muriwai Beach")
        
        assert location.has_exit("south")
        assert location.has_exit("east")
        assert location.has_exit("west")
        assert not location.has_exit("north")
        
        assert location.get_destination("south") == "Parakai"
        assert location.get_destination("east") == "Kumeu"
        assert location.get_destination("west") == "Muriwai Beach"

    def test_location_get_nonexistent_exit(self):
        """Test getting a destination for a nonexistent exit."""
        location = Location("Helensville")
        location.add_exit("south", "Parakai")
        assert location.get_destination("north") is None


class TestWorld:
    """Tests for the World class."""

    def test_world_creation(self):
        """Test creating an empty world."""
        world = World()
        assert world is not None

    def test_world_add_location(self):
        """Test adding a location to the world."""
        world = World()
        location = Location("Helensville")
        world.add_location(location)
        
        retrieved = world.get_location("Helensville")
        assert retrieved is not None
        assert retrieved.name == "Helensville"

    def test_world_add_multiple_locations(self):
        """Test adding multiple locations to the world."""
        world = World()
        helensville = Location("Helensville")
        parakai = Location("Parakai")
        kumeu = Location("Kumeu")
        
        world.add_location(helensville)
        world.add_location(parakai)
        world.add_location(kumeu)
        
        assert world.get_location("Helensville") is not None
        assert world.get_location("Parakai") is not None
        assert world.get_location("Kumeu") is not None

    def test_world_get_nonexistent_location(self):
        """Test getting a location that doesn't exist."""
        world = World()
        assert world.get_location("Nonexistent") is None

    def test_world_with_connected_locations(self):
        """Test world with locations connected by exits."""
        world = World()
        
        helensville = Location("Helensville")
        parakai = Location("Parakai")
        kumeu = Location("Kumeu")
        
        helensville.add_exit("south", "Parakai")
        helensville.add_exit("east", "Kumeu")
        parakai.add_exit("north", "Helensville")
        kumeu.add_exit("west", "Helensville")
        
        world.add_location(helensville)
        world.add_location(parakai)
        world.add_location(kumeu)
        
        # Verify connections work through world
        helensville_retrieved = world.get_location("Helensville")
        assert helensville_retrieved.has_exit("south")
        assert helensville_retrieved.get_destination("south") == "Parakai"
        
        parakai_retrieved = world.get_location("Parakai")
        assert parakai_retrieved.has_exit("north")
        assert parakai_retrieved.get_destination("north") == "Helensville"

    def test_world_starting_location(self):
        """Test that world has a defined starting location constant."""
        assert World.STARTING_LOCATION == "Helensville"

    @pytest.fixture
    def populated_world(self):
        """Fixture providing a world with multiple connected locations."""
        world = World()
        
        helensville = Location("Helensville")
        helensville.add_exit("south", "Parakai")
        helensville.add_exit("east", "Kumeu")
        helensville.add_exit("west", "Muriwai Beach")
        
        parakai = Location("Parakai")
        parakai.add_exit("north", "Helensville")
        
        kumeu = Location("Kumeu")
        kumeu.add_exit("west", "Helensville")
        
        muriwai = Location("Muriwai Beach")
        muriwai.add_exit("east", "Helensville")
        
        world.add_location(helensville)
        world.add_location(parakai)
        world.add_location(kumeu)
        world.add_location(muriwai)
        
        return world

    def test_populated_world_navigation(self, populated_world):
        """Test navigation through a populated world."""
        start = populated_world.get_location("Helensville")
        assert start is not None
        
        # Can go south to Parakai
        assert start.has_exit("south")
        parakai_name = start.get_destination("south")
        parakai = populated_world.get_location(parakai_name)
        assert parakai is not None
        assert parakai.name == "Parakai"
        
        # From Parakai can go back north
        assert parakai.has_exit("north")
        assert parakai.get_destination("north") == "Helensville"