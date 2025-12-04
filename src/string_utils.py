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


def capitalize_string(input_str: str) -> str:
    """
    Capitalize the first character of the given string.
    
    Converts the first character to uppercase and all remaining characters
    to lowercase. Handles edge cases such as empty strings, strings with
    leading whitespace, and strings containing numbers or special characters.
    
    Args:
        input_str: The string to capitalize
        
    Returns:
        The capitalized string with the first character in uppercase and
        the rest in lowercase
        
    Raises:
        TypeError: If input is not a string
        
    Examples:
        >>> capitalize_string("hello")
        'Hello'
        >>> capitalize_string("HELLO")
        'Hello'
        >>> capitalize_string("hello world")
        'Hello world'
        >>> capitalize_string("")
        ''
        >>> capitalize_string("123abc")
        '123abc'
        >>> capitalize_string("  hello")
        '  hello'
    """
    if not isinstance(input_str, str):
        raise TypeError(
            f"Input must be a string, got {type(input_str).__name__}"
        )
    
    return input_str.capitalize()