"""
Behave environment configuration for BDD tests.

This module provides setup and teardown hooks for behave test scenarios.
"""


def before_all(context):
    """
    Execute before all tests.
    
    Args:
        context: Behave context object
    """
    pass


def after_all(context):
    """
    Execute after all tests.
    
    Args:
        context: Behave context object
    """
    pass


def before_scenario(context, scenario):
    """
    Execute before each scenario.
    
    Args:
        context: Behave context object
        scenario: Current scenario being executed
    """
    # Initialize context attributes for each scenario
    context.counter = None
    context.exception = None


def after_scenario(context, scenario):
    """
    Execute after each scenario.
    
    Args:
        context: Behave context object
        scenario: Completed scenario
    """
    # Clean up context attributes
    context.counter = None
    context.exception = None