"""
Comprehensive test suite for Pi calculation function.

This module contains BDD-style tests covering all 10 scenarios
for the calculate_pi() function implementation.
"""

import time
from decimal import Decimal
from typing import Callable

import pytest

from src.pi_calculator import calculate_pi


# Fixtures
@pytest.fixture
def pi_function() -> Callable:
    """Fixture that provides the calculate_pi function."""
    return calculate_pi


@pytest.fixture
def expected_pi_value() -> Decimal:
    """Fixture that provides the expected Pi value to 13 decimal places."""
    return Decimal("3.1415926535897")


# Test 1: Function exists and is callable
def test_function_exists_and_callable(pi_function: Callable) -> None:
    """
    Test that the calculate_pi function exists and is callable.
    
    Scenario: Verify function can be imported and invoked
    """
    assert pi_function is not None
    assert callable(pi_function)


# Test 2: Function returns numeric value
def test_calculate_pi_returns_numeric(pi_function: Callable) -> None:
    """
    Test that calculate_pi returns a numeric type (Decimal or float).
    
    Scenario: Verify return type is appropriate for mathematical constant
    """
    result = pi_function()
    assert isinstance(result, (Decimal, float))


# Test 3: Pi value has correct precision and exact value
def test_pi_correct_precision(pi_function: Callable, expected_pi_value: Decimal) -> None:
    """
    Test that calculate_pi returns Pi to exactly 13 decimal places.
    
    Scenario: Verify the exact value matches 3.1415926535897
    """
    result = pi_function()
    
    # Convert to Decimal for precise comparison
    if isinstance(result, float):
        result_decimal = Decimal(str(result))
    else:
        result_decimal = result
    
    # Check exact value
    assert result_decimal == expected_pi_value
    
    # Check number of decimal places
    result_str = str(result_decimal)
    if '.' in result_str:
        decimal_places = len(result_str.split('.')[1])
        assert decimal_places == 13


# Test 4: Pi accuracy verification - first and last digits
def test_pi_accuracy_verification(pi_function: Callable) -> None:
    """
    Test that Pi value has correct first 5 and last 5 digits.
    
    Scenario: Verify specific digit patterns in the result
    """
    result = pi_function()
    result_str = str(result)
    
    # Remove decimal point for digit checking
    digits_only = result_str.replace('.', '')
    
    # First 5 digits should be 31415
    assert digits_only[:5] == "31415"
    
    # Last 5 digits should be 35897
    assert digits_only[-5:] == "35897"


# Test 5: Return type precision - no rounding errors
def test_return_type_precision(pi_function: Callable, expected_pi_value: Decimal) -> None:
    """
    Test that return type maintains precision without rounding errors.
    
    Scenario: Verify Decimal or high-precision float type
    """
    result = pi_function()
    
    # Should be Decimal or float
    assert isinstance(result, (Decimal, float))
    
    # Convert to string and check precision
    result_str = str(result)
    
    # Should match expected value when compared as strings
    expected_str = str(expected_pi_value)
    assert result_str == expected_str


# Test 6: Repeated calls consistency
def test_repeated_calls_consistency(pi_function: Callable) -> None:
    """
    Test that multiple calls to calculate_pi return identical results.
    
    Scenario: Call function 100 times and verify all results match
    """
    results = [pi_function() for _ in range(100)]
    
    # All results should be identical
    first_result = results[0]
    for result in results[1:]:
        assert result == first_result


# Test 7: Performance test
def test_performance(pi_function: Callable) -> None:
    """
    Test that calculate_pi executes in reasonable time.
    
    Scenario: Execution time should be less than 1 second
    """
    start_time = time.perf_counter()
    result = pi_function()
    end_time = time.perf_counter()
    
    execution_time = end_time - start_time
    
    # Should complete in less than 1 second
    assert execution_time < 1.0
    
    # Verify result is valid
    assert result is not None


# Test 8: No external input required
def test_no_external_input(pi_function: Callable) -> None:
    """
    Test that calculate_pi works without any parameters.
    
    Scenario: Function should be callable with no arguments
    """
    # Should not raise any exception
    result = pi_function()
    
    # Should return a valid result
    assert result is not None
    assert isinstance(result, (Decimal, float))


# Test 9: Edge case precision - internal precision and rounding
def test_edge_case_precision(pi_function: Callable, expected_pi_value: Decimal) -> None:
    """
    Test that internal precision is sufficient and rounding is correct.
    
    Scenario: Verify that 14th decimal place is properly handled
    """
    result = pi_function()
    
    if isinstance(result, float):
        result_decimal = Decimal(str(result))
    else:
        result_decimal = result
    
    # The result should be exactly 3.1415926535897
    assert result_decimal == expected_pi_value
    
    # Check that if we had one more decimal place, it would be 3.14159265358979...
    # The 14th decimal place of Pi is 9, so rounding at 13 places should give 7
    result_str = str(result_decimal)
    assert result_str.endswith('97') or result_str.endswith('897')
    
    # Verify no trailing zeros (should be exact)
    assert not result_str.endswith('0')


# Test 10: Function documentation
def test_function_documentation(pi_function: Callable) -> None:
    """
    Test that calculate_pi has proper documentation.
    
    Scenario: Verify docstring and metadata exist
    """
    # Should have a docstring
    assert pi_function.__doc__ is not None
    assert len(pi_function.__doc__.strip()) > 0
    
    # Should have a name
    assert pi_function.__name__ == "calculate_pi"
    
    # Docstring should mention Pi or the return value
    docstring_lower = pi_function.__doc__.lower()
    assert 'pi' in docstring_lower or 'return' in docstring_lower


# Additional edge case tests
def test_result_format_consistency(pi_function: Callable) -> None:
    """
    Test that result format is consistent across calls.
    
    Scenario: String representation should be stable
    """
    result1 = pi_function()
    result2 = pi_function()
    
    # String representations should match
    assert str(result1) == str(result2)
    
    # Type should be consistent
    assert type(result1) == type(result2)


def test_mathematical_correctness(pi_function: Callable) -> None:
    """
    Test mathematical correctness of Pi value.
    
    Scenario: Verify value is within known bounds of Pi
    """
    result = pi_function()
    
    # Convert to float for comparison
    if isinstance(result, Decimal):
        result_float = float(result)
    else:
        result_float = result
    
    # Pi should be between 3.14 and 3.15
    assert 3.14 < result_float < 3.15
    
    # More specifically, between 3.1415 and 3.1416
    assert 3.1415 < result_float < 3.1416


def test_decimal_precision_attributes(pi_function: Callable) -> None:
    """
    Test that Decimal type result has correct precision attributes.
    
    Scenario: If result is Decimal, verify its precision characteristics
    """
    result = pi_function()
    
    if isinstance(result, Decimal):
        # Should have exactly 13 decimal places
        result_tuple = result.as_tuple()
        
        # Count significant digits
        result_str = str(result)
        if '.' in result_str:
            integer_part, decimal_part = result_str.split('.')
            assert len(decimal_part) == 13