"""
Player state management module for text-based adventure game.

This module provides the Player class that manages player state including
current location and movement between locations in the game world.
"""

from typing import Tuple, Optional


class Player:
    """
    Manages player state and location in the game world.
    
    The Player class tracks the player's current location and handles
    movement between locations with validation.
    
    Attributes:
        world: Reference to the World instance containing all locations
        current_location: Name of the player's current location
    """
    
    def __init__(self, world, starting_location: str = "Helensville"):
        """
        Initialize a new player in the game world.
        
        Args:
            world: The World instance containing all game locations
            starting_location: The name of the location where player starts
                             (default: "Helensville")
        """
        self.world = world
        self.current_location = starting_location
    
    def get_location(self) -> str:
        """
        Get the name of the player's current location.
        
        Returns:
            The name of the current location as a string
        """
        return self.current_location
    
    def move(self, direction: str) -> Tuple[bool, Optional[str]]:
        """
        Attempt to move the player in the specified direction.
        
        Validates that an exit exists in the given direction from the current
        location. If valid, updates the player's location. If invalid, the
        player remains at the current location.
        
        Args:
            direction: The direction to move (e.g., "north", "south", "east", "west")
        
        Returns:
            A tuple containing:
                - bool: True if movement was successful, False otherwise
                - str or None: Error message if movement failed, None if successful
        """
        location = self.world.get_location(self.current_location)
        
        if location is None:
            return False, f"Current location '{self.current_location}' not found in world"
        
        if not location.has_exit(direction):
            return False, f"Cannot move {direction} from {self.current_location}"
        
        destination = location.get_exit(direction)
        self.current_location = destination
        return True, None