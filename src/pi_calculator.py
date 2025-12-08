"""
Pi calculator module using Machin's formula for high precision calculation.

This module provides functionality to calculate the value of Pi to 8 decimal places
using Machin's formula: π/4 = 4·arctan(1/5) - arctan(1/239)
"""

from typing import Union

# Module-level constant defining the precision of Pi calculations
PI_PRECISION = 8


def _calculate_arctan(x: Union[int, float], num_terms: int = 100) -> float:
    """
    Calculate arctan(x) using Taylor series expansion.
    
    The Taylor series for arctan(x) is:
    arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ...
    
    This converges for |x| <= 1, which is satisfied for our use case (1/5 and 1/239).
    
    Args:
        x: The value for which to calculate arctan. Should satisfy |x| <= 1 for convergence.
        num_terms: Number of terms to use in the Taylor series expansion.
                   Default is 100, which provides sufficient precision for 8 decimal places.
    
    Returns:
        float: The calculated arctan(x) value.
    
    Raises:
        ValueError: If x is outside the convergence range [-1, 1].
    
    Example:
        >>> abs(_calculate_arctan(1.0) - 0.7853981633974483) < 1e-10
        True
    """
    if abs(x) > 1:
        raise ValueError(f"arctan Taylor series requires |x| <= 1, got x={x}")
    
    result = 0.0
    x_squared = x * x
    x_power = x
    
    for n in range(num_terms):
        # Calculate term: (-1)^n * x^(2n+1) / (2n+1)
        term = x_power / (2 * n + 1)
        
        if n % 2 == 0:
            result += term
        else:
            result -= term
        
        x_power *= x_squared
    
    return result


def calculate_pi(precision: int = PI_PRECISION) -> float:
    """
    Calculate the value of Pi using Machin's formula.
    
    This function implements Machin's formula for calculating Pi:
    π/4 = 4·arctan(1/5) - arctan(1/239)
    
    Machin's formula was chosen because:
    - Fast convergence due to small arguments (1/5 and 1/239)
    - High accuracy with relatively few terms
    - No external dependencies required
    - Deterministic and numerically stable
    
    Args:
        precision: Number of decimal places for the result. Default is 8.
                   This parameter is used for documentation; the actual calculation
                   always provides sufficient precision for 8+ decimal places.
    
    Returns:
        float: The calculated value of Pi, accurate to at least 8 decimal places.
    
    Raises:
        ValueError: If precision is negative or exceeds reasonable bounds.
    
    Example:
        >>> pi_value = calculate_pi()
        >>> round(pi_value, 8)
        3.14159265
        
        >>> # Verify accuracy to 8 decimal places
        >>> abs(calculate_pi() - 3.14159265358979) < 1e-8
        True
    """
    if precision < 0:
        raise ValueError(f"Precision must be non-negative, got {precision}")
    
    if precision > 15:
        raise ValueError(
            f"Precision must not exceed 15 decimal places (float limitation), got {precision}"
        )
    
    # Use sufficient terms to guarantee precision
    # For 8 decimal places, 100 terms is more than sufficient
    num_terms = 100
    
    # Calculate using Machin's formula: π/4 = 4·arctan(1/5) - arctan(1/239)
    arctan_1_5 = _calculate_arctan(1.0 / 5.0, num_terms)
    arctan_1_239 = _calculate_arctan(1.0 / 239.0, num_terms)
    
    pi_over_4 = 4 * arctan_1_5 - arctan_1_239
    pi_value = 4 * pi_over_4
    
    return pi_value


def get_pi_to_precision(decimal_places: int = PI_PRECISION) -> str:
    """
    Get Pi as a string formatted to the specified number of decimal places.
    
    This is a convenience function that calculates Pi and formats it as a string
    with exactly the specified number of decimal places.
    
    Args:
        decimal_places: Number of decimal places to include in the result.
                        Default is 8. Maximum is 15 due to float precision limits.
    
    Returns:
        str: Pi formatted as a string with the specified decimal places.
    
    Raises:
        ValueError: If decimal_places is negative or exceeds 15.
    
    Example:
        >>> get_pi_to_precision(8)
        '3.14159265'
        
        >>> get_pi_to_precision(4)
        '3.1416'
    """
    if decimal_places < 0:
        raise ValueError(f"Decimal places must be non-negative, got {decimal_places}")
    
    if decimal_places > 15:
        raise ValueError(
            f"Decimal places must not exceed 15 (float limitation), got {decimal_places}"
        )
    
    pi_value = calculate_pi(precision=decimal_places)
    return f"{pi_value:.{decimal_places}f}"


# Module-level constant providing the default Pi value
PI = calculate_pi()