import pytest
import math
from src.pi_calculator import calculate_pi


class TestCalculatePi:
    """Test suite for the Pi calculator function."""

    def test_calculate_pi_accuracy(self):
        """Test that calculate_pi returns Pi accurate to 7 decimal places."""
        result = calculate_pi()
        expected = 3.1415927
        assert f"{result:.7f}" == f"{expected:.7f}", (
            f"Expected Pi to be {expected:.7f}, got {result:.7f}"
        )

    def test_calculate_pi_precision(self):
        """Test that calculate_pi is within acceptable precision of math.pi."""
        result = calculate_pi()
        tolerance = 1e-7
        difference = abs(result - math.pi)
        assert difference < tolerance, (
            f"Difference from math.pi ({difference}) exceeds tolerance ({tolerance})"
        )

    def test_calculate_pi_return_type(self):
        """Test that calculate_pi returns a float."""
        result = calculate_pi()
        assert isinstance(result, float), (
            f"Expected return type float, got {type(result).__name__}"
        )

    def test_calculate_pi_consistency(self):
        """Test that calculate_pi returns consistent results across multiple calls."""
        results = [calculate_pi() for _ in range(10)]
        first_result = results[0]
        
        for i, result in enumerate(results[1:], start=1):
            assert result == first_result, (
                f"Call {i+1} returned {result}, expected {first_result}"
            )

    def test_calculate_pi_performance(self):
        """Test that calculate_pi completes in reasonable time."""
        import time
        
        start_time = time.time()
        calculate_pi()
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        max_time_ms = 100
        
        assert execution_time < max_time_ms, (
            f"Execution took {execution_time:.2f}ms, expected < {max_time_ms}ms"
        )

    def test_calculate_pi_exact_digits(self):
        """Test specific digits of Pi for correctness."""
        result = calculate_pi()
        # Pi = 3.14159265358979...
        # Testing to 7 decimal places: 3.1415927 (rounded)
        result_str = f"{result:.10f}"
        
        # Check integer part
        assert result_str[0] == "3", "Integer part should be 3"
        
        # Check first few decimal digits
        assert result_str[2] == "1", "First decimal should be 1"
        assert result_str[3] == "4", "Second decimal should be 4"
        assert result_str[4] == "1", "Third decimal should be 1"
        assert result_str[5] == "5", "Fourth decimal should be 5"
        assert result_str[6] == "9", "Fifth decimal should be 9"

    def test_calculate_pi_positive(self):
        """Test that calculate_pi returns a positive value."""
        result = calculate_pi()
        assert result > 0, f"Pi should be positive, got {result}"

    def test_calculate_pi_reasonable_range(self):
        """Test that calculate_pi returns a value in the expected range."""
        result = calculate_pi()
        assert 3.14 < result < 3.15, (
            f"Pi should be between 3.14 and 3.15, got {result}"
        )