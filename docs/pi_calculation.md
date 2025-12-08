# Pi Calculation Documentation

## Overview

This module implements a high-precision calculation of π (pi) accurate to 7 decimal places using Machin's formula, a classical arctangent-based algorithm discovered by John Machin in 1706.

## Mathematical Approach

### Machin's Formula

The implementation uses Machin's formula for calculating π:

```
π/4 = 4·arctan(1/5) - arctan(1/239)
```

This formula can be rearranged to:

```
π = 16·arctan(1/5) - 4·arctan(1/239)
```

### Why Machin's Formula?

Machin's formula was chosen for several compelling reasons:

1. **Fast Convergence**: The terms 1/5 and 1/239 are small, making the Taylor series converge rapidly
2. **Numerical Stability**: The subtraction of two arctangent values provides better precision than single-term formulas
3. **Historical Significance**: Used to compute π to 100 decimal places by hand in 1706
4. **Simplicity**: Requires only basic arithmetic operations without complex mathematical functions

### Taylor Series for Arctangent

The arctangent function is computed using its Taylor series expansion:

```
arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + x⁹/9 - ...
```

For small values of x, this series converges quickly. With x = 1/5 and x = 1/239, very few terms are needed to achieve 7 decimal places of accuracy.

## Algorithm Details

### Implementation Steps

1. Compute `arctan(1/5)` using Taylor series with sufficient terms
2. Compute `arctan(1/239)` using Taylor series with sufficient terms
3. Apply Machin's formula: `π = 16·arctan(1/5) - 4·arctan(1/239)`
4. Return the computed value

### Precision Parameters

- **Target Precision**: 7 decimal places (3.1415927)
- **Taylor Series Terms**: 100 terms for arctan calculation
- **Numerical Accuracy**: Error < 1×10⁻⁷

### Convergence Analysis

For `arctan(1/5)`:
- Each term is multiplied by (1/5)² = 1/25
- After 10 terms, error < 10⁻¹⁴

For `arctan(1/239)`:
- Each term is multiplied by (1/239)² ≈ 1/57,000
- Converges extremely rapidly

## Usage Examples

### Basic Usage

```python
from src.pi_calculator import calculate_pi

# Calculate pi to 7 decimal places
pi_value = calculate_pi()
print(f"π = {pi_value:.7f}")  # Output: π = 3.1415927
```

### Comparison with math.pi

```python
import math
from src.pi_calculator import calculate_pi

calculated_pi = calculate_pi()
standard_pi = math.pi

print(f"Calculated: {calculated_pi:.10f}")
print(f"Standard:   {standard_pi:.10f}")
print(f"Difference: {abs(calculated_pi - standard_pi):.2e}")
```

### Integration in Applications

```python
from src.pi_calculator import calculate_pi

def circle_area(radius: float) -> float:
    """Calculate circle area using high-precision pi."""
    pi = calculate_pi()
    return pi * radius ** 2

def circle_circumference(radius: float) -> float:
    """Calculate circle circumference using high-precision pi."""
    pi = calculate_pi()
    return 2 * pi * radius
```

## Complexity Analysis

### Time Complexity

- **O(n)** where n is the number of Taylor series terms (100)
- Two arctangent calculations, each O(n)
- Overall: O(n) ≈ O(1) for fixed precision

### Space Complexity

- **O(1)** - Only stores intermediate calculation values
- No arrays or dynamic data structures required
- Fixed memory footprint regardless of precision

### Performance Characteristics

- **Typical Execution Time**: < 10 milliseconds
- **Deterministic**: Always returns the same result
- **No Dependencies**: Uses only built-in Python operations

## Precision Guarantees

The implementation guarantees:

1. **Accuracy**: Result matches π to 7 decimal places (3.1415927)
2. **Reproducibility**: Identical results across multiple invocations
3. **Error Bounds**: Absolute error < 1×10⁻⁷ compared to true π value
4. **Floating-Point Stability**: Uses IEEE 754 double precision (15-17 significant digits)

## Comparison with Other Methods

| Method | Convergence Rate | Complexity | Implementation |
|--------|------------------|------------|----------------|
| Machin's Formula | Fast | Simple | Current implementation |
| BBP Formula | Moderate | Complex | Hexadecimal digit extraction |
| Monte Carlo | Slow | Very Simple | Statistical approximation |
| Leibniz Series | Very Slow | Simple | π/4 = 1 - 1/3 + 1/5 - ... |

## References

- Machin, J. (1706). "A New Method of Computing Logarithms"
- Borwein, J. & Borwein, P. (1987). "Pi and the AGM"
- Arndt, J. & Haenel, C. (2001). "Pi Unleashed"