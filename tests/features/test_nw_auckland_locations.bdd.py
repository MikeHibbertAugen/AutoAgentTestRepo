"""
BDD-style tests for North-West Auckland locations feature.

These tests verify the authentic north-west Auckland location data
matches the specifications defined in the feature scenarios.
"""

import pytest
from src.game_world import GameWorld
from src.locations_data import populate_nw_auckland_world


@pytest.fixture
def nw_auckland_world():
    """Fixture that creates a fresh GameWorld populated with NW Auckland locations."""
    world = GameWorld()
    populate_nw_auckland_world(world)
    return world


def test_scenario_1_helensville_starting_location(nw_auckland_world):
    """
    Scenario 1: Helensville as the starting location
    Given the game world is initialized with north-west Auckland locations
    When I query for the starting location
    Then I should get Helensville
    And it should have a description mentioning the Kaipara River
    """
    world = nw_auckland_world
    
    # Verify starting location exists
    assert world.starting_location is not None, "Starting location should be set"
    
    # Verify starting location is Helensville
    assert world.starting_location.name == "Helensville", \
        "Starting location should be Helensville"
    
    # Verify description mentions Kaipara River
    description = world.starting_location.description.lower()
    assert "kaipara river" in description, \
        "Helensville description should mention the Kaipara River"


def test_scenario_2_kumeu_wine_region(nw_auckland_world):
    """
    Scenario 2: Kumeu wine region location
    Given the game world contains Kumeu
    When I examine Kumeu
    Then it should describe the wine country
    And it should be connected to Huapai to the north
    """
    world = nw_auckland_world
    
    # Verify Kumeu exists
    kumeu = world.get_location("Kumeu")
    assert kumeu is not None, "Kumeu location should exist"
    
    # Verify wine country description
    description = kumeu.description.lower()
    assert "wine" in description, "Kumeu description should mention wine"
    
    # Verify connection to Huapai (north from Kumeu)
    assert "north" in kumeu.connections, "Kumeu should have a north connection"
    assert kumeu.connections["north"].name == "Huapai", \
        "Kumeu's north connection should be Huapai"
    
    # Verify bidirectional connection (south from Huapai to Kumeu)
    huapai = world.get_location("Huapai")
    assert huapai is not None, "Huapai location should exist"
    assert "south" in huapai.connections, "Huapai should have a south connection"
    assert huapai.connections["south"].name == "Kumeu", \
        "Huapai's south connection should be Kumeu"


def test_scenario_3_muriwai_beach(nw_auckland_world):
    """
    Scenario 3: Muriwai Beach location
    Given the game world contains Muriwai Beach
    When I examine Muriwai Beach
    Then it should describe the gannet colony
    And it should be connected to Waimauku to the east
    """
    world = nw_auckland_world
    
    # Verify Muriwai Beach exists
    muriwai = world.get_location("Muriwai Beach")
    assert muriwai is not None, "Muriwai Beach location should exist"
    
    # Verify gannet colony description
    description = muriwai.description.lower()
    assert "gannet" in description, "Muriwai Beach description should mention gannets"
    
    # Verify connection to Waimauku (east from Muriwai)
    assert "east" in muriwai.connections, "Muriwai Beach should have an east connection"
    assert muriwai.connections["east"].name == "Waimauku", \
        "Muriwai Beach's east connection should be Waimauku"
    
    # Verify bidirectional connection (west from Waimauku to Muriwai)
    waimauku = world.get_location("Waimauku")
    assert waimauku is not None, "Waimauku location should exist"
    assert "west" in waimauku.connections, "Waimauku should have a west connection"
    assert waimauku.connections["west"].name == "Muriwai Beach", \
        "Waimauku's west connection should be Muriwai Beach"


