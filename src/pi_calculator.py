"""
Pi calculator module using the Machin-like formula for high precision calculation.

This module provides functionality to calculate Pi to 13 decimal places using
the Machin formula: π/4 = 4·arctan(1/5) - arctan(1/239)
"""

from decimal import Decimal, getcontext
from typing import Optional


# Constants
TARGET_PRECISION = 13
DECIMAL_PLACES = 50  # Internal precision for intermediate calculations
DEFAULT_ARCTAN_TERMS = 100


def calculate_pi(precision: Optional[int] = None) -> Decimal:
    """
    Calculate Pi to the specified number of decimal places using Machin's formula.
    
    The formula used is: π/4 = 4·arctan(1/5) - arctan(1/239)
    
    This formula converges rapidly and is well-suited for calculating Pi to
    moderate precision (up to ~50 decimal places efficiently).
    
    Args:
        precision: Number of decimal places to calculate. Defaults to 13.
                  Must be a positive integer.
    
    Returns:
        Decimal: Pi calculated to the specified precision.
    
    Raises:
        ValueError: If precision is not a positive integer.
    
    Examples:
        >>> from src.pi_calculator import calculate_pi
        >>> pi = calculate_pi()
        >>> print(f"{pi:.13f}")
        3.1415926535897
        
        >>> pi = calculate_pi(precision=5)
        >>> print(f"{pi:.5f}")
        3.14159
    """
    if precision is None:
        precision = TARGET_PRECISION
    
    if not isinstance(precision, int) or precision <= 0:
        raise ValueError("Precision must be a positive integer")
    
    # Set internal precision higher than target to ensure accuracy
    internal_precision = max(precision + 10, DECIMAL_PLACES)
    getcontext().prec = internal_precision
    
    # Calculate number of terms needed for convergence
    num_terms = _calculate_terms_needed(precision)
    
    # Apply Machin's formula: π/4 = 4·arctan(1/5) - arctan(1/239)
    one = Decimal(1)
    five = Decimal(5)
    two_three_nine = Decimal(239)
    four = Decimal(4)
    
    arctan_1_5 = _arctan_series(one / five, num_terms)
    arctan_1_239 = _arctan_series(one / two_three_nine, num_terms)
    
    pi_over_4 = four * arctan_1_5 - arctan_1_239
    pi = four * pi_over_4
    
    # Round to the requested precision
    getcontext().prec = precision + 5
    result = +pi  # Unary plus to apply current precision
    
    return result


def _arctan_series(x: Decimal, num_terms: int) -> Decimal:
    """
    Calculate arctan(x) using Taylor series expansion.
    
    The Taylor series for arctan(x) is:
    arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + x⁹/9 - ...
    
    This converges for |x| ≤ 1.
    
    Args:
        x: The value to calculate arctan for (must be Decimal type).
        num_terms: Number of terms to calculate in the series.
    
    Returns:
        Decimal: The calculated arctan(x) value.
    
    Note:
        This is a private helper function and should not be called directly
        outside of this module.
    """
    getcontext().prec = DECIMAL_PLACES
    
    power = x
    result = power
    x_squared = x * x
    
    for n in range(1, num_terms):
        power *= -x_squared
        denominator = Decimal(2 * n + 1)
        term = power / denominator
        result += term
        
        # Early termination if term becomes negligible
        if abs(term) < Decimal(10) ** -(DECIMAL_PLACES - 5):
            break
    
    return result


def _calculate_terms_needed(precision: int) -> int:
    """
    Calculate the number of terms needed in the Taylor series for desired precision.
    
    This provides a conservative estimate to ensure convergence to the
    requested number of decimal places.
    
    Args:
        precision: Target number of decimal places.
    
    Returns:
        int: Number of terms to calculate in the arctan series.
    
    Note:
        This is a private helper function. The formula used provides a
        conservative estimate that ensures sufficient accuracy while
        maintaining reasonable performance.
    """
    # Conservative estimate: more terms for higher precision
    # For Machin's formula with arctan(1/5) and arctan(1/239),
    # convergence is rapid. This formula ensures sufficient terms.
    base_terms = 50
    additional_terms = max(0, (precision - 10) * 5)
    return base_terms + additional_terms