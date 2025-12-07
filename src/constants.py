"""
Constants for the text-based adventure game movement system.

This module defines cardinal directions, abbreviation mappings, and standard
messages used throughout the movement system.
"""

from typing import Dict

# Cardinal directions
NORTH = "north"
SOUTH = "south"
EAST = "east"
WEST = "west"

# Direction abbreviation mappings
DIRECTION_ABBREVIATIONS: Dict[str, str] = {
    "n": NORTH,
    "s": SOUTH,
    "e": EAST,
    "w": WEST,
}

# All valid directions (full names)
VALID_DIRECTIONS = [NORTH, SOUTH, EAST, WEST]

# Success message templates
SUCCESS_MESSAGE_TEMPLATE = "You move {direction} to {location}."

# Error message templates
INVALID_DIRECTION_MESSAGE = "You cannot go that way."
NO_EXIT_MESSAGE = "You cannot go that way."