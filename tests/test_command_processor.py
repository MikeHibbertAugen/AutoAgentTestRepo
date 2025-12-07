"""
Unit tests for the command processor module.

Tests cover command normalization, parsing, validation, and case-insensitive
command processing with comprehensive whitespace handling.
"""

import pytest
from src.command_processor import (
    normalize_command,
    parse_command,
    is_valid_command,
    VALID_COMMANDS
)


class TestNormalizeCommand:
    """Test command normalization including whitespace trimming and case conversion."""

    def test_normalize_lowercase(self):
        """Test that uppercase commands are converted to lowercase."""
        assert normalize_command("NORTH") == "north"
        assert normalize_command("SOUTH") == "south"
        assert normalize_command("EAST") == "east"
        assert normalize_command("WEST") == "west"

    def test_normalize_mixed_case(self):
        """Test that mixed case commands are converted to lowercase."""
        assert normalize_command("North") == "north"
        assert normalize_command("SoUtH") == "south"
        assert normalize_command("EaSt") == "east"

    def test_trim_leading_whitespace(self):
        """Test that leading whitespace is removed."""
        assert normalize_command("  north") == "north"
        assert normalize_command("   south") == "south"
        assert normalize_command("\tnorth") == "north"

    def test_trim_trailing_whitespace(self):
        """Test that trailing whitespace is removed."""
        assert normalize_command("north  ") == "north"
        assert normalize_command("south   ") == "south"
        assert normalize_command("north\t") == "north"

    def test_trim_both_whitespace(self):
        """Test that both leading and trailing whitespace is removed."""
        assert normalize_command("  north  ") == "north"
        assert normalize_command("   south   ") == "south"
        assert normalize_command("\tnorth\t") == "north"

    def test_normalize_empty_string(self):
        """Test that empty strings are handled correctly."""
        assert normalize_command("") == ""
        assert normalize_command("   ") == ""

    def test_normalize_multi_word_command(self):
        """Test normalization of commands with multiple words."""
        assert normalize_command("  GO NORTH  ") == "go north"
        assert normalize_command("LOOK AROUND") == "look around"


class TestParseCommand:
    """Test command parsing to extract command and arguments."""

    def test_parse_single_word_command(self):
        """Test parsing commands with no arguments."""
        command, args = parse_command("north")
        assert command == "north"
        assert args == []

    def test_parse_command_with_one_argument(self):
        """Test parsing commands with a single argument."""
        command, args = parse_command("go north")
        assert command == "go"
        assert args == ["north"]

    def test_parse_command_with_multiple_arguments(self):
        """Test parsing commands with multiple arguments."""
        command, args = parse_command("take red key")
        assert command == "take"
        assert args == ["red", "key"]

    def test_parse_empty_command(self):
        """Test parsing empty strings."""
        command, args = parse_command("")
        assert command == ""
        assert args == []

    def test_parse_whitespace_only(self):
        """Test parsing strings with only whitespace."""
        command, args = parse_command("   ")
        assert command == ""
        assert args == []

    def test_parse_command_with_extra_spaces(self):
        """Test parsing commands with multiple spaces between words."""
        command, args = parse_command("go   north")
        assert command == "go"
        assert args == ["north"]

    def test_parse_preserves_normalization(self):
        """Test that parsing works with normalized input."""
        command, args = parse_command("  NORTH  ")
        assert command == "north"
        assert args == []


class TestIsValidCommand:
    """Test command validation against the command registry."""

    def test_valid_movement_commands(self):
        """Test that all movement commands are recognized as valid."""
        assert is_valid_command("north") is True
        assert is_valid_command("south") is True
        assert is_valid_command("east") is True
        assert is_valid_command("west") is True

    def test_valid_utility_commands(self):
        """Test that utility commands are recognized as valid."""
        assert is_valid_command("help") is True
        assert is_valid_command("look") is True
        assert is_valid_command("inventory") is True

    def test_invalid_commands(self):
        """Test that unrecognized commands are identified as invalid."""
        assert is_valid_command("dance") is False
        assert is_valid_command("jump") is False
        assert is_valid_command("fly") is False
        assert is_valid_command("unknown") is False

    def test_empty_command(self):
        """Test that empty commands are invalid."""
        assert is_valid_command("") is False

    def test_case_insensitive_validation(self):
        """Test that command validation is case-insensitive."""
        assert is_valid_command("NORTH") is True
        assert is_valid_command("North") is True
        assert is_valid_command("nOrTh") is True

    def test_whitespace_in_validation(self):
        """Test that validation handles whitespace correctly."""
        assert is_valid_command("  north  ") is True
        assert is_valid_command("  dance  ") is False


class TestCommandRegistry:
    """Test the command registry structure and contents."""

    def test_valid_commands_exist(self):
        """Test that the VALID_COMMANDS set is defined and non-empty."""
        assert VALID_COMMANDS is not None
        assert len(VALID_COMMANDS) > 0

    def test_movement_commands_in_registry(self):
        """Test that all cardinal directions are in the registry."""
        assert "north" in VALID_COMMANDS
        assert "south" in VALID_COMMANDS
        assert "east" in VALID_COMMANDS
        assert "west" in VALID_COMMANDS

    def test_utility_commands_in_registry(self):
        """Test that utility commands are in the registry."""
        assert "help" in VALID_COMMANDS
        assert "look" in VALID_COMMANDS
        assert "inventory" in VALID_COMMANDS

    def test_commands_are_lowercase(self):
        """Test that all commands in the registry are lowercase."""
        for command in VALID_COMMANDS:
            assert command == command.lower(), f"Command '{command}' should be lowercase"


class TestIntegrationScenarios:
    """Integration tests combining normalization, parsing, and validation."""

    def test_full_command_processing_pipeline(self):
        """Test complete command processing from raw input to validation."""
        raw_input = "  NORTH  "
        normalized = normalize_command(raw_input)
        command, args = parse_command(normalized)
        is_valid = is_valid_command(command)
        
        assert normalized == "north"
        assert command == "north"
        assert args == []
        assert is_valid is True

    def test_invalid_command_pipeline(self):
        """Test pipeline with an invalid command."""
        raw_input = "  DANCE  "
        normalized = normalize_command(raw_input)
        command, args = parse_command(normalized)
        is_valid = is_valid_command(command)
        
        assert normalized == "dance"
        assert command == "dance"
        assert args == []
        assert is_valid is False

    def test_multi_word_command_pipeline(self):
        """Test pipeline with multi-word commands."""
        raw_input = "  GO NORTH  "
        normalized = normalize_command(raw_input)
        command, args = parse_command(normalized)
        
        assert normalized == "go north"
        assert command == "go"
        assert args == ["north"]