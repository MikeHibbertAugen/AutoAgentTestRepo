"""World initialization module for the Auckland adventure game.

This module provides functionality to initialize the game world with
locations in north-west Auckland and their connections.
"""

from typing import TYPE_CHECKING

from src.game_world import GameWorld
from src.location import Location

if TYPE_CHECKING:
    pass


def initialize_world() -> GameWorld:
    """Initialize the game world with Auckland locations and connections.
    
    Creates a GameWorld instance populated with locations in north-west Auckland
    including Helensville, Parakai, Kumeu, Huapai, Riverhead, Coatesville, and
    Muriwai Beach. Establishes bidirectional connections between specific location
    pairs and sets Helensville as the starting location.
    
    Connections established:
        - Helensville ↔ Parakai (north/south)
        - Kumeu ↔ Huapai (north/south)
        - Riverhead ↔ Coatesville (east/west)
    
    Returns:
        GameWorld: A fully initialized game world with all locations and connections.
        
    Example:
        >>> world = initialize_world()
        >>> starting = world.starting_location
        >>> print(starting.name)
        Helensville
    """
    # Create GameWorld instance
    world = GameWorld()
    
    # Create location instances
    helensville = Location(
        name="Helensville",
        description="A charming town in north-west Auckland, known for its hot pools and rural atmosphere."
    )
    
    parakai = Location(
        name="Parakai",
        description="A small settlement famous for the Parakai Springs hot pools, located north of Helensville."
    )
    
    kumeu = Location(
        name="Kumeu",
        description="A semi-rural town known for its wineries and vineyards in the Kumeu wine region."
    )
    
    huapai = Location(
        name="Huapai",
        description="A town adjacent to Kumeu, surrounded by vineyards and farmland."
    )
    
    riverhead = Location(
        name="Riverhead",
        description="A historic village at the head of the Waitemata Harbour's Upper Harbour."
    )
    
    coatesville = Location(
        name="Coatesville",
        description="A rural locality with lifestyle blocks and equestrian properties."
    )
    
    muriwai_beach = Location(
        name="Muriwai Beach",
        description="A rugged west coast beach famous for its black sand, surf, and gannet colony."
    )
    
    # Add all locations to the game world
    world.add_location(helensville)
    world.add_location(parakai)
    world.add_location(kumeu)
    world.add_location(huapai)
    world.add_location(riverhead)
    world.add_location(coatesville)
    world.add_location(muriwai_beach)
    
    # Establish bidirectional connections
    world.connect_locations("Helensville", "north", "Parakai")
    world.connect_locations("Kumeu", "north", "Huapai")
    world.connect_locations("Riverhead", "east", "Coatesville")
    
    # Set starting location
    world.set_starting_location(helensville)
    
    return world