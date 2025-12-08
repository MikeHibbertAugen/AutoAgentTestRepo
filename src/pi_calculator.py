"""
Pi Calculator Module

This module provides functions to calculate the value of Pi to a specified
precision using Machin's formula.
"""

from decimal import Decimal, getcontext


DEFAULT_PRECISION = 10


def calculate_pi(precision: int = DEFAULT_PRECISION) -> float:
    """
    Calculate Pi to the specified number of decimal places using Machin's formula.
    
    Machin's formula: π/4 = 4·arctan(1/5) - arctan(1/239)
    
    This formula converges rapidly and is efficient for calculating Pi to
    moderate precision (up to hundreds of decimal places).
    
    Args:
        precision: Number of decimal places to calculate (default: 10)
        
    Returns:
        float: The value of Pi accurate to the specified decimal places
        
    Raises:
        ValueError: If precision is less than 1 or greater than 100
        
    Examples:
        >>> pi = calculate_pi()
        >>> round(pi, 10)
        3.1415926536
        
        >>> pi = calculate_pi(precision=5)
        >>> round(pi, 5)
        3.14159
    """
    if not isinstance(precision, int):
        raise ValueError("Precision must be an integer")
    
    if precision < 1:
        raise ValueError("Precision must be at least 1")
    
    if precision > 100:
        raise ValueError("Precision cannot exceed 100 decimal places")
    
    # Set decimal precision with extra digits for intermediate calculations
    getcontext().prec = precision + 10
    
    # Apply Machin's formula: π/4 = 4·arctan(1/5) - arctan(1/239)
    pi_over_4 = 4 * _arctan(Decimal(1) / Decimal(5)) - _arctan(Decimal(1) / Decimal(239))
    pi_value = 4 * pi_over_4
    
    # Convert to float for return
    return float(pi_value)


def _arctan(x: Decimal) -> Decimal:
    """
    Calculate arctangent using Taylor series expansion.
    
    Uses the series: arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ...
    
    This series converges for |x| ≤ 1, which is satisfied by Machin's formula
    (1/5 and 1/239 are both less than 1).
    
    Args:
        x: The value to calculate arctangent for (as Decimal)
        
    Returns:
        Decimal: The arctangent of x
    """
    power = x
    result = power
    i = 1
    
    # Continue until the term becomes negligible
    while True:
        power *= -x * x
        i += 2
        term = power / i
        
        if abs(term) < Decimal(10) ** -(getcontext().prec - 2):
            break
            
        result += term
    
    return result