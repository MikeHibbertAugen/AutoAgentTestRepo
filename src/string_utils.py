"""String utility functions for text manipulation."""

from typing import Any


def reverse_string(input_str: str) -> str:
    """
    Reverse the given string.
    
    Args:
        input_str: The string to reverse
        
    Returns:
        The reversed string
        
    Raises:
        TypeError: If input is not a string
        
    Examples:
        >>> reverse_string("hello")
        'olleh'
        >>> reverse_string("")
        ''
        >>> reverse_string("a")
        'a'
    """
    if not isinstance(input_str, str):
        raise TypeError(
            f"Input must be a string, got {type(input_str).__name__}"
        )
    
    return input_str[::-1]