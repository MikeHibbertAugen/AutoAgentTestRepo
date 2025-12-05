"""
Nelson Time package for fetching current date and time in Nelson, New Zealand.

This package provides utilities to fetch the current time in Nelson (New Zealand)
using the WorldTimeAPI service. Nelson uses the Pacific/Auckland timezone.
"""

from src.nelson_time import get_current_time
from src.string_utils import reverse_string, capitalize_string

__version__ = "0.1.0"
__all__ = ["get_current_time", "reverse_string", "capitalize_string"]