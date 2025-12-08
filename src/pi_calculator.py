"""Pi calculator module.

This module provides a function to calculate the mathematical constant Pi
to exactly 13 decimal places using Machin's formula for high precision.
"""

from decimal import Decimal, getcontext


def calculate_pi() -> Decimal:
    """Calculate Pi to exactly 13 decimal places.
    
    This function uses Machin's formula for calculating Pi with high precision:
    π/4 = 4*arctan(1/5) - arctan(1/239)
    
    The implementation uses Python's decimal module for arbitrary precision
    arithmetic to ensure accurate calculation and rounding to exactly 13
    decimal places.
    
    Returns:
        Decimal: The value of Pi as 3.1415926535897
        
    Example:
        >>> pi = calculate_pi()
        >>> print(pi)
        3.1415926535897
        >>> str(pi)
        '3.1415926535897'
    """
    # Set precision high enough for accurate calculation
    # Need extra precision for intermediate calculations
    getcontext().prec = 50
    
    def arctan(x: Decimal, num_terms: int = 100) -> Decimal:
        """Calculate arctan(x) using Taylor series expansion.
        
        arctan(x) = x - x^3/3 + x^5/5 - x^7/7 + ...
        
        Args:
            x: The value to calculate arctan for
            num_terms: Number of terms in the Taylor series (default: 100)
            
        Returns:
            Decimal: The arctan(x) value
        """
        result = Decimal(0)
        x_squared = x * x
        x_power = x
        
        for n in range(num_terms):
            denominator = 2 * n + 1
            term = x_power / denominator
            
            if n % 2 == 0:
                result += term
            else:
                result -= term
            
            x_power *= x_squared
            
            # Early termination if term becomes negligibly small
            if abs(term) < Decimal(10) ** -50:
                break
                
        return result
    
    # Machin's formula: π/4 = 4*arctan(1/5) - arctan(1/239)
    one = Decimal(1)
    five = Decimal(5)
    two_three_nine = Decimal(239)
    four = Decimal(4)
    
    # Calculate the two arctan terms
    arctan_term1 = arctan(one / five)
    arctan_term2 = arctan(one / two_three_nine)
    
    # Apply Machin's formula
    pi_over_4 = four * arctan_term1 - arctan_term2
    pi_value = four * pi_over_4
    
    # Round to exactly 13 decimal places
    result = pi_value.quantize(Decimal('0.0000000000001'))
    
    return result