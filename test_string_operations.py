import pytest
from src.utils.string_operations import reverse_string


class TestReverseString:
    """Comprehensive test suite for the reverse_string function."""

    def test_basic_string_reversal(self):
        """Test reversing a basic ASCII string."""
        assert reverse_string("hello") == "olleh"
        assert reverse_string("world") == "dlrow"
        assert reverse_string("Python") == "nohtyP"

    def test_empty_string(self):
        """Test reversing an empty string."""
        assert reverse_string("") == ""

    def test_single_character(self):
        """Test reversing a single character string."""
        assert reverse_string("a") == "a"
        assert reverse_string("Z") == "Z"
        assert reverse_string("5") == "5"

    def test_string_with_spaces(self):
        """Test reversing strings containing spaces."""
        assert reverse_string("hello world") == "dlrow olleh"
        assert reverse_string("a b c") == "c b a"
        assert reverse_string("  spaces  ") == "  secaps  "

    def test_unicode_characters(self):
        """Test reversing strings with Unicode characters."""
        assert reverse_string("Hello 👋 World") == "dlroW 👋 olleH"
        assert reverse_string("café") == "éfac"
        assert reverse_string("你好世界") == "界世好你"
        assert reverse_string("🎉🎊🎈") == "🎈🎊🎉"

    def test_numbers_as_strings(self):
        """Test reversing numeric strings."""
        assert reverse_string("12345") == "54321"
        assert reverse_string("0") == "0"
        assert reverse_string("987654321") == "123456789"

    def test_special_characters(self):
        """Test reversing strings with special characters."""
        assert reverse_string("!@#$%") == "%$#@!"
        assert reverse_string("a-b-c") == "c-b-a"
        assert reverse_string("test@example.com") == "moc.elpmaxe@tset"
        assert reverse_string("line1\nline2") == "2enil\n1enil"

    def test_palindromes(self):
        """Test reversing palindromes returns the same string."""
        assert reverse_string("racecar") == "racecar"
        assert reverse_string("noon") == "noon"
        assert reverse_string("a") == "a"

    def test_mixed_case(self):
        """Test reversing strings with mixed case."""
        assert reverse_string("HeLLo WoRLd") == "dLRoW oLLeH"
        assert reverse_string("PyThOn") == "nOhTyP"

    def test_type_error_with_none(self):
        """Test that passing None raises TypeError."""
        with pytest.raises(TypeError, match="Input must be a string"):
            reverse_string(None)

    def test_type_error_with_integer(self):
        """Test that passing an integer raises TypeError."""
        with pytest.raises(TypeError, match="Input must be a string"):
            reverse_string(123)

    def test_type_error_with_list(self):
        """Test that passing a list raises TypeError."""
        with pytest.raises(TypeError, match="Input must be a string"):
            reverse_string(["h", "e", "l", "l", "o"])

    def test_type_error_with_dict(self):
        """Test that passing a dictionary raises TypeError."""
        with pytest.raises(TypeError, match="Input must be a string"):
            reverse_string({"key": "value"})

    def test_type_error_with_float(self):
        """Test that passing a float raises TypeError."""
        with pytest.raises(TypeError, match="Input must be a string"):
            reverse_string(3.14)

    def test_type_error_with_boolean(self):
        """Test that passing a boolean raises TypeError."""
        with pytest.raises(TypeError, match="Input must be a string"):
            reverse_string(True)

    def test_long_string(self):
        """Test reversing a long string."""
        long_string = "a" * 1000
        reversed_long = reverse_string(long_string)
        assert reversed_long == long_string
        assert len(reversed_long) == 1000

    def test_string_with_newlines_and_tabs(self):
        """Test reversing strings with newlines and tabs."""
        assert reverse_string("hello\tworld") == "dlrow\tolleh"
        assert reverse_string("line1\nline2\nline3") == "3enil\n2enil\n1enil"

    def test_string_with_quotes(self):
        """Test reversing strings containing quotes."""
        assert reverse_string('He said "Hello"') == '"olleH" dias eH'
        assert reverse_string("It's a test") == "tset a s'tI"

    def test_alphanumeric_with_symbols(self):
        """Test reversing complex alphanumeric strings with symbols."""
        assert reverse_string("Test123!@#") == "#@!321tseT"
        assert reverse_string("user_name_2023") == "3202_eman_resu"