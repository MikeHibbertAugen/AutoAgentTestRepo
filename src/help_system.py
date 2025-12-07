"""Help system module for the text-based game.

This module provides the HelpSystem class which manages and displays help text,
including available commands and welcome messages for players.
"""

from typing import Dict, List


class HelpSystem:
    """Manages help text and guidance for game players.
    
    The HelpSystem class provides methods to generate formatted help text
    showing available commands, including movement and utility commands,
    and displays welcome messages at game start.
    """
    
    def __init__(self) -> None:
        """Initialize the HelpSystem with command information."""
        self.movement_commands: Dict[str, str] = {
            "north (n)": "Move north",
            "south (s)": "Move south",
            "east (e)": "Move east",
            "west (w)": "Move west"
        }
        
        self.utility_commands: Dict[str, str] = {
            "look": "Look around the current location",
            "help": "Display this help message",
            "quit": "Exit the game"
        }
    
    def get_help_text(self) -> str:
        """Generate and return formatted help text.
        
        Returns:
            str: Formatted string containing all available commands with descriptions.
        """
        help_lines: List[str] = []
        help_lines.append("=" * 50)
        help_lines.append("AVAILABLE COMMANDS")
        help_lines.append("=" * 50)
        help_lines.append("")
        
        help_lines.append("Movement Commands:")
        help_lines.append("-" * 50)
        for command, description in self.movement_commands.items():
            help_lines.append(f"  {command:<15} - {description}")
        help_lines.append("")
        
        help_lines.append("Utility Commands:")
        help_lines.append("-" * 50)
        for command, description in self.utility_commands.items():
            help_lines.append(f"  {command:<15} - {description}")
        help_lines.append("")
        
        help_lines.append("=" * 50)
        
        return "\n".join(help_lines)
    
    def get_welcome_message(self) -> str:
        """Generate and return the welcome message for game start.
        
        Returns:
            str: Formatted welcome message with instructions to access help.
        """
        welcome_lines: List[str] = []
        welcome_lines.append("=" * 50)
        welcome_lines.append("Welcome to the Text Adventure Game!")
        welcome_lines.append("=" * 50)
        welcome_lines.append("")
        welcome_lines.append("You find yourself at the beginning of an adventure.")
        welcome_lines.append("Type 'help' at any time to see available commands.")
        welcome_lines.append("")
        
        return "\n".join(welcome_lines)