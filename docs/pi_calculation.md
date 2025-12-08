# Pi Calculation Documentation

## Overview

This document describes the implementation of Pi calculation using the Leibniz formula (also known as the Gregory-Leibniz series), a mathematical series for computing the value of π.

## The Leibniz Formula

The Leibniz formula for π is an infinite series:

```
π = 4 * (1 - 1/3 + 1/5 - 1/7 + 1/9 - 1/11 + ...)
```

Or more formally:

```
π = 4 * Σ((-1)^n / (2n + 1)) for n = 0 to ∞
```

### Mathematical Properties

- **Convergence**: The series converges to π, but does so relatively slowly
- **Alternating Series**: Each term alternates in sign, providing natural error bounds
- **Simple Terms**: Each term only requires basic arithmetic operations
- **Monotonic Error**: Error decreases monotonically with more terms

## Implementation Details

### Algorithm

The implementation iteratively computes terms of the series until the desired precision is achieved:

1. Initialize sum to 0
2. For each iteration n (starting from 0):
   - Calculate term: `(-1)^n / (2n + 1)`
   - Multiply by 4 to get contribution to π
   - Add to running sum
   - Check if precision target is met
3. Return final sum

### Precision Target

The function calculates π to **5 decimal places** (3.14159).

### Convergence Criteria

The algorithm continues iterating until the difference between consecutive approximations is less than `10^-6`, ensuring accuracy to at least 5 decimal places when rounded.

## Computational Complexity

### Time Complexity

- **O(n)** where n is the number of iterations required
- Approximately **500,000 iterations** needed for 5 decimal place accuracy
- Each iteration performs constant-time operations (O(1))

### Space Complexity

- **O(1)** - constant space usage
- Only stores running sum and current term value

### Performance Characteristics

- Expected execution time: 100-500 milliseconds on modern hardware
- Deterministic: same number of iterations for same precision target
- No recursion or stack growth

## Usage Examples

### Basic Usage

```python
from math_utils import calculate_pi

# Calculate Pi to 5 decimal places
pi_value = calculate_pi()
print(f"Pi ≈ {pi_value:.5f}")  # Output: Pi ≈ 3.14159
```

### Comparison with Standard Library

```python
import math
from math_utils import calculate_pi

calculated_pi = calculate_pi()
standard_pi = math.pi

print(f"Calculated: {calculated_pi:.5f}")
print(f"Standard:   {standard_pi:.5f}")
print(f"Difference: {abs(calculated_pi - standard_pi):.10f}")
```

### Integration in Applications

```python
from math_utils import calculate_pi

def calculate_circle_area(radius: float) -> float:
    """Calculate circle area using our Pi calculation."""
    pi = calculate_pi()
    return pi * radius ** 2

area = calculate_circle_area(5.0)
print(f"Circle area: {area:.2f}")
```

## Accuracy and Limitations

### Accuracy

- **Target Precision**: 5 decimal places (3.14159)
- **Actual Accuracy**: Typically within 10^-6 of true π value
- **Rounding**: Result should be rounded to 5 decimals for guaranteed accuracy

### Limitations

1. **Slow Convergence**: Requires many iterations compared to modern algorithms
2. **Not Suitable for High Precision**: For more than 10 decimal places, consider alternative algorithms
3. **Computational Cost**: Higher CPU usage than using `math.pi` constant

### Error Analysis

The error after n terms is bounded by the next term in the series:

```
|Error| ≤ 4 / (2n + 1)
```

For 5 decimal place accuracy (error < 10^-5):
```
4 / (2n + 1) < 10^-5
n > (4 × 10^5 - 1) / 2
n > 199,999.5
```

Therefore, approximately **200,000+ iterations** are required.

## Alternative Algorithms Considered

### 1. Machin's Formula
```
π = 16 * arctan(1/5) - 4 * arctan(1/239)
```
- **Pros**: Much faster convergence
- **Cons**: More complex implementation

### 2. Nilakantha Series
```
π = 3 + 4/(2×3×4) - 4/(4×5×6) + 4/(6×7×8) - ...
```
- **Pros**: Faster than Leibniz
- **Cons**: More complex terms

### 3. Bailey–Borwein–Plouffe Formula
```
π = Σ(1/16^k * (4/(8k+1) - 2/(8k+4) - 1/(8k+5) - 1/(8k+6)))
```
- **Pros**: Extremely fast, can compute hex digits directly
- **Cons**: Significantly more complex

### Why Leibniz?

The Leibniz formula was chosen for this implementation due to:
- **Simplicity**: Easy to understand and implement
- **Educational Value**: Demonstrates series convergence
- **No Dependencies**: Requires only basic arithmetic
- **Sufficient Performance**: Adequate for 5 decimal place target

## References

- Leibniz, G. W. (1682). "De vera proportione circuli ad quadratum circumscriptum"
- Gregory, J. (1671). "Geometriae Pars Universalis"
- Weisstein, Eric W. "Leibniz Series." From MathWorld--A Wolfram Web Resource

## Future Improvements

Potential enhancements for future versions:

1. **Configurable Precision**: Allow users to specify desired decimal places
2. **Algorithm Selection**: Support multiple algorithms based on precision needs
3. **Caching**: Cache previously calculated values
4. **Parallel Computation**: Divide series calculation across multiple cores
5. **Arbitrary Precision**: Use `decimal.Decimal` for higher precision calculations