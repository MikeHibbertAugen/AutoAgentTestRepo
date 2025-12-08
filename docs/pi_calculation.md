# Pi Calculation Documentation

## Overview

This module provides a high-precision implementation of Pi calculation accurate to 13 decimal places using the Machin-like formula. The implementation uses Python's `decimal` module to ensure arbitrary precision arithmetic.

## Mathematical Background

### Machin's Formula

The calculator uses Machin's formula, discovered by John Machin in 1706:

```
π/4 = 4·arctan(1/5) - arctan(1/239)
```

This formula is particularly efficient because:
- The arguments (1/5 and 1/239) are small, leading to fast convergence
- It requires fewer terms in the Taylor series compared to other formulas
- It has been historically used to calculate Pi to millions of digits

### Taylor Series for Arctan

The arctan function is calculated using its Taylor series expansion:

```
arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + x⁹/9 - ...
```

For small values of x (like 1/5 and 1/239), this series converges rapidly, requiring relatively few terms to achieve high precision.

## Usage

### Basic Usage

```python
from decimal import Decimal
from src.pi_calculator import calculate_pi

# Calculate Pi to 13 decimal places
pi = calculate_pi()
print(pi)  # Output: 3.1415926535897
```

### Type Information

The function returns a `Decimal` type for maximum precision:

```python
pi = calculate_pi()
assert isinstance(pi, Decimal)
print(type(pi))  # <class 'decimal.Decimal'>
```

### Using in Calculations

```python
from decimal import Decimal

pi = calculate_pi()

# Calculate circle area
radius = Decimal('5.0')
area = pi * radius ** 2
print(f"Circle area: {area}")

# Calculate circle circumference
circumference = 2 * pi * radius
print(f"Circle circumference: {circumference}")
```

## Performance Characteristics

- **Computation Time**: Typically completes in less than 1 millisecond
- **Precision**: Accurate to 13 decimal places (3.1415926535897)
- **Internal Precision**: Uses 50 decimal places internally to ensure accurate rounding
- **Memory Usage**: Minimal, uses only standard library components
- **Deterministic**: Always produces identical results

## Implementation Details

### Precision Settings

The module uses the following precision settings:

- **Target Precision**: 13 decimal places for the final result
- **Internal Precision**: 50 decimal places to maintain accuracy through calculations
- **Term Count**: Dynamically calculated based on required precision (typically 30-50 terms)

### Error Handling

The implementation is designed to be robust:

- No user input is required, eliminating input validation concerns
- Pure mathematical computation with no I/O operations
- Uses only Python standard library for maximum compatibility

## Algorithm Complexity

- **Time Complexity**: O(n) where n is the number of terms in the Taylor series
- **Space Complexity**: O(1) constant space for storing intermediate results

## References

1. Machin, J. (1706). "A formula for calculating π"
2. Weisstein, Eric W. "Machin's Formula." From MathWorld--A Wolfram Web Resource.
3. Python Documentation: decimal — Decimal fixed point and floating point arithmetic

## Testing

Comprehensive unit tests are available in `tests/test_pi_calculator.py`. Run tests with:

```bash
pytest tests/test_pi_calculator.py -v
```

## Limitations

- Maximum precision is limited by Python's `Decimal` implementation
- For applications requiring more than 13 decimal places, increase `INTERNAL_PRECISION` constant
- Not optimized for calculating Pi beyond 20-30 decimal places (other algorithms are more efficient for extreme precision)