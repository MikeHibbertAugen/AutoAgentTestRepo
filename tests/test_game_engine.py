"""
Unit tests for the game engine module.

This module contains tests for the GameEngine class, including help system integration,
command processing, and game state management.
"""

import pytest
from unittest.mock import Mock, patch, call
from src.game_engine import GameEngine


@pytest.fixture
def game_engine():
    """Fixture that provides a fresh GameEngine instance for each test."""
    return GameEngine()


@pytest.fixture
def mock_output():
    """Fixture that provides a mock for output capturing."""
    with patch('builtins.print') as mock_print:
        yield mock_print


class TestGameEngineInitialization:
    """Tests for GameEngine initialization."""

    def test_game_engine_instantiation(self, game_engine):
        """Test that GameEngine can be instantiated."""
        assert game_engine is not None
        assert isinstance(game_engine, GameEngine)

    def test_game_engine_has_help_system(self, game_engine):
        """Test that GameEngine has a help system."""
        assert hasattr(game_engine, 'help_system')
        assert game_engine.help_system is not None


class TestWelcomeMessage:
    """Tests for welcome message display."""

    def test_display_welcome_shows_welcome_message(self, game_engine, mock_output):
        """Test that display_welcome shows the welcome message."""
        game_engine.display_welcome()
        
        # Verify that print was called at least once
        assert mock_output.called
        
        # Get all printed text
        printed_text = ' '.join(str(call[0][0]) for call in mock_output.call_args_list)
        
        # Verify welcome message content
        assert len(printed_text) > 0

    def test_welcome_message_contains_help_hint(self, game_engine, mock_output):
        """Test that welcome message includes a hint to type 'help'."""
        game_engine.display_welcome()
        
        # Get all printed text
        printed_text = ' '.join(str(call[0][0]) for call in mock_output.call_args_list)
        
        # Verify help hint is present
        assert 'help' in printed_text.lower()

    def test_welcome_message_called_at_game_start(self, mock_output):
        """Test that welcome message is displayed when game starts."""
        with patch.object(GameEngine, 'display_welcome') as mock_welcome:
            engine = GameEngine()
            engine.start()
            
            # Verify display_welcome was called
            mock_welcome.assert_called_once()


class TestHelpCommand:
    """Tests for help command functionality."""

    def test_help_command_displays_help_text(self, game_engine, mock_output):
        """Test that 'help' command triggers help display."""
        game_engine.process_command('help')
        
        # Verify that print was called
        assert mock_output.called
        
        # Get all printed text
        printed_text = ' '.join(str(call[0][0]) for call in mock_output.call_args_list)
        
        # Verify help content is displayed
        assert len(printed_text) > 0

    def test_help_command_shows_movement_commands(self, game_engine, mock_output):
        """Test that help command displays movement commands."""
        game_engine.process_command('help')
        
        # Get all printed text
        printed_text = ' '.join(str(call[0][0]) for call in mock_output.call_args_list)
        
        # Verify movement commands are present
        assert 'north' in printed_text.lower() or 'movement' in printed_text.lower()

    def test_help_command_shows_utility_commands(self, game_engine, mock_output):
        """Test that help command displays utility commands."""
        game_engine.process_command('help')
        
        # Get all printed text
        printed_text = ' '.join(str(call[0][0]) for call in mock_output.call_args_list)
        
        # Verify utility commands are present
        assert 'look' in printed_text.lower() or 'quit' in printed_text.lower()

    @pytest.mark.parametrize('help_command', ['help', 'HELP', 'Help'])
    def test_help_command_case_insensitive(self, game_engine, mock_output, help_command):
        """Test that help command works regardless of case."""
        game_engine.process_command(help_command)
        
        # Verify that print was called
        assert mock_output.called


class TestHelpIntegration:
    """Tests for help system integration with game engine."""

    def test_help_does_not_break_other_commands(self, game_engine, mock_output):
        """Test that help integration doesn't interfere with other commands."""
        # Process help command
        game_engine.process_command('help')
        
        # Reset mock
        mock_output.reset_mock()
        
        # Process another command (e.g., look)
        game_engine.process_command('look')
        
        # Verify that the other command still works
        assert mock_output.called

    def test_help_available_throughout_game(self, game_engine, mock_output):
        """Test that help command is available at any point in the game."""
        # Process some other commands first
        game_engine.process_command('look')
        game_engine.process_command('north')
        
        # Reset mock
        mock_output.reset_mock()
        
        # Process help command
        game_engine.process_command('help')
        
        # Verify help is displayed
        assert mock_output.called

    def test_multiple_help_calls(self, game_engine, mock_output):
        """Test that help command can be called multiple times."""
        # Call help multiple times
        game_engine.process_command('help')
        first_call_count = mock_output.call_count
        
        mock_output.reset_mock()
        
        game_engine.process_command('help')
        second_call_count = mock_output.call_count
        
        # Verify help is displayed each time
        assert first_call_count > 0
        assert second_call_count > 0


class TestGameEngineCommandProcessing:
    """Tests for general command processing in game engine."""

    def test_process_command_accepts_string(self, game_engine):
        """Test that process_command accepts string input."""
        # Should not raise an exception
        game_engine.process_command('help')
        game_engine.process_command('look')
        game_engine.process_command('quit')

    def test_process_command_handles_empty_string(self, game_engine, mock_output):
        """Test that process_command handles empty string gracefully."""
        # Should not raise an exception
        game_engine.process_command('')
        
        # Some output may occur (e.g., prompt or error message)
        # Just verify no exception is raised

    def test_process_command_handles_whitespace(self, game_engine, mock_output):
        """Test that process_command handles whitespace correctly."""
        # Should not raise an exception
        game_engine.process_command('  help  ')
        
        # Verify that print was called (help should be processed)
        assert mock_output.called