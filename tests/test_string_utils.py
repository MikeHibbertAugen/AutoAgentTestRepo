"""
Comprehensive unit tests for string_utils module.

Tests the reverse_string function with various inputs including
edge cases, unicode characters, and error conditions.
"""

import pytest
from src.string_utils import reverse_string


class TestReverseString:
    """Test suite for reverse_string function."""

    def test_reverse_string_normal(self):
        """Test reversing a normal string."""
        assert reverse_string("hello") == "olleh"
        assert reverse_string("world") == "dlrow"
        assert reverse_string("Python") == "nohtyP"

    def test_reverse_string_empty(self):
        """Test reversing an empty string."""
        assert reverse_string("") == ""

    def test_reverse_string_single_char(self):
        """Test reversing a single character string."""
        assert reverse_string("a") == "a"
        assert reverse_string("Z") == "Z"
        assert reverse_string("5") == "5"

    def test_reverse_string_with_spaces(self):
        """Test reversing strings with spaces."""
        assert reverse_string("hello world") == "dlrow olleh"
        assert reverse_string("  spaces  ") == "  secaps  "
        assert reverse_string(" ") == " "

    def test_reverse_string_unicode(self):
        """Test reversing strings with unicode characters."""
        assert reverse_string("café") == "éfac"
        assert reverse_string("こんにちは") == "はちにんこ"
        assert reverse_string("🎉🎊🎈") == "🎈🎊🎉"
        assert reverse_string("Ω≈ç√") == "√ç≈Ω"

    def test_reverse_string_special_characters(self):
        """Test reversing strings with special characters."""
        assert reverse_string("!@#$%") == "%$#@!"
        assert reverse_string("a-b-c") == "c-b-a"
        assert reverse_string("test123") == "321tset"
        assert reverse_string("line\nbreak") == "kaerb\nenil"
        assert reverse_string("tab\there") == "ereh\tbat"

    def test_reverse_string_numbers(self):
        """Test reversing numeric strings."""
        assert reverse_string("12345") == "54321"
        assert reverse_string("0") == "0"
        assert reverse_string("3.14159") == "95141.3"

    def test_reverse_string_palindrome(self):
        """Test reversing palindromes."""
        assert reverse_string("racecar") == "racecar"
        assert reverse_string("level") == "level"
        assert reverse_string("noon") == "noon"

    def test_reverse_string_mixed_case(self):
        """Test reversing strings with mixed case."""
        assert reverse_string("HeLLo") == "oLLeH"
        assert reverse_string("PyThOn") == "nOhTyP"

    def test_reverse_string_type_error_none(self):
        """Test that TypeError is raised for None input."""
        with pytest.raises(TypeError, match="Input must be a string"):
            reverse_string(None)

    def test_reverse_string_type_error_int(self):
        """Test that TypeError is raised for integer input."""
        with pytest.raises(TypeError, match="Input must be a string"):
            reverse_string(123)

    def test_reverse_string_type_error_list(self):
        """Test that TypeError is raised for list input."""
        with pytest.raises(TypeError, match="Input must be a string"):
            reverse_string(["hello"])

    def test_reverse_string_type_error_dict(self):
        """Test that TypeError is raised for dict input."""
        with pytest.raises(TypeError, match="Input must be a string"):
            reverse_string({"key": "value"})

    def test_reverse_string_type_error_float(self):
        """Test that TypeError is raised for float input."""
        with pytest.raises(TypeError, match="Input must be a string"):
            reverse_string(3.14)

    def test_reverse_string_type_error_bool(self):
        """Test that TypeError is raised for boolean input."""
        with pytest.raises(TypeError, match="Input must be a string"):
            reverse_string(True)


@pytest.fixture
def sample_strings():
    """Fixture providing sample strings for testing."""
    return {
        "short": "hi",
        "medium": "hello world",
        "long": "a" * 1000,
        "unicode": "こんにちは世界",
        "special": "!@#$%^&*()",
        "mixed": "Test123!@#"
    }


class TestReverseStringWithFixtures:
    """Additional tests using pytest fixtures."""

    def test_reverse_string_with_fixture(self, sample_strings):
        """Test reverse_string using fixture data."""
        assert reverse_string(sample_strings["short"]) == "ih"
        assert reverse_string(sample_strings["medium"]) == "dlrow olleh"
        assert reverse_string(sample_strings["special"]) == ")(*&^%$#@!"

    def test_reverse_string_long(self, sample_strings):
        """Test reversing a very long string."""
        long_string = sample_strings["long"]
        reversed_long = reverse_string(long_string)
        assert len(reversed_long) == len(long_string)
        assert reversed_long == "a" * 1000

    def test_reverse_string_idempotent(self, sample_strings):
        """Test that reversing twice returns the original string."""
        for key, value in sample_strings.items():
            assert reverse_string(reverse_string(value)) == value