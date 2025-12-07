"""Core game world location model for text-based adventure game.

This module provides the Location class for representing navigable locations
in a text-based adventure game set in north-west Auckland.
"""

from typing import Dict, List, Optional


class Location:
    """Represents a location in the game world with name, description, and exits.

    A location is a place in the game world that the player can visit. Each
    location has a name, an optional description, and a collection of exits
    that connect it to other locations.

    Attributes:
        name: The name of the location (e.g., "Taupaki Village").
        description: A textual description of the location.

    Example:
        >>> village = Location("Taupaki Village", "A quiet rural village")
        >>> forest = Location("Kumeu Forest")
        >>> village.add_exit("north", forest)
        >>> village.get_available_exits()
        ['north']
        >>> village.get_exit("north") == forest
        True
    """

    def __init__(self, name: str, description: str = "") -> None:
        """Initialize a new location.

        Args:
            name: The name of the location. Must be a non-empty string.
            description: Optional description of the location. Defaults to empty string.

        Raises:
            ValueError: If name is empty or not a string.
        """
        if not isinstance(name, str) or not name:
            raise ValueError("Location name must be a non-empty string")

        self._name = name
        self._description = description
        self._exits: Dict[str, Location] = {}

    @property
    def name(self) -> str:
        """Get the name of the location.

        Returns:
            The location's name.
        """
        return self._name

    @property
    def description(self) -> str:
        """Get the description of the location.

        Returns:
            The location's description.
        """
        return self._description

    def add_exit(self, direction: str, destination: "Location") -> None:
        """Add an exit from this location to another location.

        Creates a one-way connection from this location to the destination
        location in the specified direction. If an exit already exists in
        that direction, it will be overwritten.

        Args:
            direction: The direction of the exit (e.g., "north", "south").
            destination: The Location object that this exit leads to.

        Raises:
            ValueError: If direction is empty or destination is not a Location.

        Example:
            >>> village = Location("Village")
            >>> forest = Location("Forest")
            >>> village.add_exit("north", forest)
        """
        if not isinstance(direction, str) or not direction:
            raise ValueError("Direction must be a non-empty string")

        if not isinstance(destination, Location):
            raise ValueError("Destination must be a Location instance")

        self._exits[direction] = destination

    def get_exit(self, direction: str) -> Optional["Location"]:
        """Get the destination location for a given direction.

        Args:
            direction: The direction to query (e.g., "north", "south").

        Returns:
            The Location object in that direction, or None if no exit exists.

        Example:
            >>> village = Location("Village")
            >>> forest = Location("Forest")
            >>> village.add_exit("north", forest)
            >>> village.get_exit("north") == forest
            True
            >>> village.get_exit("south") is None
            True
        """
        return self._exits.get(direction)

    def has_exit(self, direction: str) -> bool:
        """Check if an exit exists in the given direction.

        Args:
            direction: The direction to check (e.g., "north", "south").

        Returns:
            True if an exit exists in that direction, False otherwise.

        Example:
            >>> village = Location("Village")
            >>> forest = Location("Forest")
            >>> village.add_exit("north", forest)
            >>> village.has_exit("north")
            True
            >>> village.has_exit("south")
            False
        """
        return direction in self._exits

    def get_available_exits(self) -> List[str]:
        """Get a list of all available exit directions from this location.

        Returns:
            A list of direction strings for all exits from this location.
            Returns an empty list if there are no exits.

        Example:
            >>> village = Location("Village")
            >>> village.get_available_exits()
            []
            >>> village.add_exit("north", Location("Forest"))
            >>> village.add_exit("east", Location("River"))
            >>> sorted(village.get_available_exits())
            ['east', 'north']
        """
        return list(self._exits.keys())

    def __repr__(self) -> str:
        """Return a string representation of the location.

        Returns:
            A string representation suitable for debugging.
        """
        return f"Location(name='{self._name}', exits={list(self._exits.keys())})"

    def __str__(self) -> str:
        """Return a human-readable string representation of the location.

        Returns:
            The location's name.
        """
        return self._name