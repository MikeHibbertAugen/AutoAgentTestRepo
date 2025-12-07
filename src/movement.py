"""Movement command processing and validation logic for the text-based adventure game.

This module implements the MoveCommand class that handles movement requests,
validates directions, and generates appropriate feedback messages.
"""

from typing import Optional
from src.constants import DIRECTION_ABBREVIATIONS
from src.player import Player


class MovementResult:
    """Represents the result of a movement command execution.
    
    Attributes:
        success (bool): Whether the movement was successful
        message (str): Feedback message describing the result
    """
    
    def __init__(self, success: bool, message: str):
        """Initialize a movement result.
        
        Args:
            success: Whether the movement was successful
            message: Feedback message for the player
        """
        self.success = success
        self.message = message


class MoveCommand:
    """Processes movement commands and executes player movement."""
    
    @staticmethod
    def normalize_direction(direction: str) -> str:
        """Normalize a direction string, converting abbreviations to full names.
        
        Args:
            direction: The direction string (e.g., 'n', 'north', 'NORTH')
            
        Returns:
            The normalized direction in lowercase (e.g., 'north')
        """
        direction_lower = direction.lower().strip()
        
        # Check if it's an abbreviation
        if direction_lower in DIRECTION_ABBREVIATIONS:
            return DIRECTION_ABBREVIATIONS[direction_lower]
        
        return direction_lower
    
    @staticmethod
    def execute(player: Player, direction: str) -> MovementResult:
        """Execute a movement command for a player.
        
        Args:
            player: The player attempting to move
            direction: The direction to move (can be abbreviated)
            
        Returns:
            MovementResult indicating success/failure and containing a message
        """
        # Normalize the direction (handle abbreviations and case)
        normalized_direction = MoveCommand.normalize_direction(direction)
        
        # Get the player's current location
        current_location = player.get_current_location()
        
        # Check if the direction is valid from the current location
        destination = current_location.get_exit(normalized_direction)
        
        if destination is None:
            # Invalid movement - no exit in that direction
            return MovementResult(
                success=False,
                message=f"You cannot go {normalized_direction} from here."
            )
        
        # Valid movement - move the player
        player.set_location(destination)
        
        return MovementResult(
            success=True,
            message=f"You moved {normalized_direction} to {destination.name}."
        )
    
    @staticmethod
    def is_valid_direction(player: Player, direction: str) -> bool:
        """Check if a direction is valid from the player's current location.
        
        Args:
            player: The player checking the direction
            direction: The direction to check (can be abbreviated)
            
        Returns:
            True if the direction is valid, False otherwise
        """
        normalized_direction = MoveCommand.normalize_direction(direction)
        current_location = player.get_current_location()
        return current_location.has_exit(normalized_direction)