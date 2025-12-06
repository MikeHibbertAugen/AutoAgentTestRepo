"""
Command processor module for text-based adventure game.

This module handles command parsing, validation, and normalization.
It provides functions to process user input, validate commands against
a registry, and normalize input for consistent handling.
"""

from typing import List, Tuple, Optional, Set


# Command registry - all valid commands the game recognizes
MOVEMENT_COMMANDS: Set[str] = {
    'north', 'south', 'east', 'west',
    'n', 's', 'e', 'w',
    'northeast', 'northwest', 'southeast', 'southwest',
    'ne', 'nw', 'se', 'sw',
    'up', 'down'
}

UTILITY_COMMANDS: Set[str] = {
    'help', 'look', 'inventory', 'quit', 'exit'
}

ALL_COMMANDS: Set[str] = MOVEMENT_COMMANDS | UTILITY_COMMANDS


def normalize_command(command: str) -> str:
    """
    Normalize a command string by trimming whitespace and converting to lowercase.
    
    Args:
        command: The raw command string from user input
        
    Returns:
        The normalized command string (trimmed and lowercase)
        
    Examples:
        >>> normalize_command("  NORTH  ")
        'north'
        >>> normalize_command("North")
        'north'
        >>> normalize_command("north")
        'north'
    """
    return command.strip().lower()


def parse_command(command: str) -> Tuple[str, List[str]]:
    """
    Parse a command string into the command verb and its arguments.
    
    Args:
        command: The command string to parse (should be normalized first)
        
    Returns:
        A tuple containing:
            - The command verb (str)
            - List of arguments (List[str])
            
    Examples:
        >>> parse_command("north")
        ('north', [])
        >>> parse_command("go north")
        ('go', ['north'])
        >>> parse_command("take red key")
        ('take', ['red', 'key'])
    """
    parts = command.split()
    
    if not parts:
        return ('', [])
    
    verb = parts[0]
    arguments = parts[1:] if len(parts) > 1 else []
    
    return (verb, arguments)


def is_valid_command(command: str) -> bool:
    """
    Check if a command is valid (exists in the command registry).
    
    Args:
        command: The command to validate (should be normalized first)
        
    Returns:
        True if the command is valid, False otherwise
        
    Examples:
        >>> is_valid_command("north")
        True
        >>> is_valid_command("dance")
        False
        >>> is_valid_command("help")
        True
    """
    return command in ALL_COMMANDS


def is_movement_command(command: str) -> bool:
    """
    Check if a command is a movement command.
    
    Args:
        command: The command to check (should be normalized first)
        
    Returns:
        True if the command is a movement command, False otherwise
        
    Examples:
        >>> is_movement_command("north")
        True
        >>> is_movement_command("help")
        False
    """
    return command in MOVEMENT_COMMANDS


def expand_direction(direction: str) -> str:
    """
    Expand abbreviated directions to their full form.
    
    Args:
        direction: The direction string (can be abbreviated)
        
    Returns:
        The full direction name
        
    Examples:
        >>> expand_direction("n")
        'north'
        >>> expand_direction("north")
        'north'
        >>> expand_direction("ne")
        'northeast'
    """
    direction_map = {
        'n': 'north',
        's': 'south',
        'e': 'east',
        'w': 'west',
        'ne': 'northeast',
        'nw': 'northwest',
        'se': 'southeast',
        'sw': 'southwest'
    }
    
    return direction_map.get(direction, direction)


def get_available_commands() -> List[str]:
    """
    Get a list of all available commands.
    
    Returns:
        A sorted list of all valid commands
    """
    return sorted(ALL_COMMANDS)


def get_movement_commands() -> List[str]:
    """
    Get a list of all available movement commands.
    
    Returns:
        A sorted list of all valid movement commands
    """
    return sorted(MOVEMENT_COMMANDS)


def get_utility_commands() -> List[str]:
    """
    Get a list of all available utility commands.
    
    Returns:
        A sorted list of all valid utility commands
    """
    return sorted(UTILITY_COMMANDS)