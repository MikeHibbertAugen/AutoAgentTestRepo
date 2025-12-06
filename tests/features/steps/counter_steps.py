"""
Step definitions for Counter BDD scenarios.

This module implements the step definitions for behave BDD testing of the Counter class.
"""

from behave import given, when, then
from src.counter import Counter


@given("a counter initialized with default values")
def step_given_counter_default(context):
    """Initialize a counter with default start=1 and end=10."""
    context.counter = Counter()


@given("a counter initialized with start={start:d} and end={end:d}")
def step_given_counter_custom(context, start, end):
    """Initialize a counter with custom start and end values."""
    context.counter = Counter(start=start, end=end)


@given("a counter with start={start:d} and end={end:d}")
def step_given_counter_with_values(context, start, end):
    """Initialize a counter with specified start and end values."""
    context.counter = Counter(start=start, end=end)


@when("I increment the counter")
def step_when_increment(context):
    """Increment the counter by one."""
    context.counter.increment()


@when("I increment the counter {count:d} times")
def step_when_increment_multiple(context, count):
    """Increment the counter multiple times."""
    for _ in range(count):
        context.counter.increment()


@when("I attempt to increment the counter")
def step_when_attempt_increment(context):
    """Attempt to increment the counter and catch any exceptions."""
    try:
        context.counter.increment()
        context.exception = None
    except ValueError as e:
        context.exception = e


@when("I reset the counter")
def step_when_reset(context):
    """Reset the counter to its start value."""
    context.counter.reset()


@then("the current value should be {expected:d}")
def step_then_current_value(context, expected):
    """Verify the current value of the counter."""
    assert context.counter.current == expected, (
        f"Expected current value to be {expected}, but got {context.counter.current}"
    )


@then("the counter should not have reached the end")
def step_then_not_reached_end(context):
    """Verify that the counter has not reached its end value."""
    assert not context.counter.has_reached_end(), (
        "Expected counter to not have reached the end"
    )


@then("the counter should have reached the end")
def step_then_reached_end(context):
    """Verify that the counter has reached its end value."""
    assert context.counter.has_reached_end(), (
        "Expected counter to have reached the end"
    )


@then("a ValueError should be raised")
def step_then_value_error_raised(context):
    """Verify that a ValueError was raised."""
    assert context.exception is not None, (
        "Expected a ValueError to be raised, but no exception occurred"
    )
    assert isinstance(context.exception, ValueError), (
        f"Expected ValueError, but got {type(context.exception).__name__}"
    )


@then("the counter should indicate it has reached the end")
def step_then_indicate_reached_end(context):
    """Verify that the counter indicates it has reached its end value."""
    assert context.counter.has_reached_end(), (
        "Expected counter to indicate it has reached the end"
    )