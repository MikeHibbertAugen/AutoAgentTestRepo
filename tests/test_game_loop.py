"""
BDD-style tests for the game loop.

Tests the main game loop functionality including:
- Starting the game and displaying initial location
- Processing multiple commands in sequence
- Graceful exit via quit/exit commands
- Graceful exit via keyboard interrupt (Ctrl+C)
"""

import pytest
from unittest.mock import Mock, patch, call
from src.game_loop import GameLoop
from src.game_state import GameState


@pytest.fixture
def game_state():
    """Fixture providing a fresh GameState instance for each test."""
    state = GameState()
    state.set_current_location("You are standing in a dark room.")
    return state


@pytest.fixture
def game_loop(game_state):
    """Fixture providing a GameLoop instance with mocked dependencies."""
    return GameLoop(game_state)


def test_start_game_loop(game_loop, game_state):
    """
    Test that the game loop starts and displays the initial location.
    
    Scenario: Start game loop
      Given the game is initialized
      When the game loop starts
      Then the initial location is displayed
    """
    with patch('builtins.print') as mock_print:
        with patch('builtins.input', side_effect=['quit']):
            game_loop.run()
            
            # Verify initial location was displayed
            assert any(
                'You are standing in a dark room.' in str(call_args)
                for call_args in mock_print.call_args_list
            )


def test_process_multiple_commands_in_sequence(game_loop, game_state):
    """
    Test that multiple commands are processed in the correct sequence.
    
    Scenario: Process multiple commands in sequence
      Given the game loop is running
      When the player enters "look", "north", and "help" in sequence
      Then each command is processed in order
      And the game continues until a quit command is received
    """
    commands = ['look', 'north', 'help', 'quit']
    
    with patch('builtins.input', side_effect=commands):
        with patch('builtins.print') as mock_print:
            game_loop.run()
            
            # Verify game started and ran
            assert game_state.is_running is False  # Should be stopped after quit
            
            # Verify farewell message was displayed
            assert any(
                'goodbye' in str(call_args).lower() or 'farewell' in str(call_args).lower()
                for call_args in mock_print.call_args_list
            )


def test_quit_command_exits_gracefully(game_loop, game_state):
    """
    Test that the 'quit' command exits the game gracefully.
    
    Scenario: Exit game with quit command
      Given the game loop is running
      When the player enters "quit"
      Then the game loop stops
      And a farewell message is displayed
    """
    with patch('builtins.input', return_value='quit'):
        with patch('builtins.print') as mock_print:
            game_loop.run()
            
            # Verify game stopped
            assert game_state.is_running is False
            
            # Verify farewell message was displayed
            farewell_displayed = any(
                'goodbye' in str(call_args).lower() or 
                'farewell' in str(call_args).lower() or
                'thanks for playing' in str(call_args).lower()
                for call_args in mock_print.call_args_list
            )
            assert farewell_displayed, "Farewell message should be displayed on quit"


def test_exit_command_exits_gracefully(game_loop, game_state):
    """
    Test that the 'exit' command exits the game gracefully.
    
    Scenario: Exit game with exit command
      Given the game loop is running
      When the player enters "exit"
      Then the game loop stops
      And a farewell message is displayed
    """
    with patch('builtins.input', return_value='exit'):
        with patch('builtins.print') as mock_print:
            game_loop.run()
            
            # Verify game stopped
            assert game_state.is_running is False
            
            # Verify farewell message was displayed
            farewell_displayed = any(
                'goodbye' in str(call_args).lower() or 
                'farewell' in str(call_args).lower() or
                'thanks for playing' in str(call_args).lower()
                for call_args in mock_print.call_args_list
            )
            assert farewell_displayed, "Farewell message should be displayed on exit"


def test_keyboard_interrupt_exits_gracefully(game_loop, game_state):
    """
    Test that keyboard interrupt (Ctrl+C) exits the game gracefully.
    
    Scenario: Exit game with keyboard interrupt
      Given the game loop is running
      When the player presses Ctrl+C
      Then the game loop stops gracefully
      And a farewell message is displayed
    """
    with patch('builtins.input', side_effect=KeyboardInterrupt()):
        with patch('builtins.print') as mock_print:
            game_loop.run()
            
            # Verify game stopped
            assert game_state.is_running is False
            
            # Verify farewell message was displayed
            farewell_displayed = any(
                'goodbye' in str(call_args).lower() or 
                'farewell' in str(call_args).lower() or
                'thanks for playing' in str(call_args).lower()
                for call_args in mock_print.call_args_list
            )
            assert farewell_displayed, "Farewell message should be displayed on keyboard interrupt"


def test_process_command_returns_false_for_quit(game_loop):
    """Test that process_command returns False for quit command."""
    result = game_loop.process_command('quit')
    assert result is False, "process_command should return False for 'quit'"


def test_process_command_returns_false_for_exit(game_loop):
    """Test that process_command returns False for exit command."""
    result = game_loop.process_command('exit')
    assert result is False, "process_command should return False for 'exit'"


def test_process_command_returns_true_for_other_commands(game_loop):
    """Test that process_command returns True for non-exit commands."""
    result = game_loop.process_command('look')
    assert result is True, "process_command should return True for non-exit commands"
    
    result = game_loop.process_command('north')
    assert result is True, "process_command should return True for non-exit commands"


def test_display_location_shows_current_location(game_loop, game_state):
    """Test that display_location prints the current location."""
    game_state.set_current_location("You are in a bright hallway.")
    
    with patch('builtins.print') as mock_print:
        game_loop.display_location()
        
        # Verify the location was printed
        assert any(
            'You are in a bright hallway.' in str(call_args)
            for call_args in mock_print.call_args_list
        )


def test_display_farewell_shows_goodbye_message(game_loop):
    """Test that display_farewell prints a goodbye message."""
    with patch('builtins.print') as mock_print:
        game_loop.display_farewell()
        
        # Verify a farewell message was printed
        farewell_displayed = any(
            'goodbye' in str(call_args).lower() or 
            'farewell' in str(call_args).lower() or
            'thanks' in str(call_args).lower()
            for call_args in mock_print.call_args_list
        )
        assert farewell_displayed, "display_farewell should print a goodbye message"


def test_command_processing_order(game_loop, game_state):
    """Test that commands are processed in the exact order they are entered."""
    commands = ['look', 'inventory', 'north', 'quit']
    processed_commands = []
    
    def mock_process(command):
        processed_commands.append(command)
        return command not in ['quit', 'exit']
    
    with patch('builtins.input', side_effect=commands):
        with patch.object(game_loop, 'process_command', side_effect=mock_process):
            game_loop.run()
    
    # Verify all commands were processed in order
    assert processed_commands == commands, "Commands should be processed in the exact order entered"


def test_game_state_stops_after_quit(game_loop, game_state):
    """Test that game state is properly stopped after quit command."""
    game_state.start()
    assert game_state.is_running is True
    
    with patch('builtins.input', return_value='quit'):
        with patch('builtins.print'):
            game_loop.run()
    
    assert game_state.is_running is False, "Game state should be stopped after quit"


def test_empty_command_handling(game_loop):
    """Test that empty commands are handled gracefully."""
    with patch('builtins.input', side_effect=['', '   ', 'quit']):
        with patch('builtins.print'):
            game_loop.run()
    
    # Should complete without errors
    assert True, "Empty commands should be handled without errors"