"""
BDD-style integration tests for the counter CLI application.

These tests execute the CLI script as a subprocess and validate
the behavior matches the BDD scenarios.
"""

import subprocess
import sys
from pathlib import Path


def get_cli_script_path():
    """Get the path to the counter CLI script."""
    return Path(__file__).parent.parent / "src" / "counter_cli.py"


def run_cli(*args):
    """
    Helper function to run the CLI with given arguments.
    
    Args:
        *args: Command-line arguments to pass to the CLI
        
    Returns:
        subprocess.CompletedProcess with returncode, stdout, and stderr
    """
    cli_path = get_cli_script_path()
    cmd = [sys.executable, str(cli_path)] + list(args)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    return result


def test_run_counter_default_parameters():
    """
    Scenario: Run counter with default parameters
    Given the counter CLI is available
    When I run the counter without any parameters
    Then it should display numbers from 1 to 10
    """
    result = run_cli()
    
    assert result.returncode == 0
    output_lines = result.stdout.strip().split('\n')
    
    # Verify output contains numbers 1 through 10
    assert len(output_lines) == 10
    for i in range(1, 11):
        assert str(i) in output_lines


def test_run_counter_custom_start():
    """
    Scenario: Run counter with custom start parameter
    Given the counter CLI is available
    When I run the counter with --start 5
    Then it should display numbers from 5 to 10
    """
    result = run_cli("--start", "5")
    
    assert result.returncode == 0
    output_lines = result.stdout.strip().split('\n')
    
    # Verify output contains numbers 5 through 10
    assert len(output_lines) == 6
    for i in range(5, 11):
        assert str(i) in output_lines


def test_run_counter_custom_end():
    """
    Scenario: Run counter with custom end parameter
    Given the counter CLI is available
    When I run the counter with --end 15
    Then it should display numbers from 1 to 15
    """
    result = run_cli("--end", "15")
    
    assert result.returncode == 0
    output_lines = result.stdout.strip().split('\n')
    
    # Verify output contains numbers 1 through 15
    assert len(output_lines) == 15
    for i in range(1, 16):
        assert str(i) in output_lines


def test_run_counter_custom_start_and_end():
    """
    Scenario: Run counter with both custom parameters
    Given the counter CLI is available
    When I run the counter with --start 3 and --end 7
    Then it should display numbers from 3 to 7
    """
    result = run_cli("--start", "3", "--end", "7")
    
    assert result.returncode == 0
    output_lines = result.stdout.strip().split('\n')
    
    # Verify output contains numbers 3 through 7
    assert len(output_lines) == 5
    for i in range(3, 8):
        assert str(i) in output_lines


def test_invalid_parameter_input():
    """
    Scenario: Handle invalid parameter input
    Given the counter CLI is available
    When I run the counter with --start abc
    Then it should display an error message
    And exit with a non-zero status code
    """
    result = run_cli("--start", "abc")
    
    assert result.returncode != 0
    # Error message should be present in stderr
    assert len(result.stderr) > 0


def test_display_help_information():
    """
    Scenario: Display help information
    Given the counter CLI is available
    When I run the counter with --help
    Then it should display usage information
    And describe the --start and --end parameters
    """
    result = run_cli("--help")
    
    assert result.returncode == 0
    help_output = result.stdout
    
    # Verify help contains parameter descriptions
    assert "--start" in help_output
    assert "--end" in help_output
    assert "usage:" in help_output.lower()


def test_start_greater_than_end():
    """
    Scenario: Handle invalid range where start > end
    Given the counter CLI is available
    When I run the counter with --start 10 and --end 5
    Then it should display an error message
    And exit with a non-zero status code
    """
    result = run_cli("--start", "10", "--end", "5")
    
    assert result.returncode != 0
    # Error should be communicated
    assert len(result.stderr) > 0 or "error" in result.stdout.lower()


def test_negative_numbers():
    """
    Scenario: Run counter with negative numbers
    Given the counter CLI is available
    When I run the counter with --start -5 and --end -1
    Then it should display numbers from -5 to -1
    """
    result = run_cli("--start", "-5", "--end", "-1")
    
    assert result.returncode == 0
    output_lines = result.stdout.strip().split('\n')
    
    # Verify output contains numbers -5 through -1
    assert len(output_lines) == 5
    for i in range(-5, 0):
        assert str(i) in output_lines


def test_single_number_range():
    """
    Scenario: Run counter with start equal to end
    Given the counter CLI is available
    When I run the counter with --start 5 and --end 5
    Then it should display only the number 5
    """
    result = run_cli("--start", "5", "--end", "5")
    
    assert result.returncode == 0
    output_lines = result.stdout.strip().split('\n')
    
    # Verify output contains only the number 5
    assert len(output_lines) == 1
    assert "5" in output_lines[0]