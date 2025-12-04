"""
String operations utility module.

This module provides utility functions for string manipulation.
"""

from typing import Any


def reverse_string(input_string: str) -> str:
    """
    Reverse a string.
    
    This function takes a string as input and returns a new string with
    the characters in reverse order. It handles Unicode characters correctly
    and validates input types.
    
    Args:
        input_string (str): The string to reverse
        
    Returns:
        str: The reversed string
        
    Raises:
        TypeError: If input is not a string
        
    Examples:
        >>> reverse_string("hello")
        'olleh'
        >>> reverse_string("Hello World")
        'dlroW olleH'
        >>> reverse_string("")
        ''
        >>> reverse_string("Python 3.11")
        '11.3 nohtyP'
        >>> reverse_string("Hello 👋 World")
        'dlroW 👋 olleH'
    """
    if not isinstance(input_string, str):
        raise TypeError(
            f"Input must be a string, got {type(input_string).__name__}"
        )
    
    return input_string[::-1]


__all__ = ["reverse_string"]