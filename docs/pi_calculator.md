# Pi Calculator Documentation

## Overview

The Pi Calculator module provides a high-precision implementation for calculating the mathematical constant π (pi) to 8 decimal places using Machin's formula. This implementation is optimized for accuracy and performance while maintaining simplicity and readability.

## Mathematical Background

### Machin's Formula

The implementation uses Machin's formula, discovered by John Machin in 1706:

```
π/4 = 4·arctan(1/5) - arctan(1/239)
```

This formula is particularly well-suited for computing π because:

1. **Fast Convergence**: The arguments (1/5 and 1/239) are small, allowing the Taylor series to converge rapidly
2. **High Accuracy**: Achieves 8 decimal place precision with relatively few terms
3. **Computational Efficiency**: Requires only basic arithmetic operations
4. **Numerical Stability**: Avoids issues with floating-point precision loss

### Taylor Series Expansion

The arctan function is computed using its Taylor series expansion:

```
arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + x⁹/9 - ...
```

For |x| < 1, this series converges quickly. The implementation calculates sufficient terms to guarantee 8 decimal place accuracy.

## Usage

### Basic Usage

```python
from pi_calculator import calculate_pi

# Calculate pi to 8 decimal places
pi_value = calculate_pi()
print(f"Pi = {pi_value}")  # Output: Pi = 3.14159265
```

### Expected Output

The function returns a float representing π accurate to 8 decimal places:

```
3.14159265
```

## Function Reference

### `calculate_pi()`

Calculates the value of π (pi) to 8 decimal places using Machin's formula.

**Parameters:**
- None

**Returns:**
- `float`: The value of π accurate to 8 decimal places (3.14159265)

**Raises:**
- None (pure mathematical calculation with no error conditions)

**Example:**

```python
from pi_calculator import calculate_pi

pi = calculate_pi()
assert round(pi, 8) == 3.14159265
```

## Implementation Details

### Precision Guarantee

The implementation guarantees accuracy to 8 decimal places by:

1. Computing sufficient terms in the Taylor series (typically 15-20 terms for each arctan calculation)
2. Using Python's native floating-point arithmetic (IEEE 754 double precision)
3. Carefully ordering operations to minimize accumulated rounding errors

### Performance Characteristics

- **Time Complexity**: O(n) where n is the number of Taylor series terms
- **Space Complexity**: O(1) - constant space usage
- **Typical Execution Time**: < 1 millisecond on modern hardware

### Algorithm Steps

1. Calculate arctan(1/5) using Taylor series
2. Calculate arctan(1/239) using Taylor series
3. Apply Machin's formula: π = 4 × [4·arctan(1/5) - arctan(1/239)]
4. Return the result

## Testing

The module includes comprehensive unit tests to verify:

- Accuracy to 8 decimal places
- Consistency across multiple invocations
- Type correctness
- Performance requirements

Run tests with:

```bash
pytest tests/test_pi_calculator.py -v
```

## Why Machin's Formula?

Several methods exist for calculating π. Machin's formula was chosen because:

1. **Historical Significance**: Used for centuries in manual and computational π calculations
2. **Educational Value**: Clear mathematical foundation, easy to understand
3. **Proven Accuracy**: Well-studied convergence properties
4. **No Dependencies**: Requires only basic arithmetic operations
5. **Suitable Precision**: Perfect balance for 8 decimal place accuracy

### Alternatives Considered

- **Bailey–Borwein–Plouffe (BBP) Formula**: More complex, better suited for hexadecimal digit extraction
- **Nilakantha Series**: Slower convergence for 8 decimal places
- **Monte Carlo Methods**: Non-deterministic, less accurate
- **Chudnovsky Algorithm**: Overkill for 8 decimal places, more complex implementation

## References

- Machin, John (1706). Original formula for π calculation
- [Machin's Formula - Wikipedia](https://en.wikipedia.org/wiki/Machin%27s_formula)
- [Taylor Series - Wikipedia](https://en.wikipedia.org/wiki/Taylor_series)
- Arndt, J. & Haenel, C. (2001). "Pi Unleashed". Springer-Verlag.

## Module Constants

### `PI_PRECISION`

Defines the precision level (number of decimal places) for π calculation.

```python
PI_PRECISION = 8
```

This constant is used throughout the module to ensure consistency in precision requirements and can be referenced by users to understand the accuracy guarantees.