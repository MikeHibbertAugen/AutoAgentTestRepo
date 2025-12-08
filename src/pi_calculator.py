"""
Pi Calculator Module

This module provides a high-precision implementation for calculating Pi
to 12 decimal places using Machin's formula.
"""

from decimal import Decimal, getcontext
from typing import Union


# Module-level constant for Pi precision
PI_PRECISION = 12


def _arctan(x: Union[Decimal, int], num_terms: int = 100) -> Decimal:
    """
    Calculate arctangent using Taylor series expansion.

    The Taylor series for arctan(x) is:
    arctan(x) = x - x^3/3 + x^5/5 - x^7/7 + ...

    Args:
        x: The value to calculate arctangent for (should be |x| <= 1 for convergence)
        num_terms: Number of terms to use in the series expansion (default: 100)

    Returns:
        Decimal: The arctangent of x with high precision
    """
    x = Decimal(x)
    power = x
    result = power
    
    for n in range(1, num_terms):
        power *= -x * x
        result += power / (2 * n + 1)
    
    return result


def calculate_pi(precision: int = PI_PRECISION) -> str:
    """
    Calculate Pi to the specified number of decimal places using Machin's formula.

    This implementation uses Machin's formula:
    π/4 = 4*arctan(1/5) - arctan(1/239)

    Machin's formula was discovered by John Machin in 1706 and provides
    fast convergence for calculating Pi with high precision.

    Args:
        precision: Number of decimal places to return (default: 12)

    Returns:
        str: Pi as a string formatted to the specified number of decimal places

    Example:
        >>> pi_value = calculate_pi()
        >>> print(pi_value)
        3.141592653589

        >>> pi_15 = calculate_pi(precision=15)
        >>> print(pi_15)
        3.141592653589793
    """
    # Set decimal precision higher than required output to ensure accuracy
    getcontext().prec = precision + 10
    
    # Machin's formula: π/4 = 4*arctan(1/5) - arctan(1/239)
    one = Decimal(1)
    five = Decimal(5)
    two_three_nine = Decimal(239)
    
    # Calculate the two arctangent terms
    arctan_1_5 = _arctan(one / five, num_terms=150)
    arctan_1_239 = _arctan(one / two_three_nine, num_terms=150)
    
    # Apply Machin's formula
    pi_over_4 = 4 * arctan_1_5 - arctan_1_239
    pi_value = 4 * pi_over_4
    
    # Format to the specified precision
    format_string = f"{{:.{precision}f}}"
    return format_string.format(pi_value)


def get_pi() -> str:
    """
    Convenience function to get Pi to 12 decimal places.

    Returns:
        str: Pi as a string formatted to 12 decimal places

    Example:
        >>> from pi_calculator import get_pi
        >>> print(get_pi())
        3.141592653589
    """
    return calculate_pi(PI_PRECISION)


if __name__ == "__main__":
    # Demonstration when module is run directly
    print(f"Pi to {PI_PRECISION} decimal places: {calculate_pi()}")
    print(f"Pi to 15 decimal places: {calculate_pi(15)}")
    print(f"Pi to 20 decimal places: {calculate_pi(20)}")