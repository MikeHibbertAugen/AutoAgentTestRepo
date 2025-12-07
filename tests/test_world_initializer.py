"""
BDD-style tests for world initialization scenarios.

Tests the complete world initialization process, verifying that:
1. World contains at least one location and has a starting location
2. Specific location pairs are connected as specified
3. All connections are bidirectional
4. All required Auckland locations are present
"""

import pytest
from src.world_initializer import initialize_world
from src.game_world import GameWorld


@pytest.fixture(scope="module")
def game_world() -> GameWorld:
    """Fixture to initialize the game world once for all tests in this module."""
    return initialize_world()


def test_world_contains_locations_and_has_starting_location(game_world: GameWorld) -> None:
    """
    Scenario 1: World contains at least one location and has starting location.
    
    Given the game world is initialized
    When I check the world state
    Then the world should contain at least one location
    And the world should have a defined starting location
    """
    # Check that at least one location exists
    assert game_world.has_location("Helensville"), "World should contain at least one location"
    
    # Check that starting location is defined
    assert game_world.starting_location is not None, "World should have a starting location"
    assert game_world.starting_location.name == "Helensville", "Starting location should be Helensville"


def test_specific_location_pairs_are_connected(game_world: GameWorld) -> None:
    """
    Scenario 2: Specific location pairs are connected.
    
    Given the game world is initialized
    When I check the connections between specific locations
    Then Helensville should be connected to Parakai (north/south)
    And Kumeu should be connected to Huapai (north/south)
    And Riverhead should be connected to Coatesville (east/west)
    """
    # Test Helensville-Parakai connection
    helensville = game_world.get_location("Helensville")
    assert helensville is not None, "Helensville should exist"
    parakai = helensville.get_exit("north")
    assert parakai is not None, "Helensville should have a north exit to Parakai"
    assert parakai.name == "Parakai", "North exit from Helensville should lead to Parakai"
    
    # Test Kumeu-Huapai connection
    kumeu = game_world.get_location("Kumeu")
    assert kumeu is not None, "Kumeu should exist"
    huapai = kumeu.get_exit("north")
    assert huapai is not None, "Kumeu should have a north exit to Huapai"
    assert huapai.name == "Huapai", "North exit from Kumeu should lead to Huapai"
    
    # Test Riverhead-Coatesville connection
    riverhead = game_world.get_location("Riverhead")
    assert riverhead is not None, "Riverhead should exist"
    coatesville = riverhead.get_exit("east")
    assert coatesville is not None, "Riverhead should have an east exit to Coatesville"
    assert coatesville.name == "Coatesville", "East exit from Riverhead should lead to Coatesville"


def test_connections_are_bidirectional(game_world: GameWorld) -> None:
    """
    Scenario 3: Bidirectional connections.
    
    Given the game world is initialized
    When I check if location A connects to location B
    Then location B should also connect back to location A
    """
    # Test Helensville-Parakai bidirectional connection
    helensville = game_world.get_location("Helensville")
    parakai = game_world.get_location("Parakai")
    assert helensville is not None and parakai is not None
    
    assert helensville.get_exit("north") == parakai, "Helensville should connect north to Parakai"
    assert parakai.get_exit("south") == helensville, "Parakai should connect south to Helensville"
    
    # Test Kumeu-Huapai bidirectional connection
    kumeu = game_world.get_location("Kumeu")
    huapai = game_world.get_location("Huapai")
    assert kumeu is not None and huapai is not None
    
    assert kumeu.get_exit("north") == huapai, "Kumeu should connect north to Huapai"
    assert huapai.get_exit("south") == kumeu, "Huapai should connect south to Kumeu"
    
    # Test Riverhead-Coatesville bidirectional connection
    riverhead = game_world.get_location("Riverhead")
    coatesville = game_world.get_location("Coatesville")
    assert riverhead is not None and coatesville is not None
    
    assert riverhead.get_exit("east") == coatesville, "Riverhead should connect east to Coatesville"
    assert coatesville.get_exit("west") == riverhead, "Coatesville should connect west to Riverhead"


def test_all_required_auckland_locations_are_loaded(game_world: GameWorld) -> None:
    """
    Scenario 4: All required Auckland locations are loaded.
    
    Given the game world is initialized
    When I check for all required locations
    Then all of the following locations should exist:
    - Helensville
    - Parakai
    - Kumeu
    - Huapai
    - Riverhead
    - Coatesville
    - Muriwai Beach
    """
    required_locations = [
        "Helensville",
        "Parakai",
        "Kumeu",
        "Huapai",
        "Riverhead",
        "Coatesville",
        "Muriwai Beach"
    ]
    
    for location_name in required_locations:
        assert game_world.has_location(location_name), f"World should contain {location_name}"
        location = game_world.get_location(location_name)
        assert location is not None, f"{location_name} should be retrievable"
        assert location.name == location_name, f"Location name should be {location_name}"