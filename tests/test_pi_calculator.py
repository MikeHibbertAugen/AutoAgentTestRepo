"""
Unit tests for the Pi calculator module.

Tests the calculate_pi() function for accuracy, precision, and correctness
using Machin's formula implementation.
"""

import pytest
import math
from src.pi_calculator import calculate_pi, PI_PRECISION


class TestCalculatePi:
    """Test suite for the calculate_pi function."""

    @pytest.fixture
    def expected_pi(self):
        """Fixture providing the expected Pi value to 8 decimal places."""
        return 3.14159265

    @pytest.fixture
    def pi_tolerance(self):
        """Fixture providing the tolerance for Pi comparison."""
        return 1e-8  # Tolerance for 8 decimal places

    def test_calculate_pi_accuracy(self, expected_pi, pi_tolerance):
        """Test that calculate_pi returns Pi accurate to 8 decimal places."""
        result = calculate_pi()
        assert isinstance(result, float), "Result should be a float"
        assert abs(result - expected_pi) < pi_tolerance, \
            f"Pi calculation not accurate enough. Expected {expected_pi}, got {result}"

    def test_calculate_pi_matches_known_value(self, expected_pi):
        """Test that the calculated Pi matches the known value when rounded."""
        result = calculate_pi()
        rounded_result = round(result, PI_PRECISION)
        assert rounded_result == expected_pi, \
            f"Rounded Pi should be {expected_pi}, got {rounded_result}"

    def test_calculate_pi_precision(self):
        """Test that calculate_pi returns a value with appropriate precision."""
        result = calculate_pi()
        # Convert to string and check decimal places
        result_str = f"{result:.10f}"
        # Verify we get a reasonable value (not checking exact decimal places in string)
        assert result > 3.14159264 and result < 3.14159266, \
            "Pi value should be within expected range"

    def test_calculate_pi_return_type(self):
        """Test that calculate_pi returns a float type."""
        result = calculate_pi()
        assert type(result) is float, f"Expected float, got {type(result)}"

    def test_calculate_pi_positive(self):
        """Test that calculate_pi returns a positive value."""
        result = calculate_pi()
        assert result > 0, "Pi should be positive"

    def test_calculate_pi_greater_than_three(self):
        """Test that calculate_pi returns a value greater than 3."""
        result = calculate_pi()
        assert result > 3, "Pi should be greater than 3"

    def test_calculate_pi_less_than_four(self):
        """Test that calculate_pi returns a value less than 4."""
        result = calculate_pi()
        assert result < 4, "Pi should be less than 4"

    def test_calculate_pi_consistency(self):
        """Test that calculate_pi returns consistent results across multiple calls."""
        result1 = calculate_pi()
        result2 = calculate_pi()
        result3 = calculate_pi()
        assert result1 == result2 == result3, \
            "calculate_pi should return consistent results"

    def test_calculate_pi_performance(self):
        """Test that calculate_pi completes in reasonable time."""
        import time
        start_time = time.time()
        calculate_pi()
        end_time = time.time()
        execution_time = end_time - start_time
        assert execution_time < 1.0, \
            f"calculate_pi took {execution_time}s, should be under 1 second"

    def test_calculate_pi_vs_math_pi(self):
        """Test that calculate_pi is close to math.pi."""
        result = calculate_pi()
        difference = abs(result - math.pi)
        # Should be accurate to at least 8 decimal places
        assert difference < 1e-8, \
            f"Difference from math.pi is {difference}, should be less than 1e-8"

    def test_pi_precision_constant(self):
        """Test that PI_PRECISION constant is set correctly."""
        assert PI_PRECISION == 8, "PI_PRECISION should be 8"
        assert isinstance(PI_PRECISION, int), "PI_PRECISION should be an integer"

    def test_calculate_pi_docstring(self):
        """Test that calculate_pi has proper documentation."""
        assert calculate_pi.__doc__ is not None, \
            "calculate_pi should have a docstring"
        assert len(calculate_pi.__doc__.strip()) > 0, \
            "calculate_pi docstring should not be empty"

    def test_calculate_pi_specific_digits(self):
        """Test specific digits of Pi calculation."""
        result = calculate_pi()
        result_str = f"{result:.8f}"
        expected_str = "3.14159265"
        assert result_str == expected_str, \
            f"Expected {expected_str}, got {result_str}"


class TestPiCalculatorEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_module_imports_correctly(self):
        """Test that the pi_calculator module can be imported."""
        try:
            from src import pi_calculator
            assert hasattr(pi_calculator, 'calculate_pi'), \
                "Module should have calculate_pi function"
        except ImportError as e:
            pytest.fail(f"Failed to import pi_calculator module: {e}")

    def test_no_arguments_required(self):
        """Test that calculate_pi can be called without arguments."""
        try:
            result = calculate_pi()
            assert result is not None, "calculate_pi should return a value"
        except TypeError:
            pytest.fail("calculate_pi should not require arguments")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.pi_calculator", "--cov-report=term-missing"])