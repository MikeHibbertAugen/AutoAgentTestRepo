"""
World and Location management for the text-based adventure game.

This module provides classes for managing game locations and the overall
game world structure, including location connections and navigation.
"""

from typing import Dict, Optional


class Location:
    """
    Represents a single location in the game world.
    
    A location has a name and a set of exits leading to other locations.
    Exits are stored as a dictionary mapping direction names to destination
    location names.
    """
    
    def __init__(self, name: str):
        """
        Initialize a new location.
        
        Args:
            name: The name of this location
        """
        self.name = name
        self.exits: Dict[str, str] = {}
    
    def add_exit(self, direction: str, destination: str) -> None:
        """
        Add an exit from this location.
        
        Args:
            direction: The direction of the exit (e.g., "north", "south")
            destination: The name of the destination location
        """
        self.exits[direction] = destination
    
    def has_exit(self, direction: str) -> bool:
        """
        Check if an exit exists in the given direction.
        
        Args:
            direction: The direction to check
            
        Returns:
            True if an exit exists in that direction, False otherwise
        """
        return direction in self.exits
    
    def get_destination(self, direction: str) -> Optional[str]:
        """
        Get the destination location for a given direction.
        
        Args:
            direction: The direction to check
            
        Returns:
            The name of the destination location, or None if no exit exists
        """
        return self.exits.get(direction)


class World:
    """
    Manages all locations in the game world.
    
    The World class maintains a collection of locations and provides
    methods for retrieving locations and setting up connections between them.
    """
    
    STARTING_LOCATION = "Helensville"
    
    def __init__(self):
        """Initialize a new game world with an empty set of locations."""
        self.locations: Dict[str, Location] = {}
    
    def add_location(self, name: str) -> Location:
        """
        Add a new location to the world.
        
        Args:
            name: The name of the location to add
            
        Returns:
            The newly created Location object
        """
        location = Location(name)
        self.locations[name] = location
        return location
    
    def get_location(self, name: str) -> Optional[Location]:
        """
        Retrieve a location by name.
        
        Args:
            name: The name of the location to retrieve
            
        Returns:
            The Location object, or None if not found
        """
        return self.locations.get(name)
    
    def connect_locations(self, from_location: str, direction: str, 
                         to_location: str) -> None:
        """
        Create a one-way connection between two locations.
        
        Args:
            from_location: The name of the starting location
            direction: The direction of travel
            to_location: The name of the destination location
        """
        location = self.get_location(from_location)
        if location:
            location.add_exit(direction, to_location)