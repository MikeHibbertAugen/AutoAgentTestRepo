"""Counter module implementing a basic counter with configurable range and boundary validation.

This module provides a Counter class that maintains an integer value with configurable
start and end values, with proper boundary validation and exception handling.
"""


class Counter:
    """A counter with configurable start and end values that can be incremented within bounds.

    The counter maintains an internal value that starts at a specified initial value
    and can be incremented up to a maximum value. Attempting to increment beyond the
    maximum raises a ValueError.

    Attributes:
        _start (int): The initial/reset value of the counter.
        _end (int): The maximum value the counter can reach.
        _current (int): The current counter value.

    Args:
        start (int): Starting value for the counter. Defaults to 1.
        end (int): Maximum value for the counter. Defaults to 10.

    Examples:
        >>> counter = Counter()
        >>> counter.get_current()
        1
        >>> counter.increment()
        >>> counter.get_current()
        2
        >>> counter.reset()
        >>> counter.get_current()
        1
    """

    def __init__(self, start: int = 1, end: int = 10) -> None:
        """Initialize the counter with specified start and end values.

        Args:
            start: The initial value for the counter. Defaults to 1.
            end: The maximum value for the counter. Defaults to 10.
        """
        self._start: int = start
        self._end: int = end
        self._current: int = start

    def increment(self) -> None:
        """Increment the counter by 1.

        Raises:
            ValueError: If the counter is already at the maximum value and cannot
                       be incremented further.
        """
        if self._current >= self._end:
            raise ValueError(
                f"Cannot increment counter beyond maximum value of {self._end}"
            )
        self._current += 1

    def get_current(self) -> int:
        """Get the current value of the counter.

        Returns:
            int: The current counter value.
        """
        return self._current

    def reset(self) -> None:
        """Reset the counter to its initial start value."""
        self._current = self._start

    def has_reached_end(self) -> bool:
        """Check if the counter has reached its maximum value.

        Returns:
            bool: True if the counter is at the maximum value, False otherwise.
        """
        return self._current == self._end

    @property
    def start(self) -> int:
        """Get the start value of the counter.

        Returns:
            int: The initial/reset value of the counter.
        """
        return self._start

    @property
    def end(self) -> int:
        """Get the end value of the counter.

        Returns:
            int: The maximum value of the counter.
        """
        return self._end

    @property
    def current(self) -> int:
        """Get the current value of the counter.

        Returns:
            int: The current counter value.
        """
        return self._current