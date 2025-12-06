#!/usr/bin/env python3
"""
Command-line interface for the counter application.

This module provides a CLI that accepts optional --start and --end parameters
to customize the counting range, with defaults of 1 to 10.
"""

import argparse
import sys
from typing import NoReturn

from counter import Counter, CounterValidationError


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the counter CLI.

    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="A simple counter application that prints numbers in a specified range.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Count from 1 to 10 (default)
  %(prog)s --start 5          # Count from 5 to 10
  %(prog)s --end 15           # Count from 1 to 15
  %(prog)s --start 3 --end 7  # Count from 3 to 7
        """
    )
    
    parser.add_argument(
        '--start',
        type=int,
        default=1,
        help='Starting number (default: 1)'
    )
    
    parser.add_argument(
        '--end',
        type=int,
        default=10,
        help='Ending number (default: 10)'
    )
    
    return parser


def main() -> int:
    """
    Main entry point for the counter CLI application.

    Parses command-line arguments, creates a Counter instance,
    and executes the counting operation.

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    parser = create_parser()
    
    try:
        args = parser.parse_args()
        
        # Create and execute counter
        counter = Counter(start=args.start, end=args.end)
        counter.execute()
        
        return 0
        
    except CounterValidationError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
        
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())