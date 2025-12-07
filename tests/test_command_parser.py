"""
BDD-style tests for command parser functionality.

Tests cover:
- Movement commands (full and abbreviated)
- Look, help, quit commands
- Invalid commands
- Empty input handling
- Case insensitivity
- Whitespace handling
"""

import pytest
from src.command_parser import CommandParser, CommandType, ParsedCommand


@pytest.fixture
def parser():
    """Fixture that provides a CommandParser instance for tests."""
    return CommandParser()


class TestMovementCommands:
    """Test suite for movement command parsing."""

    def test_go_north_parsed_as_move_command(self, parser):
        """Scenario 2: Test 'go north' parsed as MOVE command with direction 'north'."""
        result = parser.parse("go north")
        assert result.type == CommandType.MOVE
        assert result.direction == "north"
        assert result.raw_input == "go north"

    def test_go_south_parsed_as_move_command(self, parser):
        """Test 'go south' parsed as MOVE command with direction 'south'."""
        result = parser.parse("go south")
        assert result.type == CommandType.MOVE
        assert result.direction == "south"
        assert result.raw_input == "go south"

    def test_go_east_parsed_as_move_command(self, parser):
        """Test 'go east' parsed as MOVE command with direction 'east'."""
        result = parser.parse("go east")
        assert result.type == CommandType.MOVE
        assert result.direction == "east"
        assert result.raw_input == "go east"

    def test_go_west_parsed_as_move_command(self, parser):
        """Test 'go west' parsed as MOVE command with direction 'west'."""
        result = parser.parse("go west")
        assert result.type == CommandType.MOVE
        assert result.direction == "west"
        assert result.raw_input == "go west"

    def test_abbreviated_north_parsed_as_move_command(self, parser):
        """Scenario 3: Test 'n' parsed as MOVE command to north."""
        result = parser.parse("n")
        assert result.type == CommandType.MOVE
        assert result.direction == "north"
        assert result.raw_input == "n"

    def test_abbreviated_south_parsed_as_move_command(self, parser):
        """Test 's' parsed as MOVE command to south."""
        result = parser.parse("s")
        assert result.type == CommandType.MOVE
        assert result.direction == "south"
        assert result.raw_input == "s"

    def test_abbreviated_east_parsed_as_move_command(self, parser):
        """Test 'e' parsed as MOVE command to east."""
        result = parser.parse("e")
        assert result.type == CommandType.MOVE
        assert result.direction == "east"
        assert result.raw_input == "e"

    def test_abbreviated_west_parsed_as_move_command(self, parser):
        """Test 'w' parsed as MOVE command to west."""
        result = parser.parse("w")
        assert result.type == CommandType.MOVE
        assert result.direction == "west"
        assert result.raw_input == "w"

    def test_movement_command_case_insensitivity(self, parser):
        """Test movement commands work with different cases."""
        test_cases = [
            ("Go North", "north"),
            ("GO SOUTH", "south"),
            ("Go East", "east"),
            ("go WEST", "west"),
            ("N", "north"),
            ("S", "south"),
            ("E", "east"),
            ("W", "west"),
        ]
        for command, expected_direction in test_cases:
            result = parser.parse(command)
            assert result.type == CommandType.MOVE
            assert result.direction == expected_direction


class TestLookCommand:
    """Test suite for look command parsing."""

    def test_look_parsed_as_look_command(self, parser):
        """Scenario 4: Test 'look' parsed as LOOK command."""
        result = parser.parse("look")
        assert result.type == CommandType.LOOK
        assert result.direction is None
        assert result.raw_input == "look"

    def test_look_command_case_insensitivity(self, parser):
        """Test look command works with different cases."""
        test_cases = ["look", "Look", "LOOK", "LoOk"]
        for command in test_cases:
            result = parser.parse(command)
            assert result.type == CommandType.LOOK
            assert result.direction is None


class TestHelpCommand:
    """Test suite for help command parsing."""

    def test_help_parsed_as_help_command(self, parser):
        """Scenario 5: Test 'help' parsed as HELP command."""
        result = parser.parse("help")
        assert result.type == CommandType.HELP
        assert result.direction is None
        assert result.raw_input == "help"

    def test_help_command_case_insensitivity(self, parser):
        """Test help command works with different cases."""
        test_cases = ["help", "Help", "HELP", "HeLp"]
        for command in test_cases:
            result = parser.parse(command)
            assert result.type == CommandType.HELP
            assert result.direction is None


class TestQuitCommand:
    """Test suite for quit command parsing."""

    def test_quit_parsed_as_quit_command(self, parser):
        """Scenario 6: Test 'quit' parsed as QUIT command."""
        result = parser.parse("quit")
        assert result.type == CommandType.QUIT
        assert result.direction is None
        assert result.raw_input == "quit"

    def test_quit_command_case_insensitivity(self, parser):
        """Test quit command works with different cases."""
        test_cases = ["quit", "Quit", "QUIT", "QuIt"]
        for command in test_cases:
            result = parser.parse(command)
            assert result.type == CommandType.QUIT
            assert result.direction is None


class TestInvalidCommands:
    """Test suite for invalid command handling."""

    def test_jump_parsed_as_invalid_command(self, parser):
        """Scenario 7: Test 'jump' parsed as INVALID command."""
        result = parser.parse("jump")
        assert result.type == CommandType.INVALID
        assert result.direction is None
        assert result.raw_input == "jump"

    def test_unknown_command_parsed_as_invalid(self, parser):
        """Test various unknown commands are parsed as INVALID."""
        invalid_commands = [
            "dance",
            "fly",
            "swim",
            "run",
            "attack",
            "go nowhere",
            "go up",
            "move",
        ]
        for command in invalid_commands:
            result = parser.parse(command)
            assert result.type == CommandType.INVALID
            assert result.raw_input == command


class TestEmptyInputHandling:
    """Test suite for empty input handling."""

    def test_empty_string_handling(self, parser):
        """Scenario 8: Test empty string handling."""
        result = parser.parse("")
        assert result.type == CommandType.INVALID
        assert result.direction is None
        assert result.raw_input == ""

    def test_whitespace_only_string_handling(self, parser):
        """Test whitespace-only input is treated as empty."""
        whitespace_inputs = ["   ", "\t", "\n", "  \t  \n  "]
        for whitespace in whitespace_inputs:
            result = parser.parse(whitespace)
            assert result.type == CommandType.INVALID


class TestWhitespaceHandling:
    """Test suite for whitespace handling in commands."""

    def test_leading_whitespace_stripped(self, parser):
        """Test commands with leading whitespace are parsed correctly."""
        result = parser.parse("   go north")
        assert result.type == CommandType.MOVE
        assert result.direction == "north"

    def test_trailing_whitespace_stripped(self, parser):
        """Test commands with trailing whitespace are parsed correctly."""
        result = parser.parse("go south   ")
        assert result.type == CommandType.MOVE
        assert result.direction == "south"

    def test_extra_whitespace_between_words(self, parser):
        """Test commands with extra whitespace between words are parsed correctly."""
        result = parser.parse("go    east")
        assert result.type == CommandType.MOVE
        assert result.direction == "east"

    def test_whitespace_handling_for_single_word_commands(self, parser):
        """Test single word commands with whitespace are parsed correctly."""
        test_cases = [
            ("  look  ", CommandType.LOOK),
            ("  help  ", CommandType.HELP),
            ("  quit  ", CommandType.QUIT),
            ("  n  ", CommandType.MOVE),
        ]
        for command, expected_type in test_cases:
            result = parser.parse(command)
            assert result.type == expected_type