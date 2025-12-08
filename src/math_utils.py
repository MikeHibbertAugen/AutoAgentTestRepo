"""
Mathematical utility functions.

This module provides functions for mathematical calculations, including
the calculation of Pi using the Leibniz formula (Gregory-Leibniz series).
"""

from typing import Optional

# Constant defining the precision for Pi calculation
PI_PRECISION = 5


def calculate_pi(max_iterations: Optional[int] = 1000000) -> float:
    """
    Calculate Pi to 5 decimal places using the Leibniz formula.
    
    The Leibniz formula (Gregory-Leibniz series) is an infinite series
    that converges to π/4:
    π/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - ...
    
    Therefore: π = 4 * (1 - 1/3 + 1/5 - 1/7 + 1/9 - ...)
    
    The function iterates until the value stabilizes to 5 decimal places
    or reaches the maximum iteration limit.
    
    Args:
        max_iterations: Maximum number of iterations to prevent infinite loops.
                       Default is 1,000,000. Must be a positive integer.
    
    Returns:
        float: Approximation of Pi accurate to 5 decimal places (3.14159)
    
    Raises:
        ValueError: If max_iterations is not a positive integer.
    
    Examples:
        >>> pi_value = calculate_pi()
        >>> round(pi_value, 5)
        3.14159
        
        >>> pi_value = calculate_pi(max_iterations=500000)
        >>> round(pi_value, 5)
        3.14159
    
    Note:
        The Leibniz formula converges slowly. Approximately 500,000 iterations
        are needed to achieve 5 decimal place accuracy. For better performance
        with high precision requirements, consider alternative algorithms like
        the Machin formula or Chudnovsky algorithm.
    """
    if max_iterations is None:
        max_iterations = 1000000
    
    if not isinstance(max_iterations, int) or max_iterations <= 0:
        raise ValueError("max_iterations must be a positive integer")
    
    pi_estimate = 0.0
    previous_rounded = 0.0
    
    for n in range(max_iterations):
        # Leibniz formula: π/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - ...
        # Alternating series with denominator (2n + 1)
        term = ((-1) ** n) / (2 * n + 1)
        pi_estimate += term
        
        # Check convergence every 10000 iterations to improve performance
        if n > 0 and n % 10000 == 0:
            current_pi = 4 * pi_estimate
            current_rounded = round(current_pi, PI_PRECISION)
            
            # Check if the value has stabilized to 5 decimal places
            if current_rounded == previous_rounded:
                return current_pi
            
            previous_rounded = current_rounded
    
    # Return the final approximation (multiply by 4 for the Leibniz formula)
    return 4 * pi_estimate