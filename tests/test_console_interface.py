"""
Tests for the console interface module.

This module contains tests for the ConsoleInterface class, which handles
console I/O operations and integrates with the command parser.
"""

import pytest
from unittest.mock import Mock, patch, call
from src.console_interface import ConsoleInterface
from src.command_parser import CommandParser, CommandType, ParsedCommand


@pytest.fixture
def parser():
    """Fixture that provides a CommandParser instance."""
    return CommandParser()


@pytest.fixture
def console(parser):
    """Fixture that provides a ConsoleInterface instance with a parser."""
    return ConsoleInterface(parser)


class TestPromptDisplay:
    """Tests for prompt display functionality."""

    def test_display_prompt_includes_location_name(self, console):
        """Test that the prompt displays the location name in brackets."""
        with patch('builtins.print') as mock_print:
            console.display_prompt("Helensville")
            mock_print.assert_called_once_with("[Helensville] > ", end="")

    def test_display_prompt_with_different_locations(self, console):
        """Test that the prompt correctly displays various location names."""
        locations = ["Town Square", "Dark Forest", "Mountain Peak"]
        
        with patch('builtins.print') as mock_print:
            for location in locations:
                console.display_prompt(location)
            
            expected_calls = [
                call("[Town Square] > ", end=""),
                call("[Dark Forest] > ", end=""),
                call("[Mountain Peak] > ", end="")
            ]
            mock_print.assert_has_calls(expected_calls)


class TestInputHandling:
    """Tests for input handling functionality."""

    def test_get_input_returns_user_input(self, console):
        """Test that get_input returns the user's input string."""
        with patch('builtins.input', return_value="go north"):
            result = console.get_input()
            assert result == "go north"

    def test_get_input_strips_whitespace(self, console):
        """Test that get_input strips leading and trailing whitespace."""
        with patch('builtins.input', return_value="  look  "):
            result = console.get_input()
            assert result == "look"


class TestErrorDisplay:
    """Tests for error message display functionality."""

    def test_display_error_shows_message(self, console):
        """Test that display_error prints the error message."""
        with patch('builtins.print') as mock_print:
            console.display_error("Unknown command")
            mock_print.assert_called_once_with("Error: Unknown command")

    def test_display_error_with_various_messages(self, console):
        """Test that display_error handles different error messages."""
        messages = ["Invalid command", "Cannot go that way", "Unknown direction"]
        
        with patch('builtins.print') as mock_print:
            for message in messages:
                console.display_error(message)
            
            expected_calls = [
                call(f"Error: {msg}") for msg in messages
            ]
            mock_print.assert_has_calls(expected_calls)


class TestCommandProcessing:
    """Tests for command processing integration."""

    def test_process_command_returns_parsed_command(self, console):
        """Test that process_command returns a ParsedCommand object."""
        result = console.process_command("go north", "Helensville")
        assert isinstance(result, ParsedCommand)
        assert result.type == CommandType.MOVE
        assert result.direction == "north"

    def test_process_command_with_look_command(self, console):
        """Test processing a look command."""
        result = console.process_command("look", "Town Square")
        assert result.type == CommandType.LOOK
        assert result.direction is None

    def test_process_command_with_help_command(self, console):
        """Test processing a help command."""
        result = console.process_command("help", "Dark Forest")
        assert result.type == CommandType.HELP
        assert result.direction is None

    def test_process_command_with_quit_command(self, console):
        """Test processing a quit command."""
        result = console.process_command("quit", "Mountain Peak")
        assert result.type == CommandType.QUIT
        assert result.direction is None

    def test_process_command_with_invalid_command(self, console):
        """Test processing an invalid command."""
        result = console.process_command("jump", "Helensville")
        assert result.type == CommandType.INVALID

    def test_process_command_with_empty_string(self, console):
        """Test that empty input is handled gracefully."""
        result = console.process_command("", "Helensville")
        assert result.type == CommandType.INVALID
        assert result.raw_input == ""

    def test_process_command_with_abbreviated_direction(self, console):
        """Test processing abbreviated direction commands."""
        result = console.process_command("n", "Helensville")
        assert result.type == CommandType.MOVE
        assert result.direction == "north"


class TestIntegration:
    """Integration tests for console interface with parser."""

    def test_console_uses_injected_parser(self):
        """Test that the console uses the parser passed via dependency injection."""
        mock_parser = Mock(spec=CommandParser)
        mock_parser.parse.return_value = ParsedCommand(
            type=CommandType.MOVE,
            direction="north",
            raw_input="go north"
        )
        
        console = ConsoleInterface(mock_parser)
        result = console.process_command("go north", "Helensville")
        
        mock_parser.parse.assert_called_once_with("go north")
        assert result.type == CommandType.MOVE
        assert result.direction == "north"

    def test_full_console_interaction_flow(self, console):
        """Test a complete console interaction flow."""
        with patch('builtins.print') as mock_print, \
             patch('builtins.input', return_value="go north"):
            
            # Display prompt
            console.display_prompt("Helensville")
            
            # Get input
            user_input = console.get_input()
            
            # Process command
            result = console.process_command(user_input, "Helensville")
            
            # Verify flow
            mock_print.assert_called_once_with("[Helensville] > ", end="")
            assert result.type == CommandType.MOVE
            assert result.direction == "north"

    def test_error_flow_with_invalid_command(self, console):
        """Test error handling flow for invalid commands."""
        with patch('builtins.print') as mock_print:
            result = console.process_command("invalid", "Helensville")
            
            if result.type == CommandType.INVALID:
                console.display_error("Unknown command")
            
            mock_print.assert_called_once_with("Error: Unknown command")