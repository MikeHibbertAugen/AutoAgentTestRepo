"""Mathematical utility functions.

This module provides mathematical calculation functions, including
high-precision calculation of mathematical constants.
"""


def calculate_pi(iterations: int = 1000000) -> float:
    """Calculate Pi using the Machin formula for fast convergence.
    
    Uses Machin's formula: π/4 = 4*arctan(1/5) - arctan(1/239)
    The arctan function is calculated using the Taylor series expansion.
    
    This method provides faster convergence than the Leibniz formula,
    achieving 6 decimal place accuracy with fewer iterations.
    
    Args:
        iterations: Number of terms to use in the Taylor series expansion.
                   Default is 1000000 which provides accuracy to 6+ decimal places.
    
    Returns:
        float: The value of Pi accurate to at least 6 decimal places (3.141593).
    
    Examples:
        >>> pi = calculate_pi()
        >>> round(pi, 6)
        3.141593
        
        >>> # Using fewer iterations for faster (but less precise) calculation
        >>> pi_fast = calculate_pi(iterations=100000)
        >>> round(pi_fast, 6)
        3.141593
    
    Notes:
        - The function uses Machin's formula which converges much faster
          than the simple Leibniz formula
        - The result is deterministic and will always return the same value
          for the same number of iterations
        - Floating-point precision is limited by Python's float type (IEEE 754)
    """
    
    def arctan(x: float, num_terms: int) -> float:
        """Calculate arctan(x) using Taylor series expansion.
        
        Uses the series: arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ...
        
        Args:
            x: The value to calculate arctan for.
            num_terms: Number of terms to use in the series.
        
        Returns:
            float: The arctan(x) value.
        """
        result = 0.0
        x_squared = x * x
        x_power = x
        
        for n in range(num_terms):
            denominator = 2 * n + 1
            if n % 2 == 0:
                result += x_power / denominator
            else:
                result -= x_power / denominator
            x_power *= x_squared
            
            # Early termination if contribution becomes negligible
            if abs(x_power / denominator) < 1e-15:
                break
        
        return result
    
    # Machin's formula: π/4 = 4*arctan(1/5) - arctan(1/239)
    # These specific values are chosen because they converge very quickly
    pi_over_4 = 4 * arctan(1/5, iterations) - arctan(1/239, iterations)
    pi = 4 * pi_over_4
    
    return pi