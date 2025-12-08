"""Module for calculating Pi to high precision using Machin's formula.

This module provides a function to calculate Pi to 9 decimal places using
Machin's formula: π/4 = 4·arctan(1/5) - arctan(1/239)

The implementation uses Python's decimal module for arbitrary precision
arithmetic to ensure accuracy.
"""

from decimal import Decimal, getcontext
from typing import Union


def _arctan(x: Decimal, precision: int) -> Decimal:
    """Calculate arctangent using Taylor series expansion.
    
    Uses the series: arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ...
    
    Args:
        x: The value to calculate arctangent for (as Decimal)
        precision: Number of decimal places for precision
        
    Returns:
        Decimal: The arctangent of x
    """
    getcontext().prec = precision + 10  # Extra precision for intermediate calculations
    
    power = x
    result = power
    i = 1
    
    # Continue until terms become negligibly small
    while True:
        power *= -x * x
        term = power / (2 * i + 1)
        if abs(term) < Decimal(10) ** -(precision + 5):
            break
        result += term
        i += 1
    
    return result


def calculate_pi() -> float:
    """Calculate Pi to 9 decimal places using Machin's formula.
    
    This function implements Machin's formula for calculating Pi:
    π/4 = 4·arctan(1/5) - arctan(1/239)
    
    The formula is particularly efficient for high-precision calculations
    because the arctangent series converges rapidly for small arguments.
    
    Returns:
        float: Pi calculated to 9 decimal places (3.141592654)
        
    Examples:
        >>> pi = calculate_pi()
        >>> print(f"{pi:.9f}")
        3.141592654
        
        >>> pi == calculate_pi()  # Consistent results
        True
    """
    # Set precision high enough to ensure 9 accurate decimal places
    precision = 50
    getcontext().prec = precision
    
    # Convert to Decimal for high precision arithmetic
    one = Decimal(1)
    five = Decimal(5)
    two_three_nine = Decimal(239)
    four = Decimal(4)
    
    # Calculate using Machin's formula: π/4 = 4·arctan(1/5) - arctan(1/239)
    arctan_1_5 = _arctan(one / five, precision)
    arctan_1_239 = _arctan(one / two_three_nine, precision)
    
    # π/4 = 4·arctan(1/5) - arctan(1/239)
    pi_over_4 = four * arctan_1_5 - arctan_1_239
    
    # Multiply by 4 to get π
    pi_decimal = pi_over_4 * four
    
    # Convert to float and round to 9 decimal places
    pi_float = float(pi_decimal)
    
    return round(pi_float, 9)