"""
Location-based adventure game package for a text-based game set in north-west Auckland.

This package provides core game world models including Location for representing
navigable game locations with descriptions and interconnected exits, GameWorld
for managing the collection of locations and their connections, and world
initialization utilities for setting up the north-west Auckland map.
"""

from src.location import Location
from src.game_world import GameWorld
from src.world_initializer import initialize_world

__version__ = "0.1.0"
__all__ = ["Location", "GameWorld", "initialize_world"]