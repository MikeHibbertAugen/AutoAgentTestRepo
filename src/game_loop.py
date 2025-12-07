"""
Game loop module for the text adventure game.

This module implements the main game loop that handles command input,
processing, and game state management.
"""

from typing import Optional
from src.game_state import GameState


class GameLoop:
    """
    Main game loop that handles command processing and game flow.
    
    The game loop continuously accepts player commands, processes them,
    and updates the game state accordingly. It supports graceful exit
    through quit/exit commands or keyboard interrupt (Ctrl+C).
    """
    
    def __init__(self, game_state: GameState) -> None:
        """
        Initialize the game loop with game state.
        
        Args:
            game_state: The game state object to manage game data
        """
        self.game_state = game_state
    
    def display_location(self) -> None:
        """
        Display the current location description.
        
        Prints the description of the player's current location to the console.
        """
        location = self.game_state.get_current_location()
        if location:
            print(location)
    
    def display_farewell(self) -> None:
        """
        Display farewell message when exiting the game.
        
        Prints a goodbye message to the player when they exit the game.
        """
        print("Thanks for playing! Goodbye!")
    
    def process_command(self, command: str) -> bool:
        """
        Process a single command from the player.
        
        Args:
            command: The command string entered by the player
            
        Returns:
            bool: True if the game should continue, False if it should exit
        """
        # Strip whitespace and convert to lowercase for comparison
        command = command.strip().lower()
        
        # Check for exit commands
        if command in ('quit', 'exit'):
            return False
        
        # For now, just echo that we received the command
        # Future implementation will delegate to command handler
        if command:
            # Placeholder for command processing
            # Will be replaced with actual command handler
            pass
        
        return True
    
    def run(self) -> None:
        """
        Run the main game loop.
        
        This method:
        1. Starts the game state
        2. Displays the initial location
        3. Continuously reads and processes player commands
        4. Handles quit/exit commands and keyboard interrupts
        5. Displays farewell message on exit
        
        The loop continues until the player enters a quit/exit command
        or presses Ctrl+C.
        """
        try:
            # Start the game
            self.game_state.start()
            
            # Display initial location
            self.display_location()
            
            # Main game loop
            while self.game_state.is_running:
                try:
                    # Get command from player
                    command = input("> ")
                    
                    # Process the command
                    should_continue = self.process_command(command)
                    
                    # Check if we should exit
                    if not should_continue:
                        self.game_state.stop()
                        
                except EOFError:
                    # Handle end of input (e.g., piped input ending)
                    self.game_state.stop()
                    
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print()  # Print newline after ^C
            self.game_state.stop()
            
        finally:
            # Always display farewell message when exiting
            self.display_farewell()