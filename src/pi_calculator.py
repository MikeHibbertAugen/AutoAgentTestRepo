"""Pi calculator module using Machin's formula.

This module provides functionality to calculate Pi to 11 decimal places
using Machin's formula: π/4 = 4*arctan(1/5) - arctan(1/239)
"""

PI_PRECISION = 11


def _calculate_arctan(x: float, terms: int) -> float:
    """Calculate arctan(x) using Taylor series expansion.
    
    Uses the Taylor series: arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ...
    
    Args:
        x: The value to calculate arctan for (should be between -1 and 1 for fast convergence)
        terms: The number of terms to calculate in the series
        
    Returns:
        The arctangent of x as a float
        
    Note:
        More terms provide higher precision. For Machin's formula with
        x=1/5 and x=1/239, sufficient terms ensure 11 decimal place accuracy.
    """
    result = 0.0
    x_squared = x * x
    x_power = x
    
    for n in range(terms):
        denominator = 2 * n + 1
        if n % 2 == 0:
            result += x_power / denominator
        else:
            result -= x_power / denominator
        x_power *= x_squared
    
    return result


def calculate_pi() -> float:
    """Calculate Pi to 11 decimal places using Machin's formula.
    
    Uses Machin's formula: π/4 = 4*arctan(1/5) - arctan(1/239)
    
    This formula was discovered by John Machin in 1706 and is known for
    its rapid convergence, making it efficient for calculating Pi to high
    precision.
    
    Returns:
        Pi calculated to 11 decimal places (3.14159265359)
        
    Examples:
        >>> pi = calculate_pi()
        >>> f"{pi:.11f}"
        '3.14159265359'
        
        >>> pi_value = calculate_pi()
        >>> abs(pi_value - 3.14159265359) < 1e-11
        True
    """
    # Calculate sufficient terms for 11 decimal place accuracy
    # For 1/5, we need more terms than for 1/239 due to slower convergence
    terms_for_fifth = 20
    terms_for_239th = 10
    
    # Apply Machin's formula: π/4 = 4*arctan(1/5) - arctan(1/239)
    arctan_fifth = _calculate_arctan(1.0 / 5.0, terms_for_fifth)
    arctan_239th = _calculate_arctan(1.0 / 239.0, terms_for_239th)
    
    pi_over_four = 4.0 * arctan_fifth - arctan_239th
    pi = 4.0 * pi_over_four
    
    return pi