"""
String utility functions for text manipulation.

This module provides utilities for common string operations with proper
input validation and security considerations.
"""

import re
from typing import Optional


# Maximum string length to prevent DoS attacks (10MB)
MAX_STRING_LENGTH = 10 * 1024 * 1024


def capitalize_words(text: Optional[str]) -> str:
    """
    Capitalize the first letter of each word in a string.
    
    This function takes an input string and capitalizes the first letter of
    each word while preserving the original spacing and punctuation. Words
    are identified by whitespace boundaries.
    
    Args:
        text: The input string to capitalize. Can be None or empty.
        
    Returns:
        A new string with the first letter of each word capitalized.
        Returns empty string if input is None or empty.
        
    Raises:
        TypeError: If input is not a string or None.
        ValueError: If input string exceeds maximum allowed length.
        
    Examples:
        >>> capitalize_words("hello world")
        'Hello World'
        >>> capitalize_words("hello  world")
        'Hello  World'
        >>> capitalize_words("don't stop")
        "Don't Stop"
        >>> capitalize_words("")
        ''
        >>> capitalize_words(None)
        ''
        
    Security Notes:
        - Input length is limited to prevent DoS attacks
        - Control characters are preserved but not interpreted
        - No dynamic code execution or eval usage
        - Input is not logged to prevent sensitive data exposure
    """
    # Handle None and empty string cases
    if text is None:
        return ""
    
    # Type validation to prevent injection
    if not isinstance(text, str):
        raise TypeError(f"Expected string or None, got {type(text).__name__}")
    
    # Handle empty string
    if not text:
        return ""
    
    # Length validation to prevent DoS
    if len(text) > MAX_STRING_LENGTH:
        raise ValueError(
            f"Input string exceeds maximum length of {MAX_STRING_LENGTH} characters"
        )
    
    # Sanitize control characters (except common whitespace: space, tab, newline, carriage return)
    # This prevents potential injection attacks while preserving normal formatting
    sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    
    # Split into words while preserving whitespace
    # Use a pattern that captures both words and whitespace
    parts = re.split(r'(\s+)', sanitized)
    
    # Capitalize the first letter of each non-whitespace part
    result_parts = []
    for part in parts:
        if part and not part.isspace():
            # Capitalize first character if it's a letter
            if part[0].isalpha():
                result_parts.append(part[0].upper() + part[1:])
            else:
                # Handle words starting with punctuation or numbers
                # Find first letter and capitalize it
                capitalized = False
                chars = list(part)
                for i, char in enumerate(chars):
                    if char.isalpha():
                        chars[i] = char.upper()
                        capitalized = True
                        break
                result_parts.append(''.join(chars))
        else:
            # Preserve whitespace as-is
            result_parts.append(part)
    
    return ''.join(result_parts)


def _sanitize_input(text: str) -> str:
    """
    Internal helper to sanitize string input.
    
    Removes potentially dangerous control characters while preserving
    normal whitespace and printable characters.
    
    Args:
        text: The string to sanitize.
        
    Returns:
        Sanitized string with control characters removed.
    """
    # Remove control characters except tab, newline, and carriage return
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)


def _validate_string_input(text: Optional[str], max_length: int = MAX_STRING_LENGTH) -> None:
    """
    Internal helper to validate string input.
    
    Args:
        text: The string to validate.
        max_length: Maximum allowed string length.
        
    Raises:
        TypeError: If input is not a string or None.
        ValueError: If input exceeds maximum length.
    """
    if text is None:
        return
    
    if not isinstance(text, str):
        raise TypeError(f"Expected string or None, got {type(text).__name__}")
    
    if len(text) > max_length:
        raise ValueError(
            f"Input string exceeds maximum length of {max_length} characters"
        )