"""Counter module providing a simple counter class with increment functionality.

This module implements a Counter class that maintains a numeric counter value,
starting at 1 and allowing increments up to a maximum value of 10.
"""

from typing import Final


class Counter:
    """A simple counter class that starts at 1 and can be incremented.
    
    The counter maintains an internal value that starts at 1 and can be
    incremented by one at a time. The counter has a maximum value of 10.
    
    Attributes:
        MAX_VALUE: Class constant defining the maximum counter value (10).
    """
    
    MAX_VALUE: Final[int] = 10
    
    def __init__(self) -> None:
        """Initialize a new Counter instance with starting value of 1."""
        self._value: int = 1
    
    def increment(self) -> None:
        """Increment the counter value by 1.
        
        Increases the internal counter value by exactly one unit.
        """
        self._value += 1
    
    def get_value(self) -> int:
        """Retrieve the current counter value.
        
        Returns:
            The current integer value of the counter.
        """
        return self._value