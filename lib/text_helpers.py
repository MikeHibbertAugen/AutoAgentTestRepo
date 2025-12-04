"""
Text manipulation helper functions.

This module provides utility functions for text processing with security
considerations and proper input validation.
"""

import re
from typing import Optional


# Maximum string length to prevent DoS attacks (10MB)
MAX_STRING_LENGTH = 10 * 1024 * 1024


class StringValidationError(ValueError):
    """Raised when string validation fails."""
    pass


def capitalize_words(text: Optional[str]) -> str:
    """
    Capitalize the first letter of each word in a string.
    
    This function capitalizes the first character of each word while preserving
    the original spacing and structure of the input string. It handles Unicode
    characters properly and includes security safeguards against malicious input.
    
    Args:
        text: The input string to process. Can be None (returns empty string).
    
    Returns:
        A new string with the first letter of each word capitalized.
        Returns empty string for None or empty input.
    
    Raises:
        StringValidationError: If input exceeds maximum length or contains
                              invalid null bytes.
        TypeError: If input is not a string or None.
    
    Security Considerations:
        - Input length is limited to prevent DoS attacks
        - Null byte injection is prevented
        - No dynamic code execution is used
        - Control characters are preserved but not interpreted
    
    Examples:
        >>> capitalize_words("hello world")
        'Hello World'
        >>> capitalize_words("hello  world")
        'Hello  World'
        >>> capitalize_words("don't stop")
        "Don't Stop"
        >>> capitalize_words("café naïve")
        'Café Naïve'
        >>> capitalize_words("")
        ''
        >>> capitalize_words(None)
        ''
    """
    # Handle None input
    if text is None:
        return ""
    
    # Type validation
    if not isinstance(text, str):
        raise TypeError(f"Expected string or None, got {type(text).__name__}")
    
    # Handle empty string
    if not text:
        return ""
    
    # Security: Check maximum length to prevent DoS
    if len(text) > MAX_STRING_LENGTH:
        raise StringValidationError(
            f"String length exceeds maximum allowed length of {MAX_STRING_LENGTH} bytes"
        )
    
    # Security: Prevent null byte injection
    if '\x00' in text:
        raise StringValidationError("String contains null bytes")
    
    # Process the string character by character to preserve all spacing
    result = []
    # Track if we're at the start of a new word
    capitalize_next = True
    
    for char in text:
        if char.isspace():
            # Preserve all whitespace characters
            result.append(char)
            # Next non-space character should be capitalized
            capitalize_next = True
        elif char.isalpha():
            # Capitalize if we're at the start of a word
            if capitalize_next:
                result.append(char.upper())
                capitalize_next = False
            else:
                result.append(char.lower())
        else:
            # Handle punctuation, numbers, and other characters
            # These don't reset the word boundary for cases like "don't"
            result.append(char)
            # Only reset capitalize_next for certain punctuation
            # that typically ends a word (not apostrophes)
            if char in '.,;:!?-—–':
                capitalize_next = True
    
    return ''.join(result)


def sanitize_control_characters(text: str, replace_with: str = ' ') -> str:
    """
    Remove or replace control characters from text.
    
    This is a helper function for cases where control characters need to be
    sanitized before processing.
    
    Args:
        text: The input string to sanitize.
        replace_with: Character to replace control characters with (default: space).
    
    Returns:
        Sanitized string with control characters replaced.
    
    Examples:
        >>> sanitize_control_characters("hello\x07world")
        'hello world'
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected string, got {type(text).__name__}")
    
    # Replace control characters (except newline, tab, carriage return)
    # with the replacement character
    return re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', replace_with, text)