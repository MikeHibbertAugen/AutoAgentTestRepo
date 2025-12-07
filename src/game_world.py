"""Game world manager for the text-based adventure game.

This module contains the GameWorld class which manages all locations
and their connections within the game world.
"""

from typing import Dict, Optional
from collections import deque
from src.location import Location


class GameWorld:
    """Manages the collection of locations and their connections in the game world.
    
    The GameWorld class is responsible for:
    - Storing and managing all game locations
    - Providing access to locations by name
    - Managing the starting location for the player
    - Creating bidirectional connections between locations
    - Verifying world connectivity through graph analysis
    
    Attributes:
        locations: Dictionary mapping location names to Location objects
        starting_location: The location where the player begins the game
    """
    
    def __init__(self) -> None:
        """Initialize an empty game world."""
        self.locations: Dict[str, Location] = {}
        self.starting_location: Optional[Location] = None
    
    def add_location(self, name: str, description: str, is_starting: bool = False) -> Location:
        """Add a location to the game world.
        
        Args:
            name: The name of the location
            description: The atmospheric description of the location
            is_starting: Whether this location is the starting location
            
        Returns:
            The created Location object
        """
        location = Location(name, description)
        self.locations[name] = location
        
        if is_starting:
            self.starting_location = location
        
        return location
    
    def get_location(self, name: str) -> Optional[Location]:
        """Retrieve a location by its name.
        
        Args:
            name: The name of the location to retrieve
            
        Returns:
            The Location object if found, None otherwise
        """
        return self.locations.get(name)
    
    def has_location(self, name: str) -> bool:
        """Check if a location exists in the game world.
        
        Args:
            name: The name of the location to check
            
        Returns:
            True if the location exists, False otherwise
        """
        return name in self.locations
    
    def set_starting_location(self, location: Location) -> None:
        """Set the starting location for the game.
        
        Args:
            location: The Location object to use as the starting point
        """
        self.starting_location = location
    
    def connect_locations(
        self, loc1_name: str, loc2_name: str, direction: str
    ) -> None:
        """Create a bidirectional connection between two locations.
        
        This method creates a two-way connection between locations, allowing
        navigation in both directions. For example, connecting location A to
        location B with direction "north" will allow traveling north from A to B,
        and automatically create a "south" connection from B to A.
        
        Args:
            loc1_name: The name of the first location
            loc2_name: The name of the second location
            direction: The direction from loc1 to loc2 (e.g., "north", "east")
            
        Raises:
            KeyError: If either location name is not found in the world
        """
        # Define opposite directions for bidirectional connections
        opposite_directions = {
            "north": "south",
            "south": "north",
            "east": "west",
            "west": "east",
            "northeast": "southwest",
            "southwest": "northeast",
            "northwest": "southeast",
            "southeast": "northwest",
        }
        
        loc1 = self.locations[loc1_name]
        loc2 = self.locations[loc2_name]
        
        # Create connection from loc1 to loc2
        loc1.add_exit(direction, loc2)
        
        # Create reverse connection from loc2 to loc1
        opposite = opposite_directions.get(direction)
        if opposite:
            loc2.add_exit(opposite, loc1)
    
    def count_locations(self) -> int:
        """Count the total number of locations in the game world.
        
        Returns:
            The number of locations in the world
        """
        return len(self.locations)
    
    def is_fully_connected(self) -> bool:
        """Verify that all locations are reachable from the starting location.
        
        Uses breadth-first search (BFS) to traverse the location graph starting
        from the starting location. A fully connected world means every location
        can be reached by following connections from the starting point.
        
        Returns:
            True if all locations are reachable from the starting location,
            False if the world is empty, has no starting location, or has
            unreachable locations
        """
        # Cannot be connected if empty or no starting location
        if not self.locations or self.starting_location is None:
            return False
        
        # BFS to find all reachable locations
        visited = set()
        queue = deque([self.starting_location])
        visited.add(self.starting_location.name)
        
        while queue:
            current = queue.popleft()
            
            # Visit all connected locations
            for next_location in current.exits.values():
                if next_location.name not in visited:
                    visited.add(next_location.name)
                    queue.append(next_location)
        
        # World is fully connected if all locations were visited
        return len(visited) == len(self.locations)