def test_scenario_4_parakai_springs(nw_auckland_world):
    """
    Scenario 4: Parakai hot springs location
    Given the game world contains Parakai
    When I examine Parakai
    Then it should describe the hot springs
    And it should be connected to Helensville to the south
    """
    world = nw_auckland_world
    
    # Verify Parakai exists
    parakai = world.get_location("Parakai")
    assert parakai is not None, "Parakai location should exist"
    
    # Verify hot springs description
    description = parakai.description.lower()
    assert "hot spring" in description or "springs" in description, \
        "Parakai description should mention hot springs"
    
    # Verify connection to Helensville (south from Parakai)
    assert "south" in parakai.connections, "Parakai should have a south connection"
    assert parakai.connections["south"].name == "Helensville", \
        "Parakai's south connection should be Helensville"
    
    # Verify bidirectional connection (north from Helensville to Parakai)
    helensville = world.get_location("Helensville")
    assert helensville is not None, "Helensville location should exist"
    assert "north" in helensville.connections, "Helensville should have a north connection"
    assert helensville.connections["north"].name == "Parakai", \
        "Helensville's north connection should be Parakai"


def test_scenario_5_riverhead_area(nw_auckland_world):
    """
    Scenario 5: Riverhead and surrounding areas
    Given the game world contains Riverhead
    When I examine Riverhead
    Then it should describe the historic wharf
    And it should be connected to both Kumeu and Coatesville
    """
    world = nw_auckland_world
    
    # Verify Riverhead exists
    riverhead = world.get_location("Riverhead")
    assert riverhead is not None, "Riverhead location should exist"
    
    # Verify historic wharf description
    description = riverhead.description.lower()
    assert "wharf" in description or "harbour" in description, \
        "Riverhead description should mention wharf or harbour"
    
    # Verify connection to Kumeu exists (in any direction)
    kumeu_connected = any(
        conn.name == "Kumeu" for conn in riverhead.connections.values()
    )
    assert kumeu_connected, "Riverhead should be connected to Kumeu"
    
    # Verify connection to Coatesville exists (in any direction)
    coatesville_connected = any(
        conn.name == "Coatesville" for conn in riverhead.connections.values()
    )
    assert coatesville_connected, "Riverhead should be connected to Coatesville"
    
    # Verify bidirectional connections
    kumeu = world.get_location("Kumeu")
    assert kumeu is not None, "Kumeu location should exist"
    riverhead_from_kumeu = any(
        conn.name == "Riverhead" for conn in kumeu.connections.values()
    )
    assert riverhead_from_kumeu, "Kumeu should be connected back to Riverhead"
    
    coatesville = world.get_location("Coatesville")
    assert coatesville is not None, "Coatesville location should exist"
    riverhead_from_coatesville = any(
        conn.name == "Riverhead" for conn in coatesville.connections.values()
    )
    assert riverhead_from_coatesville, \
        "Coatesville should be connected back to Riverhead"


def test_scenario_6_minimum_locations_count(nw_auckland_world):
    """
    Scenario 6: Minimum number of locations
    Given the game world is populated with north-west Auckland locations
    When I count all locations
    Then there should be at least 8 distinct locations
    """
    world = nw_auckland_world
    
    location_count = world.count_locations()
    assert location_count >= 8, \
        f"Game world should have at least 8 locations, but has {location_count}"
    
    # Verify all locations are distinct by checking names
    location_names = list(world.locations.keys())
    unique_names = set(location_names)
    assert len(location_names) == len(unique_names), \
        "All locations should have unique names"


def test_scenario_7_world_connectivity(nw_auckland_world):
    """
    Scenario 7: All locations are connected
    Given the game world is fully populated
    When I analyze the location graph
    Then all locations should be reachable from the starting location
    """
    world = nw_auckland_world
    
    # Verify the world is fully connected
    assert world.is_fully_connected(), \
        "All locations should be reachable from the starting location (Helensville)"
    
    # Additional verification: ensure starting location exists
    assert world.starting_location is not None, \
        "Starting location must be set for connectivity check"
    
    # Verify at least one location has connections
    total_connections = sum(
        len(loc.connections) for loc in world.locations.values()
    )
    assert total_connections > 0, \
        "Game world should have at least some connections between locations"