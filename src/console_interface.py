"""Console interface module for handling user input and output in the text adventure game.

This module provides the ConsoleInterface class that manages the display of prompts,
reading user input, and coordinating with the command parser to process commands.
"""

from typing import Optional
from command_parser import CommandParser, ParsedCommand


class ConsoleInterface:
    """Handles console I/O operations and user interaction for the game.
    
    This class is responsible for displaying prompts, reading user input,
    and coordinating with the CommandParser to process commands. It provides
    a clean separation between I/O handling and command parsing logic.
    
    Attributes:
        parser: CommandParser instance used to parse user commands.
    """
    
    def __init__(self, parser: CommandParser) -> None:
        """Initialize the console interface with a command parser.
        
        Args:
            parser: CommandParser instance for parsing user commands.
        """
        self.parser = parser
    
    def display_prompt(self, location: str) -> None:
        """Display the command prompt with the current location.
        
        The prompt format is: [Location Name] > 
        For example: [Helensville] > 
        
        Args:
            location: The name of the current location to display in the prompt.
        """
        print(f"[{location}] > ", end="", flush=True)
    
    def get_input(self) -> str:
        """Read user input from the console.
        
        Returns:
            The user's input as a string, with leading/trailing whitespace stripped.
        """
        return input().strip()
    
    def process_command(self, command_str: str, location: str) -> ParsedCommand:
        """Process a command string and return the parsed result.
        
        This method takes a command string, parses it using the command parser,
        and returns the resulting ParsedCommand object. It handles empty input
        gracefully by returning an invalid command without displaying an error.
        
        Args:
            command_str: The command string to process.
            location: The current location (for context, currently unused).
        
        Returns:
            ParsedCommand object containing the parsed command information.
        """
        # Handle empty input gracefully - don't show error, just return invalid command
        if not command_str:
            return self.parser.parse(command_str)
        
        # Parse the command
        parsed_command = self.parser.parse(command_str)
        
        return parsed_command
    
    def display_error(self, message: str) -> None:
        """Display an error message to the user.
        
        Args:
            message: The error message to display.
        """
        print(f"Error: {message}")