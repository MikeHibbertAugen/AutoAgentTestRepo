"""Counter module implementing a configurable counter with start and end values.

This module provides a Counter class that maintains an integer value with configurable
start and end boundaries, supporting increment, reset, and boundary checking operations.
"""


class Counter:
    """A counter with configurable start and end values.

    The counter maintains an internal value that starts at a configurable position
    and can be incremented up to a configurable end value. The counter can be reset
    to its starting value and provides boundary checking capabilities.

    Attributes:
        start (int): The starting value of the counter.
        end (int): The maximum value the counter can reach.
        current (int): The current value of the counter.

    Raises:
        ValueError: If start is greater than end during initialization.
        ValueError: If attempting to increment beyond the end value.

    Example:
        >>> counter = Counter(start=1, end=10)
        >>> counter.current
        1
        >>> counter.increment()
        >>> counter.current
        2
        >>> counter.reset()
        >>> counter.current
        1
    """

    def __init__(self, start: int = 1, end: int = 10) -> None:
        """Initialize the counter with start and end values.

        Args:
            start: The starting value of the counter. Defaults to 1.
            end: The maximum value the counter can reach. Defaults to 10.

        Raises:
            ValueError: If start is greater than end.
        """
        if start > end:
            raise ValueError(f"Start value ({start}) cannot be greater than end value ({end})")
        
        self.start = start
        self.end = end
        self.current = start

    def increment(self) -> None:
        """Increment the counter by 1.

        Raises:
            ValueError: If the counter has already reached the end value.

        Example:
            >>> counter = Counter(start=1, end=5)
            >>> counter.increment()
            >>> counter.current
            2
        """
        if self.current >= self.end:
            raise ValueError(f"Cannot increment beyond end value ({self.end})")
        self.current += 1

    def reset(self) -> None:
        """Reset the counter to its starting value.

        Example:
            >>> counter = Counter(start=5, end=10)
            >>> counter.increment()
            >>> counter.current
            6
            >>> counter.reset()
            >>> counter.current
            5
        """
        self.current = self.start

    def has_reached_end(self) -> bool:
        """Check if the counter has reached its end value.

        Returns:
            bool: True if the current value equals the end value, False otherwise.

        Example:
            >>> counter = Counter(start=1, end=3)
            >>> counter.has_reached_end()
            False
            >>> counter.increment()
            >>> counter.increment()
            >>> counter.has_reached_end()
            True
        """
        return self.current == self.end