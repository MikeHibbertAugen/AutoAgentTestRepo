"""
Game State Module

This module manages the game state including the running status and current location.
"""

from typing import Optional


class GameState:
    """
    Manages the state of the game including running status and location tracking.
    
    Attributes:
        _is_running (bool): Flag indicating if the game loop is active
        _current_location (str): Description of the current location
        _initialized (bool): Flag indicating if the game has been initialized
    """
    
    def __init__(self) -> None:
        """
        Initialize game state with default values.
        
        The game starts in a stopped state and must be explicitly started.
        """
        self._is_running: bool = False
        self._current_location: str = "You are standing at the entrance of a dark cave."
        self._initialized: bool = False
    
    def start(self) -> None:
        """
        Set the game to running state.
        
        This method should be called when the game loop begins execution.
        """
        self._is_running = True
        self._initialized = True
    
    def stop(self) -> None:
        """
        Set the game to stopped state.
        
        This method should be called when the game loop should terminate.
        """
        self._is_running = False
    
    @property
    def is_running(self) -> bool:
        """
        Get the current running status of the game.
        
        Returns:
            bool: True if the game is running, False otherwise
        """
        return self._is_running
    
    @property
    def is_initialized(self) -> bool:
        """
        Get the initialization status of the game.
        
        Returns:
            bool: True if the game has been initialized, False otherwise
        """
        return self._initialized
    
    def get_current_location(self) -> str:
        """
        Get the description of the current location.
        
        Returns:
            str: The current location description
        """
        return self._current_location
    
    def set_current_location(self, location: str) -> None:
        """
        Update the current location.
        
        Args:
            location (str): The new location description
            
        Raises:
            ValueError: If location is None or empty string
        """
        if not location:
            raise ValueError("Location cannot be None or empty")
        self._current_location = location