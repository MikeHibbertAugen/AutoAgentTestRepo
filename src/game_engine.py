"""
Game Engine Module

This module contains the core game engine that manages game state, processes player commands,
and coordinates game flow for the text-based adventure game.
"""

from typing import Optional, Dict, Any
from src.help_system import HelpSystem


class GameEngine:
    """
    Main game engine class that manages game state and command processing.
    
    Attributes:
        current_location (str): The player's current location in the game world.
        help_system (HelpSystem): The help system for displaying command information.
        running (bool): Flag indicating whether the game is currently running.
    """
    
    def __init__(self):
        """Initialize the game engine with default state."""
        self.current_location = "start"
        self.help_system = HelpSystem()
        self.running = False
        self.locations = {
            "start": {
                "description": "You are at the starting location.",
                "north": "room1",
                "south": None,
                "east": None,
                "west": None
            },
            "room1": {
                "description": "You are in room 1.",
                "north": None,
                "south": "start",
                "east": "room2",
                "west": None
            },
            "room2": {
                "description": "You are in room 2.",
                "north": None,
                "south": None,
                "east": None,
                "west": "room1"
            }
        }
    
    def display_welcome(self) -> str:
        """
        Display the welcome message at game start.
        
        Returns:
            str: The welcome message to be displayed.
        """
        return self.help_system.get_welcome_message()
    
    def start(self) -> None:
        """Start the game and display welcome message."""
        self.running = True
        print(self.display_welcome())
        self.look()
    
    def process_command(self, command: str) -> Optional[str]:
        """
        Process a player command and execute the corresponding action.
        
        Args:
            command (str): The command entered by the player.
            
        Returns:
            Optional[str]: Response message or None if command is invalid.
        """
        command = command.strip().lower()
        
        if not command:
            return None
        
        # Handle help command
        if command == "help":
            return self.help_system.get_help_text()
        
        # Handle quit command
        if command == "quit":
            self.running = False
            return "Thanks for playing! Goodbye!"
        
        # Handle look command
        if command == "look":
            return self.look()
        
        # Handle movement commands
        direction_map = {
            "n": "north",
            "s": "south",
            "e": "east",
            "w": "west",
            "north": "north",
            "south": "south",
            "east": "east",
            "west": "west"
        }
        
        if command in direction_map:
            direction = direction_map[command]
            return self.move(direction)
        
        return f"I don't understand '{command}'. Type 'help' for available commands."
    
    def move(self, direction: str) -> str:
        """
        Move the player in the specified direction.
        
        Args:
            direction (str): The direction to move (north, south, east, west).
            
        Returns:
            str: Message describing the result of the movement.
        """
        current = self.locations.get(self.current_location)
        
        if not current:
            return "Error: Invalid location."
        
        next_location = current.get(direction)
        
        if next_location is None:
            return f"You cannot go {direction} from here."
        
        self.current_location = next_location
        return self.look()
    
    def look(self) -> str:
        """
        Get the description of the current location.
        
        Returns:
            str: Description of the current location.
        """
        current = self.locations.get(self.current_location)
        
        if not current:
            return "You are in an unknown location."
        
        return current.get("description", "You see nothing special.")
    
    def get_current_location(self) -> str:
        """
        Get the player's current location.
        
        Returns:
            str: The current location identifier.
        """
        return self.current_location
    
    def is_running(self) -> bool:
        """
        Check if the game is currently running.
        
        Returns:
            bool: True if the game is running, False otherwise.
        """
        return self.running