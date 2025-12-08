"""Mathematical utility functions.

This module provides high-precision mathematical calculations, including
Pi calculation using the Chudnovsky algorithm.
"""

from decimal import Decimal, getcontext
from typing import Decimal as DecimalType


def calculate_pi() -> Decimal:
    """Calculate Pi to at least 12 decimal places using the Chudnovsky algorithm.
    
    The Chudnovsky algorithm is one of the fastest known algorithms for computing
    Pi. It converges extremely rapidly, requiring only a few iterations to achieve
    high precision.
    
    The algorithm uses the following formula:
    1/π = 12 * Σ((-1)^k * (6k)! * (545140134k + 13591409)) / ((3k)! * (k!)^3 * 640320^(3k + 3/2))
    
    Returns:
        Decimal: The value of Pi accurate to at least 12 decimal places.
        
    Examples:
        >>> from decimal import Decimal
        >>> pi = calculate_pi()
        >>> str(pi)[:14]
        '3.141592653589'
        >>> isinstance(pi, Decimal)
        True
        
    References:
        Chudnovsky, D. V., & Chudnovsky, G. V. (1989).
        "The Computation of Classical Constants"
    """
    # Set precision high enough to ensure accuracy at 12 decimal places
    getcontext().prec = 50
    
    # Constants for the Chudnovsky algorithm
    C = 426880 * Decimal(10005).sqrt()
    K = Decimal(6)
    M = Decimal(1)
    X = Decimal(1)
    L = Decimal(13591409)
    S = Decimal(13591409)
    
    # Number of iterations needed for 12+ decimal places (1-2 iterations sufficient)
    # We use 3 to ensure accuracy with margin
    for i in range(1, 3):
        M = M * (K ** 3 - 16 * K) / ((i) ** 3)
        K += 12
        L += 545140134
        X *= -262537412640768000
        S += Decimal(M * L) / X
    
    # Calculate Pi
    pi = C / S
    
    return pi


def get_pi_string(decimal_places: int = 12) -> str:
    """Get Pi as a string formatted to the specified number of decimal places.
    
    This is a convenience function that calculates Pi and formats it as a string
    with the requested precision.
    
    Args:
        decimal_places: Number of decimal places to include (default: 12).
        
    Returns:
        str: Pi formatted as a string with the specified decimal places.
        
    Examples:
        >>> get_pi_string(5)
        '3.14159'
        >>> get_pi_string(10)
        '3.1415926535'
        
    Raises:
        ValueError: If decimal_places is negative or greater than 12.
    """
    if decimal_places < 0:
        raise ValueError("decimal_places must be non-negative")
    if decimal_places > 12:
        raise ValueError("This implementation guarantees accuracy only up to 12 decimal places")
    
    pi = calculate_pi()
    
    # Format to the requested number of decimal places
    format_string = f"{{:.{decimal_places}f}}"
    return format_string.format(pi)