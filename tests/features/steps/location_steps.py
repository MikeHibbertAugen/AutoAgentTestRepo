"""
Step definitions for location BDD scenarios.

This module implements the step definitions for the behave BDD tests
that verify the Location class functionality.
"""

from behave import given, when, then
from src.location import Location


@given('a location named "{name}"')
def step_create_location(context, name):
    """Create a location with the given name."""
    if not hasattr(context, "locations"):
        context.locations = {}
    context.locations[name] = Location(name)


@given('a location named "{name}" with description "{description}"')
def step_create_location_with_description(context, name, description):
    """Create a location with the given name and description."""
    if not hasattr(context, "locations"):
        context.locations = {}
    context.locations[name] = Location(name, description)


@given("the following locations exist")
def step_create_multiple_locations(context):
    """Create multiple locations from a data table."""
    if not hasattr(context, "locations"):
        context.locations = {}
    for row in context.table:
        name = row["name"]
        description = row.get("description", "")
        if description:
            context.locations[name] = Location(name, description)
        else:
            context.locations[name] = Location(name)


@when('I add an exit "{direction}" from "{source}" to "{destination}"')
def step_add_exit(context, direction, source, destination):
    """Add an exit from source location to destination location."""
    source_location = context.locations[source]
    destination_location = context.locations[destination]
    source_location.add_exit(direction, destination_location)


@when('I query the available exits from "{location_name}"')
def step_query_exits(context, location_name):
    """Query available exits from the specified location."""
    location = context.locations[location_name]
    context.available_exits = location.get_available_exits()


@when('I navigate "{direction}" from "{location_name}"')
def step_navigate_direction(context, direction, location_name):
    """Navigate in the specified direction from the location."""
    location = context.locations[location_name]
    context.destination = location.get_exit(direction)


@then('the location should have name "{expected_name}"')
def step_verify_name(context, expected_name):
    """Verify the location has the expected name."""
    location = context.locations[expected_name]
    assert location.name == expected_name, f"Expected name '{expected_name}', got '{location.name}'"


@then('the location should have description "{expected_description}"')
def step_verify_description(context, expected_description):
    """Verify the location has the expected description."""
    # Get the most recently created location
    location_name = list(context.locations.keys())[-1]
    location = context.locations[location_name]
    assert location.description == expected_description, f"Expected description '{expected_description}', got '{location.description}'"


@then('the location "{location_name}" should have description "{expected_description}"')
def step_verify_location_description(context, location_name, expected_description):
    """Verify a specific location has the expected description."""
    location = context.locations[location_name]
    assert location.description == expected_description, f"Expected description '{expected_description}', got '{location.description}'"


@then("the available exits should be")
def step_verify_exits_list(context):
    """Verify the list of available exits matches the expected list."""
    expected_exits = [row["direction"] for row in context.table]
    assert sorted(context.available_exits) == sorted(expected_exits), \
        f"Expected exits {sorted(expected_exits)}, got {sorted(context.available_exits)}"


@then('I should arrive at "{expected_destination}"')
def step_verify_destination(context, expected_destination):
    """Verify that navigation leads to the expected destination."""
    expected_location = context.locations[expected_destination]
    assert context.destination == expected_location, \
        f"Expected to arrive at '{expected_destination}', but got {context.destination.name if context.destination else None}"


@then("I should not be able to navigate")
def step_verify_no_navigation(context):
    """Verify that navigation is not possible (destination is None)."""
    assert context.destination is None, \
        f"Expected navigation to fail, but arrived at {context.destination.name if context.destination else None}"