"""
Command parser module for text-based adventure game.

This module provides command parsing functionality to interpret user input
and convert it into structured command objects.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CommandType(Enum):
    """Enumeration of valid command types in the game."""
    MOVE = "move"
    LOOK = "look"
    HELP = "help"
    QUIT = "quit"
    INVALID = "invalid"


@dataclass
class ParsedCommand:
    """
    Represents a parsed command from user input.
    
    Attributes:
        type: The type of command (MOVE, LOOK, HELP, QUIT, INVALID)
        direction: The direction for movement commands (north, south, east, west)
        raw_input: The original user input string
    """
    type: CommandType
    direction: Optional[str] = None
    raw_input: str = ""


class CommandParser:
    """
    Parser for game commands.
    
    Handles parsing of movement commands (full and abbreviated),
    look, help, quit commands, and invalid input.
    """
    
    # Valid directions for movement commands
    VALID_DIRECTIONS = {"north", "south", "east", "west"}
    
    # Mapping of abbreviated directions to full names
    DIRECTION_ABBREVIATIONS = {
        "n": "north",
        "s": "south",
        "e": "east",
        "w": "west"
    }
    
    def parse(self, command: str) -> ParsedCommand:
        """
        Parse a command string into a structured ParsedCommand object.
        
        Args:
            command: The user input string to parse
            
        Returns:
            ParsedCommand object with the parsed command information
        """
        # Store original input for reference
        raw_input = command
        
        # Normalize input: strip whitespace and convert to lowercase
        command = command.strip().lower()
        
        # Handle empty input
        if not command:
            return ParsedCommand(
                type=CommandType.INVALID,
                raw_input=raw_input
            )
        
        # Try to parse as movement command
        direction = self._parse_movement(command)
        if direction:
            return ParsedCommand(
                type=CommandType.MOVE,
                direction=direction,
                raw_input=raw_input
            )
        
        # Check for abbreviated direction commands
        direction = self._is_abbreviated_direction(command)
        if direction:
            return ParsedCommand(
                type=CommandType.MOVE,
                direction=direction,
                raw_input=raw_input
            )
        
        # Check for single-word commands
        if command == "look":
            return ParsedCommand(
                type=CommandType.LOOK,
                raw_input=raw_input
            )
        
        if command == "help":
            return ParsedCommand(
                type=CommandType.HELP,
                raw_input=raw_input
            )
        
        if command == "quit":
            return ParsedCommand(
                type=CommandType.QUIT,
                raw_input=raw_input
            )
        
        # Command not recognized
        return ParsedCommand(
            type=CommandType.INVALID,
            raw_input=raw_input
        )
    
    def _parse_movement(self, command: str) -> Optional[str]:
        """
        Parse movement commands in the format "go <direction>".
        
        Args:
            command: The normalized command string
            
        Returns:
            The direction if valid movement command, None otherwise
        """
        # Check if command starts with "go "
        if not command.startswith("go "):
            return None
        
        # Extract the direction part
        parts = command.split(maxsplit=1)
        if len(parts) != 2:
            return None
        
        direction = parts[1].strip()
        
        # Validate the direction
        if direction in self.VALID_DIRECTIONS:
            return direction
        
        return None
    
    def _is_abbreviated_direction(self, command: str) -> Optional[str]:
        """
        Check if command is an abbreviated direction (n, s, e, w).
        
        Args:
            command: The normalized command string
            
        Returns:
            The full direction name if valid abbreviation, None otherwise
        """
        if command in self.DIRECTION_ABBREVIATIONS:
            return self.DIRECTION_ABBREVIATIONS[command]
        
        return None