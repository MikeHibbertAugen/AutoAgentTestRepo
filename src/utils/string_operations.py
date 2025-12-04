"""
String operations utility module.

This module provides utility functions for common string manipulation tasks.
"""

from typing import Any


def reverse_string(input_string: str) -> str:
    """
    Reverse a string.
    
    Takes an input string and returns a new string with all characters
    in reverse order. Handles Unicode characters, special characters,
    and all standard string content correctly.
    
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
        >>> reverse_string("a")
        'a'
        >>> reverse_string("12345")
        '54321'
        >>> reverse_string("Hello 👋 World")
        'dlroW 👋 olleH'
    """
    if not isinstance(input_string, str):
        raise TypeError(
            f"Input must be a string, got {type(input_string).__name__}"
        )
    
    return input_string[::-1]