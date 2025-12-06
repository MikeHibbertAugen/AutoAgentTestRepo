"""
Feedback messages module for text-based adventure game.

This module contains all user-facing messages and feedback constants used
throughout the game. Centralizing messages here makes it easy to update
text and add localization support in the future.
"""

from typing import Optional

# Success messages
SUCCESS_MOVEMENT = "You travel {direction} to {location}."
SUCCESS_LOOK = "You are currently in {location}."

# Error messages
ERROR_INVALID_DIRECTION = "You cannot go {direction} from here."
ERROR_UNRECOGNIZED_COMMAND = "I don't understand '{command}'."
ERROR_EMPTY_COMMAND = "Please enter a command."
ERROR_NO_EXIT = "There is no exit in that direction."

# Help messages
HELP_SUGGESTION = "Type 'help' for a list of available commands."
HELP_TEXT = """Available commands:
  Movement: north, south, east, west, n, s, e, w
  Actions: look, inventory, help
  Other: quit, exit"""

# Command aliases
DIRECTION_ALIASES = {
    'n': 'north',
    's': 'south',
    'e': 'east',
    'w': 'west',
    'ne': 'northeast',
    'nw': 'northwest',
    'se': 'southeast',
    'sw': 'southwest',
}


def format_success_movement(direction: str, location: str) -> str:
    """
    Format a success message for movement to a new location.
    
    Args:
        direction: The direction the player moved (e.g., 'north')
        location: The name of the destination location
        
    Returns:
        Formatted success message
    """
    return SUCCESS_MOVEMENT.format(direction=direction, location=location)


def format_success_look(location: str) -> str:
    """
    Format a success message for the look command.
    
    Args:
        location: The name of the current location
        
    Returns:
        Formatted success message
    """
    return SUCCESS_LOOK.format(location=location)


def format_error_invalid_direction(direction: str) -> str:
    """
    Format an error message for an invalid direction.
    
    Args:
        direction: The direction that was attempted
        
    Returns:
        Formatted error message
    """
    return ERROR_INVALID_DIRECTION.format(direction=direction)


def format_error_unrecognized_command(command: str) -> str:
    """
    Format an error message for an unrecognized command.
    
    Args:
        command: The command that was not recognized
        
    Returns:
        Formatted error message with help suggestion
    """
    error_msg = ERROR_UNRECOGNIZED_COMMAND.format(command=command)
    return f"{error_msg} {HELP_SUGGESTION}"


def get_help_text() -> str:
    """
    Get the help text showing available commands.
    
    Returns:
        Complete help text string
    """
    return HELP_TEXT


def format_empty_command_error() -> str:
    """
    Format an error message for empty command input.
    
    Returns:
        Error message for empty commands
    """
    return ERROR_EMPTY_COMMAND