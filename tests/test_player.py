"""
BDD-style tests for player state management.

Tests cover:
- Player initialization at starting location
- Location tracking
- Successful movement between locations
- Blocked movement with error handling
"""

import pytest
from src.player import Player
from src.world import World, Location


@pytest.fixture
def world():
    """Create a test world with multiple locations."""
    test_world = World()
    
    # Create locations
    helensville = Location("Helensville")
    parakai = Location("Parakai")
    kumeu = Location("Kumeu")
    muriwai_beach = Location("Muriwai Beach")
    
    # Set up connections
    helensville.add_exit("south", "Parakai")
    helensville.add_exit("east", "Kumeu")
    parakai.add_exit("north", "Helensville")
    kumeu.add_exit("west", "Helensville")
    kumeu.add_exit("north", "Muriwai Beach")
    muriwai_beach.add_exit("south", "Kumeu")
    
    # Add locations to world
    test_world.add_location(helensville)
    test_world.add_location(parakai)
    test_world.add_location(kumeu)
    test_world.add_location(muriwai_beach)
    
    return test_world


@pytest.fixture
def player(world):
    """Create a player in the test world."""
    return Player(world)


def test_initialize_player_at_starting_location(world):
    """
    Scenario: Initialize player at starting location
    Given the game world is initialized
    When a new game is started
    Then the player should be at "Helensville"
    """
    # Given the game world is initialized (world fixture)
    
    # When a new game is started
    player = Player(world)
    
    # Then the player should be at "Helensville"
    assert player.get_current_location() == "Helensville"


def test_track_player_current_location(world):
    """
    Scenario: Track player current location
    Given the player is at "Kumeu"
    When the location is queried
    Then it should return "Kumeu"
    """
    # Given the player is at "Kumeu"
    player = Player(world, starting_location="Kumeu")
    
    # When the location is queried
    current_location = player.get_current_location()
    
    # Then it should return "Kumeu"
    assert current_location == "Kumeu"


def test_successful_movement(player):
    """
    Scenario: Successful movement
    Given the player is at "Helensville"
    And there is an exit south to "Parakai"
    When the player moves south
    Then the player should be at "Parakai"
    And the movement should be successful
    """
    # Given the player is at "Helensville"
    assert player.get_current_location() == "Helensville"
    
    # And there is an exit south to "Parakai" (already set up in world fixture)
    
    # When the player moves south
    success, message = player.move("south")
    
    # Then the player should be at "Parakai"
    assert player.get_current_location() == "Parakai"
    
    # And the movement should be successful
    assert success is True
    assert message == "Moved south to Parakai"


def test_blocked_movement(world):
    """
    Scenario: Blocked movement
    Given the player is at "Muriwai Beach"
    And there is no exit to the north
    When the player attempts to move north
    Then the player should remain at "Muriwai Beach"
    And an error message should be generated
    """
    # Given the player is at "Muriwai Beach"
    player = Player(world, starting_location="Muriwai Beach")
    assert player.get_current_location() == "Muriwai Beach"
    
    # And there is no exit to the north (no north exit from Muriwai Beach)
    
    # When the player attempts to move north
    success, message = player.move("north")
    
    # Then the player should remain at "Muriwai Beach"
    assert player.get_current_location() == "Muriwai Beach"
    
    # And an error message should be generated
    assert success is False
    assert "cannot go north" in message.lower() or "no exit" in message.lower()


def test_multiple_movements(player):
    """
    Test multiple consecutive movements to verify state persistence.
    """
    # Start at Helensville
    assert player.get_current_location() == "Helensville"
    
    # Move south to Parakai
    success, _ = player.move("south")
    assert success is True
    assert player.get_current_location() == "Parakai"
    
    # Move back north to Helensville
    success, _ = player.move("north")
    assert success is True
    assert player.get_current_location() == "Helensville"
    
    # Move east to Kumeu
    success, _ = player.move("east")
    assert success is True
    assert player.get_current_location() == "Kumeu"
    
    # Move north to Muriwai Beach
    success, _ = player.move("north")
    assert success is True
    assert player.get_current_location() == "Muriwai Beach"


def test_invalid_direction(player):
    """
    Test movement with an invalid direction that doesn't exist.
    """
    # Player starts at Helensville
    assert player.get_current_location() == "Helensville"
    
    # Try to move in an invalid direction
    success, message = player.move("northeast")
    
    # Player should remain at Helensville
    assert player.get_current_location() == "Helensville"
    assert success is False
    assert message is not None