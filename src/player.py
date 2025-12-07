"""
Player state management module for text-based adventure game.

This module provides the Player class that manages player state including
current location and movement between locations in the game world.
"""

from typing import Optional


class Player:
    """
    Manages player state and location in the game world.
    
    The Player class tracks the player's current location and provides
    methods to query and update the player's position.
    
    Attributes:
        current_location: The Location object where the player is currently positioned
    """
    
    def __init__(self, starting_location):
        """
        Initialize a new player at a specific location.
        
        Args:
            starting_location: The Location object where the player starts
        """
        self.current_location = starting_location
    
    def get_current_location(self):
        """
        Get the player's current location.
        
        Returns:
            The Location object where the player is currently positioned
        """
        return self.current_location
    
    def move_to(self, location) -> None:
        """
        Move the player to a new location.
        
        This method updates the player's current location to the specified
        location object. It is typically called by the game controller after
        validating that the movement is allowed.
        
        Args:
            location: The Location object to move the player to
        """
        self.current_location = location
    
    def set_location(self, location) -> None:
        """
        Set the player's location.
        
        This method is used by the movement system to update the player's
        position after a successful move command. This is an alias for
        move_to() to maintain backward compatibility.
        
        Args:
            location: The Location object to move the player to
        """
        self.current_location = location