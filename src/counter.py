"""Counter module implementing a basic counter with maximum value constraint.

This module provides a Counter class that maintains an integer value starting at 1
and can be incremented up to a maximum value of 10.
"""

from typing import Optional


class Counter:
    """A counter that starts at 1 and can be incremented up to a maximum value of 10.

    The counter maintains an internal value that can be incremented and retrieved.
    Once the counter reaches the maximum value, further increment attempts will
    not change the value and will return a message indicating the limit has been reached.

    Attributes:
        MAX_VALUE (int): Class constant defining the maximum counter value (10).
        _value (int): Private attribute storing the current counter value.
    """

    MAX_VALUE: int = 10

    def __init__(self) -> None:
        """Initialize the counter with a starting value of 1."""
        self._value: int = 1

    def increment(self) -> Optional[str]:
        """Increment the counter by 1 if it hasn't reached the maximum value.

        The counter will only increment if the current value is less than MAX_VALUE.
        If the counter is already at MAX_VALUE, no change occurs and a message is
        returned indicating the counter has reached its limit.

        Returns:
            Optional[str]: None if the counter was successfully incremented, or a
                          message string if the counter is already at MAX_VALUE and
                          could not be incremented.
        """
        if self._value < self.MAX_VALUE:
            self._value += 1
            return None
        return "Counter has reached maximum value"

    def get_value(self) -> int:
        """Get the current value of the counter.

        Returns:
            int: The current counter value.
        """
        return self._value