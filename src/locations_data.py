"""
North-west Auckland locations data for the text-based adventure game.

This module contains the authentic location data and connections for the
north-west Auckland region, including towns, beaches, and natural attractions.
"""

from src.game_world import GameWorld


def populate_nw_auckland_world(world: GameWorld) -> None:
    """
    Populate the game world with north-west Auckland locations and connections.
    
    Creates authentic locations from the north-west Auckland region including
    Helensville (starting location), Kumeu wine country, Muriwai Beach, Parakai
    hot springs, and other connected areas. All locations are fully connected
    to ensure the world is traversable from the starting location.
    
    Args:
        world: The GameWorld instance to populate with locations
    """
    # Add all locations (Helensville is the starting location)
    world.add_location(
        "Helensville",
        "A historic town on the banks of the Kaipara River",
        is_starting=True
    )
    
    world.add_location(
        "Kumeu",
        "The heart of Auckland's wine country",
        is_starting=False
    )
    
    world.add_location(
        "Huapai",
        "A charming village in the wine region, neighboring Kumeu",
        is_starting=False
    )
    
    world.add_location(
        "Muriwai Beach",
        "A wild west coast beach famous for its gannet colony",
        is_starting=False
    )
    
    world.add_location(
        "Waimauku",
        "A rural township connecting the wine region to the west coast",
        is_starting=False
    )
    
    world.add_location(
        "Parakai",
        "Home to natural hot springs and pools",
        is_starting=False
    )
    
    world.add_location(
        "Riverhead",
        "A historic wharf town on the upper Waitemata Harbour",
        is_starting=False
    )
    
    world.add_location(
        "Coatesville",
        "A rural settlement with scenic countryside views",
        is_starting=False
    )
    
    world.add_location(
        "Wainui",
        "A coastal settlement near the entrance to the Kaipara Harbour",
        is_starting=False
    )
    
    # Establish connections between locations
    # Kumeu wine region connections
    world.connect_locations("Kumeu", "Huapai", "north")
    
    # Muriwai Beach area connections
    world.connect_locations("Muriwai Beach", "Waimauku", "east")
    world.connect_locations("Waimauku", "Kumeu", "east")
    
    # Parakai and Helensville connection
    world.connect_locations("Parakai", "Helensville", "south")
    
    # Riverhead area connections
    world.connect_locations("Riverhead", "Kumeu", "north")
    world.connect_locations("Riverhead", "Coatesville", "north")
    
    # Additional connections to ensure full connectivity from Helensville
    world.connect_locations("Helensville", "Kumeu", "south")
    world.connect_locations("Helensville", "Wainui", "west")
    world.connect_locations("Wainui", "Parakai", "east")