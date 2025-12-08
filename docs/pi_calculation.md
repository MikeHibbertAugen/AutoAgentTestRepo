# Pi Calculation Documentation

## Overview

The `math_utils` module provides a function to calculate the value of Pi (π) to 6 decimal places using a mathematical algorithm.

## Algorithm

This implementation uses the **Machin-like formula** for calculating Pi, which provides fast convergence and excellent accuracy:

```
π/4 = 4 * arctan(1/5) - arctan(1/239)
```

This formula was discovered by John Machin in 1706 and is significantly more efficient than the simple Leibniz formula. The arctan function is computed using a Taylor series expansion:

```
arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + x⁹/9 - ...
```

## Usage

### Basic Example

```python
from math_utils import calculate_pi

# Calculate Pi to 6 decimal places
pi_value = calculate_pi()
print(f"Pi = {pi_value}")  # Output: Pi = 3.141592653589793
print(f"Pi (6 decimals) = {round(pi_value, 6)}")  # Output: Pi (6 decimals) = 3.141593
```

### Integration Example

```python
from math_utils import calculate_pi

def calculate_circle_area(radius: float) -> float:
    """Calculate the area of a circle using our Pi calculation."""
    pi = calculate_pi()
    return pi * radius ** 2

area = calculate_circle_area(5.0)
print(f"Area of circle with radius 5: {area}")
```

## Precision and Accuracy

- **Guaranteed Precision**: The function returns Pi accurate to at least 6 decimal places (3.141593)
- **Actual Precision**: Python's float type provides precision up to approximately 15-17 significant decimal digits
- **Return Value**: `3.141592653589793` (full float precision)
- **Validation**: Unit tests verify that `round(calculate_pi(), 6) == 3.141593`

## Performance Considerations

- **Convergence Speed**: Machin's formula converges much faster than the Leibniz formula (O(n) vs O(n²) terms needed)
- **Computational Cost**: The function typically requires fewer than 20 iterations to achieve 6 decimal place accuracy
- **Time Complexity**: O(n) where n is the number of iterations needed for desired precision
- **Space Complexity**: O(1) - constant space usage
- **Execution Time**: Sub-millisecond performance on modern hardware

## Mathematical References

1. **Machin's Formula**: J. Machin (1706) - Used for calculating 100 digits of Pi by hand
2. **Taylor Series**: Standard arctangent series expansion
3. **Convergence Theory**: The series converges for |x| ≤ 1

## Function Signature

```python
def calculate_pi() -> float:
    """
    Calculate the value of Pi using Machin's formula.
    
    Returns:
        float: The value of Pi accurate to at least 6 decimal places (3.141593)
    """
```

## Testing

The function is thoroughly tested in `tests/test_math_utils.py` with the following test cases:

- Accuracy verification (6 decimal places)
- Return type validation
- Reproducibility verification
- Precision bounds checking

To run the tests:

```bash
pytest tests/test_math_utils.py -v
```

## Implementation Notes

- No external dependencies required (pure Python implementation)
- Deterministic output (same result on every invocation)
- Thread-safe (pure function with no side effects)
- No floating-point precision issues for the target accuracy level

## See Also

- `README.md` - Project overview and quick start guide
- `tests/test_math_utils.py` - Comprehensive test suite