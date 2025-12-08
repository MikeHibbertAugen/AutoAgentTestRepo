# API Reference

## Pi Calculator Module

### `calculate_pi() -> Decimal`

Calculate the mathematical constant Pi (π) to exactly 13 decimal places.

#### Parameters

None - This function takes no parameters.

#### Returns

- `Decimal`: The value of Pi as a Decimal object with exactly 13 decimal places: `3.1415926535897`

#### Raises

This function does not raise any exceptions under normal circumstances.

#### Description

This function calculates the mathematical constant Pi (π) using Machin's formula, a fast-converging algorithm for computing Pi to arbitrary precision. The formula used is:

```
π/4 = 4*arctan(1/5) - arctan(1/239)
```

The function implements the arctangent calculation using the Taylor series expansion:

```
arctan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ...
```

The implementation uses Python's `decimal` module to ensure high-precision arithmetic. Internally, the function sets the decimal precision to at least 20 places to guarantee accurate rounding to 13 decimal places in the final result.

The function is deterministic and will always return the same value: `3.1415926535897`

#### Algorithm Details

**Machin's Formula** was discovered by John Machin in 1706 and was used to calculate Pi to 100 decimal places by hand. It converges rapidly because:
- The term `arctan(1/5)` has a small argument, leading to fast convergence
- The term `arctan(1/239)` converges even faster due to the very small argument
- The coefficients (4 and -1) balance the series for optimal accuracy

**Internal Precision**: The function sets `decimal.getcontext().prec` to 20 or higher to ensure that rounding errors do not affect the 13th decimal place.

**Rounding**: The final result is rounded to exactly 13 decimal places using the `quantize()` method with `Decimal('0.0000000000001')`.

#### Examples

**Basic usage:**
```python
from src.pi_calculator import calculate_pi

pi_value = calculate_pi()
print(pi_value)  # Output: 3.1415926535897
```

**Verify precision:**
```python
from decimal import Decimal
from src.pi_calculator import calculate_pi

pi_value = calculate_pi()
print(type(pi_value))  # Output: <class 'decimal.Decimal'>
print(f"{pi_value:.13f}")  # Output: 3.1415926535897
```

**Multiple calls (consistency check):**
```python
from src.pi_calculator import calculate_pi

results = [calculate_pi() for _ in range(100)]
assert all(result == results[0] for result in results)
print("All results are identical!")
```

**Using in calculations:**
```python
from src.pi_calculator import calculate_pi
from decimal import Decimal

pi = calculate_pi()
radius = Decimal('5.0')
area = pi * radius * radius
print(f"Area of circle with radius {radius}: {area}")
# Output: Area of circle with radius 5.0: 78.53981633974...
```

**Comparing with math.pi:**
```python
import math
from src.pi_calculator import calculate_pi

our_pi = calculate_pi()
math_pi = math.pi
print(f"Our Pi:   {our_pi}")
print(f"math.pi:  {math_pi}")
print(f"Difference: {abs(float(our_pi) - math_pi)}")
```

#### Performance Characteristics

- **Time Complexity**: O(n) where n is the number of terms needed in the Taylor series (approximately 15-20 terms for 13 decimal places)
- **Space Complexity**: O(1) - constant space for intermediate calculations
- **Execution Time**: Typically completes in less than 0.01 seconds on modern hardware
- **Deterministic**: Always returns the same value with no randomness or external dependencies

#### Notes

- The function is completely deterministic and requires no external input
- No network calls, file I/O, or system dependencies are required
- The result is cached internally by the algorithm's deterministic nature, but each call performs the full calculation
- The precision of 13 decimal places is sufficient for most scientific and engineering applications
- For comparison, NASA uses only 15 decimal places of Pi for interplanetary navigation calculations
- The `Decimal` type ensures no floating-point precision errors occur

#### Type Information

```python
from decimal import Decimal

def calculate_pi() -> Decimal:
    """
    Calculate Pi to exactly 13 decimal places.
    
    Returns:
        Decimal: Pi value as 3.1415926535897
    """
    ...
```

#### Thread Safety

This function is thread-safe as it:
- Does not modify any global state (except temporarily setting decimal context precision)
- Performs pure mathematical calculations
- Does not use any shared mutable data structures

Multiple threads can safely call this function concurrently.